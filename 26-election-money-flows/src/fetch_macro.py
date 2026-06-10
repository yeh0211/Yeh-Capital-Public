"""Macro/uncertainty series with per-source fallbacks.

Working sources verified 2026-06-11: CBOE (VIX full history), policyuncertainty.com
(daily EPU), matteoiacoviello.com (GPR monthly 1900- and daily recent).
FRED is unreachable from this network at build time; fetch_fred() stays in the
module so the series (FX, yields, MMF assets) can be topped up when it returns.
"""
import io
import sys
import time

import pandas as pd
import requests

from config import DATA_DIR, FRED_SERIES, UA

OUT = DATA_DIR / "macro"
OUT.mkdir(parents=True, exist_ok=True)


def fetch_cboe_vix() -> pd.DataFrame:
    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
    r = requests.get(url, headers=UA, timeout=(15, 60))
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")[["close"]].rename(columns={"close": "vix"}).sort_index()


def fetch_epu() -> pd.DataFrame:
    url = "https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv"
    r = requests.get(url, headers=UA, timeout=(15, 120))
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.dropna(subset=["year", "month", "day"])
    df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=df["day"]))
    val_cols = [c for c in df.columns if c not in ("year", "month", "day", "date")]
    out = df.set_index("date")[val_cols].sort_index()
    out.columns = [f"epu_{c}"[:40] for c in out.columns]
    return out


def fetch_gpr() -> dict:
    candidates = {
        "gpr_daily": [
            "https://www.matteoiacoviello.com/gpr_files/gpr_daily_recent.xls",
            "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls",
            "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xlsx",
        ],
        "gpr_monthly": [
            "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls",
            "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xlsx",
        ],
    }
    got = {}
    for name, urls in candidates.items():
        for url in urls:
            try:
                r = requests.get(url, headers=UA, timeout=(15, 120))
                if r.status_code != 200 or len(r.content) < 1000:
                    continue
                df = pd.read_excel(io.BytesIO(r.content))
                got[name] = (url, df)
                break
            except Exception:  # noqa: BLE001
                continue
    return got


def parse_gpr_dates(df: pd.DataFrame, date_col) -> pd.Series:
    """GPR files store dates as yyyymmdd ints (daily) or datetimes (monthly)."""
    col = df[date_col]
    if pd.api.types.is_numeric_dtype(col) and col.dropna().between(19000101, 21001231).all():
        return pd.to_datetime(col.astype("Int64").astype(str), format="%Y%m%d", errors="coerce")
    return pd.to_datetime(col, errors="coerce")


def fetch_fred(series: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    r = requests.get(url, headers=UA, timeout=(10, 30))
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    date_col = df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.rename(columns={date_col: "date", df.columns[1]: series.lower()})
    df[series.lower()] = pd.to_numeric(df[series.lower()], errors="coerce")
    return df.set_index("date").sort_index()


def main():
    ok, fail = [], []

    try:
        vix = fetch_cboe_vix()
        vix.to_parquet(OUT / "vix_cboe.parquet")
        ok.append(("vix_cboe", str(vix.index.min().date()), str(vix.index.max().date()), len(vix)))
    except Exception as e:  # noqa: BLE001
        fail.append(("vix_cboe", repr(e)[:120]))

    try:
        epu = fetch_epu()
        epu.to_parquet(OUT / "epu_daily.parquet")
        ok.append(("epu_daily", str(epu.index.min().date()), str(epu.index.max().date()), len(epu)))
    except Exception as e:  # noqa: BLE001
        fail.append(("epu_daily", repr(e)[:120]))

    got = fetch_gpr()
    for name, (url, df) in got.items():
        date_col = None
        for c in df.columns:
            if str(c).strip().lower() in ("date", "day", "month", "yearmonth"):
                date_col = c
                break
        if date_col is None:
            date_col = df.columns[0]
        df[date_col] = parse_gpr_dates(df, date_col)
        df = df.dropna(subset=[date_col]).set_index(date_col).sort_index()
        df.to_parquet(OUT / f"{name}.parquet")
        ok.append((name, str(df.index.min().date()), str(df.index.max().date()), f"{len(df)} via {url.rsplit('/',1)[-1]}"))
    for name in ("gpr_daily", "gpr_monthly"):
        if name not in got:
            fail.append((name, "no candidate URL worked"))

    # FRED best-effort (FX, yields, money market funds) - currently unreachable
    fred_ok = 0
    for series in FRED_SERIES:
        try:
            df = fetch_fred(series)
            df.to_parquet(OUT / f"fred_{series.lower()}.parquet")
            fred_ok += 1
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.3)
    print(f"FRED series fetched: {fred_ok}/{len(FRED_SERIES)}", flush=True)

    for row in ok:
        print("OK  ", *row, flush=True)
    for row in fail:
        print("FAIL", *row, flush=True)
    if any(n in ("vix_cboe", "epu_daily", "gpr_monthly") for n, _ in fail):
        sys.exit(1)


if __name__ == "__main__":
    main()
