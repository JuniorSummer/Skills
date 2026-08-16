---
source: self-generated
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

### 方案三：脚本直接发送（最可靠）

脚本自己通过 lark_oapi 发送消息到飞书，然后只输出 `{"wakeAgent": false}`。完全不依赖 LLM 和 cron 的 delivery 机制。

```python
def load_env():
    """Cron 脚本环境没有 .profile，需要手动加载环境变量。"""
    try:
        with open('/root/.profile', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('export ') and '=' in line:
                    var_part = line[7:]
                    key, _, value = var_part.partition('=')
                    os.environ.setdefault(key, value.strip().strip('"'))
    except Exception:
        pass

def send_to_feishu(message):
    import lark_oapi as lark
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    load_env()  # 关键：cron 上下文缺环境变量
    app_id = os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('FEISHU_APP_SECRET')
    chat_id = os.environ.get('FEISHU_HOME_CHANNEL')
    client = lark.Client.builder().app_id(app_id).app_secret(app_secret).build()
    body = (CreateMessageRequestBody.builder()
        .receive_id(chat_id).msg_type("text")
        .content(json.dumps({"text": message}, ensure_ascii=False)).build())
    req = (CreateMessageRequest.builder()
        .receive_id_type("chat_id").request_body(body).build())
    client.im.v1.message.create(req)

if __name__ == "__main__":
    load_env()
    data = get_gold_price()
    message = format_message(data)
    send_to_feishu(message)
    print('{"wakeAgent": false}')  # 脚本已自行发送，跳过 agent
```

**关键注意点**：
- cron 脚本运行环境不加载 `/root/.profile`，必须手动 `load_env()`
- 用 `/root/.hermes/hermes-agent/venv/bin/python` 调用子脚本（如 london_gold_cny.py），系统 `python3` 可能缺依赖
- 脚本只输出 `{"wakeAgent": false}` 一行，不再输出消息内容（已自行发送）

### 三种方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 脚本直接发送 | 最可靠，完全不依赖 LLM/cron delivery | 需写飞书 API 代码，cron 上下文需手动加载 env |
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