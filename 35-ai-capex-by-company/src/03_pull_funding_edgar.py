#!/usr/bin/env python3
"""
Pull the FUNDING side of the AI build from SEC EDGAR, to sit alongside the capex
table: how is each company paying for what it's building?

For the same 45-name universe we add, from the audited balance sheet and the
financing section of the cash-flow statement (latest full fiscal year):
  - cash        : cash & equivalents (instant, balance sheet)
  - liquidity   : cash + short-term investments / current marketable securities
  - total_debt  : long-term debt incl. current portion (the leverage stock)
  - debt_issued : proceeds from new debt raised this year   (financing inflow)
  - debt_repaid : repayments of debt this year              (financing outflow)
  - net_debt    : debt_issued - debt_repaid                 (net new borrowing)
  - equity_iss  : proceeds from issuing stock (IPOs, raises)
  - buyback     : cash spent buying back stock
  - net_equity  : equity_iss - buyback   (negative = net return of cash)

Tags vary by issuer far more here than for capex, so each concept has a fallback
list and we pick the tag reaching the latest period end-date (freshness), tie-
broken by list order. Anything that won't resolve cleanly is left blank, never
guessed. Output: data/funding_raw.csv (latest FY per company).
"""
import csv
import json
import time
import urllib.request
from datetime import date
from pathlib import Path

UA = "yeh-capital-research elonyeh0211@gmail.com"
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

# reuse the universe + cik map from the capex puller
import importlib.util
spec = importlib.util.spec_from_file_location("cap", ROOT / "src" / "pull_capex_edgar.py")
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)

FLOW = {
    "debt_issued": ["ProceedsFromIssuanceOfLongTermDebt", "ProceedsFromIssuanceOfSeniorLongTermDebt",
                    "ProceedsFromDebtNetOfIssuanceCosts", "ProceedsFromIssuanceOfDebt",
                    "ProceedsFromConvertibleDebt", "ProceedsFromDebtMaturingInMoreThanThreeMonths"],
    "debt_repaid": ["RepaymentsOfLongTermDebt", "RepaymentsOfSeniorDebt", "RepaymentsOfDebt",
                    "RepaymentsOfDebtMaturingInMoreThanThreeMonths"],
    "equity_iss": ["ProceedsFromIssuanceOfCommonStock", "ProceedsFromIssuanceInitialPublicOffering",
                   "ProceedsFromIssuanceOfCommonStockNetOfIssuanceCosts"],
    "buyback": ["PaymentsForRepurchaseOfCommonStock",
                "PaymentsForRepurchaseOfCommonStockAndConvertibleDebt"],
}
INST = {
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "sti": ["ShortTermInvestments", "MarketableSecuritiesCurrent",
            "AvailableForSaleSecuritiesCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
}
# total debt: prefer the all-in combined tag; else noncurrent+current; else LongTermDebt
DEBT_COMBINED = ["DebtLongtermAndShorttermCombinedAmount"]   # ORCL and others report this cleanly
DEBT_NC = ["LongTermDebtNoncurrent", "LongTermNotesPayable", "LongTermDebtAndCapitalLeaseObligations",
           "SeniorNotesNoncurrent", "SeniorNotes", "ConvertibleNotesPayableNoncurrent"]
DEBT_C = ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent", "DebtCurrent", "SeniorNotesCurrent"]
DEBT_ALLIN = ["LongTermDebt"]


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def series(cik, tags, instant):
    """(end_year -> (end_date,val)) for the fallback tag reaching the latest end."""
    chosen, chosen_max = {}, None
    for tag in tags:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
        try:
            d = _get(url)
        except Exception:
            continue
        units = d.get("units", {}).get("USD")
        if not units:
            continue
        ser = {}
        for u in units:
            if not str(u.get("form", "")).startswith(("10-K", "20-F")):
                continue
            start, end = u.get("start"), u.get("end")
            if not end:
                continue
            if instant:
                if start:            # instants have no start
                    continue
            else:
                if not start:
                    continue
                if not (350 <= (_d(end) - _d(start)).days <= 380):
                    continue
            yr, filed = int(end[:4]), u.get("filed", "")
            if yr not in ser or (filed, end) > (ser[yr][0], ser[yr][1]):
                ser[yr] = (filed, end, u["val"])
        if not ser:
            continue
        max_end = max(v[1] for v in ser.values())
        # freshness wins; tie -> earlier in preference list (already iterating in order)
        if chosen_max is None or max_end > chosen_max:
            chosen, chosen_max = {y: (v[1], v[2]) for y, v in ser.items()}, max_end
    return chosen


def latest(ser, ref_year=None):
    if not ser:
        return None
    yr = ref_year if (ref_year in ser) else max(ser)
    return ser[yr][1]


def total_debt_series(cik):
    """{end_year: total_debt}: prefer the all-in combined tag, else noncurrent+current,
    else all-in LongTermDebt."""
    comb = series(cik, DEBT_COMBINED, instant=True)
    if comb:
        return {y: comb[y][1] for y in comb}
    nc = series(cik, DEBT_NC, instant=True)
    c = series(cik, DEBT_C, instant=True)
    if nc:
        return {y: (nc[y][1] + (c[y][1] if y in c else 0)) for y in nc}
    allin = series(cik, DEBT_ALLIN, instant=True)
    if allin:
        return {y: allin[y][1] for y in allin}
    return {}


def two_years(ser, ref_year):
    """(latest_value, prior_value) from a {year:(end,val)} or {year:val} series,
    anchored on ref_year if present."""
    if not ser:
        return None, None
    norm = {y: (v[1] if isinstance(v, tuple) else v) for y, v in ser.items()}
    yrs = sorted(norm)
    cur = ref_year if ref_year in norm else yrs[-1]
    idx = yrs.index(cur)
    prior = yrs[idx - 1] if idx > 0 else None
    return norm[cur], (norm[prior] if prior is not None else None)


def main():
    cm = cap.cik_map()
    rows = []
    for tkr, layer in cap.UNIVERSE:
        cik = cm.get(tkr)
        if not cik:
            continue
        # reference fiscal year = the capex puller's latest capex year (align periods);
        # skip names with no capex tag (excluded from the study, e.g. NEE)
        _, capser = cap.annual_series(cik, cap.CAPEX_TAGS)
        if not capser:
            print(f"  {tkr:6s} no capex -> excluded from funding table too")
            continue
        ref = max(capser)

        cash, cash_p = two_years(series(cik, INST["cash"], instant=True), ref)
        sti, _ = two_years(series(cik, INST["sti"], instant=True), ref)
        liq = (cash or 0) + (sti or 0) if cash is not None else None
        debt, debt_p = two_years(total_debt_series(cik), ref)
        # net new borrowing = YoY change in the debt stock (immune to commercial-
        # paper gross-flow inflation that contaminates the issuance/repayment tags)
        net_borrow = (debt - debt_p) if (debt is not None and debt_p is not None) else None
        # raw flows kept for transparency, NOT headlined
        di = latest(series(cik, FLOW["debt_issued"], instant=False), ref)
        dr = latest(series(cik, FLOW["debt_repaid"], instant=False), ref)
        ei = latest(series(cik, FLOW["equity_iss"], instant=False), ref)
        bb = latest(series(cik, FLOW["buyback"], instant=False), ref)
        # net cash returned to holders = buybacks - new equity (positive = returning)
        net_return = ((bb or 0) - (ei or 0)) if (ei is not None or bb is not None) else None

        rows.append({
            "ticker": tkr, "layer": layer, "fy": ref,
            "cash": cash, "liquidity": liq,
            "total_debt": debt, "total_debt_prior": debt_p, "net_borrow": net_borrow,
            "debt_issued_gross": di, "debt_repaid_gross": dr,
            "equity_iss": ei, "buyback": bb, "net_return_to_holders": net_return,
        })
        print(f"  {tkr:6s} cash={_b(cash)} liq={_b(liq)} debt={_b(debt)} "
              f"netborrow={_b(net_borrow)} netreturn={_b(net_return)}")
        time.sleep(0.08)

    fields = ["ticker", "layer", "fy", "cash", "liquidity", "total_debt",
              "total_debt_prior", "net_borrow", "debt_issued_gross",
              "debt_repaid_gross", "equity_iss", "buyback", "net_return_to_holders"]
    with open(D / "funding_raw.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(r[k] / 1e9, 2) if isinstance(r.get(k), (int, float)) and k != "fy"
                            else r.get(k)) for k in fields})
    print(f"\nwrote {D/'funding_raw.csv'} ({len(rows)} rows)")


def _b(v):
    return f"{v/1e9:7.1f}" if isinstance(v, (int, float)) else "    n/a"


if __name__ == "__main__":
    main()
