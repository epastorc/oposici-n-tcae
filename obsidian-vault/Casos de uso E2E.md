---
title: Casos de uso E2E
tags:
  - proyecto/tcae
  - tests/e2e
status: activo
updated: 2026-06-10
---

# Casos de uso E2E

- Carga inicial de la app y de los bancos de preguntas.
- Validación del formulario de inicio, incluyendo nombre vacío.
- Creación y ejecución de un test normal de 25 preguntas.
- Marcado de preguntas para repasar y avance entre preguntas.
- Guardado, reanudación y borrado de un test en progreso.
- Bloqueo de nombres duplicados al crear retos nuevos.
- Ejecución del examen oficial `Turno Libre 2013`.
- Ejecución de un test por temario con tamaño configurable.
- Registro de fallos y arranque del test de preguntas incorrectas.

## Cobertura actual

Estos casos están automatizados en `tests/e2e/app.spec.js`.

## Notas relacionadas

- [[Pruebas E2E]]
- [[Arquitectura del proyecto]]
