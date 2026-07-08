# Handoff 格式

> 從 ui-ux-pro-max 拿到 design 後，整理成 Reflex 實作 spec
>
> ⚠️ **本章節需要 `ui-ux-pro-max` skill 已安裝**。沒裝的話請看 [SKILL.md 開頭的安裝 SOP](../SKILL.md#-安裝-ui-ux-pro-max)。如果你用其他 design 工具（Figma / 手繪 / 自訂 tokens），把「ui-ux-pro-max」換成你的 design 來源即可。

---

## 📥 主人會收到什麼

從 ui-ux-pro-max 通常拿到：

1. `tokens.json` — design tokens
2. `wireframes/<page>.md` — 每 page 草圖
3. `components.md` — components 規格
4. （optional）`user-flows.md` — 互動流程
5. （optional）`a11y-notes.md` — accessibility 重點

---

## 📋 Handoff 整理 checklist

收到後先檢查這些都到位：

### Design tokens ✅
- [ ] colors（primary / secondary / background / text / 灰階 / semantic）
- [ ] spacing scale（4/8/16/24/32 px 系統）
- [ ] typography（h1/h2/h3/body/caption）
- [ ] border radius
- [ ] shadow
- [ ] breakpoints（mobile/tablet/desktop）

### Page wireframes ✅
- [ ] 每 page 有 ASCII art 或描述
- [ ] 互動元素標清楚（button / input / dropdown）
- [ ] 狀態：default / hover / focus / disabled / loading / error / empty
- [ ] 響應式 breakpoints

### Components ✅
- [ ] 每個 component 的用途
- [ ] Variants（primary/secondary/ghost button）
- [ ] States（default/hover/disabled）
- [ ] 對應到 Reflex 的哪個 rx.* 或 custom

### Interaction ✅
- [ ] 點 A 會發生什麼
- [ ] 哪 state 跨 page
- [ ] 哪些需要 optimistic update
- [ ] 哪些需要 server sync

### A11y ✅
- [ ] 鍵盤 nav 規劃
- [ ] Focus management
- [ ] ARIA labels
- [ ] 顏色對比

---

## 🔄 整理成 Reflex 實作 spec

主人收到後，用這模板整理（給自己看的 working notes）：

```markdown
# [App name] Reflex 實作 spec

## Tech Stack
- Frontend: Reflex 0.9.x
- DB: Supabase Postgres
- Auth: Supabase Auth
- AI: minimax M2.7

## Design Tokens
- Primary: #3B82F6 → rx.theme() colors.primary
- Spacing 1-5: 4/8/16/24/32 → rx theme spacing
- ...

## Pages
### /login
- components: form (email + password) + button
- state: AuthState (local)
- a11y: aria-label, keyboard nav

### /todos
- components: list + filter + add button
- state: TodoState (shared)
- a11y: list role, focus management

## Cross-page State
- AuthState: user, token
- (其他 local state 在各自 page)

## Inter-page flows
- 未登入 → /login
- 登入後 → /todos
- 點 todo → /todos/[id]

## A11y 重點
- Form validation error 要 aria-live
- Modal 要 focus trap
- Tab 順序要邏輯
```

---

## 🚨 沒給的東西要主動問

如果 ui-ux-pro-max 沒給某個東西，主動問：

- ❓ 「按鈕被 disable 時的視覺？」
- ❓ 「loading state 用 spinner 還是 skeleton？」
- ❓ 「error state 顯示方式？」
- ❓ 「empty state 怎麼辦？」
- ❓ 「mobile 版的 layout？」
- ❓ 「form validation 錯誤顯示位置？」

---

## 🎨 Token 對應範例

ui-ux-pro-max 給的 token：
```json
{
  "colors": {
    "primary": "#3B82F6",
    "primary-hover": "#2563EB",
    "background": "#FFFFFF",
    "surface": "#F9FAFB",
    "text-primary": "#1F2937",
    "text-secondary": "#6B7280",
    "border": "#E5E7EB",
    "error": "#EF4444",
    "success": "#10B981"
  },
  "spacing": {
    "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"
  },
  "fontSizes": {
    "xs": "12px", "sm": "14px", "base": "16px", "lg": "18px",
    "xl": "20px", "2xl": "24px", "3xl": "30px"
  }
}
```

對應的 `rx.theme()`（詳見 [design-tokens-mapping.md](./design-tokens-mapping.md)）：
```python
theme = {
    "colors": {
        "primary": "#3B82F6",
        "primary_hover": "#2563EB",
        "background": "#FFFFFF",
        "surface": "#F9FAFB",
        "text_primary": "#1F2937",
        "text_secondary": "#6B7280",
        "border": "#E5E7EB",
        "error": "#EF4444",
        "success": "#10B981",
    },
    "spacing": {
        "1": "4px", "2": "8px", "3": "16px", "4": "24px", "5": "32px"
    },
    "font_sizes": {
        "xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem",
        "xl": "1.25rem", "2xl": "1.5rem", "3xl": "1.875rem"
    },
}

app = rx.App(theme=rx.theme(theme))
```

---

## 🔗 延伸

- [when-to-call.md](./when-to-call.md) — 何時叫
- [design-tokens-mapping.md](./design-tokens-mapping.md) — token 詳細對應
- [component-mapping.md](./component-mapping.md) — component 對應
- [accessibility.md](./accessibility.md) — a11y
