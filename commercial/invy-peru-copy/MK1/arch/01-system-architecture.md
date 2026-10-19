# Arquitectura objetivo — IPC-ARCH-001

**2026-10-19 · PROPOSED / no deployment productivo.** Core monolítico Odoo Community 19; fiscalidad desacoplada; plano SaaS mínimo. No arquitecturar «microservicios por moda».

## C4 — contexto

~~~mermaid
flowchart LR
    C["Cajero / propietario / supervisor / contador"] --> WEB["Web POS y backoffice"]
    WEB --> ERP["Odoo Community 19"]
    ERP --> EXT["Frontera fiscal autorizada"]
    EXT --> SUNAT["SUNAT / PSE / OSE según modalidad"]
    OWNER["Equipo SaaS"] --> OPS["Operación, soporte, backups"]
    OPS -.-> ERP
    PAYMENT["Proveedor de pagos opcional"] -.-> ERP
    RALLY["Rally, futura extensión independiente"] -.-> ERP
~~~

**No existe** comunicación productiva a SUNAT en el código actual; la flecha del diagrama es diseño objetivo.

## C4 — contenedores y límites de confianza

~~~mermaid
flowchart TB
    U["Navegador de cada tenant"] --> EDGE["HTTPS / ingress + identidad"]
    EDGE --> ODOO["Odoo 19 Community (ventas, caja, stock, account.move)"]
    ODOO --> DB[("PostgreSQL tenant")]
    ODOO --> STORE[("Filestore tenant")]
    ODOO --> OUT[("Outbox / jobs fiscales durables")]
    OUT --> EDI["Adaptador fiscal Python"]
    EDI --> GTE["Motor EDI elegido: Greenter u OPeru/proveedor"]
    GTE --> API["Canal SUNAT/tercero"]
    API --> GTE
    GTE --> EVID[("Evidencia fiscal por tenant")]
    EVID --> ODOO
    OPS["Plano SaaS separado"] -. "Orquesta instancias; datos mínimos" .-> ODOO
    SEC[("Vault / secretos segregados")] -.-> GTE
    BAK[("Backup cifrado DB + filestore + metadatos")] -.-> DB
    BAK -.-> STORE
~~~

**Fronteras:** internet/navegador; identidad del usuario dentro del tenant; entre tenants; entre Odoo y motor fiscal; entre motor fiscal y proveedor; entre administrador SaaS y datos privados de empresa. TLS, RBAC, segregación, logging, rotación y pruebas negativas en cada frontera.

## Componentes y propiedad

| Componente | Responsable y datos | Reusar/construir | Gate |
|---|---|---|---|
| Web POS, caja, stock | Odoo transaccional | reusar Odoo + adaptación mínima | G1 |
| Catálogo, impuestos, comprador | Odoo | configurar versión/restricciones | G1 |
| Bandeja fiscal | Odoo + proyección de eventos | extensión candidata | G3 |
| Conector pedido→fiscal | Odoo | construir contrato idempotente | G3 |
| Outbox persistente con leases/locking | integración | diseñar y construir | G3 |
| Adaptador Greenter/OPeru/Nubefact | integración elegida | evaluar derechos/TCO | G3 |
| XML/constancia/CPE | repositorio seguro por emisor | construir política conservación | G3 |
| Plano SaaS | alta, SLA, suscripción, soporte | construir mínimo y verificar | G4 |
| Observabilidad | métricas sin secretos ni datos innecesarios | construir/operar | G4 |
| Rally | custodia/exception future | no integrar al MVP | posterior |

## Propiedad transaccional y consistencia

1. Odoo confirma venta/efecto comercial en su transacción y persiste intención fiscal duradera correlacionada. El mecanismo definitivo debe impedir «venta sin rastro fiscal» donde aplica; se precisa un outbox ORM integrado o patrón equivalente probado.
2. Worker consume intención con llave natural y lease/lock; registra resultado técnico, hash, actor y timestamps. Retries idempotentes; no repetir envío si el estado fiscal es incierto.
3. El adaptador llama a canal legal. Un HTTP 200 de transporte no es CDR aceptado; la respuesta se valida según modalidad y tipo.
4. El resultado actualiza proyección en Odoo sin recrear venta/pago/stock; eventos inmutables.
5. Reconciliador verifica pendientes/desconocidos mediante consulta cuando proceda, con escalamiento humano.

**Evitar:** dos bases independientes como fuente de verdad de ventas, triggers SQL directos sobre Odoo, colas solo en memoria, auto-reintentos fiscales ciegos, firmar con secretos de otro contribuyente.

## Modelo conceptual

- Tenant → Company/RUC → Store → POS config → Session → Sale → OrderLine → Payment; Sale → StockMovement.
- Sale → Invoice/CommercialDocument (según capacidades reales de POS) → FiscalRequest → FiscalEvent[] → FiscalEvidence[].
- Sale → Return[] → StockReturn/Refund/FiscalCorrection (entidades relacionadas, no una sola operación).
- Tenant → Subscription/SupportCase/BackupManifest/RestoreRun.
- Referential integrity: identidad fiscal compuesta (emisor/tipo/serie/número), idempotency key, SHA256 de snapshot, correlación entre sale/order/account.move.

## Integridad y precisión

PEN y redondeos reglamentarios: usar tipos decimales/monetarios definidos, vectores dorados y verificación Odoo→motor EDI→XML→constancia; no confiar en floats serializados sin control. Operación 18% simple como primer perfil; extensiones por ADR y pruebas legales. No cambiar documentos firmados.

## Capacidad y fallos

2 cajas/tenant, 2000 SKU y objetivos de rendimiento SRS son umbrales **propuestos**, no benchmarks. Fallos: DB no disponible, cambio de esquema Odoo, worker muerto, timeout SUNAT, certificado vencido, red offline, backup incompleto, cruce de tenants, costo excesivo. Cada caso debe tener alerta, acción y prueba.

## Licencias

Odoo Community y cada addon con licencia individual; Greenter y dependencias PHP bajo revisión de versión y obligaciones; OPeru módulos externos con licencia/costo/compatibilidad no verificados; no reutilizar código/branding de INVY ni terceros sin derecho. Generar SBOM y matriz de derechos antes de distribución.
