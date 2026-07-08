"""index.py — Landing page"""
import reflex as rx
from ..components.layout import layout


def index() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Welcome to Reflex", size="2xl"),
            rx.text("這是 starter template 的 landing page。", color="text_secondary"),
            rx.hstack(
                rx.button("開始使用", on_click=rx.redirect("/dashboard"), color_scheme="blue"),
                rx.button("GitHub", on_click=rx.redirect("https://github.com"), variant="outline"),
                spacing="4",
            ),
            spacing="6",
            align="center",
            padding="40px",
        )
    )
