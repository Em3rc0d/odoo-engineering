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
  master-password)
    [[ -f .local/odoo.conf ]] || { echo "Initialize first" >&2; exit 1; }
    echo "Sensitive: local output only; do not paste into chat, logs or issues" >&2
    sed -n 's/^admin_passwd = //p' .local/odoo.conf
    ;;
  *)
    echo "Usage: bash scripts/lab.sh {init|up|down|status|logs|version|master-password}"
    exit 2
    ;;
esac
