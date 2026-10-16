# Integración SUNAT desde Odoo Community 19 — MK0/MK1 y experimento

**Corte: 16 de octubre de 2026.** Estado: contrato de datos, transporte Nubefact experimental y **pruebas locales con HTTP simulado**, no emisión fiscal. NO instalar directamente en empresas.

## Decisión técnica

**Ruta preferida para vender rápido:** comprobar instalación/licencia de los módulos OPeru 19 (`l10n_pe_edi_base`, `l10n_pe_edi_odoofact`) sobre Odoo Community 19, con una cuenta **propia/autorizada** Nubefact de pruebas. El fabricante describe Odoo → Nubefact → SUNAT y declara soporte para facturas, boletas y notas. Solicitar condiciones de API, tarifas, soporte, licencia y posibles cuotas por comprobante; los módulos y la API NO son necesariamente el mismo contrato comercial.

**Plan alternativo:** integración propia limitada al proveedor mediante `nubefact_gateway/` (fuente original en este repositorio), después de validar el payload y la cuenta de pruebas. Este código NO es todavía un addon instalado en Odoo ni un reemplazo de un PSE/OSE. Tampoco implementa generación/firma UBL, consultas, anulaciones ni notas.

**No elegir** desarrollo directo de SOAP SUNAT como primera ruta: añade firma, UBL, CDR, identidad de emisión, certificados, contigencias y operación normativa. SUNAT sí publica servicios beta/producción, pero que existan endpoints no equivale a estar habilitado para emitir.

## Fuentes confirmadas

- Odoo 19 localización oficial: https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html
- Código público Odoo 19: https://github.com/odoo/odoo/tree/19.0/addons/l10n_pe y https://github.com/odoo/odoo/tree/19.0/addons/l10n_pe_pos
- OPeru E-Documents 19.0: https://apps.odoo.com/apps/modules/19.0/l10n_pe_edi_base
- OPeru OdooFact 19.0: https://apps.odoo.com/apps/modules/19.0/l10n_pe_edi_odoofact
- Integración oficial Nubefact JSON: https://www.nubefact.com/integracion
- SUNAT servicios beta/producción y consulta: https://orientacion.sunat.gob.pe/guias-manuales-y-servicios-web
- SUNAT definición PSE: https://cpe.sunat.gob.pe/aliados/pse
- SUNAT definición OSE: https://cpe.sunat.gob.pe/aliados/ose
- OPeru flujo Odoo→Nubefact: https://www.operu.pe/facturacion-electronica

## Evidencia y límites

Odoo documenta `l10n_pe_edi` como motor EDI, pero su disponibilidad para nuestra distribución Community requiere verificación directa de instalación y licencia. `l10n_pe` y `l10n_pe_pos` existen en fuente Community; no confundirlos con EDI listo para producción.

El módulo fuente `integrations/sunat/nubefact_gateway/` implementa **solamente**: estructura de factura/boleta de venta interna PEN gravada al 18%, controles de identidad/numeración, suma de líneas y redondeo, hash de solicitud, proyección conservadora del estado reportado por proveedor y transporte HTTPS con lista estricta de hosts aprobados, sin reintentos y con autorización explícita. Se probó localmente con `unittest` y HTTP simulado; **ninguna cuenta, certificado o API real fue consultada**.

No es una conversión automática de `account.move` ni controla por sí sola duplicados entre procesos. Un error de comunicación implica resultado incierto: consultar manualmente antes de reenviar. Estado `provider_reports_accepted` significa solo que el proveedor lo informó, no que hayamos descargado/verificado la CDR. Ninguna validación fiscal está certificada.

## Probar únicamente contratos, sin emitir nada

```bash
cd integrations/sunat
python3 -m unittest discover -s tests -v
python3 -m compileall -q nubefact_gateway tests
```

El transporte se construye con `enable_emission=False` y además exige `human_authorized=True` por invocación. **No habilitar** ambos interruptores hasta tener proveedor, entorno correcto, clave propia, política de outbox, serie/número únicos y verificación de estados. Los tests utilizan un opener simulado que no realiza solicitudes de red.

## Diseño final esperado (no implementado)

```text
Odoo POS → account.move publicado + serie/número único
         → outbox transaccional por (RUC,tipo,serie,número)
         → adaptador OPeru oficial del proveedor [camino preferido]
            O bridge de Nubefact sólo si la adopción anterior falla
         → Nubefact PSE/OSE autorizado → SUNAT
         → respuesta + CDR/XML/PDF verificados
         → estado fiscal + auditoría + archivo + soporte
```

Reglas: nunca emita desde un evento POS no confirmado; bloqueo/clave única por CPE; una sola fuente de números; diferencia entre error HTTP, entrega incierta, rechazo expreso y CDR aceptada; ningún reintento ciego; credenciales por RUC custodiadas fuera de Git/logs; reversos/notas como operaciones nuevas, no eliminación de registros.

## Pendientes antes de conectar Odoo

1. Verificar que los módulos OPeru sean realmente compatibles con **Community 19** y sus dependencias, sin requerir Enterprise inadvertidamente, y si facturación POS precisa otro módulo.
2. Cotizar Nubefact: cuenta de desarrollo, activación, costo por volumen y autorización PSE del contribuyente.
3. Obtener de un emisor autorizado una cuenta de pruebas, comprobantes de ensayo y reglas de tipo, serie, IGV, descuentos, exoneración, anticipos, notas.
4. Instalar módulos en un lab Odoo 19 aislado y **ejecutar** emisión→consulta→CDR con evidencias, nunca con datos reales en CI.
5. Confirmar flujo POS→`account.move`→proveedor; revisar casos de boleta, factura, notas, devolución, doble clic, corte de red y concurrencia.
6. Implementar outbox/transiciones de estado y almacenamiento XML/CDR/PDF de manera fiable, con fallas recuperables.
7. Revisar privacidad, retención, responsabilidad fiscal, poderes del emisor, contratos PSE/OSE, competencia comercial, titularidad y soportabilidad.
8. Mantener SIRE, GRE, RUC/DNI enrichment, PDF para cliente, bulk y offline avanzado fuera del MVP hasta validar demanda.

**Gate:** nada se declara `SUNAT_INTEGRATED` antes de una emisión autorizada y CDR real verificadas.
