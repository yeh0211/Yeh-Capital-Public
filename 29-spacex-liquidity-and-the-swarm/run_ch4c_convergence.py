#!/usr/bin/env python3
"""Study 29, Chapter 4c — the convergence figure.

Two independent methods, run blind to each other, on one timeline:
  - the bootstrap cone (Finding 4a): P(SPCX below $135) at each lock-up milestone
  - the swarm rehearsal (Finding 4c): the regime it flags at each milestone
Both put the break in the back half of the unlock calendar. This draws that agreement.
"""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})

# bootstrap cone milestones (from Finding 4a / results)
days = [0, 70, 135, 180, 252]
p_below_135 = [0, 35, 41, 43, 46]   # P(SPCX < $135 IPO price), %

# swarm regime by phase (Finding 4c)
swarm_phases = [
    (0, 70, "demand story governs\n(scarcity + index buying)", GREY),
    (70, 135, "fracture: borrow + insider\nsupply enter pricing", "#c77b58"),
    (135, 252, "supply calendar governs\nday-180 cleanup = peak stress", ACCENT),
]

fig, ax = plt.subplots(figsize=(10, 5.2))

# swarm phase bands (background)
for lo, hi, label, col in swarm_phases:
    ax.axvspan(lo, hi, color=col, alpha=0.13, linewidth=0)
    ax.text((lo + hi) / 2, 8, label, ha="center", va="bottom", fontsize=8.5,
            color=INK, style="italic")

# cone line
ax.plot(days, p_below_135, "-o", color=ACCENT, linewidth=2.0, markersize=6,
        label="Bootstrap cone: P(SPCX below $135 IPO price)")
for d, p in zip(days, p_below_135):
    if d > 0:
        ax.text(d, p + 1.6, f"{p}%", ha="center", fontsize=8.5, color=ACCENT)

# lock-up markers
for d, lab in [(70, "day 70\n1st unlock"), (135, "day 135\nlast tranche"),
               (180, "day 180\ncleanup (Dec)")]:
    ax.axvline(d, color=INK, linestyle=":", linewidth=0.9, alpha=0.6)
    ax.text(d, 52, lab, ha="center", fontsize=7.5, color=INK)

ax.set_xlim(0, 255)
ax.set_ylim(0, 56)
ax.set_xlabel("Trading days from listing")
ax.set_ylabel("P(SPCX below $135 IPO price), %")
ax.set_title("Two methods, run blind, agree: the break is in the back half of the unlock calendar",
             loc="left", fontsize=12)
ax.legend(frameon=False, fontsize=9, loc="lower right")
fig.text(0.012, 0.01,
         "Background bands = the swarm's emergent regimes (Finding 4c). Line = the statistical "
         "bootstrap cone (Finding 4a). Independent methods; same back-half break.",
         fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(HERE / "fig5_swarm_cone_convergence.png", dpi=160)
print("wrote fig5_swarm_cone_convergence.png")
