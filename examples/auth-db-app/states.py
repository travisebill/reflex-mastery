"""states.py — AuthState + NotesState"""
import reflex as rx
from .db import Note
from .supabase_client import supabase
from sqlmodel import select


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    user_id: str = ""
    is_authenticated: bool = False
    error: str = ""
    loading: bool = False

    @rx.event
    def set_email(self, v: str): self.email = v
    @rx.event
    def set_password(self, v: str): self.password = v

    @rx.event
    async def login(self):
        self.loading = True
        try:
            response = supabase.auth.sign_in_with_password({
                "email": self.email,
                "password": self.password,
            })
            if response.user:
                self.user_id = response.user.id
                self.is_authenticated = True
                self.error = ""
                yield rx.toast.success("登入成功")
                yield rx.redirect("/notes")
            else:
                self.error = "登入失敗"
                yield rx.toast.error(self.error)
        except Exception as e:
            self.error = str(e)
            yield rx.toast.error(self.error)
        finally:
            self.loading = False

    @rx.event
    async def register(self):
        self.loading = True
        try:
            response = supabase.auth.sign_up({
                "email": self.email,
                "password": self.password,
            })
            if response.user:
                yield rx.toast.success("註冊成功，請登入")
                yield rx.redirect("/login")
            else:
                self.error = "註冊失敗"
        except Exception as e:
            self.error = str(e)
            yield rx.toast.error(self.error)
        finally:
            self.loading = False

    @rx.event
    def logout(self):
        supabase.auth.sign_out()
        self.is_authenticated = False
        self.user_id = ""
        return rx.redirect("/login")


class NotesState(rx.State):
    items: list[Note] = []
    new_text: str = ""
    loading: bool = False

    @rx.event
    async def load(self):
        auth = await self.get_state(AuthState)
        if not auth.is_authenticated:
            return

        self.loading = True
        with rx.session() as session:
            self.items = session.exec(
                select(Note).where(Note.user_id == auth.user_id)
            ).all()
        self.loading = False

    @rx.event
    async def add(self):
        auth = await self.get_state(AuthState)
        if not auth.is_authenticated or not self.new_text.strip():
            return

        with rx.session() as session:
            note = Note(text=self.new_text, user_id=auth.user_id)
            session.add(note)
            session.commit()
        self.new_text = ""
        return NotesState.load

    @rx.event
    def set_new_text(self, v: str):
        self.new_text = v
