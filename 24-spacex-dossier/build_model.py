#!/usr/bin/env python3
"""Build the SpaceX IPO decision model artifacts.

This is a public-repo model: all hard-coded facts should be traceable to
public filings or public market data. It intentionally avoids private
pipeline dependencies.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

PROSPECTUS_DATE_ASSUMPTION = date(2026, 6, 11)
FIRST_TRADE_DATE_ASSUMPTION = date(2026, 6, 12)
IPO_FLOAT_M = 555.555555
IPO_PRICE = 135.00
POST_A_M = 7380.196910
POST_B_M = 5695.668265
POST_TOTAL_M = POST_A_M + POST_B_M
LOCKUP_180_DAY_POOL_M = 4557.5
EXTENDED_LOCKUP_EX_MUSK_POOL_M = 1759.5
MUSK_LOCKUP_M = 6400.0
TESLA_SPACEX_INVESTMENT_USD_B = 2.0
US_MARKET_HOLIDAYS_2026 = {
    date(2026, 6, 19),  # Juneteenth
    date(2026, 7, 3),  # Independence Day observed
}


def model_date(days: int) -> str:
    return (PROSPECTUS_DATE_ASSUMPTION + timedelta(days=days)).isoformat()


def nth_trading_day(start: date, n: int) -> str:
    current = start
    seen = 0
    while True:
        if current.weekday() < 5 and current not in US_MARKET_HOLIDAYS_2026:
            seen += 1
            if seen == n:
                return current.isoformat()
        current += timedelta(days=1)


def write(df: pd.DataFrame, name: str) -> None:
    df.to_csv(DATA / f"{name}.csv", index=False)


def date_meta(raw_date: str, basis: str) -> tuple[str, str, str]:
    if raw_date.startswith("TBD"):
        return raw_date, basis, "expected_month"
    return raw_date, basis, "model_calendar_date"


sources = pd.DataFrame(
    [
        {
            "source": "SpaceX S-1/A",
            "date": "2026-06-03",
            "filing_or_article": "S-1/A, accession 0001628280-26-040364",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/spaceexplorationtechnologib.htm",
            "used_for": "Offering math, ownership, segment financials, lock-up schedule, risk factors",
            "status": "primary",
        },
        {
            "source": "SpaceX FWP - UK retail offer",
            "date": "2026-06-04",
            "filing_or_article": "FWP, accession 0001628280-26-040874",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026040874/spacexukfwp.htm",
            "used_for": "Retail-offer context, UK distribution, disclosure-summary cross-check",
            "status": "primary",
        },
        {
            "source": "SpaceX FWP - company update",
            "date": "2026-06-04",
            "filing_or_article": "FWP, accession 0001628280-26-040610",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026040610/spacexfwp.htm",
            "used_for": "Filing completeness check",
            "status": "primary",
        },
        {
            "source": "SpaceX FWP - Google compute agreement",
            "date": "2026-06-05",
            "filing_or_article": "FWP, accession 0001628280-26-041150",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026041150/spacexagreementfwp.htm",
            "used_for": "Post-S-1 compute revenue delta: Google $920M/month contract disclosure",
            "status": "primary",
        },
        {
            "source": "SpaceX FWP - Japan retail offer",
            "date": "2026-06-05",
            "filing_or_article": "FWP, accession 0001628280-26-041013",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026041013/japanfwp_06042026.htm",
            "used_for": "Retail-offer context and filing completeness check",
            "status": "primary",
        },
        {
            "source": "SpaceX FWP - EU interview transcript",
            "date": "2026-06-08",
            "filing_or_article": "FWP, accession 0001628280-26-041365",
            "url": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026041365/eu_interviewtranscript06.htm",
            "used_for": "Latest EDGAR filing check as of model build date",
            "status": "primary",
        },
        {
            "source": "SpaceX IPO launch release",
            "date": "2026-06-04",
            "filing_or_article": "Company IPO launch release",
            "url": "https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/6.4.26_SpaceX_Announces_IPO_US.pdf",
            "used_for": "Company announcement cross-check",
            "status": "primary",
        },
        {
            "source": "Axios - SpaceX IPO raise",
            "date": "2026-06-03",
            "filing_or_article": "SpaceX plans to raise $75B in its IPO",
            "url": "https://www.axios.com/2026/06/03/spacex-ipo-raise",
            "used_for": "News cross-check on size, price and largest-IPO context",
            "status": "secondary",
        },
        {
            "source": "Axios - retail allocation color",
            "date": "2026-06-08",
            "filing_or_article": "Elon Musk's market magic",
            "url": "https://www.axios.com/2026/06/08/musk-spacex-stocks-ipo",
            "used_for": "Retail allocation and market-sentiment color only",
            "status": "secondary",
        },
        {
            "source": "TechCrunch - IPO filing overview",
            "date": "2026-05-20",
            "filing_or_article": "The SpaceX IPO filing is filled with AI bets, Starship dreams, and Elon Musk at the center",
            "url": "https://techcrunch.com/2026/05/20/the-spacex-ipo-filing-has-arrived/",
            "used_for": "Qualitative news cross-check; not a model input",
            "status": "secondary",
        },
        {
            "source": "YehCapital study 15 - Should you chase IPOs?",
            "date": "2026-06-08",
            "filing_or_article": "15-ipo-chase public research note",
            "url": "../15-ipo-chase/",
            "used_for": "Broad aftermarket IPO base rate: day-1 close entries versus SPY",
            "status": "internal published research",
        },
        {
            "source": "Nasdaq-100 Index Methodology",
            "date": "2026-05-01",
            "filing_or_article": "Methodology_NDX.pdf",
            "url": "https://indexes.nasdaq.com/docs/Methodology_NDX.pdf",
            "used_for": "Nasdaq-100 fast-entry, seasoning, liquidity and low-float weighting rules",
            "status": "primary",
        },
        {
            "source": "Nasdaq-100 methodology update",
            "date": "2026-05-08",
            "filing_or_article": "Nasdaq-100 Index Methodology Update: Why Now, and What It Means",
            "url": "https://www.nasdaq.com/newsroom/nasdaq100-index-methodology-update-why-now",
            "used_for": "Cross-check on May 1 rule changes and June 22 first rebalance under new rules",
            "status": "primary",
        },
        {
            "source": "S&P U.S. Indices Methodology",
            "date": "2026-05",
            "filing_or_article": "methodology-sp-us-indices.pdf",
            "url": "https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-us-indices.pdf",
            "used_for": "S&P 500 eligibility, seasoning, liquidity, IWF and profitability rules",
            "status": "primary",
        },
        {
            "source": "S&P DJI MegaCap consultation results",
            "date": "2026-06-04",
            "filing_or_article": "S&P Dow Jones Indices Consultation on Treatment of MegaCap Companies - Results",
            "url": "https://www.spglobal.com/spdji/en/documents/indexnews/announcements/20260604-1483731/1483731_spdji-us-indices-megacaps-results-20260604.pdf",
            "used_for": "S&P 500 no-change decision and Total Market Index mega-cap IWF update",
            "status": "primary",
        },
        {
            "source": "Tesla 10-Q",
            "date": "2026-04-23",
            "filing_or_article": "Tesla Form 10-Q for quarter ended March 31, 2026",
            "url": "https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm",
            "used_for": "Tesla SpaceX equity investment and Q1 2026 SpaceX Megapack related-party transaction cross-check",
            "status": "primary",
        },
        {
            "source": "Tesla 10-K/A",
            "date": "2026-04-30",
            "filing_or_article": "Tesla Form 10-K/A for fiscal year 2025",
            "url": "https://www.sec.gov/Archives/edgar/data/1318605/000110465926053166/tm2611837d1_10ka.htm",
            "used_for": "Musk outside roles and Tesla/SpaceX/xAI/X related-party transaction cross-check",
            "status": "primary",
        },
    ]
)
write(sources, "sources")


offering_math = pd.DataFrame(
    [
        ("Class A shares offered", IPO_FLOAT_M, "million shares", "S-1/A", "Primary issuance; freely tradable unless bought by affiliates."),
        ("Over-allotment option", 83.333333, "million shares", "S-1/A", "Primary shares; no underwriting discount on option shares per filing."),
        ("IPO price assumption", IPO_PRICE, "USD/share", "S-1/A", "Expected initial public offering price."),
        ("Gross proceeds", IPO_FLOAT_M * IPO_PRICE / 1000, "USD billion", "calculated", "Base offering before fees."),
        ("Net proceeds", 74.4, "USD billion", "S-1/A", "Company estimate after underwriting discounts and expenses."),
        ("Net proceeds if option exercised", 85.7, "USD billion", "S-1/A", "Company estimate with full over-allotment."),
        ("Class A shares post offering", POST_A_M, "million shares", "S-1/A", "After base offering, no option exercise."),
        ("Class B shares post offering", POST_B_M, "million shares", "S-1/A", "After base offering, no option exercise."),
        ("Total common shares post offering", POST_TOTAL_M, "million shares", "calculated", "Class A plus Class B; not fully diluted."),
        ("Implied market cap", POST_TOTAL_M * IPO_PRICE / 1000, "USD billion", "calculated", "Basic post-offering common shares times IPO price."),
        ("Immediate public float", IPO_FLOAT_M, "million shares", "S-1/A", "IPO shares only; excludes option exercise."),
        ("Immediate free-float percentage", IPO_FLOAT_M / POST_TOTAL_M * 100, "percent of basic shares", "calculated", "Legally tradable Class A supply at IPO."),
        ("Immediate public float if option exercised", IPO_FLOAT_M + 83.333333, "million shares", "S-1/A/calculated", "IPO shares plus full over-allotment."),
        ("Free-float percentage if option exercised", (IPO_FLOAT_M + 83.333333) / (POST_TOTAL_M + 83.333333) * 100, "percent of basic shares", "calculated", "Assumes additional primary shares are issued."),
        ("Directed share program", IPO_FLOAT_M * 0.05, "million shares", "S-1/A", "Up to 5% of IPO shares; not subject to lock-up if purchased."),
        ("Class A voting power", 11.5, "percent", "S-1/A", "After base offering."),
        ("Class B voting power", 88.5, "percent", "S-1/A", "After base offering."),
        ("Registration-rights overhang", 12200.0, "million shares", "S-1/A", "Approximate Class A shares including Class B conversion shares with registration rights."),
        ("Nasdaq-100 full market cap for eligibility", POST_TOTAL_M * IPO_PRICE / 1000, "USD billion", "Nasdaq methodology/calculated", "Eligibility ranking considers full market cap, including listed and unlisted shares."),
        ("Nasdaq-100 modified market cap - base float", min(POST_A_M, IPO_FLOAT_M * 3) * IPO_PRICE / 1000, "USD billion", "Nasdaq methodology/calculated", "Weighting uses listed Class A market cap capped at 3x free-floating shares for low-float securities."),
        ("Nasdaq-100 modified market cap - option exercised", min(POST_A_M + 83.333333, (IPO_FLOAT_M + 83.333333) * 3) * IPO_PRICE / 1000, "USD billion", "Nasdaq methodology/calculated", "Same low-float cap if the over-allotment option is fully exercised."),
        ("S&P float-adjusted market cap at IPO", IPO_FLOAT_M * IPO_PRICE / 1000, "USD billion", "S&P methodology/calculated", "Base public float value; relevant for S&P IWF/FMC screens and broad-index fast-track math."),
        ("Anthropic compute contract", 1.25, "USD billion/month", "S-1/A", "May 2026 cloud services agreements through May 2029; terminable after initial 3-month period on 90 days notice."),
        ("Google compute contract", 0.92, "USD billion/month", "June 5 FWP", "October 2026 through June 2029 after ramp; terminable after Dec. 31, 2026 on 90 days notice."),
    ],
    columns=["metric", "value", "unit", "source", "note"],
)
write(offering_math, "offering_math")


shareholder_ratios = pd.DataFrame(
    [
        ("Elon Musk", 849.494440, 5569.053075, 6418.547515, 6418.547515 / POST_TOTAL_M * 100, 84.4, "Includes restricted Class B shares that may be voted; S-1/A ownership table."),
        ("Gwynne Shotwell", 5.759610, 7.113550, 12.873160, 12.873160 / POST_TOTAL_M * 100, 0.0, "Less than 1% combined voting power."),
        ("Bret Johnsen", 9.048565, 0.0, 9.048565, 9.048565 / POST_TOTAL_M * 100, 0.0, "CFO ownership; less than 1% voting power."),
        ("Antonio J. Gracias", 503.414530, 0.0, 503.414530, 503.414530 / POST_TOTAL_M * 100, 0.0, "Director and Valor founder; 6.7% Class A after offering."),
        ("Luke Nosek", 32.987360, 0.0, 32.987360, 32.987360 / POST_TOTAL_M * 100, 0.0, "Director; less than 1% voting power."),
        ("All executive officers and directors", 1402.027270, 5576.731275, 6978.758545, 6978.758545 / POST_TOTAL_M * 100, 85.3, "Group table after offering."),
        ("Public IPO buyers", IPO_FLOAT_M, 0.0, IPO_FLOAT_M, IPO_FLOAT_M / POST_TOTAL_M * 100, 0.9, "Approximate voting power: IPO Class A votes divided by total post-offering votes."),
    ],
    columns=["holder", "class_a_m", "class_b_m", "economic_shares_m", "economic_pct_basic", "combined_voting_pct", "note"],
)
write(shareholder_ratios, "shareholder_ratios")


tesla_estimated_spacex_shares_m = TESLA_SPACEX_INVESTMENT_USD_B * 1000 / IPO_PRICE
tesla_spacex_related_parties = pd.DataFrame(
    [
        (
            "Tesla equity investment in SpaceX",
            "2026-03",
            TESLA_SPACEX_INVESTMENT_USD_B,
            tesla_estimated_spacex_shares_m,
            tesla_estimated_spacex_shares_m / POST_TOTAL_M * 100,
            "Less than 1% per Tesla 10-Q; approx 0.11% if valued at $135 IPO price.",
            "Tesla 10-Q says the company invested $2.00B in SpaceX common stock, formerly a preferred share investment in xAI, representing an ownership interest of less than 1%.",
            "This is not listed as a named holder in the SpaceX S-1/A beneficial ownership table; use as Tesla economic exposure, not control.",
            "Tesla 10-Q 2026-04-23",
        ),
        (
            "Tesla revenue from SpaceX Megapack purchase",
            "2026-Q1",
            0.087,
            pd.NA,
            pd.NA,
            "Q1 2026 related-party operating transaction.",
            "Tesla recognized $87M of revenues and $65M of cost of revenues from SpaceX for its purchase of Megapack products in ordinary course.",
            "Confirms commercial relationship; not equity ownership.",
            "Tesla 10-Q 2026-04-23",
        ),
        (
            "SpaceX Megapack purchases from Tesla",
            "2025",
            0.506,
            pd.NA,
            pd.NA,
            "SpaceX related-party capex purchase.",
            "SpaceX S-1/A says the company purchased $506M of Megapack products from Tesla in 2025, recorded in property, plant and equipment.",
            "Adds related-party/capital-intensity complexity around AI/compute power infrastructure.",
            "SpaceX S-1/A 2026-06-03",
        ),
        (
            "SpaceX Megapack purchases from Tesla",
            "2024",
            0.191,
            pd.NA,
            pd.NA,
            "SpaceX related-party capex purchase.",
            "SpaceX S-1/A says the company purchased $191M of Megapack products from Tesla in 2024.",
            "Commercial relationship predates the IPO and xAI consolidation.",
            "SpaceX S-1/A 2026-06-03",
        ),
        (
            "Tesla commercial/licensing/support transactions with SpaceX",
            "2025",
            0.1433,
            pd.NA,
            pd.NA,
            "Tesla revenue from SpaceX-related commercial arrangements.",
            "Tesla 10-K/A says Tesla recognized approximately $143.3M of revenue in 2025, primarily for vehicle sales, under SpaceX commercial/licensing/support agreements.",
            "Related-party commercial activity; not proof of material SpaceX equity ownership beyond the separate $2.00B investment.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Tesla expenses under SpaceX commercial/licensing/support agreements",
            "2025",
            0.0114,
            pd.NA,
            pd.NA,
            "Tesla expense to SpaceX.",
            "Tesla 10-K/A says Tesla incurred approximately $11.4M of expenses in 2025 under SpaceX commercial/licensing/support agreements.",
            "Small operating related-party expense.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Tesla aircraft-use expense to SpaceX",
            "2025",
            0.0004,
            pd.NA,
            pd.NA,
            "Tesla expense to SpaceX.",
            "Tesla 10-K/A says SpaceX invoiced Tesla for use of aircraft owned and operated by SpaceX; Tesla incurred about $0.4M in 2025.",
            "Immaterial but disclosed related-party link.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Tesla advertising on X",
            "2025",
            0.0033,
            pd.NA,
            pd.NA,
            "Tesla expense to X.",
            "Tesla 10-K/A says Tesla directly or indirectly purchased advertising on X and incurred about $3.3M in 2025.",
            "Relevant because X became part of xAI, and xAI became part of SpaceX in 2026.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Tesla revenue from xAI Megapack sales",
            "2025",
            0.4301,
            pd.NA,
            pd.NA,
            "Tesla revenue from xAI before xAI became SpaceX subsidiary.",
            "Tesla 10-K/A says Tesla recognized approximately $430.1M of revenue in 2025 from xAI, primarily for Megapack products.",
            "Shows Tesla/xAI commercial relationship feeding into the later SpaceX AI segment.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Tesla revenue from xAI through February 2026",
            "2026-01_to_2026-02",
            0.0781,
            pd.NA,
            pd.NA,
            "Tesla revenue from xAI before/around SpaceX xAI acquisition effective date.",
            "Tesla 10-K/A says Tesla recognized approximately $78.1M of revenue through February 2026 from xAI, primarily for Megapack products.",
            "Cross-checks Tesla/xAI/SpaceX related-party chain.",
            "Tesla 10-K/A 2026-04-30",
        ),
        (
            "Musk cross-company role",
            "2026-04-30",
            pd.NA,
            pd.NA,
            pd.NA,
            "Governance and related-party context.",
            "Tesla 10-K/A describes Musk roles at Tesla, SpaceX, X/xAI, The Boring Company and Neuralink; SpaceX S-1/A shows Musk 84.4% voting control after offering.",
            "Explains why Tesla says it is presumed to have significant influence over SpaceX for accounting even with less than 1% ownership.",
            "Tesla 10-K/A 2026-04-30; Tesla 10-Q 2026-04-23; SpaceX S-1/A 2026-06-03",
        ),
    ],
    columns=[
        "relationship",
        "period_or_date",
        "amount_usd_b",
        "estimated_spacex_shares_m_at_ipo_price",
        "estimated_economic_pct_basic",
        "headline",
        "filing_fact",
        "model_read",
        "source",
    ],
)
write(tesla_spacex_related_parties, "tesla_spacex_related_parties")


lockup_rows = [
    (0, "IPO float", "At offering", PROSPECTUS_DATE_ASSUMPTION.isoformat(), IPO_FLOAT_M, "IPO shares", 100.0, "Freely tradable unless held by affiliates; includes any directed-share purchases.", True),
    (1, "Over-allotment option", "30 days after prospectus", model_date(30), 83.333333, "IPO option", 15.0, "Only if underwriters exercise option.", True),
    (2, "First earnings release unlock", "2nd full trading day after Q2 2026 earnings release", "TBD - likely Aug 2026", 911.5, "180-day pool", 164.1, "20% release from 180-day lock-up pool, non-affiliates only.", True),
    (3, "Performance early release", "Same Q2 2026 release window", "TBD - likely Aug 2026", 455.8, "180-day pool", 82.0, "Only if closing price is at least 30% above IPO price for 5 of 10 trading days ending on first earnings release date.", True),
    (4, "Day 70 release", "70th day after prospectus", model_date(70), 319.0, "180-day pool", 57.4, "7% release from 180-day lock-up pool, non-affiliates only.", True),
    (5, "Day 90 release", "90th day after prospectus", model_date(90), 319.0, "180-day pool", 57.4, "7% release from 180-day lock-up pool, non-affiliates only.", True),
    (6, "Affiliate catch-up release", "91st day after prospectus", model_date(91), 59.1, "180-day affiliate pool", 10.6, "Affiliate shares previously released from lock-up but delayed by Rule 144 timing.", True),
    (7, "Day 105 release", "105th day after prospectus", model_date(105), 328.4, "180-day pool", 59.1, "7% release from 180-day lock-up pool.", True),
    (8, "Day 120 release", "120th day after prospectus", model_date(120), 328.4, "180-day pool", 59.1, "7% release from 180-day lock-up pool.", True),
    (9, "Day 135 release", "135th day after prospectus", model_date(135), 328.4, "180-day pool", 59.1, "7% release from 180-day lock-up pool.", True),
    (10, "Q3 2026 earnings release unlock", "2nd full trading day after Q3 2026 earnings release", "TBD - likely Nov 2026", 1300.0, "180-day pool", 234.0, "28% release from 180-day lock-up pool.", True),
    (11, "Day 180 final 180-day release", "180th day after prospectus", model_date(180), 328.4, "180-day pool", 59.1, "If performance early release occurred; otherwise up to 797.6M shares.", True),
    (12, "Day 180 final 180-day release - no performance release case", "180th day after prospectus", model_date(180), 797.6, "180-day pool", 143.6, "Alternative case if Q2 price-trigger release did not occur.", True),
    (13, "Q4 2026 extended-lock release", "2nd full trading day after Q4 2026 earnings release", "TBD - likely Mar 2027", 351.9, "extended lock-up ex-Musk", 63.3, "20% of extended lock-up pool excluding Musk.", False),
    (14, "Day 280 extended release", "280th day after prospectus", model_date(280), 176.0, "extended lock-up ex-Musk", 31.7, "10% of extended lock-up pool excluding Musk.", False),
    (15, "Q1 2027 extended-lock release", "2nd full trading day after Q1 2027 earnings release", "TBD - likely May 2027", 351.9, "extended lock-up ex-Musk", 63.3, "20% of extended lock-up pool excluding Musk.", False),
    (16, "Day 340 extended release", "340th day after prospectus", model_date(340), 176.0, "extended lock-up ex-Musk", 31.7, "10% of extended lock-up pool excluding Musk.", False),
    (17, "Day 366 extended release", "366th day after prospectus", model_date(366), 351.9, "extended lock-up ex-Musk", 63.3, "20% of extended lock-up pool excluding Musk.", False),
    (18, "Musk lock-up release", "366th day after prospectus", model_date(366), 6400.0, "Musk lock-up", 1152.0, "All Musk-held shares, including Class B conversion shares and options; no early release.", False),
    (19, "Q2 2027 remaining extended release", "2nd full trading day after Q2 2027 earnings release", "TBD - likely Aug 2027", 351.9, "extended lock-up ex-Musk", 63.3, "Remaining extended lock-up pool.", False),
]
lockup_calendar = pd.DataFrame(
    lockup_rows,
    columns=["order", "event", "timing", "model_date_if_prospectus_2026_06_11", "shares_released_m", "pool", "percent_of_base_ipo_float", "condition", "inside_first_6_months"],
)
lockup_calendar[["event_date", "date_basis", "date_precision"]] = lockup_calendar.apply(
    lambda row: pd.Series(date_meta(row["model_date_if_prospectus_2026_06_11"], row["timing"])),
    axis=1,
)
lockup_calendar["milestone_date"] = lockup_calendar["event_date"]
lockup_calendar["milestone_with_date"] = lockup_calendar["event"] + " (" + lockup_calendar["event_date"] + ")"
lockup_calendar["release_x_base_ipo_float"] = lockup_calendar["shares_released_m"] / IPO_FLOAT_M
lockup_calendar["release_pct_basic_common"] = lockup_calendar["shares_released_m"] / POST_TOTAL_M * 100
lockup_calendar["release_pct_post_class_a"] = lockup_calendar["shares_released_m"] / POST_A_M * 100
lockup_calendar["release_pct_relevant_pool"] = pd.NA
lockup_calendar.loc[lockup_calendar["pool"].str.contains("180-day", case=False), "release_pct_relevant_pool"] = (
    lockup_calendar.loc[lockup_calendar["pool"].str.contains("180-day", case=False), "shares_released_m"] / LOCKUP_180_DAY_POOL_M * 100
)
lockup_calendar.loc[lockup_calendar["pool"].str.contains("extended", case=False), "release_pct_relevant_pool"] = (
    lockup_calendar.loc[lockup_calendar["pool"].str.contains("extended", case=False), "shares_released_m"] / EXTENDED_LOCKUP_EX_MUSK_POOL_M * 100
)
lockup_calendar.loc[lockup_calendar["pool"].str.contains("Musk", case=False), "release_pct_relevant_pool"] = (
    lockup_calendar.loc[lockup_calendar["pool"].str.contains("Musk", case=False), "shares_released_m"] / MUSK_LOCKUP_M * 100
)
write(lockup_calendar, "lockup_calendar")


lockup_supply_summary = pd.DataFrame(
    [
        (
            "Immediate IPO float",
            IPO_FLOAT_M,
            IPO_FLOAT_M / IPO_FLOAT_M,
            IPO_FLOAT_M / POST_TOTAL_M * 100,
            IPO_FLOAT_M / POST_A_M * 100,
            "Tradable at listing unless purchased by affiliates; this is the denominator for all unlock multiples.",
        ),
        (
            "Over-allotment option",
            83.333333,
            83.333333 / IPO_FLOAT_M,
            83.333333 / (POST_TOTAL_M + 83.333333) * 100,
            83.333333 / (POST_A_M + 83.333333) * 100,
            "Optional primary issuance, not a lock-up release. If exercised, immediate float rises to 638.9M shares.",
        ),
        (
            "180-day lock-up pool before affiliate timing",
            LOCKUP_180_DAY_POOL_M,
            LOCKUP_180_DAY_POOL_M / IPO_FLOAT_M,
            LOCKUP_180_DAY_POOL_M / POST_TOTAL_M * 100,
            LOCKUP_180_DAY_POOL_M / POST_A_M * 100,
            "Approximate pool inferred from S-1/A release percentages; releases are staged across Q2 earnings, day 70, day 90, day 105, day 120, day 135, Q3 earnings and day 180.",
        ),
        (
            "Base float plus 180-day pool",
            IPO_FLOAT_M + LOCKUP_180_DAY_POOL_M,
            (IPO_FLOAT_M + LOCKUP_180_DAY_POOL_M) / IPO_FLOAT_M,
            (IPO_FLOAT_M + LOCKUP_180_DAY_POOL_M) / POST_TOTAL_M * 100,
            (IPO_FLOAT_M + LOCKUP_180_DAY_POOL_M) / POST_A_M * 100,
            "Approximate before the 59.1M affiliate catch-up timing line; this is the clean first-six-month supply scale.",
        ),
        (
            "Extended lock-up excluding Musk",
            EXTENDED_LOCKUP_EX_MUSK_POOL_M,
            EXTENDED_LOCKUP_EX_MUSK_POOL_M / IPO_FLOAT_M,
            EXTENDED_LOCKUP_EX_MUSK_POOL_M / POST_TOTAL_M * 100,
            EXTENDED_LOCKUP_EX_MUSK_POOL_M / POST_A_M * 100,
            "Post-180-day releases beginning around Q4 2026 earnings, excluding Musk.",
        ),
        (
            "Musk 366-day lock-up",
            MUSK_LOCKUP_M,
            MUSK_LOCKUP_M / IPO_FLOAT_M,
            MUSK_LOCKUP_M / POST_TOTAL_M * 100,
            MUSK_LOCKUP_M / POST_A_M * 100,
            "Largest single overhang; no early release in the S-1/A lock-up schedule.",
        ),
        (
            "All named lock-up overhang after IPO float",
            LOCKUP_180_DAY_POOL_M + EXTENDED_LOCKUP_EX_MUSK_POOL_M + MUSK_LOCKUP_M,
            (LOCKUP_180_DAY_POOL_M + EXTENDED_LOCKUP_EX_MUSK_POOL_M + MUSK_LOCKUP_M) / IPO_FLOAT_M,
            (LOCKUP_180_DAY_POOL_M + EXTENDED_LOCKUP_EX_MUSK_POOL_M + MUSK_LOCKUP_M) / POST_TOTAL_M * 100,
            (LOCKUP_180_DAY_POOL_M + EXTENDED_LOCKUP_EX_MUSK_POOL_M + MUSK_LOCKUP_M) / POST_A_M * 100,
            "Potential supply overhang, not expected sale volume. Some Class B shares would need conversion before Class A trading.",
        ),
    ],
    columns=["pool", "shares_m", "x_base_ipo_float", "pct_basic_common", "pct_post_class_a", "interpretation"],
)
write(lockup_supply_summary, "lockup_supply_summary")


scenario_events = [
    ("IPO float", "At offering", PROSPECTUS_DATE_ASSUMPTION.isoformat(), IPO_FLOAT_M, IPO_FLOAT_M, "Starting tradable Class A supply."),
    ("First earnings release unlock", "Q2 2026 earnings window", "TBD - likely Aug 2026", 911.5, 911.5, "20% release from 180-day pool."),
    ("Performance early release", "Q2 2026 earnings window", "TBD - likely Aug 2026", 455.8, 0.0, "Only in performance case: price at least 30% above IPO price for 5 of 10 trading days."),
    ("Day 70 release", "70th day after prospectus", model_date(70), 319.0, 319.0, "7% release from 180-day pool."),
    ("Day 90 release", "90th day after prospectus", model_date(90), 319.0, 319.0, "7% release from 180-day pool."),
    ("Affiliate catch-up release", "91st day after prospectus", model_date(91), 59.1, 59.1, "Rule 144 timing catch-up; shown as incremental tradable supply, not a new percentage tranche."),
    ("Day 105 release", "105th day after prospectus", model_date(105), 328.4, 328.4, "7% release from 180-day pool."),
    ("Day 120 release", "120th day after prospectus", model_date(120), 328.4, 328.4, "7% release from 180-day pool."),
    ("Day 135 release", "135th day after prospectus", model_date(135), 328.4, 328.4, "7% release from 180-day pool."),
    ("Q3 2026 earnings release unlock", "Q3 2026 earnings window", "TBD - likely Nov 2026", 1300.0, 1300.0, "28% release from 180-day pool."),
    ("Day 180 final release", "180th day after prospectus", model_date(180), 328.4, 797.6, "Final 180-day release is smaller if the performance release happened, larger if it did not."),
]

scenario_rows = []
cumulative_perf = 0.0
cumulative_no_perf = 0.0
for order, (event, timing, model_day, incremental_perf, incremental_no_perf, note) in enumerate(scenario_events):
    cumulative_perf += incremental_perf
    cumulative_no_perf += incremental_no_perf
    scenario_rows.append(
        (
            order,
            event,
            timing,
            model_day,
            incremental_perf,
            incremental_perf / IPO_FLOAT_M,
            cumulative_perf,
            cumulative_perf / IPO_FLOAT_M,
            cumulative_perf / POST_TOTAL_M * 100,
            cumulative_perf / POST_A_M * 100,
            incremental_no_perf,
            incremental_no_perf / IPO_FLOAT_M,
            cumulative_no_perf,
            cumulative_no_perf / IPO_FLOAT_M,
            cumulative_no_perf / POST_TOTAL_M * 100,
            cumulative_no_perf / POST_A_M * 100,
            note,
        )
    )

lockup_first_6m_scenarios = pd.DataFrame(
    scenario_rows,
    columns=[
        "order",
        "event",
        "timing",
        "model_date_if_prospectus_2026_06_11",
        "incremental_perf_case_m",
        "incremental_perf_case_x_ipo_float",
        "cumulative_perf_case_m",
        "cumulative_perf_case_x_ipo_float",
        "cumulative_perf_case_pct_basic_common",
        "cumulative_perf_case_pct_post_class_a",
        "incremental_no_perf_case_m",
        "incremental_no_perf_case_x_ipo_float",
        "cumulative_no_perf_case_m",
        "cumulative_no_perf_case_x_ipo_float",
        "cumulative_no_perf_case_pct_basic_common",
        "cumulative_no_perf_case_pct_post_class_a",
        "note",
    ],
)
lockup_first_6m_scenarios[["event_date", "date_basis", "date_precision"]] = lockup_first_6m_scenarios.apply(
    lambda row: pd.Series(date_meta(row["model_date_if_prospectus_2026_06_11"], row["timing"])),
    axis=1,
)
lockup_first_6m_scenarios["milestone_date"] = lockup_first_6m_scenarios["event_date"]
lockup_first_6m_scenarios["milestone"] = lockup_first_6m_scenarios["event"]
lockup_first_6m_scenarios["milestone_with_date"] = (
    lockup_first_6m_scenarios["event"] + " (" + lockup_first_6m_scenarios["event_date"] + ")"
)
lockup_first_6m_scenarios["circulating_free_float_perf_case_m"] = lockup_first_6m_scenarios["cumulative_perf_case_m"]
lockup_first_6m_scenarios["circulating_free_float_perf_case_pct_basic_common"] = lockup_first_6m_scenarios["cumulative_perf_case_pct_basic_common"]
lockup_first_6m_scenarios["circulating_free_float_perf_case_pct_post_class_a"] = lockup_first_6m_scenarios["cumulative_perf_case_pct_post_class_a"]
lockup_first_6m_scenarios["circulating_free_float_no_perf_case_m"] = lockup_first_6m_scenarios["cumulative_no_perf_case_m"]
lockup_first_6m_scenarios["circulating_free_float_no_perf_case_pct_basic_common"] = lockup_first_6m_scenarios["cumulative_no_perf_case_pct_basic_common"]
lockup_first_6m_scenarios["circulating_free_float_no_perf_case_pct_post_class_a"] = lockup_first_6m_scenarios["cumulative_no_perf_case_pct_post_class_a"]
write(lockup_first_6m_scenarios, "lockup_first_6m_scenarios")


lockup_free_float_bridge = lockup_first_6m_scenarios[
    [
        "order",
        "event_date",
        "milestone",
        "date_basis",
        "date_precision",
        "incremental_perf_case_m",
        "incremental_no_perf_case_m",
        "circulating_free_float_perf_case_m",
        "circulating_free_float_perf_case_pct_basic_common",
        "circulating_free_float_perf_case_pct_post_class_a",
        "circulating_free_float_no_perf_case_m",
        "circulating_free_float_no_perf_case_pct_basic_common",
        "circulating_free_float_no_perf_case_pct_post_class_a",
        "note",
    ]
].copy()
lockup_free_float_bridge["starting_ipo_float_m"] = IPO_FLOAT_M
lockup_free_float_bridge["starting_ipo_float_pct_basic_common"] = IPO_FLOAT_M / POST_TOTAL_M * 100
lockup_free_float_bridge["interpretation"] = (
    "Circulating/free float means potential legally tradable Class A supply after the milestone; it is not a sale forecast."
)
write(lockup_free_float_bridge, "lockup_free_float_bridge")


nasdaq_explainer = pd.DataFrame(
    [
        (
            "Nasdaq exchange listing",
            "A company trades on the Nasdaq exchange. This is a listing venue, like NYSE versus Nasdaq.",
            "Lets the shares trade publicly under the ticker, subject to exchange listing standards.",
            "Gives investors a public trading venue and continuous price discovery.",
            "No. Listing does not create extra equity beyond the shares sold or registered.",
        ),
        (
            "Nasdaq-100 index inclusion",
            "The company becomes a constituent of the Nasdaq-100 index, which is tracked by ETFs and benchmarked products.",
            "Raises visibility, may improve liquidity, and can create passive/index demand. It does not raise new cash for SpaceX.",
            "Can create forced buying and higher liquidity, but it is not a fundamental guarantee and can be offset by valuation or unlock supply.",
            "No new shares are created. The index assigns a weight to existing shares; for low-float names Nasdaq-100 caps modified market cap at 3x free float.",
        ),
        (
            "Low-float weighting",
            "Nasdaq-100 has no minimum free-float requirement, but low-float securities are weighted using the lesser of listed shares or 3x free-floating shares.",
            "As more shares unlock and become free floating, the stock could represent more index market cap at later reviews.",
            "Unlocks can increase future index weight but also add sellable supply. The same event can be both passive-demand positive and supply-risk negative.",
            f"Base IPO float supports about ${min(POST_A_M, IPO_FLOAT_M * 3) * IPO_PRICE / 1000:.1f}B of Nasdaq modified market cap versus ${POST_TOTAL_M * IPO_PRICE / 1000:.1f}B full basic market cap.",
        ),
        (
            "Capital raised",
            "Index inclusion is secondary-market index mechanics, not a primary offering.",
            "SpaceX raises capital from the IPO proceeds, not from Nasdaq-100 inclusion itself.",
            "Index funds buy shares from the market or other holders; they do not inject cash into the company unless a separate primary issuance occurs.",
            "No. Equity outstanding changes only through issuance, conversion, exercise, buyback, or similar corporate actions.",
        ),
    ],
    columns=["concept", "plain_english", "company_meaning", "investor_meaning", "equity_supply_answer"],
)
write(nasdaq_explainer, "nasdaq_explainer")


spacex_business_breakdown = pd.DataFrame(
    [
        (
            "Rocket / Space",
            "Falcon, Dragon, Starship and customer launch operations.",
            4.086,
            -0.657,
            3.832,
            0.619,
            -0.662,
            1.052,
            "Strategic moat and launch cadence are the core franchise. Starship is the upside and execution-risk center.",
            "Execution risk, mission failure, capital intensity, government/customer concentration, launch cadence and regulatory approvals.",
        ),
        (
            "Starlink / Connectivity",
            "Starlink broadband/connectivity services and associated offerings.",
            11.387,
            4.423,
            4.178,
            3.257,
            1.188,
            1.332,
            "Best current business quality: 2025 operating margin 38.8%, 8.9M subscribers at year-end 2025 and 10.3M in Q1 2026.",
            "ARPU declined from $99 in 2023 to $81 in 2025 and $66 in Q1 2026; spectrum, orbital, regulatory and capacity constraints matter.",
        ),
        (
            "AI / xAI / X",
            "AI compute, Grok, X platform and related AI infrastructure acquired through xAI/X transactions.",
            3.201,
            -6.355,
            12.727,
            0.818,
            -2.469,
            7.723,
            "Largest optionality and largest quality penalty. SpaceX acquired xAI effective 2026-02-02; xAI had acquired X Holdings effective 2025-03-28.",
            "Heavy losses, high capex, power/GPU execution, related-party complexity, platform moderation/regulatory risk and terminable compute contracts.",
        ),
        (
            "Cursor / Anysphere",
            "April 2026 compute plus option agreement with Anysphere, Inc., doing business as Cursor.",
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            "Not acquired as of the S-1/A. SpaceX has the right, not obligation, to acquire Cursor at a $60B implied equity value after the offering.",
            "Potential strategic AI coding distribution and training-data asset; also creates option/termination-fee complexity.",
        ),
    ],
    columns=[
        "business_line",
        "description",
        "revenue_2025_usd_b",
        "operating_income_2025_usd_b",
        "capex_2025_usd_b",
        "revenue_q1_2026_usd_b",
        "operating_income_q1_2026_usd_b",
        "capex_q1_2026_usd_b",
        "why_it_matters",
        "key_risks",
    ],
)
write(spacex_business_breakdown, "spacex_business_breakdown")


spacex_ai_timeline = pd.DataFrame(
    [
        ("2022-10", "Twitter acquisition by X Holdings", "actual_month", "X Holdings acquired Twitter in October 2022, before the later xAI and SpaceX common-control transactions."),
        ("2023-07", "Twitter rebranded to X", "actual_month", "S-1/A describes impairment of the Twitter brand when Twitter was rebranded to X in July 2023."),
        ("2025-03-28", "xAI acquired X Holdings/X", "actual_effective_date", "S-1/A says X Holdings was acquired by xAI effective March 28, 2025."),
        ("2026-02-02", "SpaceX acquired xAI", "actual_effective_date", "S-1/A says X.AI Holdings Corp. was acquired by SpaceX effective February 2, 2026."),
        ("2026-04", "SpaceX entered Cursor compute + option agreement", "actual_month", "SpaceX entered a compute and option agreement with Anysphere/Cursor in April 2026."),
        ("2026-05", "Anthropic cloud services agreements", "actual_month", "SpaceX entered Anthropic cloud services agreements in May 2026 for approximately 325,000 NVIDIA GPUs."),
        ("2026-06-05", "Google cloud services agreement FWP", "actual_filing_date", "June 5 FWP disclosed Google agreement for approximately 110,000 NVIDIA GPUs."),
    ],
    columns=["event_date", "event", "date_precision", "note"],
)
spacex_ai_timeline["date_basis"] = "SpaceX S-1/A and FWPs"
write(spacex_ai_timeline, "spacex_ai_timeline")


cursor_option_analysis = pd.DataFrame(
    [
        ("Status", "Not acquired as of S-1/A", "SpaceX has a collaboration and option, not completed ownership of Cursor."),
        ("Counterparty", "Anysphere, Inc. doing business as Cursor", "Private software company focused on AI-assisted coding workflows."),
        ("Agreement date", "2026-04", "Compute and option agreement entered in April 2026."),
        ("Compute agreement", "SpaceX provides certain GPU cluster compute capacity", "Cursor contributes personnel, data/datasets, documentation, technical know-how, workflows, prompts, specifications and code per FWP/S-1 disclosure."),
        ("Option", "Right, not obligation, to acquire Cursor", "Consideration would be SpaceX Class A stock based on Cursor implied equity value of $60.0B and SpaceX VWAP before closing."),
        ("Termination economics", "$1.5B termination fee plus $8.5B deferred services fee if applicable", "Fees payable in cash or Class A stock if the offering has not been consummated when payable."),
        ("Investor read", "Strategic upside with dilution/complexity risk", "Cursor could add developer distribution and model-training data, but it is not current owned revenue and should not be valued as a completed acquisition."),
    ],
    columns=["topic", "answer", "investor_read"],
)
write(cursor_option_analysis, "cursor_option_analysis")


quality_scores = pd.DataFrame(
    [
        ("SPCX", "SpaceX", "Subject", 4.5, 4.0, 4.5, 1.5, 3.0, "Elite execution and underwriting; penalized for control, related parties, AI losses and unlock overhang."),
        ("V", "Visa", "Core quality comp", 4.5, 5.0, 5.0, 4.0, 4.5, "Best-in-class scaled network IPO; cleaner governance and profitability than SpaceX."),
        ("CRWD", "CrowdStrike", "Core quality comp", 4.5, 4.5, 4.0, 4.0, 4.0, "Founder-led cybersecurity compounder with credible underwriting and strong public-market quality."),
        ("DDOG", "Datadog", "Core quality comp", 4.5, 4.5, 4.0, 4.0, 4.0, "High-quality founder-led software IPO with good governance and durable growth."),
        ("ABNB", "Airbnb", "Core quality comp", 4.5, 4.5, 4.5, 3.5, 4.0, "Founder-led platform with brand quality and strong IPO execution; dual-class governance but less extreme than SpaceX."),
        ("META", "Meta/Facebook", "Scale/control comp", 4.0, 5.0, 5.0, 2.5, 4.0, "Best scale and founder-control comp; weak early trading shows scarcity does not immunize valuation."),
        ("ARM", "Arm", "Scale/control comp", 4.0, 4.5, 4.5, 2.5, 4.0, "High-quality tech asset with parent-control overhang; useful float-scarcity comp."),
        ("UBER", "Uber", "Scale comp", 3.5, 4.0, 4.0, 3.5, 3.5, "Large institutional IPO; useful caution on valuation and post-listing profitability questions."),
        ("SNOW", "Snowflake", "Valuation caution comp", 4.0, 4.0, 4.5, 3.5, 3.0, "Great company, extreme valuation at IPO; useful for pop/fade and valuation discipline."),
        ("DASH", "DoorDash", "Valuation caution comp", 4.0, 3.5, 4.5, 3.0, 3.0, "Founder-led but cyclically expensive IPO; useful first-6-month caution."),
        ("RIVN", "Rivian", "Capital intensity caution comp", 3.0, 2.5, 4.0, 3.0, 2.0, "Institutional-scale but capex-heavy story IPO; useful negative comp for AI/Starship capex risk."),
        ("BABA", "Alibaba", "Liquidity-only comp", 3.5, 4.0, 5.0, 1.5, 3.0, "Mega IPO liquidity comp; not a clean U.S. governance comp due ADR/China/VIE issues."),
        ("COIN", "Coinbase", "Excluded from core", 4.0, 3.5, 1.0, 3.0, 2.5, "Large liquid listing, but direct listing with no primary IPO proceeds or lead underwriter."),
    ],
    columns=["ticker", "company", "inclusion_tier", "management_quality", "business_quality", "ipo_quality", "governance_quality", "market_setup", "note"],
)
weights = {
    "management_quality": 0.20,
    "business_quality": 0.25,
    "ipo_quality": 0.20,
    "governance_quality": 0.15,
    "market_setup": 0.20,
}
quality_scores["weighted_quality_score"] = sum(quality_scores[col] * w for col, w in weights.items())
write(quality_scores, "quality_scores")


comp_universe = pd.DataFrame(
    [
        ("SPCX", "SpaceX", "2026-06-12 expected trading", 75.0, 1765.7, "Primary IPO", "Goldman Sachs, Morgan Stanley; large global syndicate", "Subject", "Passes scale and underwriting; unique control and AI roll-up risk."),
        ("V", "Visa", "2008-03-19", 17.9, 42.0, "Primary IPO", "J.P. Morgan, Goldman Sachs, BofA", "Core", "Large, profitable, high-quality operating company."),
        ("META", "Meta/Facebook", "2012-05-18", 16.0, 104.0, "Primary IPO", "Morgan Stanley, J.P. Morgan, Goldman Sachs", "Core", "Founder-control and mega-liquidity comp."),
        ("BABA", "Alibaba", "2014-09-19", 21.8, 168.0, "Primary IPO / ADR", "Credit Suisse, Deutsche Bank, Goldman Sachs, J.P. Morgan, Morgan Stanley, Citi", "Scale only", "Largest historical IPO comp; governance/geography not clean."),
        ("UBER", "Uber", "2019-05-10", 8.1, 75.5, "Primary IPO", "Morgan Stanley, Goldman Sachs, BofA", "Core", "Large growth IPO with profitability debate."),
        ("ABNB", "Airbnb", "2020-12-10", 3.5, 47.0, "Primary IPO", "Morgan Stanley, Goldman Sachs", "Core", "Founder-led platform quality comp."),
        ("ARM", "Arm", "2023-09-14", 4.9, 54.5, "Primary IPO", "Barclays, Goldman Sachs, J.P. Morgan, Mizuho", "Core", "High-quality controlled-company float-scarcity comp."),
        ("SNOW", "Snowflake", "2020-09-16", 3.4, 33.0, "Primary IPO", "Goldman Sachs, Morgan Stanley, J.P. Morgan", "Core", "Quality company, valuation-risk comp."),
        ("DASH", "DoorDash", "2020-12-09", 3.4, 39.0, "Primary IPO", "Goldman Sachs, J.P. Morgan", "Core", "Founder-led but valuation-sensitive growth IPO."),
        ("RIVN", "Rivian", "2021-11-10", 11.9, 66.5, "Primary IPO", "Morgan Stanley, Goldman Sachs, J.P. Morgan", "Core", "Capital-intensity and story-stock caution comp."),
        ("CRWD", "CrowdStrike", "2019-06-12", 0.6, 6.8, "Primary IPO", "Goldman Sachs, J.P. Morgan, BofA, Barclays", "Core", "Passes lower bound; high-quality software/security comp."),
        ("DDOG", "Datadog", "2019-09-19", 0.6, 7.8, "Primary IPO", "Morgan Stanley, Goldman Sachs, J.P. Morgan", "Core", "Passes lower bound; high-quality software/infrastructure comp."),
        ("COIN", "Coinbase", "2021-04-14", 0.0, 85.8, "Direct listing", "None", "Excluded from core", "Useful retail/liquidity context, but no primary IPO proceeds or underwriting comp."),
        ("RDDT", "Reddit", "2024-03-21", 0.75, 6.4, "Primary IPO", "Morgan Stanley, Goldman Sachs, J.P. Morgan", "Excluded", "Passes market-cap floor but too retail/social-media specific for SpaceX core comp."),
        ("CAVA", "Cava", "2023-06-15", 0.37, 2.5, "Primary IPO", "J.P. Morgan, Jefferies, Citi", "Excluded", "Below $5B IPO market-cap filter."),
        ("CART", "Instacart/Maplebear", "2023-09-19", 0.66, 9.9, "Primary IPO", "Goldman Sachs, J.P. Morgan", "Excluded", "Weaker business-quality comparability and smaller offering."),
    ],
    columns=["ticker", "company", "ipo_date", "ipo_proceeds_usd_b", "ipo_market_cap_usd_b", "listing_type", "lead_underwriters", "inclusion", "rationale"],
)
comp_universe["approx_ipo_public_float_pct"] = (
    comp_universe["ipo_proceeds_usd_b"] / comp_universe["ipo_market_cap_usd_b"] * 100
).where(comp_universe["ipo_market_cap_usd_b"] > 0)
comp_universe.loc[comp_universe["listing_type"].str.contains("Direct", case=False), "approx_ipo_public_float_pct"] = pd.NA
comp_universe["float_note"] = "Approximate: IPO proceeds / IPO market cap, excluding over-allotment and secondary-seller details."
comp_universe.loc[comp_universe["ticker"] == "SPCX", "float_note"] = "Calculated from S-1/A base IPO shares / post-offering basic shares."
comp_universe.loc[comp_universe["ticker"] == "SPCX", "approx_ipo_public_float_pct"] = IPO_FLOAT_M / POST_TOTAL_M * 100
write(comp_universe, "comp_universe")


index_inclusion_rules = pd.DataFrame(
    [
        (
            "Nasdaq-100",
            "Fast Entry",
            "IPO can skip the normal three-full-calendar-month seasoning rule if its Full Market Capitalization ranks within the top 40 current Nasdaq-100 constituents. It is evaluated after the 7th trading day and typically added after 15 trading days, with announcement after the 10th trading day.",
            "Likely eligible if SPCX lists on an eligible Nasdaq market and no final filing changes the share count. At $1.77T basic market cap, the top-40 size test should not be the gating item.",
            "Creates a near-term QQQ/NDX flow catalyst around late June to early July 2026, not a day-one inclusion.",
            "Nasdaq-100 Index Methodology",
        ),
        (
            "Nasdaq-100",
            "Liquidity",
            "Standard liquidity screen is three-month ADVT of at least $5M. For IPO fast entry, ADVT is measured from first trading day through the applicable reference date.",
            "A $75B IPO should almost certainly clear $5M ADVT, but this cannot be final until trading occurs.",
            "Liquidity is a check-the-box risk, not the main risk.",
            "Nasdaq-100 Index Methodology",
        ),
        (
            "Nasdaq-100",
            "Free float",
            "No minimum free-float criterion. For low-float securities, index weighting uses the lesser of reported TSO or 3x free-floating shares.",
            f"Base IPO float is {IPO_FLOAT_M:.1f}M shares, or {IPO_FLOAT_M / POST_TOTAL_M * 100:.2f}% of basic shares. Initial NDX modified market cap is about ${min(POST_A_M, IPO_FLOAT_M * 3) * IPO_PRICE / 1000:.1f}B, not the full ${POST_TOTAL_M * IPO_PRICE / 1000:.1f}B company value.",
            "The rule allows inclusion but scales the starting weight to tradable supply. This reduces, but does not eliminate, forced-buy pressure.",
            "Nasdaq-100 Index Methodology",
        ),
        (
            "Nasdaq-100",
            "Quarterly path",
            "The updated framework adds rank-based quarterly reviews in March, June and September, plus the annual December reconstitution.",
            "If fast entry were missed for an operational reason, the next scheduled framework matters. The first quarterly rebalance under the new rules is June 22, 2026.",
            "Index demand can arrive in tranches rather than only at December reconstitution.",
            "Nasdaq methodology update",
        ),
        (
            "S&P 500",
            "Seasoning",
            "IPOs should trade on an eligible exchange for at least 12 months before consideration for S&P Composite 1500 inclusion. No IPO fast track is allowed for S&P Composite 1500 candidates.",
            "Assuming first trade on June 12, 2026, the earliest simple seasoning date is June 12, 2027. This is only a possible consideration date, not an inclusion guarantee.",
            "No S&P 500 forced-buy catalyst in the first six months.",
            "S&P U.S. Indices Methodology; S&P MegaCap consultation results",
        ),
        (
            "S&P 500",
            "Financial viability",
            "GAAP net income from continuing operations must be positive for the most recent quarter and for the sum of the most recent four consecutive quarters.",
            "SpaceX reported a 2025 net loss and a Q1 2026 net loss. It does not currently clear the profitability screen.",
            "Even after 12 months, S&P 500 inclusion likely requires a demonstrated profit turn.",
            "S&P U.S. Indices Methodology; S&P MegaCap consultation results",
        ),
        (
            "S&P 500",
            "Float and liquidity",
            "S&P Composite 1500 additions require IWF of at least 0.10, security-level FMC of at least 50% of the index market-cap threshold, FALR of at least 0.75, and at least 250,000 shares traded in each of the six months before evaluation.",
            f"Base IPO float is only {IPO_FLOAT_M / POST_TOTAL_M * 100:.2f}% of basic shares, below the 10% IWF screen if only IPO shares count. Lock-up releases could change this later.",
            "Float unlocks matter for S&P eligibility, but they also create supply risk.",
            "S&P U.S. Indices Methodology; S&P MegaCap consultation results",
        ),
        (
            "S&P Total Market / Dow Jones U.S. Total Stock Market",
            "Mega-cap broad-index update",
            "Effective June 8, 2026, broad-market indices allow an alternative IWF path for mega-cap companies and preserve IPO fast-track treatment when all other criteria are met.",
            f"Base float-adjusted market cap is about ${IPO_FLOAT_M * IPO_PRICE / 1000:.1f}B, so broad-index eligibility may arrive much earlier than S&P 500 eligibility.",
            "Potential total-market ETF flow is relevant, but it should not be confused with S&P 500 membership.",
            "S&P MegaCap consultation results",
        ),
    ],
    columns=["index", "rule_area", "rule", "spacex_read", "first_6m_model_impact", "source"],
)
write(index_inclusion_rules, "index_inclusion_rules")


index_inclusion_timeline = pd.DataFrame(
    [
        ("First trade assumption", "SPCX begins trading", FIRST_TRADE_DATE_ASSUMPTION.isoformat(), "Assumption based on June 2026 launch timing; update once 424B4/final exchange notice is filed."),
        ("Nasdaq-100 IPO reference date", "7th trading day evaluation", nth_trading_day(FIRST_TRADE_DATE_ASSUMPTION, 7), "Full market cap top-40 test and fast-entry eligibility check."),
        ("Nasdaq-100 announcement window", "10th trading day announcement", nth_trading_day(FIRST_TRADE_DATE_ASSUMPTION, 10), "Methodology says announcement typically occurs after close on the 10th trading day."),
        ("Nasdaq-100 addition window", "15th trading day typical addition", nth_trading_day(FIRST_TRADE_DATE_ASSUMPTION, 15), "Methodology says IPO fast-entry addition typically occurs after 15 trading days; effective date can depend on notice conventions."),
        ("S&P broad-index fast-track", "S&P TMI / Dow Jones TSM possible fast-track", "TBD", "Depends on S&P DJI announcement and all applicable criteria; this is not S&P 500."),
        ("S&P 500 earliest seasoning date", "12 months after first trade", date(2027, 6, 12).isoformat(), "Only a possible consideration date. Profitability, IWF, liquidity and committee selection still apply."),
    ],
    columns=["event", "description", "model_date", "note"],
)
write(index_inclusion_timeline, "index_inclusion_timeline")


comp_perf = pd.DataFrame(
    [
        ("META", "2012-05-18", 37.93, -11.0, -16.5, -50.2, -40.0),
        ("BABA", "2014-09-19", 89.17, -4.3, -6.0, 16.4, -10.3),
        ("V", "2008-03-19", 12.42, 13.9, 22.1, 48.4, 13.6),
        ("UBER", "2019-05-10", 41.57, -10.8, 2.1, -3.7, -34.1),
        ("ABNB", "2020-12-10", 144.71, -3.8, 11.1, 45.1, 3.1),
        ("ARM", "2023-09-14", 63.59, -4.5, -20.1, 3.2, 99.7),
        ("SNOW", "2020-09-16", 253.93, -10.4, -5.1, 29.4, -14.7),
        ("DASH", "2020-12-09", 189.51, -1.9, -11.9, -25.1, -18.7),
        ("RIVN", "2021-11-10", 100.73, 22.1, 13.8, -35.7, -75.9),
        ("CRWD", "2019-06-12", 58.00, 16.5, 26.7, 19.2, -18.0),
        ("DDOG", "2019-09-19", 37.55, -3.7, -15.9, 1.8, -11.1),
    ],
    columns=["ticker", "first_trade_date", "first_close_adj_usd", "return_from_first_close_1d_pct", "return_from_first_close_1m_pct", "return_from_first_close_3m_pct", "return_from_first_close_6m_pct"],
)
comp_perf["source"] = "yfinance adjusted close downloaded 2026-06-08; returns start at first listed close, not IPO allocation price"
write(comp_perf, "comp_ipo_performance")


ipo_chase_base_rate = pd.DataFrame(
    [
        (30, 760, 53.2, 0.2, -2.1, -1.9, 39.0),
        (90, 731, 52.8, 0.3, -1.6, -6.6, 29.0),
        (180, 641, 47.6, -1.1, -11.3, -15.4, 25.0),
        (365, 474, 45.6, -4.1, -16.2, -28.4, 19.0),
    ],
    columns=["horizon_days", "n", "positive_pct", "median_abs_return_pct", "mean_abs_return_pct", "median_excess_vs_spy_pct", "beat_spy_pct"],
)
ipo_chase_base_rate["source"] = "YehCapital study 15; day-1-close entries for 760 US IPOs since 2022-10"
write(ipo_chase_base_rate, "ipo_chase_base_rate")


ipo_chase_sector_base_rate = pd.DataFrame(
    [
        ("Software / IT", 30, 65.5, 3.4, 9.1, "Survivor bucket in study 15; closest public-market analogue to profitable infrastructure/software quality."),
        ("Real Estate / REIT", 192, 79.8, 1.0, 4.9, "Survivor bucket but not comparable to SpaceX business quality or capital cycle."),
        ("Biotech / Pharma", 53, 32.1, -13.0, -30.3, "Explicitly excluded from the SpaceX comp set."),
        ("Industrials", 21, 47.4, -4.7, -63.4, "Too small/noisy as a broad bucket; not a mega-cap aerospace/space comp."),
        ("Micro-cap / unclassified", 324, 43.8, -8.3, -63.7, "Explicitly excluded from the SpaceX comp set."),
    ],
    columns=["sector", "n", "positive_90d_pct", "median_90d_return_pct", "median_365d_return_pct", "spacex_model_read"],
)
ipo_chase_sector_base_rate["source"] = "YehCapital study 15 sector table"
write(ipo_chase_sector_base_rate, "ipo_chase_sector_base_rate")


combined_ipo_decision_bridge = pd.DataFrame(
    [
        (
            "Broad IPO prior",
            "Study 15",
            "Day-1-close IPO chasing is a negative base-rate trade.",
            "365d median excess vs SPY -28.4%; only 19% beat SPY.",
            "Start from skepticism; do not buy SpaceX just because the IPO is famous.",
        ),
        (
            "Quality filter",
            "Study 24",
            "Small/noisy IPOs are removed; only institutional-scale comps remain.",
            f"Filtered 6m comp median from first close {comp_perf['return_from_first_close_6m_pct'].median():.1f}%.",
            "Quality filter reduces junk risk but still leaves post-IPO fade risk.",
        ),
        (
            "Scarcity and index flow",
            "Study 24",
            "SpaceX has unusually tight immediate tradable supply plus a Nasdaq-100 fast-entry path.",
            f"Immediate float {IPO_FLOAT_M / POST_TOTAL_M * 100:.2f}%; Nasdaq low-float modified market cap about ${min(POST_A_M, IPO_FLOAT_M * 3) * IPO_PRICE / 1000:.0f}B.",
            "Treat early upside as flow/scarcity, not proof of long-term entry quality.",
        ),
        (
            "Unlock and governance penalty",
            "Study 24",
            "First-six-month releases, Musk control and registration-rights overhang cap public-entry quality.",
            "Q2/Q3 earnings unlocks plus 70/90/105/120/135/180-day releases are multiples of IPO float.",
            "Wait for unlock absorption before underwriting a larger long-term position.",
        ),
    ],
    columns=["layer", "source", "finding", "key_number", "spacex_decision_rule"],
)
write(combined_ipo_decision_bridge, "combined_ipo_decision_bridge")


underwriter_quality = pd.DataFrame(
    [
        ("Goldman Sachs", "Joint bookrunner / lead-left group", 5.0, "Top-tier mega-cap IPO franchise and stabilization credibility."),
        ("Morgan Stanley", "Joint bookrunner / lead-left group", 5.0, "Top-tier technology IPO franchise; stabilization agent per S-1/A."),
        ("BofA Securities", "Joint bookrunner", 4.5, "Top global distribution and lending relationship."),
        ("Citigroup", "Joint bookrunner", 4.5, "Top global distribution; strong cross-border reach."),
        ("J.P. Morgan", "Joint bookrunner", 4.5, "Top global equity capital markets franchise."),
        ("Barclays", "Joint bookrunner", 4.0, "Strong global technology/industrial ECM distribution."),
        ("Deutsche Bank Securities", "Joint bookrunner", 3.5, "Global bank; useful international distribution."),
        ("Wells Fargo Securities", "Bookrunner", 3.5, "Large U.S. distribution and lending relationship."),
        ("Allen & Company", "Bookrunner", 4.0, "Elite tech/media relationship bank; narrower distribution."),
        ("Cantor", "Bookrunner", 3.0, "Distribution support; not lead franchise."),
        ("Needham", "Bookrunner", 3.0, "Growth/technology distribution support."),
        ("Raymond James", "Bookrunner", 3.0, "Retail and middle-market distribution support."),
        ("Societe Generale", "Bookrunner", 3.0, "European distribution support."),
        ("Stifel", "Bookrunner", 3.0, "Retail and growth distribution support."),
        ("William Blair", "Bookrunner", 3.0, "Growth-company distribution support."),
        ("BTG Pactual", "Bookrunner", 2.5, "Latin America distribution support."),
        ("ING", "Bookrunner", 2.5, "European distribution support."),
        ("Macquarie Capital", "Bookrunner", 2.5, "Asia-Pacific/infrastructure distribution support."),
        ("Mirae Asset Securities", "Bookrunner", 2.5, "Asia distribution support."),
        ("Mizuho", "Bookrunner", 3.0, "Japan/global distribution support."),
        ("Santander", "Bookrunner", 2.5, "European/Latin America distribution support."),
    ],
    columns=["underwriter", "role", "quality_score", "note"],
)
write(underwriter_quality, "underwriter_quality")


segment_quality = pd.DataFrame(
    [
        ("Space", 4.086, -0.657, 0.653, 3.832, 0.619, -0.662, -0.351, 1.052, 4.0, "Launch cadence and vertical integration are elite; still loss-making in Q1 and Starship execution is key."),
        ("Connectivity", 11.387, 4.423, 7.168, 4.178, 3.257, 1.188, 2.087, 1.332, 4.5, "Best current business: 2025 operating margin 38.8%, subscribers 8.9M at year-end and 10.3M Q1 2026; ARPU declining from $99 in 2023 to $66 Q1 2026."),
        ("AI/xAI/X", 3.201, -6.355, -1.237, 12.727, 0.818, -2.469, -0.609, 7.723, 2.5, "Biggest upside and biggest quality penalty: $12.7B 2025 capex, large operating losses, related-party and regulatory complexity; Anthropic/Google contracts improve revenue visibility but are terminable."),
    ],
    columns=["segment", "revenue_2025_usd_b", "operating_income_2025_usd_b", "adjusted_ebitda_2025_usd_b", "capex_2025_usd_b", "revenue_q1_2026_usd_b", "operating_income_q1_2026_usd_b", "adjusted_ebitda_q1_2026_usd_b", "capex_q1_2026_usd_b", "business_quality_score", "note"],
)
segment_quality["operating_margin_2025_pct"] = segment_quality["operating_income_2025_usd_b"] / segment_quality["revenue_2025_usd_b"] * 100
segment_quality["capex_to_revenue_2025_pct"] = segment_quality["capex_2025_usd_b"] / segment_quality["revenue_2025_usd_b"] * 100
write(segment_quality, "segment_quality")


valuation_rows = []
for revenue_case, revenue_b in [
    ("2025 reported revenue", 18.674),
    ("Q1 2026 annualized", 4.694 * 4),
    ("2025 revenue + Anthropic annualized run-rate", 18.674 + 1.25 * 12),
    ("2025 revenue + Anthropic + Google annualized run-rate", 18.674 + 1.25 * 12 + 0.92 * 12),
]:
    valuation_rows.append(
        {
            "case": revenue_case,
            "revenue_usd_b": revenue_b,
            "implied_market_cap_usd_b": POST_TOTAL_M * IPO_PRICE / 1000,
            "price_to_sales_x": (POST_TOTAL_M * IPO_PRICE / 1000) / revenue_b,
            "note": "Contract run-rate cases are not risk-adjusted; Anthropic/Google contracts are terminable and delivery-dependent.",
        }
    )
valuation_sensitivity = pd.DataFrame(valuation_rows)
write(valuation_sensitivity, "valuation_sensitivity")


excluded_comps = pd.DataFrame(
    [
        ("Small IPOs", "Excluded", "Below $5B IPO market cap or below $500M proceeds."),
        ("SPACs/de-SPACs", "Excluded", "Different incentives, redemption mechanics and sponsor economics."),
        ("Biotech binary names", "Excluded", "Clinical-binary risk is not comparable to SpaceX."),
        ("Firefly Aerospace", "Context only", "Useful space-sector context, not a SpaceX-scale valuation or liquidity comp."),
        ("Reddit", "Excluded from core", "Passes size floor but retail/social-media profile would overweight meme-demand mechanics."),
        ("Instacart", "Excluded from core", "Not small by market cap, but lower-quality business comparability and smaller offering."),
        ("Coinbase", "Context only", "Large direct listing, but no primary proceeds and no lead-underwriter execution."),
    ],
    columns=["group_or_company", "treatment", "reason"],
)
write(excluded_comps, "excluded_comps")


# Charts
plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(10, 5.5))
plot_df = lockup_first_6m_scenarios.copy()
labels = [
    "IPO\n2026-06-11",
    "Q2 earn.\nTBD Aug 2026",
    "Perf.\nTBD Aug 2026",
    "D70\n2026-08-20",
    "D90\n2026-09-09",
    "D91\n2026-09-10",
    "D105\n2026-09-24",
    "D120\n2026-10-09",
    "D135\n2026-10-24",
    "Q3 earn.\nTBD Nov 2026",
    "D180\n2026-12-08",
]
x = range(len(plot_df))
ax.plot(x, plot_df["cumulative_perf_case_x_ipo_float"], marker="o", linewidth=2.2, label="performance trigger")
ax.plot(x, plot_df["cumulative_no_perf_case_x_ipo_float"], marker="o", linewidth=2.2, label="no performance trigger")
ax.axhline(1.0, color="#d62728", linestyle="--", linewidth=1.4, label="IPO float")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, rotation=35, ha="right")
ax.set_ylabel("Circulating free float / base IPO float")
ax.set_title("SpaceX first-six-month circulating free-float scenarios")
ax.legend(loc="upper left")
for idx in [0, 1, 2, 9, 10]:
    y_val = plot_df.loc[idx, "cumulative_perf_case_x_ipo_float"]
    ax.text(idx, y_val + 0.18, f"{y_val:.1f}x", ha="center", fontsize=8)
fig.tight_layout()
fig.savefig(ROOT / "fig1_first_6m_float_unlocks.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
qs = quality_scores[quality_scores["inclusion_tier"] != "Excluded from core"].sort_values("weighted_quality_score")
colors = ["#d62728" if t == "SPCX" else "#2ca02c" if "Core" in tier else "#7f7f7f" for t, tier in zip(qs["ticker"], qs["inclusion_tier"])]
ax.barh(qs["ticker"], qs["weighted_quality_score"], color=colors)
ax.set_xlim(0, 5)
ax.set_xlabel("Weighted quality score (1-5)")
ax.set_title("Filtered IPO quality scores")
fig.tight_layout()
fig.savefig(ROOT / "fig2_quality_scores.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
perf = comp_perf.sort_values("return_from_first_close_6m_pct")
ax.barh(perf["ticker"], perf["return_from_first_close_6m_pct"], color=["#d62728" if x < 0 else "#2ca02c" for x in perf["return_from_first_close_6m_pct"]])
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("6-month return from first listed close, %")
ax.set_title("Large IPO comp 6-month trading outcomes")
fig.tight_layout()
fig.savefig(ROOT / "fig3_comp_6m_returns.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
index_caps = pd.DataFrame(
    [
        ("Full market cap\neligibility", POST_TOTAL_M * IPO_PRICE / 1000),
        ("Nasdaq-100\nmodified cap", min(POST_A_M, IPO_FLOAT_M * 3) * IPO_PRICE / 1000),
        ("S&P float-adjusted\nbase cap", IPO_FLOAT_M * IPO_PRICE / 1000),
    ],
    columns=["measure", "usd_b"],
)
ax.bar(index_caps["measure"], index_caps["usd_b"], color=["#7f7f7f", "#1f77b4", "#ff7f0e"])
ax.set_ylabel("USD billions")
ax.set_title("Index eligibility size vs tradable-float weighting")
for idx, row in index_caps.iterrows():
    ax.text(idx, row["usd_b"], f"${row['usd_b']:.0f}B", ha="center", va="bottom")
fig.tight_layout()
fig.savefig(ROOT / "fig4_index_inclusion_float_math.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
bridge_bars = pd.DataFrame(
    [
        ("Study 15\nall IPOs\n180d excess", ipo_chase_base_rate.loc[ipo_chase_base_rate["horizon_days"] == 180, "median_excess_vs_spy_pct"].iloc[0]),
        ("Filtered comps\n6m median", comp_perf["return_from_first_close_6m_pct"].median()),
        ("Filtered comps\nbest case", comp_perf["return_from_first_close_6m_pct"].max()),
        ("Filtered comps\nworst case", comp_perf["return_from_first_close_6m_pct"].min()),
    ],
    columns=["measure", "return_pct"],
)
ax.bar(
    bridge_bars["measure"],
    bridge_bars["return_pct"],
    color=["#d62728" if v < 0 else "#2ca02c" for v in bridge_bars["return_pct"]],
)
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Return / excess return, %")
ax.set_title("Study 15 IPO-chase prior vs filtered large IPO comps")
for idx, row in bridge_bars.iterrows():
    va = "bottom" if row["return_pct"] >= 0 else "top"
    offset = 1.5 if row["return_pct"] >= 0 else -1.5
    ax.text(idx, row["return_pct"] + offset, f"{row['return_pct']:.1f}%", ha="center", va=va)
fig.tight_layout()
fig.savefig(ROOT / "fig5_study15_base_rate_bridge.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
pool_plot = lockup_supply_summary[lockup_supply_summary["pool"].isin([
    "Immediate IPO float",
    "180-day lock-up pool before affiliate timing",
    "Extended lock-up excluding Musk",
    "Musk 366-day lock-up",
])].copy()
ax.barh(pool_plot["pool"], pool_plot["x_base_ipo_float"], color=["#1f77b4", "#ff7f0e", "#7f7f7f", "#d62728"])
ax.set_xlabel("Shares / base IPO float")
ax.set_title("Lock-up pools as multiples of the IPO float")
for idx, row in pool_plot.reset_index(drop=True).iterrows():
    ax.text(row["x_base_ipo_float"] + 0.2, idx, f"{row['x_base_ipo_float']:.1f}x", va="center")
fig.tight_layout()
fig.savefig(ROOT / "fig6_lockup_pool_ratios.png", dpi=180)
plt.close(fig)


workbook_path = ROOT / "spacex_ipo_quality_model.xlsx"
with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
    for name in [
        "sources",
        "offering_math",
        "shareholder_ratios",
        "tesla_spacex_related_parties",
        "lockup_calendar",
        "lockup_supply_summary",
        "lockup_first_6m_scenarios",
        "lockup_free_float_bridge",
        "nasdaq_explainer",
        "spacex_business_breakdown",
        "spacex_ai_timeline",
        "cursor_option_analysis",
        "quality_scores",
        "comp_universe",
        "comp_ipo_performance",
        "ipo_chase_base_rate",
        "ipo_chase_sector_base_rate",
        "combined_ipo_decision_bridge",
        "underwriter_quality",
        "segment_quality",
        "valuation_sensitivity",
        "excluded_comps",
        "index_inclusion_rules",
        "index_inclusion_timeline",
    ]:
        pd.read_csv(DATA / f"{name}.csv").to_excel(writer, sheet_name=name[:31], index=False)
    ws = writer.book.create_sheet("summary")
    ws["A1"] = "SpaceX IPO model stance"
    ws["A2"] = "Trade-only / wait-for-unlock bias at IPO valuation."
    ws["A4"] = "Key numbers"
    ws["A5"] = "Immediate base free float"
    ws["B5"] = f"{IPO_FLOAT_M:.1f}M shares ({IPO_FLOAT_M / POST_TOTAL_M * 100:.2f}% of basic shares)"
    ws["A6"] = "Implied basic market cap"
    ws["B6"] = f"${POST_TOTAL_M * IPO_PRICE / 1000:.1f}B"
    ws["A7"] = "Class B voting power"
    ws["B7"] = "88.5%"
    ws["A8"] = "Musk combined voting power"
    ws["B8"] = "84.4% after offering per S-1/A table"
    ws["A9"] = "First-six-month issue"
    ws["B9"] = "IPO float scarcity can support the tape, but cumulative tradable supply reaches about 9.4x IPO float by day 180 in both release scenarios."
    ws["A10"] = "Nasdaq-100 path"
    ws["B10"] = "Fast Entry can evaluate a mega IPO on trading day 7 and typically add after trading day 15; low-float weight is capped at 3x free float."
    ws["A11"] = "S&P 500 path"
    ws["B11"] = "No mega-cap fast track: 12-month IPO seasoning, positive GAAP income screens and IWF/liquidity screens remain."
    ws["A12"] = "Day-180 lock-up ratio"
    ws["B12"] = "Performance case: 5.23B shares / 9.42x IPO float / 40.0% of basic shares. No-performance case: 5.25B shares / 9.44x / 40.1%."

print(f"Wrote {workbook_path}")
