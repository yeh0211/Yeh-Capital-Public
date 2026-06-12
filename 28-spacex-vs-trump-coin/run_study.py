#!/usr/bin/env python3
"""Study 26 — SpaceX IPO vs the TRUMP coin launch.

Three tests:
  1. TRUMP launch event study on its host market (Solana / crypto majors /
     memecoin basket): liquidity vacuum + top-marking.
  2. Mega-IPO base rate: NASDAQ Composite and S&P 500 forward returns after
     the 34 largest US-listed IPOs (1996-2024) vs the unconditional
     distribution over the same era.
  3. Relative-scale test: event size as a share of host-market turnover,
     TRUMP weekend vs SpaceX IPO.

Inputs: ./data/*.csv (see pull_data.py). Outputs: results.json,
ipo_event_returns.csv, fig1..fig4 PNGs.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"

# House style
CREAM = "#faf8f3"
INK = "#1c1a17"
GREY = "#7a8a78"
ACCENT = "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e4ded2", "grid.linewidth": 0.6,
})

HORIZONS = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}


def load_close(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    s = df.set_index("date")["close"].astype(float).sort_index()
    return s[~s.index.duplicated()]


def load_high(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    s = df.set_index("date")["high"].astype(float).sort_index()
    return s[~s.index.duplicated()]


# ----------------------------------------------------------------------
# Test 1 — TRUMP launch event study
# ----------------------------------------------------------------------

def test1() -> dict:
    trump = load_close("TRUMPUSDT")
    sol = load_close("SOLUSDT")
    btc = load_close("BTCUSDT")
    eth = load_close("ETHUSDT")
    basket_names = ["DOGEUSDT", "SHIBUSDT", "PEPEUSDT", "WIFUSDT", "BONKUSDT"]
    basket_px = pd.concat({n: load_close(n) for n in basket_names}, axis=1)

    launch = pd.Timestamp("2025-01-17")          # Meteora launch (Fri night UTC-5)
    anchor = pd.Timestamp("2025-01-16")          # last full pre-launch day
    window_end = pd.Timestamp("2025-06-30")

    basket = (basket_px / basket_px.loc[anchor]).mean(axis=1) * 100.0

    def peak_in_window(s: pd.Series, lo: str, hi: str):
        w = s.loc[lo:hi]
        return w.idxmax().date().isoformat(), float(w.max())

    # peaks use intraday highs (Binance listed TRUMP mid-day Jan 19; daily
    # closes understate the documented extremes)
    sol_peak_d, sol_peak = peak_in_window(load_high("SOLUSDT"), "2024-10-01", "2025-06-30")
    btc_peak_d, btc_peak = peak_in_window(load_high("BTCUSDT"), "2024-10-01", "2025-03-31")
    trump_peak_d, trump_peak = peak_in_window(load_high("TRUMPUSDT"), "2025-01-19", "2025-06-30")

    def at_offset(s: pd.Series, days: int) -> float:
        target = launch + pd.Timedelta(days=days)
        return float(s.asof(target))

    res = {
        "launch_date": "2025-01-17",
        "binance_listing_date": trump.index.min().date().isoformat(),
        "trump_peak": {"date": trump_peak_d, "price": round(trump_peak, 2)},
        "sol_peak": {"date": sol_peak_d, "price": round(sol_peak, 2),
                     "days_after_launch": (pd.Timestamp(sol_peak_d) - launch).days},
        "btc_peak_q1": {"date": btc_peak_d, "price": round(btc_peak, 0),
                        "days_after_launch": (pd.Timestamp(btc_peak_d) - launch).days},
        "memecoin_basket_indexed_to_100_at_0116": {
            "launch_weekend_low_jan17_21": round(float(basket.loc["2025-01-17":"2025-01-21"].min()), 1),
            "plus_30d": round(at_offset(basket, 30), 1),
            "plus_90d": round(at_offset(basket, 90), 1),
            "plus_180d": round(at_offset(basket, 180), 1),
            "max_after_launch_thru_jun2025": round(float(basket.loc[launch:window_end].max()), 1),
            "max_after_launch_date": basket.loc[launch:window_end].idxmax().date().isoformat(),
        },
        "drawdowns_from_jan_peak_to_2025_06_30": {
            "TRUMP": round(float(trump.loc[:window_end].iloc[-1] / trump_peak - 1) * 100, 1),
            "SOL": round(float(sol.loc[:window_end].iloc[-1] / sol_peak - 1) * 100, 1),
            "BTC_to_april_low": round(float(btc.loc["2025-02-01":"2025-04-30"].min() / btc_peak - 1) * 100, 1),
        },
        "sol_now_vs_jan19_peak_pct": round(float(sol.iloc[-1] / sol_peak - 1) * 100, 1),
    }

    # Fig 1 — indexed performance around the launch
    fig, ax = plt.subplots(figsize=(9, 5))
    lo, hi = pd.Timestamp("2024-11-01"), pd.Timestamp("2025-06-30")
    for s, label, color, lw in [
        (btc, "Bitcoin", INK, 1.4),
        (sol, "Solana (SOL)", "#5a5145", 1.4),
        (basket_px.mean(axis=1, skipna=False), None, None, 0),  # placeholder, basket below
    ][:2]:
        idx = (s / s.loc[anchor]) * 100
        ax.plot(idx.loc[lo:hi].index, idx.loc[lo:hi], label=label, color=color, linewidth=lw)
    ax.plot(basket.loc[lo:hi].index, basket.loc[lo:hi], label="Memecoin basket (DOGE/SHIB/PEPE/WIF/BONK, eq-wt)",
            color=GREY, linewidth=1.4)
    tr_idx = (trump / trump_peak) * 100  # TRUMP scaled to 100 at its own peak
    ax.plot(tr_idx.loc[:hi].index, tr_idx.loc[:hi], label="TRUMP (100 = Jan 19 peak)",
            color=ACCENT, linewidth=1.8)
    ax.axvline(pd.Timestamp("2025-01-17"), color=ACCENT, linestyle=":", linewidth=1.2)
    ax.text(pd.Timestamp("2025-01-19"), ax.get_ylim()[1] * 0.97, "TRUMP launch\nJan 17, 2025",
            fontsize=8.5, color=ACCENT, va="top")
    ax.set_ylabel("Indexed level (100 = Jan 16, 2025)")
    ax.set_title("The TRUMP launch marked the top of its host market", loc="left", fontsize=12, color=INK)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.tight_layout()
    fig.savefig(HERE / "fig1_trump_event_study.png", dpi=160)
    plt.close(fig)
    return res


# ----------------------------------------------------------------------
# Test 2 — mega-IPO base rate
# ----------------------------------------------------------------------

def forward_returns(level: pd.Series, dates: list[pd.Timestamp]) -> pd.DataFrame:
    """Forward returns from the close on/just before each date."""
    px = level.values
    idx = level.index
    out = []
    for d in dates:
        i = idx.searchsorted(d, side="right") - 1
        row = {"date": idx[i]}
        for label, h in HORIZONS.items():
            row[label] = px[i + h] / px[i] - 1 if i + h < len(px) else np.nan
        out.append(row)
    return pd.DataFrame(out)


def base_rate(level: pd.Series, lo: str, hi: str) -> pd.DataFrame:
    w = level.loc[lo:hi]
    px, n = w.values, len(w)
    full = level.loc[lo:].values
    rows = {}
    for label, h in HORIZONS.items():
        fr = np.array([full[i + h] / full[i] - 1 for i in range(n) if i + h < len(full)])
        rows[label] = fr
    return rows


def test2() -> tuple[dict, pd.DataFrame]:
    ndq = load_close("nasdaq_composite")
    spx = load_close("sp500")
    ipos = pd.read_csv(DATA / "mega_ipos.csv", parse_dates=["first_trade_date"])

    ev_ndq = forward_returns(ndq, list(ipos["first_trade_date"]))
    ev_spx = forward_returns(spx, list(ipos["first_trade_date"]))
    base_ndq = base_rate(ndq, "1996-01-01", "2025-06-10")
    base_spx = base_rate(spx, "1996-01-01", "2025-06-10")

    table = ipos[["ticker", "company", "first_trade_date", "proceeds_usd_b"]].copy()
    for label in HORIZONS:
        table[f"ndq_{label}"] = (ev_ndq[label] * 100).round(2)
        table[f"spx_{label}"] = (ev_spx[label] * 100).round(2)
    table.to_csv(HERE / "ipo_event_returns.csv", index=False)

    def summarize(ev: pd.DataFrame, base: dict) -> dict:
        out = {}
        for label in HORIZONS:
            e = ev[label].dropna().values
            b = base[label]
            out[label] = {
                "event_median_pct": round(float(np.median(e)) * 100, 2),
                "event_mean_pct": round(float(np.mean(e)) * 100, 2),
                "event_pct_positive": round(float((e > 0).mean()) * 100, 1),
                "base_median_pct": round(float(np.median(b)) * 100, 2),
                "base_mean_pct": round(float(np.mean(b)) * 100, 2),
                "base_pct_positive": round(float((b > 0).mean()) * 100, 1),
                "event_median_percentile_of_base": round(
                    float((b < np.median(e)).mean()) * 100, 1),
            }
        return out

    # bootstrap: median 12m forward return of 34 random dates, 10k draws
    rng = np.random.default_rng(26)
    b12 = base_ndq["12m"]
    n_ev = int(ev_ndq["12m"].notna().sum())
    boot = np.array([np.median(rng.choice(b12, n_ev, replace=False)) for _ in range(10_000)])
    ev_med = float(np.median(ev_ndq["12m"].dropna()))
    p_lower = float((boot <= ev_med).mean())

    # forward-looking max drawdown within 12m of each day
    def fwd_max_dd(level: pd.Series, i: int, h: int = 252) -> float:
        seg = level.values[i:i + h + 1]
        runmax = np.maximum.accumulate(seg)
        return float((seg / runmax - 1).min())

    ndq_idx = ndq.index
    ev_dd = []
    for d in ipos["first_trade_date"]:
        i = ndq_idx.searchsorted(d, side="right") - 1
        if i + 252 < len(ndq):
            ev_dd.append(fwd_max_dd(ndq, i))
    lo_i = ndq_idx.searchsorted(pd.Timestamp("1996-01-01"))
    base_dd = np.array([fwd_max_dd(ndq, i) for i in range(lo_i, len(ndq) - 252, 5)])
    ev_dd = np.array(ev_dd)

    res = {
        "n_ipos": int(len(ipos)),
        "nasdaq": summarize(ev_ndq, base_ndq),
        "sp500": summarize(ev_spx, base_spx),
        "bootstrap_12m_nasdaq": {
            "event_median_pct": round(ev_med * 100, 2),
            "p_random_dates_median_below_event": round(p_lower, 3),
        },
        "nasdaq_max_drawdown_within_12m": {
            "event_median_pct": round(float(np.median(ev_dd)) * 100, 1),
            "base_median_pct": round(float(np.median(base_dd)) * 100, 1),
            "event_pct_with_dd_worse_than_20": round(float((ev_dd <= -0.20).mean()) * 100, 1),
            "base_pct_with_dd_worse_than_20": round(float((base_dd <= -0.20).mean()) * 100, 1),
        },
    }

    # Robustness 1 — drop the five H1-2000 IPOs (the dot-com cluster)
    yr2000 = ipos["first_trade_date"].dt.year == 2000
    ex2000 = ev_ndq.loc[~yr2000.values, "12m"].dropna()
    res["robustness_ex_2000_cluster"] = {
        "n": int(len(ex2000)),
        "event_median_12m_pct": round(float(np.median(ex2000)) * 100, 2),
        "event_pct_positive": round(float((ex2000 > 0).mean()) * 100, 1),
    }

    # Robustness 2 — rival: "the tape was already hot". Base rate conditioned
    # on trailing 12m NASDAQ return at least as hot as the median event's.
    ndq_px = ndq.values
    trail = np.full(len(ndq_px), np.nan)
    trail[252:] = ndq_px[252:] / ndq_px[:-252] - 1
    ev_trail = []
    for d in ipos["first_trade_date"]:
        i = ndq_idx.searchsorted(d, side="right") - 1
        ev_trail.append(trail[i])
    ev_trail = np.array(ev_trail)
    med_trail = float(np.nanmedian(ev_trail))
    fwd12 = np.full(len(ndq_px), np.nan)
    fwd12[:-252] = ndq_px[252:] / ndq_px[:-252] - 1
    mask = (np.arange(len(ndq_px)) >= ndq_idx.searchsorted(pd.Timestamp("1996-01-01"))) \
        & (trail >= med_trail) & ~np.isnan(fwd12)
    hot_base = fwd12[mask]
    res["robustness_hot_tape_base"] = {
        "median_event_trailing_12m_pct": round(med_trail * 100, 1),
        "n_hot_days": int(mask.sum()),
        "hot_base_median_fwd12_pct": round(float(np.median(hot_base)) * 100, 2),
        "hot_base_pct_positive": round(float((hot_base > 0).mean()) * 100, 1),
    }

    # Fig 2 — median indexed NASDAQ path around mega-IPO dates vs random base
    fig, ax = plt.subplots(figsize=(9, 5))
    px, idx = ndq.values, ndq.index
    paths = []
    for d in ipos["first_trade_date"]:
        i = idx.searchsorted(d, side="right") - 1
        if i - 60 >= 0 and i + 252 < len(px):
            paths.append(px[i - 60:i + 253] / px[i] * 100)
    P = np.vstack(paths)
    t = np.arange(-60, 253)
    med = np.median(P, axis=0)
    q25, q75 = np.percentile(P, 25, axis=0), np.percentile(P, 75, axis=0)
    # unconditional path 1996+
    lo_i = idx.searchsorted(pd.Timestamp("1996-01-01"))
    starts = np.arange(lo_i + 60, len(px) - 253, 5)
    B = np.vstack([px[i - 60:i + 253] / px[i] * 100 for i in starts])
    bmed = np.median(B, axis=0)
    ax.fill_between(t, q25, q75, color=GREY, alpha=0.25, linewidth=0)
    ax.plot(t, med, color=ACCENT, linewidth=1.8, label=f"Median around {len(paths)} mega-IPOs (IQR shaded)")
    ax.plot(t, bmed, color=INK, linewidth=1.4, linestyle="--", label="Median around all days, 1996-2025")
    ax.axvline(0, color=INK, linewidth=0.8, linestyle=":")
    ax.set_xlabel("Trading days from IPO")
    ax.set_ylabel("NASDAQ Composite (100 = IPO day)")
    ax.set_title("Markets after mega-IPOs vs the unconditional path", loc="left", fontsize=12)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig2_megaipo_event_path.png", dpi=160)
    plt.close(fig)

    # Fig 3 — 12m forward NASDAQ return per event, sorted
    fig, ax = plt.subplots(figsize=(9, 6.5))
    t3 = table.dropna(subset=["ndq_12m"]).sort_values("ndq_12m")
    labels = [f"{r.company} ({r.first_trade_date.year})" for r in t3.itertuples()]
    colors = [ACCENT if v < 0 else "#5a5145" for v in t3["ndq_12m"]]
    ax.barh(labels, t3["ndq_12m"], color=colors, height=0.7)
    ax.axvline(0, color=INK, linewidth=1)
    ax.axvline(np.median(base_ndq["12m"]) * 100, color=INK, linestyle="--", linewidth=1,
               label=f"Unconditional median ({np.median(base_ndq['12m'])*100:.1f}%)")
    ax.set_xlabel("NASDAQ Composite return, 12 months after IPO (%)")
    ax.set_title("Twelve months after each mega-IPO", loc="left", fontsize=12)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig3_megaipo_12m_bars.png", dpi=160)
    plt.close(fig)

    return res, table


# ----------------------------------------------------------------------
# Test 3 — relative scale
# ----------------------------------------------------------------------

def test3() -> dict:
    # Documented constants (sources in README)
    sol_baseline_dex_daily = 6.0      # $B/day pre-launch (Helius/DefiLlama)
    sol_peak_dex_daily = 39.2         # $B Jan 20, 2025
    sol_stable_before, sol_stable_after = 6.15, 10.6  # $B, Jan 17 -> 23
    spacex_raise = 75.0               # $B
    spacex_retail = 0.30 * spacex_raise
    spacex_shares_b = 13.08           # B shares outstanding post-IPO (Reuters)
    us_equity_mcap = 72_000.0         # $B (Siblis: $69.0T Jan 2026; Visual Capitalist: >$75T Apr 2026)
    us_equity_mcap_2021 = 50_000.0    # $B (approx, early 2021)
    us_equity_adv = 1_100.0           # $B/day (Cboe: 2025 US equities ADNV $1.1T)
    sol_mcap_jan2025 = 140.0          # $B (SOL market cap mid-Jan 2025, approx)
    crypto_total_mcap_jan2025 = 3_800.0  # $B (cycle peak, mid-Jan 2025)
    trump_peak_fdv = 75.0             # $B (peak price ~$75 x 1B total supply)
    trump_peak_circ = 15.0            # $B (200M circulating x ~$75)
    gme_peak_mcap_close = 24.2        # $B (close peak $347.51 x 69.75M shares)

    res = {
        "trump_peak_dex_volume_x_baseline": round(sol_peak_dex_daily / sol_baseline_dex_daily, 1),
        "trump_stablecoin_float_growth_6d_pct": round((sol_stable_after / sol_stable_before - 1) * 100, 1),
        "spacex_raise_pct_of_us_mcap": round(spacex_raise / us_equity_mcap * 100, 3),
        "spacex_raise_pct_of_one_day_volume": round(spacex_raise / us_equity_adv * 100, 1),
        "spacex_retail_tranche_usd_b": round(spacex_retail, 1),
        "trump_fdv_peak_pct_of_sol_mcap": round(trump_peak_fdv / sol_mcap_jan2025 * 100, 1),
        "trump_fdv_peak_pct_of_total_crypto": round(trump_peak_fdv / crypto_total_mcap_jan2025 * 100, 2),
        "trump_circ_mcap_pct_of_total_crypto": round(trump_peak_circ / crypto_total_mcap_jan2025 * 100, 2),
        "spacex_mcap_at_135_pct_of_us": round(spacex_shares_b * 135 / us_equity_mcap * 100, 2),
        "spacex_mcap_at_170_pct_of_us": round(spacex_shares_b * 170 / us_equity_mcap * 100, 2),
        "gme_peak_mcap_pct_of_us_2021": round(gme_peak_mcap_close / us_equity_mcap_2021 * 100, 3),
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axes[0]
    items = [
        ("GME close peak / US equities (2021)", res["gme_peak_mcap_pct_of_us_2021"]),
        ("TRUMP peak FDV / all crypto", res["trump_fdv_peak_pct_of_total_crypto"]),
        ("SpaceX at $135 / US equities", res["spacex_mcap_at_135_pct_of_us"]),
        ("SpaceX at $170 / US equities", res["spacex_mcap_at_170_pct_of_us"]),
        ("TRUMP peak FDV / its host chain (SOL)", res["trump_fdv_peak_pct_of_sol_mcap"]),
    ]
    vals = [v for _, v in items]
    ax.barh([k for k, _ in items], vals,
            color=[GREY, ACCENT, "#5a5145", "#5a5145", ACCENT], height=0.55)
    ax.set_xscale("log")
    ax.set_xlim(None, max(vals) * 12)
    ax.set_xlabel("Asset value as % of host asset class (log scale)")
    for y, v in enumerate(vals):
        ax.text(v * 1.2, y, f"{v:,.2f}%", va="center", fontsize=8.5, color=INK)
    ax.set_title("Stock: instant size vs the whole class", loc="left", fontsize=11)

    ax = axes[1]
    items2 = [
        ("GME peak day / US tape (approx)", 32.5 / 600 * 100),
        ("SpaceX raise / one day of US volume", res["spacex_raise_pct_of_one_day_volume"]),
        ("TRUMP peak-day DEX vol / host baseline", res["trump_peak_dex_volume_x_baseline"] * 100),
    ]
    vals2 = [v for _, v in items2]
    ax.barh([k for k, _ in items2], vals2, color=[GREY, "#5a5145", ACCENT], height=0.45)
    ax.set_xscale("log")
    ax.set_xlim(None, max(vals2) * 12)
    ax.set_xlabel("Event flow vs host turnover (%, log scale)")
    for y, v in enumerate(vals2):
        ax.text(v * 1.2, y, f"{v:,.1f}%", va="center", fontsize=8.5, color=INK)
    ax.set_title("Flow: trading shock vs host tape", loc="left", fontsize=11)
    fig.suptitle("Same pattern, different dose: size of each mania vs its host market",
                 x=0.01, ha="left", fontsize=12.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(HERE / "fig4_relative_scale.png", dpi=160)
    plt.close(fig)
    return res


# ----------------------------------------------------------------------
# Test 4 — the GameStop control case (low-float squeeze, January 2021)
# ----------------------------------------------------------------------

def test4() -> dict:
    gme = pd.read_csv(DATA / "GME.csv", parse_dates=["date"]).set_index("date").sort_index()
    spx = load_close("sp500")
    ndq = load_close("nasdaq_composite")

    peak_d = pd.Timestamp("2021-01-27")          # close peak (adj $86.88 = $347.51 unadj)
    close = gme["close"]
    peak = float(close.loc[peak_d])
    after = close.loc[peak_d:]

    # decay
    trough_1m = float(after.iloc[:25].min())
    trough_1m_d = after.iloc[:25].idxmin()
    sessions_to_trough = int(after.index.get_loc(trough_1m_d))
    echo_max = float(close.loc["2021-02-20":"2021-12-31"].max())
    one_year = float(close.asof(peak_d + pd.Timedelta(days=365)))

    # dollar volume, peak days (volume is unadjusted millions of shares;
    # prices are split-adjusted -> x4 before the July 2022 4-for-1 split)
    dv = {d: round(float(gme.loc[d, "volume"] * gme.loc[d, "close"] * 4 / 1000), 1)
          for d in ("2021-01-26", "2021-01-27", "2021-01-28")}

    # broad-market spillover: the degrossing week and the recovery
    pre = float(spx.asof(pd.Timestamp("2021-01-22")))
    low_wk = float(spx.loc["2021-01-25":"2021-01-29"].min())
    rec = spx.loc["2021-02-01":]
    recovery_day = rec[rec >= pre].index[0]
    ndq_pre = float(ndq.asof(pd.Timestamp("2021-01-22")))
    ndq_low = float(ndq.loc["2021-01-25":"2021-01-29"].min())

    res = {
        "close_peak": {"date": "2021-01-27", "adj": round(peak, 2), "unadjusted": 347.51},
        "intraday_high_jan28_unadjusted": 483.0,
        "drawdown_to_feb_trough_pct": round((trough_1m / peak - 1) * 100, 1),
        "sessions_peak_to_trough": sessions_to_trough,
        "echo_high_2021_pct_of_peak": round(echo_max / peak * 100, 1),
        "one_year_later_pct_of_peak": round(one_year / peak * 100, 1),
        "peak_day_dollar_volume_usd_b": dv,
        "spx_degross_week_pct": round((low_wk / pre - 1) * 100, 2),
        "ndq_degross_week_pct": round((ndq_low / ndq_pre - 1) * 100, 2),
        "spx_sessions_to_recover": int(spx.loc["2021-01-25":recovery_day].shape[0]),
    }

    # Fig 5 — decay paths from the peak close: GME vs TRUMP
    fig, ax = plt.subplots(figsize=(9, 5))
    gme_path = (after.iloc[:131] / peak) * 100
    trump = load_close("TRUMPUSDT")
    tpeak_d = trump.loc["2025-01-19":"2025-06-30"].idxmax()
    tafter = trump.loc[tpeak_d:]
    trump_path = (tafter.iloc[:131] / float(trump.loc[tpeak_d])) * 100
    ax.plot(range(len(gme_path)), gme_path.values, color=INK, linewidth=1.6,
            label="GameStop from Jan 27, 2021 close peak")
    ax.plot(range(len(trump_path)), trump_path.values, color=ACCENT, linewidth=1.6,
            label="TRUMP from Jan 19, 2025 close peak")
    ax.axhline(100 - 14.7, color=GREY, linestyle="--", linewidth=1.2)
    ax.text(2, 86.8, "large-IPO comp median at 6 months (-14.7%, study 24)",
            fontsize=8.5, color=GREY)
    ax.set_xlabel("Trading days from peak close")
    ax.set_ylabel("Price (100 = peak close)")
    ax.set_ylim(0, 105)
    ax.set_title("After the vertical: what low-float manias do next", loc="left", fontsize=12)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig5_lowfloat_decay.png", dpi=160)
    plt.close(fig)
    return res


# ----------------------------------------------------------------------
# Test 5 — cross-check with study 15: do mega-IPO stocks chase any better?
# ----------------------------------------------------------------------

# Study 15 base rates (760 IPOs, 2022-10+ vintage, day-1 close entry,
# excess vs SPY): median -15.4% at 180d (25% beat), -28.4% at 365d (19% beat).
STUDY15 = {"6m": {"median_excess": -15.4, "pct_beat": 25.0},
           "12m": {"median_excess": -28.4, "pct_beat": 19.0}}


def test5() -> dict:
    ndq = load_close("nasdaq_composite")
    spx = load_close("sp500")
    ipos = pd.read_csv(DATA / "mega_ipos.csv", parse_dates=["first_trade_date"])
    rows = []
    for f in sorted((DATA / "megastocks").glob("*.csv")):
        tick = f.stem
        px = pd.read_csv(f, parse_dates=["date"]).set_index("date").sort_index()
        # macrotrends prepends an offer-price placeholder row (volume 0)
        # and, for some names, when-issued rows before the listing date
        sample_tick = {"META": "FB"}.get(tick, tick)
        ftd = ipos.loc[ipos["ticker"] == sample_tick, "first_trade_date"].iloc[0]
        live = px[(px.index >= ftd) & (px["volume"] > 0)]["close"]
        day1 = float(live.iloc[0])
        day1_d = live.index[0]
        out = {"ticker": tick, "day1_close_date": day1_d.date().isoformat()}
        for label, h in (("6m", 126), ("12m", 252)):
            if len(live) <= h:
                out[f"abs_{label}"] = np.nan
                out[f"excess_ndq_{label}"] = out[f"excess_spx_{label}"] = np.nan
                continue
            stock_r = live.iloc[h] / day1 - 1
            out[f"abs_{label}"] = round(stock_r * 100, 1)
            for bname, bser in (("ndq", ndq), ("spx", spx)):
                i = bser.index.searchsorted(day1_d, side="right") - 1
                idx_r = bser.values[i + h] / bser.values[i] - 1
                out[f"excess_{bname}_{label}"] = round((stock_r - idx_r) * 100, 1)
        rows.append(out)
    t = pd.DataFrame(rows)
    t.to_csv(HERE / "megaipo_chase_returns.csv", index=False)

    summary = {"n": int(len(t)), "study15_base": STUDY15}
    for label in ("6m", "12m"):
        a = t[f"abs_{label}"].dropna()
        summary[label] = {"median_abs_pct": round(float(a.median()), 1)}
        for bname in ("ndq", "spx"):
            e = t[f"excess_{bname}_{label}"].dropna()
            summary[label][f"median_excess_{bname}_pct"] = round(float(e.median()), 1)
            summary[label][f"pct_beating_{bname}"] = round(float((e > 0).mean()) * 100, 1)

    # Fig 6 — per-name 12m S&P excess (study 15's benchmark family) vs its base rate
    fig, ax = plt.subplots(figsize=(9, 4.8))
    t6 = t.dropna(subset=["excess_spx_12m"]).sort_values("excess_spx_12m")
    colors = [ACCENT if v < 0 else "#5a5145" for v in t6["excess_spx_12m"]]
    ax.barh(t6["ticker"], t6["excess_spx_12m"], color=colors, height=0.6)
    ax.axvline(0, color=INK, linewidth=1)
    ax.axvline(STUDY15["12m"]["median_excess"], color=GREY, linestyle="--", linewidth=1.3,
               label="Study 15 broad-IPO median excess at 1y (-28.4%)")
    med = float(t6["excess_spx_12m"].median())
    ax.axvline(med, color=ACCENT, linestyle=":", linewidth=1.3,
               label=f"Mega-IPO subset median ({med:+.1f}%)")
    ax.set_xlabel("Stock return minus S&P 500, 12 months from day-1 close (%)")
    ax.set_title("Chasing the mega-IPOs themselves, vs study 15's broad base rate",
                 loc="left", fontsize=12)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(HERE / "fig6_megaipo_chase_vs_study15.png", dpi=160)
    plt.close(fig)
    return summary


def main() -> None:
    results = {"test1_trump_event_study": test1()}
    t2, _ = test2()
    results["test2_megaipo_base_rate"] = t2
    results["test3_relative_scale"] = test3()
    results["test4_gme_control_case"] = test4()
    results["test5_study15_crosscheck"] = test5()
    (HERE / "results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
