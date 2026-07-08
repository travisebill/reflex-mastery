#!/bin/bash
# self_update.sh — 更新 reflex-upgrade-monitor 的 manifest
# Usage: bash self_update.sh [--version VERSION] [--note "message"]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/../version_manifest.json"

NEW_VERSION=""
NOTE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --version) NEW_VERSION="$2"; shift 2 ;;
        --note) NOTE="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 --version VERSION [--note 'message']"
    exit 1
fi

if [ ! -f "$MANIFEST" ]; then
    echo "❌ Manifest not found: $MANIFEST"
    exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 -c "
import json
from datetime import datetime

with open('$MANIFEST', 'r') as f:
    m = json.load(f)

# Backup
backup = '$MANIFEST.bak.' + datetime.now().strftime('%Y%m%d%H%M%S')
with open(backup, 'w') as f:
    json.dump(m, f, indent=2)

# Update
old_version = m.get('tracked_version', 'unknown')
m['tracked_version'] = '$NEW_VERSION'
m['last_check'] = '$TIMESTAMP'
m['last_update_note'] = '$NOTE'
m['last_update_from'] = old_version

with open('$MANIFEST', 'w') as f:
    json.dump(m, f, indent=2)

print(f'✅ Updated: {old_version} → $NEW_VERSION')
print(f'   Backup: {backup}')
"

echo ""
echo "=== 驗證 ==="
python3 -c "
import json
with open('$MANIFEST') as f:
    m = json.load(f)
print(f'tracked_version: {m[\"tracked_version\"]}')
print(f'last_check:      {m[\"last_check\"]}')
"
