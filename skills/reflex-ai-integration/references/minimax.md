# minimax 整合（主人預設）

> minimax API + Reflex 完整整合指南

---

## 1. 安裝

```bash
pip install minimax
```

或 `requirements.txt`：
```
minimax>=1.0.16
```

## 2. 設定 API Key

`.env`：
```bash
MINIMAX_API_KEY=your-key-here
```

`rxconfig.py` 或 `config.py`：
```python
import os
from minimax import Minimax

client = Minimax(api_key=os.environ["MINIMAX_API_KEY"])
```

## 3. 最小整合

```python
import reflex as rx
import os
from minimax import Minimax

client = Minimax(api_key=os.environ["MINIMAX_API_KEY"])

class ChatState(rx.State):
    messages: list[dict] = []
    loading: bool = False

    @rx.event
    async def send(self, user_input: str):
        self.loading = True
        self.messages.append({"role": "user", "content": user_input})
        yield

        response = await client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=self.messages,
        )
        self.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        self.loading = False

def chat_page() -> rx.Component:
    return rx.vstack(
        rx.foreach(ChatState.messages, lambda m: rx.text(f"{m['role']}: {m['content']}")),
        rx.input(on_submit=ChatState.send, placeholder="說點什麼..."),
        width="100%", max_width="600px", margin="auto", padding="20px",
    )

app = rx.App()
app.add_page(chat_page, route="/")
```

## 4. 模型選擇

主人目前 Token Plan：
- `MiniMax-M2.7`（預設）
- `MiniMax-M2.7-highspeed`
- `MiniMax-M3`（OpenClaw 用的）

切換 model：
```python
response = await client.chat.completions.create(
    model="MiniMax-M3",  # 改這行
    messages=...,
)
```

## 5. Streaming

```python
@rx.event
async def stream_response(self, user_input: str):
    self.messages.append({"role": "user", "content": user_input})
    self.messages.append({"role": "assistant", "content": ""})
    yield

    stream = await client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=self.messages[:-1],
        stream=True,
    )

    full = ""
    async for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full += delta
        self.messages[-1] = {"role": "assistant", "content": full}
        yield  # 每個 chunk yield 一次
```

詳見 [streaming.md](./streaming.md)

## 6. Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查天氣",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
            },
        },
    }
]

response = await client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[{"role": "user", "content": "台北天氣？"}],
    tools=tools,
    tool_choice="auto",
)

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        if tool_call.function.name == "get_weather":
            result = await weather_api.get(args["city"])
            # 再次 call model 把 result 給它
            ...
```

## 7. Cost

詳見 [cost-control.md](./cost-control.md)

---

## 🛟 Troubleshooting

### API key 沒設
```
minimax.AuthenticationError: No API key provided.
```
→ 檢查 `.env` 有 `MINIMAX_API_KEY`

### Rate limit
```
minimax.RateLimitError
```
→ 加 retry + backoff

### Timeout
```python
client = Minimax(api_key=..., timeout=30.0)
```

---

## 🔗 延伸

- [openai.md](./openai.md) — OpenAI 整合
- [anthropic.md](./anthropic.md) — Anthropic 整合
- [ollama.md](./ollama.md) — 本地 Ollama
- [streaming.md](./streaming.md) — Streaming 完整指南
