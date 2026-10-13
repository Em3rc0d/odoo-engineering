# Derived from the sale/task relationship in JoseCarlosLuque/sale_task_creator.
# Changes: private namespace for collision safety, independent from sale_project.
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    oe_sale_order_id = fields.Many2one(
        "sale.order",
        string="Related Sale Order (OE)",
        index=True,
        ondelete="set null",
        copy=False,
    )
