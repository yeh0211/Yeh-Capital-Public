# Cohere Health (private)

> **The read.** A real L8 utilization-management rail on the right side of the moat map, but at private stage its pricing power is asserted through ARR growth, not proven through NRR-at-price - grade B / B-, conditional durable value-capturer.

**Snapshot**

| | |
|---|---|
| Listing | private |
| Region | US |
| Value-chain layer | L8 - utilization-management / claims-to-cash rail |
| Archetype | AI-services on a savings-share + SaaS base |
| Size | undisclosed (a circulating "$5.5bn" mark is unverified / likely contaminated) |
| Revenue (latest) | private; >60% YoY committed-ARR growth, stated path to ~$500m run-rate by end-2026 |
| Moat verdict | conditional (durable side) |
| Expectation | full |
| Evidence quality | med |

![positioning](../figures/co_COHERE-HEALTH.png)

## What it is
Prior-authorization and utilization-management AI sold to health plans (payers), not providers - it sits on the insurer's side of the approval transaction, auto-adjudicating care requests against evidence-based clinical pathways and, increasingly, auditing claims for payment integrity. Founded 2019 (Boston; now Portsmouth, NH). Not to be confused with Cohere Inc., the enterprise-LLM lab.

## Business model - how it makes money
Archetype 05 (savings-share / risk-share) fused with Archetype 02 (SaaS / PMPM) - the L8 pattern. Revenue comes from three streams: (i) per-member / per-transaction platform fees for running a plan's UM function (Cohere Unify / Next / Connect); (ii) savings-share on medical-expense reduction - Cohere is paid from cost avoided, and results count toward medical-loss ratios, aligning it with the payer as beneficiary; and (iii) payment-integrity / claims-audit via the ZignaAI acquisition (Sept 2025).

The product surface is the Cohere Unify platform plus a named module set: Cohere Align (personalizes in-house UM workflows), Cohere Connect (FHIR API-based interoperability and CMS-0057-F compliance), and Cohere Review Assist (an AI copilot for medical-necessity review) [disclosed, Aug 2025]. In Jun 2026 the company extended Unify's agentic AI from utilization management and payment accuracy into appeals, care management, claims operations, and quality [disclosed] - a "shift right" across the care-and-cost continuum that widens the wallet inside each existing plan rather than only adding new plans. Company-disclosed platform scale: 15m+ clinical decisions/yr, ~4,500 clinical policies and guidelines, ~100,000 clinical indications, and ~27m unique patient profiles [disclosed, Jun 2026].

Growth (company-sourced): >60% YoY committed-ARR growth; a stated path to a ~$500m revenue run-rate by end-2026; ambition to manage 50m+ lives. Named to the 2025 Inc. 5000 (No. 1,161) on ~2021-2024 revenue growth, and to TIME's World's Top HealthTech 2025 list [reported, Aug 2025]. Capital character is mostly capital-light - no wet lab, no reimbursement gate - but with a real services tail: human clinical reviewers and payer-specific integration / change-management are a cost that scales with each new plan, so it is lighter than a lab and heavier than pure SaaS.

## Financial summary
Private company - funding table, real disclosed numbers only.

| Round | Date | Amount | Lead | Notes |
|---|---|---|---|---|
| Series A | 2020 | $10m+ | - | [reported] |
| Series B | Apr 2021 | $36m | Polaris | [reported] |
| Equity | Feb 2024 | $50m | Deerfield | [disclosed] |
| Series C | May 2025 | $90m | Temasek | [disclosed]; return backers Deerfield Management, Define Ventures, Flare Capital, Longitude Capital, Polaris Partners |
| Total raised | - | ~$200m | across three rounds | [reported] |

Valuation is undisclosed. A reported "$5.5bn" circulates via data aggregators (PitchBook / DeepNewz-style tertiary feeds) and should be treated as a red flag, not a fact. A $5.5bn mark on only ~$200m raised implies a ~28x cumulative-cash-to-value ratio, far outside the venture norm; it does not appear in the primary Series C release, which discloses no post-money, and it collides with the near-identically-named Cohere Inc. (the LLM lab, $6.8bn Aug 2025) - a likely cross-contamination. The honest read: a $90m round from crossover names like Temasek typically prices a healthcare-services company at low-single-digit $bn at most, and the "$5.5bn" should not be used as a load-bearing input.

## Value-chain position and competition
L8 is the utilization-management / claims-to-cash rail - it re-plumbs the money-flow decision between provider and payer. Clinical documentation flows in; an approve / deny / pend decision plus a paid / audited claim flows out. Reported throughput ~12m PA requests/yr, ~13m+ covered members, ~560,000-660,000 providers, and ~47m payer-provider interactions/yr. Named plans: Humana (musculoskeletal, multi-state), Geisinger, regional Blues.

It is a crowded L8. Rivals: Availity (largest clearinghouse, Anthem channel), Rhyme / PriorAuthNow (~4m PAs/yr, provider-network side), Myndshft (600+ payer rules, med + pharmacy), CoverMyMeds, Anterior, plus in-house payer builds and the legacy UM outsourcers (Cohere's real displacement target). A newer competitive read comes from the CMS WISeR Medicare pilot [reported, Aug-Oct 2025], the first federal AI-assisted prior-auth model to name its vendors: the six selected are Cohere Health (Texas), Genzeon (New Jersey), Humata Health (Oklahoma), Innovaccer (Ohio), Virtix Health (Washington), and Zyter (Arizona). That list is the closest thing to a public peer set for the "AI on the payer/reviewer side" node - Humata Health and Innovaccer are the names to watch as direct L8 substitutes. Cohere's edge: it runs on the payer's side of the transaction with an evidence-pathway / clinical-intelligence layer, several large payers run it as their UM engine, and it has the FHIR-API maturity (Cohere Connect) to sell CMS-0057-F 2027-mandate compliance - a regulatory forcing function every US plan must meet by 1 Jan 2027. It also sits on the HL7 Da Vinci Project Steering Committee shaping the FHIR PA implementation guides [disclosed, May 2026], which is a standards-body seat at the table its smaller rivals do not hold. Critically, it sits against the payer - a counterparty the EHR platform (Epic) does not own - which is the whole moat argument. That is a distribution + timing edge, not a technology monopoly.

## Moat
Applies: Moat 2 (workflow embedding / distribution), conditional - and Cohere is placed on the durable side. Ch5's single surviving moat type is workflow ownership of a scarce input the platform cannot cheaply replicate; Cohere's scarce input is the payer relationship and the claims-to-cash / UM rail, which Epic does not own and cannot cheaply clone - the switching cost is re-wiring money flow and re-clearing payer adjudication. That is genuinely more durable than the rented-EHR-slot scribe layer (~1-3yr), and Ch5 names Cohere explicitly among the owned-workflow survivors (~5-7yr).

Durability here is conditional on two things the private status hides: (a) whether the savings-share take-rate holds as the automation commoditizes - Ch5 / Ch4 warn that savings-share quietly reverts to per-transaction SaaS as take-rates on commodity automation compress; (b) whether payers, once the 2027 API plumbing is built, in-source the function. The mechanism is the right one (owns the payer rail), but at this stage it is asserted on private ARR growth, not proven by audited NRR-at-price through a renewal cycle. The rail is real; its pricing power is unverified.

## Core variables
1. **Savings-share take-rate durability / NRR-at-price** - does Cohere keep its share of avoided cost as auto-approval (reported "up to 90%") commoditizes, or does it revert to thin per-transaction SaaS? The single number that decides whether it is a value-capturer or a utility.
2. **Payer in-sourcing risk post-2027** - CMS-0057-F forces every plan to build FHIR PA APIs. The mandate is Cohere's near-term tailwind and its medium-term threat: once the plumbing is standard, the largest payers (with in-house AI) can replicate the UM engine and drop the vendor.
3. **The real valuation** - the load-bearing unknown. The "$5.5bn" is unverified / likely-contaminated; the actual price paid by Temasek gates any return math.

Held below the line (second-order noise): ZignaAI payment-integrity cross-sell execution; regulatory / PR risk on AI-driven denials (the sector's reputational tail); client concentration on Humana.

## Bear case / key risks
It is a UM-outsourcing services business wearing an AI-platform multiple. The three-way payer / provider / patient split (the Babylon lesson) is a hazard: the buyer (payer) wants denials that reduce cost; regulatory and political pressure on AI-driven prior-auth denials is rising, and a denial-algorithm controversy is a live headline risk that can reprice trust overnight. The savings-share model compresses as automation commoditizes (archetype-05 bear: take-rates on commodity automation revert to per-transaction SaaS). The 2027 CMS API mandate that Cohere sells today simultaneously hands large payers the standard plumbing to in-source the function. And the headline valuation is unverified and implausible on the cash raised - anyone underwriting a return off "$5.5bn" is underwriting a number that does not appear in a primary source.

## The expectation read
The circulating "$5.5bn" mark, if anyone took it as real, would price Cohere as a proven AI platform - a ~28x cumulative-cash-to-value ratio the ~$200m raised cannot support and no primary source confirms. The defensible read is that a $90m Temasek-led round prices a fast-growing healthcare-services company at low-single-digit $bn at most, which is a full expectation for a business whose pricing power is still asserted (ARR growth) rather than proven (NRR-at-price through a renewal cycle). What looks soft: the market belief embedded in the headline number assumes savings-share take-rates hold through automation commoditization and that payers do not in-source post-2027 - neither is yet demonstrated.

## Recent developments (2025-2026)
The private status still hides the load-bearing numbers (real valuation, NRR-at-price), but the year added concrete facts that sharpen - and in one case materialize - the existing thesis.

- **Named to the CMS WISeR Medicare prior-auth pilot** [reported/disclosed, Aug-Oct 2025; CMS primary source]. Cohere is one of six technology-only participants in the Center for Medicare and Medicaid Innovation's Wasteful and Inappropriate Service Reduction (WISeR) model, assigned Texas (JH Novitas MAC). The others: Genzeon (NJ), Humata Health (OK), Innovaccer (OH), Virtix Health (WA), Zyter (AZ). It is the first Innovation Center model in which technology firms are the only participants, runs six performance years (Jan 1, 2026 - Dec 31, 2031), covers a pre-selected set of low-value services (e.g. skin/tissue substitutes, electrical nerve-stimulator implants), and pays each vendor a percentage of "averted" expenditures adjusted for provider-experience scores. This is the first time Cohere's savings-share economics extend into Original Medicare - a large new addressable pool.
- **WISeR is also the reputational tail going live.** In Oct 2025 six House Democrats (Larsen, DelBene, Schrier, Landsman, Bera, Pocan) introduced the Seniors Deserve SMARTER Care Act to repeal the model [reported], arguing paying vendors a share of averted spend "creates a dangerous incentive to put profits ahead of patients." Physician societies (e.g. ASE, ASNC, SCAI) and the AHA filed opposition. CMS says final coverage denials are made by a licensed clinician and that emergency / inpatient-only / delay-risk services are excluded. This is Core Variable #2 (denial-algorithm controversy) turning from hypothetical into a named, dated headline risk on a specific Cohere contract.
- **ZignaAI acquired (payment integrity)** [disclosed, Sep 9, 2025]. Cohere framed it as a "shift right" from pre-care prior authorization into post-service claims / coding validation, welding PA and payment integrity into one workflow and displacing "stacked audit vendors" with in-house automated review. This is the concrete build-out of the third revenue stream referenced above.
- **Cohere Unify platform expansion** [disclosed, Jun 9, 2026]. Agentic AI extended from UM and payment accuracy into appeals, care management, claims operations, and quality - a land-and-expand within existing plans, positioned as "redesigning operations" rather than retrofitting AI onto broken processes. Disclosed scale: 15m+ clinical decisions/yr, ~4,500 clinical policies, ~100,000 clinical indications, ~27m unique patient profiles.
- **CMS interoperability posture** [disclosed, May 20, 2026]. Cohere joined the CMS Health Tech Ecosystem and Electronic Prior Authorization Acceleration initiatives and sits on the HL7 Da Vinci Project Steering Committee. Company-stated operating metrics: 47m payer-provider interactions/yr, care 70% faster than legacy PA, 94% provider satisfaction, up to 9x ROI. These are marketing-sourced and unaudited, but they are the numbers a payer buyer sees.
- **Responsible-AI positioning** [reported, Aug-Sep 2025]. Joined the Coalition for Health AI (CHAI); repeatedly states its AI is "built to support and accelerate decision-making, never to deny care" - a defensive posture aimed squarely at the WISeR-style political risk.

No 2025-2026 primary source disclosed a post-money valuation. The circulating "$5.5bn" mark remains unverified / likely contaminated by the near-identically-named LLM lab Cohere Inc. (which raised $500m at a $6.8bn valuation in Aug 2025), and should still not be used as a load-bearing input.

## Verdict
Conditional durable value-capturer, grade B / B-, moderate confidence - a real L8 rail on the right side of the moat map, but at private stage the pricing power is asserted (ARR growth) not proven (NRR-at-price), and it is exposed to savings-share compression plus post-2027 payer in-sourcing; the circulating "$5.5bn" valuation is a red flag, not a fact. Good business at a full expectation.
