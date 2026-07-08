# Reflex Patterns — 常用 pattern 集

> 寫進階 Reflex app 的 10 個 pattern + code 範例

---

## 1️⃣ Computed Var Dependency 圖

Reflex 自動追蹤 computed var 依賴（基於屬性存取）：

```python
class CartState(rx.State):
    items: list[dict] = []
    discount_rate: float = 0.0

    @rx.var
    def subtotal(self) -> float:
        return sum(item["price"] * item["qty"] for item in self.items)

    @rx.var
    def discount(self) -> float:
        return self.subtotal * self.discount_rate  # ✅ 自動追蹤 subtotal

    @rx.var
    def total(self) -> float:
        return self.subtotal - self.discount
```

**陷阱**：computed var 不能依賴**自己**或**循環依賴**（會 infinite loop）。

---

## 2️⃣ Event Chaining — Yield 多 Event

```python
class FormState(rx.State):
    loading: bool = False
    error: str = ""
    data: dict = {}

    @rx.event
    async def submit(self, form_data: dict):
        self.loading = True
        self.error = ""
        yield  # 第一次：立刻更新 UI（loading = True）

        try:
            result = await api.save(form_data)
            self.data = result
            yield rx.toast.success("已送出！")
            yield rx.redirect("/dashboard")
        except Exception as e:
            self.error = str(e)
            yield rx.toast.error(f"失敗：{e}")
        finally:
            self.loading = False
            yield  # 第二次：關閉 loading
```

`yield` 在 async event handler 裡會**立即送出 event → UI 更新**，handler 繼續跑。

---

## 3️⃣ State 拆分（不要一個 State 管全部）

```python
# ❌ 不好 — 一個 State 100+ vars
class AppState(rx.State):
    user: dict = {}
    todos: list = []
    settings: dict = {}
    # ... 100 個 var

# ✅ 好 — 拆分 + 共享 base
class BaseState(rx.State):
    user: dict = {}

class TodoState(BaseState):
    todos: list = []

class SettingsState(BaseState):
    theme: str = "light"
```

`BaseState` 是 `TodoState` 和 `SettingsState` 的**共同 base**，但 Reflex 只會把當前 page 用到的 state 同步到前端。

---

## 4️⃣ Form Pattern（controlled + validation）

```python
import re

class SignupForm(rx.State):
    email: str = ""
    password: str = ""
    errors: dict = {}

    @rx.var
    def is_valid(self) -> bool:
        return not self.errors and self.email and self.password

    @rx.event
    def set_email(self, value: str):
        self.email = value
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            self.errors["email"] = "Email 格式錯誤"
        else:
            self.errors.pop("email", None)

    @rx.event
    def set_password(self, value: str):
        self.password = value
        if len(value) < 8:
            self.errors["password"] = "密碼至少 8 字"
        else:
            self.errors.pop("password", None)

    @rx.event
    async def submit(self):
        if not self.is_valid:
            yield rx.toast.error("請修正錯誤")
            return
        # 呼叫 API / DB
        ...
```

UI：
```python
def form() -> rx.Component:
    return rx.vstack(
        rx.input(
            value=SignupForm.email,
            on_change=SignupForm.set_email,
            placeholder="Email",
        ),
        rx.cond(
            SignupForm.errors.contains("email"),
            rx.text(SignupForm.errors["email"], color="red"),
        ),
        # ... password
        rx.button(
            "送出",
            on_click=SignupForm.submit,
            is_disabled=~SignupForm.is_valid,
        ),
    )
```

---

## 5️⃣ Database Pattern（SQLModel）

```python
from sqlmodel import Field, SQLModel
from datetime import datetime

class TodoItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    text: str
    done: bool = False
    user_email: str  # foreign key 邏輯
    created_at: datetime = Field(default_factory=datetime.now)

# rxconfig.py
config = rx.Config(db_url="sqlite:///todos.db")

class TodoState(rx.State):
    items: list[TodoItem] = []

    @rx.event
    async def load(self):
        with rx.session() as session:
            self.items = session.exec(
                select(TodoItem).where(TodoItem.user_email == self.user_email)
            ).all()

    @rx.event
    async def add(self, text: str):
        with rx.session() as session:
            item = TodoItem(text=text, user_email=self.user_email)
            session.add(item)
            session.commit()
        yield TodoState.load  # 重新 load
```

**重點**：
- `rx.session()` 自動管理 transaction
- Foreign key 用邏輯處理（SQLModel 不強制 DB-level FK）
- 用 yield 觸發 reload（不要直接 mutate self.items）

---

## 6️⃣ Authentication Pattern

```python
import reflex as rx

class AuthState(rx.State):
    user_email: str = ""
    is_authenticated: bool = False

    @rx.event
    async def login(self, email: str, password: str):
        # 呼叫 auth API（自架 / Supabase / Clerk / Auth0）
        user = await auth_api.verify(email, password)
        if user:
            self.user_email = user.email
            self.is_authenticated = True
            yield rx.redirect("/dashboard")
        else:
            yield rx.toast.error("登入失敗")

    @rx.event
    def logout(self):
        self.is_authenticated = False
        yield rx.redirect("/login")

# 用在 page guard
def require_auth(page_func):
    @rx.page(route=page_func.__name__)
    def wrapper():
        if rx.State.is_authenticated:
            return page_func()
        return rx.center(rx.spinner())
    return wrapper

@require_auth
def dashboard():
    return rx.text("Dashboard")
```

---

## 7️⃣ Async Event Handler

```python
class AIState(rx.State):
    response: str = ""
    loading: bool = False

    @rx.event
    async def ask_ai(self, prompt: str):
        self.loading = True
        yield

        # 可以用任何 async lib
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.example.com/ai", json={"prompt": prompt}) as resp:
                data = await resp.json()
                self.response = data["answer"]

        self.loading = False
```

**注意**：必須是 `async def`，才能用 `await` / `yield`。

---

## 8️⃣ Multi-page State 重置

```python
class WizardState(rx.State):
    step: int = 1
    form_data: dict = {}

    @rx.event
    def reset(self):
        self.step = 1
        self.form_data = {}
```

進新 wizard 時呼叫 `reset()`。

---

## 9️⃣ Optimistic Update Pattern

```python
class LikeState(rx.State):
    likes: dict[str, int] = {}

    @rx.event
    async def like(self, post_id: str):
        # Optimistic: 立刻更新 UI
        self.likes[post_id] = self.likes.get(post_id, 0) + 1
        yield  # 立刻 sync 到 frontend

        try:
            await api.like(post_id)
        except Exception:
            # 失敗就 revert
            self.likes[post_id] -= 1
            yield rx.toast.error("按讚失敗")
```

---

## 🔟 上傳檔案 Pattern

```python
class UploadState(rx.State):
    upload_progress: float = 0.0
    uploaded_url: str = ""

    @rx.event
    async def handle_upload(self, file: rx.UploadFile):
        self.upload_progress = 0
        yield

        # 讀檔案
        content = await file.read()

        # 分塊上傳
        chunk_size = 1024 * 256
        total = len(content)
        for i in range(0, total, chunk_size):
            chunk = content[i:i + chunk_size]
            await api.upload_chunk(chunk)
            self.upload_progress = (i + len(chunk)) / total
            yield

        self.uploaded_url = await api.finalize()

# UI
rx.upload(
    rx.text("拖曳檔案或點擊上傳"),
    id="upload1",
    on_drop=UploadState.handle_upload(rx.upload_files("upload1")),
    max_files=1,
    accept={"application/pdf": [".pdf"]},
)
```

---

## 📚 延伸

- [architecture.md](./architecture.md) — 架構基礎
- [pitfalls.md](./pitfalls.md) — 踩坑大全
- [scaling.md](./scaling.md) — State 規模化
