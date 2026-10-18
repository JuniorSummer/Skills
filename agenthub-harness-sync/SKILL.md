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
- 脚本：`~/.hermes/scripts/agenthub_harness_sync.py`（`--dry-run` 只报告、`--all` 全量输出、`--harness-selfcheck` 额外让 Codex 跑一遍只读自查）
- 仓库：`/Users/spike/Documents/projects/00-agenthub`（`AGENTHUB_ROOT` 可覆盖），remote 走 `git@github-agenthub:...`
- 状态：`~/.hermes/state/agenthub-harness-sync.json`；日志同名 `.log`；已发布 inbox 归档 `~/.hermes/state/agenthub-published/<日期>/`

## 三个方向
1. **消费**：`git fetch` + 本地 main 落后则 `--ff-only` 拉取
2. **提交**：`memory/inbox/*.md` 未发布文件按 `source_harness` 分组（`dsh`→`deepseek-harness`），走 `proposal/<harness>/<YYYYMMDD>-memory-inbox-<rid>` 分支推送，成功后本地文件移入归档目录并从 checkout 删除
3. **检测**（每个 harness 多层）：Hermes cron 目录指纹 vs `manifests/hermes-cron.md`（漂移则重建目录并提案）；各 harness 入口 SHA vs `manifests/deployment.md`；live 托管块 vs `adapters/<slug>/AGENTS.managed.md`；`rules/harness/<slug>.md` 里记的本机路径是否存在。规则/适配器类变更（含 `rules/harness/*.md` 过时）**只报不改**
4. **AgentHub 内容自查**（**除 hermes 本身**）：逐 harness 看**它读的 AgentHub 内容是否有更新/是否一致**。检查项：
   - 共享 Skill 副本 `~/.agents/skills/agenthub-bootstrap/SKILL.md` ↔ 仓库 `skills/agenthub-bootstrap/SKILL.md`（哈希）
   - `memory/memory_summary.md`、`memory/MEMORY.md` 哈希变化 → “记忆有更新，各 harness 下次任务会读到新版”
   - 每个 harness 入口 `AGENTS.md` **整文件哈希**变化（基线上次记录在 state 的 `content_state`）→ “入口内容有变化”
   - **harness 原生可见性实证**：ZCode 用 `node /Applications/ZCode.app/Contents/Resources/glm/zcode.cjs skills list` 能看到 `agenthub-bootstrap`；Codex 用 `codex exec`（实测可用，见下节）

### 为什么只有 ZCode 能“自己查”（实测结论，别再试一遍）

- `codex exec ...`：**2026-10-13 复测：能跑通**（方子见下节「让 codex 真自查」）。裸跑松散长 prompt 会去翻 harness 的 sqlite / 全盘 rg，跑到 420s 被工具超时截断；偶发第一条 `failed to refresh available models: request timed out` 直接退出 → 重试一次即可
- `zcode -p "<prompt>"`：报 `无法定位 CLI ZCode Built-in Provider Config`（打包布局下缺 provider 配置）→ 只能跑 `skills list` / `doctor` / `version` 这些子命令
- `dsh`（DeepSeek Harness）：**无 CLI**（只有 Electron 应用 + `app.asar.unpacked/dsh/node_modules`）
- `workbuddy`：`~/.workbuddy` 不存在 → 直接跳过

所以口径是：**能驱动的（ZCode、codex）用它的原生命令实证；其余用共享 Skill 根 + 入口文件哈希做内容级校验**，并在报告里如实注明原因。

### 让 codex 真自查（2026-10-13 实测可用）

**首选：`python3 ~/.hermes/scripts/agenthub_harness_sync.py --dry-run --harness-selfcheck`** —— 2026-10-14 起已经把它包成了 flag：脚本内部用 `codex exec --sandbox read-only --skip-git-repo-check -C <repo> -o ~/.hermes/state/codex-selfcheck.md "<清单式 prompt>"`（timeout 420），结果拼进【AgentHub 内容自查】。因为单次要 3-5 分钟，**默认不开**，不拖慢每日 18:00 的看门狗。

手动跑（需要自己控 prompt 时）：

```bash
cd /Users/spike && codex exec --skip-git-repo-check -s read-only \
  -c model_reasoning_effort="low" - < <清单式 prompt 文件>
```

- cwd 给 `/Users/spike`：read-only 沙箱下仍能读全盘 harness 状态（`~/.codex`、`~/.zcode`、`~/.dsh`、`~/.hermes`、`00-agenthub`）；prompt 走 stdin（`-`）。
- **prompt 必须是清单式短 prompt**（「第 1 步…第 4 步…做完即收尾，不要再跑工具」），否则它会自行探索到被 420s 工具超时截断（实测第一版就是这样，日志停在半路、没有结论）。
- 耗时 1–4 分钟；先出现 `Reconnecting...` / `Falling back from WebSockets to HTTPS` 属正常（websocket 通道不可达会回退 HTTPS）。
- **成本参考：单次约 13k–19k tokens**（10-13 实测 13,407；10-14 实测 19,095）——所以 `--harness-selfcheck` 默认关闭，别接进每日流程；真要常态化建议降到周级。
- **codex 沙箱里 PATH 没有 `zcode`**，它会据此报「zcode 无 CLI」→ 别把它当冲突：ZCode 的原生可见性要在 Hermes 侧跑 `node /Applications/ZCode.app/Contents/Resources/glm/zcode.cjs skills list`（`which zcode` 为空，只有打包内的 cjs）。
- 要它给哈希/mtime 级证据，跑完和 `--all` 的 `【AgentHub 内容自查】` 对一遍；结论不一致时以两层都复现的为准。

**别走 GUI 路线**（2026-10-13 踩过）：用 `computer_use` 往 ChatGPT 桌面版的 Codex 输入框打长中文 prompt，`type` 会 MCP 超时；排障时若杀掉 Hermes 托管的 `cua-driver serve/mcp` 进程，`computer_use` 会对整个 Hermes 进程永久失效（详见 computer-use skill）。

「没有 X 的提案」不等于漏检：三层检查全绿就是真没漂移。想看逐 harness 结论用 `--all`（默认真无变化时静默）。报告分段：`本地同步` / `提案提交` / `harness 更新检测` / `AgentHub 内容自查` / `记忆` / `跳过异常`。

## 硬约束（照抄自 docs/harness-proposal-workflow.md）
- 工作区有**已跟踪**改动 → 全部写操作跳过（invariant 1）；只容忍 `memory/inbox/` 下的未跟踪文件
- 提交前密钥扫描，命中即跳过该文件
- 目录/清单里**不得**出现 job ID、prompt 正文、投递目标 ID、凭据
- 不自动提升 `memory/MEMORY.md` / `memory_summary.md`，那需要单独的评审 PR

## 分支清理（定期做）

推送出去的分支**不会自动回收**，会一直堆在 origin。清理前先逐条确认内容是否已在 main：

```bash
git fetch origin "$b" --quiet && git diff --name-status main FETCH_HEAD
git cat-file -e "main:<分支新增的文件路径>"   # 存在=已合入，可删
```

- **可删**：被新分支取代的（如旧的 cron-catalog）、内容已合入 main 的
- **不可删**：包含**未合并**内容的（如某条还没合的 `memory/inbox` 提案）
- 删除：`git push origin --delete "$b"`（deploy key 有写权限就能删，不需要 gh/token）
- **误删恢复**：对象还在本地 `.git` 里（之前 fetch 过），用 `git push origin <原tip-sha>:refs/heads/<branch>` 原样推回；tip sha 从之前的 `git ls-remote --heads origin` 记录里取。已恢复过一次（2026-10-14）。
- **已废弃（别再恢复）**：`proposal/deepseek-harness/20261005-memory-inbox-fa68f9`（内容 `memory/inbox/20261001-hermes-agenthub-integration-a7c41f.md`）—— 用户 2026-10-14 决定直接废弃并删分支；本地归档副本留在 `~/.hermes/state/agenthub-published/20261005/` 仅作记录，**不要再重推**。

### cron-catalog 提案为什么要人工合并

脚本只在**成功推送后**才把 live 指纹写进 state，而 `manifests/hermes-cron.md` 在 main 上仍是旧的。所以：

- 提案挂着不合并 → **本机 cron 每有新变更就会再开一条新分支**（不是每轮重复，是“每次变更再开一条”）
- 合并后才会收敛。2026-10-05~10-14 就堆了 6 条这种分支
- 排查手法：`git diff --stat main origin/<分支>:manifests/hermes-cron.md` —— 有差异 = 没合

## 坑
- **脚本里的 `run()` 返回 `CompletedProcess`**（用 `proc.returncode` / `proc.stdout`），不是 `(rc, out, err)` 元组；新增调用时别按元组解包。`run()` 现支持 `timeout=` 参数（默认 180）。
- **不要加“harness 软件版本检查”**（2026-10-13 用户明确要求去掉）：只做 **AgentHub 内容**层面的检查（入口/memory/共享 Skill）；厂商版本跟 AgentHub 不相关，不进报告。
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

**每次合并后要做**：`cd 00-agenthub && git pull --ff-only origin main` —— 本地 checkout 不会自己跟进 main（脚本只会 `fetch` + 落后时 ff），开发助手很容易在旧 main 上读文件。
