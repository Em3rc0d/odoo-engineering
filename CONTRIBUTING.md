# Contribución

Una contribución debe aportar un **nuevo hecho, patrón o prueba**, no reescribir la misma conclusión.

1. Confirmar que afecta a Odoo, no solo a tecnología general.
2. Adjuntar fuente y SHA fijo; para hechos de Odoo 19 preferir documentación oficial.
3. Clasificar como `STATIC_OBSERVATION`, `OFFICIAL_REFERENCE`, `INFERRED` o `RUNTIME_VALIDATED`.
4. Dar un identificador estable `FND-NNN` o `PAT-NNN`, actualizar el JSON y la ficha Markdown.
5. Declarar impacto, precondiciones, límites, corrección propuesta y procedimiento de validación.
6. Revisar derechos antes de incluir material ajeno; los enlaces no transfieren licencias.
7. Ejecutar `python scripts/validate_repo.py`. Cuando haya Odoo disponible, adjuntar pruebas reales por separado.

No aceptar `PASS` sin evidencia; no declarar corregido un defecto en repositorios externos mientras esos repositorios permanezcan intactos.
