#!/usr/bin/env bash
# Disposable local Odoo Community lab. NEVER use real customer data.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TASK="${1:-help}"

initialize() {
  command -v python3 >/dev/null || { echo "Python 3 required" >&2; exit 1; }
  mkdir -p .local
  chmod 700 .local
  python3 - <<'PY'
import os
from pathlib import Path
from secrets import token_urlsafe

env = Path(".env.local")
if not env.exists():
    fd = os.open(str(env), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write("# Local disposable lab; do not commit or share.\n")
        f.write("RETAIL_DB_PASSWORD=" + token_urlsafe(36) + "\n")
config = Path(".local/odoo.conf")
if not config.exists():
    fd = os.open(str(config), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "w") as f:
        f.write("[options]\n")
        f.write("admin_passwd = " + token_urlsafe(48) + "\n")
        f.write("dbfilter = ^retail_peru_lab$\n")
        f.write("list_db = True\n")
        f.write("proxy_mode = False\n")
        f.write("addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons\n")
# Migrate pre-existing lab configs without touching the master password.
existing = config.read_text()
if "addons_path =" not in existing:
    with config.open("a") as f:
        f.write("addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons\n")
os.chmod(env, 0o600)
PY
}

compose() {
  docker compose --env-file .env.local -f compose.yaml "$@"
}

case "$TASK" in
  init)
    initialize
    echo "Lab secrets generated locally. Never commit .env.local or .local/."
    ;;
  up)
    initialize
    command -v docker >/dev/null || { echo "Docker Compose required" >&2; exit 1; }
    compose up -d --wait
    echo "Open http://127.0.0.1:8079 and create database: retail_peru_lab."
    echo "Obtain its master password locally: bash scripts/lab.sh master-password"
    ;;
  down)
    if [[ -f .env.local ]]; then compose stop; else echo "Lab not initialized"; fi
    ;;
  status)
    if [[ -f .env.local ]]; then compose ps; else echo "Lab not initialized"; fi
    ;;
  logs)
    if [[ -f .env.local ]]; then compose logs --tail=80 odoo; else echo "Lab not initialized"; fi
    ;;
  version)
    command -v curl >/dev/null || { echo "curl required" >&2; exit 1; }
    curl --fail-with-body --silent --show-error http://127.0.0.1:8079/web/version
    ;;
  demo-setup)
    initialize
    command -v docker >/dev/null || { echo "Docker Compose required" >&2; exit 1; }
    compose up -d --wait postgres
    # -i is safe for the existing database: installs missing modules; never deletes data.
    compose stop odoo
    if ! compose run --rm --no-deps odoo --no-http --stop-after-init \
        -d retail_peru_lab -i base,account,stock,l10n_pe,point_of_sale,l10n_pe_pos,oe_pe_cpe_lab; then
      echo "Odoo module installation FAILED; review logs." >&2
      exit 1
    fi
    compose up -d --wait odoo
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/seed_demo.py
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/check_demo.py
    echo "DEMO ready: http://127.0.0.1:8079  (real SUNAT emission DISABLED)"
    ;;
  seed-demo)
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/seed_demo.py
    ;;
  check-demo)
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/check_demo.py
    ;;
  invoice-sim-smoke)
    # Test a posted accounting document against the LOCAL simulator only.
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/invoice_simulation_smoke.py
    ;;
  probe-edi)
    # Read-only inventory of modules actually present in THIS Odoo Community image.
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/probe_edi_modules.py
    ;;
  checkout-smoke)
    compose exec -T odoo sh -c 'exec odoo shell -d retail_peru_lab --no-http --db_host="$HOST" --db_port="$PORT" --db_user="$USER" --db_password="$PASSWORD"' < scripts/checkout_smoke.py
    ;;
  install-addon|upgrade-addon)
    initialize
    command -v docker >/dev/null || { echo "Docker Compose required" >&2; exit 1; }
    # Database must have been created through the browser first.
    # Stop application writes while applying Odoo schema/module updates.
    compose stop odoo
    mode="-i"
    [[ "$TASK" == "upgrade-addon" ]] && mode="-u"
    if ! compose run --rm --no-deps odoo --no-http --stop-after-init \
        -d retail_peru_lab "$mode" oe_pe_cpe_lab; then
      echo "Addon install/upgrade FAILED. Review Odoo logs; not certified." >&2
      compose up -d odoo
      exit 1
    fi
    compose up -d --wait odoo
    echo "Addon installation/upgrade command completed; inspect Apps and invoice form."
    ;;
  validate-contract)
    (cd ../../integrations/sunat && python3 -m unittest discover -s tests -v)
    ;;
  master-password)
    [[ -f .local/odoo.conf ]] || { echo "Initialize first" >&2; exit 1; }
    echo "Sensitive: local output only; do not paste into chat, logs or issues" >&2
    sed -n 's/^admin_passwd = //p' .local/odoo.conf
    ;;
  *)
    echo "Usage: bash scripts/lab.sh {init|up|down|status|logs|version|demo-setup|seed-demo|check-demo|checkout-smoke|invoice-sim-smoke|probe-edi|install-addon|upgrade-addon|validate-contract|master-password}"
    exit 2
    ;;
esac
