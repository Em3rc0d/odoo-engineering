# Build MK1 — estado real y guía reproducible

**NO es entrega SaaS/tributaria productiva.** El código y los datos de ejemplo se conservan en una sola fuente, sin duplicarlos bajo invy-peru-copy.

## Versionado y origen

- Repositorio: https://github.com/Em3rc0d/odoo-engineering
- Laboratorio: experiments/retail-pos-lab/
- Commit ejecutado y verificado: 48efd4564891887c6ce89b16f7dd65e369f286c6.
- GitHub Actions verde: https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080
- Odoo 19.0-20260908, PostgreSQL 16; addon oe_pe_cpe_lab, localización l10n_pe y l10n_pe_pos, POS y stock.
- Datos: tres SKUs sintéticos, empresa demo, PEN e IGV 18%, caja de prueba, cash + Yape/Plin MANUAL.

## Arranque de una demo en Windows con WSL 2 y Docker Desktop

~~~bash
git clone https://github.com/Em3rc0d/odoo-engineering.git
cd odoo-engineering/experiments/retail-pos-lab
bash scripts/lab.sh demo-setup
bash scripts/lab.sh version
bash scripts/lab.sh check-demo
bash scripts/lab.sh checkout-smoke
~~~

Abrir http://127.0.0.1:8079; en base recién provisionada por CLI, cambiar clave administrativa inicial inmediatamente. Si la BD ya existía, se preservan usuarios/contraseñas. Sin certificados reales ni claves SOL.

## Evidencia observada (ORM real, CI del SHA)

- DEMO_SEED_OK: caja demo y SKU DEMO-CUADERNO / LAPICERO / MOCHILA, cash + registro manual.
- DEMO_CHECK_OK: Perú, PEN, IGV 18%, seis módulos.
- CHECKOUT_SMOKE_OK: sesión abierta, venta pagada, cierre y stock 30→29, seguido de rollback para no afectar el fixture.

**Limitación:** no es prueba E2E interactiva del navegador, ni prueba de facturas/numeración SUNAT, ni prueba de importación masiva, devolución, 2 tenants, impuestos mixtos u offline. No publicar claims distintos.

## Recorrido humano por validar

1. Acceso con admin local, apertura en POS, conteo inicial.
2. Venta de 2 productos ficticios; pagar en efectivo y consultar resultado.
3. Otra venta, medio manual Yape/Plin; ver mensaje veraz.
4. Seleccionar comprador y facturación POS conforme a la configuración; ver account.move si Odoo lo crea; no asumir que CPE real se emitió.
5. En factura contable publicada usar botón Simular CPE (NO SUNAT) bajo las restricciones del contrato de laboratorio. Probar aceptado/rechazo/timeout simulados.
6. Cierre de caja y comparación de efectivo/stock. Registrar capturas sin datos sensibles, versión, clicks, tiempos y fallos.

[Runbook detallado](../../../../experiments/retail-pos-lab/DEMO-RUNBOOK.md). Los comandos no modifican el repositorio Rally ni requieren Greenter o Nubefact.

## Componentes por construir después del gate

- Adaptador fiscal autenticado y autorizado, outbox, firma XML y conciliación CDR.
- CRUD/panel de incidencias y cambios de estado independiente.
- Provisionador por tenant y vault de secretos, backup/restore y operator console.
- CI de dos usuarios/cajas, seguridad entre tenants, navegador real, notas y timeout.
- Observabilidad, soporte, gestión de suscripción y guías operativas.

No modificar core Odoo si puede extenderse; documentar cada personalización y licencia. No incorporar automáticamente los addons experimentales no relacionados de addons/ ni el snapshot Rally.
