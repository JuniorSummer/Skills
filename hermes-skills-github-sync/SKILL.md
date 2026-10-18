---
source: self-generated
name: hermes-skills-github-sync
description: Sync Hermes Agent skills to a GitHub repo with automatic categorization, README generation, and weekly cron job. Self-generated skills at root, pre-installed skills in subfolder.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [github, skills, sync, automation, cron]
    related_skills: [github-repo-management, write-a-skill, cron-script-output-handling]
---

# Hermes Skills GitHub Sync

Sync Hermes Agent's `~/.hermes/skills/` directory to a GitHub repository with automatic categorization and README generation.

## Use When

- User wants to back up or share Hermes skills on GitHub
- Setting up automated weekly skill sync via cron
- Reorganizing a skills repo (e.g., separating self-generated from pre-installed)

## Prerequisites

- SSH key configured for GitHub (`ssh -T git@github.com` works)
- Skills exist in `~/.hermes/skills/`

## Repository Structure

```
repo/
├── README.md                    ← Self-generated + external skills
├── self-generated-skill-1/
├── self-generated-skill-2/
├── external-skill/
└── hermes_raw_skill/            ← Pre-installed/built-in skills
    ├── README.md                ← Categorized listing
    ├── category-skill-1/
    └── category-skill-2/
```

## Steps

### 1. Classify Skills

Determine which skills are self-generated vs built-in:

```python
# Self-generated = created by Hermes in solving problems (check file mtime + session history)
SELF_GENERATED = {"cron-dup-messages", "playwright-scraper", ...}

# External = installed from GitHub/ClawHub
EXTERNAL = {"london-gold-cny"}

# Everything else in ~/.hermes/skills = pre-installed built-in skills
```

**How to identify self-generated skills:**
- Check `find ~/.hermes/skills -name "SKILL.md" -mtime -14` for recent files
- Cross-reference with session_search for `skill_manage create` activities
- Exclude skills that came pre-installed with Hermes Agent

### 2. Sync Script

Location: `~/.hermes/scripts/sync_skills_to_github.py`

Key logic:
1. `git clone` the repo to `/tmp/Skills-sync`
2. Scan `~/.hermes/skills` for SKILL.md modified in last N days
3. Copy to correct location (root for self-generated, `hermes_raw_skill/` for built-in)
4. Skip unchanged files (content comparison)
5. Generate both README files
6. `git add -A && git commit && git push`

**Pitfall: `execute_code` limits** — The `terminal()` function inside `execute_code` uses different return keys than top-level `terminal`. Use top-level `terminal` for complex operations or keep `execute_code` calls under 50.

### 3. README Generation

**Root README.md** — Focus on self-generated skills:
- Table with skill name, description, creation date
- Section for external installs with source link
- Link to `hermes_raw_skill/README.md` for built-in skills

**hermes_raw_skill/README.md** — Categorized listing:
- 17+ categories (AI Agent, Creative, MLOps, DevOps, GitHub, etc.)
- Extract descriptions from YAML frontmatter: `sed -n '/^---$/,/^---$/{ /^description:/s/^description: *//p; }'`
- Category mapping dict for skill→category assignment

### 4. Cron Job

```python
cronjob(
    action="create",
    name="Skills 每周同步到 GitHub",
    schedule="0 22 * * 0",  # Sunday 10 PM
    script="sync_skills_to_github.py",
    prompt="直接输出下面的数据，不要做任何分析、总结或解释。如果数据格式有问题才报告错误。"
)
```

**Important:** Use `prompt` with raw-output instruction (see `cron-script-output-handling` skill) to prevent LLM from adding analysis to script output.

## Pitfalls

1. **`execute_code` tool call limit (50)** — Moving 70+ directories in one script hits the limit. Use `terminal` for bulk file operations instead.
2. **`terminal` return keys** — Inside `execute_code`, terminal returns `{'returncode': ..., 'stdout': ...}` not `{'exit_code': ..., 'output': ...}`. Mix them up → KeyError.
3. **Git rename detection** — `git mv` or moving files then `git add -A` correctly detects renames (preserves history).
4. **SSH vs HTTPS** — Use `git@github.com:user/repo.git` (SSH) for push. HTTPS requires token in URL.
6. **非交互环境（cron/launchd）必须用无密码短语的密钥** —— 症状：抄本报 `Permission denied (publickey)`，但 `ssh -vT` 里明明有 `Server accepts key`，紧接着 `read_passphrase: can't open /dev/tty`。这说明 GitHub **认得**这把密钥，只是它**带密码短语而无人解锁**（agent 空、Keychain 无记录、cron 无 TTY）。排查先看：`ssh-keygen -y -f <key>`（报错=有密码短语）、`ssh-add -l`（空=没解锁）。修法：新建专用无密码密钥 + 仓库 Deploy Key（write） + ssh 别名：
   ```bash
   ssh-keygen -t ed25519 -N "" -C "hermes skills-sync cron (host)" -f ~/.ssh/id_ed25519_skills_sync
   # ~/.ssh/config 加别名（避免影响其他 github 仓库的密钥选择）
   # Host github-skills-sync / HostName github.com / User git
   #   IdentityFile ~/.ssh/id_ed25519_skills_sync / IdentitiesOnly yes
   ```
   然后把脚本的 `REPO_URL` 改成 `git@github-skills-sync:Owner/Repo.git`，公钥加到 `https://github.com/Owner/Repo/settings/keys`（Deploy key，勾选 Allow write access）。
7. **迁移/换主机后同步必挂**：旧机器的密钥/agent 不会跟过来；检查 `~/.ssh/config` 里有没有裸 `github.com` 的 Host 块（只有别名不算），以及有没有默认名密钥（`id_ed25519`/`id_rsa`）——都没有时非交互 clone 必失败。
8. **一个 profile 只留一个同步任务** —— 两个 job 跑同一份脚本、共用 `/tmp/Skills-sync` 时，一个进程的 `rm -rf` 会删掉另一个正在用的 clone：症状是 `could not create work tree dir '/tmp/Skills-sync': File exists`，或另一份跑出假的 `Permission denied (publickey)` / push 失败（脚本 clone 失败才 `sys.exit(1)`，push 失败只打印 ERROR 仍退 0，所以 job 可能显示 ok 而内容是报错）。排查：`hermes cron list` 对比各 profile 的 job 名。脚本里工作目录按 pid 隔离（`/tmp/Skills-sync-<pid>`）兜底。
9. **推送类 job 必须放在 default profile** —— 飞书 chat_id 绑定 app，profile 的 FEISHU_HOME_CHANNEL 只对本 profile 的 app 有效：default profile 的 app（cli_aa35，显示名「消息推送」）= 私聊 `oc_30288b066546ba3e239689965f8b37d7`；xiaoxia profile 的 app（cli_a960，夏小虾）home 是私聊 `oc_09adea...`。所以在 xiaoxia profile 里写 `deliver=feishu` 会把定时结果推进「夏小虾」会话，且无法改指「消息推送」。判定哪个对话是哪个 app：`curl -s https://open.feishu.cn/open-apis/bot/v3/info -H "Authorization: Bearer <tenant_token>"` 读 `app_name`。
10. **扫描多个 skill 根目录** —— 只看 `~/.hermes/skills` 会漏掉 `~/.hermes/profiles/<name>/skills` 里 profile 独有的 skill。用 `SKILLS_ROOTS = [~/.hermes/skills] + glob(profiles/*/skills)`，同名 skill 保留 mtime 最新的一份。注意 mtime 窗口机制：从未同步过、且 7 天内没改动的 skill 不会进仓库。
5. **Category uncategorized** — New skills without category mapping default to "productivity". Update `CATEGORY_MAP` when adding new built-in skills.

## Verification

```bash
# Check repo structure
cd /tmp/Skills-sync && ls -d */ | grep -v hermes_raw | grep -v .git
# Should show only self-generated + external + existing skills

# Check hermes_raw_skill count
ls hermes_raw_skill/ | wc -l
# Should be ~78 for full Hermes Agent

# Test sync script
python3 ~/.hermes/scripts/sync_skills_to_github.py

# Verify cron job
# Should show "d236866267c1" or similar
```
