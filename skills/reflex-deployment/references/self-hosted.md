# Self-Hosted — k8s / Bare Metal / systemd

> 自架 Reflex app — 完全控制

---

## 🎯 何時用

- 完全控制需求（on-premise / 內網）
- 法規限制（資料不能出公司）
- 已有 k8s / VM infra
- 成本敏感（自架可能比 managed 便宜）

---

## 方案 A：systemd（單一 VM）

最適合：小型自架、單機、開發用

### Setup

`/etc/systemd/system/reflex.service`：
```ini
[Unit]
Description=Reflex App
After=network.target postgresql.service

[Service]
Type=simple
User=reflex
Group=reflex
WorkingDirectory=/opt/reflex-app
Environment="PATH=/opt/reflex-app/.venv/bin"
Environment="DB_URL=postgresql://reflex:PASSWORD@localhost:5432/reflex"
ExecStart=/opt/reflex-app/.venv/bin/reflex run --env prod --backend-port 8000 --single-port
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# 資源限制
MemoryMax=512M
CPUQuota=200%

# 安全
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/reflex-app/.web /var/log/reflex

[Install]
WantedBy=multi-user.target
```

### 指令

```bash
sudo systemctl daemon-reload
sudo systemctl enable reflex
sudo systemctl start reflex
sudo systemctl status reflex

# 看 log
sudo journalctl -u reflex -f
```

### Reverse proxy（Caddy）

`/etc/caddy/Caddyfile`：
```
reflex.example.com {
    reverse_proxy localhost:8000
    encode gzip zstd
}
```

```bash
sudo systemctl reload caddy
```

---

## 方案 B：Docker Compose on VM

最適合：中型自架、單機多服務

`docker-compose.yml`（見 [docker.md](./docker.md)）：
```yaml
services:
  app:
    image: ghcr.io/your-org/my-reflex-app:latest
    restart: unless-stopped
    # ...

  caddy:
    image: caddy:2
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - app

volumes:
  caddy_data:
  caddy_config:
```

`Caddyfile`：
```
reflex.example.com {
    reverse_proxy app:8000
}
```

---

## 方案 C：k8s 部署

最適合：大型、HA、scale

### Namespace + ConfigMap

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: reflex-app
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: reflex-config
  namespace: reflex-app
data:
  REFLEX_ENV: "prod"
  BACKEND_PORT: "8000"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: reflex-secrets
  namespace: reflex-app
type: Opaque
stringData:
  DB_URL: "postgresql://reflex:password@postgres:5432/reflex"
  MINIMAX_API_KEY: "..."
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reflex
  namespace: reflex-app
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
        image: ghcr.io/your-org/my-reflex-app:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: reflex-config
        - secretRef:
            name: reflex-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Service + Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: reflex
  namespace: reflex-app
spec:
  type: ClusterIP
  selector:
    app: reflex
  ports:
  - port: 80
    targetPort: 8000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: reflex
  namespace: reflex-app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
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

### HPA（自動 scale）

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: reflex
  namespace: reflex-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: reflex
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 方案 D：Bare Metal + Reverse Proxy

最適合：on-premise、無雲端

```
[Internet]
  ↓
[Hardware Firewall]
  ↓
[Nginx / Caddy] (port 80/443)
  ↓
[Reflex App VM] (port 8000)
  ↓
[Postgres VM] (port 5432, internal only)
```

### 監控

```bash
# 系統監控
htop
iostat -x 1
vmstat 1
netstat -tulnp

# App 監控
journalctl -u reflex -f
```

### 自動更新 SOP

```bash
# 1. pull 新 image
docker pull ghcr.io/your-org/my-reflex-app:latest

# 2. 重啟
docker compose up -d

# 3. 確認 health
curl http://localhost:8000/api/health
```

---

## 🔒 安全性 checklist

- [ ] HTTPS（Let's Encrypt / Cloudflare）
- [ ] Firewall 只開 80/443/22
- [ ] SSH key only（關密碼登入）
- [ ] fail2ban
- [ ] 自動 security update
- [ ] DB 密碼用 secret manager
- [ ] API key 用 secret manager
- [ ] Rate limiting（Nginx / Cloudflare）
- [ ] Log aggregation（避免 log 寫滿 disk）
- [ ] Backup 策略（DB + config）

---

## 📊 規模決策

| MAU | 推薦 |
|-----|------|
| < 1k | systemd + 單一 VM（$5/月 VPS） |
| 1k-10k | Docker Compose + 單一 VM（$10-20/月）|
| 10k-100k | k8s（managed 或自架，$50-200/月）|
| > 100k | k8s + 多 region + CDN |

---

## 🔗 延伸

- [docker.md](./docker.md) — Dockerfile + Compose
- [platforms.md](./platforms.md) — 8 平台比較
- [ci-cd.md](./ci-cd.md) — 自動化 build / deploy
