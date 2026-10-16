# Retail POS — disposable Odoo 19 lab

**Status:** source/config authored, image tag cross-checked on Docker Hub, **not executed** in this delivery. This is a learning and acceptance sandbox, **not** a production stack or SUNAT-certified solution.

## Why a separate lab?

Rally contains an Odoo laboratory, but its scripts are coupled to Rally's Compose project. This independent sandbox has its own PostgreSQL/filestore volumes and host port **8079**, so it does not collide with Rally's local 8069 lab. Nothing inside `external/rally/` was edited.

## Prerequisites

Docker Engine/Compose v2, Python 3 and Bash (on Windows: WSL2 recommended), adequate RAM/disk and networking to pull images. Version-stamped `odoo:19.0-20260908` is documented on Docker Hub. Update only after recording a reviewed image digest and passing scenario tests.

## Start

```bash
cd experiments/retail-pos-lab
bash scripts/lab.sh init
bash scripts/lab.sh up
bash scripts/lab.sh status
bash scripts/lab.sh version
```

Open **http://127.0.0.1:8079**. Create exactly **`retail_peru_lab`** with the local master password (read only from your machine):

```bash
bash scripts/lab.sh master-password
```

Configure Peru and PEN, install **Point of Sale**, **Inventory**, **Purchase** and **Peru - Accounting** where available. Check exact module names in Apps and do not assume `l10n_pe_edi` is licensed/installed in Community. Use only fictitious products/customers and sample prices. Validate a full sale, stock decrement, refund, register closing and user roles. No SUNAT issuance or real taxpayer credentials.

```bash
bash scripts/lab.sh logs
bash scripts/lab.sh down  # Stops; preserves DB and filestore
```

**Do not run `docker compose down -v`** on a database you wish to keep. The script intentionally has no reset/destroy command.

## Isolation and security

- DB has **no host-exposed port**; Odoo listens only on `127.0.0.1:8079`.
- Local random PostgreSQL credential and random Odoo database-manager password; files `.env.local` and `.local/` are ignored from Git.
- A dedicated private Docker DB network, separate volumes for PostgreSQL and filestore.
- This is not Internet-facing, no TLS, no off-host encrypted backups, no customer isolation orchestrator, no production monitoring. Do not expose it publicly.
- `up --wait` waits for configured health checks. Since Odoo service has no health check, **web application readiness is only shown by the explicit `version` check and UI tests**.
- WSL/Windows file permissions can differ; keep private files in a WSL Linux filesystem where possible.

## Checks still required

1. Docker Compose `config` and real Odoo first bootstrap in an available environment.
2. Confirm image compatibility, POS/inventory modules and clean database creation.
3. Full `commercial/retail-peru/acceptance-gates.md` G1 tests including isolation and backup/restore.
4. Separate e-invoicing/SUNAT compliance; do not suggest a native completed CPE chain.
5. Performance, concurrency and security tests before any pilot.

Official sources: https://hub.docker.com/_/odoo and https://www.odoo.com/documentation/19.0/applications/sales/point_of_sale/use.html .
