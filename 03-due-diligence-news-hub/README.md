# 03 — A due-diligence news hub: verified event tracking for one name

**Question.** Can fragmented, mixed-reliability sources — filings, financial press, and social chatter — be turned into a verified, source-scored event timeline for a single fast-moving company, separating fact from rumour reproducibly?

**Finding.** Yes, as a methodology. A single-name pipeline ingests and extracts coverage, then routes every claim through an **independent verification gate** that promotes an item to "fact" only at confidence > 70, producing a clean timeline with unverified chatter quarantined. This is an **engineering / methodology case study** (built on Tempus AI, $TEM) — not a return backtest. Its honest test is the verifier's precision and recall, set out below.

> Methodology / tooling case study. Design and approach only — no code, keys, endpoints, or deployment. Not investment advice; not a backtested signal.

## The problem

Diligence on a fast-moving AI-healthcare name means reconciling sources that disagree and vary wildly in reliability:

- **Primary** — SEC filings (8-K / 10-Q), investor-relations releases
- **Secondary** — financial press
- **Noisy / early** — Reddit, X, and other social chatter, where a partnership "rumour" can move the stock days before it is confirmed (or turns out false)

The hard part isn't *collecting* this — it's **separating verified fact from unverified chatter**, attaching a reliability weight to each source, and assembling a timeline you can reason from. Reading 40 tabs by hand doesn't scale and isn't reproducible.

## The approach

```
  INGEST                 ANALYSE              VERIFY                  SCORE & STRUCTURE
  ──────                 ───────              ──────                  ─────────────────
  SEC EDGAR filings  ┐                    ┌ cross-check each      ┌ source-reliability
  Investor relations ┤   LLM extraction   │ claim against an      │ weight per source
  Financial press    ┼─► of entities,  ─► │ independent search ─► ┤ verified flag +
  Reddit             │   events, claims    │ engine; confidence    │ confidence (0-100)
  X / social         ┘   + sentiment       │ 0-100 + discrepancies │ event timeline,
                                           └ list                  └ value chain, catalysts
```

## The gate that makes it diligence, not a feed reader

Every extracted claim is sent to an **independent verification step** (a separate search-grounded model) that returns a structured result: a `verified` flag, a `confidence` score (0–100), a short summary, and an explicit list of `discrepancies`. An item is promoted to **verified** only when the verifier returns `verified = true` **and** `confidence > 70`. Everything else stays flagged and is held out of the "facts" timeline; conflicts between sources are captured explicitly rather than averaged away.

That single thresholded, independent check is the difference between a diligence tool and a news aggregator.

## What it produces

- **Verified event timeline** — chronological, filing-grounded, with unverified items quarantined
- **Source-reliability scoring** — each source carries a weight, so a 10-K and a Reddit post are never treated as equal
- **Value-chain view** — partners, customers, and supply-chain relationships mapped from the coverage
- **Catalyst tracker** — upcoming and recent events that could move the thesis

## How it should be validated (the honest test)

Because this is tooling, the right test is not a P&L but the verifier's accuracy — two measurable checks:

1. **Precision / recall of the gate** against a hand-labelled set of later-confirmed vs later-falsified claims: does `confidence > 70` actually separate true from false, and at what cost in missed true items?
2. **Lead-time**: do items the gate marks "verified" *precede* the eventual filing or price confirmation, or merely lag it?

Until those are run on a labelled sample, this is a validated *design*, not a validated *signal* — and that distinction is the point of publishing it honestly.

## Why single-name, not a market scanner

Diligence depth beats breadth. Pointing the whole stack at **one** company (here Tempus AI — where the genomics/data narrative and the reported financials need careful reconciliation) lets the verification layer be tuned to that company's people, partners, and claims, instead of producing shallow coverage of hundreds of tickers.

## Honest scope

Personal research tooling. **Not investment advice** — the output is a verified information layer to support judgement, not a recommendation. Verification quality is bounded by the underlying search model; `confidence > 70` reduces false positives but does not eliminate them, so discrepancies are surfaced rather than hidden.
