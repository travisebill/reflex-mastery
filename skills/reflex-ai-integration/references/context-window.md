# Context Window 管理

> 超過 model context window 怎麼辦？truncation / summary / vector store / sliding window

---

## 各 model context window

| Model | Context | 適合 |
|-------|---------|------|
| `gpt-4o-mini` | 128K | 通用 |
| `gpt-4o` | 128K | 通用 |
| `claude-3-5-sonnet` | 200K | 長文 |
| `minimax-m2.7` | 200K+ | 長文 |
| `llama3.1:8b` | 128K | 通用 |

> 1 token ≈ 0.75 英文單字 / 1.5 中文字

---

## 為什麼要管理

- ❌ 超過 window → 報錯或被截斷
- 💸 越長 context 越貴（input token 計費）
- 🐌 越長 response 越慢

---

## 策略 1：Sliding Window（最簡單）

```python
def sliding_window(messages: list, max_messages: int = 20) -> list:
    """只保留最近 N 則對話"""
    if messages[0]["role"] == "system":
        return [messages[0]] + messages[-(max_messages-1):]
    return messages[-max_messages:]
```

**優點**：簡單  
**缺點**：忘記早期 context

---

## 策略 2：Token-based Truncation

```python
def trim_to_token_limit(messages: list, max_tokens: int = 8000) -> list:
    if not messages:
        return messages

    system = messages[0] if messages[0]["role"] == "system" else None
    rest = messages[1:] if system else messages

    trimmed = []
    total = count_tokens(system["content"]) if system else 0

    # 從最新往舊加，加到上限為止
    for msg in reversed(rest):
        msg_tokens = count_tokens(msg["content"])
        if total + msg_tokens > max_tokens:
            break
        trimmed.insert(0, msg)
        total += msg_tokens

    return ([system] if system else []) + trimmed
```

---

## 策略 3：Summary（用 AI 摘要舊對話）

```python
@rx.event
async def maybe_summarize(self):
    total = sum(count_tokens(m["content"]) for m in self.messages)

    if total < 5000:  # 還沒超
        return

    # 保留 system + 最後 2 則
    system = self.messages[0] if self.messages[0]["role"] == "system" else None
    recent = self.messages[-2:]

    # 中間的用 AI 摘要
    middle = self.messages[1:-2] if system else self.messages[:-2]

    summary_response = await client.chat.completions.create(
        model="gpt-4o-mini",  # 用便宜 model
        messages=[
            {"role": "system", "content": "把以下對話摘要成 200 字內，保留關鍵決策和事實"},
            {"role": "user", "content": "\n".join(f"{m['role']}: {m['content']}" for m in middle)},
        ],
    )
    summary = summary_response.choices[0].message.content

    # 重建 messages
    new_messages = []
    if system:
        new_messages.append(system)
    new_messages.append({
        "role": "system",
        "content": f"以下是對話早期摘要：\n{summary}",
    })
    new_messages.extend(recent)

    self.messages = new_messages
```

---

## 策略 4：Vector Store RAG

對**長文件 QA**（RAG 模式）：

```python
import chromadb
from openai import AsyncOpenAI

client = AsyncOpenAI()
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("docs")

# === 索引文件 ===
async def index_document(text: str, doc_id: str):
    # 切 chunks
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    # Embedding
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks,
    )
    embeddings = [e.embedding for e in response.data]

    # 存 vector DB
    collection.add(
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"doc_id": doc_id} for _ in chunks],
    )

# === Query ===
@rx.event
async def ask_with_rag(self, question: str):
    # 1. Embed question
    q_emb = await client.embeddings.create(
        model="text-embedding-3-small",
        input=question,
    )

    # 2. Retrieve top 5
    results = collection.query(
        query_embeddings=[q_emb.data[0].embedding],
        n_results=5,
    )
    context = "\n\n---\n\n".join(results["documents"][0])

    # 3. Build prompt
    prompt = f"""根據以下文件回答問題。如果文件沒有相關資訊，回答「我不知道」。

文件：
{context}

問題：{question}
"""

    # 4. Call LLM
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
```

**優點**：scale 到 1M+ tokens  
**缺點**：需要維護 vector DB

---

## 策略 5：分塊 + 多次 call

對超長摘要（100K+ tokens）：

```python
async def summarize_long_text(text: str) -> str:
    chunks = [text[i:i+50000] for i in range(0, len(text), 50000)]

    # 每塊先摘要
    chunk_summaries = []
    for chunk in chunks:
        r = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"摘要這段：\n{chunk}"}],
        )
        chunk_summaries.append(r.choices[0].message.content)

    # 再把所有摘要合併摘要
    combined = "\n\n".join(chunk_summaries)
    final = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"整合摘要：\n{combined}"}],
    )
    return final.choices[0].message.content
```

**Map-Reduce pattern**：分散 → 處理 → 聚合

---

## 策略選擇決策

```
text length?
├─ < 1K tokens
│  └─ 直接傳
├─ 1K-10K
│  └─ Sliding window / Token trim
├─ 10K-50K
│  └─ Summary 策略
├─ 50K-200K
│  └─ Vector Store RAG
└─ > 200K
   └─ Map-Reduce + RAG
```

---

## 🛟 監控

```python
@rx.event
async def track_context_size(self):
    total = sum(count_tokens(m["content"]) for m in self.messages)
    self.context_tokens = total

    if total > 100_000:  # 警告
        yield rx.toast.warning(f"Context {total} tokens，建議清理")
```

---

## 🔗 延伸

- [streaming.md](./streaming.md)
- [cost-control.md](./cost-control.md)
- [minimax.md](./minimax.md) — minimax 有 200K context
- [anthropic.md](./anthropic.md) — Claude 3.5 有 200K context
