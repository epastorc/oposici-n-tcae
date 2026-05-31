# Oposición TCAE

Web estática y responsive para practicar tests de oposición de Técnico en Cuidados
Auxiliares de Enfermería (TCAE).

El repositorio incluye un banco de `3.100` preguntas extraídas de `38` PDF y un
importador reproducible para regenerarlo cuando se añadan nuevos exámenes.

## Funcionalidades

- Tests aleatorios de `100`, `50` o `25` preguntas.
- Navegación entre preguntas conservando las respuestas.
- Marcado de preguntas para repasar.
- Resumen final de preguntas respondidas y pendientes.
- Diseño adaptado a escritorio, tablet y móvil.
- Extracción automática de preguntas desde PDF.

## Ejecutar la web

```bash
./scripts/serve.sh
```

Después visita [http://localhost:8000](http://localhost:8000).

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
- `web/`: aplicación estática.

## Respuestas correctas

Los PDF originales no contienen plantillas de soluciones. El formato JSON incluye
el campo opcional `correctAnswer` para incorporar corrección automática más adelante.
