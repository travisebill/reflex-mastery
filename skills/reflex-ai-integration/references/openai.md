# OpenAI 整合

> OpenAI API（GPT-4o / o1 / o3）+ Reflex 整合

---

## 1. 安裝

```bash
pip install openai
```

## 2. 設定

```python
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

> 用 `AsyncOpenAI` 才有 async，reflex 推薦。

## 3. 最小整合

```python
@rx.event
async def send(self, user_input: str):
    self.loading = True
    self.messages.append({"role": "user", "content": user_input})
    yield

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=self.messages,
    )
    self.messages.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    self.loading = False
```

## 4. 模型選擇

| Model | 用途 | 價格/1M input | 價格/1M output |
|-------|------|---------------|----------------|
| `gpt-4o` | 通用 | $2.50 | $10.00 |
| `gpt-4o-mini` | 便宜 | $0.15 | $0.60 |
| `o1` | 推理 | $15.00 | $60.00 |
| `o3-mini` | 推理便宜 | $1.10 | $4.40 |
| `gpt-4-turbo` | legacy | $10.00 | $30.00 |

## 5. Streaming

```python
stream = await client.chat.completions.create(
    model="gpt-4o",
    messages=self.messages,
    stream=True,
)

async for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    self.messages[-1]["content"] += delta
    yield
```

## 6. Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜尋文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    }
]

response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "搜尋文件"}],
    tools=tools,
)
```

## 7. Vision

```python
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "圖片裡有什麼？"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)
```

## 8. 結構化輸出（JSON mode）

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]

response = await client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "給我蛋糕食譜"}],
    response_format=Recipe,
)
recipe = response.choices[0].message.parsed
```

## 9. Embedding

```python
response = await client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world",
)
embedding = response.data[0].embedding  # 1536-dim vector
```

## 10. Assistant API（持久 thread）

```python
assistant = await client.beta.assistants.create(
    name="My Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o",
)

thread = await client.beta.threads.create()

await client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello",
)

run = await client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# 等待完成
while run.status in ["queued", "in_progress"]:
    run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    await asyncio.sleep(0.5)

messages = await client.beta.threads.messages.list(thread_id=thread.id)
```

## 11. Cost

詳見 [cost-control.md](./cost-control.md)

## 🛟 Troubleshooting

### Rate limit
```python
from openai import RateLimitError
import backoff

@backoff.on_exception(backoff.expo, RateLimitError, max_tries=3)
async def call_openai():
    return await client.chat.completions.create(...)
```

### Token 超限
- 用 `tiktoken` 預先算
- 或壓縮 context（見 [context-window.md](./context-window.md)）

---

## 🔗 延伸

- [minimax.md](./minimax.md) — minimax 整合
- [anthropic.md](./anthropic.md) — Anthropic
- [ollama.md](./ollama.md) — 本地
- [streaming.md](./streaming.md) — Streaming
