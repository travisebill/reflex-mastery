---
name: reflex-ux-workflow
description: >
  Reflex app 與 ui-ux-pro-max skill 協作：design tokens → rx.theme() 對應、
  component 規格 → rx.* 對應、互動規格 → state + event handler 規劃、
  accessibility (a11y) checklist。
  Use when 把 design 轉成 Reflex 實作、需要 a11y review、wireframe → code。
  Load when user mentions design tokens, wireframe, mockup, Figma, accessibility,
  or wants to use ui-ux-pro-max skill.
---

# Reflex UX Workflow

> 與 [`ui-ux-pro-max`](https://docs.openclaw.ai) skill 協作的完整工作流

---

## 🎯 何時用

- ✅ 把 design（tokens / wireframe / mockup）轉成 Reflex code
- ✅ 用 ui-ux-pro-max 出 design → handoff 給 Reflex
- ✅ a11y 檢查（ARIA / keyboard / focus）
- ✅ Design system 整合（shadcn / radix / custom）
- ✅ Component library 對應

❌ **不適用於**：
- 純 Reflex 寫 code（沒 design input）— 用 `reflex-docs-advanced`
- 想直接跳過設計（不推薦，但可選）

---

## 📚 References

| Topic | URL |
|-------|-----|
| 何時叫 ui-ux-pro-max | [references/when-to-call.md](./references/when-to-call.md) |
| Handoff 格式 | [references/handoff-format.md](./references/handoff-format.md) |
| Design Tokens → rx.theme() | [references/design-tokens-mapping.md](./references/design-tokens-mapping.md) |
| Component 規格 → rx.* 對應 | [references/component-mapping.md](./references/component-mapping.md) |
| Accessibility (a11y) | [references/accessibility.md](./references/accessibility.md) |

---

## 🔄 完整工作流

```
[主人：要寫新 Reflex app]
   ↓
Step 1: 規劃 scope（用 reflex-docs-advanced 確認技術可行性）
   ↓
Step 2: 叫 ui-ux-pro-max 出 design
   ↓
Step 3: 拿到 3 份 design 產出
   ├─ design tokens（colors / spacing / typography）
   ├─ wireframe（每 page layout）
   └─ component list（要用的 components）
   ↓
Step 4: 用本 skill 把 design 轉成 Reflex
   ├─ tokens → rx.theme()  ← 詳見 design-tokens-mapping.md
   ├─ components → rx.* 對應  ← 詳見 component-mapping.md
   └─ 互動 → state + event handler 規劃
   ↓
Step 5: 寫 code
   ↓
Step 6: a11y review（accessibility.md checklist）
```

---

## ⚡ Quick Start：叫 ui-ux-pro-max 出 design

> 這是主人會下的 prompt

```
我要寫一個 todo app（Reflex 技術棧），使用 Supabase auth。

請先用 ui-ux-pro-max skill 出 design：
- design tokens（主色 / 中性色 / spacing scale）
- 3 個 page wireframe：login / todo list / todo detail
- component list（每 page 用到的 components）
- accessibility 重點

出完後告訴我，我用 reflex-ux-workflow skill 轉成 Reflex code。
```

**ui-ux-pro-max 會回**：3 份 design 文件（JSON 或 markdown）

**然後** reflex-ux-workflow 引導把 design 套成 Reflex code。

---

## 🎨 Design Tokens → rx.theme() 對應

**ui-ux-pro-max 給的 tokens**（常見格式）：
```json
{
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#10B981",
    "background": "#FFFFFF",
    "text": "#1F2937"
  },
  "spacing": {
    "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"
  },
  "typography": {
    "h1": "32px/40px",
    "body": "16px/24px"
  }
}
```

**對應的 `rx.theme()` 設定**：
```python
import reflex as rx

theme = {
    "colors": {
        "primary": "#3B82F6",
        "secondary": "#10B981",
        "background": "#FFFFFF",
    },
    "spacing": {
        "1": "4px", "2": "8px", "3": "16px", "4": "24px", "5": "32px"
    },
    "font_sizes": {
        "h1": "2rem", "body": "1rem"
    },
}

app = rx.App(theme=rx.theme(theme))
```

詳細對應規則：[references/design-tokens-mapping.md](./references/design-tokens-mapping.md)

---

## 🧩 Component 規格 → rx.* 對應

| ui-ux-pro-max 設計 | Reflex 對應 |
|-------------------|-----------|
| `<Button primary>` | `rx.button("...", color_scheme="blue")` |
| `<Card>` | `rx.card(rx.vstack(...))` |
| `<Modal>` | `rx.dialog(...)` 或 `rx.alert_dialog(...)` |
| `<Input>` | `rx.input(...)` |
| `<Select>` | `rx.select(...)` |
| `<Table>` | `rx.table(...)` |
| 自訂 component | `rx.Component` 繼承 + 自訂 |

完整對應表：[references/component-mapping.md](./references/component-mapping.md)

---

## ♿ Accessibility Checklist

部署前必檢：

- [ ] 所有按鈕有 `aria-label`（icon-only button）
- [ ] Form input 有 `<label>` 對應
- [ ] 鍵盤可操作（Tab / Enter / Esc）
- [ ] Focus visible（不要 `outline: none`）
- [ ] 顏色對比 ≥ 4.5:1（文字）/ 3:1（大文字）
- [ ] Image 有 `alt` 屬性
- [ ] 動態內容用 `aria-live`
- [ ] 測試螢幕閱讀器（VoiceOver / NVDA）

詳細：[references/accessibility.md](./references/accessibility.md)

**a11y testing 整合進 CI**：
```bash
npm install -D @axe-core/cli
axe https://my-reflex-app.com --exit
```

---

## 🔗 與其他 sub-skill 關係

- **本 `reflex-docs-advanced`** — design 對應 code 前先看 state 進階 pattern
- **本 `reflex-ai-integration`** — chat UI 設計要 streaming-friendly
- **`ui-ux-pro-max`** — 主導 design，本 skill 負責 handoff

---

## 📋 Handoff 完整清單

從 ui-ux-pro-max 收到後，主人要檢查：

- [ ] **Design tokens** — colors / spacing / typography / shadows
- [ ] **Page wireframes** — 每 page 的 layout 草圖
- [ ] **Component spec** — 用到的 components + variant
- [ ] **互動規格** — 點 button A 會發生什麼
- [ ] **State 規格** — 哪些 state 跨 page、哪些 local
- [ ] **Empty state / Loading state / Error state** 設計
- [ ] **Responsive breakpoints**（mobile / tablet / desktop）

詳細：[references/handoff-format.md](./references/handoff-format.md)
