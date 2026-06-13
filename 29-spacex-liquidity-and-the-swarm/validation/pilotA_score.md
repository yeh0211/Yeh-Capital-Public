# Pilot A score — 2001 telecom (validation run)

Seed: state of the telecom system as of 30 June 2001. Asked to simulate Q3 2001 - Q2 2003.
Report: report_46108d8ad571 (19.2k chars). Scored on mechanism breadth, NOT outcome recall
(the model's training data contains the 2001-2003 outcome).

## Mechanisms the swarm surfaced (5 of 5 of the seed's causal channels)

1. Carrier failure via inflated revenue + rigid debt + financing-window closure — and the
   report's tool calls homed in on WorldCom's margin/line-cost reconciliation, the actual
   fraud mechanism. The "WorldCom tell" (margins peers cannot reconcile) is exactly the
   open casting-call signal flagged for 2026. PASS.
2. Vendor financing as the loss-transfer channel — Winstar bankruptcy -> Lucent ~$700M
   exposure cited explicitly as the "early sample" of the mechanism. PASS.
3. Tier-1 differentiation — Lucent/Nortel deeper in vendor financing, Cisco healthier
   balance sheet but "not immune" to the order decline. Matches reality (Cisco survived,
   stock still fell ~75%). PASS.
4. Component cascade — JDSU falls later and harder, demand = carrier capex through "two
   layers of inventory," plus goodwill-writedown risk from stock-funded M&A. PASS.
5. Self-reinforcing loop reasoning: price down -> revenue down -> cashflow down ->
   capex down -> orders down, staged quarter by quarter Q3'01->Q2'03. PASS.

## Epistemic discipline (good)

Declined to invent specific impairment magnitudes: "the simulation did not provide
specific impairment amounts, so we cannot assert how large the writedowns will be."
This is the right restraint — it predicts direction and mechanism, not fake precision.

## Limitations (critical for the SpaceX run)

- CONTAMINATION: outcomes are in training data. This validates machinery (mechanism
  discovery, persona-fact grounding, staged causal path, magnitude restraint) — NOT foresight.
- The swarm extrapolates the SEED's causal structure forward; it grounds almost every claim
  on a seed fact ("模拟事实显示..."). It does NOT inject exogenous surprises (a 9/11, a
  surprise rate move). So for SpaceX, the swarm will rehearse the consequences of the
  mechanisms we put in the seed — its value is tracing second/third-order effects and
  ordering, not forecasting a bolt from the blue.
- No quantified price paths; timing only to quarter granularity.

## Verdict

Machinery VALIDATED for mechanism rehearsal. Use the swarm as the third evidence layer:
it traces how the casting-table mechanisms cascade and in what order. Outcome claims stay
owned by the backtests (Ch1-3) and the bootstrap cone (Ch4a). The only blind test is the
SpaceX run, scored against reality at each unlock date.
