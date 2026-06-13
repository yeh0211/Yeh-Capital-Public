#!/usr/bin/env python3
"""Study 29, Chapter 4 (cross-check) — bootstrap fan chart for SPCX.

Independent statistical companion to the MiroFish simulation: resample
12-month daily-return paths from the two empirical families SPCX belongs to
(study 28):
  A. mega-IPO chase paths from day-1 close (10 names, 2012-2023)
  B. low-float vertical decay paths (GME 2021, TRUMP 2025)
Blend A:B 70:30 (SPCX is an IPO first, a scarcity vertical second), block-
bootstrap 20-day segments, 10k paths from the $160.90 day-1 close.
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
S28 = HERE.parent / "28-spacex-vs-trump-coin"
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})

DAY1_CLOSE = 160.90
IPO_PRICE = 135.0
OPEN_PRICE = 150.0
H = 252
UNLOCK_DAYS = [70, 90, 105, 120, 135, 180]


def daily_returns_from_day1(csv: Path, vol_col: bool = True) -> np.ndarray | None:
    df = pd.read_csv(csv, parse_dates=["date"]).set_index("date").sort_index()
    px = df["close"].astype(float)
    if "volume" in df and vol_col:
        live = px[(df["volume"] > 0)]
    else:
        live = px
    r = live.pct_change().dropna().values[:H]
    return r if len(r) >= 120 else None


def main() -> None:
    fam_a = []
    for f in sorted((S28 / "data" / "megastocks").glob("*.csv")):
        r = daily_returns_from_day1(f)
        if r is not None:
            fam_a.append(r)
    # family B from the peak close (the scarcity-vertical decay regime)
    fam_b = []
    gme = pd.read_csv(S28 / "data" / "GME.csv", parse_dates=["date"]).set_index("date")["close"]
    fam_b.append(gme.loc["2021-01-27":].pct_change().dropna().values[:H])
    trump = pd.read_csv(S28 / "data" / "TRUMPUSDT.csv", parse_dates=["date"]).set_index("date")["close"]
    fam_b.append(trump.loc["2025-01-19":].pct_change().dropna().values[:H])

    rng = np.random.default_rng(29)
    BLOCK, N = 20, 10_000
    paths = np.empty((N, H + 1))
    paths[:, 0] = DAY1_CLOSE
    for n in range(N):
        fam = fam_a if rng.random() < 0.7 else fam_b
        rets = np.empty(H)
        t = 0
        while t < H:
            src = fam[rng.integers(len(fam))]
            j = rng.integers(0, max(1, len(src) - BLOCK))
            seg = src[j:j + BLOCK]
            take = min(len(seg), H - t)
            rets[t:t + take] = seg[:take]
            t += take
        paths[n, 1:] = DAY1_CLOSE * np.cumprod(1 + rets)

    pct = lambda q, d: float(np.percentile(paths[:, d], q))
    out = {
        "anchor": {"day1_close": DAY1_CLOSE, "ipo_price": IPO_PRICE, "open": OPEN_PRICE},
        "families": {"mega_ipo_chase_n": len(fam_a), "low_float_decay_n": len(fam_b), "blend": "70/30"},
        "p_below_ipo_price": {f"day_{d}": round(float((paths[:, d] < IPO_PRICE).mean()) * 100, 1)
                              for d in UNLOCK_DAYS + [252]},
        "p_below_open": {f"day_{d}": round(float((paths[:, d] < OPEN_PRICE).mean()) * 100, 1)
                         for d in UNLOCK_DAYS + [252]},
        "day_252_percentiles": {f"p{q}": round(pct(q, 252), 0) for q in (10, 25, 50, 75, 90)},
        "median_path_day_180": round(pct(50, 180), 0),
    }
    (HERE / "ch4_fanchart_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

    fig, ax = plt.subplots(figsize=(9, 5))
    days = np.arange(H + 1)
    for lo, hi, alpha in ((10, 90, 0.15), (25, 75, 0.3)):
        ax.fill_between(days, np.percentile(paths, lo, axis=0), np.percentile(paths, hi, axis=0),
                        color=GREY, alpha=alpha, linewidth=0)
    ax.plot(days, np.percentile(paths, 50, axis=0), color=INK, linewidth=1.6, label="Median bootstrap path")
    ax.axhline(IPO_PRICE, color=ACCENT, linestyle="--", linewidth=1.2)
    ax.text(3, IPO_PRICE - 7, "IPO $135", fontsize=8.5, color=ACCENT)
    ax.axhline(OPEN_PRICE, color=GREY, linestyle="--", linewidth=1)
    ax.text(3, OPEN_PRICE + 3, "open $150", fontsize=8.5, color=GREY)
    for d in UNLOCK_DAYS:
        ax.axvline(d, color=ACCENT, linestyle=":", linewidth=0.8, alpha=0.7)
    ax.text(UNLOCK_DAYS[0], ax.get_ylim()[0] * 1.02, "unlocks", fontsize=8, color=ACCENT)
    ax.set_xlabel("Trading days from day-1 close (unlock dates dotted)")
    ax.set_ylabel("SPCX price ($)")
    ax.set_title("SPCX 12-month bootstrap cone from the empirical post-listing families",
                 loc="left", fontsize=11.5)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig4_spcx_fanchart.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
