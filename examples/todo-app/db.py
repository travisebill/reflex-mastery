"""db.py — SQLite + SQLModel"""
import reflex as rx
from sqlmodel import Field, SQLModel, select
from datetime import datetime


class Todo(rx.Model, table=True):
    text: str
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
