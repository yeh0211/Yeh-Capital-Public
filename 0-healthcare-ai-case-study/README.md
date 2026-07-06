# Healthcare AI research: how the field actually works (US and Taiwan)

**What this is.** I spent a while trying to understand healthcare AI from one end to the other, and this is my write-up of what I found. Not a single application, the whole field: the global trend, the companies and what they actually do day to day, how they make money, who the players are and how they connect to each other, what protects the good ones from being copied, the rules they have to live under, and the size of the thing. I looked hardest at two markets, the US and Taiwan.

**The question I used to hold it together.** Trying to understand a whole field can turn into a shapeless list of company names. So I hung the whole thing on one question, sharp enough to force real answers: out of every player I could find, which ones own something that lasts, and which ones just have a good demo? That question turned out to teach me most of what I now understand about how the field works.

**Why bother.** "AI is transforming medicine" is true and it tells you almost nothing. I wanted to actually walk the field instead of nodding at the headline. So I looked at 94 companies and profiled 94 of them in depth, and this document is me explaining what that walk taught me.

*By Hsin Cheng Yeh.*

---

## The short version, if you read nothing else

I went in assuming the value in this field would sit with whoever had the smartest AI models. It does not, and figuring out why became the core of what I learned. Here is the field in a handful of lines, before any of the longer reasoning below.

- The thing that actually matters in healthcare AI is not the model. It is whether a company owns some scarce input that cannot easily be copied. A permanent code that guarantees an insurer will pay them. A physical clinical asset they own outright. A licensed pile of data they can resell. Own one of those and you have a real business. Own a clever model and you have a head start that lasts about a year.
- The thing that gates everything is payment, not technology. In the US, roughly **1,451** AI medical devices have been cleared by the FDA, meaning regulators have said they are safe to sell. But only **3** of those hold a permanent, nationally-paid billing code, meaning an insurer is actually obligated to pay for them. Getting the device approved is easy now. Getting anyone to pay for it is the wall.
- In drug discovery, AI got good at chemistry and is still stuck on biology. AI-designed molecules pass the first clinical stage, the safety test, at **80-90%**. But they pass the second stage, the first real test of whether the drug works, at only about **40%**, the same rate the industry has had for thirty years. As of 2026, zero AI-discovered drugs have been approved.
- I took the four things people usually call a "moat" in this field and tried to break each one. Only one type survived: owning the workflow itself, which in practice means owning the payment rail, the physical asset, or the data plumbing that everything else plugs into. The rest have a shelf life of about a year.
- Taiwan runs a smaller copy of the whole US picture, on under NT$600m of combined revenue from its listed pure-plays. It also has the strongest data moat of anyone, a single national insurer sitting on everyone's health records, but that moat belongs to the government, not to any company you could invest in.
- I broke my one big question into nine smaller yes-or-no questions and graded each against the evidence. I ended at **2 Yes, 3 No, 3 Conditional, 1 mostly-No**. The honest summary is: healthcare AI is real, but the part of it that is a durable business is narrow, and it mostly belongs to whoever owns a scarce input rather than to the AI companies the headlines talk about.

Everything after this is me showing my work so you can push back on any single line of it.

---

## How I went about this

I want to be plain about the method up front, because someone whose opinion I trust asked me to make it visible instead of burying it. I approached this the way an investor sizes up an industry, not the way a technology reviewer rates gadgets. Six choices shaped the whole thing.

**I built the framework before I touched the data.** For each part of the field, the first question I asked was not "what is the number" but "what is the essential thing this kind of business does, and what would I even need to know to judge whether it is any good." Get that foundation wrong at the start and even a very thorough-looking analysis is just sitting on the wrong ground.

**I drew the whole map instead of digging one deep hole.** The classic mistake in healthcare research is to pick one application, say AI reading X-rays, drill into it forever, and call that a view of the sector. So I forced myself to put every sub-sector on one page and connect them, because the interesting value often hides in the seam between two of them. That paid off: it turned out the diagnostics-data business quietly feeds the drug-discovery business through exactly one connection, and I would have missed it if I had only dug one hole.

**I treated "how big is this market" as a real question, not a slide.** People throw around enormous market-size numbers. I sized each piece from the ground up, adding up what is actually being spent, and then threw away the top-down headline number whenever the two disagreed. They disagreed by 20-25 times. Instead of hiding that, I made the gap itself one of the findings.

**In drug discovery, I looked at picking, not making.** The exciting story is "AI can design a new molecule." But the harder and more valuable question is "can AI pick the one molecule out of many that will actually survive human trials." I organized that whole section around picking rather than making, and it changed the answer.

**I tested every claimed moat by trying to kill it.** For each thing a company claimed protected it, I made a genuine attempt to argue it away, then gave it a verdict (holds up, holds up under conditions, or does not hold up) and an estimate of how many years the advantage really lasts. A moat you have not tried to break is a moat you do not actually understand.

**I watched the direction of the payment rules, not the size of the prize.** In a market where an insurer decides whether you get paid, the signal that matters is which way the coverage rules are moving, not how big the theoretical market could be. And I tried to state every claim so that a specific, watchable number could later prove me wrong. A conclusion that can never be wrong is not research.

One housekeeping note so you know what you are reading. This is a method-and-findings write-up. I read a large stack of company filings, analyst notes, and regulatory records privately, and in the text I refer to them in general terms ("a filing", "an analyst note", "disclosed") rather than by name. I tag each load-bearing number so you know how solid it is: **[disclosed]** means it came from a company or primary source, **[sell-side]** means an analyst or market-research note, **[estimate]** means I derived it, **[reported]** means press, and **[unverified]** means it was cited somewhere but I could not confirm it against a primary source. Where that last case happened, I say so and use the corrected figure.

The universe is **94 companies** across the US and Taiwan, picked so that every layer of the value-chain map has at least one company sitting in it. That is the widest coverage the sources would honestly support, and where the evidence on a name is thin I flag it right there rather than quietly leaving it out.

---

## How we got here: a healthcare-AI timeline, 2010 to now

![Healthcare AI timeline, 2010 to now](figures/08_timeline.png)

To make sense of where the field sits today, it helps to walk the fifteen years that built it. The short story is that the science kept arriving years ahead of the business, and the thing that decided who made money was almost never the cleverness of the model. It was who got paid.

The early years were the hype years. In 2011 a question-answering machine beat two human champions on television, and by 2015 that same brand had a health division and about $4bn of acquisitions behind it, promising to read cancer like a specialist. It did not work. In 2022 the whole effort was sold for parts at roughly a quarter of what it cost to build. That arc, brilliant demo to quiet sale, turned out to be the pattern the field would keep repeating.

Underneath the noise, two real breakthroughs landed. The first was regulatory: in 2018 the FDA cleared the first AI allowed to diagnose a patient with no doctor in the loop, an eye-screening tool. The second was scientific: between 2018 and 2024, protein-structure prediction went from a strong contest result to a solved 50-year problem to a free public database of 200m-plus structures to a Nobel Prize. That last part matters more than it looks. The breakthrough that was supposed to be a private drug-discovery moat became a commons within about a year, because open copies caught the frontier. The science was a gift to everyone, which is exactly why it was a moat for almost no one.

Then came the money questions, and this is where the field actually gets decided. Getting an insurer to pay for AI is the wall. In 2020 a stroke tool won the first extra Medicare payment for AI; the code-writing plumbing followed in 2021; and by 2024 exactly one heart-imaging tool had graduated all the way to a permanent national billing code. Set that against roughly 1,451 AI devices the FDA has cleared, only 3 of which hold a permanent paid code, and you have the single most important fact in the field: clearance is easy and payment is the gate. The 2025 bill to create a defined AI payment category is the tell. It has to exist because no durable path does yet.

The 2022-23 stretch is when the general-purpose chatbots showed up and clinicians started using them, approved or not, to draft notes and answer questions. That pulled ambient scribes and clinical assistants into the mainstream. But it also set up the trap that is playing out now: in 2026 the dominant records system built its own AI scribe straight into the chart, and the startups that had been renting depth from that system found the landlord had become the competitor.

The deals and listings round it out. Isomorphic, spun out of the protein breakthrough in 2021, signed two pharma partners in 2024 for headline numbers near $3bn, of which only a low-single-digit percent was actually paid upfront, the honest shape of an AI-drug deal. Tempus and Caris took the diagnostics-data model public in 2024 and 2025. And when two of the loudest AI-drug names merged in late 2024, it read as consolidation forced by thin pipelines, not strength. The recurring lesson across all of it: the durable value tends to sit with whoever owns the payment rail, the physical asset, or the data, and that is usually the incumbent, not the AI startup the headlines got excited about.

- **2011-02 -** IBM Watson wins Jeopardy. A question-answering machine beats two human champions and becomes the face of AI in medicine before it ever touched a patient.
- **2015-04 -** IBM launches Watson Health. IBM stands up a health unit and buys its way in for about $4bn [reported], promising Watson would read oncology like a specialist.
- **2016-02 -** DeepMind Streams goes live at the Royal Free. An AI-branded kidney-injury alert app ships to a London hospital on a data-sharing deal covering about 1.6m patient records [reported].
- **2017-07 -** UK regulator rules the Streams data deal broke the law. The privacy regulator finds the hospital handed over patient data unlawfully; no fine, but the first shot across the bow on health-data consent [reported].
- **2018-04 -** FDA clears IDx-DR, the first autonomous diagnostic AI. De Novo authorization for a tool that reads eyes for diabetic retinopathy with no doctor in the loop, the first AI allowed to diagnose on its own [disclosed].
- **2018-12 -** AlphaFold wins CASP13. DeepMind's first protein-folding model tops the field's benchmark contest, a strong result that still leaves the problem unsolved.
- **2020-04 -** Nuance ships Dragon Ambient eXperience (DAX). The ambient-scribe idea, an AI that listens to the visit and writes the note, goes commercial and defines the category doctors would actually adopt [reported].
- **2020-09 -** Viz.ai wins the first AI add-on payment from Medicare. CMS grants a stroke-triage tool a temporary New Technology Add-on Payment of up to $1,040 per use, the first time a US public payer pays extra for AI [disclosed].
- **2020-11 -** AlphaFold2 solves protein folding at CASP14. The second model scores about 92 on a 100-point accuracy test [disclosed], and the contest organizers call a 50-year grand-challenge effectively solved.
- **2021-01 -** FDA publishes its AI/ML Action Plan. The regulator lays out how it will oversee learning software and floats letting devices update under a pre-agreed plan instead of re-filing each change [disclosed].
- **2021-07 -** The AlphaFold protein-structure database opens. DeepMind and a public genomics lab release structures for a first tranche of proteins for free [disclosed], later scaling past 200m and turning a moat into a commons.
- **2021-09 -** AMA creates an AI taxonomy for billing codes. The body that writes US procedure codes adds a framework sorting AI into assistive, augmentative, and autonomous, the plumbing before anything gets paid [disclosed].
- **2021-11 -** Isomorphic Labs is founded. Alphabet spins AlphaFold's drug ambitions into a standalone company, betting the protein breakthrough can be turned into medicines.
- **2022-06 -** IBM sells Watson Health for parts. The oncology-AI flagship that cost about $4bn to build is sold to a private-equity firm for about $1.07bn [reported] and renamed, closing the Watson-in-medicine story.
- **2022-11 -** ChatGPT is released. A general-purpose chatbot goes public and, within weeks, clinicians start using it to draft notes and answer questions it was never approved for.
- **2023-02 -** ChatGPT is shown to nearly pass the US medical licensing exam. A published study puts the model at or near the ~60% passing line across all three exam steps [disclosed], the moment clinical use stopped being hypothetical.
- **2023-08 -** Babylon Health files for bankruptcy. The AI-symptom-checker unicorn, worth about $2bn at its 2021 SPAC listing [reported], liquidates, the clearest sign that an AI demo is not a business.
- **2024-01 -** Isomorphic signs Lilly and Novartis for up to ~$3bn. Two pharma deals with about $83m paid upfront against roughly $2.9bn in milestones [disclosed], the template for how AI-drug deals are really structured: cheap staged bets.
- **2024-01 -** FFR-CT graduates to a permanent national billing code. A heart-blood-flow AI collapses four temporary codes into one permanent Category I code effective this year [disclosed], the rare AI tool with a durable payment path.
- **2024-05 -** AlphaFold3 is released. The third model extends beyond proteins to how they bind DNA, drugs, and other molecules, moving closer to the chemistry that matters for medicines.
- **2024-06 -** Tempus AI goes public. The multi-data diagnostics-and-data platform lists on Nasdaq at $37 a share, raising about $410m [disclosed], the first big pure-play healthcare-AI IPO.
- **2024-10 -** AlphaFold's creators win the Nobel Prize in Chemistry. DeepMind's Hassabis and Jumper share the prize [disclosed], the field's scientific high-water mark, and a reminder the science ran years ahead of the business.
- **2024-11 -** Recursion completes its merger with Exscientia. Two of the loudest AI-drug names combine in an all-stock deal valuing Exscientia at about $650m [reported], consolidation driven by thin pipelines, not strength.
- **2025-04 -** The Health Tech Investment Act is introduced. A Senate bill (S.1399) would create a defined Medicare payment category for algorithm-based services with at least five years of separate pay [disclosed]; that it is needed at all is the tell there is no durable AI payment path today.
- **2025-06 -** Caris Life Sciences goes public. The precision-oncology lab raises about $494m on Nasdaq and pops on day one [disclosed], the second major diagnostics-data IPO in a year.
- **2026-02 -** Epic ships its own ambient AI scribe into the chart. The dominant records system builds note-writing straight into the workflow at a rumored ~$80 per provider per month [sell-side], and the landlord becomes the competitor to the scribe startups renting its rails.

---

## What I found

I organized the middle of this around a simple sequence. Size the field. Find the real gate. Map who sits where. Take apart the one sub-sector everyone is excited about. Try to break the moats. Check the rules in each market. Each finding below carries its own reasoning so you can watch it earn its place rather than taking my word for it.

### Finding 1 - The headline market is 20-25x bigger than the money actually being spent, so the number to watch is the rate of change

![The headline TAM vs the money actually invoiced](figures/04_tam_gap.png)

*What I expected.* I assumed the market-sizing firms and I would roughly agree on how big healthcare AI is, give or take.

*What I found.* The top-down estimates put the "healthcare AI market" at roughly **$27-37bn** for 2025 [sell-side]. But when I added up from the bottom what was actually spent on healthcare-specific AI software in 2025, I got about **$1.4bn**, up roughly 3x on the year before [sell-side]. That is a 20-25x gap between the headline and the money that actually changed hands.

*Why it matters.* A gap that big means the headline number is a "count everything AI touches" construct, basically decorative. The useful thing to watch is not the size of the pie, it is how fast adoption and payment are actually moving. Money is clearly flowing in through an AI lens (AI took **54%** of 2025 US digital-health funding dollars, up from 37% in 2024 [sell-side]). But I made myself argue the other side. Strip out the nine biggest fundraisers and 2025 actually falls below 2024, and total healthcare investment was down 12% [sell-side]. So part of what looks like a boom is money rotating inside a shrinking pool, not fresh money arriving.

*How I would know I was wrong.* If the bottom-up spend I measured had come within, say, 3x of the headline number, I would size the field on the headline and drop the whole rate-of-change idea. It is nowhere near that close.

*Verdict.* **Confirmed.** From here on, every sub-sector I look at is judged on whether payment and adoption are moving, not on a single big market-size number. That one choice falls straight out of this gap.

There is a picture that carries this, in the house palette (cream background, near-black ink, one clay-red accent, no clutter): a running count of FDA clearances from 1995 to 2025 that bends sharply upward around 2023, with the accent marking the turn. It looks like an explosion. The very next finding is the chart that stops you from over-reading it.

### Finding 2 - Getting FDA clearance is easy and common; getting an insurer to pay is the real wall

![FDA AI/ML clearance velocity](figures/01_fda_velocity.png)

![Cleared vs paid: the reimbursement wall](figures/02_reimbursement_wall.png)

*What I expected.* On the face of it, "FDA-cleared" sounds like a serious barrier that keeps competitors out.

*How I measured it.* I counted the AI devices that have been cleared to sell against the ones that also have a permanent national code guaranteeing payment. For the clearances I used the FDA's own list of AI-enabled devices, by authorization date, across all device classes, so the curve is consistent with itself.

*What the data shows.* The running count of cleared AI devices reached **1,451** by the end of 2025, adding a record **295** in 2025 alone, and the pace is still speeding up. The yearly count stepped from 91 (2022) to 221 (2023) to 253 (2024) to 295 (2025), and the time it takes to double has shrunk from about four years to about two [sell-side]. Around **97%** of these went through a fast-track path (called 510(k)) where the company's whole argument is "this is basically the same as something already on the market." That is the opposite of owning something defensible. The typical review in 2025 took **142 days** [sell-side].

Now look at the bar right next to it. Of those roughly 1,451 cleared devices, exactly **3** hold a permanent billing code with a national payment rate attached [disclosed]. Across billions of insurance claims from 2018 to mid-2023, only **two** AI tools were ever billed more than 10,000 times total [sell-side].

*Why this happens.* Clearance gets you onto the shelf. Payment gets you revenue. A device nobody is obligated to pay for earns almost nothing. And even a permanent payment code is not safe. The one permanent code for a fully-autonomous AI (a tool that screens for diabetic eye disease) has been priced down every single year: **$47.06 in 2022, $45.74 in 2023, $40.28 in 2024**, roughly -14% over two years, because it sits inside a fixed budget where paying one tool more means paying another less [disclosed]. The one AI tool getting paid at real scale, a heart test that uses a CT scan to estimate blood flow, only got there by slowly graduating four temporary codes into one permanent one (effective 2024, roughly **$997 rising to $1,017**). In the year before that switch, that single tool drove about 14,000 Medicare claims and $12.7m, dwarfing every other paid AI tool [disclosed].

*What I checked.* The obvious counter-argument is "the clearance count IS the adoption story, it just shows the field growing." It is not, for two reasons. The clearances are held mostly by the big imaging incumbents, not startups (one large equipment maker holds 120 radiology-AI clearances, the next 89, then 50, then 45 [disclosed]). And clearance does not touch the payment gate at all. So the count actually overstates how defensible the young companies are.

*Verdict.* **Confirmed, and this is the single most important thing in the whole study.** If you take one idea from this document, take this: "FDA-cleared" tells you almost nothing about whether a healthcare-AI company has a real business. The chart here is just two bars, roughly 1,451 cleared against 3 permanently paid, and it is the cure for the exploding curve in Finding 1.

### Finding 3 - The field splits into five sub-sectors, but the type of business, not the sub-sector, decides how good the growth is

![Sub-sector: measured spend vs top-down TAM](figures/06_subsector_gap.png)

![The archetype value-capture grid](figures/05_archetype_grid.png)

*What I expected.* I assumed labels like "precision oncology" or "ambient scribe" were meaningful economic categories, that knowing the sub-sector told you something about the business.

*What I found.* They mostly are not. Two companies sitting in the same sub-sector can run businesses 35 gross-margin points apart. What actually decides the quality of the growth is what I think of as the revenue physics of the business: who pays, whether the person paying is also the person who benefits, whether some payment or effectiveness wall stands between doing the work and collecting the money, and how much cash the next sale eats up. Six patterns cover the whole universe.

| Business pattern | Who pays / the catch | Gross-margin band | Cash needed | Durability |
|---|---|---|---|---|
| Per-test / per-scan fee | insurer pays, clinician orders, patient benefits (three different people); needs a payment code | ~40-62% [disclosed] | heavy (physical lab, reagents) | conditional; the code can be priced down |
| Software subscription | provider pays per seat, and the buyer is the one who benefits, no code needed | ~70-80% | light | high, unless a platform bundles in a free substitute |
| Data-licensing to pharma | a drug company buys de-identified data; needs a contract | ~71-80% [disclosed] | light | high, an annuity that scales with data |
| Milestone + royalty (drug discovery) | a drug company pays upfront plus milestones; gated by biology | n/a (pre-revenue) | very hungry once in the clinic | weak / binary; capped by the ~40% wall at the second trial stage |
| Shared savings | insurer pays out of money saved, and the buyer benefits; gated by outcomes | ~60-75% | medium | conditional; the lock-in is the workflow, not the AI |
| Infrastructure toll | everyone above pays to use it; gated by usage, and it does not care about payment codes | bimodal | bimodal | splits internally; model IP gets copied, silicon does not |

*Why it matters.* The two durable patterns (subscription software and data-licensing) share three traits: the person paying is the person who benefits, there is no payment gate in the way, and the next sale is nearly free. The two weak patterns (per-test and drug-discovery milestones) have the opposite: a payment or effectiveness wall stands between the work and the money, and the next unit costs real cash. That pairing predicts how durable a business is far better than how good its technology is.

The cleanest proof is one single company measured two ways. The largest multi-data-type diagnostics platform runs a per-test lab at about **62%** gross margin, and it has bolted a data-licensing annuity on top running at about **73%** [disclosed]. Same company, two business patterns, an 11-point gap set purely by the revenue physics and not by the sub-sector. The chart is just those two bars.

*The honest caveat I had to add.* Gross margin is a stand-in for growth quality, not growth quality itself. A 73%-margin data annuity whose new bookings are slowing is a worse business than a 55%-margin per-test lab that is mid-takeoff. The business pattern sets the ceiling. The rate of change decides whether the company is anywhere near that ceiling. Hold onto that, because it is the hinge of the bear case on the very idea above.

*Verdict.* **Confirmed.** I read every single company through this lens, and it kept the analysis honest.

### Finding 4 - Drug discovery is a picking problem, not a making problem, and AI's edge shows up in the wrong stage

![Phase I vs Phase II success: the AI edge is in the wrong phase](figures/03_pos_split.png)

This is the sub-sector people are most excited about, so I gave it the roughest treatment.

*What the market believes.* That because AI can now predict protein structures and generate new chemistry, "AI can design drugs now," and that this is a step-change in the odds of getting an approved medicine.

*Where I differ, and the proof.* The advance is real, but it lands in the wrong stage for how drug economics actually work. Split the clinical funnel by where AI-designed molecules actually do well and the picture is clear. A quick vocabulary note first: a new drug goes through Phase I (does it hurt people, the safety test), then Phase II (does it actually work, the first real efficacy test), then Phase III (a big confirmatory trial), then approval.

| Stage | Historic pass rate | AI-designed molecules | What it tells you |
|---|---|---|---|
| Phase I (safety) | ~52% advance [sell-side] | **80-90%** (21 of 24 in one sample) [estimate] | AI solved "make a well-behaved molecule" |
| Phase II (does it work) | ~29% advance / ~39% success [sell-side] | **~40%**, same as history [estimate] | the AI edge vanishes once the question is efficacy |
| First-in-human to approval | ~8% [disclosed] | zero approved as of 2026 [estimate] | the ~90% failure rate has not budged |

Phase I is high precisely because it is not testing whether the drug works, only whether it is safe, which is exactly the "make a well-behaved molecule" problem AI is genuinely good at. Phase II is the low point in every disease area because it is the first time the biology gets tested for real, and biology is where AI is still weak. Now overlay the money. The out-of-pocket cost of these stages runs roughly $25m for Phase I, $59m for Phase II, and $255m for Phase III [estimate]. About **93% of the clinical spend happens after the point where you pick which molecule to push forward.** So the real lever is picking the right target and candidate and killing the losers before the expensive stages, in other words picking well and failing fast, not generating more molecules.

*The mechanism, spelled out.* When a drug company announces a headline "$3bn" deal for an AI platform, look at what actually changes hands. In the cleanest set of five deals over four years, the money paid upfront was a tight **1.2-3.0%** of the headline number, and the rest is contingent on milestones that mostly never trigger [disclosed components, percentages computed]. One prominent up-to-$12bn deal has actually paid out on the order of a single ~$7m milestone [estimate]. The drug company is buying a bundle of cheap staged bets on an unproven platform, not writing a conviction check. That is the tell. The experienced buyers are already treating this as a lottery ticket, not a sure thing.

*What I checked.* The strongest counter-argument is "the proprietary lab-data flywheel will compound into a real edge over time." Two facts break it. Open, commercially-licensed copies of the frontier structure-prediction models caught up within about a year, at over 1000x lower cost, so owning more proprietary data buys you almost no model advantage exactly where the moat was supposed to be. And the company with the biggest automated-lab flywheel has the field's worst clinical record and cut its three lead programs in 2025 [estimate/disclosed]. The one genuine human proof-of-concept, a single ~71-patient trial in one country from an AI-derived target and molecule, is enough to refute the too-strong claim that "nothing works," but it is nowhere near enough to prove that AI raises the base success rate.

*Verdict.* **Confirmed: AI solved the cheap half of the problem.** The only defensible position here is owning the drug asset yourself plus having a real drug company to distribute it, and even that runs into the same ~40% wall at Phase II as everyone else. The chart is a funnel: the AI spike at Phase I collapsing flat onto the historic ~40% line at Phase II, with two points pinned to the wall, "0 AI drugs approved (2026)" and "1 genuine human proof-of-concept."

## Who funds AI drug discovery, and where the value lands

![AI drug-discovery deals: up-front cash vs the headline number](figures/07_money_flow.png)

If you only read the headlines, you would think the AI drug-discovery companies are getting rich. "Isomorphic Labs signs deals worth nearly $3bn." "Takeda inks $1.7bn AI alliance." "Roche commits up to $12bn to Recursion." The numbers are enormous and they are real. But the headline number and the money that actually changes hands are two very different things, and the gap between them is the whole story of who wins in this field.

Here is the mechanism, in plain terms. When a big drug company (an incumbent - Lilly, Novartis, Sanofi, Takeda, Roche) hires an AI lab, it almost never writes a big check on day one. It writes a small one. The rest of that giant headline is a stack of "milestone" payments, and each milestone only pays out if a specific thing happens later - a molecule gets picked, a trial starts, a trial succeeds, a drug gets approved, a drug hits a sales target. Most of those things never happen, because most drug programs fail. So the headline is not a price. It is the sum of every payment that would be made in the one lucky world where everything goes right.

Look at what the incumbents actually paid upfront, as a share of the headline they announced:

| Deal | Upfront | Headline total | Upfront as share |
|---|---|---|---|
| Roche/Genentech - Recursion (2021) | $150m | up to $12bn | 1.2% |
| Sanofi - Insilico (2022) | $21.5m | up to $1.2bn | 1.8% |
| Sanofi - Exscientia (2022) | $100m | up to $5.2bn | 1.9% |
| Novo Nordisk - Valo Health (2023) | $60m | up to $2.76bn | 2.2% |
| BMS - insitro (2020) | $50m | up to $2bn | 2.5% |
| Amgen - Generate (2022) | $50m | up to $1.9bn | 2.6% |
| Lilly - Isomorphic (2024) | $45m | up to $1.745bn | 2.6% |
| Novartis - Isomorphic (2024) | $37.5m | up to $1.2bn | 3.0% |

The pattern is not subtle. Across the platform deals, the incumbent puts down roughly 1-3 cents of every headline dollar today, and promises the other 97-99 cents only if the science actually works, one gate at a time. The BMS-insitro deal is the tell: an "up to $2bn" partnership that, several years in, had paid out on the order of $25m in early discovery milestones - a little over one percent of the headline. That is not a company betting $2bn on AI. That is a company buying a cheap lottery ticket and letting the market print the $2bn number for it.

Why would an incumbent structure it this way? Because it is buying **optionality**, not a drug. For a rounding error on its R&D budget, a big pharma company gets a call option on an unproven platform: if the AI lab produces something real, the incumbent has already locked up the rights to develop it; if the AI lab produces nothing (the base case, given that the first real efficacy test still fails about 60% of the time), the incumbent walks away having spent almost nothing. Running several of these small bets at once - Takeda alone is running two, with Insilico and Iambic - is exactly how you would play a technology you think *might* work but cannot yet count on. The deal structure is the incumbents telling you, in cash, that they are treating AI discovery as a promising experiment, not a sure thing.

Now the part that matters most: **even in the lucky world where the science works, the value does not land with the AI lab.** Walk the chain of who owns what. The AI company designs a molecule. Then the incumbent runs the clinical trials (Phase I, II, III - which is where 90%-plus of the cost and nearly all the risk sits). The incumbent takes it through the regulator. The incumbent manufactures it. The incumbent's salesforce sells it, and the incumbent's payer relationships get it reimbursed. Read the fine print of these deals and it is explicit: Takeda gets "exclusive worldwide rights to develop, manufacture and commercialize" whatever comes out of the Insilico work; Merck "retains exclusive rights to develop and commercialize" the Variational compounds; AstraZeneca owns the Absci antibody. The AI lab's reward is the small upfront, plus milestone payments it mostly never collects, plus a royalty - a single-digit-to-low-teens slice of sales on a product it does not own, control, or distribute. The molecule, the trial data, the approval, and the customer all belong to the incumbent.

That is the point the whole study keeps landing on. The AI lab is a **paid tool**, not an owner. It is closer to a very sophisticated contract research shop than to a drug company. It gets hired, it does clever work, it gets paid a fee and a thin back-end - and the durable, compounding value (the approved drug, the franchise, the distribution) accrues to the incumbent who owned the expensive, un-automatable half of the business all along.

The two other kinds of money flow in this field tell the same story from different angles. **Acquisitions** are incumbents buying the tool outright rather than renting it: Microsoft paid $19.7bn for Nuance not for a model but for the workflow rail already sitting inside most US hospitals; BioNTech paid ~$680m to fold InstaDeep's AI team into its own pipeline. In both cases a platform or a drug owner absorbed the AI capability into a business that already owned the scarce input. And **compute** deals are the one place the money is not contingent at all - because the supplier does not care whether any drug ever works. When Lilly and NVIDIA commit up to ~$1bn to a joint AI lab, or the Novo Nordisk Foundation funds a supercomputer, or GSK buys a Cerebras system, the chipmaker gets paid for the hardware and the cloud time whether or not a single molecule ever reaches a patient. NVIDIA's $50m stake in Recursion is the neatest illustration: it sells the shovels to the miners, and it also owns a piece of one miner - it wins on the picks either way. The compute layer is the one node in this whole map that collects real, non-contingent cash on every single bet at the table, which is exactly why the study flags it as a separate silicon story rather than a healthcare-AI one.

So the money map, top to bottom: incumbents pay small and contingent, and keep the drug; AI labs collect fees and thin royalties on assets they do not own; chipmakers get paid in full no matter what happens. The headlines are written in the AI labs' names. The value lands on the other two.

---

### Finding 5 - Run four moats through a break-it test, and only owning the workflow survives

*What I did.* I took the four moats the market keeps paying up for and tried to kill each one, giving each a verdict and an estimate of how long the advantage actually compounds.

- **Regulatory clearance. Does not hold up, ~0 years once granted.** A "barrier" that 1,451 firms have already cleared, with ~295 more crossing every year and a 142-day median review, is a commodity checkpoint. What does survive in its place is a different thing entirely: owning the payment code and the insurance coverage, which is worth maybe 5-8 years, and even that can get priced down.
- **Workflow embedding / distribution. Holds up under conditions.** The moat belongs to the platform, not to the app running on top of it. In February 2026 the dominant medical-records system (used by 42% of acute hospitals, covering 55% of beds) shipped its own built-in AI note-writing straight into the chart and the orders, at a rumored ~$80 per provider per month against incumbents charging several hundred [sell-side]. The leading note-writing startups' only real advantage was how deeply they plugged into that records system, and they were renting that depth from the platform. The landlord just became the competitor. It is a textbook case of a platform swallowing the apps on top of it, playing out live. This moat only survives where the app owns some scarce input the platform cannot cheaply reproduce.
- **Pharma distribution / owning your own pipeline. Holds up under conditions.** This is genuinely the only drug-discovery moat where value can accrue to a company. But it is a binary bet gated by the unchanged Phase II wall, not something that compounds. The model gets you in the door; it is not the moat.
- **Data flywheel. Holds up under conditions (breaks for discovery, survives for licensing).** The loop "more data makes a better model makes a better drug" is empirically broken, because the public copies caught the frontier. But the data-licensing flywheel survives just fine, because there the data itself is the product and the drug-company buyer carries the risk of whether it works. The strongest version of all, a single national insurer's dataset covering an entire population, is real but owned by the state, so no company you could invest in captures it.

*The one line that carries this section:* the durable value is in owning the payment rail, the physical asset, or the data plumbing, and never in the model, the raw-data flywheel, or the clearance certificate.

*Verdict.* **The only moat type that survives is owning a scarce input that refuses to become a commodity.** Everything else has a shelf life: a model about a year, a rented slot in someone's records system one to three years, a bare clearance basically zero once it is granted.

### Finding 6 - The rules act as a filter, and the US and Taiwan gates are shaped in opposite ways

*What I did.* I treated regulation not as a compliance checklist but as a filter that sorts the businesses: for each market, which rule binds which type of company, and which number that rule actually moves.

*What I found.* There are two gates, not one, and the binding gate is not the one you would guess. In the US, the FDA controls whether you can enter the market at all, and that gate is wide open. A separate body, Medicare (CMS), controls the size of the market by deciding what gets paid, and that gate is nearly shut. The US payment gate is a fragmented, climbable curve: win the national payer first, then sign up commercial insurers one at a time, and even a device that gets rejected can still be sold directly to patients for cash. The single event that would rewrite the entire per-test column at a stroke is a bill (introduced in 2025) that would create a defined payment category for "algorithm-based healthcare services" and guarantee at least five years of separate payment. The fact that such a bill needs to exist at all is the tell: there is no durable AI payment path today.

Taiwan flips the shape of the gate. It runs a single national insurer, so one committee decision is all-or-nothing: covered nationwide, or effectively impossible to sell at scale. And it all sits inside a budget fixed at about 7% of GDP, which makes every new AI payment zero-sum, because paying for one thing means not paying for another. The bar is set deliberately higher than in the US: to get paid, you have to prove through a randomized trial that your tool actually saves the insurer money, not merely that it is accurate. A standing AI payment does exist (a tool that predicts dangerous drops in blood pressure, paid since mid-2023 as a per-use point value, roughly NT$22.8m a year), which kills any assumption that "Taiwan is 100% pilots." But it took about two years and nine months to get there, and it is paid as a bundled medical material, not as a software service. So a pure documentation or triage AI, which is a perfectly good subscription business in the US, fails the Taiwan savings test unless it is tied to a specific downstream treatment whose cost you can point to.

*Verdict.* **Confirmed and consistent.** I re-checked every company's declared core variable against these rules and found no contradictions, and in three places the rules sharpened the case. The number that matters flips by market: in the US it is which way coverage is moving; in Taiwan it is whether the one gate cleared, and through which vehicle.

---

## The company universe, placed on the map

![The whole universe on two axes: business quality, moat duration, and market expectation](figures/00_positioning_master.png)

The companies are placed so that every layer of the value-chain map has someone standing in it. (A value chain just means the sequence of steps from raw inputs to the final customer, with a different set of companies at each step.) The diagnostics chain runs from reagents and sequencing machines, up through the lab, then the AI that interprets the results, then the clinical workflow, then the resale of de-identified data to drug companies, and finally the insurer who pays. The drug-discovery chain runs in parallel, from identifying a biological target, through generating candidate molecules, picking the best ones, translating them toward humans, and running the clinical trials, with a spine of computing power and AI models underneath the whole thing. The two chains touch at exactly one point worth drawing: selling diagnostics data to drug companies feeds directly into the target-identification step of drug discovery. That is the single connection where a diagnostics company quietly becomes a supplier to drug discovery.

Three things the map makes obvious. The crowd is bunched up at generating molecules and at clinical workflow, while the thinnest real occupancy is at pre-clinical translation, which is exactly the unsolved, value-bearing step, and tellingly nobody sells it as a standalone product. I flag that empty spot rather than paper over it. Nineteen names touch the drug-discovery ladder but only one has a genuine human proof-of-concept. And Taiwan is solid across the diagnostics chain but almost entirely missing from every layer of drug discovery. Its one load-bearing node there is computing silicon, which belongs to the semiconductor world, not to any healthcare-AI stock.

The per-company deep profiles live in **[`companies/`](companies/)**, one file per name. Each one reads the company through four lenses (its business model, where it sits in the value chain, who it competes with, and the handful of numbers that actually drive it), plus a verdict on its moat, a bear case, and a read on what the market is expecting. A verdict-at-a-glance table across all 94 is in **[`companies/INDEX.md`](companies/INDEX.md)**. The depth scales to the evidence: the public companies carry real financials, the private ones carry funding and moat-thesis, the Taiwan ones carry whatever the local filings disclose, and I flag where that is thin. The table below is the compact placement, and each row links into the detail.

*Key to the shorthand: DO = drug-owner, P&S = picks-and-shovels (sells tools to everyone else), WF = workflow-software, DP = data-platform, AIS = AI-services, SaMD = regulated software treated as a medical device, INF = infrastructure. Q = how good my evidence is on that specific name, which is not the same as how good the company is.*

| # | Company | Ticker | Region | Pub/Priv | Primary layer | Pattern | Q |
|---|---|---|---|---|---|---|---|
| 1 | Tempus AI | TEM | US | Pub | interpretive AI (+lab/workflow/data) | DP/AIS | high |
| 2 | Caris Life Sciences | CAI | US | Pub | interpretive AI (+lab/data) | DP/SaMD | high |
| 3 | Natera | NTRA | US | Pub | assay-lab-AI | SaMD/DP | high |
| 4 | Guardant Health | GH | US | Pub | assay-lab-AI | SaMD/DP | high |
| 5 | Exact Sciences | EXAS | US | Pub | assay-lab-AI | SaMD/WF | med |
| 6 | Personalis | PSNL | US | Pub | assay-lab-AI | SaMD/DP | high |
| 7 | Veracyte | VCYT | US | Pub | assay-lab-AI | SaMD/AIS | med |
| 8 | Invitae / Labcorp Genetics | NVTA (delisted) | US | Pub | assay-lab | SaMD | high |
| 9 | GE HealthCare | GEHC | US | Pub | imaging instrument/AI/workflow | INF/SaMD | high |
| 10 | Butterfly Network | BFLY | US | Pub | imaging instrument/AI | P&S/SaMD | med |
| 11 | Aidoc | private | US | Priv | imaging AI/workflow | WF/SaMD | med |
| 12 | Viz.ai | private | US | Priv | imaging AI/workflow/payment | WF/SaMD | high |
| 13 | Absci | ABSI | US | Pub | generation-to-clinical | DO | high |
| 14 | Recursion | RXRX | US | Pub | target-ID/selection-to-clinical | DO | high |
| 15 | Schrodinger | SDGR | US | Pub | generation/selection/clinical | P&S/DO | med |
| 16 | CRISPR Therapeutics | CRSP | US | Pub | edit-selection-to-clinical | DO | med |
| 17 | Beam Therapeutics | BEAM | US | Pub | edit-selection-to-clinical | DO | med |
| 18 | Intellia | NTLA | US | Pub | selection-to-clinical | DO | med |
| 19 | Prime Medicine | PRME | US | Pub | edit-selection | DO | med |
| 20 | Generate:Biomedicines | GBIO | US | Pub | generation-to-clinical | DO | med |
| 21 | Insilico Medicine | ISM | HK | Pub | target-to-clinical | DO | high |
| 22 | Isomorphic Labs | private | US | Priv | generation-to-clinical | DO | high |
| 23 | Xaira Therapeutics | private | US | Priv | target-to-translation | DO | med |
| 24 | Iambic Therapeutics | private | US | Priv | generation-to-clinical | DO | med |
| 25 | Genesis Therapeutics | private | US | Priv | generation-to-translation | DO | low |
| 26 | Retro Biosciences | private | US | Priv | target/selection | DO | low |
| 27 | Chai Discovery | private | US | Priv | generation/compute | P&S | high |
| 28 | EvolutionaryScale | private | US | Priv | generation/compute | P&S | med |
| 29 | OpenAI (life-sci) | private | US | Priv | compute/generation | INF | med |
| 30 | NVIDIA BioNeMo | NVDA | US | Pub | compute spine | INF | high |
| 31 | Anthropic (Claude for Life Sci) | private | US | Priv | compute/tooling | AIS | med |
| 32 | Latent Labs | private | US | Priv | generation | P&S | low |
| 33 | Abridge | private | US | Priv | clinical workflow | WF | high |
| 34 | Ambience Healthcare | private | US | Priv | workflow (+coding) | WF | high |
| 35 | Suki | private | US | Priv | clinical workflow | WF | high |
| 36 | Nuance / Dragon Copilot | MSFT | US | Pub | infra (+workflow) | INF | high |
| 37 | Commure (+Athelas) | private | US | Priv | workflow / RCM | WF | high |
| 38 | Waystar | WAY | US | Pub | revenue-cycle / payment | WF | high |
| 39 | Cohere Health | private | US | Priv | payer-side prior-auth | AIS | high |
| 40 | Anterior | private | US | Priv | payer-side reasoning | AIS | med |
| 41 | OpenEvidence | private | US | Priv | clinical decision support | AIS | high |
| 42 | Hippocratic AI | private | US | Priv | patient-facing agent | AIS | high |
| 43 | Doximity | DOCS | US | Pub | physician workflow | WF | high |
| 44 | Veeva Systems | VEEV | US | Pub | pharma data-platform | DP | high |
| 45 | Microsoft | MSFT | US | Pub | infra | INF | high |
| 46 | Alphabet | GOOGL | US | Pub | infra | INF | med |
| 47 | Amazon | AMZN | US | Pub | infra | INF | med |
| 48 | Oracle Health / Cerner | ORCL | US | Pub | EHR rail (+workflow) | INF | high |
| 49 | Epic Systems | private | US | Priv | EHR rail (+workflow) | INF | high |
| 50 | NVIDIA (Clara/BioNeMo) | NVDA | US | Pub | silicon toll | P&S | high |
| 51 | Ever Fortune AI 長佳智能 | 6841 TT | TW | Pub | diagnostics/imaging AI | SaMD | high |
| 52 | aetherAI 雲象科技 | 7803 TT | TW | Pub | digital-pathology AI | WF/SaMD | high |
| 53 | Acer Medical 宏碁智醫 | 6857 TT | TW | Pub | imaging-triage AI | SaMD | med |
| 54 | Amcad Biomed 安克生醫 | 4188 TT | TW | Pub | ultrasound CAD AI | SaMD | med |
| 55 | EBM Technologies 商之器 | 8409 TT | TW | Pub | imaging infra | WF/INF | med |
| 56 | Health2Sync 慧康 | 7851 TT | TW | Pub | chronic-disease monitoring | WF/DP | med |
| 57 | ASUS AICS 華碩 | 2357 TT | TW | Pub | documentation / coding | AIS/WF | low |
| 58 | Quanta QOCA 廣達 | 2382 TT | TW | Pub | medical-cloud platform | DP/INF | low |
| 59 | Wistron Medical 緯創醫學 | 3231 TT | TW | Pub | medtech ODM / smart-care | P&S/AIS | low |
| 60 | Foxconn CoDocator 鴻海 | 2317 TT | TW | Pub | medical foundation model | AIS/INF | low |
| 61 | Hospital AI centres (NTUH / VGHTPE / CGMH) | n/a | TW | Priv | data source / model-build | AIS | med |

### The expansion: incumbents, the rest of the world, and consumer health

The original map above is the US and Taiwan core. This round adds three groups the first pass missed: the big-pharma incumbents that actually fund AI drug discovery, the leading AI-health players outside the US and Taiwan, and the consumer and telehealth names. Full profiles are in [`companies/`](companies/); the one-line reads:


**Pharma incumbents - the capex funders**

| Company | Read |
|---|---|
| [AbbVie](companies/ABBV.md) | Diversified immunology incumbent that out-ran the Humira cliff via Skyrizi/Rinvoq and serial M&A; uses AI as a cheap internal tool plus a few option-sized deals (BigHat, Caris/ConcertAI) while keeping every asset - AI is immateria |
| [Amgen](companies/AMGN.md) | Durable diversified biotech that both funds and builds its own AI (owns deCODE data), but keeps value at L9 because it bears Phase-II risk and owns the molecule; equity is a MariTide-obesity and base-durability call, not an AI sto |
| [AstraZeneca](companies/AZN.md) | Good business, wide franchise/oncology moat - not an AI moat; the incumbent funds the AI, licenses shared oncology models, and now buys the AI outright (Modella) while keeping the drugs, trials, biomarkers, and value. AI is immate |
| [Bristol Myers Squibb](companies/BMY.md) | Good business, cheaply priced as a patent-cliff pharma not an AI story; the incumbent funds the AI (insitro >$2bn pact, Claude across 30,000 employees) and keeps the drug at L9, but a steep near-term Eliquis/Opdivo/Revlimid cliff  |
| [Eli Lilly](companies/LLY.md) | The mega-cap incumbent that funds AI drug discovery and keeps the value; AI is a cheap option and efficiency lever, immaterial to a ~$1.15tn valuation built on the GLP-1 franchise, not AI. |
| [GSK](companies/GSK.md) | Cash-rich incumbent and early AI-in-discovery mover (23andMe 2018, Cerebras 2022, Noetik virtual-cell subscription 2026) that funds the AI and keeps the drugs; AI is immaterial to a ~32.7bn-pound company whose real story is a 2028 |
| [Johnson & Johnson](companies/JNJ.md) | Diversified incumbent that funds the AI on BOTH chains - drug discovery (Isomorphic, milestone+royalty, keeps the molecules) and surgery (Ottava/Polyphonic, owns the robot + operating-room data) - and keeps the value; at ~$633bn o |
| [Merck & Co](companies/MRK.md) | Good, durable pharma franchise but the whole equity thesis is Keytruda-cliff succession, not AI; the cleanest incumbent example of the study's core claim - MRK funds the AI (Variational, Mayo, internal GenAI) and keeps the value b |
| [Novartis](companies/NVS.md) | One of the deepest AI adopters in big pharma - four external AI-discovery deals plus the data42 internal platform - and the cleanest European illustration of the study's rule: the incumbent funds the AI as cheap staged options and |
| [Novo Nordisk](companies/NVO.md) | GLP-1 mega-cap incumbent that funds AI (Valo milestones), rents its compute (Gefion, owned by its Foundation not itself), and keeps the drugs - but the moat is the eroding metabolic franchise, not AI; stock lives and dies on GLP-1 |
| [Pfizer](companies/PFE.md) | The cleanest incumbent case: Pfizer rents commoditizing AI models from the frontier labs, embeds them as an opex cost lever inside a $10-11bn R&D line, and keeps all the value at L9 because it owns the reimbursed molecule, the tri |
| [Roche](companies/RHHBY.md) | The incumbent most like a data platform - already owns Flatiron (outcomes), Foundation Medicine (genomics), and Genentech plus the largest disclosed pharma GPU footprint, but at ~$330bn on CHF 61.5bn revenue it is a pipeline bet,  |
| [Sanofi](companies/SNY.md) | Loudest "all in on AI" incumbent - 20,000-user internal plai tool plus 5+ external AI-discovery deals - but AI is immaterial to a ~$103bn cap; the real story is Dupixent concentration (~36% of sales) versus the coming patent cliff |
| [Takeda](companies/TAK.md) | Japan's largest pharma; funds the AI-discovery chain (Insilico ~$600m, Iambic up to $1.7bn) and keeps the assets, with one completed proof point (Schrodinger-designed, Takeda-owned zasocitinib through positive Phase III). AI is im |

**Global AI-native (Europe, China, Korea, Japan, India)**

| Company | Read |
|---|---|
| [Airdoc (Beijing Airdoc Technology)](companies/AIRDOC.md) | Clearest listed pure-play on retinal-image AI screening in China with real regulatory firsts and ~73% gross margins, but a sub-scale (~RMB173m) business whose core screen is commoditizing as rivals win the same NMPA Class III clea |
| [BeiGene (BeOne Medicines)](companies/ONC.md) | Real, cash-generative oncology franchise on a proven discover-develop-commercialize engine, but priced (~68x, ~5x sales) as a diversified global compounder when it is still ~70% one drug (Brukinsa), one year into GAAP profit, and  |
| [BioNTech](companies/BNTX.md) | Clearest EU AI-native drug play by capability (in-house InstaDeep stack) and best-capitalized name in the AI-drug cohort (~EUR 16.8bn cash, a $1.5bn-upfront partnered BNT327 lead), but today's value rests on the pipeline and the b |
| [Lunit](companies/LUNIT.md) | Korea AI-imaging champion with real global distribution and a 2027 breakeven path, but the cash core is acquired SaaS (Volpara) in a crowded low-pricing-power screening market and the durable moat leg (SCOPE pharma biomarker) is s |
| [Niramai Health Analytix](companies/NIRAMAI.md) | Real, clinically validated, FDA-touched radiation-free AI breast screen for the market mammography cannot reach - but a ~$9m-funded, ~74-person company selling a low-ASP screen into grant-funded public-health channels has not show |
| [Owkin](companies/OWKIN.md) | The EU's Tempus-for-pharma with a real, scarce pharma-access / GDPR-federated-data asset, but a moat that rents rather than owns; a ~$1bn 2021 unicorn mark its own carve-outs (Waiv, Bioptimus) and the commoditizing agentic-softwar |
| [Oxford Nanopore](companies/ONT.md) | A genuine sole-source nanopore platform monopoly with a real consumable annuity and an AI basecaller welded to the hardware, priced fairly (~5x EV/sales) because the market withholds a software multiple; the moat (~7-10yr of platf |
| [Ping An Healthcare (Good Doctor)](companies/PAGD.md) | Now-profitable China telehealth/AI-triage platform whose moat is the Ping An insurance channel, not its AI - about 60% of revenue is related-party F-end enablement, priced as a fair de-risked small-cap turnaround with no AI premiu |
| [Preferred Networks](companies/PFN.md) | Rare full-stack AI national champion, but as a healthcare-AI name it is an unpriced option not a thesis: drug discovery is one undisclosed vertical with no owned pipeline, no pharma economics, no recent financials, and no traded s |
| [Qure.ai](companies/QURE.md) | Clearest global-south leader in radiology-image AI - scarce distribution (4,500+ sites, 100+ countries), widest FDA-cleared chest-X-ray set, a WHO-cited TB franchise, capital-light per-scan model - but a small (~$23m), still-priva |
| [Sophia Genetics](companies/SOPH.md) | Real asset-light genomics-SaaS with software-grade margins and a small but genuine decentralized data-network moat; not yet a proven compounder - mid-teens constant-currency growth and live cash burn mean the thesis rests on reach |
| [Sysmex](companies/SYSMEX.md) | Profitable ~50%-share hematology leader with a durable reagent-annuity moat, cheap on a China/profit reset; the AI + genomics is honest optionality, not the engine - the study's incumbent-diagnostics control case. |
| [Tempus-China / iCarbonX](companies/ICARBONX.md) | China multi-omics data-platform analogue to Tempus in ambition, opposite in outcome: consumer data flywheel never got fuel (~6,000 tests, ~96 loci, <1,000 paying users), CFIUS force-divested the cross-border PatientsLikeMe leg, ~4 |
| [United Imaging](companies/UIH.md) | Genuine China #1-tier imaging OEM taking share from GE/Siemens/Philips with native AI in the box, but priced ~45-50x forward as a secular compounder when it is a capital-heavy, procurement-cycle-driven equipment maker whose overse |
| [Vuno (338220 / KOSDAQ)](companies/VUNO.md) | Rare breakeven medical-AI name, but a single-product, single-country business (DeepCARS ~74% of revenue) riding a reimbursement exception that hits its permanent test around mid-2026, with US FDA entry delayed; ~60% de-rate leaves |
| [WuXi AppTec (2359 / HKEX)](companies/WUXI.md) | Good, wide-moat, cash-generative picks-and-shovels CRDMO leader (FY2025 continuing-ops +21.4%, TIDES +96%, adj OCF RMB 16.67bn, RMB 58bn backlog) whose AI is an ancillary workflow tool, not the story - but the expectation is un-un |

**Consumer, telehealth and payer AI**

| Company | Read |
|---|---|
| [Function Health](companies/FUNCTION.md) | Good brand and a genuinely accumulating data asset, but priced ~$2.5bn (~25x est. run-rate) as a data platform when today it is a fast-growing, thin-margin subscription over a commodity, price-warring lab layer; rich until retenti |
| [Hims & Hers Health](companies/HIMS.md) | Good, cash-generative subscription brand with a real but rented consumer moat; the AI/data-flywheel that justifies the premium is still narrative, so the expectation is demanding - fair if the flywheel turns and GLP-1 margins norm |
| [Hinge Health](companies/HNGE.md) | Good business, real moat - but the moat is enterprise payer distribution and the 3,000-client contract book, not the motion AI, which is a margin-funding feature rivals also have; priced full for durable 25-35% compounding that co |
| [Omada Health](companies/OMDA.md) | Real evidence-and-distribution moat with an early profitability inflection, but growth rides a GLP-1 drug wave its own channel partners could bundle away and the AI is coaching-efficiency tooling not a cleared model - priced full- |
| [Oscar Health](companies/OSCR.md) | Well-run subscale ACA insurer with genuine AI-driven admin efficiency but no MLR lever and a thin moat, priced full for a durable margin recovery into a subsidy cliff (enhanced PTCs expired 31-Dec-2025, Senate blocked the extensio |
| [Teladoc Health](companies/TDOC.md) | Scaled, real and cheap at ~0.65x sales, but not a good business today: flat-to-declining revenue, a no-moat D2C half on a marketing treadmill, a shallow enterprise distribution moat eroded by its own visit-based pricing reset, and |

A few names I would not treat as clean healthcare-AI plays, flagged here so nobody mistakes them for one: Genesis Therapeutics, Retro Biosciences, and Latent Labs (all private, thin disclosure), and the four large Taiwan parents (ASUS AICS, Quanta QOCA, Wistron Medical, Foxconn CoDocator) whose healthcare-AI economics are buried inside a much larger business.

---

## The answer, in the data

I broke the driving question into nine smaller ones and graded each Yes / No / Conditional against the evidence above.

| # | Question | Verdict | Basis |
|---|---|---|---|
| 1 | Is healthcare AI a real durable business today | **Conditional** | Yes for narrow patterns (data-licensing, code-owners); no for pure-play model or clearance plays |
| 2 | Is AI drug discovery a *generation* revolution | **No** | It is a *picking* edge; Phase II success ~40%, unmoved; zero AI drugs approved by 2026 |
| 3 | Is the data flywheel a durable moat | **No (discovery) / Conditional (licensing)** | Broken where public data suffices; survives where the data itself is the product |
| 4 | Is FDA clearance a moat | **No** | ~1,451 cleared, ~97% fast-track; a commodity |
| 5 | Is payment (CMS / NHI) the binding constraint | **Yes** | 3 permanent codes vs 1,451 clearances; a single-payer chokepoint in Taiwan |
| 6 | Do the big pharma-AI deals signal conviction | **No** | Upfront is 1.2-3.0% of headline; cheap staged bets |
| 7 | Does the note-writing AI have a durable moat | **Conditional** | The product gets commoditized; only owning the workflow/records-system persists; the platform is now the competitor |
| 8 | Is Taiwan healthcare AI a durable business | **Mostly No** | Real activity, weak listed equity; the data moat belongs to the state; thin public names |
| 9 | Do the incumbents (equipment makers / records systems / pharma) capture the AI value | **Yes (tendency)** | They own the clearances, the workflow, and the milestone gates |

**Tally: 2 Yes, 3 No, 3 Conditional, 1 mostly-No.**

The one-line summary of the whole field: the disruption is real, but the durable value tends to accrue to whoever owns the payment rail or the scarce data or asset. And that is often the incumbent, not the AI startup the headlines get excited about. The equipment makers own the radiology clearances, the records systems own the workflow, and the drug companies own the milestone gates.

---

## Where I could be wrong, and which way it bends

- **The AI Phase-II numbers come from a small sample** (roughly two dozen molecules) [estimate]. If a bigger dataset showed AI molecules clearing Phase II above ~45-50%, Finding 4 is wrong, and drug discovery becomes a compounding business rather than a lottery. Which way I lean: my "no" is the cautious call on thin data, and I would rather be caught under-claiming here.
- **The payment wall is one law away from moving.** If the US passes a general permanent payment path for AI, the "narrow" picture in Finding 2 widens to "broad." Which way I lean: my skepticism is anchored to today's rules, which could change on a single vote.
- **Taiwan is my thinnest evidence.** There is no credible Taiwan-specific market size. I triangulated from two listed pure-plays that combine to under NT$600m, and one core count (cumulative device approvals, ~104) sits inside a document I could not fully extract. Treat the Taiwan section as directionally right and numerically soft.
- **Several load-bearing numbers came from analyst notes I could not always confirm against a primary source.** Where an analyst number was contradicted by a filing, I used the corrected value and flagged the original. For example, two cancer tests I had been told carried different Medicare rates turn out to both sit at the same $3,500, which erases a premium some comparison tables still show.
- **A model edge could revive the moat I broke.** If open models stall on the hardest brand-new-target cases while one proprietary lab pulls durably ahead, the model moat I refuted comes back. I do not think it will, but it is worth watching.

Every one of those is a specific, dated number I can be checked against, which is the point. A study you cannot lose is not research.

**Where this goes next.** The obvious extension is the computing floor sitting under both chains, the silicon toll that every training run and every inference pays whether or not any drug works or any code gets covered. I left it out here on purpose, because it is really a semiconductor story, not a healthcare-AI one, and it deserves its own study rather than a healthcare label pinned onto it.

---

## How this was built

- **Universe:** 94 companies across the US and Taiwan, public and private, picked so every layer of the value-chain map has at least one company in it. Thin-evidence names are flagged inline rather than dropped.
- **Sizing method:** each sub-sector sized from the bottom up as a first-pass valuation; the top-down market number is reported only to show the ~20-25x gap against measured spend, then set aside in favor of a rate-of-change number.
- **Clearance vs payment count:** cleared-device counts use the public regulator's device list, by authorization date, across all classes, for internal consistency; permanent-payment counts come from a public policy analysis of billing codes.
- **Drug-discovery funnel:** stage-transition base rates from public industry data; AI-molecule transition rates from a published small-sample study; per-stage cost from a published clinical-cost study; deal upfront-percentages computed from disclosed upfront and headline figures.
- **Moat test:** each candidate moat stated as a claim, given a real attempt to break it, a verdict (holds up / holds up under conditions / does not hold up), and an estimate of how long the advantage compounds.
- **Rules filter:** for each market, the statutory anchors come from primary regulatory, payer, and legislative records, mapped to which business pattern each rule binds and which core number it moves.
- **Provenance and cross-checks:** every load-bearing number carries a tag, [disclosed], [sell-side], [estimate], [reported], or [unverified]. Where an analyst figure was contradicted by a primary source, the corrected value is used and the original flagged. Sources were read privately, so this write-up is method-and-findings only.
- No fabricated figures; everything is reproduced from source materials. Byline: Hsin Cheng Yeh.
