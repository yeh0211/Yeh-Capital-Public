#!/usr/bin/env python3
"""
Build the publishable capex-by-company table from data/capex_raw.csv.

For each company we take the latest reported fiscal year and the prior one, then
compute the three lenses that matter for the AI capital cycle:
  - magnitude      : capex ($bn) and its YoY growth
  - intensity      : capex / revenue  (how capex-heavy the business model is)
  - self-funding   : capex / operating cash flow  (>100% = build outruns the cash
                     it throws off, i.e. funded by balance sheet / debt / equity)
  - free cash flow : operating cash flow - capex  (negative = burning to build)

Outputs:
  data/capex_table.csv   one row per company, sorted by capex desc
  data/layer_rollup.csv  capex summed by value-chain layer
  prints concentration stats used in the writeup.
"""
import csv
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"


def load():
    rows = []
    with open(D / "capex_raw.csv") as f:
        for r in csv.DictReader(f):
            for k in ("capex", "revenue", "ocf"):
                r[k] = float(r[k]) if r[k] not in ("", None) else None
            r["fy"] = int(r["fy"]) if r["fy"] else None
            rows.append(r)
    return rows


def main():
    rows = load()
    by_tkr = defaultdict(list)
    for r in rows:
        if r["fy"]:
            by_tkr[r["ticker"]].append(r)

    table, excluded = [], []
    for tkr, rs in by_tkr.items():
        rs = sorted(rs, key=lambda r: r["fy"])
        with_cap = [r for r in rs if r["capex"] is not None]
        if not with_cap:
            excluded.append((tkr, rs[0]["layer"], "no us-gaap capex tag"))
            continue
        cur = with_cap[-1]
        prior = with_cap[-2] if len(with_cap) > 1 else None
        capex = cur["capex"]
        rev = cur["revenue"]
        ocf = cur["ocf"]
        yoy = ((capex / prior["capex"] - 1) if prior and prior["capex"] else None)
        table.append({
            "ticker": tkr,
            "layer": cur["layer"],
            "fy_end": cur["fy_end"],
            "capex_bn": round(capex / 1e9, 2),
            "capex_prior_bn": round(prior["capex"] / 1e9, 2) if prior else None,
            "yoy_pct": round(yoy * 100, 1) if yoy is not None else None,
            "revenue_bn": round(rev / 1e9, 2) if rev else None,
            "ocf_bn": round(ocf / 1e9, 2) if ocf else None,
            "intensity_pct": round(capex / rev * 100, 1) if rev else None,
            "self_funding_pct": round(capex / ocf * 100, 1) if ocf and ocf > 0 else None,
            "fcf_bn": round((ocf - capex) / 1e9, 2) if ocf is not None else None,
        })

    table.sort(key=lambda r: r["capex_bn"], reverse=True)

    # write the table
    fields = ["ticker", "layer", "fy_end", "capex_bn", "capex_prior_bn", "yoy_pct",
              "revenue_bn", "ocf_bn", "intensity_pct", "self_funding_pct", "fcf_bn"]
    with open(D / "capex_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(table)

    # layer rollup
    layer = defaultdict(lambda: [0.0, 0])
    for r in table:
        layer[r["layer"]][0] += r["capex_bn"]
        layer[r["layer"]][1] += 1
    roll = sorted(([k, round(v[0], 1), v[1]] for k, v in layer.items()),
                  key=lambda x: -x[1])
    with open(D / "layer_rollup.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["layer", "capex_bn", "n_companies"])
        w.writerows(roll)

    # concentration stats
    total = sum(r["capex_bn"] for r in table)
    top5 = sum(r["capex_bn"] for r in table[:5])
    top1 = table[0]["capex_bn"]
    hypers = sum(r["capex_bn"] for r in table if r["layer"] == "Hyperscaler")
    shares = sorted((r["capex_bn"] / total for r in table), reverse=True)
    hhi = sum(s * s for s in shares) * 10000

    print(f"\n=== {len(table)} companies, total capex ${total:,.0f}bn ===")
    print(f"top-1 ({table[0]['ticker']}): ${top1:,.0f}bn = {top1/total*100:.0f}% of total")
    print(f"top-5: ${top5:,.0f}bn = {top5/total*100:.0f}% of total")
    print(f"hyperscalers (5 names): ${hypers:,.0f}bn = {hypers/total*100:.0f}% of total")
    print(f"HHI (capex concentration): {hhi:,.0f}")
    print("\n=== by layer ===")
    for k, c, n in roll:
        print(f"  {k:22s} ${c:7,.1f}bn  ({n} names, {c/total*100:4.1f}%)")
    print("\n=== negative-FCF (burning to build) ===")
    for r in table:
        if r["fcf_bn"] is not None and r["fcf_bn"] < 0:
            print(f"  {r['ticker']:6s} FCF ${r['fcf_bn']:7.1f}bn  "
                  f"intensity {r['intensity_pct']}%  self-fund {r['self_funding_pct']}%")
    if excluded:
        print("\n=== excluded (no standard capex tag) ===")
        for t, lyr, why in excluded:
            print(f"  {t} ({lyr}): {why}")


if __name__ == "__main__":
    main()
