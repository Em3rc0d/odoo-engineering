# AGENTS.md — Odoo Engineering

## Mission
Build a verifiable **Odoo-only** knowledge base. Never imply third-party code or exercises are certified. Do not implement addons unless a separately approved build gate explicitly authorizes it.

## Sources and truth ranking
1. **OFFICIAL_REFERENCE**: Odoo 19 documentation with exact URL and version.
2. **STATIC_OBSERVATION**: observed code at a pinned repository commit + file line(s).
3. **INFERRED**: a technically plausible consequence requiring tests.
4. **RUNTIME_VALIDATED**: named Odoo version/edition, test command, environment, fixtures and actual output.

An absence of runtime testing MUST NOT become a pass claim. A code smell is not proof of every user-visible failure.

## Workflow
- Read `research/MK0` and `research/MK1` and `docs/quality-gates.md` first.
- Re-check source SHA and official documentation before adding an assertion.
- Create or revise machine-readable entries (`findings/index.json`, `patterns/index.json`).
- Update corresponding Markdown records; use original prose, not copied implementations.
- Run `python scripts/validate_repo.py` and preserve evidence of its output.
- Include impacts, boundary conditions, alternatives, reproducibility and attribution.
- Prefer smallest useful delta; avoid duplicate patterns or unproven architecture.
- Never write to `personal_knowledge`, original sources or other projects as a side effect.

## Never
- Invent runtime tests, module compatibility, license grants or source SHA.
- Paste complete third-party modules, tests, AGENTS.md or exercise answers.
- Call an OWL+Vite mock a working Odoo integration.
- Suggest copying outdated Odoo APIs without verifying Odoo 19 semantics.
- Modify unrelated code or activate GitHub Actions by default.
