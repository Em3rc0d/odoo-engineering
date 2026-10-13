# Gates de calidad

| Gate | Condición objetiva | Actual |
|---|---|---|
| G0 — Fuente | URL, ref inmutable, archivo y procedencia registrados | **PASS documental**, 5 fuentes |
| G1 — Licencia | Derecho de redistribución acreditado antes de copiar fuente | **BLOCKED**: sin evidencia de licencia raíz para 5 fuentes |
| G2 — Conocimiento | Conceptos y límites claros, validación estructural local | **PREPARED**, requiere ejecución/verificación de paquete |
| G3 — Runtime | Odoo real con versión, addons instalados, logs, test-tags y resultados | **NOT RUN** |
| G4 — Reutilización | Nuevo caso independiente resuelto gracias al patrón y medido | **NOT RUN** |
| G5 — Uso productivo | Seguridad, ACL/rules, tests multiusuario, migración y compatibilidad | **NOT AUTHORIZED** |

**Norma:** un `PASS` de G0/G2 no implica `PASS` de G3. `BLOCKED` no se convierte automáticamente en `KILL`: impide la operación concreta.

## Evidencia mínima de prueba real (G3)

- Commit Odoo, edición (Community/Enterprise) y versión exacta; addons-path y dependencias.
- Comando reproducible, base efímera o aislada, fixtures y test tags.
- Salida y resultado, incluida instalación del módulo y validación de ACL/record rules.
- Registro de falsos positivos, estado de datos demo y casos multi-registro.
- Sin credenciales, datos personales o volúmenes de producción.

## Regla de promoción

`STATIC_OBSERVATION` → `RUNTIME_VALIDATED` **solo** tras ejecutar y conservar evidencia. Un hallazgo de sintaxis evidente puede estar muy bien fundamentado estáticamente sin que se le atribuya una reproducción funcional inexistente.
