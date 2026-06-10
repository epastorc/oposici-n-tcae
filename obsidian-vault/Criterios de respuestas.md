---
title: Criterios de respuestas
tags:
  - proyecto/tcae
  - docs/criterios
status: activo
updated: 2026-06-10
---

# Criterios de respuestas

El objetivo del banco es entrenar con trazabilidad. Cada respuesta debe conservar una
referencia suficiente para poder revisarla después.

## Prioridad de fuentes

1. Plantillas oficiales del proceso selectivo.
2. BOE, DOE o normativa vigente aplicable.
3. Documentación institucional sanitaria.
4. Plantillas o material docente público del autor.
5. Respuesta forzada documentada cuando el usuario pide que no queden sin contestar.

## Cuándo excluir

Un enunciado se excluye si:

- admite varias opciones válidas;
- depende claramente de un protocolo local;
- falta una figura o contexto imprescindible;
- la norma vigente no encaja con ninguna opción;
- la pregunta usa una taxonomía antigua sin equivalencia clara.

## Cuándo forzar

Se fuerza respuesta cuando el objetivo práctico es que el test sea corregible aunque
la pregunta sea imperfecta. En ese caso se usa `forced-official`, `forced-clinical` o
`forced-figure`, y el motivo debe quedar escrito en `answerSourceDetail`.

## Estado de revisión

| Estado | Significado |
| --- | --- |
| `verified` | Tiene respuesta aplicable al banco |
| `pending` | Aún necesita investigación |
| `excluded` | Revisada, pero sin respuesta publicable con el criterio estricto |

## Notas relacionadas

- [[Banco de preguntas]]
- [[Flujos de mantenimiento]]
