# Spec de artículo (formato definitivo)

**Concepto**: cada writeup es el ARTÍCULO de la charla — como si la charla se
hubiera publicado como artículo técnico de revista. Un lector que NO vio el
video lo lee como pieza standalone y se lleva el contenido completo.

## Voz (CRÍTICO)

- El artículo es sobre el TEMA, no sobre el evento. Estilo Wired/Krebs/Phrack:
  divulgativo-técnico denso, sin relleno.
- PROHIBIDO cualquier metalenguaje de video/charla: "en esta charla",
  "el ponente", "el orador dice", "la presentación comienza", "el autor
  menciona", "durante el talk", "el video muestra".
- PROHIBIDO narrar la estructura del material ("primero habla de X, luego de Y").
- La estructura del artículo es la del ARTÍCULO, no la del video.

## Estructura del archivo

1. `# <título editorial>` — sobre el tema, no el título original de la charla.
2. Línea de metadatos (trazabilidad, única mención del material fuente):
   `- **Video:** <id> · **Conferencia:** <source> · **Título original:** <title>`
3. `## Resumen` — 2-3 párrafos: el problema, por qué importa, qué aporta.
4. `## <título editorial>` × 2-6 — secciones con subtítulos propios del
   artículo, que sigan la lógica del tema (no el orden del video).
5. Opcional: cierre con ideas clave, consejos prácticos o implicaciones.

## Diagramas (Mermaid)

- Formato: bloques fenced ` ```mermaid ` dentro del md. PROHIBIDO imágenes
  (png/svg) y ASCII-art (salvo sketch de <5 líneas).
- Incluir diagrama SOLO cuando la estructura importa: cadenas de 3+ pasos
  encadenados, flujos de protocolo, arquitecturas con relaciones no lineales o
  trust boundaries. Máximo 1-2 por artículo.
- Un pipeline lineal va como lista numerada, NO como diagrama.
- Tipos permitidos: `flowchart`, `sequenceDiagram`, `graph`. Chicos, leibles
  a la primera.

## Nombre de archivo (CRÍTICO)

- El archivo NO se llama `<id>.md` sino `<slug-del-título>.md`, derivado del
  TÍTULO del artículo.
- Slug: minúsculas ASCII, solo letras/números/guiones, 3-6 palabras
  descriptivas del CONTENIDO, corto. Ej: "Cazando credenciales en memoria con
  Volatility 3" → `cazando-credenciales-volatility-3.md`.
- El id SIEMPRE queda en la línea de metadatos interna; esa es la trazabilidad.
- Si el archivo ya existe con otro nombre, renombrarlo; no dejar duplicados.

## Fidelidad y casos límite

- TODO el contenido sale del transcript. NO inventar datos, cifras, nombres ni
  herramientas que no aparezcan.
- Si el transcript tiene < 50 chars (prácticamente solo música / sin habla):
  artículo breve que lo indica, sin desarrollarlo.
- Idioma por defecto del artículo: el definido en el dispatch (el corpus puede
  mezclar idiomas; los términos técnicos se dejan en inglés).
