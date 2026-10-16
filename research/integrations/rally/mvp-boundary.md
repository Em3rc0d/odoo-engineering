# Reproducible retail MVP | boundaries inherited from Rally study

**Goal:** one standard Odoo Community retail installation, reproducible across independent customers. This is not an exact INVY copy and is not yet production certified.

## MVP-in

- Product catalog, barcode, stock movements, sales/POS, cash sessions, basic reporting, roles and permissions using native Odoo modules.
- One client = isolated database **and filestore**, configuration, credentials, backups and tested restore. Keep Odoo as the single commercial system of record.
- Simple onboarding recipe: create company, import customers/products, permissions, payment methods, POS configuration, sample transactions, verify accounting assumptions.
- Peru localization gate: check legal invoice issuance and provider/EDI integration separately. Do not claim SUNAT e-invoicing from Community alone.

## MVP-out

- Custody GPS/RFID/Traccar, employee payroll, Temporal, Rally case automation, AI forecasts, multisucursal orchestration, complex self-service billing, Odoo Enterprise-only functionality.
- Installing untested custom addons, using quarantined vendor UI code, cloning private/licenseless product source.

## Evidence-driven GO criteria

1. Two independent isolated customer installations created from the same immutable image/tag with audited config differences only.
2. Correct totals, stock and cash for sale, discount, refund and concurrent same-item attempts; no duplicate writes on retries.
3. Cross-client access denied by live tests under non-admin roles.
4. PostgreSQL and filestore backup restored in an isolated environment; recovery procedure documented and practiced.
5. Exact license/SBOM and IP rights reviewed, credentials/HTTPS, monitoring, retention and support agreement in place.
6. If electronic fiscal emission is sold, genuine end-to-end authorized SUNAT/provider validation and relevant legal review.
7. At least one external buyer agrees to a bounded paid pilot; production use follows customer acceptance, not demo alone.

## Integration rule

Rally is only a later independent assurance add-on with explicit customer value, contracts, read-only source scopes and actual provider validation. No code from `external/rally` is automatically shipped.

## Implementation order

First close platform/license architecture (MK0/MK1), then build/test MVP, then onboard paying pilots. No claim of finished SaaS from this documentation or Git submodule addition.