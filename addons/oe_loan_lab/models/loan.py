from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LoanLab(models.Model):
    _name = "oe.loan.lab"
    _description = "Training-only loan schedule"

    name = fields.Char(required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")
    principal = fields.Monetary(required=True, currency_field="currency_id")
    annual_interest_percent = fields.Float(default=0.0)
    term_months = fields.Integer(default=12, required=True)
    start_date = fields.Date(default=fields.Date.context_today, required=True)
    state = fields.Selection([("draft", "Draft"), ("simulated", "Simulated")], default="draft")
    line_ids = fields.One2many("oe.loan.lab.line", "loan_id")

    @api.constrains("principal", "annual_interest_percent", "term_months")
    def _check_values(self):
        for row in self:
            if row.principal <= 0 or row.annual_interest_percent < 0 or not (1 <= row.term_months <= 360):
                raise ValidationError(_("Principal must be positive, interest nonnegative, term 1..360."))

    def action_build_schedule(self):
        for loan in self:
            if loan.state != "draft":
                raise UserError(_("Reset the simulation before regenerating."))
            if loan.principal <= 0 or loan.term_months <= 0 or loan.annual_interest_percent < 0:
                raise UserError(_("Complete valid simulation inputs."))
            loan.line_ids.unlink()
            rate = loan.annual_interest_percent / 1200.0
            months = loan.term_months
            payment = (loan.principal / months if not rate else
                       loan.principal * (rate / (1 - (1 + rate) ** (-months))))
            balance = loan.principal
            for number in range(1, months + 1):
                interest = loan.currency_id.round(balance * rate)
                capital = loan.currency_id.round(payment - interest)
                if number == months:
                    capital = balance
                if capital < 0:
                    raise UserError(_("Negative principal amortization is invalid."))
                balance = max(0, loan.currency_id.round(balance - capital))
                self.env["oe.loan.lab.line"].create({
                    "loan_id": loan.id,
                    "sequence": number,
                    "due_date": fields.Date.add(loan.start_date, months=number),
                    "principal_component": capital,
                    "interest_component": interest,
                    "total_payment": capital + interest,
                    "balance_after": balance,
                })
            loan.state = "simulated"

    def action_reset(self):
        for loan in self:
            loan.line_ids.unlink()
            loan.state = "draft"


class LoanLabLine(models.Model):
    _name = "oe.loan.lab.line"
    _description = "Training amortization line"
    _order = "sequence"

    loan_id = fields.Many2one("oe.loan.lab", required=True, ondelete="cascade")
    sequence = fields.Integer(required=True)
    due_date = fields.Date(required=True)
    currency_id = fields.Many2one("res.currency", related="loan_id.currency_id")
    principal_component = fields.Monetary(currency_field="currency_id", readonly=True)
    interest_component = fields.Monetary(currency_field="currency_id", readonly=True)
    total_payment = fields.Monetary(currency_field="currency_id", readonly=True)
    balance_after = fields.Monetary(currency_field="currency_id", readonly=True)
