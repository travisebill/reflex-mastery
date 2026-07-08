# A11y Pre-launch Checklist

> Reflex app 上線前的 accessibility 檢查

---

## 🎨 顏色與視覺

- [ ] 文字 vs 背景對比 ≥ 4.5:1（正常文字）
- [ ] 文字 vs 背景對比 ≥ 3:1（大文字 ≥ 18pt 或 14pt bold）
- [ ] UI 元件 / icon 對比 ≥ 3:1
- [ ] 不只用顏色傳達資訊（也要用 icon / text）
- [ ] Focus indicator 明顯可見
- [ ] 不用純灰階（色盲友善）

---

## ⌨️ 鍵盤

- [ ] 所有功能可用鍵盤完成
- [ ] Tab order 邏輯（從上到下、從左到右）
- [ ] 沒 keyboard trap（卡住出不來）
- [ ] Skip to main content link
- [ ] Esc 關閉 modal / dropdown
- [ ] Enter submit form
- [ ] Arrow keys 用於 menu / listbox

---

## 🖼️ 圖片與媒體

- [ ] 資訊性圖片有 `alt` 描述內容
- [ ] 裝飾性圖片 `alt=""` 或 `aria-hidden`
- [ ] Icon button 有 `aria-label`
- [ ] 影片有字幕
- [ ] 音訊有 transcript

---

## 📋 表單

- [ ] 每個 input 有對應 label
- [ ] Required field 標記（aria-required + visual）
- [ ] 錯誤訊息用 `aria-live="polite"` 或 `role="alert"`
- [ ] 錯誤訊息文字描述問題（不是 "Invalid"）
- [ ] 錯誤訊息鄰近 input
- [ ] 成功提交有 confirmation

---

## 🏗️ 結構

- [ ] Heading 階層連續（h1 → h2 → h3）
- [ ] Page 有 `<h1>` 標題
- [ ] 用 `<button>` 做 button，`<a>` 做 link
- [ ] Landmark 有正確 role（`<main>`, `<nav>`, `<aside>`）
- [ ] List 用 `<ul>` / `<ol>` / `<dl>`
- [ ] Table 有 `<th>` 標題

---

## 🪟 Modal / Dialog

- [ ] 開啟時 focus 移到 modal 內
- [ ] 關閉時 focus 回原 trigger
- [ ] Focus trap（Tab 不會跑到 modal 外）
- [ ] Esc 關閉
- [ ] `aria-modal="true"`
- [ ] `aria-labelledby` 指向標題

---

## 🎬 動態內容

- [ ] Toast / 通知用 `aria-live`
- [ ] Loading state 有文字（不只是 spinner）
- [ ] Auto-rotating carousel 可暫停
- [ ] Timeout warning 給使用者延長選項
- [ ] 尊重 `prefers-reduced-motion`

---

## 📱 響應式

- [ ] 200% 放大仍可讀
- [ ] 320px 寬度仍可操作
- [ ] 觸控目標 ≥ 44x44px

---

## 🧪 測試

- [ ] 跑 `axe http://...` 無 critical issue
- [ ] 跑 Lighthouse accessibility ≥ 95
- [ ] VoiceOver / NVDA 完整測過
- [ ] 純鍵盤（沒滑鼠）能完成所有任務
- [ ] 螢幕閱讀器測過 form 流程

---

## 🆘 緊急修正

| 問題 | 修正 |
|------|------|
| 顏色對比不足 | 改用 darker / lighter token |
| 沒 alt | 加 `alt` 或 `alt=""` |
| 沒 label | 加 `rx.label` 或 `aria-label` |
| 沒 focus visible | 加 `_focus={{ outline: "2px solid blue" }}` |
| 跳 heading | 改用正確 h1/h2/h3 |
| 沒 keyboard nav | 用 `<button>` 不要 `<div onClick>` |
| Modal 沒 trap | 用 `rx.dialog.root`（自動處理） |

---

## ✅ 最終 sign-off

- [ ] 開發者自查
- [ ] 另一位 reviewer 跑過
- [ ] 自動測試 0 critical
- [ ] 螢幕閱讀器測過關鍵流程
- [ ] 純鍵盤測過關鍵流程

**完成後才能上 production**
