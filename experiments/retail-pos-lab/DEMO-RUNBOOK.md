# DEMO 001 — punto de venta local (NO SUNAT)

**Propósito:** recorrer en una computadora propia una tienda ficticia: abrir caja, vender, registrar efectivo/Yape manual, solicitar factura desde POS, consultar el simulador local y cerrar caja. **No es un producto tributario ni un deploy SaaS.**

## Preparación en Windows 11

Instala Docker Desktop con backend WSL 2; utiliza terminal Ubuntu WSL 2 (no PowerShell sin Bash). Asegura memoria y espacio suficientes para Odoo y PostgreSQL.

```bash
git clone https://github.com/Em3rc0d/odoo-engineering.git
cd odoo-engineering/experiments/retail-pos-lab
bash scripts/lab.sh demo-setup
```

El comando genera credenciales de DB y maestra **en tu máquina**, inicia PostgreSQL y Odoo 19 Community, instala POS + inventario + l10n_pe + l10n_pe_pos + CPE simulado, inicializa el plan contable peruano, agrega tres productos ficticios, stock inicial y caja **Caja DEMO - Retail Peru**. No se conecta con SUNAT ni Nubefact. Tampoco instala ni necesita Greenter.

Abre **http://127.0.0.1:8079**. La nueva base `retail_peru_lab` tiene el administrador por defecto que Odoo crea al inicializarla por CLI (normalmente `admin/admin` en la base desechable). **Cambia la contraseña inmediatamente desde Preferencias antes de operar la demo**, aunque se publique solo en localhost; no reutilices credenciales. No se imprimen secretos en CI. Si ya habías creado la base, se conservan sus usuarios y contraseñas.

Validación repetible:

```bash
bash scripts/lab.sh version
bash scripts/lab.sh check-demo
bash scripts/lab.sh checkout-smoke  # prueba transaccional con rollback, no afecta tus ventas
bash scripts/lab.sh status
```

## Prueba manual de seis pasos

1. En **Punto de Venta → Tablero**, encuentra **Caja DEMO - Retail Peru** y abre el registro. Declara efectivo inicial (por ejemplo S/ 100).
2. Busca **Cuaderno A5 (DEMO)** o **Mochila escolar (DEMO)**, agrega una o dos unidades. Los precios son de demostración y el impuesto asignado es IGV 18 %.
3. Pulsa **Pago**. Registra **Efectivo**, o **Yape / Plin - REGISTRO MANUAL**. El segundo medio **no confirma transferencias reales**; debe verificarse aparte. Finaliza la operación solo una vez.
4. Para probar la simulación tributaria, realiza **otra venta POS** y selecciona cliente antes de marcar **Factura**. La localización peruana puede solicitar un RUC válido. La pantalla POS emitirá una factura contable de Odoo, no un CPE SUNAT; la simulación solo acepta una factura publicada `account.move` y valores de impuesto restringidos.
5. En **Facturación/Contabilidad → Facturas de cliente**, abre el `account.move` generado y, si cumple las validaciones, establece una **serie ficticia F001, correlativo nuevo**, escenario Aceptado/Rechazado/Timeout y pulsa **Simular CPE (NO SUNAT)**. Comprueba que el estado diga **SIMULADO** y que la acción duplicada quede bloqueada. Si Odoo exige campos fiscales adicionales, configúralos con datos de pruebas y anota el error; **no fuerces ni suplantes una emisión real**.
6. Vuelve a **Punto de Venta** y cierra la sesión. Cuenta el efectivo, verifica movimientos e identifica las diferencias. El cierre es de Odoo; no certifica CPE alguno.

## Productos incluidos

| SKU | Nombre | Precio neto de demostración | Stock inicial deseado |
|---|---|---:|---:|
| DEMO-CUADERNO | Cuaderno A5 (DEMO) | S/ 10 | 30 |
| DEMO-LAPICERO | Lapicero azul (DEMO) | S/ 2,50 | 50 |
| DEMO-MOCHILA | Mochila escolar (DEMO) | S/ 50 | 12 |

**La carga es idempotente:** `seed-demo` no restablece precios ni existencias tras vender. Las cifras pueden variar al repetir la prueba.

## Comandos útiles

```bash
bash scripts/lab.sh logs
bash scripts/lab.sh seed-demo        # no repone stock existente
bash scripts/lab.sh check-demo       # solo verifica configuración
bash scripts/lab.sh down             # conserva datos
```

**No uses** `docker compose down -v` a menos que quieras borrar por completo las bases de datos y el filestore de la demostración.

## Límite confirmado del hito

- **CI:** instalación real de módulos y ejecución ORM de carga/verificación, si el workflow del commit exacto termina en verde.
- **Manual:** recorrido visual y acciones de usuario aún requieren tu prueba en Windows con Docker.
- **No implementado:** generación UBL XML real, firma, envío SUNAT beta/producción, CDR verificable, colas fiscales de producción, notas de crédito electrónicas y servicios SaaS multi-tenant.
- **No se modificó** el código importado de Rally.

No uses datos de contribuyentes reales, ni certificados, ni claves SOL.

## Prueba automática de ciclo de caja (ORM, no navegador)

El comando `checkout-smoke` abre una sesión ficticia en el ORM real de Odoo, cobra una unidad en efectivo, comprueba el pago, cierra la caja y verifica la reducción de stock. **Todo se revierte** mediante `rollback` para no alterar tus existencias. Exige que no haya una sesión abierta en la caja demo. Este test no sustituye las pruebas visuales en el navegador ni toca SUNAT.

## Prueba de factura CONTABLE publicada contra simulador local

En el laboratorio desechable (sin fuentes externas ni emisión real), el comando nuevo ejecuta el flujo de una factura contable sintética, su envío al **simulador local**, rechazo del segundo envío, prueba del estado incierto y consulta posterior de estado. Requiere Odoo Community 19 configurado y usa un rollback único al concluir:

```bash
bash scripts/lab.sh demo-setup
bash scripts/lab.sh invoice-sim-smoke
```

La prueba utiliza identificadores **ficticios**, nunca se comunica con SUNAT, no produce firma XML ni CDR y no deja registros contables de los casos de prueba. Un PASS de esta ruta ORM no representa un recorrido de cajero en navegador **POS→account.move**, que sigue pendiente.

## Smoke POS→factura contable→simulador LOCAL (ORM, NO INTERFAZ)

Con datos enteramente ficticios y rollback, el nuevo comando abre caja, registra una venta POS pagada en efectivo, utiliza `action_pos_order_invoice()` de Odoo 19 con la generación/envío automático PDF deshabilitados, comprueba que una factura contable publicada se vincula a la orden, y verifica el simulador local con bloqueo de duplicados; finalmente cierra la sesión y revierte todo.

```bash
bash scripts/lab.sh demo-setup
bash scripts/lab.sh pos-invoice-sim-smoke
```

**No es E2E del navegador**, no usa Web POS/OWL y no genera ni transmite CPE XML/CDR. Los identificadores de emisor/comprador son ficticios, transitorios y sin credenciales. Nunca probar en una base de un contribuyente real.

## Error CRLF al ejecutar en Ubuntu WSL

Si `bash scripts/lab.sh demo-setup` produce `: invalid option name... set: pipefail` o aparece `^M` en `cat -v scripts/lab.sh | head`, probablemente Git para Windows hizo checkout con finales de línea CRLF. Desde `experiments/retail-pos-lab`:

```bash
sed -i 's/\r$//' scripts/lab.sh
bash -n scripts/lab.sh
bash scripts/lab.sh demo-setup
```

Este repositorio fija ahora `*.sh text eol=lf` en su `.gitattributes` de raíz para nuevas extracciones. **La regla no reescribe necesariamente archivos ya existentes en tu árbol de trabajo**, por lo que la corrección `sed` local sigue siendo necesaria. Si otro `.sh` sufriera el mismo problema, conviértelo individualmente. No modifiques ni compartas `.env.local`, `.local/odoo.conf` ni datos de usuarios para resolver un error de fin de línea.

**Rutas:** `scripts/lab.sh` es relativo a `experiments/retail-pos-lab`, no a la raíz del repositorio. Usa Bash de WSL, no el shell de PowerShell.
