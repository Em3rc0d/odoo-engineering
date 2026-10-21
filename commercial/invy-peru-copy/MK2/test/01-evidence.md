# Test · matriz de evidencia acotada MK2

Conservar la trazabilidad individual de 88 RF y 43 RNF del SRS en MK1/test/traceability.csv. Una prueba de laboratorio no puede aprobar toda una familia RF.

| Test | Qué evidencia tenemos | Estado |
|---|---|---|
| T-M2-01 origen Odoo + addons base | Workflow 39642972244: módulos base instalados y DEMO_CHECK_OK | PASS LAB |
| T-M2-02 disponibilidad EDI de imagen | EDI_PROBE_OK: nombres EDI externos ausentes en esa imagen | PASS INVENTARIO |
| T-M2-03 venta de efectivo, sesión caja, decremento de stock | CHECKOUT_SMOKE_OK, rollback desde 30 a 29 | PASS ORM RESTRINGIDO |
| T-M2-04 Gateway Nubefact modificado/timeout | Run 39634967651, 10 tests mock; guard de hash antes de HTTP | PASS MOCK ÚNICAMENTE |
| T-M2-05 navegación manual POS, lector/caja y accesibilidad | No existe resultado de navegación E2E validado por esta ejecución | PENDIENTE |
| T-M2-06 POS→factura publicada→simulador con rechazo/timeout | No existe ejecución E2E completa | PENDIENTE |
| T-M2-06a factura contable publicada→simulador local, doble envío, timeout y consulta | [Workflow 39644924493](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39644924493) SHA b6e1091: INVOICE_SIM_SMOKE_OK con dos facturas y rollback | **PASS ORM MOCK**, no origen POS ni SUNAT |
| T-M2-07 doble click, concurrencia, devolución, dos cajas | No hay batería completa ejecutada | PENDIENTE |
| T-M2-08 proveedor OPeru real instalado con licencias verificadas | No instalado; listas comerciales no certifican addons | BLOQUEADO |
| T-M2-09 XML firmado/UBL y CDR SUNAT oficial | Sin credenciales de emisor autorizado ni operación ejecutada | BLOQUEADO |
| T-M2-10 DB/filestore por tenant y restore auditado | Sin implementación | PENDIENTE |
| T-M2-11 comprador/experimento de precio | Sin entrevistas ni usuarios pagadores | BLOQUEADO L1 |
| T-M2-12 soporte y margen medidos en pilotos | Sin pilotos | BLOQUEADO |

**Formato requerido por evidencia nueva:** fecha/tz, ID, archivo/fixture ficticio, commit, versión Docker, comando, resultado esperado/real, salida redactada, alcance, defectos y lo que NO demuestra.

El estado aceptado por un mock es SIMULADO. La recepción HTTP 200 del proveedor no es CDR verificada. La ausencia de módulo EDI en nuestra imagen no demuestra que Odoo Enterprise ni terceros carezcan de ella.
