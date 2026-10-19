# INVY Perú Copy — expediente de producto independiente

**Corte:** 2026-10-19. **Estado:** modelo y dirección UX aprobados conceptualmente; laboratorio experimental, no SaaS comercial ni emisor certificado. El nombre «COPY» es interno para observar, adaptar y mejorar capacidades legales: nunca copiar software, código, interfaces protegidas, marca, imágenes o bases de datos de INVY.

## Norte
Producto SaaS de punto de venta, inventario, caja y comprobantes electrónicos para pequeños comercios peruanos. Objetivos simultáneos: adquirir experiencia profesional verificable, obtener ingresos recurrentes con margen sostenible y ayudar a PyMES a operar mejor.

## Estructura MK0/MK1

| Flujo | MK0: evidencia, mercado, viabilidad | MK1: especificación, diseño, entrega |
|---|---|---|
| brainstorming | [Visión](MK0/brainstorming/01-vision.md) | [Personas y journeys](MK1/brainstorming/01-actors-and-journeys.md) |
| design | [Segmento y alcance](MK0/design/01-scope.md) | [SRS canónico](MK1/design/SRS.md), [Casos de uso](MK1/design/use-cases.md), [Reglas](MK1/design/business-rules.md) |
| arch | [Opciones y compromisos](MK0/arch/01-options.md) | [Arquitectura](MK1/arch/01-system-architecture.md), [Contratos](MK1/arch/02-contracts-and-states.md), [ADRs y riesgos](MK1/arch/03-decisions-and-risks.md) |
| plan | [Validación](MK0/plan/01-gates.md) | [Carrera del producto](MK1/plan/01-delivery-plan.md) |
| build | [Inventario real](MK0/build/01-assets.md) | [Laboratorio y estado](MK1/build/01-lab-and-integration.md) |
| test | [Hipótesis refutables](MK0/test/01-hypotheses.md) | [Plan maestro](MK1/test/01-master-test-plan.md), [trazabilidad](MK1/test/traceability.csv) |
| quarries | [Extracciones](MK0/quarries/01-extractions.md) | [Brechas](MK1/quarries/01-findings-and-gaps.md) |
| mining-site | [Procedencia y fuentes](MK0/mining-site/01-sources.md) | [Libro de evidencia](MK1/mining-site/01-research-ledger.md) |

## Historia y evidencias consolidadas

- [**Decisiones de la conversación, implementación y pendientes**](CONVERSATION-DECISIONS.md)
- [**MK1 / brainstorming: actores, objetivos y journeys**](MK1/brainstorming/01-actors-and-journeys.md)
- [**MK1 / registro de evidencias de CI y bloqueos**](MK1/test/EVIDENCE-REGISTER.md)

## Regla de verdad

- **Probado:** GitHub Actions [38936119080](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080) 16-oct-2026, Odoo 19 Community: carga POS/inventario, tienda ficticia, venta ORM en efectivo, cierre de caja y stock 30→29 con rollback.
- **Diseñado:** 22 pantallas, siete diagramas de secuencia, escenarios de excepción, oferta por segmento, objetivos SaaS.
- **Pendiente:** prueba humana completa del navegador, emisión SUNAT/XML/CDR real, modalidad legal/certificados, multi-tenant, backup/restore y pilotos/ingresos.

No equiparar respuesta de un simulador a aceptación SUNAT. Venta, pago y resultado fiscal son eventos distintos.

## Código/documentos existentes, sin duplicación

[Matriz competitiva](../retail-peru/parity.json) · [contrato técnico](../retail-peru/technical-contract.md) · [gates](../retail-peru/acceptance-gates.md) · [diseño UX](../retail-peru/design/README.md) · [demo local](../../experiments/retail-pos-lab/DEMO-RUNBOOK.md) · [ADR fiscal histórica](../../integrations/sunat/DEC-PE-EDI-001.md).

El snapshot external/rally/ y el repositorio de origen Rally permanecen intactos. Los módulos de aprendizaje en addons/ no se convierten por inercia en software del producto.
