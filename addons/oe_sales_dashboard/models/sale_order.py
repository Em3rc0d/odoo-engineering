from collections import defaultdict
from odoo import api, models, _
from odoo.exceptions import AccessError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def oe_dashboard_metrics(self):
        if not self.env.user.has_group("sales_team.group_sale_salesman"):
            raise AccessError(_("You need sales access to view this dashboard."))
        # Bounded preview; never misleadingly label as lifetime revenue.
        orders = self.search([("state", "in", ["sale", "done"])], order="date_order desc, id desc", limit=500)
        currencies = defaultdict(lambda: {"count": 0, "total": 0.0})
        products = defaultdict(int)
        for order in orders:
            unit = order.currency_id.name or "?"
            currencies[unit]["count"] += 1
            currencies[unit]["total"] += order.amount_total
            for line in order.order_line:
                if line.product_id and not line.display_type:
                    products[line.product_id.display_name] += 1  # line incidence, NOT quantity/revenue
        return {
            "sample_limit": 500,
            "sample_count": len(orders),
            "metric_definition": "Most recent 500 confirmed sale orders visible to your user. Product metric counts order lines; totals are separated by currency.",
            "currency_totals": [{"currency": code, "orders": row["count"], "total": round(row["total"], 2)} for code, row in sorted(currencies.items())],
            "products": [{"name": k, "line_count": v} for k, v in sorted(products.items(), key=lambda x: (-x[1], x[0]))[:12]],
        }
