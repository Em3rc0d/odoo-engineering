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
