"""todo_app.py — App 入口"""
import reflex as rx
from .states import TodoState


def todo_item(todo: TodoState.items.type) -> rx.Component:
    return rx.hstack(
        rx.checkbox(
            is_checked=todo.done,
            on_change=lambda _: TodoState.toggle(todo.id),
        ),
        rx.text(
            todo.text,
            text_decoration=rx.cond(todo.done, "line-through", "none"),
            color=rx.cond(todo.done, "gray.400", "text_primary"),
            flex_grow=1,
        ),
        rx.icon_button(
            rx.icon("trash-2"),
            aria_label="Delete",
            on_click=lambda: TodoState.delete(todo.id),
            size="sm",
            variant="ghost",
            color_scheme="red",
        ),
        width="100%",
        padding="2",
        border_bottom="1px solid",
        border_color="border",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("📝 Todo App", size="xl"),
            rx.hstack(
                rx.input(
                    placeholder="Add a task...",
                    value=TodoState.new_text,
                    on_change=TodoState.set_new_text,
                    on_key_down=lambda k: rx.cond(k == "Enter", TodoState.add, rx.noop()),
                    width="100%",
                ),
                rx.button(
                    "Add",
                    on_click=TodoState.add,
                    color_scheme="blue",
                ),
                width="100%",
            ),
            rx.cond(
                TodoState.items.length() > 0,
                rx.vstack(
                    rx.foreach(TodoState.items, todo_item),
                    width="100%",
                    spacing="0",
                ),
                rx.center(
                    rx.text("No todos yet. Add one above!", color="text_secondary"),
                    padding="20px",
                ),
            ),
            spacing="4",
            padding_y="8",
            on_mount=TodoState.load,
        ),
        max_width="600px",
    )


app = rx.App()
app.add_page(index, route="/", title="Todo App")
