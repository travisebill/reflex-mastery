# build.reflex.dev — Reflex 官方 Deploy Platform + MCP Server

> https://build.reflex.dev 是 Reflex 官方的 deploy platform + MCP server

---

## 🎯 三種用法

1. **Web UI** — https://build.reflex.dev 直接 deploy
2. **CLI** — `reflex deploy` 一行
3. **MCP Server** — agent 透過 MCP 直接 deploy / query

---

## 方式 1：CLI（最簡單）

```bash
# 1. 安裝最新 reflex
pip install --upgrade reflex

# 2. 登入
reflex login
# 開瀏覽器授權

# 3. Deploy
reflex deploy
# 自動偵測專案 + 上傳 + 部署 + 給你 URL
```

**輸出**：
```
✓ Built image
✓ Pushed to registry
✓ Deploying to build.reflex.dev...
✓ Live at: https://my-app.reflex.run
```

---

## 方式 2：Web UI

1. 開 https://build.reflex.dev
2. 連 GitHub repo
3. 選 branch + env vars
4. Deploy

---

## 方式 3：MCP Server（給 AI agent 用）

### Claude Code 啟用

```bash
claude mcp add --transport http reflex https://build.reflex.dev/mcp
```

### Claude Desktop 設定

`~/.config/claude/claude_desktop_config.json`：
```json
{
  "mcpServers": {
    "reflex": {
      "transport": "http",
      "url": "https://build.reflex.dev/mcp"
    }
  }
}
```

### OpenClaw 啟用

`~/.openclaw/config/openclaw.json`（示意）：
```json
{
  "mcp": {
    "servers": {
      "reflex": {
        "transport": "http",
        "url": "https://build.reflex.dev/mcp"
      }
    }
  }
}
```

### 透過 MCP 部署

> ⚠️ **注意**：MCP server 的功能還在演進，**並非所有 agent 都已整合**。可用的話，prompt 範例：

```
Use the reflex MCP server to deploy my current directory to build.reflex.dev
```

```
Show me the status of my reflex deploys via the reflex MCP
```

```
List my reflex projects on build.reflex.dev
```

### MCP 工具（推測，實際以 server 回應為準）

- `deploy(project_path)` — 部署專案
- `list_deploys()` — 列出所有 deploy
- `get_status(deploy_id)` — 查部署狀態
- `get_logs(deploy_id)` — 拿 log
- `set_env(deploy_id, key, value)` — 設環境變數
- `rollback(deploy_id, to_version)` — 回滾

---

## 環境變數管理

### CLI

```bash
reflex env set DB_URL=postgresql://...
reflex env list
```

### Web UI

Deployments → Settings → Environment Variables

---

## Custom Domain

1. Deployments → Settings → Domains
2. Add custom domain: `app.example.com`
3. 設 DNS CNAME：`app.example.com → my-app.reflex.run`
4. 自動 HTTPS（Let's Encrypt）

---

## 價格（截至 2026-07）

> ⚠️ **價格不透明** — 請上官網查最新

- **Free tier**：個人 / 小型 app
- **Pro tier**：更多 resource + custom domain
- **Team tier**：協作 + SSO

---

## 為什麼選 build.reflex.dev？

**優點**：
- ✅ 官方原生支援，0 配置
- ✅ 自動 compile + deploy
- ✅ 自動 HTTPS
- ✅ 整合 MCP（未來 agent-first deploy）
- ✅ 跟 Reflex 框架同步更新

**缺點**：
- ❌ 較新，社群案例少
- ❌ 價格不透明
- ❌ Vendor lock-in（雖然 source 是你的）

---

## fallback：不用 build.reflex.dev 也能 deploy

本 sub-skill 提供的 8 個其他平台（見 [platforms.md](./platforms.md)）：
- Fly.io / Railway / Render / DigitalOcean / AWS / GCP / 自架 k8s / 自架 VM

**選擇策略**：
- 想用官方體驗 → build.reflex.dev
- 企業 / on-premise / 成本敏感 → 自架
- 個人 side project → Fly.io $1.94/月

---

## 🔗 延伸

- [platforms.md](./platforms.md) — 8 平台比較
- [docker.md](./docker.md) — Dockerfile（自架用）
- [self-hosted.md](./self-hosted.md) — 自架細節
