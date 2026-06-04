#!/usr/bin/env python3
"""Rebuild the Computex keynote transcripts from the public videos in sessions.csv.

This dataset publishes derived data and links only — not transcripts. This script
lets you reconstruct the transcripts yourself, captions-first, from the official
videos. The two caption-less sessions (transcript_source=whisper_asr in
sessions.csv) need local ASR (e.g. openai-whisper on the downloaded audio); they
are skipped here.

Usage:
    pip install youtube-transcript-api
    python regenerate.py --out transcripts/
"""
import argparse
import csv
import sys
from pathlib import Path


def get_captions(video_id: str) -> str:
    """Fetch English captions. Raises on failure (the caller reports the reason —
    e.g. an IP block from too many requests vs. a video that has no captions)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        sys.exit("pip install youtube-transcript-api")
    # youtube-transcript-api v1.x (instance .fetch); fall back to legacy classmethod
    try:
        ft = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US", "en-GB"])
        return " ".join(s.text for s in ft)
    except AttributeError:
        segs = YouTubeTranscriptApi.get_transcript(video_id)  # type: ignore[attr-defined]
        return " ".join(s["text"] for s in segs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="transcripts")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(Path(__file__).parent / "sessions.csv")))

    ok = skipped = failed = 0
    for r in rows:
        vid, who = r["video_id"], f"{r['year']} {r['company']}"
        if r["transcript_source"] != "captions":
            print(f"  skip {vid}  {who}  (needs ASR)"); skipped += 1; continue
        try:
            txt = get_captions(vid)
        except Exception as e:
            name = type(e).__name__
            hint = (" — YouTube rate-limited this IP; wait a while or use a proxy"
                    if name in ("IpBlocked", "TooManyRequests", "RequestBlocked") else "")
            print(f"  fail {vid}  {who}  ({name}){hint}"); failed += 1; continue
        if txt and len(txt) > 200:
            (out / f"{r['year']}_{r['company']}_{vid}.txt").write_text(txt)
            print(f"  ok   {vid}  {who}  ({len(txt)} chars)"); ok += 1
        else:
            print(f"  fail {vid}  {who}  (no captions returned)"); failed += 1

    print(f"\n{ok} transcripts -> {out}/   ({skipped} need ASR, {failed} failed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
