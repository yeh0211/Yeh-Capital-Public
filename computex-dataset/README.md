# Computex Data Library (2024–2026)

An open, structured dataset of the **Computex Taipei** keynote and press program —
NVIDIA, AMD, Intel, Qualcomm, Arm, MediaTek and the Taiwan supply chain (TSMC,
Foxconn, Quanta, ASUS, Gigabyte, Delta, Wiwynn, Supermicro…). It captures **what
each company announced**, as machine-readable rows, every one linked to the
official video and anchored in a verbatim quote.

This publishes **derived data and links only** — not the source videos or full
transcripts. Run [`regenerate.py`](regenerate.py) to rebuild the transcripts
yourself from the public videos.

| Year | Sessions | Announcements | Presenters |
|---|---|---|---|
| 2024 | 12 | 142 | NVIDIA, AMD, Intel, Qualcomm, MediaTek, Arm, Supermicro, ASUS, Delta, Acer, Pegatron, Gigabyte |
| 2025 | 11 | 108 | NVIDIA, Qualcomm, MediaTek, Foxconn, Supermicro, ASUS, Gigabyte, Wiwynn, Delta, Advantech |
| 2026 | 10 | 123 | NVIDIA, Qualcomm, Intel, Arm, Marvell, NXP, Supermicro, ASUS, Gigabyte |
| **Total** | **33** | **373** | **16 companies · 55 tickers · 75 with a stated ship window** |

## Files

| File | Rows | What |
|---|---|---|
| `sessions.csv` / `.json` | 33 | One row per keynote/press session — company, speaker, date, official video link, transcript source (captions vs ASR), language, #announcements. |
| `announcements.csv` / `.json` | 373 | One row per product / roadmap / partnership announcement — company, ticker(s), product, category, headline number, **ship quarter**, availability, a one-sentence supporting quote, and the source video. |
| `session_metadata.json` | 33 | Per-session derived summary, key numbers, themes, sectors, tickers. |
| `news_index.csv` | 38 | Taiwan press coverage index — headline, date, source, link. |
| `regenerate.py` | — | Rebuild transcripts from the public videos (captions-first). |

## Schema — `announcements`

`event, year, date, company, tickers (;-separated), speaker, announcement,
category` (gpu·cpu·npu·accelerator·platform·software·networking·memory·server·
partnership·roadmap·other), `summary, key_number, metric_value, metric_unit,
ship_quarter, availability` (announced·sampling·shipping·GA·roadmap), `quote`
(verbatim, from the transcript), `confidence, video_id, video_url`.

## How it was built

Official keynote / press videos → captions (or local Whisper ASR for the two
without captions) → LLM extraction of structured announcements, **each required
to be grounded in a verbatim quote from the transcript**, then hand-cleaned
(ungrounded rows and non-numeric metrics dropped). The full method, plus an
event study that asks whether these names beat the semis tape after the keynote,
is in [`../18-computex-event-study/`](../18-computex-event-study/).

## Provenance & license

- **This dataset** (the structured rows, summaries, and index) is original
  derived work, released under **CC-BY-4.0** — attribute *“Yeh Capital / Hsin
  Cheng Yeh”*.
- **The source videos** remain the property of their owners (NVIDIA, AMD, Intel,
  Qualcomm, Arm, MediaTek, the OEMs, and TAITRA). This repository contains only
  links and short single-sentence quotes used for commentary and data
  attribution (fair use); **no full transcripts are republished**. Use
  `regenerate.py` to reconstruct transcripts from the public videos for your own
  research.

## Caveats

- `date` / `video_date` is the video's publish date (≈ the keynote date; a few
  re-uploads differ).
- Announcements are LLM-extracted then cleaned; every row carries a source video
  and a grounding quote, but treat the structuring as best-effort, not a
  hand-curated press archive.
- 2026 sessions were captured during/just after the show; later official uploads
  may add a few sessions.
- Research dataset. Not investment advice.
