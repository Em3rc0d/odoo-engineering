# Registro verificable de evidencias de MK1

| ID | Afirmación estricta | Evidencia | Resultado | No demuestra |
|---|---|---|---|---|
| E-001 | Odoo 19 Community/Postgres 16 y CPE addon se instalan | [Workflow 38911817634](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38911817634) · SHA `f6837b00b83afe4e8f083c16c3ae2d6957190950` | PASS | Emisión real y uso humano POS |
| E-002 | `demo-setup` crea configuración demo y módulos base | [Workflow 38936119080](https://github.com/Em3rc0d/odoo-engineering/actions/runs/38936119080) · SHA `48efd4564891887c6ce89b16f7dd65e369f286c6` | PASS | Alta SaaS multiempresa |
| E-003 | POS ORM permite apertura, venta pagada, cierre y stock | Logs E-002: `CHECKOUT_SMOKE_OK ... stock_before=30.0 stock_after=29.0 real_sunat=NO` | PASS con rollback | Prueba E2E navegador o pagos bancarios |
| E-004 | Tres SKU/IGV 18%/PEN y método manual están preparados | Logs E-002: `DEMO_SEED_OK`, `DEMO_CHECK_OK` | PASS | Cobro Yape confirmado por API |
| E-005 | 22 pantallas / 7 secuencias / 20 criterios de diseño | [DUX](../../../retail-peru/design/README.md) | DOCUMENTADO | UI implementada o pruebas de usabilidad |
| E-006 | Flujo fiscal oficial SUNAT completo | Ninguna | **NO PROBADO / BLOQUEADO** | — |
| E-007 | Restauración y aislamiento tenant de SaaS | Ninguna | **NO PROBADO / BLOQUEADO** | — |
| E-008 | Ventas comerciales, clientes de pago y margen | Ninguna | **NO PROBADO / BLOQUEADO** | — |

No marcar requisitos del [SRS](../design/SRS.md) como aprobados por la sola existencia de documentación. [Plan maestro](01-master-test-plan.md) y [matriz de trazabilidad](traceability.csv) contienen los tests propuestos.
