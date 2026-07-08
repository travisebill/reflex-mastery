"""layout.py — 統一 layout (header + sidebar + main)"""
import reflex as rx
from ..states.base import BaseState


def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("🐱 App Name", size="md"),
            rx.spacer(),
            rx.hstack(
                rx.link("Home", href="/"),
                rx.link("Dashboard", href="/dashboard"),
                spacing="4",
            ),
            rx.spacer(),
            rx.cond(
                BaseState.is_authenticated,
                rx.button("Logout", on_click=BaseState.logout, size="sm", variant="outline"),
                rx.button("Login", on_click=rx.redirect("/login"), size="sm", color_scheme="blue"),
            ),
            padding="4",
            border_bottom="1px solid",
            border_color="border",
            width="100%",
        ),
        position="sticky",
        top="0",
        bg="background",
        z_index="100",
    )


def layout(content: rx.Component) -> rx.Component:
    return rx.vstack(
        header(),
        rx.container(
            content,
            max_width="1200px",
            padding_y="8",
        ),
        spacing="0",
        min_height="100vh",
        bg="background",
    )
