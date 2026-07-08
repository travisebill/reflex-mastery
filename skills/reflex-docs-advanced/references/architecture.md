# Reflex Architecture & Compile Flow

> 深入了解 Reflex 內部運作 — 寫進階 app 的基礎

Reflex 是**純 Python 全端 web framework**。表面上寫 Python，底層編譯成 React + FastAPI。

---

## 🏛 高層架構

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React SPA (從 .web/ 資料夾 serve)                      │  │
│  │  - rx.Component 編譯成 React                           │  │
│  │  - WebSocket 連到 backend                              │  │
│  │  - State mirror (reactive display)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ WebSocket + HTTP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI + Reflex runtime)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  rx.App                                               │  │
│  │  ├─ Pages (rx.page 修飾函數)                          │  │
│  │  ├─ State (rx.State subclasses, server-side)          │  │
│  │  └─ Event Handlers (@rx.event 修飾 methods)          │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SQLModel / Database                                  │  │
│  │  Authentication (AuthState)                           │  │
│  │  Custom FastAPI routes (api router)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Compile 流程

`reflex run` 時的內部流程：

```
1. reflex run
   ↓
2. 讀 rxconfig.py + 所有 .py 檔
   ↓
3. Scan rx.State subclasses → 註冊到 server
   ↓
4. Scan @rx.event methods → 註冊 event endpoints
   ↓
5. Scan @rx.page 修飾函數 → 產生 routes
   ↓
6. Compile .web/ 資料夾：
   - Python components → React components
   - Vars → reactive bindings
   - Theme → Tailwind config
   - Assets → static files
   ↓
7. Start FastAPI server (port 8000 預設)
   + Start Next.js dev server (port 3000 預設, --single-port 整合到 8000)
   ↓
8. Browser 載入 → WebSocket 連到 backend
   → State 同步建立 mirror
```

**驗證編譯**（不啟動 server）：
```bash
reflex compile --dry
# 檢查 syntax / import / component 問題，但不實際 build
```

**正式編譯**（產生 production assets）：
```bash
reflex compile
# 產出 .web/ 資料夾（可部署）
```

---

## 🌉 Frontend ↔ Backend 邊界

### State 在 server（**這是 Reflex 最反直覺的部分**）

```python
# 全部 state 都跑在 BACKEND
class State(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count += 1
```

瀏覽器**不會**直接存 `count`。它只存 **mirror**（用 WebSocket sync 的複本）。

### Event handler 在 backend

```python
@rx.event
def complex_compute(self):
    # 這裡跑在 server
    import pandas as pd  # server-only lib
    df = pd.DataFrame(...)
    return df.head().to_dict()
```

前端只是觸發器 → backend 執行 → 結果 sync 回前端。

### Component 是 declarative

```python
def page() -> rx.Component:
    return rx.vstack(
        rx.text(State.count),       # 自動 reactive
        rx.button("+", on_click=State.increment),
    )
```

`State.count` 變了 → 前端自動 re-render 對應 component。

### 變數分兩類

- **Base var**：state 屬性（client 可讀、server 可寫）
- **Computed var**：`@rx.var` 修飾的方法（依賴其他 var）

```python
class State(rx.State):
    first_name: str = ""
    last_name: str = ""

    @rx.var
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

`first_name` 變了 → `full_name` 自動更新。

---

## 🔌 內建子系統

### 1. Routing

```python
import reflex as rx

class State(rx.State):
    pass

@rx.page(route="/", title="Home")
def home() -> rx.Component:
    return rx.text("Home")

@rx.page(route="/about")
def about() -> rx.Component:
    return rx.text("About")

app = rx.App()
```

或動態加：
```python
app.add_page(home, route="/")
app.add_page(about, route="/about")
```

動態路由：
```python
@rx.page(route="/posts/[slug]")
def post() -> rx.Component:
    return rx.text(rx.State.router.page.params.get("slug", "default"))
```

### 2. State Persistence

```python
import pickle, base64

class PersistentState(rx.State):
    data: str = ""  # base64-encoded pickle

    @rx.event
    def save(self, value):
        self.data = base64.b64encode(pickle.dumps(value)).decode()

    @rx.event
    def load(self):
        return pickle.loads(base64.b64decode(self.data))
```

或用 `rx.ClientStorage`（client-side cookie + localStorage）。

### 3. API Routes（FastAPI-style）

```python
app = rx.App()

@app.api_route("/api/health", methods=["GET"])
async def health():
    return {"status": "ok"}
```

可在 `http://localhost:8000/api/health` 直接呼叫（繞過 WebSocket）。

### 4. Background Tasks

```python
import asyncio

class State(rx.State):
    progress: int = 0

    async def long_task(self):
        for i in range(100):
            await asyncio.sleep(0.1)
            self.progress = i
            yield
```

---

## ⚙️ rxconfig.py 設定

```python
import reflex as rx

config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",           # SQLAlchemy URL
    enable_bun=False,                       # JS bundler (預設 False = 用 Next.js)
    backend_port=8000,
    frontend_port=3000,
    env=rx.Env.DEV,                         # 或 rx.Env.PROD
    cors_allowed_origins=["*"],
    loglevel="info",
    tailwind={                              # Tailwind 設定（如果有 enable_bun=False）
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#3B82F6",
                }
            }
        }
    },
)
```

---

## 🧪 Debugging

### 1. 啟用 log

```python
config = rx.Config(loglevel="debug")
```

### 2. 看 backend log

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3. compile error

```bash
reflex compile --dry
# 顯示詳細 error
```

### 4. WebSocket 問題

開瀏覽器 DevTools → Network → WS → 看 messages。

---

## 🚦 為什麼這設計？

Reflex 的設計哲學：

1. **Server-side state** — 保護商業邏輯、不要前端被破解
2. **Reactive by default** — Var 變了就 re-render，不用手動訂閱
3. **Single language** — Python 全棧，不用 JS
4. **Progressive enhancement** — 簡單 app 用 state 就好，複雜用 API route + FastAPI

**取捨**：
- ✅ 開發快、安全
- ❌ 每個 interaction 都過 WebSocket（有 latency）
- ❌ 大 state 效能下降（mirror 整個同步）

> 想 scale → 參考 [scaling.md](./scaling.md)

---

## 📚 延伸閱讀

- [patterns.md](./patterns.md) — 常用 pattern 集
- [pitfalls.md](./pitfalls.md) — 踩坑大全
- [scaling.md](./scaling.md) — State 規模化策略
