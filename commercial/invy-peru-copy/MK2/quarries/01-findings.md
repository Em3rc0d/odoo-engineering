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
