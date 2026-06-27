#!/usr/bin/env python3
"""Funding-lens figures: the choice-vs-necessity quadrant and the cash war-chest."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
D, FIG = ROOT / "data", ROOT / "figures"
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "font.family": "serif", "font.size": 10, "axes.edgecolor": INK,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.titlesize": 12, "axes.titleweight": "bold",
})


def load():
    rows = list(csv.DictReader(open(D / "funding_table.csv")))
    for r in rows:
        for k in ("capex_bn", "fcf_bn", "liquidity_bn", "runway_years",
                  "net_borrow_bn", "net_return_bn", "total_debt_bn"):
            try:
                r[k] = float(r[k])
            except (TypeError, ValueError):
                r[k] = None
    return rows


def fig_quadrant(rows):
    """x = free cash flow (internal funding surplus/deficit),
       y = net cash returned to shareholders, bubble = net new debt raised.
       Top-right = funds itself and still hands cash back (the core);
       bottom = negative FCF, borrowing, returning nothing (the dependent edge)."""
    fig, ax = plt.subplots(figsize=(9.0, 6.8))
    for r in rows:
        x, y = r["fcf_bn"], r["net_return_bn"]
        if x is None or y is None:
            continue
        nb = r["net_borrow_bn"] or 0
        size = 40 + abs(nb) * 12
        dependent = (x < 0)
        ax.scatter(x, y, s=size, color=ACCENT if dependent else INK,
                   alpha=0.55 if dependent else 0.40, edgecolor=INK, linewidth=0.6, zorder=3)
        if abs(x) > 5 or abs(y) > 5 or (r["capex_bn"] or 0) > 10:
            ax.annotate(r["ticker"], (x, y), fontsize=7.5, xytext=(4, 3),
                        textcoords="offset points", color=ACCENT if dependent else INK)
    ax.axhline(0, color=GREY, lw=1.0)
    ax.axvline(0, color=GREY, lw=1.0)
    ax.set_xlabel("Free cash flow after the build  =  operating cash flow − capex   ($bn)")
    ax.set_ylabel("Net cash returned to shareholders  ($bn)\n(buybacks − stock issued)")
    ax.set_title("Is the debt a choice or a necessity?")
    ax.text(0.98, 0.96, "self-funds the build AND\nhands cash back  (the core)",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, color=INK, style="italic")
    ax.text(0.02, 0.40, "negative free cash flow,\nborrowing, returning nothing\n(the dependent edge)",
            transform=ax.transAxes, ha="left", va="center", fontsize=8, color=ACCENT, style="italic")
    ax.text(0.98, 0.04, "bubble size = net new debt raised this year",
            transform=ax.transAxes, ha="right", fontsize=7.5, color=GREY, style="italic")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "funding_quadrant.png", dpi=150)
    plt.close(fig)


def fig_warchest(rows):
    """Years of capex sitting in cash + short-term investments (liquidity / capex)."""
    rs = [r for r in rows if r["runway_years"] is not None and (r["capex_bn"] or 0) >= 2]
    rs = sorted(rs, key=lambda r: r["runway_years"], reverse=True)
    fig, ax = plt.subplots(figsize=(8.2, 6.6))
    ys = range(len(rs))[::-1]
    for y, r in zip(ys, rs):
        thin = r["runway_years"] < 1.0
        ax.barh(y, r["runway_years"], color=ACCENT if thin else INK, height=0.66, zorder=3)
        ax.text(r["runway_years"] + 0.08, y, f"{r['runway_years']:.1f}", va="center",
                ha="left", fontsize=8.5, color=ACCENT if thin else INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r["ticker"] for r in rs], fontsize=9)
    ax.axvline(1.0, color=GREY, lw=1.0, ls="--", zorder=1)
    ax.text(1.03, len(rs) - 1.5, "1 year of\ncapex in cash", fontsize=7.5, color=GREY, va="top")
    ax.set_xlabel("War chest  =  cash + short-term investments ÷ annual capex   (years)")
    ax.set_title("Who could fund the build from cash on hand\nSpenders over $2bn, by years of capex held in liquidity")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.97, 0.04, "accent = under one year of capex in cash",
            transform=ax.transAxes, ha="right", fontsize=7.5, color=ACCENT, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "war_chest.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    rows = load()
    fig_quadrant(rows)
    fig_warchest(rows)
    print("wrote figures/funding_quadrant.png, figures/war_chest.png")
