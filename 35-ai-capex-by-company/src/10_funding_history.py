#!/usr/bin/env python3
"""
Five-year capital history per US hyperscaler, from SEC EDGAR: capex, operating
cash flow, net new debt raised (YoY change in the debt stock), equity issued,
buybacks, and cash reserves. The "how the build got funded, year by year" table.

capex/OCF come from data/capex_raw.csv; cash reserves from data/hyperscaler_cash.csv;
the debt and equity flows are pulled here. Output: data/funding_history.csv
"""
import csv
import json
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

UA = "yeh-capital-research elonyeh0211@gmail.com"
D = Path(__file__).resolve().parent.parent / "data"
TICKERS = ["AMZN", "GOOGL", "META", "MSFT", "ORCL"]

DEBT_COMBINED = ["DebtLongtermAndShorttermCombinedAmount"]
DEBT_NC = ["LongTermDebtNoncurrent", "LongTermNotesPayable", "LongTermDebtAndCapitalLeaseObligations"]
DEBT_C = ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent", "DebtCurrent"]
DEBT_ALLIN = ["LongTermDebt"]
EQ_ISS = ["ProceedsFromIssuanceOfCommonStock", "ProceedsFromStockOptionsExercised"]
BUYBACK = ["PaymentsForRepurchaseOfCommonStock"]


def _get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30))


def _d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def series(cik, tags, instant):
    best, best_max = {}, None
    for tag in tags:
        try:
            j = _get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json")
        except Exception:
            continue
        usd = j.get("units", {}).get("USD")
        if not usd:
            continue
        ser = {}
        for u in usd:
            if not str(u.get("form", "")).startswith("10-K"):
                continue
            if instant:
                if u.get("start"):
                    continue
            else:
                if not u.get("start") or not (350 <= (_d(u["end"]) - _d(u["start"])).days <= 380):
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


def total_debt(cik):
    comb = series(cik, DEBT_COMBINED, instant=True)
    if comb:
        return comb
    nc = series(cik, DEBT_NC, instant=True)
    c = series(cik, DEBT_C, instant=True)
    if nc:
        return {y: nc[y] + c.get(y, 0) for y in nc}
    return series(cik, DEBT_ALLIN, instant=True)


def load_csv_series(path, valcol):
    out = defaultdict(dict)
    for r in csv.DictReader(open(path)):
        try:
            out[r["ticker"]][int(r.get("fy") or r.get("year"))] = float(r[valcol])
        except (ValueError, TypeError, KeyError):
            pass
    return out


def main():
    cm = {r["ticker"].upper(): str(r["cik_str"]).zfill(10)
          for r in _get("https://www.sec.gov/files/company_tickers.json").values()}
    capex = load_csv_series(D / "capex_raw.csv", "capex")     # in $ (raw)
    ocf = load_csv_series(D / "capex_raw.csv", "ocf")
    cash = load_csv_series(D / "hyperscaler_cash.csv", "cash_reserves_usd_bn")  # already $bn

    rows = []
    for tkr in TICKERS:
        cik = cm[tkr]
        debt = total_debt(cik)
        eq = series(cik, EQ_ISS, instant=False)
        bb = series(cik, BUYBACK, instant=False)
        yrs = sorted(y for y in set(capex[tkr]) | set(debt) if 2021 <= y <= 2026)
        for y in yrs:
            nd = (debt.get(y, 0) - debt.get(y - 1)) / 1e9 if (y in debt and y - 1 in debt) else None
            rows.append({
                "ticker": tkr, "year": y,
                "capex_bn": round(capex[tkr].get(y, 0) / 1e9, 1) if y in capex[tkr] else None,
                "ocf_bn": round(ocf[tkr].get(y, 0) / 1e9, 1) if y in ocf[tkr] else None,
                "net_debt_raised_bn": round(nd, 1) if nd is not None else None,
                "equity_issued_bn": round(eq.get(y, 0) / 1e9, 1) if y in eq else None,
                "buyback_bn": round(bb.get(y, 0) / 1e9, 1) if y in bb else None,
                "cash_reserves_bn": cash.get(tkr, {}).get(y),
            })
        print(f"\n{tkr}")
        for r in rows[-len(yrs):]:
            print(f"  FY{r['year']}: capex {r['capex_bn']}  OCF {r['ocf_bn']}  "
                  f"netdebt {r['net_debt_raised_bn']}  eq {r['equity_issued_bn']}  "
                  f"buyback {r['buyback_bn']}  cash {r['cash_reserves_bn']}")
    with open(D / "funding_history.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "year", "capex_bn", "ocf_bn",
                                          "net_debt_raised_bn", "equity_issued_bn",
                                          "buyback_bn", "cash_reserves_bn"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {D/'funding_history.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
