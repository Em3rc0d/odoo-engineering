# Plan maestro de pruebas MK1 — IPC-TEST-001

**Estado:** pruebas de diseño + evidencia parcial CI para demo. El CSV [traceability.csv](traceability.csv) define 88 TC-RF y 43 TC-RNF; todos están DESIGN_ONLY porque NO hay evidencia individual del comportamiento comercial entero. Los resultados CI se registran de forma explícita abajo.

## 1. Pirámide de validación

| Nivel | Objeto | Ejemplo | Gate |
|---|---|---|---|
| Static | Python AST, Odoo manifests, XML/ACL, Compose, licencias | código y configuración válidos | G0 |
| Unit | funciones sin IO, cálculo decimal, identidad y estados | importes IGV, serie, reintento | G1/G3 |
| ORM integration | modelos Odoo 19 y transacciones | vender/cobrar/cerrar/revertir stock | G1 |
| Browser E2E | UI Odoo/OWL, teclado, escáner, mensajes | caja→venta→pago→CPE estado→cierre | G1/G2 |
| Fiscal sandbox | UBL, firma, envío, respuesta/consulta según modalidad | boleta, factura, rechazo y CDR | G3 |
| Fiscal productivo autorizado | emisor habilitado y documentos válidos | resultado legal con evidencia y supervisión | G3 |
| Security | auth, multi-tenant, secretos, protección de datos | cross-tenant 0 | G3 |
| Continuity | backup/restore, worker muerto, cola, rollback | RPO/RTO medidos | G4 |
| Performance/chaos | 2 cajas, hasta 2000 SKU, red/proveedor caído | SLA y límites verificables | G1/G4 |
| UX | usuario real no técnico y accesibilidad | tareas sin ayuda crítica | G2 |
| Commercial | soporte, onboarding, CAC, unit economics | costo de atención y pagos reales | G4 |

## 2. Escenarios prioritarios numerados

| Test | RF relacionados | Procedimiento | Resultado exigido | Estado |
|---|---|---|---|---|
| E2E-01 | RF-024 a RF-038 | abrir caja, 2 SKU, cash, factura opcional y cierre | una venta, stock/pago/caja correctos | ORM parcial CI; UI pendiente |
| E2E-02 | RF-034, RF-035, RF-037 | dos confirmaciones de la misma venta | una sola venta, una salida stock | pendiente |
| E2E-03 | RF-024, RF-025 y RF-040 a RF-044 | apertura S/100, ventas, egreso y arqueo con diferencia | saldo esperado y acta justificada | pendiente |
| E2E-04 | RF-019 a RF-022 | 2 cajas venden el último artículo | no doble consumo, política declarada | pendiente |
| E2E-05 | RF-030, RF-046 a RF-065 | factura sin RUC válido, igv no soportado | error previo envío sin falso CPE | pendiente |
| E2E-06 | RF-045 a RF-065 | preparar XML, firmar y enviar autorizadamente | evidencia tributaria por tipo | BLOCKED |
| E2E-07 | RF-054 y RF-057 a RF-059 | timeout posterior a envío posible | estado desconocido, sin duplicación | BLOCKED |
| E2E-08 | RF-060 a RF-062 | rechazo/nota/corrección con origen | histórico preservado y procedimiento válido | BLOCKED |
| E2E-09 | RF-066 a RF-069 | devolución repetida/parcial/deteriorada | no exceso, dinero/stock/fiscal independientes | pendiente |
| E2E-10 | RF-070 a RF-072 | pérdida internet, caché, re-sync dos veces | bloqueo o sincronización única | pendiente |
| SEC-01 | RF-001, RF-002, RF-010, RNF-001 | 2 tenants, lectura/escritura cruzada | denegar todo acceso cruzado | pendiente |
| SEC-02 | RF-045, RF-063, RNF-003 | credenciales expiradas o cruzadas | bloqueo, 0 secretos en logs | BLOCKED |
| OPS-01 | RF-078 a RF-082, RNF-016 a RNF-019 | restaurar DB+filestore y comparar hashes | disponibilidad y datos íntegros | pendiente |
| PERF-01 | RNF-020 a RNF-024 | cargar 2 cajas/2000 SKU | P95 y concurrencia SRS | pendiente |
| UX-01 | RNF-028 a RNF-031 | 5 tareas observadas con usuarios | tasa y tiempos documentados | pendiente |
| BUS-01 | RF-083 y RF-084, RNF-040 | cobrar piloto y medir soporte real | margen sostenible demostrable | pendiente |

**Advertencia:** los rangos RF agrupados son orientativos para navegación; el mapeo autoritativo individual es el CSV. Nunca asignar estado PASSED a un TC por analogía.

## 3. Dataset sintético de aceptación

- Empresa DEMO sin RUC de terceros; DNI/RUC válidos **solo en contextos de prueba autorizados** y sin suplantar contribuyentes.
- SKU CUADERNO 10 PEN neto, 30 unidades; LAPICERO 2,50, 50 unidades; MOCHILA 50, 12 unidades.
- IGV del 18 % cuando aplica perfil base; factura manual 2 × 50 PEN neto = 118 PEN con impuesto 18%, **solo demostración contable**.
- Escenarios: accepted_simulated, rejected_simulated, uncertain_simulated **NO SUNAT**.
- Crear fixtures adicionales para lote/sin stock/descuento/baja/nota/invalidez exclusivamente para comprobar bloqueos, no habilitar funciones fuera alcance.

## 4. Inyección de fallos obligatoria

1. Repetición concurrente de checkout y retry tardío.
2. Corte entre commit Odoo y escritura de outbox.
3. Pérdida de respuesta tras posible recepción en canal fiscal.
4. Certificado inválido, vencido y secreto del tenant equivocado.
5. SUNAT/proveedor caído, respuestas malformadas, error 200 sin aceptación real.
6. Reintento worker luego de reinicio o lease expirado.
7. Cierre de caja con operación draft y diferencia.
8. Stock final vendido por dos cajas.
9. Browser offline/caché borrada/sincronización duplicada.
10. DB restaurada sin filestore o con adjuntos corruptos.
11. Soporte sin autorización intenta acceso a datos personales.
12. Upgrade falla después de migrar esquema, comprobar rollback.

## 5. Formato obligatorio de evidencia

EVIDENCE-ID, commit SHA, versión imagen y addons, etapa, fixture (sintético), precondición, pasos/comando, resultado esperado/real, logs redactados, hashes o capturas si corresponden, actor, fecha, cobertura y ticket del defecto. Toda afirmación de conformidad se vincula desde traceability.csv; reporte de seguridad no incluirá RUC real, certificado, SOL ni PII de clientes.

## 6. Evidencia existente observada

**2026-10-16** · commit 48efd4564891887c6ce89b16f7dd65e369f286c6 · GitHub Actions [38936119080](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080): dos jobs exitosos, DEMO_SEED_OK, DEMO_CHECK_OK, CHECKOUT_SMOKE_OK (abrir, cobrar efectivo, cerrar, 30→29 stock con rollback). Los tests Python simulados del gateway Nubefact fueron verdes en un workflow anterior. Esto **no cubre** browser UX, CPE real, 2 tenants, performance, restauraciones o compliance; ninguna de esas casillas está aprobada.

## 7. Gate de salida

- G0: trazabilidad, derechos, especificación y decisiones críticas aprobadas.
- G1: flujos comerciales, UI, permisos/stock/doble clic, reproducibilidad.
- G2: operación piloto acotada con soporte/seguridad/contrato y limitaciones expresas.
- G3: evidencia tributaria real por modalidad/tipo, outbox, correcciones y seguridad.
- G4: observabilidad, backup/restore, soporte y unit economics reales.

Si hay prueba crítica pendiente: **NO GO** de esa capacidad. No contar tests del simulador como validez ante SUNAT.
