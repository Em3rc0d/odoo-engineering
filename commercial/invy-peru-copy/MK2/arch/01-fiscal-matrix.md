# Arquitectura — DEC-FISCAL-02 · comparación con evidencia

**Estado: SIN DECISIÓN FINAL.** El ADR antiguo que proponía OPeru+Nubefact y la preferencia posterior por Greenter/directo se mantienen como alternativas. No adoptar por entusiasmo OSS ni solo por precio.

| Ruta | Evidencia observada | Compatibilidad/limitación | Estado |
|---|---|---|---|
| Odoo Community 19: l10n_pe + l10n_pe_pos | Manifiestos LGPL-3 en el repositorio público de Odoo 19; nuestro CI los instaló | Son base peruana contable/POS, no emisión CPE real | BASE DEMO |
| Odoo l10n_pe_edi documentado | La documentación de Odoo 19 enumera EDI; la ruta correspondiente en el repositorio público Community devolvió 404 | No inferir que una edición o distribución distinta carezca de él | INVESTIGAR DISTRIBUCIÓN |
| OPeru E-Documents + OdooFact + addon POS y Nubefact | Catálogo Odoo Apps 19: base y OdooFact LGPL-3, dependencias adicionales; OPeru anuncia ruta POS y proveedor | No están en nuestra imagen; proveedor API, tarifas, catálogos, permisos y POS no probados | PRIMER CANDIDATO A BENCH AUTORIZADO |
| Greenter | MIT, PHP >=7.4, genera/firma XML y procesa CDR según README | Necesita puente PHP y custodia de certificados + cola propia | BENCHMARK |
| Kembec SDK | MIT, motor Rust y bindings Python; README release candidate rc.6 | Compatibilidad wheel/versión y pruebas de firma por confirmar | BENCHMARK |
| CPEForge | MIT, Rust con Decimal y estados tipados; CI/benchmarks según autor | Servicio o integración FFI y dependencia operativa | BENCHMARK |
| davcito/sunat-cpe | MIT, Node.js con identidad, CDR y conciliación según autor | Declaración de uso en producción no verificada externamente | PATRÓN DE ERRORES |
| ContaPerú | MIT, contabilidad/SIRE/PLE y adaptadores | **No es un emisor de comprobantes** | SEPARAR DEL EDI |
| Adaptador Nubefact experimental nuestro | 10 pruebas simuladas y hash contra cambios posteriores, sin envío habilitado | No tiene outbox durable, XML firmado, CDR ni integración fiscal real | TEST ONLY |

## Riesgo de licencias de componentes transitivos
Los módulos OPeru observados se anuncian LGPL-3. Su sección de dependencias hace referencia a catálogos SUNAT, pero NO se verificó la identidad exacta del addon requerido. Un addon distinto de **Ganemo** denominado l10n_pe_catalog aparece con licencia OPL-1 y precio USD 40.24, sin evidencia de que sea el requerido por OPeru. Nunca asumir que todo el árbol es OSS o gratuito sin revisar manifests reales.

## Regla condicional de selección
OPeru + Nubefact es el primer camino a **probar**, por integración potencial, no el ganador. Greenter/Kembec/CPEForge solo pueden compararse con mismos XML ficticios, firmas, estados, costos de hosting, rotación y seguridad. Si ninguna ruta demuestra costo/licencia/cumplimiento aceptable, PIVOT a utilizar emisor autorizado externo ya existente o KILL de la promesa CPE; nunca representar una simulación como emisión.

No instalar módulos de terceros sin derechos confirmados; no usar certificados o claves SOL reales en GitHub Actions.
