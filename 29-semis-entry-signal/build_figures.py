#!/usr/bin/env python3
"""House-style figures for study 29 (the semis entry-signal model).

Reads only the shipped data/ files (public market data + reproduced backtest aggregates) and writes
the figures/ PNGs. No warehouse access - fully reproducible from this folder alone.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)

CREAM = "#f7f3ec"; INK = "#1a1a1a"; ACCENT = "#8c2b2b"; GREY = "#9a958c"; SUP = "#7a8a78"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "font.family": "serif",
})


def _title(ax, text):
    ax.set_title(text, loc="left", fontsize=12, fontweight="bold")


def _note(ax, text, loc="br"):
    pos = {"br": (0.99, 0.02, "right", "bottom"), "tr": (0.99, 0.96, "right", "top"),
           "tl": (0.02, 0.93, "left", "top")}[loc]
    ax.text(pos[0], pos[1], text, transform=ax.transAxes, ha=pos[2], va=pos[3],
            fontsize=8, color=GREY, style="italic")


def fig_complex_path():
    df = pd.read_csv(DATA / "complex_prices.csv", parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    ax.plot(df["date"], df["SOXX_growth"], color=INK, lw=1.8, label="SOXX (the chips, 1x)")
    ax.plot(df["date"], df["SOXL_growth"], color=ACCENT, lw=1.6, label="SOXL (3x long)")
    ax.plot(df["date"], df["SOXS_growth"], color=SUP, lw=1.6, label="SOXS (3x inverse)")
    ax.axhline(1.0, color=INK, lw=0.8)
    ax.set_yscale("log")
    ax.set_ylabel("growth of $1 (log)")
    _title(ax, "The chips ran; the 3x inverse bled to almost nothing")
    ax.legend(frameon=False, fontsize=9, loc="center left")
    _note(ax, "adjusted close, option-data window 2024-03-11 to 2026-06-09")
    fig.tight_layout(); fig.savefig(FIG / "complex-path.png", dpi=150); plt.close(fig)


def fig_checklist():
    ev = pd.read_csv(DATA / "checklist_events.csv")
    summ = json.load(open(DATA / "checklist_summary.json"))
    bh = json.load(open(DATA / "checklist_summary.json"))["soxl_buyhold_mean_fwd20"]
    longs = ev.loc[ev["side"] == "LONG SOXL setup", "fwd20"].to_numpy() * 100.0
    shorts = ev.loc[ev["side"] == "SHORT SOXS setup", "fwd20"].to_numpy() * 100.0

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.4))

    # LONG: show all 11 events as a strip (honest about tiny n) + mean and buy-hold lines
    rng = np.linspace(-0.18, 0.18, len(longs))
    a1.scatter(longs, rng, s=42, color=ACCENT, alpha=0.85, zorder=3)
    a1.axvline(0, color=INK, lw=0.8)
    a1.axvline(summ["long"]["mean"] * 100.0, color=ACCENT, lw=1.6, ls="-",
               label=f"setup mean {summ['long']['mean']*100:+.1f}%")
    a1.axvline(bh * 100.0, color=GREY, lw=1.4, ls="--", label=f"buy & hold mean {bh*100:+.1f}%")
    a1.set_yticks([])
    a1.set_xlabel("SOXL forward 20-day return (%)")
    a1.set_ylim(-0.5, 0.5)
    _title(a1, f"LONG checklist: works, on n={summ['long']['n']}")
    a1.legend(frameon=False, fontsize=8, loc="upper left")
    _note(a1, f"hit {summ['long']['hit']*100:.0f}%, median {summ['long']['median']*100:+.1f}%")

    # SHORT: histogram of 142 events, mostly negative
    a2.hist(shorts, bins=28, color=SUP, edgecolor=CREAM, linewidth=0.6)
    a2.axvline(0, color=INK, lw=0.8)
    a2.axvline(summ["short"]["mean"] * 100.0, color=ACCENT, lw=1.6,
               label=f"setup mean {summ['short']['mean']*100:+.1f}%")
    a2.set_xlabel("SOXS forward 20-day return (%)")
    a2.set_ylabel("count")
    _title(a2, f"SHORT checklist: loses, on n={summ['short']['n']}")
    a2.legend(frameon=False, fontsize=8, loc="upper right")
    _note(a2, f"only {summ['short']['hit']*100:.0f}% of windows positive", loc="tl")

    fig.tight_layout(); fig.savefig(FIG / "checklist.png", dpi=150); plt.close(fig)


def _ic_grouped(rows, signals, horizons, hcolors, title, note, fname, ymin=None, note_loc="br"):
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    x = np.arange(len(signals))
    w = 0.8 / len(horizons)
    lut = {(r["horizon"], r["signal"]): r["ic"] for r in rows}
    for j, h in enumerate(horizons):
        vals = [lut.get((h, s), np.nan) for s in signals]
        ax.bar(x + (j - (len(horizons) - 1) / 2) * w, vals, w, color=hcolors[j], label=h)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(signals, fontsize=9)
    ax.set_ylabel("Spearman IC")
    if ymin is not None:
        ax.set_ylim(ymin, max(0.45, max(r["ic"] for r in rows) + 0.06))
    _title(ax, title)
    ax.legend(frameon=False, fontsize=9)
    _note(ax, note, loc=note_loc)
    fig.tight_layout(); fig.savefig(FIG / fname, dpi=150); plt.close(fig)


def fig_options():
    d = json.load(open(DATA / "options_ic.json"))
    _ic_grouped(
        d["rows"],
        signals=["put/call", "d put/call 5d", "OI-weighted IV", "d IV 5d"],
        horizons=["fwd5d", "fwd20d"], hcolors=[GREY, ACCENT],
        title="Options positioning is the strongest factor - in a bull-only window",
        note=f"{d['option_days']} EOD days, {d['n_names']} names; overlapping fwd windows, ~25 independent obs",
        fname="options-ic.png", ymin=-0.55,
    )


def fig_social():
    d = json.load(open(DATA / "social_ic.json"))
    _ic_grouped(
        d["rows"],
        signals=["attention", "engagement", "credible-handle"],
        horizons=["fwd5d", "fwd20d"], hcolors=[ACCENT, GREY],
        title="Buzz predicts the next week, then fades - and can't say which way",
        note=f"{d['posts']} posts over ~5 months, {d['n_obs']} overlapping obs, stance-free",
        fname="social-ic.png", ymin=0.0, note_loc="tl",
    )


def main():
    fig_complex_path()
    fig_checklist()
    fig_options()
    fig_social()
    print("study29 figures:", sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
