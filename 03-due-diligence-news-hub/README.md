# A due-diligence news hub: verified event tracking for a fast-moving name

**Case study — turning fragmented, mixed-reliability sources into a verified, source-scored event timeline for a single company (Tempus AI, $TEM).**

*Hsin Cheng Yeh · independent research tooling · 2026*

---

## The problem

Doing diligence on a fast-moving AI-healthcare name means reconciling sources that disagree and vary wildly in reliability:

- **Primary** — SEC filings (8-K/10-Q), investor-relations releases
- **Secondary** — financial press
- **Noisy/early** — Reddit, X/Twitter, and other social chatter, where a partnership "rumour" can move the stock days before it's confirmed (or turn out false)

The hard part isn't *collecting* this — it's **separating verified fact from unverified chatter**, attaching a reliability weight to each source, and assembling a clean event timeline you can actually reason from. Reading 40 tabs by hand doesn't scale and isn't reproducible.

## The approach

I built a single-name diligence pipeline that ingests, analyses, **independently verifies**, scores, and structures coverage of one company end-to-end.

```
  INGEST                 ANALYSE              VERIFY                  SCORE & STRUCTURE
  ──────                 ───────              ──────                  ─────────────────
  SEC EDGAR filings  ┐                    ┌ cross-check each      ┌ source-reliability
  Investor relations ┤   LLM extraction   │ claim against an      │ weight per source
  Financial press    ┼─► of entities,  ─► │ independent search ─► ┤ verified flag +
  Reddit             │   events, claims    │ engine; confidence    │ confidence (0-100)
  X / Twitter        ┘   + sentiment       │ 0-100 + discrepancies │ event timeline,
                                           └ list                  └ value chain, catalysts
```

## The bit that makes it diligence, not a feed reader

Every extracted claim is sent to an **independent verification step** (a separate search-grounded model) that returns structured output:

```json
{ "verified": true/false, "confidence": 0-100, "summary": "...", "discrepancies": ["..."] }
```

An item is only promoted to **verified** when the verifier returns `verified = true` **and** `confidence > 70`. Everything else stays flagged as unverified and is held out of the "facts" timeline. Discrepancies (where sources conflict) are captured explicitly rather than averaged away.

That single gate is the difference between a diligence tool and a news aggregator: it forces every "fact" to clear an independent, thresholded check before it's treated as one.

## What it produces

- **Verified event timeline** — chronological, filing-grounded, with unverified items quarantined
- **Source-reliability scoring** — each source carries a weight, so a 10-K and a Reddit post are never treated as equal
- **Value-chain view** — partners, customers, and supply-chain relationships mapped from the coverage
- **Catalyst tracker** — upcoming/!recent events that could move the thesis
- **Pipeline console** — run status + error surface, so I can trust the data is fresh and complete

Data model (Postgres via Supabase): `articles` (source, url, score, **verified**, verification_notes, tags), `timeline_events`, `catalysts`, `source_reliability`, `network_verification`, plus `pipeline_errors` / `pipeline_schedule` for observability. Row-level security is enabled on every table.

## Why single-name, not a market scanner

Diligence depth beats breadth. Pointing the whole stack at **one** company (here, Tempus AI — an AI-driven precision-medicine name where the genomics/data narrative and the reported financials need careful reconciliation) means the verification layer can be tuned to that company's people, partners, and claims, instead of producing shallow coverage of hundreds of tickers.

## Honest scope

- Personal research tooling, built on a Vite/React front end with a Supabase (Postgres + edge-function) backend.
- **Not investment advice.** The output is a verified information layer to support judgement, not a recommendation.
- Verification quality is bounded by the underlying search model; `confidence > 70` reduces false positives but does not eliminate them — discrepancies are surfaced, not hidden.
- The live deployment, credentials, and backend endpoints are kept private; this case study describes the design and methodology only.

---

*Part of a series of independent research notes. Method and design only — no code, keys, or infrastructure published.*
