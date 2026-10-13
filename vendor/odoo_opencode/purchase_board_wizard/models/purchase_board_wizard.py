from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseBoardWizard(models.TransientModel):
    _name = 'purchase.board.wizard'
    _description = 'Add Board to Purchase Order'

    order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        required=True,
        ondelete='cascade',
        default=lambda self: self.env.context.get('active_id'),
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        domain=[('purchase_ok', '=', True)],
    )
    format_id = fields.Many2one(
        'board.format',
        string='Format',
        required=True,
        domain="[('product_id', '=', product_id)]",
    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
    )
    calculated_area = fields.Float(
        string='Total Area (m²)',
        compute='_compute_calculated_area',
        readonly=True,
    )

    @api.depends('format_id', 'quantity')
    def _compute_calculated_area(self):
        for wizard in self:
            wizard.calculated_area = (wizard.format_id.area or 0.0) * (wizard.quantity or 0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.format_id = False

    def action_add_line(self):
        self.ensure_one()

        # Validate product UoM is m² (square meter)
        m2_uom = self.env.ref('uom.product_uom_square_meter', raise_if_not_found=False)
        area_category = self.env.ref('uom.uom_categ_area', raise_if_not_found=False)

        if not m2_uom or not area_category:
            raise UserError(_('Area UoM category or Square Meter UoM not found in system.'))

        if self.product_id.uom_id.category_id != area_category:
            raise UserError(_(
                "Product '%s' must have an Area unit of measure (current: %s).",
                self.product_id.display_name, self.product_id.uom_id.name
            ))

        if self.product_id.uom_id != m2_uom:
            raise UserError(_(
                "Product '%s' must use 'Square Meter (m²)' as unit of measure (current: %s).",
                self.product_id.display_name, self.product_id.uom_id.name
            ))

        # Calculate total area
        total_area = self.format_id.area * self.quantity

        # Create purchase order line
        self.env['purchase.order.line'].create({
            'order_id': self.order_id.id,
            'product_id': self.product_id.id,
            'product_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'board_format_id': self.format_id.id,
            'board_area': total_area,
            'name': self._get_line_description(),
        })

        return {'type': 'ir.actions.act_window_close'}

    def _get_line_description(self):
        self.ensure_one()
        format_name = self.format_id.name or ''
        product_name = self.product_id.display_name or ''
        return f'{product_name} - {format_name} ({self.format_id.area} m² × {self.quantity})'