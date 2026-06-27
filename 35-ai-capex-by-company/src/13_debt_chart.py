#!/usr/bin/env python3
"""Debt-structure chart: floating-rate share (x) vs the coupon paid (y), bubble =
total debt, colour = credit grade. Good credit clusters cheap + fixed (insulated);
weak credit sits dear + floating (exposed if the situation worsens)."""
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


def grade_color(grade):
    g = grade.lower()
    if "junk" in g or "unrated" in g:
        return ACCENT
    if "neg" in g or "split" in g or grade.strip() == "IG (neg)":
        return GREY
    return INK


def main():
    rows = list(csv.DictReader(open(D / "debt_schedule.csv")))
    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    for r in rows:
        x = float(r["pct_floating"])
        y = float(r["wavg_coupon_pct"])
        if y < 0:
            continue
        debt = float(r["total_debt_bn"])
        col = grade_color(r["grade"])
        ax.scatter(x, y, s=40 + debt * 4, color=col, alpha=0.55 if col == ACCENT else 0.40,
                   edgecolor=INK, linewidth=0.6, zorder=3)
        # label the notable / exposed names and the biggest; fan out the crowded
        # bottom-left AA cluster so labels don't collide
        OFF = {"AMZN": (4, 6), "GOOGL": (4, -8), "META": (-34, 2), "MSFT": (-30, -8),
               "NVDA": (-32, 8), "ORCL": (6, 4), "DUK": (6, 5), "SO": (6, -6)}
        if col != INK or debt > 60 or x > 20:
            lbl = {"private": "ByteDance", "0981.HK": "SMIC", "0700.HK": "Tencent",
                   "2317.TW": "Foxconn", "005930.KS": "Samsung"}.get(r["ticker"], r["ticker"])
            ax.annotate(lbl, (x, y), fontsize=7.5, xytext=OFF.get(r["ticker"], (4, 3)),
                        textcoords="offset points", color=col if col != GREY else INK)
    ax.axhline(6, color=GREY, lw=0.8, ls=":", zorder=1)
    ax.axvline(25, color=GREY, lw=0.8, ls=":", zorder=1)
    ax.set_xlabel("Floating-rate share of debt  (%)  — reprices immediately if rates rise")
    ax.set_ylabel("Weighted-average coupon  (%)  — the rate they borrow at")
    ax.set_title("Good credit borrows cheap and locks it in; weak credit pays more and floats")
    ax.set_xlim(-4, 100)
    ax.set_ylim(0, 10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.015, 0.05, "cheap + fixed\n= insulated", transform=ax.transAxes, fontsize=8,
            color=INK, style="italic", va="bottom")
    ax.text(0.985, 0.96, "dear + floating\n= exposed if it worsens", transform=ax.transAxes,
            fontsize=8, color=ACCENT, style="italic", ha="right", va="top")
    ax.text(0.985, 0.05, "bubble = total debt   ·   ink = AA/A   grey = BBB/pressured   accent = junk/unrated",
            transform=ax.transAxes, fontsize=7, color=GREY, ha="right", style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "debt_rate_exposure.png", dpi=150)
    plt.close(fig)
    print("wrote figures/debt_rate_exposure.png")


if __name__ == "__main__":
    main()
