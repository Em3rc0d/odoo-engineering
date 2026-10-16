# Salidas técnicas y comerciales

**Nunca confundir:** fuentes Odoo existentes / instalaciones exitosas / casos de uso correctos / pilotos comerciales / paridad con INVY. Son escalones distintos.

## G0 — Viabilidad y derechos

- [ ] Competidor auditado con fuentes y capturas legales; 22 capacidades clasificadas en `parity.json`, dudas registradas.
- [ ] 10 entrevistas efectivas con operadores o dueños independientes; al menos 5 del perfil objetivo.
- [ ] Solución actual, gasto, pérdidas, soporte y obstáculos registrados sin datos personales innecesarios.
- [ ] Licencias de Odoo / extensiones, titularidad de nuestro nuevo código y limitaciones de marca revisadas.
- [ ] Seleccionar quién compra y qué tres problemas tendrán prioridad. Si no hay problemas costosos repetidos, PIVOT/KILL.

## G1 — Demo de núcleo POS en entorno desechable

- [ ] Odoo 19 Community arranca reproduciblemente con tag/commit y módulos `point_of_sale`, `stock`, `purchase` y `l10n_pe` disponibles.
- [ ] Crear 2 tiendas ficticias aisladas con catálogo independiente (DB y filestore); nada de datos de clientes.
- [ ] Importación de 100 SKU ficticios, 2 usuarios, 1 caja. Trazar tiempo y pasos exactos.
- [ ] Comprar/ingresar 10 unidades, vender 2, verificar stock físico-contable configurado.
- [ ] Venta multiartículo, descuentos/IGV redondeo, apertura/cierre con diferencia controlada.
- [ ] Devolución, cancelación y reinicio/reintento sin duplicar pedido o stock.
- [ ] Prueba negativa entre tenants, permisos operario vs administrador.
- [ ] Exportación, backup DB+filestore y restauración en instancia separada con comprobación.

## G2 — Piloto POS e inventario delimitado

- [ ] Cliente firma aceptación y describe si usa emisor SUNAT externo; sin confundir ticket POS con CPE.
- [ ] Datos reales importados con consentimiento y proceso de reversión; inventario inicial conciliado.
- [ ] Pilotaje paralelo acordado para no interrumpir el negocio.
- [ ] Canal/horario de soporte y responsables explícitos; incidentes críticos y pérdida de ventas tienen rollback.
- [ ] Costo por alta y soporte medidos; acuerdo de precio pagado verificable.

## G3 — Competencia directa con INVY Pyme

**Puerta crítica fiscal:** si el cliente necesita CPE desde el mismo POS, G3 se BLOQUEA hasta prueba real SUNAT/OSE/PSE bajo autorización.

- [ ] POS→comprobante legal en una operación; boleta y factura con números/estados correctos.
- [ ] CDR aceptación/rechazo, XML/PDF y emisión sin duplicación; recuperación de fallos documentada.
- [ ] Notas de crédito/devoluciones, anulaciones o bajas según régimen/procedimiento aplicable y prueba real.
- [ ] Confirmación de certificado, RUC/emisor, retención, estado de la transacción y límites contratados.
- [ ] Política de costos por documento y contingencia incluida en precio.
- [ ] Un usuario de tienda completa tareas principales sin asistencia intensiva.
- [ ] Comparación funcional con INVY por escenario, sin afirmar igualdad absoluta ni copiar activos protegidos.

## G4 — Escala

- [ ] 2+ pilotos pagados independientes con el mismo build/config estándar.
- [ ] Variación de tiempo de onboarding y soporte mensual documentada.
- [ ] Retención/uso durante un periodo operativo completo; tickets y razones de cancelación registrados.
- [ ] Margen de contribución positivo tras costos variables y soporte; CAC/recuperación justificables.
- [ ] Monitoreo, backups probados, incidentes, upgrades con rollback, acceso y datos protegidos.
- [ ] Decisión GO/PIVOT/KILL fundada en evidencia y aprobada explícitamente.

**Estado de todas las casillas:** PENDIENTE hasta aportar logs, actas o contratos. Esta documentación no ejecuta pruebas.
