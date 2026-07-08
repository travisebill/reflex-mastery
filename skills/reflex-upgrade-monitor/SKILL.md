---
name: reflex-upgrade-monitor
description: >
  Reflex 自動版本追蹤 + 升級指南（0.8 → 0.9 → 1.0 breaking changes）。
  Use when 想知道 Reflex 最新版本、breaking changes、規劃升級、
  確認當前依賴是否過時。
  Load when user asks "version", "upgrade", "breaking change", "changelog",
  or about specific Reflex version numbers.
---

# Reflex Upgrade Monitor

> **自動追蹤 Reflex 最新版本** — 0.9.x 活躍、1.0 將到，主人最在意的點

---

## 🎯 何時用

- ✅ 想知道當前 Reflex 是不是最新版
- ✅ 規劃升級（0.8 → 0.9 → 1.0）
- ✅ 看 breaking changes 影響
- ✅ 確認部署的 app 用的依賴是否過時
- ✅ 自動偵測新版本 → 提示主人

❌ **不適用於**：
- 純架構 / 模式問題（用 `reflex-docs-advanced`）
- 部署（用 `reflex-deployment`）

---

## 🛠 Scripts（4 個）

| Script | 用途 |
|--------|------|
| `scripts/check_version.sh` | 查 PyPI 最新版 + GitHub release |
| `scripts/fetch_changelog.sh` | 抓 changelog（PyPI + GitHub release notes） |
| `scripts/suggest_upgrade.sh` | 解析 changelog → 標記 breaking changes |
| `scripts/self_update.sh` | 比對 `version_manifest.json` → 提示更新 |

---

## 📊 version_manifest.json

記錄當前追蹤狀態：

```json
{
  "tracked_version": "0.9.6",
  "last_check": "2026-07-08T22:00:00Z",
  "last_release_checked": "v0.9.6.post1",
  "breaking_changes_since": [],
  "upgrade_recommended": false
}
```

每次 `check_version.sh` 跑會更新。

---

## ⚡ 快速使用

### 1. 查當前版本

```bash
pip show reflex | grep Version
# 或
reflex --version
```

### 2. 跑 check_version.sh

```bash
bash skills/reflex-upgrade-monitor/scripts/check_version.sh
```

**輸出範例**：
```
✅ Current: 0.9.6
🌐 Latest PyPI: 0.9.6.post1
🌐 Latest GitHub: v0.9.6.post1
📅 Released: 2026-06-26 (12 days ago)
⚠️  Breaking changes since your version: 0
🔄 Upgrade recommended: NO
```

### 3. 完整 changelog

```bash
bash scripts/fetch_changelog.sh --from 0.9.0 --to latest
```

**輸出**：完整 changelog（PyPI + GitHub release notes 合併去重）

### 4. Breaking change 分析

```bash
bash scripts/suggest_upgrade.sh
```

**輸出範例**：
```
📊 Analyzing 0.9.6 → 0.9.6.post1:
  - 0 breaking changes
  - 3 minor improvements
  - 2 bug fixes
✅ Safe to upgrade
```

---

## 🤖 自動觸發機制

**設計原則**：偵測到新版**只提示**，**不自動寫檔**（避免污染，主人決定要不要 apply）

```
每次 skill 載入
  └─→ check_version.sh（cache 1 天，輕量）
       ├─ 新版？→ fetch_changelog.sh → suggest_upgrade.sh
       │           └─ 提示: "Reflex v0.9.7 出現於 2026-07-XX，5 個 breaking changes，
       │              建議主人下指令重整 skill"
       └─ 沒新？→ silent
```

---

## 📚 References

| Topic | URL |
|-------|-----|
| 0.8 → 0.9 → 1.0 升級指南 | [references/upgrade-guide.md](./references/upgrade-guide.md) |

---

## 🔄 升級 SOP

### A. Patch 版本（0.9.6 → 0.9.6.post1）— 通常安全

```bash
pip install --upgrade reflex
# 跑 test 確認沒壞
pytest
```

### B. Minor 版本（0.9.x → 0.9.y）— 看 changelog

```bash
bash scripts/fetch_changelog.sh --from 0.9.6 --to 0.9.7
# 看 breaking changes 區塊
bash scripts/suggest_upgrade.sh
# 確認 OK 才升
pip install --upgrade reflex==0.9.7
pytest
```

### C. Major 版本（0.9 → 1.0）— 必看 upgrade-guide.md

```bash
cat skills/reflex-upgrade-monitor/references/upgrade-guide.md
# 找對應章節
# 依指示改 code（API rename / removed feature）
pip install --upgrade reflex==1.0.0
pytest
reflex compile --dry  # 確認 compile 過
```

---

## 📋 升級前 Checklist

- [ ] 看完整 changelog
- [ ] 跑 `suggest_upgrade.sh` 看 breaking changes 數
- [ ] 看 `references/upgrade-guide.md` 對應版本
- [ ] 在 dev branch 升（不是 main）
- [ ] 跑全套 test
- [ ] 跑 `reflex compile --dry`
- [ ] dev server 跑一遍主流程
- [ ] 部署到 staging（不是 prod）
- [ ] 看 24-48 小時 monitoring
- [ ] 才升 main + 部署 prod

---

## 🔗 與其他 sub-skill 關係

- **本 `reflex-docs-advanced`** — 新版本可能引入新 pattern
- **本 `reflex-deployment`** — 升級前確認部署平台相容性
- **本 `reflex-ai-integration`** — 升級可能影響 streaming response
- **本 `reflex-ux-workflow`** — 升級可能改 theme / component API

---

## 🛡 安全設計

- **不自動 apply** — 偵測到新版只提示，主人決定
- **不寫 remote** — scripts 只 read-only + 更新本地 manifest
- **cache 1 天** — 避免每次載入都打 PyPI / GitHub
- **可關閉** — 在 `version_manifest.json` 設 `"enabled": false`

---

## 🐛 故障排除

### check_version.sh 失敗

- 沒網路 → 檢查 `curl` / DNS
- PyPI rate limit → 等 1 小時
- GitHub rate limit → 用 GH token 或加 `--auth`

### 升級後 compile 失敗

```bash
reflex compile --dry
# 看 error message
# 通常是 import path 改或 API 改
# 查 upgrade-guide.md 對應章節
```

### 升級後 test 失敗

```bash
# 先看哪個 test 掛
pytest -x
# 通常是 state mutation 行為改變
# 查 changelog 的 "Bug Fixes" + "Breaking Changes"
```
