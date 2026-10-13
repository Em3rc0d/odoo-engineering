# ADR-0004 — Licencias y transformación efectiva del baseline

**13-10-2026 · ACCEPTED.** Supersede la prohibición absoluta de copiar código de ADR-0002 **solo donde exista una licencia válida por módulo**, respetando sus términos.

**Decisión:** los addons de JoseCarlosLuque que declaren LGPL-3 en el manifiesto son candidatos de modificación con atribución, historial de cambios, y cumplimiento LGPL. El repositorio original sin licencia raíz **no licencia automáticamente todos los archivos**. Otras obras sin licencia quedan restringidas a análisis de requisitos/patrones generales y reconstrucción original. Subcomponentes de otros autores exigen validación adicional.

**No importamos monorepos enteros**: seleccionamos módulos por unidad legal/técnica y evitamos duplicaciones/conflictos de `_name`. Todas las modificaciones quedan identificadas en `UPSTREAM.md`, conservan texto LGPL cuando aplica y tienen tests propios.

**Criterio final:** duplicar un proyecto sin poder instalarlo, comprobar seguridad y medir mejoras **no** cumple el método. Se exige trazabilidad baseline → cambios → prueba.

**Consecuencias:** dos addons piloto en `addons/`; resto de candidatos en `research/baselines/adoption-matrix.json`. Ninguno está certificado en Odoo runtime.
