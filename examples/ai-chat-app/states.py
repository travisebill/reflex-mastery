"""states.py — ChatState"""
import reflex as rx
from .providers import get_client, MODELS
from .cost import calc_cost


class ChatState(rx.State):
    messages: list[dict] = []
    user_input: str = ""
    provider: str = "minimax"
    loading: bool = False
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0

    @rx.event
    def set_input(self, v: str): self.user_input = v
    @rx.event
    def set_provider(self, v: str): self.provider = v

    @rx.event
    async def send(self):
        if not self.user_input.strip():
            return

        user_msg = {"role": "user", "content": self.user_input, "provider": self.provider}
        self.messages.append(user_msg)
        self.user_input = ""
        self.loading = True
        yield

        self.messages.append({"role": "assistant", "content": "", "provider": self.provider})
        yield

        try:
            client = get_client(self.provider)
            model = MODELS[self.provider]

            if self.provider == "anthropic":
                stream = await client.messages.stream(
                    model=model,
                    max_tokens=1024,
                    messages=self.messages[:-1],
                )
                async for text in stream.text_stream:
                    self.messages[-1]["content"] += text
                    yield
            else:
                # minimax / OpenAI / Ollama（都用 OpenAI 相容 API）
                sdk_client = client.AsyncClient() if hasattr(client, 'AsyncClient') else client
                stream = await sdk_client.chat.completions.create(
                    model=model,
                    messages=self.messages[:-1],
                    stream=True,
                )
                async for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        self.messages[-1]["content"] += delta
                        yield

            # 估算 cost（簡化版）
            input_estimate = sum(len(m["content"].split()) for m in self.messages[:-1])
            output_estimate = len(self.messages[-1]["content"].split())
            self.total_input_tokens += input_estimate
            self.total_output_tokens += output_estimate
            self.total_cost += calc_cost(model, input_estimate, output_estimate)
        except Exception as e:
            self.messages[-1]["content"] = f"Error: {str(e)}"
            yield rx.toast.error(str(e))
        finally:
            self.loading = False

    @rx.event
    def clear(self):
        self.messages = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
