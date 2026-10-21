# UAT real de Odoo POS y regresión contable condicional — INVY MK2

**Estado:** PROTOCOLO, NO EJECUTADO. Usar exclusivamente retail_peru_lab con fixtures ficticios, Windows/WSL2 y navegador en localhost. Sin SUNAT, Clave SOL ni datos personales de clientes.

## Precondiciones

1. Registrar SHA del repositorio, imagen Odoo 19, fecha America/Lima, versión Docker, navegador, dispositivo y datos ficticios.
2. Ejecutar en experiments/retail-pos-lab: bash scripts/lab.sh demo-setup; check-demo; checkout-smoke; probe-edi; invoice-sim-smoke; pos-invoice-sim-smoke.
3. Cambiar credenciales iniciales de la BD descartable. No copiar usuario o contraseña en capturas, reportes ni tickets.
4. Mantener entorno offline fiscal y comprobar que toda acción del laboratorio diga SIMULADO.

## Escenarios de interfaz (pendientes)

| ID | Pasos GUI en Odoo | Evidencia exigida |
|---|---|---|
| UAT-01 | Abrir Caja DEMO, efectivo inicial 100 PEN | Estado, operador y hora visibles |
| UAT-02 | Vender CUADERNO/LAPICERO y pagar efectivo | Un solo pedido, total e IGV exactos, stock coherente |
| UAT-03 | Venta separada con Yape/Plin REGISTRO MANUAL | No declarar confirmación bancaria de transferencia |
| UAT-04 | Comprador sintético, seleccionar factura desde POS | account.move publicado asociado al mismo pedido, o fallo documentado |
| UAT-05 | En factura, Simular CPE con correlativo ficticio | Estado aceptado/rechazado/timeout claramente **SIMULADO**, sin XML/CDR |
| UAT-06 | Simular segunda vez, consultar estado incierto | Un solo documento; consulta no emite segunda factura |
| UAT-07 | Cerrar caja y contar efectivo físico ficticio | Arqueo, responsable y diferencia preservados |
| UAT-08 | Cajero y supervisor: probar rol/permisos | Acceso restringido sin bypass; documentar denegación |
| UAT-09 | Cortar red solo en laboratorio, reconectar y reintentar | Sin doble pedido ni falsa aceptación de impuestos |

Para cada caso: esperado vs real, captura sin PII, SHA, severidad, pasos y rollback. **NO marcar UAT PASS por pruebas ORM.**

## Regresión upstream específica, no reproducida

[Issue Odoo 19 #290124](https://github.com/odoo/odoo/issues/290124) y [tests-only PR #290126](https://github.com/odoo/odoo/pull/290126) reportan COGS duplicado al facturar **masivamente con asistente** y diferir actualización de existencias hasta el cierre, con contabilidad anglosajona/FIFO y valoración automatizada. El método individual action_pos_order_invoice del smoke no equivale al asistente.

Si se considera ofrecer esa modalidad: en base aislada con método contable correctamente configurado, vender 2 unidades, facturar pedidos por separado y luego con asistente antes/después de cerrar, contrastar valor esperado FIFO y asientos de costo contra una única salida por unidad; realizar comparaciones de control con actualización inmediata y revisar issue/versión Odoo. No ejecutar en datos reales ni afirmar que este fallo se reproduce antes de la prueba. Estado: PENDIENTE.

## Gates

UI real/roles y prueba contable condicionada antes de G1 comercial; XML firmado/CDR oficial y emisor autorizado antes de G3; reversión DB+filestore y piloto legítimo antes de G4. La mejora ORM ejecutada no adelanta esos gates.
