---
name: writeup-verify
description: Use when verifying a round of generated articles before recording progress. Coverage, naming, voice and structure checks.
---

# Writeup Verify — verificación de ronda

Correr DESPUÉS de que los subagentes de una ronda reportan, ANTES de registrar
progreso. La verdad es el disco, no el reporte.

## Automático (scripts/verify.py)

```bash
python scripts/verify.py --root <corpus> --batches _batches.json \
    --art-dir articles --id-key id   # corpus distill: --art-dir writeups --id-key vid
```

Chequea y reporta:

1. **Cobertura**: cada id de batch aparece en los metadatos de exactamente un
   artículo. Faltantes → reencolar. Huérfanos (artículos con id fuera del
   corpus) → investigar (suelen ser outputs zombie).
2. **Duplicados**: mismo id en dos archivos → borrar el duplicado y conservar
   el que tenga la metadata correcta (pasó con un vid repetido).
3. **Naming**: archivos llamados `<id>.md` → violación (deben ser slug).
4. **Voz**: coincidencias de la lista `--banned` (por línea, excluida la línea
   de metadatos `- **Video:**` — el título original puede contenerlas).
5. **Metadatos**: artículos sin el id en la línea de metadatos → sin trazabilidad.

## Manual (obligatorio, 1-2 artículos por ronda)

Leer artículos completos al azar y juzgar:

- ¿Se entiende sin haber visto el video? (standalone)
- ¿Hay narración disfrazada que la regex no caza? ("comienza", "sigue",
  "cierra", "a lo largo de la exposición")?
- ¿El contenido es fiel y sustancioso, o relleno genérico?

## Interpretación

- **Uso nominal benigno** ("la presentación de su herramienta", "la segunda
  mitad") ≠ violación. Solo parchear metalenguaje real.
- Violación chica → patch directo en el acto (una línea). Violación estructural
  → reencolar el item con nota.
- Solo cuando TODOS los items del batch pasan → registrar el batch en
  `_progress.json` como done.
