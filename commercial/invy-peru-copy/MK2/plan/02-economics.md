# MK2 — análisis de economía y competencia (hipótesis)

## Precio público observado el 21 de octubre de 2026

| Producto/plan publicado | Precio mensual anunciado, incluido IGV | CPE anunciados | Fuente |
|---|---:|---:|---|
| INVY Pyme | S/169 | 500/mes | https://www.invyperu.com/precios |
| INVY Negocio | S/229 | 1,500/mes | https://www.invyperu.com/precios |
| Alegra POS Emprendedor | S/81 | 250/mes | https://www.alegra.com/peru/punto-venta/precios/ |
| Alegra POS Pyme | S/93 | 1,000/mes | https://www.alegra.com/peru/punto-venta/precios/ |
| Bsale Básico | S/189 | comprobar condiciones exactas | https://www.bsale.com.pe/sheet/precios |
| Bsale Estándar | S/233 | comprobar condiciones exactas | https://www.bsale.com.pe/sheet/precios |

Ofertas del proveedor (SOURCE-REPORTED), no condiciones contractuales verificadas ni pruebas de paridad funcional. La comparación no incluye usuarios, soporte, impuestos/fiscalidad por tipo, pasarela, descuentos anuales, terminales, migración o SLA.

**Inferencia:** vender exclusivamente «POS barato con factura electrónica» no distingue nuestro producto. El dolor de migración/onboarding/operación tendrá que demostrarse, no asumirse.

## Fórmula de contribución

Para precio con IGV al 18 % cuando sea aplicable: ingreso neto ≈ precio / 1.18. Contribución = ingreso neto – hosting – proveedor fiscal/API – tarifas de cobro – horas de soporte valoradas – reserva de incidencias – variables de servicio. Utilidad personal neta requiere aún considerar CAC, onboarding, ingeniería, impuestos aplicables, fijos y reinversión.

Escenarios SOLO DIDÁCTICOS con precio S/169 incluido IGV => neto aproximado S/143.22; hosting ficticio S/20/mes; soporte imputado a S/35/h; costos fiscales ficticios NO obtenidos de Nubefact:

| Escenario | Horas soporte/mes | Costo fiscal hipotético | Contribución parcial |
|---|---:|---:|---:|
| A favorable | 1 | S/0 | S/88.22 |
| B prudente | 2 | S/20 | S/33.22 |
| C complicado | 3 | S/50 | -S/31.78 |

Esos montos no son tarifa sugerida ni estimación de rentabilidad: faltan CAC/onboarding, tarifas de cobro, otros costos, contingencia de incidentes y tributos sobre la renta. Nubefact publicita desde S/70/mes en modo ONLINE con 500 documentos; no conocemos aún la cotización específica para la API de OPeru, de modo que **no** se puede insertar esos S/70 como costo de integración.

Antes de escoger proveedor: pedir, lícitamente, cotización de 1/2/10 tiendas y 100/500/1000 CPE al mes; derechos de licencia, costo por exceso, hosting por tenant, instalación, rotación de certificados, SLAs, costos de reintentos, almacenamiento CDR y soporte nocturno. GO empresarial requiere 2 pilotos legítimamente pagados y mediciones de horas/márgenes reales, no estas tablas.
