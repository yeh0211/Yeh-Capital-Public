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
| 04 | *News-sentiment signal validation* | *(in progress — awaiting sufficient realised forward-return history)* Does a sentiment × source-trust × recency score predict forward returns out-of-sample? | — |
| 05 | *Crypto token market structure* | *(linked paper)* How does blockchain infrastructure shape token risk-return and monetary function? | Co-authored, accepted at ICMAIF 2026. |

## Method notes

- **Validation:** out-of-sample / walk-forward splits, bootstrap confidence intervals, Spearman information coefficient, hit-rate, t-tests with reported p-values; multiple-comparison adjustment where relevant.
- **Honesty first:** null and decayed results are published, not hidden. A signal only graduates to "interesting" after it survives a larger, out-of-sample test.
- **Reproducibility:** each note states its universe, window, thresholds, and metric so the result can be challenged.

## About

Final-year BSc Business with Finance, Bayes Business School (City St George's, University of London). Research analyst experience in cross-border capital markets. Interested in systematic strategy, market microstructure, and the boundary between fundamental and quantitative research.

*Contact details on request.*
