---
name: llm-technical-comparison
description: Comparative analysis workflow for LLM technical reports - extract parameters, benchmarks, pricing, and unique features from multiple models
tags: [llm, comparison, technical-analysis, benchmark, pricing]
version: 1.0
---

# LLM Technical Comparison Workflow

Systematic approach for comparing multiple LLMs' technical reports, benchmarks, and API pricing.

## When to Use

- Comparing 2+ LLM models for technical capabilities
- Researching model specifications before selection
- Creating comparison reports for Chinese or international LLMs
- Evaluating API costs across providers

## Step 1: Identify Official Sources

### Primary Sources (in order of reliability)

1. **GitHub Official Repositories**
   - Use GitHub API to fetch README.md content
   - Most reliable for recent benchmark data
   ```
   curl -s -H "Accept: application/vnd.github.v3+json" \
     "https://api.github.com/repos/{org}/{repo}/readme"
   ```
   - Base64 decode the `content` field

2. **HuggingFace Model Cards**
   - `https://huggingface.co/{org}/{model}`
   - Contains architecture details, parameter counts

3. **arXiv Papers**
   - Search: `https://arxiv.org/search/?query={model_name}`
   - Technical depth but may be outdated

4. **ModelScope (Chinese models)**
   - `https://modelscope.cn/models/{org}/{model}`
   - PDF access often requires browser - use GitHub as fallback

### Common Model Repositories

| Model | GitHub Repo |
|-------|-------------|
| DeepSeek | deepseek-ai/DeepSeek-V4 |
| Kimi | MoonshotAI/Kimi-K2.5 |
| MiniMax | MiniMax-AI/MiniMax-M2 |
| GLM | THUDM/chatglm* |
| Qwen | QwenLM/Qwen* |

## Step 2: Extract Key Information

### Model Architecture Parameters

Extract these dimensions for comparison:

| Dimension | What to Look For |
|-----------|------------------|
| Architecture | MoE, Dense, Hybrid |
| Total Parameters | Full model size |
| Active Parameters | Per-token activation (MoE only) |
| Expert Count | Number of experts (MoE) |
| Context Length | Max tokens |
| Attention | MLA, MHA, GQA |
| Vocabulary Size | Token count |
| Layers | Depth |

### Benchmark Categories

Standard benchmarks to compare:

**Reasoning & Knowledge:**
- MMLU / MMLU-Pro
- GPQA-Diamond
- AIME (math)
- HLE (with/without tools)

**Coding:**
- SWE-Bench Verified
- Multi-SWE-Bench
- LiveCodeBench
- Terminal-Bench
- HumanEval

**Agent & Tools:**
- τ²-Bench
- GAIA
- BrowseComp

**Long Context:**
- LongBench v2
- AA-LCR

### Cross-Reference Tip

**Benchmark data is often in competitor reports!**
- Kimi README includes DeepSeek scores
- MiniMax README includes GLM, Kimi, DeepSeek comparisons
- Extract all models from one table when available

## Step 3: API Pricing Analysis

### Official Pricing Pages

| Provider | Pricing URL |
|----------|-------------|
| DeepSeek | platform.deepseek.com/pricing |
| Kimi | platform.moonshot.cn/docs/pricing |
| MiniMax | platform.minimax.io/document/guides/pricing |
| GLM | open.bigmodel.cn/pricing |
| Qwen | help.aliyun.com/document_detail/*.html |

### Pricing Dimensions

- Input token cost (per million)
- Output token cost (per million)
- Thinking mode surcharge
- Long context surcharge
- Free tiers / trials
- Token packages vs pay-as-you-go

### Cost Calculation Example

```python
# Single call cost (10K input + 5K output)
def calc_cost(input_price, output_price):
    return (10_000 * input_price / 1_000_000) + (5_000 * output_price / 1_000_000)
```

## Step 4: Technical Feature Extraction

### Unique Features to Identify

Look for proprietary innovations:

- **Attention mechanisms**: MLA (DeepSeek, Kimi), GQA, etc.
- **Training approach**: Continual pretraining, RL stages
- **Multimodal**: Native vision support vs bolted-on
- **Agent capabilities**: Tool calling, swarm architectures
- **Thinking modes**: CoT, extended thinking, interleaved
- **Special optimizations**: Coding, math, domain-specific

### Common Technical Patterns

Current trends (2024-2025):
- MoE architecture dominant
- 128K+ context standard
- Thinking mode differentiation
- Agent tool-calling standardized
- MLA for KV cache efficiency

## Step 5: Structure Comparison Report

### Recommended Report Structure

```markdown
# [Models] Technical Comparison

## 1. Parameter Overview (table)
## 2. Unique Technical Features (per model)
## 3. Common Technologies
## 4. Benchmark Comparison (tables by category)
## 5. API Pricing Comparison
## 6. Token/Coding Plans
## 7. Recommendations by Use Case
## 8. Trend Analysis
```

### Comparison Table Format

```
| Metric | Model A | Model B | Model C |
|--------|---------|---------|---------|
| ...    | ...     | ...     | ...     |
```

Use `-` for unavailable data, `*` for estimated values.

## Pitfalls to Avoid

1. **Model naming variations** - K2.5 vs K2.6, M2 vs M2.7
   - Search broadly, use most recent available
   - Note version differences in report

2. **PDF access issues** - ModelScope PDFs often need browser
   - Use GitHub README as primary source
   - Fall back to cached/summarized data

3. **Outdated benchmarks** - Papers lag behind repos
   - Prioritize GitHub README over arXiv
   - Check benchmark dates

4. **Inconsistent naming** - SWE-Bench vs SWE-bench
   - Normalize naming in your tables
   - Keep original names in citations

5. **Missing data** - Not all models test all benchmarks
   - Use `-` for missing, don't extrapolate
   - Compare only where data exists

## Quick Reference: Chinese LLM Ecosystem

| Company | Model Series | Focus |
|---------|--------------|-------|
| DeepSeek | V3, V4 | Cost-efficient, reasoning |
| Moonshot | Kimi K2 | Multimodal, agents |
| MiniMax | M2 | Coding, efficiency |
| Zhipu | GLM-5 | Enterprise, coding |
| Alibaba | Qwen | General purpose |
| Baichuan | Baichuan 4 | Chinese optimization |

## Example: Single-Model Data Extraction

```python
from hermes_tools import terminal
import base64, json

def get_readme(org, repo):
    result = terminal(
        f'curl -s -H "Accept: application/vnd.github.v3+json" '
        f'"https://api.github.com/repos/{org}/{repo}/readme"',
        timeout=30
    )
    data = json.loads(result["output"])
    return base64.b64decode(data["content"]).decode('utf-8')

# Usage
readme = get_readme("MiniMax-AI", "MiniMax-M2")
```

## Verification Checklist

Before finalizing comparison:

- [ ] All models have parameter counts
- [ ] At least 3 benchmark categories compared
- [ ] Pricing data sourced or marked estimated
- [ ] Unique features identified for each model
- [ ] Common patterns summarized
- [ ] Use-case recommendations provided
- [ ] Report date and sources documented
