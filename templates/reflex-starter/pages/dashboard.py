"""dashboard.py — Dashboard page（需登入）"""
import reflex as rx
from ..components.layout import layout
from ..states.base import BaseState
from ..states.auth import AuthState


def dashboard() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Dashboard", size="xl"),
            rx.cond(
                BaseState.is_authenticated,
                rx.text(f"歡迎, {BaseState.user_email}"),
                rx.vstack(
                    rx.text("請先登入", color="text_secondary"),
                    rx.button("Login", on_click=rx.redirect("/login"), color_scheme="blue"),
                ),
            ),
            spacing="4",
            align="start",
            width="100%",
        )
    )
