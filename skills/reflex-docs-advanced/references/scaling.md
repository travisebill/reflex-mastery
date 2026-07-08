# Scaling State — 規模化策略

> 1000+ vars 怎麼處理？大資料怎麼 sync？延遲怎麼降？

---

## 📊 規模問題的真相

Reflex 的設計是 **server-side state + WebSocket mirror**。每個 state var 變更會：
1. Server 更新
2. WebSocket 推 mirror 給 frontend
3. Frontend re-render 受影響 component

**100 個 var → 沒事**
**1000 個 var → 開始慢**
**10000 個 var → 卡到不行**

---

## 🎯 策略 1：只放必要的 state

```python
# ❌ 不要這樣
class State(rx.State):
    all_users: list[User] = []  # 1萬筆全放 state

# ✅ 只放當前頁
class State(rx.State):
    users_page: list[User] = []  # 20 筆
    page: int = 0
    total: int = 0
    search_query: str = ""

    @rx.event
    async def load_page(self):
        result = await api.get_users(
            page=self.page,
            limit=20,
            search=self.search_query,
        )
        self.users_page = result.items
        self.total = result.total
```

---

## 🎯 策略 2：分頁 + virtual scroll

對 1000+ items 表格，用分頁或 virtual scroll：

```python
class TableState(rx.State):
    items: list[dict] = []
    visible_start: int = 0
    visible_end: int = 50  # 只 render 50 個

    @rx.var
    def visible_items(self) -> list[dict]:
        return self.items[self.visible_start:self.visible_end]
```

UI 用 virtual scroll component（自製或第三方程式庫）。

---

## 🎯 策略 3：Computed Var 緩存

Reflex 預設會緩存 computed var（如果依賴沒變），但複雜計算仍會 re-run。

```python
class State(rx.State):
    raw_data: list[float] = []

    # ❌ 沒緩存 — raw_data 變了又算一次
    @rx.var
    def statistics(self) -> dict:
        return {
            "mean": sum(self.raw_data) / len(self.raw_data),
            "std": ...,
        }

    # ✅ 緩存策略：拆解依賴
    @rx.var
    def mean(self) -> float:
        return sum(self.raw_data) / len(self.raw_data) if self.raw_data else 0

    @rx.var
    def std(self) -> float:
        # 只依賴 raw_data，獨立緩存
        ...
```

---

## 🎯 策略 4：批次更新

不要每個 var 改一次 yield 一次，改成**批次**：

```python
# ❌ 慢 — 100 個 yield
@rx.event
async def load_all(self):
    for i in range(100):
        self.items.append(...)  # 每次 yield 觸發 re-render
        yield

# ✅ 快 — 一次設完
@rx.event
async def load_all(self):
    new_items = []
    for i in range(100):
        new_items.append(...)
    self.items = new_items  # 一次更新
```

---

## 🎯 策略 5：debounce 輸入

連續輸入（搜尋框）會觸發很多 event，要 debounce：

```python
class State(rx.State):
    search_query: str = ""
    results: list = []
    _debounce_task: str = ""

    @rx.event
    async def on_search_change(self, value: str):
        self.search_query = value

        # 取消上次的 debounce
        if self._debounce_task:
            # ... cancel logic

        # 等 300ms 才搜
        import asyncio
        await asyncio.sleep(0.3)

        if self.search_query == value:  # 確保沒被覆寫
            self.results = await api.search(value)
```

或用 JS 端 debounce（前端 on_change 已經 debounce 過了）。

---

## 🎯 策略 6：WebSocket 訊息壓縮

如果 state 大量更新，可以壓縮 diff：

```python
# Reflex 內部已有 diff 算法，正常不需要改
# 但如果你發現 WebSocket 訊息大：
# 1. 確認沒有多餘 var
# 2. 用 rx.session 共享 state
# 3. 開 Pro plan 升級 backend resource
```

---

## 🎯 策略 7：拆 State Instance

對**不同 user / tenant** 的獨立 state：

```python
# 多租戶範例
class TenantState(rx.State):
    tenant_id: str = ""

# 每個連線有獨立 state instance（Reflex 自動）
# 不用手動管理，但要知道 memory cost = users × state size
```

---

## 🎯 策略 8：Server-side 計算 + 只傳結果

```python
class State(rx.State):
    # ❌ client 算 — 1萬筆資料 sync 過去
    raw_records: list[dict] = []

    @rx.var
    def aggregated(self) -> dict:
        # 在 server 算，只傳結果
        ...

    # ✅ 只傳結果
    aggregated_chart_data: dict = {}

    @rx.event
    async def load_chart(self):
        # server 聚合 → 只傳最終資料
        data = await aggregate_api.get(self.filter)
        self.aggregated_chart_data = data
```

---

## 🎯 策略 9：Streaming 替代 State

對於「即時資料流」（log、chat），用 **WebSocket streaming endpoint** 而非 state：

```python
# ❌ 錯 — 所有 log 都放 state
class State(rx.State):
    logs: list[str] = []

    @rx.event
    async def stream_logs(self):
        async for log in log_stream():
            self.logs.append(log)
            yield

# ✅ 對 — 用 FastAPI WebSocket endpoint 推送
@app.web_socket("/ws/logs")
async def logs_ws(ws):
    async for log in log_stream():
        await ws.send(log)
```

UI 用 `rx.connection` 接 custom WebSocket。

---

## 📐 規模決策樹

```
data size?
├─ < 100 items
│  └─ 直接放 state ✅
├─ 100-1000 items
│  └─ 分頁（page + per_page）
├─ 1000-10000 items
│  ├─ server-side aggregate + 只傳結果
│  └─ 或 virtual scroll + 延遲載入
└─ > 10000 items
   ├─ 必用 server-side aggregation
   ├─ 用 FastAPI endpoint + custom WebSocket
   └─ 或外接 search engine（Elasticsearch / Algolia）
```

---

## 🧪 測量效能

```python
# 開 debug log
config = rx.Config(loglevel="debug")

# 看 WebSocket 訊息大小
# 開瀏覽器 DevTools → Network → WS → 看每個 frame 大小
```

**健康指標**：
- 每個 WebSocket frame < 1KB
- Re-render 時間 < 50ms
- State vars < 100 per page

---

## 📚 延伸

- [architecture.md](./architecture.md) — 為什麼 state 在 server
- [patterns.md](./patterns.md) — 常見 pattern
- [pitfalls.md](./pitfalls.md) — 踩坑大全
