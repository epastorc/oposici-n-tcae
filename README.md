# Oposición TCAE

Web estática y responsive para practicar tests de oposición de Técnico en Cuidados
Auxiliares de Enfermería (TCAE).

El repositorio incluye un banco de `3.100` preguntas extraídas de `38` PDF y un
importador reproducible para regenerarlo cuando se añadan nuevos exámenes.

## Funcionalidades

- Tests aleatorios de `100`, `50` o `25` preguntas.
- Modo oposición de `85` preguntas: `80` puntuables y `5` de reserva, con penalización
  de un acierto por cada tres fallos.
- Navegación entre preguntas conservando las respuestas.
- Marcado de preguntas para repasar.
- Resumen final de preguntas respondidas y pendientes.
- Diseño adaptado a escritorio, tablet y móvil.
- Extracción automática de preguntas desde PDF.
- Banco independiente para preguntas nuevas según temario.

## Ejecutar la web

```bash
./scripts/serve.sh
```

Después visita [http://localhost:8000](http://localhost:8000).

## Web pública

La rama `develop` se publica automáticamente mediante GitHub Pages:

[https://epastorc.github.io/oposici-n-tcae/](https://epastorc.github.io/oposici-n-tcae/)

Cada despliegue genera `web/version.json` con el commit publicado y la fecha UTC.
La versión se muestra en el pie de página para comprobar qué subida está activa.

## Recursos visuales

El GIF animado de Pikachu utilizado durante la carga procede del repositorio público
[PokeAPI/sprites](https://github.com/PokeAPI/sprites), en la colección `showdown`
diseñada por la comunidad de Smogon.

## Regenerar el banco de preguntas

El script crea automáticamente un entorno virtual local e instala `pypdf` la
primera vez que se ejecuta.

```bash
./scripts/import_pdfs.sh /Users/enrique.pastor/Downloads/TCAE_EXAMEN*.pdf
```

El resultado se guarda en `web/data/questions.json`. Si un bloque no tiene
exactamente cuatro opciones, se excluye y queda registrado en el campo `warnings`.

## Estructura

- `scripts/extract_questions.py`: parser de preguntas.
- `scripts/import_pdfs.sh`: importador reproducible.
- `scripts/serve.sh`: servidor web local.
- `web/data/questions.json`: banco de preguntas.
- `web/data/thematic-questions.json`: banco independiente de preguntas nuevas según temario.
- `web/`: aplicación estática.

Las preguntas nuevas según temario se generan exclusivamente para TCAE a partir de
soluciones verificadas del banco principal:

```bash
python3 scripts/generate_tcae_thematic_questions.py
```

El resultado se guarda en `web/data/thematic-questions.json`. Cada entrada usa el
mismo formato que el banco principal y declara `topic` para indicar el bloque:

```json
{
  "id": "temario-anatomia-1",
  "topic": "Anatomía",
  "number": 1,
  "prompt": "Texto de la pregunta",
  "options": [
    { "key": "a", "text": "Primera opción" },
    { "key": "b", "text": "Segunda opción" },
    { "key": "c", "text": "Tercera opción" },
    { "key": "d", "text": "Cuarta opción" }
  ],
  "correctAnswer": "a"
}
```

## Respuestas correctas

La mayoría de los PDF originales no contienen plantillas de soluciones. El formato
JSON incluye el campo opcional `correctAnswer`. Las soluciones se investigan en
fuentes institucionales, se incorporan desde plantillas de corrección publicadas
por el autor o se contrastan con su material docente público, indicando expresamente
la procedencia. Todas se auditan por separado en `data/answer-review.json`.

```bash
./.venv/bin/python scripts/build_answer_review.py
./.venv/bin/python scripts/import_answer_seeds.py
./.venv/bin/python scripts/import_ses_official_answers.py
./.venv/bin/python scripts/apply_verified_answers.py
```

Cada solución documentada conserva la URL, el artículo, apartado o plantilla
consultada y la fecha de revisión.

Las plantillas de corrección de Academia Opolis se convierten en lotes importables
con una validación textual de cada opción:

```bash
./.venv/bin/python scripts/import_opolis_answer_sheet.py \
  "TCAE_EXAMEN 2.pdf" /ruta/a/plantilla-correccion-2.pdf \
  --output data/author-answer-seeds-02.json
```
