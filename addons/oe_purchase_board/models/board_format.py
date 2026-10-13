from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OeBoardFormat(models.Model):
    _name = "oe.board.format"
    _description = "Board dimensions for purchase area"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    width_mm = fields.Float(string="Width (mm)", required=True)
    height_mm = fields.Float(string="Height (mm)", required=True)
    area_m2 = fields.Float(string="Area (m²)", compute="_compute_area_m2", store=True)

    @api.depends("width_mm", "height_mm")
    def _compute_area_m2(self):
        for rec in self:
            rec.area_m2 = (rec.width_mm * rec.height_mm) / 1000000.0

    @api.constrains("width_mm", "height_mm")
    def _check_dimensions(self):
        for rec in self:
            if rec.width_mm <= 0 or rec.height_mm <= 0:
                raise ValidationError(_("Both dimensions must be positive."))
