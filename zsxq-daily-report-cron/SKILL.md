---
name: zsxq-daily-report-cron
description: "创建知识星球每日日报定时任务的完整方案。使用 zsxq-cli 采集前一天的主题和评论，通过 Python 脚本预处理后注入 cron prompt，由 LLM 整理成日报并发送到飞书。当需要设置知识星球内容监控、日报、周报等定时推送任务时使用。"
source: self-generated
---

# 知识星球每日日报定时任务

## 适用场景

- 为某个知识星球创建每日/每周内容日报，自动推送到飞书/微信
- 需要采集星球主题 + 评论 + 去重对比前日报告
- zsxq-cli 已安装且已登录

## 关键架构

```
Python采集脚本 (script字段)
  → 调用 zsxq-cli 拉取主题+评论 (subprocess)
  → 按日期筛选、去重、读取前日报告
  → 输出 JSON 到 stdout
      ↓ (自动注入 cron prompt)
LLM 分析 JSON
  → 整理成结构化日报
  → 保存 .md 文件到工作目录
  → 输出日报正文 (自动发送飞书)
```

## zsxq skill 安装位置（重要）

通过 `npx skills add` 安装的 zsxq skill 位于 `~/.agents/skills/zsxq/`，**不在** Hermes 的 `~/.hermes/skills/` 目录中。因此 `skill_view(name="zsxq")` 找不到它。

正确做法：直接用 `read_file` 读取 `~/.agents/skills/zsxq/SKILL.md` 及其 `references/` 子目录。

## zsxq-cli 关键命令

```bash
# 主题列表（JSON，含分页）
/usr/bin/zsxq-cli group +topics --group-id <ID> --limit 30 --json
# 翻页：用上页返回的 next_end_time 作为 --end-time
/usr/bin/zsxq-cli group +topics --group-id <ID> --limit 30 --json --end-time "2026-08-08T10:00:00.000+0800"

# 主题详情
/usr/bin/zsxq-cli topic +detail --topic-id <ID>

# 评论列表
/usr/bin/zsxq-cli api call get_topic_comments --params '{"topic_id":"<ID>","limit":30}'
```

### 分页去重陷阱
`--end-time` 包含等于，翻页时上一页最后一条会作为下一页第一条重复返回。**必须按 topic_id 去重**。

### zsxq 时间格式
`2026-08-08T20:40:12.666+0800`，Python 解析需截断微秒到6位或用 strptime fallback：
```python
clean = time_str[:26] + time_str[29:] if len(time_str) > 29 else time_str
datetime.fromisoformat(clean)
```

### 日期筛选
zsxq-cli 的 `group +topics` 没有起始时间参数，只有上界 `--end-time`。需要在 Python 脚本中按 `create_time` 客户端筛选。翻页时检查每页最早主题是否已早于目标日期，是则停止。

## auth login 的后台处理

`zsxq-cli auth login` 会阻塞等待用户在浏览器授权，终端前台会超时。解决方案：
1. 后台运行：`terminal(background=true)` + `notify_on_complete=true`
2. 将输出重定向到文件，然后读取链接和确认码给用户
3. 用户完成授权后，进程自动返回成功

## 采集脚本模板要点

参考 `~/.hermes/scripts/fetch_zsxq_data.py`，关键逻辑：

1. **时间计算**：用 `datetime.now(CST)` 获取当前时间，`now - timedelta(days=1)` 得到前一天
2. **主题筛选**：遍历每条 topic，检查 `create_time` 是否落在前一天 00:00~23:59
3. **星主识别**：`owner.name == "星主名"` 或 `owner.user_id == "星主ID"`
4. **合伙人识别**：`owner.description` 含"嘉宾"或"合伙人"
5. **评论筛选**：同样按 `create_time` 过滤，只统计前一天的评论
6. **去重准备**：读取前一天的日报文件（`居丽叶日报_YYYY-MM-DD.md`），截取前3000字作为 `prev_report_excerpt` 注入 prompt
7. **输出 JSON**：包含 stats、owner_topics、other_topics、owner_comments、prev_report_excerpt

## Cron Job 配置

```json
{
  "schedule": "0 7 * * *",
  "deliver": "feishu",
  "script": "fetch_zsxq_data.py",
  "workdir": "/root/zsxq-reports",
  "enabled_toolsets": ["terminal", "file"],
  "prompt": "<LLM分析指令，包含数据说明、去重规则、日报格式、执行步骤>"
}
```

### Prompt 关键指令
- 告诉 LLM 数据是 JSON 格式，各字段含义
- 去重规则：按 topic_id 和话题相似度排除重复
- 飞书格式：纯文本+列表，不用 markdown 表格（飞书不支持）
- 输出要求：直接输出日报正文，不加前言
- 保存要求：用 terminal/write_file 保存 .md 到工作目录

## 注意事项

- zsxq-cli 绝对路径 `/usr/bin/zsxq-cli`，不要直接用 `zsxq-cli`（cron 环境可能 PATH 不同）
- 采集脚本放在 `~/.hermes/scripts/` 下（cron job 的 script 字段默认在此目录查找）
- 日报 .md 文件保存在 `workdir` 指定的工作目录（如 `/root/zsxq-reports/`）
- 限流（429）：在脚本中对每个 API 调用加 try/except，失败时跳过继续
- 内容中的 zsxq 特殊标记（`<e type="web" .../>`）和 URL 编码链接需在 prompt 中要求 LLM 清理
