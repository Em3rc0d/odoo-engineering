# Economía comercial — escenario, no ingresos reales

## Punto de referencia

INVY publica S/169/mes **incluido IGV** para su plan Pyme (verificado 2026-10-16). Un competidor sin integración CPE o soporte equivalente no puede presumir que S/149 sea "mejor". Precios de prueba propuestos: S/129, S/169 y S/199 con impuestos incluidos, sujetos a validación.

Con IGV 18% como supuesto para operación gravada, ingresos por suscripción **antes del IGV** = cobro bruto / 1.18. Confirmar régimen tributario y obligaciones reales antes de cotizar.

| Tarifa con IGV | Ingreso sin IGV aproximado |
|---:|---:|
| S/129 | S/109.32 |
| S/169 | S/143.22 |
| S/199 | S/168.64 |

## Modelo por empresa por mes

`MC = precio_igv_incluido / 1.18 - hosting_aislado - proveedor_CPE - comisiones_cobro - soporte_horas * costo_hora - otros_variables`.

`CAC = gastos_comerciales_reales_para_captar / nuevos_clientes_que_pagaron`.

`payback_meses = CAC / MC`, únicamente si MC > 0. No confundir ventas, utilidad, margen, flujo de caja ni valor de contratos.

**Ejemplo hipotético no validado:** a S/169 total, suponiendo S/30 de hosting, S/20 de costos CPE, S/4 de cobro y 1.5 horas de soporte × S/30 = S/45, contribución antes de costos fijos = S/143.22 - S/99 = **S/44.22/mes**. Si soporte sube a 3h, contribución pasa a **-S/0.78/mes**. Estos importes no son precios de proveedores observados.

Si CAC fuera S/200 y la contribución sostenible S/44.22, recuperación teórica ≈ **4.5 meses**, antes de churn, costo fijo e impuestos sobre renta. No usar esta simulación como justificación de inversión.

## Instrumentación desde el piloto

Medir horas de venta/demostración, altas, importación, entrenamiento, soporte, infraestructura, costo por comprobante, tickets, incumplimientos, renovaciones y pagos cobrados. No escalar anuncios ni contratar vendedores hasta tener margen y CAC reales.

## Regla GO

Pilotos con pagos reales + costo total verificable + margen de contribución sostenible positivo + soporte repetible + aceptación SUNAT si se ofrece. Si la economía no cierra, elevar ticket, cobrar implantación transparente, especializar vertical o detener el proyecto.
