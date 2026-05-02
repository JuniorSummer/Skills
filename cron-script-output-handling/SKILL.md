---
name: cron-script-output-handling
description: Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出
tags: [cron, script, wakeAgent, feishu, push]
---

# Cron Job 脚本输出处理模式

## 问题场景

当 cron job 配置了 `script` 字段时，系统会：
1. 执行脚本
2. **默认将脚本输出发送给 LLM 处理**
3. LLM 处理后的输出发送到目标（飞书等）

**问题**：LLM 可能会重新格式化输出，导致：
- 省略部分信息（如具体价格数字）
- 添加/修改内容（添加摘要等）
- 格式变化

## 解决方案

在脚本的最后一行添加 `{"wakeAgent": false}`，这会告诉 cron 系统：
- 跳过 LLM 处理
- **直接发送脚本的原始输出**到目标

### 示例：修复黄金价格推送缺少价格数字

```python
# 原脚本最后
if __name__ == "__main__":
    data = get_gold_price()
    message = format_feishu_message(data)
    print(message)  # 输出会被 LLM 处理，可能丢失具体价格

# 修复后
if __name__ == "__main__":
    data = get_gold_price()
    message = format_feishu_message(data)
    print(message)
    print("{\"wakeAgent\": false}")  # 跳过 LLM，直接发送原始输出
```

## 方案二：Prompt 指令法

当脚本输出不适合直接发送（需要一定格式化但不希望 LLM 自由发挥），可以在 cron job 的 `prompt` 中添加明确指令：

```
直接输出下面的数据，不要做任何分析、总结或解释。如果数据格式有问题才报告错误。
```

### 创建 cron job 示例

```python
cronjob(
    action="create",
    name="数据推送",
    schedule="0 22 * * 0",
    script="sync_data.py",  # 脚本输出会注入到 prompt 中
    prompt="直接输出下面的数据，不要做任何分析、总结或解释。如果数据格式有问题才报告错误。"
)
```

### 两种方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| `wakeAgent: false` | 完全跳过 LLM，零成本 | 无法格式化、无错误处理 |
| Prompt 指令法 | LLM 可做格式化/错误处理 | 仍有 token 消耗，LLM 可能偶尔添加多余内容 |

## 使用场景

| 场景 | 方法 |
|------|------|
| 简单数据推送（如天气、股价） | 添加 `{"wakeAgent": false}` |
| 脚本输出需要轻微格式化或错误处理 | Prompt 指令法 |
| 需要 LLM 分析/总结的数据 | 保留默认行为 |
| 需要 LLM 格式化但信息丢失 | 修复脚本或调整 prompt |

## 相关技能

- `cron-dup-messages`：处理重复推送问题
- `time-restricted-cron`：创建时间限制的定时任务