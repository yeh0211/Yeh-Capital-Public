"""Long-history gold (monthly) + French 49-industry daily returns.

Gold monthly: datahub mirror of the LBMA-style series; spliced forward with
GC=F monthly closes where the mirror lags. Industries: Ken French 49 daily
value-weighted returns, 1926-07 to present ("Guns" = defense)."""
import io
import zipfile

import pandas as pd
import requests

from config import DATA_DIR, UA

OUT = DATA_DIR / "macro"

GOLD_URL = "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv"
FF49_URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
            "49_Industry_Portfolios_Daily_CSV.zip")


def fetch_gold_monthly() -> pd.DataFrame:
    r = requests.get(GOLD_URL, headers=UA, timeout=(15, 120))
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"price": "gold"}).set_index("date")[["gold"]].sort_index()
    # splice forward with futures monthly closes if the mirror lags
    fut_path = DATA_DIR / "prices" / "idx_gold.parquet"
    if fut_path.exists():
        fut = pd.read_parquet(fut_path)["close"].resample("MS").last()
        tail = fut[fut.index > df.index.max()]
        if len(tail):
            df = pd.concat([df, tail.rename("gold").to_frame()])
    return df


def fetch_ff49() -> pd.DataFrame:
    r = requests.get(FF49_URL, headers=UA, timeout=(30, 300))
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    raw = zf.read(zf.namelist()[0]).decode("utf-8", errors="replace")
    lines = raw.splitlines()
    # first data table = Average Value Weighted Returns -- Daily
    header_i = next(i for i, l in enumerate(lines)
                    if l.startswith(",") and "Agric" in l)
    cols = ["date"] + [c.strip() for c in lines[header_i].split(",")[1:]]
    rows = []
    for l in lines[header_i + 1:]:
        first = l.split(",")[0].strip()
        if not (first.isdigit() and len(first) == 8):
            break  # end of the first table
        rows.append([p.strip() for p in l.split(",")])
    df = pd.DataFrame(rows, columns=cols)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
        df.loc[df[c] <= -0.99, c] = pd.NA  # -99.99 = missing
    return df.set_index("date").sort_index()


def main():
    g = fetch_gold_monthly()
    g.to_parquet(OUT / "gold_monthly.parquet")
    print("OK gold_monthly", g.index.min().date(), "->", g.index.max().date(), len(g), flush=True)
    ff = fetch_ff49()
    ff.to_parquet(OUT / "ff49_daily.parquet")
    print("OK ff49_daily", ff.index.min().date(), "->", ff.index.max().date(),
          f"{len(ff)} rows x {ff.shape[1]} industries", flush=True)
    print("industries:", ", ".join(list(ff.columns)[:12]), "...", flush=True)


if __name__ == "__main__":
    main()
