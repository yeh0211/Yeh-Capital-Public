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
| 04 | [License-driven crypto-infra M&A](04-license-driven-crypto-ma/) | Why does the CLARITY/GENIUS regime make a money-transmitter licence stack the strategic asset, and who holds it? | Maps the public licence landscape + a decade of public licence-driven deals; identifies the pattern, not named targets. |
| 05 | *News-sentiment signal validation* | *(in progress — awaiting sufficient realised forward-return history)* Does a sentiment × source-trust × recency score predict forward returns out-of-sample? | — |
| 06 | *Crypto token market structure* | *(linked paper)* How does blockchain infrastructure shape token risk-return and monetary function? | Co-authored, accepted at ICMAIF 2026. |
| 07 | [Intraday vs close](07-intraday-overnight-decomposition/) | Where does a semi's daily return come from — the overnight gap or the session? | Overnight drives the *leaders* (NVDA +480% vs +130% intraday) but only 56% of names; intraday momentum doesn't replicate; direction is set early (corr 0.6 by 10:00 ET). |
| 08 | [AI model-launch event study](08-ai-model-launch-event-study/) | Does a frontier model launch reliably move the compute complex? | The bullish "pop" is a coin flip and faded since 2023; only the DeepSeek efficiency shock reliably hit NVDA (−17%, largely retraced), and it rests on one episode. |
| 09 | [Activist short post-performance](09-activist-short-post-performance/) | Do short reports on AI/quantum names play out, or get bought back? | All four 2024–26 campaigns were faded within 3–6 months; the valuation short (IonQ) roughly doubled. Regime-dependent vs classic fraud shorts. |
| 10 | [Korea memory cycle + leverage](10-korea-memory-cycle-leverage/) | Why did the DRAM empire move to Korea, and is its retail leverage a 2026 risk? | DRAM is the textbook capital cycle; a record 38tn-won retail-margin base now rides a memory-driven KOSPI — the forced-liquidation cascade is primed. |
| 11 | [Semiconductor concentration](11-semiconductor-concentration/) | When one stock supplies >40% of an index's gain, what comes next? | NVDA is 37% of a semis proxy and 44% of its 5y gain; concentration peaked in 2024 then resolved by *broadening*, not a crash. Five hypotheses, separated. |
| 12 | [GOOGL five-year hold](12-googl-five-year-hold/) | What did a five-year GOOGL hold return, and where is it now? | +220% (≈26% CAGR), $10k → ~$32k, but it lagged the +360% NVDA-driven semis complex; −44% drawdown en route. |

*Studies 07–12 form one connected program — is 2026 a 2000 echo for semiconductors?*

## Method notes

- **Validation:** out-of-sample / walk-forward splits, bootstrap confidence intervals, Spearman information coefficient, hit-rate, t-tests with reported p-values; multiple-comparison adjustment where relevant.
- **Honesty first:** null and decayed results are published, not hidden. A signal only graduates to "interesting" after it survives a larger, out-of-sample test.
- **Reproducibility:** each note states its universe, window, thresholds, and metric so the result can be challenged.

## About

Final-year BSc Business with Finance, Bayes Business School (City St George's, University of London). Research analyst experience in cross-border capital markets. Interested in systematic strategy, market microstructure, and the boundary between fundamental and quantitative research.

*Contact details on request.*
