# Plantilla de dispatch por batch

Sustituir `{{N}}`, `{{ROOT}}` y `{{BATCHES}}`. Enviar 2 en paralelo por ronda.

---

Escribí el writeup-artículo de CADA video del batch {{N}} siguiendo la spec.

Pasos:

1. Leé PRIMERO `{{ROOT}}/spec/article-spec.md` y seguíla al pie de la letra
   (formato artículo standalone, NO narración de charla; nombre de archivo =
   slug del título, 3-6 palabras).
2. Leé `{{BATCHES}}`; tomá el batch índice {{N}} (array de items
   `{source, id, title, chars}`).
3. Para cada item, leé el transcript
   `{{ROOT}}/<source>/transcripts/<id>.txt` (salteá el header hasta `---`).
4. Escribí el artículo en `{{ROOT}}/<source>/articles/<slug-del-título>.md`
   con la estructura de la spec.
5. Verificá que cada archivo exista antes de reportarlo.

Al final reportá JSON:
`{"batch": {{N}}, "escritos": <M>, "faltantes": [], "archivos": [rutas]}`
