# Componentes que debemos acomodar por encima de Odoo

**DUX-CMP-001 — arquitectura objetivo.** No confundir «componente propuesto» con código existente.

## Diagrama de responsabilidades

~~~mermaid
flowchart TB
    Personas["Cajero · Dueño · Supervisor · Contador"] --> UX["Experiencia: POS / caja / reportes / bandeja fiscal"]
    UX --> Odoo["Odoo Community 19: ventas, pagos registrados, inventario, caja, documentos"]
    Odoo --> Bridge["Conector fiscal Odoo: evento y referencia comercial"]
    Bridge --> Outbox["Outbox persistente: identidad, cola, reintentos seguros"]
    Outbox --> Adapter["Adaptador EDI intercambiable"]
    Adapter --> Provider["OPeru + Nubefact (a evaluar) / alternativa aprobada"]
    Provider --> SUNAT["SUNAT / canal de validación aplicable"]
    SUNAT --> Provider
    Provider --> Adapter
    Adapter --> Evidence["Estado + XML / constancias / evidencias verificadas"]
    Evidence --> Odoo
    SaaS["Plataforma SaaS: alta, aislamiento, HTTPS, backups, monitoreo, soporte"] -.-> UX
    SaaS -.-> Odoo
    SaaS -.-> Outbox
    Rally["Rally opcional: custodia / casos avanzados"] -.-> Odoo
~~~

Las flechas punteadas representan administración o integración futura, **no acceso libre a la base de datos**.

## Qué reutilizar, adaptar o construir

| Capa | Componente | Responsable del dato | Estado actual / trabajo |
|---|---|---|---|
| Experiencia | POS y sesiones de caja | Odoo | Módulos base; comprobar en laboratorio |
| Experiencia | Panel simple de dueño | Odoo | Definir si basta reporte existente o extensión |
| Experiencia | Bandeja de incidencias fiscales | Odoo + integración | Propuesta de UI, sin implementación |
| Comercio | Productos, precios, stock, devoluciones | Odoo | Reutilizar, validar flujos reales |
| Comercio | Pagos manuales y pagos integrados | Odoo / proveedor de pago | Distinguir registro de confirmación |
| Fiscal | Conector POS→documento fiscal | Odoo | Por construir o integrar; contrato por validar |
| Fiscal | Cola y deduplicación durables | Motor fiscal | Por diseñar y probar |
| Fiscal | Emisor/adaptador | Proveedor elegido | OPeru 19 + Nubefact: evaluación prioritaria, no validada |
| Fiscal | Gateway Nubefact experimental | Este repositorio | Contrato parcial con HTTP simulado; no addon Odoo |
| Fiscal | Evidencia y estado tributario | Integración, visible en Odoo | Falta persistencia/consulta/verificación |
| SaaS | Alta, aislamiento y configuración | Plataforma SaaS | Diseño, no aprovisionador operativo |
| SaaS | Backups y restauración | Plataforma SaaS | No validados para clientes reales |
| SaaS | Seguridad y acceso de soporte | Plataforma SaaS + Odoo | Diseño y pruebas pendientes |
| Extensión | Rally | Rally | Independiente, fuera del MVP |

## Contratos mínimos

### Operación comercial → solicitud fiscal

Entradas: tenant, RUC emisor, venta persistida, tipo documental, serie/número autorizados, importes/impuestos, comprador, versión de reglas y clave de idempotencia. No enviar un comprobante de una venta borrador o no confirmada.

Salidas: identificador estable de solicitud, vínculo a venta/documento de Odoo, fecha de creación, estado inicial y errores de validación.

### Solicitud fiscal → adaptador

Entradas: identidad única (RUC, tipo, serie, número), payload validado, versión de adaptador, referencia segura a credenciales por tenant y contexto de entorno. Los secretos nunca viajan en logs ni Git.

Salidas: recepción técnica, resultado reportado por proveedor, estado fiscal *verificado* cuando proceda, códigos de error, marcas de tiempo y referencias de evidencias.

### Adaptador → Odoo

Publicar un cambio de estado **idempotente**, con evento auditable. No alterar ventas ni pagos como efecto implícito de una respuesta fiscal. Si el canal solo reporta éxito técnico, mantener etiqueta diferenciada hasta verificar evidencia fiscal aplicable.

### SaaS → instancia del cliente

Alta idempotente, DB/filestore/secretos aislados, TLS, módulos permitidos, cuenta admin única, pruebas de acceso cruzado y restauración; suspensión con política de retención/exportación.

## Decisiones técnicas que bloquean la implementación

- **D-CMP-01:** verificar el flujo real POS→factura/boleta en Odoo Community 19, no asumir que se crea account.move automáticamente.
- **D-CMP-02:** resolver si OPeru 19 + Nubefact cubre la ruta con licencias, costo y evidencia suficiente; Greenter sigue en investigación.
- **D-CMP-03:** escoger mecanismo durable de outbox, transacciones, locks y deduplicación.
- **D-CMP-04:** diseñar retención y cifrado de evidencias tributarias.
- **D-CMP-05:** definir política de pagos externos y hardware de caja.
- **D-CMP-06:** aprobar esquema de aislamiento, acceso soporte y restauración.
- **D-CMP-07:** definir reglas de documentos por tipo y modalidad fiscal con revisión competente.

## Invariantes

1. No se genera otro CPE por repetir una petición o perder una respuesta.
2. Un comprobante rechazado o incierto permanece visible y trazable.
3. Venta, cobro, movimiento de stock y estado fiscal no se confunden.
4. La firma, serie, número y credenciales pertenecen al emisor autorizado.
5. No se alteran documentos firmados ni evidencias históricas.
6. Ningún cliente SaaS puede leer datos o secretos de otro.
7. Rally no escribe directamente en tablas comerciales de Odoo.
