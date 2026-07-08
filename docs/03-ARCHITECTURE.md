# Architecture Decisions — 為什麼這樣設計

> 解釋 reflex-mastery 為什麼拆成 5 個 sub-skill + 各種結構決策

---

## 🎯 核心決策

### 1. 為什麼拆成 5 個 sub-skill（不是 1 個 mega-skill）

**理由**：
- Agent Skills 標準要求**獨立資料夾 + SKILL.md**
- 主流安裝方式（Claude Code / npx / Copilot / Cursor）吃 GitHub repo URL
- 主人可選擇性裝（只要 deployment 就只裝 `reflex-deployment`）
- 可單獨升級某個 sub-skill
- Claude Code marketplace 可分開列出

**對比**：
- ❌ 1 個 mega-skill：不能選擇性裝、升級要整包
- ❌ 拆 3 個：粒度太粗，deployment + ai + ux 不該綁一起
- ✅ 5 個：剛好對應 5 個不同 use case

### 2. 為什麼走 PyPI + GitHub API 查版本（不 require MCP）

**理由**：
- MCP 是 optional enhancement
- skill 主體要能獨立運作（任何 agent 都能用，不依賴 MCP）
- scripts 走 PyPI + GitHub release API 是 universal
- 在 `05-deployment.md` 介紹 build.reflex.dev MCP（作為 deploy 選項）

### 3. 為什麼 5 個 sub-skill 各自一個 SKILL.md

**理由**：
- 符合 Agent Skills 標準
- description 觸發條件精準（不會誤觸）
- load 順序可控制
- 一個 page 只觸發需要的 sub-skill（省 context）

### 4. 為什麼 starter template 獨立在 templates/（不在 sub-skill）

**理由**：
- starter 是**程式碼**，不是**知識型 skill**
- skill 應該是「教 agent 怎麼做」不是「給 agent 用的程式碼」
- 放 templates/ 主人複製改名 → 開新 app
- 跟 reflex-dev/agent-skills 結構一致

### 5. 為什麼 3 個 examples（todo / auth-db / ai-chat）

**理由**：
- todo: 最小 MVP 模板
- auth-db: real-world 整合（Supabase + Postgres）
- ai-chat: 4 provider + streaming + cost（最複雜場景）
- 涵蓋 80% 主人 use case

### 6. 為什麼 design 用 semantic colors（不用 raw Tailwind）

**理由**：
- 換 design theme 不用改每個 component
- 對 dark mode 友善
- 跟 nuxt-ui / shadcn 主流設計系統一致
- ai-ux-pro-max skill 出的 tokens 直接套用

### 7. 為什麼 4 個 AI provider 都支援

**理由**：
- 主人用 minimax（預設）
- 但工作場景會切換（成本 / 隱私 / 品質）
- OpenAI: 某些任務最強
- Anthropic: 長 context / 推理
- Ollama: 隱私 / 離線 / 省錢
- 1 個 abstraction layer（providers.py）切換零改 code

### 8. 為什麼不在 sub-skill 內放完整 code example

**理由**：
- example 太長會擠壓 references
- 改放 `examples/<app>/` 主人看完整可跑的 code
- references 講「為什麼這樣」+ 「概念」
- example 講「完整實作」

---

## 🔗 跟其他 skill 的互補

| 這個 skill 提供 | 不重複官方 | 互補其他 skill |
|----------------|----------|---------------|
| Reflex 進階知識 | 官方 reflex-docs | - |
| Reflex 部署 | 官方 reflex-process-management (僅 dev) | - |
| Reflex + AI | ❌ 官方沒有 | minimax/OpenAI/Anthropic skill（如果存在） |
| Reflex + UX | ❌ 官方沒有 | **ui-ux-pro-max**（這個 skill 引導去叫它） |
| Reflex 版本追蹤 | ❌ 官方沒有 | - |

---

## 🛡 設計原則

1. **Self-contained**：每個 sub-skill 獨立可讀
2. **Progressive disclosure**：SKILL.md 簡介 → references 細節
3. **No magic**：scripts 是 plain bash，不依賴特殊工具
4. **Cross-platform**：bash + Python 標準庫，避免外部依賴
5. **Fail-safe**：scripts 有顏色提示 + 失敗訊息清楚
6. **Open source**：MIT license，歡迎 PR

---

## 📈 未來演進

### v0.4 可能加

- More sub-skill: `reflex-testing`（pytest + playwright E2E）
- More sub-skill: `reflex-performance`（bundle size / SSR / state 規模化）
- i18n：英文版 SKILL.md
- CI workflow（GitHub Actions for skill validation）

### v1.0（等 Reflex 1.0 stable）

- 更新 upgrade-guide.md
- Re-test 所有 examples 對 1.0
- Re-build starter template for 1.0 API
- Tag v1.0

---

## 🤝 貢獻

歡迎 PR：

1. 修 typo / 改進 wording
2. 加新 references
3. 改進 scripts
4. 翻譯成其他語言

詳見 [04-CONTRIBUTING.md](./04-CONTRIBUTING.md)（待寫）
