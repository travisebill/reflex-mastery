"""db/connection.py — DB 連線範例"""
import os
from sqlmodel import Session, create_engine
from .models import User, Todo

DB_URL = os.environ.get("DB_URL", "sqlite:///reflex.db")
engine = create_engine(DB_URL, echo=True)


def init_db():
    """初始化 DB tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
