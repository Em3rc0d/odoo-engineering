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

## Rally — versioned external reference (2026-10-16)

The full Rally upstream tree is linked at `external/rally` as a **read-only Git submodule**, pinned to `b4726668b7a88d1c1cd58ed80c04c1d48d120482`. Rally remains its own operational-assurance product; this does **not** merge its custody service into Odoo or automatically license its code for redistribution.

Use `git clone --recurse-submodules` or `git submodule update --init external/rally`. See [integration analysis](research/integrations/rally/README.md), [capability ownership](research/integrations/rally/feature-decisions.md), [full source manifest](research/integrations/rally/source-manifest.json) and [commercial MVP boundary](research/integrations/rally/mvp-boundary.md).

Odoo remains responsible for POS, sales, inventory, legal invoicing and cash. Rally retains equipment custody, evidence, GPS/RFID and operational exception resolution. Production deployment, API integration and Odoo addon installation remain separate quality gates.
