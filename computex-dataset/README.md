# Computex Data Library (2024–2026)

An open, **independently verified** dataset of the Computex Taipei keynote and
press program — who actually presented, in what form, and what they actually
announced. Every session and headline is cross-checked against the official
Computex program and the live tech press, with a **source URL on each row**.

This publishes derived data and links only — not the source videos or full
transcripts. Run [`regenerate.py`](regenerate.py) to rebuild transcripts from
the public videos.

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

Official keynote / press videos → captions (or local ASR) → LLM extraction →
**independent web verification** against the official program + tech press →
hand-correction from the cited report. The event study built on this data is in
[`../18-computex-event-study/`](../18-computex-event-study/).

## Provenance & license

- The dataset (sessions, verified announcements, index) is original derived work
  under **CC-BY-4.0** — attribute *“Yeh Capital / Hsin Cheng Yeh”*.
- Source videos remain their owners' (NVIDIA, AMD, Intel, Qualcomm, Arm,
  MediaTek, the OEMs, TAITRA). Only links and short quotes are included; no full
  transcripts are republished. `regenerate.py` reconstructs transcripts from the
  public videos.

## Caveats

- The **verified** tier is cited and cross-checked; the **extracted** tier is
  transcript-derived and best-effort (it can still contain misframings — it is
  kept for breadth, not authority).
- `sessions.csv` reflects the true *form* of each appearance; a `video_status` of
  "mislabeled" means our collected recording is not a faithful capture of that
  session (see notes).
- Research dataset. Not investment advice.
