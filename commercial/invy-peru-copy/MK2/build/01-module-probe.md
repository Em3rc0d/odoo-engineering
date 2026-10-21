# Build — prueba Odoo Community 19 sin efectos tributarios

## Mejora aplicada

Archivos en la raíz del repositorio:
- experiments/retail-pos-lab/scripts/probe_edi_modules.py
- experiments/retail-pos-lab/scripts/lab.sh, nuevo comando probe-edi
- experiments/retail-pos-lab/EDI-PROBE.md
- .github/workflows/retail-cpe-lab.yml, ejecución de probe-edi tras checkout-smoke

Verifica, por separado, presencia en addons_path y estado ir.module.module. Exige instalados los seis módulos del laboratorio y se niega a continuar si hay algún motor EDI externo instalado accidentalmente.

## Ejecución real

GitHub Actions run: https://github.com/Em3rc0d/odoo-engineering/actions/runs/39642972244
SHA inspeccionado: 091636e09855b607cae767b9e0ae0e1513ca8d95.

Resultados observados en log: static SUCCESS, odoo-install SUCCESS, DEMO_SEED_OK, DEMO_CHECK_OK y CHECKOUT_SMOKE_OK (stock 30→29 con rollback). **EDI_PROBE_OK** informa l10n_pe, l10n_pe_pos y oe_pe_cpe_lab instalados. Los nombres l10n_pe_edi, l10n_pe_edi_base, l10n_pe_edi_odoofact, l10n_pe_edi_odoofact_pos y l10n_pe_catalog figuran no listados/no presentes en la ruta configurada.

Esto prueba la **imagen y configuración utilizadas**, no que los add-ons no puedan instalarse en Odoo Community mediante rutas legales. No se descargaron addons nuevos ni se probó su compatibilidad/licencia.

## Reproducción en equipo aislado

Desde experiments/retail-pos-lab:
- bash scripts/lab.sh demo-setup
- bash scripts/lab.sh probe-edi
- bash scripts/lab.sh checkout-smoke

La prueba de CLI y Odoo Shell se limita a retail_peru_lab. No hay emisión fiscal, conexión con SUNAT, token ni certificado. La prueba visual mediante navegador Windows sigue abierta.

## Prueba ORM adicional sobre factura publicada

Se añadió [invoice_simulation_smoke.py](../../../../experiments/retail-pos-lab/scripts/invoice_simulation_smoke.py), disponible con `bash scripts/lab.sh invoice-sim-smoke`. En [CI run 39644924493](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39644924493), SHA `b6e1091a7f85aeffac74dc928d765efd66a307e4`, los jobs static y odoo-install fueron verdes; log `INVOICE_SIM_SMOKE_OK posted=2 accepted_mock=1 unknown_then_checked=1 duplicate_blocked=1 real_sunat=NO rollback=YES`. Las identidades son sintéticas y las operaciones se revierten. **No cubre POS→account.move ni emisor fiscal verdadero**.
