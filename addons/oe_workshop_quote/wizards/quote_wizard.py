from odoo import fields, models, _
from odoo.exceptions import UserError


class WorkshopQuoteWizard(models.TransientModel):
    _name = "oe.workshop.quote.wizard"
    _description = "Dimension-based quotation line"

    order_id = fields.Many2one("sale.order", required=True, readonly=True)
    product_id = fields.Many2one("product.product", required=True, domain=[("sale_ok", "=", True)])
    width_mm = fields.Float(required=True)
    height_mm = fields.Float(required=True)
    pieces = fields.Integer(default=1, required=True)
    price_per_m2 = fields.Monetary(required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", related="order_id.currency_id", readonly=True)

    def action_add_line(self):
        self.ensure_one()
        if self.order_id.state not in ("draft", "sent"):
            raise UserError(_("Only draft quotations can be edited."))
        if min(self.width_mm, self.height_mm, self.pieces, self.price_per_m2) <= 0:
            raise UserError(_("Dimensions, pieces and price must be positive."))
        sqm = self.env.ref("uom.product_uom_square_meter")
        uom = self.product_id.uom_id
        if uom.category_id != sqm.category_id:
            raise UserError(_("Select a product measured in area units."))
        total_m2 = (self.width_mm * self.height_mm / 1000000.0) * self.pieces
        self.env["sale.order.line"].create({
            "order_id": self.order_id.id, "product_id": self.product_id.id,
            "name": "%s — %.0f×%.0f mm × %d" % (self.product_id.display_name, self.width_mm, self.height_mm, self.pieces),
            "product_uom_qty": sqm._compute_quantity(total_m2, uom),
            "product_uom_id": uom.id,
            "price_unit": self.price_per_m2 * uom._compute_quantity(1.0, sqm),
        })
        return {"type": "ir.actions.act_window_close"}
