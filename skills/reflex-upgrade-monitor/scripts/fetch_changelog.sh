#!/bin/bash
# fetch_changelog.sh — 抓完整 changelog
# Usage: bash fetch_changelog.sh [--from VERSION] [--to VERSION] [--output FILE]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FROM_VERSION="0.9.0"
TO_VERSION="latest"
OUTPUT_FILE=""

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --from) FROM_VERSION="$2"; shift 2 ;;
        --to) TO_VERSION="$2"; shift 2 ;;
        --output) OUTPUT_FILE="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

echo "=== Reflex Changelog ==="
echo "From: $FROM_VERSION"
echo "To:   $TO_VERSION"
echo ""

# 1. PyPI changelog (from description)
echo "=== PyPI Description (前 500 chars) ==="
curl -sf https://pypi.org/pypi/reflex/json 2>/dev/null | \
    python3 -c "
import json, sys
d = json.load(sys.stdin)
desc = d['info'].get('description', '')[:500]
print(desc)
" 2>/dev/null || echo "(無法讀取)"

echo ""
echo ""

# 2. GitHub Releases
echo "=== GitHub Releases ==="
if [ "$TO_VERSION" = "latest" ]; then
    curl -sf "https://api.github.com/repos/reflex-dev/reflex/releases?per_page=20" 2>/dev/null | \
        python3 -c "
import json, sys
releases = json.load(sys.stdin)
for r in releases:
    if r.get('draft') or r.get('prerelease'):
        continue
    name = r.get('name') or r.get('tag_name')
    date = r.get('published_at', '')[:10]
    body = r.get('body', '')[:1000]
    print(f'## {name} ({date})')
    print()
    print(body)
    print()
    print('---')
    print()
" 2>/dev/null || echo "(無法讀取 GitHub)"
fi

# 3. Output to file
if [ -n "$OUTPUT_FILE" ]; then
    echo ""
    echo "=== 寫到 $OUTPUT_FILE ==="
    {
        echo "# Reflex Changelog"
        echo "From: $FROM_VERSION → To: $TO_VERSION"
        echo "Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
        echo ""
    } > "$OUTPUT_FILE"
fi
