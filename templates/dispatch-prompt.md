# Per-batch dispatch template

Substitute `{{N}}`, `{{ROOT}}`, `{{BATCHES}}` and `{{LANGUAGE}}` (the writeup
language — moonshine default is English, but the orchestrator asks the user
once per corpus). Send 2 in parallel per round.

---

Write the writeup-article for EVERY video of batch {{N}} following the spec.

Steps:

1. Read FIRST `{{ROOT}}/spec/article-spec.md` and follow it to the letter
   (standalone-article format, NO talk narration; filename = title slug,
   3-6 words).
2. Read `{{BATCHES}}`; take batch index {{N}} (array of items
   `{source, id, title, chars}`).
3. For each item, read the transcript
   `{{ROOT}}/<source>/transcripts/<id>.txt` (skip the header up to `---`).
4. Write the article to `{{ROOT}}/<source>/articles/<title-slug>.md` with the
   spec's structure.
5. **Language: {{LANGUAGE}}.** Write the ENTIRE article in that language.
   Technical terms stay in English. Zero foreign-language artifacts.
6. Verify every file exists before reporting it.

At the end report JSON:
`{"batch": {{N}}, "written": <M>, "missing": [], "files": [paths]}`
