"""login.py — Login page"""
import reflex as rx
from ..components.layout import layout
from ..states.auth import AuthState


def login() -> rx.Component:
    return layout(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Login", size="lg"),
                    rx.vstack(
                        rx.text("Email"),
                        rx.input(
                            placeholder="you@example.com",
                            value=AuthState.email,
                            on_change=AuthState.set_email,
                            type="email",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Password"),
                        rx.input(
                            placeholder="••••••",
                            value=AuthState.password,
                            on_change=AuthState.set_password,
                            type="password",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.cond(
                        AuthState.error != "",
                        rx.text(AuthState.error, color="error", role="alert", aria_live="polite"),
                    ),
                    rx.button(
                        "Sign in",
                        on_click=AuthState.login,
                        is_loading=AuthState.loading,
                        color_scheme="blue",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                max_width="400px",
                width="100%",
            ),
            min_height="70vh",
        )
    )
