"""Read-only database smoke check; executed by Odoo shell in disposable lab."""
if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("Invalid database")
company = env.company
assert company.country_id.code == "PE", "Company is not in Peru"
assert company.currency_id.name == "PEN", "Company currency is not PEN"
assert company.chart_template == "pe", "Peru chart not active"
installed = env["ir.module.module"].sudo().search([
    ("name", "in", ["account", "stock", "point_of_sale", "l10n_pe",
                   "l10n_pe_pos", "oe_pe_cpe_lab"])
])
assert len(installed) == 6 and all(m.state == "installed" for m in installed), (
    "Missing Odoo demo modules: %s" % [(m.name, m.state) for m in installed]
)
cfg = env["pos.config"].sudo().search([
    ("name", "=", "Caja DEMO - Retail Peru"), ("company_id", "=", company.id)
], limit=1)
assert cfg, "Missing demo POS"
assert cfg.payment_method_ids.filtered("is_cash_count"), "No cash method"
assert cfg.payment_method_ids.filtered(
    lambda x: x.name == "Yape / Plin - REGISTRO MANUAL"
), "Missing manual bank method"
for sku in ("DEMO-CUADERNO", "DEMO-LAPICERO", "DEMO-MOCHILA"):
    product = env["product.product"].sudo().search([("default_code", "=", sku)], limit=1)
    assert product and product.available_in_pos, "Missing POS product: " + sku
    assert product.taxes_id.filtered(lambda t: t.amount == 18), "IGV 18%% missing: " + sku
assert env["oe.pe.lab.document"].sudo().search_count([]) == 0, (
    "Fresh demo has fiscal simulation records; never treat them as real CPEs"
)
print("DEMO_CHECK_OK company=%s config=%s currency=PEN tax=18%% modules=6 stock_products=3 fiscal=SIMULATED_ONLY" % (
    company.id, cfg.id,
))
