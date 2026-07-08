"""providers.py — 4 provider 抽象"""
import os
from minimax import Minimax
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic


def get_client(provider: str):
    if provider == "minimax":
        return Minimax(api_key=os.environ.get("MINIMAX_API_KEY", ""))
    elif provider == "openai":
        return AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    elif provider == "anthropic":
        return AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    elif provider == "ollama":
        return AsyncOpenAI(
            base_url=os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/v1",
            api_key="ollama",
        )


MODELS = {
    "minimax": "MiniMax-M2.7",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "ollama": "llama3.1",
}
