"""ai_chat_app.py — App 入口"""
import reflex as rx
from .states import ChatState


def message_bubble(msg: dict) -> rx.Component:
    is_user = msg["role"] == "user"
    return rx.box(
        rx.hstack(
            rx.badge(msg["role"], color_scheme=rx.cond(is_user, "blue", "gray")),
            rx.text(msg["provider"], font_size="xs", color="gray.500"),
        ),
        rx.text(msg["content"], white_space="pre-wrap", margin_top="2"),
        padding="3",
        border_radius="md",
        background=rx.cond(is_user, "blue.50", "gray.50"),
        max_width="80%",
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
    )


def cost_indicator() -> rx.Component:
    return rx.hstack(
        rx.text(f"Tokens: in={ChatState.total_input_tokens} / out={ChatState.total_output_tokens}", font_size="xs", color="gray.500"),
        rx.text(f"Cost: ${ChatState.total_cost:.4f}", font_size="xs", color="green.600", font_weight="bold"),
        spacing="4",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("🤖 Multi-Provider AI Chat", size="lg"),
                rx.spacer(),
                rx.select(
                    ["minimax", "openai", "anthropic", "ollama"],
                    value=ChatState.provider,
                    on_change=ChatState.set_provider,
                    size="sm",
                ),
                rx.button("Clear", on_click=ChatState.clear, size="sm", variant="outline"),
                width="100%",
            ),
            cost_indicator(),
            rx.box(
                rx.vstack(
                    rx.foreach(ChatState.messages, message_bubble),
                    spacing="3",
                    align="stretch",
                    width="100%",
                ),
                height="500px",
                overflow_y="auto",
                padding="3",
                border="1px solid",
                border_color="border",
                border_radius="md",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="問 AI 任何問題...",
                    value=ChatState.user_input,
                    on_change=ChatState.set_input,
                    on_key_down=lambda k: rx.cond(k == "Enter", ChatState.send, rx.noop()),
                    width="100%",
                ),
                rx.button(
                    "送出",
                    on_click=ChatState.send,
                    is_loading=ChatState.loading,
                    color_scheme="blue",
                ),
            ),
            spacing="4",
            padding_y="8",
        ),
        max_width="700px",
    )


app = rx.App()
app.add_page(index, route="/", title="AI Chat")
