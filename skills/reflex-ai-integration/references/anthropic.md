# Anthropic 整合（Claude）

> Anthropic Claude API + Reflex 整合

---

## 1. 安裝

```bash
pip install anthropic
```

## 2. 設定

```python
import os
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
```

## 3. 最小整合

```python
@rx.event
async def send(self, user_input: str):
    self.loading = True
    self.messages.append({"role": "user", "content": user_input})
    yield

    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=self.messages,  # 注意：Anthropic 不接受 system role in messages
    )
    self.messages.append({
        "role": "assistant",
        "content": response.content[0].text,
    })
    self.loading = False
```

> ⚠️ Anthropic 跟 OpenAI 不同：system prompt 是獨立參數，不在 messages 裡。

## 4. System Prompt

```python
response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="你是一個專業的助手，回答要簡潔。",  # 系統 prompt
    messages=[{"role": "user", "content": "你好"}],
)
```

## 5. 模型選擇

| Model | 用途 | 價格/1M input | 價格/1M output |
|-------|------|---------------|----------------|
| `claude-3-5-sonnet-20241022` | 通用 + 推理 | $3.00 | $15.00 |
| `claude-3-5-haiku-20241022` | 便宜快速 | $0.80 | $4.00 |
| `claude-3-opus-20240229` | 最強 | $15.00 | $75.00 |

## 6. Streaming

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

## 7. Tool Use（function calling）

```python
tools = [
    {
        "name": "get_weather",
        "description": "查天氣",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
            },
            "required": ["city"],
        },
    }
]

response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "台北天氣？"}],
)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = await weather_api.get(tool_use.input["city"])

    # 把 tool result 回給 Claude
    messages = [
        {"role": "user", "content": "台北天氣？"},
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                }
            ],
        },
    ]
    final = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
```

## 8. Vision

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "圖片裡有什麼？"},
            ],
        }
    ],
)
```

## 9. Prompt Caching（省錢）

```python
response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "你是客服助手，這份文件是你的知識庫...",
            "cache_control": {"type": "ephemeral"},  # 標記可快取
        }
    ],
    messages=[{"role": "user", "content": "問題"}],
)
```

> Prompt caching：第二次 call 起 cache 命中，input 成本降 90%

## 10. Cost

詳見 [cost-control.md](./cost-control.md)

## 🛟 Troubleshooting

### Rate limit
Anthropic 用 token bucket 限流：
```python
from anthropic import APIStatusError
import asyncio

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_claude():
    return await client.messages.create(...)
```

### Long context (200K)
- Claude 3.5 Sonnet 支援 200K context
- 但成本高，要分頁（見 [context-window.md](./context-window.md)）

---

## 🔗 延伸

- [minimax.md](./minimax.md)
- [openai.md](./openai.md)
- [ollama.md](./ollama.md)
- [streaming.md](./streaming.md)
