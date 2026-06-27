#!/usr/bin/env python3
"""YoY capex ramp line chart for the big spenders (house style, direct-labelled)."""
import csv
from collections import defaultdict
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

START = 2019
# (ticker, label, color, linestyle, linewidth, label_dy)  — direct-labelled, no legend
SERIES = [
    ("AMZN", "Amazon", INK, "-", 2.2, 0),
    ("GOOGL", "Alphabet", INK, "-", 1.6, 0),
    ("META", "Meta", INK, "-", 1.6, 1.5),
    ("MSFT", "Microsoft", INK, "-", 1.6, -1.5),
    ("ORCL", "Oracle", ACCENT, "-", 2.2, 0),
    ("NVDA", "Nvidia", GREY, "--", 1.6, 0),
]


def main():
    hist = defaultdict(dict)
    for r in csv.DictReader(open(D / "capex_raw.csv")):
        if r["capex"] and r["fy"]:
            hist[r["ticker"]][int(r["fy"])] = float(r["capex"]) / 1e9

    fig, ax = plt.subplots(figsize=(8.8, 6.4))
    for tkr, lab, color, ls, lw, dy in SERIES:
        d = hist.get(tkr, {})
        yrs = sorted(y for y in d if y >= START)
        if not yrs:
            continue
        vals = [d[y] for y in yrs]
        ax.plot(yrs, vals, ls, color=color, lw=lw, marker="o", ms=3.5, zorder=3)
        ax.text(yrs[-1] + 0.08, vals[-1] + dy, f"  {lab} {vals[-1]:.0f}",
                va="center", ha="left", fontsize=9,
                color=color, fontweight="bold" if color == ACCENT else "normal")

    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Capex  ($bn)")
    ax.set_title("The capex hockey stick: flat for years, then a wall of money\n"
                 "Annual capex of the five hyperscalers (Nvidia shown for contrast)")
    ax.set_xlim(START, 2027.6)
    ax.set_ylim(0, 145)
    ax.set_xticks(range(START, 2027))
    # mark where the ramp begins
    ax.axvspan(2023, 2027.6, color=GREY, alpha=0.06, zorder=0)
    ax.text(2025, 8, "the AI build", fontsize=8.5, color=GREY, style="italic", ha="center")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.02, 0.97, "Nvidia (dashed) barely spends — it sells into the build,\nit doesn't pay for it",
            transform=ax.transAxes, va="top", fontsize=8, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "capex_ramp.png", dpi=150)
    plt.close(fig)
    print("wrote figures/capex_ramp.png")


if __name__ == "__main__":
    main()
