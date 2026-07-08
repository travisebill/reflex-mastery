# Contributing

> 歡迎 PR！以下是流程

---

## 🚀 Quick Start

```bash
# 1. Fork + clone
git clone https://github.com/YOUR_USERNAME/reflex-mastery.git
cd reflex-mastery

# 2. 建 branch
git checkout -b feat/your-feature

# 3. 改 code
# ... 編輯檔案 ...

# 4. 跑 smoke test
bash scripts/smoke_test.sh  # (待建立)

# 5. Commit + push
git commit -m "feat: 你的改動"
git push origin feat/your-feature

# 6. 開 PR
gh pr create --fill
```

---

## 📋 改什麼

### 加新 reference

1. 在對應 sub-skill 內建 `.md`：
   ```
   skills/<sub-skill>/references/<topic>.md
   ```
2. 在對應 `SKILL.md` 的 `## References` section 加一行
3. 跑 smoke test
4. Commit + PR

### 加新 sub-skill

1. 建 `skills/<new-skill>/` 資料夾
2. 寫 `SKILL.md`（含 frontmatter）
3. 在 `package.json` 的 `skills.manifests` 加
4. 在 `.claude-plugin/marketplace.json` 的 `plugins` 加
5. 在 root `README.md` 的「Sub-skills」section 加說明
6. 跑 smoke test
7. Commit + PR

### 修 bug

1. 在 `issues/` 開 issue 描述 bug
2. Fork + fix
3. PR 引用 issue

---

## ✅ PR checklist

- [ ] 跑過 smoke test
- [ ] 沒引入新 warning
- [ ] 改 README（如果加新 sub-skill）
- [ ] Commit message 清楚（`feat:` / `fix:` / `docs:` / `chore:`）
- [ ] 一個 PR 一個 feature（不要 mega-PR）

---

## 🎨 Style Guide

### Markdown

- 用 ATX 風格 heading（`#` 不是 `===`）
- 程式碼用 fenced block（` ```python `）
- 內部連結用相對路徑（`./upgrade-guide.md`）
- 外部連結用 full URL

### Bash

- 4 space indent
- `set -e` 開頭
- 顏色用 ANSI escape（`\033[0;32m`）
- error 用 `set -e` 或明確 `exit 1`

### Python

- PEP 8
- Type hints
- 函數 docstring

### Commit Message

```
<type>(<scope>): <subject>

<body>

<footer>
```

Type:
- `feat`: 新功能
- `fix`: 修 bug
- `docs`: 改文件
- `style`: 格式（不改 logic）
- `refactor`: 重構
- `test`: 加測試
- `chore`: 雜項

Scope: sub-skill 名（如 `reflex-deployment`）或區域

---

## 🛡 License

MIT — 詳見 [LICENSE](../LICENSE)

---

## 💬 問問題

開 issue 或 discussion。
