# Cost Control — Token + Money

> 控制 LLM 成本：per-user quota / daily cap / model tier 切換

---

## Token 計數

### 用 tiktoken（OpenAI 精準）

```bash
pip install tiktoken
```

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

### Provider SDK 自帶

```python
# OpenAI
response = await client.chat.completions.create(...)
print(response.usage.prompt_tokens, response.usage.completion_tokens)

# Anthropic
response = await client.messages.create(...)
print(response.usage.input_tokens, response.usage.output_tokens)
```

---

## 成本計算

```python
PRICING = {
    "minimax-m2.7": {"input": 0.50, "output": 1.00},  # per 1M tokens
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
    "ollama": {"input": 0, "output": 0},  # 本地
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICING.get(model, {"input": 0, "output": 0})
    return (input_tokens / 1_000_000) * p["input"] + (output_tokens / 1_000_000) * p["output"]
```

---

## Per-User Quota

```python
class QuotaState(rx.State):
    user_id: str = ""
    daily_input_tokens: int = 0
    daily_output_tokens: int = 0
    daily_cap: int = 100_000  # 100K tokens / day

    @rx.event
    async def check_and_increment(self, input_tokens: int, output_tokens: int) -> bool:
        # 從 DB 讀
        today = datetime.date.today()
        usage = await db.get_usage(self.user_id, today)

        if usage.input_tokens + usage.output_tokens + input_tokens + output_tokens > self.daily_cap:
            yield rx.toast.error("今日額度用完")
            return False

        # 更新 DB
        await db.update_usage(self.user_id, today, input_tokens, output_tokens)
        return True

    @rx.event
    async def ask_ai(self, prompt: str):
        # 1. 預估 input tokens
        input_tokens = count_tokens(prompt)

        # 2. 檢查 quota
        ok = await self.check_and_increment(input_tokens, 0)
        if not ok:
            return

        # 3. Call AI
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        # 4. 累積實際使用
        actual_input = response.usage.prompt_tokens
        actual_output = response.usage.completion_tokens
        await self.check_and_increment(0, actual_output)  # 補扣 output
```

DB schema：
```sql
CREATE TABLE usage (
    user_id TEXT,
    date DATE,
    input_tokens INT,
    output_tokens INT,
    PRIMARY KEY (user_id, date)
);
```

---

## Model Tier 切換（依複雜度）

```python
def select_model(prompt: str, history: list) -> str:
    # 簡單任務用便宜 model
    if len(prompt) < 100 and not history:
        return "gpt-4o-mini"  # 簡單問答
    # 中等任務用中價
    elif len(prompt) < 1000:
        return "gpt-4o"  # 一般對話
    # 複雜任務用最強
    else:
        return "claude-3-5-sonnet"  # 推理 / 長文
```

或讓使用者自選：
```python
class State(rx.State):
    model: str = "gpt-4o-mini"  # 預設便宜

# UI: dropdown 讓使用者切
rx.select(
    ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"],
    value=State.model,
    on_change=State.set_model,
)
```

---

## Prompt Compression

減少 input tokens 來省錢：

### 1. 截斷 history

```python
MAX_HISTORY_TOKENS = 4000

def trim_history(messages: list, max_tokens: int = MAX_HISTORY_TOKENS) -> list:
    """保留 system + 最近對話，截斷中間"""
    if not messages:
        return messages

    system = messages[0] if messages[0]["role"] == "system" else None
    rest = messages[1:] if system else messages

    # 從最新往前加，加到超 token 為止
    trimmed = []
    total = 0
    for msg in reversed(rest):
        tokens = count_tokens(msg["content"])
        if total + tokens > max_tokens:
            break
        trimmed.insert(0, msg)
        total += tokens

    return ([system] if system else []) + trimmed
```

### 2. Summary 舊對話

```python
@rx.event
async def maybe_summarize(self):
    if self.total_tokens > 10000:
        # 用便宜 model 摘要
        summary = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "請把以下對話摘要成 200 字內"},
                *self.messages,
            ],
        )
        self.messages = [
            {"role": "system", "content": f"以下是對話摘要：{summary.choices[0].message.content}"},
            self.messages[-1],  # 保留最新一輪
        ]
```

### 3. Vector Store 檢索

對長文件 QA：
- 切成 chunks
- Embedding 存 vector DB
- Query 時只取 top-K 相關 chunks

```python
import chromadb

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("docs")

@rx.event
async def ask_with_context(self, question: str):
    # 1. Retrieve top 5 relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=5,
    )
    context = "\n\n".join(results["documents"][0])

    # 2. Build prompt
    prompt = f"""根據以下資料回答問題：

{context}

問題：{question}
"""

    # 3. Call AI
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
```

---

## Budget Alert

```python
class State(rx.State):
    monthly_cost: float = 0.0
    monthly_budget: float = 100.0  # $100/月

    @rx.event
    async def alert_if_over(self):
        if self.monthly_cost > self.monthly_budget * 0.8:  # 80% 警告
            yield rx.toast.warning(f"已用 80% 月度預算 (${self.monthly_cost:.2f})")
        if self.monthly_cost > self.monthly_budget:
            yield rx.toast.error(f"已超過月度預算 (${self.monthly_cost:.2f})")
            return False
        return True
```

---

## 🛟 預防爆量

- [ ] 預設用便宜 model
- [ ] 設 per-user daily cap
- [ ] 設 monthly budget + alert
- [ ] 壓縮 history（不傳整個對話）
- [ ] Stream + 中斷（防止無窮生成）
- [ ] 監控 dashboard（每日成本）

---

## 🔗 延伸

- [streaming.md](./streaming.md) — Streaming
- [context-window.md](./context-window.md) — 壓縮 context
- [minimax.md](./minimax.md)
