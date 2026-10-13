from odoo import models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_open_board_wizard(self):
        self.ensure_one()
        return {
            'name': _('Add Board'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.board.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }