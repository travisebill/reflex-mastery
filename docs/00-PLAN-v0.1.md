# Reflex Mastery Skill — Plan v0.1
**Date**: 2026-07-08 22:44 GMT+8
**Author**: Nigo 🐱
**Status**: Draft (待主人 review)

---

## 🎯 核心定位

**互補官方 `reflex-dev/agent-skills`，做「進階模式 + 自動版本追蹤」**

### 官方 3 個 sub-skill（reflex-dev/agent-skills）
| Skill | 內容 |
|-------|------|
| `reflex-docs` | Framework 知識（components/state/events/styling/database/routing/auth） |
| `setup-python-env` | 建 Python venv + 裝 Reflex |
| `reflex-process-management` | Compile / run / reload / debug |

### 官方缺的 3 件事 → **這是我要做的**
1. ❌ **自動版本追蹤**（主人最在意 — Reflex 0.9.x 活躍，1.0 將到）
2. ❌ **進階模式 + 真實踩坑**（官方是 reference doc，缺 pattern / pitfall / 升級指南）
3. ❌ **Production 部署**（官方 process-management 只講 dev，沒講 production）

---

## 📦 命名（待主人選）
- `reflex-mastery` ← **推薦**（語意清晰）
- `reflex-advanced`
- `reflex-pro`

---

## 🗂 檔案結構

```
reflex-mastery/
├── SKILL.md                      # 入口（~5KB，1-page 概念總覽 + 載入順序）
├── version_manifest.json         # {tracked_version, last_check, breaking_since}
├── references/
│   ├── 01-architecture.md        # Reflex 架構圖、compile 流程、frontend↔backend 邊界
│   ├── 02-patterns.md            # 常用 pattern：state、forms、auth、db、async
│   ├── 03-pitfalls.md            # 踩坑大全（state mutation、reactive trap、deploy 雷）
│   ├── 04-upgrade-guide.md       # 0.8 → 0.9 → 1.0 升級 changelog 重點
│   └── 05-deployment.md          # 部署：Vercel / Fly.io / Railway / Docker / 自架
├── scripts/
│   ├── check_version.sh          # 查 PyPI 最新版 + GitHub release（cache 1 天）
│   ├── fetch_changelog.sh        # 抓 changelog（PyPI + GitHub release notes）
│   ├── suggest_upgrade.sh        # 解析 changelog → 標記 breaking changes
│   └── self_update.sh            # 比對 version_manifest → 提示更新
└── examples/                     # 完整 mini app 範例（auth + db + deploy）
    ├── todo-app/                 # 最簡 todo（MVP 模板）
    └── auth-db-app/              # Supabase auth + Postgres（real-world 場景）
```

---

## 🤖 自動更新機制（主人最在意的點）

**設計原則**：偵測到新版只**提示**，**不自動寫檔**（避免污染，主人決定要不要 apply）

```
每次 skill 載入
  └─→ check_version.sh（cache 1 天，輕量）
       ├─ 新版？→ fetch_changelog.sh → suggest_upgrade.sh
       │           └─ 提示: "Reflex v0.9.7 出現於 2026-07-XX，5 個 breaking changes，
       │              建議主人下指令重整 skill"
       └─ 沒新？→ silent
```

**不自動更新的理由**：
- 主人要控制 apply 與否
- changelog 解析要 agent 理解，不是純 regex
- skill 本身被更新才算「真更新」，不是偵測到就行

---

## 🔗 與官方 reflex-dev/agent-skills 互補設計

| 場景 | 用哪個 |
|------|--------|
| 查 framework 知識 | 官方 `reflex-docs` |
| 建環境 | 官方 `setup-python-env` |
| 跑 dev server / 重載 | 官方 `reflex-process-management` |
| **查最新版本** | **本 skill `check_version`** |
| **寫進階 pattern** | **本 skill `02-patterns`** |
| **踩坑** | **本 skill `03-pitfalls`** |
| **升級** | **本 skill `04-upgrade-guide`** |
| **Production deploy** | **本 skill `05-deployment`** |

**結論**：本 skill 是「**reference + operations**」之上的「**進階 + 時效**」層。

---

## 🔄 流程計畫（v0.1 — 避免上次的污染）

| Step | 動作 | 落底位置 |
|------|------|---------|
| 1 | ✅ 寫 plan | `/tmp/reflex-mastery/00-PLAN.md`（這次） |
| 2 | 主人 approve 後 → 寫 references (5 files) | `/tmp/reflex-mastery/references/` |
| 3 | 寫 scripts (4 files) | `/tmp/reflex-mastery/scripts/` |
| 4 | 寫 examples (2 apps) | `/tmp/reflex-mastery/examples/` |
| 5 | 寫 SKILL.md 入口 | `/tmp/reflex-mastery/SKILL.md` |
| 6 | 跑 scripts 驗證 | 終端 + log |
| 7 | 透過 `skill_workshop` 提案（pending） | 不自動 apply |
| 8 | 主人 review → 決定 apply | `skill_workshop apply` |

**關鍵改進**（vs 上一輪失敗原因）：
- ✅ 每寫一個檔案**立即落底磁碟**，不再依賴 session context
- ✅ 全部在 `/tmp/reflex-mastery/`（draft folder），**不污染** workspace/skills/
- ✅ 最後才走 `skill_workshop` 提案（pending，不直接 apply）

---

## 📊 預估

| 項目 | 估計大小 |
|------|---------|
| Research Reflex 文件 1.0 | ~5-8 KB content |
| 5 個 references | ~15-20 KB |
| 4 個 scripts | ~3-5 KB |
| 2 個 example apps | ~10-15 KB |
| SKILL.md 入口 | ~5 KB |
| **總計** | **~40-50 KB skill content + 跑 4 個 scripts 驗證** |

**預計 token 花費**：中等（每檔案 ~2-3KB context 暫用，研究文件需多次 web_fetch）

---

## ❓ 待主人決策

1. **命名**：`reflex-mastery` / `reflex-advanced` / `reflex-pro`？
2. **scope 邊界**：是否包含 examples/ 資料夾（完整 mini app）？或只要 references + scripts？
3. **自動更新策略**：同意「偵測到新版只提示不自動 apply」嗎？還是要全自動？
4. **apply 時機**：要不要等所有檔案寫完一次 apply？還是要分批 review？
