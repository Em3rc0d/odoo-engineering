# Odoo 19 Community + simulador CPE local

## Estado y alcance

**Integrado en código para prueba local; instalación/ejecución real de Odoo aún por verificar en CI/Docker.**
Este laboratorio usa `Odoo 19 Community`, `PostgreSQL 16`, módulos nativos POS/inventario y un addon propio `oe_pe_cpe_lab` montado automáticamente desde `local-addons/`. Reutiliza el **mismo contrato Python Nubefact JSON** bajo `integrations/sunat/nubefact_gateway`, montado en `/opt/retail-sunat-integration` y accesible mediante `PYTHONPATH`.

El addon sólo **simula** aceptación/rechazo/timeout después de preparar un payload fiscal con datos de una factura contabilizada. No hay HTTP a SUNAT/Nubefact, ni XML, firma digital, CDR real, consulta de comprobantes oficiales, anulación ni emisión válida. No admite certificados ni tokens. Nunca usar con transacciones tributarias reales.

## Requisitos

Docker Desktop con Compose v2, Bash (WSL recomendado en Windows), Python 3, espacio en disco y memoria suficiente. Versiones pinneadas de imagen: `odoo:19.0-20260908` y `postgres:16-bookworm`.

## Arranque — laboratorio nuevo

```bash
git clone https://github.com/Em3rc0d/odoo-engineering.git
cd odoo-engineering/experiments/retail-pos-lab
bash scripts/lab.sh validate-contract
bash scripts/lab.sh init
bash scripts/lab.sh up
bash scripts/lab.sh version
```

Abrir **http://127.0.0.1:8079**. En el gestor inicial crea la base **`retail_peru_lab`**. Para obtener la contraseña maestra localmente:

```bash
bash scripts/lab.sh master-password
```

No utilices identificadores ni datos reales. Escoge usuario y contraseña de administrador únicos para este laboratorio. Si la base ya existía de una prueba anterior, el script conserva sus volúmenes y su contraseña.

## Instalar el addon y módulos base

En Odoo configura país **Perú**, PEN, Contabilidad/Facturación, `l10n_pe`, `point_of_sale` e `stock`. Los nombres visuales pueden diferir; `oe_pe_cpe_lab` aparece bajo Apps una vez actualizada la lista. Alternativamente, **después de crear la base**, instala el addon y sus dependencias desde CLI:

```bash
bash scripts/lab.sh install-addon
# Para actualizar el addon tras modificar código:
bash scripts/lab.sh upgrade-addon
```

El script detiene Odoo, ejecuta `-i`/`-u` con la base conocida y luego restaura el servicio. No sobrescribe ni elimina bases de datos. Consultar `bash scripts/lab.sh logs` si la instalación falla.

**Importante:** una instalación del addon no instala ni configura el POS automáticamente. Activa `point_of_sale` y crea una tienda/caja de prueba con los procedimientos normales de Odoo. Para pruebas POS→factura debe seleccionarse explícitamente la opción de crear factura, que puede exigir configurar cliente e impuestos.

## Prueba A — factura manual → CPE local

1. Configura una **empresa de demostración** con RUC de 11 dígitos aceptado por la validación de Odoo, PEN y régimen de IGV 18 %. Utiliza datos sintéticos exclusivamente. Si Odoo rechaza el identificador, ajusta los datos ficticios de forma válida; no utilices el RUC de una empresa ajena.
2. Crea un cliente demo con RUC de 11 dígitos para **Factura (01)** o DNI sintético de 8 dígitos para **Boleta (03)**. Establece su VAT/Tax ID y denominación.
3. Crea un producto ficticio con un solo impuesto porcentual de **18 % no incluido** en el precio, precio unitario neto **S/ 50.00**.
4. Crea una factura de cliente en Contabilidad → Clientes → Facturas, con **2 unidades**, importe total **S/ 118.00**. Valida/contabiliza la factura; el asiento debe estar en estado `posted`.
5. En la factura aparece `Laboratorio CPE — SIMULACIÓN LOCAL, NO SUNAT`. Introduce **F001**, correlativo **1**, tipo **Factura (01)** y escenario **Aceptado**.
6. Pulsa **Simular CPE (NO SUNAT)**. Verás **Aceptado (SIMULADO)** y un registro en **Contabilidad → CPE SIMULADO - NO SUNAT**.
7. Repite la acción o abre la misma factura nuevamente: **no se crea otro documento**. Otro comprobante con misma identidad RUC/tipo/serie/correlativo será rechazado por la restricción única.

Para probar la boleta crea otra factura contable independiente y usa tipo `03`, serie `B001`, correlativo `1` con DNI de ocho dígitos.

## Prueba B — rechazo y timeout sin duplicados

- **Rechazo:** en otra factura con nueva serie/correlativo elige `Rechazado`, envía al simulador y observa `Rechazado (SIMULADO)`; no hace un segundo envío.
- **Timeout:** en otra factura elige `Comunicación incierta`. El resultado queda `Incierto (SIMULADO)`. Pulsa **Consultar simulador**: seguirá incierto. Cambia el escenario a `Aceptado` y pulsa **Consultar simulador**: sólo cambia el estado existente, **no reenvía**.
- **Prevalidaciones:** crea una factura en USD, con descuento, IGV distinto al 18 %, serie inválida o cliente sin VAT; el addon debe rechazarla antes de crear un registro de envío.

## Prueba C — POS → factura → CPE local

1. Configura Punto de Venta, producto/stock y medio de pago, inicia sesión, registra venta.
2. Activa **Factura** para esa venta POS, con cliente y datos de identificación; confirma y comprueba que Odoo generó un `account.move` contabilizado.
3. Abre el `account.move` generado y ejecuta el mismo flujo de simulación A.
4. Revisa stock, factura, caja y devoluciones según la documentación oficial Odoo; **las devoluciones/ notas de crédito CPE no están implementadas en el addon**.

**No se instala código JavaScript custom de POS**: se usa el flujo estándar POS→invoice de Odoo. Si esa ruta no crea `account.move` contabilizado, es una brecha real a registrar antes de vender.

## Comandos de operación

```bash
bash scripts/lab.sh status
bash scripts/lab.sh logs
bash scripts/lab.sh version
bash scripts/lab.sh down   # Detiene servicios; mantiene datos
```

Nunca utilizar `docker compose down -v` para detener el laboratorio, pues borra volúmenes PostgreSQL/filestore.

## Confiabilidad y límites

- **Única simulación:** el registro de Odoo se limita por `move_id` y por identidad de documento con restricciones SQL; el botón bloquea concurrentemente la factura mediante `FOR UPDATE`.
- **Orígenes:** un `account.move` contabilizado es obligatorio; nunca un evento POS incompleto.
- **No reintentos automáticos:** no hay HTTP de salida; consultar únicamente el estado simulado cuando sea incierto.
- **Protección básica:** permisos de contabilidad y regla multiempresa; el JSON de respuesta es sintético, el payload con datos de cliente sólo es visible al grupo gerente contable.
- **Sin fraude de estado:** todas las etiquetas y respuestas indican **SIMULADO**; no se crea CDR/XML/PDF ni se declara validación tributaria.
- **Aislamiento técnico:** servicio Odoo accesible sólo por `127.0.0.1:8079`; DB no expuesto; secretos locales únicos.
- **Sin cierre comercial:** el addon es una ayuda de integración para MK1/MK2; no es una facturación electrónica autorizada ni una solución de uso real.

## Verificaciones

```bash
python3 scripts/verify_static.py
bash scripts/lab.sh validate-contract
docker compose --env-file .env.local -f compose.yaml config --quiet
```

Con Docker, verificar la instalación del addon mediante `install-addon`; en un entorno con GitHub Actions disponible, `.github/workflows/retail-cpe-lab.yml` comprueba montaje y módulos contra base desechable. **La existencia de código/CI no sustituye una ejecución verde del commit exacto.**

Siguiente hito para emitir legalmente: adquirir/verificar `l10n_pe_edi_base`, `l10n_pe_edi_odoofact` y `l10n_pe_edi_odoofact_pos` para Odoo Community 19 y contratar proveedor PSE/OSE; sólo entonces certificar POS→CPE→CDR real en sandbox/ambiente autorizado. No suplantar esos módulos con esta simulación.

Referencias: https://www.operu.pe/knowledge/article/141 · https://www.operu.pe/knowledge/article/70 · https://www.nubefact.com/integracion · https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html
