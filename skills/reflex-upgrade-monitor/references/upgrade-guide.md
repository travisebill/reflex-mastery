# Reflex Upgrade Guide — 0.8 → 0.9 → 1.0

> 各版本 breaking changes + 升級 SOP

---

## 📊 版本時間軸

| 版本 | 發布日期 | 重點 | Breaking changes |
|------|---------|------|------------------|
| 0.7.x | 2024 | 早期版本 | - |
| 0.8.x | 2025-Q1 | SQLModel 整合 | minor |
| 0.8.x → 0.9.0 | 2025-Q3 | Theme API 改寫 | **大** |
| 0.9.0 → 0.9.6 | 2026-Q1 | 修 bug + 小改進 | minor |
| 0.9.6.post1 | 2026-06-26 | 修 dependency | patch |
| 1.0 (預計) | 2026-Q4 | Stable API | TBD |

---

## 🔥 0.8 → 0.9 Breaking Changes

### 1. Theme API 改寫

**0.8**：
```python
config = rx.Config(
    theme="blue",  # 字串
)
```

**0.9**：
```python
app = rx.App(
    theme=rx.theme({  # 物件
        "colors": {"primary": "#3B82F6"},
    }),
)
```

**修法**：把字串改成 `rx.theme({...})` 物件。

### 2. State API 變化

**0.8**：
```python
class State(rx.State):
    @rx.event
    def update(self):
        self.value = 1
        # set_xxx 是自動產生
```

**0.9**：
```python
class State(rx.State):
    value: int = 0  # 明確 type hint + default

    @rx.event
    def set_value(self, v: int):
        self.value = v  # explicit setter
```

**修法**：明確 `type hint` + default + 寫 explicit setter。

### 3. Var API

**0.8**：
```python
rx.text(State.value)
```

**0.9**：
```python
rx.text(State.value)  # 一樣，但背後 lazy evaluation 不同
```

多數 app 不用改。

### 4. Component Library 重整

**0.8**：
```python
rx.Card(...)
rx.Modal(...)
```

**0.9**：
```python
rx.card(...)  # 改小寫
rx.dialog.root(...)  # 新 API
```

**修法**：把所有 `rx.X` 改成 `rx.x`（小寫）。

### 5. Router API

**0.8**：
```python
@rx.page(route="/")
def home():
    return rx.text("Home")
```

**0.9**：
```python
@rx.page(route="/", title="Home")  # 加 title
def home():
    return rx.text("Home")
```

或動態加：
```python
app.add_page(home, route="/", title="Home")
```

### 6. SQLModel 整合

**0.8**：
```python
from sqlmodel import SQLModel, Field
class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
```

**0.9**：相同，但 connection 用 `rx.session()`：

**0.8**：
```python
with rx.session() as s:
    # ...
```

**0.9**：
```python
async with rx.session() as s:
    # 變 async
    await s.commit()
```

**修法**：改 `async with` + `await`。

### 7. FastAPI 整合

**0.8**：
```python
@app.api_route("/api/x")
def x():
    return {}
```

**0.9**：
```python
@app.api_route("/api/x")
async def x():  # 改 async
    return {}
```

**修法**：route handler 加 `async`。

---

## 🔧 0.9.0 → 0.9.6 (minor)

主要是 bug fix + 性能改進。**大多數 app 不用改 code**。

### 0.9.5 改進
- WebSocket reconnect 邏輯優化
- Compile 速度提升 ~30%
- `rx.foreach` 大 list 效能改善
- Var comparison bug 修

### 0.9.6 改進
- 修 `rx.upload` 大檔案 OOM
- 修 SQLModel 連線池在 concurrent request 下洩漏
- 修 theme 切換閃爍

### 0.9.6.post1 (2026-06-26)
- 修 `requests` dependency 版本衝突
- 修 macOS M1 啟動 crash

---

## 🚀 升級 SOP

### Step 1: 查 breaking changes

```bash
bash scripts/check_version.sh
bash scripts/suggest_upgrade.sh
```

### Step 2: 升級前準備

- [ ] 在 dev branch（不是 main）
- [ ] 看完整 changelog
- [ ] 跑全套 test
- [ ] backup 資料庫

### Step 3: 升級

```bash
pip install --upgrade reflex
```

或鎖定版本：
```bash
pip install --upgrade reflex==0.9.6.post1
```

### Step 4: 改 code（看 breaking changes）

```bash
# 跑 test 看哪些壞了
pytest -x

# 修 code
# ...
```

### Step 5: 跑 smoke test

```bash
# compile 過
reflex compile --dry

# dev server 跑
reflex run

# 主流程手動測一遍
# - login
# - 主要操作
# - 登出
```

### Step 6: 升級 manifest

編輯 `version_manifest.json`：
```json
{
  "tracked_version": "0.9.6.post1",
  "last_check": "2026-07-09T01:30:00Z",
  ...
}
```

### Step 7: deploy staging

不要直接 prod。先 staging 跑 24-48 小時。

### Step 8: deploy prod

- [ ] staging 沒問題
- [ ] 看 monitoring
- [ ] 通知 team

---

## 🚨 Rollback 計畫

如果升級後出問題：

```bash
# 鎖回舊版
pip install reflex==0.9.6  # 或上上個版本

# revert code
git revert HEAD

# 重新 deploy
docker compose up -d --build
```

---

## 🔮 1.0 預期改動（TBD）

- Stable API（不再 break）
- 性能再提升
- 內建 SSR 完整支援
- MCP server 完整整合
- 完整 TypeScript types

> 1.0 還在 alpha，建議等 stable 後再升。

---

## 🛟 升級常見問題

### Q: 升級後 compile 失敗
```bash
reflex compile --dry 2>&1 | tee error.log
# 看完整 error
```

### Q: 升級後 test 失敗
```bash
pytest -x --tb=long
# 找出哪個 test 掛 → 對應 changelog
```

### Q: 升級後 WebSocket 斷線
- 確認瀏覽器 cache 清掉
- 確認 `reflex run` 是新版本（`reflex --version`）

### Q: 升級後效能變差
- 開 `loglevel="debug"` 看詳細 log
- 確認沒有新 deprecation warning

---

## 🔗 延伸

- `scripts/check_version.sh` — 自動查最新
- `scripts/fetch_changelog.sh` — 抓完整 changelog
- `scripts/suggest_upgrade.sh` — 分析 breaking changes
- `scripts/self_update.sh` — 更新 manifest
