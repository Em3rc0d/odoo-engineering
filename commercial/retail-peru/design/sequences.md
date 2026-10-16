# Diagramas de secuencia — personas, Odoo, motor fiscal y SUNAT

**DUX-SEQ-001 — comportamiento objetivo, NO implementación existente.** Diagramas Mermaid renderizables en GitHub. «Canal» puede incluir OPeru/Nubefact y los procedimientos de SUNAT que correspondan; no se presupone un único endpoint ni que toda boleta obtenga una CDR individual idéntica a una factura.

## UC-01. Venta, cobro y solicitud de comprobante

~~~mermaid
sequenceDiagram
    autonumber
    actor Cajero
    participant UI as POS
    participant ERP as Odoo
    participant Cola as Solicitud fiscal persistente
    participant EDI as Adaptador autorizado
    participant Canal as Proveedor / canal SUNAT
    Cajero->>UI: Seleccionar productos y comprobante
    UI->>ERP: Validar sesión, productos y datos fiscales
    ERP-->>UI: Total y condiciones
    Cajero->>UI: Registrar medio de pago y confirmar
    UI->>ERP: Confirmar operación con clave única
    ERP->>ERP: Persistir venta y efecto comercial
    ERP->>Cola: Registrar solicitud fiscal vinculada
    ERP-->>UI: Venta registrada; pago según evidencia
    UI-->>Cajero: Mostrar estado fiscal pendiente
    Cola->>EDI: Procesar solicitud idempotente
    EDI->>Canal: Transmitir según tipo y modalidad
    alt Evidencia fiscal favorable verificada
        Canal-->>EDI: Resultado y evidencia aplicable
        EDI->>ERP: Actualizar estado y custodiar evidencias
    else Rechazo explícito
        Canal-->>EDI: Rechazo y motivo
        EDI->>ERP: Marcar incidencia, sin borrar venta
    else Resultado incierto o diferido
        EDI->>ERP: Mantener pendiente / desconocido
    end
    ERP-->>UI: Estado actualizado al consultar
~~~

**Nota de consistencia:** se busca que venta y solicitud fiscal queden vinculadas de forma durable; el mecanismo transaccional exacto depende de la integración real con Odoo. La confirmación comercial no puede esperar indefinidamente una respuesta fiscal.

## UC-02. Rechazo de comprobante

~~~mermaid
sequenceDiagram
    autonumber
    participant Canal as Canal fiscal
    participant EDI as Integración fiscal
    participant ERP as Odoo
    actor Supervisor
    actor Contador
    Canal-->>EDI: Rechazo expreso y código
    EDI->>ERP: Guardar resultado y evidencia
    ERP-->>Supervisor: Alerta requiere atención
    Supervisor->>ERP: Abrir detalle y motivo
    ERP-->>Contador: Mostrar documento original y eventos
    Contador->>ERP: Solicitar subsanación permitida
    ERP->>ERP: Validar permisos y procedimiento
    alt Procedimiento aplicable y autorizado
        ERP->>EDI: Crear nueva operación fiscal trazable
        EDI-->>ERP: Nueva solicitud con vínculo al original
    else No procede corrección automática
        ERP-->>Contador: Escalar y conservar estado
    end
~~~

**Regla:** no editar un XML firmado, cambiar silenciosamente una serie ni borrar un rechazo. La corrección depende del tipo de documento y la normativa vigente.

## UC-03. Se envió, pero la respuesta se perdió

~~~mermaid
sequenceDiagram
    autonumber
    participant Cola as Solicitud fiscal
    participant EDI as Integración fiscal
    participant Canal as Proveedor / canal
    participant ERP as Odoo
    actor Soporte
    Cola->>EDI: Procesar documento identificado
    EDI->>Canal: Enviar documento
    Note over EDI,Canal: Corte de red tras posible recepción
    EDI-->>ERP: Resultado desconocido
    ERP-->>Soporte: Alertar documento incierto
    EDI->>Canal: Consultar estado si el canal lo permite
    alt Existe resultado verificable
        Canal-->>EDI: Resultado y evidencia
        EDI->>ERP: Conciliar la solicitud original
    else Sigue sin poder verificarse
        EDI->>ERP: Mantener en revisión
        Soporte->>ERP: Registrar investigación y decisión
    end
    Note over Cola,ERP: Prohibido reemitir o renumerar a ciegas
~~~

**Regla:** identidad documental estable por emisor/tipo/serie/número y referencia a operación; la idempotencia debe persistir entre procesos y reinicios, no depender de un botón deshabilitado.

## UC-04. Devolución, reembolso, stock y corrección fiscal

~~~mermaid
sequenceDiagram
    autonumber
    actor Cajero
    actor Supervisor
    participant ERP as Odoo
    participant Pago as Registro de pagos
    participant Stock as Inventario Odoo
    participant EDI as Integración fiscal
    Cajero->>ERP: Buscar venta y solicitar devolución
    ERP-->>Cajero: Venta, cantidades y estado fiscal
    Cajero->>Supervisor: Solicitar autorización
    Supervisor->>ERP: Autorizar o rechazar con motivo
    alt Autorizada y no duplicada
        ERP->>ERP: Crear devolución ligada a venta
        ERP->>Stock: Registrar recepción / disposición
        ERP->>Pago: Registrar reembolso según medio
        alt Documento correctivo legalmente procedente
            ERP->>EDI: Solicitar nota u operación aplicable
            EDI-->>ERP: Estado fiscal independiente
        else Aún no procede acción fiscal
            ERP->>ERP: Dejar pendiente para revisión
        end
        ERP-->>Cajero: Resultado comercial, pago y fiscal
    else Denegada o inconsistente
        ERP-->>Cajero: Explicar motivo sin alterar venta
    end
~~~

**Regla:** devolver mercancía, devolver dinero y emitir una nota son procesos distintos. El reintegro de un pago electrónico puede depender de un tercero.

## UC-05. Apertura, movimientos y cierre de caja

~~~mermaid
sequenceDiagram
    autonumber
    actor Cajero
    actor Supervisor
    participant POS as Pantalla de caja
    participant ERP as Odoo
    Cajero->>POS: Abrir caja y declarar saldo inicial
    POS->>ERP: Validar rol y sesión
    ERP-->>POS: Sesión abierta
    loop Jornada
        Cajero->>POS: Venta o movimiento autorizado
        POS->>ERP: Registrar operación identificada
    end
    Cajero->>POS: Solicitar cierre y declarar conteo
    POS->>ERP: Calcular esperado y diferencia
    alt Sin diferencia o dentro de política
        ERP-->>POS: Permitir cierre y guardar acta
    else Diferencia requiere aprobación
        ERP-->>POS: Mostrar diferencia y solicitar motivo
        Cajero->>Supervisor: Solicitar autorización
        Supervisor->>ERP: Autorizar o investigar
        ERP-->>POS: Cerrar auditado o dejar pendiente
    end
~~~

**Regla:** ningún ajuste de caja debe borrar la diferencia original; el proceso de cierre no modifica retrospectivamente la situación fiscal de una venta.

## UC-06. Caída de conexión y sincronización

~~~mermaid
sequenceDiagram
    autonumber
    actor Cajero
    participant Browser as POS navegador
    participant ERP as Odoo servidor
    participant Cola as Solicitud fiscal
    Cajero->>Browser: Intentar venta sin internet
    Browser->>Browser: Evaluar capacidades offline probadas
    alt Operación offline autorizada
        Browser-->>Cajero: Indicar operación local pendiente
        Note over Browser: Riesgo de pérdida de caché o sesión
        Cajero->>Browser: Reconectar y sincronizar
        Browser->>ERP: Enviar con identificador estable
        ERP->>ERP: Detectar repetidos y confirmar una vez
        ERP-->>Browser: Resultado servidor
        ERP->>Cola: Crear solicitud fiscal solo si procede
        Browser-->>Cajero: Mostrar estado real
    else Operación no soportada sin conexión
        Browser-->>Cajero: Bloquear y explicar alternativa
    end
~~~

**Regla:** offline de POS no equivale a comprobante tributario emitido. No prometer recuperación si se pierde la caché del navegador. La modalidad fiscal de contingencia requiere validación independiente.

## UC-07. Alta de un comercio y habilitación operativa

~~~mermaid
sequenceDiagram
    autonumber
    actor Propietario
    participant Portal as Asistente de alta
    participant SaaS as Operación SaaS
    participant ERP as Instancia Odoo aislada
    participant Fiscal as Preparación fiscal
    participant QA as Pruebas y aprobación
    Propietario->>Portal: Solicitar alta y aceptar condiciones
    Portal->>SaaS: Crear tenant con identidad única
    SaaS->>ERP: Aprovisionar DB, filestore y secretos aislados
    SaaS->>QA: Verificar aislamiento, HTTPS y restauración
    Propietario->>Portal: Configurar tienda y catálogo
    Portal->>ERP: Guardar configuración validada
    Propietario->>Portal: Solicitar habilitación fiscal
    Portal->>Fiscal: Verificar modalidad y credenciales autorizadas
    Fiscal->>QA: Reportar pruebas y pendientes
    alt Gates comerciales, operativos y fiscales aprobados
        QA->>SaaS: Autorizar salida a producción
        SaaS-->>Propietario: Instancia habilitada
    else Falta algún requisito bloqueante
        QA-->>Portal: Mostrar bloqueos y siguientes pasos
        Portal-->>Propietario: Solo demo o servicio acotado permitido
    end
~~~

**Regla:** crear una base de datos no habilita automáticamente la emisión real. Para un piloto sin CPE integrado, la limitación contractual y el emisor externo deben estar explícitos.

## Puntos de implementación aún no resueltos

1. Contrato de creación del documento fiscal desde POS hacia el modelo real de Odoo Community 19.
2. Si OPeru + Nubefact cubre facturas, boletas y notas para el segmento; confirmar licencias, dependencias y precios.
3. Ubicación y transacción de la cola persistente, política de bloqueo por documento y consulta de estados.
4. Reglas por modalidad SUNAT, tipo documental y mecanismo de respuesta; no imponer un estado universal falso.
5. Integración de pagos externos: registro manual vs confirmación automática.
6. Política offline por navegador y hardware, y contingencia tributaria.
7. Matriz de permisos de cajero, supervisor, contador, soporte y operador SaaS.
