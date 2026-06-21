#!/usr/bin/env python3
"""build_index.py — generate + validate the research-notes index table.

The root README "Notes" table is GENERATED from per-study metadata, never
hand-edited. Each study owns exactly one fragment — its own
``<NN-slug>/meta.json`` — and this is the single producer of the table. Two
studies therefore never touch the same line of the README, so the
stale-index / duplicate-number / row-without-folder / merge-conflict class of
bug goes away: study PRs add only their own folder, and the index is
regenerated as its own commit.

Run it from anywhere; the repo root is derived from this file's location
(``<root>/tools/build_index.py``), so it works in any worktree without editing
a hardcoded path.

Inputs (all optional):
  --repo-root DIR   repo to read studies from (default: the repo this file lives in)
  --extra FILE      non-folder rows, e.g. the linked paper #06
                    (default: <repo-root>/index_extra.json)

Modes:
  (default)         print the generated table block; validation issues -> stderr,
                    exit 1 if any
  --check README    diff the generated table against README's existing table block
                    (exit 0 only if it round-trips exactly and validation passes)
  --apply README    splice the generated table into README in place
                    (refuses if validation fails)
  --full TEMPLATE   fill TEMPLATE's {{NOTES_TABLE}} marker and print the full README
  --next-number     print the next free study number (max existing + 1) and exit;
                    new-task.sh calls this to claim a number at creation time so
                    two parallel sessions can't both grab the same one
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = "| # | Study | Question | Finding |\n|---|---|---|---|"


def _cell(value) -> str:
    """Make a value safe to drop into one Markdown table cell: no embedded
    newline can split the row, no raw pipe can open a phantom column."""
    text = str(value).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return text.replace("|", r"\|")


def is_study_dir(path: Path) -> bool:
    return path.is_dir() and path.name[:2].isdigit() and "-" in path.name


def load_metas(repo_root: Path):
    return [repo_root / d.name / "meta.json"
            for d in sorted(repo_root.iterdir())
            if is_study_dir(d) and (d / "meta.json").is_file()]


def collect_numbers(repo_root: Path, extra_file: Path) -> set[int]:
    """Every study number currently claimed — folder-backed metas + extra rows."""
    numbers: set[int] = set()
    for mf in load_metas(repo_root):
        numbers.add(int(json.loads(mf.read_text())["number"]))
    if extra_file and extra_file.exists():
        for e in json.loads(extra_file.read_text()):
            numbers.add(int(e["number"]))
    return numbers


def build(repo_root: Path, extra_file: Path):
    rows, issues, seen = [], [], {}
    foldered = set()
    for mf in load_metas(repo_root):
        m = json.loads(mf.read_text())
        num = int(m["number"])
        folder = mf.parent.name           # the URL is always the real folder, never meta's slug
        foldered.add(folder)
        seen.setdefault(num, []).append(folder)
        if m.get("slug") != folder:
            issues.append(f"meta slug '{m.get('slug')}' != folder '{folder}'")
        rows.append((num, f"[{_cell(m['title'])}]({folder}/)",
                     _cell(m["question"]), _cell(m["finding"])))

    if extra_file and extra_file.exists():
        for e in json.loads(extra_file.read_text()):
            num = int(e["number"])
            seen.setdefault(num, []).append(e.get("study_cell", "(extra)"))
            rows.append((num, _cell(e["study_cell"]),
                         _cell(e["question"]), _cell(e["finding"])))

    # every folder-backed study must have a meta row
    for d in sorted(repo_root.iterdir()):
        if is_study_dir(d) and d.name not in foldered:
            issues.append(f"folder '{d.name}' has no meta row")

    for num, who in sorted(seen.items()):
        if len(who) > 1:
            issues.append(f"duplicate study number {num:02d}: {who}")

    rows.sort(key=lambda r: r[0])
    return rows, issues


def render_table(rows) -> str:
    return "\n".join([HEADER] + [f"| {n:02d} | {s} | {q} | {f} |" for n, s, q, f in rows])


def _table_bounds(readme_text: str):
    lines = readme_text.splitlines()
    hdr = next(i for i, l in enumerate(lines) if l.strip().startswith("| # | Study"))
    end = hdr
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    return lines, hdr, end


def table_block(readme_text: str) -> str:
    lines, hdr, end = _table_bounds(readme_text)
    return "\n".join(lines[hdr:end])


def splice_table(readme_text: str, new_table: str) -> str:
    """Replace the existing Notes-table block, leaving all surrounding prose
    untouched so the index regen never disturbs narrative edits."""
    lines, hdr, end = _table_bounds(readme_text)
    out = lines[:hdr] + new_table.splitlines() + lines[end:]
    return "\n".join(out) + ("\n" if readme_text.endswith("\n") else "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(ROOT))
    ap.add_argument("--extra", default=None,
                    help="non-folder rows JSON (default: <repo-root>/index_extra.json)")
    ap.add_argument("--full", metavar="TEMPLATE")
    ap.add_argument("--check", metavar="README")
    ap.add_argument("--apply", metavar="README",
                    help="splice the generated table into README in place")
    ap.add_argument("--next-number", action="store_true",
                    help="print the next free study number and exit")
    args = ap.parse_args()

    repo_root = Path(args.repo_root)
    extra_file = Path(args.extra) if args.extra else (repo_root / "index_extra.json")

    if args.next_number:
        nums = collect_numbers(repo_root, extra_file)
        print((max(nums) + 1) if nums else 0)
        sys.exit(0)

    rows, issues = build(repo_root, extra_file)
    table = render_table(rows)

    if issues:
        print("VALIDATION ISSUES:", file=sys.stderr)
        for i in issues:
            print(f"  - {i}", file=sys.stderr)
    else:
        print(f"validation OK ({len(rows)} rows, numbers unique, folders matched)",
              file=sys.stderr)

    if args.check:
        current = table_block(Path(args.check).read_text())
        if current.strip() == table.strip() and not issues:
            print(f"TABLE MATCHES reference ({len(rows)} rows) — round-trip exact.",
                  file=sys.stderr)
            sys.exit(0)
        if current.strip() != table.strip():
            print("TABLE DIFFERS from reference:", file=sys.stderr)
            cur, gen = current.splitlines(), table.splitlines()
            for i in range(max(len(cur), len(gen))):
                c = cur[i] if i < len(cur) else "<none>"
                g = gen[i] if i < len(gen) else "<none>"
                if c != g:
                    print(f"  row {i}:\n    current: {c}\n    generated: {g}",
                          file=sys.stderr)
        sys.exit(1)

    if args.apply:
        if issues:
            print("REFUSING to apply — fix validation issues first.", file=sys.stderr)
            sys.exit(1)
        tgt = Path(args.apply)
        tgt.write_text(splice_table(tgt.read_text(), table))
        print(f"applied index to {tgt} ({len(rows)} rows)", file=sys.stderr)
        sys.exit(0)

    if args.full:
        sys.stdout.write(Path(args.full).read_text().replace("{{NOTES_TABLE}}", table))
    else:
        print(table)
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
