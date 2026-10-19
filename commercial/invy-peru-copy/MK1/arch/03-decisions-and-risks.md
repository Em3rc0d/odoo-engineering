# Registro de decisiones y riesgos — IPC-ADR-001

**Método:** cada ADR lleva contexto, opciones, evidencia, dueño, fecha y estado. «Aprobado modelo» no sustituye aprobar dependencia comercial o fiscal.

## Decisiones

| ID | Propuesta / historial | Pro | Contra | Estado / gate |
|---|---|---|---|---|
| ADR-01 | Odoo 19 Community núcleo ERP/POS | madura transacciones | personalización/versiones | ACEPTADA como baseline laboratorio; G1/G4 comerciales pendientes |
| ADR-02 | No forkear core; addons aislados | upgrades claros | menos libertad inicial | PROPOSED |
| ADR-03 | Tenant = DB/filestore/secretos separados | recuperación/privacidad | overhead por cuenta | PROPOSED, G3/G4 |
| ADR-04 | Emisión asíncrona por outbox durable | resiliencia ante SUNAT | estados/operación extra | PROPOSED, G3 |
| **DEC-FISCAL-02** | **Greenter + directo** vs OPeru 19 + Nubefact | OSS/control/costo potencial vs proveedor integrado | responsabilidad legal/operativa vs dependencia comercial | **BLOCKED: NO decidir sin pruebas y TCO** |
| ADR-06 | POS offline limitado por escenarios | continuidad acotada | caché y stock incierto | PROPOSED; gate legal fiscal |
| ADR-07 | Rally fuera del runtime MVP | foco, aislamiento de dominios | menos aseguramiento operativo | ACEPTADA |
| ADR-08 | Yape/Plin sin API = registro manual | permite demo honesta | conciliación manual | ACEPTADA como lab, verificar uso comercial |
| ADR-09 | Contratos independientes del motor EDI | opción de migrar | más testing de adapters | PROPOSED |
| ADR-10 | MVP un rubro, un local y PEN | menor soporte | no cubre todos los mercados | PROPOSED validar MK0 |

## DEC-FISCAL-02: criterios obligatorios y precedencia

El ADR del repositorio [DEC-PE-EDI-001](../../../../integrations/sunat/DEC-PE-EDI-001.md) (16-oct-2026) prioriza **OPeru+Nubefact** por velocidad potencial; posteriormente se explicitó preferencia fuerte por **full OSS/free** y se propuso **Greenter + SUNAT directo**. **Esta contradicción queda conservada, no se altera el ADR histórico sin nueva evidencia**.

**Para resolver:** compatibilidad Odoo Community 19 y POS real, licencias (incluidas dependencias y redistribución), modo SUNAT elegible por contribuyente, diferencia PSE/OSE, certificado/firma y custodia, factura/boleta/notas/correcciones, tiempos de respuesta, estados/CPE/CDR, documentación/SLA, emisión/rechazo/timeout en beta y producción autorizada, coste por 1/100/1000/10000 documentos, hosting PHP, soporte y cambios normativos. No introducir credenciales reales en laboratorio/CI.

**Criterio GO:** costo total y riesgos aceptables + end-to-end verificado; **NO GO:** imposible técnica/legalmente o más caro/riesgoso que un proveedor sin ventaja apreciada. Si la opción directa es elegible solo para algunos RUC, ofrecer fallback contractual o declarar segmento excluido.

## Riesgos priorizados

| ID | Amenaza/escenario | Severidad | Mitigación y prueba |
|---|---|---|---|
| R01 | factura duplicada ante timeout | crítica | identity + lock/outbox + consulta, fault injection |
| R02 | aceptación ficticia sin constancia | crítica | evidencia por modalidad, no HTTP/simulador |
| R03 | certificado/Clave SOL filtrados | crítica | vault, rotación, logs redactados, secret scan |
| R04 | datos tenant A visibles a B | crítica | DB/filestore/secretos, pruebas negativas |
| R05 | backups incompletos / restore inválido | crítica | ejercicios DB+filestore, RPO/RTO medidos |
| R06 | obligación PSE/OSE ignorada | crítica | validación por contribuyente y asesores |
| R07 | transacción POS repetida | alta | llave idempotente y auditoría efectos |
| R08 | inventario incorrecto por offline/concurrencia | alta | sincronizar una vez, restricciones por modo |
| R09 | cálculo IGV incorrecto o regla nueva | alta | golden fixtures y changelog SUNAT |
| R10 | devolución con reembolso doble | alta | límites por venta, autorización |
| R11 | caja cierra maquillando diferencia | alta | acta/umbral/actor, prueba negativa |
| R12 | licencias de addon o dependencia incompatibles | alta | SBOM/licensing gate |
| R13 | costo de soporte mayor que mensualidad | alta | medir tiempo/tickets, modelo margen |
| R14 | copiar activos protegidos INVY | alta | benchmark por capacidades, marca propia |
| R15 | actualización Odoo rompe POS localización | alta | staging, pruebas, rollback |
| R16 | mercado sin interés real | alta | entrevistas, pilotos pagados o PIVOT/KILL |
| R17 | información personal en logs/soporte | alta | minimización, acceso temporal, scrub |
| R18 | hardware no compatible en tienda | media/alta | piloto de dispositivos y bloqueo de promesa |
| R19 | dependencia permanente fundador | alta | runbook, delegación, documentación y soporte |
| R20 | hoja de ruta se llena de IA y verticales antes del MVP | alta | gates de valor y control de cambio |

## Modelo de amenazas STRIDE

**Spoofing:** credenciales robadas / token de otra empresa. **Tampering:** modificar precio, XML, cierre, stock. **Repudiation:** devolución o apertura sin actor. **Information disclosure:** backup/secretos/XML de otro tenant. **Denial of service:** spam POS/API fiscal, caídas SUNAT, saturación de workers. **Elevation of privilege:** cajero obtiene administrador o soporte consulta otra empresa. Para cada amenaza exigir test negativo y respuesta a incidentes antes de operaciones reales.
