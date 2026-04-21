---
name: "Cron Job Environment Variable Troubleshooting"
description: Debug and fix cron jobs that appear to succeed but produce no output. Covers why terminal-exported variables don't persist, why ~/.bashrc doesn't help, and how to properly configure env vars in cron jobs.
metadata:
  triggers:
    - cron job not working
    - scheduled task no output
    - environment variable not set in cron
    - export variable lost after closing terminal
    - cron job fails silently
    - skill permission denied
    - cron runs but no output received
---

# Cron Job Environment Variable Troubleshooting

## The Problem

Cron jobs run in **isolated, non-interactive shells** that:
1. Don't inherit environment variables from your terminal
2. Skip `~/.bashrc` (due to early-exit for non-interactive shells)
3. Have an empty/minimal environment

This causes the classic "works in terminal, fails in cron" issue.

## Quick Diagnosis

**Symptoms:**
- `cronjob list` shows `last_status: "ok"` (framework ran)
- No actual output/messages received
- Manual testing works fine
- Problem started after closing terminal

**Test in isolated environment:**
```bash
# This simulates what cron sees:
cd ~/.hermes/skills/skill-name
python3 script.py 2>&1
# Look for: "Error: X must be set in environment"
```

## The Root Cause

```
Terminal Session          Cron Job Session
─────────────────         ─────────────────
export KEY=xxx     ❌    KEY not set
   │                         │
terminal closed              │
   │                         │
   └── variable lost ────────┘
```

Why `~/.bashrc` doesn't help:
- Most `.bashrc` files start with: `case $- in *i*) ;; *) return;; esac`
- This means "if not interactive, exit immediately"
- Cron jobs are non-interactive, so they skip the whole file

## Solution: Embed Variables in Job Prompt

Update the cron job to set variables at runtime:

```bash
cronjob update <job_id> prompt="查询伦敦金价格。

执行步骤：
1. 设置环境变量：export JISU_API_KEY='your-key-here'
2. 切换到目录：cd ~/.hermes/skills/london-gold-cny
3. 运行脚本：python3 london_gold_cny.py
4. 格式化结果并发送到微信"
```

## Verification

After updating, immediately test:
```bash
cronjob run <job_id>
```

Then verify:
- Did you receive the expected message?
- Check `cronjob list` for updated `last_run_at`
- Wait for next scheduled run to confirm automation works

## Pitfall: Stale Credentials in Existing Cronjobs

**Scenario:** You just updated your global API key in `~/.profile`, but your cronjob still uses an old hardcoded key.

**Check for this:**
```bash
cronjob list
```

Look at the `prompt_preview` field - if you see a hardcoded API key there that differs from your new key, the cronjob is using stale credentials.

**Fix:** Update the cronjob with the new key:
```bash
cronjob update <job_id> prompt="查询黄金价格。

执行步骤：
1. 设置环境变量：export JISU_API_KEY='your-NEW-key-here'
2. cd ~/.hermes/skills/gold
3. python3 gold.py london"
```

**Key insight:** Cronjob prompts are snapshots - they don't auto-update when you change global config. Always verify existing cronjobs after rotating API keys.

## Pitfall: Skill File Permission Issues

**Scenario:** Cron job shows `last_status: "ok"` but user reports no notifications received. Manual execution works fine, but scheduled jobs produce no output.

**Symptoms:**
- `cronjob list` shows `last_status: "ok"` 
- Output files exist in `~/.hermes/cron/output/<job_id>/`
- But user receives nothing
- Error logs show: `Permission denied: '/home/agentuser/.hermes/skills/.../SKILL.md'`

**Root Cause:** Some skill files may be owned by `root` with restrictive permissions (e.g., 600). When cron runs as the regular user, it cannot read these files.

**Diagnosis:**
```bash
# Check for root-owned files in skills directory
find ~/.hermes/skills -user root -type f

# Check specific file permissions
ls -la ~/.hermes/skills/<skill-name>/
```

**Common problematic files:**
- `~/.hermes/skills/.bundled_manifest` (can be root-owned after certain updates)
- Skill directories installed via `sudo` or with root privileges
- Files created during system package installations

**Fix:**
```bash
# Change ownership to current user
sudo chown -R $(whoami):$(whoami) ~/.hermes/skills/<problematic-dir>/

# Fix permissions (644 for files, 755 for directories)
chmod 644 ~/.hermes/skills/<problematic-dir>/*.md
chmod 755 ~/.hermes/skills/<problematic-dir>/
```

**Prevention:** Avoid using `sudo` when installing or updating skills. Always check file ownership after any skill installation that might have used elevated privileges.

## Key Insight

> Never rely on terminal-exported variables for cron jobs. Cron runs in fresh sessions. Always include `export VAR=value` in the job prompt itself, or configure the service to load variables from a secure configuration method.

## Related Commands

- `cronjob list` - View all jobs and status
- `cronjob run <id>` - Manually trigger a job
- `cronjob update <id> prompt="..."` - Update job configuration
