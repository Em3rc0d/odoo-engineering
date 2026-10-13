# New wizard: selection of a real project instead of detached project tasks.
from odoo import fields, models, _
from odoo.exceptions import UserError


class SaleTaskWizard(models.TransientModel):
    _name = "oe.sale.task.wizard"
    _description = "Create Task from Confirmed Sale"

    sale_order_id = fields.Many2one("sale.order", required=True, readonly=True)
    project_id = fields.Many2one("project.project", required=True)
    name = fields.Char(required=True)

    def action_create_task(self):
        self.ensure_one()
        order = self.sale_order_id
        if not order or order.state != "sale":
            raise UserError(_("A confirmed sale order is required."))
        order.check_access("write")
        Task = self.env["project.task"]
        Task.check_access("create")
        if not self.project_id.active:
            raise UserError(_("Choose an active project."))
        task = Task.create({
            "name": self.name,
            "project_id": self.project_id.id,
            "oe_sale_order_id": order.id,
        })
        return {
            "type": "ir.actions.act_window",
            "name": _("Project Task"),
            "res_model": "project.task",
            "res_id": task.id,
            "view_mode": "form",
            "target": "current",
        }
