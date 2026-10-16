# MK4 — Rally full source import (2026-10-16)

- Imported **94/94 tracked Rally files physically**, as ordinary files in `external/rally/`, from source commit `b4726668b7a88d1c1cd58ed80c04c1d48d120482`.
- Compared original vs target: **all paths, Git blob SHAs and executable modes match exactly**. Zero missing or unexpected Rally files.
- Removed the previous Git submodule entry and `.gitmodules`; a standard clone of `odoo-engineering` contains all imported Rally files without the original repository's availability.
- Did **not** modify `em3rc0dTh/Rally` or delete any source file. The original Git history remains in its own repository and is not imported here.
- All 22 documented functional authority decisions remain: Odoo ERP for retail/fiscal transactions; Rally for independent custody, evidence, work-order assurance and reconciliation.
- Existing Rally CI evidence applies to the source commit. No full combined-repo runtime or live Odoo/SUNAT/Traccar/RFID tests were performed as part of the import.
- Next gate: commercial reuse rights for third-party materials, Odoo 19 install/ACL/stock/POS tests, separation of Odoo customer databases and filestores, recovery drills, SUNAT provider validation and first paid pilot.

See: [source-manifest.json](source-manifest.json) · [feature-decisions.md](feature-decisions.md) · [README.md](README.md).
