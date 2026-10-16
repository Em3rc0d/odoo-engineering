# DEC-PE-EDI-001 — Motor fiscal del MVP

**Estado:** PROVISIONAL; capacidad sin certificar. 2026-10-16.

| Camino | Ventaja | Riesgo | Decisión |
|---|---|---|---|
| OPeru 19 + Nubefact PSE/OSE | Posible flujo Odoo→proveedor ya existente; mínima programación propia | Compatibilidad Community/POS, contratos, extensiones y costos no demostrados | **PRIORIDAD 1: probar y evaluar derechos** |
| Nubefact JSON directo con adaptador propio | API documentada, control sobre despliegue y estados | Mantener impuestos, excepciones y conciliación EDI | **PRIORIDAD 2: fallback experimental** |
| `l10n_pe_edi` nativo Odoo | Experiencia integrada documentada | Edición/disponibilidad/licencia Community sin confirmar | VERIFICAR |
| SUNAT SOAP directo | Reduce intermediario | Firma UBL, homologación, seguridad, CDR y mantenimiento considerable | NO MVP |
| Greenter (PHP) | Motor UBL/firma/transmisión open source | Servicio aparte en PHP, no es addon Odoo Python; integración y responsabilidad propia | INVESTIGACIÓN, NO ADOPTADO |

**Separación legal:** PSE no es OSE; PSE emite por cuenta de emisor autorizado, OSE comprueba. No denominar nuestro producto PSE/OSE ni transmitir como proveedor autorizado sin acreditación. En la modalidad PSE, el PSE puede firmar con su certificado; no pedir al cliente su Clave SOL indiscriminadamente si la ruta contractual no la requiere.

**Decisión fiscal definitiva pendiente:** cotización real, prueba aislada y comparación de costo mensual/documento, soporte y cumplimiento.
