# Research plan — beyond semiconductors: a multi-sector expansion

**Status:** plan / not yet executed · **Owner:** Hsin Cheng Yeh · **Drafted:** 2026-06

Notes **07–19** form one connected program built around a single question — *is 2026 a 2000 echo for **semiconductors**, and which "edges" survive an honest test?* The machinery built to answer it (concentration/breadth, supply-chain layer decomposition, event studies, conditional shorts, persistence tests, all run through the same OOS + bootstrap + random-baseline harness) is **not semiconductor-specific**. This plan reuses that machinery across more sectors to answer the broader question:

> **Are the structural facts we documented in semis — extreme concentration, no winner-persistence, null event alpha, "overbought ≠ short" — properties of *one hot sector*, or properties of *the market right now*?**

The honesty-first contract is unchanged: nulls and decayed results get published, every claim states its universe/window/threshold/metric, and nothing graduates to "interesting" until it survives a larger out-of-sample test.

---

## 1. Why expand, and what stays fixed

**Why.** A finding from a single sector in a single regime (an AI-driven bull leg, 2022–2026) is fragile. Re-running each semi result across 8–10 sectors does three things at once: (a) **stress-tests** every existing claim out-of-domain — the strongest possible robustness check; (b) **isolates** what is genuinely a 2026-market fact from what is a semis quirk; and (c) **extends the dot-com-echo thesis** downstream — the AI build-out does not stop at the chip; it runs into power, cooling, networking, software and the balance sheets that finance it.

**What stays fixed (the invariants).** Every new study reuses the published method stack, so results stay comparable to 07–19:

- cap-weighted-vs-equal-weighted proxy from split-adjusted closes × implied shares (as in 11);
- Spearman information coefficient + quintile sorts for persistence/leadership (11, 16);
- CAAR / abnormal-return event study **measured relative to the sector ETF, not raw** (08, 18) — the single most important discipline, since 18 showed raw "alpha" is mostly sector beta;
- conditional vs blind/random-entry baselines so drift is never mistaken for signal (01, 19);
- dependence-adjusted t-tests, multiplicity correction, bootstrap CIs, and an explicit out-of-sample / walk-forward split on every headline number;
- survivorship and proxy caveats stated up front.

If a result needs a method we haven't published, that method ships as its own note first.

---

## 2. Sector selection

**Criteria.** Each candidate sector must clear four gates: **(i) public data** — a liquid cap- and equal-weighted ETF pair plus reconstructable constituent closes; **(ii) a clear leadership structure** to test concentration/persistence against; **(iii) datable catalysts** (launches, readouts, awards, prints) for the event-study leg; **(iv) a thesis link** to the AI build-out or the 2000-echo question, so the program stays connected rather than sprawling.

**Shortlist, by priority tier** (ETF pairs are cap-weight / equal-weight stand-ins, same role as SOXX/XSD and QQQ/QQEW in 11):

| Tier | Sector | Cap / Equal proxy | Why it's in, thesis link |
|---|---|---|---|
| **1** | Power & electrification (utilities + IPPs + grid/cooling) | XLU / RYU, plus VST·CEG·NRG·GEV·VRT·ETN names | The AI build-out's downstream bottleneck; the cleanest extension of the semi story into a *different* sector with the *same* driver. |
| **1** | Software / SaaS & cloud | IGV / equal-weight basket | Already half-touched in 08; the "AI eats software or feeds it" question; classic concentration. |
| **1** | Communication services / mega-cap platforms | XLC / equal-weight | The most concentrated sector of all (GOOGL+META); direct test of whether 11's concentration is *more* extreme outside semis. |
| **2** | Financials & banks (incl. regionals) | XLF·KRE / RYF | The SVB confound surfaced in 08 and 13; tests concentration/breadth in a *non-tech* sector. |
| **2** | Healthcare — diagnostics & biotech | XBI·IHI / equal-weight | Ties to the Tempus tracker (03) and activist-short names (09); GLP-1 readouts are ideal event-study fuel. |
| **2** | Defense & aerospace | ITA / equal-weight | Catalyst-rich (contract awards), low correlation to AI beta — a true out-of-domain check. |
| **3** | Energy (oil & gas / midstream) | XLE / RYE | Concentration + a *value* counterweight to the growth sectors above. |
| **3** | Industrials / EVs & batteries | XLI·LIT / RYJ | A second supply-chain decomposition vertical to test 17 out-of-domain. |
| **3** | Crypto-equities & digital-asset infra | custom basket | Extends 04 and 13 from asset to equity layer. |

Tier 1 is built first (strongest data + tightest thesis link); Tiers 2–3 follow as the templates prove out.

---

## 3. The expansion matrix — existing study → cross-sector generalization

Each row is an existing semi result and the new study that tests whether it generalizes. New notes slot in at **20+**, continuing the numbering.

| Existing | What it found (semis) | New study | Cross-sector question | Prior hypothesis |
|---|---|---|---|---|
| **11** concentration + persistence | NVDA = 50% of gain; winners don't persist (IC ≈ 0) | **20 — Concentration across sectors** | Is one-name dominance and no-persistence a market-wide regime? | Concentration generalizes (Comm Svcs *worse*); persistence-null generalizes. |
| **16** breadth/leadership timing | No breadth warning survives | **(folded into 20)** | Does the breadth null hold per sector? | Yes — still untradable. |
| **17** supply-chain layers | Only 6/13 layers beat SMH; rest is beta | **21 — Power & electrification layers** | Which AI-power layer leads, and how much is just utility/AI beta? | Real exposure exists but is mostly sector beta. |
| **17** (template) | — | **22 — A second vertical's layers** (biotech *or* EV/battery) | Does the layer-decomposition template replicate out-of-domain? | Same dilution-to-beta result. |
| **08 / 18** event studies | Abnormal vs ETF ≈ 0; raw moves are beta | **23 — Flagship-catalyst event study** (Apple keynotes, GLP-1 readouts, defense awards, delivery days) | Do marquee catalysts beat the *sector* tape anywhere? | Mostly null vs sector ETF, as in 18. |
| **09** activist shorts | No tradable post-report drift | **(extended in 23)** | Does publisher-only structure recur in non-tech targets? | Indicative, not significant (small n). |
| **19** conditional short | Overbought ≠ short signal; melt-up risk | **24 — Shorting overbought, everywhere** | Does the overbought-short null hold across sector ETFs? | Yes — null replicates; deepest setups are worst shorts. |
| **02 / 15** IPO behavior | IPO chase loses ~28%/yr; only REITs + profitable software survive | **25 — IPO aftermarket by sector** | Which sectors' IPOs (if any) survive the aftermarket, on bigger samples? | Survivors stay narrow (cash-flow + hard-asset). |
| **13** collapse insurance | BTC is a risk asset; gold protects | **26 — What actually hedges a selloff** | Across the 8 SPY selloffs, which hedges (TLT, DXY, utilities, staples, low-vol) truly protect? | Duration + defensives protect; "growth hedges" don't. |
| **07** intraday decision-time | Morning calls the close; rest-of-day untradable | **(optional)** intraday decomposition on a non-tech ETF | Is the rest-of-day coin-flip universal? | Yes — mechanical overlap, no edge. |
| **10** Korea memory/leverage | No death spiral on the proxy | reused as a single-market case, not generalized | — | — |

**Capstone — 27: The 2000 echo, cross-sector.** Synthesis note. Score every sector on a common dot-com-echo index — concentration (Herfindahl, top-1 share), valuation dispersion, IPO froth, breadth deterioration, cap-vs-equal gap — and rank which sector *today* most resembles 1999 internet/semis. This closes the loop the 07–19 program opened, now with cross-sector evidence instead of one sector.

---

## 4. Phasing

**Phase 0 — scaffolding (1 sprint).** Generalize the private pipeline's universe builder from "semi SIC classes" to a sector parameter; define the ETF cap/equal pairs in §2; write a shared sector-panel spec (window 2022-01 → 2026-06, split-adjusted, common-panel start) so all new notes are directly comparable to 11/17/19. No findings yet — infrastructure and a reproducibility checklist.

**Phase 1 — Tier-1 breadth (Studies 20, 21).** Concentration-across-sectors (20) and the power/electrification layer decomposition (21). These are the highest-signal, best-data extensions and they validate the scaffolding.

**Phase 2 — generalize the harness (Studies 22, 23, 24).** Second layer-vertical (22), flagship-catalyst event study (23), overbought-short replication (24). Each is a direct re-run of a published method on new universes — fast to execute once Phase 1 proves the panel.

**Phase 3 — cross-asset + synthesis (Studies 25, 26, 27).** IPO-by-sector (25), selloff-hedge map (26), and the 2000-echo capstone (27) that ties the whole expansion back to the original question.

Each study ships in the existing format: `NN-slug/README.md` (hypothesis → data & method → claims with figures → "the answer, in the data" → caveats → references), a `meta.json`, and its figures — then a one-row addition to the root `README.md` table.

---

## 5. Expected-results discipline (pre-registration)

To keep the program honest, each study's **prior hypothesis is written above before the data is run** (the §3 table). The interesting outcomes are the *surprises* against these priors — e.g. if a sector *does* show winner-persistence where semis didn't, or a catalyst that *does* beat its sector ETF. Given the base rate of 07–19 (most results are nulls), the honest expectation is that **most of these generalize as nulls**, and the deliverable value is the *map* of which structural facts are market-wide vs sector-specific — not a basket of new "signals."

## 6. Risks & guardrails

- **Sprawl.** Hard cap at the Tier-1/2 sectors until a template has produced at least one published note; Tier-3 only after. The capstone (27) exists to force synthesis over accumulation.
- **One regime.** Every note repeats the 2022–2026 single-regime caveat; where a longer ETF history exists (XLU, XLF, XLE pre-date the window), extend the backtest and say so explicitly.
- **Proxy error.** Cap-weight remains a closes × implied-shares proxy, ETF pairs remain stand-ins for true cap/equal weights — stated as in 11.
- **Survivorship.** Common-panel construction biases the cross-section upward; disclosed per note, and where it matters, re-run with a delist-inclusive panel.
- **Data gates.** Any sector that fails the §2 data gate (e.g. a single-name limb that is data-blocked, as in 10) is published as a *hedged conditional*, not dropped silently.
- **No third-party material** is reproduced; sector context informs framing only, never content.

---

### One-line summary

Reuse the semiconductor program's honest-test harness across ~8 sectors to separate **2026-market facts** (concentration, no persistence, null event-alpha, overbought≠short) from **semiconductor quirks** — and rank which sector today most resembles the 2000 echo. Built in three phases, nulls published, every prior pre-registered.
