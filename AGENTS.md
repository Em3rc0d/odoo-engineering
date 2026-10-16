# Odoo Engineering instructions

**Mission:** Maintain Odoo-only feature addons with linked baselines. Principle: COPY when licensed, ADAPT for platform, IMPROVE demonstrably, VALIDATE when separately authorized.

- Read `research/MK3/README.md` before claiming full coverage.
- `addons/` includes candidate source, not production-ready code. Seven learning domains are only inventoried in `learning/curricula.json`.
- Preserve Odoo 19 origin, each `UPSTREAM.md`, and notices. Do not transplant files with unclear license.
- No conflict-inducing duplicate `_name` models. No replacing `web/static/src/main.js` without compatibility evidence.
- Never claim a test executed without logs. The MK3 delivery explicitly prohibits testing.
- Avoid edits to `personal_knowledge` and source GitHub repositories.

## Imported Rally source boundary

- `external/rally/` contains 94 ordinary versioned files copied from the Rally source commit `b4726668b7a88d1c1cd58ed80c04c1d48d120482`; it is no longer a submodule.
- Never modify or delete the external `em3rc0dTh/Rally` repository as a side effect of `odoo-engineering` work.
- Keep the imported snapshot byte-identical unless an independently planned local adaptation is explicitly required; record divergence and new tests. For synchronized updates, re-import from a pinned upstream commit and re-verify blob SHA + mode for all files.
- Read `research/integrations/rally/README.md` and `feature-decisions.md` before planning integration; Rally is a standalone operational-assurance service, not an Odoo ERP replacement or addon.
- The owner states they own both repositories, but commercial third-party/employee/customer rights and product-brand restrictions must still be reviewed before external redistribution.
- No claims of production certification, actual customer integration, SUNAT validity or Odoo addon runtime tests without reproducible evidence.
