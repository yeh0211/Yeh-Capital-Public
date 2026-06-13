# Pre-registered rubric — Pilot A (2000-03 telecom backtest), written BEFORE any simulation run
Cutoff of seed information: 30 June 2001. Known ground truth (not in the seed):
WorldCom fraud revealed June 2002, Chapter 11 July 2002 (then-largest US bankruptcy); Lucent revenue ~$30B FY2000 -> ~$12B FY2002 (~-60%), survives only via merger (Alcatel 2006); Nortel revenue collapses (Q4-01 $3.4B), ultimately bankrupt 2009; JDSU revenue $3.2B FY01 -> $676M FY03 (-79%, worse than tier-1) + $44.8B goodwill writedown (largest annual loss in history at the time); Cisco falls but survives on FCF + no vendor financing; the cascade amplifies away from final demand.

## Scoring (each 0/1/2: 0 = wrong/absent, 1 = partially right, 2 = clearly right)
1. DEMAND-LAYER FAILURE: a major carrier fails within the window (2 if a large acquisitive long-distance carrier fails on debt/accounting; 1 if only small CLECs fail; 0 if none).
2. ACCOUNTING MECHANISM: the simulation surfaces accounting fragility/restatement at a major carrier as a trigger or accelerant (2 explicit; 1 vague "confidence collapse"; 0 absent).
3. VENDOR-FINANCING TRANSMISSION: tier-1 losses arrive via customer-financing writeoffs, not just lower orders (2 explicit; 1 implied; 0 absent).
4. TIER-1 DIFFERENTIATION: Lucent/Nortel impaired existentially while Cisco survives, attributed to balance sheet / vendor financing / FCF (2 right with right reason; 1 right ranking wrong reason; 0 wrong ranking).
5. TIER-2 OVERSHOOT: component tier falls MORE than tier-1 (2 explicit with mechanism inventory/double-ordering; 1 directionally; 0 says less or equal).
6. GOODWILL/WRITEDOWN LOCUS: largest balance-sheet losses appear as acquisition-goodwill writedowns at the component tier and financing writeoffs at tier-1 (2 both; 1 one; 0 neither).
7. MAGNITUDE SANITY: revenue decline magnitudes within 2x of truth (tier-1 ~-60%, tier-2 ~-79%) (2 both within; 1 one; 0 fantasy numbers).
8. NO HALLUCINATED SAVIORS: no deus-ex-machina (government bailout of carriers, sudden demand recovery) driving the outcome (2 clean; 1 minor; 0 outcome depends on one).

## Verdict bands (max 16)
- 12-16: engine rediscovers the known cascade — forward runs worth taking seriously as hypothesis generators.
- 7-11: partial — directionally useful, mechanisms unreliable.
- 0-6: decoration — do not use for forward work; say so plainly.

## Protocol notes
- Run once at small scale; if the report is coherent, run a second seed for stability; score each run independently; report both.
- The grader (Claude) must quote the simulation report verbatim for every scored point.
- Failure mode to watch: the LLM already knows 2002 history from training. A high score may reflect RECALL, not simulation. Mitigation: check whether the report names WorldCom's specific fraud quarter/timing (recall tell) vs producing a generic carrier failure (simulation); note the judgment explicitly in the verdict. This caveat caps Pilot A: it validates plumbing and mechanism-coherence, NOT true predictive power. Pilot B (genuinely unknown future) is the real test; A mainly screens for incoherence.
