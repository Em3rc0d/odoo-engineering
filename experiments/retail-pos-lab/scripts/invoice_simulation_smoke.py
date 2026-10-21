"""Rollback-only posted accounting invoice -> local CPE simulator smoke.

NO SUNAT / OSE / PSE / external provider calls, no actual CDR, no legal invoice.
Uses only synthetic numbers in the ephemeral Odoo retail_peru_lab database.
"""
from odoo import Command, fields
from odoo.exceptions import UserError

if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("Refusing invoice simulation outside isolated retail_peru_lab")
company = env.company.sudo()
if company.country_id.code != "PE" or company.currency_id.name != "PEN":
    raise RuntimeError("Demo company must be configured PE/PEN")
if not env.user.has_group("account.group_account_invoice"):
    raise RuntimeError("Odoo shell user lacks invoice simulator permissions")

# Fully fictitious, checksum-shaped identities used only within a transaction
# that is always rolled back. NEVER attach issuer credentials to this test.
SYNTHETIC_ISSUER = "20123456786"
SYNTHETIC_BUYER = "20987654326"
product = env["product.product"].sudo().search([
    ("default_code", "=", "DEMO-MOCHILA"), ("company_id", "=", company.id),
], limit=1)
if not product:
    raise RuntimeError("Missing seeded DEMO-MOCHILA fixture")
taxes = env["account.tax"].sudo().search([
    ("company_id", "=", company.id), ("type_tax_use", "=", "sale"),
    ("amount_type", "=", "percent"), ("amount", "=", 18),
])
tax = taxes.filtered(lambda x: not x.price_include)[:1]
if not tax:
    raise RuntimeError("Missing excluded IGV 18% demo tax")
journal = env["account.journal"].sudo().search([
    ("company_id", "=", company.id), ("type", "=", "sale"),
], limit=1)
if not journal:
    raise RuntimeError("Missing demo sales journal")
before_docs = env["oe.pe.lab.document"].sudo().search_count([])
try:
    company.write({"vat": SYNTHETIC_ISSUER})
    partner = env["res.partner"].sudo().create({
        "name": "CLIENTE SIMULADO — NUNCA SUNAT",
        "country_id": company.country_id.id,
        "vat": SYNTHETIC_BUYER,
    })

    def new_posted_invoice(number, scenario):
        invoice = env["account.move"].sudo().create({
            "move_type": "out_invoice",
            "company_id": company.id,
            "journal_id": journal.id,
            "partner_id": partner.id,
            "invoice_date": fields.Date.context_today(env.user),
            "oe_pe_lab_kind": "01",
            "oe_pe_lab_series": "F001",
            "oe_pe_lab_number": number,
            "oe_pe_lab_scenario": scenario,
            "invoice_line_ids": [Command.create({
                "name": "Mochila de demostración",
                "product_id": product.id,
                "quantity": 2,
                "price_unit": 50.0,
                "tax_ids": [Command.set(tax.ids)],
            })],
        })
        invoice.action_post()
        assert invoice.state == "posted", "Accounting invoice did not post"
        assert abs(invoice.amount_total - 118.0) < 0.001, "Unexpected taxed total"
        return invoice

    accepted = new_posted_invoice(9001, "accepted")
    accepted.action_oe_pe_lab_send()
    adoc = accepted.oe_pe_lab_document_ids
    assert len(adoc) == 1 and adoc.state == "accepted_simulated"
    assert adoc.attempt_count == 1 and adoc.identity_key.endswith(":01:F001:9001")
    try:
        accepted.action_oe_pe_lab_send()
    except UserError:
        pass
    else:
        raise AssertionError("Double submit did not fail closed")
    assert len(accepted.oe_pe_lab_document_ids) == 1, "Duplicate created record"

    uncertain = new_posted_invoice(9002, "timeout")
    uncertain.action_oe_pe_lab_send()
    udoc = uncertain.oe_pe_lab_document_ids
    assert udoc.state == "uncertain_simulated" and udoc.attempt_count == 1
    uncertain.action_oe_pe_lab_check()
    assert udoc.state == "uncertain_simulated", "Timeout check must preserve UNKNOWN"
    uncertain.write({"oe_pe_lab_scenario": "accepted"})
    uncertain.action_oe_pe_lab_check()
    assert udoc.state == "accepted_simulated", "Mock status lookup not resolved"
    assert udoc.attempt_count == 1, "Re-check must not increment submission"
    assert len(uncertain.oe_pe_lab_document_ids) == 1
    assert env["oe.pe.lab.document"].sudo().search_count([]) == before_docs + 2
    print("INVOICE_SIM_SMOKE_OK posted=2 accepted_mock=1 unknown_then_checked=1 "
          "duplicate_blocked=1 real_sunat=NO rollback=YES")
finally:
    # Neither posted invoice nor test identity may survive this operation.
    env.cr.rollback()
