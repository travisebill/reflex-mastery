# Reflex Mastery Skill — Plan v0.2
**Date**: 2026-07-09 00:58 GMT+8
**Author**: Nigo 🐱
**Status**: Draft v0.2 (待主人 review)
**Supersedes**: v0.1（保留為 archive）

---

## 🆕 v0.2 新增原因

主人 3 個新需求：

1. **未來主力使用 Reflex 當工作棧**（多 app、long-term）
2. **app 中直接使用 AI SDK**（minimax / OpenAI / Anthropic / Ollama）
3. **搭配 ui-ux-pro-max skill 最佳化 UX**

v0.1 涵蓋分析（3 個層次）：

| 需求 | v0.1 涵蓋 | 評估 |
|------|----------|------|
| ① 主力工作棧 | ✅ 開發流程部分 | ⚠️ 缺**多專案管理** + starter template |
| ② AI SDK 整合 | ❌ 完全沒提 | ❌ **完全要新增** |
| ③ ui-ux-pro-max 協作 | ❌ 完全沒提 | ❌ **完全要新增** |

**結論：3 個需求 → 要擴充成 v0.2**

---

## 🆕 v0.2 擴充內容

### 新增 1：`references/06-ai-sdk-integration.md`（~5-8 KB）

**目標**：Reflex app 整合 AI LLM SDK 的完整指南

**涵蓋**：
- 4 個 provider 的最小接法：
  - `minimax-python-sdk`（主人目前用）
  - `openai` SDK（GPT-4o / o1 / o3）
  - `anthropic` SDK（Claude 3.5/4）
  - `ollama`（本地模型，self-hosted）
- API key 安全管理（env var / dotenv / secret manager）
- chat UI 模式：streaming response（generator-based event handler）
- token 計數 + cost 控制（per-user quota、daily cap、model tier 切換）
- context window 管理（truncation strategy、summary、vector store）
- function calling / tool use（如果 provider 支援）
- 完整 working example：Reflex chat app

### 新增 2：`references/07-ux-workflow.md`（~3-5 KB）

**目標**：與 ui-ux-pro-max skill 協作的完整工作流

**涵蓋**：
- **何時**叫 ui-ux-pro-max（需求階段 + design 階段）
- **handoff 格式**：從 ui-ux-pro-max 拿到什麼 → 怎麼轉成 Reflex 實作
  - design tokens（colors / spacing / typography）→ `rx.theme()` 對應
  - component 規格（shadcn / radix / custom）→ `rx.*` 或 custom component
  - 互動規格 → state + event handler 規劃
- **page 結構**對應（ui-ux-pro-max wireframe → Reflex pages）
- **accessibility checklist**（ARIA、keyboard nav、focus management）
- **a11y testing**：axe-core / pa11y 整合進 CI

### 新增 3：`templates/reflex-starter/`（starter project，~6-10 KB）

**目標**：主人未來每個 Reflex app 從同一個起點開始

**包含**：
```
templates/reflex-starter/
├── README.md                  # 快速啟動 SOP
├── rxconfig.py                # 預先配好（db url / theme / port）
├── .env.example               # env var 範本
├── requirements.txt           # 預裝 reflex + sqlmodel + dotenv
├── assets/
│   └── theme.py               # rx.theme() 預設（semantic colors）
├── pages/
│   ├── __init__.py
│   ├── index.py               # landing page
│   ├── dashboard.py           # 含 auth guard 範例
│   └── _404.py
├── states/
│   ├── base.py                # 全域 state（含 auth 檢查）
│   └── auth.py                # login / logout state
├── db/
│   ├── models.py              # SQLModel 範例
│   └── connection.py          # db 連線 + migration
├── components/
│   └── layout.py              # 統一 layout (header / sidebar / footer)
└── scripts/
    └── dev.sh                 # 啟動 SOP (load .env + reflex run)
```

**starter 特性**：
- ✅ 內建 semantic color theme
- ✅ 內建 layout component（避免每個 app 重寫）
- ✅ 內建 auth 範例（可以接 Supabase / Clerk / 自架）
- ✅ 內建 db 連線範例（SQLModel + Postgres / SQLite）
- ✅ 內建 404 + loading state
- ✅ README 有「從這開始」的 5 步 SOP

### 新增 4：`examples/ai-chat-app/`（~8-12 KB）

**目標**：完整可跑的 Reflex + AI SDK chat app

**包含**：
- 4 個 provider 切換（dropdown UI 選 minimax / OpenAI / Anthropic / Ollama）
- streaming response UI
- conversation history（db 存）
- token usage + cost tracker
- 多 model 比較（同一個問題問 2 個 model 並排顯示）
- 完整 code + README + 啟動 SOP

---

## 🆕 整合後的新工作流程（v0.2）

```
[主人下指令：要寫 Reflex app]
   ↓
Step 1: 規劃 scope（page 結構 / data flow / 要不要 AI）
   ↓
Step 2: 叫 ui-ux-pro-max 出 design（tokens / wireframe / component list）
   ↓
Step 3: 從 templates/reflex-starter 開新專案（複製 → 改名 → 跑）
   ↓
Step 4: 套用 design tokens → rx.theme()（07-ux-workflow 教）
   ↓
Step 5: 寫 pages / state / events（02-patterns 教）
   ↓
Step 6: 接 AI SDK（如果需要）→ 06-ai-sdk-integration 教
   ↓
Step 7: 本地跑（官方 reflex-process-management + templates/reflex-starter/scripts/dev.sh）
   ↓
Step 8: 部署（05-deployment 教）— 包含 build.reflex.dev
   ↓
Step 9: 跑 check_version.sh 確認依賴最新（scripts）
   ↓
Step 10: 持續改進 + 自動追蹤新版本（version monitor）
```

---

## 📊 v0.2 完整檔案結構

```
reflex-mastery/
├── SKILL.md                              # 入口
├── version_manifest.json                 # {tracked_version, last_check, breaking_since}
├── references/
│   ├── 01-architecture.md
│   ├── 02-patterns.md
│   ├── 03-pitfalls.md
│   ├── 04-upgrade-guide.md
│   ├── 05-deployment.md
│   ├── 06-ai-sdk-integration.md          # 🆕 v0.2
│   └── 07-ux-workflow.md                 # 🆕 v0.2
├── scripts/
│   ├── check_version.sh
│   ├── fetch_changelog.sh
│   ├── suggest_upgrade.sh
│   ├── self_update.sh
│   ├── setup_ai_provider.sh              # 🆕 v0.2 (env + 驗證連線)
│   └── estimate_cost.sh                  # 🆕 v0.2 (token cost 預估)
├── templates/                            # 🆕 v0.2
│   └── reflex-starter/
│       └── ... (見上方)
└── examples/
    ├── todo-app/
    ├── auth-db-app/
    └── ai-chat-app/                      # 🆕 v0.2
```

---

## 📊 v0.2 預估工作量

| 項目 | v0.1 | v0.2 新增 | 總計 |
|------|------|----------|------|
| References | 5 個 ~20KB | +2 個 ~10KB | 7 個 ~30KB |
| Scripts | 4 個 ~5KB | +2 個 ~3KB | 6 個 ~8KB |
| Templates | 0 | +1 個 ~8KB | 1 個 ~8KB |
| Examples | 2 個 ~15KB | +1 個 ~10KB | 3 個 ~25KB |
| SKILL.md | 1 個 ~5KB | 改寫整合 ~7KB | 1 個 ~7KB |
| **總計** | ~45KB | **+~38KB** | **~83KB** |

**預估 token 花費**：偏大（這是個**完整 skill suite**，不是單一文件）

---

## ❓ 待主人決策（v0.2 新增）

### 5️⃣ AI SDK 範圍
- 🅰️ **4 家全支援**（minimax / OpenAI / Anthropic / Ollama）→ 通用但工作量大
- 🅱️ **只 minimax**（主人目前用）→ 最小 scope，但未來加 provider 要改
- 🅲️ **minimax + OpenAI**（兩家主流）→ 平衡

### 6️⃣ ui-ux-pro-max 整合深度
- 🅰️ **強烈建議每個 app 都要先過 ui-ux-pro-max**（SKILL.md 寫進 SOP）
- 🅱️ **Optional**（只在 07-ux-workflow 提到，不強制）

### 7️⃣ starter template 範圍
- 🅰️ **完整版**（auth + db + layout + theme）→ 主人複製就能用，但 8-10KB
- 🅱️ **精簡版**（只有 rx config + theme + 1 page）→ 5KB，未來要自己加

### 8️⃣ 範例 app 範圍
- 🅰️ **完整版 ai-chat-app**（4 provider + streaming + cost tracker）→ 10-12KB
- 🅱️ **MVP 版**（只 minimax + 1 個 chat page）→ 5KB

### 9️⃣ apply 時機
- 🅰️ **全寫完一次 apply**（所有 83KB 一起）
- 🅱️ **分批 apply**（先 references → 主人 review → 再 templates/examples）

---

## 📋 累計待決策（v0.1 + v0.2 共 9 題）

1. 命名（reflex-mastery / advanced / pro）
2. v0.1 scope（要不要 examples/）
3. 自動更新策略（只提示 / 全自動）
4. v0.1 apply 時機
5. AI SDK 範圍 🆕
6. ui-ux-pro-max 整合深度 🆕
7. starter template 範圍 🆕
8. 範例 app 範圍 🆕
9. v0.2 apply 時機 🆕
