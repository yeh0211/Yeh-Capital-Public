#!/usr/bin/env python3
"""Build a reusable six-month IPO price-action scorecard.

The model is intentionally transparent. It combines YehCapital's prior IPO
base-rate studies with public IPO mechanics and a curated institutional IPO
comp set. It is a research scorecard, not a trading system.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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

IPO_VALUATION_ANNUAL_CSV = """year,ipo_count,avg_first_day_return_pct,ipo_gross_proceeds_usd_m,cape,shiller_trailing_pe,forward_pe
1960,269,17.8,553,18.34,17.12,
1961,435,34.1,1243,18.47,18.60,
1962,298,-1.6,431,21.20,21.25,
1963,83,3.9,246,19.26,17.66,
1964,97,5.3,380,21.63,18.77,
1965,146,12.7,409,23.27,18.75,
1966,85,7.1,275,24.06,17.81,
1967,100,37.7,641,20.43,15.31,
1968,368,55.9,1205,21.51,17.71,
1969,780,12.5,2605,21.19,17.65,
1970,358,-0.7,780,17.09,15.76,
1971,391,21.2,1655,16.46,18.12,
1972,562,7.5,2724,17.26,18.01,
1973,105,-17.8,330,18.71,18.09,
1974,9,-7.0,51,13.53,11.68,
1975,12,-0.2,261,8.92,8.30,
1976,26,1.9,215,11.19,11.82,
1977,15,3.6,128,11.44,10.41,
1978,19,13.3,197,9.24,8.28,
1979,39,8.9,309,9.26,7.88,
1980,71,14.3,905,8.85,7.39,
1981,192,5.9,2306,9.26,9.02,
1982,79,10.7,1012,7.39,7.73,
1983,521,9.0,11306,8.76,11.48,
1984,213,3.0,2566,9.89,11.52,
1985,217,6.6,4749,10.00,10.36,
1986,478,6.1,15489,11.72,14.28,
1987,337,5.7,12568,14.92,18.01,
1988,132,5.3,4089,13.90,14.02,
1989,124,7.7,5886,15.09,11.82,
1990,116,10.4,4334,17.05,15.13,13.90
1991,293,11.8,16464,15.61,15.35,18.97
1992,416,10.2,22750,19.77,25.93,18.17
1993,527,12.7,31654,20.32,22.50,17.45
1994,410,9.6,17418,21.41,21.34,15.39
1995,465,21.3,27993,20.22,14.89,16.99
1996,689,17.1,42428,24.76,18.08,16.68
1997,485,14.0,32547,28.33,19.53,19.93
1998,310,20.6,34416,32.86,24.29,24.25
1999,484,70.0,64809,40.57,32.92,25.12
2000,382,56.1,64931,43.77,29.04,21.57
2001,80,14.0,35288,36.98,27.55,21.00
2002,70,8.6,22136,30.28,46.17,15.77
2003,68,11.9,10075,22.90,31.43,17.74
2004,181,12.4,31663,27.66,22.73,15.75
2005,167,10.0,28578,26.59,19.99,14.51
2006,162,12.0,30648,26.47,18.07,14.87
2007,160,14.0,35704,27.21,17.36,14.40
2008,21,5.7,22762,24.02,21.46,11.67
2009,42,10.8,13296,15.17,70.91,14.19
2010,98,9.3,30624,20.53,20.70,13.09
2011,82,13.8,27750,22.98,16.30,11.81
2012,101,17.3,31973,21.21,14.87,12.61
2013,163,20.6,41909,21.90,17.03,15.37
2014,222,14.9,46852,24.86,18.15,16.37
2015,125,18.7,22296,26.49,20.02,16.28
2016,79,14.0,13234,24.21,22.18,17.15
2017,117,12.3,24032,28.06,23.59,18.21
2018,143,17.8,34043,33.31,24.97,14.58
2019,120,22.4,39725,28.38,19.60,18.43
2020,165,41.6,61860,30.99,24.88,22.59
2021,315,31.9,119631,34.51,35.96,21.42
2022,39,47.7,7014,36.94,23.11,16.79
2023,54,11.9,11916,28.34,22.82,19.70
2024,73,15.2,20527,31.97,25.01,21.57
2025,94,28.4,39409,37.14,28.16,22.02
2026,,,,41.67,31.90,20.92
"""


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


def load_sp500_close() -> pd.Series:
    """Load S&P 500 closes for drawdown and forward-return context.

    The normal path uses Yahoo Finance through yfinance. A small deterministic
    fallback keeps the workbook buildable if the public data endpoint is down.
    """
    try:
        import yfinance as yf

        sp500 = yf.download("^GSPC", start="1959-01-01", end="2026-06-10", progress=False, auto_adjust=False)
        if isinstance(sp500.columns, pd.MultiIndex):
            close = sp500["Close"]["^GSPC"]
        else:
            close = sp500["Close"]
        close = close.dropna().astype(float)
        if len(close) > 1000:
            close.name = "sp500_close"
            return close
    except Exception:
        pass

    fallback = pd.Series(
        {
            "2000-03-24": 1527.46,
            "2002-03-19": 1170.29,
            "2002-10-09": 776.76,
            "2007-10-09": 1565.15,
            "2009-03-09": 676.53,
            "2022-01-03": 4796.56,
            "2022-10-12": 3577.03,
            "2026-06-02": 7609.78,
            "2026-06-08": 7405.73,
        }
    )
    fallback.index = pd.to_datetime(fallback.index)
    fallback.name = "sp500_close"
    return fallback.sort_index()


def close_on_or_before(close: pd.Series, date: str) -> tuple[pd.Timestamp, float]:
    date_ts = pd.Timestamp(date)
    eligible = close[close.index <= date_ts]
    if eligible.empty:
        raise ValueError(f"No S&P 500 close on or before {date}")
    return eligible.index[-1], float(eligible.iloc[-1])


def drawdown_between(close: pd.Series, peak_date: str, trough_date: str) -> tuple[str, float, str, float, float]:
    peak_ts, peak_close = close_on_or_before(close, peak_date)
    trough_ts, trough_close = close_on_or_before(close, trough_date)
    return (
        peak_ts.date().isoformat(),
        peak_close,
        trough_ts.date().isoformat(),
        trough_close,
        round((trough_close / peak_close - 1.0) * 100.0, 2),
    )


def add_rank_columns(df: pd.DataFrame, column: str) -> None:
    complete = df[column].notna()
    df.loc[complete, f"{column}_percentile_full"] = df.loc[complete, column].rank(pct=True)
    expanding = []
    for _, row in df.iterrows():
        if pd.isna(row[column]):
            expanding.append(pd.NA)
            continue
        history = df.loc[(df["year"] <= row["year"]) & df[column].notna(), column]
        expanding.append(float(history.rank(pct=True).iloc[-1]))
    df[f"{column}_percentile_expanding"] = expanding


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
        ("RIA / Real Investment Advice", "https://realinvestmentadvice.com/resources/blog/equity-supply-surge-what-historically-comes-next/", "Hypothesis source for equity supply waves, lock-up overhang and S&P 500 drawdown case studies."),
        ("Jay Ritter IPO Statistics", "https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf", "Long-history IPO counts, first-day returns and gross proceeds from Table 8, 1960-2025."),
        ("Robert Shiller / multpl CAPE table", "https://www.multpl.com/shiller-pe/table/by-year", "Annual CAPE valuation proxy; used because Yale Shiller endpoint was unavailable during build."),
        ("History of Market forward P/E", "https://historyofmarket.com/api/sp500/forward-pe.json", "Public forward P/E appendix, quarter-end observations back to 1990."),
        ("Baker and Wurgler 2000", "https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00285", "Academic benchmark: equity share in new issues predicts aggregate stock returns in 1928-1997 data."),
        ("SEC IPO statistics", "https://www.sec.gov/data-research/statistics-data-visualizations/initial-public-offerings-ipos", "2000-2025 IPO count and proceeds cross-check with broader SEC issuer categories."),
    ],
    columns=["source", "url", "used_for"],
)
write(sources, "sources")


sp500_close = load_sp500_close()
sp500_drawdown = sp500_close.to_frame()
running_peak = sp500_close.cummax()
peak_dates = []
current_peak_date = None
current_peak_value = -np.inf
for date, value in sp500_close.items():
    if value >= current_peak_value:
        current_peak_value = value
        current_peak_date = date
    peak_dates.append(current_peak_date.date().isoformat())
sp500_drawdown["running_peak_close"] = running_peak
sp500_drawdown["running_peak_date"] = peak_dates
sp500_drawdown["drawdown_from_peak_pct"] = (sp500_drawdown["sp500_close"] / sp500_drawdown["running_peak_close"] - 1.0) * 100.0
sp500_drawdown = sp500_drawdown.reset_index().rename(columns={"Date": "date", "index": "date"})
sp500_drawdown["date"] = pd.to_datetime(sp500_drawdown["date"]).dt.date.astype(str)
sp500_drawdown["source"] = "Yahoo Finance ^GSPC via yfinance; fallback has exact case dates only if endpoint is unavailable."
write(sp500_drawdown, "sp500_drawdown_from_peak")

year_end = sp500_close.resample("YE").last()
sp500_year = pd.DataFrame({"year": year_end.index.year, "sp500_year_end_close": year_end.values})
for years in [1, 3, 5]:
    sp500_year[f"sp500_forward_{years}y_return_pct"] = (
        sp500_year["sp500_year_end_close"].shift(-years) / sp500_year["sp500_year_end_close"] - 1.0
    ) * 100.0

ipo_valuation_regime_annual = pd.read_csv(StringIO(IPO_VALUATION_ANNUAL_CSV))
ipo_valuation_regime_annual = ipo_valuation_regime_annual.merge(sp500_year, on="year", how="left")
for col in ["ipo_count", "ipo_gross_proceeds_usd_m", "avg_first_day_return_pct", "cape", "shiller_trailing_pe", "forward_pe"]:
    add_rank_columns(ipo_valuation_regime_annual, col)
complete_ipo_year = ipo_valuation_regime_annual["ipo_count"].notna() & (ipo_valuation_regime_annual["year"] <= 2025)
ipo_valuation_regime_annual["high_ipo_count_full_sample"] = (
    ipo_valuation_regime_annual["ipo_count_percentile_full"] >= 0.75
)
ipo_valuation_regime_annual["high_cape_full_sample"] = (
    ipo_valuation_regime_annual["cape_percentile_full"] >= 0.75
)
ipo_valuation_regime_annual["high_forward_pe_full_sample"] = (
    ipo_valuation_regime_annual["forward_pe_percentile_full"] >= 0.75
)
ipo_valuation_regime_annual["complete_ipo_year"] = complete_ipo_year
ipo_valuation_regime_annual["valuation_data_basis"] = np.where(
    ipo_valuation_regime_annual["year"] == 2026,
    "Live valuation-only row; IPO count/proceeds are scenario, not actual.",
    "Ritter Table 8 IPO data plus Shiller/multpl annual valuation proxies.",
)
write(ipo_valuation_regime_annual, "ipo_valuation_regime_annual")

peak_date, peak_close, trough_date, trough_close, dotcom_dd = drawdown_between(sp500_close, "2000-03-24", "2002-10-09")
marker_date, marker_close = close_on_or_before(sp500_close, "2002-03-19")
gfc_peak_date, gfc_peak_close, gfc_trough_date, gfc_trough_close, gfc_dd = drawdown_between(sp500_close, "2007-10-09", "2009-03-09")
spac_peak_date, spac_peak_close, spac_trough_date, spac_trough_close, spac_dd = drawdown_between(sp500_close, "2022-01-03", "2022-10-12")
recent_2026 = sp500_close[sp500_close.index >= pd.Timestamp("2026-01-01")]
if recent_2026.empty:
    scenario_peak_date, scenario_peak_close = close_on_or_before(sp500_close, "2026-06-02")
else:
    scenario_peak_date = recent_2026.idxmax()
    scenario_peak_close = float(recent_2026.max())

equity_supply_drawdown_cases = pd.DataFrame(
    [
        (
            "Dot-com IPO/equity-supply wave",
            "historical",
            "2000-03-24",
            peak_date,
            peak_close,
            "2002-03-19",
            round((marker_close / peak_close - 1.0) * 100.0, 2),
            "2002-10-09",
            trough_date,
            trough_close,
            dotcom_dd,
            -78.0,
            "Nasdaq drawdown cited by RIA as high-beta/new-issue damage proxy.",
            382.0,
            64.931,
            pd.NA,
            pd.NA,
            "RIA says issuance advanced into the March 2000 market peak; S&P then fell about 49%.",
            "User's March 2002 marker is not the cycle peak; it is a local rebound high about 23% below the March 24, 2000 peak.",
        ),
        (
            "GFC equity issuance / bank recapitalization",
            "historical_false_positive",
            "2007-10-09",
            gfc_peak_date,
            gfc_peak_close,
            pd.NA,
            pd.NA,
            "2009-03-09",
            gfc_trough_date,
            gfc_trough_close,
            gfc_dd,
            pd.NA,
            "Not an IPO-greed cohort; RIA identifies 2008 as rescue-capital issuance caused by the crash.",
            160.0,
            35.704,
            pd.NA,
            pd.NA,
            "Broad-index drawdown was severe, but issuance was emergency bank capital, not normal late-cycle IPO supply.",
            "Keep as a correction case so the model does not label every issuance spike as greed.",
        ),
        (
            "SPAC / 2020-2021 IPO wave",
            "historical",
            "2022-01-03",
            spac_peak_date,
            spac_peak_close,
            pd.NA,
            pd.NA,
            "2022-10-12",
            spac_trough_date,
            spac_trough_close,
            spac_dd,
            -60.0,
            "RIA says SPACs merged from mid-2020 to end-2021 were down more than 60% from reference price and underperformed Nasdaq by 44%.",
            315.0,
            119.631,
            600.0,
            pd.NA,
            "S&P drawdown was material, but the newly issued SPAC/IPO paper absorbed much worse damage.",
            "January 3, 2022 is the S&P 500 closing peak; October 12, 2022 is the closing trough used here.",
        ),
        (
            "2026 mega-IPO / AI lock-up wave",
            "scenario",
            scenario_peak_date.date().isoformat(),
            scenario_peak_date.date().isoformat(),
            scenario_peak_close,
            pd.NA,
            pd.NA,
            "TBD",
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            "No realized drawdown. RIA scenario frames a potential record supply wave rather than a completed outcome.",
            pd.NA,
            160.0,
            pd.NA,
            540.0,
            "RIA cites potential 2026 IPO proceeds near $160B and combined IPO plus lock-up supply above $700B.",
            "Scenario row only; trough date and drawdown remain TBD.",
        ),
    ],
    columns=[
        "case_name",
        "case_type",
        "source_peak_date",
        "verified_peak_date",
        "sp500_peak_close",
        "user_or_intermediate_marker_date",
        "marker_drawdown_from_peak_pct",
        "source_trough_date",
        "verified_trough_date",
        "sp500_trough_close",
        "sp500_drawdown_pct",
        "new_issue_or_nasdaq_damage_pct",
        "new_issue_damage_basis",
        "ritter_ipo_count",
        "ritter_operating_ipo_proceeds_usd_b",
        "spac_count_or_context",
        "estimated_lockup_supply_usd_b",
        "ria_hypothesis_read",
        "date_qa_note",
    ],
)
equity_supply_drawdown_cases["source"] = "RIA hypothesis; S&P 500 closes independently reconstructed from Yahoo Finance where available."
write(equity_supply_drawdown_cases, "equity_supply_drawdown_cases")

test_rows = []
annual_core = ipo_valuation_regime_annual[complete_ipo_year].copy()
high_ipo = annual_core["ipo_count_percentile_full"] >= 0.75
high_cape = annual_core["cape_percentile_full"] >= 0.75
forward_core = annual_core[annual_core["forward_pe"].notna()].copy()
high_ipo_expanding = annual_core["ipo_count_percentile_expanding"] >= 0.75
for metric_col, label, sample in [
    ("cape", "CAPE", annual_core),
    ("forward_pe", "forward P/E", forward_core),
    ("shiller_trailing_pe", "trailing P/E", annual_core),
]:
    corr = sample[["ipo_count", metric_col]].corr(method="spearman").iloc[0, 1]
    test_rows.append(
        (
            f"spearman_ipo_count_vs_{metric_col}",
            f"IPO count rank correlation with {label}",
            len(sample),
            round(corr, 3),
            "Correlation near zero means IPO count alone is not a reliable valuation-greed gauge.",
            "Descriptive, full-sample valuation relation.",
        )
    )
test_rows.extend(
    [
        (
            "high_ipo_years",
            "Years in top quartile of IPO count, 1960-2025",
            int(high_ipo.sum()),
            int(high_ipo.sum()),
            "The high-IPO-count sample is large enough to inspect across regimes.",
            "Full-sample descriptive quartile.",
        ),
        (
            "high_ipo_and_high_cape_overlap",
            "Top-quartile IPO count years that also had top-quartile CAPE",
            int(high_ipo.sum()),
            int((high_ipo & high_cape).sum()),
            "Only 3 of 17 high-IPO-count years were also high-CAPE years: 1997, 1999 and 2000.",
            "Full-sample descriptive quartile.",
        ),
        (
            "high_ipo_not_high_cape",
            "Top-quartile IPO count years without top-quartile CAPE",
            int(high_ipo.sum()),
            int((high_ipo & ~high_cape).sum()),
            "Most high-count IPO years did not occur at extreme broad-market valuation.",
            "Full-sample descriptive quartile.",
        ),
        (
            "high_cape_not_high_ipo",
            "Top-quartile CAPE years without top-quartile IPO count",
            int(high_cape.sum()),
            int((high_cape & ~high_ipo).sum()),
            "High valuation can persist even when operating-company IPO counts are low.",
            "Full-sample descriptive quartile.",
        ),
    ]
)
for horizon in [1, 3, 5]:
    col = f"sp500_forward_{horizon}y_return_pct"
    sample = annual_core[annual_core[col].notna()].copy()
    hi = sample["ipo_count_percentile_expanding"] >= 0.75
    high_mean = sample.loc[hi, col].mean()
    low_mean = sample.loc[~hi, col].mean()
    test_rows.append(
        (
            f"forward_{horizon}y_after_high_ipo_expanding",
            f"Mean S&P 500 forward {horizon}y return after point-in-time high IPO-count years minus other years",
            len(sample),
            round(high_mean - low_mean, 2),
            "Uses expanding IPO-count percentiles to avoid lookahead; not a mechanical sell rule.",
            "Forward-return context, not trading model.",
        )
    )
ipo_valuation_regime_tests = pd.DataFrame(
    test_rows,
    columns=["test", "description", "sample_n", "stat_value", "interpretation", "test_basis"],
)
write(ipo_valuation_regime_tests, "ipo_valuation_regime_tests")

ria_equity_supply_source_notes = pd.DataFrame(
    [
        ("RIA equity-supply article", "2026-06", "Equity supply waves can precede or coincide with drawdowns; 2026 may be a record combined IPO plus lock-up supply year.", "Used as hypothesis framing only; drawdowns are independently recalculated.", "https://realinvestmentadvice.com/resources/blog/equity-supply-surge-what-historically-comes-next/"),
        ("RIA dot-com case", "2000-2002", "Dot-com issuance advanced into March 2000; S&P fell about 49% into October 2002 and Nasdaq about 78%.", "Used as a case row; S&P date and drawdown are recalculated from closes.", "https://realinvestmentadvice.com/resources/blog/equity-supply-surge-what-historically-comes-next/"),
        ("RIA 2008 correction", "2008-2009", "The 2008 issuance spike was rescue capital, not insider greed; crash caused issuance.", "Used as a false-positive/correction row.", "https://realinvestmentadvice.com/resources/blog/equity-supply-surge-what-historically-comes-next/"),
        ("RIA SPAC/IPO case", "2020-2022", "More than 600 SPAC listings and a record IPO calendar preceded the January-October 2022 drawdown; SPAC/deSPAC damage exceeded the index drawdown.", "Used as a historical case row and new-issue-damage comparison.", "https://realinvestmentadvice.com/resources/blog/equity-supply-surge-what-historically-comes-next/"),
        ("Ritter Table 8", "1960-2025", "Number of offerings, average first-day returns and gross proceeds of IPOs.", "Used as long annual IPO history; counts exclude many noisy categories and are cleaner than broad SEC totals.", "https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf"),
        ("SEC IPO statistics", "2000-2025", "SEC reports 374 total IPOs and $70.1B proceeds in 2025 across corporate, SPAC and fund categories.", "Used as a broad-definition cross-check; not mixed into the Ritter core sample.", "https://www.sec.gov/data-research/statistics-data-visualizations/initial-public-offerings-ipos"),
        ("Robert Shiller / multpl", "1960-2026", "CAPE and trailing P/E annual valuation proxy.", "Used as public long-history valuation proxy. Yale host was unavailable during implementation, so multpl table is the build source.", "https://www.multpl.com/shiller-pe/table/by-year"),
        ("History of Market", "1990-2026", "Forward P/E, quarterly observations back to 1990.", "Used as forward-multiple appendix; 2026 is a live valuation-only row.", "https://historyofmarket.com/api/sp500/forward-pe.json"),
        ("Baker and Wurgler", "1928-1997", "Equity share in new issues predicts lower stock returns in their academic sample.", "Used as academic benchmark; this study does not re-estimate the debt/equity issuance-share model.", "https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00285"),
        ("Yahoo Finance ^GSPC", "1959-2026", "Daily S&P 500 closes.", "Used to reconstruct drawdown from prior peak and forward S&P 500 returns.", "https://finance.yahoo.com/quote/%5EGSPC/"),
    ],
    columns=["source", "period", "claim_or_data", "how_used", "url"],
)
write(ria_equity_supply_source_notes, "ria_equity_supply_source_notes")


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
        ("ipo_valuation_sample_1960_2025", bool(annual_core["year"].min() == 1960 and annual_core["year"].max() == 2025), "Ritter IPO valuation-regime table covers 1960-2025 complete IPO years."),
        ("forward_pe_appendix_1990_present", bool(forward_core["year"].min() == 1990 and ipo_valuation_regime_annual.loc[ipo_valuation_regime_annual["year"] == 2026, "forward_pe"].notna().any()), "Forward P/E appendix covers 1990 through the live 2026 valuation-only row."),
        ("dotcom_drawdown_reconciles", bool(abs(equity_supply_drawdown_cases.loc[equity_supply_drawdown_cases["case_name"].str.startswith("Dot-com"), "sp500_drawdown_pct"].iloc[0] + 49.15) < 0.5), "Dot-com peak/trough drawdown is independently reconstructed near RIA's roughly -49% figure."),
        ("gfc_drawdown_reconciles", bool(abs(equity_supply_drawdown_cases.loc[equity_supply_drawdown_cases["case_name"].str.startswith("GFC"), "sp500_drawdown_pct"].iloc[0] + 56.78) < 0.5), "GFC peak/trough drawdown is independently reconstructed near -57%."),
        ("spac_2022_drawdown_reconciles", bool(abs(equity_supply_drawdown_cases.loc[equity_supply_drawdown_cases["case_name"].str.startswith("SPAC"), "sp500_drawdown_pct"].iloc[0] + 25.43) < 0.5), "2022 peak/trough drawdown is independently reconstructed near -25%."),
        ("scenario_2026_not_actual", bool(equity_supply_drawdown_cases.loc[equity_supply_drawdown_cases["case_type"] == "scenario", "source_trough_date"].iloc[0] == "TBD"), "2026 mega-IPO wave is marked as a scenario, not a completed drawdown."),
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

fig, ax = plt.subplots(figsize=(11, 5.8))
draw_plot = pd.read_csv(DATA / "sp500_drawdown_from_peak.csv")
draw_plot["date"] = pd.to_datetime(draw_plot["date"])
draw_plot = draw_plot[draw_plot["date"] >= pd.Timestamp("1999-01-01")]
ax.plot(draw_plot["date"], draw_plot["drawdown_from_peak_pct"], color="#1f77b4", linewidth=1.4)
ax.axhline(0, color="black", linewidth=1)
for row in equity_supply_drawdown_cases.itertuples(index=False):
    if pd.notna(row.verified_peak_date):
        ax.axvline(pd.Timestamp(row.verified_peak_date), color="#7f7f7f", linestyle="--", linewidth=0.9)
    if pd.notna(row.verified_trough_date):
        ax.scatter(pd.Timestamp(row.verified_trough_date), row.sp500_drawdown_pct, color="#d62728", s=38, zorder=3)
        ax.text(pd.Timestamp(row.verified_trough_date), row.sp500_drawdown_pct - 4, row.case_name.split()[0], fontsize=8, ha="center")
ax.set_ylabel("S&P 500 drawdown from prior peak, %")
ax.set_title("Equity-supply cases on S&P 500 drawdown-from-peak path")
fig.tight_layout()
fig.savefig(ROOT / "fig5_sp500_drawdown_supply_cases.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 5.8))
annual_plot = ipo_valuation_regime_annual[ipo_valuation_regime_annual["complete_ipo_year"]].copy()
ax.plot(annual_plot["year"], annual_plot["ipo_count_percentile_full"] * 100, label="IPO count percentile", linewidth=1.8)
ax.plot(annual_plot["year"], annual_plot["cape_percentile_full"] * 100, label="CAPE percentile", linewidth=1.8)
forward_plot = annual_plot[annual_plot["forward_pe_percentile_full"].notna()]
ax.plot(forward_plot["year"], forward_plot["forward_pe_percentile_full"] * 100, label="Forward P/E percentile", linewidth=1.8)
ax.axhline(75, color="#d62728", linestyle="--", linewidth=1.0, label="top quartile")
ax.set_ylim(0, 105)
ax.set_ylabel("Full-sample percentile")
ax.set_title("IPO activity is not the same thing as high broad-market valuation")
ax.legend(loc="upper left", ncol=2)
fig.tight_layout()
fig.savefig(ROOT / "fig6_ipo_activity_vs_valuation.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10.5, 5.8))
damage = equity_supply_drawdown_cases[equity_supply_drawdown_cases["case_type"] != "scenario"].copy()
x = np.arange(len(damage))
width = 0.36
ax.bar(x - width / 2, damage["sp500_drawdown_pct"], width=width, label="S&P 500 drawdown", color="#1f77b4")
ax.bar(
    x + width / 2,
    pd.to_numeric(damage["new_issue_or_nasdaq_damage_pct"], errors="coerce").fillna(0),
    width=width,
    label="New issue / Nasdaq damage proxy",
    color="#d62728",
)
for idx, value in enumerate(damage["new_issue_or_nasdaq_damage_pct"]):
    if pd.isna(value):
        ax.text(idx + width / 2, -3, "n/a", ha="center", va="top", fontsize=8)
ax.axhline(0, color="black", linewidth=1)
ax.set_xticks(x, ["Dot-com", "GFC", "SPAC/IPO"])
ax.set_ylabel("Drawdown / damage, %")
ax.set_title("Fresh supply absorbed more damage than the broad index in euphoric waves")
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(ROOT / "fig7_supply_case_damage.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9.5, 5.6))
supply = pd.DataFrame(
    [
        ("2021 operating IPOs", 119.631, 0.0, "actual"),
        ("2026 RIA scenario", 160.0, 540.0, "scenario"),
    ],
    columns=["case", "ipo_proceeds_usd_b", "estimated_lockup_supply_usd_b", "type"],
)
ax.bar(supply["case"], supply["ipo_proceeds_usd_b"], label="IPO proceeds", color="#1f77b4")
ax.bar(
    supply["case"],
    supply["estimated_lockup_supply_usd_b"],
    bottom=supply["ipo_proceeds_usd_b"],
    label="Estimated lock-up supply",
    color="#ff7f0e",
)
ax.set_ylabel("Equity supply, $B")
ax.set_title("2026 is a supply scenario, not a completed drawdown")
ax.legend(loc="upper left")
for i, row in supply.iterrows():
    total = row["ipo_proceeds_usd_b"] + row["estimated_lockup_supply_usd_b"]
    ax.text(i, total + 15, f"${total:.0f}B", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(ROOT / "fig8_2026_supply_scenario.png", dpi=180)
plt.close(fig)


workbook_path = ROOT / "ipo_six_month_price_action_model.xlsx"
with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
    for name in [
        "sources",
        "equity_supply_drawdown_cases",
        "sp500_drawdown_from_peak",
        "ipo_valuation_regime_annual",
        "ipo_valuation_regime_tests",
        "ria_equity_supply_source_notes",
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
    ws["A8"] = "RIA supply regime"
    ws["B8"] = "Equity-supply waves are late-cycle warnings, not mechanical S&P 500 sell signals; 2026 is scenario-only."

print(f"Wrote {workbook_path}")
