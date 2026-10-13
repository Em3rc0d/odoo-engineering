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
