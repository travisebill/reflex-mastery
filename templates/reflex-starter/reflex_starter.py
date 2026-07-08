"""reflex_starter.py — App 入口"""
import reflex as rx
from assets.theme import theme
from pages.index import index
from pages.dashboard import dashboard
from pages.login import login
from pages.not_found import not_found

app = rx.App(theme=rx.theme(theme))

app.add_page(index, route="/", title="Home")
app.add_page(login, route="/login", title="Login")
app.add_page(dashboard, route="/dashboard", title="Dashboard")
