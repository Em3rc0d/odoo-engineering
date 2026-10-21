# Design — diferenciación medida por tarea, no por características

El SRS MK1 sigue siendo el contrato. No se autoriza una pantalla adicional en esta etapa.

| Tarea crítica | Observación que necesitamos | Condición mínima de ensayo |
|---|---|---|
| Onboarding 100 SKU | Tiempo, errores, repetición | Importación con previsualización y errores por fila |
| Apertura/cierre efectivo | Saldo esperado, diferencia, actor | El arqueo no modifica cifras históricas |
| Pago Yape/Plin | Declaración de cajero vs verificación externa | Etiqueta MANUAL sin simular pago bancario |
| Doble clic en venta | Venta/cobro/stock de la misma operación | Una sola salida física y un pago |
| Venta a factura/CPE | Estado de venta vs fiscal | SIMULADO jamás equivale a CDR |
| Interrupción de red | ID, reconsulta y estado incierto | Ningún correlativo nuevo en reintento incierto |
| Salida de plataforma | Datos y adjuntos exportables | Restore y formato portable verificables |

Medir tasa de tareas completadas, minutos, incidentes, ayuda requerida, cantidad de errores y tiempo de soporte; no fijar mejoras porcentuales antes de tener una línea base.

No copiar pantallas ni nombres protegidos de INVY o de clientes de Thradex. Usar diseño original con validación visual y accesibilidad.
