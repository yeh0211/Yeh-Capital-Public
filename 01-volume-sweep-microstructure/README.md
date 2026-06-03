# 01 — Do cross-ticker volume sweeps predict next-day semiconductor returns?

**Question.** If several liquid semiconductors all print an abnormal-volume bar at the *same* 15-minute timestamp — a "sweep" — does that cluster of activity carry information about the basket's **next-day** return?

**Finding.** Mostly no. A 14-day pilot's "BUY sweep" (+1.06%, n=34, 71% win, p≈0.002) collapsed to **+0.20% (p≈0.08)** once tested on a sample ~12× larger — small-sample noise. One *unplanned* result survived: **MIXED (two-sided) sweeps returned +0.65% next day (n=92, 60% win, p≈0.008)** — but it is one significant cell among four tests and needs out-of-sample confirmation before it means anything.

> Research / backtested. 7 US semiconductors, 15-minute bars, regular hours, ~5 years (~12× the sweep events of the 14-day pilot). No live capital, no execution costs.

## Data & method

- **Basket:** NVDA, TSM, AVGO, AMD, ASML, AMAT, KLAC.
- For each ticker/bar, a rolling **volume Z-score** (60-bar window); a bar **qualifies** if Z ≥ 3.0 (top ~0.1% by volume), with **side** = sign(close − open).
- Qualifying bars are grouped by timestamp and the **sweep** classified: `BUY_SWEEP` (≥2 buy), `SELL_SWEEP` (≥2 sell), `MIXED` (both sides), `SINGLE` (one). Outcome = next-day basket return (mean across the 7); two-sided t-test per type.

## Claim 1 — The headline pilot signal did not survive

The BUY-sweep effect collapsed from **+1.06% → +0.20%** and lost significance (p≈0.08) on a sample ~12× larger; the original 71% win rate regressed to 53%, barely a coin flip. The 14-day result was mostly small-sample noise — the kind of false positive that survives only because nobody re-tests it at scale.

![Next-day return by sweep type](fwd-return-by-sweep-type.png)

| Sweep type | n | Mean next-day | Win rate | p-value |
|---|---:|---:|---:|---:|
| SINGLE | 649 | +0.06% | 51.4% | 0.51 |
| SELL_SWEEP | 287 | +0.04% | 54.4% | 0.77 |
| BUY_SWEEP | 393 | +0.20% | 53.4% | 0.081 |
| MIXED | 92 | +0.65% | 60.4% | **0.008** |

## Claim 2 — One unplanned result survived: MIXED sweeps

Timestamps where the basket prints abnormal volume on *both* sides at once returned **+0.65%** the next day (n=92, 60% win, p≈0.008) — consistent with a *contested-tape → continuation* read: simultaneous two-sided institutional pressure resolving in the basket's favour the next session.

## Claim 3 — The honest next step (out-of-sample + costs)

MIXED is a hypothesis, not a strategy. Before it could carry weight it needs two things this study deliberately does not claim: **(1)** a separate out-of-sample window — it is one significant cell out of four tests and is not multiplicity-corrected; and **(2)** a transaction-cost / slippage / borrow haircut — a +0.65% next-day basket edge is thin once a round trip is deducted. Reported as the thread worth pulling next, not a result.

## The answer, in the data

**Q: Do cross-ticker volume sweeps predict the basket's next-day return?**
**A: No for the directional (BUY/SELL) sweeps** — they regress to a coin flip at scale. Only the two-sided **MIXED** cell is suggestive (+0.65%, p≈0.008) and remains unconfirmed out-of-sample.

## Caveats

Backtest only; next-day *basket* returns ignore transaction costs, slippage and borrow. Multiple comparisons (4 sweep types) — the MIXED p-value is not multiplicity-corrected. Single sector, 7 names — may not generalise. 15-minute bars and the close-vs-open side proxy are coarse.

## References

- Kyle, A. (1985). *Continuous auctions and insider trading.* Econometrica — informed order flow and price impact.
- Easley, López de Prado & O'Hara (2012). *Flow toxicity and liquidity in a high-frequency world* (VPIN). RFS.
- Community: r/algotrading on "unusual volume" / sweep signals that look strong in a short backtest and then vanish out-of-sample — the exact failure mode logged here.
