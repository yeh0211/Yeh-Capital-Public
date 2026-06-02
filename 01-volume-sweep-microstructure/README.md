# Do cross-ticker volume sweeps predict next-day returns in semiconductors?

**A small in-sample signal, tested to destruction out-of-sample.**

*Hsin Cheng Yeh · independent research · 2026*

---

## Question

If several liquid names in the same sector all print an abnormal-volume bar at the *same* 15-minute timestamp — a "sweep" — does that cluster of activity carry information about the basket's **next-day** return?

I first saw a hint of this in a 14-day pilot on Finviz data: a "BUY sweep" basket returned **+1.06%** the next day (n=34, 71% win, p≈0.002). That looked strong. The point of this study was to find out whether it was *real* or just a small-sample mirage.

## Data & universe

- **Basket:** 7 US-listed semiconductors — NVDA, TSM, AVGO, AMD, ASML, AMAT, KLAC.
- **Bars:** 15-minute OHLCV, regular hours only (09:30–16:00 ET).
- **Period:** ~5 years (~250× the *raw data* of the 14-day pilot; ~12× as many sweep *events* once detected).

## Method

1. For each ticker/bar, compute a rolling **volume Z-score** over a 60-bar (~1 trading day) window.
2. A bar **qualifies** if Z ≥ 3.0 (top ~0.1% of bars by volume). Its **side** = sign(close − open).
3. Group qualifying bars by timestamp across the basket and classify the **sweep**:
   - `BUY_SWEEP` — ≥2 qualifying *buy* bars at the same timestamp
   - `SELL_SWEEP` — ≥2 qualifying *sell* bars
   - `MIXED` — qualifying bars on *both* sides
   - `SINGLE` — exactly one qualifying bar
4. For each sweep, measure the **next-day basket return** (mean across the 7 names).
5. Report mean/median next-day return, win rate, and a two-sided t-test per sweep type.

## Result

![Next-day return by sweep type](fwd-return-by-sweep-type.png)

| Sweep type | n | Mean next-day | Win rate | p-value |
|---|---:|---:|---:|---:|
| SINGLE | 649 | +0.06% | 51.4% | 0.51 |
| SELL_SWEEP | 287 | +0.04% | 54.4% | 0.77 |
| BUY_SWEEP | 393 | +0.20% | 53.4% | **0.081** |
| MIXED | 92 | +0.65% | 60.4% | **0.008** |

**The headline pilot signal did not survive.** The BUY-sweep effect collapsed from **+1.06% → +0.20%** and lost significance (p≈0.08) once tested on a sample ~12× larger. The original 71% win rate regressed to 53% — barely a coin-flip edge. On this evidence, the 14-day result was **mostly small-sample noise**, exactly the kind of false positive that survives only because nobody re-tested it at scale.

**An unplanned finding did survive:** `MIXED` sweeps — timestamps where the basket prints abnormal volume on *both* sides at once — returned **+0.65%** the next day (n=92, 60% win, **p≈0.008**). That is consistent with a *contested-tape → continuation* read: simultaneous two-sided institutional pressure resolving in the basket's favour the following session. It is one significant result among four tests, so it needs its own out-of-sample confirmation before I'd weight it — but it's the thread worth pulling next.

## What I take from it

- **Out-of-sample testing is not optional.** A p=0.002 result on 34 observations told me almost nothing; the same idea on 393 observations told me the truth.
- **Report the null.** The interesting output of this study is that my own initial hypothesis was wrong. Logging that honestly is the only way the research compounds instead of accumulating false positives.
- **The surviving effect (MIXED) is a hypothesis, not a strategy** — next step is a separate hold-out window and a transaction-cost / slippage haircut before it means anything tradable.

## Caveats

- Backtest only. No live capital, no execution; next-day *basket* returns ignore transaction costs, slippage, and borrow.
- Multiple comparisons (4 sweep types) — the MIXED p-value is not corrected for multiplicity; treat as a lead, not a conclusion.
- Single sector, 7 names — findings may not generalise beyond large-cap semiconductors.
- 15-minute bars; intrabar timing and the close-vs-open side proxy are coarse.

---

*Part of a series of independent research notes. The data pipeline that produced these results is operated privately; this note publishes the method and findings only.*
