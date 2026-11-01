---
name: agenthub-change-publishing
description: Use when publishing changes to the AgentHub repo.
source: self-generated
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [agenthub, git, pull-request, shared-repo]
    related_skills: [agenthub-bootstrap]
---

# AgentHub 变更发布

AgentHub（`/Users/spike/Documents/projects/00-agenthub`，remote `JuniorSummer/AgentHub`）是跨 Harness 的共享规则与记忆源。所有改动**必须走提案分支 + PR + squash merge**，仓库 `AGENTS.md` 明确禁止任何 Harness 直推 `main`——即使用户说「同步更新到 main」也不例外，该请求的解就是合并 PR。

## When to Use

- 用户要求把改动「同步/更新到 AgentHub」或「推到 main」。
- 要往 `memory/inbox/` 提交候选记忆，或改 `rules/`、`adapters/`、`templates/`。
- 接手其他会话遗留的提案分支，判断它还有没有必要发布。

## 流程

1. **先看约定**：读仓库 `AGENTS.md` 与 `docs/harness-proposal-workflow.md`（分支命名、允许内容、审查/合并/同步/清理都写在那里）。提交信息与 PR 文本用简体中文。
2. **判定要发布什么**：
   - 候选记忆 → `memory/inbox/<YYYYMMDD>-<harness>-<slug>-<rand>.md`，frontmatter 含 `id / created_at / source_harness / scope / kind / evidence`。
   - 规则/适配器 → `rules/`、`adapters/`、`templates/`。
   - 一个 PR 一件事；不要把记忆候选和规则改动混在一起。
3. **同步 main 再开分支**：
   ```bash
   cd /Users/spike/Documents/projects/00-agenthub
   git fetch origin && git checkout main && git pull --ff-only origin main
   git checkout -b proposal/<harness>/<YYYYMMDD>-<slug>-<rand>
   ```
   不要从落后的本地 main 开分支；落后的分支合并时会大面积冲突。
4. **提交前扫敏感信息**（仓库禁止凭据/账号信息）：
   ```bash
   HITS=$(grep -inE "(sk-[a-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|Bearer [A-Za-z0-9]|password[=:]|passwd[=:]|token[=:]|api[_-]?key[=:]|cookie|session_id|@[a-z0-9.-]+\\.(com|cn|net))" "$F" || true)
   [ -n "$HITS" ] && echo "$HITS" || echo clean
   ```
   别写成 `if grep ... | head; then`：管道退出码是 `head` 的，永远为 0，扫描结论必然假阳性。
5. **提交并推送分支**：
   ```bash
   git add <files> && git commit -m "<中文动词>: <一句话>"
   git push -u origin HEAD
   ```
6. **开 PR**：push 后 remote 会回显 `Create a pull request ... /pull/new/<branch>` 链接，把它原样给用户。本机没有 `gh`、也没有 GitHub token 时**开不了也合不了 PR**——如实说明并递链接，**不要**改成直推 main 绕过规则。
7. **合并后清理**：squash merge → 本地切回 main、`git pull --ff-only`、删本地和远端提案分支。

## 旧分支是否还值得发布

读别的会话留下的提案分支时，先判断它是否已被 main 里的 PR 取代：

```bash
git cherry main <proposal-branch>     # '+' = patch-id 不在 main；'-' = 已在
```

`+` **不等于还需要发**：另一条 PR 可能用不同写法实现了同一意图。挑一个代表文件看清 main 现状（如 `grep -c "<章节名>" AGENTS.md`、`ls docs/<同名文档>`），内容已覆盖就丢弃旧提交。

cherry-pick 冲突几乎总是「旧分支早于某个已合并的同主题 PR」的信号：

```bash
git cherry-pick --abort; git reset --hard <main>; git checkout -f main
```

强行解冲突会把握手退回旧版本。宁可只发真正新增的那一个文件。

## 坑

- **用户说「同步到 main」≠ 可以直推**：给 PR 链接是最短路径；没有 token 就明确说做不到自动合并。
- **`git checkout main` 在冲突未清时会失败**（`Entry ... not uptodate. Cannot merge.`）却仍打印出 HEAD：先 `--abort` + `reset --hard`，再用 `git rev-parse --short HEAD` 确认真回到了 main。
- **未跟踪的 inbox 文件在切分支/reset 后会保留**（`reset --hard` 不删未跟踪文件）——不要以为丢了，但也别忘了一起提交。
- 提交前不要顺手 `git add -A`：会把其他会话的半成品带进提案。
