"""One-transaction Odoo 19 POS order -> posted account.move -> LOCAL CPE simulator.

It creates synthetic company/customer identities, performs cash payment and a
single-accounting-invoice POS operation, then rolls back all changes. Never
contacts SUNAT, PSE/OSE, Nubefact, bank or email APIs; never generates PDF.
No other database is allowed.
"""
from odoo import Command
from odoo.exceptions import UserError

if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("Refusing non-demo database")
company = env.company.sudo()
config = env["pos.config"].sudo().search([
    ("company_id", "=", company.id), ("name", "=", "Caja DEMO - Retail Peru")
], limit=1)
if not config or config.current_session_id:
    raise RuntimeError("Requires an idle seeded demo cash register")
if not env.user.has_group("account.group_account_invoice"):
    raise RuntimeError("Odoo shell user must hold accounting invoice permissions")
product = env["product.product"].sudo().search([
    ("company_id", "=", company.id), ("default_code", "=", "DEMO-CUADERNO")
], limit=1)
cash = config.payment_method_ids.filtered("is_cash_count")[:1]
if not product or not cash or not product.is_storable:
    raise RuntimeError("Demo product, cash method or stock configuration missing")
stock_before = product.qty_available
if stock_before < 1:
    raise RuntimeError("Insufficient synthetic demo stock")

try:
    # Checksum-valid *fabricated* strings are never transmitted or persisted.
    company.write({"vat": "20123456786"})
    partner = env["res.partner"].sudo().create({
        "name": "CLIENTE FICTICIO POS — NO SUNAT",
        "country_id": company.country_id.id,
        "vat": "20987654326",
    })
    session = env["pos.session"].sudo().create({
        "user_id": env.ref("base.user_admin").id,
        "config_id": config.id,
    })
    session.set_opening_control(100, "POS/Invoice bridge smoke — rollback")
    if session.state != "opened":
        raise AssertionError("POS session not opened")
    order = env["pos.order"].sudo().create({
        "session_id": session.id,
        "company_id": company.id,
        "partner_id": partner.id,
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
        raise AssertionError("Computed POS amount must be positive")
    ctx = {"active_id": order.id, "active_ids": order.ids}
    payment = env["pos.make.payment"].sudo().with_context(**ctx).create({
        "amount": order.amount_total,
        "payment_method_id": cash.id,
    })
    payment.with_context(**ctx).check()
    if order.state not in ("paid", "done"):
        raise AssertionError("POS order was not paid")

    # The exact Odoo 19 API moves from POS to posted account.move; disable
    # auto PDF generation/send side effects, since this is just an offline lab.
    order.with_context(generate_pdf=False).action_pos_order_invoice()
    invoice = order.account_move
    if not invoice or invoice.state != "posted" or invoice.move_type != "out_invoice":
        raise AssertionError("POS order did not produce a posted customer invoice")
    if invoice.partner_id != partner:
        raise AssertionError("POS invoice lost the synthetic customer")
    invoice.write({
        "oe_pe_lab_kind": "01",
        "oe_pe_lab_series": "F001",
        "oe_pe_lab_number": 9003,
        "oe_pe_lab_scenario": "accepted",
    })
    invoice.action_oe_pe_lab_send()
    doc = invoice.oe_pe_lab_document_ids
    if len(doc) != 1 or doc.state != "accepted_simulated":
        raise AssertionError("POS-derived invoice did not reach LOCAL simulator")
    try:
        invoice.action_oe_pe_lab_send()
    except UserError:
        pass
    else:
        raise AssertionError("Second simulation should be rejected")

    # Closing the cashier shift is part of the observable accounting flow.
    counted = session.cash_register_balance_start + order.amount_total
    if session.cash_control:
        check = session.post_closing_cash_details(counted)
        if check.get("successful") is False:
            raise AssertionError("Cash count failed")
    result = session.close_session_from_ui()
    if not result.get("successful") or session.state != "closed":
        raise AssertionError("Cash session close did not succeed")
    product.invalidate_recordset(["qty_available"])
    if product.qty_available > stock_before - 0.5:
        raise AssertionError("Sale did not decrement stock")

    print("POS_INVOICE_SIM_SMOKE_OK paid_pos=1 posted_invoice=1 local_simulation=1 "
          "duplicate_rejected=1 cash_closed=1 stock_delta=-1 "
          "xml_signed=NO real_sunat=NO rollback=YES")
finally:
    env.cr.rollback()
