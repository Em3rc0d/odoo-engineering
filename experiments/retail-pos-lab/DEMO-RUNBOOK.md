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
