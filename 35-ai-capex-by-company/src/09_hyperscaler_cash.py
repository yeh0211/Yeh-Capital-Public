#!/usr/bin/env python3
"""
Multi-year cash reserves (cash + short-term investments) for the hyperscalers,
from SEC EDGAR. US names + the two China names that file with the SEC (Alibaba,
Baidu). Tencent / ByteDance history comes from the china-hyperscaler workflow.
Output: data/hyperscaler_cash.csv  (ticker, year, cash_reserves_usd_bn)
"""
import csv
import json
import urllib.request
from datetime import date
from pathlib import Path

UA = "yeh-capital-research elonyeh0211@gmail.com"
D = Path(__file__).resolve().parent.parent / "data"

TICKERS = ["AMZN", "GOOGL", "META", "MSFT", "ORCL", "BABA", "BIDU"]
CASH = ["CashAndCashEquivalentsAtCarryingValue"]
STI = ["ShortTermInvestments", "MarketableSecuritiesCurrent",
       "AvailableForSaleSecuritiesCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"]


def _get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30))


def _d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def instant_usd(cik, tags):
    """{year: value_usd} for the tag (in USD unit) reaching the latest year."""
    best, best_max = {}, None
    for ns in ("us-gaap", "ifrs-full"):
        for tag in tags:
            try:
                j = _get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{ns}/{tag}.json")
            except Exception:
                continue
            usd = j.get("units", {}).get("USD")
            if not usd:
                continue
            ser = {}
            for u in usd:
                if u.get("start") or not str(u.get("form", "")).startswith(("10-K", "20-F")):
                    continue
                yr, filed = int(u["end"][:4]), u.get("filed", "")
                if yr not in ser or (filed, u["end"]) > ser[yr][0]:
                    ser[yr] = ((filed, u["end"]), u["val"])
            if not ser:
                continue
            mx = max(ser)
            if best_max is None or mx > best_max:
                best, best_max = {y: v[1] for y, v in ser.items()}, mx
    return best


def main():
    cm = {r["ticker"].upper(): str(r["cik_str"]).zfill(10)
          for r in _get("https://www.sec.gov/files/company_tickers.json").values()}
    rows = []
    for tkr in TICKERS:
        cik = cm.get(tkr)
        if not cik:
            continue
        cash = instant_usd(cik, CASH)
        sti = instant_usd(cik, STI)
        yrs = sorted(set(cash) | set(sti))
        for y in yrs:
            res = (cash.get(y, 0) + sti.get(y, 0))
            rows.append({"ticker": tkr, "year": y, "cash_reserves_usd_bn": round(res / 1e9, 1)})
        recent = [y for y in yrs if y >= 2021]
        print(f"{tkr:6s} " + " ".join(f"{y}:{(cash.get(y,0)+sti.get(y,0))/1e9:.0f}" for y in recent))
    with open(D / "hyperscaler_cash.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "year", "cash_reserves_usd_bn"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {D/'hyperscaler_cash.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
