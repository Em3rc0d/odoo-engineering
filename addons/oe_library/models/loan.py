from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LibraryLoan(models.Model):
    _name = "oe.library.loan"
    _description = "Physical Book Loan"
    _order = "loan_date desc, id desc"

    copy_id = fields.Many2one("oe.library.copy", required=True, index=True, ondelete="restrict")
    borrower_id = fields.Many2one("res.partner", required=True, index=True, ondelete="restrict")
    loan_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.context_today(self), days=14),
        required=True,
    )
    return_date = fields.Date(readonly=True, copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("active", "On Loan"), ("returned", "Returned"), ("cancelled", "Cancelled")],
        required=True,
        default="draft",
        index=True,
        copy=False,
    )
    is_overdue = fields.Boolean(compute="_compute_overdue", string="Overdue")

    @api.depends("due_date", "state")
    def _compute_overdue(self):
        # Intentionally non-stored: calendar-day changes have no @api.depends trigger.
        today = fields.Date.context_today(self)
        for loan in self:
            loan.is_overdue = bool(loan.state == "active" and loan.due_date and loan.due_date < today)

    @api.constrains("loan_date", "due_date", "return_date")
    def _check_dates(self):
        for loan in self:
            if loan.loan_date and loan.due_date and loan.due_date < loan.loan_date:
                raise ValidationError(_("Due date cannot precede loan date."))
            if loan.loan_date and loan.return_date and loan.return_date < loan.loan_date:
                raise ValidationError(_("Return date cannot precede loan date."))

    def init(self):
        # PostgreSQL enforces one active loan per physical copy across transactions.
        self.env.cr.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS oe_library_one_active_loan_per_copy "
            "ON oe_library_loan (copy_id) WHERE state = 'active'"
        )

    def action_start(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only draft loans can be started."))
        # Serialize checkout by locking the copy before checking availability.
        self.env.cr.execute("SELECT id FROM oe_library_copy WHERE id = %s FOR UPDATE", (self.copy_id.id,))
        if self.copy_id.condition != "ready":
            raise UserError(_("This physical copy is not ready to lend."))
        if self.search_count([
            ("copy_id", "=", self.copy_id.id),
            ("state", "=", "active"),
            ("id", "!=", self.id),
        ]):
            raise UserError(_("Another active loan already uses this copy."))
        self.write({"state": "active"})
        return True

    def action_return(self):
        self.ensure_one()
        if self.state != "active":
            raise UserError(_("Only active loans can be returned."))
        self.write({"state": "returned", "return_date": fields.Date.context_today(self)})
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only draft loans can be cancelled."))
        self.write({"state": "cancelled"})
        return True
