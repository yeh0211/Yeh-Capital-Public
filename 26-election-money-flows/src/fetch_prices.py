"""Daily close history for the ETF panel + indices via Yahoo Finance (full depth).

Stooq serves 404s from this network; Yahoo verified working (EEM back to 2003,
^GSPC back to 1927). auto_adjust=False keeps raw closes; we use Close for
returns (dividends ignored — fine for direction/rotation at our horizons,
and the iShares NAV series provides the clean per-fund levels anyway).
"""
import sys
import time

import pandas as pd
import yfinance as yf

from config import DATA_DIR, PANEL_TICKERS

OUT = DATA_DIR / "prices"
OUT.mkdir(parents=True, exist_ok=True)

INDICES = {"idx_spx": "^GSPC", "idx_vix": "^VIX", "idx_dxy": "DX-Y.NYB", "idx_tnx": "^TNX",
           "idx_oil": "CL=F", "idx_gold": "GC=F"}


def fetch_one(symbol: str) -> pd.DataFrame:
    t = yf.Ticker(symbol)
    df = t.history(period="max", auto_adjust=False)
    if df is None or df.empty:
        raise RuntimeError(f"yahoo empty for {symbol}")
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.index.name = "date"
    return df.sort_index()


def main():
    symbols = {t: t for t in PANEL_TICKERS}
    symbols.update(INDICES)
    ok, fail = [], []
    for name, sym in symbols.items():
        try:
            df = fetch_one(sym)
            df.to_parquet(OUT / f"{name}.parquet")
            ok.append((name, str(df.index.min().date()), str(df.index.max().date()), len(df)))
        except Exception as e:  # noqa: BLE001
            fail.append((name, repr(e)[:120]))
        time.sleep(0.8)
    for row in ok:
        print("OK  ", *row, flush=True)
    for row in fail:
        print("FAIL", *row, flush=True)
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
