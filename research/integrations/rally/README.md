# Rally directly imported into odoo-engineering

Source: https://github.com/em3rc0dTh/Rally  
Pinned source revision: `b4726668b7a88d1c1cd58ed80c04c1d48d120482`  
Imported on: 2026-10-16  
Import mode: **physical Git-tracked snapshot, not a submodule**.

## What is actually inside the target

All **94 upstream tracked files** are committed directly as regular files under [`external/rally/`](../../../external/rally/) with unchanged relative paths and Git blob SHAs. They include:

- `rally/`: FastAPI app, persistence, authorization, worker, ERP policies, Mission Control web interface;
- `adapters/`: Odoo JSON-2 / enterprise read-only state bridge, GPS/Traccar, RFID ingestion;
- `workflows/`: optional Temporal review examples;
- `ops/`: backup/restore, runbooks, preflight, smoke checks, Odoo local lab script;
- `tests/` and `.github/workflows/ci.yml`: test suites and original CI configuration;
- `docs/`: vision, market research, architecture, Odoo integration, release/operations and commercial feasibility;
- Docker/Compose, Python dependency locks, `README.md`, `AGENTS.md`, example environment files.

**Git independence:** `git clone https://github.com/Em3rc0d/odoo-engineering.git` now suffices; no `--recurse-submodules` is needed. It remains an exact imported snapshot, **not the complete upstream Git history**, and future upstream changes do not appear automatically. We did not make any writes to Rally's own repository.

## Verified source integrity

The full upstream Git tree and the target import tree were compared: **94/94 same path, Git blob SHA and mode; 0 missing or extra tracked files inside the imported directory**. Original source commit and file metadata are listed in [source-manifest.json](source-manifest.json). This is source-level integrity only, not a completed application/runtime test.

## How to work with the copied application

```bash
git clone https://github.com/Em3rc0d/odoo-engineering.git
cd odoo-engineering/external/rally
# Review README.md and AGENTS.md here before running anything.
# Optionally, in an isolated environment with Docker available:
cp .env.example .env
# Set a strong distinct RALLY_ADMIN_KEY locally (never commit secrets).
docker compose up --build -d
```

**Important:** Rally's existing Compose file expects relative paths from `external/rally/`, not the parent `odoo-engineering`. Its nested `.github/workflows/ci.yml` is preserved verbatim but does **not** run automatically as a GitHub Actions workflow in the root repository. No extra CI or deployment was activated by this import.

## Separation of responsibilities

- `addons/`: Odoo addon candidates, subject to installation/ACL/license/runtime testing.
- `external/rally/`: independent, complete Rally application source snapshot. Do **not** put this directory in Odoo's addons search path or copy Rally migrations into the ERP database.
- `research/integrations/rally/`: integration decisions, source manifest and MVP boundary.
- Odoo handles POS, inventory, sales, cash, invoices and fiscal legal records. Rally handles custody, execution evidence, exceptions, GPS/RFID and read-only ERP state observations.
- API-based integration is a later optional, separately tested contract. No existing Odoo/Rally functional integration is certified by this import.

## Proprietary and third-party considerations

The user states ownership of both repositories. Their company/client obligations, third-party dependencies, referenced datasets and the product name should still be checked prior to commercialization; a source copy does not replace licensing and product compliance review. Preserve upstream provenance in the manifest. Do not incorporate Enterprise-only Odoo code unless explicitly licensed.

## Next steps

1. Keep owner-specific Odoo addons and the Rally service isolated and runnable from their own roots.
2. Close the commercial MVP's product, Peru/SUNAT and deployment requirements before implementing.
3. Prove Odoo Community POS, stock, session-close and refund flows with real database tests.
4. Design a separate reproducible customer setup (DB **and** filestore, secrets, HTTPS, backup and restore).
5. Only enable Rally assurance for a contracted use case with verified ROI, source rights and cross-system validation.

See [capability matrix](feature-decisions.md) and [MVP boundaries](mvp-boundary.md).
