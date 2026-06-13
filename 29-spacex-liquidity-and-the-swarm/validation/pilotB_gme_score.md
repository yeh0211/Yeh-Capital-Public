# Pilot B-GME score — GameStop squeeze (validation run, study-29-specific)

Seed: market state as of 22 Jan 2021 (facts only — short interest, forum, gamma loop,
NSCC clearing, sister names — outcome NOT stated). Report: report_68904b558cbc (19.3k chars).
Scored on mechanism breadth; GME 2021 is in training data, so this validates machinery +
reasoning, not foresight. The decisive test: does the swarm find the buy-side plumbing halt?

| Channel | Result | Detail |
|---|---|---|
| 1. Price path & peak timing | PASS | Peak window "late Jan, around the broker restriction"; vertical-then-stairstep decline. Correct (Jan 27-28). Refused to fabricate price levels the sim didn't produce — good discipline. |
| 2. Broker halt via clearing collateral | **STRONG PASS** | Found NSCC + T+2 + escalating collateral, AND made the seed-absent deduction: "the peak occurs when the BUY CHANNEL is constrained, not when sellers overwhelm buyers." It inferred the top coincides with the buy restriction. |
| 3. Short side | PASS | Melvin + peers shift from holding to seeking exit; de-grossing as upward fuel. |
| 4. Broad-market spillover | PARTIAL PASS | Identified the de-grossing channel (funds compress other positions to cut risk; MMs tighten risk-warehousing) but honestly gave no magnitude/duration. Mechanism right, no number. |
| 5. Sister meme names | PASS | Named all five (AMC/BB/KOSS/EXPR/NOK), correctly framed as a "high-short, squeezable" basket, not a fundamental cohort. |
| Bonus | PASS | Correctly identified Citadel Securities as the dominant market maker. |

## The decisive finding (why this pilot matters for the SpaceX question)

The seed listed the clearing-collateral fact as one bullet but did NOT say the price peaks
when buying is constrained. The swarm REASONED to that ordering: the top is set by a
*supply-of-buying* constraint, not by sellers exhausting buyers. That is the exact
structural question study 29 asks of SpaceX — whether the absorption/plumbing side
(index demand vs unlock supply, lockup mechanics) governs the price path. The swarm found
the plumbing-binds-the-price logic unprompted in the GME case. That earns the swarm a
genuine (caveated) role on the SpaceX run, not just narrative color.

## Caveats (same as study 30's pilots)
- Contamination: outcome in training data; seed contained the collateral fact. Genuine
  value-add = the causal ORDERING (buy-constraint marks the top), which was seed-absent.
- No quantified price path; spillover magnitude declined (honestly).
- The swarm still grounds heavily on seed facts; it extrapolates structure, no surprises.

## Verdict
5/5 channels surfaced; the non-obvious plumbing halt found with correct causal ordering.
Combined with study 30's general validation (12/16 contamination-adjusted), the swarm is
validated as a mechanism/ordering rehearser. Cleared to run on SpaceX as the 3rd evidence
layer; outcome probabilities stay owned by the backtests (Ch1-3) and the bootstrap cone (Ch4a).
