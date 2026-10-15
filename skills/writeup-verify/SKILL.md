---
name: writeup-verify
description: Use when verifying a round of generated articles before recording progress. Coverage, naming, voice and structure checks.
---

# Writeup Verify — round verification

Run AFTER a round's subagents report, BEFORE recording progress. The disk is
the truth, not the report.

## Automated (scripts/verify.py)

```bash
python scripts/verify.py --root <corpus> --batches _batches.json \
    --art-dir articles --id-key id   # distill corpus: --art-dir writeups --id-key vid
```

`--lang en|es` picks the built-in banned-phrase list (default `en`, matching
moonshine's English default; use `es` for a Spanish-language corpus). Pass
`--banned` to override with a custom list.

It checks and reports:

1. **Coverage**: every batch id appears in the metadata of exactly one
   article. Missing → requeue. Orphans (articles whose id is not in the
   corpus) → investigate (usually zombie outputs).
2. **Duplicates**: same id in two files → delete the duplicate, keep the one
   with correct metadata (this happened with a repeated vid).
3. **Naming**: files named `<id>.md` → violation (must be a title slug).
4. **Voice**: matches of the `--banned` list (per line, excluding the
   `- **Video:**` metadata line — the original title may legitimately contain
   those words).
5. **Metadata**: articles without the id in their metadata line → no
   traceability.

## Manual (mandatory, 1-2 articles per round)

Read full articles at random and judge:

- Understood without having watched the video? (standalone)
- Any disguised narration the regex misses ("begins", "then", "wraps up",
  "over the course of the presentation")?
- Is the content faithful and substantive, or generic filler?

## Interpretation

- **Benign nominal use** ("the presentation of his tool", "the second half")
  ≠ violation. Patch only real meta-language.
- Small violation → immediate targeted patch (one line). Structural violation
  → requeue the item with a note.
- Only when ALL batch items pass → record the batch in `_progress.json` as
  done.
