# 35 — AI capex by company: who is actually paying for the build, and how exposed are they?

**The question.** Everyone says "the AI capital cycle." But a cycle made of *whom*? I wanted the real number, company by company: who is spending the capex, how fast it is growing, and — the part that actually decides who survives a downturn — whether each company is paying for the build out of its own cash or out of someone else's balance sheet.

**Why it matters.** If the AI buildout is a broad boom shared across the whole value chain, a wobble is survivable — lots of shoulders carry it. If instead the spend is a handful of names, and the people most stretched to fund it are a small debt-financed edge, then the risk is concentrated and nameable. You can watch it. That changes how you'd hedge an AI-exposed book.

## Summary of results

- Across **45 US-listed companies** spanning the whole AI value chain, latest-fiscal-year capex totals **about $520bn**. It is not a broad boom. The **top five names are 79% of it**; Amazon alone is a quarter.
- The five are the hyperscalers — **Amazon $132bn, Alphabet $91bn, Meta $70bn, Microsoft $65bn, Oracle $56bn**. Their combined capex grew **+73% in one year**, from $238bn to $413bn.
- Everyone else barely spends. Fabless silicon (Nvidia, Broadcom, AMD) and software (Palantir, Salesforce) run capex **under 3% of revenue** and throw off huge free cash flow. They *monetize* the build; they don't pay for it.
- The fragility is not the size of the spend — it is **how it's funded**. The cash-rich core self-funds (Microsoft, Alphabet, Meta, Nvidia all print double-digit-billions of free cash flow even after the build). The danger sits in a small edge that spends **more than its entire operating cash flow**: Oracle (−$24bn free cash flow), CoreWeave (capex 3.4× operating cash), and the neoclouds (capex 2–6× revenue, several with negative operating cash flow).
- **Following the cash (the deeper cut): in aggregate the build pays for itself.** The 45 names generated **$910bn of operating cash against $520bn of capex — a $390bn surplus** — and still returned **$182bn to shareholders**. Even the five biggest spenders self-fund (hyperscaler operating cash $588bn vs $413bn capex). "AI is a credit bubble" fails at the aggregate.
- **The debt is a choice for the core, a necessity for the edge.** Alphabet added **$37bn of net new debt — the same as Oracle** — but Alphabet also returned $46bn to shareholders and earned +$73bn free cash flow, while Oracle returned nothing and burned −$24bn. The tell that separates them: returning cash while building. Only **4 of 45 are genuinely debt-funded** (Oracle + neoclouds + utilities). The war chest agrees: Nvidia holds 7.5 years of capex in cash, the core 1–1.5, Oracle 0.6, CoreWeave 0.3.
- **Verdict: conditional.** "AI capex" as a market-wide phenomenon is a myth — it is five companies, and in aggregate they pay for it out of cash with a surplus. The systemic risk is narrow and nameable: Oracle and the neoclouds, the AI-build names funding with outside money (debt for Oracle and CoreWeave, equity raises for the smaller neoclouds) while burning cash, on the thinnest cushions.

This builds on study [27 — the AI capital cycle](../27-ai-capital-cycle/) (which priced the *blast radius* of a capex cut) and study [30 — LLM players forecast](../30-llm-players-forecast/) (which mapped the break-order). Here I do the thing under both: put a real, sourced capex number on every company and ask who can pay for what they started.

## What I expected, and how I'd know if I was wrong

The loose consensus you hear is that "the whole AI supply chain is spending hand over fist." My prior was the opposite, and sharper:

- **H0 (the thing I'm testing against):** capex is spread reasonably across the value chain — many layers, many names, each carrying a meaningful slice. A broad, shared boom.
- **H1 (what I expected to find):** capex is brutally concentrated in the demand layer (the hyperscalers), the rest of the chain spends little and instead *collects* the spend as revenue, and the real stress is a small set of names funding the build with debt and equity rather than cash.

What would have proven me wrong: if no single layer held more than ~40% of capex, if the top five names were under half the total, or if the self-funding picture were uniformly stretched (everyone burning cash, not just a fringe). Any of those would say "broad fragile boom" and kill H1. Let's see what the filings say.

## How I checked it

Capex has no "AI" label in any filing, so I went to the one place every US company has to report the cash it spent on plant and equipment: **SEC EDGAR**, the XBRL company-facts API. For each company I pulled three lines straight from the audited cash-flow and income statements:

- **capex** — cash paid for property, plant and equipment (`PaymentsToAcquirePropertyPlantAndEquipment` and its tag siblings; some firms tag it `PaymentsToAcquireProductiveAssets`, a REIT tags it `PaymentsToDevelopRealEstateAssets`).
- **revenue** — total net revenue.
- **operating cash flow** — net cash from operating activities.

From those three I built the only three lenses that matter:

| lens | formula | what it tells you |
|---|---|---|
| **magnitude** | capex, and capex YoY | how big the spend is, and how fast it's ramping |
| **intensity** | capex / revenue | how capex-heavy the business model is |
| **self-funding** | capex / operating cash flow | >100% means the build outruns the cash the business throws off — it's funded by the balance sheet |
| **free cash flow** | operating cash flow − capex | negative = burning cash to build |

**One method choice worth explaining.** I used each company's latest *full fiscal year*, not a trailing-twelve-month figure. Cash-flow-statement items in a 10-Q are reported year-to-date (cumulative within the fiscal year), so naively summing quarters double-counts. The annual 10-K number is clean and audited. The cost is that fiscal years end on different dates (Microsoft June, Nvidia January, Oracle May, most others December), so this is a snapshot of "each company's most recent complete year," not a single calendar instant. For a spend that's ramping this fast, I'd rather have clean audited numbers than a fragile same-date splice.

## The data

**Universe — 45 US-listed filers across ten value-chain layers**, chosen to span the chain end to end rather than cherry-pick the famous names: the demand layer (hyperscalers), the GPU-cloud "neoclouds," compute silicon, foundry/memory, semicap equipment, networking/optical, servers/ODM, data-center REITs, power/cooling, and software. Every name is a US filer with capex in standard us-gaap tags. Foreign capex giants (TSMC, Samsung, SK Hynix, Alibaba, Tencent, Nebius) are **out of scope** — they don't file capex in us-gaap XBRL — which means the real global AI capex number is materially larger than my $520bn (see caveats). One US name, NextEra (NEE), files capex under a custom non-standard tag and is excluded rather than guessed at.

- Source: SEC EDGAR XBRL `companyconcept` / `companyfacts`. Range: latest reported fiscal year (FY2025 for most; FY2026 for May/January year-ends already filed). Transform: none — values are as-reported, in USD.
- Capex is **gross** purchases of PP&E (the cash outflow line). A few firms, Amazon most notably, report proceeds/incentives on a separate line, so their *net* capex is a little lower than the gross figure here. I use gross because it's the consistent, comparable line across all 45 names.
- For the funding side (Findings 4–6) I pull, from the same filings: cash & equivalents, short-term investments, total debt (long-term plus current portion), and the financing-statement flows for buybacks and stock issuance. Net new borrowing is measured as the **year-over-year change in the total-debt stock**, not the issuance/repayment cash-flow lines — those are inflated by commercial-paper that's issued and repaid many times a year (Alphabet's gross issuance line reads $65bn against a $37bn actual rise in its debt). Tags vary far more here than for capex, so each concept uses a fallback list; anything that won't resolve cleanly is left blank, never guessed.

Raw pulls: [`data/capex_raw.csv`](data/capex_raw.csv), [`data/funding_raw.csv`](data/funding_raw.csv) · computed tables: [`data/capex_table.csv`](data/capex_table.csv), [`data/funding_table.csv`](data/funding_table.csv) · pull + build code: [`src/`](src/).

## What the data looks like first

Before any analysis, just rank the 45 names by capex and look.

![Capex by company](figures/capex_by_company.png)

The shape is the finding. Five bars, then a cliff. The sixth-largest spender (Micron, $16bn) is less than a third of the smallest hyperscaler. This is not a boom with broad participation — it's an oligopoly of spenders with a long tail of much smaller ones. Now let's earn each piece of that.

## Finding 1 — AI-market capex is five companies

**What I expected & why.** H1 said the demand layer would dominate, because the hyperscalers are the ones building the data centers everyone else sells into. I expected concentration, but I wanted to measure exactly how much.

**How I measured it.** Sum capex across all 45, then look at the top-five share and the layer rollup.

```python
total = sum(r.capex for r in companies)            # $520bn
top5  = sum(sorted(capex, reverse=True)[:5])       # $413bn
top5_share = top5 / total                          # 0.79
# layer rollup: groupby(layer).capex.sum()
```

**What the data shows.**

| layer | capex ($bn) | names | share |
|---|---:|---:|---:|
| Hyperscaler | 413.2 | 5 | 79.5% |
| Power / cooling | 32.8 | 8 | 6.3% |
| Foundry / memory | 30.5 | 2 | 5.9% |
| Neocloud | 13.8 | 6 | 2.7% |
| Compute silicon | 9.2 | 5 | 1.8% |
| Data-center REIT | 7.5 | 2 | 1.4% |
| Servers / ODM | 5.0 | 3 | 1.0% |
| Semicap equipment | 3.4 | 4 | 0.7% |
| Software / apps | 2.7 | 5 | 0.5% |
| Networking / optical | 1.8 | 5 | 0.3% |

One layer is four-fifths of the spend. The capex concentration index (Herfindahl on company shares) is about **1,440** — squarely in "concentrated" territory for what's supposed to be a whole-sector boom. And the five aren't coasting: combined hyperscaler capex went from **$238bn to $413bn in a single year, +73%**, led by Oracle (+162%), Meta (+87%) and Alphabet (+74%).

**Why (mechanism).** This is what a demand-pull buildout looks like. The hyperscalers own the end demand (cloud, ads, AI services), so they're the ones writing checks for land, buildings, power and GPUs. Everyone upstream gets paid *by* those checks — they don't have to write their own.

**What I checked.** Could the concentration be an artifact of my universe — did I just include too many tiny names downstream? No: even if I drop the entire tail and keep only the 17 names spending over $2bn, the top five are still 82% of *that* subset. The cliff is real, not a denominator trick.

**Verdict: confirmed.** Capex is five companies. H0 (a broad, shared boom) is rejected on its face.

## Finding 2 — everyone else doesn't pay for the build; they cash it

**What I expected & why.** If the hyperscalers are the spenders, the upstream chain should show the mirror image: low capex relative to revenue, and fat free cash flow. The fabless chip designers and the software firms in particular should be near-zero-capex businesses that simply sell into the build.

**How I measured it.** Capex intensity (capex/revenue) per name, and free cash flow (operating cash flow − capex).

```python
intensity = capex / revenue
fcf       = operating_cash_flow - capex
```

**What the data shows.**

![Free cash flow by company](figures/fcf_by_company.png)

The split is stark. **Nvidia spends $6bn of capex on $216bn of revenue — 2.8% intensity — and throws off $97bn of free cash flow.** Broadcom: 1.0% intensity, +$27bn. The software names are even lighter: Palantir 0.8%, Salesforce 1.4%, ServiceNow 6.5%. These businesses are *asset-light by design* — they sell the picks and shovels, or the seats, and let the hyperscalers carry the steel and silicon on their balance sheets.

Put the two findings together and the structure of the whole market falls out: a handful of hyperscalers pay, and the chain above them collects. The top of the free-cash-flow table (Nvidia +$97bn, Alphabet +$73bn, Microsoft +$72bn) and the bottom (Oracle −$24bn, CoreWeave −$7bn) are *the same buildout* seen from the two ends.

**Why (mechanism).** Capex intensity is a fingerprint of where you sit in the chain. Own the fabs or the data centers and you spend 25–80% of revenue on plant. Design the chip and outsource the fab, or sell software, and you spend almost nothing. The AI build is enormous, but for most of the value chain it shows up as *demand*, not as *spend*.

**What I checked.** Is the fat free cash flow just because these firms are bigger? No — intensity is a ratio, size-neutral, and it still separates cleanly: fabless and software cluster under 5%, foundry/REIT/utility cluster 25–55%, hyperscalers in between at 18–35%. The layer, not the size, predicts the intensity.

**Verdict: confirmed.** The value chain monetizes the build; it does not fund it. Which raises the real question — among the ones who *do* fund it, who can actually afford it?

## Finding 3 — the fragility is the funding, not the magnitude

**What I expected & why.** This is the one that matters for risk. A $130bn capex bill is not dangerous if you generate $140bn of operating cash. It's very dangerous if you generate $32bn and are spending $56bn. So I expected the hyperscaler *core* to be safe (self-funded) and a specific *edge* to be exposed (spending past its cash).

**How I measured it.** Self-funding ratio = capex / operating cash flow. Above 100% means the build is bigger than all the cash the business produced that year — the gap has to come from the balance sheet (cash reserves, new debt, or new equity).

```python
self_funding = capex / operating_cash_flow      # >1.0  ->  build outruns internal cash
burning      = (operating_cash_flow - capex) < 0 # negative free cash flow
```

**What the data shows.**

![Intensity vs self-funding](figures/intensity_vs_selffunding.png)

The chart sorts the whole market into two worlds along the dashed 100% line.

- **Below the line — the self-funded core.** Microsoft (47%), Alphabet (56%), Meta (60%), Nvidia (6%). Even Amazon, the biggest spender, lands right at 95% — its $132bn build is almost entirely covered by its $140bn of operating cash, leaving a thin but *positive* $8bn of free cash flow. These names could keep building through a downturn out of their own pockets.
- **Above the line — the funded-by-someone-else edge.** Oracle spends 174% of its operating cash flow, posting **−$24bn of free cash flow** — the one mega-cap genuinely funding its AI build with debt. The neoclouds are further out: CoreWeave at 337% (capex 3.4× operating cash), and CIFR, APLD, WULF actually run *negative* operating cash flow while spending billions — their capex is funded entirely by raising money. Their intensity runs 200–600% of revenue.

The capex-heavy utilities (Southern, Duke) and Intel also sit above the line, but that's the normal life of a regulated utility or a turnaround fab, not an AI-specific fragility — I separate them out in the rivals section.

**Why (mechanism).** Self-funding is solvency-through-a-cycle in one number. When financing stays cheap and available, spending past your cash flow is fine — you just roll it. The moment lenders re-underwrite (tighter terms on GPU collateral, wider credit spreads), the names above the line are the ones who can't simply slow down and coast on internal cash. They have to *refinance to keep building*. That is exactly the "financing-refusal trigger" study 27 and study 30 identified as the thing that fires first — and here it has names and numbers: Oracle, CoreWeave, the neoclouds.

**What I checked.** I'll do that next, because the obvious objection is that some of these high-self-funding names are perfectly safe.

**Verdict: confirmed, and it's the load-bearing finding.** The risk in the AI build is not the $520bn. It's the slice of it being funded on credit — a thin, identifiable edge, plus one mega-cap (Oracle).

## Digging deeper: how is the build actually funded?

Finding 3 said the danger is the funding, not the magnitude. That's a claim about *sources of cash*, so I went and pulled them: each company's cash war-chest, its total debt and how much that debt changed in the year, and how much stock it bought back or issued. Three more findings come out, and they sharpen the verdict in a direction I did not expect.

## Finding 4 — step back, and the whole thing pays for itself

**What I expected & why.** The bear case is "AI is a credit bubble": capex outruns cash, so the build is floated on debt. If that's true at the level of the whole AI market, the 45 companies together should be cash-negative.

**How I measured it.** Sum operating cash flow and capex across all 45, and add up the year's net new debt and net cash returned to shareholders.

```python
total_ocf   = sum(c.operating_cash_flow for c in companies)   # $910bn
total_capex = sum(c.capex for c in companies)                  # $520bn
aggregate_fcf = total_ocf - total_capex                        # +$390bn
net_new_debt  = sum(c.total_debt - c.total_debt_prior)         # +$176bn
returned      = sum(c.buybacks - c.stock_issued)               # +$182bn
```

**What the data shows.** The 45 names generated **$910bn of operating cash against $520bn of capex — a $390bn surplus** — and still handed **$182bn back to shareholders**, while adding $176bn of net new debt (the debt and the buybacks roughly cancel). Even if you keep only the five biggest spenders, the hyperscalers alone produced **$588bn of operating cash against $413bn of capex, a $175bn surplus.** The build is not floated on debt in aggregate; it is funded out of the largest corporate cash engines that have ever existed, with money left over.

**Why (mechanism).** Capex is enormous in dollars but modest against the cash these businesses throw off. Microsoft and Alphabet each generate ~$140–165bn of operating cash a year; a $65–91bn build is large but leaves a surplus. The dollars are scary in isolation and unremarkable next to the cash flow behind them.

**What I checked.** Nvidia's +$97bn of free cash flow flatters the aggregate — it collects the build rather than paying for it (Finding 2). Fair. So I stripped it out: the remaining 44 still self-fund, and the five hyperscalers self-fund on their own. The surplus is not a one-name artifact.

**Verdict: confirmed — the "AI is a credit bubble" framing fails at the aggregate.** The risk is not that the sector can't pay; it's that a small part of it pays differently. Which is the next finding.

## Finding 5 — the debt is a choice for the core, a necessity for the edge

**What I expected & why.** Borrowing by itself says nothing — a company can borrow because it must, or because debt is cheap and buying back stock with it is efficient. To tell them apart you need one more fact: is the company *also returning cash to shareholders* while it builds? If yes, the debt is optimization. If it's borrowing while burning cash and returning nothing, the debt is necessity.

**How I measured it.** For each company: net new borrowing (the year's change in total debt), net cash returned (buybacks minus stock issued), and free cash flow. Then plot return-to-shareholders against free cash flow, sizing each by how much debt it added.

```python
net_borrow = total_debt - total_debt_prior      # YoY change in the debt stock
net_return = buybacks - stock_issued            # >0 = handing cash back
# the tell: returning cash to holders WHILE building => debt is a choice
```

**What the data shows.**

![Is the debt a choice or a necessity?](figures/funding_quadrant.png)

The single most revealing number in the whole study: **Alphabet added $37bn of net new debt this year — exactly as much as Oracle did.** But Alphabet also generated +$73bn of free cash flow and handed +$46bn back to shareholders in buybacks. Oracle generated **−$24bn of free cash flow, returned nothing, and is funding the gap with the borrowing.** Same $37bn of debt; opposite meaning. Meta is Alphabet's twin (+$30bn debt, +$26bn returned, +$46bn FCF). Microsoft actually *paid down* debt and returned $16bn. The core borrows the way a homeowner with full pockets takes a cheap mortgage; Oracle borrows the way someone covers a shortfall.

Across all 45, the funding split is lopsided toward health: **32 of 45 self-fund the build** (21 of them while also returning cash), and only **four are genuinely debt-funded** (Oracle, CoreWeave, and the two regulated utilities) with another four raising equity. Among the five hyperscalers, four self-fund and **Oracle stands completely alone** as the one paying for its build with outside money.

**Why (mechanism).** Issuing cheap investment-grade debt and using it to buy back stock is textbook balance-sheet optimization for a company swimming in cash — it lowers the cost of capital without touching the build. Oracle and the neoclouds aren't optimizing; their operating cash can't cover the capex, so the debt closes a real gap. The behavior looks superficially similar (both "borrowed billions") and is economically opposite.

**What I checked.** The two utilities (Duke, Southern) land in the debt-funded bucket, but that's how regulated utilities always operate — they fund rate-based investment with debt recovered through tariffs, AI or no AI. Stripping them out leaves Oracle and the neoclouds as the only AI-build names funding with debt, which is exactly the set Finding 3 flagged on self-funding ratio. Two independent lenses (capex/operating-cash, and the change in the debt stock) point at the same names.

**Verdict: confirmed, and it reframes the risk.** Net borrowing is not the danger signal. Net borrowing *with negative free cash flow and nothing returned to shareholders* is — and that test isolates Oracle and the neoclouds from a core that is borrowing by choice.

## Finding 6 — the war chest: who could keep building if financing stopped tomorrow

**What I expected & why.** The thing that decides who survives a financing freeze is how long they can keep building from cash already in the bank. So I measured each company's liquidity (cash plus short-term investments) against its annual capex — years of capex sitting in reserve.

**How I measured it.**

```python
runway_years = (cash + short_term_investments) / annual_capex
```

**What the data shows.**

![Who could fund the build from cash on hand](figures/war_chest.png)

Nvidia holds **7.5 years** of its (small) capex in cash. The cash-funded core holds one to one-and-a-half years (Microsoft 1.5, Alphabet 1.4, Meta 1.2) — enough to keep building straight through a frozen market. Then the line drops: Amazon 0.9, Oracle **0.6**, CoreWeave **0.3**. The names that depend on financing are exactly the ones with the least cash to fall back on if it disappears.

**Why (mechanism).** The war chest is optionality. A core name can shrug off a year of closed credit markets and keep spending from reserves; Oracle and the neoclouds would have to slow the build or raise on whatever terms are offered. The cushion and the funding source line up: the self-funders also hold the most cash, the debt-funders the least.

**What I checked.** The two utilities sit at the very bottom (Southern 0.1, Duke 0.0), but utilities deliberately hold almost no cash — they run a continuous debt-funded capital program, so a thin war chest is normal there, not a warning. Same carve-out as Finding 5.

**Verdict: confirmed.** The runway maps cleanly onto the core/edge split: the companies most dependent on outside financing are the ones with the least cash to survive without it.

## Did I just find noise?

A few honest stress tests:

- **Is the concentration a universe artifact?** Covered in Finding 1 — drop the long tail, keep only $2bn+ spenders, and the top five are still 84%. Adding *more* small names would only push concentration higher, not lower.
- **Are the fragile names fragile because of one weird year?** Look at the growth, not just the level. CoreWeave, CIFR, APLD, WULF all show capex growing faster than revenue for two straight years — the gap is structural, not a one-off. Oracle's self-funding went from comfortable to 174% as FY2026 capex tripled; it's a deteriorating trend, not a blip.
- **Costs / definitional drift.** Switching Amazon from gross to net capex (about $13bn of incentives) moves it from 95% to roughly 86% self-funding — still positive free cash flow, still in the safe camp. The verdict doesn't hinge on the gross/net choice for any name near the line.

## Steelman the rivals

Three competing stories, each tested:

1. **"The high-self-funding names are just utilities and that's normal."** Partly true, and it's why I separate them. Southern (130%) and Duke (114%) spend past operating cash flow every year — regulated utilities always do, funding rate-based grid investment with debt they recover through tariffs. That is *not* AI fragility. But stripping the utilities out doesn't save the thesis-relevant edge: Oracle, CoreWeave and the neoclouds remain above the line, and their build is AI data centers, not regulated grid. The rival explains the utilities; it doesn't explain Oracle.
2. **"Capex isn't AI capex — Amazon's number is mostly warehouses."** A real contamination, and it cuts in my favor on magnitude (the true *AI* figure is lower than $520bn) but against me on nothing structural. Amazon's fulfillment capex inflates its dollar level, yet Amazon is still self-funded (95%), so it stays in the safe camp regardless. The contamination changes the size of the boom, not who's exposed.
3. **"Negative free cash flow is the strategy, not a warning."** This is management's own framing — CoreWeave and Oracle both say they're deliberately deploying ahead of revenue against a contracted backlog. Fair. But "deploying ahead of revenue" *is* the dependency on financing staying open. The strategy and the fragility are the same fact viewed from two sides; the data can't tell you the backlog won't convert, only that the build is bet on outside money continuing to flow.

## The answer, in the data

**Is "AI capex" a broad market-wide boom? No. Is it dangerous? Only at a nameable edge — conditional yes.**

It is five companies (79% of $520bn), growing 73% a year, with the rest of the value chain collecting the spend as revenue rather than funding it. Following the cash settles the bigger question: in aggregate the build pays for itself — $910bn of operating cash against $520bn of capex, a $390bn surplus, with $182bn handed back to shareholders on top. The systemic risk is not the aggregate and not the dollar figure. It is a small, nameable set — Oracle and the neoclouds — that funds its build with outside money (debt for Oracle and CoreWeave, equity raises for the smaller neoclouds) while burning cash and returning nothing, on the thinnest cash cushions in the group. They are the names to watch when the financing window tightens.

| metric (45 US filers, latest FY) | value |
|---|---:|
| Total capex | $520bn |
| Top-5 (hyperscaler) share | 79% |
| Largest single spender (Amazon) | $132bn (25%) |
| Hyperscaler combined capex YoY | +73% |
| Median capex intensity (capex/revenue) | 6.5% |
| Median fabless-silicon intensity | 2.8% |
| **Aggregate operating cash flow** | **$910bn** |
| **Aggregate capex** | **$520bn** |
| **Aggregate free cash flow (surplus)** | **+$390bn** |
| **Net cash returned to shareholders** | **$182bn** |
| **Net new debt raised** | **$176bn** |
| Companies that self-fund the build | 32 of 45 (21 also return cash) |
| Genuinely debt-funded (AI build) | Oracle + neoclouds (utilities separate) |
| War chest — Nvidia / core / Oracle / CoreWeave | 7.5 / ~1.3 / 0.6 / 0.3 yrs of capex in cash |

## Caveats (with the direction of the bias)

- **US filers only — understates the true total.** TSMC, Samsung, SK Hynix, Alibaba, Tencent and Nebius file capex outside us-gaap XBRL and aren't here. They are huge: TSMC alone guided around $40bn for 2025. The real global AI capex number is well above $520bn; my concentration figure (top-5 = 79%) is therefore an *overstatement of US concentration* and would fall somewhat if foreign foundries/clouds were included. The *direction* of the finding (concentrated, demand-led) holds; the exact share would soften.
- **Capex is not "AI capex."** It's all PP&E. Amazon's warehouses, the utilities' grid, Intel's non-AI fabs are all in here. This inflates the dollar magnitude (the AI-only figure is lower) but does not change who is self-funded vs not.
- **Gross capex, mixed fiscal-year ends.** Gross of disposal proceeds/incentives (matters mainly for Amazon), and each company's latest full year ends on its own date, so this is a rolling snapshot, not a single instant.
- **NextEra excluded** (custom capex tag); one real US power-capex spender is missing from the power layer.

## Reproducibility

Every number here comes from SEC EDGAR XBRL, no API key required. The capex side and the funding side are each a pull plus a build:

```bash
cd 35-ai-capex-by-company
python3 src/pull_capex_edgar.py    # -> data/capex_raw.csv     (capex/revenue/OCF per name, all fiscal years)
python3 src/01_build_table.py      # -> data/capex_table.csv    (intensity, self-funding, FCF, concentration)
python3 src/02_figures.py          # -> figures/capex_*, fcf_*, intensity_*
python3 src/03_pull_funding_edgar.py  # -> data/funding_raw.csv (cash, debt, buybacks, equity per name)
python3 src/04_build_funding.py    # -> data/funding_table.csv  (war chest, net borrowing, funding class)
python3 src/05_funding_figures.py  # -> figures/funding_quadrant, war_chest
```

Two method subtleties, both in code:
- **Capex tag selection.** Pick the tag whose series reaches the **latest** period end-date (so a tag-switcher like Amazon resolves to its current tag, not the retired one), and key annual values by the **period end-year**, not the filing's stated fiscal year (which mislabels comparative prior-year rows). That single fix is the difference between Amazon reading $5bn (stale tag, FY2016) and $132bn (current tag, FY2025).
- **Net new borrowing.** Measured as the year-over-year change in the total-debt stock, not the financing-statement issuance line, which is inflated by commercial-paper roll. Oracle's total-debt tag is non-standard (`DebtLongtermAndShorttermCombinedAmount`, $129.5bn) — the puller carries a fallback list so the most important fragility name resolves correctly. See [`src/pull_capex_edgar.py`](src/pull_capex_edgar.py) and [`src/03_pull_funding_edgar.py`](src/03_pull_funding_edgar.py).

## References & forward pointer

- **Data:** SEC EDGAR XBRL frames/company-concept API (public-domain corporate filings).
- **Builds on:** [27 — the AI capital cycle](../27-ai-capital-cycle/) (blast radius of a capex cut) and [30 — LLM players forecast](../30-llm-players-forecast/) (the break-order down the chain). This study supplies the per-company capex and funding numbers those two reason *about*.
- **Next:** the natural extension is to add the foreign capex giants (TSMC, Samsung, SK Hynix, Alibaba) from their own filings to get a true global AI-capex total, and to track the self-funding ratio of the fragile edge quarter by quarter — it's the single most direct read on when the financing perimeter starts to bind.

*Research, not investment advice.*
