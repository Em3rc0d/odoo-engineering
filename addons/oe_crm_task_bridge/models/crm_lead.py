from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    oe_task_ids = fields.One2many("project.task", "oe_crm_lead_id", string="Project tasks")
    oe_task_count = fields.Integer(compute="_compute_oe_task_count")

    @api.depends("oe_task_ids")
    def _compute_oe_task_count(self):
        for lead in self:
            lead.oe_task_count = len(lead.oe_task_ids)

    def action_oe_open_tasks(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": _("Opportunity tasks"),
                "res_model": "project.task", "view_mode": "list,form",
                "domain": [("oe_crm_lead_id", "=", self.id)],
                "context": {"default_oe_crm_lead_id": self.id}}

    def action_oe_create_task(self):
        self.ensure_one()
        if not self.env.user.has_group("project.group_project_user"):
            raise UserError(_("Project user permission required."))
        return {"type": "ir.actions.act_window", "name": _("New project task"),
                "res_model": "project.task", "view_mode": "form", "target": "current",
                "context": {"default_name": self.name,
                            "default_oe_crm_lead_id": self.id,
                            "default_partner_id": self.partner_id.id or False}}
