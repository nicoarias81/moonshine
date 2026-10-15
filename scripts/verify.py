#!/usr/bin/env python3
"""verify.py — verificación de cobertura/naming/voz/metadatos del corpus.

- Cobertura: cada id de _batches.json aparece en los metadatos de exactamente
  un artículo (línea con la clave de metadatos, default '**Video:**').
- Naming: marca archivos llamados '<id>.md' (deberían ser slug del título).
- Voz: marca artículos con coincidencias de la regex --banned.
- Huérfanos: artículos cuyo id no está en ningún batch (outputs zombie).
- Metadatos: artículos sin línea de metadatos.
Opcionalmente escribe _progress.json con los batches totalmente cubiertos.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def article_texts(root: Path, art_dir: str = "articles"):
    for src in sorted(p for p in root.iterdir() if p.is_dir()):
        adir = src / art_dir
        if not adir.is_dir():
            continue
        for md in sorted(adir.glob("*.md")):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                print(f"warn: no se pudo leer {md}: {exc}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--batches", default="_batches.json")
    ap.add_argument("--progress", default="_progress.json",
                    help="si se define, escribir done/failed aquí")
    ap.add_argument("--no-progress", action="store_true")
    ap.add_argument("--meta-key", default=r"\*\*Video:\*\*",
                    help="clave de metadatos que porta el id")
    ap.add_argument("--art-dir", default="articles",
                    help="subdirectorio de artículos dentro de cada fuente "
                         "(writeups para el corpus distill)")
    ap.add_argument("--id-key", default="id",
                    help="clave del item que porta el id (vid en el corpus distill)")
    ap.add_argument("--banned",
                    default=r"el ponente|la ponente|en esta charla|el orador"
                            r"|del orador|durante la charla|el speaker"
                            r"|del speaker|esta charla|de la charla"
                            r"|de la presentación|el video muestra|del talk"
                            r"|el talk")
    ap.add_argument("--banned-flag", default="re.IGNORECASE")
    args = ap.parse_args()

    root = Path(args.root)
    batches = json.loads(Path(args.batches).read_text(encoding="utf-8"))
    banned_re = re.compile(rf"\b({args.banned})\b", re.I)

    # índice id -> archivo
    id_to_file, orphans, banned_hits, no_meta = {}, [], [], []
    meta_re = re.compile(args.meta_key + r"\s*(\S+)")
    for path, text in article_texts(root, args.art_dir):
        m = meta_re.search(text)
        if not m:
            no_meta.append(path.name)
            continue
        art_id = m.group(1).strip()
        if art_id in id_to_file:
            print(f"duplicado: {art_id} en {id_to_file[art_id]} y {path.name}")
        id_to_file[art_id] = path.name
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("- **Video:**"):
                continue  # metadatos: el título original puede contener esas palabras
            if banned_re.search(line):
                banned_hits.append((path.name, lineno, line.strip()[:120]))
        if path.stem == art_id:
            print(f"naming: {path.name} usa el id como nombre (debería ser slug)")
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
    print(f"\nartículos en disco: {n_art}")
    print(f"cobertura: {total - len(missing)}/{total} ids "
          f"({100 * (total - len(missing)) / max(total, 1):.0f}%)")
    print(f"batches completos: {len(done_batches)}/{len(batches)}")
    if missing:
        print(f"faltantes ({len(missing)}): {missing[:20]}"
              + (" ..." if len(missing) > 20 else ""))
    if orphans:
        print(f"huérfanos: {orphans}")
    if no_meta:
        print(f"sin metadatos: {no_meta}")
    if banned_hits:
        print(f"hits de voz ({len(banned_hits)}):")
        for name, lineno, ctx in banned_hits[:20]:
            print(f"  {name}:{lineno}: {ctx}")

    if not args.no_progress:
        prog = {"done": done_batches, "failed": []}
        Path(args.progress).write_text(json.dumps(prog), encoding="utf-8")
        print(f"progreso escrito en {args.progress}")


if __name__ == "__main__":
    main()
