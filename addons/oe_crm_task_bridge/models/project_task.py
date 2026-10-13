from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    oe_crm_lead_id = fields.Many2one("crm.lead", index=True, ondelete="set null", copy=False)
