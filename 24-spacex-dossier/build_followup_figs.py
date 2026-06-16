#!/usr/bin/env python3
"""Day-two follow-up figures: the two clocks, and the semis extension."""
from __future__ import annotations
import csv, json, datetime as dt
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
    "axes.grid": True, "grid.color": "#e4ded2", "grid.linewidth": 0.6,
})

# ---- Figure A: the two clocks ----
trump = list(csv.DictReader(open(HERE / "data/TRUMPUSDT.csv")))
peak_d = dt.date(2025, 1, 19); peak_hi = 77.24
pts = []
for r in trump:
    d = dt.date.fromisoformat(r["date"])
    if d >= peak_d:
        pts.append(((d - peak_d).days, (float(r["close"]) / peak_hi - 1) * 100))
pts = [p for p in pts if p[0] <= 185]

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ACCENT, linewidth=2.0,
        label="TRUMP coin decay from peak (the memecoin clock)")
ax.axhline(0, color=INK, linewidth=0.8)
# SPCX unlock calendar markers (days from listing; the SPCX clock)
unlocks = [(70, "day 70\n1st unlock"), (90, "90"), (105, "105"), (120, "120"),
           (135, "day 135\nlast tranche"), (180, "day 180\ncleanup (Dec)")]
for d, lab in unlocks:
    ax.axvline(d, color=GREY, linestyle="--", linewidth=1.1)
    ax.text(d, 6, lab, fontsize=7.5, color="#5a5145", ha="center", va="bottom")
ax.axvspan(70, 180, color=GREY, alpha=0.10, linewidth=0)
ax.text(125, -45, "SPCX's risk window:\nthe unlock calendar\n(Sept-Dec 2026)", ha="center",
        fontsize=9, color="#5a5145", style="italic")
ax.text(7, -55, "TRUMP: -65% within a\nweek of the peak", fontsize=8.5, color=ACCENT)
ax.set_xlabel("Days from the peak / from listing")
ax.set_ylabel("TRUMP: % from peak")
ax.set_xlim(-3, 185); ax.set_ylim(-100, 12)
ax.set_title("Two clocks: the TRUMP coin collapsed in days; SPCX's risk is months out",
             loc="left", fontsize=12)
ax.legend(frameon=False, fontsize=9, loc="lower right")
fig.tight_layout()
fig.savefig(HERE / "figd2_two_clocks.png", dpi=160)
plt.close(fig)
print("wrote figd2_two_clocks.png")

# ---- Figure B: the semis extension ----
soxx = json.load(open(HERE / "data/soxx_2026.json"))["results"]
closes = [(dt.datetime.utcfromtimestamp(b["t"] / 1000).date(), b["c"]) for b in soxx]
c = [x[1] for x in closes]; days = [x[0] for x in closes]
def ema(v, n):
    k = 2 / (n + 1); e = v[0]; out = [e]
    for x in v[1:]:
        e = x * k + e * (1 - k); out.append(e)
    return out
e21 = ema(c, 21)
fig, ax = plt.subplots(figsize=(9.5, 5.0))
ax.plot(days, c, color=INK, linewidth=1.7, label="SOXX (semiconductor ETF)")
ax.plot(days, e21, color=ACCENT, linewidth=1.4, linestyle="--", label="21-day EMA (trend filter)")
ax.fill_between(days, c, e21, where=[ci > ei for ci, ei in zip(c, e21)],
                color=ACCENT, alpha=0.10, linewidth=0)
last, lastema = c[-1], e21[-1]; lo = min(c)
ax.annotate(f"+{(last/lastema-1)*100:.0f}% above 21-EMA\n+{(last/lo-1)*100:.0f}% off the Mar-30 low\n(doubled in ~10 weeks)",
            xy=(days[-1], last), xytext=(days[len(days)//3], last * 0.92),
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
ax.set_ylabel("SOXX close ($)")
ax.set_title("The sector you'd hedge is going vertical: SOXX +12% above its 21-EMA, at new highs",
             loc="left", fontsize=11.5)
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout()
fig.savefig(HERE / "figd2_semis_extension.png", dpi=160)
plt.close(fig)
print("wrote figd2_semis_extension.png")
