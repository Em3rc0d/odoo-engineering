# ADR-0001 — Repositorio Odoo independiente

**Fecha:** 2026-10-13 — **Status: ACCEPTED**.

**Contexto:** otros repositorios personales mantienen ámbitos independientes; se requiere centralizar conocimiento Odoo sin mezclar dominios.

**Decisión:** un repositorio autónomo `odoo-engineering` con estructura MK y sin referencias de escritura a `personal_knowledge`. Solo temas de Odoo, incluido OWL **cuando** sirve al framework Odoo.

**Consecuencias:** menos contaminación de repositorios; mantenimiento específico de versión Odoo. No convertirlo en tienda de prompts ni en plataforma de módulos sin un MK nuevo.
