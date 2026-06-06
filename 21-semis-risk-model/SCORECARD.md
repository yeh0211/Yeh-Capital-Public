# Scorecard — semiconductor risk-overlay model

Append-only log of the deterministic dial's monthly call, graded against realized forward outcomes on the cap-weighted semis proxy. Research only; no live capital.
Every row is **reconstructed** — the dial is replayed on history with no look-ahead (exposure decided at each month-start close, graded on the proxy's next 20 / 60 trading-day return). The forward columns read `(pending)` until the horizon has elapsed. "Ext" is the proxy's percentage extension above its 200-day average. "Call right (20d)" scores a de-risked month as right if the proxy fell over the next 20 days, and a full month as right if it rose.

| Date | Source | Safety | Dial | Ext | Proxy fwd20 | Proxy fwd60 | Call right (20d) |
|---|---|---|---|---|---|---|---|
| 2023-01-03 | reconstructed | RED | 0.5 | -0.09 | +24.3% | +32.9% | False |
| 2023-02-01 | reconstructed | GREEN | 1.0 | 0.15 | -1.9% | +1.9% | False |
| 2023-03-01 | reconstructed | GREEN | 1.0 | 0.11 | +8.9% | +22.9% | True |
| 2023-04-03 | reconstructed | GREEN | 1.0 | 0.22 | -5.5% | +18.3% | False |
| 2023-05-01 | reconstructed | GREEN | 1.0 | 0.15 | +21.9% | +29.8% | True |
| 2023-06-01 | reconstructed | GREEN | 1.0 | 0.36 | +4.3% | +4.0% | True |
| 2023-07-03 | reconstructed | GREEN | 1.0 | 0.36 | +4.2% | -7.8% | True |
| 2023-08-01 | reconstructed | GREEN | 1.0 | 0.34 | -2.5% | -13.0% | False |
| 2023-09-01 | reconstructed | GREEN | 1.0 | 0.24 | -6.5% | +2.9% | False |
| 2023-10-02 | reconstructed | GREEN | 1.0 | 0.12 | -5.3% | +20.9% | False |
| 2023-11-01 | reconstructed | GREEN | 1.0 | 0.05 | +12.0% | +36.6% | True |
| 2023-12-01 | reconstructed | GREEN | 1.0 | 0.14 | +5.9% | +38.2% | True |
| 2024-01-02 | reconstructed | GREEN | 1.0 | 0.17 | +12.9% | +39.5% | True |
| 2024-02-01 | reconstructed | GREEN | 1.0 | 0.28 | +19.2% | +18.3% | True |
| 2024-03-01 | reconstructed | GREEN | 1.0 | 0.43 | +3.6% | +16.5% | True |
| 2024-04-01 | reconstructed | GREEN | 1.0 | 0.40 | -4.2% | +19.7% | False |
| 2024-05-01 | reconstructed | AMBER | 0.5 | 0.21 | +20.0% | +19.2% | False |
| 2024-06-03 | reconstructed | GREEN | 1.0 | 0.40 | +8.7% | +3.3% | True |
| 2024-07-01 | reconstructed | GREEN | 1.0 | 0.42 | -13.8% | -3.2% | False |
| 2024-08-01 | reconstructed | AMBER | 0.5 | 0.16 | +5.1% | +17.3% | False |
| 2024-09-03 | reconstructed | AMBER | 0.5 | 0.08 | +7.0% | +13.4% | False |
| 2024-10-01 | reconstructed | AMBER | 0.5 | 0.11 | +11.9% | +13.9% | False |
| 2024-11-01 | reconstructed | GREEN | 1.0 | 0.13 | +1.5% | -1.1% | True |
| 2024-12-02 | reconstructed | GREEN | 1.0 | 0.10 | +0.9% | -11.4% | True |
| 2025-01-02 | reconstructed | GREEN | 1.0 | 0.10 | -7.5% | -17.7% | False |
| 2025-02-03 | reconstructed | RED | 0.5 | -0.00 | -5.4% | -10.5% | True |
| 2025-03-03 | reconstructed | RED | 0.5 | -0.09 | -5.7% | +14.1% | True |
| 2025-04-01 | reconstructed | RED | 0.5 | -0.13 | +0.5% | +38.2% | False |
| 2025-05-01 | reconstructed | RED | 0.5 | -0.09 | +16.7% | +46.0% | False |
| 2025-06-02 | reconstructed | GREEN | 1.0 | 0.07 | +11.9% | +25.5% | True |
| 2025-07-01 | reconstructed | GREEN | 1.0 | 0.17 | +11.6% | +18.0% | True |
| 2025-08-01 | reconstructed | GREEN | 1.0 | 0.22 | +1.3% | +20.8% | True |
| 2025-09-02 | reconstructed | GREEN | 1.0 | 0.19 | +12.6% | +15.3% | True |
| 2025-10-01 | reconstructed | GREEN | 1.0 | 0.32 | +11.2% | +6.0% | True |
| 2025-11-03 | reconstructed | GREEN | 1.0 | 0.38 | -5.3% | +2.0% | False |
| 2025-12-01 | reconstructed | GREEN | 1.0 | 0.25 | +1.8% | +7.4% | True |
| 2026-01-02 | reconstructed | GREEN | 1.0 | 0.24 | +4.5% | -2.1% | True |
| 2026-02-02 | reconstructed | GREEN | 1.0 | 0.23 | -3.5% | +18.0% | False |
| 2026-03-02 | reconstructed | GREEN | 1.0 | 0.16 | -10.9% | +33.4% | False |
| 2026-04-01 | reconstructed | GREEN | 1.0 | 0.07 | +23.2% | (pending) | True |
| 2026-05-01 | reconstructed | GREEN | 1.0 | 0.27 | +16.8% | (pending) | True |
| 2026-06-01 | reconstructed | GREEN | 1.0 | 0.41 | (pending) | (pending) |  |

## Grade so far

- Resolved rows (20-day horizon elapsed): 41.
- When DE-RISKED (dial < 1, n = 9): mean proxy fwd-20d **+8.3%**.
- When FULL (dial = 1, n = 32): mean proxy fwd-20d **+4.1%**.
- Directional call-right rate (20d): **56%** (n = 41).
- De-risk value (full minus de-risk fwd-20d): **−4.2pp**.

Read this honestly. The dial de-risked *into strength* more often than into weakness — the de-risk value is negative, the wrong sign for a market timer. A call-right rate of 56% is barely above a coin flip. This is exactly what the study concludes: the model is a **drawdown-reducer, not a direction predictor**. Its value is in the path (shallower losses), which the regime and bucket tables show, not in calling tops. The private judgment layer is graded separately and is not published here.
