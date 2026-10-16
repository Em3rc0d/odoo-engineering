# Validation — 2026-10-16

Scope: `integrations/sunat/nubefact_gateway/` only. Executed locally in isolated Python environment, WITHOUT Odoo, Docker, provider credentials or network calls.

Commands:
```sh
python -m compileall -q integrations/sunat/nubefact_gateway integrations/sunat/tests
python -m unittest discover -s integrations/sunat/tests -v
```

Observed: **9 test cases passed, 0 failed**, and bytecode compilation succeeded. Coverage: invoice/boleta basic tax payload, two-decimal rounding rejection, document identity, opt-in fail-closed default, route/token guard, request format with HTTP simulator, no blind retry on uncertain network outcome, mismatch and conservative status projection.

Not proved: complete Nubefact schema for a tenant, Odoo `account.move` mapping, SUNAT transmission, XML signatures, certificates, real CDR interpretation, persistence/outbox, approval workflow, third-party module operation, accounting legality and SLA/capacity. The integration is **NOT PRODUCTION-READY**.

Local source test run was performed before GitHub commit. The repository update itself was not used to trigger production actions or transmit any invoices.
