"""states.py — TodoState"""
import reflex as rx
from .db import Todo


class TodoState(rx.State):
    items: list[Todo] = []
    new_text: str = ""
    loading: bool = False

    @rx.event
    async def load(self):
        self.loading = True
        with rx.session() as session:
            self.items = session.exec(select(Todo).order_by(Todo.created_at.desc())).all()
        self.loading = False

    @rx.event
    async def add(self):
        if not self.new_text.strip():
            return
        with rx.session() as session:
            todo = Todo(text=self.new_text)
            session.add(todo)
            session.commit()
        self.new_text = ""
        return TodoState.load

    @rx.event
    async def toggle(self, todo_id: int):
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                todo.done = not todo.done
                session.add(todo)
                session.commit()
        return TodoState.load

    @rx.event
    async def delete(self, todo_id: int):
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                session.delete(todo)
                session.commit()
        return TodoState.load

    @rx.event
    def set_new_text(self, value: str):
        self.new_text = value
