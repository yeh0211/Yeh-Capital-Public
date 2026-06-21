# Adding or changing a study

The root `README.md` "Notes" table is **generated, never hand-edited.** Each study
owns one fragment — its own `NN-slug/meta.json` — and that is the single source of
the table row. This is what lets several studies be written in parallel without
colliding on the README: two studies never touch the same line, because no study
touches the README at all.

## To add a study

1. **Claim the next free number** so two parallel sessions can't both grab it:

   ```sh
   python3 tools/build_index.py --next-number      # prints e.g. 32
   ```

2. Create `NN-slug/` (zero-padded number, kebab-case slug) with the study and a
   `meta.json`:

   ```json
   {
     "number": 32,
     "slug": "32-your-slug",
     "title": "Short title",
     "question": "The question the study answers.",
     "finding": "The answer, stated as a conclusion.",
     "date": "YYYY-MM-DD",
     "author": "Hsin Cheng Yeh"
   }
   ```

   `slug` **must** equal the folder name; the build refuses otherwise. The table
   link is built from the folder name, so the URL can never break.

3. **Do not edit the README table by hand.** Regenerate it as its own commit:

   ```sh
   python3 tools/build_index.py --apply README.md   # refuses if validation fails
   git add README.md NN-slug/ && git commit -m "study NN: <title>"
   ```

## Validation

`build_index.py` refuses to write a broken index. It fails on a **duplicate study
number** (the guard that catches two sessions both publishing the same number), a
folder with no `meta.json`, a `meta.json` whose `slug` doesn't match its folder, and
sanitizes any stray `|` or newline in a cell so one bad field can't break the table.

```sh
python3 tools/build_index.py --check README.md   # CI-style: exit 0 only if exact + valid
```

Linked papers and other non-folder rows live in `index_extra.json`.
