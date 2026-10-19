# MK0 — Análisis agnóstico de alternativas

| Alternativa | Pro | Contra | Decisión |
|---|---|---|---|
| Odoo Community 19 + addons acotados | reutiliza POS/stock/caja; PostgreSQL | upgrade y UX pueden demandar adaptación | base preferida |
| ERP POS propio completo | control total de interfaces | recrea transacciones, contabilidad, stock, fiscalidad | NO MVP |
| OPeru 19 + Nubefact | ruta posible ya creada por terceros | costo variable, compatibilidad y licencia no verificados | ADR histórica provisional |
| Greenter PHP + adaptador Odoo + SUNAT | motor abierto/costo licencia potencialmente cero | firma, UBL, SOAP, estados y mantenimiento bajo responsabilidad propia | **preferencia del propietario para investigar**, no adoptado |
| Conector SOAP propio desde cero | elimina intermediario técnico | superficie normativa y costo de mantenimiento elevados | evitar para primer MVP |
| Odoo Enterprise o componente no licenciado | funciones adicionales | licenciamiento y distribución | NO usar sin derechos |
| Multi-tenant DB y filestore separados | aislamiento y restauración por cliente | mayor costo y automatización | propuesta |
| DB única de clientes | puede ahorrar recursos | más riesgo inter-tenant | NO preferido |
| POS offline universal y CPE inmediato | continuidad aparente | caché/stock/tributación requieren controles | fuera del MVP |

## Decisión fiscal pendiente DEC-FISCAL-02

Comparar por modalidad tributaria permitida, tipos de comprobantes, notas, obligación de PSE/OSE, certificado, licencias, costo total, soporte, APIs de consulta, CDR/constancias y fallos ambiguos. La ruta directa **puede** reducir tarifas de terceros; no garantiza gratuidad completa ni elegibilidad universal.

## Fronteras

Odoo = fuente comercial. Adaptador fiscal = solicitudes, firma, envío, conciliación y evidencia sin modificar venta. Plataforma SaaS = aprovisionar, aislar, respaldar y atender. Rally = servicio ajeno al alcance inicial.
