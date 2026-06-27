#!/usr/bin/env python3
"""House-style figures for the AI capex-by-company study (monochrome + one accent)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parent.parent
D, FIG = ROOT / "data", ROOT / "figures"
FIG.mkdir(exist_ok=True)

CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "font.family": "serif", "font.size": 10, "axes.edgecolor": INK,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.titlesize": 12, "axes.titleweight": "bold",
})


def load():
    with open(D / "capex_table.csv") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("capex_bn", "revenue_bn", "ocf_bn", "intensity_pct",
                  "self_funding_pct", "fcf_bn", "yoy_pct"):
            r[k] = float(r[k]) if r[k] not in ("", None) else None
    return rows


def fig_bars(rows):
    top = rows[:18]
    fig, ax = plt.subplots(figsize=(8.2, 7.0))
    ys = range(len(top))[::-1]
    for y, r in zip(ys, top):
        burning = r["fcf_bn"] is not None and r["fcf_bn"] < 0
        ax.barh(y, r["capex_bn"], color=ACCENT if burning else INK,
                height=0.66, zorder=3)
        ax.text(r["capex_bn"] + 1.5, y, f"{r['capex_bn']:,.0f}",
                va="center", ha="left", fontsize=8.5,
                color=ACCENT if burning else INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{r['ticker']}" for r in top], fontsize=9)
    ax.set_xlabel("Latest fiscal-year capex  ($bn, gross purchases of PP&E)")
    ax.set_title("AI-market capex is five companies\nTop-18 US filers by capex")
    ax.set_xlim(0, 150)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.97, 0.04,
            "accent = negative free cash flow (burning to build)",
            transform=ax.transAxes, ha="right", fontsize=7.5, color=ACCENT,
            style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "capex_by_company.png", dpi=150)
    plt.close(fig)


def fig_scatter(rows):
    """Capex intensity (x) vs self-funding (y). The fragile zone is high-intensity,
    >100% self-funding, negative FCF — the financing-refusal blast radius."""
    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    CAP_Y = 380.0  # cap for plotting; names above (incl. neg-OCF) pinned here
    # stagger pinned (negative-OCF / over-cap) names so labels don't collide
    pinned = sorted([r for r in rows if r["intensity_pct"] is not None and (
        r["self_funding_pct"] is None or r["self_funding_pct"] > CAP_Y or
        (r["ocf_bn"] is not None and r["ocf_bn"] < 0))],
        key=lambda r: r["intensity_pct"])
    pin_y = {r["ticker"]: CAP_Y - 14 * i for i, r in enumerate(pinned)}
    for r in rows:
        x = r["intensity_pct"]
        if x is None:
            continue
        sf = r["self_funding_pct"]
        neg_ocf = (r["ocf_bn"] is not None and r["ocf_bn"] < 0)
        y = pin_y.get(r["ticker"], sf) if r["ticker"] in pin_y else sf
        burning = r["fcf_bn"] is not None and r["fcf_bn"] < 0
        size = 40 + (r["capex_bn"] or 0) * 7
        ax.scatter(x, y, s=size, color=ACCENT if burning else INK,
                   alpha=0.55 if burning else 0.4, edgecolor=INK,
                   linewidth=0.6, zorder=3, marker="^" if (neg_ocf or sf is None) else "o")
        # label the notable names
        if (r["capex_bn"] and r["capex_bn"] > 5) or x > 150 or (sf and sf > 120):
            ax.annotate(r["ticker"], (x, y), fontsize=7.5,
                        xytext=(4, 4), textcoords="offset points",
                        color=ACCENT if burning else INK)
    ax.axhline(100, color=GREY, lw=1.0, ls="--", zorder=1)
    ax.axvline(100, color=GREY, lw=1.0, ls=":", zorder=1)
    ax.text(101, 102, "self-funding = 100%\n(build outruns operating cash)",
            fontsize=7, color=GREY, va="bottom")
    ax.set_xscale("log")
    ax.set_xlabel("Capex intensity  =  capex / revenue   (%, log scale)")
    ax.set_ylabel("Self-funding  =  capex / operating cash flow   (%)")
    ax.set_title("The fragility is the funding, not the magnitude")
    ax.set_ylim(0, CAP_Y + 25)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.text(0.985, 0.035,
            "triangles pinned at top = capex exceeds operating cash flow many-fold\n"
            "or operating cash flow is negative   ·   accent = negative free cash flow",
            transform=ax.transAxes, ha="right", fontsize=7, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "intensity_vs_selffunding.png", dpi=150)
    plt.close(fig)


def fig_fcf(rows):
    """Free cash flow by company: who collects the AI build (prints cash while
    barely spending) vs who pays for it (burns cash to build)."""
    rs = [r for r in rows if r["fcf_bn"] is not None]
    rs = sorted(rs, key=lambda r: r["fcf_bn"], reverse=True)
    top = rs[:8]
    bot = rs[-8:]
    show = top + bot
    fig, ax = plt.subplots(figsize=(8.2, 7.2))
    ys = range(len(show))[::-1]
    for y, r in zip(ys, show):
        neg = r["fcf_bn"] < 0
        ax.barh(y, r["fcf_bn"], color=ACCENT if neg else INK, height=0.66, zorder=3)
        off = -2.5 if neg else 2.5
        ha = "right" if neg else "left"
        ax.text(r["fcf_bn"] + off, y, f"{r['fcf_bn']:+,.0f}", va="center",
                ha=ha, fontsize=8.5, color=ACCENT if neg else INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r["ticker"] for r in show], fontsize=9)
    ax.axvline(0, color=INK, lw=1.0)
    ax.set_xlabel("Free cash flow  =  operating cash flow − capex   ($bn)")
    ax.set_title("Who collects the build, and who pays for it\n"
                 "Top-8 and bottom-8 by free cash flow")
    ax.set_xlim(-40, 120)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fcf_by_company.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    rows = load()
    fig_bars(rows)
    fig_scatter(rows)
    fig_fcf(rows)
    print("wrote 3 figures to figures/")
