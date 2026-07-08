# Reflex Starter Template

> 主人未來每個 Reflex app 從這複製開始

## 🚀 5 步快速啟動

```bash
# 1. 複製
cp -r templates/reflex-starter/ my-app/
cd my-app/

# 2. 改名
# 編輯 rxconfig.py 的 app_name
# 編輯 pyproject.toml / package.json / 任何有 "reflex_starter" 的地方

# 3. 設定 env
cp .env.example .env
# 編輯 .env 設 DB_URL / API_KEY 等

# 4. 裝 deps
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 5. 跑
bash scripts/dev.sh
# 開 http://localhost:3000
```

## 📦 包含什麼

- ✅ **rxconfig.py** — 預先配好 theme + port + db url
- ✅ **theme.py** — semantic color theme（含 dark mode）
- ✅ **layout.py** — 統一 layout（header / sidebar / footer）
- ✅ **auth state** — login/logout/register state（搭配 Supabase）
- ✅ **base state** — 共用 base state
- ✅ **db models** — User + Todo 範例
- ✅ **4 個 pages** — index / dashboard / 404
- ✅ **a11y 預設** — 鍵盤 nav + focus + ARIA

## 🎨 換 design

1. 編輯 `assets/theme.py` 改色
2. 編輯 `components/layout.py` 改 layout
3. 編輯 `pages/*.py` 改 page 結構

## 🔌 整合

- **Supabase auth**：在 `states/auth.py` 換成 Supabase 呼叫
- **Postgres**：在 `db/connection.py` 改 connection string
- **AI SDK**：在 `pages/index.py` 串接（看 reflex-ai-integration skill）

## 📚 延伸

- 看 `reflex-docs-advanced` skill 學進階 pattern
- 看 `reflex-ux-workflow` skill 學 design handoff
- 看 `reflex-deployment` skill 學 deploy
