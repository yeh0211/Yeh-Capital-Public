# Scorecard — semiconductor risk-overlay model

Append-only log of the model's live calls, graded against realized forward outcomes. The point is an
honest, dated track record to optimize against — not a recommendation. Research only; no live capital.

How to read it: each row is the model's posture on a date. The realized-forward columns are filled in
later (20 and 60 trading days on), so the calls are scored against what actually happened, not curve-fit.

| Date | Safety state | Net-long dial | Leadership | Posture | SOXX fwd 20d | SOXX fwd 60d |
|---|---|---|---|---|---|---|
| 2026-06-05 | RED | 0.50 | risk-on | core at half; defined-risk hedge armed; no new longs except a high-volume washout | (pending) | (pending) |

Notes:
- "Net-long dial" 1.0 = full long, 0.5 = de-risked. It halves when the index loses its 200-day average
  or falls >10% off its 60-day high.
- The fwd columns grade the *systematic* posture. The private judgment layer is graded separately and is
  not published here.
