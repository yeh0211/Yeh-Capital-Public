# 02 — Is IPO-anchored VWAP a "real" level? 202 semiconductors, US + Asia

**Question.** A common technical claim: for a recently-IPO'd stock, a VWAP *anchored to the first trading day* marks a more meaningful support/resistance level than a generic anchor. Does it — and do classical EMA crossovers carry standalone edge in this universe?

**Finding.** Both priors were falsified. IPO-anchored reclaims bounced 55.6% vs 44.8% for a 10-year anchor — but with only n=27 the **95% confidence intervals overlap heavily**, so the honest verdict is "unproven at this sample," not "confirmed." And across **57,136 EMA crossovers in 48 cells, not one** had a 95%-CI lower bound above 50%; the golden cross bounced just **36%** (vs the 55–65% folklore).

> Research / backtested. 202 semiconductors (124 US + 78 Asia), 463,621 daily bars, ~5 years; bootstrap 95% CIs, Bonferroni considered. No live capital, no costs.

## Data & method

- **Universe:** 202 tickers — 36 *true-IPO* names (first listed post-2016: CRWD, DDOG, NET, SNOW, PLTR, ARM, ALAB …) vs 166 *long-anchor* names (pre-2016).
- **Reclaim event:** a high-volume, strong-close day closing back above the anchored VWAP after 60+ days below (152 events).
- **EMA stack** (0–6 score) and **57,136 crossover events** across 8 cross-types × sector clusters. **Outcome:** 20-day bounce rate; bootstrap 95% CIs; Bonferroni for the 48-cell grid.

## Claim 1 — IPO anchor does not beat a generic anchor

![Anchor-type bounce comparison](anchor-type-bounce.png)

| Anchor type | n | 20d bounce | 95% CI | mean 30d return |
|---|---:|---:|---|---:|
| True-IPO | 27 | 55.6% | [37.0, 74.1] | +26.2% |
| 10-year | 125 | 44.8% | [36.8, 53.6] | +7.5% |

True-IPO reclaims *look* better (+10.8pp bounce, +18.7pp return) — but the CIs overlap heavily and the lower bounds nearly coincide. With n=27 I cannot reject that the two are the same distribution; the return gap is driven by a few AI-cycle winners.

## Claim 2 — The "trend-confirmation filter" was already baked in

Filtering reclaims to EMA-stack ≥ 4 was meant to lift the hit rate — but **all 152 reclaim events already had stack ≥ 4**, because the reclaim definition (high volume + strong close + back above VWAP) mechanically forces price above its short EMAs. The filter added nothing because it was implicit in the event.

## Claim 3 — Classical EMA crossovers carry no standalone edge here

![Best crossover signal per cluster](crossover-by-cluster.png)

Across 57,136 crossovers and 48 (cross-type × cluster) cells, **not one cell has a 95%-CI lower bound above 50%**; the best tops out at 37–42%. The **golden cross (50×200 up) bounced 36.3%** in the AI-capex cluster (n=832) — far below its 55–65% reputation. Several *down*-crosses outperformed *up*-crosses on the 20-day window, consistent with short-term mean-reversion after sharp breakdowns, not trend-following.

## The answer, in the data

**Q: Is IPO-anchored VWAP a real edge, and does the golden cross work here?**
**A: No on both.** The anchor is unproven at n=27 (CIs overlap); the golden cross underperformed badly.

| Signal | n | 20d bounce | Verdict |
|---|---:|---:|---|
| True-IPO anchor reclaim | 27 | 55.6% | CI [37,74] overlaps 10y [37,54] → unproven |
| 10-year anchor reclaim | 125 | 44.8% | baseline |
| Golden cross (AI-capex) | 832 | 36.3% | far below 55–65% folklore |

## Caveats

Small true-IPO sample (n=27) and multiple comparisons (48 cells) — treat any single positive as a lead. Survivorship / regime bias (the true-IPO cohort rode the AI cycle). No costs; bounce rates are gross. Daily bars and a close-vs-open side proxy are coarse. The right move on the true-IPO cohort is to re-test in 1–2 years as it grows, not to trade it now.

## References

- Sullivan, Timmermann & White (1999). *Data-snooping, technical trading rule performance, and the bootstrap.* Journal of Finance — why "obvious" rules vanish out-of-sample.
- Brock, Lakonishok & LeBaron (1992). *Simple technical trading rules and the stochastic properties of stock returns.* Journal of Finance.
- Community: r/Daytrading and r/TechnicalAnalysis on anchored-VWAP and golden-cross belief — the priors this note tests and falsifies.
