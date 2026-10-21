"""Read-only Odoo 19 Community module inventory; cannot emit any document.

Run via `bash scripts/lab.sh probe-edi` against disposable retail_peru_lab.
Presence on filesystem != installed != licensed != enabled to emit via SUNAT.
"""
import json
from odoo.modules.module import get_module_path

if env.cr.dbname != "retail_peru_lab":
    raise RuntimeError("Refusing EDI probe outside disposable retail_peru_lab")

baseline = ("account", "point_of_sale", "stock", "l10n_pe", "l10n_pe_pos", "oe_pe_cpe_lab")
candidates = ("l10n_pe_edi", "l10n_pe_edi_base", "l10n_pe_edi_odoofact",
              "l10n_pe_edi_odoofact_pos", "l10n_pe_catalog")
names = baseline + candidates
recordset = env["ir.module.module"].sudo().search([("name", "in", list(names))])
states = {mod.name: mod.state for mod in recordset}
findings = {
    name: {
        # Do not print absolute module paths or secrets from the lab container.
        "in_configured_addons_path": bool(get_module_path(name)),
        "database_state": states.get(name, "not_listed"),
    }
    for name in names
}
for name in baseline:
    assert findings[name]["in_configured_addons_path"], "Missing baseline module: " + name
    assert findings[name]["database_state"] == "installed", "Baseline module not installed: " + name
for name in candidates:
    if findings[name]["database_state"] == "installed":
        raise AssertionError("External/EDI module unexpectedly installed in restricted demo: " + name)
print("EDI_PROBE_OK " + json.dumps(findings, sort_keys=True, ensure_ascii=True))
print("EDI_PROBE_NOTE No real issuer status, XML, credential, OSE/PSE, CDR or license verification")
