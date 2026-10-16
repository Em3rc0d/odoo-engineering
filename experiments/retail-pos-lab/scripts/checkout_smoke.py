"""Rollback-only Odoo 19 ORM POS checkout smoke. NO actual CPE or external payments.

Runs on disposable retail_peru_lab DB; creates a transaction-bound opened
session, paid sale, stock movement, cash close, and rolls everything back.
"""
from odoo import Command

if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("Refusing non-demo database")
company = env.company
config = env["pos.config"].sudo().search([
    ("company_id", "=", company.id),
    ("name", "=", "Caja DEMO - Retail Peru"),
], limit=1)
if not config:
    raise RuntimeError("Run seed-demo first")
config._check_before_creating_new_session()
if config.current_session_id:
    raise RuntimeError("Close existing POS session before running checkout smoke")
product = env["product.product"].sudo().search([
    ("default_code", "=", "DEMO-CUADERNO"),
], limit=1)
if not product or not product.is_storable:
    raise RuntimeError("Missing storable demo product")
cash = config.payment_method_ids.filtered("is_cash_count")[:1]
if not cash:
    raise RuntimeError("Cash payment method missing")
stock_before = product.qty_available
if stock_before < 2:
    raise RuntimeError("Not enough stock for checkout smoke")
try:
    session = env["pos.session"].sudo().create({
        "user_id": env.ref("base.user_admin").id,
        "config_id": config.id,
    })
    session.set_opening_control(100, "ORM smoke - rollback")
    if session.state != "opened":
        raise RuntimeError("Session did not open")
    order = env["pos.order"].sudo().create({
        "session_id": session.id,
        "company_id": company.id,
        "amount_total": 0.0,
        "amount_paid": 0.0,
        "amount_tax": 0.0,
        "amount_return": 0.0,
        "lines": [Command.create({
            "product_id": product.id,
            "qty": 1,
            "price_unit": product.lst_price,
            "tax_ids": [Command.set(product.taxes_id.ids)],
            "price_subtotal": product.lst_price,
            "price_subtotal_incl": 0.0,
        })],
    })
    order.lines._onchange_amount_line_all()
    order._compute_prices()
    if not order.amount_total > 0:
        raise AssertionError("Sale total is invalid")
    context = {"active_id": order.id, "active_ids": order.ids}
    payment = env["pos.make.payment"].sudo().with_context(**context).create({
        "amount": order.amount_total,
        "payment_method_id": cash.id,
    })
    payment.with_context(**context).check()
    if order.state not in ("paid", "done") or abs(order.amount_paid - order.amount_total) > 0.001:
        raise AssertionError("POS sale/payment did not settle")
    counted = session.cash_register_balance_start + order.amount_total
    if session.cash_control:
        result = session.post_closing_cash_details(counted)
        if result.get("successful") is False:
            raise RuntimeError("Cash count failed: " + str(result))
    result = session.close_session_from_ui()
    if not result.get("successful") or session.state != "closed":
        raise AssertionError("Cash closing failed: " + str(result))
    product.invalidate_recordset(["qty_available"])
    stock_after = product.qty_available
    if stock_after > stock_before - 0.5:
        raise AssertionError("Stock not reduced after paid sale/closing: %s => %s" % (
            stock_before, stock_after))
    print("CHECKOUT_SMOKE_OK opened=1 paid_sale=1 cash_closed=1 stock_before=%s stock_after=%s real_sunat=NO" % (
        stock_before, stock_after))
finally:
    # This smoke MUST NEVER consume demo stock or generate a persistent order.
    env.cr.rollback()
