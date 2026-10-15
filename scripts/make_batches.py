#!/usr/bin/env python3
"""make_batches.py — transcript corpus → batches JSON.

Scans <root>/<source>/transcripts/<id>.txt, parses the header
(id/title/lang/chars/---) and emits batches of items
{"source", "id", "title", "chars"}.
"""
import argparse
import json
import sys
from pathlib import Path


def parse_header(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"warn: could not read {path}: {exc}", file=sys.stderr)
        return None
    lines = text.splitlines()
    if len(lines) < 5 or lines[4].strip() != "---":
        print(f"warn: invalid header in {path}", file=sys.stderr)
        return None
    item_id, title, lang, chars = lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[3].strip()
    try:
        n = int(chars)
    except ValueError:
        print(f"warn: non-numeric char count in {path}: {chars!r}", file=sys.stderr)
        n = 0
    return {"source": path.parent.parent.name, "id": item_id,
            "title": title, "lang": lang, "chars": n}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, help="corpus root")
    ap.add_argument("--out", default="_batches.json", help="output file")
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--min-chars", type=int, default=0,
                    help="skip items with fewer chars (0 = include all)")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        sys.exit(f"corpus does not exist: {root}")

    items = []
    for source_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        tdir = source_dir / "transcripts"
        if not tdir.is_dir():
            continue
        for txt in sorted(tdir.glob("*.txt")):
            item = parse_header(txt)
            if item and item["chars"] >= args.min_chars:
                items.append(item)

    if not items:
        sys.exit("no transcripts found")

    batches = [items[i:i + args.batch_size]
               for i in range(0, len(items), args.batch_size)]
    out = Path(args.out)
    out.write_text(json.dumps(batches, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"{len(items)} items from {len(set(i['source'] for i in items))} sources "
          f"-> {len(batches)} batches ({args.batch_size}/batch) in {out}")


if __name__ == "__main__":
    main()
