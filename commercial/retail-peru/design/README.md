# Diseño de experiencia y operación — Retail Perú (DUX-001)

**Versión:** 0.1, propuesta para revisión (2026-10-16). **Estado:** diseño, no software implementado ni prueba de producción.

## Para qué sirve este paquete

Pasar de una idea de ERP/POS a recorridos verificables de personas reales: cajero, dueño, supervisor, contador, administrador del negocio y soporte. El primer segmento propuesto es una tienda minorista peruana, un RUC, una sede y una o dos cajas; el rubro final depende de entrevistas.

**Promesa al comerciante:** vender con sencillez, entender caja y stock, y conocer el estado verdadero de sus comprobantes. No se promete emisión tributaria lista, funcionamiento offline sin límites ni paridad con INVY.

## Cómo leerlo

1. [Mapa de pantallas](screen-map.md): qué ve cada persona, a dónde navega y bocetos de las pantallas críticas.
2. [Secuencias usuario–sistema–canal fiscal](sequences.md): siete recorridos normales y de falla, con diagramas Mermaid.
3. [Estados, excepciones y criterios de aceptación](states-and-acceptance.md): mensajes, invariantes y escenarios de prueba.
4. [Mapa de componentes y contratos](component-map.md): qué construimos encima de Odoo y qué sistema posee cada dato.
5. [Línea de carrera del producto](roadmap-and-outcomes.md): aprendizaje, rentabilidad e impacto en PyMES; hitos con puertas de salida.

Documentos existentes: [contrato técnico](../technical-contract.md), [gates G0–G4](../acceptance-gates.md), [matriz competitiva](../parity.json), [decisión fiscal provisional](../../../integrations/sunat/DEC-PE-EDI-001.md).

## Tres hechos distintos

- **Venta:** existe una operación comercial persistida por Odoo.
- **Cobro:** existe un registro del medio de pago, manual o confirmado por un tercero según corresponda.
- **Comprobante:** existe una solicitud fiscal con un estado respaldado por evidencia del canal correspondiente.

El sistema nunca convertirá «enviado», «HTTP 200» o «proveedor informa éxito» en «aceptado por SUNAT» sin comprobar la evidencia y el procedimiento aplicables. Una boleta, una factura y sus correcciones pueden tener circuitos diferentes.

## Límites de arquitectura

- Odoo Community 19 es la fuente de verdad comercial: POS, clientes, productos, stock, caja y documentos comerciales/contables.
- La integración fiscal es una frontera explícita. La prioridad **provisional** del repositorio es evaluar OPeru 19 + Nubefact; Greenter queda como alternativa de investigación, no elección aprobada.
- El adaptador experimental actual de Nubefact y sus pruebas simuladas **no** demuestran un flujo Odoo→SUNAT productivo.
- SaaS: base, filestore y secretos separados por cliente, sujeto a pruebas reales de aislamiento y restauración.
- Rally permanece separado del MVP y no se modifica ni se instala como addon Odoo.
- Las pantallas son **contratos de experiencia propuestos**, no afirmaciones de que Odoo Community incluya hoy cada vista sin adaptación.

## Cómo pasar del diseño a ingeniería

Revisar estos recorridos con al menos un cajero y un propietario; decidir los puntos abiertos; vincular cada caso UC y prueba T al identificador **real** de RF/RNF del SRS cuando el SRS esté versionado. No inventamos identificadores de SRS. Prototipar las pantallas críticas; luego comprobarlas contra Odoo 19 real en el laboratorio. Ningún diagrama sustituye pruebas de instalación, seguridad o fiscalidad.
