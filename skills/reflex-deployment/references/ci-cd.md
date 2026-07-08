# CI/CD — 自動化 Build / Test / Deploy

> GitHub Actions / GitLab CI 範本

---

## GitHub Actions 完整版

`.github/workflows/deploy.yml`：

```yaml
name: Deploy Reflex App

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: reflex
          POSTGRES_PASSWORD: reflex
          POSTGRES_DB: reflex_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: |
          uv run ruff check .
          uv run mypy .

      - name: Test
        env:
          DB_URL: postgresql://reflex:reflex@localhost:5432/reflex_test
        run: |
          uv run pytest -v --cov=. --cov-report=xml

      - name: Upload coverage
        if: always()
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,format=short
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to Fly.io (staging)
        uses: superfly/flyctl-actions/setup-flyctl@master
        with:
          version: latest

      - name: Deploy
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN_STAGING }}
        run: |
          flyctl deploy --app my-reflex-staging --image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}

      - name: Smoke test
        run: |
          sleep 30  # 等待 app 啟動
          curl -f https://my-reflex-staging.fly.dev/api/health || exit 1

  deploy-prod:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://my-reflex-app.example.com
    steps:
      - name: Deploy to Fly.io (prod)
        uses: superfly/flyctl-actions/setup-flyctl@master
        with:
          version: latest

      - name: Deploy
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN_PROD }}
        run: |
          flyctl deploy --app my-reflex-app --image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: "Deployed ${{ github.sha }} to production"
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 簡化版（只 build + push）

`.github/workflows/build.yml`：

```yaml
name: Build & Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

---

## GitLab CI

`.gitlab-ci.yml`：

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

test:
  stage: test
  image: python:3.11
  services:
    - postgres:16
  variables:
    POSTGRES_USER: reflex
    POSTGRES_PASSWORD: reflex
    POSTGRES_DB: reflex_test
  before_script:
    - pip install uv
    - uv sync
  script:
    - uv run ruff check .
    - uv run mypy .
    - uv run pytest -v
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

deploy-staging:
  stage: deploy
  script:
    - apt-get update && apt-get install -y curl
    - curl -X POST $WEBHOOK_STAGING -d "{\"image\":\"$DOCKER_IMAGE\"}"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main
```

---

## Pre-commit Hooks

`.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [reflex, types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key
```

**安裝**：
```bash
pip install pre-commit
pre-commit install
```

---

## Deploy 策略

### Blue-Green

兩個環境切換，零 downtime：
```bash
# deploy 新版到 green
flyctl deploy --app my-reflex-app-green

# smoke test
curl -f https://my-reflex-app-green.fly.dev/api/health

# 切換 traffic
flyctl releases rollback my-reflex-app  # 或用 LB 切換
```

### Canary

5% → 25% → 50% → 100%：
- AWS CodeDeploy：原生 canary
- GCP Cloud Run：traffic splitting
- Fly.io：weights

### Rolling Update（k8s 預設）

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

---

## 通知整合

### Slack

```yaml
- name: Notify
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: |
      ${{ github.workflow }} - ${{ job.status }}
      Commit: ${{ github.sha }}
      Author: ${{ github.actor }}
```

### Discord

```yaml
- name: Notify Discord
  if: always()
  uses: sarisia/actions-status-discord@v1
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    title: "Deploy ${{ job.status }}"
    description: "Commit: ${{ github.sha }}"
```

### Telegram

```bash
curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
  -d "chat_id=$CHAT_ID" \
  -d "text=✅ Deploy success: $GITHUB_SHA"
```

---

## 🔗 延伸

- [platforms.md](./platforms.md) — 8 平台
- [docker.md](./docker.md) — Dockerfile
- [self-hosted.md](./self-hosted.md) — 自架
- [build-reflex-dev.md](./build-reflex-dev.md) — 官方 deploy
