"""House-style chart helpers: cream background, near-black ink, single accent,
monochrome series. No emojis, no decoration. Typography does the work."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import OUTPUT_DIR

FIG_DIR = OUTPUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

CREAM = "#faf8f2"
INK = "#1c1b18"
GRAY = "#b9b3a4"
GRID = "#e4dfd2"
ACCENT = "#8c1c13"

plt.rcParams.update({
    "figure.facecolor": CREAM,
    "axes.facecolor": CREAM,
    "savefig.facecolor": CREAM,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "serif",
    "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "figure.dpi": 150,
})


def fan_panel(ax, stacked: pd.DataFrame, title: str, ylabel: str = "",
              highlight: str | None = None, unit_line: bool = True):
    """Thin gray per-event lines + bold median; optional accent highlight series."""
    if stacked is None or stacked.empty:
        ax.set_title(title)
        ax.text(0.5, 0.5, "no data", transform=ax.transAxes, ha="center", color=GRAY)
        return
    for col in stacked.columns:
        if highlight is not None and col == highlight:
            continue
        ax.plot(stacked.index, stacked[col], color=GRAY, lw=0.7, alpha=0.8)
    med = stacked.median(axis=1)
    ax.plot(med.index, med, color=INK, lw=1.8, label="median")
    if highlight is not None and highlight in stacked.columns:
        ax.plot(stacked.index, stacked[highlight], color=ACCENT, lw=1.6, label=str(highlight))
        ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.axvline(0, color=ACCENT, lw=0.9, alpha=0.9)
    if unit_line:
        ax.axhline(0, color=INK, lw=0.6, alpha=0.5)
    ax.set_title(title, loc="left")
    ax.set_ylabel(ylabel)


def single_panel(ax, series_map: dict[str, pd.Series], title: str, ylabel: str = "",
                 accent_key: str | None = None, zero_line: bool = True):
    """A few named series, monochrome except one accent."""
    grays = ["#1c1b18", "#6e6857", "#a39c89", "#c9c2b0"]
    gi = 0
    plotted = False
    for name, s in series_map.items():
        if s is None or (hasattr(s, "empty") and s.empty):
            continue
        if accent_key is not None and name == accent_key:
            ax.plot(s.index, s.values, color=ACCENT, lw=1.6, label=name)
        else:
            ax.plot(s.index, s.values, color=grays[min(gi, 3)], lw=1.2, label=name)
            gi += 1
        plotted = True
    if not plotted:
        ax.text(0.5, 0.5, "no data", transform=ax.transAxes, ha="center", color=GRAY)
    else:
        ax.legend(frameon=False, fontsize=7.5, loc="upper left", ncol=2)
    ax.axvline(0, color=ACCENT, lw=0.9, alpha=0.9)
    if zero_line:
        ax.axhline(0, color=INK, lw=0.6, alpha=0.5)
    ax.set_title(title, loc="left")
    ax.set_ylabel(ylabel)


def event_figure(fname: str, panels: list, suptitle: str, ncols: int = 2) -> Path:
    """panels: list of callables(ax). Returns saved path."""
    n = len(panels)
    nrows = (n + ncols - 1) // ncols
    import numpy as np
    fig, axes = plt.subplots(nrows, ncols, figsize=(5.4 * ncols, 3.1 * nrows))
    axes = list(np.atleast_1d(axes).flat)
    for ax, draw in zip(axes, panels):
        draw(ax)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle(suptitle, x=0.01, ha="left", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = FIG_DIR / f"{fname}.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out
