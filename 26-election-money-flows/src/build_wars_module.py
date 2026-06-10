"""Wars module: war-puzzle verdict table per event, GPR overlay, oil reaction.

Outputs derived/war_puzzle_table.csv and output/dossiers/wars_summary.html.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import events as EV
import event_study as ES
import figures as FG
from build_dossiers import CSS, PAGE
from config import DATA_DIR, DERIVED_DIR, OUTPUT_DIR

DOSSIER_DIR = OUTPUT_DIR / "dossiers"


def ret_between(s: pd.Series, d0, d1) -> float:
    s = s.dropna()
    try:
        a, b = s.asof(pd.Timestamp(d0)), s.asof(pd.Timestamp(d1))
        if pd.isna(a) or pd.isna(b):
            return np.nan
        return float(np.log(b / a) * 100)
    except Exception:  # noqa: BLE001
        return np.nan


def fwd_return(s: pd.Series, d0, tdays: int) -> float:
    s = s.dropna()
    i = ES.reaction_iloc(s.index, d0)
    if i is None or i + tdays >= len(s):
        return np.nan
    return float(np.log(s.iloc[i + tdays] / s.iloc[i]) * 100)


def gpr_jump(gprd: pd.Series, d0) -> float:
    """GPR daily: mean of [0,+5] days minus mean of [-30,-6] days."""
    s = gprd.dropna()
    i = ES.reaction_iloc(s.index, d0)
    if i is None or i < 30:
        return np.nan
    return float(s.iloc[i : i + 6].mean() - s.iloc[i - 30 : i - 5].mean())


def main():
    prices = ES.load_prices()
    spx = prices["idx_spx"]
    oil = prices.get("idx_oil")
    gpr_file = DATA_DIR / "macro" / "gpr_daily.parquet"
    gprd = None
    if gpr_file.exists():
        g = pd.read_parquet(gpr_file)
        cand = [c for c in g.columns if str(c).upper() in ("GPRD", "GPR_DAILY", "GPRD_ACT")] or list(g.columns[:1])
        gprd = pd.to_numeric(g[cand[0]], errors="coerce")

    wars = EV.wars_df()
    rows = []
    for _, e in wars.iterrows():
        buildup_ret = ret_between(spx, e["buildup"], e["t0"]) if pd.notna(e["buildup"]) else np.nan
        post20, post60 = fwd_return(spx, e["t0"], 20), fwd_return(spx, e["t0"], 60)
        oil20 = fwd_return(oil, e["t0"], 20) if oil is not None else np.nan
        jump = gpr_jump(gprd, e["t0"]) if gprd is not None else np.nan
        if e["telegraphed"] and pd.notna(buildup_ret):
            puzzle = "consistent" if (buildup_ret < 0 and post20 > 0) else "mixed"
        elif not e["telegraphed"]:
            puzzle = "consistent" if post20 < 1.0 else "mixed"
        else:
            puzzle = "n/a"
        rows.append(dict(
            admin=e["admin"], event=e["name"], date=str(e["t0"].date()),
            kind=e["kind"], telegraphed=e["telegraphed"],
            spx_buildup=round(buildup_ret, 1) if pd.notna(buildup_ret) else None,
            spx_post20=round(post20, 1) if pd.notna(post20) else None,
            spx_post60=round(post60, 1) if pd.notna(post60) else None,
            oil_post20=round(oil20, 1) if pd.notna(oil20) else None,
            gpr_jump=round(jump, 1) if pd.notna(jump) else None,
            war_puzzle=puzzle,
        ))
    tab = pd.DataFrame(rows)
    tab.to_csv(DERIVED_DIR / "war_puzzle_table.csv", index=False)

    # GPR overlay figure: daily GPR around each outbreak (fan) + oil paths for oil shocks
    panels = []
    if gprd is not None:
        stacks = {}
        for _, e in wars.iterrows():
            p = ES.level_path(gprd, e["t0"], 60, 60)
            if p is not None:
                stacks[f"{e['t0'].year} {e['name'][:18]}"] = p
        gpr_stack = pd.DataFrame(stacks)
        panels.append(lambda ax, st=gpr_stack: FG.fan_panel(
            ax, st, "Geopolitical Risk index (daily) around outbreaks", "GPR", unit_line=False))
    if oil is not None:
        oil_map = {}
        for _, e in wars.iterrows():
            if e["t0"].year in (2003, 2022, 2024, 2025) or "Iran" in e["name"] or "Houthi" in e["name"]:
                p = ES.daily_path(oil, e["t0"], 40, 60)
                if p is not None:
                    oil_map[f"{e['t0'].year} {e['name'][:16]}"] = p
        panels.append(lambda ax, m=oil_map: FG.single_panel(
            ax, m, "WTI crude cumulative return around oil-relevant events, %", "%"))
    fig = FG.event_figure("wars_summary", panels, "Wars: risk pricing and the outbreak effect", ncols=2)

    show = tab.copy()
    show["telegraphed"] = show["telegraphed"].map({True: "yes", False: "no"})
    blocks = [
        dict(kind="img", src=f"../figures/{fig.name}"),
        dict(kind="h2", text="The war-puzzle test, event by event"),
        dict(kind="table", html=show.to_html(index=False, na_rep="--")),
        dict(kind="note", text=(
            "spx_buildup = S&P 500 log return from first credible threat to outbreak. "
            "war_puzzle marks whether the episode matches the buildup-down/outbreak-up pattern "
            "(telegraphed wars) or muted-to-negative initial reaction (surprise events). "
            "gpr_jump = change in daily Geopolitical Risk index, event week vs prior month.")),
    ]
    html = PAGE.render(title="Wars and military actions: summary", css=CSS, blocks=blocks,
                       subtitle="Every US-relevant military event 2001-2025 through the same event-study lens.")
    (DOSSIER_DIR / "wars_summary.html").write_text(html)
    print(tab.to_string(index=False), flush=True)
    print("wars module written", flush=True)


if __name__ == "__main__":
    main()
