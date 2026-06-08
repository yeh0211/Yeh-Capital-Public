"""Build public figures for study 23 from published CSVs only.

Run from this directory or from the repository root:

    python3 23-robotics-fund-mstr-premium-replay/build_figures.py

No private database, API key, or YehCapital pipeline import is required.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, NullFormatter, PercentFormatter


STUDY_DIR = Path(__file__).resolve().parent
DATA_DIR = STUDY_DIR / "data"

FIGSIZE = (9.5, 5.6)
DPI = 180
INK = "#17202A"
GRID = "#D6DBDF"
MUTED = "#6C7A89"
BLUE = "#1F77B4"
GREEN = "#2CA02C"
RED = "#D62728"
ORANGE = "#FF7F0E"
PURPLE = "#9467BD"


def percent_axis(x, _pos):
    return f"{x:.0%}"


def money_axis(x, _pos):
    if x >= 1000:
        return f"${x:,.0f}"
    return f"${x:.0f}"


def clean_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#AAB7B8")
    ax.spines["bottom"].set_color("#AAB7B8")
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.8)
    ax.tick_params(colors=INK)
    ax.title.set_color(INK)


def save(fig, filename: str):
    fig.tight_layout()
    fig.savefig(STUDY_DIR / filename, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig1_mstr_decomposition():
    df = pd.read_csv(DATA_DIR / "mstr_monthly_mnav_decomposition.csv", parse_dates=["date"])

    fig, ax = plt.subplots(figsize=FIGSIZE)
    series = [
        ("MSTR price", "mstr_price_return", INK, 2.8),
        ("BTC price", "btc_price_return", ORANGE, 2.2),
        ("BTC / diluted share", "btc_per_share_return", GREEN, 2.2),
        ("Simplified mNAV", "mnav_return", RED, 2.2),
    ]
    for label, col, color, lw in series:
        ax.plot(df["date"], df[col], label=label, color=color, linewidth=lw)
        ax.scatter(df["date"].iloc[-1], df[col].iloc[-1], color=color, s=22, zorder=3)

    ax.axhline(0, color="#7F8C8D", linewidth=1)
    ax.set_title("MSTR price was the product of BTC, BTC/share, and mNAV compression")
    ax.set_ylabel("Return since Jan. 2025")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.legend(frameon=False, ncol=2, loc="lower left")
    clean_ax(ax)
    save(fig, "fig1_mstr_decomposition.png")


def fig2_bot_premium_path():
    df = pd.read_csv(DATA_DIR / "bot_massive_price_nav.csv", parse_dates=["date"])

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(df["date"], df["price_nav_multiple"], color=BLUE, linewidth=2.8, marker="o", markersize=4)
    for y, label in [(1, "NAV"), (2, "2x NAV"), (5, "5x NAV")]:
        ax.axhline(y, color="#AAB7B8", linewidth=1, linestyle="--")
        ax.text(df["date"].min(), y + 0.05, label, color=MUTED, fontsize=9, va="bottom")

    latest = df.iloc[-1]
    ax.scatter(latest["date"], latest["price_nav_multiple"], color=RED, s=42, zorder=4)
    ax.annotate(
        f"{latest['price_nav_multiple']:.2f}x on {latest['date'].date()}",
        xy=(latest["date"], latest["price_nav_multiple"]),
        xytext=(-98, 25),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1},
        fontsize=9,
        color=INK,
    )
    ax.set_title("BOT traded at a large private-access premium to reported NAV")
    ax.set_ylabel("Price / reported NAV per share")
    ax.set_ylim(0, max(5.8, df["price_nav_multiple"].max() + 0.4))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    clean_ax(ax)
    save(fig, "fig2_bot_premium_path.png")


def fig3_replay_scenarios():
    df = pd.read_csv(DATA_DIR / "bot_mstr_replay_scenarios.csv")
    order = ["Good Sector Bad Entry", "Private Access Base", "MSTR Replay Multiple", "Flywheel Bull"]
    colors = {
        "Good Sector Bad Entry": RED,
        "Private Access Base": BLUE,
        "MSTR Replay Multiple": PURPLE,
        "Flywheel Bull": GREEN,
    }

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for scenario in order:
        part = df[df["scenario"] == scenario].sort_values("month")
        ax.plot(part["year"], part["modeled_price"], color=colors[scenario], linewidth=2.5, label=scenario)

    ax.set_yscale("log")
    ax.set_title("BOT needs both NAV/share growth and multiple durability")
    ax.set_xlabel("Years")
    ax.set_ylabel("Modeled BOT price, log scale")
    ax.set_xlim(0, 10)
    ax.set_yticks([20, 40, 75, 150, 300, 600, 1200])
    ax.yaxis.set_major_formatter(FuncFormatter(money_axis))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.legend(frameon=False, loc="upper left")
    clean_ax(ax)
    save(fig, "fig3_replay_scenarios.png")


def fig4_break_even_heatmap():
    df = pd.read_csv(DATA_DIR / "bot_private_access_premium_break_even.csv")
    pivot = df.pivot(index="nav_cagr", columns="terminal_multiple", values="annualized_return").sort_index()
    values = pivot.values

    fig, ax = plt.subplots(figsize=(10, 6.0))
    vmax = max(abs(np.nanmin(values)), abs(np.nanmax(values)))
    im = ax.imshow(values, cmap="RdYlGn", vmin=-vmax, vmax=vmax, aspect="auto")

    ax.set_title("Break-even depends on both NAV CAGR and terminal price/NAV multiple")
    ax.set_xlabel("Terminal price / NAV multiple")
    ax.set_ylabel("10-year NAV/share CAGR")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"{c:g}x" for c in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f"{r:.0%}" for r in pivot.index])

    for i, nav_cagr in enumerate(pivot.index):
        for j, multiple in enumerate(pivot.columns):
            val = pivot.loc[nav_cagr, multiple]
            color = "white" if abs(val) > 0.18 else INK
            ax.text(j, i, f"{val:.0%}", ha="center", va="center", color=color, fontsize=8.5)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    cbar.set_label("Annualized investor return")
    clean_ax(ax)
    save(fig, "fig4_break_even_heatmap.png")


def main():
    fig1_mstr_decomposition()
    fig2_bot_premium_path()
    fig3_replay_scenarios()
    fig4_break_even_heatmap()
    print("wrote fig1_mstr_decomposition.png")
    print("wrote fig2_bot_premium_path.png")
    print("wrote fig3_replay_scenarios.png")
    print("wrote fig4_break_even_heatmap.png")


if __name__ == "__main__":
    main()
