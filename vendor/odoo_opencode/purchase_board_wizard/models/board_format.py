from odoo import models, fields, api


class BoardFormat(models.Model):
    _name = 'board.format'
    _description = 'Board Format'
    _order = 'product_id, name'

    name = fields.Char(string='Format Name', required=True)
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        ondelete='cascade',
        domain=[('purchase_ok', '=', True)],
    )
    area = fields.Float(
        string='Area (m²)',
        required=True,
        help='Area of a single board in square meters',
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_format_per_product', 'unique(product_id, name)',
         'Format name must be unique per product!'),
    ]

    def name_get(self):
        result = []
        for record in self:
            product_name = record.product_id.display_name if record.product_id else ''
            name = f'{product_name} - {record.name}' if product_name else record.name
            result.append((record.id, name))
        return result