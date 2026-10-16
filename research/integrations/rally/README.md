# Rally pinned reference and integration contract

Captured 2026-10-16; upstream: https://github.com/em3rc0dTh/Rally; pinned commit: `b4726668b7a88d1c1cd58ed80c04c1d48d120482`.

## What was brought over

`external/rally/` is a **Git submodule** pointing to the full Rally repository at the recorded SHA. On recursive clone, it checks out **all upstream files**, including application, adapters, tests, operations, docs, optional Traccar/Odoo labs, and workflows. We deliberately did not bulk-copy or modify Rally's source files.

```bash
git clone --recurse-submodules https://github.com/Em3rc0d/odoo-engineering.git
cd odoo-engineering
git submodule status
# For an existing clone:
git submodule update --init external/rally
```

GitHub's web interface shows a submodule link; to inspect actual upstream files, follow its commit. The source manifest [source-manifest.json](source-manifest.json) inventories every tracked file from this pinned commit with blob SHA and size.

## Explicit boundaries

- `odoo-engineering/addons/`: Odoo-specific addons, each separately licensed, attributed, tested and installed.
- `external/rally/`: upstream source snapshot for inspection, **not** installable Odoo addons, not a vendored/copied codebase, and not a production dependency.
- `research/integrations/rally/`: ownership map and commercial selection gates, without rewriting Rally's mission.
- Odoo handles POS, products, inventory, sales, invoices and cash. Rally independently handles custody, evidence, exception recovery, GPS/RFID observations and read-only ERP statuses.
- No cross-repo integration, data migration, auth federation, billing, or production deployment was performed in this change.

## Ownership and licensing

Rally lives under a different GitHub account, and the inspected root has **no blanket LICENSE**. Its documents include company-specific references. This submodule is a non-mutating Git reference, not a grant of rights to extract, commercialize, sublicense or rebrand its code. Confirm intellectual-property ownership and any employment/client obligations before making derivative deployments. Odoo community modules, external vendors and images each retain their own independent terms.

## Evidence by function

| Capability | Rally files | What is reusable | What is not inherited |
|---|---|---|---|
| Tenant-scoped access | `rally/app.py`, `rally/security.py`, `rally/storage.py` | Threat model, tests, audit contracts | Odoo ACL / record rules, SSO or certified IAM |
| Concurrent custody | `rally/app.py`, `rally/storage.py` | Unique-active-item and idempotency patterns | Inventory reservation or POS concurrency guarantees |
| Exceptions and recovery | `rally/worker.py`, `rally/erp_policies.py` | Deterministic comparisons and acknowledged resolution | Accounting/payment settlement proof |
| Odoo bridge | `adapters/odoo_json2.py`, `adapters/odoo_enterprise_cli.py`, `rally/erp_contract.py` | Source scoping and status projections | A complete bidirectional Odoo integration |
| Traccar / RFID | `adapters/traccar.py`, `adapters/rfid*.py`, `compose.traccar.yaml` | Observation/provenance/freshness patterns | Physical completion or legal custody proof |
| Deployment and recovery | `compose.production.yaml`, `ops/backup.sh`, `ops/restore.sh` | Runbook and restore drills | Backup of an Odoo filestore or tenant provisioning |
| Odoo lab | `compose.odoo-lab.yaml`, `ops/odoo_lab.sh` | Isolated reference environment | Retail production distribution |
| Test quality | `.github/workflows/ci.yml`, `tests/` | CI scenario list and fixture techniques | Tested Odoo addons and live customer acceptance |

## Next steps / gates

1. Confirm rights to reuse code and applicable Odoo/third-party licenses.
2. Validate Odoo 19 clean installation and required Community modules (`point_of_sale`, `stock`, `purchase`) in a dedicated test DB.
3. Check each candidate addon for ACLs, install/upgrade paths and actual functionality on Odoo 19.
4. Build a **separate** repeatable-client delivery template (database + filestore, HTTPS, secrets, restore, tenant-specific configuration); do not turn Rally's custody stack into POS.
5. Run accepted scenarios for POS, stock, cash, returns and fiscal flow; optionally add Rally assurance only if a paying pilot proves need.

Related: [Decision matrix](feature-decisions.md) · [MVP gates](mvp-boundary.md).