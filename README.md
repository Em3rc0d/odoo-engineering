# Odoo Engineering — Evidence-Driven Knowledge Base

> **Estado (13-10-2026):** fundación documental reproducible. **NO es una colección de addons certificados ni un framework productivo listo para instalar.**

Repositorio **exclusivo de Odoo**: aprendizaje, arquitectura, ORM, seguridad, OWL, pruebas, revisión de addons y análisis de fallos reales, con procedencia verificable. Proyecto separado de `personal_knowledge`, sin acoplamiento ni sincronización entre ambos.

## Por qué existe

Unificar conocimiento técnico útil de **cinco repositorios públicos Odoo** de JoseCarlosLuque bajo una estructura limpia, sin clonar indiscriminadamente sus fuentes ni heredar defectos. La prioridad es el **aprendizaje y la toma de decisiones**; no se fusionan módulos ajenos ni se afirma que funcionan en Odoo 19 sin ejecutarlos.

**Fuentes auditadas:** `odoo_practices` (7 módulos, 245 ejercicios planificados), `odoo_opencode` (2 addons), `odoo_19_addons` (4 addons), `proyecto_OWL` (dashboard de laboratorio) y `Pruebas_Odoo` (biblioteca de laboratorio). Las cifras corresponden al inventario estático inspeccionado; los ejercicios pendientes no equivalen a ejercicios resueltos ni pruebas aprobadas.

## Empieza aquí

| Necesidad | Documento |
|---|---|
| Alcance, estado y viabilidad | [MK0](research/MK0/README.md) |
| Contratos del conocimiento | [MK1](research/MK1/README.md) |
| Fuentes, SHA y licencias | [Catálogo JSON](research/sources/catalog.json), [licencias](research/sources/LICENSE_REVIEW.md) |
| Problemas encontrados | [Índice de hallazgos](findings/README.md) |
| Patrones reutilizables | [Índice de patrones](patterns/README.md) |
| Reglas para agentes de IA | [AGENTS.md](AGENTS.md) |
| Calificación y gates | [Quality gates](docs/quality-gates.md) |
| Documentación oficial Odoo 19 | [Referencias](docs/official-references.md) |
| Validar estructura sin instalar Odoo | `python scripts/validate_repo.py` |

## Reglas innegociables

1. **Odoo-only.** No se almacenan patrones genéricos de React, Spring, Android, etc.
2. **No trasplante de código sin permiso/licencia.** Descripciones originales, enlaces a las fuentes y ejemplos propios cuando corresponda.
3. **Evidencia ≠ ejecución.** `STATIC_OBSERVATION`, `OFFICIAL_REFERENCE`, `HYPOTHESIS` y `RUNTIME_VALIDATED` son estados distintos.
4. **Referencia Odoo 19, sin compatibilidad asumida.** Proyectos antiguos o laboratorios externos no son equivalentes a módulos instalables Odoo 19.
5. **Sin dependencias ni automatizaciones caras.** Validador estándar de Python; sin GitHub Actions ni Docker obligatorio para el repositorio documental.
6. **Gates antes de construir.** Esta fundación no autoriza implementar un addon, agente Odoo o SaaS.

## Madurez actual

- **MK0:** inventario y tesis de consolidación documentados; permiso de redistribución y ejecución real siguen **pendientes**.
- **MK1:** contratos, categorías, índices y primer lote de patrones/hallazgos estructurados.
- **Validación local:** comprobador documental incluido; se deben adjuntar logs/resultados cuando se ejecute.
- **Producción:** **NOT AUTHORIZED** hasta contar con evidencia funcional y pruebas de seguridad.

## Derechos y atribución

Este repositorio documenta observaciones **sobre** trabajos ajenos. No contiene copias de sus addons. La visibilidad pública de una fuente **no** equivale a licencia de redistribución. Antes de importar código, revisar la licencia aplicable por repositorio y archivo, y solicitar autorización cuando corresponda. Véase [LICENSE_REVIEW](research/sources/LICENSE_REVIEW.md).

## Cómo contribuir

Seguir [CONTRIBUTING.md](CONTRIBUTING.md) y [AGENTS.md](AGENTS.md). Cada hallazgo debe referirse a archivo y versión concretos; cada patrón debe indicar cuándo **no** usarlo y cómo validarlo.
