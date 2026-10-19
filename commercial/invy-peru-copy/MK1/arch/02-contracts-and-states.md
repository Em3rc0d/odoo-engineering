# Contratos y estados — IPC-CONTRACT-001

Los contratos siguientes son **lógicos y propuestos**, no endpoints actualmente desplegados. Versionar DTO, no acoplar el dominio a los campos de Nubefact/Greenter.

## Comando comercial POS

**Entrada:** tenant_id; cash_session_id; client_order_uuid estable; SKU/cantidad; precio/impuesto calculado según servidor; comprador; medio de pago con tipo MANUAL o PROVIDER_CONFIRMED; requested_doc_type opcional. **Salida:** sale_id, snapshot y hash, commercial_state, payment_state, fiscal_state y timestamps. **Reintento:** devolver respuesta asociada al UUID, nunca crear orden duplicada.

### Precondiciones

Sesión abierta autorizada, productos disponibles y tax profile soportado, total reconciliado, regla stock, permiso de quien cobra, prueba server-side. El cliente no dicta un estado fiscal favorable.

## Solicitud fiscal y outbox

**Entrada:** tenant_id, issuer_ruc, document_kind, series, number, commercial_ref, invoice_snapshot_version, taxpayer_mode, unique_idempotency_key, payload_hash, created_at. **Persistir de forma atómica o mediante patrón demostrablemente seguro respecto a factura.** Unicidad por (issuer_ruc, kind, series, number) + (commercial_ref, logical_operation).

**Estados internos:** REQUESTED → VALIDATING → READY → SIGNED → SENDING → WAITING / UNKNOWN / REJECTED / VERIFIED_RESULT. Estados precisos de SUNAT no se reducen a esta abstracción sin mapping por modalidad.

## Respuesta de adaptador

Campos: request_id, attempt_id, adapter_version, technical_transport_status, provider_reference, fiscal_evidence_status, response_code, response_message_redacted, evidence_refs[], evidence_hashes[], observed_at, confirmation_source. **Prohibido:** accepted=true a partir de 200 HTTP, desambiguar timeout como fallo seguro, imprimir certificado o comprador completo en logs.

## Reconciliación de incertidumbre

1. Capturar envío/attempt y punto de corte.
2. Si error previo a transmisión probado, reprogramar bajo política.
3. Si envío pudo llegar, marcar UNKNOWN; consultar por ID o mecanismo permitido.
4. Si respuesta y constancia verificables, transicionar en mismo documento.
5. Si estado sigue incierto, abrir ticket al responsable autorizado; sin reemisión/renumeración ciega.
6. Si hace falta subsanar, iniciar operación vinculada y conservar original.

## Máquina de estado comercial, pago y fiscal

~~~mermaid
stateDiagram-v2
    state "Comercial" as C {
      [*] --> Borrador
      Borrador --> Registrada: Confirmación única
      Registrada --> DevoluciónVinculada: Política autorizada
    }
    state "Pago" as P {
      [*] --> SinRegistro
      SinRegistro --> Manual: Declaración cajero
      SinRegistro --> ConfirmadoTercero: Evidencia proveedor
      Manual --> ConciliaciónPendiente: Verificación
      ConfirmadoTercero --> Reembolso: Operación independiente
    }
    state "Fiscal" as F {
      [*] --> NoSolicitado
      NoSolicitado --> Pendiente: Emisor habilitado
      Pendiente --> EnProceso
      EnProceso --> ResultadoVerificado: Evidencia fiscal
      EnProceso --> Rechazo: Respuesta expresa
      EnProceso --> Desconocido: Timeout ambiguo
      Desconocido --> ResultadoVerificado: Consulta válida
      Desconocido --> Revisión: Sin evidencia
      Rechazo --> Revisión: Subsanación
    }
~~~

## Contratos de devolución

ReturnRequest tiene sale_ref, lines_qty, condition, supervisor_authorization, reason; ReturnEffects separa stock_effect (vendible/no vendible), money_effect (reembolso/manual/pendiente), fiscal_effect (nota/resolución/bloqueado), evidencia y relación a documentos previos.

## Caja

~~~mermaid
stateDiagram-v2
    [*] --> Cerrada
    Cerrada --> Abriendo
    Abriendo --> Abierta: Saldo y usuario
    Abierta --> EnArqueo
    EnArqueo --> Cerrada: Conciliado o aprobado
    EnArqueo --> PendienteAutorización: Diferencia excedida
    PendienteAutorización --> Cerrada: Supervisor + acta
~~~

Si existen draft/pagos inconciliables, cierre bloqueado o en revisión. Lo cerrado no edita el pasado.

## Offline

ClientOrderUUID estable dentro del navegador permitido y sincronización idempotente al volver internet. Cualquier estado local se distingue de confirmación servidor. Sin red no existen garantías de stock global actual ni de CPE válido. No prometer persistencia cuando el usuario borra caché o cierra sesión incorrectamente.

## Esquema de errores funcionales

400 VALIDATION (campo/requisito), 401/403 identidad/permiso, 409 CONFLICT (idempotencia/serie/stock), 422 TAX_RULE, 429 RATE_LIMIT, 503 DEPENDENCY_UNAVAILABLE, 504 UNKNOWN_OUTCOME. No se exige implementar exactamente HTTP REST: son categorías de contrato; el endpoint real y códigos se deciden cuando se cierre la tecnología.
