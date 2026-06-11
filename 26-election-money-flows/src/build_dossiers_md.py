"""Markdown rendering of the dossier set (per-event pages, cohorts, regimes,
wars summary) for venues that render .md natively (the public GitHub repo).
Figures are NOT regenerated - pages reference the PNGs in ../figures/."""
from __future__ import annotations

import pandas as pd

import events as EV
from build_dossiers import auto_bullets, load, slugify
from config import DERIVED_DIR, OUTPUT_DIR

MD_DIR = OUTPUT_DIR / "dossiers_md"
MD_DIR.mkdir(parents=True, exist_ok=True)


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("--" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(lines)


def fmt_pct(v):
    return "--" if pd.isna(v) else f"{v:+.1f}%"


def stats_table_df(ret, cls, anchor, event) -> pd.DataFrame:
    rows = []
    sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) & (ret.event == event)]
    for name in ["SPX", "US", "EM", "China", "Taiwan", "Europe", "Japan", "Bonds", "Gold"]:
        s = sub[sub.series == name].set_index("rel_day")["value"]
        if s.empty:
            continue
        def at(h):
            return s.loc[h] if h in s.index else float("nan")
        rows.append((name, fmt_pct(-at(-60)), fmt_pct(at(20)), fmt_pct(at(60)), fmt_pct(at(120))))
    return pd.DataFrame(rows, columns=["series", "runup pre-60d", "+20d", "+60d", "+120d"])


def event_md(ret, flows, vix, cls, anchor, event, title, subtitle, meta_note=""):
    slug = slugify(f"{cls}_{event}")
    bullets = auto_bullets(ret, flows, vix, cls, anchor, event, meta_note)
    parts = [
        f"# {title}", "",
        f"*{subtitle}*", "",
        "[Index](README.md)", "",
        f"![](../figures/{slug}.png)", "",
        "## What moved", "",
        *[f"- {b}" for b in bullets], "",
        "## Detail", "",
        md_table(stats_table_df(ret, cls, anchor, event)), "",
    ]
    (MD_DIR / f"{slug}.md").write_text("\n".join(parts))
    return f"{slug}.md", title


def cohort_md(cohort_name, title, subtitle, events_list):
    slug = slugify(f"cohort_{cohort_name}")
    coh = pd.read_csv(DERIVED_DIR / "cohort_summary.csv")
    tab = coh[coh.cohort == cohort_name].copy()
    if not tab.empty:
        tab["median"] = tab["median"].map(lambda v: f"{v:+.2f}")
        tab["hit_rate_pos"] = (tab["hit_rate_pos"] * 100).map(lambda v: f"{v:.0f}%")
        tab = tab[["series", "horizon", "median", "hit_rate_pos", "n"]]
        table = md_table(tab)
    else:
        table = "no cohort stats"
    parts = [
        f"# {title}", "", f"*{subtitle}*", "", "[Index](README.md)", "",
        f"![](../figures/{slug}.png)", "",
        "## Cohort statistics (medians and sign hit-rates)", "", table, "",
        f"Events: {', '.join(events_list)}.", "",
    ]
    (MD_DIR / f"{slug}.md").write_text("\n".join(parts))
    return f"{slug}.md", title


def main():
    ret, flows, vix = load()
    pres = EV.presidential_df()
    mids = EV.midterms_df()
    wars = EV.wars_df()
    tars = EV.tariffs_df()
    sections: dict[str, list] = {"Presidential elections": [], "Midterm elections": [],
                                 "Wars and military actions": [], "Tariff shocks": [],
                                 "Cohorts and regimes": []}

    for _, e in pres.iterrows():
        y = e["date"].year
        label = f"{y} {e['winner']}"
        kind = "party flip" if e["flip"] else "incumbent-party hold"
        sub = (f"Presidential election, {e['date'].date()} - winner {e['winner']} ({e['party']}), {kind}, "
               f"day-before odds of winner ~{int(e['winner_pre_odds']*100)}%."
               + (" Result known only " + str(e['result_known'].date()) + "." if (e['result_known'] - e['date']).days > 3 else ""))
        sections["Presidential elections"].append(
            event_md(ret, flows, vix, "presidential", "vote", label, f"{y}: {e['winner']} ({e['party']})", sub, e["note"]))

    for _, e in mids.iterrows():
        y = e["date"].year
        flips = []
        if e["house_flip"]: flips.append("House flipped")
        if e["senate_flip"]: flips.append("Senate flipped")
        sub = f"Midterm election, {e['date'].date()}. {'; '.join(flips) if flips else 'No chamber flipped'}."
        sections["Midterm elections"].append(
            event_md(ret, flows, vix, "midterm", "vote", f"{y} midterm", f"{y} midterm", sub, e["note"]))

    for _, e in wars.iterrows():
        label = f"{e['t0'].year} {e['name']}"
        sub = (f"{e['admin']} administration. Outbreak/event {e['t0'].date()}"
               + (f", buildup from {e['buildup'].date()}" if pd.notna(e["buildup"]) else ", no buildup window")
               + f". {'Telegraphed' if e['telegraphed'] else 'Surprise'}; type: {e['kind']}.")
        sections["Wars and military actions"].append(
            event_md(ret, flows, vix, "war", "outbreak", label, label, sub, e["note"]))

    for _, e in tars.iterrows():
        label = f"{e['t0'].date()} {e['name']}"
        sub = f"{e['admin']} administration tariff/policy shock, {e['t0'].date()}."
        sections["Tariff shocks"].append(
            event_md(ret, flows, vix, "tariff", "announce", label, e["name"], sub))

    pres_events = {f"{e['date'].year} {e['winner']}": e for _, e in pres.iterrows()}
    cohort_defs = [
        ("pres_all", "All presidential elections (1992-2024)", list(pres_events)),
        ("pres_flip", "Party-flip elections", [k for k, e in pres_events.items() if e["flip"]]),
        ("pres_hold", "Incumbent-party holds", [k for k, e in pres_events.items() if not e["flip"]]),
        ("pres_trump", "Trump wins (2016, 2024)", [k for k in pres_events if "Trump" in k]),
        ("midterm_all", "All midterms (1994-2022)", [f"{e['date'].year} midterm" for _, e in mids.iterrows()]),
        ("war_telegraphed", "Telegraphed military actions",
         [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if e["telegraphed"]]),
        ("war_surprise", "Surprise military actions",
         [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if not e["telegraphed"]]),
    ]
    for name, title, evlist in cohort_defs:
        sections["Cohorts and regimes"].append(
            cohort_md(name, title, "Median paths with per-event detail.", evlist))

    # wars summary page
    wp = DERIVED_DIR / "war_puzzle_table.csv"
    if wp.exists():
        tab = pd.read_csv(wp)
        tab["telegraphed"] = tab["telegraphed"].map({True: "yes", False: "no"})
        parts = [
            "# Wars and military actions: summary", "",
            "*Every US-relevant military event 2001-2025 through the same event-study lens.*", "",
            "[Index](README.md)", "",
            "![](../figures/wars_summary.png)", "",
            "## The war-puzzle test, event by event", "", md_table(tab), "",
            "spx_buildup = S&P 500 log return from first credible threat to outbreak. "
            "war_puzzle marks whether the episode matches the buildup-down/outbreak-up pattern "
            "(telegraphed wars) or muted-to-negative initial reaction (surprise events). "
            "gpr_jump = change in daily Geopolitical Risk index, event week vs prior month.", "",
        ]
        (MD_DIR / "wars_summary.md").write_text("\n".join(parts))
        sections["Wars and military actions"].insert(0, ("wars_summary.md", "Wars summary: the war-puzzle table and GPR overlay"))

    # regimes page
    adm = pd.read_csv(DERIVED_DIR / "admin_regimes.csv").round(1)
    parts = [
        "# Regimes: the presidential cycle and per-administration volatility", "",
        "*S&P 500, 1950-2026.*", "", "[Index](README.md)", "",
        "![](../figures/cycle_seasonal.png)", "",
        "## Return and volatility by administration", "", md_table(adm), "",
        "Annualized daily-return statistics within each term; share_big_days = share of days "
        "with absolute move over 1 percent.", "",
    ]
    (MD_DIR / "regimes.md").write_text("\n".join(parts))
    sections["Cohorts and regimes"].append(("regimes.md", "Presidential-cycle seasonality + per-administration regimes"))

    idx = ["# Money around U.S. elections and wars - event dossiers", "",
           "*Cumulative returns, fund flows, and volatility around every U.S. presidential election, "
           "midterm, war, and tariff shock, 1992-2026.*", ""]
    for section, links in sections.items():
        idx += [f"## {section}", ""]
        idx += [f"- [{label}]({href})" for href, label in links]
        idx += [""]
    (MD_DIR / "README.md").write_text("\n".join(idx))
    total = sum(len(v) for v in sections.values())
    print(f"markdown dossiers written: {total} pages + index -> {MD_DIR}", flush=True)


if __name__ == "__main__":
    main()
