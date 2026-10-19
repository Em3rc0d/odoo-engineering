# Mining Site MK1 — libro de fuentes y decisiones reproducibles

**Fecha:** 2026-10-19. Metodología: OFFICIAL / OBSERVED / INFERRED / PROPOSED / BLOCKED. Las referencias externas se conservan para recotejar en cada gate; esta consolidación **no** simula una revisión oficial nueva hoy.

| ID | Referencia | Evidencia que soporta | Confianza / advertencia |
|---|---|---|---|
| O-01 | https://github.com/odoo/odoo/tree/19.0 | Odoo Community, POS y localización pública | ALTA fuente, verificar SHA de release |
| O-02 | https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html | localización PE documentada | ALTA como doc, no licencia EDI Enterprise |
| O-03 | https://www.odoo.com/documentation/19.0/applications/sales/point_of_sale/use.html | límites de operación POS offline | ALTA documento, probar nuestro hardware |
| O-04 | https://cpe.sunat.gob.pe/sistema_emision/see_contribuyente | modalidad contribuyente | FUENTE PRIMARIA, reglas por caso pendientes |
| O-05 | https://cpe.sunat.gob.pe/aliados/pse | PSE regulado | FUENTE PRIMARIA, no afirmar que somos PSE |
| O-06 | https://cpe.sunat.gob.pe/aliados/ose | OSE y funciones | FUENTE PRIMARIA, elegibilidad pendiente |
| O-07 | https://github.com/thegreenter/greenter | motor OSS candidato | revisar versión, LICENSE, cadena deps |
| O-08 | https://www.nubefact.com/integracion | API de proveedor candidato | condiciones/precio todavía no contratados |
| O-09 | https://www.invyperu.com/precios | benchmark público registrado 16/oct/2026 | marketing, no prueba técnica/actual |
| L-01 | https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080 | CI Odoo+POS+stock demo | OBSERVED 16/oct/2026, SHA 48efd45 |
| L-02 | commercial/retail-peru/design/sequences.md | siete recorridos de usuario documentados | diseño, no runtime |
| L-03 | integrations/sunat/VALIDATION-2026-10-16.md | nueve pruebas gateway mock | alcance restringido, sin proveedor |
| L-04 | integrations/sunat/DEC-PE-EDI-001.md | fiscal OPeru+Nubefact provisional | contradice nueva preferencia OSS, dejar abierta |
| L-05 | commercial/retail-peru/unit-economics.md | tarifas hipotéticas y fórmula de margen | no factura real ni costos auditados |

## Provenance y confidence

Las decisiones deben registrar qué componente, commit/version, fecha, documento/línea, evidencia de prueba, responsable y estado corresponde. Ningún «costo S/0» se declara antes de considerar infraestructura, certificados, mantenimiento, asesoría y cumplimiento. Evitar asignar fuente OFFICIAL a una inferencia o a propaganda de competidor.

## Preguntas para fuentes primarias

- ¿Qué modalidades y tipos CPE aplican a cada contribuyente del piloto?
- ¿Cuándo se requiere firma/certificado propio, PSE u OSE?
- ¿Cómo se determina un resultado final válido y se consulta cuando el envío es ambiguo?
- ¿Cuánto conservar XML/CDR y bajo qué condiciones?
- ¿Qué normativas de datos personales, contratos y protección de consumidores se aplican al SaaS en Perú?
- ¿Qué licencia tiene exactamente cada dependencia usada en el producto distribuido?
- ¿Cuál es el costo total por emisor para las dos rutas fiscales candidatas?
