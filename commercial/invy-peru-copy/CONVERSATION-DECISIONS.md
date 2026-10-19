# Memoria de decisiones y estado de evidencia — INVY Perú Copy

**Corte:** 19/10/2026. Documento de transferencia para humanos/agentes; no constituye transcripción literal ni SRS alternativo. Las decisiones más recientes pueden modificar prioridades, pero no convierten una hipótesis en hecho comprobado.

## Histórico de esta línea de trabajo

| Hito | Lo pedido / acordado | Estado | Ubicación canónica |
|---|---|---|---|
| Investigación | Evaluar negocio tipo INVY en Perú, con diferenciación y aprendizaje | Expediente comercial y matriz, mercado por validar | [Retail Perú](../retail-peru/README.md), [MK0](MK0/README.md) |
| Ingeniería base | Odoo 19 Community + PostgreSQL, reutilizar ERP y evitar escribir un ERP entero | Baseline técnica probada en laboratorio | [Arquitectura](MK1/arch/01-system-architecture.md) |
| Fiscal inicial | Contrato candidato Nubefact y evaluación OPeru 19 | Gateway simulado; integración legal no probada | [ADR histórico](../../integrations/sunat/DEC-PE-EDI-001.md) |
| Preferencia nueva | **No exigir cuenta Nubefact** si se puede usar OSS/free; evaluar Greenter PHP y SUNAT directo | **Preferencia fuerte; gate legal y técnico abierto** | [Decisiones](MK1/arch/03-decisions-and-risks.md) |
| SRS galáctico | Requisitos medibles, alcance explícito, RF/RNF, errores, abuso, casos y pruebas | [SRS v0.9](MK1/design/SRS.md) propuesto, no certificado/firmado | [SRS](MK1/design/SRS.md), [UC](MK1/design/use-cases.md) |
| Diseño completo | Persona–sistema–SUNAT, pantallas, componentes, estados, excepciones | Modelo/prototipo **conceptualmente aceptados** | [Pantallas](../retail-peru/design/screen-map.md), [secuencias](../retail-peru/design/sequences.md) |
| Línea de carrera | Ganar experiencia, dinero y ayudar a PyMES peruanas | Objetivos definidos; métricas reales pendientes | [Roadmap](MK1/plan/01-delivery-plan.md), [journeys](MK1/brainstorming/01-actors-and-journeys.md) |
| Acción real | Arranque automático local de POS, caja, inventario y simulación de CPE | Workflow CI verde **48efd45**; UI humana pendiente | [Demo](../../experiments/retail-pos-lab/DEMO-RUNBOOK.md) |
| Encargo actual | Consolidar en **odoo-engineering/invy-peru-copy**, MK0/MK1 con brainstorming/design/arch/plan/build/test/quarries/mining-site | Expediente consolidado; este documento agrega trazabilidad y huecos | [Índice](README.md), [estado](STATUS.md) |

## Qué se construyó realmente

- Addon local **oe_pe_cpe_lab**: factura Odoo contabilizada a payload restringido y respuesta local simulado (aceptado/rechazado/timeout), con unicidad local. **No SOAP SUNAT, XML UBL firmado ni CDR**.
- Laboratorio Docker Odoo Community 19/Postgres 16: localización PE, instalación POS, tres SKU ficticios, IGV 18%, inventario, pagos efectivo/Yape–Plin manual, apertura y cierre de caja.
- Comando `bash scripts/lab.sh demo-setup` y test `checkout-smoke` de venta/cobro/arqueo/stock, con rollback. CI aprobado: [ejecución 38936119080](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080), SHA `48efd4564891887c6ce89b16f7dd65e369f286c6`.
- Documentación de diseño con pantallas, siete secuencias, estados e hipótesis de arquitectura/costos. No es evidencia de piloto, ingresos ni paridad de INVY.

## Restricciones de gobernanza

1. Requisitos y arquitectura se formalizan antes de añadir features productivos: brainstorming → design → arch → plan → build → test; extracción desde quarries y fuentes en mining-site.
2. MK0 no aprueba comercialización sin mercado/costos/cumplimiento. MK1 documenta objetivo, no indica que todo RF esté implementado.
3. El nombre **«INVY Perú Copy» es un alias interno** de benchmarking; no copiar marca, código, imagen, diseño protegido, API privada o datos ajenos. Comercialmente se requerirá nombre propio.
4. Elegir licencia por archivo/dependencia; Community/Greenter open source no convierte los servicios, cumplimiento y operación en coste cero.
5. No copiar Rally a runtime: snapshot en `external/rally/` y upstream `em3rc0dTh/Rally` deben quedar intactos.
6. No subir claves, certificados, RUC reales, claves SOL o CDR privados. Producción SUNAT deshabilitada hasta gate.
7. No mezclar **venta registrada**, **pago registrado/confirmado** y **aceptación fiscal acreditada**.

## Gates bloqueantes en curso

- **MERCADO:** entrevistados y primeros pilotos con evidencia independiente, segmento y disposición a pagar.
- **FISCAL:** modalidad por contribuyente, PSE/OSE/SEE, certificado, boleta/factura/notas, XML firmado, consulta ante timeout, resultado y evidencia verificados; decidir Greenter directo vs proveedor con TCO y licencias.
- **OPERACIÓN:** aislamiento tenant, restauración DB+filestore, seguridad/secretos, SLA y soporte.
- **UX:** prueba visual real del flujo POS→factura→simulador y excepciones.
- **COMERCIAL:** precio, márgenes, retención, costos de soporte e implementación contractual.

**Puerta actual:** GO para laboratorio y validación; NO GO para emisión fiscal productiva o venta como SaaS integral.
