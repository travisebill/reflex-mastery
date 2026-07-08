---
name: reflex-ai-integration
description: >
  Reflex app 整合 AI SDK：minimax / OpenAI / Anthropic / Ollama。
  含 streaming response + token cost control + context window 管理 + function calling。
  Use when 在 Reflex app 內用 LLM、寫 chat app、cost 控制、streaming UI。
  Load when user asks to integrate AI/LLM, build chat app, mentions
  minimax / OpenAI / Claude / Ollama, or discusses tokens / cost.
---

# Reflex AI Integration

> 4 個 LLM provider × Reflex 全端 = 完整 AI app 開發指南

---

## 🎯 何時用

- ✅ 在 Reflex app 內呼叫 LLM（chat / completion / embedding）
- ✅ Streaming response UI（打字機效果）
- ✅ Token 計數 + cost 控制（per-user quota / daily cap）
- ✅ Context window 管理（truncation / summary / vector store）
- ✅ Function calling（如 provider 支援）
- ✅ Multi-model comparison（A/B test 不同 LLM）

❌ **不適用於**：
- 純前端 JS 整合（用 React/Vue 自己的 SDK）
- 非 LLM 的 AI（傳統 ML / 影像辨識）— 走其他 skill

---

## 📚 References

| Topic | URL |
|-------|-----|
| minimax 整合（主人預設） | [references/minimax.md](./references/minimax.md) |
| OpenAI 整合（GPT-4o / o1 / o3） | [references/openai.md](./references/openai.md) |
| Anthropic 整合（Claude 3.5/4） | [references/anthropic.md](./references/anthropic.md) |
| Ollama 本地模型 | [references/ollama.md](./references/ollama.md) |
| Streaming Response | [references/streaming.md](./references/streaming.md) |
| Token Cost Control | [references/cost-control.md](./references/cost-control.md) |
| Context Window 管理 | [references/context-window.md](./references/context-window.md) |

---

## 🛠 Scripts

| Script | 用途 |
|--------|------|
| `scripts/setup_ai_provider.sh` | 設定 API key env + 驗證連線 |
| `scripts/estimate_cost.sh` | 估算 token 用量 + cost 預估 |
| `scripts/test_streaming.py` | 測試 4 provider streaming 是否正常 |

---

## 🎯 4 Provider 速查

| Provider | 主人常用 | SDK | 預設 model | Cost/1M tokens |
|----------|---------|-----|-----------|----------------|
| **minimax** | ✅ | `minimax-python-sdk` | M2.7 / M3 | ~$0.50 |
| **OpenAI** | - | `openai` | gpt-4o | $2.50-10 |
| **Anthropic** | - | `anthropic` | claude-3-5-sonnet | $3-15 |
| **Ollama** | - | `ollama` (本地) | llama3.1 | $0 (本地) |

---

## ⚡ 最小整合範例（minimax）

### 1. 安裝 SDK

```bash
pip install minimax
```

### 2. State + Event Handler

```python
import reflex as rx
from minimax import Minimax

client = Minimax(api_key=os.environ["MINIMAX_API_KEY"])

class ChatState(rx.State):
    messages: list[dict] = []
    loading: bool = False

    @rx.event
    async def send(self, user_input: str):
        self.loading = True
        self.messages.append({"role": "user", "content": user_input})
        yield  # 立即更新 UI

        response = await client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=self.messages,
        )
        self.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        self.loading = False
```

### 3. UI

```python
def chat_page() -> rx.Component:
    return rx.vstack(
        rx.foreach(ChatState.messages, render_message),
        rx.input(on_submit=ChatState.send),
        width="100%", max_width="600px", margin="auto",
    )
```

詳細：[references/minimax.md](./references/minimax.md)

---

## 🌊 Streaming Response

```python
@rx.event
async def stream_response(self, user_input: str):
    self.messages.append({"role": "user", "content": user_input})
    self.messages.append({"role": "assistant", "content": ""})
    yield

    stream = await client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=self.messages[:-1],  # 排除空的 assistant
        stream=True,
    )

    full = ""
    async for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full += delta
        self.messages[-1] = {"role": "assistant", "content": full}
        yield  # 每個 chunk yield 一次
```

詳細：[references/streaming.md](./references/streaming.md)

---

## 💰 Cost Control Pattern

```python
class CostControlState(rx.State):
    daily_tokens: int = 0
    daily_cap: int = 100_000  # 100k tokens/day per user

    @rx.event
    async def check_quota(self):
        if self.daily_tokens >= self.daily_cap:
            yield rx.toast.error("今日額度用完")
            return
        # ... 繼續處理
```

詳細：[references/cost-control.md](./references/cost-control.md)

---

## 🔌 Multi-Provider 切換

```python
# config.py
PROVIDERS = {
    "minimax": {"client": lambda: Minimax(...), "model": "MiniMax-M2.7"},
    "openai": {"client": lambda: OpenAI(...), "model": "gpt-4o"},
    "anthropic": {"client": lambda: Anthropic(...), "model": "claude-3-5-sonnet"},
    "ollama": {"client": lambda: OpenAI(base_url="http://localhost:11434/v1"), "model": "llama3.1"},
}

class ChatState(rx.State):
    provider: str = "minimax"

    def get_client(self):
        return PROVIDERS[self.provider]["client"]()

    def get_model(self):
        return PROVIDERS[self.provider]["model"]
```

UI 加 dropdown 切換 provider。

---

## 🔗 與其他 sub-skill 關係

- **本 `reflex-deployment`** — AI app 需要 streaming-friendly deploy（WebSocket）
- **本 `reflex-ux-workflow`** — chat UI 設計 → ui-ux-pro-max 出 wireframe
- **本 `reflex-docs-advanced`** — stateful chat 需要進階 state pattern

---

## 📦 範例

完整可跑範例：
- [examples/chat-stream.py](./examples/chat-stream.py) — 單 provider streaming
- `examples/ai-chat-app/`（repo 根目錄）— 4 provider + multi-model 比較
