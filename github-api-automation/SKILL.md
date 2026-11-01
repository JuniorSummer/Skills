---
name: github-api-automation
description: 无 gh CLI 时用 GitHub REST API 自动建 PR、合并、清理分支。
version: 1.0.0
author: Hermes Agent
license: MIT
source: self-generated
metadata:
  hermes:
    tags: [github, pull-request, api, squash-merge, pat, automation]
    related_skills: [cron-job-management, hermes-skills-github-sync]
---

# GitHub REST API 自动化（无 gh CLI）

## When to Use / 何时用
- 本机没有 `gh`，但需要脚本化/无人值守地建 PR、合并、清理分支（cron 任务、批量提案、自动同步仓库）。
- 仓库自带「proposal 分支 + PR」约定，要求走 PR 而不能直推 main。
- 想在本机完成 git push 之外的步骤（开 PR、合并、读 PR 状态）。

## 1. 凭据：fine-grained PAT

需要的权限（只勾这些就够）：
- **Contents: Read and write**（建分支、合并写入 main）
- **Pull requests: Read and write**
- Metadata 自动只读

**最容易卡住的一步：Repository access 必须显式包含目标仓库。** 没勾的仓库，API 返回 **404 而不是 403** —— 极易误判成「仓库名写错 / 仓库不存在」，然后去改代码。判别：

```python
# 先看 token 到底能碰哪些仓库
GET /user/repos?per_page=100&affiliation=owner,collaborator,organization_member
# 目标不在列表里 → 是授权范围问题，去 token 设置里加仓库（改范围即时生效，不用重新生成）
```

存放：写进 `~/.hermes/.env` 的 `GITHUB_TOKEN=...`，文件 600。脚本从文件读，不依赖进程环境变量（cron 环境的 env 不可靠）。**永不**写进 prompt、日志、Git、聊天回复。

### 读 .env 的坑：注释占位符
模板里常有 `# GITHUB_TOKEN=ghp_xxxxxx`。用 `line.startswith("GITHUB_TOKEN=")` 判断会误命中；用 `re.sub(r"^GITHUB_TOKEN=.*$", ...)` 替换则**一行都不匹配、静默不写入**（脚本报「已写入」但磁盘没变）。正确写法：

```python
lines = [l for l in open(env).read().splitlines() if not l.startswith("GITHUB_TOKEN=")]
lines.append(f"GITHUB_TOKEN={token}")
open(env, "w").write("\n".join(lines) + "\n")
```
写完后**回读校验**（能取到值且长度合理），不要只看「写入成功」。

## 2. 标准闭环

```text
git checkout -b proposal/<harness>/<date>-<slug>-<rid> origin/main
↓ 改文件 + commit
git push -u origin <branch>
↓ POST /repos/{owner}/{repo}/pulls            → 拿 number + html_url
↓ GET  /repos/{owner}/{repo}/pulls/{n}        → 轮询 mergeable（首次常为 null，2~3s 后重试）
↓ PUT  /repos/{owner}/{repo}/pulls/{n}/merge  {merge_method: "squash"}
↓ 合并成功后 GitHub 自动删远端分支
git fetch --prune && git branch -D <远端已消失的本地分支>
git checkout main && git pull --ff-only
```

要点：
- **`mergeable` 首次必为 `null`**（GitHub 异步计算），立刻读会误以为不可合并。轮询 6 次 × 2s 足够；`mergeable=false` 说明有冲突 → **不要强合**，保留 PR 并把人指过去。
- **squash merge 后本地提案分支不是 main 的祖先**，`git branch --merged main` 抓不到它。要靠 `git fetch --prune` 后 `git branch -vv` 里的 `: gone]` 来清理。
- 无 token 时降级为 compare 链接（`{repo}/compare/main...{branch}?expand=1`），不要静默失败。
- PR 已存在时（重复运行）复用：`GET /pulls?state=open&head={owner}:{branch}`。

## 3. 仓库约定优先于方便

仓库根 `AGENTS.md` / `docs/*proposal*` 若规定「不得直推 main、必须走 proposal 分支 + PR」，就照做——即使 token 有 Contents 写权限能直推。这类约定通常列明允许的内容类型（规则 / 记忆候选 / 适配器 / 清单）与禁止项（凭据、日志、业务产物）；提交前按它扫一遍敏感模式。

## 4. PR 模板

**模板是从 base 分支（main）读的。** 改 `.github/pull_request_template.md` 的那个 PR，在合并前仍显示旧模板——所以「把模板改成中文」这类请求，交付物要包含两份：
1. 模板文件的改动（合并后永久生效）
2. **一份可直接粘贴的 PR 描述**（当次 PR 用），否则用户会以为没生效

## 坑

- **`{token}` 在工具输出里会显示成 `***`**：`read_file` / 终端输出对疑似凭据做了脱敏，看到 `Bearer ***` 不要断定源码里是字面占位符。先用另一条路径确认行内容，再决定要不要改，否则会把好代码改坏。
- **用户在聊天里贴了 token**：直接写进 `.env`（600），不回显、不重复、不再追问；同时提示「它已进入会话记录，用完建议 Regenerate」。
- **无人值守的自动合并要留开关**：脚本默认自动合并时，另加 `--no-merge`（只开 PR 留人工评审），并把「冲突未合并」与「按开关跳过」渲染成不同标记（❌ vs ⏸），否则报告里分不清是故障还是主动选择。
- **合并摘要要写清「合并了什么」**：PR 号 + 标题 + 涉及文件 + 链接；只给 PR 号，用户还得点进去才知道动了什么。

## 验证

```bash
# API 侧：状态 + 是否真的合并了
GET /repos/{owner}/{repo}/pulls/{n}         # state=closed, merged=true, merge_commit_sha
# 本地侧：main 是否真拿到内容
git -C <repo> log --oneline origin/main -3
git -C <repo> status --short                 # 应为空
git -C <repo> branch -vv | grep ': gone]'    # 应为空
```
