#!/usr/bin/env python3
"""Two angles: (1) where the AI-server dollar goes (BOM cascade — top-heavy, not
pyramid-shaped); (2) spenders vs collectors — hyperscaler FCF vs chipmaker FCF
crossing as the capex flows out to the chip sellers."""
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


def fig_bom():
    rows = list(csv.DictReader(open(D / "bom_cascade.csv")))
    rows.sort(key=lambda r: float(r["share_pct"]), reverse=True)
    fig, ax = plt.subplots(figsize=(9.4, 7.0))
    ys = range(len(rows))[::-1]
    for y, r in zip(ys, rows):
        share = float(r["share_pct"])
        inpyr = "pyramid" not in r["gs_layer"] and "apex" not in r["gs_layer"] and r["gs_layer"].startswith("L")
        col = ACCENT if inpyr else INK
        ax.barh(y, share, color=col, height=0.66, zorder=3)
        star = " *" if r["bottleneck"] == "yes" else ""
        ax.text(share + 0.6, y, f"{share:g}%{star}", va="center", ha="left", fontsize=8,
                color=col)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{r['component']}" for r in rows], fontsize=8.3)
    ax.set_xlabel("Share of the AI-server bill of materials  (%, 2026 / VR200-era analyst estimate)")
    ax.set_title("Where the AI capex dollar goes: top-heavy, not pyramid-shaped\n"
                 "GPU + memory + packaging ≈ 85% of the server BOM")
    ax.set_xlim(0, 60)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.97, 0.06, "accent = a Goldman 'AI pyramid' layer   ·   * = supply bottleneck despite the small slice",
            transform=ax.transAxes, ha="right", fontsize=7.5, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "bom_cascade.png", dpi=150)
    plt.close(fig)


def fig_inversion():
    rows = list(csv.DictReader(open(D / "spenders_collectors.csv")))
    yr = [int(r["year"]) for r in rows]
    hyp = [float(r["hyperscaler_fcf_bn"]) for r in rows]
    chip = [float(r["chipmaker_fcf_bn"]) for r in rows]
    na = sum(1 for r in rows if r["kind"] == "actual")  # actual count
    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    # actual solid, estimate dashed last segment
    ax.plot(yr[:na], hyp[:na], "-", color=INK, lw=2.2, marker="o", ms=4, zorder=3)
    ax.plot(yr[na - 1:], hyp[na - 1:], "--", color=INK, lw=2.0, marker="o", ms=4, zorder=3)
    ax.plot(yr[:na], chip[:na], "-", color=ACCENT, lw=2.2, marker="s", ms=4, zorder=3)
    ax.plot(yr[na - 1:], chip[na - 1:], "--", color=ACCENT, lw=2.0, marker="s", ms=4, zorder=3)
    ax.text(yr[-1] + 0.05, hyp[-1], "  hyperscaler FCF\n  (the spenders)", va="center",
            ha="left", fontsize=8.5, color=INK)
    ax.text(yr[-1] + 0.05, chip[-1], "  chipmaker FCF\n  (the collectors)", va="center",
            ha="left", fontsize=8.5, color=ACCENT, fontweight="bold")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Aggregate free cash flow  ($bn)")
    ax.set_title("Spenders vs collectors: the chipmakers' cash flow overtakes the clouds'\n"
                 "Aggregate FCF — 5 US hyperscalers vs 4 big chipmakers")
    ax.set_xlim(2019, 2027.6)
    ax.set_ylim(-30, 290)
    ax.set_xticks(range(2019, 2027))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.02, 0.96, "2019–2025 actual (SEC filings); 2026 estimate (consensus / Bloomberg-GLJ).\n"
            "The capex the clouds spend IS the chipmakers' cash flow — and in 2026 it crosses over.",
            transform=ax.transAxes, va="top", fontsize=8, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "spenders_vs_collectors.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_bom()
    fig_inversion()
    print("wrote figures/bom_cascade.png, figures/spenders_vs_collectors.png")
