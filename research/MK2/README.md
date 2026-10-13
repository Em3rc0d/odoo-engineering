# MK2 — Baselines convertidos en módulos instalables (piloto)

**Decisión:** reorientar `odoo-engineering` a implementación Odoo 19 basada en upstreams externos: **copiar (solo con licencia) → adaptar → mejorar → validar**. La documentación `MK0/MK1` pasa a soporte de ingeniería, no al producto final.

## Alcance inicial

**Dos vertical slices originales o legalmente adaptados:**

1. `oe_sale_task_bridge`: actualización del baseline LGPL-3 `sale_task_creator` de `odoo_opencode`.
2. `oe_library`: rediseño de biblioteca a partir de los requerimientos observados y el patrón educativo LGPL-3 de `odoo_practices`; **no** se copiará el código de `Pruebas_Odoo` sin concesión de derechos.

**Pendiente:** wizard de superficies, crédito/amortización, integración OWL real, responsive web client, pruebas de seguridad/roles, compatibilidad real Odoo 19, ediciones Enterprise y versiones alternativas. **No mergear automáticamente** modelos distintos de addons del upstream que definen el mismo `_name`.

## Matriz de mejoras

| Baseline | Mejora implementada | Prueba incluida | Estado |
|---|---|---|---|
| `odoo_opencode/sale_task_creator` | Conteo `_read_group` tuplas en Odoo19, namespaced fields y wizard de proyecto | 5 `TransactionCase` | Estático PASS; Odoo no probado |
| `odoo_practices/cd_library_practices` + requisitos `Pruebas_Odoo` | Ejemplar físico en vez de simple estado del título; préstamo único via índice PostgreSQL; overdue no almacenado | 6 `TransactionCase` | Estático PASS; Odoo no probado |

## Acceptance gates

- **A0 provenance:** upstream, commit, licencia por addon, autoría, modificaciones; estado: **PASS documental condicionado por copyright de terceros**.
- **A1 estructura:** Python AST, XML, manifiestos, ACL; **PASS local** (ver `validation/2026-10-13-static.md`).
- **A2 instalación:** instalar en Odoo 19 limpio con dependencias, sin datos demo por defecto; **PENDIENTE**.
- **A3 test:** 11 tests TransactionCase ejecutados exitosamente, logs reales; **PENDIENTE**.
- **A4 seguridad:** grupos/ACL/record rules y multiempresa probados bajo usuarios reales; **PENDIENTE**.
- **A5 mejora comprobable:** comparar fallos originales con comportamientos actuales; **PENDIENTE**.

**Regla de comunicación:** `STATIC_PASS` nunca significa `ODOO_RUNTIME_PASS`. Esta fase produce implementaciones **candidatas**: no recomendar instalación productiva.

## Cómo probar en una instancia Odoo 19 existente

Desde el árbol Odoo, con PostgreSQL disponible y un `addons-path` que incluya `./addons` de este repo:

```bash
python3 scripts/validate_repo.py
python3 scripts/validate_addons.py

# En el entorno Odoo, apuntando a una base de prueba vacía:
./odoo-bin -d oe_test -i oe_library,oe_sale_task_bridge \
  --addons-path=addons,/ruta/odoo-engineering/addons \
  --test-enable --test-tags=/oe_library,/oe_sale_task_bridge \
  --stop-after-init --log-level=test
```

Usar paths reales de la instalación. El ejemplo **no** se ha ejecutado en esta sesión. Registrar versión, edición, logs, test count y resultado en `validation/` antes de pasar a A3.
