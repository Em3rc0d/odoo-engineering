# Adapted from JoseCarlosLuque/odoo_opencode/sale_task_creator, LGPL-3.
# Changed: namespaced inverse, Odoo 19 tuple _read_group, guards and UI contract.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    oe_task_ids = fields.One2many(
        "project.task", "oe_sale_order_id", string="Project Tasks (OE)"
    )
    oe_task_count = fields.Integer(compute="_compute_oe_task_count", string="Project Tasks")

    @api.depends("oe_task_ids")
    def _compute_oe_task_count(self):
        count_by_order = {}
        if self.ids:
            groups = self.env["project.task"]._read_group(
                [("oe_sale_order_id", "in", self.ids)],
                ["oe_sale_order_id"],
                ["__count"],
            )
            count_by_order = {order.id: count for order, count in groups if order}
        for order in self:
            order.oe_task_count = count_by_order.get(order.id, 0)

    def action_oe_view_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Related Project Tasks"),
            "res_model": "project.task",
            "view_mode": "list,form",
            "domain": [("oe_sale_order_id", "=", self.id)],
            "context": {"default_oe_sale_order_id": self.id},
            "target": "current",
        }

    def action_oe_new_task(self):
        self.ensure_one()
        if self.state != "sale":
            raise UserError(_("Only confirmed sale orders can create project tasks."))
        self.check_access("write")
        self.env["project.task"].check_access("create")
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Project Task"),
            "res_model": "oe.sale.task.wizard",
            "view_mode": "form",
            "views": [(self.env.ref("oe_sale_task_bridge.view_oe_task_wizard_form").id, "form")],
            "target": "new",
            "context": {"default_sale_order_id": self.id},
        }
