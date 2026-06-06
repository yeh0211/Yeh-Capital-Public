# 01 — Volume-sweep microstructure: does the sweep effect depend on company size?

The folk belief on a trading desk is simple: when a stock suddenly trades far more than usual, *somebody knows something*, and the price will keep moving their way. Scale it up — when **several** related chip stocks all light up with abnormal volume in the **same** fifteen minutes, that synchronized burst (a "sweep") feels like informed money tipping its hand, and the basket should drift in that direction tomorrow.

A natural next question: **if** that information edge is real, it should be **biggest in small, thinly-covered names** — where one informed buyer can move the tape and the rest of the market is slow to notice — and **weakest in mega-caps**, where everything is already priced. This rebuild takes that size hypothesis seriously. It runs the *same* sweep test inside **four market-cap buckets** of a large semiconductor universe, and asks one cross-sectional question: **does the (non-)effect depend on size?**

The short answer: the size prior shows up exactly where you'd expect — in the *point estimates* of the smallest names — and it is exactly there that it turns out to be **a handful of wild days, not a tradable edge.** Once the inference is honest, no bucket, large or small, produces a sweep signal that survives. The only thing size changes is how *loud the noise* is.

**Question.** When several semiconductors all print an abnormal-volume 15-minute bar at the *same* timestamp, does that burst predict the basket's **next-day** return — and does any such effect grow as the names get smaller and less liquid?

**Why it matters.** If a sweep edge existed and concentrated in small caps, it would be a cheap, scalable intraday entry rule for a sector book: trade the sweep in the names where information travels slowest. If it does not — and especially if the small-cap "signal" is just volatility masquerading as edge — that is the textbook trap, worth documenting as a null so the next person does not pay to re-learn it.

> Research / backtested. 39 US-listed semiconductors, 15-minute bars, regular hours, 2021-04 to 2026-04. No live capital, no execution costs assumed unless stated. A clean null, reported as a null, now resolved *across the size spectrum.*

---

## Summary of results

- **Verdict: No — and the size prior fails in an instructive way.** No sweep type beats its own basket's ordinary next-day drift, in *any* of the four cap buckets or the full 39-name universe, once the inference is done properly.
- **The size prior does appear — as a point estimate.** The smallest bucket's two-sided "MIXED" sweep shows a huge raw next-day mean (**+1.40%**, vs a +0.47% drift), the largest cell anywhere. That is precisely what "information travels slower in small caps" predicts.
- **But it is a few episodes, not an edge.** That +1.40% comes almost entirely from **five days**: the five largest-magnitude days contribute +335 percentage-points of the +462pp five-year sum, and removing them collapses the mean to **+0.39%** — below the basket's own +0.47% drift. Its excess-over-drift t-test is **p=0.31** (not significant) despite the giant point estimate, because the confidence band is enormous.
- **The fingerprints of noise, scaled by size.** The small-cap MIXED cell **explodes** as the Z threshold rises (+1.40% at Z3.0 → +7.77% at Z5.0 — fewer, wilder days) and **explodes again out-of-sample** (+0.46% train → +2.79% hold-out — a *different* set of wild days). Mid, Large and Mega all stay pinned near drift across both tests. Small caps are not more informative; they are more volatile.
- **No directional structure anywhere.** Across all four buckets, **BUY** sweeps are *negative* in excess-over-drift (−0.31% Small, −0.14% Mid, −0.17% Large, −0.26% Mega) — the opposite of the informed-continuation story, at every size.
- **The spine:** compute each name's market cap → split into four buckets → run the full sweep battery (effective-n collapse, cluster-robust + block-bootstrap p, multiplicity correction, random same-names baseline, chronological hold-out, cost haircut) *inside each bucket* and for the full 39 → ask whether the bucket's size explains anything. It does not, except as a volatility dial.

---

## Theory and hypothesis

This sits in the **microstructure** literature — the study of how individual orders and trades move price, as opposed to fundamentals. The plain prior is one sentence: **if a synchronized abnormal-volume burst carries information, the edge should be larger in smaller, less-liquid names (more information asymmetry, slower price discovery) and weakest in mega-caps (everything already priced).** That is the cross-sectional claim this study tests.

Two canonical results frame *what* a sweep might mean, and they disagree on the two-sided case, which is why we keep all four sweep types:

- **Kyle (1985) — informed order flow moves price.** An informed trader splits a large order to hide it, so signed order flow ("net buying minus net selling") is itself informative and price impact is roughly linear in it. A *one-sided* burst — a **BUY sweep**, several names spiking on up-bars — is a candidate proxy for informed, sector-wide flow, and Kyle predicts the information keeps getting impounded: a next-day drift in the flow's direction. By the size prior, this should bite hardest in small caps.
- **Easley, López de Prado & O'Hara (2012) — flow toxicity (VPIN).** When buy and sell volume both arrive in abnormal size at once, order flow is *toxic*: market-makers cannot tell who is informed, and the aftermath is noise and adverse selection, not a clean direction. A *two-sided* (**MIXED**) sweep — one chip spiking up while another spikes down in the same bar — is the picture of high toxicity, and this read predicts the next-day response is **closer to noise.**

The unit being tested is **excess over drift**, not the raw return level. In a five-year semiconductor bull run almost any "signal" looks positive in levels — the chips went up most days regardless, and the smaller, more volatile names drifted up *fastest* (the Small bucket's average day is +0.47%, versus +0.13% for the Large bucket). The honest question per bucket is whether a sweep beats *simply being long that bucket's basket*. Concretely: if the small-cap basket drifts +0.47% on an average next day, a small-cap BUY sweep has to clear meaningfully more than +0.47% to count — not merely "more than zero," and certainly not "more than the mega-cap drift."

**Hypotheses (per sweep type, per bucket, on the next-day basket return):**

- **H0 (the null we expect to keep):** conditional next-day return = the unconditional next-day drift of the *same bucket's* basket. Sweeps carry no incremental information, at any size.
- **H1, directional:** a BUY (SELL) sweep predicts a positive (negative) *excess* next-day return — informed-flow continuation.
- **H1, the size claim:** the magnitude and significance of any excess should **increase monotonically as bucket size falls** (Small > Mid > Large > Mega).

**What would prove us wrong:** a sweep cell with a positive *excess-over-drift* return that (a) stays the same sign and stays significant after the dependence adjustment, multiplicity correction, random-entry baseline, chronological hold-out, and cost haircut, **and** (b) is systematically larger in the smaller buckets. One bucket producing a surviving cell would reject H0; a clean small→mega gradient of surviving cells would confirm the size claim. Neither happens.

**Our approach, in one breath:** first we cut the 39-name universe into four cap buckets by market value; then inside each we run the naive per-event picture, repair the two defects that inflate it, benchmark against random same-names entry, split out-of-sample, and haircut for costs; then we line the buckets up small→mega and ask whether size explains the pattern. Only a surviving cell with a size gradient would count.

This study opens a thread that runs through the repo: *which intraday/short-horizon "edges" survive an honest test?* It is the methodological sibling of [study 07 (intraday decision-time)](../07-intraday-overnight-decomposition/) and shares the random same-names baseline used in [study 09 (activist shorts)](../09-activist-short-post-performance/). The cap-bucketing mirrors the size-conditioning lens of [study 17 (semiconductor layers)](../17-semiconductor-layers/).

## Method, and why each piece

- **Universe (the biggest the data supports).** 39 US-listed semiconductors with usable 15-minute intraday history: NVDA, AMD, INTC, TSM, AVGO, MU, QCOM, TXN, ADI, NXPI, MCHP, ON, MRVL, STM, WOLF, WDC, AMAT, LRCX, KLAC, ASML, TER, ENTG, ACLS, AEHR, PLAB, AMKR, UMC, TSEM, GFS, RMBS, HIMX, SKYT, CRDO, NVTS, COHR, LITE, AAOI, SNPS, CDNS. The intraday history caps the count at ~39 names; a ~100-name version is a separate **daily-data** study, not this one.
- **Market cap → buckets.** Each name's cap = its latest reported diluted-average-share count × its latest daily close. The 39 are sorted into four mutually-exclusive tiers: **Small (< $10B), Mid ($10–100B), Large ($100–500B), Mega (> $500B).** Seven names are foreign issuers (ADRs) for which the warehouse carries **no share-count line** (diluted *or* basic): TSM, STM, ASML, UMC, TSEM, GFS, HIMX. They are **dropped from the bucketed test** (32 names bucketed) but **kept in the full-39 test**, which needs no cap.
- **Sample / window.** 15-minute bars, regular trading hours only (09:30–16:00 ET), 2021-04-30 → 2026-04-30 (1,258 trading days). Source bars are 5-minute; we resample to 15-minute (sum volume, first/last/max/min OHLC). Regular-hours-only because the open/close auctions have a different volume distribution and would contaminate the abnormal-volume measure.
- **Timezone + the open-auction bar.** Timestamps in the warehouse are naive UTC; we localize to UTC, convert to America/New_York (which handles the EDT/EST shift automatically), then keep 09:30–16:00 ET. The **09:30 ET open bar has auction-inflated volume**, so it is excluded — consistently across every name and bucket — from *both* the rolling-volume baseline *and* from qualifying as a sweep bar.
- **Sweep definition (identical per bucket).** For each ticker/bar, a rolling 60-bar volume **Z-score** — how many standard deviations the bar's volume sits above its own recent norm. A bar *qualifies* when Z ≥ 3.0. Qualifying bars are grouped by timestamp **within the bucket** and the cluster classified: `BUY_SWEEP` (≥2 qualifying names closing up, none down), `SELL_SWEEP` (≥2 down, none up), `MIXED` (both sides present, neither reaching two), `SINGLE` (one qualifying name). "Side" is `sign(close − open)` on the bar — a coarse but standard intraday buy/sell proxy.
- **Outcome (own basket per bucket).** Each bucket is its **own** equal-weight basket and its **own** sweeps. Next-day return = equal-weight mean across the bucket's names of (next daily close / today's close − 1).
- **Dependence adjustment (the core fix).** Many sweep events land on the *same trading day* and share **one** next-day basket return; counting them as independent overstates the sample size. We collapse to **one observation per trading day per type per bucket** (the honest *effective n*) and confirm with a **stationary block bootstrap** (mean block ≈ 5 trading days) — a resampling scheme that keeps short runs intact. Reported as cluster-robust + bootstrap p-values and a bootstrap 95% CI.
- **Multiplicity.** Four sweep types tested per bucket, so we report **Bonferroni** corrections (multiply the p-value by 4) — one suggestive cell out of four is not a hit.
- **Random-entry baseline.** Per bucket per type we draw 20,000 random sets of the *same number of distinct trading days* from the *same bucket basket*, and ask where the observed mean falls. An honest signal must beat random same-names entry, not merely beat zero.
- **Chronological out-of-sample (OOS).** A true forward split per bucket — train 2021-04 → 2024-10, hold out 2024-10 → 2026-04.
- **Cost haircut.** A flat 10 bps round-trip is deducted to see whether any gross tilt survives execution.
- **Robustness.** Z-threshold swept 2.5 → 5.0 per bucket; the headline small-cap cell decomposed by episode removal.

The identification problem stated out loud: in a bull market, **drift contaminates everything, and it contaminates small caps most** (their average day is the biggest). Any rule that is "in the market on selected small-cap days" will look profitable in levels. The whole method nets out that drift per bucket — the excess-over-drift framing and the random same-names baseline are the load-bearing pieces, not the t-test.

## Data

**The universe, bucketed.** Caps are latest-share-count × latest close, in $B.

| Bucket | Range | Count | Members (cap $B) | Total cap |
|---|---|---:|---|---:|
| **Small** | < $10B | 6 | NVTS (7), ACLS (5), AEHR (4), SKYT (2), PLAB (2), WOLF (2) | $21B |
| **Mid** | $10–100B | 12 | SNPS (95), LITE (91), COHR (83), NXPI (82), TER (65), ON (54), MCHP (53), CRDO (42), ENTG (21), RMBS (19), AMKR (18), AAOI (13) | $634B |
| **Large** | $100–500B | 9 | LRCX (423), AMAT (401), KLAC (281), TXN (279), MRVL (273), QCOM (262), WDC (219), ADI (211), CDNS (113) | $2,462B |
| **Mega** | > $500B | 5 | NVDA (5,333), AVGO (2,048), MU (1,137), AMD (863), INTC (568) | $9,950B |

*Dropped from bucketing (no share-count line, ADR foreign issuers): TSM, STM, ASML, UMC, TSEM, GFS, HIMX — these 7 remain in the full-39 test.* All 32 bucketed names use the **diluted** average-share count; none required the basic-share fallback.

![The universe across four cap buckets](cap-buckets-overview.png)

| | |
|---|---|
| Bars | 15-minute (5-min resampled), regular hours (09:30–16:00 ET) |
| Window | 2021-04-30 → 2026-04-30 (1,258 trading days) |
| Qualifying bars | Z ≥ 3.0 on a 60-bar rolling volume window, open-auction bar excluded |
| Sweep events (full 39) | 7,451; per bucket: Small 2,680 · Mid 4,027 · Large 2,369 · Mega 1,418 |

One line per series: 15-minute consolidated US equity aggregates for the 39 names → 2021-04-30 to 2026-04-30 → UTC→ET conversion, regular-hours filter, 60-bar rolling volume Z-score, daily-close resample for the outcome; latest reported diluted shares × latest daily close for the cap split. All from a private intraday + reference warehouse.

## Descriptive — the per-bucket, per-type picture

Collapsing to one observation per trading day per type (the honest effective n) and reading each bucket's basket against its **own** drift:

![Next-day return by sweep type, per bucket](fwd-return-by-bucket.png)

The eye is drawn straight to the **Small / MIXED** bar: +1.40% next-day, more than triple any other cell and nearly triple the Small basket's own +0.47% drift. That is exactly the shape the size prior predicts — the loudest sweep "signal" sits in the smallest names. Every other cell in every other bucket hugs its drift line.

Lined up as the size test the prior actually asks for — **excess over each bucket's own drift, small → mega** — the gradient is not the clean rising staircase the prior wants. Only one point (Small/MIXED) sits far above zero; the directional (BUY/SELL) cells are *negative* across the board, and Mid/Large/Mega cluster at zero:

![Sweep effect vs cap bucket](sweep-effect-vs-cap.png)

The spine from here: **we see one giant cell in the smallest bucket → which means the size prior might be right → so we must ask whether that cell is a stable effect or a few days, and whether the gradient holds across buckets.**

How a sweep is defined and classified, in code (analysis logic only, run *within each bucket*):

```python
# per ticker, per 15-min bar (regular hours, open-auction bar dropped)
vol_z = (volume - volume.rolling(60).mean()) / volume.rolling(60).std()
qualifies = (vol_z >= 3.0) & (bartime != "09:30")   # ~3 sigma; exclude auction
side = np.sign(close - open)                         # +1 up-bar, -1 down-bar

# group qualifying bars in THIS bucket that share a timestamp, classify the cluster
ups, downs = (side > 0).sum(), (side < 0).sum()
if   ups   >= 2 and downs == 0: cluster = "BUY_SWEEP"
elif downs >= 2 and ups   == 0: cluster = "SELL_SWEEP"
elif ups   >= 1 and downs >= 1: cluster = "MIXED"     # contested / toxic tape
else:                           cluster = "SINGLE"

# outcome: equal-weight next-day return of THIS bucket's basket
next_day_ret = bucket_close.shift(-1) / bucket_close - 1   # mean across the bucket
```

---

## Analysis

### Finding 1 — Inside each bucket, no type beats its own drift after the honest collapse

- **What we expected & why.** Under H0 the conditional next-day return equals the bucket's drift. The naive per-event count inflates significance because dozens of same-day events share one outcome, so the real question is the per-day picture, per bucket.
- **How we measured it.** Collapse to one observation per trading day per type per bucket (effective n), re-run the t-test cluster-robust, confirm with a stationary block bootstrap, and Bonferroni-correct across the four types:

  ```python
  daily = events.groupby(["bucket", "trading_day", "type"]).first()   # 1 obs/day/type
  for b in buckets:
      for t in types:
          x = daily.loc[(daily.bucket == b) & (daily.type == t), "next_day_ret"]
          cluster_p = ttest_1samp(x, 0).pvalue                        # honest n
          boot   = [mean(stationary_bootstrap(x, mean_block=5)) for _ in range(10_000)]
          boot_p = 2 * min((boot <= 0).mean(), (boot >= 0).mean())
          bonf_p = min(1.0, cluster_p * 4)
  ```

- **What the data shows.** Effective-n collapsed, per bucket (mean next-day %, win %, cluster p, bootstrap p, Bonferroni p):

  | Bucket | Type | n_eff | mean % | win % | cluster p | boot p | Bonf p |
  |---|---|---:|---:|---:|---:|---:|---:|
  | **Small** | SINGLE | 926 | +0.54 | 50.0 | 0.111 | 0.031 | 0.443 |
  | (drift +0.47%) | SELL | 171 | −0.03 | 50.3 | 0.902 | 0.908 | 1.000 |
  | | BUY | 187 | +0.16 | 46.0 | 0.651 | 0.692 | 1.000 |
  | | **MIXED** | 329 | **+1.40** | 54.4 | 0.124 | 0.008 | 0.494 |
  | **Mid** | SINGLE | 971 | +0.18 | 55.6 | 0.032 | 0.027 | 0.130 |
  | (drift +0.18%) | SELL | 246 | +0.35 | 56.5 | 0.036 | 0.026 | 0.145 |
  | | BUY | 290 | +0.05 | 52.8 | 0.776 | 0.778 | 1.000 |
  | | MIXED | 652 | +0.19 | 55.1 | 0.050 | 0.034 | 0.201 |
  | **Large** | SINGLE | 728 | +0.20 | 55.4 | 0.016 | 0.008 | 0.064 |
  | (drift +0.13%) | SELL | 237 | −0.01 | 51.5 | 0.959 | 0.976 | 1.000 |
  | | BUY | 242 | −0.05 | 53.7 | 0.754 | 0.758 | 1.000 |
  | | MIXED | 518 | +0.16 | 52.9 | 0.086 | 0.064 | 0.342 |
  | **Mega** | SINGLE | 624 | +0.10 | 53.2 | 0.290 | 0.284 | 1.000 |
  | (drift +0.19%) | SELL | 156 | +0.24 | 57.1 | 0.187 | 0.207 | 0.747 |
  | | BUY | 170 | −0.07 | 48.2 | 0.746 | 0.720 | 1.000 |
  | | MIXED | 257 | +0.26 | 56.0 | 0.086 | 0.095 | 0.344 |

  **Not one cell out of sixteen survives Bonferroni.** The single lowest raw p anywhere is Large/SINGLE (0.016 → Bonferroni 0.064, still > 0.05). The eye-catching Small/MIXED cell, despite its +1.40% point estimate, is cluster-p 0.124 and Bonferroni 0.494 — its standard error is huge. And the headline framing — *excess over the bucket's own drift* — kills it cleanly: Small/MIXED is **+0.93% excess, p=0.31**; no bucket's MIXED or directional cell has a significant excess at all. The faceted bars above (each bucket's types against its own dashed drift line) and the size-gradient line both make the same point visually — only one bar pulls away from drift, and the directional cells sit *below* it.

  ![Next-day return by sweep type, per bucket](fwd-return-by-bucket.png)

- **Why (mechanism).** Pool *all* sweep days against *all* trading days, per bucket, and the reason is plain — a sweep day is an ordinary day in every bucket:

  | Bucket | sweep-day mean | all-day mean | sweep-day %pos | all-day %pos |
  |---|---:|---:|---:|---:|
  | Small | +0.484% | +0.472% | 50.1% | 50.1% |
  | Mid | +0.179% | +0.184% | 55.4% | 55.1% |
  | Large | +0.130% | +0.127% | 53.5% | 53.6% |
  | Mega | +0.156% | +0.191% | 53.5% | 54.2% |

  Identical to within a basis point or two. The rolling-volume filter selects busy days, but busy days in these baskets are not special days — at any size.

- **What we checked.** The random same-names baseline (20,000 draws of the same number of distinct days from the *same bucket basket*) is decisive for the directional cells: in every bucket the observed BUY mean falls *below* most random draws (Small 32% below, Mid 15%, Large 9%, Mega 7% of draws lie below it) — a BUY sweep does not even beat picking the same names on random days.
- **Verdict.** **Null in all four buckets.** H0 is not rejected for any type at any size. The directional-flow (Kyle) prediction fails for BUY/SELL everywhere; the only cell that even *looks* like the size prior is Small/MIXED, which Finding 2 dismantles.

### Finding 2 — The small-cap "signal" is a handful of days — the size prior fails where it most appears

- **What we expected & why.** The size prior predicts the strongest sweep effect in the smallest, least-liquid bucket, and Finding 1's point estimate (+1.40% Small/MIXED) seems to deliver. A *real* small-cap edge would be spread across many days; a volatility artifact would be carried by a few extreme days and would blow up as you select for more extreme bars.
- **How we measured it.** Take the Small/MIXED daily series, sum it, and re-compute the mean after removing the largest-magnitude days; separately, sweep the Z threshold and re-read the cell:

  ```python
  x = small_mixed.next_day_ret                    # 329 trading days
  total      = x.sum()                            # five-year sum
  top5_share = x[abs(x).argsort()[-5:]].sum()     # the 5 wildest days
  mean_ex5   = x[abs(x).argsort()[:-5]].mean()    # mean without them
  for z in [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:        # threshold sensitivity
      recompute_small_mixed(z)
  ```

- **What the data shows.** The +1.40% is **five days wearing a trench coat.** Over five years the Small/MIXED series sums to **+462 percentage-points**; the **five largest-magnitude days alone contribute +335pp** of that. Strip those five and the mean drops from **+1.40% to +0.39%** — *below* the bucket's own +0.47% drift. Strip the top ten and it is +0.26%.

  ![The Small-bucket MIXED edge is a few days](small-mixed-episodes.png)

  The threshold sweep is the tell. As Z rises (selecting rarer, wilder bars), the Small/MIXED cell **explodes**: +0.92% (Z2.5) → +1.40% (Z3.0) → +3.14% (Z4.0) → +7.77% (Z5.0). A stable edge would be roughly flat in Z; a few-wild-days artifact runs away with it. Mid, Large and Mega stay pinned near their drift across the whole sweep.

  ![Threshold sensitivity of MIXED by bucket](threshold-by-bucket.png)

- **Why (mechanism).** A concrete case: in the Small basket, NVTS spikes up while AEHR spikes down in the same 15 minutes; the next day a single sub-$10B name gaps 12% on a product headline and the equal-weight basket lurches. The "MIXED edge" is not informed flow resolving — it is that **small, illiquid chips have fat-tailed daily moves**, and a 6-name equal-weight basket lets one of them dominate. The same toxic-tape configuration in the Mega bucket (NVDA up, INTC down) produces a +0.26% next-day blip that is statistically zero. Size does not amplify *information*; it amplifies *variance*.
- **What we checked.** The random-baseline panel for Small is itself **bimodal** — the small-cap basket's own random 329-day draws have a second hump out past +1% — which is *why* the observed +1.40% sits "above 98% of random" yet is still not an edge: the random benchmark is that volatile too. Mid/Large/Mega random distributions are tight single humps and the observed MIXED lands mid-pack (55%/66%/70% above random).

  ![MIXED vs random same-names entry, per bucket](random-baseline-by-bucket.png)

- **Verdict.** **The size prior is rejected.** The one cell that looked like "bigger effect in smaller names" is a five-day volatility artifact with an insignificant excess (p=0.31), a sign that runs away with the threshold, and a random benchmark just as wild as itself. Small caps host *louder noise*, not a *stronger signal*.

### Finding 3 — Nothing carries out-of-sample, in any bucket; size only changes the size of the surprise

- **What we expected & why.** A real edge — at any cap — carries its sign and rough magnitude into an untouched forward window. A noise edge does not; and if the noise is volatility-driven, the smallest bucket should *surprise the most* out-of-sample.
- **How we measured it.** A true chronological split per bucket (no peeking), plus a 10 bps round-trip cost haircut on the collapsed daily means:

  ```python
  train = daily[daily.trading_day <  "2024-10-01"]   # fit window
  hold  = daily[daily.trading_day >= "2024-10-01"]   # untouched forward window
  net   = gross_mean - 0.10                           # 10 bps round-trip, in %
  ```

- **What the data shows.** The MIXED cell, train → hold-out, by bucket:

  | Bucket | MIXED train | MIXED hold-out |
  |---|---:|---:|
  | Small | +0.46% | **+2.79%** |
  | Mid | +0.15% | +0.28% |
  | Large | +0.12% | +0.23% |
  | Mega | +0.32% | +0.10% |

  ![MIXED out-of-sample by bucket](oos-by-bucket.png)

  The small-cap cell behaves exactly as a volatility artifact should: it does not *persist* at +0.46%, it **leaps to +2.79%** out-of-sample — a *different* clutch of wild days, not the same edge showing up again. Mega goes the other way (+0.32% → +0.10%). The mid/large cells are small both windows but never significant (best hold-out p across all MIXED cells is 0.13). The full-39 universe tells the same story: SINGLE/SELL/MIXED all show low train means and "fresh" higher hold-out means (e.g. SELL +0.03% train → +0.62% hold-out, p=0.02) — the in-window flukes an OOS test exists to catch, with no sign-carry from training.

  **Costs.** A 10 bps round trip turns every BUY cell net-negative or flat (Small +0.06%, Mid −0.05%, Large −0.15%, Mega −0.17%) and trims every benign SINGLE/SELL tilt to single-basis-point territory; none is significant after the dependence adjustment. Only the Small/MIXED point estimate survives 10 bps numerically (+1.30% net) — but it is the five-day artifact, not a tradable series.

- **Why (mechanism).** A mean that *grows* out-of-sample rather than reverting toward its training value, and that grows most in the smallest bucket, is the signature of a series scattered around drift with fat tails — there is no underlying constant for the hold-out to confirm, only more episodes.
- **What we checked.** Costs are a stylized flat haircut; real fills on the mega names are cheaper than 10 bps, while the small names would be *more* expensive (wider spreads), so the cost test is, if anything, lenient on exactly the small-cap cell that looks best gross.
- **Verdict.** **Null in every bucket.** Fails out-of-sample everywhere; fails on costs for the directional cells. Size changes only the magnitude of the out-of-sample surprise — bigger in small caps — which is the opposite of a stable, size-dependent edge.

---

## Robustness — did we just find noise?

Pulled together as a stated goal: the three axes (a true forward hold-out, a 10 bps cost haircut, a Z-threshold sweep) are the "is this noise?" battery, and they were run *inside each bucket*. The small-cap MIXED cell fails all three in the most diagnostic way — it grows with the threshold, grows out-of-sample, and its random benchmark is as fat-tailed as itself. The other buckets never had a cell to break. The block bootstrap is the fourth leg: it agrees with the cluster t-tests in every bucket, so the null is not a quirk of one inference method. The episode-removal test (top-5 days carry +335pp of +462pp) is the clincher.

## Steelman the rival, then kill it

Three alternative explanations could each produce the surface appearance of a size-dependent sweep edge. Each is steelmanned, then tested on its own numbers.

**Rival A — small caps really are more informative (the size prior itself).** *Steelman:* the +1.40% Small/MIXED cell is the predicted "information travels slower in small caps" effect. *Test:* re-express it as excess over the *small-cap* drift and decompose by episode — **+0.93% excess, p=0.31**, of which the five wildest days carry +335 of +462 percentage-points; remove them and the mean falls *below* the bucket's own drift. **Rival A loses** — the small-cap "edge" is volatility, not information; the prior's *direction* shows up only in the noise amplitude.

**Rival B — it's just basket drift, bucket by bucket.** *Steelman:* each bucket rose over five years (Small fastest at +0.47%/day); any "in the market on selected days" rule inherits that drift. *Test:* re-express every cell as excess over its *own* bucket drift. Result — **no cell in any bucket has a significant excess**: every BUY excess is negative (−0.31% / −0.14% / −0.17% / −0.26%, small→mega), and the largest positive excess anywhere (Small/MIXED +0.93%) is insignificant. **Rival B wins** — every positive *level* is the bucket drifting up.

**Rival C — a few big episodes, not a stable edge.** *Steelman:* maybe a small real edge is masked by averaging. *Test:* the episode-removal and threshold-explosion results show the exact opposite — the apparent effect is *made of* a handful of days and runs away as you select for extremity. **Rival C describes the truth** — this is the signature of noise, concentrated in the smallest, most fat-tailed bucket.

The rivals that win (drift, a few episodes) are exactly the ones that imply *no tradable, size-dependent sweep signal*. The rival that would rescue the size prior (small caps genuinely more informative) is the one the data rejects.

---

## The answer, in the data

**Q: Do cross-ticker volume sweeps predict the basket's next-day return — and does the effect depend on company size?**

**A: No, and no.** Run inside four market-cap buckets and across the full 39-name universe, with honest inference — effective n, cluster-robust and block-bootstrap p-values, multiplicity correction, a random same-names baseline, a chronological hold-out, and a cost haircut — **no sweep type produces a next-day edge over its own basket's drift in any bucket.** The size prior (bigger effect in smaller names) appears only as a *point estimate* in the smallest bucket's MIXED cell, and that estimate is a five-day volatility artifact: insignificant in excess (p=0.31), exploding with the threshold (+7.77% at Z5.0) and out-of-sample (+2.79%), and benchmarked against a random distribution just as fat-tailed as itself. **Size scales the noise, not the signal.**

| Bucket | best raw cell | best cell mean | excess vs own drift (p) | survives Bonferroni? | survives OOS + costs? |
|---|---|---:|---:|:--|:--|
| Small (< $10B, n=6) | MIXED | +1.40% | +0.93% (0.31) | No (0.494) | No — 5-day artifact, explodes OOS |
| Mid ($10–100B, n=12) | SELL | +0.35% | +0.16% (0.32) | No (0.145) | No |
| Large ($100–500B, n=9) | SINGLE | +0.20% | +0.07% (0.38) | No (0.064) | No |
| Mega (> $500B, n=5) | SELL | +0.24% | +0.05% (0.79) | No (0.747) | No |
| **Full 39-name universe** | MIXED | +0.22% | +0.02% (0.76) | No (0.023→n.s. on excess) | No |

**The two questions, separated.** *Did the effect hold, and does it depend on size?* No on both — a clean null at every cap. *Was the method sound / what did we learn?* Yes: cutting the universe by size turned a single ambiguous null into a *diagnosis* — the place the folk belief looked truest (small, illiquid names) is exactly where volatility most easily counterfeits a signal, and the cap-bucket lens is what exposes the counterfeit. The live alternative we **cannot** fully exclude is that a finer order-flow tape (true signed volume rather than close-vs-open at 15-minute resolution) hides a small-cap MIXED effect this data is too coarse to see — so this is *inconsistent with* a tradable, size-dependent sweep signal, not a proof one can never exist. A clean null, now resolved across the size spectrum, is the result, and the right one.

## Caveats

- Backtest only; next-day *basket* returns, equal-weight, per bucket. The cost haircut is a stylized flat 10 bps and ignores that small-cap spreads are wider (direction: makes the small-cap cells look *better* than reality — the opposite of rescuing them).
- The Small bucket is only **6 names** and the Mega bucket only **5**; small baskets are inherently fat-tailed, which is itself part of the finding but limits the precision of those two cells (direction: widens their CIs, makes a true small effect harder to detect — yet none is found even so).
- Side is a close-vs-open bar proxy, not true signed volume; 15-minute bars are coarse. A finer tape could expose an effect this resolution cannot — but the burden of proof is on that data (direction: could only *add* a missed signal, not remove a found one).
- 7 ADR names lack share-count data and are dropped from bucketing; they remain in the full-39 test, which agrees with the buckets (direction: unknown, but the full-39 null matches).
- Single sector, one (mostly bull) regime; the per-bucket drift baseline absorbs the level effect, but generalization to other baskets/regimes is untested (direction: unknown).

## Reproducibility

**Market-cap bucketing (the cross-sectional split).** For each name: cap = (latest diluted average shares) × (latest daily close); assign to Small (< $10B) / Mid ($10–100B) / Large ($100–500B) / Mega (> $500B). Names with no share-count line are dropped from buckets, kept in the full-39 test.

**Sweep definition (the governing formula).** For ticker *i*, bar *t*, 60-bar rolling mean/std of volume, open-auction bar excluded:

```
Z_{i,t} = ( V_{i,t} − mean_60(V_i) ) / std_60(V_i)
qualify if  Z_{i,t} ≥ 3.0  and  bartime ≠ 09:30 ET
side_{i,t} = sign( close_{i,t} − open_{i,t} )
```

Group qualifying bars by timestamp *within the bucket*; classify by how many names print on each side (≥2 up = BUY, ≥2 down = SELL, both sides = MIXED, one name = SINGLE). Outcome = equal-weight next-day return of that bucket's basket.

**The two load-bearing inference steps, in code:**

```python
# 1) honest sample size — one observation per trading day per type per bucket
daily = events.groupby(["bucket", "trading_day", "type"]).first()

# 2) dependence-robust p-value — stationary (block) bootstrap, ~5-day mean block,
#    so short autocorrelated runs survive resampling intact
def stationary_bootstrap(x, mean_block=5, n_boot=10_000):
    out = []
    for _ in range(n_boot):
        idx, p = [], 1.0 / mean_block
        i = np.random.randint(len(x))
        while len(idx) < len(x):
            idx.append(i)
            i = np.random.randint(len(x)) if np.random.rand() < p else (i + 1) % len(x)
        out.append(np.mean(np.asarray(x)[idx]))
    return np.array(out)
```

Full pipeline (5-min→15-min resample, UTC→ET conversion, per-bucket event construction, the random-entry baseline, the OOS split, episode decomposition, and every chart) lives in the study's research notebook in the private method repo; the formulas and code boxes above reproduce the headline numbers from raw 15-minute bars. Source: 15-minute consolidated US equity aggregates for the 39 names + latest reported diluted shares and daily closes, 2021–2026, from a private warehouse.

## References & forward pointer

- Kyle, A. (1985). *Continuous auctions and insider trading.* Econometrica — informed order flow and linear price impact (the BUY-sweep prior).
- Easley, D., López de Prado, M. & O'Hara, M. (2012). *Flow toxicity and liquidity in a high-frequency world* (VPIN). Review of Financial Studies — balanced abnormal flow as toxic/noisy (the MIXED prior).
- Politis, D. & Romano, J. (1994). *The stationary bootstrap.* JASA — dependence-robust resampling behind the block-bootstrap p-values.
- Data: end-of-day and 15-minute consolidated US equity aggregates for the 39 names, plus reported diluted shares for the cap split, 2021–2026.

**Builds on / part of:** the repo-wide thread on *which short-horizon "edges" survive an honest test*. Shares the random same-names baseline with [study 09 — activist short post-performance](../09-activist-short-post-performance/) and the size-conditioning lens with [study 17 — semiconductor layers](../17-semiconductor-layers/).

**Next:** [study 07 — intraday decision-time](../07-intraday-overnight-decomposition/), which asks the same "describe vs trade" question one layer up — how early in the day the close is callable, and whether that mechanical predictability is actually tradable (it is not). Same lesson, different clock.
