"""Build figures for study 00 (Tempus AI). House palette, monochrome, zero chartjunk.
Run: python build_figures.py  (reads data/tem_prices.csv, writes figures/)."""
import csv
from datetime import datetime
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CREAM, INK, ACCENT, GRAY = "#faf8f3", "#1c1a17", "#9c3d2e", "#7a8a78"
HERE = Path(__file__).parent

dates, close = [], []
with open(HERE / "data" / "tem_prices.csv") as f:
    for r in csv.DictReader(f):
        dates.append(datetime.fromisoformat(r["date"]))
        close.append(float(r["close"]))

fig, ax = plt.subplots(figsize=(9, 4.6))
fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
ax.plot(dates, close, color=INK, lw=1.1)

# anchor markers: IPO close, all-time high, last
hi_i = max(range(len(close)), key=lambda i: close[i])
for i, label, dy in [(0, f"IPO close ${close[0]:.0f}", 8),
                     (hi_i, f"peak ${close[hi_i]:.0f}", 8),
                     (len(close) - 1, f"latest ${close[-1]:.0f}", 8)]:
    ax.scatter([dates[i]], [close[i]], color=ACCENT, s=18, zorder=3)
    ax.annotate(label, (dates[i], close[i]), textcoords="offset points",
                xytext=(0, dy), ha="center", fontsize=9, color=INK)

ax.set_title("Tempus AI (TEM): a violent round trip since the 2024 IPO", color=INK, fontsize=12, loc="left")
ax.set_ylabel("share price ($)", color=INK, fontsize=9)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(GRAY)
ax.tick_params(colors=INK, labelsize=8)
ax.margins(x=0.02)
fig.tight_layout()
fig.savefig(HERE / "figures" / "tem_tape.png", dpi=140, facecolor=CREAM)
print("wrote figures/tem_tape.png")
