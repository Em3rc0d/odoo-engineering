"""Safe local Odoo→Nubefact JSON candidate→simulator path.

Uses the standalone contract implementation mounted by the Docker lab.
Does not send or certify electronic tax documents. The simulator is local
and its results MUST NEVER be passed off as real CDR acceptance.
"""
from decimal import Decimal, ROUND_HALF_UP
import json
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from nubefact_gateway import CPEIdentity, prepare_standard_sale


_CENT = Decimal("0.01")


def _cents(value):
    return Decimal(str(value)).quantize(_CENT, rounding=ROUND_HALF_UP)


class AccountMove(models.Model):
    _inherit = "account.move"

    oe_pe_lab_kind = fields.Selection(
        [("01", "Factura (01)"), ("03", "Boleta (03)")],
        string="Tipo CPE (solo simulador)", default="01", copy=False,
    )
    oe_pe_lab_series = fields.Char(string="Serie de prueba F001/B001", copy=False)
    oe_pe_lab_number = fields.Integer(string="Correlativo de prueba", copy=False)
    oe_pe_lab_scenario = fields.Selection(
        [
            ("accepted", "Aceptado por simulador"),
            ("rejected", "Rechazado por simulador"),
            ("timeout", "Comunicación incierta simulada"),
        ],
        default="accepted",
        string="Respuesta del simulador", copy=False,
    )
    oe_pe_lab_document_ids = fields.One2many(
        "oe.pe.lab.document", "move_id", string="Evidencia de simulación", readonly=True,
    )
    oe_pe_lab_state = fields.Selection(
        [
            ("not_submitted", "No enviado al simulador"),
            ("accepted_simulated", "Aceptado (SIMULADO)"),
            ("rejected_simulated", "Rechazado (SIMULADO)"),
            ("uncertain_simulated", "Resultado incierto (SIMULADO)"),
        ],
        compute="_compute_oe_pe_lab_state",
        string="Estado LOCAL (no SUNAT)",
    )

    @api.depends("oe_pe_lab_document_ids.state")
    def _compute_oe_pe_lab_state(self):
        for move in self:
            doc = move.oe_pe_lab_document_ids[:1]
            move.oe_pe_lab_state = doc.state if doc else "not_submitted"

    def write(self, vals):
        protected = {"oe_pe_lab_kind", "oe_pe_lab_series", "oe_pe_lab_number"}
        if protected.intersection(vals):
            for move in self:
                if move.oe_pe_lab_document_ids:
                    raise UserError(_("Cannot change a CPE simulator identity after its first submission."))
        return super().write(vals)

    def _oe_pe_lab_require_rights(self):
        self.ensure_one()
        if not self.env.user.has_group("account.group_account_invoice"):
            raise UserError(_("Only authorized accounting users may run the CPE simulator."))
        if self.move_type != "out_invoice" or self.state != "posted":
            raise UserError(_("Post a customer invoice first; draft or credit notes cannot be simulated."))
        if self.company_id != self.env.company and self.company_id not in self.env.companies:
            raise UserError(_("Invoice company not allowed for this user."))

    def _oe_pe_lab_prepare(self):
        self._oe_pe_lab_require_rights()
        company = self.company_id
        ruc = re.sub(r"\s", "", company.vat or "")
        buyer = self.partner_id.commercial_partner_id
        customer_doc = re.sub(r"\s", "", buyer.vat or "")
        if not re.fullmatch(r"[0-9]{8}|[0-9]{11}", customer_doc):
            raise UserError(_("Customer must have an 8-digit DNI or 11-digit RUC in its VAT field."))
        if not re.fullmatch(r"[0-9]{11}", ruc):
            raise UserError(_("Company must have an 11-digit RUC in the VAT field."))
        if not self.invoice_date:
            raise UserError(_("Invoice date is required."))
        if self.currency_id.name != "PEN":
            raise UserError(_("Only PEN is supported by this demonstration."))
        if not self.oe_pe_lab_series or self.oe_pe_lab_number < 1:
            raise UserError(_("Choose a test series and a positive document number."))
        try:
            identity = CPEIdentity(
                issuer_ruc=ruc, kind=self.oe_pe_lab_kind,
                series=self.oe_pe_lab_series.upper().strip(),
                number=self.oe_pe_lab_number,
            )
        except ValueError as exc:
            raise UserError(_("Invalid simulator document type/series/number: %s") % str(exc)) from exc

        lines = self.invoice_line_ids.filtered(lambda ln: ln.display_type in (False, "product"))
        if not lines:
            raise UserError(_("At least one taxable product line is required."))
        items = []
        for line in lines:
            if line.discount:
                raise UserError(_("Discount lines are not yet supported by the local CPE simulator."))
            if len(line.tax_ids) != 1 or line.tax_ids[0].amount_type != "percent" or line.tax_ids[0].amount != 18:
                raise UserError(_("Each line must have exactly one percentage 18%% IGV tax."))
            if line.quantity < 1 or line.quantity != int(line.quantity):
                raise UserError(_("The simulator supports only positive whole-unit quantities."))
            unit_net = _cents(line.price_unit)
            quantity = int(line.quantity)
            if unit_net <= 0 or _cents(line.price_subtotal) != _cents(unit_net * quantity):
                raise UserError(_("Use 18%% IGV excluded unit prices without special rounding or discounts."))
            items.append({
                "sku": line.product_id.default_code or "",
                "description": line.name or line.product_id.display_name,
                "quantity": quantity,
                "unit_net": str(unit_net),
            })
        sale = {
            "currency": "PEN",
            "tax_profile": "pe_igv_18_taxable",
            "issue_date": fields.Date.to_string(self.invoice_date),
            "buyer_doc_kind": "6" if len(customer_doc) == 11 else "1",
            "buyer_doc_number": customer_doc,
            "buyer_name": buyer.name,
            "buyer_address": buyer.contact_address or "",
            "items": items,
            "odoo_total": str(_cents(self.amount_total)),
        }
        if _cents(self.amount_tax) != _cents(_cents(self.amount_untaxed) * Decimal("0.18")):
            raise UserError(_("Invoice IGV total is outside the simulator's restricted tax regime."))
        try:
            return prepare_standard_sale(identity, sale)
        except ValueError as exc:
            # Do not display raw taxpayer payload to unauthorized operators.
            raise UserError(_("Invoice not eligible for the restricted CPE simulator: %s") % str(exc)) from exc

    def _oe_pe_lab_response(self, scenario):
        # Mock only. Names deliberately marked SIMULATED; no CDR/PDF/XML generated.
        if scenario == "accepted":
            return ("accepted_simulated", {"simulated": True, "provider": "LOCAL_ONLY",
                    "aceptada_por_sunat": True, "sunat_responsecode": "SIM-0"})
        if scenario == "rejected":
            return ("rejected_simulated", {"simulated": True, "provider": "LOCAL_ONLY",
                    "aceptada_por_sunat": False, "sunat_responsecode": "SIM-REJECT"})
        return ("uncertain_simulated", {"simulated": True, "provider": "LOCAL_ONLY",
                "status": "unknown", "message": "Simulated timeout. Do not resubmit."})

    def action_oe_pe_lab_send(self):
        self.ensure_one()
        self._oe_pe_lab_require_rights()
        # Serialize within a move to stop parallel attempts with same source key.
        self.env.cr.execute("SELECT id FROM account_move WHERE id = %s FOR UPDATE", (self.id,))
        docs = self.env["oe.pe.lab.document"].search([("move_id", "=", self.id)], limit=1)
        if docs:
            raise UserError(_("Already simulated for this invoice. Check its existing status; never emit twice."))
        prepared = self._oe_pe_lab_prepare()
        state, reply = self._oe_pe_lab_response(self.oe_pe_lab_scenario)
        self.env["oe.pe.lab.document"].create({
            "move_id": self.id, "company_id": self.company_id.id,
            "identity_key": prepared.identity.key, "payload_sha256": prepared.sha256,
            "payload_json": json.dumps(prepared.payload, ensure_ascii=False, sort_keys=True),
            "simulated_response": json.dumps(reply, sort_keys=True),
            "state": state, "attempt_count": 1,
            "last_checked_at": fields.Datetime.now(),
            "last_actor_id": self.env.user.id,
        })
        return {"type": "ir.actions.client", "tag": "reload"}

    def action_oe_pe_lab_check(self):
        """Resolve uncertain SIMULATED status by local lookup; never resend the CPE."""
        self.ensure_one()
        self._oe_pe_lab_require_rights()
        self.env.cr.execute("SELECT id FROM account_move WHERE id = %s FOR UPDATE", (self.id,))
        doc = self.env["oe.pe.lab.document"].search([("move_id", "=", self.id)], limit=1)
        if not doc or doc.state != "uncertain_simulated":
            raise UserError(_("Only uncertain simulated documents can be checked."))
        if self.oe_pe_lab_scenario != "timeout":
            state, reply = self._oe_pe_lab_response(self.oe_pe_lab_scenario)
            doc.write({
                "state": state,
                "simulated_response": json.dumps(reply, sort_keys=True),
                "last_checked_at": fields.Datetime.now(),
                "last_actor_id": self.env.user.id,
            })
        else:
            doc.write({"last_checked_at": fields.Datetime.now()})
        return {"type": "ir.actions.client", "tag": "reload"}
