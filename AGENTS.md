# AGENTS.md — moonshine

Guidance for coding agents working in this repository.

## What this repo is

Moonshine is a transcript→article distillation pipeline: conference/course
transcripts go in, standalone writeup articles come out, authored by subagents
in batches and verified by a linter.

```
spec/article-spec.md      # authoritative article spec (structure, style, metadata)
skills/writeup-author/    # SKILL.md for the agent that writes writeups
skills/writeup-verify/    # SKILL.md for the agent that verifies writeups
templates/dispatch-prompt.md   # prompt template used to dispatch a batch ({{LANGUAGE}})
scripts/make_batches.py   # builds batch JSON from a distill root
scripts/verify.py         # linter: metadata, banned phrases, voice, coverage
```

## Non-negotiables

1. **`spec/article-spec.md` is the single source of truth.** Any change to
   article structure, metadata, or style happens there first; keep the skills
   and the dispatch template in sync in the same commit.
2. **Default language is English.** Language is a pipeline parameter, not a
   hardcoded style. The orchestrator asks the user per corpus and injects it
   via `{{LANGUAGE}}` in the dispatch prompt; `verify.py --lang en|es` selects
   the matching banned-phrase list. Never add language-specific rules outside
   the built-in `en`/`es` lists in `verify.py`.
3. **No talk/video metalanguage in article bodies.** No "the speaker", "this
   talk", "the presenter", "en esta charla", etc. The ONLY allowed mention of
   the source is the metadata line.
4. **Metadata line format** (first token after `**Video:**` must stay the vid —
   `verify.py` parses it from there):

   ```
   - **Video:** <id> · **URL:** https://youtu.be/<id> · **Conference:** <source> · **Original title:** <title>
   ```

   Include the URL whenever the id is a resolvable video link; omit it only for
   non-video sources.

## Verification before any push

```bash
python scripts/verify.py \
  --root <distill-root> \
  --batches <distill-root>/_writeup_batches.json \
  --art-dir writeups --id-key vid --lang <en|es> --no-progress
```

Coverage numbers in commit messages or PRs must come from this command, not
from memory.

## Conventions

- Commits in English, imperative mood.
- Python scripts: stdlib only, no third-party deps.
- Do not commit corpus data (transcripts, writeups) here — this repo is the
  pipeline, the corpus lives in its own distill tree.
