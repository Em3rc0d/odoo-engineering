# odoo-engineering

**Independent Odoo-only engineering source collection.** Approach: **copy licensed → adapt → improve → validate (validation explicitly deferred at user's request)**. Not connected to `personal_knowledge`.

## Current inventory

### Feature addon candidates (UNTESTED)

- `addons/oe_sale_task_bridge` — Odoo sales → projects, revised from licensed `sale_task_creator`.
- `addons/oe_library` — physical book copies and loan integrity, from licensed library curriculum / independent requirements.
- `addons/oe_purchase_board` — quantity/area and purchase order wizard, purchase board upstream.
- `addons/oe_crm_task_bridge` — independent CRM lead → project task association, avoiding duplicate sales fields.
- `addons/oe_workshop_quote` — clean-room workshop quote flow.
- `addons/oe_loan_lab` — educational amortization simulation, not financial accounting.
- `addons/oe_sales_dashboard` — Odoo OWL client action and ORM data; no simulated product IDs.

### Baseline curriculum / references

- `learning/curricula.json` indexes **all seven modules and their 245 exercises** from `odoo_practices`; **does not** contain all seven original exercise modules or their tests.
- `research/MK0` through `MK3`, `research/baselines/adoption-matrix.json`, 11 observed findings, eight patterns, source SHA pins.
- `ica_web_responsive` is held as third-party / web-client override candidate pending independent provenance and compatibility decisions.

## Provenance and license

Each candidate records its own upstream source in `UPSTREAM.md`. Material without copying permission has been independently authored based on conceptual requirements. Some upstream addons declare LGPL-3 in their manifests; there is no assumption of a root-level blanket license. All code needs independent rights and compatibility review before redistribution as a finished product.

## Validation

**No tests were run for this delivery.** Source, XML, manifests, permissions, visuals, security, integration, Odoo 19 installation and database behavior remain unverified. This is a **complete candidate handoff of functional themes**, not a certified Odoo distribution. For optional future validation, see `research/MK2/README.md` and `scripts/`; do not run automatically.

## Upstream snapshots in `vendor/` (not our improved modules)

The imported baseline tree now contains 11 source addon folders: the 7 `odoo_practices` curricula, 2 `odoo_opencode` addons, and `cd_custom_task` plus `ica_web_responsive` from `odoo_19_addons`. There are 312 files under `vendor/` at commit `313fc7f`. These are **unmodified reference snapshots**, not audited/improved production packages. Original 35-exercise modules include pedagogical placeholders; presence of those 245 exercises is **not** completion of solutions. Some original source areas are not copied because no clear rights were identified, and the implementation candidates in `addons/` cover their conceptual functionality independently.

**License caveat:** particularly `ica_web_responsive` has distinct third-party authorship and should be treated as **quarantined**, not distributed/installed pending per-file provenance and compatibility verification. No tests were run at the user's request.

## Rally — independent full source snapshot (2026-10-16)

The entire 94-file source snapshot from `em3rc0dTh/Rally` is now **copied directly** into [`external/rally/`](external/rally/) as ordinary Git files, pinned by recorded source commit `b4726668b7a88d1c1cd58ed80c04c1d48d120482`. This is **not a Git submodule**; a normal `git clone` contains all imported source files. The source Rally repository has not been modified.

The source-to-target Git blob SHA + file mode comparison passed **94/94** at import time. The original Rally commit history is not copied; this repository carries an exact source **snapshot**. Updates do not sync automatically. Refer to [integration guide](research/integrations/rally/README.md), [full file manifest](research/integrations/rally/source-manifest.json), [22 capability decisions](research/integrations/rally/feature-decisions.md) and [commercial MVP scope](research/integrations/rally/mvp-boundary.md).

**Distinct responsibilities:** Odoo handles POS, sales, inventory, cash and fiscal documents; Rally handles custody, operational evidence and reconciliation as a separate optional application. Physical copying does not automatically install Rally as an Odoo addon, integrate it at runtime or qualify either system for production.

## Competir con INVY en Perú — investigación y MVP

La estrategia de un **POS + inventario + caja con Odoo 19**, criterios reales para facturación SUNAT, onboarding repetible y primeros pilotos pagados está documentada en [commercial/retail-peru](commercial/retail-peru/README.md).

Contiene [matriz de 22 capacidades](commercial/retail-peru/parity.json), [contrato técnico](commercial/retail-peru/technical-contract.md), [gates de aceptación](commercial/retail-peru/acceptance-gates.md), [experimento de ventas](commercial/retail-peru/sales-experiment.md), [unit economics](commercial/retail-peru/unit-economics.md) y [sprint de 14 días](commercial/retail-peru/execution-plan.md). **Todavía no es una distribución comercial instalada ni una integración CPE certificada.**

## SUNAT / CPE — experimental adapter and fiscal decision

The Peru retail track now has an [experimental Nubefact JSON gateway](integrations/sunat/README.md), a [fiscal provider choice ADR](integrations/sunat/DEC-PE-EDI-001.md), a limited original Python adapter and **nine unit tests with simulated HTTP**. No CPE has been emitted; the gateway is opt-in and cannot send by default. OPeru 19 + Nubefact is the preferred adoption candidate pending real Community compatibility, provider terms, and a controlled CDR validation.

## INVY Perú Copy — dossier MK0/MK1 (2026-10-19)

El expediente maestro de gestión comercial peruana está en [commercial/invy-peru-copy](commercial/invy-peru-copy/README.md): SRS canónico (88 RF, 43 RNF), 20 casos de uso, 45 BR, arquitectura, UX, fiscalidad open source como opción por validar, planes, fuentes y matriz RF/RNF→UC→TC. El laboratorio Odoo 19, POS/caja/stock fue comprobado en CI [38936119080](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080); esto **no** valida la emisión real SUNAT ni un SaaS multi-tenant comercial.
