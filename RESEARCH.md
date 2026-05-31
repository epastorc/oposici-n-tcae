# Investigación de soluciones

## Estado

- Preguntas extraídas: `3.100`.
- Enunciados únicos tras deduplicación: `2.816`.
- Soluciones verificadas: `56`.
- Preguntas excluidas por redacción ambigua o desactualizada: `1`.

## Criterio

Una respuesta solo se publica como correcta cuando dispone de una fuente primaria:

- Diario Oficial de Extremadura (DOE).
- Boletín Oficial del Estado (BOE).
- Documentación institucional de la Junta de Extremadura o del SES.
- Guías oficiales de organismos sanitarios públicos para el bloque clínico.

Cada respuesta conserva URL, artículo o apartado y fecha de revisión. Las respuestas
no verificadas permanecen como `null`; no se completan mediante inferencias.

## Primera tanda: Estatuto Marco

Se han revisado `56` preguntas del archivo `TCAE_EXAMEN 11 ESTATUTO.pdf` contra el
texto consolidado de la Ley 55/2003:

- BOE: <https://www.boe.es/buscar/act.php?id=BOE-A-2003-23101>

La pregunta 17 no se publica como corregible: pregunta por una edad fija para la
jubilación voluntaria, pero el artículo 26.3 remite a los requisitos de la legislación
de Seguridad Social.

## Fuentes localizadas para las siguientes tandas

- Ley 8/2011 de Extremadura:
  <https://doe.juntaex.es/pdfs/doe/2011/590o/11010008.pdf>
- Ley 40/2015:
  <https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566>

## Flujo de trabajo

```bash
./.venv/bin/python scripts/build_answer_review.py
./.venv/bin/python scripts/import_answer_seeds.py
./.venv/bin/python scripts/apply_verified_answers.py
```
