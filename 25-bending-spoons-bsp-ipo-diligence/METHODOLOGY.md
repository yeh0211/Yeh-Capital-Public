# Methodology - Bending Spoons ($BSP) IPO due diligence

## Evidence Hierarchy

This note uses a strict source hierarchy:

1. **SEC-filed facts.** Financials, IPO mechanics, governance, risk factors, acquisition accounting, pro forma information, and public-company transaction terms come from EDGAR filings wherever possible.
2. **Company claims.** Product descriptions, transformation examples, hiring model, AI/platform claims, and business-positioning language are treated as company claims unless independently verified.
3. **Press-reported facts.** Layoffs, deal context, and market narrative are included when reported by credible business/technology press and are labeled as press evidence.
4. **Community/customer signal.** Reddit, Hacker News, forums, app stores, Trustpilot, and similar sources are used only to map user concerns and reputational/product-risk patterns.
5. **Analytical inference.** Any conclusion about the operating model, risk, or IPO framing is explicitly an inference from the source stack.

## SEC Refresh Process

- The latest public SEC filing located in the publication check was the Form F-1 filed June 8, 2026, accession `0001104659-26-071170`.
- The SEC filing detail page showed Form F-1, filing date 2026-06-08, accepted 2026-06-08 07:09:31, with 60 documents.
- A public EDGAR/search pass on 2026-06-09 did not locate a later F-1/A.
- If a later amendment appears, this note should be updated before being used as current IPO diligence.

## Financial Verification

The following figures were checked against the F-1-derived diligence record and treated as SEC-filed facts:

- Revenue, operating income, adjusted operating income, net income, cash flow, cash, assets, liabilities, shareholders' equity, and debt.
- Revenue mix by subscription, advertising, and other revenue.
- Monthly active user and monthly paying customer metrics, with the non-de-duplicated caveat.
- Pro forma revenue and net income/loss for Eventbrite, AOL, and Vimeo.
- Acquisition enterprise value / purchase consideration where disclosed.
- Governance and high-vote share structure.
- Internal-control material weaknesses and other listed risk factors.
- Interest expense for all five periods, the per-facility hedged rates, the contractual debt-maturity schedule, the leverage covenant, and the acquisitions-vs-capex split inside investing cash flow.

## Cash-Flow-Quality And Leverage Analysis

The deepened section of this note reads the cash flow statement against the company's preferred "adjusted operating income" metric. The computed ratios are all simple arithmetic on filed figures, recomputed independently:

- **Cash conversion** = operating cash flow / adjusted operating income.
- **Funding mix** = operating, investing, and financing cash flow as filed; investing is treated as ~100% acquisitions because filed capex is under $1m a year and the company capitalizes essentially no internal software.
- **Interest cover** = GAAP operating income / interest expense.
- **Leverage** = period-end debt (gross and net of cash) over four different denominators: the company's pro-forma adjusted-EBITDA-plus-cost-savings base, annualized Q1 2026 adjusted operating income, trailing 2025 adjusted operating income, and 2025 GAAP operating income.

Two honesty rules govern this section:

- **Like-for-like periods only.** Operating cash flow is seasonally weakest in the first quarter, so a Q1 ratio is never compared against a full-year ratio. The headline cash-conversion decline reported here is the full-year figure (68% in 2024 to 47% in 2025); Q1 2026 is compared only against Q1 2025.
- **Adjusted vs cash metrics are flagged.** Adjusted operating income is measured before interest and tax; operating cash flow is after both. For a company tripling its debt, the two diverge by arithmetic, so the note states this explicitly and uses the OCF-versus-GAAP-operating-income comparison as a cross-check.

The leverage multiples carry a period-matching caveat: a point-in-time post-acquisition balance sheet is placed over pre-acquisition full-year income, which overstates the multiple in absolute terms. Correcting for it does not get anywhere near the reported 2.19x (pro-forma 2025 revenue was only $2.608bn and pro-forma net income $22.4m), so the directional conclusion — leverage on any actually-earned metric is mid-single-digit to low-teens — is robust.

## Conglomerate Classification

Each owned business was classified by end-market and customer type, then assessed for whether it shares product, customers, billing, or go-to-market with the others. The conglomerate-versus-roll-up call follows from that map: a roll-up consolidates one fragmented market; a conglomerate holds unrelated businesses for cash. The classification is judgement applied to the F-1's descriptions, not a financial measurement, and is labeled as inference.

## Community Signal Method

The community section is designed to answer: "What product/customer failure modes recur across independent user communities?"

It does **not** attempt to measure representative sentiment, quantify churn, or prove financial impact. The main limitations are:

- Negative selection: unhappy users are more likely to post.
- Power-user bias: Reddit/HN/forums skew toward technical and high-engagement users.
- Anecdotal evidence: individual comments can be wrong, incomplete, or unrepresentative.
- Platform moderation and review-solicitation effects: Trustpilot, app stores, and forums each have their own sampling problems.

The memo therefore uses community evidence only when a theme recurs across multiple products or platforms: pricing, free-tier restrictions, layoffs, support/product quality, migration behavior, fear of PE-style behavior, AI/privacy concerns, and positive counterpoints about product survival or faster release velocity.

## Public-Note Cleanup Rules

- No private paths, API keys, internal logs, or unpublished source material.
- No long user quotes.
- No claim is presented as a recommendation.
- Press and community material is separated from SEC-filed facts.
- The memo uses rounded figures and concise public wording rather than raw draft notes.
