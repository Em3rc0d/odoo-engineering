# Odoo Engineering instructions

**Mission:** Maintain Odoo-only feature addons with linked baselines. Principle: COPY when licensed, ADAPT for platform, IMPROVE demonstrably, VALIDATE when separately authorized.

- Read `research/MK3/README.md` before claiming full coverage.
- `addons/` includes candidate source, not production-ready code. Seven learning domains are only inventoried in `learning/curricula.json`.
- Preserve Odoo 19 origin, each `UPSTREAM.md`, and notices. Do not transplant files with unclear license.
- No conflict-inducing duplicate `_name` models. No replacing `web/static/src/main.js` without compatibility evidence.
- Never claim a test executed without logs. The MK3 delivery explicitly prohibits testing.
- Avoid edits to `personal_knowledge` and source GitHub repositories.
