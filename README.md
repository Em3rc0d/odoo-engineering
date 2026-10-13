# Odoo Engineering

**From proven baselines to improved Odoo modules.** `odoo-engineering` is an **independent Odoo-only engineering repository** that turns public Odoo examples into traceable, safer, testable implementations: **copy when licensed → adapt → improve → validate**. It does not change `personal_knowledge` or the upstream repositories.

> **Status v0.2.0 (2026-10-13): 2 candidate Odoo 19 addons, static validation PASS, runtime validation NOT RUN.** Do not deploy to production until installation, functional tests and security gates pass.

## Working software (candidate addons)

| Module | What it does | Baseline | Added engineering |
|---|---|---|---|
| [`oe_sale_task_bridge`](addons/oe_sale_task_bridge/) | Sale order → selected project task | LGPL-3 `odoo_opencode/sale_task_creator` | Odoo19 `_read_group` tuple handling, namespaced link, project wizard, conservative ACL, tests |
| [`oe_library`](addons/oe_library/) | Books, physical copies, loans | LGPL-3 educational `odoo_practices`; independent rebuild of unlicensed `Pruebas_Odoo` requirements | Per-copy active loan DB invariant, transition checks, nonstored overdue, demo isolation, tests |

**Licensing:** Both modules declare LGPL-3 and include the license text under their directories. Original source and modifications are described in their `UPSTREAM.md`; the documentation repository as a whole does **not** assert a single blanket license. Sources without identifiable reuse grants are **not** copied. For more details, see [adoption matrix](research/baselines/adoption-matrix.json) and [license review](research/sources/LICENSE_REVIEW.md).

## Quick check (no Odoo required)

```bash
python3 scripts/validate_repo.py
python3 scripts/validate_addons.py
```

Offline checks cover document indexes, manifest file references, Python AST, XML syntax, ACL shape and a few known issue guardrails; they **do not prove installability or runtime behavior**.

## Install/test (requires your Odoo 19 + PostgreSQL environment)

Add this repository's `addons/` directory to Odoo's `--addons-path`, then install in a **disposable test database**:

```bash
./odoo-bin -d oe_test -i oe_library,oe_sale_task_bridge \
  --addons-path=addons,/ruta/odoo-engineering/addons \
  --test-enable --test-tags=/oe_library,/oe_sale_task_bridge \
  --stop-after-init --log-level=test
```

The command is a recipe **not executed** in this work. Installation depends on Odoo 19's `base`, `sale` and `project`, PostgreSQL, and users/ACL. Save logs and actual test results under `validation/`; a clean Python syntax check is insufficient.

## Research and decisions

- [MK0 — original evaluation](research/MK0/README.md) and [MK1 — knowledge contract](research/MK1/README.md).
- [MK2 — baseline adaptation and acceptance gates](research/MK2/README.md).
- [Baseline adoption matrix](research/baselines/adoption-matrix.json) — five sources, nine candidate components.
- [Findings](findings/README.md) and [patterns](patterns/README.md) — diagnosis informs modifications.
- [License/copyright review](research/sources/LICENSE_REVIEW.md), [ADR-0004](decisions/ADR-0004-baseline-adaptation.md), [agents](AGENTS.md), [quality gates](docs/quality-gates.md).
- [Validation evidence](validation/2026-10-13-static.md).

## Next improvements — only after A2/A3

- Reconcile `purchase_board_wizard` with workshop flows: avoid model-name collisions and ambiguous square-metre quantity pricing.
- Assess Odoo-native OWL frontend rather than reusing a Vite dashboard containing fabricated product KPIs.
- Validate accounting/loan management logic and provenance separately (no unlicensed code copy).
- Add librarian group/record-rule matrix and concurrency race tests once the modules install and their operations work.

**No GitHub Actions CI is enabled.** The repository is maintained with local validation and reproducible evidence.
