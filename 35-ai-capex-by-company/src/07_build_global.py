#!/usr/bin/env python3
"""
Merge the US-filer capex table with the verified foreign-filer capex into a single
global view, recompute concentration, and build the global figures.

US figures: SEC EDGAR (10-K), total-company gross PP&E capex, latest FY.
Foreign figures: each company's own audited filing / earnings release, converted to
USD, double-verified against a second source (see data/foreign_capex.csv for the
per-name source, currency, FX basis and confidence). Both are total-company capex.
"""
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


# clean display labels for foreign tickers
SHORT = {
    "TSM": "TSMC", "005930.KS": "Samsung", "000660.KS": "SK Hynix", "private": "ByteDance",
    "BABA": "Alibaba", "0700.HK": "Tencent", "0981.HK": "SMIC", "2317.TW": "Foxconn",
    "285A.T": "Kioxia", "0992.HK": "Lenovo", "ASML": "ASML", "BIDU": "Baidu",
    "UMC": "UMC", "2308.TW": "Delta", "8035.T": "TokyoElec", "4062.T": "Ibiden",
}


def load_global():
    rows = []
    for r in csv.DictReader(open(D / "capex_table.csv")):
        rows.append({"ticker": r["ticker"], "name": r["ticker"], "company": r["ticker"],
                     "layer": r["layer"], "capex_bn": float(r["capex_bn"]), "region": "US filer"})
    for r in csv.DictReader(open(D / "foreign_capex.csv")):
        rows.append({"ticker": r["ticker"], "name": SHORT.get(r["ticker"], r["ticker"]),
                     "company": r["company"], "layer": r["layer"],
                     "capex_bn": float(r["capex_usd_bn"]), "region": "Foreign"})
    rows.sort(key=lambda r: r["capex_bn"], reverse=True)
    return rows


def main():
    g = load_global()
    with open(D / "global_capex.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "company", "layer", "capex_bn", "region"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(g)

    total = sum(r["capex_bn"] for r in g)
    us = sum(r["capex_bn"] for r in g if r["region"] == "US filer")
    foreign = total - us
    top5 = sum(r["capex_bn"] for r in g[:5])
    top10 = sum(r["capex_bn"] for r in g[:10])

    # layer rollup, split US vs foreign
    layer = defaultdict(lambda: {"US filer": 0.0, "Foreign": 0.0})
    for r in g:
        layer[r["layer"]][r["region"]] += r["capex_bn"]
    layers = sorted(layer.items(), key=lambda kv: -(kv[1]["US filer"] + kv[1]["Foreign"]))

    print(f"=== GLOBAL: {len(g)} companies, total ${total:,.0f}bn ===")
    print(f"  US filers:  ${us:,.0f}bn ({us/total*100:.0f}%)   Foreign: ${foreign:,.0f}bn ({foreign/total*100:.0f}%)")
    print(f"  top-5 (US hyperscalers): ${top5:,.0f}bn = {top5/total*100:.0f}% of global (was 79% US-only)")
    print(f"  top-10: ${top10:,.0f}bn = {top10/total*100:.0f}%")
    print("\n  Layer rollup (US | Foreign | total):")
    for name, v in layers:
        tot = v["US filer"] + v["Foreign"]
        print(f"   {name:22s} {v['US filer']:7.1f} | {v['Foreign']:7.1f} | {tot:7.1f}  ({tot/total*100:4.1f}%)")
    # China hyperscaler bloc
    china = sum(r["capex_bn"] for r in g if r["region"] == "Foreign" and r["layer"] == "Hyperscaler")
    us_hyp = sum(r["capex_bn"] for r in g if r["region"] == "US filer" and r["layer"] == "Hyperscaler")
    print(f"\n  US hyperscaler bloc ${us_hyp:.0f}bn  vs  China cloud bloc ${china:.0f}bn  ({us_hyp/china:.1f}x)")
    print("\n  Top 15 global:")
    for r in g[:15]:
        print(f"   {r['ticker']:10s} {r['capex_bn']:7.1f}  {r['region']:9s} {r['layer']}")

    fig_top(g, total)
    fig_layers(layers, total)
    print("\nwrote figures/global_top.png, figures/global_layers.png, data/global_capex.csv")


def fig_top(g, total):
    top = g[:22]
    fig, ax = plt.subplots(figsize=(8.4, 7.6))
    ys = range(len(top))[::-1]
    for y, r in zip(ys, top):
        foreign = r["region"] == "Foreign"
        ax.barh(y, r["capex_bn"], color=ACCENT if foreign else INK, height=0.66, zorder=3)
        ax.text(r["capex_bn"] + 1.5, y, f"{r['capex_bn']:.0f}", va="center", ha="left",
                fontsize=8, color=ACCENT if foreign else INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r["name"] for r in top], fontsize=8.5)
    ax.set_xlabel("Latest fiscal-year capex  ($bn)")
    ax.set_title("The build is global, but the spend still concentrates in US clouds\n"
                 "Top-22 AI value-chain spenders worldwide")
    ax.set_xlim(0, 145)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.97, 0.05, "accent = non-US filer (foreign)", transform=ax.transAxes,
            ha="right", fontsize=8, color=ACCENT, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "global_top.png", dpi=150)
    plt.close(fig)


def fig_layers(layers, total):
    names = [n for n, _ in layers]
    usv = [v["US filer"] for _, v in layers]
    fgv = [v["Foreign"] for _, v in layers]
    fig, ax = plt.subplots(figsize=(8.6, 6.2))
    ys = range(len(names))[::-1]
    for y, n, u, fr in zip(ys, names, usv, fgv):
        ax.barh(y, u, color=INK, height=0.62, zorder=3)
        ax.barh(y, fr, left=u, color=ACCENT, height=0.62, zorder=3)
        ax.text(u + fr + 3, y, f"{u+fr:.0f}", va="center", ha="left", fontsize=8, color=INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Capex by value-chain layer  ($bn)")
    ax.set_title("Where the US-only view was blind: foundry & memory\n"
                 "Global capex by layer, US filers (ink) vs foreign (accent)")
    ax.set_xlim(0, 500)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.97, 0.06, "ink = US filer   ·   accent = foreign", transform=ax.transAxes,
            ha="right", fontsize=8, color=GREY, style="italic")
    fig.tight_layout()
    fig.savefig(FIG / "global_layers.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
