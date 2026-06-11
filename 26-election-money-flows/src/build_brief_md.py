"""Markdown rendering of the synthesis brief, for venues that render .md
natively (the public GitHub repo). Same numbers as the HTML brief via
build_brief.context(); figures referenced from the same directory."""
from jinja2 import Template

from build_brief import BRIEF_DIR, context

TPL_MD = Template("""# Money around U.S. elections

*Where it goes before the vote, after the result, under each kind of winner, and when the shooting starts. Every U.S. presidential election and midterm 1992-2024, every U.S.-relevant military action 2001-2025, measured in fund flows, returns, and volatility.*

June 2026 - the dossier set with per-event detail accompanies this note.

## The election cycle in one motion

Investors hedge the event, not the outcome. Implied volatility builds for roughly two months into a presidential vote (median VIX {{ vix_m20 }} twenty days out against {{ vix_m60 }} sixty days out) and collapses within days of a result, whoever wins: {{ vix_p1 }} the day after, {{ vix_p5 }} a week after. Cash-proxy funds absorb a median {{ cash_pre13 }} of assets in the quarter before the vote. Then the re-risking: U.S. equity funds take in a median **{{ us_post13 }} of assets in the thirteen weeks after the vote** - positive after every election in the sample - and {{ us_post26 }} by twenty-six weeks. The S&P 500's median path: {{ spx_pre20 }} in the month before, **{{ spx_p20 }} in the month after, {{ spx_p120 }} over six months**.

![All presidential elections](cohort_pres_all.png)

## Does the money leave America? Mostly no - it leaves China

The popular narrative says capital flees the U.S. when the result displeases it. The flow data say otherwise: after a typical election, U.S. and foreign-region funds get inflows together - allocation is not a zero-sum exit. What moves is the relative line, and the clean repeated case is a Trump win. In the thirteen weeks after November 2016, U.S. equity funds gained {{ t16_us13 }} of assets while China funds lost **{{ t16_cn13 }}**; after November 2024, U.S. funds gained {{ t24_us13 }} while China funds lost **{{ t24_cn13 }}**, reaching {{ t24_cn26 }} by half a year. Taiwan funds saw {{ t24_tw13 }} over the same 2024 window, and Taiwan underperformed U.S. equities by {{ t24_tw60 }} in the first sixty trading days, Korea by {{ t24_kr60 }}. Money did not leave America after Trump won; it left the tariff targets.

The reversal comes later and is just as regular. By six months after both Trump wins, Europe-relative returns had flipped positive ({{ t_eu120 }} versus U.S. at 120 trading days, both episodes) and in 2025 the rotation became flows: Europe funds took in roughly twenty percent of assets across February-April 2025 while U.S. funds bled through the tariff quarter. The first quarter after a Trump win belongs to America; the second leg has twice belonged to everyone else.

![Trump cohort](cohort_pres_trump.png)

## Midterms are the better signal

The strongest, most repeatable pattern in the dataset is not the presidential race. After midterm elections the S&P 500's median move is {{ mid_p120 }} over the next 120 trading days - **positive after all eight midterms since 1994**. The average midterm year since 1950 troughs around September ({{ y2_min }} year-to-date at the low) before the strongest stretch of the four-year cycle begins: the average pre-election-year gain is {{ y3_end }}. Flows confirm the de-risk/re-risk shape: Europe funds lose {{ mid_eu_pre13 }} of assets in the quarter before a midterm and gain {{ mid_eu_post13 }} in the quarter after ({{ mid_eu_post26 }} by twenty-six weeks); bond funds take in {{ mid_bond_post26 }} in the half-year after.

![Cycle seasonality](cycle_seasonal.png)

## Wars: priced in the buildup, bought at the outbreak

Across seventeen U.S.-relevant military events since 2001, the old pattern holds: when conflict is telegraphed, equities sag during the buildup and rally once the uncertainty resolves - Iraq 2003 fell through the six-month buildup and gained {{ iraq_p60 }} in the sixty trading days after the invasion; the median telegraphed event gained {{ war_tel_p20 }} in the month after outbreak. Surprise events bite on impact but rarely persist. Oil tells the same story from the other side: the war premium typically decays within a month unless supply is actually hit. Eleven of seventeen episodes match the buildup-down, outbreak-up template; the exceptions are dominated by confounding macro (the post-Soleimani window runs into COVID; Ukraine's relief rally drowned in the 2022 tightening cycle).

![Wars summary](wars_summary.png)

## Presidents as volatility regimes

Annualized S&P 500 volatility by administration: Clinton {{ vol_clinton }}, Bush 43 {{ vol_bush43 }}, Obama {{ vol_obama }}, Trump I **{{ vol_trump1 }}**, Biden {{ vol_biden }}, Trump II {{ vol_trump2 }} to date. Trump I ran five points hotter than Biden, but the volatility is episodic, not ambient: it clusters on policy announcement days rather than around the election itself. The 2019 escalation tweet cost {{ tar_2019_5d }} in five sessions; Liberation Day 2025 cost {{ tar_lib_5d }} in five sessions and was followed by the largest one-day gain since 2008 when the pause was announced. Under this kind of administration the tradable unit is the policy headline, and the historical base rate is that tariff-shock drawdowns retraced once de-escalation began ({{ tar_geneva_20d }} in the month after the May 2025 Geneva step-down).

## The century view: 25 elections, 18 presidents

Extending returns to every election since 1928: the post-midterm pattern strengthens to {{ deep_mid120 }} median over the next 120 trading days, positive in {{ deep_mid_hits }} midterms since 1930. Party-flip elections resolve uncertainty - realized volatility falls in {{ flip_vol_falls }} flips ({{ flip_vol }} vol points median) - while incumbent holds leave it slightly higher. Across presidents, the best risk-adjusted market of the century belonged to Eisenhower (Sharpe {{ eis_sharpe }} on total returns over T-bills); both Trump terms earn high returns the loud way ({{ t1_ret }} annualized at {{ t1_vol }} volatility - Sharpe {{ t1_sharpe }} for Trump I, {{ t2_sharpe }} for Trump II to date).

## Gold

Gold's climb predates the 2024 election: the central-bank accumulation era of 2022-2024 already ran {{ gold_base }} annualized. The vote accelerated it - {{ gold_t2 }} annualized since, against {{ gold_t1 }} across all of Trump I. The dollar correlation is unchanged at roughly -0.4 in every era; what changed under Trump II is the gold-equity correlation turning positive ({{ gold_corr_spx_t2 }}). Gold rising with stocks is an allocation bid, not a fear bid.

## Sectors: the money rotates to defense

Within US equities, the post-Trump-win flow league is led by materials and aerospace-defense ({{ def_flow_trump }} of assets median in 13 weeks, positive both times), with utilities, staples, healthcare and biotech in outflows both times. The century agrees: across 25 elections, defense is the most Republican-sensitive industry ({{ guns_r }} median in the 60 trading days after R wins, {{ guns_r_hit }} hit rate, against {{ guns_d }} after D wins), while semiconductors carry the largest Democratic tilt ({{ chips_spread }} points R-minus-D). Around wars the rotation is flows-first: defense funds took in {{ ita_ukraine }} of assets in the quarter after the Ukraine invasion and {{ ita_2016 }} after the 2016 election.

## What history says for November 3, 2026

| Pattern | Historical median | Hit rate | Sample |
|---|---|---|---|
| Midterm-year chop, trough near September | {{ y2_min }} YTD at the low; year ends {{ y2_end }} | pattern, not a level | 19 cycles |
| S&P 500, 120 trading days after the midterm | {{ mid_p120 }} | 8 of 8 | 1994-2022 |
| S&P 500, 20 days after | {{ mid_p20 }} | 6 of 8 | 1994-2022 |
| U.S. equity fund flows, 26 weeks after | {{ mid_us_post26 }} of assets | 5 of 6 | 2002-2022 |
| Europe fund flows, 13 weeks before | {{ mid_eu_pre13 }} | 5 of 7 negative | 1998-2022 |
| Europe fund flows, 26 weeks after | {{ mid_eu_post26 }} | 6 of 7 | 1998-2022 |
| VIX from vote to vote+5 | {{ vix_m1 }} to {{ vix_p5 }} (presidential median) | fell day-after in 7 of last 10 | 1990-2024 |

The 2018 analog deserves respect: the one recent midterm whose aftermath broke down (December 2018, minus sixteen percent) did so on Federal Reserve tightening, not the election. The pattern is conditional on the macro regime staying out of the way.

---

*Limits. Flow claims rest on nine presidential and eight midterm elections; return claims extend to 25 presidential and 24 midterm elections since 1928; gold is monthly from 1971 and daily from 2000; sector flows start 2000. Medians and sign counts, not statistics. Fund-flow panel covers U.S.-listed ETFs (predominantly U.S.-domiciled money) from 2000-2004 onward; pre-2000 statements rest on index prices and volatility only. The 2020 post-election window contains the vaccine announcement; the 2008 window contains the financial crisis; the post-Soleimani window contains COVID. These are patterns, not predictions.*
""")


def main():
    md = TPL_MD.render(**context())
    out = BRIEF_DIR / "README.md"
    out.write_text(md)
    print(f"markdown brief -> {out}", flush=True)


if __name__ == "__main__":
    main()
