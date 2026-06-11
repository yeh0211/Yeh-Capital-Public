"""Chapter 9: where the money goes INSIDE America around elections.

Two layers:
  Flows (2000-)   17 iShares sector funds, weekly creation/redemption as % AUM.
  Returns (1926-) French 49 value-weighted industries around all 25 elections;
                  "Guns" (defense) around every major war since 1939.

Outputs
  derived/sector_flow_league.csv     cohort medians of +13w flows by sector
  derived/industry_party_matrix.csv  49 industries x (D win, R win) medians + hit rates
  derived/defense_wars.csv           Guns/Aero CAR around historic wars
  derived/tech_defense.csv           IYW vs ITA around Trump-era events
  output/figures/sector_flows_elections.png, industry_party.png, tech_defense.png
  output/deep/sectors.md
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import event_study as ES
import events as EV
import figures as FG
from config import DATA_DIR, DERIVED_DIR, OUTPUT_DIR, SECTOR_PANEL

DEEP_DIR = OUTPUT_DIR / "deep"

HISTORIC_WARS = [
    ("WWII begins (Europe)", "1939-09-01"),
    ("Pearl Harbor", "1941-12-08"),
    ("Korea invasion", "1950-06-26"),
    ("Kuwait invaded", "1990-08-02"),
    ("Desert Storm", "1991-01-17"),
    ("9/11 (reopen)", "2001-09-17"),
    ("Iraq invasion", "2003-03-20"),
    ("Russia invades Ukraine", "2022-02-24"),
    ("Israel-Iran war", "2025-06-13"),
    ("US strikes Iran", "2025-06-22"),
]

TD_EVENTS = [
    ("2016 election", "2016-11-08"), ("2024 election", "2024-11-05"),
    ("Russia invades Ukraine", "2022-02-24"), ("Liberation Day", "2025-04-02"),
    ("Israel-Iran war", "2025-06-13"),
]


def sector_flows() -> tuple[pd.DataFrame, dict]:
    funds = ES.load_fund_histories()
    pct = {t: ES.weekly_flow_pct(funds[t]) for t in SECTOR_PANEL if t in funds}
    pres = EV.presidential_df()
    mids = EV.midterms_df()
    events = {f"{e['date'].year} {e['winner']}": e["date"] for _, e in pres.iterrows()}
    events.update({f"{e['date'].year} midterm": e["date"] for _, e in mids.iterrows()})
    rows = []
    for t, s in pct.items():
        for label, date in events.items():
            cp = ES.weekly_caf_path(s, date, 26, 26)
            if cp is None or 13 not in cp.index:
                continue
            rows.append(dict(sector=SECTOR_PANEL[t], ticker=t, event=label,
                             post13w=float(cp.loc[13]),
                             post26w=float(cp.loc[26]) if 26 in cp.index else np.nan))
    df = pd.DataFrame(rows)
    cohorts = {
        "all_presidential": [k for k in events if "midterm" not in k],
        "R_wins": ["2004 Bush", "2016 Trump", "2024 Trump"],
        "D_wins": ["2008 Obama", "2012 Obama", "2020 Biden"],
        "trump_wins": ["2016 Trump", "2024 Trump"],
        "midterms": [k for k in events if "midterm" in k],
    }
    league_rows = []
    for coh, evs in cohorts.items():
        sub = df[df.event.isin(evs)]
        for sector, g in sub.groupby("sector"):
            league_rows.append(dict(cohort=coh, sector=sector,
                                    median_post13w=round(g["post13w"].median(), 1),
                                    hit_rate_pos=round((g["post13w"] > 0).mean(), 2),
                                    n=len(g)))
    league = pd.DataFrame(league_rows)
    league.to_csv(DERIVED_DIR / "sector_flow_league.csv", index=False)
    return league, pct


def industry_indexes() -> pd.DataFrame:
    ff49 = pd.read_parquet(DATA_DIR / "macro" / "ff49_daily.parquet")
    return (1 + ff49.fillna(0)).cumprod().where(ff49.notna().cummax())


def industry_party_matrix(idx: pd.DataFrame) -> pd.DataFrame:
    pres = EV.presidential_df(deep=True)
    rows = []
    for ind in idx.columns:
        s = idx[ind].dropna()
        vals = {"D": [], "R": []}
        for _, e in pres.iterrows():
            p = ES.daily_path(s, e["date"], 10, 120)
            if p is not None and 60 in p.index:
                vals[e["party"]].append(float(p.loc[60]))
        if len(vals["D"]) + len(vals["R"]) < 15:
            continue
        rows.append(dict(
            industry=ind,
            d_win_post60=round(np.median(vals["D"]), 1), d_hit=round(np.mean([v > 0 for v in vals["D"]]), 2), d_n=len(vals["D"]),
            r_win_post60=round(np.median(vals["R"]), 1), r_hit=round(np.mean([v > 0 for v in vals["R"]]), 2), r_n=len(vals["R"]),
        ))
    m = pd.DataFrame(rows)
    m["r_minus_d"] = (m["r_win_post60"] - m["d_win_post60"]).round(1)
    m = m.sort_values("r_minus_d", ascending=False)
    m.to_csv(DERIVED_DIR / "industry_party_matrix.csv", index=False)
    return m


def defense_wars(idx: pd.DataFrame, mkt_idx: pd.Series) -> pd.DataFrame:
    rows = []
    for name, d in HISTORIC_WARS:
        for ind in ("Guns", "Aero"):
            if ind not in idx.columns:
                continue
            s = idx[ind].dropna()
            p = ES.daily_path(s, d, 10, 120)
            pm = ES.daily_path(mkt_idx, d, 10, 120)
            if p is None:
                continue
            def at(path, h):
                return round(float(path.loc[h]), 1) if path is not None and h in path.index else np.nan
            rows.append(dict(event=name, date=d, industry=ind,
                             post20=at(p, 20), post60=at(p, 60), post120=at(p, 120),
                             rel_mkt_60=round(at(p, 60) - at(pm, 60), 1) if pm is not None and 60 in pm.index and 60 in p.index else np.nan))
    df = pd.DataFrame(rows)
    df.to_csv(DERIVED_DIR / "defense_wars.csv", index=False)
    return df


def tech_defense(pct: dict) -> pd.DataFrame:
    funds = ES.load_fund_histories()
    rows = []
    for name, d in TD_EVENTS:
        row = dict(event=name, date=d)
        for t, key in (("IYW", "tech"), ("ITA", "defense")):
            if t in pct:
                cp = ES.weekly_caf_path(pct[t], d, 26, 26)
                row[f"{key}_flow_13w"] = round(float(cp.loc[13]), 1) if cp is not None and 13 in cp.index else np.nan
            if t in funds:
                nav = funds[t]["nav"].dropna()
                p = ES.daily_path(nav, d, 10, 120)
                row[f"{key}_ret_60d"] = round(float(p.loc[60]), 1) if p is not None and 60 in p.index else np.nan
        if "tech_ret_60d" in row and "defense_ret_60d" in row:
            row["defense_minus_tech_60d"] = round(row["defense_ret_60d"] - row["tech_ret_60d"], 1)
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(DERIVED_DIR / "tech_defense.csv", index=False)
    return df


def make_figures(league: pd.DataFrame, matrix: pd.DataFrame, pct: dict, idx: pd.DataFrame):
    # f1: sector flow league
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.2), sharex=False)
    for ax, coh, title in zip(axes, ["all_presidential", "trump_wins", "midterms"],
                              ["All elections 2004-2024", "Trump wins (2016, 2024)", "Midterms 2002-2022"]):
        s = league[league.cohort == coh].sort_values("median_post13w")
        ax.barh(s["sector"], s["median_post13w"], color=FG.INK, height=0.6)
        ax.axvline(0, color=FG.INK, lw=0.8)
        ax.set_title(f"{title}\nmedian fund flow, % of AUM, 13 weeks after", loc="left", fontsize=9)
        ax.tick_params(labelsize=7.5)
    fig.tight_layout()
    fig.savefig(FG.FIG_DIR / "sector_flows_elections.png", bbox_inches="tight")
    plt.close(fig)

    # f2: industries by party (top/bottom by R-D spread)
    m = matrix.dropna(subset=["r_minus_d"])
    show = pd.concat([m.head(10), m.tail(10)])
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    y = np.arange(len(show))
    ax.barh(y - 0.2, show["r_win_post60"], height=0.38, color=FG.GRAY, label="after R wins")
    ax.barh(y + 0.2, show["d_win_post60"], height=0.38, color=FG.INK, label="after D wins")
    ax.set_yticks(y, show["industry"], fontsize=8)
    ax.axvline(0, color=FG.INK, lw=0.8)
    ax.invert_yaxis()
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Industry return, 60 trading days after the election - median across 25 elections since 1928\n(top/bottom 10 by R-minus-D spread)", loc="left", fontsize=10)
    ax.set_xlabel("median cumulative return, %")
    fig.tight_layout()
    fig.savefig(FG.FIG_DIR / "industry_party.png", bbox_inches="tight")
    plt.close(fig)

    # f3: tech vs defense
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7))
    for ax, (name, d) in zip(axes.flat[:2], [("2024 election", "2024-11-05"), ("Russia invades Ukraine", "2022-02-24")]):
        for t, style, lab in (("IYW", "--", "tech (IYW)"), ("ITA", "-", "defense (ITA)")):
            cp = ES.weekly_caf_path(pct[t], d, 26, 26)
            if cp is not None:
                ax.plot(cp.index, cp.values, color=FG.INK if t == "ITA" else FG.GRAY, lw=1.4, ls=style, label=lab)
        ax.axvline(0, color=FG.ACCENT, lw=0.9)
        ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
        ax.legend(frameon=False, fontsize=8)
        ax.set_title(f"Fund flows around {name}, cum % of AUM (weekly)", loc="left", fontsize=9)
    ax = axes.flat[2]
    guns = idx["Guns"].dropna()
    stacks = {}
    for name, d in HISTORIC_WARS:
        p = ES.daily_path(guns, d, 20, 120)
        if p is not None:
            stacks[name] = p
    FG.fan_panel(ax, pd.DataFrame(stacks), "Defense industry (Guns) around wars since 1939, %", "%")
    ax = axes.flat[3]
    rel = (idx["Guns"] / idx["Hardw"]).dropna()
    p22 = ES.daily_path(rel, "2022-02-24", 60, 120)
    p25 = ES.daily_path(rel, "2025-06-13", 60, 120)
    p24 = ES.daily_path(rel, "2024-11-05", 60, 120)
    for p, lab, style in [(p22, "Ukraine 2022", "-"), (p24, "2024 election", "--"), (p25, "Israel-Iran 2025", ":")]:
        if p is not None:
            ax.plot(p.index, p.values, color=FG.INK, lw=1.3, ls=style, label=lab)
    ax.axvline(0, color=FG.ACCENT, lw=0.9)
    ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Defense-vs-tech relative return (Guns/Hardware), %", loc="left", fontsize=9)
    fig.tight_layout()
    fig.savefig(FG.FIG_DIR / "tech_defense.png", bbox_inches="tight")
    plt.close(fig)


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("--" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(lines)


def main():
    league, pct = sector_flows()
    idx = industry_indexes()
    ff = pd.read_parquet(DATA_DIR / "macro" / "ff_factors_daily.parquet")
    mkt_idx = (1 + ff["mkt_tr"]).cumprod()
    matrix = industry_party_matrix(idx)
    dwars = defense_wars(idx, mkt_idx)
    td = tech_defense(pct)
    make_figures(league, matrix, pct, idx)

    md = [
        "# Sector rotation: where the money goes inside America", "",
        "*Two layers: creation/redemption flows for 17 iShares sector funds (2000-), and the French 49 value-weighted industries (1926-) for returns around all 25 elections and every major war since 1939.*", "",
        "![](../figures/sector_flows_elections.png)", "",
        "## Sector fund flows, 13 weeks after the vote (cohort medians)", "",
        md_table(league.pivot_table(index="sector", columns="cohort", values="median_post13w").round(1).reset_index()), "",
        "![](../figures/industry_party.png)", "",
        "## Who wins under whom: industries 60 trading days after the election, 1928-2024", "",
        md_table(matrix), "",
        "![](../figures/tech_defense.png)", "",
        "## Tech vs defense around the Trump-era events", "",
        md_table(td), "",
        "## Defense around wars since 1939", "",
        md_table(dwars), "",
        "Flows are % of each fund's AUM (sector funds differ hugely in size - percentages are not dollars). "
        "Industry returns are value-weighted French industries; 'Guns' = defense, 'Hardw'/'Chips'/'Softw' = the tech stack.", "",
    ]
    (DEEP_DIR / "sectors.md").write_text("\n".join(md))

    # verification
    banks = idx["Banks"].dropna()
    p16 = ES.daily_path(banks, "2016-11-08", 10, 120)
    print("VERIFY Banks post-2016 +60d strongly positive:", round(float(p16.loc[60]), 1), flush=True)
    guns22 = ES.daily_path(idx["Guns"].dropna(), "2022-02-24", 10, 120)
    print("VERIFY Guns post-Ukraine +60d positive:", round(float(guns22.loc[60]), 1), flush=True)
    ita = ES.weekly_caf_path(pct["ITA"], "2022-02-24", 26, 26)
    print("VERIFY ITA flows post-Ukraine +13w:", round(float(ita.loc[13]), 1), flush=True)
    print("matrix industries:", len(matrix), "| league rows:", len(league), flush=True)


if __name__ == "__main__":
    main()
