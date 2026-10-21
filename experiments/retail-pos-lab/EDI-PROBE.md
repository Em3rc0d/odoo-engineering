# EDI module inventory probe (disposable Odoo Community 19)

**What is tested:** presence in the configured Odoo addons path and current `ir.module.module` state for base accounting/POS modules and candidate SUNAT EDI integration addon names. **No network to SUNAT, no invoice, no installation, no credentials beyond ephemeral lab DB, no third-party download**.

```bash
cd experiments/retail-pos-lab
bash scripts/lab.sh demo-setup
bash scripts/lab.sh probe-edi
```

The script refuses databases other than `retail_peru_lab`; asserts base modules are installed; **fails closed if any external/fiscal EDI module was accidentally installed in the sandbox**, because the default local laboratory is *simulator-only*. It prints a JSON inventory without filesystem paths, taxpayer data, secrets or tokens. Included in the existing CI `odoo-install` job.

**Interpretation:** `in_configured_addons_path=false` proves absence *from this configured lab image*, **not absence from all Odoo 19 Community distributions** or impossibility of legally obtaining/installing an extension. `database_state=not_listed` is not evidence of a vendor's license terms; verify those independently. If a module later becomes available/installed, investigate in a **separate, explicitly scoped and licensed test environment**, never silently enable fiscal emission in this simulator.

Related gates: [INVY MK2](../../../commercial/invy-peru-copy/MK2/README.md), [F-01 comparison](../../../integrations/sunat/REVIEW-OPEN-SOURCE-EDI-2026-10-21.md). No paid cloud calls or customer data.
