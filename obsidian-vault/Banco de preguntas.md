---
title: Banco de preguntas
tags:
  - proyecto/tcae
  - docs/datos
status: activo
updated: 2026-06-10
---

# Banco de preguntas

El banco principal está en `web/data/questions.json`. Contiene preguntas de exámenes
con opciones, respuesta correcta cuando existe y trazabilidad de la fuente usada.

## Estado actual

| Métrica | Valor |
| --- | ---: |
| Preguntas totales | 3.186 |
| Fuentes | 39 |
| Preguntas con respuesta aplicada | 2.957 |
| Banco por temario | 200 |

## Tipos de fuente de respuesta

| `answerSourceKind` | Uso |
| --- | --- |
| `official` | Norma, plantilla oficial o fuente institucional |
| `author-key` | Plantilla de corrección publicada por autor/academia |
| `author-material` | Material docente público del autor |
| `forced-official` | Respuesta forzada contra norma oficial cuando el enunciado/opciones no encajan perfectamente |
| `forced-clinical` | Respuesta forzada por convención clínica/docente |
| `forced-figure` | Respuesta inferida por emparejamiento de figura y uso |

## Archivos importantes

- `data/answer-review.json`: cola deduplicada de revisión.
- `data/legal-answer-seeds*.json`: lotes jurídicos o normativos.
- `data/clinical-answer-seeds*.json`: lotes clínicos revisados.
- `data/batch-answer-seeds*.json`: lotes por tanda.
- `data/forced-answer-seeds*.json`: respuestas forzadas documentadas.
- `web/data/questions.json`: banco final consumido por la app.

## Comandos de regeneración

```bash
./.venv/bin/python scripts/build_answer_review.py
./.venv/bin/python scripts/import_answer_seeds.py
./.venv/bin/python scripts/import_ses_official_answers.py
./.venv/bin/python scripts/apply_verified_answers.py
```

> [!warning]
> Las respuestas `forced-*` deben tratarse como solucionario práctico para entrenar,
> no como garantía de que el enunciado fuera perfecto. La explicación queda en
> `answerSourceDetail`.

## Notas relacionadas

- [[Criterios de respuestas]]
- [[Flujos de mantenimiento]]
