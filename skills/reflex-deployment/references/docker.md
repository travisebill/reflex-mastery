# Docker — Dockerfile + Compose

> Reflex app 的 Docker 容器化 + 多服務 compose

---

## 最小 Dockerfile

```dockerfile
FROM python:3.11-slim

# 系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 建立 app user
RUN useradd -m -u 1000 app
WORKDIR /app

# 先裝 Python deps（用 cache layer）
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 複製 source
COPY --chown=app:app . .

USER app

# Reflex 預設 port 8000 (backend) / 3000 (frontend)
EXPOSE 8000

# Production 模式
ENV REFLEX_ENV=prod
ENV BACKEND_PORT=8000

CMD ["reflex", "run", "--env", "prod", "--backend-port", "8000", "--single-port"]
```

**build + run**：
```bash
docker build -t my-reflex-app .
docker run -p 8000:8000 my-reflex-app
```

---

## 進階 Dockerfile（多階段 build）

```dockerfile
# === Stage 1: builder ===
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === Stage 2: runtime ===
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 app

WORKDIR /app
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .

USER app
ENV PATH=/home/app/.local/bin:$PATH

EXPOSE 8000
ENV REFLEX_ENV=prod
ENV BACKEND_PORT=8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["reflex", "run", "--env", "prod", "--backend-port", "8000", "--single-port"]
```

**Size 差異**：
- 簡單版：~800MB
- 多階段：~500MB

---

## docker-compose（含 Postgres + Redis）

```yaml
version: "3.9"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_URL: postgresql://reflex:reflex@db:5432/reflex
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 30s

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: reflex
      POSTGRES_PASSWORD: reflex
      POSTGRES_DB: reflex
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U reflex"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
  redisdata:
```

**啟動**：
```bash
docker compose up -d
docker compose logs -f app
```

---

## .dockerignore

```
# Git
.git
.gitignore
.github

# Python
__pycache__
*.py[cod]
.pytest_cache
.mypy_cache
.ruff_cache
.venv
venv

# Node
node_modules

# IDE
.vscode
.idea

# Reflex
.web
.reflex

# Docs
docs/
*.md
!README.md
LICENSE

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.*
!.env.example
```

---

## Registry 推送

### Docker Hub

```bash
docker tag my-reflex-app:latest docker.io/YOUR_USERNAME/my-reflex-app:latest
docker push docker.io/YOUR_USERNAME/my-reflex-app:latest
```

### GitHub Container Registry（推薦）

```bash
# 登入
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 標記 + push
docker tag my-reflex-app:latest ghcr.io/YOUR_USERNAME/my-reflex-app:latest
docker push ghcr.io/YOUR_USERNAME/my-reflex-app:latest
```

---

## 環境變數管理

**方式 1：`.env` file**（不進 git）
```bash
DB_URL=postgresql://...
SECRET_KEY=...
MINIMAX_API_KEY=...
```

**方式 2：Docker secrets**（production）
```bash
echo "my-secret" | docker secret create db_password -
```

**方式 3：平台 secret manager**
- Fly.io：`fly secrets set DB_URL=...`
- Railway：UI 或 `railway variables set DB_URL=...`

---

## 疑難排解

### 1. Container 啟動慢

`reflex run` 第一次要 compile，可能要 30-60s。

**修法**：在 entrypoint 加 warmup：
```bash
#!/bin/bash
# entrypoint.sh
reflex compile  # 預先 compile
exec reflex run --env prod
```

### 2. Memory 不足

```bash
docker run -p 8000:8000 -m 512m my-reflex-app
```

或在 compose：
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
```

### 3. 靜態檔案 404

確保 `assets/` 資料夾在 image 裡：
```dockerfile
COPY --chown=app:app assets/ assets/
```

### 4. WebSocket 連不上

確認 platform 沒擋 WebSocket upgrade：
- Vercel ❌
- Netlify ❌
- Cloud Run ⚠️（要 session affinity）
- Fly.io / Railway / Render / DigitalOcean / ECS / k8s ✅

---

## 🔗 延伸

- [platforms.md](./platforms.md) — 8 平台比較
- [self-hosted.md](./self-hosted.md) — 自架 / bare metal
- [ci-cd.md](./ci-cd.md) — CI/CD 自動化 build
