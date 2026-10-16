# Arquitectura documental

`research/` almacena evidencia, MKs y fuentes; `findings/` conserva observaciones con impacto y cómo reproducir; `patterns/` captura soluciones generalizables; `knowledge/` organiza la lectura por disciplina; `scripts/` y `schemas/` verifican la estructura de conocimiento.

## Máquina de estados

- `OBSERVED`: sustentado por lectura puntual de una fuente fijada.
- `INFERRED`: consecuencia razonada y pendiente de comprobar.
- `RUNTIME_VALIDATED`: probado en instalación Odoo concreta y auditable.
- `REJECTED`: el patrón/hallazgo fue refutado o corregido con evidencia.

## Etiquetas de procedencia

- `OFFICIAL`: documentación oficial Odoo de versión específica.
- `OBSERVED`: fichero real y líneas inspeccionadas.
- `INFERRED`: interpretación no probada en runtime.
- `GENERATED`: material original de este repositorio.

Nunca usar `OFFICIAL` para fuentes comunitarias y nunca convertir una recomendación en un test pasado.

## External Rally source boundary (2026-10-16)

`external/rally` is an immutable-by-policy gitlink to an independent repository. It supplies architectural and implementation evidence for authorization, custody, read-only Odoo JSON-2 state projection, reconciliations, GPS/RFID and ops. It is not placed under `addons/`, the Odoo module loading path, the Odoo filestore, or the commercial runtime image. See `research/integrations/rally/`.

**Authority split:** Odoo = commercial transactions and master data. Rally = observations, custody and recoverable exceptions. Interfaces, if later authorized, must be API-based and versioned with source provenance, tenant grants and stale-data semantics. No shared database and no assumed bidirectional writes.
