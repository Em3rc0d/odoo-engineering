# Quality gates (knowledge + runnable addons)

| Gate | Condition | Status as of 2026-10-13 |
|---|---|---|
| G0 — Source | SHA pinned and evidence link | PASS for 5 baselines |
| G1 — License | Per-file/per-module copy permission + attribution + modifications | CONDITIONAL: licensed source modules identified, third-party chains not exhaustively audited |
| G2 — Static | All XML, manifest, Python, ACL shapes, source indices | PASS locally on two candidate addons |
| G3 — Install | Clean Odoo 19 install/upgrade with database and required dependencies | NOT RUN |
| G4 — Test | All 11 tests, concurrency checks, ACL roles & logs | NOT RUN |
| G5 — Product | User acceptance, enterprise/community compatibility, security, performance | NOT AUTHORIZED |

**No one should infer G3/G4/G5 from a G2 pass.**

## Proof checklist
Record exact Odoo edition/build, PostgreSQL version, addon commits, command line, isolated fixture seeds, logs, installation result, test case counts, concurrency attempt and permissions with a non-admin user. Consider security and module upgrade after basic behavior passes.

## Rally source-reference gates (2026-10-16)

| Gate | State | Meaning |
|---|---|---|
| R0 — Pin and manifest | RECORDED | External Rally gitlink SHA and full file manifest captured |
| R1 — IP/redistribution | BLOCKED | No root Rally license verified; company/customer ownership and sublicensing unresolved |
| R2 — Source separation | DOCUMENTED | Domain authority split; no wholesale transplant into Odoo addons |
| R3 — Odoo 19/runtime | NOT RUN HERE | Existing addons remain untested in Odoo 19; Rally CI only validates Rally at its SHA |
| R4 — Live integration | NOT RUN HERE | Real Odoo JSON-2 compatibility, SUNAT and customer credentials not verified |
| R5 — Paid pilot | NOT VALIDATED | Repeatable onboarding, isolation, recovery, support economics and acceptance absent |

A green Rally CI does not upgrade G3/G4/G5 for `odoo-engineering`.
