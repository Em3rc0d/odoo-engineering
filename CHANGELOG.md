# Changelog

## 0.1.0 — 2026-10-13
- Primera fundación documental exclusiva Odoo, cinco fuentes con revisiones fijadas.
- MK0/MK1, catálogo JSON, patrones y hallazgos vinculados.
- Contrato para agentes, validación documental local y registro de riesgos/licencias.
- Sin modificación de los cinco repositorios fuente, ni pruebas Odoo ejecutadas, ni despliegue.

## 0.2.0 — 2026-10-13
- Pivot to source-baseline **copy licensed → adapt → improve → validate** implementation strategy (ADR-0004).
- Created `oe_sale_task_bridge` as an LGPL-3 adaptation of the licensed sale-task addon, with namespace, wizard, ORM correction and test suite.
- Created new `oe_library` addon from Odoo educational patterns/library requirements, with PostgreSQL active-loan invariant and tests; no source copy from unlicensed `Pruebas_Odoo`.
- Added adoption matrix for all five inspected repositories, MK2 implementation gates and offline addon validator.
- Offline static checks pass; real Odoo 19 install/test remains pending.
