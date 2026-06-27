#!/usr/bin/env python3
"""
Reproducible cross-check anchor for the foreign-filer capex (the workflow gathers
the current-year figures from primary sources; this pulls whatever the foreign
20-F filers report directly to SEC EDGAR, which is clean but lags by a year).

Foreign private issuers file 20-F with either the IFRS taxonomy (ifrs-full
namespace) or us-gaap; some (TSMC, UMC) even publish a USD-translated capex line
alongside the local-currency one. We capture both. Output: data/foreign_edgar_anchor.csv
"""
import csv
import json
import urllib.request
from datetime import date
from pathlib import Path

UA = "yeh-capital-research elonyeh0211@gmail.com"
D = Path(__file__).resolve().parent.parent / "data"

# foreign 20-F filers that report capex to EDGAR
TICKERS = ["TSM", "UMC", "ASML", "NBIS", "BABA", "BIDU", "SONY", "LPL"]
TAGS = [
    ("ifrs-full", "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"),
    ("ifrs-full", "PurchaseOfPropertyPlantAndEquipmentIntangibleAssetsAndOtherAssets"),
    ("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment"),
    ("us-gaap", "PaymentsToAcquireProductiveAssets"),
]


def _get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30))


def _d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def main():
    cm = {r["ticker"].upper(): (str(r["cik_str"]).zfill(10), r["title"])
          for r in _get("https://www.sec.gov/files/company_tickers.json").values()}
    rows = []
    for tkr in TICKERS:
        info = cm.get(tkr)
        if not info:
            print(f"{tkr:6s} not in EDGAR ticker map")
            continue
        cik, title = info
        found = {}  # unit -> (end, val, ns, tag)
        for ns, tag in TAGS:
            try:
                j = _get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{ns}/{tag}.json")
            except Exception:
                continue
            for unit, arr in j.get("units", {}).items():
                best = None
                for u in arr:
                    if not u.get("start") or not str(u.get("form", "")).startswith("20-F"):
                        continue
                    if not (350 <= (_d(u["end"]) - _d(u["start"])).days <= 380):
                        continue
                    if best is None or (u.get("filed", ""), u["end"]) > best[0]:
                        best = ((u.get("filed", ""), u["end"]), u["val"])
                if best and (unit not in found or best[0][1] > found[unit][0]):
                    found[unit] = (best[0][1], best[1], ns, tag)
        if not found:
            print(f"{tkr:6s} ({title[:30]}) no EDGAR capex")
            continue
        usd = found.get("USD")
        local_unit = next((u for u in found if u != "USD"), None)
        local = found.get(local_unit)
        rows.append({
            "ticker": tkr, "title": title,
            "fiscal_end": (usd or local)[0],
            "capex_usd_bn": round(usd[1] / 1e9, 2) if usd else None,
            "capex_local_bn": round(local[1] / 1e9, 2) if local else None,
            "local_ccy": local_unit or "",
            "tag": (usd or local)[3], "source": "SEC EDGAR 20-F",
        })
        u = f"{usd[1]/1e9:.2f}" if usd else "n/a"
        lc = f"{local[1]/1e9:.1f} {local_unit}" if local else ""
        print(f"{tkr:6s} {(usd or local)[0]}  USD {u:>7}bn   {lc}")
    with open(D / "foreign_edgar_anchor.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "title", "fiscal_end", "capex_usd_bn",
                                          "capex_local_bn", "local_ccy", "tag", "source"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {D/'foreign_edgar_anchor.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
