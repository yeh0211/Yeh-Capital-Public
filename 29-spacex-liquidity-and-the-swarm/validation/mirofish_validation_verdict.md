# MiroFish test — final verdict (2026-06-13)

Tested 666ghj/MiroFish (Shanda-incubated swarm-simulation engine on CAMEL-AI OASIS) as a forecasting tool, driven headless via its API, LLM = gpt-5.5 through the rehdasu proxy, memory = Zep Cloud. Two pilots with pre-registered rubrics; Pilot B graded by a 7-agent adversarial workflow with an explicit seed-contamination guard.

## Pilot A — 2001 telecom backtest (control)
Raw rubric 15/16, BUT the seed was a rich state report that already contained the answer (WorldCom vulnerability, Cisco-healthiest, JDSU goodwill, two-layer transmission). The engine faithfully synthesized seeded facts into a coherent, honest, hallucination-free 8-quarter forecast — but did NOT demonstrate prediction. **Validated plumbing + coherence; not predictive power.** Lesson: a rich seed inflates the score. Fixed before Pilot B.

## Pilot B — AI-circle forward run (the real test)
Seed = study-27 FACTS with our exposure ladder and verdict STRIPPED OUT, so the swarm had to reason to the ranking itself. 61 agents, 15 rounds. The ReportAgent synthesis step hit the LLM daily cap, so the graded artifact is the raw emergent world (12 posts + 90 comments).

- **Raw rubric (median of 3 graders): 14/16**
- **Contamination-adjusted: 12/16** (drop item 4 — subsidy economics were verbatim in seed; keep item 7 — 5 novel mechanisms confirmed seed-absent by grep). This is the decisive number.
- **Audit: ~65% of load-bearing content is seed restatement.**

### Where the swarm AGREED with study-27 (without being shown it)
- **Trigger: financing/refinancing refusal, NOT demand collapse** — "demand shortfall and price shocks are amplifiers, not the primary trigger." Full agreement.
- **Periphery-first**: high-leverage neoclouds break FIRST, valuation-problem → liquidity-problem at the 2027 refi window.
- **Core survives** (NVDA/TSMC/hyperscalers) as credit-stratification / multiple-compression, not solvency.
- **Anthropic less exposed** (actively re-pricing); relay losses are operational not solvency.

### Where it DIVERGED (the investigable payoff)
- Ranks the **relay/gray-market economy LOW**, where study-27 ranks it #2 — with a specific reason: no GPU-collateral debt, no datacenter capex, losses are account-attrition not insolvency.
- **Refuses to single out OpenAI** by name as deepest-subsidy casualty; stays at category level.

### Genuinely novel mechanisms (grep-confirmed absent from both seeds)
1. **GPU residual-value / haircut / LTV repricing as the precise refinancing pivot** — a next-gen accelerator launch collapses old-GPU residuals → lenders cut collateral ratio → refusal. "2026-financeable does not prove 2027-refinanceable." (most decision-relevant)
2. **Asset/contract/debt triple-duration mismatch** forcing a procurement slowdown even while demand grows — capital-structure risk distinct from demand risk.
3. Take-or-pay coverage of depreciation+amortization as the real neocloud underwriting test.
4. Relay economy's distinct loss-type (attrition/bans, not balance sheet).
5. Power-equipment / project-finance-bankability as a parallel non-GPU transmission channel.

## Bottom line: qualified YES, hypothesis generator only
MiroFish earns a narrow toolkit slot as a scenario stress-tester. Pilot B is materially cleaner than Pilot A (the answer was withheld, so the financing-led pick is genuine). Value = the 2-5 novel credit mechanisms (esp. residual-value/LTV pivot and triple-duration mismatch) + the two specific disagreements. Caps: heavy seed-anchoring (~65%), the headline ranked-ladder was never produced (synthesis hit the cap), ~60/90 comments are corporate-IR roleplay noise, and agreement with study-27 may reflect SHARED LLM PRIORS, not independent foresight. Public framing if shipped: "simulation suggests," never evidence.

## Operational findings (for the toolkit)
- Drives fully headless via REST: ontology/generate → graph/build → simulation/create → prepare → start (max_rounds cap) → report/generate. All long steps are async + pollable.
- rehdasu plugs in as an OpenAI-compatible endpoint; bump the openai client to max_retries=6/timeout=180 (patched 3 sites) to survive rehdasu's intermittent 502 bursts during long report jobs.
- The Lite key (628106) hit its DAILY cap mid-report. Simulation data persists on disk, so the polished ReportAgent report can be regenerated later (cap reset or next key) without re-running the sim.
- localhost:3000 collides with Grafana; ran frontend on :3100.
- Cost guard: 61-agent / 15-round sim + report is heavy; rehdasu throttles per-user concurrency, so parallel_profile_count=3 and ≤15 rounds.
