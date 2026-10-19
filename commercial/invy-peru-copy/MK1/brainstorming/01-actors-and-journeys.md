# Actores, journeys y tensiones de producto — MK1

**Estado:** diseño conceptual aprobado; sin validación humana aún. **Procedencia:** conversación sobre SRS, diseño maestro, prototipo, viabilidad económica y ejecución local del POS; corte 19/10/2026.

## Tres resultados que justifican el sistema

1. **Experiencia profesional verificable:** ingeniería de producto y plataforma, Odoo 19, contabilidad/operación comercial, resiliencia distribuida, fiscalidad peruana, soporte, contratos y comercialización. La evidencia esperada son pruebas, pilotos, decisiones justificadas y contribuciones lícitas, no volumen de código.
2. **Dinero sostenible:** vender **servicio gestionado**, no revender Odoo sin valor. Hipótesis de suscripción, onboarding y soporte; validar CAC, MRR, retención, costo por cuenta, horas de soporte y margen antes de escalar. Cualquier precio sugerido es hipótesis, nunca ingreso observado.
3. **Ayuda a PyMES peruanas:** menos desorden en caja e inventario, menor tiempo para ubicar comprobantes, decisiones basadas en información y visibilidad clara de incidencias.

## Personas y trabajo real

| Persona | Primera pregunta | Camino prioritario | Fallos que debe comprender |
|---|---|---|---|
| Dueño | ¿Cuánto se vendió y qué debo resolver? | Inicio → alertas → reportes / detalle | Caja diferente; comprobante pendiente; stock bajo |
| Cajero | ¿Puedo cobrar y pasar al siguiente cliente? | Abrir caja → buscar producto → pago → estado → nueva venta | Doble clic; falta de red; pago sin confirmación |
| Supervisor | ¿Qué puedo autorizar sin borrar la historia? | Incidencias → revisar evidencia → aprobar/denegar | Devolución repetida; faltante de caja; reembolso indebido |
| Inventario | ¿Cuánto hay realmente? | Productos → stock → recepción / ajuste con motivo | Concurrencia; stock inexacto; devoluciones dañadas |
| Contador | ¿Qué documentos tienen resultado verificable? | Bandeja fiscal → evento → XML/CDR cuando exista | Rechazo, resultado desconocido, corrección legal |
| Admin del comercio | ¿Estamos listos para operar? | Alta → usuarios → productos → caja → fiscalidad | Certificado/roles/configuración incompletos |
| Soporte autorizado | ¿Cuál es el problema sin acceder de más? | Caso → logs redactados → acción auditada | Datos sensibles, acceso cross-tenant |
| Operador SaaS | ¿Podemos sostener y recuperar a cada cliente? | Provisionar → observar → backup/restore → soporte | Falla de aislamiento, actualización, sobrecostos |

## Journeys de extremo a extremo

**J01. Alta:** descubre → evalúa oferta → acepta condiciones → instancia aislada → configura negocio/PEN/roles → importa productos → prepara tributación → prueba caja → certifica condiciones de producción. Falta un gate fiscal = **demo o servicio acotado**, nunca afirmar emisión legal.

**J02. Venta:** caja abierta → agrega unidades → confirma precio/IGV → elige medio → registra pago conforme a su evidencia → persiste venta → genera solicitud fiscal si procede → muestra tres estados separados: **venta, pago, fiscal**.

**J03. Respuesta fiscal:** preparado → validado → firmado → transmitido por procedimiento aplicable → evidencia recibida o pendiente/desconocida/rechazada → conservar historial, consultar o escalar; no repetir emisión a ciegas.

**J04. Devolución:** encuentra venta → comprueba no duplicado/cantidad disponible → autorización → retorno al stock vendible o segregado → reembolso según fuente → documento correctivo cuando corresponda; tres hechos diferentes, vinculados.

**J05. Cierre:** declara efectivo inicial → movimientos durante sesión → conteo → diferencia → autorización o corrección registrada → cierre auditado. El cierre comercial no resuelve por sí solo incidencias tributarias.

**J06. Red interrumpida:** marcar offline → limitar capacidades a las validadas → persistencia local donde esté demostrado → reanudación con identidad estable y deduplicación → actualización desde servidor. No presumir derecho a emitir CPE fiscalmente offline.

**J07. Salida de cliente:** avisos contractuales → exportación de sus datos/evidencias permitidas → conservar lo exigido legalmente → revocar accesos → eliminar según política; no destruir por suspensión de la suscripción.

## Experiencia UX pactada

Sobria, legible, en español peruano; tres estados del resultado sin un «Listo» ambiguo; prioridad a cobro rápido, accesibilidad y teclado/escáner; las acciones irreversibles requieren permisos y confirmación. Se reutiliza POS nativo primero, personalizando solo ante brecha verificada. Bocetos, navegación y secuencias: [pantallas](../../../retail-peru/design/screen-map.md), [secuencias](../../../retail-peru/design/sequences.md). Casos formales: [UC](../design/use-cases.md).

## Contradicciones que debemos tratar como decisiones, no errores que se esconden

- Full OSS y evitar tarifa variable **vs** proveedor fiscal que acelera tiempo de salida. Investigación comparativa y gate de licencias/regulación antes de escoger.
- POS que pueda seguir sin red **vs** stock/identidades fiscales consistentes. Offline limitado y probado, sin CPE de validez presupuesta.
- Onboarding autoservicio **vs** configuración legal y operativa sensible. Activación productiva requiere verificación.
- Precio asequible **vs** soporte/respaldo por tenant. Medir unit economics, no prometer precios sin margen.
- Agregar módulos de Rally **vs** cerrar primer flujo que genere valor. Rally fuera del MVP y sin tocar repositorio original.

**Próxima evidencia requerida:** entrevistas con propietarios/cajeros; prueba humana S10–S16 y cierre; prueba fiscal bajo autorización; costos/soporte reales.
