# Índice de requisitos y convenciones

El documento canónico [SRS.md](SRS.md) contiene **88 RF y 43 RNF** con criterios observables. [traceability.csv](../test/traceability.csv) contiene una fila por cada ID y su prueba propuesta TC; ninguna prueba se declara ejecutada solo por estar en el CSV.

- UC-01: Alta y configuración
- UC-02: Login y sesión
- UC-03: Catálogo y precios
- UC-04: Recepción/ajuste stock
- UC-05: Apertura y movimientos caja
- UC-06: Venta/cobro POS
- UC-07: Preparar/emitir CPE
- UC-08: Consultar/conciliar fiscal
- UC-09: Rechazo/corrección
- UC-10: Devolución
- UC-11: Cierre de caja
- UC-12: Panel/reportes/alertas
- UC-13: Offline y sincronización
- UC-14: Operación y soporte SaaS
- UC-15: Suscripción
- UC-16: Usuarios/RBAC
- UC-17: Exportación/baja
- UC-18: Cobro externo
- UC-19: Habilitación fiscal
- UC-20: Release/upgrade

Regla de cambios: añadir RF/RNF conservando IDs estables; nunca renumerar un requisito usado por pruebas, incidentes o decisiones. Para cambios breaking, registrar versión y crear nueva referencia controlada.
