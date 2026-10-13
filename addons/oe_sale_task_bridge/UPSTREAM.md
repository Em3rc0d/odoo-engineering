# Provenance and LGPL-3 obligations

**Original concept and adapted component:** [JoseCarlosLuque/odoo_opencode/sale_task_creator](https://github.com/JoseCarlosLuque/odoo_opencode/tree/9b3a89326c790d7987550d529b04bdeb9d684f56/sale_task_creator), snapshot `9b3a89326c790d7987550d529b04bdeb9d684f56`, manifest declares `LGPL-3`. Maintainer/source attribution: JoseCarlosLuque; upstream manifest lists "Your Company" as its author, so actual ownership needs confirmation.

**Modifications by Odoo Engineering (2026-10-13):** changed field namespace, added inverse field to `project.task`, corrected `_read_group` tuple semantics for Odoo 19, added a wizard requiring an active project, guarded operation on confirmed sale order, removed third-party ACLs broadening native Odoo records, simplified form extension, and introduced tests. This is a **modified derivative**, not identical source nor verified runtime substitute.

The modified addon declares `LGPL-3` and contains the LGPL-3 text in `COPYING.LGPL-3`. Original upstream attribution and all modification notes must be retained in downstream redistribution. Do not imply upstream endorsement. **License on the manifest is evidence of a grant claimed by the project, not proof of every contribution's authorship**.

**Test status:** source-level compilation/XML/static checks only pending; installation and TransactionCase tests require Odoo 19 with `sale` and `project`.
