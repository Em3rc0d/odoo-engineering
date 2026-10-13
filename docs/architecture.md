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
