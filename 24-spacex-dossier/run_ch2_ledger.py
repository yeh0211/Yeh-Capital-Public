#!/usr/bin/env python3
"""Study 29, Chapter 2 — the liquidity ledger.

Is there enough cash to absorb SpaceX plus the record 2026 pipeline?
Compare each mania era's equity-supply calendar against its absorption
capacity (money-market cash, buybacks, total market cap). All constants
sourced in the README; deliberately rounded.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})

# $B unless noted. Sources in README (ICI, S&P DJI, Goldman, Ritter, BI).
ERAS = {
    "1999 (dot-com)": {
        "ipo_proceeds": 65.0,          # Ritter
        "us_mcap": 15_000.0,           # approx
        "mmf_assets": 1_610.0,         # ICI year-end 1999
        "buybacks_yr": 140.0,          # S&P 500, approx
    },
    "2021 (SPAC/IPO wave)": {
        "ipo_proceeds": 142.0,         # traditional IPOs; SPACs added ~160 more
        "ipo_proceeds_incl_spac": 300.0,
        "us_mcap": 53_000.0,
        "mmf_assets": 4_700.0,
        "buybacks_yr": 882.0,          # S&P DJI 2021
    },
    "2026F (mega-IPO year)": {
        "ipo_proceeds": 160.0,         # Goldman forecast incl SpaceX 75
        "ipo_plus_lockup_supply": 700.0,   # RIA upper estimate (study 15)
        "us_mcap": 72_000.0,
        "mmf_assets": 7_870.0,         # ICI week of Jun 10, 2026 (record)
        "buybacks_yr": 1_100.0,        # 2025 run-rate (Q1 record $293.5B)
    },
}

SPACEX = {
    "raise": 75.0,
    "retail_tranche": 22.5,
    "float_now_b_shares": 0.5556,
    "close_day1": 160.9,
    "index_absorb_share_6m": 0.24,     # BI: R1000 + NDX funds, share of float
    "supply_x_float_day180": 9.4,      # study 24
}


def main() -> None:
    out = {"eras": {}}
    for era, c in ERAS.items():
        supply = c.get("ipo_plus_lockup_supply", c.get("ipo_proceeds_incl_spac", c["ipo_proceeds"]))
        out["eras"][era] = {
            "ipo_proceeds_pct_mcap": round(c["ipo_proceeds"] / c["us_mcap"] * 100, 2),
            "ipo_proceeds_pct_mmf": round(c["ipo_proceeds"] / c["mmf_assets"] * 100, 1),
            "ipo_proceeds_pct_buybacks": round(c["ipo_proceeds"] / c["buybacks_yr"] * 100, 0),
            "max_supply_pct_mcap": round(supply / c["us_mcap"] * 100, 2),
            "max_supply_pct_mmf": round(supply / c["mmf_assets"] * 100, 1),
        }

    float_usd = SPACEX["float_now_b_shares"] * SPACEX["close_day1"]
    out["spacex_specific"] = {
        "float_value_day1_close_usd_b": round(float_usd, 0),
        "index_forced_demand_6m_usd_b": round(float_usd * SPACEX["index_absorb_share_6m"], 0),
        "potential_supply_day180_usd_b_at_day1_close": round(float_usd * SPACEX["supply_x_float_day180"], 0),
        "note": "supply at day 180 assumes the full 9.4x float at the day-1 close; actual insider selling is a fraction",
    }
    (HERE / "ch2_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

    # Fig — relative supply shock by era
    fig, ax = plt.subplots(figsize=(9, 4.6))
    eras = list(ERAS)
    x = np.arange(len(eras))
    a = [out["eras"][e]["ipo_proceeds_pct_mmf"] for e in eras]
    b = [out["eras"][e]["max_supply_pct_mmf"] for e in eras]
    ax.bar(x - 0.18, a, width=0.34, color=INK, label="IPO proceeds / money-market cash")
    ax.bar(x + 0.18, b, width=0.34, color=ACCENT, label="Max supply incl SPACs or lockups / money-market cash")
    for xi, (va, vb) in enumerate(zip(a, b)):
        ax.text(xi - 0.18, va + 0.15, f"{va:.1f}%", ha="center", fontsize=9)
        ax.text(xi + 0.18, vb + 0.15, f"{vb:.1f}%", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(eras, fontsize=9.5)
    ax.set_ylabel("% of money-market fund assets")
    ax.set_title("The record 2026 pipeline is the smallest relative cash call of the three manias",
                 loc="left", fontsize=11.5)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "fig3_liquidity_ledger.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
