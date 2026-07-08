# Todo App Example

> 最小可跑的 Reflex Todo app — MVP 模板

## 啟動

```bash
cd examples/todo-app/
pip install -r requirements.txt
reflex run
# 開 http://localhost:3000
```

## 學到什麼

- ✅ State 管理（`TodoState`）
- ✅ Event handler（`@rx.event`）
- ✅ SQLModel 整合（SQLite）
- ✅ Form（add todo）
- ✅ List render（`rx.foreach`）
- ✅ 樂觀更新（toggle done）
- ✅ A11y（aria-live + focus management）

## 結構

```
todo-app/
├── README.md
├── requirements.txt
├── rxconfig.py
├── todo_app.py       # App 入口
├── states.py         # TodoState
├── db.py             # SQLModel + SQLite
└── theme.py          # Theme
```

## 改 code

加 edit 功能：
```python
# 在 TodoState 加
edit_text: str = ""
editing_id: int = -1

@rx.event
async def start_edit(self, todo_id: int):
    self.editing_id = todo_id
    # 載入現有 text

@rx.event
async def save_edit(self):
    # 更新
    pass
```
