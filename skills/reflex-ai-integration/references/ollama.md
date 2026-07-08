# Ollama 整合（本地模型）

> Ollama 本地 LLM + Reflex 整合 — 完全免費、隱私、離線

---

## 🎯 何時用 Ollama

- ✅ **隱私敏感** — 資料不能出本地（醫療 / 金融 / 法律）
- ✅ **離線** — 沒網路也能跑
- ✅ **省錢** — 長期大量使用比 API 便宜
- ✅ **客製** — 自訓 / fine-tune 模型
- ❌ 不適合：需要最大模型（GPT-4 / Claude 3.5）時

---

## 1. 安裝 Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 下載 https://ollama.com/download
```

啟動 service：
```bash
ollama serve
```

## 2. 拉模型

```bash
# 推薦模型（依照 RAM）
ollama pull llama3.1:8b          # 8B 參數，要 8GB RAM
ollama pull llama3.1:70b         # 70B 參數，要 64GB+ RAM
ollama pull codellama:13b        # 程式專用
ollama pull mistral:7b           # 輕量
ollama pull phi3:mini            # 3.8B 最小
ollama pull gemma2:27b           # Google
```

## 3. 用 OpenAI 兼容 API

Ollama 內建 OpenAI 兼容 endpoint：

```python
import os
from openai import AsyncOpenAI

# 指到 Ollama 本地 server
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不需要真 key
)

@rx.event
async def send(self, user_input: str):
    self.loading = True
    self.messages.append({"role": "user", "content": user_input})
    yield

    response = await client.chat.completions.create(
        model="llama3.1",
        messages=self.messages,
    )
    self.messages.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    self.loading = False
```

> ✅ **好處**：用 OpenAI SDK 寫 code，Ollama 跟 OpenAI 切換**零改 code**

## 4. 用 ollama-python SDK（更原生）

```bash
pip install ollama
```

```python
import ollama

@rx.event
async def send(self, user_input: str):
    self.loading = True
    self.messages.append({"role": "user", "content": user_input})
    yield

    response = await ollama.AsyncClient().chat(
        model="llama3.1",
        messages=self.messages,
    )
    self.messages.append({
        "role": "assistant",
        "content": response["message"]["content"]
    })
    self.loading = False
```

## 5. Streaming

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

## 6. Embedding

```python
response = ollama.embeddings(
    model="nomic-embed-text",
    prompt="Hello world",
)
embedding = response["embedding"]
```

## 7. 在 Reflex app 中檢查 Ollama 可用

```python
import httpx

async def check_ollama() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:11434/api/tags", timeout=2.0)
            return r.status_code == 200
    except:
        return False

class State(rx.State):
    ollama_available: bool = False

    @rx.event
    async def on_load(self):
        self.ollama_available = await check_ollama()
        if not self.ollama_available:
            yield rx.toast.warning("Ollama 未啟動")
```

## 8. 切換 provider（Ollama ↔ OpenAI）

```python
# config.py
import os
from openai import AsyncOpenAI

def get_client(provider: str = "ollama"):
    if provider == "ollama":
        return AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
    elif provider == "openai":
        return AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif provider == "minimax":
        from minimax import Minimax
        return Minimax(api_key=os.environ["MINIMAX_API_KEY"])

class State(rx.State):
    provider: str = "ollama"

    @rx.event
    async def send(self, user_input: str):
        client = get_client(self.provider)
        ...
```

## 9. Model 管理

```bash
# 列出已下載
ollama list

# 刪除
ollama rm llama3.1:70b

# 更新
ollama pull llama3.1
```

## 10. GPU 加速

Ollama 自動用 GPU（Metal / CUDA）：

```bash
# 確認 GPU 偵測
ollama ps

# 強制 CPU
OLLAMA_NUM_GPU=0 ollama serve
```

---

## 🛟 Troubleshooting

### Ollama 沒啟動
```
Connection refused to localhost:11434
```
→ `ollama serve` 開另一個 terminal

### Model 太慢
- 用小一點的 model（`llama3.1:8b` 而非 `70b`）
- 確認 GPU 加速有開
- 關掉其他 GPU 程式

### Memory 不足
- 8B model 要 8GB RAM
- 70B 要 64GB+ RAM
- 用量化版（`llama3.1:8b-q4_0`）

### 輸出品質差
- 本地模型天生比 GPT-4 / Claude 弱
- 重要任務用雲端 API
- 簡單任務（分類 / 摘要 / 翻譯）用本地 OK

---

## 💰 成本比較

| Provider | 1000 requests (avg 1K tokens) | 成本 |
|----------|-------------------------------|------|
| Ollama 8B | - | $0（電力） |
| minimax M2.7 | ~1M tokens | $0.50 |
| GPT-4o | ~1M tokens | $2.50 |
| Claude 3.5 Sonnet | ~1M tokens | $3.00 |

> **長期大量使用 → Ollama 完勝**。但要前期投資硬體（Mac M4 / RTX 4090 / A100）

---

## 🔗 延伸

- [minimax.md](./minimax.md)
- [openai.md](./openai.md)
- [anthropic.md](./anthropic.md)
- [cost-control.md](./cost-control.md) — 雖然免費但要算電力
