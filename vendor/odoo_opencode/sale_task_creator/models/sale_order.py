from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='sale_order_id',
        string='Tasks',
    )

    task_count = fields.Integer(
        compute='_compute_task_count',
        string='Task Count',
    )

    @api.depends('task_ids')
    def _compute_task_count(self):
        records_data = self.env['project.task']._read_group(
            [('sale_order_id', 'in', self.ids)],
            ['sale_order_id'],
            ['sale_order_id'],
        )
        data = {r['sale_order_id'][0]: r['sale_order_id_count'] for r in records_data}
        for record in self:
            record.task_count = data.get(record.id, 0)

    def action_view_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'domain': [('sale_order_id', '=', self.id)],
            'view_mode': 'list,kanban',
            'res_model': 'project.task',
            'target': 'current',
            'context': {'default_sale_order_id': self.id},
        }

    def create_task(self):
        self.ensure_one()
        new_task = self.env['project.task'].create({
            'sale_order_id': self.id,
            'name': 'New Task',
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': new_task.id,
            'target': 'new',
            'context': {'form_view_initial_mode': 'edit'},
        }
