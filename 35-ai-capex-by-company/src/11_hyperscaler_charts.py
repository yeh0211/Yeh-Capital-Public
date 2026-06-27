#!/usr/bin/env python3
"""All-hyperscaler charts: the capex ramp (US + China, with tickers) and the
cash-reserves war chest over time. House palette; US solid/ink, China dashed/accent."""
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

# label = "Company (TICKER)"; color/style by region
US = [("AMZN", "Amazon"), ("GOOGL", "Alphabet"), ("META", "Meta"),
      ("MSFT", "Microsoft"), ("ORCL", "Oracle")]
CN = [("BABA", "Alibaba"), ("private", "ByteDance"), ("0700.HK", "Tencent"), ("BIDU", "Baidu")]
CN_TKR = {"BABA": "BABA", "private": "ByteDance", "0700.HK": "TCEHY", "BIDU": "BIDU"}


def us_capex():
    h = defaultdict(dict)
    for r in csv.DictReader(open(D / "capex_raw.csv")):
        if r["capex"] and r["fy"]:
            h[r["ticker"]][int(r["fy"])] = float(r["capex"]) / 1e9
    return h


def china():
    cap, cash = defaultdict(dict), defaultdict(dict)
    for r in csv.DictReader(open(D / "china_history.csv")):
        y = int(r["year"])
        if r["capex_usd_bn"]:
            cap[r["ticker"]][y] = float(r["capex_usd_bn"])
        if r["cash_reserves_usd_bn"]:
            cash[r["ticker"]][y] = float(r["cash_reserves_usd_bn"])
    return cap, cash


def us_cash():
    h = defaultdict(dict)
    for r in csv.DictReader(open(D / "hyperscaler_cash.csv")):
        h[r["ticker"]][int(r["year"])] = float(r["cash_reserves_usd_bn"])
    return h


def label_end(ax, x, y, text, color, dy=0):
    ax.text(x + 0.1, y + dy, text, va="center", ha="left", fontsize=8.5, color=color,
            fontweight="bold" if color == ACCENT else "normal")


def fig_ramp():
    uc = us_capex()
    cc, _ = china()
    fig, ax = plt.subplots(figsize=(9.6, 6.8))
    for tkr, name in US:
        d = uc.get(tkr, {})
        yrs = sorted(y for y in d if y >= 2019)
        ax.plot(yrs, [d[y] for y in yrs], "-", color=INK,
                lw=2.4 if tkr == "AMZN" else 1.5, marker="o", ms=3, zorder=3)
        label_end(ax, yrs[-1], d[yrs[-1]], f"  {name} ({tkr}) {d[yrs[-1]]:.0f}", INK)
    cn_dy = {"private": 3.5, "BABA": -3.5, "0700.HK": 0, "BIDU": 0}  # split close labels
    for tkr, name in CN:
        d = cc.get(tkr, {})
        yrs = sorted(d)
        ax.plot(yrs, [d[y] for y in yrs], "--", color=ACCENT, lw=1.5, marker="s", ms=3, zorder=3)
        label_end(ax, yrs[-1], d[yrs[-1]], f"  {name} ({CN_TKR[tkr]}) {d[yrs[-1]]:.0f}", ACCENT, cn_dy[tkr])
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Capex  ($bn)")
    ax.set_title("Five years of hyperscaler capex: US clouds (solid) vs China clouds (dashed)")
    ax.set_xlim(2019, 2028.4)
    ax.set_ylim(0, 145)
    ax.set_xticks(range(2019, 2027))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.02, 0.97, "Even the largest Chinese cloud spends less than the smallest US hyperscaler.\n"
            "Solid = US filers · dashed = China (ByteDance private/estimated)",
            transform=ax.transAxes, va="top", fontsize=8, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "capex_ramp_all.png", dpi=150)
    plt.close(fig)


def fig_cash():
    uc = us_cash()
    _, cc = china()
    fig, ax = plt.subplots(figsize=(9.4, 6.8))
    for tkr, name in US:
        d = uc.get(tkr, {})
        yrs = sorted(y for y in d if y >= 2021)
        ax.plot(yrs, [d[y] for y in yrs], "-", color=INK, lw=1.5, marker="o", ms=3, zorder=3)
        label_end(ax, yrs[-1], d[yrs[-1]], f"  {name} ({tkr}) {d[yrs[-1]]:.0f}", INK)
    for tkr, name in [("BABA", "Alibaba"), ("0700.HK", "Tencent"), ("BIDU", "Baidu")]:
        d = cc.get(tkr, {})
        yrs = sorted(d)
        if not yrs:
            continue
        ax.plot(yrs, [d[y] for y in yrs], "--", color=ACCENT, lw=1.5, marker="s", ms=3, zorder=3)
        label_end(ax, yrs[-1], d[yrs[-1]], f"  {name} ({CN_TKR[tkr]}) {d[yrs[-1]]:.0f}", ACCENT)
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Cash reserves  ($bn)")
    ax.set_title("The war chest held as capex exploded — except Oracle\n"
                 "Cash + short-term investments, year by year")
    ax.set_xlim(2021, 2028.2)
    ax.set_ylim(0, 160)
    ax.set_xticks(range(2021, 2027))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.30, 0.98,
            "US + Baidu: cash + short-term investments (SEC filings).\n"
            "Alibaba / Tencent: reported cash + treasury investments (broader basis).",
            transform=ax.transAxes, va="top", ha="left", fontsize=7.5, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "cash_reserves.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_ramp()
    fig_cash()
    print("wrote figures/capex_ramp_all.png, figures/cash_reserves.png")
