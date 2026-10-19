# Estado y decisiones — 19/oct/2026

## Aprobaciones y límites

**Aprobado:** dirección del producto, prototipo conceptual, documentar SRS detallado y avanzar por etapas con evidencia. **No aprobado:** emisión tributaria real, SaaS productivo, licencia Enterprise no verificada, promesa de paridad 1:1 con INVY.

**Preferencia comercial:** full open source, sin tarifa de licencia o por comprobante si resulta viable y legal. **Choque aún abierto:** la ADR del 16-oct-2026 consideró OPeru + Nubefact primera opción; la conversación posterior prefirió investigar Greenter + envío SUNAT directo. Una preferencia no sustituye validación legal ni un bench técnico. Ver MK1/arch/03-decisions-and-risks.md.

**Segmento candidato:** comercio minorista formal, 1 RUC, 1 local, 1–2 cajas, PEN, productos físicos por unidad. No hay entrevistas ni clientes pagadores verificados en este expediente.

## Hechos de ingeniería

| Evidencia | Estado |
|---|---|
| Docker Odoo Community 19 + Postgres 16 | CI VERDE, commit 48efd45 |
| Instalar módulos y seed de 3 SKU, método efectivo y Yape/Plin manual | CI VERDE |
| Apertura, venta pagada, cierre y decremento de stock con rollback | CI VERDE |
| POS visual desde Windows y recorrido completo POS→factura→simulador | PENDIENTE |
| Local CPE con rechazo/timeout y no duplicación | Código de simulación; no emisión |
| XML firmado, SUNAT y CDR oficial | NO IMPLEMENTADO |
| Hosting multi-tenant, backups restaurados y SLA | NO IMPLEMENTADO |
| Dos pilotos y márgenes verificados | NO DEMOSTRADO |

## Definiciones de procedencia

OFFICIAL = fuente primaria; OBSERVED = log o hecho reproducible; INFERRED = deducción; PROPOSED = elección pendiente; BLOCKED = gate sin evidencia. Fecha y SHA obligatorios para afirmar validación.
