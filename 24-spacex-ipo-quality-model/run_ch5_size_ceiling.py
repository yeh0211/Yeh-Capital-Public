#!/usr/bin/env python3
"""Study 29, Chapter 5 — the "next FAANG" arithmetic ceiling.

The claim "SpaceX is the next FAANG" compares SpaceX's TODAY price to FAANG's IPO
price. But FAANG's returns came from IPO'ing small. This chapter quantifies the
category error: from a $2T entry, the multiple is bounded by how large a company can
plausibly become, and FAANG-style multiples would require SpaceX to exceed the largest
company in history many times over, or all world equity.

Output: ch5_results.json + fig6 (two panels: entry caps + required terminal cap).
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

# reality benchmarks ($B), sourced (see README)
LARGEST_EVER = 5500.0        # NVDA, first to $5.5T (2026)
US_EQUITY = 75000.0          # US total equity, crossed $75T in 2026 (Wikipedia/VisualCap)
WORLD_EQUITY = 126700.0      # SIFMA global equity mkt cap, 2024
WORLD_GDP = 110000.0         # IMF approx 2025-26
SPCX_ENTRY = 1770.0          # $1.77T IPO market value


def main() -> None:
    df = pd.read_csv(DATA / "faang_ipo_caps.csv")
    faang = df[df.ticker != "SPCX"].copy()

    # required terminal cap for SPCX to match each name's price-return multiple
    faang["spcx_terminal_to_match_usd_b"] = SPCX_ENTRY * faang["price_return_multiple"]
    faang["x_largest_ever"] = faang["spcx_terminal_to_match_usd_b"] / LARGEST_EVER
    faang["x_world_equity"] = faang["spcx_terminal_to_match_usd_b"] / WORLD_EQUITY

    res = {
        "spcx_entry_usd_b": SPCX_ENTRY,
        "spcx_entry_vs_faang_ipo": {
            "vs_smallest_ipo_NFLX_x": round(SPCX_ENTRY / float(faang.loc[faang.ticker == "NFLX", "ipo_mktcap_usd_b"].iloc[0]), 0),
            "vs_largest_ipo_META_x": round(SPCX_ENTRY / float(faang.loc[faang.ticker == "META", "ipo_mktcap_usd_b"].iloc[0]), 1),
            "median_faang_ipo_cap_usd_b": round(float(faang.ipo_mktcap_usd_b.median()), 2),
        },
        "benchmarks_usd_b": {"largest_company_ever": LARGEST_EVER, "us_equity": US_EQUITY,
                             "world_equity": WORLD_EQUITY, "world_gdp": WORLD_GDP},
        "to_match_each_faang": {},
        "realistic_ladder": {
            "3x_great_outcome_usd_b": SPCX_ENTRY * 3,
            "3x_vs_largest_ever": round(SPCX_ENTRY * 3 / LARGEST_EVER, 2),
            "10x_usd_b": SPCX_ENTRY * 10,
            "10x_vs_largest_ever": round(SPCX_ENTRY * 10 / LARGEST_EVER, 2),
            "10x_vs_us_equity_pct": round(SPCX_ENTRY * 10 / US_EQUITY * 100, 1),
        },
    }
    for r in faang.itertuples():
        res["to_match_each_faang"][r.ticker] = {
            "multiple": int(r.price_return_multiple),
            "spcx_terminal_usd_t": round(r.spcx_terminal_to_match_usd_b / 1000, 1),
            "x_largest_ever": round(r.x_largest_ever, 1),
            "x_world_equity": round(r.x_world_equity, 2),
        }
    (HERE / "ch5_results.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))

    # ---- figure ----
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4))

    # Panel 1 — entry market caps (log), SPCX vs FAANG IPOs
    ax = axes[0]
    d1 = df.sort_values("ipo_mktcap_usd_b")
    colors = [ACCENT if t == "SPCX" else GREY for t in d1.ticker]
    ax.barh(d1.company + "  (" + d1.ipo_date.str[:4] + ")", d1.ipo_mktcap_usd_b,
            color=colors, height=0.62)
    ax.set_xscale("log")
    ax.set_xlabel("Market cap at IPO ($B, log scale)")
    for y, (v, t) in enumerate(zip(d1.ipo_mktcap_usd_b, d1.ticker)):
        lab = f"${v:,.0f}B" if v >= 10 else f"${v*1000:,.0f}M"
        ax.text(v * 1.3, y, lab, va="center", fontsize=8,
                color=ACCENT if t == "SPCX" else INK,
                fontweight="bold" if t == "SPCX" else "normal")
    ax.set_title("Where each one STARTED", loc="left", fontsize=11.5)

    # Panel 2 — required terminal cap for SPCX to match each multiple, vs ceilings
    ax = axes[1]
    order = faang.sort_values("price_return_multiple")
    term = order.spcx_terminal_to_match_usd_b.values
    labels = [f"match {c} ({int(m):,}x)" for c, m in zip(order.company, order.price_return_multiple)]
    ax.barh(labels, term, color=ACCENT, height=0.6, alpha=0.85)
    ax.set_xscale("log")
    for x, v in [(LARGEST_EVER, "largest co. ever ($5.5T)"),
                 (WORLD_EQUITY, "all world equity ($127T)")]:
        ax.axvline(x, color=INK, linestyle="--", linewidth=1.1)
        ax.text(x, len(labels) - 0.4, v, rotation=90, fontsize=7.5, va="top", ha="right", color=INK)
    ax.set_xlabel("Terminal cap SpaceX would need, from $1.77T ($B, log)")
    ax.set_title("What matching them REQUIRES from $2T", loc="left", fontsize=11.5)

    fig.suptitle('"The next FAANG" compares SpaceX\'s exit price to FAANG\'s entry price',
                 x=0.012, ha="left", fontsize=13, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(HERE / "fig6_size_ceiling.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
