# Retail Perú — competencia directa por etapas

**Fecha de investigación:** 2026-10-16. **Estado:** MK0/MK1 comercial en evaluación, sin GO de producto listo ni operaciones de clientes.

## Tesis y objetivo

Crear una solución propia de gestión comercial para pequeñas tiendas peruanas usando Odoo Community 19 como sistema de registro, con instalación repetible, onboarding asistido y soporte medible. INVY es una referencia competitiva, no una fuente de código. No se copiarán su marca, materiales ni elementos protegidos.

**Meta inmediata:** dos pilotos pagados con alcance explícito y una misma versión desplegable. **Meta de competencia directa:** ofrecer venta + caja + inventario + facturación electrónica integral validada con SUNAT; hasta entonces, competir solo por subcasos de POS e inventario y ser transparentes con cualquier brecha.

## Evidencia pública (no confundir marketing con auditoría técnica)

- [INVY precios](https://www.invyperu.com/precios): Pyme S/169, Negocio S/229, Corporativo S/289 mensuales, IGV incluido; 1/2/3 sucursales, 500/1500/2000 documentos; acceso de 15 días sin tarjeta, usuarios y SKU ilimitados declarados.
- [INVY portada](https://www.invyperu.com/): anuncia POS, caja, stock, factura/boleta/notas de crédito SUNAT, catálogo, IA y medios de pago. Estas son declaraciones comerciales, no tests contra una cuenta.
- INVY describe la integración SUNAT como uno de los puntos centrales de valor. **No** vender "equivalencia 1:1" sin pruebas de cada flujo y límites.
- [Odoo 19 documentación Perú](https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html): enumera `l10n_pe`, `l10n_pe_edi`, `l10n_pe_pos`. Que aparezca en la documentación no demuestra que EDI esté disponible en nuestro checkout Community ni habilitado para nuestro flujo.
- [Odoo 19 flujo POS offline](https://www.odoo.com/documentation/19.0/applications/sales/point_of_sale/use.html): permite transacciones POS offline bajo condiciones, pero no factura ni sincroniza stock en tiempo real desconectado.
- [SUNAT - PSE](https://cpe.sunat.gob.pe/aliados/pse): los PSE están sujetos a acreditación/homologación; usar o integrar un proveedor no equivale a ser PSE.

**Inconsistencia pública a investigar:** INVY anuncia cuotas mensuales de créditos IA y una FAQ habla de "IA ilimitada". Registrar condiciones actuales contractuales antes de comparar uso real; no inferir fraude ni cumplimiento.

## Separación del repositorio

- `addons/` contiene experimentos y módulos Odoo no validados: **no** incluirlos en la distribución comercial por inercia.
- `external/rally/` conserva exactamente su snapshot original: usar ideas/patrones solo cuando corresponda; Rally no es motor POS ni sube a producción con el producto inicial.
- `commercial/retail-peru/` es **la especificación de producto** y un repositorio de decisiones para go-to-market; no contiene componentes listos para despliegue.

## Laboratorio técnico disponible (sin pruebas ejecutadas)

Se añadió [experiments/retail-pos-lab](../../experiments/retail-pos-lab/README.md): entorno aislado reproducible en Docker con Odoo 19 y PostgreSQL, independiente de Rally, solo para evaluación. No incluye POS preconfigurado, facturación SUNAT ni onboarding de clientes: esas son pruebas/gates posteriores.

## Documentos de trabajo

1. [Matriz de paridad](parity.json) — 22 capacidades y grado de evidencia.
2. [Oferta y cliente inicial](offer-and-icp.md) — segmento, servicios, posicionamiento, precio experimental.
3. [Contrato de producto/arquitectura](technical-contract.md) — sistema de registro, aislamiento, SUNAT y dependencias.
4. [Escenarios y puertas de salida](acceptance-gates.md) — demo, piloto, competencia directa y escala.
5. [Experimento comercial](sales-experiment.md) — entrevistas, demostraciones, pricing y mediciones.
6. [Plan de 14 días](execution-plan.md) — responsabilidades, entregables y bloqueadores.
7. [Economía del negocio](unit-economics.md) — margen, CAC, tiempo de soporte e hipótesis.

## Decisión

**GO: investigación específica + demo técnica acotada en entorno desechable + ventas de descubrimiento.**
**NO GO: vender un POS integral con facturación SUNAT antes de integración real y aceptación.**
**NO GO: desarrollar IA, catálogo, multisucursal o generar un clon visual idéntico antes de cerrar operaciones y compradores.**

## Diseño de experiencia y operación (DUX-001)

Se añadió un [paquete de diseño visual y recorridos](design/README.md) con [mapa de pantallas y bocetos](design/screen-map.md), [siete diagramas de secuencia](design/sequences.md), [estados y criterios de aceptación](design/states-and-acceptance.md), [componentes y contratos](design/component-map.md) y [línea de carrera](design/roadmap-and-outcomes.md). **Es una propuesta sin pruebas de producción**, alineada con la decisión fiscal provisional OPeru + Nubefact y los gates G0–G4.
