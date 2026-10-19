# SRS — Plataforma independiente POS/ERP Retail Perú

**Identificador:** IPC-SRS-001 · **Versión:** 0.9 propuesta · **Fecha:** 2026-10-19 · **Estado:** alcance global de diseño aprobado, requisitos específicos pendientes de revisión/firmas · **Base:** ISO/IEC/IEEE 29148 adaptada a nuestro flujo documental. Este documento no acredita cumplimiento SUNAT ni producción.

## 1. Propósito y criterio de éxito

Describir de forma trazable qué debe hacer el producto y qué calidad debe alcanzar. **Triple objetivo:** experiencia verificable de arquitectura/operación/comercialización; ingresos recurrentes con contribución positiva; mayor control y menos errores para PyMES peruanas. Las decisiones se cierran con evidencia, no con entusiasmo.

**Actores:** dueño/propietario, cajero, supervisor, inventario, contador, administrador del negocio, soporte autorizado, operador SaaS, canal fiscal SUNAT/tercero, pasarela de pago externa cuando exista. **Segmento inicial propuesto:** tienda minorista formal, un RUC, una sede, 1–2 cajas, unidades físicas, moneda PEN, IGV 18% gravado; rubro a confirmar. Idioma español, zona horaria Lima.

## 2. Alcance explícito

### 2.1. En el MVP comercial objetivo, condicionado a gates

- Alta y configuración estandarizadas de contribuyente/tienda, usuarios y permisos; importación de productos.
- POS web, búsqueda de productos, carrito, registro de efectivo y transferencias manuales, comprobación del cobro con evidencia adecuada.
- Sesiones de caja, apertura, ingresos/egresos, arqueo, diferencias, cierre y reporte diario.
- Inventario y stock por movimientos del ERP, ajustes auditados, alertas básicas y devoluciones permitidas.
- Emisión, consulta, corrección y custodia de CPE aplicables (boleta/factura/notas) **solo tras demostrar y autorizar** modalidades y cumplimiento; XML, firma, respuesta y evidencias cuando correspondan.
- Aislamiento SaaS por empresa, onboarding, TLS, backups probados, monitoreo, soporte, exportación y suscripción simple.
- UX con estados distintos para venta comercial, pago y documento fiscal; diagnóstico accionable ante errores.

### 2.2. MVP LOCAL DEMO (lo que existe hoy, distinto del objetivo comercial)

Odoo 19 Community + PostgreSQL, localización peruana, productos ficticios, POS/caja/inventario probados por ORM en CI y simulador CPE no fiscal. **No** es un emisor habilitado. El script checkout_smoke.py revierte la transacción; las pruebas visuales y el flujo POS→factura→simulador deben ejecutarse aparte.

### 2.3. Fuera del MVP comercial

Restaurantes con mesas/comandas, farmacias y productos regulados, combustible, contabilidad universal, IGV exonerado/inafecto/ISC/percepciones o créditos complejos no validados, guías de remisión electrónica y SIRE integral, contabilidad de grupos multi-RUC, IA autónoma, multimoneda, e-commerce/marketplaces, multisucursal compleja, lotes/caducidades controlados, pagos bancarios integrados por defecto, impresión especializada no validada, fiscalización automatizada, offline fiscal universal, Rally como parte del ERP, clon 1:1 de INVY. Se incorporarán solo mediante versión/gate posterior y cambio del SRS.

### 2.4. Delimitación legal y económica

Greenter + SUNAT directo es opción preferida para investigar por control/OSS; OPeru+Nubefact figura como opción histórica provisional. **Ninguna ruta se adopta ni se garantiza S/0 de operación** sin licencia, compatibilidad, contribuyente habilitado, prueba fiscal y TCO. PSE ≠ OSE ≠ SEE del contribuyente. Un ticket POS o estado SIMULADO **no es** CPE legal. Información de consumidor, certificados y RUC se protegen por controles/contratos aplicables.

## 3. Contexto, supuestos y dependencias

- Odoo Community 19: fuente transaccional para venta, cuenta, caja, productos, stock y contabilidad soportada.
- PostgreSQL: persistencia; filestore separado. No escribir directamente a tablas Odoo desde el motor fiscal ni Rally.
- Integración fiscal desacoplada y segura, con cola/outbox durable, identidad, firma, estado y evidencias; elección de adaptador abierta.
- SaaS: una DB + filestore + secretos por tenant como hipótesis inicial. Confirmar escalabilidad/costos y pruebas negativas.
- Cálculos en PEN, IGV 18% del régimen restringido al inicio. Reglas exactas/regulación deben verificarse antes de emitir.
- Dependencia de internet y disponibilidad del canal; no reintento ciego ante timeout. Flujo offline del POS es limitado.
- Hardware objetivo: navegador de escritorio/tableta compatible, lector de código de barras opcional. Impresoras y terminales sin validación, fuera del compromiso.
- Cambios de ley o esquema SUNAT obligan a revalidar contratos fiscales y actualizar tests.
- **Seguridad de fuentes:** solo datos sintéticos en laboratorio y CI. Cero secretos reales en git, logs o screenshots.

## 4. Definiciones operativas

**Venta registrada:** operación persistida por Odoo. **Pago registrado manualmente:** declaración del cajero, no confirmación de entidad financiera. **Pago confirmado externamente:** evidencia verificada del procesador. **CPE pendiente:** solicitud sin resultado fiscal concluyente. **Aceptación fiscal:** solo evidencia apropiada al documento/modalidad. **Resultado desconocido:** envío posiblemente recibido pero sin constancia verificable. **Tenant:** cliente SaaS aislado; no equivale necesariamente a una sola cuenta de usuario. **Idempotencia:** repetición de una misma acción no duplica efectos.

## 5. Prioridad y verificación

M = Must para oferta comercial delimitada; S = Should, incorporable solo si no compromete Must. Los RF marcados Must sobre SUNAT son **gates de comercialización**, no afirmaciones de que ya estén implementados. Cada requisito se verifica con TC-RF-nnn y evidencia por release en traceability.csv. Criterio de aceptación redactado como resultado observable; casos UC describen precondiciones, flujos y fallos.

## 6. Requisitos funcionales (RF)

| ID | Prioridad | Requisito verificable | Aceptación mínima observable | Caso |
|---|---|---|---|---|
| RF-001 | M | Registrar tenant con identidad única y estado de ciclo de vida | Dos altas iguales retornan el tenant original; no duplicación | UC-01 |
| RF-002 | M | Crear entorno aislado por tenant con DB y filestore dedicados | Tenant A no accede a datos/archivos de B | UC-01 |
| RF-003 | M | Controlar alta contractual y aceptación de tratamiento de datos | Sin consentimiento/base legal o contrato requerido no se activa | UC-01 |
| RF-004 | M | Configurar razón social, RUC, país, PEN y zona horaria Lima por cliente | No pasar a producción con campos fiscales obligatorios incompletos | UC-01 |
| RF-005 | M | Mantener estado DEMO separado de instancia tributaria productiva | Toda demo visible como ficticia y no envía CPE | UC-01 |
| RF-006 | M | Crear administrador inicial mediante canal seguro | Credencial inicial única, no compartida y rotada al primer uso | UC-01 |
| RF-007 | M | Registrar checklist de configuración e hitos de onboarding | Se conoce responsable/fecha de cada bloqueo | UC-01 |
| RF-008 | M | Permitir diagnóstico de readiness sin modificar datos | Check devuelve lista de pendientes y evidencias | UC-01 |
| RF-009 | M | Autenticar usuarios y manejar sesiones con expiración | Sesión inválida no abre POS ni API | UC-02 |
| RF-010 | M | Aplicar roles: propietario, cajero, supervisor, inventario, contador, admin y soporte | Acciones denegadas sin rol y auditadas | UC-16 |
| RF-011 | M | Aplicar permisos por empresa, caja y tenant | Usuario A no lee ventas/secretos de empresa B | UC-16 |
| RF-012 | M | Revocar usuarios y sesiones ante baja o incidente | Nueva petición con sesión revocada falla | UC-16 |
| RF-013 | S | Mostrar ayuda contextual para tareas frecuentes | Desde caja se accede a la guía pertinente sin perder venta | UC-02 |
| RF-014 | M | Crear producto con SKU, nombre, unidad, precio e impuesto | Faltan atributos mínimos: no se publica en POS | UC-03 |
| RF-015 | M | Importar catálogo con vista previa de validaciones | 100 SKU ficticios: filas inválidas reportadas sin duplicar | UC-03 |
| RF-016 | M | Actualizar precios con permisos y registro de cambios | Cambio no altera valores históricos de ventas pagadas | UC-03 |
| RF-017 | M | Definir visibilidad de producto en punto de venta | Producto inactivo/no autorizado no aparece en caja | UC-03 |
| RF-018 | M | Configurar impuestos por línea según alcance gravado 18% | Se rechazan perfiles fuera del MVP fiscal sin cálculo ambiguo | UC-03 |
| RF-019 | M | Configurar y consultar existencias por almacén interno | Disponible corresponde a movimientos Odoo, no cifra inventada | UC-04 |
| RF-020 | M | Registrar recepción o ajuste con motivo y actor | Stock cambia una vez y conserva movimiento asociado | UC-04 |
| RF-021 | M | Evitar doble aplicación de carga o ajuste con clave única | Repetir importación no duplica inventario | UC-04 |
| RF-022 | M | Aplicar política explícita para venta sin stock | Bloqueo/admisión sigue configuración documentada | UC-06 |
| RF-023 | S | Alertar umbral de stock bajo sin modificar compras | Se muestra umbral/producto/fecha de corte | UC-12 |
| RF-024 | M | Abrir una sesión de caja por cajero/configuración compatible | No permite sesiones incompatibles abiertas | UC-05 |
| RF-025 | M | Registrar efectivo inicial y usuario responsable | Apertura conserva monto, tiempo y actor | UC-05 |
| RF-026 | M | Exigir sesión abierta al realizar cobro | Caja cerrada redirige a apertura o bloquea operación | UC-06 |
| RF-027 | M | Buscar producto por nombre, SKU y código de barras si existe | Búsqueda produce precios/impuestos correctos | UC-06 |
| RF-028 | M | Calcular subtotal, IGV y total reproduciblemente | Se verifica contra motor de impuestos de Odoo y moneda PEN | UC-06 |
| RF-029 | M | Modificar cantidades con límites y permisos | Cantidad inválida no produce venta ni stock | UC-06 |
| RF-030 | M | Seleccionar comprador cuando sea obligatorio para documento | Factura sin identificación compatible no continúa | UC-06 |
| RF-031 | M | Registrar pagos en efectivo correctamente | Venta completa se concilia contra pago registrado | UC-06 |
| RF-032 | M | Registrar Yape/Plin como medio manual sin fingir confirmación externa | UI/registro dicen MANUAL, nunca confirmado por entidad | UC-06 |
| RF-033 | S | Permitir otros medios de pago configurados sin asumir conciliación bancaria | Estado de confirmación depende de evidencia del proveedor | UC-18 |
| RF-034 | M | Asegurar idempotencia de confirmar venta con clave persistente | Doble clic/repetición genera una sola venta, pago y salida stock | UC-06 |
| RF-035 | M | Recuperar resultado después de cierre de navegador o timeout | Al reabrir se consulta ID original antes de repetir | UC-06 |
| RF-036 | M | Persistir venta con líneas, impuestos y referencias | Se puede reconstruir total original desde registros | UC-06 |
| RF-037 | M | Evitar stock duplicado en reintentos de venta | Cantidad física desciende exactamente una vez | UC-06 |
| RF-038 | M | Mostrar por separado estado comercial, de pago y fiscal | No existe «todo aceptado» por pago manual/HTTP 200 | UC-06 |
| RF-039 | M | Permitir consulta histórica de ventas y filtros | Por ID/fecha se recupera venta autorizada | UC-12 |
| RF-040 | M | Registrar movimientos extraordinarios de caja autorizados | Cada ingreso/egreso tiene causa y actor | UC-05 |
| RF-041 | M | Calcular efectivo esperado por sesión | Total igual a saldo inicial + movimientos/ventas efectivo pertinentes | UC-11 |
| RF-042 | M | Comparar conteo físico con efectivo esperado | Diferencia exacta se muestra sin alteración del esperado | UC-11 |
| RF-043 | M | Solicitar justificación y supervisor según umbral | Cierre no se fuerza sin autorización requerida | UC-11 |
| RF-044 | M | Cerrar caja con acta inmutable y trazable | Estado cerrado no admite edición informal de operaciones pasadas | UC-11 |
| RF-045 | M | Configurar emisor y modalidad fiscal independiente de caja | No se habilita emisión con emisor no autorizado | UC-19 |
| RF-046 | M | Validar documentos comprador/emisor según tipo y legislación | Factura con RUC inválido resulta error previo al envío | UC-07 |
| RF-047 | M | Determinar tipo fiscal 01/03 según solicitud y reglas | Factura y boleta usan validaciones diferenciadas | UC-07 |
| RF-048 | M | Controlar serie y correlativo por emisor y tipo | Dos cajas no generan igual identidad fiscal | UC-07 |
| RF-049 | M | Generar solicitud fiscal durable asociada a venta/documento | Se mantiene identificador y payload al reiniciar worker | UC-07 |
| RF-050 | M | Crear payload fiscal desde snapshot validado de operación | Montos/fecha/documento no cambian silenciosamente tras firma | UC-07 |
| RF-051 | M | Generar XML UBL por modalidad habilitada | Validación de esquema y reglas supera tests por tipo | UC-07 |
| RF-052 | M | Firmar XML con certificado autorizado del contribuyente/canal | Firma validable sin revelar clave privada en logs | UC-07 |
| RF-053 | M | Enviar por canal y mecanismo tributario correspondiente | Respuestas de transporte no se etiquetan aceptación final | UC-07 |
| RF-054 | M | Registrar eventos de envío, respuestas y códigos | Consulta muestra línea temporal e identidad estable | UC-08 |
| RF-055 | M | Conservar XML, CDR/constancia y representación imprimible cuando apliquen | Archivos con hash, retención y acceso controlados | UC-08 |
| RF-056 | M | Mostrar estado fiscal sustentado en evidencia aplicable | Aprobación simulada se muestra solo como SIMULADA | UC-08 |
| RF-057 | M | Mantener resultado desconocido cuando envío puede haber llegado | Timeout no dispara nuevo documento/correlativo automático | UC-08 |
| RF-058 | M | Consultar estado en proveedor/SUNAT si la modalidad lo permite | Reconciliación actualiza misma identidad fiscal | UC-08 |
| RF-059 | M | Reintentar únicamente operaciones seguras según política documentada | No hay reenvío ciego ante incertidumbre | UC-08 |
| RF-060 | M | Notificar rechazo con código y próximo paso | Venta persiste y usuario autorizado ve incidencia | UC-09 |
| RF-061 | M | Gestionar subsanación sin editar XML firmado anterior | Nueva operación/estado conserva vínculo y evidencia | UC-09 |
| RF-062 | M | Tramitar nota de crédito y correcciones permitidas en fase fiscal comercial | Regla legal/tipo/referencia comprobados, o gate bloquea | UC-09 |
| RF-063 | M | Distinguir mecanismos de boleta/factura/resumen según régimen | No presupone CDR individual idéntico para todos los documentos | UC-07 |
| RF-064 | M | Prevenir credenciales/certificados de otro tenant | Solicitud falla ante emisor/credencial cruzados | UC-19 |
| RF-065 | M | Alertar antes de vencimiento de certificado y bloquear cuando corresponda | Emisión inválida queda pendiente sin fuga de secretos | UC-19 |
| RF-066 | M | Recuperar venta original para devolución con histórico | No se puede devolver venta inexistente | UC-10 |
| RF-067 | M | Prohibir devoluciones acumuladas superiores a lo vendido | Segunda devolución excedente se rechaza | UC-10 |
| RF-068 | M | Requerir autorización para devoluciones sensibles | Actor, motivo y fecha preservados | UC-10 |
| RF-069 | M | Separar retorno físico, reembolso monetario y corrección fiscal | Tres resultados aparecen independientes | UC-10 |
| RF-070 | S | Administrar operación offline solo en escenarios verificados | Sin conexión se informa alcance y riesgo de caché | UC-13 |
| RF-071 | M | Deduplicar al sincronizar operaciones offline permitidas | Repetir sincronización no crea venta duplicada | UC-13 |
| RF-072 | M | Bloquear emisión fiscal offline sin contingencia aprobada | No se imprime etiqueta de CPE válido por falla de red | UC-13 |
| RF-073 | M | Dar resumen del día con ventas, medios, caja y cortes temporales | Suma demostrable y período de datos explícito | UC-12 |
| RF-074 | S | Destacar stock bajo, rechazos e inciertos con acciones | Alerta posee enlace a detalle/responsable | UC-12 |
| RF-075 | M | Permitir exportación de datos propios del cliente | Datos/casos exportables conforme a permisos/retención | UC-17 |
| RF-076 | M | Registrar auditoría de operaciones sensibles | Cambio de rol, serie, caja, CPE y soporte atribuibles | UC-16 |
| RF-077 | M | Notificar incidencias críticas a responsables | Incidencias no quedan escondidas tras una venta | UC-12 |
| RF-078 | M | Aprovisionar base, filestore y secretos repetiblemente | Dos altas independientes no comparten secretos ni backups | UC-14 |
| RF-079 | M | Respaldar DB, filestore y configuración crítica conjuntamente | Conjunto de copias íntegro con puntos de restauración | UC-14 |
| RF-080 | M | Restaurar tenant en ambiente aislado y verificarlo | Restore drill demuestra acceso, datos y adjuntos | UC-14 |
| RF-081 | M | Gestionar acceso de soporte delegado y temporal | Acceso exige autorización, expira y queda auditado | UC-14 |
| RF-082 | S | Mostrar salud y errores por tenant sin exponer ventas privadas | Panel solo muestra métricas operativas autorizadas | UC-14 |
| RF-083 | M | Aplicar ciclo de suscripción, mora y suspensión con retención | No se elimina evidencia fiscal por falta de pago | UC-15 |
| RF-084 | M | Registrar precio, impuestos, comisiones y soporte por cuenta | Contribución mensual rastreable para análisis financiero | UC-15 |
| RF-085 | M | Generar logs estructurados con IDs de correlación, sin secretos | Caso se investiga con request/documento/tenant | UC-14 |
| RF-086 | M | Mantener procedimientos versionados de upgrade/rollback | Upgrade con fallo restaura servicio siguiendo runbook probado | UC-20 |
| RF-087 | S | Recopilar incidentes y feedback sin datos secretos | Ticket con tipo, severidad, estado y resolución | UC-14 |
| RF-088 | M | No habilitar producción fiscal sin evidencia de gate firmado | La interfaz indica BLOQUEADO hasta checklist aprobado | UC-19 |

## 7. Requisitos no funcionales medibles (RNF)

Los objetivos son **umbrales propuestos**, no SLAs contratados ni resultados medidos. Antes de firmarlos, cerrar hardware, muestra, carga, ventanas, tamaño de base, precio y error budget.

| ID | Categoría | Propiedad | Umbral/objetivo | Método verificable | Gate |
|---|---|---|---|---|---|
| RNF-001 | Seguridad | Aislamiento de lectura/escritura entre tenants | 0 accesos exitosos cruzados en pruebas negativas | Prueba 2 tenants RBAC/ORM/API | G3 |
| RNF-002 | Seguridad | TLS para acceso público | TLS 1.2+ mínimo; certificado válido | Escaneo TLS por entorno | G3 |
| RNF-003 | Seguridad | Secretos nunca en Git ni logs | 0 hallazgos en escaneo secrets | Secret scan y revisión de logs | G3 |
| RNF-004 | Seguridad | Acceso de mínimo privilegio | 100% de acciones privilegiadas requieren rol/permiso | Matriz RBAC positiva y negativa | G3 |
| RNF-005 | Seguridad | Sesiones revocables | Revocación efectiva en petición siguiente | Prueba revocación tokens/sesión | G3 |
| RNF-006 | Seguridad | Dependencias con licencia revisada | 100% inventariadas y aptas antes de distribución | SBOM y revisión licencias | G0 |
| RNF-007 | Seguridad | Evitar modificación de evidencia firmada | 0 ediciones directas de XML firmado en pruebas | Prueba tamper y hash | G3 |
| RNF-008 | Privacidad | Minimización de datos centrales SaaS | El plano SaaS no almacena líneas de venta en claro por defecto | Inspección schema/telemetría | G3 |
| RNF-009 | Privacidad | Acceso de soporte auditado | 100% accesos con actor, propósito, expiración | Logs y casos de autorización | G3 |
| RNF-010 | Privacidad | Política de retención y exportación | Baja con export y borrado según matriz legal aprobada | Prueba salida y retención | G4 |
| RNF-011 | Fiabilidad | Idempotencia de venta y pago | 0 duplicados tras 100 reenvíos concurrentes por misma clave | Prueba concurrente | G1 |
| RNF-012 | Fiabilidad | Idempotencia fiscal | 0 solicitudes originales duplicadas por identidad | Prueba locks, timeout y retries | G3 |
| RNF-013 | Fiabilidad | Recuperación de timeout incierto | 100% incertidumbres conservan rastreo hasta resolución | Fault injection de pérdida de respuesta | G3 |
| RNF-014 | Fiabilidad | Conservación de eventos fiscales | 100% envíos/respuestas tienen ID y marca temporal | Prueba auditoría | G3 |
| RNF-015 | Disponibilidad | Objetivo inicial piloto mensual | ≥99.5% excluyendo ventana pactada, sujeto a presupuesto | Medición 30 días y reporte | G4 |
| RNF-016 | Continuidad | RPO objetivo crítico | ≤15 min solo si backup/replicación verificados | Ensayo pérdida datos reciente | G4 |
| RNF-017 | Continuidad | RTO objetivo incidente recuperable | ≤4 h en escenario definido y ensayado | Drill de restauración | G4 |
| RNF-018 | Continuidad | Respaldo verificable | 100% backups definidos tienen verificación integridad | Verificación diaria y logs | G4 |
| RNF-019 | Continuidad | Restauración funcional | 100% drills incluyen DB, filestore y acceso | Ensayo independiente | G4 |
| RNF-020 | Rendimiento | POS: latencia operación local en línea | P95 ≤2 s excluyendo tercero fiscal, hardware definido | Load test medido del API POS | G1 |
| RNF-021 | Rendimiento | Búsqueda producto 2000 SKU | P95 ≤500 ms en ambiente piloto especificado | Prueba funcional + medición | G1 |
| RNF-022 | Rendimiento | Apertura de dashboard | P95 ≤3 s con 30 días datos de prueba | Browser/perf test | G1 |
| RNF-023 | Rendimiento | Concurrencia MVP | ≥2 cajas por cliente sin doble serie/venta | Prueba 2 sesiones y locks | G1 |
| RNF-024 | Escalabilidad | Tenant aislado y aprovisionable | Alta de 2 tenants reproduce mismo paquete | Prueba provisioning | G3 |
| RNF-025 | Integridad | Precisión moneda PEN | Montos con 2 decimales y reglas de redondeo aprobadas | Golden vectors fiscales | G3 |
| RNF-026 | Integridad | Stock no negativo o política explícita | 100% ventas sin stock siguen configuración | Prueba borde/concurrencia | G1 |
| RNF-027 | Integridad | Cierre auditable | 0 diferencias suprimidas, todo ajuste con actor | Prueba cierres con diferencias | G1 |
| RNF-028 | Accesibilidad | Navegación teclado | 100% acciones esenciales con teclado | Checklist teclado | G1 |
| RNF-029 | Accesibilidad | Contraste mínimo AA | WCAG AA para texto/interacción esencial | Auditoría contraste | G1 |
| RNF-030 | Usabilidad | Tareas principales ejecutables | ≥80% usuarios piloto completan 5 tareas sin ayuda crítica | Sesiones observadas con ≥5 usuarios | G2 |
| RNF-031 | Usabilidad | Mensajes accionables | 100% errores críticos incluyen siguiente acción | Revisión UX casos negativos | G1 |
| RNF-032 | Mantenibilidad | Dependencias pinneadas | 100% imágenes y módulos críticos tienen versión | Revisión lockfile/SBOM | G0 |
| RNF-033 | Mantenibilidad | Despliegue reproducible | Instalación limpia y smoke CI verde SHA exacto | CI sobre rama limpia | G1 |
| RNF-034 | Mantenibilidad | No fork del core Odoo en MVP | 0 parches directos core salvo ADR excepcional | Diff upstream/scan | G0 |
| RNF-035 | Observabilidad | Métrica de cola fiscal | Se mide edad, pendientes, rechazo, incertidumbre | Monitor test | G3 |
| RNF-036 | Observabilidad | Logs sin datos sensibles | 0 tokens/certificados en logs capturados | Escaneo y audit log | G3 |
| RNF-037 | Portabilidad | Exportación portable | 100% tablas/archivos previstos recuperables por cliente | Test export/import | G4 |
| RNF-038 | Interoperabilidad | Contratos API versionados | Cambios breaking disparan versión y suite contrato | Contract tests | G3 |
| RNF-039 | Operación | Plan de soporte por severidad | 100% incidentes críticos asignados y con escalamiento | Simulación de incidente | G4 |
| RNF-040 | Costo | Contribución comercial medible | Costo variable real registrado por tenant/mes | Revisión factura hosting y horas | G4 |
| RNF-041 | Costo | Costo por documento no supuesto cero | TCO real vs ruta directa y proveedor comparado | Cotizaciones y carga medida | G0 |
| RNF-042 | Cumplimiento | No simular validez SUNAT | 0 pantallas/manuales presentan mock como CDR válido | Test etiquetas y revisión | G3 |
| RNF-043 | Cumplimiento | Aprobación fiscal previa al piloto real | 100% tipos documento usados tienen evidencia/gate | Acta fiscal por tipo | G3 |
## 8. Modelo de datos conceptual y propiedad

Entidades: Tenant, plan y suscripción; Company/Emisor, establecimiento, caja, sesión, empleado/rol; producto, código, impuesto, precio, almacén, stock move, ajuste; comprador, venta POS, línea, pago/confirmación, devolución, reembolso; solicitud fiscal, identidad (RUC/tipo/serie/número), payload/version, XML firmado, entrega, consulta, respuesta/constancia/CDR según modalidad, incidente fiscal; auditoría, backup, restore, ticket de soporte.

**Sistema de registro:** Odoo para comercio, caja, stock y contabilidad; plataforma SaaS para alta/planes/despliegues y salud; módulo fiscal para envío y evidencia de cada intento vinculada a Odoo. **No** duplicar el ledger comercial en una base de terceros; correlación mediante claves estables, no sesiones de navegador.

**Relaciones:** tenant 1:N usuarios/cajas/ventas; venta 1:N líneas y pagos; venta 0:N solicitudes fiscales vinculadas por procedimiento; solicitud 1:N eventos/consultas y 0:N evidencias; venta 0:N devoluciones, cada una con referencia a original. Serie/identidad tiene unicidad fiscal por emisor y tipo. No permitir actualización destructiva de evidencia firmada.

## 9. Interacciones y máquinas de estado

**Comercial:** borrador → confirmada → pagada/completada; cancelación/devolución mediante registros y políticas específicas. **Pago:** no registrado → registrado manual o confirmado por tercero → reembolso/conciliación independiente. **Fiscal:** no solicitado → pendiente → preparación/firma → envío/resultado pendiente → aceptado/observado/rechazado según mecanismo, o resultado desconocido; consulta/conciliación sin reemisión ciega. **Caja:** cerrada → apertura → abierta → cierre → cerrada con acta; diferencia requiere justificación/autorización.

Ver secuencias completas en MK1/design/use-cases.md y contratos de transición en MK1/arch/02-contracts-and-states.md.

## 10. Restricciones, excepciones y escenarios adversos

A) Doble clic tras pago → mismo identificador, sin segunda venta/pago/movimiento. B) Pago Yape declarado sin verificación → registro explícitamente MANUAL. C) Caída navegador luego del commit → consultar origen antes de repetir. D) Venta contra stock final en dos cajas → política/lock del ERP y alerta. E) Factura sin RUC comprador válido → detener prevalidación. F) Emisor/certificado inválido → no enviar ni filtrar secretos. G) Envío completado y respuesta perdida → estado desconocido, consulta y escalamiento. H) Rechazo real → conservar XML/constancia/error, aplicar procedimiento correctivo. I) Respuesta HTTP 200 sin CDR verificable → no afirmar aceptación. J) Boleta/resumen vs factura → usar circuito correcto por régimen. K) Devolución repetida o superior al original → impedir efecto duplicado. L) Diferencia de caja → acta y aprobación, nunca maquillar. M) Pérdida caché POS offline → mostrar limitación de recuperación. N) Restauración incompleta DB sin filestore → fallar gate. O) Suscripción vencida → respetar retención y exportación. P) Usuario soporte sin delegación → denegar y auditar. Q) Actualización de addon rompe vista → rollback con evidencia. R) Datos de otro tenant visibles → incidente crítico y bloqueo de release.

## 11. Exclusiones tributarias controladas

IGV del 18% en el escenario base, bienes gravados, PEN, cantidades positivas enteras, sin descuentos ni perfiles mixtos en el simulador actual. No extrapolar ese simulador a régimen fiscal real, pues impuestos incluidos, descuentos, anticipos, exoneración/inafectación, ISC, detracciones, percepciones, retenciones, exportaciones, líneas gratuitas y notas requieren reglas particulares. El alcance exacto de boletas, facturas y notas comerciales queda bloqueado hasta matriz por modalidad SUNAT y pilotos autorizados.

## 12. Gobernanza, cambios y liberaciones

**Propietario de producto:** aprueba alcance/experiencia/costo; **responsable técnico:** API, datos, seguridad, despliegue; **responsable fiscal con asesoría competente:** reglas, canal, tipos, validez; **responsable soporte:** runbooks/SLA; **cliente piloto:** aceptación operativa. Las funciones pueden recaer en una persona, las aprobaciones no se presumen.

Todo cambio mantiene: solicitud → impacto RF/RNF/BR/UC → ADR si arquitectónico → plan/test/datos y presupuesto → aprobación → implementación → evidencia CI/manual/fiscal → release y rollback. G0 (alcance/licencia), G1 (núcleo/QA), G2 (piloto acotado), G3 (fiscal y seguridad), G4 (operación/negocio) prevalecen. Ningún CHECK de gate se marca solo por crear documentos.

## 13. Dependencias bloqueantes y puntos abiertos

1. Rubro/ICP confirmado por entrevistas.
2. Contrato funcional Odoo POS→documento y nota de crédito para localización peruana.
3. Ruta fiscal final: Greenter vs OPeru/Nubefact vs otro, con licencia/TCO/modalidad legal.
4. Habilitación del emisor y eventual obligación/figura PSE/OSE; credenciales y certificado sin almacenarlos en repositorio.
5. Tratamiento de incertidumbre en envíos, outbox, consulta, identidad documental y mecanismo por tipo.
6. Aislamiento real de tenant, cifrado, backups, restore, retención y privacidad peruana.
7. Política de offline y pagos; límites de impresora y hardware.
8. SLAs, pricing, unidad económica y alcance contractual con primer piloto.
9. Prueba end-to-end browser con persona real, no solo ORM.

## 14. Puertas para pasar a build y a producción

**Build comercial:** cerrar decisiones principales, dependencias, diseño, pruebas de aceptación y viabilidad; el laboratorio sigue permitido con datos ficticios. **Piloto:** controles de datos/backup/soporte y contrato explícito; emisor externo cuando el nuestro no esté certificado, sin fingir equivalencia. **Producción integral:** evidencia por tipo documento, canal autorizado, procedimientos correctivos, permisos, backups restaurados, incidentes y soporte. El criterio GO/PIVOT/KILL puede concluir NO GO.

## 15. Referencias y trazabilidad

Casos de uso en use-cases.md; BR en business-rules.md; arquitectura/contratos en arch/; matriz bidireccional generada con IDs aquí en test/traceability.csv. Fuentes internas oficiales listadas en MK0/mining-site/01-sources.md. La matriz no significa que las pruebas estén ejecutadas; status por defecto DESIGN_ONLY.
