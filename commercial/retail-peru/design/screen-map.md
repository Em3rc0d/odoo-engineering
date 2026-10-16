# Mapa visual de pantallas y transiciones

**DUX-UI-001 — propuesta, no interfaz implementada.** Identificadores Sxx propios de este diseño; no son IDs del SRS.

## 1. Mapa general

~~~mermaid
flowchart TD
    S00["S00 Acceso"] --> S10["S10 Inicio del negocio"]
    S00 --> S01["S01 Alta y bienvenida"]
    S01 --> S02["S02 Configurar tienda"]
    S02 --> S03["S03 Cargar productos"]
    S03 --> S04["S04 Preparación fiscal"]
    S04 --> S05{"S05 ¿Listo para operar?"}
    S05 -->|"Solo demo / faltan requisitos"| S06["S06 Modo demostración"]
    S05 -->|"Gates aprobados"| S10
    S10 --> S20["S20 Abrir caja"]
    S20 --> S11["S11 Punto de venta"]
    S11 --> S12["S12 Cobro"]
    S12 --> S13["S13 Resultado de venta"]
    S13 --> S11
    S13 --> S15["S15 Detalle de comprobante"]
    S10 --> S14["S14 Bandeja fiscal"]
    S14 --> S15
    S15 -->|"Requiere acción"| S16["S16 Resolver incidencia"]
    S16 --> S15
    S10 --> S23["S23 Inventario"]
    S10 --> S24["S24 Reportes"]
    S10 --> S25["S25 Usuarios y permisos"]
    S10 --> S21["S21 Cierre de caja"]
    S11 --> S22["S22 Devolución"]
    S22 --> S15
    S10 --> S26["S26 Ayuda y soporte"]
    S10 --> S17["S17 Historial de ventas"]
    S17 --> S22
    S17 --> S15
~~~

**Interpretación:** las flechas muestran caminos lógicos, no enlaces que siempre estarán habilitados. S11 requiere caja abierta y permisos; S10 puede mostrar accesos distintos por rol. S04 nunca habilita emisión real solo porque el usuario terminó el asistente.

## 2. Inventario y permisos

| ID | Pantalla | Persona principal | Acción clave / salida | Regla crítica |
|---|---|---|---|---|
| S00 | Acceso | Todos | Autenticarse → S10 | No mostrar datos entre tenants |
| S01 | Alta y bienvenida | Propietario | Iniciar alta → S02 | No activar servicio sin contrato/configuración |
| S02 | Configurar tienda | Administrador | RUC, sede, moneda, zona → S03 | Datos fiscales verificados por proceso autorizado |
| S03 | Importar catálogo | Administrador / inventario | Validar productos → S04 | Detectar duplicados y precios inválidos |
| S04 | Preparación fiscal | Administrador + asesor | Configurar emisor / proveedor → S05 | Secretos fuera de UI/logs; autorización explícita |
| S05 | Control de habilitación | Operador SaaS | Demo o activación → S06/S10 | Gates de fiscalidad, backup y seguridad |
| S06 | Demostración | Invitado autorizado | Simular venta | Datos ficticios; etiqueta permanente DEMO |
| S10 | Inicio del negocio | Propietario / supervisor | Revisar indicadores y alertas | Cifras con período y alcance visibles |
| S11 | Punto de venta | Cajero | Agregar artículos → S12 | Caja abierta; no doble venta |
| S12 | Cobro | Cajero | Elegir medio y confirmar → S13 | Manual no significa pago externo confirmado |
| S13 | Resultado de venta | Cajero | Nueva venta / ver comprobante | Mostrar estados comercial, pago y fiscal separados |
| S14 | Bandeja fiscal | Contador / supervisor | Filtrar pendientes y errores → S15 | No ocultar documentos inciertos |
| S15 | Detalle fiscal | Contador / supervisor | Ver evidencia / historial | «Aceptado» solo con evidencia válida |
| S16 | Resolver incidencia | Supervisor / contador | Consultar, subsanar o escalar | Nunca reenviar a ciegas |
| S17 | Historial de ventas | Cajero autorizado / supervisor | Buscar venta → S22 | Respeta permisos y trazabilidad |
| S20 | Apertura de caja | Cajero | Declarar efectivo inicial → S11 | Evitar sesiones incompatibles |
| S21 | Cierre de caja | Cajero / supervisor | Contar y cerrar | Diferencia queda registrada |
| S22 | Devolución | Supervisor / cajero autorizado | Relacionar venta, stock, reembolso y fiscal | No duplicar devolución ni borrar original |
| S23 | Inventario | Encargado | Ver existencias y movimientos | Ajustes con causa y autorización |
| S24 | Reportes | Propietario | Ver ventas, caja, stock, incidencias | Fuente y fecha de corte visibles |
| S25 | Usuarios y permisos | Administrador | Alta/baja y roles | Mínimo privilegio y auditoría |
| S26 | Ayuda y soporte | Todos | Abrir caso y consultar guía | No exponer contraseñas ni certificados |

**Pantalla fuera del menú del cliente:** OPS-01, consola interna de aprovisionamiento, salud, respaldo y soporte; su acceso es separado y auditado. No incluir datos detallados de ventas de todos los clientes por defecto.

## 3. Bocetos de baja fidelidad

Son *wireframes* para conversar con comerciantes. No copian la interfaz de ningún competidor.

### S10 — El dueño quiere saber cómo va el día

~~~text
┌─────────────────────────────────────────────────────────┐
│ MI TIENDA    Hoy, Lima          [Caja: abierta] [Ayuda] │
├─────────────────────────────────────────────────────────┤
│ Ventas registradas    S/ 1 250     Operaciones: 28      │
│ Efectivo esperado     S/   480     Pendientes fiscales: 2│
│ Stock bajo: 6 productos           Diferencias caja: 0  │
├─────────────────────────────────────────────────────────┤
│ REQUIERE ATENCIÓN                                      │
│ ! 2 comprobantes pendientes  [Ver estado]              │
│ ! 6 productos por reponer    [Ver inventario]          │
├─────────────────────────────────────────────────────────┤
│ [Nueva venta] [Caja] [Comprobantes] [Inventario]        │
│ [Ventas] [Reportes] [Usuarios] [Ayuda]                  │
└─────────────────────────────────────────────────────────┘
Cifras ficticias de diseño; nunca son métricas reales.
~~~

### S11 + S12 — Cobrar sin confundir los estados

~~~text
┌─────────────────────────────────────────────────────────┐
│ CAJA 1 — ABIERTA      Cajero: Operador                  │
├──────────────────────────────┬──────────────────────────┤
│ Buscar / escanear producto   │ CARRITO                  │
│ [________________________]   │ 2 x Producto A    S/ 30 │
│ Producto A   S/15 [Añadir]  │ 1 x Producto B    S/ 20 │
│ Producto B   S/20 [Añadir]  │                          │
│                              │ TOTAL            S/ 50 │
│                              │ [Continuar al cobro]    │
├──────────────────────────────┴──────────────────────────┤
│ COBRO: Efectivo / Tarjeta / Yape-Plin (registro manual) │
│ COMPROBANTE: Boleta / Factura / Otro flujo permitido    │
│ [Volver]                 [Confirmar una sola vez]       │
└─────────────────────────────────────────────────────────┘
~~~

### S13 — Resultado inequívoco

~~~text
┌─────────────────────────────────────────────────────────┐
│ VENTA #V-001: REGISTRADA                                │
│ PAGO: REGISTRADO MANUALMENTE (Yape)                     │
│ COMPROBANTE: PENDIENTE DE RESULTADO FISCAL              │
│                                                         │
│ La venta está guardada. Aún no hay resultado confirmado │
│ del canal tributario.                                   │
│ [Nueva venta] [Ver comprobante] [Solicitar ayuda]       │
└─────────────────────────────────────────────────────────┘
~~~

### S14 + S15 — Bandeja de comprobantes

~~~text
┌─────────────────────────────────────────────────────────┐
│ COMPROBANTES [Todos] [Pendientes] [Requieren atención]  │
├─────────────────────────────────────────────────────────┤
│ Venta   Documento    Estado              Acción        │
│ V-001   B001-00001   Pendiente            [Ver]         │
│ V-002   F001-00002   Resultado desconocido [Revisar]    │
│ V-003   F001-00003   Rechazado            [Resolver]     │
├─────────────────────────────────────────────────────────┤
│ DETALLE: eventos, proveedor/canal, códigos, evidencias  │
│ [Consultar estado] [Ver historial] [Escalar a soporte]  │
└─────────────────────────────────────────────────────────┘
~~~

## 4. Reglas de interacción

- **Cajero:** teclado y escáner primero; foco visible, botones grandes, importe legible, confirmación protegida contra doble clic.
- **Propietario:** datos del día y alertas antes de gráficos complejos; separar monto de ventas de efectivo disponible.
- **Contador:** filtros por documento/fecha/estado; eventos y evidencias exportables con permiso.
- **Supervisor:** toda autorización excepcional registra quién, cuándo, por qué y qué operación.
- **Soporte:** ve salud técnica y casos; para datos del cliente requiere acceso temporal autorizado.
- **Todos:** textos claros, contraste suficiente, navegación por teclado, zona horaria America/Lima, moneda PEN y fechas explícitas.

## 5. Estados vacíos y de error que debemos diseñar

| Contexto | Mensaje de interfaz propuesto | Acción |
|---|---|---|
| Sin productos | «Tu catálogo está vacío» | Cargar productos |
| Caja cerrada | «Abre una caja antes de vender» | Ir a S20 |
| Pago externo no confirmado | «Aún no tenemos confirmación del cobro» | Verificar con el medio de pago |
| Envío fiscal en cola | «Comprobante pendiente de procesamiento» | Ver detalle |
| Respuesta fiscal incierta | «No sabemos si el canal recibió el documento» | Consultar / escalar |
| Rechazo expreso | «El documento requiere corrección» | Ver motivo y procedimiento |
| Sin conexión | «Sin conexión: algunas funciones están limitadas» | Ver pendientes / reconectar |
| Certificado o autorización faltante | «Emisión real no habilitada» | Revisar configuración |
| Diferencia de caja | «Existe una diferencia que requiere revisión» | Justificar / solicitar supervisor |

## 6. Prueba con usuarios

Antes de construir una interfaz propia, observar a un cajero realizando: abrir caja, buscar tres productos, registrar dos medios de pago distintos, encontrar un comprobante pendiente y cerrar caja. Registrar tiempo, errores, confusiones y frases utilizadas. Validar si la interfaz estándar de Odoo resuelve cada tarea antes de personalizar.
