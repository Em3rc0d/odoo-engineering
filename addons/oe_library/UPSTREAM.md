# Baselines and independent redesign

- **Licensed educational inspiration:** [JoseCarlosLuque/odoo_practices/cd_library_practices](https://github.com/JoseCarlosLuque/odoo_practices/tree/f2058b2ffac379332868fa1429d790468fe6f20e/cd_library_practices), manifest LGPL-3. Its original 35 incomplete exercises were **not** imported.
- **Functional benchmark only (no copying):** [JoseCarlosLuque/Pruebas_Odoo/biblioteca_proyecto](https://github.com/JoseCarlosLuque/Pruebas_Odoo/tree/8460c6fcf372806886f7505220e192886c4b59da/biblioteca_proyecto). Root license and addon-level grant were **not identified**. We reproduce generic domain requirements (books, borrowers, loans) with independent implementation rather than redistributing its source.

## Changes compared with baseline feature set

- Physical `book -> copy -> loan` inventory rather than mutating a book's single borrowed state.
- Use standard `res.partner` without duplicating personally identifying membership records.
- DB partial unique index for **maximum one active loan per physical copy**, plus serialized checkout and early business error.
- Non-stored overdue computes from the actual current day; no stale stored boolean or email-spamming cron.
- No chatter/mail dependency, no fake demo records on normal installation.
- Conservative ACL: internal users can read, Odoo administrators can manage. Custom librarian groups/record rules deferred until role matrix is approved.
- Unit test suite for state transitions and edge cases.

**Scope limitation:** this is a minimal pilot addon, not a library-management product; no reservations, renewals, fines, circulation policy, catalog integration or email alerts. Confirm runtime behavior on Odoo 19 before claiming compatibility.

This authored module is distributed under LGPL-3; license text at `COPYING.LGPL-3`. Source references remain credited; no endorsement implied.
