---
name: reflex-deployment
description: >
  Reflex app 部署到 production：Vercel / Fly.io / Railway / Render / DigitalOcean / AWS / GCP / 自架 k8s + Docker + build.reflex.dev MCP 整合。
  Use when deploy Reflex app 到 production、選 deploy 平台、寫 Dockerfile、設 CI/CD。
  Load when user asks "deploy", "production", "hosting", "Docker", "k8s",
  or mentions specific platform names.
---

# Reflex Deployment

> Production 部署全攻略 — 官方 `reflex-process-management` 只管 dev，這個管 prod

---

## 🎯 何時用

- ✅ Deploy Reflex app 到任何 production 平台
- ✅ 寫 Dockerfile / docker-compose
- ✅ 設 CI/CD（GitHub Actions / GitLab CI）
- ✅ 比較 8 個 deploy 平台（價格 / 難度 / features）
- ✅ 整合 [build.reflex.dev](https://build.reflex.dev) 官方 MCP server

❌ **不適用於**：
- 本地 dev server（用官方 `reflex-process-management`）
- 純架構問題（用 `reflex-docs-advanced`）

---

## 📚 References

| Topic | URL |
|-------|-----|
| 8 Platforms Comparison | [references/platforms.md](./references/platforms.md) |
| Docker (單容器 + compose) | [references/docker.md](./references/docker.md) |
| Self-hosted / k8s | [references/self-hosted.md](./references/self-hosted.md) |
| build.reflex.dev MCP | [references/build-reflex-dev.md](./references/build-reflex-dev.md) |
| CI/CD Templates | [assets/ci-templates/](./assets/ci-templates/) |

---

## 🚀 8 個 Deploy 平台速查

| 平台 | 難度 | 價格/月 | 適合 | 自動 HTTPS |
|------|------|--------|------|-----------|
| **build.reflex.dev** | ⭐ | Free tier + pay | Reflex 原生 | ✅ |
| **Fly.io** | ⭐⭐ | $0-5 起步 | 中小型 + edge | ✅ |
| **Railway** | ⭐ | $5 起步 | 快速 deploy | ✅ |
| **Render** | ⭐ | $0-7 起步 | 簡單 web service | ✅ |
| **Vercel** | ⭐⭐ | Free tier | Frontend 重 | ✅ |
| **DigitalOcean App** | ⭐⭐ | $5 起步 | 中型 + DB | ✅ |
| **AWS ECS/Fargate** | ⭐⭐⭐⭐ | $15+ | 企業 / scale | 自己設 |
| **GCP Cloud Run** | ⭐⭐⭐ | Free tier | Serverless | ✅ |
| **自架 k8s** | ⭐⭐⭐⭐⭐ | 自管 | 完全控制 | 自己設 |

詳細比較：[references/platforms.md](./references/platforms.md)

---

## ⚡ 3 步快速部署（Fly.io 範例）

### 1. 安裝 Fly CLI + 登入

```bash
brew install flyctl  # macOS
fly auth signup
```

### 2. 初始化 + 部署

```bash
cd my-reflex-app/
fly launch  # 自動偵測 + 建立 fly.toml
fly deploy  # 部署
```

### 3. 開瀏覽器

```bash
fly open
```

完整 SOP：[references/platforms.md#flyio](./references/platforms.md)

---

## 🐳 Docker 範例

最小 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["reflex", "run", "--env", "prod", "--backend-port", "8000"]
```

build + run：
```bash
docker build -t my-reflex-app .
docker run -p 8000:8000 my-reflex-app
```

詳細：[references/docker.md](./references/docker.md)

---

## 🤖 build.reflex.dev MCP 整合

`build.reflex.dev` 是 Reflex **官方 deploy platform + MCP server**。

**啟用 MCP（Claude Code 範例）**：
```bash
claude mcp add --transport http reflex https://build.reflex.dev/mcp
```

**用 MCP deploy**：
```
> Use the reflex MCP server to deploy my app to build.reflex.dev
```

詳細：[references/build-reflex-dev.md](./references/build-reflex-dev.md)

> ⚠️ **若 agent 環境沒接 MCP，可改用 CLI**：`npx build-reflex deploy` 或 web UI

---

## 🔐 Production Checklist

部署前必檢：

- [ ] `reflex run --env prod` 測過（不是 dev mode）
- [ ] `.env` 機密放到 secret manager（不是 git）
- [ ] DB connection 改成 production URL
- [ ] HTTPS 設定（Let's Encrypt / Cloudflare）
- [ ] Health check endpoint
- [ ] Log aggregation（CloudWatch / Datadog / Sentry）
- [ ] Auto-restart on crash（systemd / k8s / platform 內建）
- [ ] Backup strategy（DB snapshot）

---

## 🔗 與其他 sub-skill 關係

- **官方 `reflex-process-management`** — dev server / compile / reload
- **本 `reflex-docs-advanced`** — architecture（部署前的設計參考）
- **本 `reflex-upgrade-monitor`** — 升級前先確認部署平台相容性
- **本 `reflex-ai-integration`** — AI app 通常需要 streaming-friendly deploy（WebSocket 支援）

---

## 💰 成本估算指南

小型 app（< 1k MAU）：
- **最低**：build.reflex.dev Free tier / Fly.io $0-5
- **推薦**：Railway $5 一鍵搞定

中型 app（1k-100k MAU）：
- **最低**：Fly.io $20-50（多 region）
- **推薦**：DigitalOcean App $12-25 + managed Postgres

大型 app（> 100k MAU）：
- AWS / GCP / k8s 自架
- 建議先做 load testing
