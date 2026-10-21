# MK2 execution plan — gates ordered by dependency

| Gate | Acción verificable | Estado |
|---|---|---|
| M2-00 | Inspeccionar fuentes oficiales, manifests y repos externos con licencias | PASS documental; no implica interoperabilidad |
| M2-01 | Ejecutar módulo de inventario en Odoo Community 19 con base ficticia | PASS acotado CI run 39642972244, sha 091636e... |
| M2-02 | Navegar POS con caja, venta de 2 SKU, Yape/Plin manual, factura opcional y cierre | PENDIENTE: GUI real; ORM anterior solo parcial |
| M2-03 | Doble clic, recuperación tras timeout, dos cajeros, último artículo y devolución | PENDIENTE: pruebas de concurrencia y errores |
| M2-04 | Comparar proveedor fiscal con árbol de dependencias, licencias, costos API, soporte, modalidad y sandbox | BLOQUEADO: material/contrato del proveedor y sandbox autorizado |
| M2-05 | XML, firma, CDR real y errores contra canal SUNAT/operador autorizado | BLOQUEADO: no tenemos emisor/credenciales aprobados |
| M2-06 | 2 tenants, DB+filestore separados, restore, secretos y auditoría de permisos | NO IMPLEMENTADO |
| M2-07 | 10 entrevistas + 3 conversaciones presupuestarias, con L1 resuelto | BLOQUEADO: L1 laboral |
| M2-08 | 2 pilotos válidos, soporte y costos reales, repetibilidad y margen | BLOQUEADO |
| M2-09 | Decidir GO, PIVOT o KILL con firmas/evidencias | NO GO |

**Secuencia siguiente de ingeniería:** prueba GUI local contra base simulada → fallos y reintentos/stock → comparador licencia y sandbox fiscal autorizado → continuidad/multi-tenant. Entrevistas, ventas y contratos solo después del gate laboral. No cambiar el SRS de 88 RF/43 RNF ni construir outbox fiscal real sin cerrar arquitectura y requisitos.

**Entregables:** video/capturas sin PII de la GUI y control por caso de prueba, log legible, commit/imagen Odoo, backup/restore, lista de permisos de módulos, fiscalidad confirmada por experto y un diario de costos reales. Cualquier falla conserva estado OPEN.
