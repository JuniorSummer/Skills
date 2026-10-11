---
name: agenthub-harness-sync
description: Use when AgentHub sync or harness proposals are in scope.
source: self-generated
---

# AgentHub harness 同步与提案

## 何时用
用户问「AgentHub 有没有同步/提案任务」「harness 更新检测」「记忆提案发布」，或要改/调试 `agenthub_harness_sync.py`。

## 现状
- 任务：`99538efefa43`「AgentHub harness 同步与提案（每日18:00）」`0 18 * * *`，`no_agent` 纯脚本 → 飞书
- 脚本：`~/.hermes/scripts/agenthub_harness_sync.py`（`--dry-run` 只报告、`--all` 全量输出）
- 仓库：`/Users/spike/Documents/projects/00-agenthub`（`AGENTHUB_ROOT` 可覆盖），remote 走 `git@github-agenthub:...`
- 状态：`~/.hermes/state/agenthub-harness-sync.json`；日志同名 `.log`；已发布 inbox 归档 `~/.hermes/state/agenthub-published/<日期>/`

## 三个方向
1. **消费**：`git fetch` + 本地 main 落后则 `--ff-only` 拉取
2. **提交**：`memory/inbox/*.md` 未发布文件按 `source_harness` 分组（`dsh`→`deepseek-harness`），走 `proposal/<harness>/<YYYYMMDD>-memory-inbox-<rid>` 分支推送，成功后本地文件移入归档目录并从 checkout 删除
3. **检测**（每个 harness 三层）：Hermes cron 目录指纹 vs `manifests/hermes-cron.md`（漂移则重建目录并提案）；各 harness 入口 SHA vs `manifests/deployment.md`；live 托管块 vs `adapters/<slug>/AGENTS.managed.md`；`rules/harness/<slug>.md` 里记的本机路径是否存在。规则/适配器类变更（含 `rules/harness/*.md` 过时）**只报不改**

「没有 X 的提案」不等于漏检：三层检查全绿就是真没漂移。想看逐 harness 结论用 `--all`（默认真无变化时静默）。

## 硬约束（照抄自 docs/harness-proposal-workflow.md）
- 工作区有**已跟踪**改动 → 全部写操作跳过（invariant 1）；只容忍 `memory/inbox/` 下的未跟踪文件
- 提交前密钥扫描，命中即跳过该文件
- 目录/清单里**不得**出现 job ID、prompt 正文、投递目标 ID、凭据
- 不自动提升 `memory/MEMORY.md` / `memory_summary.md`，那需要单独的评审 PR

## 坑
- **入口文件不能顺着 `manifests/deployment.md` 找**：hermes 行的 Entry 列写的是服务器入口（`/root/...`）、workbuddy 行根本没路径 → 按记录走会直接漏检两个 harness。用静态表 `HARNESS_ENTRIES`（`hermes` → `~/.hermes/SOUL.md`（不是 AGENTS.md）、`codex` → `~/.codex/AGENTS.md`、`zcode` → `~/.zcode/AGENTS.md`、`deepseek-harness` → `~/.dsh/AGENTS.md`、`workbuddy` → `~/.workbuddy/AGENTS.md`）。
- **adapter 缺对照文件时必须降级报警，不能静默跳过**：`adapters/hermes/`、`adapters/workbuddy/` 只有 README，没有 `AGENTS.managed.md` → 该 harness 的托管块无法逐字比对，只能做结构校验（canonical root + `rules/harness/<slug>.md` 引用）并把“缺对照文件”列入复核项。
- **`jobs.json` 的 `schedule` 是字典**（`{kind, expr/display/run_at}`），不是字符串；直接当字符串用会 `unhashable type: 'dict'`。用 `schedule_text()`。
- **本机没有 gh、没有 GitHub token** → PR 只能「推分支 + compare 链接」人工点一次。要全自动开 PR：把 fine-grained PAT 放到 `~/.config/agenthub/token`（或 `GITHUB_TOKEN`），脚本会走 API，无需改代码。
- **不要用 `cronjob_manage action=run` 测试这个任务**：手动补跑会吃掉次日 18:00 的档期（见 cron-job-management 的补跑陷阱）。测试用 `--dry-run`，真实写入用不带参数直接跑。
- **看门狗语义**：无变化时 stdout 必须为空（=不推送）。因此「需人工复核」项做了去重（state `reported_review`），只报新增，既往项只在 `--all` 出现。新增检测器时必须把结果塞进 `review`/`problems`/`proposals` 之一，否则静默会掩盖问题。
- 切分支会删掉未跟踪的 inbox 文件（因为它在提案分支里是已跟踪的）→ 归档必须在 `git checkout main` **之前**用内存里的文本写盘，不能 `copy2(src)`。
- `git status --porcelain` 的 `??` 行是 payload，别当成脏工作区。

## 验证套路
```bash
python3 ~/.hermes/scripts/agenthub_harness_sync.py --dry-run   # 看要做什么
python3 ~/.hermes/scripts/agenthub_harness_sync.py             # 真跑
python3 ~/.hermes/scripts/agenthub_harness_sync.py             # 再跑：应 0 字节输出
cd /Users/spike/Documents/projects/00-agenthub && git ls-remote --heads origin | grep proposal
```
校验推送内容没被改动：`git show origin/<branch>:<path> | shasum -a 256` 应等于 state 里的哈希。
