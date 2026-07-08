# AI Chat App Example

> 完整可跑的 Reflex AI Chat — 4 provider + streaming + cost tracker

## 啟動

```bash
cd examples/ai-chat-app/
pip install -r requirements.txt
cp .env.example .env
# 編輯 .env 設 API keys
reflex run
```

## 功能

- ✅ **4 provider 切換**（minimax / OpenAI / Anthropic / Ollama）
- ✅ **Streaming response**（打字機效果）
- ✅ **Conversation history**（記憶上下文）
- ✅ **Token 計數 + cost tracker**（顯示花多少錢）
- ✅ **Multi-model 比較**（同一問題問 2 個 model 並排）
- ✅ **Cancel streaming**（按 Esc 中斷）

## 學到什麼

- ✅ Multi-provider SDK 切換
- ✅ Streaming 完整 pattern
- ✅ Cost 計算
- ✅ Memory 跨 event handler
- ✅ 對話歷史管理

## 結構

```
ai-chat-app/
├── README.md
├── requirements.txt
├── .env.example
├── rxconfig.py
├── ai_chat_app.py     # App 入口
├── states.py          # ChatState
├── providers.py       # 4 provider 抽象
└── cost.py            # 計價邏輯
```
