# yeh-capital — research notes

Independent quant and markets research by **Hsin Cheng Yeh**. Each note is a self-contained study: a hypothesis I formed, the data and method, the result (including when the result is *no effect*), and honest caveats.

The data pipeline that produces these results is operated privately. This repository publishes **method and findings only** — not infrastructure, credentials, or any third-party confidential work.

> All studies are research / backtested. No live capital, no audited track record. Metrics are reported as method, with confidence intervals and out-of-sample tests, not as a return stream.

## Notes

| # | Study | Question | Finding |
|---|---|---|---|
| 01 | [Volume-sweep microstructure](01-volume-sweep-microstructure/) | Do cross-ticker abnormal-volume sweeps predict next-day semi-basket returns? | Pilot signal decayed out-of-sample (p 0.002 → 0.08); a two-sided "MIXED" sweep effect survived (p≈0.008) and warrants follow-up. |
| 02 | [IPO-anchored VWAP, US + Asia](02-ipo-anchored-vwap/) | Is a VWAP anchored to the IPO date a more meaningful level than a generic anchor, across 202 US & Asian semis? | No significant edge (CIs overlap); the golden cross underperformed its reputation (36% vs predicted 55-65%). Two priors falsified. |
| 03 | [Due-diligence news hub](03-due-diligence-news-hub/) | Can fragmented, mixed-reliability sources be turned into a verified, source-scored event timeline for a single name? | A single-name DD pipeline with an independent verification gate (confidence > 70) separating verified fact from chatter. |
| 04 | [License-driven crypto-infra M&A](04-license-driven-crypto-ma/) | Why does the CLARITY/GENIUS regime make a money-transmitter licence stack the strategic asset, and who holds it? | Maps the public licence landscape + a decade of licence-driven deals (~$3.1bn across 7); GENIUS is law, CLARITY cleared Senate Banking (15-9) — identifies the pattern, not named targets. |
| 05 | *News-sentiment signal validation* | *(in progress — awaiting sufficient realised forward-return history)* Does a sentiment × source-trust × recency score predict forward returns out-of-sample? | — |
| 06 | *Crypto token market structure* | *(linked paper)* How does blockchain infrastructure shape token risk-return and monetary function? | Co-authored, accepted at ICMAIF 2026. |
| 07 | [Intraday vs close](07-intraday-overnight-decomposition/) | Where does a semi's daily return come from — the overnight gap or the session? | Overnight drives the *leaders* (NVDA +480% vs +130% intraday) but only 56% of names; intraday momentum doesn't replicate; direction is set early (corr 0.6 by 10:00 ET). |
| 08 | [AI model-launch event study](08-ai-model-launch-event-study/) | Does a frontier model launch reliably move the compute complex? | No — at the honest n=19, the bullish pop is statistically zero (bootstrap CI straddles 0, placebo p=0.95); only the one-off DeepSeek efficiency shock hit NVDA (−17%, largely retraced). |
| 09 | [Activist short post-performance](09-activist-short-post-performance/) | Do short reports on AI/quantum names play out, or get bought back? | All four 2024–26 campaigns were faded within 3–6 months; the valuation short (IonQ) roughly doubled. Regime-dependent vs classic fraud shorts. |
| 10 | [Korea memory cycle + leverage](10-korea-memory-cycle-leverage/) | Why did the DRAM empire move to Korea, and is its retail leverage a 2026 risk? | DRAM is the textbook capital cycle (Korea's 45y index: 4 drawdowns, median −48%); a 3.8σ, +145% melt-up now rides on record ~36tn-won retail margin — the forced-liquidation cascade is primed. |
| 11 | [Semiconductor concentration](11-semiconductor-concentration/) | When one stock supplies >40% of an index's gain, what comes next? | NVDA is 37% of a semis proxy and 44% of its 5y gain; concentration peaked in 2024 then resolved by *broadening*, not a crash. Five hypotheses, separated. |
| 12 | [GOOGL five-year hold](12-googl-five-year-hold/) | What did a five-year GOOGL hold return, and how does it rank among the megacaps? | +225% (≈27% CAGR, Sharpe 0.92) — but #2 of five megacaps and beaten by the equal-weight basket (+335%); NVDA (+1,233%) was the cycle. |
| 13 | [Gold: collapse insurance?](13-gold-collapse-insurance/) | When equities collapse, does gold rise — or is it driven by something else? | A real-rate trade, not a crash hedge: gold falls ~0.09%/bp on the 10y real yield (t −7.7); median just +3% across 8 Nasdaq drawdowns ≥15%. |
| 14 | [Alphabet's investment book](14-alphabet-investment-portfolio/) | Is Alphabet's private-stake portfolio material to the equity story? | Yes — mark-ups added ~$24bn (≈18% of 2025 net income); the private book grew $35→$64bn, and the surge is sector-wide across megacaps. |
| 15 | [Should you chase IPOs?](15-ipo-chase/) | Do new listings pay off if you buy in the aftermarket? | No — ≈+24% first-day pop then −21.6% vs market over 3yr; de-SPACs −75%, tiny deals −52%; the index-inclusion pop has decayed to ~0. |
| 16 | [Narrow leadership & the index](16-narrow-leadership-and-the-index/) | When mega-caps carry the index and breadth thins, is that bearish — and can you time it? | No, on all counts (10y, OOS): MAG7-leadership IC +0.01; only 3/13 sectors beat the S&P; "narrow at highs" isn't bearish (fwd +4.0% vs +3.3%); a drawdown model fails OOS (AUC 0.14). Concentration is a risk-management issue, not a timing signal. |
| 17 | [Semiconductor supply-chain layers](17-semiconductor-layers/) | Which layer leads, how does money flow across them, and does price drive the chatter? | Across a complete 133-name / 13-layer sweep (≥$100M): leadership sits on the periphery (power-gen +1,000%, EMS +681%, photonics +630% vs hyperscalers +175%, solar +36%); layers co-move (no chain lead-lag); price drives the chatter, which then rides momentum (+2.4% fwd alpha; curated X +7.3%). |
| 18 | [Computex event study](18-computex-event-study/) | Do the chip names that headline or supply Computex beat the semis tape after the keynote? | No robust alpha — abnormal vs SMH is statistically zero at every horizon (0 of 40 cells significant) and flips sign across robustness cuts (drop-2021 +1.2%, pre-2021 listings −2.4%); the median name beats SMH less than half the time. Own SMH, not the basket. |

*Studies 07–12 form one connected program — is 2026 a 2000 echo for semiconductors?*

## Data

- [**Computex Data Library** (2024–2026)](computex-dataset/) — 33 keynote / press sessions and **373 structured product announcements** (company · ticker · product · ship quarter · grounding quote · source video), as CSV + JSON under CC-BY. Derived data and links only; rebuild the transcripts from the public videos with the included script. Backs [study 18](18-computex-event-study/).

## Method notes

- **Validation:** out-of-sample / walk-forward splits, bootstrap confidence intervals, Spearman information coefficient, hit-rate, t-tests with reported p-values; multiple-comparison adjustment where relevant.
- **Honesty first:** null and decayed results are published, not hidden. A signal only graduates to "interesting" after it survives a larger, out-of-sample test.
- **Reproducibility:** each note states its universe, window, thresholds, and metric so the result can be challenged.

## About

Final-year BSc Business with Finance, Bayes Business School (City St George's, University of London). Research analyst experience in cross-border capital markets. Interested in systematic strategy, market microstructure, and the boundary between fundamental and quantitative research.

*Contact details on request.*
