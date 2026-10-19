# Catálogo de 20 casos de uso — IPC-UC-001

**Versión:** 0.9 propuesta · 2026-10-19. Basado en SRS: cada caso incluye actores, disparador, precondiciones, camino principal, alternativas, excepciones, postcondición y RF relacionados. **No equivale a pruebas ejecutadas.**

## Relaciones entre actores

- Cajero controla venta y caja; no tiene credenciales fiscales.
- Supervisor autoriza devoluciones y diferencias; nunca borra documentos firmados.
- Contador analiza estados, rechazos y procedimientos correctivos.
- Plataforma fiscal interactúa según modalidad con SUNAT/PSE/OSE, nunca se asume disponibilidad instantánea.
- Operador SaaS tiene plano separado del tenant; el soporte no lee datos por defecto.

[Diseño de navegación y bocetos existentes](../../../retail-peru/design/screen-map.md) · [7 secuencias Mermaid](../../../retail-peru/design/sequences.md) · [estados documentados](../../../retail-peru/design/states-and-acceptance.md).

## UC-01 — Alta del negocio

**Actores:** Propietario / administrador SaaS. **Disparador:** Solicita un nuevo tenant y acepta condiciones. **Precondiciones:** Plan y responsabilidad contractual confirmados; entorno de prueba separado. **RF trazados:** RF-001, RF-002, RF-003, RF-004, RF-005, RF-006, RF-007, RF-008.

**Flujo principal:**

1. Verifica datos de negocio
2. crea identificador y DB/filestore
3. configura país/PEN
4. crea admin seguro
5. muestra checklist y revisión de readiness

**Alternativas:** Si falta fiscalidad permite DEMO explícito, no emisión real; solicitud repetida retorna mismo tenant.

**Excepciones / abuso:** Dato fiscal inválido, duplicidad de RUC/tenant, error provisionamiento, fuga de secretos, error restore.

**Postcondición:** Tenant aislado listo para configuración, nunca emisión automática.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-02 — Autenticación y acceso

**Actores:** Usuario del negocio. **Disparador:** Ingresa credenciales y abre módulo. **Precondiciones:** Tenant activo; usuario con estado vigente. **RF trazados:** RF-009, RF-013.

**Flujo principal:**

1. Valida autenticación
2. inicia sesión limitada
3. calcula rol
4. muestra solo módulos/acciones permitidas
5. registra acceso

**Alternativas:** Olvido de contraseña por canal seguro; cerrar sesión revoca token.

**Excepciones / abuso:** Credenciales erróneas, usuario deshabilitado, fuerza bruta, sesión expirada y cross-tenant.

**Postcondición:** Sesión auditada o denegada sin revelar datos.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-03 — Administrar catálogo

**Actores:** Administrador / encargado inventario. **Disparador:** Carga SKU o edita producto. **Precondiciones:** Empresa configurada, rol catálogo, impuestos aprobados. **RF trazados:** RF-014, RF-015, RF-016, RF-017, RF-018.

**Flujo principal:**

1. Importa CSV
2. muestra preview y errores
3. confirma filas válidas
4. actualiza precio/visibilidad sin alterar ventas anteriores

**Alternativas:** SKU existente actualiza según política; producto no vendible se archiva.

**Excepciones / abuso:** SKU duplicado ambiguo, precio negativo, tasa no soportada, campos faltantes.

**Postcondición:** Catálogo con trazabilidad de cambios y validaciones.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-04 — Recibir y ajustar inventario

**Actores:** Inventario / supervisor. **Disparador:** Llega mercancía o se detecta diferencia. **Precondiciones:** Almacén y producto existentes, rol/causa de ajuste. **RF trazados:** RF-019, RF-020, RF-021.

**Flujo principal:**

1. Consulta cantidad disponible
2. registra entrada/ajuste con origen
3. valida movimiento
4. muestra saldo actualizado

**Alternativas:** Movimiento de devolución ingresa según estado comercial; conteo corregido por autorización.

**Excepciones / abuso:** Importación duplicada, último stock concurrente, unidad incompatible, lote requerido no soportado.

**Postcondición:** Stock Odoo consistente; no se reescribe historia.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-05 — Abrir caja y mover efectivo

**Actores:** Cajero / supervisor. **Disparador:** Comienza turno o realiza egreso/ingreso. **Precondiciones:** Usuario permitido, POS configurado, ninguna sesión incompatible. **RF trazados:** RF-024, RF-025, RF-040.

**Flujo principal:**

1. Selecciona caja
2. declara efectivo inicial
3. abre sesión
4. ingresa operación extraordinaria con motivo y autorización

**Alternativas:** Si había sesión anterior del mismo cajero, requiere continuidad o cierre previo.

**Excepciones / abuso:** Doble apertura, journal no configurado, diferencia de apertura, permisos insuficientes.

**Postcondición:** Sesión abierta con saldo/actor/fecha y movimientos trazados.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-06 — Vender y cobrar

**Actores:** Cajero / comprador. **Disparador:** Cliente elige productos. **Precondiciones:** Caja abierta, productos activos, moneda/IGV configurados. **RF trazados:** RF-022, RF-026, RF-027, RF-028, RF-029, RF-030, RF-031, RF-032, RF-034, RF-035, RF-036, RF-037, RF-038.

**Flujo principal:**

1. Escanea/busca
2. agrega líneas
3. verifica total
4. elige comprador y medio
5. confirma una vez con clave estable
6. Odoo persiste venta, pago y stock
7. UI muestra estados comercial/pago/fiscal separados

**Alternativas:** Yape/Plin se registra manual y pide verificar en app; pago externo requiere confirmación; carrito puede cancelarse antes de cobro.

**Excepciones / abuso:** Stock insuficiente, importe inválido, doble clic, timeout después de persistir, desconexión y sesión cerrada.

**Postcondición:** Una sola venta/pago/stock por clave, sin aceptación fiscal inferida.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-07 — Generar solicitud fiscal

**Actores:** Cajero / contador / motor fiscal. **Disparador:** Venta elegible solicita boleta/factura. **Precondiciones:** Emisor autorizado, modalidad, comprador/tipo/serie/correlativo, configuración y credenciales válidos. **RF trazados:** RF-046, RF-047, RF-048, RF-049, RF-050, RF-051, RF-052, RF-053, RF-063.

**Flujo principal:**

1. Valida datos/IGV
2. toma snapshot inmutable
3. reserva identidad
4. registra outbox
5. prepara XML UBL
6. firma
7. transmite al canal aprobado
8. registra estado/evidencias

**Alternativas:** Boleta/factura y posibles resúmenes siguen procedimientos separados; la cola permite respuesta diferida.

**Excepciones / abuso:** RUC inválido, certificado vencido, numeración repetida, XML no válido, servicio no disponible.

**Postcondición:** CPE pendiente o con evidencia fiscal real; nunca solo SIMULADO en producción.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-08 — Consultar y conciliar estado

**Actores:** Contador / motor / soporte autorizado. **Disparador:** Documento está pendiente o incierto. **Precondiciones:** Identificador original y acceso a canal de consulta. **RF trazados:** RF-054, RF-055, RF-056, RF-057, RF-058, RF-059.

**Flujo principal:**

1. Localiza documento
2. revisa eventos
3. consulta por referencia si procede
4. valida evidencia
5. actualiza el mismo registro
6. avisa al usuario

**Alternativas:** Si el canal carece de consulta automática, asigna revisión manual y conserva desconocido.

**Excepciones / abuso:** Respuesta perdida, timeout, CDR inaccesible, código contradictorio, consulta duplicada.

**Postcondición:** Estado sustentado o incierto persistente sin reemisión ciega.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-09 — Resolver rechazo y corrección

**Actores:** Contador / supervisor. **Disparador:** Rechazo expreso o error fiscal. **Precondiciones:** Documento original persistido con eventos y reglas vigentes. **RF trazados:** RF-060, RF-061, RF-062.

**Flujo principal:**

1. Abre incidencia
2. lee código/error
3. determina procedimiento
4. autoriza
5. genera acción correctiva enlazada
6. conserva XML original
7. consulta resultado

**Alternativas:** Si no hay corrección permitida, escalar antes de nueva operación; notas dependen de tipo/estado.

**Excepciones / abuso:** Rechazo sin causa, intento de modificar XML firmado, duplicar correlativo, corregir comprobante indebido.

**Postcondición:** Incidencia auditada, acción fiscal legal o bloqueo razonado.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-10 — Devolver producto y reembolsar

**Actores:** Cajero / supervisor / contador. **Disparador:** Cliente devuelve total o parte de venta. **Precondiciones:** Venta identificada, política/permiso, cantidades disponibles. **RF trazados:** RF-066, RF-067, RF-068, RF-069.

**Flujo principal:**

1. Busca venta
2. calcula ya devuelto
3. autoriza
4. registra retorno físico
5. valida condición de stock
6. registra reembolso
7. inicia documento fiscal correctivo si aplica

**Alternativas:** Producto dañado va a ubicación no vendible; devolución parcial; pago tercero puede quedar pendiente.

**Excepciones / abuso:** Devolución duplicada, mayor que cantidad vendida, venta inexistente, rechazo de emisor/notas.

**Postcondición:** Operaciones de stock/dinero/fiscal diferenciadas y ligadas.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-11 — Cerrar caja

**Actores:** Cajero / supervisor. **Disparador:** Termina turno. **Precondiciones:** Sesión abierta, ventas de sesión conocidas. **RF trazados:** RF-041, RF-042, RF-043, RF-044.

**Flujo principal:**

1. Calcula esperado
2. cajero ingresa conteo real
3. muestra diferencia
4. solicita aprobación según umbral
5. cierra con reporte y acta

**Alternativas:** Con diferencia menor permitida se documenta; ante draft pendientes requiere resolver antes de cerrar.

**Excepciones / abuso:** Error asiento contable, permisos, intento de cerrar dos veces, efectivo negativo.

**Postcondición:** Sesión cerrada o pendiente de resolución con rastro histórico.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-12 — Consultar indicadores y alertas

**Actores:** Propietario / contador / supervisor. **Disparador:** Abre panel o consulta jornada. **Precondiciones:** Acceso al tenant y empresa. **RF trazados:** RF-023, RF-039, RF-073, RF-074, RF-077.

**Flujo principal:**

1. Selecciona período
2. consulta ventas, medios, caja, stock bajo y comprobantes pendientes
3. visualiza fecha de corte y acción

**Alternativas:** Sin datos mostrar estado vacío; permisos limitan detalle.

**Excepciones / abuso:** Inconsistencia de agregación, consulta intertenant, datos obsoletos sin marca temporal.

**Postcondición:** Información útil, contextualizada y verificable.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-13 — Operación sin conexión

**Actores:** Cajero / motor de sincronización. **Disparador:** Se cae internet durante jornada. **Precondiciones:** Dispositivo y modo offline previamente aprobados, caché intacta. **RF trazados:** RF-070, RF-071, RF-072.

**Flujo principal:**

1. Muestra banner
2. limita funciones
3. identifica venta local permitida
4. al reconectar sincroniza con clave estable
5. Odoo acepta una vez
6. muestra resultado

**Alternativas:** Función que requiere servidor queda bloqueada; emisión fiscal usa contingencia solo aprobada.

**Excepciones / abuso:** Caché borrada, navegador cerrado, doble sync, falta stock global, reconexión intermitente.

**Postcondición:** Ningún CPE se declara legal ni venta duplicada por modo offline.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-14 — Administrar y recuperar SaaS

**Actores:** Operador SaaS / soporte. **Disparador:** Alta, incidente o solicitud de acceso. **Precondiciones:** Tenant y ticket autorizados, credenciales bajo control. **RF trazados:** RF-078, RF-079, RF-080, RF-081, RF-082, RF-085, RF-087.

**Flujo principal:**

1. Comprueba salud
2. captura logs sin secretos
3. delega acceso temporal
4. ejecuta backup o restore aislado
5. verifica DB+filestore
6. registra actuación

**Alternativas:** Restauración de punto anterior con reconciliación; acceso sin permiso se deniega.

**Excepciones / abuso:** Aislamiento fallido, backup corrupto, filestore faltante, secretos expuestos.

**Postcondición:** Tenant operativo y auditoría, o incidente escalado.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-15 — Gestionar suscripción

**Actores:** Propietario / plataforma SaaS. **Disparador:** Compra, renueva, vence o cancela plan. **Precondiciones:** Plan y condiciones contractuales explícitos. **RF trazados:** RF-083, RF-084.

**Flujo principal:**

1. Registra plan/impuestos/cobro
2. actualiza estado de cuenta
3. mide infraestructura y soporte
4. notifica renovación

**Alternativas:** Mora suspende según contrato sin borrar evidencia; cambio de plan preserva datos.

**Excepciones / abuso:** Doble cargo, precio erróneo, suspensión que impide exportación legal.

**Postcondición:** Suscripción y costos medibles con trazabilidad.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-16 — Administrar usuarios y permisos

**Actores:** Administrador cliente / supervisor. **Disparador:** Alta, baja, cambio de rol. **Precondiciones:** Usuario autorizado como administrador. **RF trazados:** RF-010, RF-011, RF-012, RF-076.

**Flujo principal:**

1. Crea cuenta
2. asigna mínimos privilegios
3. revisa alcance caja/empresa
4. revoca
5. registra auditoría

**Alternativas:** Soporte delega temporalmente con autorización verificable.

**Excepciones / abuso:** Escalada de rol, acceso cruzado, usuario deshabilitado con sesión activa.

**Postcondición:** RBAC aplicado y evidencia de cambios.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-17 — Exportación y baja

**Actores:** Propietario / soporte. **Disparador:** Cliente decide migrar o terminar servicio. **Precondiciones:** Titular autorizado, obligaciones de retención identificadas. **RF trazados:** RF-075.

**Flujo principal:**

1. Genera exportación de catálogo, ventas, movimientos y evidencias propias
2. valida integridad
3. revoca credenciales
4. retiene/elimina según política

**Alternativas:** Suspensión por mora mantiene salida contractual; entrega escalonada para archivos grandes.

**Excepciones / abuso:** Intento de exportar otro tenant, datos incompletos, eliminación antes de conservar legalmente.

**Postcondición:** Portabilidad verificable y baja auditada.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-18 — Cobro con tercero

**Actores:** Cajero / proveedor de pago. **Disparador:** Cliente presenta transferencia/terminal. **Precondiciones:** Medio e integración aprobados o declarado manual. **RF trazados:** RF-033.

**Flujo principal:**

1. Indica si es registro manual o confirmación real
2. espera respuesta si integrada
3. correlaciona operación
4. finaliza solo según política

**Alternativas:** Pago parcialmente confirmado o reversado se conserva como pendiente.

**Excepciones / abuso:** Timeout, pago rechazado, webhook duplicado, coincidencia falsa.

**Postcondición:** Estado de pago real y separado de venta/fiscal.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-19 — Habilitar emisión por contribuyente

**Actores:** Administrador cliente / contador / operador habilitado. **Disparador:** Solicita operar CPE en producción. **Precondiciones:** Modalidad contribuyente definida y derechos/consentimiento confirmados. **RF trazados:** RF-045, RF-064, RF-065, RF-088.

**Flujo principal:**

1. Valida habilitación y régimen
2. gestiona credenciales por canal seguro
3. verifica certificado
4. ejecuta batería beta/producción autorizada
5. firma acta de gate

**Alternativas:** Si no es elegible para emisión directa, evaluar proveedor legal o dejar bloqueado.

**Excepciones / abuso:** Credencial cruzada, vencimiento, certificado no apto, obligación PSE/OSE, tipo no soportado.

**Postcondición:** Producción habilitada solo para tipos/canales verificados.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.

---

## UC-20 — Actualizar versión y rollback

**Actores:** Operador SaaS / ingeniero. **Disparador:** Nueva versión de Odoo/addon/adaptador. **Precondiciones:** Release aprobada, backup restaurable, ventana/plan de reversión. **RF trazados:** RF-086.

**Flujo principal:**

1. Ejecuta migración ensayada
2. valida health/ORM/UX/fiscal
3. registra cambios
4. habilita rollback
5. comunica impacto

**Alternativas:** Incidente tras release revierte y concilia jobs pendientes.

**Excepciones / abuso:** Schema incompatible, datos/filestore inconsistente, secretos alterados, falta respaldo.

**Postcondición:** Versión coherente o rollback trazado sin pérdida indebida.

**Aceptación:** ejecutar pruebas TC-RF correspondientes en una BD aislada; conservar evidencia de entradas, estados, no duplicación/errores y versión probada.


## Matriz de procesos combinados

- **Día normal:** UC-02 → UC-05 → UC-03/UC-06 → UC-07 → UC-08 → UC-12 → UC-11.
- **Rechazo:** UC-06 → UC-07 → UC-08 → UC-09, sin modificar venta.
- **Devolución:** UC-12 → UC-10 → UC-09 si procede; retorno físico ≠ reembolso ≠ nota fiscal.
- **Caída:** UC-06 → UC-13 → UC-08, sin reenvío ciego.
- **Nuevo comercio:** UC-01 → UC-03 → UC-16 → UC-19 → UC-20; mientras falta UC-19 solo DEMO.
- **Mora o salida:** UC-15 → UC-17 → UC-14 y conservación legal.

## Reglas de tests

Las rutas negativas se prueban antes de declarar GO. Un caso de uso sin captura de datos, logs/estado y prueba negativa permanece DESIGN_ONLY. Vinculación bidireccional por IDs en ../test/traceability.csv.
