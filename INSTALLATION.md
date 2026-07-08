# Installation Guide

本 skill 透過 GitHub repo 安裝到 5 種 AI coding 工具。**一行指令搞定**。

## 1️⃣ OpenClaw（推薦）

```bash
npx skills add travisebill/reflex-mastery
```

✅ 自動裝好 5 個 sub-skill 到 `~/.openclaw/skills/`。

**只裝部分 sub-skill**：
```bash
npx skills add travisebill/reflex-mastery --selective
# 然後互動式選擇要裝哪些
```

## 2️⃣ Claude Code

### A. 一鍵裝全部（推薦）

```
/plugin marketplace add travisebill/reflex-mastery
```

裝完會出現 5 個 plugin：
- `reflex-docs-advanced`
- `reflex-deployment`
- `reflex-ai-integration`
- `reflex-ux-workflow`
- `reflex-upgrade-monitor`

### B. 選擇性裝

```
/plugin marketplace add travisebill/reflex-mastery
/plugin install reflex-docs-advanced@reflex-mastery
/plugin install reflex-deployment@reflex-mastery
/plugin install reflex-ai-integration@reflex-mastery
/plugin install reflex-ux-workflow@reflex-mastery
/plugin install reflex-upgrade-monitor@reflex-mastery
```

## 3️⃣ OpenAI Codex

```bash
# 方式 A：npx skills（推薦）
npx skills add travisebill/reflex-mastery

# 方式 B：手動 clone
git clone https://github.com/travisebill/reflex-mastery.git
cp -r reflex-mastery/skills/* ~/.codex/skills/
```

## 4️⃣ GitHub Copilot

1. 開 VS Code → Settings → Extensions → GitHub Copilot
2. 找 "Rules" 設定
3. Add Rule → Remote Rule (GitHub)
4. 輸入：`travisebill/reflex-mastery`
5. 確認

## 5️⃣ Cursor

### A. Cursor Marketplace（推薦）
- Settings → Marketplace → 搜尋 "reflex-mastery" → Install

### B. Remote Rule (GitHub)
- Settings → Rules → Add Rule → Remote Rule (GitHub) → `travisebill/reflex-mastery`

### C. npx skills
```bash
npx skills add travisebill/reflex-mastery
```

## 6️⃣ Hermes（待查官方文件）

依 Hermes 官方安裝文件：
- 預期：手動 clone 或 GitHub URL 安裝
- 一旦官方文件確認，會補上

## 7️⃣ OpenCode

```bash
git clone https://github.com/travisebill/reflex-mastery.git
cp -r reflex-mastery/skills/* ~/.config/opencode/skills/
```

## 8️⃣ Pi

```bash
git clone https://github.com/travisebill/reflex-mastery.git
cp -r reflex-mastery/skills/* ~/.pi/agent/skills/
```

---

## 🔄 升級

每個 agent 升級方式不同：

| Agent | 升級指令 |
|-------|---------|
| OpenClaw | `npx skills update travisebill/reflex-mastery` |
| Claude Code | `/plugin marketplace update travisebill/reflex-mastery` |
| Codex | `npx skills update` 或重新 clone |
| Copilot | Settings → 自動更新（GitHub sync） |
| Cursor | Marketplace → Update |
| OpenCode/Pi | `cd reflex-mastery && git pull && cp -r skills/* ~/.config/opencode/skills/` |

---

## 🗑 卸載

| Agent | 卸載指令 |
|-------|---------|
| OpenClaw | `npx skills remove travisebill/reflex-mastery` |
| Claude Code | `/plugin marketplace remove travisebill/reflex-mastery` |
| Codex | `rm -rf ~/.codex/skills/reflex-*` |
| OpenCode | `rm -rf ~/.config/opencode/skills/reflex-*` |
| Pi | `rm -rf ~/.pi/agent/skills/reflex-*` |

---

## 🐛 故障排除

### Sub-skill 沒自動載入

確認安裝路徑：
- OpenClaw：`ls ~/.openclaw/skills/ | grep reflex`
- Claude Code：`/plugin list`
- Codex：`ls ~/.codex/skills/`

### 載入但 description 沒觸發

SKILL.md 的 description 太長或太模糊。檢查：
- description 是否在 160 bytes 內
- 是否明確說「何時用這個 skill」

### 跨平台問題

不同 agent 對 SKILL.md 格式容忍度不同：
- Claude Code 嚴格（要 YAML frontmatter）
- OpenClaw 容錯（沒 frontmatter 也能跑）
- Cursor 中等

---

## 💡 驗證安裝成功

裝完後，問 agent：

> "我要寫一個 Reflex todo app，幫我從 starter template 開始"

如果 agent 自動載入 `reflex-docs-advanced` 並提示從 `templates/reflex-starter/` 複製 → 成功 ✅

如果 agent 問「什麼是 Reflex」→ 沒裝好 ❌ 回到上方故障排除

---

## 🤖 完整工作流需裝 `ui-ux-pro-max`

`reflex-ux-workflow` sub-skill 的「理想工作流」（叫 ui-ux-pro-max 出 design → 套成 Reflex code）需要額外裝 `ui-ux-pro-max` skill。

**沒裝也沒關係** — `reflex-ux-workflow` 5 個 references 中 3 個（design-tokens / component-mapping / a11y）獨立可用。

**完整安裝 ui-ux-pro-max**（如要完整工作流）：

```bash
# 方法 1：CLI（推薦）
npm install -g uipro-cli
cd /path/to/your/project
uipro init --ai claude  # 或 cursor / copilot / codex / opencode / all

# 方法 2：Claude Code
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

# 方法 3：npx skills
npx skills add nextlevelbuilder/ui-ux-pro-max-skill

# 方法 4：手動 clone
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git
```

完整文檔：https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
