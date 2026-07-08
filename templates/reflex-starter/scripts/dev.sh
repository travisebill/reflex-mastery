#!/bin/bash
# dev.sh — 啟動 dev server

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# 載入 .env
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# 啟用 venv
if [ -d .venv ]; then
    source .venv/bin/activate
fi

# Init DB
python3 -c "from db.connection import init_db; init_db()"

# 啟動 Reflex
reflex run --env dev
