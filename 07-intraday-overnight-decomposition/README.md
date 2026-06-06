# 07 — Intraday decision-time: you can describe the close, not profit from it

**Question.** By late morning, how often does the direction of a high-beta semi/AI name's move-so-far already match its eventual close — and can you trade on it? **Finding.** By 11:30 ET the morning move calls the close sign 80% of the time, but that hit-rate is a mechanical artifact of overlap; the only part you could still act on — the non-overlapping rest-of-day leg — is a sub-cost coin flip. Describe, don't trade.

> Research / backtested. No live capital, no audited track record. The 80% "decision-time" hit-rate is descriptive, not a signal — it is contaminated by the morning leg sitting inside the full-day return; the only honest profit test is the rest-of-day leg, and it is null.

## Data & method

- **Universe:** 114 high-beta AI/semiconductor tickers, 5-minute bars, regular session only (open bar to close bar).
- **Window:** 2021-04-30 to 2026-05-20, 1,260 trading days, ~116k ticker-days. Returns winsorized at +/-50%.
- **Two deliberately separated tests.** (1) *Description* — at each cutoff (10:00 to 13:00 ET) how often does the sign of open→cutoff match the sign of open→close. (2) *Profit* — trade the morning direction at the cutoff and hold to close, scoring only the **non-overlapping** cutoff→close leg (the sole contamination-free statistic).
- **Validation.** Day-block bootstrap 95% CIs **averaged over 5 seeds** (the prior single-seed flag was a seed artifact), per-year breakdown, and an in-sample (2021-2023) / out-of-sample (2024-2026) walk-forward.

## Claim 1 — You CAN describe the close early (but it's mechanical)

By 11:30 ET the morning move's sign matches the eventual close sign **80.3%** of the time (95% CI [79.7%, 81.0%]), climbing to 84.7% by 13:00. This is real but **mechanical**: the later the cutoff, the more of the day is already realized inside the open→close return being compared against (the overlap trap). It is a measurement of where the day is heading, not a tradable edge.

| cutoff (ET) | n | hit-rate | edge vs coin-flip | 95% CI (day-block) | robust? |
|---|---:|:---:|:---:|:---:|:---:|
| 10:00 | 115,317 | 0.7124 | +0.2124 | [0.7050, 0.7195] | yes |
| 10:30 | 115,414 | 0.7556 | +0.2556 | [0.7484, 0.7624] | yes |
| 11:00 | 115,544 | 0.7822 | +0.2822 | [0.7756, 0.7886] | yes |
| **11:30** | **115,552** | **0.8035** | **+0.3035** | **[0.7973, 0.8097]** | **yes** |
| 12:00 | 115,554 | 0.8191 | +0.3191 | [0.8132, 0.8251] | yes |
| 13:00 | 115,587 | 0.8474 | +0.3474 | [0.8417, 0.8529] | yes |

The CIs are tight and well above the coin-flip line — but "significant" here is significant-because-mechanical, not significant-because-tradable. (Counts differ slightly from the rest-of-day profit tables below — e.g. 115,552 vs 116,033 at 11:30 — because the two tests apply different non-null filters: the description leg needs both an open→cutoff and an open→close sign, while the profit leg only needs a non-null non-overlapping cutoff→close return.)

![Decision-time curve: how early the morning move calls the close](fig_decision_time_curve.png)

## Claim 2 — You CANNOT profit (the honest test is a coin flip)

Trade the 11:30 morning direction, hold to close, and score the signed return on the **non-overlapping** 11:30→close leg: win-rate **50.4%** (95% CI [49.5%, 51.2%], straddles 0.50), mean signed return **+3.4 bp before costs** whose seed-averaged 95% CI runs **-0.1 bp to +7.0 bp** — the lower bound sits on zero. Both nulls (coin-flip win-rate, zero drift) live inside the interval. And a same-day enter-at-11:30 / exit-at-close round trip on these names costs more than 3 bp, so the rule is net-negative.

| metric | n | %positive (win) | median | mean | seed-avg 95% CI | robust? |
|---|---:|:---:|:---:|:---:|:---:|:---:|
| signed rest-of-day return (11:30→close) | 116,033 | 50.4% | +1.6 bp | +3.4 bp | mean [-0.1 bp, +7.0 bp]; win [49.5%, 51.2%] | **no — marginal, sub-cost** |

Run the same momentum rule at every cutoff and only the two earliest survive a robust CI — and only because they keep the longest rest-of-day window, at 5-6 bp gross, still below realistic frictions:

| cutoff | n | win | avg signed | seed-avg 95% CI | robust? |
|---|---:|:---:|:---:|:---:|:---:|
| 10:00 | 115,806 | 0.5027 | +5.6 bp | [+0.9, +10.4] bp | yes |
| 10:30 | 115,898 | 0.5057 | +4.6 bp | [+0.4, +9.1] bp | yes |
| 11:00 | 116,035 | 0.5018 | +3.1 bp | [-0.6, +6.8] bp | no |
| 11:30 | 116,033 | 0.5038 | +3.4 bp | [-0.1, +7.0] bp | no |
| 12:00 | 116,035 | 0.4974 | +1.4 bp | [-1.9, +4.7] bp | no |
| 13:00 | 116,070 | 0.4989 | +1.8 bp | [-1.4, +5.3] bp | no |

![Profitability of acting on the morning move, before costs — tiny and mostly inside noise](fig_restofday_profit.png)

## The answer, in the data

**Q: By late morning the day's close looks "decided" — can you trade on it?**
**A: Conditional, and the two halves point opposite ways.** You CAN describe the close — 80.3% by 11:30 — but that is a mechanical overlap artifact. You CANNOT profit: the non-overlapping rest-of-day leg is a 50.4% coin flip, +3.4 bp gross with a CI on zero, sub-cost, and its only positive year is 2022.

| Finding | Stat |
|---|---|
| Morning move calls the close (descriptive) | 80.3% by 11:30 ET, 84.7% by 13:00 — mechanical |
| Tradable rest-of-day leg (11:30→close) | win 50.4%, +3.4 bp gross, CI on zero |
| After costs | net-negative (round trip > 3 bp) |
| Edge concentration | 2022 wins 52.1%; every other year 48.9-50.2% |
| Walk-forward | IS 50.9% → OOS 49.9% (fails out-of-sample) |

## Caveats

- **Overlap trap.** The 80% hit-rate compares open→cutoff against open→close, which share the open→cutoff leg, so it mechanically rises toward 100% as the cutoff nears the close. The only contamination-free statistic is the non-overlapping rest-of-day leg — and that is a coin flip.
- **No transaction costs.** All numbers are gross; a same-day in-and-out round trip on these names costs more than 3 bp, making the 11:30 rule net-negative.
- **Single regime.** The razor-thin gross edge is carried almost entirely by 2022 (high-vol bear, win 52.1%); every other year is a coin flip, and it fails the out-of-sample walk-forward.
- **Seed fragility.** An earlier version printed "SIGNIFICANT" on the 11:30 leg off a single bootstrap seed whose CI lower bound landed at +1.3e-6 — a hair above zero. Averaging across 5 seeds, 4 of 5 put the lower bound below zero; corrected to a multi-seed averaged bootstrap reporting the fraction of seeds whose CI contains the null.
- **Universe.** 114 high-beta AI/semis only; intraday continuation in this cohort need not generalize to broad or low-beta equities. The signed (direction-following) test is drift-neutral by construction.

## References

- Gao, Han, Li & Zhou (2018). *Market intraday momentum.* JFE — the canonical intraday-momentum effect, documented in index futures.
- Lou, Polk & Skouras (2019). *A tug of war: overnight versus intraday returns.* JFE.
- Heston, Korajczyk & Sadka (2010). *Intraday return periodicity.* Journal of Finance.
- Community: r/algotrading on why naive intraday-momentum bots fail to replicate the index-futures result on single high-beta names.
