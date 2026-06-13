#!/usr/bin/env python3
"""Study 29, Chapter 3 — which past market most resembles June 2026?

Two independent reads:
  1. Regime fingerprint: month-end feature vector (trailing returns, realized
     vol, drawdown state, tech leadership) z-scored over 1996+; nearest
     neighbors to the latest month by Euclidean distance; what followed each.
  2. Price-action analog: correlation of the last 120 trading days of NASDAQ
     daily returns against every historical 120-day window since 1990.

Output: ch3_results.json + fig2 (analog paths).
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
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})


def load(name: str) -> pd.Series:
    df = pd.read_csv(DATA / f"{name}.csv", parse_dates=["date"])
    return df.set_index("date")["close"].astype(float).sort_index()


def main() -> None:
    ndq, spx = load("nasdaq_composite"), load("sp500")

    # ---- 1. monthly regime fingerprint ----
    m = ndq.resample("ME").last()
    spx_m = spx.resample("ME").last()
    dret = ndq.pct_change()
    feats = pd.DataFrame({
        "ret_12m": m.pct_change(12),
        "ret_3m": m.pct_change(3),
        "vol_63d": dret.rolling(63).std().resample("ME").last() * np.sqrt(252),
        "dd_from_high": m / m.rolling(60, min_periods=12).max() - 1,
        "tech_rel_12m": m.pct_change(12) - spx_m.reindex(m.index, method="ffill").pct_change(12),
    }).dropna()
    feats = feats.loc["1990-01-01":]
    z = (feats - feats.mean()) / feats.std()
    target = z.iloc[-1]
    hist = z.iloc[:-13]                       # exclude the last year (trivial self-matches)
    dist = np.sqrt(((hist - target) ** 2).sum(axis=1))
    nn = dist.nsmallest(10)
    fwd = {}
    analogs = []
    for d8, dv in nn.items():
        i = m.index.get_loc(d8)
        f6 = m.iloc[i + 6] / m.iloc[i] - 1 if i + 6 < len(m) else np.nan
        f12 = m.iloc[i + 12] / m.iloc[i] - 1 if i + 12 < len(m) else np.nan
        analogs.append({"month": d8.strftime("%Y-%m"), "distance": round(float(dv), 2),
                        "fwd_6m_pct": round(float(f6) * 100, 1) if np.isfinite(f6) else None,
                        "fwd_12m_pct": round(float(f12) * 100, 1) if np.isfinite(f12) else None})
    f6s = [a["fwd_6m_pct"] for a in analogs if a["fwd_6m_pct"] is not None]
    f12s = [a["fwd_12m_pct"] for a in analogs if a["fwd_12m_pct"] is not None]
    fingerprint = {
        "target_month": z.index[-1].strftime("%Y-%m"),
        "target_features": {k: round(float(feats.iloc[-1][k]), 4) for k in feats.columns},
        "top10_analogs": analogs,
        "analog_fwd_6m_median_pct": round(float(np.median(f6s)), 1),
        "analog_fwd_12m_median_pct": round(float(np.median(f12s)), 1),
        "analog_fwd_12m_pct_positive": round(float(np.mean([x > 0 for x in f12s])) * 100, 1),
        "base_fwd_12m_median_pct": round(float(m.pct_change(12).shift(-12).loc["1996":].median()) * 100, 1),
    }

    # ---- 2. price-action analog (120-day return-path correlation) ----
    r = ndq.pct_change().dropna()
    L = 120
    tail = r.iloc[-L:].values
    best = []
    vals = r.values
    for i in range(len(vals) - L - 252):
        w = vals[i:i + L]
        c = np.corrcoef(tail, w)[0, 1]
        best.append((c, i))
    best.sort(reverse=True)
    picked, used = [], []
    for c, i in best:
        d8 = r.index[i + L - 1]
        if any(abs((d8 - u).days) < 180 for u in used):
            continue
        used.append(d8)
        f6 = ndq.asof(d8 + pd.Timedelta(days=182)) / ndq.asof(d8) - 1
        f12 = ndq.asof(d8 + pd.Timedelta(days=365)) / ndq.asof(d8) - 1
        picked.append({"window_end": d8.date().isoformat(), "corr": round(float(c), 3),
                       "fwd_6m_pct": round(float(f6) * 100, 1), "fwd_12m_pct": round(float(f12) * 100, 1),
                       "_i": i})
        if len(picked) >= 5:
            break

    out = {"regime_fingerprint": fingerprint,
           "price_action_analogs_120d": [{k: v for k, v in p.items() if k != "_i"} for p in picked]}
    (HERE / "ch3_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

    # Fig — analog forward paths vs the current window
    fig, ax = plt.subplots(figsize=(9, 5))
    base_i = len(ndq) - L
    cur = ndq.iloc[-L:].values / ndq.iloc[-L] * 100
    ax.plot(range(-L, 0), cur, color=ACCENT, linewidth=2.0, label="NASDAQ, last 120 sessions")
    for p in picked:
        i = p["_i"]
        j = r.index[i + L - 1]
        jj = ndq.index.get_loc(ndq.index.asof(j))
        seg = ndq.iloc[max(0, jj - L + 1): jj + 253].values
        seg = seg / seg[L - 1] * 100 * (cur[-1] / 100)
        ax.plot(range(-L + 1, len(seg) - L + 1), seg, linewidth=1.1, color=GREY, alpha=0.8)
        ax.text(len(seg) - L + 2, seg[-1], p["window_end"][:7], fontsize=7.5, color=INK)
    ax.axvline(0, color=INK, linestyle=":", linewidth=1)
    ax.set_xlabel("Trading days (0 = today / analog window end)")
    ax.set_ylabel("Indexed level (current window end = current)")
    ax.set_title("The five closest 120-day NASDAQ path analogs, and what followed",
                 loc="left", fontsize=12)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig2_price_action_analogs.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
