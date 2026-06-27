#!/usr/bin/env python3
"""
Merge the capex table with the funding pull into one funding-decomposition table,
and answer: how is each company paying for its build, and is the debt a choice or
a necessity?

Key derived fields:
  funding_gap   = capex - operating cash flow  (>0 = the build needs outside money)
  runway_years  = liquidity / capex            (years of capex sitting in cash)
  debt_cover    = net_borrow / capex           (share of the build funded by new debt)
  returning     = net_return_to_holders > 0    (buying back stock WHILE building)
  funding_class : self-funded+returning / self-funded / debt-funded / raising
"""
import csv
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"


def load(name):
    return {r["ticker"]: r for r in csv.DictReader(open(D / name))}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    cap = load("capex_table.csv")
    fund = load("funding_raw.csv")
    out = []
    for t, c in cap.items():
        fr = fund.get(t, {})
        capex = f(c["capex_bn"])
        ocf = f(c["ocf_bn"])
        fcf = f(c["fcf_bn"])
        liq = f(fr.get("liquidity"))
        cash = f(fr.get("cash"))
        debt = f(fr.get("total_debt"))
        nb = f(fr.get("net_borrow"))
        nr = f(fr.get("net_return_to_holders"))
        gap = (capex - ocf) if (capex is not None and ocf is not None) else None
        runway = (liq / capex) if (liq is not None and capex) else None
        debt_cover = (nb / capex) if (nb is not None and capex) else None

        # classify how the build is funded. Order matters: a positive-FCF company
        # that still returns cash is the strongest; among the cash-negative names the
        # DOMINANT external source (debt vs equity) wins, so a name borrowing $37bn
        # while issuing $1bn of comp stock reads as debt-funded, not equity-raising.
        nbv, nrv = (nb or 0), (nr or 0)
        if fcf is not None and fcf > 0 and nrv > 0.2:
            cls = "self-funded + returning cash"
        elif fcf is not None and fcf > 0:
            cls = "self-funded, building"
        elif nbv > 0.5 and nbv >= abs(nrv):
            cls = "debt-funded"
        elif nrv < -0.5:
            cls = "raising equity"
        else:
            cls = "mixed / small"

        out.append({
            "ticker": t, "layer": c["layer"],
            "capex_bn": capex, "ocf_bn": ocf, "fcf_bn": fcf,
            "cash_bn": cash, "liquidity_bn": liq, "runway_years": round(runway, 2) if runway else None,
            "total_debt_bn": debt, "net_borrow_bn": nb,
            "debt_cover_pct": round(debt_cover * 100, 1) if debt_cover is not None else None,
            "net_return_bn": nr, "funding_class": cls,
        })

    out.sort(key=lambda r: (r["capex_bn"] or 0), reverse=True)
    fields = list(out[0].keys())
    with open(D / "funding_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    # ---- summary stats for the writeup ----
    big = [r for r in out if (r["capex_bn"] or 0) >= 2]
    print(f"=== {len(out)} companies; {len(big)} spend >=$2bn ===\n")
    print(f"{'ticker':6} {'capex':>7} {'fcf':>7} {'liq':>7} {'runway':>6} "
          f"{'netborrow':>9} {'netreturn':>9}  class")
    for r in big:
        print(f"{r['ticker']:6} {r['capex_bn']:>7.1f} {(r['fcf_bn'] or 0):>7.1f} "
              f"{(r['liquidity_bn'] or 0):>7.1f} {(r['runway_years'] or 0):>6.1f} "
              f"{(r['net_borrow_bn'] or 0):>9.1f} {(r['net_return_bn'] or 0):>9.1f}  {r['funding_class']}")

    # aggregate funding of the build
    tot_capex = sum(r["capex_bn"] for r in out if r["capex_bn"])
    tot_ocf = sum(r["ocf_bn"] for r in out if r["ocf_bn"])
    tot_nb = sum(r["net_borrow_bn"] for r in out if r["net_borrow_bn"])
    tot_ret = sum(r["net_return_bn"] for r in out if r["net_return_bn"])
    hyp = [r for r in out if r["layer"] == "Hyperscaler"]
    print(f"\nAll 45: capex ${tot_capex:.0f}bn  OCF ${tot_ocf:.0f}bn  "
          f"net new debt ${tot_nb:.0f}bn  net returned to holders ${tot_ret:.0f}bn")
    print("Aggregate FCF (OCF-capex): ${:.0f}bn".format(tot_ocf - tot_capex))
    print("\nHyperscaler funding:")
    for r in hyp:
        print(f"  {r['ticker']:6} netborrow {r['net_borrow_bn']:+.1f}  "
              f"netreturn {(r['net_return_bn'] or 0):+.1f}  fcf {r['fcf_bn']:+.1f}  {r['funding_class']}")
    print("\nBy funding class:")
    from collections import Counter
    cc = Counter(r["funding_class"] for r in out)
    for k, v in cc.most_common():
        print(f"  {v:2} {k}")


if __name__ == "__main__":
    main()
