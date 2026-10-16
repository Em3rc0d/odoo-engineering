"""Idempotent local-only fixture for Odoo 19 Community Retail Peru lab.

Run through: odoo shell -d retail_peru_lab --no-http < scripts/seed_demo.py
No SUNAT communication, no real taxpayer data. This script refuses other DBs.
"""
from odoo import Command

if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("This fixture refuses any database other than retail_peru_lab")

company = env.company.sudo()
pe = env.ref("base.pe")
pen = env.ref("base.PEN")
pen.active = True

# Only this disposable DB is eligible for country/chart initialization.
if company.country_id != pe or company.currency_id != pen:
    company.write({
        "name": "Retail Peru - DEMOSTRACION (NO SUNAT)",
        "country_id": pe.id,
        "currency_id": pen.id,
    })
env.user.sudo().write({"tz": "America/Lima"})

# Proper journal/accounts are required to open POS and to post invoices.
if company.chart_template != "pe":
    env["account.chart.template"].sudo().try_loading("pe", company, install_demo=False)

env = env(context=dict(env.context, allowed_company_ids=[company.id]))
taxes = env["account.tax"].sudo().search([
    ("company_id", "=", company.id),
    ("type_tax_use", "=", "sale"),
    ("amount_type", "=", "percent"),
    ("amount", "=", 18),
])
# Prefer tax-excluded configuration (the restricted mock contract requires it).
tax = taxes.filtered(lambda t: not t.price_include)[:1]
if not tax:
    raise RuntimeError("IGV 18% tax-excluded not available: review Peru chart before seeding demo")

product_model = env["product.template"].sudo()
fixtures = [
    ("DEMO-CUADERNO", "Cuaderno A5 (DEMO)", 10.0, 30),
    ("DEMO-LAPICERO", "Lapicero azul (DEMO)", 2.5, 50),
    ("DEMO-MOCHILA", "Mochila escolar (DEMO)", 50.0, 12),
]
warehouse = env["stock.warehouse"].sudo().search([("company_id", "=", company.id)], limit=1)
if not warehouse:
    raise RuntimeError("No warehouse for company: install stock before fixture")
for sku, name, price, initial_qty in fixtures:
    product = product_model.search([("default_code", "=", sku)], limit=1)
    if not product:
        values = {
            "name": name, "default_code": sku, "type": "consu",
            "list_price": price, "available_in_pos": True,
            "taxes_id": [Command.set(tax.ids)],
            "company_id": company.id,
        }
        if "is_storable" in product_model._fields:
            values["is_storable"] = True
        product = product_model.create(values)
        # Seed physical stock only at first creation; never overwrite sales.
        if product.product_variant_id.is_storable:
            quant_model = env["stock.quant"].sudo().with_context(inventory_mode=True)
            quant = quant_model.create({
                "product_id": product.product_variant_id.id,
                "location_id": warehouse.lot_stock_id.id,
                "inventory_quantity": initial_qty,
            })
            quant.action_apply_inventory()
    else:
        # Do not reset prices, taxes or stock on repeated fixture runs.
        assert product.company_id == company, "Demo SKU belongs to a different company"

# Demonstration payment method: manually recorded, not bank/API verified.
bank = env["account.journal"].sudo().search([
    ("company_id", "=", company.id), ("type", "=", "bank"),
], limit=1)
if not bank:
    raise RuntimeError("Peru chart has no bank journal")
pm_model = env["pos.payment.method"].sudo()
manual_pm = pm_model.search([
    ("company_id", "=", company.id), ("name", "=", "Yape / Plin - REGISTRO MANUAL"),
], limit=1)
if not manual_pm:
    manual_pm = pm_model.create({
        "name": "Yape / Plin - REGISTRO MANUAL",
        "company_id": company.id,
        "journal_id": bank.id,
        "payment_method_type": "none",
    })
config_model = env["pos.config"].sudo()
config = config_model.search([
    ("company_id", "=", company.id),
    ("name", "=", "Caja DEMO - Retail Peru"),
], limit=1)
if not config:
    config = config_model.create({
        "name": "Caja DEMO - Retail Peru",
        "company_id": company.id,
        "receipt_header": "DEMOSTRACION. NO ES CPE VALIDO.",
        "receipt_footer": "Sin emision fiscal real. Prohibido usar con clientes.",
    })
if manual_pm not in config.payment_method_ids:
    config.write({"payment_method_ids": [Command.link(manual_pm.id)]})
if not config.payment_method_ids.filtered("is_cash_count"):
    # Odoo 19 may default to bank-only methods when another POS payment method
    # already exists. A register cannot open without an explicit cash method.
    free_cash = pm_model.search([
        ("company_id", "=", company.id),
        ("is_cash_count", "=", True),
        ("config_ids", "=", False),
    ], limit=1)
    if not free_cash:
        free_cash = config._create_cash_payment_method()
    config.write({"payment_method_ids": [Command.link(free_cash.id)]})
assert config.payment_method_ids.filtered("is_cash_count"), "Cash method creation failed"

# An illustrative purchaser to test 8-digit DNI handling in the local simulator.
partner_model = env["res.partner"].sudo()
demo_partner = partner_model.search([("name", "=", "Consumidor ficticio - DEMO")], limit=1)
if not demo_partner:
    demo_partner = partner_model.create({
        "name": "Consumidor ficticio - DEMO",
        "country_id": pe.id,
        "vat": "00000000",
    })

env.cr.commit()
print("DEMO_SEED_OK company=%s pos_config=%s products=%s payment_methods=%s" % (
    company.id, config.id, ",".join(x[0] for x in fixtures),
    ",".join(config.payment_method_ids.mapped("name")),
))
