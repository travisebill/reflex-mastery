"""rxconfig.py — Reflex app 設定"""
import reflex as rx

config = rx.Config(
    app_name="reflex_starter",
    db_url="sqlite:///reflex.db",
    backend_port=8000,
    frontend_port=3000,
    env=rx.Env.DEV,
    loglevel="info",
    cors_allowed_origins=["*"],
    # Theme 在 assets/theme.py 定義
)
