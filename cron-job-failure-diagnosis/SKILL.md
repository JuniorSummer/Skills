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
| `RuntimeError: HTTP 401: This API key has expired... Create a new API key in OpenCode Console` | **key 过期**（非订阅、非限流）：opencode 侧作废了这把 key，重登不会续期 | 见下方「Provider key 过期（401 api_key_expired）」 |
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

## Provider key 过期（401 api_key_expired）—— 当天整批推送全灭的头号原因

特征：某天某个时刻起，**所有**走 LLM 的任务连续失败，报同一个 `HTTP 401 ... api_key_expired`；`mode: no-agent` 的任务（脚本 stdout 直投）和 monitor 任务**照常成功** → 可据此判定「不是调度坏了，是 LLM 凭证坏了」。

判定与修复：

1. 找断点：`grep -n "api_key_expired" ~/.hermes/logs/agent.log | head -3`，首条失败时间即 key 失效时刻。
2. 量范围：`sqlite3 ~/.hermes/cron/executions.db "select status,count(*) from executions where started_at like '<今天>%' group by status;"` + `hermes cron doctor`（逐条列 last run failed）。
3. 存活性实测（**不要**用 python yaml，Hermes 自带 python 无 pyyaml；直接解析 .env）：

```bash
KEY=$(grep -E "^OPENCODE_GO_API_KEY=" ~/.hermes/.env | cut -d= -f2- | tr -d '"'"'"' \r); echo "len=${#KEY}"
curl -s -o /tmp/t.json -w "HTTP %{http_code}\n" -X POST "https://opencode.ai/zen/go/v1/chat/completions" \
 -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
 -H "x-opencode-session: ses_$(openssl rand -hex 12)" \
 -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

空 KEY（`len=0`）会伪装成 `Go requires a credential`——那是提取失败，不是 key 坏。

4. key 换新后**不需要重启网关**：agent.log 会出现 `Applied updated .env credentials for opencode-go` + `OpenAI client created (env_credential_refresh)`，随后 `auth.json` 的 credential_pool 条目由 `last_status=exhausted` 变回 `ok`。
5. `fallback_providers: []` = 单点故障，一把 key 过期全灭。想抗这个就配 fallback。

### 验证 cron 是否真恢复：用一次性探头 job（零副作用）

不要拿真实任务试（会真推送、可能动档期）。建一个远期调度、`--deliver local` 的临时 job，手动触发看输出，然后删掉：

```bash
hermes cron create "0 3 1 1 *" "Reply with exactly: CRON-LLM-OK" --name TEMP-probe --deliver local
hermes cron run <id>            # 等下一次 tick（~10-60s）
# 读 ~/.hermes/cron/output/<id>/*.md，出现 '## Response' + 正确内容 = LLM 链路通了
hermes cron remove <id>; rm -rf ~/.hermes/cron/output/<id>
```

判读：输出只有 header+script、`## Response` 下是 `(No response generated)` 或文件仅 ~1350 字节 = 仍失败；正常带 Response 的输出 1900+ 字节。

### 一次性任务（repeat 1/1）失败即永久丢失

one-shot 任务**即便运行失败也照样消耗掉唯一档期**：jobs.json 里 `repeat.completed` +1、`state=completed`、`enabled=false`、`next_run_at=null`。事后 `hermes cron doctor` 里都看不见它（因为已不活跃）。

- 排查时别只看 active 任务：失败当天要 `select job_id,source,started_at,status from executions where started_at like '<今天>%'`，再去 jobs.json 里按 id 捞名字（活跃列表可能已经不显示它了）。
- 补救：同主题若还有 `提前1天/提前7天` 之类的姊妹任务，通常能兜住；没有就只能手动补或重建。

## 手动补跑会占用「下一档」→ 某天整批推送消失

`cronjob(action='run')` 补跑每日任务后，执行台账可能把这条补跑记在**次日的档期**（executions.scheduled_instant = 明天同一时刻）。调度器 `completed_occurrence()` 见该档期已 completed，**次日跳过不跑**，`next_run_at` 直跳后天。

- 症状：某天早上该批推送集体消失（前一天补跑吃掉了今天的档期）
- 排查：`sqlite3 ~/.hermes/cron/executions.db "select job_id,source,started_at,scheduled_instant from executions order by rowid desc limit 20"`，对比补跑时间 vs scheduled_instant
- 处理：补跑后复查 `next_run_at` 是否被顶到后天，是则改回次日；否则等自然恢复
- 预防：provider 故障先确认恢复再补跑；关键任务配 fallback provider（`fallback_providers: []` = 单点故障必挂，一批任务同时 403/401 全灭）
- **先验版本再补跑**：新版手动补跑在台账记 `source='direct'` 且 `scheduled_instant` 为空，而 `completed_occurrence()` 对空 instant 直接返回 False → **不吃档期**（补前后 `next_run_at` 不变）。核实：`sqlite3 ~/.hermes/cron/executions.db "select source,status,scheduled_instant from executions where job_id='<id>' order by rowid desc limit 3"`。空 = 老版本已修，放心补；若是「次日时刻」= 老行为，补后必须把 `next_run_at` 改回次日

## 换环境/迁移后：旧环境的历史报错会被监测当成"新增问题"

迁移（服务器→Mac、微信→飞书）后 jobs.json 会**原样带过旧环境的** `last_status` / `last_delivery_error` / `last_run_at`，而监测器的状态文件（如 `~/.config/cron-health/reported.json`）在新环境是全新的 → 首次巡检把几个月前、早已无关的失败当成新问题刷屏；`hermes cron doctor` 会一直重复报，直到该任务下次运行才自动清。

**鉴别**（不用逐条修）：
1. `last_run_at` 距今 >14 天的 status/delivery 报错，基本都是旧环境残留
2. 看 `origin.platform` vs `deliver`：origin=weixin 但 deliver=feishu:oc_… → 报错里的目标渠道已废弃，报错不再可操作
3. 用 executions.db 核对新环境真实投递：`select job_id,started_at,status,delivery_outcome from executions order by started_at desc limit 20`（`delivered` = 链路正常）
4. 顺手查旧路径残留：`hermes cron doctor` 会报 `workdir not found: /root/xxx`、`script not found` —— 迁移后必然出现

**修法：**
1. 巡检脚本加时效守卫：`last_run_at` 早于 14 天的 status/deliver/fire 不报（未处理项）
2. `"Interrupted by shutdown before terminal completion."` 这类错误 = 进程被外部终止（重启/关机/迁移），**不是任务故障**，只在 `--all` 里列出，不报警
3. 清掉跨环境失效字段：备份 jobs.json 后置 `last_delivery_error=null`
4. 想刷新 `last_status` 就补跑：`hermes cron run <id>`（会真的投递一条，顺便端到端验证）
5. 旧路径 workdir 改成本机路径：`hermes cron edit <id> --workdir <new>`

**验收**：`hermes cron doctor` → `✓ found no issues`；巡检 `--all` → `当前问题 0 项`。

## Pitfalls

- **迁移后必查三类幽灵**：旧环境 last_status/last_delivery_error（污染监测）、旧机器绝对路径 workdir/script（真会坏）、监测状态文件全新（造成误报洪泛）

- **`(No response generated)`** is the #1 cause of silent failures. The script runs fine, data is collected, but LLM doesn't produce output. Usually transient LLM API issues. Manual trigger usually fixes it.
- When checking logs, compare file sizes: successful runs are ~1900+ bytes, failed `(No response)` runs are ~1450 bytes (just the header + script output, no response).
- Cron jobs run in isolated sessions — they can't access current conversation context. Prompts must be fully self-contained.
- `last_status` only reflects the MOST RECENT run. If a job failed 3 times then succeeded once, `last_status` shows `ok`. Check the output directory for individual run files.
- **delivery_error with last_status: "ok"** — the job worked, only notification failed. Fix the delivery channel, not the script. Common with WeChat (`Timeout context manager` error); switch to Feishu.
