---
source: self-generated
name: dify-workflow-best-practices
description: Dify 工作流搭建最佳实践，源自多位高分选手的共性提炼。覆盖架构模式、节点选型、Prompt 工程、知识库配置、Code 节点技巧。Use when 搭建或优化 Dify/Coze 等平台的 AI 工作流、智能客服、RAG 应用。
---

# Dify 工作流搭建最佳实践

## 核心公式（高分工作流骨架）

```
Start → [Code预处理] → If-Else(工单/上下文路由)
    ├─ 有数据 → LLM(数据分析) → Answer
    └─ 无数据 → LLM(Query优化) → Question-Classifier(三分类)
                    ├─ QA      → Knowledge-Retrieval → LLM(JSON回答) → Answer
                    ├─ Repair  → LLM(三维度分析) → Answer
                    └─ Chat    → LLM(礼貌回复) → Answer
```

## 一、架构设计原则

### 1. 两级路由引擎（必须）
- **第一级：上下文路由** — `if-else` 判断是否有附加数据（如工单），走分析流程还是对话流程
- **第二级：意图路由** — `question-classifier` 或 LLM 做意图分类，分到 QA/Repair/Chat 三条专线

### 2. 多分支 + 聚合出口
- 每条分支独立处理，最后汇聚到统一的 Answer 节点（通过 `variable-assigner`）
- 或用多个 Answer 节点分别输出（更直观，但架构略散）
- **推荐**：朱兴宇的 pattern — 所有 LLM 输出写 `variable-assigner`，单 Answer 读聚合变量

### 3. 知识库 RAG 配置（一致最优参数）
```yaml
search_method: hybrid_search         # 混合检索
reranking_model: qwen3-rerank        # 重排序模型
top_k: 3                              # 召回数量
weights:
  keyword_weight: 0.3                # 关键词权重
  vector_weight: 0.7                 # 向量权重
```

## 二、节点选型决策树

| 场景 | 用 Code 节点 | 用 LLM 节点 |
|:---|:---|:---|
| 数值校验（阈值范围检查） | ✅ | ❌ 不可靠 |
| 日期/时间生成 | ✅ `datetime.now()` | ❌ 可能编造 |
| 字符串判空/JSON 解析 | ✅ `json.loads()` | ❌ 浪费 token |
| 意图分类 | ❌ 规则写死 | ✅ 语义理解 |
| 查询改写（口语→标准） | ❌ 无法泛化 | ✅ 核心场景 |
| JSON Schema 约束输出 | ❌ | ✅ `response_format: JSON` |
| 知识库结果格式化 | ✅ 去噪/截断 | ❌ 直接喂可能超长 |

### Code 节点黄金用法
```python
# 1. 预处理：阈值校验 + 数据判空 + 日期生成
def main(query, user_id, threshold, ticket_data):
    t = float(threshold) if threshold else 0.5
    t = max(0.0, min(1.0, t))  # 边界保护
    
    # 工单数据判空（兼容 list/dict/str/null）
    has_data = bool(ticket_data) and ticket_data not in (None, "", "null", "[]", "{}")
    
    return {
        "threshold": t,
        "mid_threshold": round(t * 0.6, 4),
        "has_ticket_data": has_data,
        "today": datetime.now().strftime("%Y%m%d")
    }
```

```python
# 2. 知识库召回后处理：格式化为结构化数据再喂 LLM
def main(kb_results: list) -> dict:
    items = []
    for r in kb_results[:3]:  # 只取 top3，控制 token
        items.append({
            "title": r.get("title", ""),
            "content": r.get("content", "")[:500]  # 截断长文本
        })
    return {"kb_items": items, "kb_count": len(items)}
```

## 三、Prompt 工程规范

### 通用三段式模板
```markdown
## Role / 角色
你是一个 [具体领域] 的 [角色名]，负责 [核心职责]。

## Task / 任务
[1-3 条明确的任务描述]

## Constraints / 约束
- [硬性限制条件]
- [输出格式要求]
- [边界情况处理规则]

## Output / 输出格式
严格按照以下 JSON Schema 输出，不包含任何额外文本：
{
  "field1": "类型说明",
  "field2": "枚举值范围"
}
```

### 意图分类 Prompt（必含 Few-shot 示例表）
```markdown
## 意图定义与分类标准
1. QA：OA/VPN/钉钉/网盘/邮箱 相关 FAQ
2. REPAIR：设备损坏、系统故障等需人工介入
3. CHAT：问候、感谢等非业务对话

## 判断优先级
- QA 优先于 CHAT：涉及 IT 系统使用问题，即使语气像闲聊也归 QA
- REPAIR 需确认物理损坏：纯软件问题（崩溃）归 QA

## Few-shot 示例
| 用户Query | 意图 | 理由 |
|:---|:---|:---|
| VPN怎么连？ | QA | 询问使用方法 |
| 电脑开不了机，黑屏 | REPAIR | 硬件故障 |
| 你好，在吗？ | CHAT | 纯问候 |
```

### 结构化 JSON 输出（repair 三维度分析示例）
```json
{
  "answer": "对用户问题的回复",
  "confidence": 0.85,
  "fault_type": "硬件|软件|网络",
  "urgency": "高|中|低",
  "scope": "个人|局部|全局",
  "suggestion": "处理建议",
  "notify_target": "通知部门",
  "need_ticket": true,
  "ticket_id": "TK_20240630_12345"
}
```

## 四、进阶技巧

### 1. 双模型策略
- **意图分类 / JSON 输出**：用 `kimi-k2.5` (temp=0.3) — 遵循指令强，JSON 格式稳定
- **闲聊 / 自由生成**：用 `deepseek-v3.2` (temp=0.7) — 更自然
- 配置方式：在 LLM 节点上分别指定 `model.name` 和 `model.provider`

### 2. 会话级变量（跨轮次复用）
```yaml
conversation_variables:
  currentTime:    # 工作流开始时生成一次，后续轮次复用
  orderId:        # 工单号，一次对话只生成一次
```
通过 `assigner` 节点写入 → 全局引用 `{{#conversation.currentTime#}}`

### 3. Memory 窗口
在意图分类和查询改写节点开启 `memory.window.enabled: true` + `size: 50`，让模型感知对话历史，消解"它"、"这个"等代词。

### 4. parameter-extractor（结构化传参）
```yaml
# 先让 LLM 输出 JSON，再提取为类型化变量
parameters:
  - name: query       # string
  - name: threshold   # number
  - name: ticket_data # string
```
后续节点用 `{{#1781681655267.threshold#}}` 精确引用，避免字符串拼接。

## 五、常见陷阱

1. **不要用 LLM 做数值计算** — 置信度比较、日期格式化一律用 Code 节点
2. **不要直接用 `sys.query` 检索** — 必须先经过查询优化改写
3. **知识库结果不要全量喂 LLM** — 用 Code 节点截断/格式化后再传
4. **Prompt 必须指定输出格式** — 不加 Schema 约束的 JSON 输出大概率格式不一致
5. **if-else 判断工单数据时注意兼容性** — 数据可能是 `null / "" / "[]" / list / dict`，用 Code 节点统一判空
6. **不要在 Prompt 里写 `{{#sys.query#}}` 但不加引号** — 可能破坏 JSON 结构

## 六、检查清单

搭建工作流后逐项验证：
- [ ] 有 Code 节点做输入预处理（阈值/日期/判空）
- [ ] 有两级路由（上下文路由 + 意图路由）
- [ ] 意图分类 Prompt 包含 Few-shot 示例表
- [ ] 每个 LLM 节点的输出格式有明确定义（JSON Schema）
- [ ] 知识库配置：hybrid_search + rerank + top_k=3
- [ ] 查询改写节点在知识库检索之前
- [ ] 不同任务用不同模型（分类用低 temp，闲聊用正常 temp）
- [ ] 边界情况：空输入、异常阈值、无知识库命中 均有兜底逻辑
