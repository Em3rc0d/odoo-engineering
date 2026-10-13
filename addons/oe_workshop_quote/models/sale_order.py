from odoo import models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_oe_open_quote_wizard(self):
        self.ensure_one()
        if self.state not in ("draft", "sent"):
            raise UserError(_("Only quotations can receive new custom area lines."))
        return {"type": "ir.actions.act_window", "name": _("Custom area line"),
                "res_model": "oe.workshop.quote.wizard", "view_mode": "form", "target": "new",
                "context": {"default_order_id": self.id}}
