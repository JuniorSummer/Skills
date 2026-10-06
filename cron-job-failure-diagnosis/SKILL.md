---
name: cron-job-failure-diagnosis
description: Diagnose cron job failures by checking job status, analyzing output logs, and identifying root cause (script vs LLM vs delivery).
source: self-generated
triggers:
  - cron job not sending
  - push notification stopped
  - 定时任务失败
  - 推送没收到
  - cron error
  - scheduled task failing
---

# Cron Job Failure Diagnosis

Systematic approach to diagnose why a scheduled cron job stopped delivering.

## Step 1: Identify the Job

```python
cronjob(action='list')
```

Look for:
- `last_status: "error"` — job failed
- `last_delivery_error` — delivery channel issue (Feishu/Telegram/etc)
- `last_run_at` — when was the last successful run
- `enabled: false` / `state: "paused"` — job was disabled

## Step 2: Check Output Logs

Logs are at `~/.hermes/cron/output/<job_id>/`, each file is a timestamped `.md`:

```bash
ls -la ~/.hermes/cron/output/<job_id>/ | tail -10
```

Read the most recent output files. Each contains:
- **Script Output** — what the pre-run script produced
- **Response** — what the LLM generated

### Common Failure Patterns

| Pattern | Meaning | Fix |
|---------|---------|-----|
| `## Response\n\n(No response generated)` | LLM API failed/transient error | Usually self-resolves; retry with manual trigger |
| Script Output empty or error | Data source down or script bug | Test script manually: `python3 ~/.hermes/scripts/<script>.py` |
| `last_delivery_error` has content | Feishu/Telegram channel issue | Check channel ID, bot permissions |
| `last_status: "ok"` but no message | Silent output (`[SILENT]`) or delivery filtered | Check if prompt logic triggers silence incorrectly |
| `RuntimeError: HTTP 403: ... subscription is required to use Go models` (opencode-go) | Provider/model 配置或订阅失效，全局性故障 | 见下方「Provider 403 全局故障」 |
| `Script gate returned wakeAgent=false — agent skipped` | **不是失败**：脚本门控（无变化时不唤醒 LLM），属正常设计 | 无需处理 |

## Provider 403 全局故障（opencode-go 等）

特征：多个不同任务在同一时段**同时**失败，报同一个 403/subscription 错误 → 是 provider 侧全局问题，不是单个脚本 bug。

排查顺序：

1. 用 python 直接读 config.yaml 的真 key 做 curl 实测（Hermes 会在 tool 输出里把 key 显示成 `sk-xxx...yyy`，不要以为配置坏了）：

```bash
KEY=$(python3 -c "import yaml;print(yaml.safe_load(open('/root/.hermes/config.yaml'))['model']['api_key'])")
curl -s -o /tmp/r.json -w "HTTP %{http_code}\n" -X POST "https://opencode.ai/zen/go/v1/chat/completions" \
 -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
 -H "x-opencode-session: ses_$(openssl rand -hex 12)" \
 -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

opencode.ai 的 zen/go 端点**必须带 `x-opencode-session` 头**，否则返回 400 `MissingSessionID`（这不是 403 的原因）。

2. 看失败的时间边界：`grep -n "OpenCode Go subscription" ~/.hermes/logs/agent.log | head -1` 拿到首次失败时间，和 config.yaml 的 mtime（`stat -c %y`）对比。config.yaml 会在每次 CLI 启动时被重写，mtime 新 ≠ key 被换过。
3. **确认修复**：`cronjob(action='run', job_id=...)` 触发一个任务，约 60-90s 后读 `~/.hermes/cron/output/<job_id>/` 最新的 .md，看有没有 `## Response`（有=恢复）；再 grep agent.log 找 `Job '<id>': delivered to ...` 才算真投递成功。
4. 一批任务同时挂掉后**不会自动重试**，需要逐个 `action='run'` 补跑。

注意：cron 任务的 LLM 调用发生在 **gateway 进程**内（systemd hermes-gateway.service），CLI 能正常对话不等于 cron 能跑通——两者不同进程，要分别实测。

## Step 3: Manual Test

```python
cronjob(action='run', job_id='<job_id>')
```

Wait ~30 seconds, then re-check the latest output file. If it works, the issue was transient.

## Step 4: Test Script Independently

```bash
cd ~/.hermes && python3 scripts/<script_name>.py 2>&1
```

If script works but cron fails → LLM or scheduling issue.
If script fails → fix the script.

## Step 5: Historical Trend Analysis

When user reports "updates aren't happening as expected" but `last_status: "ok"`, check all historical runs:

```bash
ls -la ~/.hermes/cron/output/<job_id>/
```

Then parse every output file to build a trend table:

```python
for f in sorted(os.listdir(output_dir)):
    content = read_file(f)
    scanned = re.search(r'Scanned:\s*(\d+)', content)
    synced = re.search(r'Synced:\s*(\d+)', content)
    pushed = 'Pushed: Yes' in content
```

This reveals:
- **Frequency perception vs reality**: Job may be running perfectly every week, but syncing only 0-2 items → user thinks "infrequent"
- **Silent success**: Job works but delivery channel (WeChat → Feishu) fails silently → user never sees results
- **Zero-sync weeks**: Scanned 0 = nothing changed that week (legitimate, not a failure)

### Key Insight: delivery_error ≠ job failure

## 健康巡检误报：内容标记必须行首锚定

自建巡检脚本用**子串**匹配「脚本报错」时，会把任务 **Prompt 说明文字**一并匹配到（输出 .md 里 Prompt 段与脚本输出同文件存放）：

- prompt 写「忽略抓取日志（开始抓取/✅ 条记录/❌ 解析失败）」→ 含 `❌ 解析失败` 子串
- prompt 写「⚠️ 数据源异常优先披露（…）」→ 含 `⚠️ 数据源异常` 子串

后果：每个跑该脚本的任务**每次都误报**，天天刷屏。修法：**行首锚定 +（必要处）冒号**，例如 `(?m)^\s*❌\s*解析失败`、`(?m)^⚠️\s*数据源异常[：:]`。改完用「已知真实故障的旧输出」+「已知干净的输出」各跑一次做回归。

## 手动补跑会占用「下一档」→ 某天整批推送消失

`cronjob(action='run')` 补跑每日任务后，执行台账可能把这条补跑记在**次日的档期**（executions.scheduled_instant = 明天同一时刻）。调度器 `completed_occurrence()` 见该档期已 completed，**次日跳过不跑**，`next_run_at` 直跳后天。

- 症状：某天早上该批推送集体消失（前一天补跑吃掉了今天的档期）
- 排查：`sqlite3 ~/.hermes/cron/executions.db "select job_id,source,started_at,scheduled_instant from executions order by rowid desc limit 20"`，对比补跑时间 vs scheduled_instant
- 处理：补跑后复查 `next_run_at` 是否被顶到后天，是则改回次日；否则等自然恢复
- 预防：provider 故障先确认恢复再补跑；关键任务配 fallback provider（`fallback_providers: []` = 单点故障必挂，一批任务同时 403 全灭）

## Pitfalls

- **`(No response generated)`** is the #1 cause of silent failures. The script runs fine, data is collected, but LLM doesn't produce output. Usually transient LLM API issues. Manual trigger usually fixes it.
- When checking logs, compare file sizes: successful runs are ~1900+ bytes, failed `(No response)` runs are ~1450 bytes (just the header + script output, no response).
- Cron jobs run in isolated sessions — they can't access current conversation context. Prompts must be fully self-contained.
- `last_status` only reflects the MOST RECENT run. If a job failed 3 times then succeeded once, `last_status` shows `ok`. Check the output directory for individual run files.
- **delivery_error with last_status: "ok"** — the job worked, only notification failed. Fix the delivery channel, not the script. Common with WeChat (`Timeout context manager` error); switch to Feishu.
