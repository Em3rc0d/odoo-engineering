# License review — per-module rights, not just repository root

**2026-10-13.** Initial root-level GitHub repository metadata for five upstream repositories did not declare a uniform license. Further direct inspection of **module manifests** finds explicit `LGPL-3` assertions on several individual addons. This supersedes the coarse root-only conclusion in v0.1.

| Repository | Manifest/module observed | Module license declaration | Current handling |
|---|---|---|---|
| `odoo_practices` | `cd_practices`, `cd_library_practices`, `cd_vet_practices` | `LGPL-3` | educational + library baseline; cite exact SHA |
| `odoo_opencode` | `sale_task_creator`, `purchase_board_wizard` | `LGPL-3` | modified derivative of sale/task with attribution |
| `odoo_19_addons` | `cd_custom_task` | `LGPL-3` | evaluate in future, avoid duplicate feature |
| `odoo_19_addons` | `cd_loan_management`, `cd_workshop_flows` | no license field in inspected manifests | reference only; no literal copying |
| `odoo_19_addons` | `ica_web_responsive` | `LGPL-3`, authors `Agga, IdeaCode Academy` | hold: check original authorship/third-party license chain |
| `proyecto_OWL` | standalone Vite project | no license identified | reimplement Odoo-specific requirements, not original source |
| `Pruebas_Odoo` | `biblioteca_proyecto` | no license identified | domain specification only, no code copying |

A `license` field in a module manifest is **evidence of a claimed license**, not a warranty that all commits/assets are owned by that manifest's author; check additional third-party sources prior to broad redistribution. Keep upstream attribution and LGPL license text. A public GitHub repo alone provides viewing/forking rights; it does not automatically license all reuse. See GitHub documentation: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository.

This repository has no **blanket** root license. The two module directories have their own LGPL-3 notices and texts. This is a technical compliance record, not a substitute for jurisdiction-specific legal review.
