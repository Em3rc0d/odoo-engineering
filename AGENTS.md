# AGENTS — Odoo Engineering

## Mission and approach
Build a sound **Odoo-only codebase** from pinned public baselines: **COPY ONLY WHEN LICENSED → ADAPT → IMPROVE → TEST**. Document original repository, commit, per-addon license, changed behavior and test evidence. No edits outside this repository.

## Before coding
1. Read `research/MK2/README.md`, `research/baselines/adoption-matrix.json`, and `decisions/ADR-0004-baseline-adaptation.md`.
2. Confirm module/file license, provenance and original author. A public repo with no license does not grant automatic redistribution rights.
3. Inspect baseline code and conflicts with installed modules, especially `_name` collisions.
4. Prioritize smallest vertical slice whose verification can be specified.

## When coding
- Target Odoo **19.0**; prefer namespaced fields, correct API semantics and safe ACL (do not grant permissions over standard Odoo models).
- Require tests beside every module, and isolate fixtures. Do not copy failed or incomplete upstream tests as validated solutions.
- Preserve LGPL-3 license text and attribution on derivatives. Use `UPSTREAM.md` for source→adaptation map.
- Never claim runtime readiness until an actual Odoo installation and TransactionCase execution have logs.
- Keep versioned MK phases, actual baseline matrix and ADR history. Supersede old decisions explicitly, rather than silently deleting them.

## Verify
`python3 scripts/validate_repo.py && python3 scripts/validate_addons.py` (offline only), then run installed Odoo 19 tests in an isolated database, record both positive and negative results. Never trigger GitHub Actions without request.

## Guardrails
No dependence on `personal_knowledge`; no migration from unlicensed projects; no copied standalone OWL mock masquerading as ERP integration; no free-form permissions on `sale.order`/`project.task`; no invented green tests; no direct production database operations.
