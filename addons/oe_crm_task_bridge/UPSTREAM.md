# Lineage

- Licensed upstream feature source: https://github.com/JoseCarlosLuque/odoo_19_addons/tree/f183143cc131de47299ffc79136da4b1a18ede81/cd_custom_task (LGPL-3 manifest).
- Existing `oe_sale_task_bridge` covers sale orders. This independent, namespaced addon covers CRM leads to **avoid duplicating** sale task fields and views.
- No new ACL grants over core `crm.lead` or `project.task`; it relies on standard model rights and groups.
- **UNTESTED** Odoo 19. Custom lead/task relational security and UI inheritance require validation before any deployment.
