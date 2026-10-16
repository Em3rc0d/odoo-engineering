# Contrato técnico del MVP POS peruano

## Decisiones de arquitectura

- Sistema transaccional principal: **Odoo Community 19**, sin bifurcar su núcleo inicialmente. PostgreSQL y filestore bajo control de cada instalación.
- Arquitectura inicial: **una base de datos + filestore + secretos separados por cliente** (revisar si host compartido aísla procesos, redes y acceso de DB correctamente). Una sola versión de código y contrato de configuración, no un fork por cliente.
- POS, inventario, clientes, ventas, asientos y documentos fiscales permanecen en el ERP. Los adaptadores solo utilizan APIs autorizadas.
- No desplazar lógica comercial a Rally ni copiar su SQLite/Postgres, locks y worker hacia la base Odoo. Rally permanece archivado en `external/rally/` y es un servicio futuro opcional.
- `l10n_pe` y `l10n_pe_pos` existen en fuente pública Odoo 19; **no** equipararlos a un emisor EDI legal. La documentación Odoo lista `l10n_pe_edi`, pero presencia/licencia/funcionalidad en el paquete Community deben comprobarse.
- Selección fiscal pendiente: integración con proveedor legalmente habilitado, contrato costo/documento, emisión boleta/factura, rectificaciones, baja/anulación, numeración, firma/certificado, respuesta y reintentos, CDR/XML/PDF, QR/tickets, custodia segura de credenciales y políticas de retención.
- La operación offline de Odoo tiene límites documentados: el navegador no debe perder caché ni cerrarse antes de sincronizar; factura y estado stock global pueden quedar diferidos. NO prometer operación offline infalible.
- Ningún addon experimental de `addons/` se habilitará por defecto hasta aprobar instalación, vistas, ACL, invariantes, upgrade, seguridad, tests y compatibilidad de versión.
- Para el laboratorio desechable ya existe referencia `external/rally/compose.odoo-lab.yaml`; no usar automáticamente su stack de custodia como despliegue comercial. El laboratorio no aprovisiona clientes ni certifica facturación.

## Contrato de provisionamiento por cliente (diseño, no implementado)

**Entradas obligatorias:** identificador irreversible/único, dominio/TLS, RUC y razón social verificados por el cliente, país, moneda PEN, zona horaria Lima, plan/sucursal/caja, contacto responsable, retención, configuración fiscal y usuario administrador.

**Salidas verificables:** DB y filestore dedicados, esquema/paquete Odoo pinneado, módulos aprobados, importación del catálogo con validación, usuarios y roles, registros de configuración, secreto por servicio, TLS, backup cifrado externo con prueba de restauración, URL de gestión, runbook de upgrade/rollback y aceptación.

**Invariantes:** no acceso a otro cliente; no bases de datos de prueba expuestas; sin admin maestro compartido; no datos reales en fixtures o CI; idempotencia de importación y envío, contabilidad y stock coherentes, logs de estado de CPE sin secretos.

## Dependencias bloqueantes / ADRs aún por resolver

| ID | Decisión | Gate |
|---|---|---|
| DEC-01 | Revisión exacta y licencias Odoo 19 + addons | Antes de distribución |
| DEC-02 | Proveedor / módulo EDI Perú, costos y límites | Antes de vender facturación |
| DEC-03 | Modelo aislamiento host/DB/filestore/domino | Antes de segundo tenant |
| DEC-04 | Estrategia de backup/restore y RPO/RTO contratado | Antes de datos reales |
| DEC-05 | Medio de pago del SaaS, cobro, suspensión y salida | Antes de suscripciones |
| DEC-06 | Alcance y horarios de soporte financiables | Antes de contrato |
| DEC-07 | Compatibilidad POS/impresora/código de barras por perfil piloto | Antes de aceptación |

**Criterio de build:** MK0/MK1 solo se cierran cuando estas decisiones están resueltas con evidencia; se permiten laboratorios desechables, no un despliegue a clientes fingiendo que los gates están superados.

## Fuentes

- https://github.com/odoo/odoo/tree/19.0/addons/point_of_sale
- https://github.com/odoo/odoo/tree/19.0/addons/l10n_pe
- https://github.com/odoo/odoo/tree/19.0/addons/l10n_pe_pos
- https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html
- https://www.odoo.com/documentation/19.0/applications/sales/point_of_sale/use.html
- https://cpe.sunat.gob.pe/aliados/pse
