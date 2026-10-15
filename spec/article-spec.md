# Article spec (definitive format)

**Concept**: every writeup is the ARTICLE of the talk — as if the talk had
been published as a technical magazine article. A reader who did NOT watch the
video reads it as a standalone piece and gets the full content.

## Voice (CRITICAL)

- The article is about the TOPIC, not about the event. Wired/Krebs/Phrack
  style: dense technical-popular writing, no filler.
- FORBIDDEN: any video/talk meta-language — "in this talk", "the speaker",
  "the presenter says", "the presentation begins", "the author mentions",
  "during the talk", "the video shows". When writing in Spanish, the same rule
  applies to its Spanish equivalents ("el ponente", "en esta charla", etc. —
  full list in `scripts/verify.py --banned`).
- FORBIDDEN: narrating the structure of the material ("first he talks about X,
  then about Y").
- The article's structure is the ARTICLE's structure, not the video's.

## Language (CRITICAL)

- Default article language: **English**.
- The orchestrator MUST ask the user which language the writeups should use
  before dispatching the first round, and record the choice in the dispatch
  prompt (`{{LANGUAGE}}`). One language per corpus/run — never mixed within a
  corpus.
- Technical terms stay in English regardless of the article language.
- The writer uses exactly the language stated in the dispatch prompt. Any
  accidental foreign-language artifact (a stray word from another language) is
  a defect to fix before reporting.

## File structure

1. `# <editorial title>` — about the topic, not the talk's original title.
2. Metadata line (traceability, the ONLY mention of the source material):
   `- **Video:** <id> · **URL:** https://youtu.be/<id> · **Conference:** <source> · **Original title:** <title>`
   (include the URL whenever the id is a resolvable video link, e.g. YouTube;
   omit it for non-video sources). The id must stay the first token after
   `**Video:**` — verification parses it from there.
3. `## Summary` — 2-3 paragraphs: the problem, why it matters, what it adds.
4. `## <editorial title>` × 2-6 — sections with the article's own headings,
   following the topic's logic (not the video's order).
5. Optional: close with key takeaways, practical advice, or implications.
   (Section headings follow the article's language; e.g. `Resumen` in Spanish.)

## Diagrams (Mermaid)

- Format: fenced ` ```mermaid ` blocks inside the md. Images (png/svg) and
  ASCII-art FORBIDDEN (except a <5-line sketch).
- Include a diagram ONLY when structure matters: chains of 3+ linked steps,
  protocol flows, architectures with non-linear relations or trust boundaries.
  Maximum 1-2 per article.
- A linear pipeline is a numbered list, NOT a diagram.
- Allowed types: `flowchart`, `sequenceDiagram`, `graph`. Small, readable at
  first glance.

## Filename (CRITICAL)

- The file is NOT named `<id>.md` but `<title-slug>.md`, derived from the
  ARTICLE's title.
- Slug: lowercase ASCII, letters/numbers/hyphens only, 3-6 descriptive words
  of the CONTENT, short. Example: "Hunting in-memory credentials with
  Volatility 3" → `hunting-credentials-volatility-3.md`.
- The id ALWAYS stays in the internal metadata line; that is the traceability.
- If a file already exists under another name for the same id, rename it; do
  not leave duplicates.

## Fidelity and edge cases

- ALL content comes from the transcript. DO NOT invent data, figures, names,
  or tools that do not appear in it.
- If the transcript has < 50 chars (essentially music / no speech): a brief
  article stating that, without developing it.
- One article per batch item; no batch item may end up without an article.
