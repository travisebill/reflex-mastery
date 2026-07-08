# 8 Deployment Platforms — 詳細比較

> Reflex app 部署到 8 個主流平台的詳細比較 + SOP

---

## 速查總表

| 平台 | 難度 | 價格/月（USD） | 最適合 | 自動 HTTPS | WebSocket | 自動 sleep |
|------|------|---------------|--------|-----------|-----------|-----------|
| **build.reflex.dev** | ⭐ | Free / pay-as-you-go | Reflex 原生 | ✅ | ✅ | ❌ |
| **Fly.io** | ⭐⭐ | $0-5 起步 | 中小型 + edge | ✅ | ✅ | ❌ |
| **Railway** | ⭐ | $5 起步 | 快速 deploy | ✅ | ✅ | ❌ |
| **Render** | ⭐ | $0-7 起步 | 簡單 web | ✅ | ✅ | ✅（free tier）|
| **Vercel** | ⭐⭐ | Free tier | Frontend 重 | ✅ | ⚠️ | ✅ |
| **DigitalOcean App** | ⭐⭐ | $5 起步 | 中型 + managed DB | ✅ | ✅ | ❌ |
| **AWS ECS/Fargate** | ⭐⭐⭐⭐ | $15+ | 企業 / scale | 自己設 | ✅ | ❌ |
| **GCP Cloud Run** | ⭐⭐⭐ | Free tier | Serverless | ✅ | ✅ | ✅ |
| **自架 k8s** | ⭐⭐⭐⭐⭐ | 自管 | 完全控制 | 自己設 | ✅ | ❌ |

> ⚠️ **Reflex 是 WebSocket-heavy app**，確認平台支援 long-lived WebSocket connection。
> Vercel / Render free tier 有限制，**生產環境用付費**。

---

## 1️⃣ build.reflex.dev（官方，推薦）

**優點**：
- Reflex 官方平台，原生支援
- 0 配置 deploy：`reflex deploy` 一行搞定
- 自動 HTTPS + 自動 scale
- 整合 MCP server（[見 build-reflex-dev.md](./build-reflex-dev.md)）

**缺點**：
- 較新，社群案例少
- 價格不透明

**SOP**：
```bash
reflex login
reflex deploy
# 完成！URL 會印出來
```

**完整文檔**：[references/build-reflex-dev.md](./build-reflex-dev.md)

---

## 2️⃣ Fly.io

**優點**：
- 多 region edge deploy
- Free tier 慷慨（3 shared VMs）
- Dockerfile 直接 deploy
- 支援 persistent volume

**缺點**：
- 學習曲線中等
- 計費按秒，複雜

**SOP**：
```bash
brew install flyctl
fly auth signup
cd my-reflex-app/
fly launch  # 自動偵測 Dockerfile
fly deploy
fly open
```

**fly.toml**（自動產生）：
```toml
app = "my-reflex-app"
primary_region = "nrt"  # Tokyo

[build]
  dockerfile = "Dockerfile"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

**價格**：$0-5 起步（256MB RAM = $1.94/月）

---

## 3️⃣ Railway

**優點**：
- 0 配置 GitHub deploy
- 一鍵 Postgres / Redis add-on
- 5 分鐘 deploy

**缺點**：
- Free tier 已取消（最低 $5）
- 計費複雜

**SOP**：
1. 連 GitHub repo → https://railway.app/new
2. 選 "Deploy from GitHub repo"
3. Railway 自動偵測 Dockerfile / requirements.txt
4. 加 Postgres plugin
5. 設 env var: `DB_URL=postgresql://...`
6. Deploy

---

## 4️⃣ Render

**優點**：
- Free tier（會 sleep）
- 簡單 YAML 設定
- 內建 managed Postgres

**缺點**：
- Free tier 15 min idle 會 sleep（cold start）
- WebSocket 在 free tier 有 5 min timeout

**SOP（`render.yaml`）**：
```yaml
services:
  - type: web
    name: my-reflex-app
    env: docker
    plan: starter
    healthCheckPath: /api/health
    envVars:
      - key: DB_URL
        fromDatabase:
          name: my-db
          property: connectionString

databases:
  - name: my-db
    plan: starter
```

---

## 5️⃣ Vercel

**優點**：
- Free tier 慷慨
- 自動 CDN
- GitHub auto-deploy

**缺點**：
- ❌ Serverless function timeout 10s（Reflex 啟動慢會超時）
- ❌ WebSocket 不適合 serverless
- 不推薦用於 Reflex（適合純前端 static site）

**結論**：⚠️ **不推薦 Reflex 用 Vercel**（除非架構分拆：frontend static + backend 他處）

---

## 6️⃣ DigitalOcean App Platform

**優點**：
- 簡單 + 直觀 UI
- $5 起跳
- 內建 managed Postgres / Redis
- 自動 HTTPS

**缺點**：
- 沒 edge network（只有固定 region）

**SOP**：
1. App Platform → Create App → GitHub
2. 選 repo + branch
3. Type: Web Service
4. Dockerfile detected
5. Plan: Basic ($5/mo)
6. 加 Database component（managed Postgres $15/mo）
7. Deploy

---

## 7️⃣ AWS ECS / Fargate

**優點**：
- 企業級 scale
- 整合 AWS 全棧（RDS / S3 / CloudFront / ALB）
- 99.99% SLA

**缺點**：
- 設定複雜
- $15+ 起步
- 需要懂 AWS

**最小部署（Terraform）**：
```hcl
resource "aws_ecs_service" "reflex" {
  name            = "reflex"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.reflex.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets = aws_subnet.public.*.id
    security_groups = [aws_security_group.reflex.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.reflex.arn
    container_name   = "reflex"
    container_port   = 8000
  }
}
```

**不推薦個人 / 小型 app**，推薦企業 / 已有 AWS infra。

---

## 8️⃣ GCP Cloud Run

**優點**：
- Serverless（按用量計費）
- Free tier 2M requests/月
- 自動 scale to 0
- HTTPS 自動

**缺點**：
- Cold start（首次 request 慢）
- WebSocket 支援有限（用 session affinity）

**SOP**：
```bash
gcloud run deploy my-reflex-app \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --port 8000
```

---

## 9️⃣ 自架 k8s

**何時用**：
- 完全控制需求
- 多 region 部署
- 已有 k8s 經驗

**最小 manifest**：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reflex
spec:
  replicas: 3
  selector:
    matchLabels:
      app: reflex
  template:
    metadata:
      labels:
        app: reflex
    spec:
      containers:
      - name: reflex
        image: my-registry/reflex:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_URL
          valueFrom:
            secretKeyRef:
              name: reflex-secrets
              key: db-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: reflex
spec:
  type: LoadBalancer
  selector:
    app: reflex
  ports:
  - port: 80
    targetPort: 8000
```

**ingress**（HTTPS termination）：
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: reflex
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - reflex.example.com
    secretName: reflex-tls
  rules:
  - host: reflex.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: reflex
            port:
              number: 80
```

---

## 🎯 選哪個？

| 你的需求 | 推薦 |
|---------|------|
| 第一次 deploy / 個人 app | **Fly.io** 或 **Railway** |
| 企業 / 已有 AWS | **AWS ECS** |
| 純 serverless / 流量不固定 | **GCP Cloud Run** |
| 完全控制 | **自架 k8s** |
| 想用官方原生體驗 | **build.reflex.dev** |

---

## 💰 成本估算（小 app, < 10k MAU）

| 平台 | 月成本 |
|------|--------|
| Fly.io | $0-5 |
| Railway | $5-10 |
| Render | $0-7 |
| DigitalOcean App | $5-12 |
| GCP Cloud Run | $0-5 |
| AWS ECS | $15-30 |
| 自架 k8s（1 node）| $30+ |
| build.reflex.dev | Free tier / pay-as-you-go |

**最小可行**：Fly.io $1.94/月 + managed Postgres $4/月 = **$6/月** 搞定

---

## 🔗 延伸

- [docker.md](./docker.md) — Dockerfile 撰寫
- [self-hosted.md](./self-hosted.md) — 自架細節
- [build-reflex-dev.md](./build-reflex-dev.md) — 官方 MCP
- [ci-cd.md](./ci-cd.md) — CI/CD
