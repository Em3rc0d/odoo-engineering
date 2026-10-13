# MK1 — Contrato de consolidación

**Sistema**: documentación comprobable, no runtime Odoo ni librería de addons.

## Objetos

- **Source**: ID, origen, commit fijo, estado de licencia, fecha y runtime status.
- **Finding**: ID, archivo y líneas, tipo de evidencia, riesgo, prueba necesaria, estado.
- **Pattern**: ID, título, problema, recomendación, límites, enlaces y gates.
- **Decision**: ADR para decisiones difíciles de revertir.

## Integridad

Cada hallazgo apunta a un `SRC-*` válido y un documento existente; cada patrón referencia al menos un hallazgo o fuente; ningún patrón puede decir que está validado en runtime mientras la evidencia sea solo estática.

## Primer corte (v0.1)

- Once hallazgos con evidencias para discutir y reproducir.
- Ocho patrones Odoo con lineamientos comprobables.
- README, agentes, gates y catálogo legibles por humanos y herramientas.
- Índices JSON fuente de verdad para inventario; documentos Markdown para contexto.

**No incluido:** fork/copia de fuentes, addon funcional nuevo, curso comercial, asistentes conectados a una base ERP, automatizaciones de GitHub, garantía sobre compatibilidad enterprise.

## Salida válida

MK1 documental puede cerrarse tras validar índice, enlaces, originalidad y review técnica. Un **GO de implementación** se evalúa aparte cuando exista caso real; no por el mero hecho de tener documentación.
