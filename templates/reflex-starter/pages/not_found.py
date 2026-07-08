"""not_found.py — 404 page"""
import reflex as rx
from ..components.layout import layout


def not_found() -> rx.Component:
    return layout(
        rx.center(
            rx.vstack(
                rx.heading("404", size="3xl"),
                rx.text("Page not found", color="text_secondary"),
                rx.button("Go home", on_click=rx.redirect("/")),
                spacing="4",
            ),
            min_height="60vh",
        )
    )
