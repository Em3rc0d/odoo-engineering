{
    "name": "Odoo Engineering - Library Lending",
    "summary": "Track physical book copies and enforce one active loan per copy",
    "version": "19.0.0.2.0",
    "category": "Services",
    "author": "Odoo Engineering contributors",
    "website": "https://github.com/Em3rc0d/odoo-engineering",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/library_views.xml",
    ],
    "demo": ["demo/library_demo.xml"],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
