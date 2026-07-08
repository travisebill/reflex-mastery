"""db/models.py — SQLModel 範例"""
from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = ""
    created_at: datetime = Field(default_factory=datetime.now)


class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    id: int = Field(default=None, primary_key=True)
    text: str
    done: bool = False
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
