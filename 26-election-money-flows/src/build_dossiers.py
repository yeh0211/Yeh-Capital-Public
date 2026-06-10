"""Render per-event dossiers + cohort pages as static HTML in house style."""
from __future__ import annotations

import re

import pandas as pd
from jinja2 import Template

import events as EV
import figures as FG
from config import DERIVED_DIR, OUTPUT_DIR

DOSSIER_DIR = OUTPUT_DIR / "dossiers"
DOSSIER_DIR.mkdir(parents=True, exist_ok=True)

CSS = """
body { background:#faf8f2; color:#1c1b18; font-family: Georgia, 'Times New Roman', serif;
       max-width: 980px; margin: 2.2rem auto; padding: 0 1.2rem; line-height: 1.5; }
h1 { font-size: 1.55rem; margin-bottom: .2rem; }
h2 { font-size: 1.1rem; margin-top: 1.6rem; border-bottom: 1px solid #1c1b18; padding-bottom: .15rem;}
.meta { color:#6e6857; font-size: .92rem; margin-bottom: 1rem; }
table { border-collapse: collapse; font-size: .88rem; margin: .8rem 0; }
th, td { padding: .25rem .7rem; text-align: right; border-bottom: 1px solid #e4dfd2; }
th:first-child, td:first-child { text-align: left; }
thead th { border-bottom: 1.5px solid #1c1b18; }
img { max-width: 100%; border: 1px solid #e4dfd2; margin: .6rem 0; }
a { color:#8c1c13; text-decoration: none; }
ul { margin: .4rem 0 .4rem 1.1rem; padding: 0; }
.note { font-size: .9rem; color:#444036; }
.navline { font-size:.9rem; margin-bottom:1.4rem; }
"""

PAGE = Template("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{{ title }}</title><style>{{ css }}</style></head>
<body>
<div class="navline"><a href="index.html">Index</a></div>
<h1>{{ title }}</h1>
<div class="meta">{{ subtitle }}</div>
{% for block in blocks %}
  {% if block.kind == 'h2' %}<h2>{{ block.text }}</h2>{% endif %}
  {% if block.kind == 'img' %}<img src="{{ block.src }}" alt="">{% endif %}
  {% if block.kind == 'table' %}{{ block.html }}{% endif %}
  {% if block.kind == 'bullets' %}<ul>{% for b in block.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  {% if block.kind == 'note' %}<p class="note">{{ block.text }}</p>{% endif %}
{% endfor %}
</body></html>
""")

INDEX = Template("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{{ title }}</title><style>{{ css }}</style></head>
<body>
<h1>{{ title }}</h1>
<div class="meta">{{ subtitle }}</div>
{% for section, links in sections.items() %}
<h2>{{ section }}</h2>
<ul>{% for href, label in links %}<li><a href="{{ href }}">{{ label }}</a></li>{% endfor %}</ul>
{% endfor %}
</body></html>
""")


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def load():
    ret = pd.read_parquet(DERIVED_DIR / "returns_paths.parquet")
    flows = pd.read_parquet(DERIVED_DIR / "flows_caf_paths.parquet")
    vix = pd.read_parquet(DERIVED_DIR / "vix_paths.parquet")
    return ret, flows, vix


def series_for(ret, cls, anchor, event, names):
    out = {}
    sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) & (ret.event == event)]
    for n in names:
        s = sub[sub.series == n].set_index("rel_day")["value"].sort_index()
        if len(s):
            out[n] = s
    return out


def flows_for(flows, cls, event, buckets):
    out = {}
    sub = flows[(flows.event_class == cls) & (flows.event == event)]
    for b in buckets:
        s = sub[sub.bucket == b].set_index("rel_week")["value"].sort_index()
        if len(s):
            out[b] = s
    return out


def fmt_pct(v):
    return "--" if pd.isna(v) else f"{v:+.1f}%"


def event_stats_table(ret, vix, cls, anchor, event) -> str:
    rows = []
    sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) & (ret.event == event)]
    for name in ["SPX", "US", "EM", "China", "Taiwan", "Europe", "Japan", "Bonds", "Gold"]:
        s = sub[sub.series == name].set_index("rel_day")["value"]
        if s.empty:
            continue
        def at(h):
            return s.loc[h] if h in s.index else float("nan")
        rows.append((name, fmt_pct(-at(-60)), fmt_pct(at(20)), fmt_pct(at(60)), fmt_pct(at(120))))
    df = pd.DataFrame(rows, columns=["series", "runup pre-60d", "+20d", "+60d", "+120d"])
    return df.to_html(index=False, escape=False)


def auto_bullets(ret, flows, vix, cls, anchor, event, meta_note="") -> list[str]:
    out = []
    sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) & (ret.event == event)]
    spx = sub[sub.series == "SPX"].set_index("rel_day")["value"]
    if not spx.empty:
        if -60 in spx.index:
            out.append(f"Equities ran {fmt_pct(-spx.loc[-60])} over the 60 trading days into the event.")
        if 60 in spx.index:
            out.append(f"The S&P 500 moved {fmt_pct(spx.loc[60])} over the following 60 trading days"
                       + (f" and {fmt_pct(spx.loc[120])} over 120." if 120 in spx.index else "."))
    for b, label in [("US", "US equity funds"), ("EM", "emerging-market funds"),
                     ("Europe", "Europe funds"), ("China", "China funds")]:
        fsub = flows[(flows.event_class == cls) & (flows.event == event) & (flows.bucket == b)]
        s = fsub.set_index("rel_week")["value"]
        if not s.empty and 13 in s.index:
            out.append(f"Cumulative net flows into {label}: {fmt_pct(s.loc[13])} of assets in the 13 weeks after"
                       + (f" (vs {fmt_pct(-s.loc[-13])} in the 13 weeks before)." if -13 in s.index else "."))
    vsub = vix[(vix.event_class == cls) & (vix.anchor == anchor) & (vix.event == event)]
    vs = vsub.set_index("rel_day")["value"]
    if not vs.empty and -1 in vs.index and 1 in vs.index:
        out.append(f"Implied volatility moved {vs.loc[1] - vs.loc[-1]:+.1f} VIX points across the event"
                   f" (from {vs.loc[-1]:.1f}).")
    if meta_note:
        out.append(meta_note)
    return out


def build_event_page(ret, flows, vix, cls, anchor, event, title, subtitle, meta_note=""):
    slug = slugify(f"{cls}_{event}")
    ret_map = series_for(ret, cls, anchor, event, ["SPX", "EM", "China", "Europe"])
    rot_map = series_for(ret, cls, anchor, event, ["EM_minus_US", "China_minus_US", "Europe_minus_US"])
    flow_map = flows_for(flows, cls, event, ["US", "EM", "Europe", "China"])
    vsub = vix[(vix.event_class == cls) & (vix.anchor == anchor) & (vix.event == event)]
    vmap = {"VIX": vsub.set_index("rel_day")["value"].sort_index()} if not vsub.empty else {}

    panels = [
        lambda ax: FG.single_panel(ax, ret_map, "Cumulative return, % (0 = event day)", "%", accent_key="SPX"),
        lambda ax: FG.single_panel(ax, rot_map, "Return relative to US equities, %", "%"),
        lambda ax: FG.single_panel(ax, flow_map, "Cumulative fund flows, % of AUM (weekly)", "% AUM"),
        lambda ax: FG.single_panel(ax, vmap, "VIX level", "", accent_key="VIX", zero_line=False),
    ]
    fig_path = FG.event_figure(slug, panels, title)
    blocks = [
        dict(kind="img", src=f"../figures/{fig_path.name}"),
        dict(kind="h2", text="What moved"),
        dict(kind="bullets", bullets=auto_bullets(ret, flows, vix, cls, anchor, event, meta_note)),
        dict(kind="h2", text="Detail"),
        dict(kind="table", html=event_stats_table(ret, vix, cls, anchor, event)),
    ]
    html = PAGE.render(title=title, subtitle=subtitle, css=CSS, blocks=blocks)
    (DOSSIER_DIR / f"{slug}.html").write_text(html)
    return f"{slug}.html", title


def build_cohort_page(ret, flows, cohort_name, title, subtitle, cls, anchor, events_list):
    slug = slugify(f"cohort_{cohort_name}")
    sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) & (ret.event.isin(events_list))]
    spx_stack = sub[sub.series == "SPX"].pivot_table(index="rel_day", columns="event", values="value")
    em_rel = sub[sub.series == "EM_minus_US"].pivot_table(index="rel_day", columns="event", values="value")
    fsub = flows[(flows.event_class == cls) & (flows.event.isin(events_list))]
    us_flow = fsub[fsub.bucket == "US"].pivot_table(index="rel_week", columns="event", values="value")
    em_flow = fsub[fsub.bucket == "EM"].pivot_table(index="rel_week", columns="event", values="value")
    panels = [
        lambda ax: FG.fan_panel(ax, spx_stack, "S&P 500 cumulative return, % (per event + median)", "%"),
        lambda ax: FG.fan_panel(ax, em_rel, "EM minus US return, %", "%"),
        lambda ax: FG.fan_panel(ax, us_flow, "US equity fund flows, cumulative % of AUM", "% AUM"),
        lambda ax: FG.fan_panel(ax, em_flow, "EM fund flows, cumulative % of AUM", "% AUM"),
    ]
    fig_path = FG.event_figure(slug, panels, title)
    coh = pd.read_csv(DERIVED_DIR / "cohort_summary.csv")
    tab = coh[coh.cohort == cohort_name].copy()
    if not tab.empty:
        tab["median"] = tab["median"].map(lambda v: f"{v:+.2f}")
        tab["hit_rate_pos"] = (tab["hit_rate_pos"] * 100).map(lambda v: f"{v:.0f}%")
        tab = tab[["series", "horizon", "median", "hit_rate_pos", "n"]]
        table_html = tab.to_html(index=False, escape=False)
    else:
        table_html = "<p class='note'>no cohort stats</p>"
    blocks = [
        dict(kind="img", src=f"../figures/{fig_path.name}"),
        dict(kind="h2", text="Cohort statistics (medians and sign hit-rates)"),
        dict(kind="table", html=table_html),
        dict(kind="note", text=f"Events: {', '.join(events_list)}."),
    ]
    html = PAGE.render(title=title, subtitle=subtitle, css=CSS, blocks=blocks)
    (DOSSIER_DIR / f"{slug}.html").write_text(html)
    return f"{slug}.html", title


def main():
    ret, flows, vix = load()
    pres = EV.presidential_df()
    mids = EV.midterms_df()
    wars = EV.wars_df()
    tars = EV.tariffs_df()
    sections = {"Presidential elections": [], "Midterm elections": [], "Wars and military actions": [],
                "Tariff shocks": [], "Cohorts and regimes": []}

    for _, e in pres.iterrows():
        y = e["date"].year
        label = f"{y} {e['winner']}"
        odds = f"day-before odds of winner ~{int(e['winner_pre_odds']*100)}%"
        kind = "party flip" if e["flip"] else "incumbent-party hold"
        sub = (f"Presidential election, {e['date'].date()} - winner {e['winner']} ({e['party']}), {kind}, "
               f"{odds}." + (" Result known only " + str(e['result_known'].date()) + "." if (e['result_known'] - e['date']).days > 3 else ""))
        sections["Presidential elections"].append(
            build_event_page(ret, flows, vix, "presidential", "vote", label,
                             f"{y}: {e['winner']} ({e['party']})", sub, meta_note=e["note"]))

    for _, e in mids.iterrows():
        y = e["date"].year
        label = f"{y} midterm"
        flips = []
        if e["house_flip"]: flips.append("House flipped")
        if e["senate_flip"]: flips.append("Senate flipped")
        sub = f"Midterm election, {e['date'].date()}. {'; '.join(flips) if flips else 'No chamber flipped'}."
        sections["Midterm elections"].append(
            build_event_page(ret, flows, vix, "midterm", "vote", label, f"{y} midterm", sub, meta_note=e["note"]))

    for _, e in wars.iterrows():
        label = f"{e['t0'].year} {e['name']}"
        sub = (f"{e['admin']} administration. Outbreak/event {e['t0'].date()}"
               + (f", buildup from {e['buildup'].date()}" if pd.notna(e["buildup"]) else ", no buildup window")
               + f". {'Telegraphed' if e['telegraphed'] else 'Surprise'}; type: {e['kind']}.")
        sections["Wars and military actions"].append(
            build_event_page(ret, flows, vix, "war", "outbreak", label, label, sub, meta_note=e["note"]))

    for _, e in tars.iterrows():
        label = f"{e['t0'].date()} {e['name']}"
        sub = f"{e['admin']} administration tariff/policy shock, {e['t0'].date()}."
        sections["Tariff shocks"].append(
            build_event_page(ret, flows, vix, "tariff", "announce", label, e["name"], sub))

    if (DOSSIER_DIR / "wars_summary.html").exists():
        sections["Wars and military actions"].insert(
            0, ("wars_summary.html", "Wars summary: the war-puzzle table and GPR overlay"))

    pres_events = {f"{e['date'].year} {e['winner']}": e for _, e in pres.iterrows()}
    cohort_defs = [
        ("pres_all", "All presidential elections (1992-2024)", "presidential", "vote", list(pres_events)),
        ("pres_flip", "Party-flip elections", "presidential", "vote", [k for k, e in pres_events.items() if e["flip"]]),
        ("pres_hold", "Incumbent-party holds", "presidential", "vote", [k for k, e in pres_events.items() if not e["flip"]]),
        ("pres_trump", "Trump wins (2016, 2024)", "presidential", "vote", [k for k in pres_events if "Trump" in k]),
        ("midterm_all", "All midterms (1994-2022)", "midterm", "vote", [f"{e['date'].year} midterm" for _, e in mids.iterrows()]),
        ("war_telegraphed", "Telegraphed military actions", "war", "outbreak",
         [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if e["telegraphed"]]),
        ("war_surprise", "Surprise military actions", "war", "outbreak",
         [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if not e["telegraphed"]]),
    ]
    for name, title, cls, anchor, evlist in cohort_defs:
        sections["Cohorts and regimes"].append(
            build_cohort_page(ret, flows, name, title, "Median paths with per-event detail.", cls, anchor, evlist))

    # presidential-cycle seasonality figure page
    seas = pd.read_csv(DERIVED_DIR / "cycle_seasonal.csv")
    smap = {f"Year {int(t)}": seas[seas.tyear == t].set_index("doy_rank")["cum_ret_pct"]
            for t in sorted(seas.tyear.dropna().unique())}
    fig = FG.event_figure("cycle_seasonal", [
        lambda ax: FG.single_panel(ax, smap, "Average S&P 500 path by presidential-cycle year (1950-2025)",
                                   "%", accent_key="Year 2", zero_line=True)],
        "The four-year cycle: midterm years (Year 2) trough, then the strongest stretch")
    adm = pd.read_csv(DERIVED_DIR / "admin_regimes.csv").round(1)
    blocks = [
        dict(kind="img", src=f"../figures/{fig.name}"),
        dict(kind="h2", text="Return and volatility by administration"),
        dict(kind="table", html=adm.to_html(index=False)),
        dict(kind="note", text="Annualized daily-return statistics within each term; share_big_days = share of days with absolute move over 1 percent."),
    ]
    (DOSSIER_DIR / "regimes.html").write_text(PAGE.render(
        title="Regimes: the presidential cycle and per-administration volatility",
        subtitle="S&P 500, 1950-2026.", css=CSS, blocks=blocks))
    sections["Cohorts and regimes"].append(("regimes.html", "Presidential-cycle seasonality + per-administration regimes"))

    idx = INDEX.render(title="Money around U.S. elections and wars - event dossiers",
                       subtitle="Cumulative returns, fund flows, and volatility around every U.S. presidential election, midterm, war, and tariff shock, 1992-2026.",
                       css=CSS, sections=sections)
    (DOSSIER_DIR / "index.html").write_text(idx)
    total = sum(len(v) for v in sections.values())
    print(f"dossiers written: {total} pages + index -> {DOSSIER_DIR}", flush=True)


if __name__ == "__main__":
    main()
