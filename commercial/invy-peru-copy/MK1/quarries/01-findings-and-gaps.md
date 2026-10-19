# Quarry MK1 — hallazgos, contradicciones y próximas extracciones

| ID | Evidencia / inferencia | Estado | Impacto |
|---|---|---|---|
| MQ01 | POS/stock/IGV/seed CI verdes a commit 48efd45 | OBSERVED | prueba una base Odoo reproducible |
| MQ02 | checkout smoke abarca sesión, cobro efectivo y stock con rollback | OBSERVED | no es E2E visual ni pago bancario |
| MQ03 | UI muestra escenarios aceptado/rechazado/timeout en código simulador | OBSERVED en fuente, no UX probado | prohibido comercializar como fiscal |
| MQ04 | 22 pantallas y 7 secuencias de usuario ya documentadas | OBSERVED documental | validar con cajeros |
| MQ05 | OPeru+Nubefact era opción 1; posteriormente el propietario priorizó OSS directo | CONTRADICTION documentada | DEC-FISCAL-02 BLOCKED |
| MQ06 | Greenter en PHP requiere integración Odoo Python y licencias verificadas | PROPOSED / análisis | costo/opción real pendiente |
| MQ07 | Multi-tenant 1 DB/filestore/secretos por cliente | PROPOSED | validar 2 tenants, backup/restore |
| MQ08 | Precio mensual competitivo necesita margen después IGV y soporte | INFERRED por modelo | medir costos reales |
| MQ09 | PSE, OSE y SEE son figuras distintas | OFFICIAL en fuentes SUNAT a reverificar | validación legal por contribuyente |
| MQ10 | SRS cubre 88 RF y 43 RNF ligados a TC designados | OBSERVED documental | no se ha aprobado cumplimiento |
| MQ11 | Copiar UX/material INVY generaría riesgo legal, aunque competir por capacidades es legítimo | riesgo por evaluar | crear marca/UI propias |
| MQ12 | La legislación de datos personales peruana exige investigación normativa actualizada | OPEN | bloquear datos reales hasta política/aprobación |
| MQ13 | Aún no existe evidencia de tickets de clientes ni margen MRR del producto | OPEN | no declarar traction |
| MQ14 | Talleres, restaurantes, fraccionamiento, ISC y multisucursal agregan variantes mayores | PROPOSED fuera alcance | proteger primer MVP |

## Prioridad de extracción posterior

1. De Odoo 19 fijado: los flujos concretos POS→account.move, nota de crédito, permisos y offline.
2. De fuentes SUNAT vigentes: formatos, resúmenes, certificados, CDR/consulta, corrección y contingencia por modalidad.
3. De proyecto Greenter: licencia/versiones/dependencias, soporte, ejemplos y compatibilidad actual.
4. De OPeru y Nubefact: licencias, contratos, tarifa, TCO, SLA, soporte y fallback.
5. De entrevistas: fricciones reales, ICP, hardware y disposición a pagar.
6. De seguridad: obligaciones de protección de datos, conservación y derechos contractuales aplicables.
