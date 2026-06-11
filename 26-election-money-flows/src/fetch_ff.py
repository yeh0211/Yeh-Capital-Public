"""Ken French daily factors: total market return (incl. dividends) + T-bill
rate, 1926-07 to present. Basis for cross-era president comparison: price-only
SPX understates older administrations (pre-1960 dividend yields ran 4-5%/yr).

Source: F-F Research Data Factors daily CSV zip (verified reachable)."""
import io
import zipfile

import pandas as pd
import requests

from config import DATA_DIR, UA

OUT = DATA_DIR / "macro"
OUT.mkdir(parents=True, exist_ok=True)

URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
       "F-F_Research_Data_Factors_daily_CSV.zip")


def fetch() -> pd.DataFrame:
    r = requests.get(URL, headers=UA, timeout=(15, 180))
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    raw = zf.read(zf.namelist()[0]).decode("utf-8", errors="replace")
    lines = raw.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("Mkt-RF") or
                 (l.split(",")[0].strip().isdigit() and len(l.split(",")[0].strip()) == 8))
    if lines[start].strip().startswith("Mkt-RF"):
        header, start = lines[start], start + 1
    rows = []
    for l in lines[start:]:
        parts = [p.strip() for p in l.split(",")]
        if len(parts) < 5 or not (parts[0].isdigit() and len(parts[0]) == 8):
            continue
        rows.append(parts[:5])
    df = pd.DataFrame(rows, columns=["date", "mkt_rf", "smb", "hml", "rf"])
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    for c in ("mkt_rf", "smb", "hml", "rf"):
        df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0  # percent -> decimal daily
    df = df.dropna(subset=["mkt_rf", "rf"]).set_index("date").sort_index()
    df["mkt_tr"] = df["mkt_rf"] + df["rf"]  # total market return incl. dividends
    return df


def main():
    df = fetch()
    df.to_parquet(OUT / "ff_factors_daily.parquet")
    print("OK ff_factors_daily", df.index.min().date(), "->", df.index.max().date(), len(df), flush=True)


if __name__ == "__main__":
    main()
