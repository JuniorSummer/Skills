---
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
