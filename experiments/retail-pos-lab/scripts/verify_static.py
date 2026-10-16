#!/usr/bin/env python3
"""Dependency-free source/structure guard for the retail POS lab.

This is NOT an Odoo runtime/install test; see CI and the manual runbook.
"""
import ast
import csv
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "local-addons" / "oe_pe_cpe_lab"


def main():
    assert (ROOT / "compose.yaml").exists(), "Compose missing"
    manifest = ast.literal_eval((ADDON / "__manifest__.py").read_text())
    assert manifest["installable"] is True
    assert "account" in manifest["depends"] and "l10n_pe" in manifest["depends"]
    for file in manifest["data"]:
        path = ADDON / file
        assert path.is_file(), f"Missing manifest resource: {file}"
        if file.endswith(".xml"):
            tree = ET.parse(path)
            assert tree.getroot().tag == "odoo", f"Invalid Odoo XML root in {file}"
    for path in (ADDON / "__init__.py", *ADDON.rglob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
    for path in (ROOT.parents[1] / "integrations/sunat/nubefact_gateway").glob("*.py"):
        ast.parse(path.read_text(), filename=str(path))
    acl = ADDON / "security" / "ir.model.access.csv"
    with acl.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows and all(row["model_id:id"] == "model_oe_pe_lab_document" for row in rows)
    assert all(row["perm_unlink"] == "0" for row in rows)
    move = (ADDON / "models" / "account_move.py").read_text()
    assert "prepare_standard_sale" in move
    assert "FOR UPDATE" in move
    assert "Simulation" in move or "SIMUL" in move
    assert "requests.post(" not in move
    assert "NubefactGateway(" not in move
    assert "PYTHONPATH: /opt/retail-sunat-integration" in (ROOT / "compose.yaml").read_text()
    assert "/mnt/extra-addons:ro" in (ROOT / "compose.yaml").read_text()
    print("PASS: addon Python + XML + manifest + ACL + offline-only mapping and mounts. NOT Odoo runtime.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, SyntaxError, ValueError, ET.ParseError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
