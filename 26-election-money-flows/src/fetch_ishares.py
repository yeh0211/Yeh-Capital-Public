"""Daily NAV + shares-outstanding history for the iShares panel.

Source: the product-page "Data Download" endpoint discovered 2026-06-11:
  https://www.blackrock.com/varnish-api/blk-one01-product-data/product-data/api/v1/
      get-fund-document?component=fundDownload&portfolioId=<id>&...
Returns Excel-2003 SpreadsheetML with a "Historical" sheet:
  As Of | NAV per Share | Ex-Dividends | Shares Outstanding | Non-FV NAV
covering inception -> present, daily. Flow_usd = diff(shares) * NAV.

Ticker -> portfolioId comes from the product screener JSON.
Raw XLS files are cached in data/ishares_raw/ so reruns don't rehit the API.
"""
import json
import re
import sys
import time
import xml.etree.ElementTree as ET

import pandas as pd
import requests

from config import DATA_DIR, ISHARES_SCREENER, PANEL_TICKERS, UA

RAW = DATA_DIR / "ishares_raw"
OUT = DATA_DIR / "ishares"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

DOC_URL = (
    "https://www.blackrock.com/varnish-api/blk-one01-product-data/product-data/"
    "api/v1/get-fund-document?appType=PRODUCT_PAGE&appSubType=ISHARES"
    "&targetSite=us-ishares&locale=en_US&userType=individual"
    "&component=fundDownload&portfolioId={pid}"
)
NS = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}


def screener_map() -> dict[str, str]:
    """ticker -> portfolioId for the US iShares range."""
    cache = RAW / "screener.json"
    if cache.exists():
        data = json.loads(cache.read_text())
    else:
        r = requests.get(ISHARES_SCREENER, headers=UA, timeout=60)
        r.raise_for_status()
        data = r.json()
        cache.write_text(json.dumps(data))
    out = {}
    for pid, v in data.items():
        t = v.get("localExchangeTicker")
        if t:
            out[t] = str(pid)
    return out


def download_fund_xls(pid: str, ticker: str) -> str:
    path = RAW / f"{ticker}.xls"
    if path.exists() and path.stat().st_size > 100_000:
        return path.read_text(encoding="utf-8", errors="replace")
    r = requests.get(DOC_URL.format(pid=pid), headers=UA, timeout=(15, 120))
    r.raise_for_status()
    if b"Workbook" not in r.content[:2000]:
        raise RuntimeError(f"{ticker}: response is not SpreadsheetML ({r.content[:80]!r})")
    path.write_bytes(r.content)
    return r.content.decode("utf-8", errors="replace")


def parse_historical(raw: str, ticker: str) -> pd.DataFrame:
    raw = re.sub(r"&(?!(amp|lt|gt|quot|apos|#)\b)", "&amp;", raw)
    root = ET.fromstring(raw)
    hist = None
    for ws in root.findall("ss:Worksheet", NS):
        if ws.get("{urn:schemas-microsoft-com:office:spreadsheet}Name") == "Historical":
            hist = ws
            break
    if hist is None:
        raise RuntimeError(f"{ticker}: no Historical sheet")
    rows = hist.findall(".//ss:Row", NS)
    def cells(r):
        return [(c.find("ss:Data", NS).text if c.find("ss:Data", NS) is not None else None)
                for c in r.findall("ss:Cell", NS)]
    header = cells(rows[0])
    recs = [cells(r) for r in rows[1:]]
    df = pd.DataFrame(recs, columns=header)
    df = df.rename(columns={
        "As Of": "date", "NAV per Share": "nav",
        "Shares Outstanding": "shares", "Ex-Dividends": "exdiv",
    })
    df["date"] = pd.to_datetime(df["date"], format="%b %d, %Y", errors="coerce")
    for c in ("nav", "shares"):
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "").replace("--", None), errors="coerce")
    df = df.dropna(subset=["date", "nav", "shares"]).set_index("date").sort_index()
    return df[["nav", "shares"]]


def main(tickers=None):
    tickers = tickers or PANEL_TICKERS
    smap = screener_map()
    ok, fail = [], []
    for t in tickers:
        try:
            pid = smap[t]
            raw = download_fund_xls(pid, t)
            df = parse_historical(raw, t)
            df.to_parquet(OUT / f"{t}.parquet")
            ok.append((t, str(df.index.min().date()), str(df.index.max().date()), len(df)))
        except Exception as e:  # noqa: BLE001 - report all, fail at end
            fail.append((t, repr(e)[:140]))
        time.sleep(1.5)
    for row in ok:
        print("OK  ", *row, flush=True)
    for row in fail:
        print("FAIL", *row, flush=True)
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
