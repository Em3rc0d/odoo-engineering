# Sprint de 14 días — secuencia, no promesa temporal

**Objetivo:** pasar de análisis de repositorios a una demo reproducible y a evidencia temprana de demanda. Las duraciones están condicionadas por compatibilidad, recursos y decisiones. Este documento no representa trabajos ya ejecutados.

| Día/s | Trabajo | Evidencia de cierre |
|---|---|---|
| 1–2 | Verificar versión Odoo, licencia, addons Community POS/Stock, separación de Rally, inventario CPE/EDI | MK0/MK1 y DEC-01/02 documentados |
| 1–4 | Prospectar 10 comercios potenciales, identificar sistemas y problemas | Registros anónimos, objeciones y necesidades CPE |
| 3–5 | Ejecutar el lab independiente en `experiments/retail-pos-lab/`, módulo POS/stock, importación 100 SKU ficticios | Logs, comandos, SHA/config y flujos reales |
| 5–7 | Dos instalaciones aisladas, caja, devoluciones, stock, permisos, copia/restauración | Evidencia G1; no datos de clientes |
| 7–9 | Evaluar PSE/OSE / EDI, costo por CPE, certificado y escenarios de rechazo | Proveedor/contrato técnico o bloqueo explícito |
| 9–11 | Demo funcional grabada y oferta acotada; 5 presentaciones útiles | Feedback registrado y objeciones categorizadas |
| 11–14 | Propuesta a primeros candidatos; cerrar alcances pagados condicionados a gates | Pago/compromiso real o PIVOT/KILL |

## No realizar durante el sprint

- No integrar automáticamente Rally al POS ni modificar su snapshot.
- No anunciar facturación electrónica lista sin pruebas reales.
- No vender IA predictiva, multisucursal, marketplace ni un clon completo.
- No desplegar para negocios sin backup, rollback, aislamiento y aceptación.
- No consumir infraestructura comercial ni publicidad pagada sin señales de compra.

## Entregables con ownership

- Ingeniería: demo con evidencia por caso, instalador reproducible y reporte de límites.
- Fiscal: opción contractual/técnica de EDI, costos, estados, contingencias y pruebas autorizadas.
- Comercial: oferta y esquema de soporte, diez entrevistas, dos propuestas piloto.
- Decisión: GO/PIVOT/KILL basada en la matriz y datos recopilados.

**Próxima acción de mayor rendimiento:** contratar/resolver la ruta fiscal y montar un POS demostrable; después buscar compradores reales antes de pulir marca o IA.
