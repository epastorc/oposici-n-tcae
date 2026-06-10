---
title: Despliegue
tags:
  - proyecto/tcae
  - docs/deploy
status: activo
updated: 2026-06-10
---

# Despliegue

La web se publica con GitHub Pages desde la rama `develop`.

## Flujo de GitHub Actions

```mermaid
flowchart TD
    A["Push a develop"] --> B["Checkout"]
    B --> C["Setup Node 22"]
    C --> D["npm ci"]
    D --> E["Instalar Chromium Playwright"]
    E --> F["npm run test:e2e"]
    F --> G["Configurar Pages"]
    G --> H["Generar web/version.json"]
    H --> I["Subir artifact"]
    I --> J["Deploy"]
```

## Versionado visible

Durante el despliegue se genera `web/version.json` con:

- `commit`: hash corto desplegado.
- `deployedAt`: fecha UTC.

La app lo muestra en el pie de página.

## Comprobación rápida

```bash
curl -fsSL "https://epastorc.github.io/oposici-n-tcae/version.json"
```

## Riesgos habituales

- Si Playwright falla, no se publica.
- Si `web/data/questions.json` no carga, fallan los E2E.
- Si `version.json` no existe localmente, la app lo ignora; en Pages se genera en CI.

## Notas relacionadas

- [[Pruebas E2E]]
- [[Flujos de mantenimiento]]
