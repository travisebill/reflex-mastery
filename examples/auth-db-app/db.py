"""db.py — SQLModel + Supabase Postgres"""
import reflex as rx
from sqlmodel import Field, SQLModel
from datetime import datetime


class Note(rx.Model, table=True):
    text: str
    user_id: str  # Supabase user UUID
    created_at: datetime = Field(default_factory=datetime.now)
