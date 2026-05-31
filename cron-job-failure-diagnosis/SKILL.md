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

## Pitfalls

- **`(No response generated)`** is the #1 cause of silent failures. The script runs fine, data is collected, but LLM doesn't produce output. Usually transient LLM API issues. Manual trigger usually fixes it.
- When checking logs, compare file sizes: successful runs are ~1900+ bytes, failed `(No response)` runs are ~1450 bytes (just the header + script output, no response).
- Cron jobs run in isolated sessions — they can't access current conversation context. Prompts must be fully self-contained.
- `last_status` only reflects the MOST RECENT run. If a job failed 3 times then succeeded once, `last_status` shows `ok`. Check the output directory for individual run files.
