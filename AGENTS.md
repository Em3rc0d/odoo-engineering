# Odoo Engineering instructions

**Mission:** Maintain Odoo-only feature addons with linked baselines. Principle: COPY when licensed, ADAPT for platform, IMPROVE demonstrably, VALIDATE when separately authorized.

- Read `research/MK3/README.md` before claiming full coverage.
- `addons/` includes candidate source, not production-ready code. Seven learning domains are only inventoried in `learning/curricula.json`.
- Preserve Odoo 19 origin, each `UPSTREAM.md`, and notices. Do not transplant files with unclear license.
- No conflict-inducing duplicate `_name` models. No replacing `web/static/src/main.js` without compatibility evidence.
- Never claim a test executed without logs. The MK3 delivery explicitly prohibits testing.
- Avoid edits to `personal_knowledge` and source GitHub repositories.

## Pinned Rally upstream boundary

- `external/rally` is a read-only pinned Git submodule, **not** a folder of Odoo addons; never commit modifications inside it or silently advance its gitlink.
- Read `research/integrations/rally/README.md` and `feature-decisions.md` before cross-repo work. Keep Rally's operational-assurance mission distinct from Odoo ERP source-of-truth writes.
- Do not copy or relicense Rally's source (no repository-wide license identified) without an independent legal/IP authorization; customer/employer ownership constraints remain open.
- Any future submodule SHA bump requires a source manifest refresh, explicit diff review, tests and an updated ownership decision. No upstream write access is assumed.
- Import no CRM/stock/accounting writes via Rally status mirror. Use explicit Odoo integration permissions and preserve no-live-provider-test caveats.
