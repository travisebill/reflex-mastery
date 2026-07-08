# Reflex Pitfalls — 踩坑大全

> Reflex 寫 code 常見的 15 個陷阱 + 解法

---

## ⚠️ 1. State mutation 沒生效

**症狀**：改了 var 但 UI 沒更新。

**原因**：沒用 `@rx.event` 修飾 / 直接改 var 沒反應。

```python
# ❌ 錯 — 沒 @rx.event
class State(rx.State):
    count: int = 0

def on_click():
    State.count = State.count + 1  # 不會生效

# ✅ 對 — 用 @rx.event
class State(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count = self.count + 1
```

---

## ⚠️ 2. Async deadlock（event handler 卡住）

**症狀**：event handler 跑了但 UI 永遠 loading。

**原因**：用 `await` 卻沒宣告 `async def`。

```python
# ❌ 錯
@rx.event
def fetch(self):
    data = await api.get()  # SyntaxError / 沒反應

# ✅ 對
@rx.event
async def fetch(self):
    data = await api.get()
    self.data = data
```

---

## ⚠️ 3. Computed var 循環依賴

**症狀**：page 載入後 CPU 100%、瀏覽器卡住。

**原因**：A computed var 依賴 B，B 依賴 A。

```python
# ❌ 錯 — infinite loop
class State(rx.State):
    a: int = 1

    @rx.var
    def b(self) -> int:
        return self.a + 1

    @rx.var
    def a(self) -> int:
        return self.b + 1  # 💥
```

**修法**：用 base var 當 source，不要 cycle。

---

## ⚠️ 4. Yield 順序錯亂

**症狀**：多個 yield 後 UI 顯示狀態錯亂。

```python
# ❌ 錯 — yield 順序不對
@rx.event
async def save(self):
    self.loading = True
    yield
    result = await api.save()
    self.data = result
    yield
    self.loading = False
    yield  # 多餘
```

```python
# ✅ 對 — yield 只在需要 update UI 時
@rx.event
async def save(self):
    self.loading = True
    yield  # 立即更新 UI（loading = True）

    result = await api.save()
    self.data = result
    yield  # 立即更新 UI（data = result）

    self.loading = False
    # 不需要 yield，handler 結束會自動 sync 最後狀態
```

---

## ⚠️ 5. State 規模爆炸（re-render 慢）

**症狀**：state 變了 1 個 var，整個 page 重 render，UI 卡。

**原因**：把所有東西都放 state。

```python
# ❌ 錯 — 1000 items 全放 state
class State(rx.State):
    items: list[dict] = [...]  # 1000 items

    @rx.event
    def search(self, query):
        # 改 query → 整個 state re-render → 慢
        self.items = filter(self.items, query)

# ✅ 對 — 分頁 + 只放必要
class State(rx.State):
    items: list[dict] = []  # 當前頁（20 items）
    page: int = 0
    total_count: int = 0

    @rx.event
    async def search(self, query):
        result = await api.search(query, page=self.page)
        self.items = result.items
        self.total_count = result.total
```

詳見 [scaling.md](./scaling.md)

---

## ⚠️ 6. Port conflict

**症狀**：`reflex run` 失敗，error: "Address already in use"。

**修法 1**：改 port
```bash
reflex run --backend-port 8001 --frontend-port 3001
```

**修法 2**：找出佔用 process
```bash
lsof -i :3000 -sTCP:LISTEN -t | xargs kill -9
```

---

## ⚠️ 7. WebSocket 連線斷掉（mobile / network switch）

**症狀**：手機切網路後 UI 不更新。

**修法**：Reflex 預設會 auto-reconnect，但複雜 state 可能不同步：

```python
@rx.event
async def on_mount(self):
    # mount 時重新 sync
    self.data = await api.get(self.id)
```

---

## ⚠️ 8. Theme 沒生效

**症狀**：改了 `rxconfig.py` 的 theme，但 UI 沒變。

**原因**：瀏覽器 cache。強制 refresh：
- macOS: `Cmd + Shift + R`
- 或關掉 reflex server 再開

---

## ⚠️ 9. SQLModel transaction 沒 commit

**症狀**：資料沒寫進 DB。

```python
# ❌ 錯
@rx.event
async def add(self, text: str):
    with rx.session() as session:
        item = Todo(text=text)
        session.add(item)
        # 忘了 commit！

# ✅ 對
@rx.event
async def add(self, text: str):
    with rx.session() as session:
        item = Todo(text=text)
        session.add(item)
        session.commit()
        session.refresh(item)  # 拿回 id
```

---

## ⚠️ 10. Form submit 沒擋 default

**症狀**：form 按 Enter 後 page reload。

**修法**：用 `on_submit` 而不是 `on_click`：
```python
rx.form(
    rx.input(...),
    rx.button("送出", type="submit"),
    on_submit=FormState.submit,
)
```

或在 event handler 裡：
```python
@rx.event
async def submit(self, form_data: dict):
    # ...
    return rx.prevent_default()  # 或在 UI 端處理
```

---

## ⚠️ 11. Computed var 用 mutating method

**症狀**：computed var 沒更新。

```python
# ❌ 錯 — list.append() 沒 trigger re-render
@rx.var
def items(self) -> list:
    self._items.append("new")  # mutating，沒變動 reference
    return self._items

# ✅ 對 — replace reference
@rx.var
def items(self) -> list:
    return self._items + ["new"]
```

或：
```python
@rx.event
def add(self, item):
    self._items = self._items + [item]  # 重新賦值
```

---

## ⚠️ 12. 圖片 / asset 路徑錯

**症狀**：`rx.image(src="...")` 顯示 broken image。

```python
# ❌ 錯 — 絕對路徑 / 外部 URL 沒處理
rx.image(src="/Users/nigo/photo.png")
rx.image(src="https://example.com/photo.png")  # CORS 可能擋

# ✅ 對 — 用 assets/ 資料夾
# 圖片放 assets/photo.png
rx.image(src="/photo.png")  # Reflex 自動從 assets/ serve

# ✅ 對 — 外部圖片
rx.image(src="https://...")  # 用完整 URL + CORS 允許
```

---

## ⚠️ 13. Hot reload 沒生效（prod mode）

**症狀**：改 code 但 dev server 沒 reload。

**原因**：用 `--env prod` 沒有 hot reload。

```python
# ✅ dev mode（預設）有 hot reload
reflex run

# ⚠️ prod mode 沒 hot reload，要手動 restart
reflex run --env prod
```

---

## ⚠️ 14. Memory leak（state 越來越大）

**症狀**：用一段時間後 server memory 暴增。

**原因**：state 沒清理 / 大 list 沒釋放。

```python
# ❌ 錯 — 累積
class State(rx.State):
    history: list = []

    @rx.event
    def add_history(self, event):
        self.history.append(event)  # 永遠不刪

# ✅ 對 — 限制大小
class State(rx.State):
    history: list = []
    MAX_HISTORY = 100

    @rx.event
    def add_history(self, event):
        self.history = (self.history + [event])[-self.MAX_HISTORY:]
```

---

## ⚠️ 15. Auth state 在多 tab 不同步

**症狀**：tab A 登入，tab B 沒同步。

**修法**：用 `rx.ClientStorage` 或 server-side session：
```python
class AuthState(rx.State):
    token: str = rx.Cookie("", "auth_token", secure=True)  # 跨 tab 同步
```

---

## 🛡 預防 checklist

- [ ] Event handler 都用 `@rx.event`
- [ ] Async event handler 用 `async def` + `yield` 控更新時機
- [ ] Computed var 不循環依賴
- [ ] 大資料用分頁 / lazy load
- [ ] DB operation 用 `with rx.session()` + commit
- [ ] State 上限設 MAX_*
- [ ] Theme 改完強制 refresh
- [ ] Port 衝突先檢查 lsof

---

## 📚 延伸

- [architecture.md](./architecture.md)
- [patterns.md](./patterns.md)
- [scaling.md](./scaling.md)
