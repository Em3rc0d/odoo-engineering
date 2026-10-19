# Plan y línea de carrera — IPC-PLAN-001

**Motivación:** experiencia de ingeniería y empresa + dinero con margen real + ayuda a PyMES. **No hay fechas contractuales ni clientes conseguidos.** La progresión depende de gates con evidencia, no de cantidad de módulos creados.

## Horizonte

| Hito | Qué entregamos | Qué ganamos en experiencia | Valor comercial | Gate |
|---|---|---|---|---|
| MK0 — investigación | ICP, competencia, hipótesis, ruta fiscal a evaluar | entrevistas, TCO, decisión | problema verificable | V0–V5 |
| MK1 — especificación | SRS, UX, dominios, contratos, pruebas y CI de laboratorio | ingeniería, modelado y Odoo real | demo reproducible, no oferta completa | G0 |
| H1 — comercio local | POS, stock, caja, permisos, devoluciones y UI observada | procesos/QA/OWl si hace falta | demo de una tienda | G1 |
| H2 — fiscalidad | EDI legal, XML, firma, evidencia, notas, timeout | regulación e integraciones | oferta CPE solo cuando pase G3 | G3 |
| H3 — SaaS | alta, tenant, backup, restore, TLS, logs, soporte | DevOps/costo/seguridad | soporte repetible | G3/G4 |
| H4 — piloto | 3–5 tiendas con alcance firmado y operador presente | UX, incidencias | primeras ventas comprobadas | G2/G4 |
| H5 — repetición | 10 clientes pagadores, soporte/costo y churn medidos | ventas, pricing y delegación | MRR/margen positivo | G4 |
| H6 — crecimiento | compras, múltiples sedes, pagos/API si demanda pagada | gestión y plataforma | mejores segmentos | nuevo MK/gate |
| H7 — extensión | Rally opcional, verticales, IA con valor demostrado | arquitectura evolutiva | expansión | nuevo proyecto |

**Nota:** ruta técnica fiscal/SaaS puede investigarse en paralelo, pero no declararse «terminada» mientras el conjunto de requisitos y controles no pase.

## Grafo de dependencias y orden de cierre

~~~mermaid
flowchart LR
    ICP["ICP y entrevistas"] --> SRS["SRS / RF / RNF"]
    SRC["Licencias y fuentes"] --> SRS
    SRS --> UX["Flujos UX / dominio"]
    UX --> ARCH["Contratos / datos / permisos"]
    FISCAL["Ruta fiscal y legal"] --> ARCH
    ARCH --> TEST["Plan de pruebas"]
    TEST --> BUILD["Implementación comercial"]
    BUILD --> QA["Pruebas ORM + browser + fiscal + security"]
    QA --> PILOT["Piloto con contrato"]
    PILOT --> GO{"GO / PIVOT / KILL"}
~~~

**Inicio de implementación:** todos los nodos decisivos del grafo cerrados, restricciones documentadas y evidencias exigidas. Los experimentos desechables para cerrar riesgos son distintos de codear un SaaS vendible.

## Trabajo operativo por fase (tickets propuestos)

**G0:** cerrar ICP, tipos CPE, matríz de licencias, modalidad, RPO/RTO costable. **G1:** verificar POS visual, doble clic, dos cajas, stock, devolución, cash discrepancy, protección de roles. **G3:** outbox, firma, envío, CDR/constancia, timeout, notas/boleta, seguridad tenant. **G4:** reproducir aprovisionamiento de 2 tenants, restore, incident response, soporte, margen y pricing. Usar [plan de pruebas](../test/01-master-test-plan.md) como criterio de cierre, no una fecha.

## Oferta y precios: solo hipótesis

Referente competitivo del expediente 16-oct-2026: INVY plan Pyme S/169/mes incl. IGV. Experimentos propios S/129/169/199 incl. IGV + posible setup transparente; no publicar precio contractual sin costos. Formula de contribución: (precio final / 1.18 si gravado a 18%) − hosting − costos fiscales − pasarela − horas soporte × costo/h − otras variables. Medir CAC, payback, churn, incidentes y RPO/RTO.

**Contraste:** a S/169 con IGV y supuestos internos S/30 hosting + S/20 fiscal + S/4 cobros + S/45 soporte, margen ilustrativo de contribución ≈ S/44.22 antes de fijos. Con 3 horas soporte a S/30/h, ese margen se vuelve negativo. No son costos ni ventas observadas.

## KPI triple

**Experiencia:** flujos reproducibles, defectos corregidos, PRs/reviews, cambios con rollback; **negocio:** MRR real, margen, CAC, retención, costo soporte/cliente; **impacto:** minutos cierre, diferencias caja, tiempo de hallar CPE, faltantes, adopción semanal. Evitar vanity metrics.

## Definition of Done por funcionalidad

1. RF/RNF/BR/UC y diseño aprobados.
2. Código con procedencia/licencia, configuración y migración.
3. Tests unit/integration/UI/seguridad y negativos; datos ficticios.
4. Evidencia vinculada a commit/ambiente y reproductibilidad.
5. Runbook de errores, rollback/upgrade, monitoreo y soporte.
6. Evaluación fiscal/legal si corresponde, sin simulaciones vendidas como CPE.
7. Revisión de costos, QA y aceptación responsable.
