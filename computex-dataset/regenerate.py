#!/usr/bin/env python3
"""Rebuild Computex transcripts from the public videos in this dataset.

This dataset publishes derived data and links only — not transcripts. This script
reconstructs the transcripts yourself, captions-first, from the official videos.

It pulls captions with yt-dlp (robust: YouTube rate-limits the lighter
youtube-transcript-api path quickly on bulk pulls). Captions are cleaned from VTT
to plain text. Videos with no captions are reported; the marquee caption-less ones
need local ASR (e.g. openai-whisper / whisper.cpp on the downloaded audio).

Sources:
    --source sessions   the 44 verified marquee sessions (sessions.csv)   [default]
    --source catalog    the full 871-video official catalogue (video_catalog.csv)

Usage:
    pip install yt-dlp
    python regenerate.py --source catalog --out transcripts/
"""
import argparse
import csv
import re
import subprocess
import sys
import time
from pathlib import Path


def clean_vtt(path: Path) -> str:
    lines = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = raw.strip()
        if s.startswith(("WEBVTT", "Kind:", "Language:")) or "-->" in s or not s:
            continue
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        if not s:
            continue
        if lines and (s == lines[-1] or s in lines[-1]):
            continue
        if lines and lines[-1] in s:        # rolling caption grew -> keep the longer
            lines[-1] = s
            continue
        lines.append(s)
    return "\n".join(lines)


def get_captions(video_id: str, tmp: Path) -> str:
    """Download English captions via yt-dlp; return cleaned text or ''."""
    for f in tmp.glob(f"{video_id}*"):
        f.unlink()
    try:
        subprocess.run(
            ["python3", "-m", "yt_dlp", "--write-auto-subs", "--write-subs",
             "--sub-langs", "en,en-orig", "--skip-download", "--sub-format", "vtt",
             "--socket-timeout", "30", "--no-warnings", "--no-progress",
             "-o", str(tmp / f"{video_id}.%(ext)s"),
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=150)
    except subprocess.TimeoutExpired:
        return ""
    except FileNotFoundError:
        sys.exit("pip install yt-dlp")
    best = ""
    for f in sorted(tmp.glob(f"{video_id}*.vtt")):
        txt = clean_vtt(f)
        if len(txt) > len(best):
            best = txt
        f.unlink()
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["sessions", "catalog"], default="sessions")
    ap.add_argument("--out", default="transcripts")
    ap.add_argument("--sleep", type=float, default=2.5, help="throttle between videos (s)")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)

    here = Path(__file__).parent
    src = here / ("video_catalog.csv" if args.source == "catalog" else "sessions.csv")
    rows = list(csv.DictReader(open(src)))

    ok = noc = 0
    for i, r in enumerate(rows, 1):
        vid = r["video_id"]
        label = f"{r.get('year','')} {r.get('company') or r.get('series_name') or ''}".strip()
        txt = get_captions(vid, tmp)
        if txt and len(txt) > 200:
            (out / f"{r.get('year','')}_{vid}.txt").write_text(txt, encoding="utf-8")
            print(f"  [{i}/{len(rows)}] ok   {vid}  {label}  ({len(txt)} chars)"); ok += 1
        else:
            print(f"  [{i}/{len(rows)}] ---  {vid}  {label}  (no captions — needs ASR)"); noc += 1
        time.sleep(args.sleep)

    print(f"\n{ok} transcripts -> {out}/   ({noc} caption-less, need local ASR)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
