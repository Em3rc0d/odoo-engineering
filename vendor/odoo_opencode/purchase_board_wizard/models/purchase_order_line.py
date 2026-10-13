from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    board_format_id = fields.Many2one(
        'board.format',
        string='Board Format',
        ondelete='set null',
        help='Format of the board used to calculate area',
    )
    board_area = fields.Float(
        string='Board Area (m²)',
        digits='Product Unit of Measure',
        group_operator='sum',
        help='Total area in square meters (format area × quantity)',
    )