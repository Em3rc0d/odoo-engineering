# MK3 — Baseline expansion (2026-10-13)

**User-requested rule: no tests or execution.** Deliver source candidates without runtime certification.

## Candidates added

| Module | Reference baseline | Implementation mode | Status |
|---|---|---|---|
| `oe_purchase_board` | `odoo_opencode/purchase_board_wizard` | rewrite, LGPL-3 baseline | UNTESTED |
| `oe_crm_task_bridge` | `odoo_19_addons/cd_custom_task` | isolated CRM link avoiding duplicate sales bridge | UNTESTED |
| `oe_workshop_quote` | `odoo_19_addons/cd_workshop_flows` | clean-room original requirements only (license unspecified) | UNTESTED |
| `oe_loan_lab` | `odoo_19_addons/cd_loan_management` | clean-room educational simulation only (license unspecified) | UNTESTED |
| `oe_sales_dashboard` | `proyecto_OWL` | clean-room original Odoo OWL/ORM dashboard; no mock-code import | UNTESTED |
| `learning/curricula.json` | `odoo_practices` | full 7×35 exercise inventory, NOT implementation migration | REFERENCE ONLY |

## Not copied

- `ica_web_responsive`: baseline snapshot present under `vendor/`, but **quarantined**; broad web-client replacement and third-party provenance prohibit treating it as a deployable improved addon.
- Original seven exercise addon snapshots: present in `vendor/odoo_practices/`, but **not solved, repaired or tested**.
- Unlicensed `Pruebas_Odoo` source or `proyecto_OWL` source: requirements adapted, original source not copied.

## Debt knowingly accepted

There has been **no static checking, installation, integration run, Odoo 19 runtime testing, ACL verification, or UI testing as part of MK3** because user explicitly requested delivery without tests. All new modules are **candidate source code**, not proven runnable or production safe.

## Source provenance

Revisions are pinned under `research/sources/catalog.json`; each candidate contains `UPSTREAM.md`. The prior two modules remain. Do not claim a completed functional consolidation merely because each functional area has a candidate.


## Final remote inventory note

By commit `313fc7f`, `vendor/` contains 11 upstream addon folders (seven educational, two opencode, two odoo_19_addons). `addons/` contains seven candidate independently improved or rewritten addons. No tests run; no functional certification. License-rights review remains separate, especially for third-party web-responsive sources.
