# Gate PAY-MAN-01 — sobrepago Yape/Plin manual y movimiento implícito de caja

**Estado:** REQUIREMENTS / POLICY DECISION OPEN, **NO IMPLEMENTAR EXTENSIÓN OWL NI PARCHEAR ODOO CORE TODAVÍA**. Hallazgo derivado del [UAT visual](UAT-2026-10-21-01.md), [issue #6](https://github.com/Em3rc0d/odoo-engineering/issues/6), SRS RF-032/UC-06, y evidencia directa del código Odoo 19 Community.

## Condiciones que vemos
- El script local seed_demo.py crea Yape/Plin con journal tipo bank, payment_method_type none. No hay vínculo ni webhook de verificación de Yape/Plin.
- Odoo 19, addons/point_of_sale/static/src/app/screens/payment_screen/payment_screen.js (líneas 199–210), evita importe mayor al saldo pendiente cuando NO existe medio cash. Con cash configurado, puede permitir exceso de pago en otro medio y liquidar cambio en efectivo.
- Recibo y arqueo UAT: digital registrado S/20 para S/11.80; devuelve contablemente S/8.20; cash esperado S/91.80 desde apertura S/100. El operador no ha confirmado todavía si entregó efectivo físico.
- Contrato funcional actual define PAGO MANUAL como declaración y PAGO CONFIRMADO como evidencia de tercero. La pantalla nativa Payment Successful expresa venta cerrada, pero puede interpretarse erróneamente como transferencia bancaria verificada.

## Decisión requerida del propietario del producto (NO cerrada)

**Opción A — Política conservadora candidata (PREFERRED, not approved):** Para pago Yape/Plin MANUAL, exigir importe positivo y **no mayor** al saldo pendiente. Una venta S/11.80 debe recibir S/11.80 manuales o combinación explícita de métodos. Nunca generar salida de efectivo implícita desde un monto de billetera manual. Etiquetar "Pago declarado manualmente; verificación bancaria externa pendiente". Cobro contable y prueba del canal deben permanecer separados.

**Opción B — Permitir vuelto de dinero previamente transferido:** Solo como operación deliberada: importe verificado por la fuente correspondiente o comprobación presencial aprobada, autorización de supervisor, registro explícito de salida de caja, motivo, ID de orden, comprobante/identidad de devolución, y arqueo. Si falta alguno, el sobrepago no se valida. Evaluar legalidad, fraude, conciliación y soporte. No convertir en comportamiento por defecto sin gate formal.

No mezclar Opción A y B silenciosamente; no asumir que el POS estándar tiene todo el RBAC/event log requerido.

## Pruebas de contrato que deben fallar primero y luego pasar

| ID | Entradas con apertura ficticia S/100 | Resultado esperado bajo opción A |
|---|---|---|
| PM-01 | Venta S/11.80 + digital manual S/11.80 | Venta registrada, digital NO verificado, cash S/100 |
| PM-02 | Venta S/11.80 + digital manual S/20 | Rechazo de sobrepago, sin venta/cash-out ni stock duplicado |
| PM-03 | Venta S/11.80 + efectivo S/20 | Cambio S/8.20, cash esperado S/111.80 |
| PM-04 | Venta S/11.80 + digital manual S/8 + cash S/3.80 | Sin vuelto digital; cash esperado S/103.80 |
| PM-05 | Venta S/11.80 + digital manual S/0, S/-1, texto inválido, 2 líneas digitales simultáneas | Validación coherente, no decrementos de caja ni pedidos duplicados |
| PM-06 | Pago digital declarado, sin evidencia del PSP | No mostrar "confirmado por Yape/Plin"; "registrado manualmente" explícito |
| PM-07 | Cierre con efectivo contado S/0 vs esperado S/91.80 | Discrepancia expuesta y autorización/auditoría según política; nunca PASS silencioso |
| PM-08 | Reintento/corte tras validar pago manual | Identidad de pedido estable, sin duplicidad de movimientos o vuelto |

**Fuentes y procedencia:** captura usuario 2026-10-21 (USER_OBSERVED), seed_demo propio (CODE_OBSERVED), Odoo 19 upstream payment_screen.js (CODE_OBSERVED), políticas y expectativas propuestas (INFERRED/PROPOSED). No se inspeccionó la base privada, no se probó código de PSP y no se efectuó pago real. Este gate no altera el SRS aprobado hasta que haya ADR y criterios acordados.

## Bloqueantes para G1
- El usuario debe confirmar efectivo entregado y recuento final de la prueba.
- Aprobar política A o B mediante decisión documentada.
- Ejecutar pruebas de efectivo, digital exacto, sobrepago y mixto en Odoo 19 pinned.
- Solo entonces diseñar parche propio compatible y permisos, sin modificar core ni exponer credenciales fiscales.
