from odoo import fields, models


class LibraryCopy(models.Model):
    _name = "oe.library.copy"
    _description = "Physical Library Copy"
    _rec_name = "code"
    _order = "code, id"

    book_id = fields.Many2one("oe.library.book", required=True, ondelete="restrict", index=True)
    code = fields.Char(required=True, copy=False, index=True)
    condition = fields.Selection(
        [("ready", "Ready"), ("repair", "In Repair"), ("retired", "Retired")],
        required=True,
        default="ready",
    )
    loan_ids = fields.One2many("oe.library.loan", "copy_id", string="Loan History")

    def init(self):
        # Database-level invariant. Python uniqueness checks alone race.
        self.env.cr.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS oe_library_copy_code_uniq "
            "ON oe_library_copy (code)"
        )
