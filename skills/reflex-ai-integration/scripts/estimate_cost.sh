#!/bin/bash
# estimate_cost.sh — 估算 LLM 成本
# Usage: bash scripts/estimate_cost.sh <input_tokens> <output_tokens> <model>

set -e

INPUT_TOKENS="${1:-1000}"
OUTPUT_TOKENS="${2:-500}"
MODEL="${3:-minimax-m2.7}"

# Pricing per 1M tokens (USD)
declare -A PRICING_INPUT=(
    ["minimax-m2.7"]=0.50
    ["minimax-m3"]=1.00
    ["gpt-4o"]=2.50
    ["gpt-4o-mini"]=0.15
    ["claude-3-5-sonnet"]=3.00
    ["claude-3-5-haiku"]=0.80
    ["claude-3-opus"]=15.00
    ["ollama"]=0
)

declare -A PRICING_OUTPUT=(
    ["minimax-m2.7"]=1.00
    ["minimax-m3"]=2.00
    ["gpt-4o"]=10.00
    ["gpt-4o-mini"]=0.60
    ["claude-3-5-sonnet"]=15.00
    ["claude-3-5-haiku"]=4.00
    ["claude-3-opus"]=75.00
    ["ollama"]=0
)

if [ -z "${PRICING_INPUT[$MODEL]}" ]; then
    echo "Unknown model: $MODEL"
    echo "Available: ${!PRICING_INPUT[@]}"
    exit 1
fi

INPUT_RATE=${PRICING_INPUT[$MODEL]}
OUTPUT_RATE=${PRICING_OUTPUT[$MODEL]}

INPUT_COST=$(echo "scale=6, $INPUT_TOKENS / 1000000 * $INPUT_RATE" | bc -l)
OUTPUT_COST=$(echo "scale=6, $OUTPUT_TOKENS / 1000000 * $OUTPUT_RATE" | bc -l)
TOTAL_COST=$(echo "scale=6, $INPUT_COST + $OUTPUT_COST" | bc -l)

# 換算 1k / 10k / 100k / 1M requests
PER_1K=$(echo "scale=4, $TOTAL_COST * 1000" | bc -l)
PER_10K=$(echo "scale=4, $TOTAL_COST * 10000" | bc -l)
PER_100K=$(echo "scale=4, $TOTAL_COST * 100000" | bc -l)
PER_1M=$(echo "scale=2, $TOTAL_COST * 1000000" | bc -l)

echo "=== LLM Cost Estimate ==="
echo "Model: $MODEL"
echo "Input tokens: $INPUT_TOKENS"
echo "Output tokens: $OUTPUT_TOKENS"
echo ""
echo "Per request:"
echo "  Input:  \$${INPUT_COST}"
echo "  Output: \$${OUTPUT_COST}"
echo "  Total:  \$${TOTAL_COST}"
echo ""
echo "At scale (assuming same token count per request):"
echo "  1,000 requests:    \$${PER_1K}"
echo "  10,000 requests:   \$${PER_10K}"
echo "  100,000 requests:  \$${PER_100K}"
echo "  1,000,000 requests: \$${PER_1M}"
