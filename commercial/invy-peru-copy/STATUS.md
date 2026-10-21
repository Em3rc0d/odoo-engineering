# Estado y decisiones — actualización MK2, 21/oct/2026

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

## Actualización MK2 2026-10-21: ejecución y límites

- **Implementado:** comando de inventario EDI de solo lectura en la imagen Odoo Community 19, con rechazo de addons EDI externos instalados accidentalmente en el laboratorio aislado.
- **Verificado:** [GitHub Actions 39642972244](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39642972244), commit `091636e09855b607cae767b9e0ae0e1513ca8d95`: static y odoo-install SUCCESS; DEMO_SEED_OK, DEMO_CHECK_OK, CHECKOUT_SMOKE_OK, EDI_PROBE_OK. Probetest: l10n_pe, l10n_pe_pos y oe_pe_cpe_lab presentes; l10n_pe_edi, l10n_pe_edi_base, l10n_pe_edi_odoofact, l10n_pe_edi_odoofact_pos y l10n_pe_catalog ausentes del addon path configurado. **No equivale a decir que no se puedan instalar legalmente.**
- **Competencia observada:** [INVY Pyme](https://www.invyperu.com/precios) S/169 incl IGV/500 CPE; [Alegra POS Pyme](https://www.alegra.com/peru/punto-venta/precios/) S/93 incl IGV/1,000 CPE; [Bsale](https://www.bsale.com.pe/sheet/precios) S/189 básico; ofertas y precios de proveedor, no contratos auditados.
- **Rutas fiscales:** OPeru/Nubefact como primera opción para probar **si** se acreditan compatibilidad/licencias/terms; Greenter/Kembec/CPEForge como alternativas OSS de benchmarking; aún sin selección, credenciales ni CDR.
- **Emisión SUNAT real y SaaS listo:** NO PROBADOS/NO AUTORIZADOS.
- **Experimento comercial:** NO GO, 0 compradores pagadores certificados y L1 laboral externo bloqueado; no hubo prospección.
- Expediente y gates: [MK2](MK2/README.md).

## Ampliación de prueba MK2: factura contable→simulador (2026-10-21)

[CI 39644924493](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39644924493) PASS sobre commit `b6e1091a7f85aeffac74dc928d765efd66a307e4`: dos `account.move` sintéticos publicados; aceptación y timeout simulados, consulta del resultado incierto, intento duplicado rechazado y rollback. Esto **cierra prueba ORM parcial del simulador**, no el recorrido de interfaz POS→account.move, ni SUNAT XML/CDR/credenciales, ni G3. Ver [MK2 test](MK2/test/01-evidence.md).
