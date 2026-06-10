"""Event-study engine: cumulative (abnormal) returns and flows around event dates.

Conventions
-----------
- Daily paths are cumulative log returns normalized to 0 at the event reaction
  day (first trading day on/after the event date): path[k] = ln(P[t0+k] / P[t0]).
  So the pre-event segment reads as the run-up INTO the event.
- Weekly flow paths use flow as a percent of fund AUM, cumulated over the
  window (CAF, in percentage points of AUM), normalized to 0 at the event week.
- Sample sizes are tiny by construction (9 presidential, 8 midterms). Outputs
  are median paths, per-event paths, and sign hit-rates. No t-stats on n=9.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import BUCKETS, DATA_DIR, US_EQUITY_BUCKETS, ROW_EQUITY_BUCKETS

# ---------------------------------------------------------------- loading


def load_prices() -> pd.DataFrame:
    """Close-price panel, columns = ticker/index names."""
    frames = {}
    for p in sorted((DATA_DIR / "prices").glob("*.parquet")):
        df = pd.read_parquet(p)
        if "close" in df.columns:
            frames[p.stem] = df["close"]
    panel = pd.DataFrame(frames).sort_index()
    panel.index = pd.to_datetime(panel.index)
    return panel


def load_fund_histories() -> dict[str, pd.DataFrame]:
    """Per-ticker daily NAV / shares outstanding / AUM from the iShares pull."""
    out = {}
    for p in sorted((DATA_DIR / "ishares").glob("*.parquet")):
        df = pd.read_parquet(p).sort_index()
        df.index = pd.to_datetime(df.index)
        out[p.stem] = df
    return out


def daily_flows(fund: pd.DataFrame) -> pd.DataFrame:
    """flow_usd = change in shares outstanding * NAV; aum = shares * NAV."""
    df = fund.copy()
    df = df[(df["nav"] > 0) & (df["shares"] > 0)]
    df["aum"] = df["nav"] * df["shares"]
    df["flow_usd"] = df["shares"].diff() * df["nav"]
    return df


def weekly_flow_pct(fund: pd.DataFrame) -> pd.Series:
    """Weekly net flow as percent of prior-week AUM (W-FRI)."""
    d = daily_flows(fund)
    wk_flow = d["flow_usd"].resample("W-FRI").sum()
    wk_aum = d["aum"].resample("W-FRI").last().shift(1)
    pct = (wk_flow / wk_aum) * 100.0
    return pct.replace([np.inf, -np.inf], np.nan).dropna()


def flow_zscore(pct: pd.Series, window: int = 52, min_periods: int = 26) -> pd.Series:
    mu = pct.rolling(window, min_periods=min_periods).mean()
    sd = pct.rolling(window, min_periods=min_periods).std()
    return (pct - mu) / sd


def group_weekly_flow_pct(funds: dict[str, pd.DataFrame], buckets: set[str]) -> pd.Series:
    """AUM-weighted weekly flow percent across all panel funds in the given buckets."""
    flows, aums = [], []
    for t, fund in funds.items():
        if BUCKETS.get(t) not in buckets:
            continue
        d = daily_flows(fund)
        flows.append(d["flow_usd"].resample("W-FRI").sum().rename(t))
        aums.append(d["aum"].resample("W-FRI").last().shift(1).rename(t))
    if not flows:
        return pd.Series(dtype=float)
    f = pd.concat(flows, axis=1).sum(axis=1, min_count=1)
    a = pd.concat(aums, axis=1).sum(axis=1, min_count=1)
    return ((f / a) * 100.0).replace([np.inf, -np.inf], np.nan).dropna()


# ---------------------------------------------------------------- windows


def reaction_iloc(index: pd.DatetimeIndex, date) -> int | None:
    """First position on/after date; None if out of range."""
    i = index.searchsorted(pd.Timestamp(date))
    return int(i) if i < len(index) else None


def daily_path(series: pd.Series, date, pre: int = 120, post: int = 120) -> pd.Series | None:
    """Cumulative log-return path around date, normalized to 0 at reaction day."""
    s = series.dropna()
    i = reaction_iloc(s.index, date)
    if i is None or i - pre < 0:
        return None
    j = min(i + post, len(s) - 1)
    seg = s.iloc[i - pre : j + 1]
    path = np.log(seg / s.iloc[i]) * 100.0
    path.index = np.arange(-pre, j - i + 1)
    return path


def level_path(series: pd.Series, date, pre: int = 120, post: int = 120) -> pd.Series | None:
    """Raw level path (e.g. VIX) around date, indexed by relative trading day."""
    s = series.dropna()
    i = reaction_iloc(s.index, date)
    if i is None or i - pre < 0:
        return None
    j = min(i + post, len(s) - 1)
    seg = s.iloc[i - pre : j + 1].copy()
    seg.index = np.arange(-pre, j - i + 1)
    return seg


def weekly_caf_path(pct: pd.Series, date, pre_w: int = 26, post_w: int = 26) -> pd.Series | None:
    """Cumulative flow (pct of AUM) around the event week, 0 at event week."""
    s = pct.dropna()
    i = reaction_iloc(s.index, date)
    if i is None or i - pre_w < 0:
        return None
    j = min(i + post_w, len(s) - 1)
    seg = s.iloc[i - pre_w : j + 1]
    path = seg.cumsum() - seg.cumsum().iloc[pre_w]
    path.index = np.arange(-pre_w, j - i + 1)
    return path


# ---------------------------------------------------------------- cohorts


def stack_paths(paths: dict[str, pd.Series | None]) -> pd.DataFrame:
    """Stack per-event paths into a rel-time x event frame (drops Nones)."""
    keep = {k: v for k, v in paths.items() if v is not None}
    return pd.DataFrame(keep)


def cohort_summary(stacked: pd.DataFrame, horizons=(20, 60, 120)) -> pd.DataFrame:
    """Median path values and sign hit-rates at +/- horizons."""
    rows = []
    for h in horizons:
        if h in stacked.index:
            post = stacked.loc[h].dropna()
            rows.append({
                "horizon": f"+{h}", "median": post.median(),
                "hit_rate_pos": (post > 0).mean(), "n": len(post),
            })
        if -h in stacked.index:
            pre = -stacked.loc[-h].dropna()  # run-up INTO the event over last h obs
            rows.append({
                "horizon": f"pre{h}", "median": pre.median(),
                "hit_rate_pos": (pre > 0).mean(), "n": len(pre),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- regimes


def realized_vol(returns: pd.Series, window: int = 21) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(252) * 100.0


def admin_regime_table(spx: pd.Series, vix: pd.Series, admins: pd.DataFrame) -> pd.DataFrame:
    """Per-administration return/vol stats."""
    r = np.log(spx / spx.shift(1)).dropna()
    rows = []
    for _, a in admins.iterrows():
        start, end = a["start"], a["end"] if pd.notna(a["end"]) else r.index.max()
        seg = r.loc[start:end]
        if len(seg) < 60:
            continue
        v = vix.reindex(seg.index).dropna()
        rows.append({
            "admin": a["admin"], "party": a["party"],
            "ann_return_pct": seg.mean() * 252 * 100,
            "ann_vol_pct": seg.std() * np.sqrt(252) * 100,
            "share_big_days_pct": (seg.abs() > 0.01).mean() * 100,
            "vix_mean": v.mean() if len(v) else np.nan,
            "vix_p90": v.quantile(0.9) if len(v) else np.nan,
            "worst_day_pct": seg.min() * 100,
            "best_day_pct": seg.max() * 100,
            "days": len(seg),
        })
    return pd.DataFrame(rows)


def us_minus_row_weekly(funds: dict[str, pd.DataFrame]) -> pd.Series:
    """Rotation series: US equity flow pct minus rest-of-world equity flow pct."""
    us = group_weekly_flow_pct(funds, US_EQUITY_BUCKETS)
    row = group_weekly_flow_pct(funds, ROW_EQUITY_BUCKETS)
    return (us - row).dropna()
