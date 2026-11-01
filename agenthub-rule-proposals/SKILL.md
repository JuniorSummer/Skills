---
name: agenthub-rule-proposals
description: Use when publishing AgentHub rules or AGENTS.md proposals.
source: self-generated
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agenthub, rules, proposals, cross-harness]
    related_skills: [agenthub-harness-sync, agenthub-bootstrap]
---

# AgentHub 规则与适配器提案

## When to Use

“把重要、通用的内容沉淀到 AGENTS.md”“更新 `rules/harness/*`”“这条结论要在 harness 之间共享”，或要给 `/Users/spike/Documents/projects/00-agenthub` 提一条 rules / adapter / 根 `AGENTS.md` 变更。每日同步脚本只处理 `memory/inbox` 与 cron 目录，规则类变更**必须手工开提案**。

## 铁律

- **别的 harness 占着工作区时不要在里面提交**：`00-agenthub` 常挂着其他 harness 的未提交改动。用 `git worktree add -b proposal/<harness>/<YYYYMMDD>-<slug>-<rid> <独立路径> origin/main` 拉工作树；不要 stash，不要顺带提交别人的改动。
- **从 `origin/main` 起，不是本地 `main`**：本地 checkout 经常落后好几个提交。
- **新章节名必须对齐入口文件已引用的名字**：先看 `~/.codex/AGENTS.md`、`~/.zcode/AGENTS.md`、`~/.dsh/AGENTS.md`、`~/.hermes/SOUL.md` 里引用了哪些章节名和模板路径（`search_files` 搜 `rules/core`、`共享`、`templates/`）。入口引用的是 `共享工作约定` / `项目约定与指令文件` / `templates/project-AGENTS.md` 这类既有名字时，新内容必须沿用，否则规则写了、入口指不到，等于不存在。宁可和并行提案撞同名标题（合并时去重），也不要自创无人引用的名字。
- **改 `rules/harness/*.md` 前先核实运行现状**：`launchctl list | grep -i hermes`、ssh 到目标机跑 `systemctl is-active/enabled <svc>`、确认目录是否存在。旧文档描述的运行环境可能早已退役；核实不了的写成“历史/条件事实”，不要当现状往前搬。
- **沉淀环境类结论前先实测**：依赖没装、能力不可用时，规则只写方法与前提（“有 X 时用 Y”），不写成“已具备”。
- **写 `AGENTS.md` / `SOUL.md` 会触发 agent-instruction 审批门**：被拦时按提示让用户确认后重试一次；不要换终端、不要用脚本绕过——guard 明令禁止绕路，绕过去等于伪造同意。
- **开 PR 不要卡住交付**：本机无 gh，`~/.hermes/.env` 里的 `GITHUB_TOKEN` 可能是注释状态（API 401）。`git push -u origin HEAD` 的 stderr 自带 `.../pull/new/<branch>` 链接，交给用户点一次即可，其余结论照常汇报。

## 步骤

1. 隔离工作树（见铁律），`git status --short` 确认主检出确实有别人的改动。
2. 收集事实：入口引用名、live 服务状态、现有 `rules/` 与 `memory/projects/`（查有没有同一条规则的第二份副本）。
3. 按下面的分工表落盘；共享章节内部按“时机与路由 → 通用方法 → 项目约定”三层写，别混成一锅。
4. 自查：旧名字 `grep` 无残留、敏感模式扫描、`git diff --stat origin/main..HEAD` 复核文件清单。
5. 提交（中文、逐条说明改了什么与为什么）→ `git push -u origin HEAD` → compare 链接交给用户。
6. 合并后再删 worktree 与远端分支；删前用 `git cat-file -e main:<path>` 确认内容已在 main。

## 落盘分工

| 内容 | 去向 |
| --- | --- |
| 跨 harness 的通用行为 | 根 `AGENTS.md` 共享章节 + `rules/core.md` 强制条目 |
| 平台差异（路径/服务/权限/投递） | `rules/harness/<slug>.md` + `adapters/<slug>/README.md` |
| 项目级骨架 | 仓库内 `00-agenthub/templates/project-AGENTS.md` |
| 长期事实、迁移、环境状态 | `memory/inbox/<YYYYMMDD>-<slug>-<rid>.md`，frontmatter 含 id/created_at/source_harness/scope/kind/content，并附“待应用的替换”；不碰 canonical 记忆 |
| 部署与校验 | `manifests/deployment.md`（入口、备份、时间、SHA-256） |
| 来源与排除项 | `docs/<topic>.md`：读了什么、核了什么、故意没沉淀什么 |

发布前清单与 PR 正文结构见 `references/proposal-checklist.md`。

## 坑

- 改过托管入口（如 `~/.hermes/SOUL.md`）必须重算 SHA-256 回填 `manifests/deployment.md`，否则下轮漂移检测会误报。
- 仓库里已有 `docs/<同类>.md` 时不要新开一份平行说明；扩写或替换，避免两套来源记录。
- 与并行提案改动同一章节时，在 PR 正文写明“合并时保留一套路由表并去重条目”，不要留给评审猜。
- 从别的 harness 分支读文件不等于已同步：提案未合并前，一律表述为“未发布、其他 harness 尚不可见”。
