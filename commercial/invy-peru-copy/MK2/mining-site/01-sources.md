# Mining-site · fuentes observadas (21-10-2026)

## Jerarquía de evidencia
OFFICIAL: SUNAT y documentos normativos oficiales. VENDOR: documentación pública y precio de proveedores; no implica verificación independiente de producto. OBSERVED: archivos obtenidos de GitHub o log de CI propio. UPSTREAM_CLAIM: afirmación del README autor, sin ejecución propia. INFERRED: nuestro juicio de encaje. UNKNOWN/BLOCKED se preservan como tales.

| Fuente | Hecho sustentable | Limitación |
|---|---|---|
| https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html | VENDOR lista l10n_pe, l10n_pe_edi y l10n_pe_pos | No prueba disponibilidad de EDI en nuestro Community |
| https://github.com/odoo/odoo/tree/19.0 | OBSERVED l10n_pe y l10n_pe_pos LGPL-3, SHA 4d4870b6e39513a8ed84b2d059a80cd4a2570c69; l10n_pe_edi manifest da 404 en ese repositorio | Otra edición/distribución podría incluir EDI |
| https://apps.odoo.com/apps/modules/19.0/l10n_pe_edi_base | VENDOR OPeru 19, LGPL-3, addons dependientes | Árbol de distribución no instalado ni licencias transitivas verificadas |
| https://apps.odoo.com/apps/modules/19.0/l10n_pe_edi_odoofact | VENDOR OPeru 19, LGPL-3 y módulo externo | Costos API/soporte desconocidos |
| https://www.operu.pe/knowledge/article/141 | VENDOR dependencia POS de OdooFact | No ensayo real Community 19 en nuestra imagen |
| https://www.operu.pe/facturacion-electronica | VENDOR flujo Odoo→Nubefact→SUNAT | No prueba que todas las extensiones sean gratis |
| https://apps.odoo.com/apps/modules/19.0/l10n_pe_catalog | VENDOR addon separado de Ganemo, OPL-1, USD 40.24 | NO hay prueba de que sea la dependencia exacta de OPeru |
| https://www.nubefact.com/precios | VENDOR S/70/mes ONLINE, 500 docs | No es cotización contractual de API OPeru |
| https://cpe.sunat.gob.pe/sistema_emision/see_contribuyente | OFFICIAL modalidad SEE del contribuyente y condiciones | Elegibilidad específica pendiente de experto/emisor |
| https://github.com/thegreenter/greenter | OBSERVED composer MIT/PHP, SHA 23db8f4d538886f9af2ff25920a12bffb8415c2b | No hemos corrido su firma o CDR |
| https://github.com/Kembec/facturacion-electronica-sunat-sdk | UPSTREAM_CLAIM Rust, Python, JS, PHP, Swift; rc.6, SHA 98ba4b042a7b6eca2e294d053fbf99458e9f8c37 | No SDK instalado o probado |
| https://github.com/alvarez25leo/cpeforge | UPSTREAM_CLAIM Rust, Decimal, CI y benchmark; SHA 8bfd3a103eb308a5c8c42aca13d30725570ceccf | Benchmarks SUNAT beta de autor, no nuestros |
| https://github.com/davcito/sunat-cpe | UPSTREAM_CLAIM Node.js, CDR, conciliación, uso productivo; SHA 706262d0f4d1ec47257c6e4959b0183ef7e98035 | Uso productivo declarado no auditado |
| https://github.com/contaperu/contaperu | UPSTREAM_CLAIM motor contable y SIRE, SHA 080b5d8342fb0e85b38d095123f2e1d8622a1229 | NO emite CPE |
| https://www.invyperu.com/precios | VENDOR S/169 Pyme 500 CPE y S/229 Negocio 1500 | Funcionalidades y precio pueden cambiar |
| https://www.alegra.com/peru/punto-venta/precios/ | VENDOR S/81 Emprendedor/250; S/93 Pyme/1000, IGV incluido | Comparar condiciones comerciales exactas |
| https://www.bsale.com.pe/sheet/precios | VENDOR S/189 Básico, S/233 Estándar, incl IGV | Planes no equivalentes por defecto |
| https://www.vendty.com/pe | VENDOR POS y precios anunciados en USD | Condiciones SUNAT aplicables Perú no verificadas |
| https://github.com/Em3rc0d/odoo-engineering/actions/runs/39642972244 | OBSERVED workflows static y Odoo lab verdes, EDI_PROBE_OK | Solo módulos en imagen, venta ORM y simulador; no fiscal |
| https://github.com/Em3rc0d/odoo-engineering/actions/runs/39634967651 | OBSERVED 10 tests de contrato Nubefact falsificado | No red/proveedor real |

Ninguna referencia justifica afirmar legalidad, SLA, rentabilidad de competidores o presencia de clientes. Pinned SHAs corresponden a snapshot de GitHub de la fecha, no al código vendorizado. Licencias de todos los componentes transitivos deben verificarse antes de distribución comercial.
