"""
chat-stream.py — Reflex AI Chat App 最小可跑範例

啟動：
1. pip install reflex minimax
2. export MINIMAX_API_KEY=your-key
3. reflex run

開瀏覽器：http://localhost:3000
"""

import reflex as rx
import os
from minimax import Minimax

client = Minimax(api_key=os.environ.get("MINIMAX_API_KEY", ""))


class ChatState(rx.State):
    messages: list[dict] = []
    user_input: str = ""
    loading: bool = False

    def set_input(self, value: str):
        self.user_input = value

    @rx.event
    async def send(self):
        if not self.user_input.strip() or not os.environ.get("MINIMAX_API_KEY"):
            return

        user_msg = {"role": "user", "content": self.user_input}
        self.messages.append(user_msg)
        self.user_input = ""
        self.loading = True
        yield  # 立即更新 UI

        # 加入空的 assistant message（等下 append streaming content）
        self.messages.append({"role": "assistant", "content": ""})
        yield

        try:
            # 用 streaming
            stream = await client.chat.completions.create(
                model="MiniMax-M2.7",
                messages=self.messages[:-1],  # 排除空的 assistant
                stream=True,
            )

            async for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    current = self.messages[-1]
                    self.messages[-1] = {
                        "role": "assistant",
                        "content": current["content"] + delta,
                    }
                    yield  # 每個 chunk 立即更新
        except Exception as e:
            self.messages[-1] = {
                "role": "assistant",
                "content": f"Error: {str(e)}",
            }
        finally:
            self.loading = False

    @rx.event
    def clear(self):
        self.messages = []


def message_bubble(msg: dict) -> rx.Component:
    is_user = msg["role"] == "user"
    return rx.box(
        rx.text(
            msg["role"],
            font_size="xs",
            color="gray.500",
            font_weight="bold",
        ),
        rx.text(msg["content"], white_space="pre-wrap"),
        padding="12px",
        border_radius="12px",
        background=rx.cond(is_user, "blue.100", "gray.100"),
        max_width="80%",
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("🐱 Reflex AI Chat", size="lg"),
                rx.spacer(),
                rx.button(
                    "Clear",
                    on_click=ChatState.clear,
                    size="sm",
                    variant="outline",
                ),
                width="100%",
            ),
            rx.box(
                rx.vstack(
                    rx.foreach(ChatState.messages, message_bubble),
                    spacing="3",
                    align="stretch",
                    width="100%",
                ),
                height="500px",
                overflow_y="auto",
                padding="10px",
                border="1px solid",
                border_color="gray.200",
                border_radius="8px",
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="說點什麼...",
                    value=ChatState.user_input,
                    on_change=ChatState.set_input,
                    on_key_down=lambda key: rx.cond(
                        key == "Enter", ChatState.send, rx.noop()
                    ),
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
            padding_y="20px",
        ),
        max_width="700px",
    )


app = rx.App()
app.add_page(index, route="/")
