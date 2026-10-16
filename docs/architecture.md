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

## Imported Rally source boundary (2026-10-16)

The standalone Rally source snapshot is physically versioned under `external/rally/` as a normal directory, not a submodule. All tracked files are recorded in `research/integrations/rally/source-manifest.json` with upstream Git blob SHA and file mode.

It is **not** part of Odoo's addon path and should not be added wholesale to Odoo's runtime. If deployed separately, enter `external/rally/` and use its own documented Docker/FastAPI commands. Rally's `rally/`, `adapters/`, `tests/`, `ops/`, `docs/`, `workflows/` and locks remain intact.

**Authority split:** Odoo owns products, POS sales, stock, cash and fiscal invoicing. Rally independently owns custody, evidence, work-order assurance, exceptions and source-state projections. Interfaces require explicit API contracts, per-tenant grants, provenance, freshness labels and bounded access. No shared transactional database is authorized.

**Source lifecycle:** no automatic synchronization from upstream; future imports must choose a reviewed source SHA and validate every path/blob SHA/mode, with local changes isolated and clearly attributed.
