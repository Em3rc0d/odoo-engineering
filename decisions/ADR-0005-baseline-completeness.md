# ADR-0005 — Full baseline coverage without false functional claims

Status: ACCEPTED, 2026-10-13.

The engineering repository separates `vendor/` (upstream snapshots) from `addons/` (our seven candidate improvements/reimplementations). `vendor/` includes seven original `odoo_practices` exercise modules, two `odoo_opencode` modules and selected `odoo_19_addons` modules. Existing exercises may remain intentionally incomplete; their mere presence does not indicate 245 completed solutions.

`ica_web_responsive` is quarantined as third-party-origin material, not an approved production addon. Source-code rights and per-file attribution must be reviewed before redistribution or installation. Unlicensed source is not to be republished; its behavior may be independently reimplemented instead.

User specifically requested **no testing**, so MK3 source candidates have NO executed Odoo 19 runtime, integration, static or security checks recorded as passes. Reconciliation retains prior upstream snapshots and candidate addons in separate locations.
