# Diseño UX/UI — propuesta aprobada conceptualmente

Reutilizar el trabajo existente, no producir un clon de interfaces INVY:
- [Mapa con 22 pantallas, roles y wireframes](../../../retail-peru/design/screen-map.md).
- [Secuencias de venta, rechazo, timeout, devolución, caja, offline y alta](../../../retail-peru/design/sequences.md).
- [Estados y 20 criterios de aceptación](../../../retail-peru/design/states-and-acceptance.md).

## Navegación por rol

**Cajero:** iniciar sesión → abrir caja → buscar/escoger → cobrar → resultado comercial/pago/fiscal → siguiente venta → cierre. **Propietario:** hoy, caja, venta, stock bajo, pendientes, reportes y ayuda. **Contador:** bandeja fiscal y documentos/evidencias. **Supervisor:** autorizaciones, devoluciones, excepciones. **Administrador:** tienda, catálogo, usuarios, dispositivos y configuración. **SaaS:** consola propia de salud, backup, plan y soporte autorizado.

## Componentes UX de arriba hacia abajo

Shell y navegación reducida; buscador/escáner; carrito/total; selector de medio; selección de comprador y documento; confirmación idempotente; estado triple; bandeja de pendientes; detalle con línea temporal; panel caja/arqueo; stock y ajustes; reportes con fecha de corte; onboarding/checklist; soporte sin accesos indiscriminados.

## Interacciones y estados de componentes

- Botón de cobro bloqueado durante envío local + clave de idempotencia en servidor.
- Aviso offline persistente; acciones inseguras deshabilitadas y explicación de caché.
- Documento pendiente/aceptado/rechazado/desconocido, nunca «OK» engañoso.
- Alertas requieren dueño, enlace a evidencia y siguiente paso.
- Formularios con errores en contexto; confirmaciones adicionales en devolución/ajuste/serie/baja.
- Respetar teclado, lector, contraste WCAG AA, feedback sin animaciones distractoras, tamaño táctil y estados vacíos.

## Validación visual

Probar en caja de escritorio con teclado/escáner y tableta a resoluciones definidas. Medir tiempo de abrir caja, añadir 3 artículos, registrar un pago manual, localizar un CPE incierto y cerrar caja. Diseño semántico versionado, tokens, componentes y regresión visual antes de customizar OWL. No implementar pantallas extra si Odoo Community existente resuelve adecuadamente el caso.

## Decisiones abiertas

¿Rubro/cantidad SKU? ¿lector/impresora/terminal? ¿cerrar caja con diferencias? ¿requerimos factura POS en el primer piloto? ¿Qué puede hacer un cajero sin internet? ¿Configuración sin asesor? ¿Accesibilidad con hardware real? El SRS define requisitos; esta UX no elimina gates técnicos.
