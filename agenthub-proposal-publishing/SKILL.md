---
name: agenthub-proposal-publishing
description: Use when syncing AgentHub to main or opening its PRs.
source: self-generated
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, github, agenthub, pull-request]
    related_skills: [agenthub-bootstrap]
---

# AgentHub 提案发布

把本地改动发布到 AgentHub 共享仓库（`~/Documents/projects/00-agenthub`）：proposal 分支 → PR → squash merge → 回到 main。

## When to Use（何时用）
用户说「AgentHub 同步到 main」「发布提案」「开个 PR 合进去」，或本地有 proposal 分支、有 `memory/inbox/` 下未发布的候选需要落地。

## 硬规则
- **绝不直推 main**：仓库 `AGENTS.md` 要求从 `proposal/<harness>/...` 分支走 PR 再 squash merge，任何人（含 agent）都不例外。
- 提交信息与 PR 文本默认**简体中文**（仓库约定）。
- 一次提案只讲一件事；记忆候选只新增到 `memory/inbox/`，不直接改 `memory/MEMORY.md` / `memory_summary.md`。
- 凭据不进仓库、不进聊天；token 只从 `~/.hermes/.env` 读，不打印。

## 标准流程

### 1. 看现场
```bash
cd ~/Documents/projects/00-agenthub
git fetch origin && git status --short && git branch --show-current
git log --oneline origin/main..HEAD
```
有与本提案无关的未提交改动 → 先停下问用户，别顺手带走。

### 2. 判断旧提交是否已被取代
```bash
git cherry main <old-branch>          # '+' 只说明「不等价」，不等于「该发布」
git show --stat <sha>                 # 它碰了哪些文件
git log --oneline -1 -- <同一文件>     # main 里是否已被别的提案重做
```
main 已含同主题的新版本（同文件/同章节被后一个 PR 重写）→ **放弃旧提交**。硬解冲突把旧内容重发上去，会把已经改进过的文档倒退。

### 3. 从最新 main 建分支
```bash
git checkout main && git pull --ff-only origin main
git checkout -b proposal/hermes/$(date +%Y%m%d)-<slug>-$(python3 -c "import secrets;print(secrets.token_hex(4))")
```

### 4. 提交前脱敏扫描
**不要写 `if grep ... | head; then`**：管道退出码取自 `head`，永远为真，连干净文件也会被判成「命中」。先把结果收进变量再判空：
```bash
HITS=$(grep -inE "(sk-[a-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|Bearer |password[=:]|token[=:]|api[_-]?key[=:]|cookie)" <files> || true)
[ -n "$HITS" ] && { echo "$HITS"; echo "命中，需人工判断"; } || echo "clean"
```

### 5. 提交并推送
```bash
git add <files> && git commit -m "记忆: <一句话>"     # 或 文档: / 规则:
git push -u origin HEAD
```
推送成功后远端会回一行 `Create a pull request ... by visiting: <url>`，留着给用户兜底。

### 6. 开 PR（无 `gh` CLI 时直接用 API）
```python
POST https://api.github.com/repos/{owner}/{repo}/pulls
{"title": "<中文标题>", "head": "proposal/hermes/...", "base": "main", "body": "<中文正文>"}
```
- 正文按仓库 `.github/pull_request_template.md` 的三段（提案 / 边界 / 验证与回滚）填齐。
- **PR 模板是从 base 分支（main）读的**：改动模板本身时，这次 PR 仍会显示旧模板——正文必须自己写全，别指望页面。
- 同分支已有 open PR 时接口返回 422；先 `GET /pulls?state=open&head={owner}:{branch}` 查一下再建。

### 7. 等可合并状态再合并
- 刚创建的 PR `mergeable=null`（GitHub 异步计算），2~3 秒轮询一次直到非 null；`mergeable=false` 说明有冲突，停下来报告。
```python
PUT https://api.github.com/repos/{owner}/{repo}/pulls/{n}/merge
{"merge_method": "squash", "commit_title": "<中文标题> (#{n})"}
```
- 成功返回 `merged: true` + `sha`。
- 合并后 **GitHub 会自动删远端 proposal 分支**；再调 `DELETE /git/refs/heads/...` 会得到 422 `Reference does not exist` —— 这是正常的，不是失败。

### 8. 收尾与核验
```bash
git checkout main && git pull --ff-only origin main
git log --oneline -2          # 应出现 squash 提交
git branch -d <proposal-branch>
git status --short            # 应为空
```
逐项确认改动真的落在 main 上（文件在不在、章节改没改、约定行有没有），再向用户报告。别只看「接口返回 200」。

## 凭据：Fine-Grained PAT
- 权限：`Contents = Read/Write`、`Pull requests = Read/Write`；`Repository access` 必须包含目标仓库。
- **`GET /user` 返回 200、`GET /repos/{owner}/{repo}` 返回 404 = 仓库没被勾进该 token 的 selected repositories**，不是 scope 问题、也不是仓库不存在。核实：`GET /user/repos?per_page=100&affiliation=owner,collaborator,organization_member` 看目标仓库在不在列表；修复只需在 token 设置里加仓库，**不用重新生成 token**，改完立即生效。
- 写入 `.env`：按行 `startswith("GITHUB_TOKEN=")` 判断/替换。`.env` 里通常已有一条**注释占位** `# GITHUB_TOKEN=ghp_xxx`，用 `text.count("GITHUB_TOKEN=")` 会把它算成「已存在」而漏写真实值。写完 `chmod 600`。
- 用户若在聊天里贴了 token：落盘后提醒去 Regenerate，后续一律从文件读、不打印。

## 自动化闭环
只推 proposal 分支、不建 PR 的自动化（如每日同步脚本）不会让 main 前进，只在本地堆分支。要真同步，必须在推送之后补「建 PR → 等可合并 → squash merge → 删本地分支」三步。
