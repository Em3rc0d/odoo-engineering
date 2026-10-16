"""Source-of-truth for the LOCAL demonstration of CPE dispatch.

DO NOT reinterpret simulator statuses as real SUNAT/provider evidence.
There is no remote HTTP request, certificate, SOL credential or provider access.
"""
from odoo import fields, models


class LocalCpeDocument(models.Model):
    _name = "oe.pe.lab.document"
    _description = "CPE local simulation - never sent to SUNAT"
    _rec_name = "identity_key"
    _order = "id desc"
    _check_company_auto = True

    move_id = fields.Many2one(
        "account.move", required=True, index=True, ondelete="restrict",
        check_company=True, copy=False, readonly=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, index=True, readonly=True,
    )
    identity_key = fields.Char(required=True, index=True, readonly=True, copy=False)
    payload_sha256 = fields.Char(required=True, readonly=True, copy=False)
    payload_json = fields.Text(readonly=True, copy=False, groups="account.group_account_manager")
    simulated_response = fields.Text(readonly=True, copy=False)
    state = fields.Selection(
        [
            ("accepted_simulated", "Aceptado (SIMULADO)"),
            ("rejected_simulated", "Rechazado (SIMULADO)"),
            ("uncertain_simulated", "Resultado incierto (SIMULADO)"),
        ],
        required=True,
        readonly=True,
        index=True,
    )
    attempt_count = fields.Integer(default=1, readonly=True)
    last_checked_at = fields.Datetime(readonly=True)
    last_actor_id = fields.Many2one("res.users", readonly=True)

    _unique_move = models.Constraint(
        "UNIQUE (move_id)", "Only one CPE simulator record is allowed per Odoo invoice.",
    )
    _unique_cpe_identity = models.Constraint(
        "UNIQUE (identity_key)", "This issuer, document type, series and number was already used.",
    )
    _positive_attempts = models.Constraint(
        "CHECK (attempt_count = 1)", "Simulator may register exactly one original submission.",
    )
