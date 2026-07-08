# 何時叫 ui-ux-pro-max

> 主人工作流：寫 Reflex app 之前先過 design

---

## 🎯 簡單規則

> **「要寫新的 Reflex app 或新 page 之前」→ 必叫 ui-ux-pro-max**

例外：
- 修改既有 page 的小 bug（不需要）
- 加個無關 design 的功能（API、backend）
- 純 infra / deployment 工作

---

## 📋 什麼時候叫（具體 trigger）

### 必叫 ✅

- ✅ 寫新 app（從 0 開始）
- ✅ 加新 page
- ✅ 大改既有 page 的 layout
- ✅ 改 design system（color / font / spacing）
- ✅ 多 page 結構
- ✅ 有 user flow（註冊 / checkout / onboarding）

### 不用叫 ❌

- ❌ 修 bug（按鈕沒反應、API 報錯）
- ❌ 改文案
- ❌ 改 refactor 內部 code（不動 UI）
- ❌ 加 API endpoint
- ❌ 升級 / 部署

---

## 🔄 完整工作流

```
Step 1: 主人下指令
   「我要寫一個 todo app，reflex 技術棧，Supabase auth」

Step 2: 寫 Reflex app 之前先 call ui-ux-pro-max
   「請先 call ui-ux-pro-max skill 出 design：
    - design tokens (主色 / 中性色 / spacing)
    - 3 page wireframe (login / todo list / todo detail)
    - component list
    - a11y 重點」

Step 3: ui-ux-pro-max 出 design 文件
   （通常會回 3 份：tokens.json / wireframe.md / components.md）

Step 4: 用本 reflex-ux-workflow skill 轉 design 成 Reflex code
   - tokens → rx.theme()
   - components → rx.* 對應
   - 互動 → state + event handlers
   - a11y → checklist

Step 5: 寫 code + 本地測試
Step 6: deploy
```

---

## 💬 Prompt 範本

### A. 新 app

```
我要寫一個 todo app（Reflex + Supabase auth）。

請先 call ui-ux-pro-max skill 出 design：
- design tokens（主色 / 中性色 / spacing scale / typography）
- 3 個 page wireframe：login / todo list / todo detail
- component list（每 page 用到的 components）
- accessibility 重點（特別是 form validation 的 a11y pattern）

出完 design 後，告訴我，我用 reflex-ux-workflow skill 轉成 Reflex code。
```

### B. 加新 page

```
我要在現有 app 加一個 settings page（使用者設定）。

請先 call ui-ux-pro-max：
- settings page 的 wireframe
- 需要的 components（form fields, toggle, dropdown）
- design tokens 沿用現有還是新增

我現有 token: [貼上 tokens.json]
```

### C. 改 design system

```
我要把現有 app 的主色從藍色改成綠色。

請先 call ui-ux-pro-max：
- 新 design tokens（主色 + 衍生色）
- 受影響 components 列表
- 改色後的 visual check 重點

我現有 token: [貼上]
```

---

## 🎨 ui-ux-pro-max 會給什麼

通常 3 份文件：

### 1. `tokens.json`（design tokens）
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
    "h1": "32px", "h2": "24px", "body": "16px"
  }
}
```

### 2. `wireframes/<page>.md`（每 page layout）
```markdown
# Login Page
[Header: logo + app name]
[Centered form]
  - Email input
  - Password input
  - "Sign in" button (primary)
  - "Forgot password?" link
[Footer: signup CTA]
```

### 3. `components.md`（component 規格）
```markdown
# Components needed
- Button (primary, secondary, ghost)
- Input (text, password)
- Form (with validation)
- Toast
- Modal
```

---

## ⚠️ 沒叫 ui-ux-pro-max 的後果

- 主人寫到一半發現 design 不好
- 來回改 color / layout 浪費時間
- a11y 出問題，事後改更貴
- design system 不一致，多 page 看起來拼湊

**結論**：**5 分鐘叫 ui-ux-pro-max，節省 2 小時改 design**

---

## 🔗 延伸

- [handoff-format.md](./handoff-format.md) — 拿到 design 後怎麼處理
- [design-tokens-mapping.md](./design-tokens-mapping.md) — tokens 轉 rx.theme()
- [component-mapping.md](./component-mapping.md) — 設計稿 → rx.* 對應
- [accessibility.md](./accessibility.md) — a11y 完整指南
