#!/usr/bin/env python3
"""verify.py — coverage/naming/voice/metadata verification of the corpus.

- Coverage: every id in _batches.json appears in the metadata of exactly one
  article (line with the meta key, default '**Video:**').
- Naming: flags files named '<id>.md' (should be a title slug).
- Voice: flags articles matching the --banned regex (per line, excluding the
  metadata line).
- Orphans: articles whose id is in no batch (zombie outputs).
- Metadata: articles without a metadata line.
Optionally writes _progress.json with the fully covered batches.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Forbidden talk/video meta-language, one list per writeup language.
BANNED = {
    "en": r"the speaker|the presenter|in this talk|during this talk"
          r"|during the talk|this talk|the talk|the presentation"
          r"|the video shows|the lecture",
    "es": r"el ponente|la ponente|en esta charla|el orador"
          r"|del orador|durante la charla|el speaker"
          r"|del speaker|esta charla|de la charla"
          r"|de la presentación|el video muestra|del talk"
          r"|el talk",
}


def article_texts(root: Path, art_dir: str = "articles"):
    for src in sorted(p for p in root.iterdir() if p.is_dir()):
        adir = src / art_dir
        if not adir.is_dir():
            continue
        for md in sorted(adir.glob("*.md")):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                print(f"warn: could not read {md}: {exc}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--batches", default="_batches.json")
    ap.add_argument("--progress", default="_progress.json",
                    help="if set, write done/failed here")
    ap.add_argument("--no-progress", action="store_true")
    ap.add_argument("--meta-key", default=r"\*\*Video:\*\*",
                    help="metadata key carrying the id")
    ap.add_argument("--art-dir", default="articles",
                    help="articles subdirectory inside each source "
                         "(writeups for the distill corpus)")
    ap.add_argument("--id-key", default="id",
                    help="batch item key carrying the id (vid in the distill corpus)")
    ap.add_argument("--lang", default="en", choices=sorted(BANNED),
                    help="writeup language, picks the built-in banned list "
                         "(en = moonshine default)")
    ap.add_argument("--banned", default=None,
                    help="custom banned regex; overrides --lang")
    ap.add_argument("--banned-flag", default="re.IGNORECASE")
    args = ap.parse_args()

    root = Path(args.root)
    batches = json.loads(Path(args.batches).read_text(encoding="utf-8"))
    banned = args.banned if args.banned is not None else BANNED[args.lang]
    banned_re = re.compile(rf"\b({banned})\b", re.I)

    # id -> file index
    id_to_file, orphans, banned_hits, no_meta = {}, [], [], []
    meta_re = re.compile(args.meta_key + r"\s*(\S+)")
    for path, text in article_texts(root, args.art_dir):
        m = meta_re.search(text)
        if not m:
            no_meta.append(path.name)
            continue
        art_id = m.group(1).strip()
        if art_id in id_to_file:
            print(f"duplicate: {art_id} in {id_to_file[art_id]} and {path.name}")
        id_to_file[art_id] = path.name
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("- **"):
                continue  # metadata bullets: the original title may contain those words
            if banned_re.search(line):
                banned_hits.append((path.name, lineno, line.strip()[:120]))
        if path.stem == art_id:
            print(f"naming: {path.name} uses the id as its name (should be a slug)")
    batch_ids = {it[args.id_key] for b in batches for it in b}
    orphans = [f for aid, f in id_to_file.items() if aid not in batch_ids]

    missing = []
    done_batches = []
    for idx, batch in enumerate(batches):
        batch_missing = [it[args.id_key] for it in batch if it[args.id_key] not in id_to_file]
        if batch_missing:
            missing.extend(batch_missing)
        else:
            done_batches.append(idx)

    total = sum(len(b) for b in batches)
    n_art = len(id_to_file) + len(no_meta)
    print(f"\narticles on disk: {n_art}")
    print(f"coverage: {total - len(missing)}/{total} ids "
          f"({100 * (total - len(missing)) / max(total, 1):.0f}%)")
    print(f"complete batches: {len(done_batches)}/{len(batches)}")
    if missing:
        print(f"missing ({len(missing)}): {missing[:20]}"
              + (" ..." if len(missing) > 20 else ""))
    if orphans:
        print(f"orphans: {orphans}")
    if no_meta:
        print(f"no metadata: {no_meta}")
    if banned_hits:
        print(f"voice hits ({len(banned_hits)}):")
        for name, lineno, ctx in banned_hits[:20]:
            print(f"  {name}:{lineno}: {ctx}")

    if not args.no_progress:
        prog = {"done": done_batches, "failed": []}
        Path(args.progress).write_text(json.dumps(prog), encoding="utf-8")
        print(f"progress written to {args.progress}")


if __name__ == "__main__":
    main()
