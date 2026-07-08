---
name: reflex-docs-advanced
description: >
  Reflex 進階 framework 知識：architecture / patterns / pitfalls。
  互補官方 reflex-docs（reference doc）的進階層。
  Use when 寫進階 Reflex app、踩到 reactivity 問題、state 規模化、或
  要 scale app 到 production。
  Load when user is working with non-trivial Reflex app, asks about state
  mutation patterns, computed var dependencies, event chaining, or
  mentions reactivity issues.
---

# Reflex Docs — Advanced

> 互補官方 [`reflex-docs`](https://github.com/reflex-dev/agent-skills) 的**進階** layer

官方 `reflex-docs` 是 reference doc（URL table + 一句話概念）。本 sub-skill 提供**進階模式 + 踩坑大全 + architecture deep dive**。

---

## 🎯 何時用

- ✅ 寫進階 Reflex app（multi-page、complex state、async、auth）
- ✅ 踩到 reactivity 問題（state mutation 沒生效、computed var 不更新）
- ✅ State 規模化（上千個 var、複雜 dependency 圖）
- ✅ Event chaining 設計（yield 多 event、async event handler）
- ✅ 想了解 Reflex 內部 architecture（compile 流程、frontend↔backend 邊界）

❌ **不適用於**：
- 第一次學 Reflex（先用官方 reflex-docs + setup-python-env）
- 簡單 hello world（不需要進階知識）

---

## 📚 References

| Topic | URL |
|-------|-----|
| Architecture & Compile Flow | [references/architecture.md](./references/architecture.md) |
| Patterns: State / Forms / Auth / DB | [references/patterns.md](./references/patterns.md) |
| Pitfalls & Reactivity Traps | [references/pitfalls.md](./references/pitfalls.md) |
| Scaling State (1000+ vars) | [references/scaling.md](./references/scaling.md) |

---

## 🏗 Quick Architecture Overview

```
┌──────────────────┐  WebSocket (state sync)  ┌──────────────────┐
│  Frontend        │ ←──────────────────────→ │  Backend (State)  │
│  (React via Py)  │                          │  rx.State classes │
│  rx.Component    │                          │  event handlers   │
└──────────────────┘                          └──────────────────┘
                                                        ↓
                                                ┌──────────────────┐
                                                │  Database        │
                                                │  (SQLModel)      │
                                                └──────────────────┘
```

- **State 在 server**，前端是 reactive mirror
- Event handler 在 backend 跑，更新 state → 自動 sync 到 frontend
- `rx.Component` 是 React 的 Python wrapper，compile 時轉 JS
- 所有 API call、DB query、auth check 都在 backend

詳細 architecture：[references/architecture.md](./references/architecture.md)

---

## ⚡ Top 3 Patterns（速查）

### 1. Computed Var Dependency 圖

```python
class State(rx.State):
    count: int = 0
    doubled: int = 0

    @rx.var
    def quadrupled(self) -> int:
        return self.doubled * 2  # ✅ 自動追蹤 doubled 變化

    @rx.event
    def increment(self):
        self.count += 1
        self.doubled = self.count * 2  # 明確 assign 才會 trigger quadrupled
```

### 2. Event Chaining

```python
@rx.event
async def complex_action(self):
    yield State.set_loading(True)      # 第一個 event
    result = await some_async_call()
    yield State.set_data(result)       # 第二個 event
    yield State.set_loading(False)     # 第三個 event
```

### 3. Multi-page State Sharing

```python
# 用 app.state 全域 state
app = rx.App(state=GlobalState)
# 或繼承 BaseState
class DashboardState(BaseState):
    pass
```

完整 patterns：[references/patterns.md](./references/patterns.md)

---

## 🚨 Top 5 Pitfalls

1. **State mutation 沒生效** — 沒用 `@rx.event` 修飾 / 直接改 var 沒用 setter
2. **Async deadlock** — `await` 在 event handler 裡但沒 `async def`
3. **Computed var 循環依賴** — A 依賴 B、B 依賴 A → infinite loop
4. **State 規模爆炸** — 把 list 全部放 state → re-render 慢 → 改用 paginated query
5. **Port conflict** — `reflex run` 預設 3000，被佔用會 crash

詳細 pitfalls：[references/pitfalls.md](./references/pitfalls.md)

---

## 🔗 與其他 sub-skill 關係

- **官方 `reflex-docs`** — 基礎 reference（先用這個）
- **官方 `reflex-process-management`** — compile / run / reload（本 skill 不重複）
- **本 `reflex-deployment`** — 部署（本 skill 講架構，不講部署）
- **本 `reflex-ai-integration`** — AI SDK 整合（stateful chat 模式詳見那邊）

---

## 📊 與官方 reflex-docs 對比

| 官方 reflex-docs | 本 sub-skill |
|-----------------|--------------|
| URL table | ✅ |
| State 一句話帶過 | **進階 state pattern + dependency 圖** |
| Components 簡介 | **進階 composition 模式** |
| Events 基本 | **Event chaining + async + yield 模式** |
| Database 簡介 | **進階 SQLModel pattern + 連線池 + migration** |
| ❌ | **Reactivity traps + 踩坑大全** |
| ❌ | **Scaling 1000+ vars 策略** |

---

## 🛠 維護

- 內容隨 Reflex 版本演進
- Reflex 0.9.x → 1.0 過渡期的 breaking changes 整理見 `reflex-upgrade-monitor/references/upgrade-guide.md`
