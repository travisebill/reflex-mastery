# Reflex Mastery Skill — Plan v0.3
**Date**: 2026-07-09 01:05 GMT+8
**Author**: Nigo 🐱
**Status**: Draft v0.3 (待主人 review)
**Supersedes**: v0.2 (保留為 archive)

---

## 🆕 v0.3 觸發原因

主人新增需求 ④：**做完後要能簡單透過 GitHub repo 安裝到其他 AI coding 工具**
- 目標 agent: GitHub Copilot / OpenAI Codex / Claude Code / Hermes / OpenClaw / Cursor

**現實限制**：
- Agent Skills 標準 (https://agentskills.io/) 要求**每個 skill 是獨立資料夾 + SKILL.md**
- 主流安裝方式都吃 GitHub repo URL：
  - Claude Code: `/plugin marketplace add <owner>/<repo>`
  - npx skills: `npx skills add <owner>/<repo>`
  - Copilot: Remote Rule (GitHub) → `<owner>/<repo>`
- 官方 `reflex-dev/agent-skills` 就是 3 個獨立 sub-skill 結構
- ❌ v0.2 設計的「**單一 skill 內含 7 個 references**」→ **不能跨 agent 安裝**

**結論：v0.2 不行，要重構為 v0.3（多 sub-skill + GitHub repo 結構）**

---

## 🆕 v0.3 核心改變：拆成 multi-skill

### 從「1 個 skill」變「5 個 sub-skill」

| Sub-skill | 涵蓋內容 | 對應 v0.2 references |
|-----------|---------|------------------|
| `reflex-docs-advanced` | architecture + patterns + pitfalls | 01 + 02 + 03 |
| `reflex-deployment` | deploy + Docker + MCP/build.reflex.dev | 05 |
| `reflex-ai-integration` | 4 providers + streaming + cost control | 06 + scripts (`setup_ai_provider`, `estimate_cost`) |
| `reflex-ux-workflow` | ui-ux-pro-max 協作 + a11y | 07 |
| `reflex-upgrade-monitor` | 自動版本追蹤 + upgrade guide | 04 + scripts (`check_version`, `fetch_changelog`, `suggest_upgrade`, `self_update`) |

> starter template (`reflex-starter`) 放在 `examples/` 不獨立成 sub-skill（太大、不是知識型 skill）

---

## 📦 v0.3 GitHub Repo 結構

```
reflex-mastery/                          # GitHub repo: travisebill/reflex-mastery
├── README.md                             # 主入口（給人看 + 給 Claude Code marketplace 讀）
├── INSTALLATION.md                       # 各 agent 安裝 SOP（5 種 agent 步驟）
├── LICENSE                               # MIT
├── .claude-plugin/
│   └── marketplace.json                  # Claude Code marketplace 設定
├── package.json                          # npx skills metadata
├── skills/                               # Agent Skills 標準結構
│   ├── reflex-docs-advanced/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── architecture.md
│   │   │   ├── patterns.md
│   │   │   └── pitfalls.md
│   │   └── assets/
│   │       └── diagrams/
│   ├── reflex-deployment/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── platforms.md             # Vercel/Fly.io/Railway/Render/DO/AWS/GCP/k8s
│   │   │   ├── docker.md
│   │   │   ├── self-hosted.md
│   │   │   └── build-reflex-dev.md      # MCP 整合
│   │   └── assets/
│   │       └── dockerfiles/
│   ├── reflex-ai-integration/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── minimax.md
│   │   │   ├── openai.md
│   │   │   ├── anthropic.md
│   │   │   ├── ollama.md
│   │   │   ├── streaming.md
│   │   │   ├── cost-control.md
│   │   │   └── context-window.md
│   │   ├── scripts/
│   │   │   ├── setup_ai_provider.sh
│   │   │   └── estimate_cost.sh
│   │   └── examples/
│   │       └── chat-stream.py
│   ├── reflex-ux-workflow/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── when-to-call.md
│   │   │   ├── handoff-format.md
│   │   │   ├── design-tokens-mapping.md # ui-ux-pro-max 輸出 → rx.theme()
│   │   │   ├── component-mapping.md     # 設計稿 → rx.* 對應
│   │   │   └── accessibility.md
│   │   └── checklists/
│   │       └── a11y-checklist.md
│   ├── reflex-upgrade-monitor/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── upgrade-guide.md
│   │   ├── scripts/
│   │   │   ├── check_version.sh
│   │   │   ├── fetch_changelog.sh
│   │   │   ├── suggest_upgrade.sh
│   │   │   └── self_update.sh
│   │   └── version_manifest.json
├── examples/                             # 完整可跑的範例 apps
│   ├── todo-app/                         # MVP 模板
│   ├── auth-db-app/                      # Supabase auth + Postgres
│   └── ai-chat-app/                      # 4 provider + streaming + cost tracker
├── templates/                            # Starter project（給主人複製）
│   └── reflex-starter/
│       ├── README.md
│       ├── rxconfig.py
│       ├── .env.example
│       ├── requirements.txt
│       ├── assets/
│       │   └── theme.py
│       ├── pages/
│       ├── states/
│       ├── db/
│       ├── components/
│       └── scripts/
│           └── dev.sh
└── docs/                                 # 額外文件（給人讀，不給 agent）
    ├── getting-started.md
    ├── architecture-decisions.md         # 為什麼這樣設計
    └── contributing.md
```

---

## 🔌 各 Agent 安裝 SOP

### 1️⃣ OpenClaw / 通用
```bash
npx skills add travisebill/reflex-mastery
```

### 2️⃣ Claude Code
```
/plugin marketplace add travisebill/reflex-mastery
/plugin install reflex-docs-advanced@reflex-mastery
/plugin install reflex-deployment@reflex-mastery
/plugin install reflex-ai-integration@reflex-mastery
/plugin install reflex-ux-workflow@reflex-mastery
/plugin install reflex-upgrade-monitor@reflex-mastery
```

### 3️⃣ OpenAI Codex
- 手動 clone 到 `~/.codex/skills/`
- 或 `npx skills add travisebill/reflex-mastery`

### 4️⃣ GitHub Copilot
- Settings > Rules > Add Rule > Remote Rule (GitHub) → `travisebill/reflex-mastery`

### 5️⃣ Cursor
- Cursor Marketplace
- 或 `npx skills add travisebill/reflex-mastery`

### 6️⃣ Hermes
- 需查官方文件（Hermes 是新興 agent）
- 預期走 GitHub clone 方式

### 7️⃣ OpenCode
- 手動 clone 到 `~/.config/opencode/skills/`

---

## 📊 v0.3 工作量估算

| 項目 | v0.2 | v0.3 變化 | 總計 |
|------|------|----------|------|
| **Sub-skills** | 1 個 (整包) | **+5 個獨立** | 5 個 SKILL.md |
| References (總內容) | 7 個 ~30KB | 分散到 5 個 sub-skill，內容不變 | ~30KB |
| Scripts | 6 個 ~8KB | 分散，內容不變 | ~8KB |
| Examples | 3 個 ~25KB | 分散，內容不變 | ~25KB |
| Templates | 1 個 ~8KB | 不變 | ~8KB |
| **Distribution metadata** | ❌ | **+~0.5KB** | marketplace.json + package.json |
| **README + INSTALLATION** | ❌ | **+~2-3KB** | 給人 + 給 agent |
| **Architecture decision doc** | ❌ | **+~1KB** | 為什麼這樣拆 |
| **總計** | ~83KB | **+~3.5KB metadata** | **~87KB** |

工作量**不變**（內容一樣），但**結構複雜度**↑：
- 5 個 SKILL.md 要各自維護
- references / scripts 分散到對應 sub-skill
- cross-sub-skill reference 要管理
- distribution metadata 要驗證

---

## 🎁 額外好處（v0.3 帶來的）

1. ✅ **主人可選擇性裝**：只要 deployment 就只裝 `reflex-deployment`（節省 skill 載入時間）
2. ✅ **跟 `reflex-dev/agent-skills` 結構一致**（都 5 個 sub-skill 規模）
3. ✅ **可單獨升級某個 sub-skill**（不用整包升）
4. ✅ **Claude Code marketplace 可列出每個 sub-skill**（使用者可選裝）
5. ✅ **README + INSTALLATION.md 是公開文件**（其他人也能用這個 skill）

---

## 🆕 新工作流程（v0.3）

```
[主人下指令：裝 reflex-mastery]
   ↓
   npx skills add travisebill/reflex-mastery
   ↓
   5 個 sub-skill 自動裝好（或主人選擇性裝）
   ↓
[主人下指令：寫新 Reflex app]
   ↓
   reflex-upgrade-monitor 先跑（確認 reflex 最新版）
   ↓
   reflex-ux-workflow 引導：叫 ui-ux-pro-max 出 design
   ↓
   reflex-docs-advanced 提供 patterns
   ↓
   reflex-ai-integration（如果需要 AI）
   ↓
   reflex-deployment 收尾
```

---

## ❓ v0.3 待主人決策

### 🔟 sub-skill 拆分粒度
- 🅰️ **5 個 sub-skill**（推薦，v0.3 設計）— docs-advanced / deployment / ai-integration / ux-workflow / upgrade-monitor
- 🅱️ **3 個 sub-skill**（合併）— docs+pitfalls / deploy+ai / ux+upgrade
- 🅲️ **保持 v0.2 單一 skill**（但要加 distribution metadata）

### ⓫ GitHub repo 命名
- 🅰️ `travisebill/reflex-mastery`（推薦）
- 🅱️ `travisebill/reflex-advanced`
- 🅲️ `travisebill/reflex-pro`

### ⓬ install 模式
- 🅰️ **全裝**（一次裝 5 個 sub-skill，預設）
- 🅱️ **主人自己選**（`npx skills add travisebill/reflex-mastery --selective`）

### ⓭ v0.3 apply 時機
- 🅰️ 全寫完一次 apply（5 個 sub-skill 一起）
- 🅱️ 分批：先 sub-skill 1（docs-advanced）+ README → 主人 review → 再加 2-5

### ⓮ 是否先做 GitHub repo init
- 🅰️ 先建 GitHub repo（讓主人看見 commit 進度）
- 🅱️ 全部在 local 寫完再 push

---

## 📋 累計待決策（v0.1 + v0.2 + v0.3 共 14 題）

| # | 問題 | 預設值（如不答） |
|---|------|----------------|
| 1 | 命名 | reflex-mastery |
| 2 | v0.1 scope | 含 examples |
| 3 | 自動更新策略 | 只提示不自動 |
| 4 | v0.1 apply | 全寫完 |
| 5 | AI SDK 範圍 | 4 家 |
| 6 | ui-ux-pro-max 整合 | 強烈建議 |
| 7 | starter template 範圍 | 完整版 |
| 8 | ai-chat-app 範圍 | 完整版 |
| 9 | v0.2 apply | 全寫完 |
| **10** | **sub-skill 拆分粒度** 🆕 | **5 個** |
| **11** | **GitHub repo 命名** 🆕 | `travisebill/reflex-mastery` |
| **12** | **install 模式** 🆕 | **全裝** |
| **13** | **v0.3 apply** 🆕 | **全寫完** |
| **14** | **先建 GitHub repo** 🆕 | **是** |

> 💡 主人若不回，就用預設值推進。
