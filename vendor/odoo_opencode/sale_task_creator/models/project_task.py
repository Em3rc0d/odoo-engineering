from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        index=True,
        ondelete='set null',
        tracking=True,
    )

    def create(self, vals_list):
        tasks = super().create(vals_list)
        sale_orders = tasks.mapped('sale_order_id')
        if sale_orders:
            sale_orders.invalidate_cache(['task_count'])
        return tasks
