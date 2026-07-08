"""auth_db_app.py — App 入口"""
import reflex as rx
from .states import AuthState, NotesState


def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Login", size="lg"),
                rx.input(
                    placeholder="Email",
                    type="email",
                    value=AuthState.email,
                    on_change=AuthState.set_email,
                    width="100%",
                ),
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    width="100%",
                ),
                rx.cond(
                    AuthState.error != "",
                    rx.text(AuthState.error, color="red.500", role="alert"),
                ),
                rx.button(
                    "Sign in",
                    on_click=AuthState.login,
                    is_loading=AuthState.loading,
                    color_scheme="blue",
                    width="100%",
                ),
                rx.link("Create account", href="/register", size="sm"),
                spacing="3",
                width="100%",
            ),
            max_width="400px",
        ),
        min_height="100vh",
    )


def register_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Sign up", size="lg"),
                rx.input(
                    placeholder="Email",
                    type="email",
                    value=AuthState.email,
                    on_change=AuthState.set_email,
                ),
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                ),
                rx.button(
                    "Sign up",
                    on_click=AuthState.register,
                    is_loading=AuthState.loading,
                    color_scheme="blue",
                ),
                rx.link("Have account? Login", href="/login", size="sm"),
                spacing="3",
            ),
            max_width="400px",
        ),
        min_height="100vh",
    )


def notes_page() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("📝 My Notes", size="xl"),
            rx.spacer(),
            rx.button("Logout", on_click=AuthState.logout, variant="outline"),
            width="100%",
        ),
        rx.hstack(
            rx.input(
                placeholder="New note...",
                value=NotesState.new_text,
                on_change=NotesState.set_new_text,
                on_key_down=lambda k: rx.cond(k == "Enter", NotesState.add, rx.noop()),
                width="100%",
            ),
            rx.button("Add", on_click=NotesState.add, color_scheme="blue"),
            width="100%",
        ),
        rx.foreach(NotesState.items, lambda n: rx.box(
            rx.text(n.text),
            padding="3",
            border="1px solid",
            border_color="border",
            border_radius="md",
            width="100%",
        )),
        spacing="4",
        padding="8",
        max_width="700px",
        margin="auto",
        on_mount=NotesState.load,
    )


app = rx.App()
app.add_page(login_page, route="/login", title="Login")
app.add_page(register_page, route="/register", title="Register")
app.add_page(notes_page, route="/notes", title="Notes")
