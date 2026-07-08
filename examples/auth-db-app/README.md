# Auth + DB App Example

> Reflex + Supabase Auth + Postgres 完整整合

## 啟動

```bash
cd examples/auth-db-app/
pip install -r requirements.txt
cp .env.example .env
# 編輯 .env 設 SUPABASE_URL + SUPABASE_KEY + DB_URL
reflex run
```

## 學到什麼

- ✅ Supabase Auth 整合（login / register / logout）
- ✅ Postgres 連線（用 SQLModel）
- ✅ Protected routes（auth guard）
- ✅ Session persistence（用 Supabase JWT）
- ✅ Row-level security（Postgres RLS）

## 結構

```
auth-db-app/
├── README.md
├── requirements.txt
├── .env.example
├── rxconfig.py
├── auth_db_app.py   # App 入口
├── states.py        # AuthState + AppState
├── db.py            # SQLModel
└── supabase_client.py
```

## ⚠️ 需先準備

1. Supabase project: https://supabase.com
2. 設 `SUPABASE_URL` + `SUPABASE_KEY`（anon key）
3. Postgres connection string：`postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres`
4. 在 Supabase SQL editor 跑 schema：

```sql
CREATE TABLE notes (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- RLS
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own notes" ON notes
  FOR ALL USING (auth.uid() = user_id);
```
