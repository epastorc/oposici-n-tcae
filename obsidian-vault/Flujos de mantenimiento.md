---
title: Flujos de mantenimiento
tags:
  - proyecto/tcae
  - docs/runbook
status: activo
updated: 2026-06-10
---

# Flujos de mantenimiento

Esta nota recoge los comandos que conviene usar para mantener el proyecto sin depender
de pasos manuales dispersos.

## Ejecutar la app local

```bash
./scripts/serve.sh
```

Después abre `http://localhost:8000`.

## Regenerar revisión y aplicar respuestas

```bash
./.venv/bin/python scripts/build_answer_review.py
./.venv/bin/python scripts/import_answer_seeds.py
./.venv/bin/python scripts/import_ses_official_answers.py
./.venv/bin/python scripts/apply_verified_answers.py
```

## Añadir respuestas investigadas

1. Crear o ampliar un archivo `data/*answer-seeds*.json`.
2. Añadir `source`, `sourceUrl`, `reviewedAt` y `answers`.
3. Usar `excluded` si el enunciado no tiene respuesta publicable.
4. Regenerar revisión y banco.
5. Ejecutar `npm run test:e2e`.

## Añadir respuestas forzadas

Usar archivos `data/forced-answer-seeds-*.json` y marcar el tercer elemento de la
respuesta como:

- `forced-official`
- `forced-clinical`
- `forced-figure`

Ejemplo:

```json
"34": ["b", "Referencia y motivo de la respuesta forzada", "forced-clinical"]
```

## Publicar

```bash
git status --short
npm run test:e2e
git add ...
git commit -m "Mensaje"
git push origin develop
```

El workflow de GitHub Pages vuelve a ejecutar los E2E antes del despliegue.

## Notas relacionadas

- [[Pruebas E2E]]
- [[Despliegue]]
- [[Banco de preguntas]]
