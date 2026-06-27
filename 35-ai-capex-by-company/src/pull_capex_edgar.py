#!/usr/bin/env python3
"""
Pull per-company capital expenditure across the AI value chain from SEC EDGAR XBRL.

Source: data.sec.gov companyconcept API (public-domain 10-K/10-Q filings).
We take *annual* figures (full fiscal-year duration) to sidestep the well-known
10-Q year-to-date cumulation trap on cash-flow-statement line items, then add a
trailing-twelve-month (TTM) value by stitching the latest reported quarters.

For each ticker we pull three concepts, each with a fallback tag list because
issuers tag the same economic line differently:
  - capex  : cash paid for property/plant/equipment
  - revenue: total net revenue
  - ocf    : net cash from operating activities

Outputs data/capex_raw.csv (long, one row per ticker x fiscal-year x metric).
Derived table is built by 01_build_table.py.

No API key required. EDGAR asks for a descriptive User-Agent with contact email.
"""
import csv
import json
import time
import urllib.request
from pathlib import Path

UA = "yeh-capital-research elonyeh0211@gmail.com"
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

# --- universe: US EDGAR filers across the AI value chain -------------------
# layer label is the reader-facing value-chain layer (mirrors study 30/17).
UNIVERSE = [
    # (ticker, layer)
    ("MSFT", "Hyperscaler"),
    ("GOOGL", "Hyperscaler"),
    ("AMZN", "Hyperscaler"),
    ("META", "Hyperscaler"),
    ("ORCL", "Hyperscaler"),
    ("CRWV", "Neocloud"),
    ("APLD", "Neocloud"),
    ("IREN", "Neocloud"),
    ("CIFR", "Neocloud"),
    ("WULF", "Neocloud"),
    ("CORZ", "Neocloud"),
    ("NVDA", "Compute silicon"),
    ("AMD", "Compute silicon"),
    ("AVGO", "Compute silicon"),
    ("MRVL", "Compute silicon"),
    ("QCOM", "Compute silicon"),
    ("INTC", "Foundry / memory"),
    ("MU", "Foundry / memory"),
    ("AMAT", "Semicap equipment"),
    ("LRCX", "Semicap equipment"),
    ("KLAC", "Semicap equipment"),
    ("ONTO", "Semicap equipment"),
    ("ANET", "Networking / optical"),
    ("CSCO", "Networking / optical"),
    ("LITE", "Networking / optical"),
    ("COHR", "Networking / optical"),
    ("CRDO", "Networking / optical"),
    ("DELL", "Servers / ODM"),
    ("SMCI", "Servers / ODM"),
    ("HPE", "Servers / ODM"),
    ("EQIX", "Data-center REIT"),
    ("DLR", "Data-center REIT"),
    ("VRT", "Power / cooling"),
    ("ETN", "Power / cooling"),
    ("GEV", "Power / cooling"),
    ("NEE", "Power / cooling"),
    ("CEG", "Power / cooling"),
    ("SO", "Power / cooling"),
    ("DUK", "Power / cooling"),
    ("BE", "Power / cooling"),
    ("PWR", "Power / cooling"),
    ("PLTR", "Software / apps"),
    ("NOW", "Software / apps"),
    ("CRM", "Software / apps"),
    ("SNOW", "Software / apps"),
    ("IBM", "Software / apps"),
]

CAPEX_TAGS = [
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsToAcquireProductiveAssets",            # AMZN, NVDA, EQIX, QCOM, HPE, GEV, LRCX
    "PaymentsToDevelopRealEstateAssets",            # DLR (data-center REIT)
    "PaymentsForCapitalImprovements",
    "PaymentsForConstructionInProcess",
    "PaymentsToAcquireOtherPropertyPlantAndEquipment",
    "PaymentsToAcquireMachineryAndEquipment",
]
REV_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueNet",
]
OCF_TAGS = [
    "NetCashProvidedByUsedInOperatingActivities",
    "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
]


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def cik_map():
    d = _get("https://www.sec.gov/files/company_tickers.json")
    m = {}
    for row in d.values():
        m[row["ticker"].upper()] = str(row["cik_str"]).zfill(10)
    return m


def annual_series(cik, tags):
    """Return (tag, {end_year: (end_date, value)}) for the BEST candidate tag.

    Best = the tag whose annual series reaches the latest period end-date (so a
    tag-switcher like AMZN/EQIX/NVDA resolves to the current tag, not the retired
    one). Annual = duration 350-380 days from a 10-K/20-F. Values are keyed by the
    period END-DATE year (NOT the filing 'fy', which mislabels comparative prior-
    year rows) and the latest-filed value wins per year."""
    chosen_tag, chosen, chosen_max_end = None, {}, None
    for tag in tags:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
        try:
            d = _get(url)
        except Exception:
            continue
        units = d.get("units", {}).get("USD")
        if not units:
            continue
        ser = {}  # end_year -> (filed, end_date, val)
        for u in units:
            start, end = u.get("start"), u.get("end")
            if not start or not end:
                continue
            dur = (_d(end) - _d(start)).days
            if not (350 <= dur <= 380):
                continue
            if not str(u.get("form", "")).startswith(("10-K", "20-F")):
                continue
            yr = int(end[:4])
            filed = u.get("filed", "")
            if yr not in ser or (filed, end) > (ser[yr][0], ser[yr][1]):
                ser[yr] = (filed, end, u["val"])
        if not ser:
            continue
        max_end = max(v[1] for v in ser.values())
        if chosen_max_end is None or max_end > chosen_max_end:
            chosen_tag, chosen, chosen_max_end = tag, ser, max_end
    return chosen_tag, {yr: (v[1], v[2]) for yr, v in chosen.items()}


def _d(s):
    from datetime import date
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def _v(series, yr):
    """value from an annual_series dict {yr:(end,val)}; None if absent."""
    return series[yr][1] if yr in series else None


def main():
    cm = cik_map()
    rows = []
    for tkr, layer in UNIVERSE:
        cik = cm.get(tkr)
        if not cik:
            print(f"  {tkr:6s} NO CIK — skipped")
            rows.append({"ticker": tkr, "layer": layer, "status": "no_cik"})
            continue
        cap_tag, cap = annual_series(cik, CAPEX_TAGS)
        rev_tag, rev = annual_series(cik, REV_TAGS)
        ocf_tag, ocf = annual_series(cik, OCF_TAGS)
        fys = sorted(set(cap) | set(rev) | set(ocf))
        for fy in fys:
            end = (cap.get(fy) or rev.get(fy) or ocf.get(fy) or (None,))[0]
            rows.append({
                "ticker": tkr, "layer": layer, "cik": cik, "fy": fy,
                "fy_end": end,
                "capex": _v(cap, fy), "revenue": _v(rev, fy), "ocf": _v(ocf, fy),
                "capex_tag": cap_tag, "rev_tag": rev_tag, "ocf_tag": ocf_tag,
                "status": "ok" if fy in cap else "no_capex",
            })
        latest = max(cap) if cap else None
        end = cap[latest][0] if latest else "?"
        print(f"  {tkr:6s} {layer:20s} {end}: capex={_b(_v(cap, latest))}  "
              f"rev={_b(_v(rev, latest))}  ocf={_b(_v(ocf, latest))}  [{cap_tag}]")
        time.sleep(0.1)  # EDGAR fair-use; 3 calls/name
    fields = ["ticker", "layer", "cik", "fy", "fy_end", "capex", "revenue",
              "ocf", "capex_tag", "rev_tag", "ocf_tag", "status"]
    p = OUT / "capex_raw.csv"
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})
    print(f"\nwrote {p} ({len(rows)} rows)")


def _b(v):
    return f"{v/1e9:7.2f}bn" if v else "   n/a"


if __name__ == "__main__":
    main()
