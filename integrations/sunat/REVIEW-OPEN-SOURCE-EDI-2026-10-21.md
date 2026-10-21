# Fiscal decision comparison — 2026-10-21

**State:** RESEARCH / HOLD (not integration GO). This document augments, but does not override, [DEC-PE-EDI-001](DEC-PE-EDI-001.md) and [INVY STATUS](../../commercial/invy-peru-copy/STATUS.md). No code, assets, or credentials copied from upstream. No real SUNAT/PSE/OSE operations executed.

## Evidence and boundary

- **Official SUNAT**: [SEE Del Contribuyente](https://cpe.sunat.gob.pe/sistema_emision/see_contribuyente), [CPE communications](https://cpe.sunat.gob.pe/comunicados), [certificates](https://cpe.sunat.gob.pe/certificado-digital). Use official documents for procedural decisions and versioned end points. The 2025 CPE notice removed legacy receiver URLs; do not hardcode old domains.
- **Odoo vendor docs**: [Peru localization in Odoo 19](https://www.odoo.com/documentation/19.0/es_419/applications/finance/fiscal_localizations/peru.html): documents `l10n_pe`, `l10n_pe_edi`, `l10n_pe_pos`; **documentation is NOT proof of a module being distributable in our chosen Community deployment**.
- **Previous local lab**: [retail-pos-lab](../../experiments/retail-pos-lab/DEMO-RUNBOOK.md) and [validation](VALIDATION-2026-10-16.md). Tested POS/stock simulation, simulated HTTP CPE contract only. XML/signature/CDR and production not validated.
- **Observed external READMEs and repo metadata**: [ContaPerú](https://github.com/contaperu/contaperu), [CPEForge](https://github.com/alvarez25leo/cpeforge), [Greenter](https://github.com/thegreenter/greenter), [Kembec](https://github.com/Kembec/facturacion-electronica-sunat-sdk), [sunat-cpe](https://github.com/davcito/sunat-cpe). Third-party claimed tests/production are not our certifications.

## Decision candidates

| Source | Scope suggested by upstream | Fit in our Odoo 19 architecture | Unclosed primary risk | Current disposition |
|---|---|---|---|---|
| OPeru 19 + Nubefact | Odoo bridge, provider gateway | Lowest bespoke code if Community-compatible | Module availability/terms, provider recurring fees, actual POS→account.move workflow | **FIRST TO TEST**, not chosen |
| Odoo native `l10n_pe_edi` | Peruvian UBL EDI in vendor documentation | May simplify fiscal workflow | Community availability/license; SUNAT and operational setup | **VERIFY DIRECTLY** |
| Direct Nubefact JSON (ours) | Restricted PEN 18% send, simulated response | Has a minimal opt-in Python experiment | Not Odoo addon; no persistent outbox, SIRE, CDR or resilient state, provider contract | **FALLBACK/HOLD** |
| Greenter | PHP UBL/XML/signature/transmit/CDR | Separate PHP service or architecture change | Bridging Python↔PHP, operations/certificate custody and maintenance | **BENCHMARK** |
| Kembec SUNAT SDK | Rust core with JS/Python/PHP/Swift bindings; beta/RC | Python binding potentially useful; must verify runtime | Release maturity, packaging, methods, security, rights, SHA pin | **BENCHMARK** |
| CPEForge | Rust SDK for SUNAT XML / CDR | FFI/service bridge, high integration overhead | Reported CI ≠ verified issuer-endpoint interoperability | **BENCHMARK** |
| davcito/sunat-cpe | Node direct SUNAT with CDR/daily reconciliation; author claims production | Distinct Node service; good failure model reference | Split runtime, tax regimes, evidence of production unverified | **BENCHMARK** |
| ContaPerú | Stateless accounting engine: SIRE/PLE/adapters | Supporting mapping/validation only | **Does not emit/send CPE**; must not replace e-invoice engine | **SEPARATE NON-ISSUER TRACK** |

## Reproducible acceptance suite (never use real customer data)

| ID | Contract | Result required before candidate promotion |
|---|---|---|
| F-01 | Build/install vendor on pinned Odoo 19 Community without Enterprise or undisclosed paid library | Clear manifest + license logs |
| F-02 | Issue boleta + factura, receipt lines/multiple rates if scope supports them | Validated UBL, own reviewed fixtures |
| F-03 | Clock/time-zone `America/Lima`, F/B series and sequential numbers | Negative and boundary tests |
| F-04 | Provider timeout, 429, 500, connection reset after remote accept | **UNKNOWN**, no resend without provider identity/status lookup |
| F-05 | Double-click/same order/concurrent workers | One fiscal identity/outbox event only |
| F-06 | CDR rejected/accepted/observed/awaiting with XML storage | Real controlled evidence, no HTTP 200==CDR acceptance |
| F-07 | Credit note, debit note, cancellation, summaries/daily flows as supported | No unsupported operation mislabelled |
| F-08 | Payment settlement Yape/Plin, cash and card vs order/invoice | No duplicate booking; difference review queue |
| F-09 | Multi-RUC isolation, tenant RBAC and storage encryption | Negative cross-company tests |
| F-10 | Customer consent, backups + restore, credential rotation/redacted logs | Written operational evidence |
| F-11 | Open-source compliance incl. core/bindings/assets, supplier contract and costs | Lawyer/accountant review before launch |
| F-12 | Update of SUNAT technical specs / endpoint deprecation | Maintenance owner, alerts and fallback |
| F-13 | Test staging that **cannot** emit by default | Network blocked until explicit written approval |

## Concrete integrity issue fixed in the experimental gateway

`PreparedCPE` is a frozen dataclass, but `payload` is a nested mutable dict/list. Originally the `sha256` generated by `prepare_standard_sale()` was not rechecked in `NubefactGateway.submit()`. Changes to amount, buyer, item or tax after preparation could therefore cross the transport boundary without the pre-validation snapshot invariant.

Now the sending path re-computes its canonical JSON hash *before* preparing an HTTP request. It fails closed on any mutation, malformed/non-JSON value, or inconsistent document type. Unit tests explicitly assert **zero provider calls** after tampering. This is a **corruption/tamper detection check, not a cryptographic signature or security boundary against malicious code creating forged objects**. It does not provide outbox uniqueness, remote outcome certainty, nor live fiscal correctness.

## Cost/viability gate

For each candidate document: recurring vendor fees, activation, per-CPE costs, quotas, server/PHP/Rust maintenance, security operations, test-run resources, 24×7 incidents, and support per store/month. A zero-license library may still cost more than an approved PSE route. Record at least one written price quote *after lawful commercial gate*, and re-run F-01..F-13 against a pinned commit.

**Verdict: keep fiscal GO = NO**, preserve preferred OPeru+Nubefact as *hypothesis* and run controlled comparison before deciding. No automatic implementation in INVY or ContaMate.
