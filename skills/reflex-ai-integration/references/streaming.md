# Streaming Response

> 打字機效果 — token-by-token 推送 LLM 回應

---

## 為什麼要 streaming

- ✅ **UX 更好** — 使用者立刻看到「AI 在想」，不用等 30 秒
- ✅ **感覺更快** — TTFT (time-to-first-token) 通常 < 1s
- ✅ **可中斷** — 隨時可以停

---

## 通用 Pattern（適用所有 provider）

```python
class State(rx.State):
    messages: list[dict] = []
    loading: bool = False

    @rx.event
    async def stream_send(self, user_input: str):
        self.loading = True

        # 1. 加入 user message
        self.messages.append({"role": "user", "content": user_input})

        # 2. 預留空的 assistant message（等下 append）
        self.messages.append({"role": "assistant", "content": ""})
        yield  # 立即更新 UI

        # 3. Stream chunks
        try:
            async for chunk in stream_provider(messages=self.messages[:-1]):
                delta = chunk.content or ""
                # 4. 累積到最後一個 message
                current = self.messages[-1]
                self.messages[-1] = {
                    "role": "assistant",
                    "content": current["content"] + delta,
                }
                yield  # 每個 chunk yield 一次 → 持續更新 UI
        finally:
            self.loading = False
```

> ⚠️ **重要**：`yield` 越多越即時，但也越多 WebSocket 流量。token 級 yield 通常太頻繁，**chunk 級**剛好。

---

## minimax Streaming

```python
stream = await client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=self.messages[:-1],
    stream=True,
)

async for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    self.messages[-1]["content"] += delta
    yield
```

---

## OpenAI Streaming

```python
stream = await client.chat.completions.create(
    model="gpt-4o",
    messages=self.messages[:-1],
    stream=True,
)

async for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    self.messages[-1]["content"] += delta
    yield
```

---

## Anthropic Streaming

```python
async with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=self.messages[:-1],
) as stream:
    async for text in stream.text_stream:
        self.messages[-1]["content"] += text
        yield
```

---

## Ollama Streaming

```python
async for chunk in await ollama.AsyncClient().chat(
    model="llama3.1",
    messages=self.messages[:-1],
    stream=True,
):
    delta = chunk["message"]["content"]
    self.messages[-1]["content"] += delta
    yield
```

---

## UI 顯示

```python
def chat_message(msg: dict) -> rx.Component:
    return rx.box(
        rx.text(msg["role"], font_weight="bold"),
        rx.text(msg["content"]),
        padding="10px",
        border_radius="8px",
        background=rx.cond(msg["role"] == "user", "blue.100", "gray.100"),
    )

def chat_page() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.foreach(State.messages, chat_message),
            height="500px", overflow_y="auto",
        ),
        rx.hstack(
            rx.input(
                placeholder="說點什麼...",
                value=State.input,
                on_change=State.set_input,
                flex_grow=1,
            ),
            rx.button(
                "送出",
                on_click=lambda: State.stream_send(State.input),
                is_loading=State.loading,
            ),
        ),
        width="100%", max_width="600px", margin="auto",
    )
```

> ⚠️ 注意：在 streaming 過程中，**整個 chat_page 會 re-render**（因為 messages 變了）。如果效能差：
> - 用 `rx.box` 包固定高度的 scroll area
> - 不要把整個 conversation history 渲染在最外層

---

## 中斷 / 取消

```python
import asyncio

class State(rx.State):
    current_task: asyncio.Task = None
    loading: bool = False

    @rx.event
    async def stream_send(self, user_input: str):
        self.loading = True
        self.messages.append({"role": "user", "content": user_input})
        self.messages.append({"role": "assistant", "content": ""})
        yield

        async def run():
            async for chunk in stream_provider(...):
                self.messages[-1]["content"] += chunk
                yield

        self.current_task = asyncio.create_task(run())
        try:
            await self.current_task
        finally:
            self.loading = False

    @rx.event
    def cancel(self):
        if self.current_task:
            self.current_task.cancel()
        self.loading = False
```

UI 加 cancel button：
```python
rx.button("取消", on_click=State.cancel, is_loading=State.loading)
```

---

## Token 計數 + Streaming

```python
class State(rx.State):
    input_tokens: int = 0
    output_tokens: int = 0

    @rx.event
    async def stream_send(self, user_input: str):
        ...
        async for chunk in stream:
            if chunk.usage:  # OpenAI / Anthropic 在最後 chunk 有 usage
                self.input_tokens = chunk.usage.prompt_tokens
                self.output_tokens = chunk.usage.completion_tokens
            ...
```

---

## 🛟 常見問題

### Stream 卡住
- 檢查 provider 連線
- 加 timeout
- 加 retry + backoff

### Yield 太多造成效能差
- 累積到 N 個 token 才 yield 一次
- 或用 `asyncio.sleep(0.05)` 控制頻率

```python
last_yield = 0
async for chunk in stream:
    self.messages[-1]["content"] += chunk
    if time.time() - last_yield > 0.05:  # 50ms 一次
        yield
        last_yield = time.time()
yield  # 最後一次確保結束狀態
```

### WebSocket 斷線導致 stream 中斷
- 加 reconnect logic
- 顯示 "重新連線中..."

---

## 🔗 延伸

- [minimax.md](./minimax.md)
- [openai.md](./openai.md)
- [anthropic.md](./anthropic.md)
- [ollama.md](./ollama.md)
- [cost-control.md](./cost-control.md) — 計 streaming token
