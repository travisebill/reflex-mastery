# Accessibility (a11y) 完整指南

> Reflex app 的無障礙設計 — WCAG 2.1 AA 標準

---

## 🎯 為什麼 a11y 重要

- **法律**：多數國家要求（ADA, EAA, 身障法）
- **市場**：全球 15%+ 人口有某種障礙
- **UX**：a11y 好的 app 通常 UX 也好
- **SEO**：搜尋引擎喜歡語意化結構

---

## 📋 WCAG 4 原則

1. **Perceivable**（可感知）— 內容可用各種感官接收
2. **Operable**（可操作）— UI 可用鍵盤、滑鼠、觸控
3. **Understandable**（可理解）— 內容清楚、行為可預測
4. **Robust**（強健）— 與 assistive tech 相容

---

## 🏗 結構性 a11y

### 1. 語意化 HTML

Reflex 自動產生語意化 HTML，但要確認 component 選對：

```python
# ❌ 用 button 做 link
rx.button("Click me", on_click=...)  # 螢幕閱讀器以為是 button

# ✅ 用 link
rx.link("Click me", href="/page")

# ❌ 用 heading 當 decoration
rx.heading("★★★", size="lg")  # 螢幕閱讀器會讀出來

# ✅ 視覺裝飾用 box
rx.box("★★★", aria_hidden=True)
```

### 2. Heading 階層

```python
# ❌ 跳階層
rx.heading("h1")
rx.heading("h3", "...")  # 跳 h2

# ✅ 連續
rx.heading("h1", "Page Title")
rx.heading("h2", "Section")
rx.heading("h3", "Subsection")
```

### 3. Landmark

```python
# 用 semantic component
rx.box(  # main
    rx.box(  # nav
        rx.link("Home", href="/"),
        rx.link("About", href="/about"),
    ),
    rx.box(  # article
        ...
    ),
    as_="main",  # 或用 reflex 的 layout
)
```

---

## ⌨️ 鍵盤導航

### Tab Order

```python
# 自動按 DOM 順序，但可以手動控制
rx.input(tab_index=1)
rx.input(tab_index=2)
rx.button(tab_index=3, "Submit")
```

### Skip to main content

```python
rx.link(
    "Skip to main content",
    href="#main",
    position="absolute",
    left="-9999px",
    _focus={"left": "8px", "top": "8px", "z_index": "100"},
)

rx.box(id="main", ...)
```

### Enter / Esc

```python
# Modal: Esc 關閉
rx.dialog.root(
    rx.dialog.content(...),
    on_escape_key_down=State.close_modal,
)

# Form: Enter submit
rx.form(
    rx.input(on_key_down=lambda k: rx.cond(k == "Enter", State.submit)),
    rx.button("Submit", type="submit"),
    on_submit=State.submit,
)
```

### Focus management

```python
class State(rx.State):
    @rx.event
    def open_modal(self):
        self.show_modal = True
        # Modal 開啟後 focus 第一個 input
        return rx.call_script("document.querySelector('#modal-input').focus()")
```

---

## 🏷️ ARIA Labels

### aria-label

```python
# icon-only button
rx.button(
    rx.icon("close"),
    aria_label="Close dialog",
    on_click=State.close,
)

# icon link
rx.link(rx.icon("github"), href="...", aria_label="GitHub repo")
```

### aria-labelledby

```python
rx.box(
    rx.heading("Confirm", id="modal-title"),
    rx.text("Are you sure?", id="modal-desc"),
    aria_labelledby="modal-title",
    aria_describedby="modal-desc",
)
```

### aria-live（動態內容）

```python
# 表單錯誤訊息
rx.text(
    State.error,
    color="red.500",
    aria_live="polite",  # 螢幕閱讀器會自動播報
    role="alert",
)

# Toast
rx.toast(...)  # 自動有 aria-live
```

### aria-hidden

```python
# 純裝飾元素
rx.icon("star", aria_hidden=True)
```

### aria-expanded

```python
rx.button(
    "Menu",
    aria_expanded=State.menu_open,
    on_click=State.toggle_menu,
)
```

---

## 🎨 顏色對比

WCAG AA 標準：
- 正常文字（< 18pt）：對比 ≥ 4.5:1
- 大文字（≥ 18pt 或 14pt bold）：對比 ≥ 3:1
- UI 元件 / 圖形：對比 ≥ 3:1

```python
# ❌ 低對比
rx.text("Hard to read", color="gray.300", bg="white")  # ~2.5:1

# ✅ 高對比
rx.text("Easy to read", color="gray.700", bg="white")  # ~7:1
```

**檢查工具**：
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- axe DevTools
- Lighthouse

---

## 📸 圖片替代文字

```python
# 資訊性圖片
rx.image(src="/chart.png", alt="Q4 營收成長 12%")

# 純裝飾圖片
rx.image(src="/decoration.png", alt="")
# 或
rx.image(src="/decoration.png", aria_hidden=True)
```

---

## 📋 表單 a11y

```python
rx.form(
    rx.vstack(
        # 每個 input 都有 label
        rx.text("Email"),  # 或 rx.label
        rx.input(
            id="email",
            aria_describedby="email-help",
            aria_invalid=FormState.email_error != "",
        ),
        rx.text("We'll never share your email", id="email-help", font_size="sm"),
        rx.cond(
            FormState.email_error != "",
            rx.text(FormState.email_error, color="red.500", id="email-error", role="alert"),
        ),

        # required 標記
        rx.input(aria_required=True, required=True),
        rx.text("Required field", id="required-help"),

        rx.button("Submit", type="submit"),
    ),
    on_submit=FormState.submit,
    aria_labelledby="form-title",
)
```

---

## 🎬 動畫

```python
# 尊重 prefers-reduced-motion
import reflex as rx

def animation_style():
    return rx.cond(
        # JS check: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        True,  # simplified
        {"transition": "none"},
        {"transition": "all 0.2s"},
    )
```

---

## 🧪 測試 a11y

### 自動

```bash
# axe CLI
npm install -g @axe-core/cli
axe http://localhost:3000 --exit

# Lighthouse
npx lighthouse http://localhost:3000 --only-categories=accessibility
```

### 手動

- [ ] Tab 鍵可達所有互動元素
- [ ] Enter / Space 觸發 button
- [ ] Esc 關閉 modal
- [ ] 螢幕閱讀器（VoiceOver / NVDA）能完整操作
- [ ] 200% 放大仍可讀
- [ ] 純鍵盤（沒滑鼠）能完成所有任務

### 螢幕閱讀器

- **macOS**：VoiceOver（Cmd + F5）
- **Windows**：NVDA（免費）
- **測試重點**：
  - Heading 結構是否合理
  - Link text 是否有 context（不要 "click here"）
  - Form error 是否被播報
  - 動態內容是否通知

---

## ✅ 上線前 checklist

- [ ] 所有 button / link 有可讀的 accessible name
- [ ] Form 有 label + 錯誤訊息用 aria-live
- [ ] Heading 階層連續不跳
- [ ] 顏色對比 ≥ 4.5:1
- [ ] 鍵盤可完成所有任務
- [ ] Modal 有 focus trap + Esc 關閉
- [ ] 圖片有 alt（或 aria-hidden 純裝飾）
- [ ] 跑過 axe / Lighthouse 0 critical issue
- [ ] 螢幕閱讀器測過

---

## 🔗 延伸

- [checklists/a11y-checklist.md](../checklists/a11y-checklist.md) — 完整 checklist
- [when-to-call.md](./when-to-call.md) — 何時叫 ui-ux-pro-max
- [component-mapping.md](./component-mapping.md) — component 對應
