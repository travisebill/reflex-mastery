"""cost.py — Token cost 計算"""
PRICING = {
    "minimax-m2.7": {"input": 0.50, "output": 1.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
    "llama3.1": {"input": 0, "output": 0},
}


def calc_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICING.get(model, {"input": 0, "output": 0})
    return (input_tokens / 1_000_000) * p["input"] + (output_tokens / 1_000_000) * p["output"]
