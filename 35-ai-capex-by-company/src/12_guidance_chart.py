#!/usr/bin/env python3
"""
Grouped bar chart: most-recent actual capex vs the latest announced 2026 guidance,
for the major AI spenders. Shows that the capex announced THIS year keeps rising.
Reads data/capex_2026_guidance.csv (ticker, company, actual_usd_bn, guidance_usd_bn,
guidance_low, guidance_high, basis).
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D, FIG = ROOT / "data", ROOT / "figures"
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "font.family": "serif", "font.size": 10, "axes.edgecolor": INK,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.titlesize": 12, "axes.titleweight": "bold",
})


def main():
    rows = list(csv.DictReader(open(D / "capex_2026_guidance.csv")))
    for r in rows:
        for k in ("actual_usd_bn", "guidance_usd_bn", "guidance_low", "guidance_high"):
            r[k] = float(r[k]) if r.get(k) not in ("", None) else None
    rows.sort(key=lambda r: r["guidance_usd_bn"] or 0, reverse=True)

    n = len(rows)
    fig, ax = plt.subplots(figsize=(9.4, 6.6))
    y = np.arange(n)[::-1]
    h = 0.38
    for yi, r in zip(y, rows):
        ax.barh(yi + h / 2, r["actual_usd_bn"], height=h, color=GREY, zorder=3)
        ax.barh(yi - h / 2, r["guidance_usd_bn"], height=h, color=ACCENT, zorder=3)
        ax.text(r["actual_usd_bn"] + 2, yi + h / 2, f"{r['actual_usd_bn']:.0f}",
                va="center", ha="left", fontsize=8, color=INK)
        # show range if present
        if r["guidance_low"] and r["guidance_high"] and r["guidance_high"] > 0:
            lbl = f"{r['guidance_usd_bn']:.0f}  ({r['guidance_low']:.0f}–{r['guidance_high']:.0f})"
        else:
            lbl = f"{r['guidance_usd_bn']:.0f}"
        ax.text(r["guidance_usd_bn"] + 2, yi - h / 2, lbl, va="center", ha="left",
                fontsize=8, color=ACCENT, fontweight="bold")
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{r['company']} ({r['ticker']})" for r in rows], fontsize=9)
    ax.set_xlabel("Capex  ($bn)")
    ax.set_title("The build keeps accelerating: 2026 guidance announced this year\n"
                 "vs the most recent full-year actual")
    ax.set_xlim(0, max(r["guidance_usd_bn"] for r in rows) * 1.22)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=GREY, label="latest full-year actual"),
                       Patch(color=ACCENT, label="2026 guidance (announced this year)")],
              loc="lower right", frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(FIG / "capex_2026_guidance.png", dpi=150)
    plt.close(fig)
    print("wrote figures/capex_2026_guidance.png")


if __name__ == "__main__":
    main()
