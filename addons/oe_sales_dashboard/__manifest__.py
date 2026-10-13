{
    "name": "OE Sales Dashboard (OWL)",
    "version": "19.0.0.1.0",
    "summary": "Odoo-native OWL sales dashboard; no fabricated products",
    "license": "LGPL-3",
    "author": "Em3rc0d (independent reimplementation)",
    "depends": ["sale", "web"],
    "data": ["views/actions.xml"],
    "assets": {"web.assets_backend": [
        "oe_sales_dashboard/static/src/dashboard.js",
        "oe_sales_dashboard/static/src/dashboard.xml",
        "oe_sales_dashboard/static/src/dashboard.scss",
    ]},
    "installable": True,
    "application": False,
}
