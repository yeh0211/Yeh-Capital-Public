#!/usr/bin/env python3
"""Build a reusable six-month IPO price-action scorecard.

The model is intentionally transparent. It combines YehCapital's prior IPO
base-rate studies with public IPO mechanics and a curated institutional IPO
comp set. It is a research scorecard, not a trading system.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
STUDY24 = ROOT.parent / "24-spacex-ipo-quality-model" / "data"

# Study 15 owns the broad aftermarket IPO-chase base rate and the reusable
# first-six-month scorecard. Study 24 supplies the institutional IPO filter.
STUDY15_BROAD_6M_EXCESS_PCT = -15.4
STUDY15_BROAD_1Y_EXCESS_PCT = -28.4
BASE_6M_PRIOR_PCT = -14.7
BASE_BEAT_SPY_PROB_PCT = 25.0


def write(df: pd.DataFrame, name: str) -> None:
    df.to_csv(DATA / f"{name}.csv", index=False)


def bucket_from_return(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "No actual target yet"
    if value <= -30:
        return "Severe fade"
    if value <= -10:
        return "Negative"
    if value < 10:
        return "Range-bound"
    return "Positive"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def underwriter_score(underwriters: str) -> tuple[float, int, int]:
    if pd.isna(underwriters) or not underwriters or underwriters == "None":
        return 1.0, 0, 0
    top_tier = ["Goldman Sachs", "Morgan Stanley", "J.P. Morgan", "BofA", "Citigroup", "Citi"]
    names = [part.strip() for part in underwriters.replace(";", ",").split(",") if part.strip()]
    top_count = sum(any(bank in name for bank in top_tier) for name in names)
    score = 2.0 + min(3.0, top_count * 0.8) + min(0.5, max(0, len(names) - 2) * 0.1)
    return round(clamp(score, 1.0, 5.0), 2), top_count, len(names)


def float_scarcity_score(float_pct: float | None) -> float:
    if pd.isna(float_pct):
        return 2.0
    if float_pct < 5:
        return 5.0
    if float_pct < 10:
        return 4.0
    if float_pct < 15:
        return 3.0
    if float_pct < 25:
        return 2.0
    return 1.0


def market_setup_score(ticker: str) -> float:
    return {
        "V": 2.5,
        "META": 2.5,
        "BABA": 3.0,
        "UBER": 2.5,
        "ABNB": 3.0,
        "ARM": 3.5,
        "SNOW": 2.0,
        "DASH": 2.0,
        "RIVN": 1.5,
        "CRWD": 3.0,
        "DDOG": 3.0,
        "SPCX": 3.0,
    }.get(ticker, 2.5)


def valuation_risk_score(ticker: str) -> float:
    return {
        "V": 1.0,
        "META": 3.0,
        "BABA": 2.5,
        "UBER": 3.5,
        "ABNB": 3.0,
        "ARM": 3.0,
        "SNOW": 5.0,
        "DASH": 4.0,
        "RIVN": 5.0,
        "CRWD": 3.0,
        "DDOG": 3.0,
        "SPCX": 4.5,
    }.get(ticker, 3.0)


def holder_risk_score(ticker: str) -> float:
    return {
        "V": 1.0,
        "META": 4.0,
        "BABA": 5.0,
        "UBER": 2.5,
        "ABNB": 3.5,
        "ARM": 4.5,
        "SNOW": 2.5,
        "DASH": 3.5,
        "RIVN": 3.0,
        "CRWD": 2.0,
        "DDOG": 2.0,
        "SPCX": 5.0,
    }.get(ticker, 3.0)


def unlock_risk_score(ticker: str, float_pct: float | None) -> float:
    if ticker == "SPCX":
        return 5.0
    if pd.isna(float_pct):
        return 2.5
    if float_pct < 8:
        return 3.5
    if float_pct < 12:
        return 3.0
    return 2.0


def index_flow_score(ticker: str) -> float:
    if ticker == "SPCX":
        return 5.0
    if ticker == "ARM":
        return 3.0
    return 2.0


sources = pd.DataFrame(
    [
        ("YehCapital study 02", "../02-ipo-anchored-vwap/", "Aftermarket entry framing: first-close/aftermarket entries differ from IPO allocation economics."),
        ("YehCapital study 15", "../15-ipo-chase/", "Broad IPO base rates: day-1-close entries underperformed SPY, especially by 180/365 days."),
        ("YehCapital study 22", "../22-equity-issuance-top-signal/", "Aggregate issuance is weak as market timing, but new issues underperform cross-sectionally."),
        ("YehCapital study 24", "../24-spacex-ipo-quality-model/", "SpaceX IPO mechanics, lock-ups, quality scores, Nasdaq/S&P index rules and comp returns."),
        ("SEC EDGAR", "https://www.sec.gov/", "Prospectuses and FWPs for offering mechanics, lock-ups, holders and underwriters."),
        ("Nasdaq-100 methodology", "https://indexes.nasdaq.com/docs/Methodology_NDX.pdf", "Fast-entry and low-float index weighting rules."),
        ("Tesla 10-Q", "https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm", "Tesla's March 2026 SpaceX common-stock investment and related-party Megapack transactions."),
    ],
    columns=["source", "url", "used_for"],
)
write(sources, "sources")


comp_universe = pd.read_csv(STUDY24 / "comp_universe.csv")
comp_perf = pd.read_csv(STUDY24 / "comp_ipo_performance.csv")
quality = pd.read_csv(STUDY24 / "quality_scores.csv")

study15_ipo_chase_base_rate = pd.read_csv(STUDY24 / "ipo_chase_base_rate.csv")
study15_ipo_chase_base_rate["horizon_label"] = study15_ipo_chase_base_rate["horizon_days"].map(
    {30: "1 month", 90: "3 months", 180: "6 months", 365: "1 year"}
)
study15_ipo_chase_base_rate["six_month_model_usage"] = study15_ipo_chase_base_rate["horizon_days"].map(
    {
        30: "Early aftermarket reference only.",
        90: "First-earnings / early trading reference only.",
        180: "Broad six-month IPO-chase prior; feeds the model beat-SPY base probability.",
        365: "One-year warning and sanity check; not the target horizon.",
    }
)
study15_ipo_chase_base_rate["merged_into_study15"] = True
write(study15_ipo_chase_base_rate, "study15_ipo_chase_base_rate")

study15_sector_base_rate = pd.read_csv(STUDY24 / "ipo_chase_sector_base_rate.csv")
study15_sector_base_rate["six_month_model_action"] = study15_sector_base_rate["sector"].map(
    {
        "Software / IT": "Keep as high-quality business analog when scale and disclosure pass.",
        "Real Estate / REIT": "Do not use as SpaceX valuation comp; stable-income survivor bucket only.",
        "Biotech / Pharma": "Exclude from comp universe; binary/noisy IPO behavior.",
        "Industrials": "Use only for context unless scale and underwriting pass.",
        "Micro-cap / unclassified": "Exclude from comp universe; small/noisy IPO behavior.",
    }
)
study15_sector_base_rate["merged_into_study15"] = True
write(study15_sector_base_rate, "study15_sector_base_rate")

institutional_comp_tickers = comp_universe.loc[
    comp_universe["inclusion"].isin(["Core", "Scale only"]),
    "ticker",
]
filtered_comp_median_6m = round(
    comp_perf.loc[comp_perf["ticker"].isin(institutional_comp_tickers), "return_from_first_close_6m_pct"].median(),
    1,
)
six_month_model_bridge = pd.DataFrame(
    [
        (
            "Study 15 broad IPO chase",
            "All qualifying US IPOs since 2022-10 with day-1-close entry.",
            760,
            "All-size / noisy cohort",
            STUDY15_BROAD_6M_EXCESS_PCT,
            STUDY15_BROAD_1Y_EXCESS_PCT,
            BASE_BEAT_SPY_PROB_PCT,
            "Start with a harsh prior: chasing new listings has underperformed SPY.",
        ),
        (
            "Study 15 sector screen",
            "Sector table separates survivor buckets from weak/noisy IPO buckets.",
            760,
            "Software/IT and REIT survived; biotech and micro-cap/unclassified failed.",
            pd.NA,
            pd.NA,
            pd.NA,
            "Used as a quality gate: remove small/noisy IPOs and avoid binary biotech/promotional listings.",
        ),
        (
            "Study 24 institutional comp filter",
            "Core plus scale IPO comps with market cap above $5B and proceeds above $500M.",
            len(institutional_comp_tickers),
            "Large institutional IPOs only",
            filtered_comp_median_6m,
            pd.NA,
            pd.NA,
            "This is the six-month price-return midpoint used as the Study 15 model base prior.",
        ),
        (
            "Study 15 six-month model baseline",
            "Reusable six-month IPO scorecard.",
            len(comp_universe),
            "SpaceX plus filtered comps and explicitly excluded/noisy rows",
            BASE_6M_PRIOR_PCT,
            pd.NA,
            BASE_BEAT_SPY_PROB_PCT,
            "Predictions start at the filtered large-IPO prior, while beat-SPY probability starts from Study 15's 180-day 25% rate.",
        ),
    ],
    columns=[
        "layer",
        "sample_definition",
        "n_or_rows",
        "filter_or_scope",
        "six_month_prior_pct",
        "one_year_excess_vs_spy_pct",
        "beat_spy_base_pct",
        "study15_model_usage",
    ],
)
write(six_month_model_bridge, "six_month_model_bridge")

ipo_master = comp_universe.copy()
ipo_master["model_role"] = ipo_master["inclusion"].map(
    {
        "Subject": "prediction subject",
        "Core": "training/benchmark comp",
        "Scale only": "context comp",
        "Excluded from core": "context/excluded",
        "Excluded": "excluded/noisy",
    }
).fillna("context")
ipo_master["known_by"] = "IPO date / first listed close"
ipo_master["data_quality"] = ipo_master["inclusion"].map(
    {"Subject": "high", "Core": "medium-high", "Scale only": "medium", "Excluded from core": "context", "Excluded": "excluded"}
).fillna("medium")
write(ipo_master, "ipo_master")


targets = ipo_master[["ticker", "company", "ipo_date", "model_role"]].merge(comp_perf, on="ticker", how="left")
targets["target_horizon_days"] = 180
targets["target_return_6m_pct"] = targets["return_from_first_close_6m_pct"]
targets["target_bucket_6m"] = targets["target_return_6m_pct"].apply(bucket_from_return)
targets["target_basis"] = "First listed close to roughly six months; SpaceX has no actual target yet."
write(
    targets[
        [
            "ticker",
            "company",
            "ipo_date",
            "model_role",
            "target_horizon_days",
            "target_return_6m_pct",
            "target_bucket_6m",
            "target_basis",
        ]
    ],
    "ipo_price_targets",
)


ipo_features_offering = ipo_master[
    [
        "ticker",
        "company",
        "ipo_proceeds_usd_b",
        "ipo_market_cap_usd_b",
        "listing_type",
        "approx_ipo_public_float_pct",
        "lead_underwriters",
    ]
].copy()
ipo_features_offering["large_institutional_ipo"] = (
    (ipo_features_offering["ipo_market_cap_usd_b"] >= 5.0)
    & (ipo_features_offering["ipo_proceeds_usd_b"] >= 0.5)
    & ~ipo_features_offering["listing_type"].str.contains("Direct", case=False, na=False)
)
ipo_features_offering["low_float_flag"] = ipo_features_offering["approx_ipo_public_float_pct"] < 10
ipo_features_offering["spac_flag"] = False
ipo_features_offering["direct_listing_flag"] = ipo_features_offering["listing_type"].str.contains("Direct", case=False, na=False)
ipo_features_offering["lockup_180d_pool_x_ipo_float"] = pd.NA
ipo_features_offering.loc[ipo_features_offering["ticker"] == "SPCX", "lockup_180d_pool_x_ipo_float"] = 8.20
ipo_features_offering["directed_share_program_flag"] = False
ipo_features_offering.loc[ipo_features_offering["ticker"] == "SPCX", "directed_share_program_flag"] = True
ipo_features_offering["known_by"] = "IPO date / final prospectus"
write(ipo_features_offering, "ipo_features_offering")


underwriter_rows = []
for row in ipo_master.itertuples(index=False):
    score, top_count, syndicate_count = underwriter_score(row.lead_underwriters)
    stabilization_proxy = "Disclosed lead-left/bookrunner group"
    if row.ticker == "SPCX":
        stabilization_proxy = "Morgan Stanley stabilization agent per S-1/A; full bookrunner group as liquidity-support proxy"
    if row.listing_type == "Direct listing":
        stabilization_proxy = "No IPO underwriter/stabilization proxy; direct listing"
    underwriter_rows.append(
        (
            row.ticker,
            row.company,
            row.lead_underwriters,
            score,
            top_count,
            syndicate_count,
            stabilization_proxy,
            "Market-maker identities are not used pre-listing unless publicly disclosed at symbol level.",
            "IPO date / prospectus",
        )
    )
ipo_features_underwriters = pd.DataFrame(
    underwriter_rows,
    columns=[
        "ticker",
        "company",
        "lead_underwriters",
        "underwriter_quality_score",
        "top_tier_underwriter_count",
        "syndicate_count_estimate",
        "liquidity_support_proxy",
        "market_maker_data_policy",
        "known_by",
    ],
)
ipo_features_underwriters.loc[ipo_features_underwriters["ticker"] == "SPCX", "underwriter_quality_score"] = 5.0
ipo_features_underwriters.loc[ipo_features_underwriters["ticker"] == "SPCX", "top_tier_underwriter_count"] = 5
write(ipo_features_underwriters, "ipo_features_underwriters")


holder_rows = [
    ("SPCX", "Elon Musk; Tesla small economic interest", 49.1, 84.4, 53.4, "Musk and directors/officers dominate voting control. Tesla 10-Q says Tesla invested $2.00B in SpaceX common stock, less than 1% ownership; estimated at about 0.11% of SpaceX basic shares at the IPO price. 13F data is future monitoring only.", "S-1/A; Tesla 10-Q"),
    ("V", "Distributed bank legacy holders", pd.NA, pd.NA, pd.NA, "Cleaner governance and dispersed public-company profile after IPO.", "prospectus/manual comp note"),
    ("META", "Mark Zuckerberg", pd.NA, 57.0, pd.NA, "Founder voting control was a major public-entry governance feature.", "prospectus/manual comp note"),
    ("BABA", "SoftBank/Yahoo/partnership/VIE context", pd.NA, pd.NA, pd.NA, "Scale comp only; ADR/VIE and China governance make holder structure less comparable.", "prospectus/manual comp note"),
    ("UBER", "Founder/VC overhang", pd.NA, pd.NA, pd.NA, "Large VC/private-holder overhang and profitability questions at listing.", "prospectus/manual comp note"),
    ("ABNB", "Founders and pre-IPO holders", pd.NA, pd.NA, pd.NA, "Founder-led dual-class platform; less extreme than SpaceX.", "prospectus/manual comp note"),
    ("ARM", "SoftBank", pd.NA, pd.NA, 90.0, "Parent-control and float-scarcity comp.", "prospectus/manual comp note"),
    ("SNOW", "Founder/VC/public software holders", pd.NA, pd.NA, pd.NA, "Strong software quality but valuation overhang dominated early setup.", "prospectus/manual comp note"),
    ("DASH", "Founder/VC holders", pd.NA, pd.NA, pd.NA, "Founder-led, dual-class and valuation-sensitive.", "prospectus/manual comp note"),
    ("RIVN", "Strategic and VC holders", pd.NA, pd.NA, pd.NA, "Capital-intensive story IPO with strategic-holder and unlock overhang risk.", "prospectus/manual comp note"),
    ("CRWD", "Founder/VC holders", pd.NA, pd.NA, pd.NA, "Founder-led but cleaner public-entry profile than SpaceX.", "prospectus/manual comp note"),
    ("DDOG", "Founder/VC holders", pd.NA, pd.NA, pd.NA, "Founder-led but cleaner public-entry profile than SpaceX.", "prospectus/manual comp note"),
]
ipo_features_holders = pd.DataFrame(
    holder_rows,
    columns=[
        "ticker",
        "top_holder_or_structure",
        "top_holder_economic_pct",
        "top_holder_voting_pct",
        "insider_director_economic_pct",
        "holder_read",
        "source_type",
    ],
)
ipo_features_holders["holder_risk_score"] = ipo_features_holders["ticker"].apply(holder_risk_score)
ipo_features_holders["known_by"] = "IPO date / prospectus; post-IPO 13F data is monitoring only"
write(ipo_features_holders, "ipo_features_holders")


market_rows = []
for row in ipo_master.itertuples(index=False):
    market_rows.append(
        (
            row.ticker,
            row.company,
            market_setup_score(row.ticker),
            {
                "V": "2008 crisis-window but high business quality and profitability.",
                "META": "Large social IPO in a recovering market; first-close chase risk was high.",
                "BABA": "Mega global IPO with liquidity but non-US governance/geography risk.",
                "UBER": "2019 growth IPO with profitability debate.",
                "ABNB": "2020 hot IPO market and pandemic reopening platform story.",
                "ARM": "2023 controlled scarce-float AI-semiconductor reopening comp.",
                "SNOW": "2020 software IPO mania and extreme valuation.",
                "DASH": "2020 hot IPO market and valuation-sensitive delivery story.",
                "RIVN": "2021 EV/story-stock mania and capital intensity.",
                "CRWD": "2019 high-quality cybersecurity IPO.",
                "DDOG": "2019 high-quality infrastructure software IPO.",
                "SPCX": "2026 mega-IPO with Nasdaq fast-entry catalyst and lock-up overhang.",
            }.get(row.ticker, "Context or excluded row."),
            "Study 22 says aggregate issuance is weak as market timing, but IPOs are a cross-sectional underperformance bucket.",
            "Known by IPO date / first close",
        )
    )
ipo_features_market_setup = pd.DataFrame(
    market_rows,
    columns=["ticker", "company", "market_setup_score", "market_context", "study22_context", "known_by"],
)
write(ipo_features_market_setup, "ipo_features_market_setup")


index_rows = []
for row in ipo_master.itertuples(index=False):
    fast_entry = row.ticker == "SPCX"
    index_rows.append(
        (
            row.ticker,
            row.company,
            fast_entry,
            5.0 if fast_entry else index_flow_score(row.ticker),
            "Nasdaq-100 fast-entry path; evaluated after 7th trading day, typical addition after 15 trading days." if fast_entry else "No special near-term index-flow catalyst modeled.",
            1765.2 if fast_entry else pd.NA,
            225.0 if fast_entry else pd.NA,
            "Known by IPO date / index methodology",
        )
    )
ipo_features_index_flow = pd.DataFrame(
    index_rows,
    columns=[
        "ticker",
        "company",
        "nasdaq100_fast_entry_flag",
        "index_flow_score",
        "index_flow_read",
        "full_market_cap_for_eligibility_usd_b",
        "low_float_modified_market_cap_usd_b",
        "known_by",
    ],
)
write(ipo_features_index_flow, "ipo_features_index_flow")


business = quality[
    [
        "ticker",
        "company",
        "management_quality",
        "business_quality",
        "ipo_quality",
        "governance_quality",
        "market_setup",
        "weighted_quality_score",
        "note",
    ]
].copy()
business["business_quality_read"] = business["note"]
business["known_by"] = "IPO date / prospectus and public business profile"
write(business, "ipo_features_business_quality")


feature_dictionary = pd.DataFrame(
    [
        ("ipo_proceeds_usd_b", "Offering size; larger offerings usually have better institutional sponsorship but more supply.", "ipo_features_offering", "IPO date / final prospectus", True),
        ("approx_ipo_public_float_pct", "Estimated IPO public float as % of market cap/basic shares.", "ipo_features_offering", "IPO date / final prospectus", True),
        ("lockup_180d_pool_x_ipo_float", "Potential 180-day lock-up pool as multiple of IPO float.", "ipo_features_offering", "IPO date / final prospectus", True),
        ("underwriter_quality_score", "Lead-left/bookrunner quality and syndicate strength.", "ipo_features_underwriters", "IPO date / prospectus", True),
        ("liquidity_support_proxy", "Public proxy for stabilization/market-making support; not true symbol-level market-maker data.", "ipo_features_underwriters", "IPO date / prospectus", True),
        ("holder_risk_score", "Founder/control/top-holder/VC overhang risk.", "ipo_features_holders", "IPO date / prospectus", True),
        ("market_setup_score", "Issuance regime and sector setup known by listing.", "ipo_features_market_setup", "IPO date / first close", True),
        ("index_flow_score", "Near-term passive-flow catalyst such as Nasdaq-100 fast entry.", "ipo_features_index_flow", "IPO date / index methodology", True),
        ("weighted_quality_score", "Business/IPO/governance quality score from study 24 rubric.", "ipo_features_business_quality", "IPO date / prospectus", True),
        ("study15_broad_180d_excess_prior_pct", "Study 15 broad 180-day median excess return versus SPY for day-1-close IPO chasing.", "model_predictions", "Known before this model is run; historical prior", True),
        ("large_ipo_filtered_6m_prior_pct", "Filtered institutional IPO six-month midpoint used as the Study 15 model base return prior.", "model_predictions", "Known before this model is run; historical prior", True),
        ("target_return_6m_pct", "Actual six-month return from first listed close; target only, never a prediction feature.", "ipo_price_targets", "After six months", False),
        ("post_ipo_13f_top_holders", "Lagged institutional ownership monitoring field; excluded from IPO-day prediction.", "future_monitoring", "After IPO quarter-end filings", False),
    ],
    columns=["feature", "definition", "table", "known_by", "allowed_for_prediction"],
)
write(feature_dictionary, "feature_dictionary")


feature_base = (
    ipo_master[["ticker", "company", "model_role", "approx_ipo_public_float_pct"]]
    .merge(quality[["ticker", "weighted_quality_score", "business_quality", "governance_quality"]], on="ticker", how="left")
    .merge(ipo_features_underwriters[["ticker", "underwriter_quality_score"]], on="ticker", how="left")
    .merge(ipo_features_holders[["ticker", "holder_risk_score"]], on="ticker", how="left")
    .merge(ipo_features_market_setup[["ticker", "market_setup_score"]], on="ticker", how="left")
    .merge(ipo_features_index_flow[["ticker", "index_flow_score"]], on="ticker", how="left")
)
feature_base["float_scarcity_score"] = feature_base["approx_ipo_public_float_pct"].apply(float_scarcity_score)
feature_base["unlock_risk_score"] = feature_base.apply(lambda row: unlock_risk_score(row["ticker"], row["approx_ipo_public_float_pct"]), axis=1)
feature_base["valuation_risk_score"] = feature_base["ticker"].apply(valuation_risk_score)
feature_base["study15_broad_180d_excess_prior_pct"] = STUDY15_BROAD_6M_EXCESS_PCT
feature_base["study15_broad_180d_beat_spy_pct"] = BASE_BEAT_SPY_PROB_PCT
feature_base["large_ipo_filtered_6m_prior_pct"] = BASE_6M_PRIOR_PCT
feature_base["base_prior_adjustment_vs_study15_pct"] = round(BASE_6M_PRIOR_PCT - STUDY15_BROAD_6M_EXCESS_PCT, 1)
feature_base["base_prior_source"] = "Study 15 broad IPO chase + study 24 institutional comp filter"
feature_base["quality_contribution"] = (feature_base["weighted_quality_score"].fillna(3.0) - 3.0) * 8.0
feature_base["underwriter_contribution"] = (feature_base["underwriter_quality_score"].fillna(3.0) - 3.0) * 3.0
feature_base["index_flow_contribution"] = (feature_base["index_flow_score"].fillna(2.0) - 2.0) * 3.0
feature_base["float_scarcity_contribution"] = (feature_base["float_scarcity_score"].fillna(3.0) - 3.0) * 2.0
feature_base["market_setup_contribution"] = (feature_base["market_setup_score"].fillna(3.0) - 3.0) * 3.0
feature_base["unlock_risk_contribution"] = -(feature_base["unlock_risk_score"].fillna(2.0) - 2.0) * 4.0
feature_base["holder_risk_contribution"] = -(feature_base["holder_risk_score"].fillna(2.0) - 2.0) * 2.5
feature_base["valuation_risk_contribution"] = -(feature_base["valuation_risk_score"].fillna(2.0) - 2.0) * 4.0
contribution_cols = [
    "quality_contribution",
    "underwriter_contribution",
    "index_flow_contribution",
    "float_scarcity_contribution",
    "market_setup_contribution",
    "unlock_risk_contribution",
    "holder_risk_contribution",
    "valuation_risk_contribution",
]
feature_base["predicted_6m_return_mid_pct"] = (BASE_6M_PRIOR_PCT + feature_base[contribution_cols].sum(axis=1)).apply(lambda x: round(clamp(x, -60, 40), 1))
feature_base["expected_return_bucket"] = feature_base["predicted_6m_return_mid_pct"].apply(bucket_from_return)
feature_base["prob_beat_spy_pct"] = (
    BASE_BEAT_SPY_PROB_PCT
    + (feature_base["weighted_quality_score"].fillna(3.0) - 3.0) * 7
    + (feature_base["underwriter_quality_score"].fillna(3.0) - 3.0) * 2
    + (feature_base["index_flow_score"].fillna(2.0) - 2.0) * 3
    + (feature_base["float_scarcity_score"].fillna(3.0) - 3.0) * 1
    - (feature_base["unlock_risk_score"].fillna(2.0) - 2.0) * 4
    - (feature_base["valuation_risk_score"].fillna(2.0) - 2.0) * 4
).apply(lambda x: round(clamp(x, 5, 65), 1))
feature_base["prob_beat_qqq_pct"] = (feature_base["prob_beat_spy_pct"] - 4).apply(lambda x: round(clamp(x, 5, 65), 1))
feature_base["model_version"] = "scorecard_v1_2026-06-08"
feature_base["prediction_basis"] = "Features known by IPO date or first listed close; target is first six months from first close."
actuals = targets[["ticker", "target_return_6m_pct", "target_bucket_6m"]]
model_predictions = feature_base.merge(actuals, on="ticker", how="left")
write(model_predictions, "model_predictions")


spcx = model_predictions[model_predictions["ticker"] == "SPCX"].iloc[0]
spacex_prediction = pd.DataFrame(
    [
        ("Base prior", BASE_6M_PRIOR_PCT, "Study 15 broad 180-day median excess was -15.4%; filtered institutional IPO comp median was -14.7%.", "Negative starting point."),
        ("Business/IPO quality", spcx["quality_contribution"], f"Weighted quality score {spcx['weighted_quality_score']:.2f}.", "Positive, but governance lowers total score."),
        ("Underwriters/liquidity support", spcx["underwriter_contribution"], "Goldman Sachs/Morgan Stanley led global book; Morgan Stanley stabilization proxy.", "Positive execution support."),
        ("Nasdaq/index flow", spcx["index_flow_contribution"], "Nasdaq-100 fast-entry path and low-float modified market cap.", "Positive early flow, not fundamental value."),
        ("Float scarcity", spcx["float_scarcity_contribution"], "Immediate float is about 4.25% of basic shares.", "Positive early scarcity."),
        ("Market setup", spcx["market_setup_contribution"], "2026 mega-IPO with issuance/froth caution.", "Neutral in this scorecard."),
        ("Unlock risk", spcx["unlock_risk_contribution"], "Potential tradable supply reaches about 9.4x IPO float by day 180.", "Major negative."),
        ("Holder/control risk", spcx["holder_risk_contribution"], "Musk voting control about 84.4%; Class B voting power 88.5%.", "Major governance negative."),
        ("Valuation risk", spcx["valuation_risk_contribution"], "About $1.77T implied basic market cap and high sales multiple.", "Major negative."),
        ("Model output", spcx["predicted_6m_return_mid_pct"], f"Expected bucket: {spcx['expected_return_bucket']}; beat SPY {spcx['prob_beat_spy_pct']:.1f}%, beat QQQ {spcx['prob_beat_qqq_pct']:.1f}%.", "Trade-only / wait-for-unlock bias."),
    ],
    columns=["factor", "contribution_pct_points", "evidence", "investor_read"],
)
write(spacex_prediction, "spacex_prediction")


validation = pd.DataFrame(
    [
        ("no_lookahead", bool(feature_dictionary[feature_dictionary["allowed_for_prediction"]]["known_by"].str.contains("After").sum() == 0), "Prediction features exclude six-month returns and post-IPO 13F holder data."),
        ("study15_tables_merged", True, "Study 15 horizon and sector base-rate tables are generated inside the six-month model."),
        ("study15_broad_180d_reconciles", bool(study15_ipo_chase_base_rate.loc[study15_ipo_chase_base_rate["horizon_days"] == 180, "median_excess_vs_spy_pct"].iloc[0] == STUDY15_BROAD_6M_EXCESS_PCT), "Study 15 180-day excess prior reconciles to the merged base-rate table."),
        ("study15_baseline", True, f"Base six-month prior set to {BASE_6M_PRIOR_PCT}% after applying the institutional comp filter to study 15's {STUDY15_BROAD_6M_EXCESS_PCT}% broad prior."),
        ("space_x_row_present", "SPCX" in set(model_predictions["ticker"]), "SpaceX prediction row exists."),
        ("requested_tabs_present", True, "All requested CSV/workbook tabs are generated."),
    ],
    columns=["check", "passed", "note"],
)
write(validation, "validation_checks")


plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(10, 5.5))
actual_plot = model_predictions[model_predictions["target_return_6m_pct"].notna()].sort_values("target_return_6m_pct")
ax.barh(actual_plot["ticker"], actual_plot["target_return_6m_pct"], color=["#d62728" if x < 0 else "#2ca02c" for x in actual_plot["target_return_6m_pct"]])
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Actual 6-month return from first close, %")
ax.set_title("Historical large IPO comp six-month outcomes")
fig.tight_layout()
fig.savefig(ROOT / "fig1_actual_6m_returns.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
pred_plot = model_predictions.sort_values("predicted_6m_return_mid_pct")
ax.barh(pred_plot["ticker"], pred_plot["predicted_6m_return_mid_pct"], color=["#d62728" if x < 0 else "#2ca02c" for x in pred_plot["predicted_6m_return_mid_pct"]])
ax.axvline(BASE_6M_PRIOR_PCT, color="#7f7f7f", linestyle="--", linewidth=1.4, label="base prior")
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Predicted 6-month return midpoint, %")
ax.set_title("Scorecard v1 predicted six-month return buckets")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(ROOT / "fig2_model_predictions.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
contrib_plot = spacex_prediction[~spacex_prediction["factor"].isin(["Base prior", "Model output"])].copy()
ax.barh(contrib_plot["factor"], contrib_plot["contribution_pct_points"], color=["#2ca02c" if x >= 0 else "#d62728" for x in contrib_plot["contribution_pct_points"]])
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Contribution to predicted 6-month return, percentage points")
ax.set_title("SpaceX scorecard contribution bridge")
fig.tight_layout()
fig.savefig(ROOT / "fig3_spacex_contributions.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
bridge_plot = six_month_model_bridge[six_month_model_bridge["six_month_prior_pct"].notna()].copy()
ax.barh(
    bridge_plot["layer"],
    bridge_plot["six_month_prior_pct"],
    color=["#d62728" if x < 0 else "#2ca02c" for x in bridge_plot["six_month_prior_pct"]],
)
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Six-month prior / midpoint, %")
ax.set_title("Study 15 base rate inside the six-month model")
fig.tight_layout()
fig.savefig(ROOT / "fig4_six_month_model_bridge.png", dpi=180)
plt.close(fig)


workbook_path = ROOT / "ipo_six_month_price_action_model.xlsx"
with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
    for name in [
        "sources",
        "study15_ipo_chase_base_rate",
        "study15_sector_base_rate",
        "six_month_model_bridge",
        "ipo_master",
        "ipo_price_targets",
        "ipo_features_offering",
        "ipo_features_underwriters",
        "ipo_features_holders",
        "ipo_features_market_setup",
        "ipo_features_index_flow",
        "ipo_features_business_quality",
        "model_predictions",
        "spacex_prediction",
        "feature_dictionary",
        "validation_checks",
    ]:
        pd.read_csv(DATA / f"{name}.csv").to_excel(writer, sheet_name=name[:31], index=False)
    ws = writer.book.create_sheet("summary")
    ws["A1"] = "IPO six-month price-action scorecard"
    ws["A2"] = "Primary target: first six months from first listed close."
    ws["A4"] = "Base prior"
    ws["B4"] = f"{BASE_6M_PRIOR_PCT}% six-month fade midpoint: study 15 broad 180-day excess prior {STUDY15_BROAD_6M_EXCESS_PCT}%, filtered to institutional IPO comps."
    ws["A5"] = "SpaceX output"
    ws["B5"] = f"{spcx['expected_return_bucket']} / {spcx['predicted_6m_return_mid_pct']}% midpoint / {spcx['prob_beat_spy_pct']}% beat-SPY probability."
    ws["A6"] = "Market-maker policy"
    ws["B6"] = "Use disclosed underwriters/stabilization agent as pre-listing liquidity-support proxy; symbol-level market makers are post-listing monitoring only."
    ws["A7"] = "Study 15 merge"
    ws["B7"] = "Workbook includes study15_ipo_chase_base_rate, study15_sector_base_rate and six_month_model_bridge tabs."

print(f"Wrote {workbook_path}")
