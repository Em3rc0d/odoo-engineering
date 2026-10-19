# Reglas de negocio e invariantes — IPC-BR-001

**Fecha:** 2026-10-19. Cada BR es un contrato de dominio propuesto; debe tener prueba positiva/negativa ligada a SRS, no un comentario de código.

| ID | Regla de negocio | Fallo/resultado esperado |
|---|---|---|
| BR-001 | Venta, pago y comprobante fiscal son hechos independientes y se visualizan separadamente. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-002 | El sistema comercial de registro es Odoo; el adaptador fiscal no escribe directamente movimientos comerciales. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-003 | Un RUC emisor y una modalidad legal verificados preceden la emisión productiva. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-004 | La identidad documental combina emisor, tipo, serie y número, con unicidad. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-005 | La numeración fiscal no proviene de IDs temporales del navegador. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-006 | La confirmación de venta es idempotente por clave estable que persiste reinicios. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-007 | El stock se descuenta exactamente una vez por operación procesada. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-008 | Una caja abierta es condición para cobrar; excepciones se definen formalmente. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-009 | El efectivo inicial se declara con usuario y fecha. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-010 | El conteo real no puede sustituir silenciosamente el esperado. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-011 | Las diferencias de caja conservan actor, motivo y autorización requerida. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-012 | Un Yape/Plin registrado manualmente no equivale a confirmación bancaria. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-013 | La factura requiere identidad del comprador compatible con el régimen aplicable. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-014 | La modalidad/tributación decide el circuito fiscal, no el nombre de un botón. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-015 | Un ticket POS no equivale a CPE válido. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-016 | Una prueba local de CPE siempre se rotula SIMULADA / NO SUNAT. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-017 | Una respuesta de transporte 200 no garantiza aceptación fiscal. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-018 | Un envío incierto permanece desconocido hasta evidencia o resolución formal. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-019 | Está prohibido reemitir/renumerar a ciegas una identidad tras timeout. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-020 | Los XML firmados y respuestas recibidas son evidencia inmutable. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-021 | Una corrección fiscal conserva referencia al original y procedimiento aplicable. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-022 | Las devoluciones no pueden exceder cantidades originales no devueltas. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-023 | Devolver producto, registrar reembolso y emitir nota son operaciones distintas. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-024 | El producto dañado no regresa automáticamente a stock vendible. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-025 | El modo offline del POS no concede facultad tributaria de emitir sin conexión. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-026 | El navegador sin caché puede perder pendientes offline; nunca prometer invulnerabilidad. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-027 | El tenant no puede leer DB, filestore, backup ni secretos de otro tenant. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-028 | Cada tenant tiene configuración y credenciales fiscales separadas. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-029 | El soporte accede a datos sensibles solo con delegación limitada y auditada. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-030 | Los secretos nunca se versionan ni imprimen en logs o tickets. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-031 | El respaldo requiere DB, filestore y configuración necesaria coherentes. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-032 | La restauración se declara válida solo tras ejecutar prueba funcional y de adjuntos. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-033 | Las suspensiones de suscripción respetan conservación y exportación contractual/legal. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-034 | Los precios y márgenes son hipótesis hasta disponer de pagos y costos medidos. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-035 | No se incorporan addons ni material con licencia/procedencia incierta. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-036 | No se modifican activos originales de INVY ni se confunde metodología de copia con apropiación. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-037 | El snapshot Rally permanece independiente y fuera del runtime MVP. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-038 | Una salida a producción requiere gates G0–G4 aplicables con evidencia, responsables y aceptación. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-039 | Cada excepción crítica tiene estado, dueño, causa y paso de resolución visible. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-040 | Los datos CI/demo son sintéticos, no clientes ni contribuyentes reales. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-041 | Los cambios legales SUNAT exigen reevaluación de requisitos, pruebas y adaptador. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-042 | Una venta anulada/corregida no borra su rastro de pago/stock/fiscal. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-043 | Los horarios y cortes de reporte se presentan en zona de tiempo explícita. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-044 | Las políticas de precios e impuestos no alteran totales de ventas históricas. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |
| BR-045 | Ningún incidente de seguridad entre tenants se considera tolerable para release. | Violación bloquea acción o genera incidencia trazable, sin silenciar evidencia |

## Matrices regulatorias pendientes

| Matriz | Variable | Necesita validación |
|---|---|---|
| Documento | 01 factura / 03 boleta / notas | datos comprador, serie, documento correctivo, envío/resumen |
| Impuesto | IGV 18% gravado vs demás perfiles | cálculo y redondeos, extensiones no MVP |
| Modalidad | SEE contribuyente / PSE / OSE | autorización, certificado, canal, competencia y contrato |
| Contingencia | fallo red/SUNAT/host | mecanismo legal y tiempo permitido |
| Custodia | XML, constancia/CDR, representación | políticas de conservación, acceso y recuperación |
| Privacidad | cliente y consumidor | rol responsable/encargado, minimización y derechos |

Estas filas son condiciones por resolver, no declaraciones de procedimiento legal vigente.
