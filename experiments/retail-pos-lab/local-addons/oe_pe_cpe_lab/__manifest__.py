{
    "name": "Peru CPE - Local Simulator (NO SUNAT)",
    "version": "19.0.1.0.0",
    "summary": "Local facturas/boletas simulation from posted Odoo invoices; never transmits to SUNAT",
    "category": "Accounting/Localizations",
    "license": "LGPL-3",
    "author": "Em3rc0d",
    "depends": ["account", "l10n_pe"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/cpe_document_views.xml",
    ],
    "application": False,
    "installable": True,
}
