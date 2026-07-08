"""base.py — 共用 base state"""
import reflex as rx


class BaseState(rx.State):
    """所有 state 的 base class"""

    user_email: str = ""
    is_authenticated: bool = False
    error: str = ""

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.user_email = ""
        return rx.redirect("/")
