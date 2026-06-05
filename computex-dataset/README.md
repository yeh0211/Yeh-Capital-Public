# Computex Data Library (2024–2026)

An open dataset of Computex Taipei built in two complementary layers:

1. **Complete coverage** — the full official record of the show, catalogued
   directly from primary sources: **871 official Computex videos** (2024–2026,
   every series — keynotes, forums, product showcases, booth tours, InnoVEX
   startups, award winners) and the **complete official exhibitor directory
   (1,444 companies)** with hall, zone, booth, brand and products. This is the
   "who was actually there, on the record" layer — authoritative because it is
   the official catalogue itself, not an extraction.
2. **Verified depth** — for the marquee keynote/press tier, a hand-checked layer:
   **44 cited sessions** (who presented, in what form) and **126 verified
   announcements**, each cross-checked against the official program and the live
   tech press with a **source URL on each row**.

Most of what you'll want — the full company universe beyond the famous names —
is in the coverage layer. The verified layer is the deep, cited detail on the
headline players. This repo publishes derived data and links only — not the
source videos or full transcripts; [`regenerate.py`](regenerate.py) rebuilds
transcripts from the public videos.

## Why this version is trustworthy

The first cut of this dataset was machine-extracted from keynote videos and was
**not** independently checked. A 22-agent web verification (official program +
tech press + the videos, 2+ sources per claim) then audited every record. It
found that ~60% was clean and ~40% carried at least one defect — a 2021 video
mislabeled as 2024, a booth-only company recorded as a keynote, hallucinated
products, and routine omission of the actual headline. **All of it is corrected
here**, and the complete, cited audit — 18 documented errors, 8 coverage gaps —
is in [`verification_report.json`](verification_report.json).

## Files

**Coverage layer — the complete official record (authoritative by source):**

| File | Rows | What |
|---|---|---|
| `video_catalog.csv` / `.json` | 871 | Every official Computex 2024–2026 video, from the two official channels, tagged by year, series (keynote · forum · Technology Unboxing · COMPUTOUR booth tour · Featured Product · Best Choice Award · InnoVEX · Tech-in-60s · AI Spotlight · creator), title, best-effort brand tags, and a watch URL. By year: 2024 = 304, 2025 = 389, 2026 = 178. |
| `exhibitors_2026.csv` / `.json` | 1,444 | The **complete official 2026 exhibitor directory** — every exhibiting company with venue (TaiNEX 1/2, TWTC), show zone, booth number, brand names and product categories. 413 are InnoVEX startups. This is the full participant universe, most of it the mid/small supply chain that never makes a headline. |
| `company_index.csv` | 332 | Distinct companies surfaced from the video catalogue, with video counts and a `major_brand` flag (59 majors: NVIDIA, Intel, AMD, Qualcomm, Arm, MediaTek, ASUS, Acer, MSI, Gigabyte, Delta, Supermicro, Phison, Foxconn…). |

> The coverage layer and the exhibitor directory are complementary: the marquee
> silicon vendors (AMD, Qualcomm, Arm, Intel, TSMC) *keynote* but take no floor
> booth, so they appear in the video catalogue, not the directory; the 1,444 floor
> exhibitors mostly *exhibit* without a keynote. Their union is the real,
> complete participant set.

**Verified-depth layer — the hand-checked marquee detail:**

| File | Rows | What |
|---|---|---|
| `sessions.csv` / `.json` | 44 | The **corrected attendance reality** — every company × year, the *real* form (official keynote / company press event / forum talk / booth-only / absent), a confidence, a source citation, and a `video_status` flag noting where a collected recording is mislabeled. |
| `announcements_verified.csv` / `.json` | 126 | The **verified tier** — the headline announcements confirmed by the live press, each with a source. Trust these. |
| `announcements_extracted.csv` / `.json` | 366 | The **extracted tier** — the detailed transcript-derived announcements, kept for depth but marked `verified=no`. Flagged errors removed, garbled names fixed, the Arm record relabeled to its true year (2021). Treat as best-effort, not gospel. |
| `verification_report.json` | — | The full cited audit: corrected attendance matrix, every dataset error + correction + source, the coverage gaps, and the verified highlights. |
| `news_index.csv` | 38 | Taiwan press coverage index (headline, date, source, link). |
| `regenerate.py` | — | Rebuild transcripts from the public videos (captions-first). |

## What the verification corrected (highlights)

- **Arm "2024"** was the **2021** keynote (2021 video, 2021-era products) — relabeled.
- **Acer "2024"** was a **post-show July forum panel**, not a Computex session — relabeled.
- **Delta 2025** did **not** present (booth-only); the "video" was a pre-show marketing upload.
- **Advantech 2025 / Wiwynn 2025 / Pegatron 2024** were **forum talks**, not press conferences, with several misattributed (wrong-date / wrong-company) announcements removed.
- **NXP 2026** carried a **hallucinated** "Boston Dynamics" partnership — dropped.
- Garbled product names fixed (Gigabyte "AI TOP Edge"→ATOM, Qualcomm "Claude Desktop"→Claude Code, NVIDIA "Spectrum-X800"→Spectrum-X, MediaTek 9400 = preview not launch).
- **Backfilled** sessions the first cut missed: AMD's 2025 press conference, NXP's 2024 + 2025 keynotes, Cisco's 2026 debut keynote (see the attendance matrix / report).
- Real-form labels: most OEM "keynotes" were company **launch/press events**, not official TAITRA keynote slots; Supermicro 2025/2026 were Supermicro-hosted "Innovate" events.

## How it was built

- **Coverage layer:** the official Computex YouTube channels enumerated across all
  2024–2026 per-year, per-series playlists (so year and series are exact, not
  inferred), de-duplicated to 871 distinct videos; the official exhibitor
  directory paged A–Z and parsed to the full 1,444-company list. Both are primary
  catalogues — authoritative by source, no extraction or model in the loop.
- **Verified-depth layer:** marquee keynote / press videos → captions (or local
  ASR) → LLM extraction → **independent web verification** against the official
  program + tech press → hand-correction from the cited report.

The event study built on this data is in
[`../18-computex-event-study/`](../18-computex-event-study/); the synthesis is in
[`../computex-dossier/`](../computex-dossier/).

## Provenance & license

- The dataset (sessions, verified announcements, index) is original derived work
  under **CC-BY-4.0** — attribute *“Yeh Capital / Hsin Cheng Yeh”*.
- Source videos remain their owners' (NVIDIA, AMD, Intel, Qualcomm, Arm,
  MediaTek, the OEMs, TAITRA). Only links and short quotes are included; no full
  transcripts are republished. `regenerate.py` reconstructs transcripts from the
  public videos.
- The video catalogue and exhibitor directory are factual records of the public
  Computex program and the organiser's (TAITRA) official exhibitor listing,
  compiled here for research; company/brand/product strings are theirs.

## Caveats

- The **coverage layer** is authoritative on *existence* (these videos and
  exhibitors are the official record) but its derived fields are best-effort: the
  catalogue's `brands` tags are parsed from video titles (high-precision for the
  59 known majors, sparser for the long tail), and the exhibitor directory is the
  **2026** edition (the live official list; 2024/2025 floor lists are not
  retained by the organiser).
- The **verified** tier is cited and cross-checked; the **extracted** tier is
  transcript-derived and best-effort (it can still contain misframings — it is
  kept for breadth, not authority).
- `sessions.csv` reflects the true *form* of each appearance; a `video_status` of
  "mislabeled" means our collected recording is not a faithful capture of that
  session (see notes).
- Research dataset. Not investment advice.
