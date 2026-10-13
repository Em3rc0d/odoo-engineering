# MK0 — Evaluación de la consolidación Odoo

**Problema:** cinco repositorios con modelos, vistas, wizards, OWL, pruebas y aprendizaje, pero calidad irregular y sin prueba transversal de funcionamiento. Importarlos como un solo proyecto elevaría el riesgo operativo, legal y de dependencias.

**Hipótesis:** es más útil un repositorio independiente de conocimiento técnico Odoo 19 con hallazgos trazables, patrones originales y gates, que un monorepo de código ajeno.

**Decisión:** **GO para documentación Odoo-only; NO-GO para trasplante masivo y producción.**

## Inventario auditado

| Origen | Archivos (lectura estática) | Aporte | Principal limitación |
|---|---:|---|---|
| odoo_practices | 212 | 7 addons educativos, 35 ejercicios por addon | ejercicios sin resolver, test isolation y pruebas reales pendientes |
| odoo_opencode | 34 | wizards, integración venta-proyectos y AGENTS | APIs ORM y consistencia de unidades por verificar |
| odoo_19_addons | 137 | addons empresariales y responsive web | campos calculados, variantes de modelos y licencias por verificar |
| proyecto_OWL | 16 | OWL y estado reactivo | datos sintéticos; no dashboard Odoo integrado |
| Pruebas_Odoo | 28 | biblioteca, avisos y cron | dependencias/chatter y demo data |

**Totales:** 427 archivos presentes en los árboles inspeccionados (no importados); 5 fuentes; 245 ejercicios planificados, no ejecutados.

## Riesgos y respuesta

- **Licencias:** enlazar/atribuir fuentes y no redistribuir implementación sin permiso explícito.
- **Deriva de Odoo 19:** comprobar con documentación y versión real.
- **Pruebas aparentes:** contar casos implementados y ejecutados, no métodos/archivos.
- **Doble fuente de verdad:** índices JSON con documentos Markdown, validados localmente.
- **Saturación del repositorio:** solo conocimiento nuevo y directamente reutilizable en Odoo.

## Pendientes antes de producción

1. Verificar disponibilidad de ambiente Odoo 19, edición y entorno efímero.
2. Validar con fixtures aisladas un primer patrón de ORM y uno de seguridad.
3. Resolver revisión de permisos/licencias si se contempla importar código.
4. Medir reutilización en un caso independiente. Si no hay caso real, dejar en archivo de referencia.
