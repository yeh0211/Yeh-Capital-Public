"""Shared configuration for the election money-flow study."""
from pathlib import Path
import os

PROJ = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("ELECTION_FLOWS_DATA", PROJ / "data"))
DERIVED_DIR = PROJ / "derived"
OUTPUT_DIR = PROJ / "output"
for _d in (DATA_DIR, DERIVED_DIR, OUTPUT_DIR):
    _d.mkdir(parents=True, exist_ok=True)

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
}

# ETF flow panel. iShares-first so one download format covers the whole panel.
# bucket -> used for aggregation in the rotation metrics.
ETF_PANEL = [
    {"ticker": "IVV",  "bucket": "US",          "label": "S&P 500"},
    {"ticker": "IWM",  "bucket": "US_smallcap", "label": "Russell 2000"},
    {"ticker": "EEM",  "bucket": "EM",          "label": "MSCI Emerging Markets"},
    {"ticker": "IEMG", "bucket": "EM",          "label": "Core MSCI EM"},
    {"ticker": "FXI",  "bucket": "China",       "label": "China Large-Cap"},
    {"ticker": "MCHI", "bucket": "China",       "label": "MSCI China"},
    {"ticker": "EWT",  "bucket": "Taiwan",      "label": "MSCI Taiwan"},
    {"ticker": "EWY",  "bucket": "Korea",       "label": "MSCI South Korea"},
    {"ticker": "EWJ",  "bucket": "Japan",       "label": "MSCI Japan"},
    {"ticker": "AAXJ", "bucket": "AsiaExJapan", "label": "MSCI All Country Asia ex Japan"},
    {"ticker": "INDA", "bucket": "India",       "label": "MSCI India"},
    {"ticker": "EZU",  "bucket": "Europe",      "label": "MSCI Eurozone"},
    {"ticker": "IEUR", "bucket": "Europe",      "label": "Core MSCI Europe"},
    {"ticker": "EWG",  "bucket": "Europe",      "label": "MSCI Germany"},
    {"ticker": "EWU",  "bucket": "Europe",      "label": "MSCI United Kingdom"},
    {"ticker": "TLT",  "bucket": "Bonds",       "label": "20+ Year Treasury"},
    {"ticker": "IEF",  "bucket": "Bonds",       "label": "7-10 Year Treasury"},
    {"ticker": "AGG",  "bucket": "Bonds",       "label": "US Aggregate Bond"},
    {"ticker": "IAU",  "bucket": "Gold",        "label": "Gold Trust"},
    {"ticker": "SHV",  "bucket": "Cash",        "label": "Short Treasury (cash proxy)"},
    {"ticker": "HYG",  "bucket": "Credit",      "label": "High Yield Corporate"},
]
PANEL_TICKERS = [e["ticker"] for e in ETF_PANEL]
BUCKETS = {e["ticker"]: e["bucket"] for e in ETF_PANEL}

# US sector panel (all iShares so the fundDownload endpoint covers flows).
SECTOR_PANEL = {
    "IYW": "Technology", "IGV": "Software", "SOXX": "Semiconductors", "IGM": "Tech-Media-Telecom",
    "IYF": "Financials", "IYE": "Energy", "IYH": "Healthcare", "IBB": "Biotech", "IHI": "Medical devices",
    "IYJ": "Industrials", "ITA": "Aerospace & defense", "IYK": "Consumer staples", "IYC": "Consumer discretionary",
    "IDU": "Utilities", "IYM": "Materials", "IYZ": "Telecom", "IYR": "Real estate",
}

# Region groups used by rotation metrics (US vs rest-of-world equity).
ROW_EQUITY_BUCKETS = {"EM", "China", "Taiwan", "Korea", "Japan", "AsiaExJapan", "India", "Europe"}
US_EQUITY_BUCKETS = {"US", "US_smallcap"}
DEFENSIVE_BUCKETS = {"Bonds", "Gold", "Cash"}

# FRED series pulled via fredgraph.csv (no API key needed).
FRED_SERIES = {
    "VIXCLS": "CBOE VIX",
    "DGS2": "2y Treasury yield",
    "DGS10": "10y Treasury yield",
    "DCOILWTICO": "WTI crude",
    "DTWEXBGS": "Broad dollar index (2006-)",
    "DTWEXM": "Major currencies dollar index (1973-2019)",
    "DEXUSEU": "USD per EUR",
    "DEXJPUS": "JPY per USD",
    "DEXCHUS": "CNY per USD",
    "DEXTAUS": "TWD per USD",
    "DEXKOUS": "KRW per USD",
    "WRMFSL": "Retail money market funds (H.6, weekly to 2021 then monthly)",
    "MMMFFAQ027S": "Money market funds total assets (Z.1 quarterly)",
}

STOOQ_INDEX_TICKERS = {"^spx": "S&P 500 index"}

ISHARES_BASE = "https://www.ishares.com"
ISHARES_SCREENER = (
    ISHARES_BASE
    + "/us/product-screener/product-screener-v3.1.jsn"
    + "?dcrPath=/templatedata/config/product-screener-v3/data/en/us-ishares/"
    + "ishares-product-screener-backend-config&siteEntryPassthrough=true"
)
