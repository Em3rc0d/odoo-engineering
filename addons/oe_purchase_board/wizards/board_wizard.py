from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class OePurchaseBoardWizard(models.TransientModel):
    _name = "oe.purchase.board.wizard"
    _description = "Add board with explicit area and price"

    order_id = fields.Many2one("purchase.order", required=True, readonly=True)
    product_id = fields.Many2one("product.product", required=True, domain=[("purchase_ok", "=", True)])
    format_id = fields.Many2one("oe.board.format", required=True)
    pieces = fields.Integer(default=1, required=True)
    price_per_m2 = fields.Monetary(string="Purchase price per m²", required=True,
                                   currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", related="order_id.currency_id", readonly=True)

    def action_add_board(self):
        self.ensure_one()
        order = self.order_id
        if order.state not in ("draft", "sent"):
            raise UserError(_("Purchase order is no longer editable."))
        if self.pieces <= 0 or self.format_id.area_m2 <= 0:
            raise UserError(_("Choose positive dimensions and number of pieces."))
        if self.price_per_m2 <= 0:
            raise UserError(_("Provide an explicit positive supplier price per m²."))
        sqm = self.env.ref("uom.product_uom_square_meter")
        if self.product_id.uom_id.category_id != sqm.category_id:
            raise UserError(_("The product must use an area unit of measure."))
        quantity_sqm = self.format_id.area_m2 * self.pieces
        # Odoo 19 purchase.order.line uses product_uom_id, unlike older releases.
        # This line deliberately does not rely on onchange-based vendor pricing.
        self.env["purchase.order.line"].create({
            "order_id": order.id,
            "product_id": self.product_id.id,
            "name": "%s | %s | %s pcs" % (self.product_id.display_name, self.format_id.name, self.pieces),
            "product_qty": sqm._compute_quantity(quantity_sqm, self.product_id.uom_id),
            "product_uom_id": self.product_id.uom_id.id,
            "price_unit": self.price_per_m2 * (self.product_id.uom_id._compute_quantity(1.0, sqm)),
            "date_planned": fields.Datetime.now(),
        })
        return {"type": "ir.actions.act_window_close"}
