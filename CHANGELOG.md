# Changelog

## 0.3.0 — 2026-10-13

- Added five source-code candidate addons covering purchases, CRM tasks, workshop quoting, loan simulation and OWL sales dashboard.
- Indexed seven Odoo practice domains × 35 exercises, without falsely claiming their source/tests were imported.
- MK3 establishes source-level adoption boundaries and no-run/no-test state.
- `ica_web_responsive` held because a wholesale web-client replacement is not an acceptable unreviewed transplant.
- No Odoo tests run or results claimed.

## 0.2.0 — 2026-10-13
- Initial sale-task bridge and book-loan candidates.

## 0.1.0 — 2026-10-13
- Evidence repository foundation and findings.

## 2026-10-16 — Import full Rally source directly

- Replaced `external/rally` Git submodule with **all 94 source files** as ordinary Git-tracked files, copied from upstream commit `b4726668b7a88d1c1cd58ed80c04c1d48d120482`.
- Removed obsolete `.gitmodules` and gitlink. No changes to the original `em3rc0dTh/Rally` repository.
- Verified path, Git blob SHA and file mode parity for all 94 files before committing.
- Preserved 22 domain ownership decisions, complete source manifest and production/MVP gates; updated handoff docs to describe an independent source snapshot.
- No cross-service integration, Odoo addon certification or customer deployment is implied.
