#!/bin/bash
# suggest_upgrade.sh — 分析 breaking changes
# Usage: bash suggest_upgrade.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/../version_manifest.json"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ ! -f "$MANIFEST" ]; then
    echo "❌ Manifest not found: $MANIFEST"
    exit 1
fi

CURRENT=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['tracked_version'])")
LATEST=$(python3 -c "import json; print(json.load(open('$MANIFEST')).get('last_release_checked', 'unknown').lstrip('v'))")

echo "=== Upgrade Analysis ==="
echo "Current: $CURRENT"
echo "Latest:  $LATEST"
echo ""

if [ "$CURRENT" = "$LATEST" ]; then
    echo -e "${GREEN}✅ 已是最新版，無需升級${NC}"
    exit 0
fi

# 簡化版：根據版本範圍給建議
# 實際應該從 GitHub changelog 解析

echo "=== 升級建議 ==="

# 判斷是 patch / minor / major
CURRENT_MAJOR=$(echo "$CURRENT" | cut -d. -f1)
CURRENT_MINOR=$(echo "$CURRENT" | cut -d. -f2)
LATEST_MAJOR=$(echo "$LATEST" | cut -d. -f1)
LATEST_MINOR=$(echo "$LATEST" | cut -d. -f2)

if [ "$CURRENT_MAJOR" != "$LATEST_MAJOR" ]; then
    echo -e "${RED}⚠️  Major 版本升級 ($CURRENT_MAJOR → $LATEST_MAJOR)${NC}"
    echo "  - 必看升級指南 references/upgrade-guide.md"
    echo "  - 多半有 API breaking change"
    echo "  - 建議先在 dev branch 測試"
elif [ "$CURRENT_MINOR" != "$LATEST_MINOR" ]; then
    echo -e "${YELLOW}⚠️  Minor 版本升級 ($CURRENT → $LATEST)${NC}"
    echo "  - 看 changelog 確認"
    echo "  - 通常有 deprecation warning"
    echo "  - 大多 safe to upgrade"
else
    echo -e "${GREEN}✅ Patch 版本升級 ($CURRENT → $LATEST)${NC}"
    echo "  - 通常 safe"
    echo "  - 修 bug 為主"
    echo "  - 可直接 pip install --upgrade"
fi

echo ""
echo "=== 行動 ==="
echo "1. 看完整 changelog:"
echo "   bash $SCRIPT_DIR/fetch_changelog.sh --from $CURRENT --to $LATEST"
echo ""
echo "2. 升級指令:"
echo "   pip install --upgrade reflex==$LATEST"
echo ""
echo "3. 升級後驗證:"
echo "   reflex compile --dry"
echo "   pytest"
echo ""
echo "4. 更新 manifest:"
echo "   # 編輯 $MANIFEST 把 tracked_version 改成 $LATEST"
