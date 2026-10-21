# INVY Perú — MK2: decisión fiscal y diferenciación comercial

Corte: 2026-10-21. Estado: **MK2 documental y laboratorio parcial; NO GO comercial ni fiscal**.

Este MK respeta el SRS existente de MK1 (88 RF y 43 RNF) sin alterarlo. No representa nuevos contratos con SUNAT, emisiones reales, instalaciones de OPeru, clientes, ventas ni aceptación del mercado.

El flujo es: brainstorming → design → arch → plan → build → test, con mining-site y quarries. El propio SRS sigue siendo la autoridad funcional.

## Objetivos
- Determinar con evidencias qué ruta fiscal merece una prueba autorizada.
- Comprobar la diferencia entre Odoo Community instalado y documentación de EDI de otras ediciones/distribuciones.
- Descartar posicionamientos POS genéricos sin diferenciación económica.
- Definir protocolos reproducibles de la próxima prueba: POS en navegador, factura contable simulada, recuperación, permisos, duplicados y respaldo.
- Mantener separado objetivo empresarial de supuestos de rentabilidad.

## Archivos del MK
- [brainstorming](brainstorming/01-falsification.md): preguntas y casos de descarte.
- [design](design/01-user-outcomes.md): resultados medibles, no más pantallas por inercia.
- [arch](arch/01-fiscal-matrix.md): decisión fiscal comparativa, manifest y derechos.
- [plan](plan/01-gates.md): secuencia y bloqueos.
- [plan económico](plan/02-economics.md): escenarios y riesgos de margen.
- [build](build/01-module-probe.md): verificación técnica efectuada y reproducibilidad.
- [test](test/01-evidence.md): qué pasó y qué no está probado.
- [mining-site](mining-site/01-sources.md): fuentes y versiones.
- [quarries](quarries/01-findings.md): contradicciones y contraargumentos.

**Resultado provisional:** continuar validación técnica con datos ficticios. Elegir proveedor, transmitir CPE, publicar SaaS y captar clientes siguen bloqueados por sus respectivos gates. El expediente comercial independiente mantiene L1 por la relación laboral.

## Avance puntual de integración ORM (21/oct/2026)

La [prueba automatizada de dos facturas contables contra el simulador](../../../experiments/retail-pos-lab/DEMO-RUNBOOK.md) pasó en [CI 39644924493](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39644924493); rechazo de duplicación, resultado incierto y consulta simulada; rollback sin persistencia. No se ha recorrido **POS→factura→simulador en navegador** y ningún CPE real fue emitido.

## Avance POS hasta simulador, solo ORM (21/oct/2026)

El [workflow 39645784357](https://github.com/Em3rc0d/odoo-engineering/actions/runs/39645784357) pasa `POS_INVOICE_SIM_SMOKE_OK`: venta POS pagada en efectivo → `account.move` publicado → respuesta local SIMULADA → duplicado bloqueado → cierre de caja y stock -1 con rollback. El navegador POS y el CDR de SUNAT siguen pendientes. [UAT real del navegador y riesgo contable](test/02-browser-and-accounting-uat.md).
