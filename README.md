# Reflex Mastery

> **進階模式 + 自動版本追蹤** — Reflex 全端 Python web 開發的完整 skill suite

Reflex 是純 Python 全端 web framework（不用寫 JavaScript）。本 repo 補官方 [`reflex-dev/agent-skills`](https://github.com/reflex-dev/agent-skills) 缺的 5 件事：

1. ✅ **進階 pattern + 踩坑大全**（官方是 reference doc，缺 pattern / pitfall / 升級指南）
2. ✅ **Production 部署全攻略**（Vercel / Fly.io / Railway / Docker / 自架 k8s）
3. ✅ **AI SDK 整合**（minimax / OpenAI / Anthropic / Ollama，含 streaming + cost control）
4. ✅ **與 ui-ux-pro-max skill 協作**（設計 → 實作 handoff）
5. ✅ **自動版本追蹤**（Reflex 0.9.x → 1.0 過渡期，自主升級提示）

---

## 📦 安裝（5 種 agent 通吃）

> 詳細 SOP 見 [INSTALLATION.md](./INSTALLATION.md)

| Agent | 安裝指令 |
|-------|---------|
| **OpenClaw** | `npx skills add travisebill/reflex-mastery` |
| **Claude Code** | `/plugin marketplace add travisebill/reflex-mastery` + 5 個 `/plugin install` |
| **OpenAI Codex** | `npx skills add travisebill/reflex-mastery` |
| **GitHub Copilot** | Settings > Rules > Add Rule > Remote Rule (GitHub) → `travisebill/reflex-mastery` |
| **Cursor** | Cursor Marketplace 或 `npx skills add travisebill/reflex-mastery` |

---

## 🧩 Sub-skills（5 個獨立可選）

| Sub-skill | 用途 |
|-----------|------|
| `reflex-docs-advanced` | 進階 framework 知識（architecture / patterns / pitfalls） |
| `reflex-deployment` | Production 部署（8 平台 + Docker + build.reflex.dev MCP） |
| `reflex-ai-integration` | AI SDK 整合（4 provider + streaming + cost control） |
| `reflex-ux-workflow` | 與 ui-ux-pro-max skill 協作（design → 實作 handoff + a11y） |
| `reflex-upgrade-monitor` | 自動版本追蹤 + 升級指南（0.8 → 0.9 → 1.0） |

> 預設**全裝**。主人可選擇性卸載不需要的 sub-skill。

---

## 🚀 快速開始

### 1. 從 starter template 開新專案

```bash
cp -r templates/reflex-starter/ my-reflex-app/
cd my-reflex-app/
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt
bash scripts/dev.sh
```

### 2. 載入 skill 後直接問

```
我要寫一個 todo app，使用 Reflex + Supabase auth，請依 reflex-ux-workflow 引導設計
```

```
幫我部署這個 Reflex app 到 Fly.io
```

```
Reflex 出新版本了嗎？breaking changes 是什麼？
```

---

## 📊 與官方 reflex-dev/agent-skills 互補

| 場景 | 用哪個 |
|------|--------|
| 查 framework 知識（基本） | 官方 `reflex-docs` |
| 建環境 | 官方 `setup-python-env` |
| 跑 dev server | 官方 `reflex-process-management` |
| 進階 pattern / 踩坑 | **本 `reflex-docs-advanced`** |
| Production 部署 | **本 `reflex-deployment`** |
| AI SDK 整合 | **本 `reflex-ai-integration`** |
| 設計 → 實作 handoff | **本 `reflex-ux-workflow`** |
| 自動版本追蹤 | **本 `reflex-upgrade-monitor`** |

---

## 🗂 Repo 結構

```
reflex-mastery/
├── README.md                        # 你正在看
├── INSTALLATION.md                  # 各 agent 安裝 SOP
├── LICENSE                          # MIT
├── .claude-plugin/marketplace.json  # Claude Code marketplace
├── package.json                     # npx skills metadata
├── skills/                          # 5 個 sub-skill
├── examples/                        # 完整可跑 apps
├── templates/reflex-starter/        # starter project
└── docs/                            # 設計 + 計畫文件
```

---

## 🤝 與 ui-ux-pro-max 協作

`reflex-ux-workflow` sub-skill 會在需求階段引導你呼叫 [`ui-ux-pro-max`](https://docs.openclaw.ai) 出 design（design tokens / wireframe / component list），然後 handoff 給 Reflex 實作。

工作流：
1. 主人下指令要寫新 Reflex app
2. `reflex-ux-workflow` 引導呼叫 `ui-ux-pro-max` 出 design
3. 把 design tokens 套成 `rx.theme()`、component 規格 → `rx.*` 對應
4. 開始實作

---

## 🛠 維護

- **自動升級提示**：`reflex-upgrade-monitor` 會偵測 Reflex 新版本
- **Breaking change 整理**：見 `skills/reflex-upgrade-monitor/references/upgrade-guide.md`
- **Issue / PR**：歡迎到 [GitHub Issues](https://github.com/travisebill/reflex-mastery/issues)

---

## 📝 License

MIT © 2026 travisebill
