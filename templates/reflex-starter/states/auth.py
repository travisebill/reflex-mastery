"""auth.py — 認證 state"""
import reflex as rx
from .base import BaseState


class AuthState(BaseState):
    email: str = ""
    password: str = ""
    loading: bool = False

    @rx.event
    def set_email(self, value: str):
        self.email = value

    @rx.event
    def set_password(self, value: str):
        self.password = value

    @rx.event
    async def login(self):
        """登入 — 換成 Supabase / 自架 / Clerk"""
        self.loading = True
        yield

        try:
            # 範例：自架 auth
            if self.email == "demo@example.com" and self.password == "demo":
                self.is_authenticated = True
                self.user_email = self.email
                self.error = ""
                yield rx.toast.success("登入成功")
                yield rx.redirect("/dashboard")
            else:
                self.error = "Email 或密碼錯誤"
                yield rx.toast.error(self.error)
        finally:
            self.loading = False

    @rx.event
    async def register(self):
        """註冊"""
        self.loading = True
        yield
        try:
            # TODO: 串接 auth API
            self.error = "註冊功能尚未實作"
            yield rx.toast.error(self.error)
        finally:
            self.loading = False
