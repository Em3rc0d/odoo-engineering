{
    "name": "Odoo Engineering - Sales to Project Tasks",
    "summary": "Create project tasks from confirmed sales with explicit project selection",
    "version": "19.0.0.2.0",
    "category": "Sales",
    "author": "Odoo Engineering contributors; adapted from JoseCarlosLuque/sale_task_creator",
    "website": "https://github.com/Em3rc0d/odoo-engineering",
    "depends": ["sale", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/task_wizard_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
