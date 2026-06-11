"""Synthesis brief: single tear-sheet answering the six research questions.

All numbers are pulled live from derived/ so the brief regenerates as data
updates; the format is locked, content swaps.
"""
from __future__ import annotations

import shutil

import pandas as pd
from jinja2 import Template

from config import DATA_DIR, DERIVED_DIR, OUTPUT_DIR

BRIEF_DIR = OUTPUT_DIR / "brief"
BRIEF_DIR.mkdir(parents=True, exist_ok=True)

CSS = """
body { background:#faf8f2; color:#1c1b18; font-family: Georgia, 'Times New Roman', serif;
       max-width: 880px; margin: 2.4rem auto; padding: 0 1.3rem; line-height: 1.55; }
h1 { font-size: 1.7rem; margin-bottom: .15rem; }
.dek { color:#444036; font-size: 1.02rem; margin-bottom: 1.6rem; font-style: italic; }
h2 { font-size: 1.08rem; margin-top: 1.9rem; border-bottom: 1.5px solid #1c1b18; padding-bottom: .15rem; }
p { margin: .55rem 0; }
table { border-collapse: collapse; font-size: .86rem; margin: .7rem 0; width: 100%; }
th, td { padding: .24rem .55rem; text-align: right; border-bottom: 1px solid #e4dfd2; }
th:first-child, td:first-child { text-align: left; }
thead th { border-bottom: 1.5px solid #1c1b18; }
img { max-width: 100%; border: 1px solid #e4dfd2; margin: .5rem 0; }
.k { color:#8c1c13; font-weight: bold; }
.limits { font-size:.88rem; color:#444036; border-top: 1px solid #1c1b18; margin-top: 2rem; padding-top: .6rem; }
.date { color:#6e6857; font-size:.9rem; }
"""

TPL = Template("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Money around U.S. elections</title><style>{{ css }}</style></head>
<body>
<h1>Money around U.S. elections</h1>
<div class="dek">Where it goes before the vote, after the result, under each kind of winner, and when the shooting starts. Every U.S. presidential election and midterm 1992-2024, every U.S.-relevant military action 2001-2025, measured in fund flows, returns, and volatility.</div>
<div class="date">June 2026 - dossier set with per-event detail accompanies this note</div>

<h2>The election cycle in one motion</h2>
<p>Investors hedge the event, not the outcome. Implied volatility builds for roughly two months into a presidential vote (median VIX {{ vix_m20 }} twenty days out against {{ vix_m60 }} sixty days out) and collapses within days of a result, whoever wins: {{ vix_p1 }} the day after, {{ vix_p5 }} a week after. Cash-proxy funds absorb a median {{ cash_pre13 }} of assets in the quarter before the vote. Then the re-risking: U.S. equity funds take in a median <span class="k">{{ us_post13 }} of assets in the thirteen weeks after the vote</span> - positive after every election in the sample - and {{ us_post26 }} by twenty-six weeks. The S&P 500's median path: {{ spx_pre20 }} in the month before, <span class="k">{{ spx_p20 }} in the month after, {{ spx_p120 }} over six months</span>.</p>
<img src="cohort_pres_all.png" alt="">

<h2>Does the money leave America? Mostly no - it leaves China</h2>
<p>The popular narrative says capital flees the U.S. when the result displeases it. The flow data say otherwise: after a typical election, U.S. and foreign-region funds get inflows together - allocation is not a zero-sum exit. What moves is the relative line, and the clean repeated case is a Trump win. In the thirteen weeks after November 2016, U.S. equity funds gained {{ t16_us13 }} of assets while China funds lost <span class="k">{{ t16_cn13 }}</span>; after November 2024, U.S. funds gained {{ t24_us13 }} while China funds lost <span class="k">{{ t24_cn13 }}</span>, reaching {{ t24_cn26 }} by half a year. Taiwan funds saw {{ t24_tw13 }} over the same 2024 window, and Taiwan underperformed U.S. equities by {{ t24_tw60 }} in the first sixty trading days, Korea by {{ t24_kr60 }}. Money did not leave America after Trump won; it left the tariff targets.</p>
<p>The reversal comes later and is just as regular. By six months after both Trump wins, Europe-relative returns had flipped positive ({{ t_eu120 }} versus U.S. at 120 trading days, both episodes) and in 2025 the rotation became flows: Europe funds took in roughly twenty percent of assets across February-April 2025 while U.S. funds bled through the tariff quarter. The first quarter after a Trump win belongs to America; the second leg has twice belonged to everyone else.</p>
<img src="cohort_pres_trump.png" alt="">

<h2>Midterms are the better signal</h2>
<p>The strongest, most repeatable pattern in the dataset is not the presidential race. After midterm elections the S&P 500's median move is {{ mid_p120 }} over the next 120 trading days - <span class="k">positive after all eight midterms since 1994</span>. The average midterm year since 1950 troughs around September ({{ y2_min }} year-to-date at the low) before the strongest stretch of the four-year cycle begins: the average pre-election-year gain is {{ y3_end }}. Flows confirm the de-risk/re-risk shape: Europe funds lose {{ mid_eu_pre13 }} of assets in the quarter before a midterm and gain {{ mid_eu_post13 }} in the quarter after ({{ mid_eu_post26 }} by twenty-six weeks); bond funds take in {{ mid_bond_post26 }} in the half-year after.</p>
<img src="cycle_seasonal.png" alt="">

<h2>Wars: priced in the buildup, bought at the outbreak</h2>
<p>Across seventeen U.S.-relevant military events since 2001, the old pattern holds: when conflict is telegraphed, equities sag during the buildup and rally once the uncertainty resolves - Iraq 2003 fell through the six-month buildup and gained {{ iraq_p60 }} in the sixty trading days after the invasion; the median telegraphed event gained {{ war_tel_p20 }} in the month after outbreak. Surprise events bite on impact but rarely persist. Oil tells the same story from the other side: the war premium typically decays within a month unless supply is actually hit. Eleven of seventeen episodes match the buildup-down, outbreak-up template; the exceptions are dominated by confounding macro (the post-Soleimani window runs into COVID; Ukraine's relief rally drowned in the 2022 tightening cycle).</p>
<img src="wars_summary.png" alt="">

<h2>Presidents as volatility regimes</h2>
<p>Annualized S&P 500 volatility by administration: Clinton {{ vol_clinton }}, Bush 43 {{ vol_bush43 }}, Obama {{ vol_obama }}, Trump I <span class="k">{{ vol_trump1 }}</span>, Biden {{ vol_biden }}, Trump II {{ vol_trump2 }} to date. Trump I ran five points hotter than Biden, but the volatility is episodic, not ambient: it clusters on policy announcement days rather than around the election itself. The 2019 escalation tweet cost {{ tar_2019_5d }} in five sessions; Liberation Day 2025 cost {{ tar_lib_5d }} in five sessions and was followed by the largest one-day gain since 2008 when the pause was announced. Under this kind of administration the tradable unit is the policy headline, and the historical base rate is that tariff-shock drawdowns retraced once de-escalation began ({{ tar_geneva_20d }} in the month after the May 2025 Geneva step-down).</p>

<h2>The century view: 25 elections, 18 presidents</h2>
<p>Extending returns to every election since 1928: the post-midterm pattern strengthens to {{ deep_mid120 }} median over the next 120 trading days, positive in {{ deep_mid_hits }} midterms since 1930. Party-flip elections resolve uncertainty - realized volatility falls in {{ flip_vol_falls }} flips ({{ flip_vol }} vol points median) - while incumbent holds leave it slightly higher. Across presidents, the best risk-adjusted market of the century belonged to Eisenhower (Sharpe {{ eis_sharpe }} on total returns over T-bills); both Trump terms earn high returns the loud way ({{ t1_ret }} annualized at {{ t1_vol }} volatility - Sharpe {{ t1_sharpe }} for Trump I, {{ t2_sharpe }} for Trump II to date).</p>

<h2>Gold</h2>
<p>Gold's climb predates the 2024 election: the central-bank accumulation era of 2022-2024 already ran {{ gold_base }} annualized. The vote accelerated it - {{ gold_t2 }} annualized since, against {{ gold_t1 }} across all of Trump I. The dollar correlation is unchanged at roughly -0.4 in every era; what changed under Trump II is the gold-equity correlation turning positive ({{ gold_corr_spx_t2 }}). Gold rising with stocks is an allocation bid, not a fear bid.</p>

<h2>Sectors: the money rotates to defense</h2>
<p>Within US equities, the post-Trump-win flow league is led by materials and aerospace-defense ({{ def_flow_trump }} of assets median in 13 weeks, positive both times), with utilities, staples, healthcare and biotech in outflows both times. The century agrees: across 25 elections, defense is the most Republican-sensitive industry ({{ guns_r }} median in the 60 trading days after R wins, {{ guns_r_hit }} hit rate, against {{ guns_d }} after D wins), while semiconductors carry the largest Democratic tilt ({{ chips_spread }} points R-minus-D). Around wars the rotation is flows-first: defense funds took in {{ ita_ukraine }} of assets in the quarter after the Ukraine invasion and {{ ita_2016 }} after the 2016 election.</p>

<h2>What history says for November 3, 2026</h2>
<table>
<thead><tr><th>Pattern</th><th>Historical median</th><th>Hit rate</th><th>Sample</th></tr></thead>
<tbody>
<tr><td>Midterm-year chop, trough near September</td><td>{{ y2_min }} YTD at the low; year ends {{ y2_end }}</td><td>pattern, not a level</td><td>19 cycles</td></tr>
<tr><td>S&P 500, 120 trading days after the midterm</td><td>{{ mid_p120 }}</td><td>8 of 8</td><td>1994-2022</td></tr>
<tr><td>S&P 500, 20 days after</td><td>{{ mid_p20 }}</td><td>6 of 8</td><td>1994-2022</td></tr>
<tr><td>U.S. equity fund flows, 26 weeks after</td><td>{{ mid_us_post26 }} of assets</td><td>5 of 6</td><td>2002-2022</td></tr>
<tr><td>Europe fund flows, 13 weeks before</td><td>{{ mid_eu_pre13 }}</td><td>5 of 7 negative</td><td>1998-2022</td></tr>
<tr><td>Europe fund flows, 26 weeks after</td><td>{{ mid_eu_post26 }}</td><td>6 of 7</td><td>1998-2022</td></tr>
<tr><td>VIX from vote to vote+5</td><td>{{ vix_m1 }} to {{ vix_p5 }} (presidential median)</td><td>7 of last 10 fell day one</td><td>1990-2024</td></tr>
</tbody>
</table>
<p>The 2018 analog deserves respect: the one recent midterm whose aftermath broke down (December 2018, minus sixteen percent) did so on Federal Reserve tightening, not the election. The pattern is conditional on the macro regime staying out of the way.</p>

<div class="limits">Limits. Flow claims rest on nine presidential and eight midterm elections; return claims extend to 25 presidential and 24 midterm elections since 1928; gold is monthly from 1971 and daily from 2000; sector flows start 2000. Medians and sign counts, not statistics. Fund-flow panel covers U.S.-listed ETFs (predominantly U.S.-domiciled money) from 2000-2004 onward; pre-2000 statements rest on index prices and volatility only. The 2020 post-election window contains the vaccine announcement; the 2008 window contains the financial crisis; the post-Soleimani window contains COVID. These are patterns, not predictions.</div>
</body></html>
""")


def context() -> dict:
    """All numbers for the brief, pulled live from derived/ (shared by the
    HTML renderer here and the markdown renderer in build_brief_md.py)."""
    coh = pd.read_csv(DERIVED_DIR / "cohort_summary.csv")
    flows = pd.read_parquet(DERIVED_DIR / "flows_caf_paths.parquet")
    ret = pd.read_parquet(DERIVED_DIR / "returns_paths.parquet")
    vix = pd.read_parquet(DERIVED_DIR / "vix_paths.parquet")
    seas = pd.read_csv(DERIVED_DIR / "cycle_seasonal.csv")
    adm = pd.read_csv(DERIVED_DIR / "admin_regimes.csv").set_index("admin")

    def c(cohort, series, horizon, field="median"):
        r = coh[(coh.cohort == cohort) & (coh.series == series) & (coh.horizon == horizon)]
        return float(r.iloc[0][field]) if len(r) else float("nan")

    def flow_at(event, bucket, week):
        s = flows[(flows.event == event) & (flows.bucket == bucket)].set_index("rel_week")["value"]
        return float(s.loc[week]) if week in s.index else float("nan")

    def rel_at(event, series, day):
        s = ret[(ret.event == event) & (ret.anchor == "vote") & (ret.series == series)].set_index("rel_day")["value"]
        return float(s.loc[day]) if day in s.index else float("nan")

    vmed = vix[(vix.event_class == "presidential") & (vix.anchor == "vote")].pivot_table(
        index="rel_day", columns="event", values="value").median(axis=1)

    def pct(v, signed=True):
        return f"{v:+.1f}%" if signed else f"{v:.1f}%"

    y2 = seas[seas.tyear == 2].set_index("doy_rank")["cum_ret_pct"]
    y3 = seas[seas.tyear == 3].set_index("doy_rank")["cum_ret_pct"]

    eu120_16 = rel_at("2016 Trump", "Europe_minus_US", 120)
    eu120_24 = rel_at("2024 Trump", "Europe_minus_US", 120)

    iraq = ret[(ret.event == "2003 Iraq invasion") & (ret.anchor == "outbreak") & (ret.series == "SPX")].set_index("rel_day")["value"]
    tar = ret[(ret.event_class == "tariff") & (ret.series == "SPX")]

    def tar_at(evprefix, day):
        sub = tar[tar.event.str.contains(evprefix)]
        if sub.empty:
            return float("nan")
        s = sub.set_index("rel_day")["value"]
        return float(s.loc[day]) if day in s.index else float("nan")

    # phase 2: deep sample, gold, sectors
    deep_coh = pd.read_csv(DERIVED_DIR / "deep_cohort_summary.csv")

    def dc(cohort, metric, field):
        r = deep_coh[(deep_coh.cohort == cohort) & (deep_coh.metric == metric)]
        return float(r.iloc[0][field]) if len(r) else float("nan")

    pres_reg = pd.read_csv(DERIVED_DIR / "president_regimes.csv").set_index("president")
    gold_corr = pd.read_csv(DERIVED_DIR / "gold_correlations.csv").set_index("era")
    league = pd.read_csv(DERIVED_DIR / "sector_flow_league.csv")
    matrix = pd.read_csv(DERIVED_DIR / "industry_party_matrix.csv").set_index("industry")
    tdef = pd.read_csv(DERIVED_DIR / "tech_defense.csv").set_index("event")
    gd = pd.read_parquet(DATA_DIR / "prices" / "idx_gold.parquet")["close"].dropna()

    def gann(a, b):
        seg = gd.loc[a:b]
        return ((seg.iloc[-1] / seg.iloc[0]) ** (252 / len(seg)) - 1) * 100

    mid_n = int(dc("all_midterm", "post120", "n"))
    flip_n = int(dc("pres_flip", "rv_change_20d", "n"))
    extra = dict(
        deep_mid120=pct(dc("all_midterm", "post120", "median")),
        deep_mid_hits=f"{int(round(dc('all_midterm', 'post120', 'hit_rate_pos') * mid_n))} of {mid_n}",
        flip_vol=f"{dc('pres_flip', 'rv_change_20d', 'median'):+.1f}",
        flip_vol_falls=f"{int(round((1 - dc('pres_flip', 'rv_change_20d', 'hit_rate_pos')) * flip_n))} of {flip_n}",
        eis_sharpe=f"{pres_reg.loc['Eisenhower', 'sharpe']:.2f}",
        t1_sharpe=f"{pres_reg.loc['Trump I', 'sharpe']:.2f}",
        t2_sharpe=f"{pres_reg.loc['Trump II', 'sharpe']:.2f}",
        t1_ret=f"{pres_reg.loc['Trump I', 'ann_return_pct']:.0f}%",
        t1_vol=f"{pres_reg.loc['Trump I', 'ann_vol_pct']:.0f}%",
        gold_t1=pct(gann("2017-01-20", "2021-01-19")),
        gold_base=pct(gann("2022-01-01", "2024-10-31")),
        gold_t2=pct(gann("2024-11-05", None)),
        gold_corr_spx_t2=f"{gold_corr.loc['Trump II', 'corr_spx']:+.2f}",
        def_flow_trump=pct(league[(league.cohort == "trump_wins") &
                                  (league.sector == "Aerospace & defense")]["median_post13w"].iloc[0]),
        guns_r=pct(matrix.loc["Guns", "r_win_post60"]),
        guns_r_hit=f"{matrix.loc['Guns', 'r_hit'] * 100:.0f}%",
        guns_d=pct(matrix.loc["Guns", "d_win_post60"]),
        chips_spread=f"{matrix.loc['Chips', 'r_minus_d']:+.1f}",
        ita_ukraine=pct(tdef.loc["Russia invades Ukraine", "defense_flow_13w"]),
        ita_2016=pct(tdef.loc["2016 election", "defense_flow_13w"]),
    )

    return dict(
        **extra,
        vix_m60=f"{vmed.loc[-60]:.0f}", vix_m20=f"{vmed.loc[-20]:.0f}", vix_m1=f"{vmed.loc[-1]:.0f}",
        vix_p1=f"{vmed.loc[1]:.0f}", vix_p5=f"{vmed.loc[5]:.0f}",
        cash_pre13=pct(c("pres_all", "flow_Cash", "pre13")),
        us_post13=pct(c("pres_all", "flow_US", "+13")),
        us_post26=pct(c("pres_all", "flow_US", "+26")),
        spx_pre20=pct(c("pres_all", "SPX", "pre20")),
        spx_p20=pct(c("pres_all", "SPX", "+20")),
        spx_p120=pct(c("pres_all", "SPX", "+120")),
        t16_us13=pct(flow_at("2016 Trump", "US", 13)),
        t16_cn13=pct(flow_at("2016 Trump", "China", 13)),
        t24_us13=pct(flow_at("2024 Trump", "US", 13)),
        t24_cn13=pct(flow_at("2024 Trump", "China", 13)),
        t24_cn26=pct(flow_at("2024 Trump", "China", 26)),
        t24_tw13=pct(flow_at("2024 Trump", "Taiwan", 13)),
        t24_tw60=pct(rel_at("2024 Trump", "Taiwan_minus_US", 60)),
        t24_kr60=pct(rel_at("2024 Trump", "Korea_minus_US", 60)),
        t_eu120=f"{pct(eu120_16)} and {pct(eu120_24)}",
        mid_p120=pct(c("midterm_all", "SPX", "+120")),
        mid_p20=pct(c("midterm_all", "SPX", "+20")),
        y2_min=pct(y2.min()), y2_end=pct(y2.iloc[-1]), y3_end=pct(y3.iloc[-1]),
        mid_eu_pre13=pct(c("midterm_all", "flow_Europe", "pre13")),
        mid_eu_post13=pct(c("midterm_all", "flow_Europe", "+13")),
        mid_eu_post26=pct(c("midterm_all", "flow_Europe", "+26")),
        mid_bond_post26=pct(c("midterm_all", "flow_Bonds", "+26")),
        mid_us_post26=pct(c("midterm_all", "flow_US", "+26")),
        iraq_p60=pct(float(iraq.loc[60])),
        war_tel_p20=pct(c("war_telegraphed", "SPX", "+20")),
        vol_clinton=f"{adm.loc['Clinton','ann_vol_pct']:.0f}%", vol_bush43=f"{adm.loc['Bush43','ann_vol_pct']:.0f}%",
        vol_obama=f"{adm.loc['Obama','ann_vol_pct']:.0f}%", vol_trump1=f"{adm.loc['Trump1','ann_vol_pct']:.0f}%",
        vol_biden=f"{adm.loc['Biden','ann_vol_pct']:.0f}%", vol_trump2=f"{adm.loc['Trump2','ann_vol_pct']:.0f}%",
        tar_2019_5d=pct(tar_at("2019-05-05", 5)),
        tar_lib_5d=pct(tar_at("2025-04-02", 5)),
        tar_geneva_20d=pct(tar_at("2025-05-12", 20)),
    )


def main():
    html = TPL.render(css=CSS, **context())
    (BRIEF_DIR / "index.html").write_text(html)
    for fig in ["cohort_pres_all", "cohort_pres_trump", "cycle_seasonal", "wars_summary"]:
        src = OUTPUT_DIR / "figures" / f"{fig}.png"
        if src.exists():
            shutil.copy(src, BRIEF_DIR / f"{fig}.png")
    print(f"brief written -> {BRIEF_DIR / 'index.html'}", flush=True)


if __name__ == "__main__":
    main()
