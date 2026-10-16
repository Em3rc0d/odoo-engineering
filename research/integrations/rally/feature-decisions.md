# Rally → odoo-engineering | Decision matrix

Source commit: [b4726668b7a88d1c1cd58ed80c04c1d48d120482](https://github.com/em3rc0dTh/Rally/tree/b4726668b7a88d1c1cd58ed80c04c1d48d120482). Scope: 22 evaluated capability domains.

Rule: Odoo remains commercial system of record; Rally remains operational verification/exception service. This is classification, not installation/functional parity.

| Domain / function | Primary authority | Treatment in odoo-engineering | Priority | Key source |
|---|---|---|---|---|
| POS, sales, cash sessions and stock | ODOO | ODOO_NATIVE | MVP | `point_of_sale, sale, stock` |
| Peruvian electronic invoicing / SUNAT | ODOO | NEW_INTEGRATION | MVP_GATE | `l10n_pe, l10n_pe_pos` |
| Products, inventory, purchase and variants | ODOO | ODOO_NATIVE | MVP | `stock, purchase` |
| Commercial sales dashboard | ODOO | EVALUATE_CANDIDATE | MVP_OPTIONAL | `addons/oe_sales_dashboard` |
| CRM and sale-to-project task link | ODOO | EVALUATE_CANDIDATE | POST_MVP | `addons/oe_crm_task_bridge, addons/oe_sale_task_bridge` |
| Dimension quotes and purchase boards | ODOO | EVALUATE_CANDIDATE | VERTICAL_ONLY | `addons/oe_workshop_quote, addons/oe_purchase_board` |
| Exclusive active custody and audited handovers | RALLY | KEEP_UPSTREAM | VERTICAL_ONLY | `rally/app.py, rally/storage.py` |
| Work order operational evidence and completion checks | RALLY | KEEP_UPSTREAM | VERTICAL_ONLY | `rally/app.py, rally/worker.py` |
| Reconciliation, cases, policy aging and recovery | RALLY | KEEP_UPSTREAM | POST_MVP | `rally/erp_policies.py, rally/worker.py` |
| Odoo JSON-2 read-only state adapters | RALLY | KEEP_UPSTREAM | POST_MVP | `adapters/odoo_json2.py, adapters/odoo_enterprise_cli.py, rally/erp_contract.py` |
| Fleet GPS and Traccar evidence | RALLY | KEEP_UPSTREAM | OUT_OF_SCOPE | `adapters/traccar.py, compose.traccar.yaml, docs/17-traccar-self-hosted.md` |
| RFID ingestion and spool | RALLY | KEEP_UPSTREAM | OUT_OF_SCOPE | `adapters/rfid.py, adapters/rfid_ingest_cli.py` |
| Temporal read-only review workflow | RALLY | KEEP_UPSTREAM | OUT_OF_SCOPE | `workflows/` |
| Tenant isolation, credentials and role audit | SHARED_PATTERN | REIMPLEMENT_PER_PLATFORM | REQUIRED | `rally/security.py, rally/app.py` |
| Idempotency, constraints, migrations, locking | SHARED_PATTERN | ADOPT_DESIGN_ONLY | REQUIRED | `rally/storage.py` |
| Caddy, Compose, nonroot, readiness | SHARED_PATTERN | ADOPT_DESIGN_ONLY | REQUIRED | `compose.production.yaml, ops/` |
| Backup, restore, recovery validation | SHARED_PATTERN | ADAPT_PROCEDURES | REQUIRED | `ops/backup.sh, ops/restore.sh` |
| Pinned Odoo 19 local lab | SHARED_PATTERN | REFERENCE_OR_EXTRACT_AFTER_LICENSE | EARLY | `compose.odoo-lab.yaml, ops/odoo_lab.sh` |
| Python, PostgreSQL, Compose tests and CI | SHARED_PATTERN | ADAPT_TEST_STRATEGY | REQUIRED | `.github/workflows/ci.yml, tests/` |
| Mission Control UX and dashboard | RALLY | KEEP_UPSTREAM | REFERENCE | `rally/web/` |
| Customer interviews, business model and ROI | SHARED_PATTERN | REFERENCE | EARLY | `docs/01-market-feasibility.md, docs/08-commercial-validation.md` |
| Product naming and legal boundaries | SHARED_PATTERN | REVIEW | REQUIRED | `docs/03-open-source-catalog.md, AGENTS.md` |

## Rules for overlap

1. **Transaction vs observation:** POS sales, stock, cash and legal invoices are written by Odoo. Rally imports authorized status only; it never posts invoices, mutates stock or certifies payment settlement.
2. **Commercial product vs assurance add-on:** integrate Rally only for a demonstrated operational exception use case (custody/work orders/assets), not for the first generic retail POS.
3. **Single lifecycle owner:** no second CRM lead or project task model with conflicting truth; bridge events with stable external IDs and explicit per-company grants.
4. **Separate data planes:** never share PostgreSQL schemas or copy an application database to pretend the systems are one. Use documented API contracts, least privilege, idempotency, stale-data markers and provenance.
5. **Reproducibility:** the upstream submodule is pinned; upgrades require SHA review, legal check, test evidence, and an explicit integration decision.
6. **Licensing:** gitlink does not grant reproduction rights. Do not redistribute Rally files inside a commercial Odoo artifact until ownership and licensing are verified.

## Evidence and gaps

- `Rally`: latest inspected `main` is CI green for its own simulated/integration scenarios; this does **not** prove live provider credentials, Odoo API entitlements or customer deployment readiness.
- `odoo-engineering`: Odoo 19 addons are source candidates and are not runtime-certified; no cross-repo functional test was performed for this handoff.
- `Rally` global write serialization is not a design to transplant into Odoo ERP; profile concurrency on the target platform before adoption.
- `Rally` Odoo lab is separate; it does not configure a second retail client, SUNAT, stock, POS or paid onboarding automatically.

Machine-readable version: [feature-decisions.json](feature-decisions.json).