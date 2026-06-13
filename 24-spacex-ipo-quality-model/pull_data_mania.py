#!/usr/bin/env python3
"""Pull raw data for study 26 (SpaceX IPO vs TRUMP coin).

Sources (all public, no keys):
  - Binance spot daily klines: TRUMP launch event window + aftermath
  - FRED: NASDAQ Composite daily closes 1971-present (NASDAQCOM),
    S&P 500 daily closes last 10y (SP500) for a modern-subset cross-check

Writes CSVs into ./data/. Re-runnable; overwrites.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import sys
import time
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

BINANCE = "https://api.binance.com/api/v3/klines"
SYMBOLS = [
    "TRUMPUSDT", "MELANIAUSDT", "SOLUSDT", "BTCUSDT", "ETHUSDT",
    "DOGEUSDT", "SHIBUSDT", "PEPEUSDT", "WIFUSDT", "BONKUSDT",
]
START = int(dt.datetime(2024, 10, 1, tzinfo=dt.timezone.utc).timestamp() * 1000)
END = int(dt.datetime(2026, 6, 12, tzinfo=dt.timezone.utc).timestamp() * 1000)


def pull_binance(symbol: str) -> int:
    rows, cursor = [], START
    while cursor < END:
        r = requests.get(
            BINANCE,
            params={"symbol": symbol, "interval": "1d", "startTime": cursor,
                    "endTime": END, "limit": 1000},
            timeout=30,
        )
        if r.status_code != 200:
            print(f"  {symbol}: HTTP {r.status_code} — skipped", file=sys.stderr)
            return 0
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        cursor = batch[-1][6] + 1
        if len(batch) < 1000:
            break
        time.sleep(0.3)
    out = DATA / f"{symbol}.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume", "quote_volume", "trades"])
        for k in rows:
            d = dt.datetime.fromtimestamp(k[0] / 1000, tz=dt.timezone.utc).date()
            w.writerow([d.isoformat(), k[1], k[2], k[3], k[4], k[5], k[7], k[8]])
    return len(rows)


def pull_fred(series: str) -> int:
    r = requests.get(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
        timeout=120,
        headers={"User-Agent": "Mozilla/5.0 (research; yeh-capital-public study 26)"},
    )
    r.raise_for_status()
    text = r.text
    n = 0
    out = DATA / f"{series}.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "close"])
        for row in csv.reader(io.StringIO(text)):
            if not row or row[0] in ("DATE", "observation_date"):
                continue
            if row[1] in (".", ""):
                continue
            w.writerow([row[0], row[1]])
            n += 1
    return n


def main() -> None:
    for s in SYMBOLS:
        n = pull_binance(s)
        print(f"{s}: {n} daily bars")
    for s in ("NASDAQCOM", "SP500"):
        n = pull_fred(s)
        print(f"FRED {s}: {n} observations")


if __name__ == "__main__":
    main()
