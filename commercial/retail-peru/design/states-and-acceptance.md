# Estados, fallas y criterios de aceptación

**DUX-QA-001.** Los estados son un **modelo conceptual**; la integración definitiva debe respetar los modelos reales de Odoo y la normativa aplicable. No son migraciones de base de datos ni tests ejecutados.

## 1. Tres ejes independientes

| Eje | Estados de presentación | Evidencia para avanzar |
|---|---|---|
| Comercial | Borrador / confirmada / cancelación o devolución vinculada | Operación persistida y autorizaciones |
| Pago | No registrado / registrado manual / confirmado por tercero / reembolso pendiente / reembolsado | Registro interno o respuesta del procesador, según medio |
| Fiscal | No solicitado / pendiente / en proceso / resultado favorable verificado / rechazado / desconocido / requiere atención | Eventos del adaptador y evidencia aplicable |

Ejemplo: **venta confirmada + Yape registrado manualmente + documento fiscal pendiente**. Es una combinación válida; no debe mostrarse como «todo aceptado».

## 2. Máquina conceptual de solicitud fiscal

~~~mermaid
stateDiagram-v2
    [*] --> NoSolicitado
    NoSolicitado --> Pendiente: Venta elegible confirmada
    Pendiente --> Validando: Trabajo tomado
    Validando --> RequiereAtencion: Datos inválidos
    Validando --> Enviando: Documento preparado
    Enviando --> ResultadoPendiente: Entrega técnica sin resultado final
    Enviando --> Desconocido: Timeout / respuesta perdida
    Enviando --> Rechazado: Rechazo expreso
    Enviando --> Favorable: Evidencia fiscal válida
    ResultadoPendiente --> Favorable: Conciliación verificada
    ResultadoPendiente --> Rechazado: Rechazo verificado
    ResultadoPendiente --> Desconocido: No verificable
    Desconocido --> ResultadoPendiente: Consulta de estado
    Desconocido --> RequiereAtencion: Escalamiento
    Rechazado --> RequiereAtencion: Revisar subsanación
    RequiereAtencion --> [*]: Caso documentado
    Favorable --> [*]
~~~

La corrección crea un **nuevo evento u operación relacionada** según el procedimiento; no se edita el pasado ni se reutiliza la identidad fiscal de forma insegura. «Favorable» se refiere a la evidencia exigible para esa modalidad, no a un HTTP exitoso.

## 3. Estados de caja

~~~mermaid
stateDiagram-v2
    [*] --> Cerrada
    Cerrada --> Abierta: Apertura autorizada
    Abierta --> EnCierre: Solicitar cierre
    EnCierre --> Cerrada: Conteo conciliado
    EnCierre --> PendienteSupervisor: Diferencia fuera de política
    PendienteSupervisor --> Cerrada: Aprobación y acta
    PendienteSupervisor --> Abierta: Reanudar según procedimiento
~~~

## 4. Criterios de aceptación por recorrido

| Prueba de diseño | UC | Dado | Cuando | Entonces |
|---|---|---|---|---|
| T-01 | UC-01 | Caja abierta y productos válidos | Se confirma una venta | Existe una sola venta con referencia estable |
| T-02 | UC-01 | Pago Yape declarado manualmente | Se confirma la operación | UI dice «registrado manualmente», no «banco confirmó» |
| T-03 | UC-01 | Venta confirmada elegible para CPE | Se genera solicitud | Solicitud fiscal durable, vinculada y única |
| T-04 | UC-01 | Canal devuelve resultado favorable | Se verifica evidencia aplicable | UI muestra estado sustentado y archivo disponible |
| T-05 | UC-02 | Canal rechaza expresamente | Se procesa rechazo | Venta persiste, motivo visible, sin editar XML firmado |
| T-06 | UC-03 | Timeout tras enviar | Se pierde respuesta | Estado desconocido; no reenvío ciego |
| T-07 | UC-03 | Documento incierto | Se consulta el canal | Conciliación sobre misma identidad o escalamiento |
| T-08 | UC-04 | Venta ya devuelta parcialmente | Se solicita otra devolución | No supera cantidad original ni duplica reembolso |
| T-09 | UC-04 | Devolución autorizada | Se ejecuta | Stock, dinero y documento correctivo trazados por separado |
| T-10 | UC-05 | Caja con diferencia | Se solicita cierre | Se conserva conteo y requiere autorización si aplica |
| T-11 | UC-06 | Conexión perdida | Se intenta función no validada offline | Bloqueo claro sin afirmar CPE emitido |
| T-12 | UC-06 | Venta offline permitida pendiente | Se sincroniza dos veces | El servidor confirma una sola venta |
| T-13 | UC-07 | Nuevo tenant | Se provisiona | DB, filestore y secretos separados y acceso cruzado denegado |
| T-14 | UC-07 | Emisor no habilitado | Solicita emitir en producción | Bloqueo explícito; demo separada |
| T-15 | UC-07 | Backup generado | Se restaura en entorno aislado | Datos y adjuntos verificables; no solo archivo existente |
| T-16 | UC-01 | Cajero confirma dos veces | Llega solicitud repetida | Sin duplicar venta, stock, pago ni solicitud fiscal |
| T-17 | UC-01 | El navegador se cierra tras confirmar | Cajero vuelve a entrar | Consulta resultado real antes de ofrecer repetir |
| T-18 | UC-02 | Certificado/credencial falla | Se intenta emisión | Bloqueo o incidencia, sin revelar secreto |
| T-19 | UC-07 | Soporte sin permiso | Intenta leer datos de cliente | Acceso denegado y auditable |
| T-20 | UC-05 | Caja cerrada | Cajero intenta vender | Se impide o se redirige a apertura autorizada |

Estas son **pruebas propuestas**, no resultados. Deben automatizarse o ejecutarse con evidencia al implementar.

## 5. Incidencias y mensajes

| Evento | Lo que ve el cajero / dueño | Lo que ve el equipo autorizado |
|---|---|---|
| SUNAT/proveedor no disponible | «El comprobante está pendiente; la venta se guardó» | Correlación, último intento, cola, política de consulta |
| Respuesta desconocida | «Aún no se confirma el estado del documento» | Identidad fiscal, envío y pasos de conciliación |
| Rechazo | «El comprobante requiere atención» | Código, descripción, XML, respuesta, responsable |
| Pago electrónico no verificado | «Pago registrado; verifica confirmación» | Fuente y evidencia de pago |
| Doble clic | «La operación ya está registrada» | Identificador original y trazas de idempotencia |
| Sin stock | «No hay existencias suficientes según la política» | Existencia y reserva real del servidor |
| Sin internet | «Operación sin conexión limitada» | Pendientes locales y riesgo de caché |
| Certificado vencido | «Emisión fiscal no disponible» | Motivo, emisor, vencimiento, plan de renovación |
| Diferencia de caja | «Hay una diferencia de S/ X» | Conteo, movimientos, justificación y aprobador |
| Backup fallido | «Servicio en revisión» solo si impacta al cliente | Alerta operativa, última copia válida, escalamiento |

## 6. Trazabilidad hacia gates existentes

- **G0:** validar con comerciantes que S10–S16 y S20–S22 cubren problemas reales; revisar derechos/licencias.
- **G1:** ejecutar T-01, T-08, T-10, T-13, T-15, T-16, T-17, T-20 en Odoo 19 aislado, con pruebas negativas.
- **G2:** piloto POS delimitado, con emisión externa si no hay CPE integrado; no confundir ticket con comprobante fiscal.
- **G3:** ejecutar T-03–T-07, T-09 y T-18 en integración fiscal real autorizada, con evidencias por tipo documental.
- **G4:** medir onboarding, soporte, restauraciones, margen y retención en dos o más pilotos comparables.

Los gates originales permanecen en [acceptance-gates.md](../acceptance-gates.md) y **no** se marcan aprobados por producir este diseño.

## 7. Decisiones abiertas para la próxima revisión

- Rubro minorista inicial, hardware, tipos de pago y política de stock.
- Qué pantallas son configuración Odoo y cuáles requieren extensión propia.
- Reglas fiscales de boleta, factura, notas, anulaciones y contingencia.
- Proveedor fiscal, modalidad autorizada y evidencia verificable.
- RPO/RTO y objetivos de disponibilidad sostenibles económicamente.
- Accesibilidad y dispositivo principal de caja.
- Matriz RF/RNF del SRS: **pendiente de enlazar a sus identificadores oficiales**, sin inventarlos.
