---
title: Pruebas E2E
tags:
  - proyecto/tcae
  - tests/e2e
status: activo
updated: 2026-06-10
---

# Pruebas E2E

La suite E2E usa Playwright y arranca un servidor estático sobre `web/`.

## Comandos

```bash
npm ci
npm run test:e2e
```

Para depurar visualmente:

```bash
npm run test:e2e:headed
```

## Qué valida

- Catálogo principal y banco por temario cargan correctamente.
- El formulario avisa si falta nombre.
- Se puede crear un test normal, responder, marcar para repasar y finalizar.
- Los tests en progreso se guardan, continúan y eliminan.
- No se permiten nombres duplicados.
- El examen oficial `Turno Libre 2013` arranca en orden.
- El test por temario respeta el tamaño elegido.
- Las preguntas falladas se registran y se pueden repetir.

## Integración con despliegue

El workflow `.github/workflows/pages.yml` ejecuta:

```bash
npm ci
npx playwright install --with-deps chromium
npm run test:e2e
```

Solo si la suite pasa se generan `web/version.json`, el artifact de Pages y el
despliegue.

## Notas relacionadas

- [[Casos de uso E2E]]
- [[Despliegue]]
