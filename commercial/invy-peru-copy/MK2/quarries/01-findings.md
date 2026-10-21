# Quarries · hallazgos críticos y contradicciones

**Q01 — Comunidad vs documentación.** Odoo documenta l10n_pe_edi, pero el manifest no está en el código público Community 19. El inventario CI del laboratorio muestra ausentes los add-ons externos. La respuesta es NO DISPONIBLE EN ESTA IMAGEN, no NO EXISTE EN NINGUNA EDICIÓN.

**Q02 — Open-source no implica operación sin costo.** Greenter, Kembec y CPEForge se anuncian MIT; requieren mantenimiento de firmas/certificados/CDR, otro runtime o enlazado y guardias de seguridad. OPeru se anuncia LGPL-3 con dependencias y Nubefact, cuyo plan ONLINE no equivale al API contractual.

**Q03 — Catálogos no identificados.** OPeru pide catálogos SUNAT; Ganemo vende otro addon con nombre parecido y OPL-1. Identidad de dependencia desconocida: prohibido concluir que OPeru obliga a comprar Ganemo o que no existe ninguna dependencia propietaria.

**Q04 — Competidores fuertes.** INVY Pyme vende 500 CPE por S/169 inc. IGV, Alegra POS Pyme anuncia 1000 CPE por S/93 inc. IGV, Bsale desde S/189. Comparar solo precio/volumen no nos favorece. Ningún cliente ha mostrado que nuestro onboarding/soporte resuelva un dolor pagable que esas suites no cubran.

**Q05 — Éxito técnico parcial.** CHECKOUT_SMOKE_OK confirma caja/venta/stock con rollback. EDI_PROBE_OK confirma módulos instalados/ausentes. No existe navegación humana POS→factura→simulador ni prueba de dos cajas/tenants ni XML/CDR real. No falsificar el gate.

**Q06 — Conflicto laboral.** El registro comercial mantiene L1 bloqueado. Ningún hallazgo técnico permite contactar compradores, empleados/prospectos del empleador ni vender el prototipo sin aclararlo.

## Test de falsación antes de adoptar
Para cada proveedor: licencias transitivas y accesibilidad de módulos; instalación Community 19 legal; fixture UBL firmado; rechazo/timeout/correlativo único; respuesta CDR real autorizada; TCO 100/500/1000 documentos; costos de continuidad; compatibilidad nota/boleta; responsable operativo. Si falla uno crítico, PIVOT/KILL.

**Veredicto MK2 actual:** GO limitado a seguir investigación y laboratorio. NO GO emisor fiscal, SaaS multi-tenant y ventas. Es una decisión consciente, no trabajo pendiente oculto.

**Q07 — Riesgo de doble costo contable condicionado (fuente externa):** [odoo/odoo#290124](https://github.com/odoo/odoo/issues/290124) reporta COGS duplicado al utilizar inventario FIFO/valoración automática + contabilidad anglosajona + actualización de stock al cierre + creación masiva de facturas POS desde asistente, antes o después del cierre. [PR de reproducción #290126](https://github.com/odoo/odoo/pull/290126) describe tests-only; no se confirmó reparación ni reproducción contra nuestra imagen. Nuestra prueba usa el método individual de pedido POS, por tanto **no implica ese defecto**. Añadir test contable específico si esa configuración se ofrece; evitar afirmar exactitud de COGS desde una prueba de unidades en stock.

**Q08 — Caso real UAT: sobrepago digital manual produce cambio de efectivo implícito.** [6 capturas del operador](../test/UAT-2026-10-21-01.md) muestran venta S/11.80, digital registrado S/20, vuelto S/8.20 y caja esperada S/91.80 desde S/100, pese a no haber confirmación bancaria. El `payment_screen.js` upstream permite exceso cuando hay medio Cash. Si se entregó efectivamente vuelto, el valor cuadra; si no, la conciliación física se rompe. [Issue #6](https://github.com/Em3rc0d/odoo-engineering/issues/6). **No arreglar core Odoo sin decidir primero política exact-only o cash-out explícito**, implementar pruebas negativas, permisos y manejo de discrepancias. Estado UAT BLOCKED FOR ACCEPTANCE, no explotación/compliance evidenciado.
