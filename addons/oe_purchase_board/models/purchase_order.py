from odoo import models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_oe_open_board_wizard(self):
        self.ensure_one()
        if self.state not in ("draft", "sent"):
            raise UserError(_("Add board lines only to unconfirmed purchase orders."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Board by Area"),
            "res_model": "oe.purchase.board.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_order_id": self.id},
        }
