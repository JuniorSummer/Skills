---
name: cron-dup-messages
description: Debug and fix duplicate cron job message推送问题 - 当定时任务同时发送重复消息时，分析并修复配置冲突
tags: [cron, debug, feishu, push]
---
# Cron Job 重复推送消息问题排查与修复

## 问题症状
- 定时任务推送有时收到2条消息，有时只有1条
- 消息内容相同或相似

## 根因分析
检查 cron job 配置中是否**同时存在 prompt 和 script**：

```json
{
  "id": "xxx",
  "prompt": "让 LLM 执行某个脚本...",
  "script": "some_script.py"
}
```

当两者同时存在时，执行路径有两条：
1. **prompt路径**: LLM 执行 prompt 中的命令 → 推送消息
2. **script路径**: 系统直接执行 script → 推送消息

有时两条路径都成功 → 收到2条
有时只有一条成功 → 收到1条

## 修复方案
清空 prompt，只保留 script：

```python
import json
with open('/root/.hermes/cron/jobs.json', 'r') as f:
    data = json.load(f)

for job in data['jobs']:
    if job['id'] == '问题任务的job_id':
        job['prompt'] = ''  # 清空 prompt

with open('/root/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 验证步骤
1. 检查任务配置
2. 手动运行测试：`cronjob action=run job_id=xxx`
3. 观察推送结果

## 预防措施
- 创建 cron job 时，要么用 prompt（让 LLM 处理），要么用 script（直接执行），不要两者同时使用