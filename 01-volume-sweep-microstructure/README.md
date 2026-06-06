# 01 — Volume-sweep microstructure: do cross-ticker volume sweeps predict next-day semiconductor returns?

The folk belief on a trading desk is simple: when a stock suddenly trades far more than usual, *somebody knows something*, and the price will keep moving their way. Scale it up — when **several** related chip stocks all light up with abnormal volume in the **same** fifteen minutes, that synchronized burst (a "sweep") feels like informed money tipping its hand, and the basket should drift in that direction tomorrow. This study takes that belief seriously, hardens the test the way a referee would, and shows the edge evaporates: once the statistics are done honestly, **a sweep day is just an ordinary day in the tape.**

**Question.** When several liquid semiconductors all print an abnormal-volume 15-minute bar at the *same* timestamp, does that burst carry information about the basket's **next-day** return — over and above being long the basket anyway?

**Why it matters.** If true, it is a cheap intraday entry signal for a sector book: wait for the sweep, take the next-day direction. If false, it is the textbook way drift gets mistaken for skill — and worth documenting as a null so the next person does not pay to re-learn it.

> Research / backtested. 7 US semiconductors, 15-minute bars, regular hours, 2021-04 to 2026-04. No live capital, no execution costs assumed unless stated. A clean null, reported as a null.

---

## Summary of results

- **Verdict: No.** No sweep type beats the basket's ordinary next-day drift once the inference is done properly. The honest result is a clean null.
- **The pilot oversold.** A 14-day pilot showed a strong "BUY sweep" edge (+1.06%, p≈0.002) and an apparently surviving two-sided "MIXED" edge (+0.65%, p≈0.008). Neither holds on the full ~5-year sample.
- **MIXED is the headline casualty.** Far from "surviving," on the full sample it is *negative* (−0.05%, dependence-adjusted p≈0.67), flips sign across thresholds, and is beaten by random same-names entry.
- **The spine:** strip out the double-counting (many sweeps share one next-day return) → correct for testing four types at once → benchmark against random entry, not zero → split out-of-sample → deduct costs. Every step shrinks the edge; the last steps erase it.
- **What's actually there is drift.** All sweep days average +0.166% next-day; all trading days average +0.163%. Identical to three decimals.
- **Direction of the lesson:** the apparent signal was the bull-market basket drifting up, plus a handful of large episodes — the signature of noise, not a stable edge.

---

## Theory and hypothesis

This sits in the **microstructure** literature — the study of how individual orders and trades move price, as opposed to fundamentals. Two canonical results motivate the test, and they pull in **opposite** directions on the key case, which is exactly why it is worth running.

- **Kyle (1985) — informed order flow moves price.** An informed trader splits a large order to hide it, so aggregate signed order flow ("net buying minus net selling") is itself informative, and price impact is roughly linear in that flow. A *synchronized* abnormal-volume burst across correlated names is a candidate proxy for informed, sector-wide flow. If the burst is one-sided — a **BUY sweep**, several names spiking on up-bars — Kyle predicts the information keeps getting impounded: a next-day drift in the flow's direction.
- **Easley, López de Prado & O'Hara (2012) — flow toxicity (VPIN).** When buy and sell volume both arrive in abnormal size at once, order flow is *toxic*: market-makers cannot tell who is informed, spreads widen, and the aftermath is dominated by noise and adverse selection rather than a clean direction. A *two-sided* (**MIXED**) sweep — one chip spiking up while another spikes down in the same bar — is the picture of high toxicity. This reading predicts the next-day response is **closer to noise**, not a reliable continuation.

So the two priors disagree on MIXED. The pilot's "contested-tape continuation" story (two-sided pressure resolving in the basket's favour) is a *Kyle-flavoured* read; the toxic-flow story says contested tape is where signal goes to die. The test arbitrates between them.

The unit being tested is **excess over drift**, not the raw return level. In a five-year semiconductor bull run almost any "signal" looks positive in levels — the chips went up most days regardless. The honest question is whether a sweep beats *simply being long the basket*. Concretely: if the basket drifts +0.16% on an average next day, a BUY sweep has to deliver meaningfully more than +0.16% to count, not merely "more than zero."

**Hypotheses (per sweep type, on the next-day basket return):**

- **H0 (the null we expect to keep):** conditional next-day return = the unconditional next-day drift of the same basket. Sweeps carry no incremental information.
- **H1, directional:** a BUY (SELL) sweep predicts a positive (negative) *excess* next-day return — informed-flow continuation.
- **H1, MIXED:** continuation story → positive excess; toxic-flow story → no excess. Competing, falsifiable predictions.

**What would prove us wrong:** any sweep type showing a positive *excess-over-drift* return that stays the same sign and stays significant after the dependence adjustment, the multiplicity correction, the random-entry baseline, the chronological hold-out, **and** a cost haircut. One cell clearing all five hurdles would reject the null. None does.

**Our approach, in one breath:** first we look at the naive per-event picture (the eyeball the pilot stopped at); then we repair the two defects that inflate it; then we benchmark against random entry and a true forward hold-out; then we actively try to kill our own result with three rival explanations. Only what survives all of that would count.

This study opens a thread that runs through the repo: *which intraday/short-horizon "edges" survive an honest test?* It is the methodological sibling of [study 07 (intraday decision-time)](../07-intraday-overnight-decomposition/) and shares the random-day baseline used in [study 09 (activist shorts)](../09-activist-short-post-performance/).

## Method, and why each piece

- **Sample / window.** Seven large-cap semiconductors — NVDA, TSM, AVGO, AMD, ASML, AMAT, KLAC — 15-minute bars, regular trading hours only (9:30–16:00 ET), 2021-04 to 2026-04 (~224k intraday bars). Regular-hours-only because the open/close auctions have a different volume distribution and would contaminate the abnormal-volume measure.
- **Sweep definition.** For each ticker/bar, a rolling 60-bar (~one trading day) volume **Z-score** — how many standard deviations the bar's volume sits above its own recent norm. A bar *qualifies* when Z ≥ 3.0 (volume ~3σ above normal). Qualifying bars are grouped by timestamp and the cluster classified: `BUY_SWEEP` (≥2 qualifying names closing up), `SELL_SWEEP` (≥2 closing down), `MIXED` (≥2 qualifying, both sides present, neither side reaching two), `SINGLE` (one qualifying name). "Side" is `sign(close − open)` on the bar — a coarse but standard intraday buy/sell proxy.
- **Outcome.** Next-day basket return = equal-weight mean across the 7 names of (next daily close / today's close − 1).
- **Naive test (where the old study stopped).** A one-sample t-test of each type's next-day returns against zero. This is the *starting* point — it has two defects that *inflate* significance, repaired below.
- **Dependence adjustment (the core fix).** Many sweep events land on the *same trading day* and therefore share **one** next-day basket return; counting them as independent overstates the sample size and shrinks the standard errors. We collapse to **one observation per trading day per type** (the honest *effective n*) and, for the headline types, run a **stationary block bootstrap** (mean block ≈ 5 trading days) — a resampling scheme that keeps short runs intact so it does not assume away the day-to-day correlation in the series. Reported as cluster-robust + bootstrap p-values and a bootstrap 95% CI.
- **Multiplicity.** Four sweep types are tested at once, so we report **Bonferroni and Šidák** corrections — one suggestive cell out of four is not a pre-registered hit. (Bonferroni: multiply the p-value by the number of tests; a crude but conservative guard against fishing.)
- **Random-entry baseline.** For each type we draw 20,000 random sets of the *same number of distinct trading days* from the same basket and window, and ask where the observed mean falls. This separates a genuine edge from the basket's drift: an honest signal must beat random same-names entry, not merely beat zero.
- **Chronological out-of-sample (OOS).** A true forward split — train 2021-04 → 2024-10, hold out 2024-10 → 2026-04. The previous study *claimed* an out-of-sample decay it never ran; this resolves it.
- **Cost haircut.** A round-trip cost (5/10/15 bps on the equal-weight basket) is deducted to see whether any gross tilt survives execution.
- **Robustness.** Z-threshold swept 2.5 → 5.0; the MIXED cell decomposed by sweep size, intra-sweep tilt, and volatility regime.

The identification problem stated out loud: in a bull market, **drift contaminates everything**. Any rule that is "in the market on selected days" will look profitable in levels. The whole method is built to net out that drift — the random-entry baseline and the excess-over-drift framing are the load-bearing pieces, not the t-test.

## Data

| | |
|---|---|
| Basket | NVDA, TSM, AVGO, AMD, ASML, AMAT, KLAC (equal-weight) |
| Bars | 15-minute, regular hours (9:30–16:00 ET) |
| Window | 2021-04-30 → 2026-04-30 (~5 years, 1,255 trading days) |
| Intraday bars | ~224k after the regular-hours filter |
| Qualifying bars | Z ≥ 3.0 on a 60-bar rolling volume window |
| Sweep events | 2,135 across 1,135 distinct trading days |

One line per series: 15-minute consolidated US equity aggregates for the seven names → 2021-04-30 to 2026-04-30 → rolling-60-bar volume Z-score, regular-hours filter, daily-close resample for the outcome. All from a private 15-minute intraday warehouse.

**Reproducibility note / data gap.** This rebuild runs on the warehouse's 15-minute intraday history. The original 14-day pilot and the first ~5-year extension were computed on a *different* intraday source that is no longer available; its exact event counts (e.g. MIXED n=92) do not reproduce here (this build yields MIXED n=121 at the same Z=3.0). The pilot's raw numbers are therefore reported as historical context, not re-derived; every number in the Analysis below is freshly computed on the data in this table. The qualitative conclusion is unchanged and, if anything, stronger: the pilot did not survive.

## Descriptive — the per-sweep-type picture

Counting events naively (each event as one observation) gives the picture the old study stopped at:

| Sweep type | events | naive mean next-day | win rate | naive p |
|---|---:|---:|---:|---:|
| SINGLE | 1,040 | +0.16% | 56.0% | 0.026 |
| SELL_SWEEP | 433 | +0.29% | 52.7% | 0.010 |
| BUY_SWEEP | 541 | +0.01% | 51.8% | 0.960 |
| MIXED | 121 | −0.05% | 44.6% | 0.798 |

The eye-catching pilot cells are already gone before any hardening: BUY_SWEEP is flat (+0.01%), and MIXED — the cell that "survived" in the pilot — is *negative*. Two cells (SINGLE, SELL_SWEEP) look significant naively. The Analysis layer asks whether any of that is real. The spine from here: **we see two naively-significant cells → which means we must check whether the significance is an artifact of double-counting → so we collapse to effective n and re-test.**

How a sweep is defined and classified, in code (analysis logic only):

```python
# per ticker, per 15-min bar (regular hours only)
vol_z = (volume - volume.rolling(60).mean()) / volume.rolling(60).std()
qualifies = vol_z >= 3.0                      # ~3 sigma above its own recent norm
side = np.sign(close - open)                  # +1 up-bar, -1 down-bar (buy/sell proxy)

# group all qualifying bars that share a timestamp, then classify the cluster
ups, downs = (side > 0).sum(), (side < 0).sum()
if   ups   >= 2 and downs == 0: cluster = "BUY_SWEEP"
elif downs >= 2 and ups   == 0: cluster = "SELL_SWEEP"
elif ups   >= 1 and downs >= 1: cluster = "MIXED"      # contested tape
else:                           cluster = "SINGLE"

# outcome: equal-weight next-day basket return
next_day_ret = basket_close.shift(-1) / basket_close - 1   # mean across the 7 names
```

---

## Analysis

### Finding 1 — Once you stop double-counting, no type beats drift

- **What we expected & why.** Under H0 (and the Kyle read having only a thin prior here), the conditional next-day return should equal the basket's drift. The naive test inflates significance because dozens of same-day events share one outcome, so the *real* question is what the per-day picture shows.
- **How we measured it.** Collapse to one observation per trading day per type (effective n), re-run the t-test cluster-robust, and confirm with a stationary block bootstrap:

  ```python
  daily = events.groupby(["trading_day", "type"]).first()       # 1 obs / day / type
  for t in types:
      x = daily.loc[daily.type == t, "next_day_ret"]
      cluster_p = ttest_1samp(x, 0).pvalue                      # honest n
      # dependence-robust p: keep ~5-day blocks intact when resampling
      boot = [np.mean(stationary_bootstrap(x, mean_block=5)) for _ in range(20_000)]
      boot_p = 2 * min((np.array(boot) <= 0).mean(), (np.array(boot) >= 0).mean())
  ```

- **What the data shows.**

  | Sweep type | effective n | mean next-day | win rate | cluster p | bootstrap p | Bonferroni p |
  |---|---:|---:|---:|---:|---:|---:|
  | SINGLE | 711 | +0.18% | 55.3% | 0.040 | — | 0.106 |
  | SELL_SWEEP | 378 | +0.20% | 52.1% | 0.097 | — | 1.000 |
  | BUY_SWEEP | 493 | +0.03% | 52.1% | 0.779 | 0.783 | 1.000 |
  | MIXED | 117 | −0.08% | 44.4% | 0.668 | 0.607 | 1.000 |

  The two naively-significant cells lose it: SELL_SWEEP slips to p≈0.10, and SINGLE (cluster p≈0.04) does not survive Bonferroni (0.106). BUY and MIXED were never significant. The block-bootstrap 95% CI for MIXED is **[−0.43%, +0.26%]** — squarely straddling zero.

  ![Next-day return by sweep type](fwd-return-by-sweep-type.png)

- **Why (mechanism).** Pool *all* sweep days against *all* trading days in the same window and the reason is plain:

  | | n | mean | median | % positive |
  |---|---:|---:|---:|---:|
  | All sweep days | 1,135 | +0.166% | +0.147% | 53.5% |
  | All trading days (baseline) | 1,255 | +0.163% | +0.147% | 53.4% |

  Identical to three decimals. A sweep day *is* an ordinary day — the rolling-volume filter selects busy days, but busy days in this basket are not special days.

- **What we checked.** The random-entry baseline (20,000 draws of the same number of distinct days) is decisive: the observed BUY mean sits below ~95% of random 493-day draws, and the MIXED mean below ~89% of random 117-day draws — the observed line falls to the *left* of the random distribution in both panels. So the rare positive cell does not even beat picking the same names on random days.

  ![Random-entry baseline](random-entry-baseline.png)

- **Verdict.** **Null.** H0 is not rejected for any type. The cluster collapse is mildly conservative on multi-event days, but the bootstrap p-values agree, so the result is not an artifact of the collapse. The directional-flow (Kyle) prediction fails for BUY/SELL; the contention-continuation prediction fails for MIXED.

### Finding 2 — MIXED has no working mechanism; the toxic-flow null fits

- **What we expected & why.** The pilot's continuation story predicts MIXED resolves in the basket's favour (positive). The competing VPIN/toxic-flow read predicts MIXED is noise (no excess). One of these should show up if either is real.
- **How we measured it.** At Z=3.0 every MIXED event is, by construction, a two-name one-up-one-down bar (with ≥3 qualifying names one side almost always reaches two and the cluster is re-labelled BUY/SELL). We read that single cell, then condition it on volatility regime:

  ```python
  mixed = daily.loc[daily.type == "MIXED"]
  overall = (mixed.next_day_ret.mean(), (mixed.next_day_ret > 0).mean())
  vix_med = mixed.vol_proxy.median()
  lo = mixed.loc[mixed.vol_proxy <= vix_med, "next_day_ret"]   # calm regime
  hi = mixed.loc[mixed.vol_proxy >  vix_med, "next_day_ret"]   # turbulent regime
  ```

- **What the data shows.** The MIXED cell is **−0.08%, 44% win, p≈0.67** — the *opposite* sign to continuation. Conditioning does not rescue it: low-vol MIXED is −0.18% (39% win), high-vol MIXED −0.06% (48% win); neither significant. No subgroup shows contested tape reliably continuing.
- **Why (mechanism).** A concrete case: NVDA spikes up while AMD spikes down in the same 15 minutes. The continuation story says the basket "picks a winner" and drifts up next day; the data says it does nothing distinguishable from a coin flip with a slight down-bias — consistent with market-makers facing two-sided uncertainty and the move washing out, exactly the toxic-flow picture.
- **What we checked.** Power is the honest caveat: with only ~117 effective MIXED days the mechanism battery is weak, so "no mechanism found" means "none detectable," not a proven absence. A finer signed-volume tape (true buy/sell classification, not close-vs-open) could in principle revive it — but the burden is on that finer data.
- **Verdict.** **Null / conditional.** The continuation mechanism is rejected at this resolution; the toxic-flow null is consistent with the data. MIXED has no demonstrated economic driver.

### Finding 3 — Nothing survives out-of-sample, costs, or threshold changes

- **What we expected & why.** A real edge should carry its sign and significance into an untouched forward window, survive a realistic cost haircut, and not depend on the exact Z cutoff. A noise edge fails all three.
- **How we measured it.** A true chronological split (no peeking), a flat round-trip cost deduction, and a sweep of the qualifying threshold:

  ```python
  train = daily[daily.trading_day <  "2024-10-01"]   # fit window
  hold  = daily[daily.trading_day >= "2024-10-01"]   # untouched forward window
  net   = gross_mean - round_trip_bps / 100          # 5 / 10 / 15 bps haircut
  for z in [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:           # threshold sensitivity
      recompute_sweeps(z); read_mixed_cell()
  ```

- **What the data shows.**

  | Sweep type | train mean (p) | hold-out mean (win, p) |
  |---|---:|---:|
  | SINGLE | +0.14% (0.16) | +0.28% (60%, 0.12) |
  | SELL_SWEEP | +0.06% (0.69) | +0.52% (62%, 0.010) |
  | BUY_SWEEP | +0.05% (0.71) | −0.01% (55%, 0.96) |
  | MIXED | −0.21% (0.39) | +0.16% (49%, 0.64) |

  MIXED flips from −0.21% in-sample to +0.16% out-of-sample — noise, not persistence. SELL_SWEEP's hold-out (+0.52%, p=0.010) is tempting but is a *fresh* appearance (train p=0.69, sign did not carry) — an in-window fluke, the exact trap an OOS test exists to catch.

  ![Chronological out-of-sample](oos-train-holdout.png)

  **Costs:** a 10 bps round trip turns BUY net-negative (−0.07%) and pushes MIXED to −0.18%; even the benign SINGLE/SELL tilts (gross ~+0.18–0.20%) shrink to +0.05–0.10% net — thin, and not significant once dependence-adjusted.

  **Thresholds:** MIXED reads +0.39% (Z2.5), −0.08% (Z3.0), +0.08% (Z3.5), +0.35% (Z4.0), +0.03% (Z4.5), −0.36% (Z5.0). The sign is unstable; no level is significant after adjustment.

  ![Threshold sensitivity](threshold-sensitivity.png)

- **Why (mechanism).** A sign that flips with the cutoff and a "hit" that only appears after the training window are the fingerprints of a series scattered around zero — there is no underlying constant for the threshold to expose.
- **What we checked.** Costs are a stylized flat haircut; real fills on these megacaps are usually cheaper than 10 bps, but borrow/short friction on a SELL sweep is not modelled — so the cost test is, if anything, lenient on the long cells and harsh on none.
- **Verdict.** **Null.** Fails out-of-sample, fails on costs, fails threshold stability. Nothing robust remains.

---

## Robustness — did we just find noise?

Pulled together as a stated goal: the three axes above (a true forward hold-out, a cost haircut, threshold sensitivity) are precisely the "is this noise?" battery. The OOS sign-flip for MIXED, the disappearance of SINGLE/SELL after the cost haircut, and the threshold instability all point the same way — there is no stable edge for any of these tests to confirm. The block bootstrap is the fourth leg: it agrees with the cluster t-tests, so the null is not a quirk of one inference method.

## Steelman the rival, then kill it

If a sweep edge is *not* the story, three alternative explanations could each produce the surface appearance of one. Each is steelmanned, then tested on its own numbers.

**Rival A — it's just basket drift.** *Steelman:* the chips rose most days for five years; any "in the market on selected days" rule inherits that drift and looks profitable in levels. *Test:* re-express every cell as **excess over the basket's unconditional next-day drift (+0.163%)**. Result — **no type has a significant excess**: SINGLE +0.018% (p=0.84), SELL +0.033% (p=0.78), BUY −0.133% (p=0.22), MIXED −0.248% (p=0.21). Every positive *level* is the basket drifting up in a bull market. **Rival A wins** — the level effect is drift.

**Rival B — it's price momentum, not sweeps.** *Steelman:* maybe sweeps just cluster on days that already moved, and what looks like a volume signal is ordinary short-horizon momentum. *Test:* the random-entry baseline draws the *same names* on random days from the *same window* — so it carries the same momentum and drift exposure as the sweep days. The observed BUY and MIXED means fall *below* that baseline (left of ~95% and ~89% of draws). A sweep does not even beat the momentum/drift already embedded in random same-names entry. **Rival B is not needed** — sweeps add nothing on top of it.

**Rival C — a few big episodes, not a stable edge.** *Steelman:* perhaps a small edge is real but masked by averaging. *Test:* sum the MIXED daily returns over five years — they total **−9.9%**, and the five largest-magnitude days alone swing the series by **+14.3%**. The whole thing is a handful of episodes oscillating around zero. *Verdict:* the opposite of a stable edge; this is the signature of noise.

  ![MIXED cumulative](mixed-cumulative.png)

The rivals that win (drift, embedded momentum) are exactly the ones that imply *no tradable sweep signal*. The rival that would rescue a real edge (a stable effect hidden by averaging) is the one the data rejects.

---

## The answer, in the data

**Q: Do cross-ticker volume sweeps predict the basket's next-day return?**

**A: No.** Once the inference is honest — effective n, cluster-robust and block-bootstrap p-values, multiplicity correction, a random same-names baseline, a true chronological hold-out, and a cost haircut — **no sweep type produces a next-day edge over the basket's own drift.** The pilot's BUY signal was small-sample noise; the MIXED cell, far from "surviving," is negative on the full sample, sign-unstable across thresholds, beaten by random entry, and net-negative after costs.

| Sweep type | effective n | median next-day | mean next-day | % positive | dependence-adj. p | survives OOS + costs? |
|---|---:|---:|---:|---:|---:|:--|
| SINGLE | 711 | +0.30% | +0.18% | 55.3% | 0.040 (n.s. after Bonferroni) | No |
| SELL_SWEEP | 378 | +0.09% | +0.20% | 52.1% | 0.097 | No |
| BUY_SWEEP | 493 | +0.04% | +0.03% | 52.1% | 0.779 | No |
| MIXED | 121 | −0.25% | −0.05% | 44.6% | 0.668 | No |
| **All sweep days** | **1,135** | **+0.15%** | **+0.17%** | **53.5%** | — (= drift) | — |
| Baseline (all days) | 1,255 | +0.15% | +0.16% | 53.4% | — | — |

**The two questions, separated.** *Did the effect hold?* No — it is a clean null. *Was the method sound / what did we learn?* Yes: the gap between the naive per-event picture and the per-day truth is the whole lesson, and the random-entry baseline is the tool that makes drift impossible to mistake for skill. The live alternative we **cannot** fully exclude is that a finer order-flow tape (true signed volume rather than close-vs-open at 15-minute resolution) hides a MIXED effect this data is too coarse to see — so this is *inconsistent with* a tradable sweep signal, not a proof one can never exist. A clean null is the result, and the right one.

## Caveats

- Backtest only; next-day *basket* returns, equal-weight. The cost haircut is stylized and ignores borrow on short sweeps (direction: makes the long cells look slightly *better* than reality, the short cells slightly worse).
- Side is a close-vs-open bar proxy, not true signed volume; 15-minute bars are coarse. A finer tape could expose a MIXED effect this resolution cannot — but the burden of proof is on that data, not on a +0.65% pilot (direction: could only *add* a missed signal, not remove a found one).
- Single sector, 7 names, one (mostly bull) regime; the drift baseline absorbs the level effect, but generalization to other baskets/regimes is untested (direction: unknown).
- The exact pilot data source could not be reproduced (see Data note); pilot figures are historical context, all Analysis numbers are recomputed on the stated sample.

## Reproducibility

**Sweep definition (the governing formula).** For ticker *i*, bar *t*, with 60-bar rolling mean and standard deviation of volume:

```
Z_{i,t} = ( V_{i,t} − mean_{60}(V_{i}) ) / std_{60}(V_{i})
qualify if  Z_{i,t} ≥ 3.0
side_{i,t} = sign( close_{i,t} − open_{i,t} )
```

Group qualifying bars by timestamp; classify the cluster by how many names print on each side (≥2 up = BUY, ≥2 down = SELL, both sides present = MIXED, one name = SINGLE). Outcome = equal-weight next-day basket return.

**The two load-bearing inference steps, in code:**

```python
# 1) honest sample size — one observation per trading day per type
daily = events.groupby(["trading_day", "type"]).first()

# 2) dependence-robust p-value — stationary (block) bootstrap, ~5-day mean block,
#    so short autocorrelated runs survive resampling intact
def stationary_bootstrap(x, mean_block=5, n_boot=20_000):
    out = []
    for _ in range(n_boot):
        idx, p = [], 1.0 / mean_block
        i = np.random.randint(len(x))
        while len(idx) < len(x):
            idx.append(i)
            i = np.random.randint(len(x)) if np.random.rand() < p else (i + 1) % len(x)
        out.append(np.mean(x[idx]))
    return np.array(out)
```

Full pipeline (event construction from raw 15-minute bars, the random-entry baseline, the OOS split, and every chart) lives in the study's research notebook in the private method repo; the formulas and code boxes above reproduce the headline numbers from raw 15-minute bars. Source: 15-minute consolidated US equity aggregates for the seven names, 2021–2026, from a private intraday warehouse.

## References & forward pointer

- Kyle, A. (1985). *Continuous auctions and insider trading.* Econometrica — informed order flow and linear price impact.
- Easley, D., López de Prado, M. & O'Hara, M. (2012). *Flow toxicity and liquidity in a high-frequency world* (VPIN). Review of Financial Studies — balanced abnormal flow as toxic/noisy.
- Politis, D. & Romano, J. (1994). *The stationary bootstrap.* JASA — dependence-robust resampling behind the block-bootstrap p-values.
- Data: end-of-day and 15-minute consolidated US equity aggregates for the seven names, 2021–2026.

**Builds on / part of:** the repo-wide thread on *which short-horizon "edges" survive an honest test*. Shares the random same-names baseline with [study 09 — activist short post-performance](../09-activist-short-post-performance/).

**Next:** [study 07 — intraday decision-time](../07-intraday-overnight-decomposition/), which asks the same "describe vs trade" question one layer up — how early in the day the close is callable, and whether that mechanical predictability is actually tradable (it is not). Same lesson, different clock.
