# Investigación de soluciones

## Estado

- Preguntas extraídas: `3.100`.
- Enunciados únicos tras deduplicación: `2.816`.
- Soluciones verificadas: `961`.
- Preguntas excluidas por redacción ambigua o desactualizada: `28`.

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

También se han revisado `57` preguntas válidas de `TCAE_EXAMEN 37.pdf` contra la
misma ley. Tres enunciados de ese bloque permanecen excluidos: dos atribuyen una
edad fija a la jubilación voluntaria y otro pregunta por un derecho inexistente
cuando todas sus opciones figuran en el artículo 17.

Se han revisado `70` preguntas válidas de `TCAE_EXAMEN 39.pdf` contra la Ley
8/2011 publicada en el DOE y contra la Ley 40/2015 consolidada en el BOE. Tres
preguntas permanecen excluidas por opciones erróneas o por incluir varias respuestas
válidas sin opción conjunta.

Se ha revisado `TCAE_EXAMEN 36.pdf` contra la Ley Orgánica 1/2011, de reforma del
Estatuto de Autonomía de Extremadura. El bloque contiene `95` respuestas verificadas
y cinco exclusiones por formulación defectuosa o por tratarse de una pregunta
histórica que no debe publicarse como solución estable.

Se ha iniciado `TCAE_EXAMEN 35.pdf`, recopilatorio sobre la Constitución Española.
El bloque `TCAE_EXAMEN 35.pdf` queda revisado con `360` respuestas verificadas
contra el texto consolidado publicado en el BOE. Ocho preguntas permanecen excluidas
por ofrecer respuestas incompletas o varias opciones válidas.

Se ha iniciado `TCAE_EXAMEN 38.pdf` sobre Ley de Salud de Extremadura y Estatutos
del SES. La primera tanda incorpora respuestas estables de la Ley 10/2001 y del
Decreto 221/2008 publicado en el DOE; las preguntas dependientes de versiones del
organigrama quedan pendientes de revisión consolidada.

La segunda tanda del mismo examen contrasta la estructura del SES con la
consolidación ELI del Decreto 221/2008. Se publican `76` respuestas verificadas del
bloque y se excluyen dos preguntas de personal cuyas opciones ya no coinciden con
la estructura orgánica consolidada.

## Plantillas oficiales SES

El examen `TCAE_EXAMEN 30.pdf` corresponde al proceso selectivo SES del 27 de abril
de 2019. Su plantilla oficial contiene `108` respuestas:

- SES: <https://saludextremadura.ses.es/bolsa/documentos/2019_04_29_002.pdf>

Los exámenes `TCAE_EXAMEN 32.pdf` y `TCAE_EXAMEN 33.pdf` son las dos versiones
oficiales de auxiliar de enfermería de la Junta de Extremadura del 19 de diciembre
de 2009:

- Junta de Extremadura, tipo 1:
  <https://www.juntaex.es/documents/77055/314190/1212%2BRESPUESTAS_E1_1212_1.pdf/42fa2448-cef5-4249-a7ad-f66c829422ba?t=1414688042010&version=1.0>
- Junta de Extremadura, tipo 2:
  <https://www.juntaex.es/documents/77055/314190/1212%2BRESPUESTAS_E1_1212_2.pdf/1cd30681-f7a1-439c-a1d0-9fcc17811f86?t=1414688045790&version=1.0>

## Fuentes localizadas para las siguientes tandas

- Ley 8/2011 de Extremadura:
  <https://doe.juntaex.es/pdfs/doe/2011/590o/11010008.pdf>
- Ley 40/2015:
  <https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566>

## Flujo de trabajo

```bash
./.venv/bin/python scripts/build_answer_review.py
./.venv/bin/python scripts/import_answer_seeds.py
./.venv/bin/python scripts/import_ses_official_answers.py
./.venv/bin/python scripts/apply_verified_answers.py
```
