#!/bin/bash
# setup_ai_provider.sh — 設定 AI provider + 驗證連線
# Usage: bash scripts/setup_ai_provider.sh [minimax|openai|anthropic|ollama|all]

set -e

PROVIDER="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 載入 .env
if [ -f "$ROOT_DIR/.env" ]; then
    set -a
    source "$ROOT_DIR/.env"
    set +a
fi

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

success() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

check_minimax() {
    echo "=== minimax ==="
    if [ -z "$MINIMAX_API_KEY" ]; then
        fail "MINIMAX_API_KEY 未設定"
        return 1
    fi
    if command -v curl >/dev/null 2>&1; then
        if curl -sf -H "Authorization: Bearer $MINIMAX_API_KEY" \
            https://api.minimax.io/v1/models >/dev/null 2>&1; then
            success "minimax API key 有效"
        else
            fail "minimax API key 無效或網路問題"
            return 1
        fi
    else
        warn "curl 未安裝，跳過驗證"
    fi
}

check_openai() {
    echo "=== OpenAI ==="
    if [ -z "$OPENAI_API_KEY" ]; then
        fail "OPENAI_API_KEY 未設定"
        return 1
    fi
    if command -v curl >/dev/null 2>&1; then
        if curl -sf -H "Authorization: Bearer $OPENAI_API_KEY" \
            https://api.openai.com/v1/models >/dev/null 2>&1; then
            success "OpenAI API key 有效"
        else
            fail "OpenAI API key 無效"
            return 1
        fi
    fi
}

check_anthropic() {
    echo "=== Anthropic ==="
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        fail "ANTHROPIC_API_KEY 未設定"
        return 1
    fi
    if command -v curl >/dev/null 2>&1; then
        if curl -sf -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            https://api.anthropic.com/v1/messages \
            -X POST -d '{"model":"claude-3-5-haiku-20241022","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}' \
            >/dev/null 2>&1; then
            success "Anthropic API key 有效"
        else
            fail "Anthropic API key 無效"
            return 1
        fi
    fi
}

check_ollama() {
    echo "=== Ollama ==="
    if command -v curl >/dev/null 2>&1; then
        if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
            success "Ollama running at localhost:11434"
            echo "已安裝 models："
            curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'  - {m[\"name\"]}') for m in d.get('models',[])]" 2>/dev/null || true
        else
            fail "Ollama 未啟動（執行 'ollama serve'）"
            return 1
        fi
    fi
}

case "$PROVIDER" in
    minimax) check_minimax ;;
    openai) check_openai ;;
    anthropic) check_anthropic ;;
    ollama) check_ollama ;;
    all)
        check_minimax
        echo ""
        check_openai
        echo ""
        check_anthropic
        echo ""
        check_ollama
        ;;
    *)
        echo "Usage: $0 [minimax|openai|anthropic|ollama|all]"
        exit 1
        ;;
esac

echo ""
echo "=== 設定完成 ==="
