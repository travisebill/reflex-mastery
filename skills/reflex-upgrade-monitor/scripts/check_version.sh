#!/bin/bash
# check_version.sh — 查當前 + 最新 Reflex 版本
# Usage: bash check_version.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/../version_manifest.json"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 查當前版本
echo "=== 當前版本 ==="
if command -v reflex >/dev/null 2>&1; then
    CURRENT=$(reflex --version 2>/dev/null | grep -oE '0\.[0-9]+\.[0-9]+(\.post[0-9]+)?' | head -1)
    if [ -z "$CURRENT" ]; then
        CURRENT=$(pip show reflex 2>/dev/null | grep -oE '0\.[0-9]+\.[0-9]+(\.post[0-9]+)?' | head -1)
    fi
    echo -e "✅ Current: ${GREEN}$CURRENT${NC}"
else
    echo -e "${RED}❌ reflex 未安裝${NC}"
    exit 1
fi

# 2. 查 PyPI 最新版
echo ""
echo "=== PyPI 最新版 ==="
if command -v curl >/dev/null 2>&1; then
    PYPI_VERSION=$(curl -sf https://pypi.org/pypi/reflex/json 2>/dev/null | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])" 2>/dev/null)
    if [ -n "$PYPI_VERSION" ]; then
        echo -e "🌐 Latest PyPI: ${GREEN}$PYPI_VERSION${NC}"
    else
        echo -e "${YELLOW}⚠️  無法查 PyPI（網路問題）${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  curl 未安裝${NC}"
fi

# 3. 查 GitHub 最新 release
echo ""
echo "=== GitHub Latest Release ==="
if command -v curl >/dev/null 2>&1; then
    GH_RELEASE=$(curl -sf https://api.github.com/repos/reflex-dev/reflex/releases/latest 2>/dev/null | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print(d['tag_name'])" 2>/dev/null)
    GH_DATE=$(curl -sf https://api.github.com/repos/reflex-dev/reflex/releases/latest 2>/dev/null | \
        python3 -c "import json,sys; d=json.load(sys.stdin); print(d['published_at'][:10])" 2>/dev/null)
    if [ -n "$GH_RELEASE" ]; then
        echo -e "🌐 Latest GitHub: ${GREEN}$GH_RELEASE${NC} (released: $GH_DATE)"
    else
        echo -e "${YELLOW}⚠️  無法查 GitHub${NC}"
    fi
fi

# 4. 比較
echo ""
echo "=== 比較 ==="
if [ -n "$CURRENT" ] && [ -n "$PYPI_VERSION" ]; then
    if [ "$CURRENT" = "$PYPI_VERSION" ]; then
        echo -e "${GREEN}✅ 已是最新版${NC}"
    else
        echo -e "${YELLOW}⚠️  有新版本可用${NC}"
        echo "  目前: $CURRENT"
        echo "  最新: $PYPI_VERSION"
        echo ""
        echo "升級指令："
        echo "  pip install --upgrade reflex"
    fi
fi

# 5. 更新 manifest
echo ""
echo "=== 更新 manifest ==="
if [ -n "$PYPI_VERSION" ] && [ -f "$MANIFEST" ]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    python3 -c "
import json
with open('$MANIFEST', 'r') as f:
    m = json.load(f)
m['tracked_version'] = '$CURRENT'
m['last_check'] = '$TIMESTAMP'
m['last_release_checked'] = 'v$PYPI_VERSION'
m['upgrade_available'] = '$CURRENT' != '$PYPI_VERSION'
with open('$MANIFEST', 'w') as f:
    json.dump(m, f, indent=2)
print('✅ Manifest updated')
"
fi
