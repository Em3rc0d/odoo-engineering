# Baseline and improvements

- Source: https://github.com/JoseCarlosLuque/odoo_opencode/tree/9b3a89326c790d7987550d529b04bdeb9d684f56/purchase_board_wizard
- License declared in upstream addon manifest: LGPL-3. Attribution retained; implementation in this path is substantially rewritten.
- Baseline features: wizard, board formats, area-based purchasing.
- Adaptations: own model namespace (avoids `board.format` collision), explicit dimensions, explicit price per square metre, quantity conversion to product area UoM, versioned purchase line field and non-manager read-only formats.
- Also consolidates the surface-ordering portion of unlicensed `cd_workshop_flows` **as independently written behavior**, not copied source.
- **UNTESTED** on Odoo 19; no assurance that the module installs, handles tax or computes vendor prices automatically. Do not use for production procurement.
