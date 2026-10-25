---
name: meeting-minutes-digest
description: Use when digesting meeting minutes daily or weekly.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meetings, minutes, digest, weekly, qwennote]
    related_skills: [mcp-oauth-onboarding, tencent-docs, delivery-readiness-review]
---

# Meeting minutes digest

Turn a pile of recorded meetings into one readable week (or day). This is the *aggregation* layer — single-meeting action extraction lives in `meeting-action-items`.

## When to use

- "整理本周周一到周五的会议纪要" / "这周开了哪些会" / "把这几场会汇总一下"
- 需要**定时推送**的听记回顾（每日晚间 / 每周固定时间），而不是一次性整理
- The user has a minutes service connected (QwenNote MCP as `qwennote`, Feishu 智能纪要, 钉钉听记) and wants a summary rather than a transcript.

## Procedure

### 1. Fix the date range before querying

Run `date` first. In a long session the wall clock drifts and "本周" silently becomes the wrong week.

- "周一到周五" = Monday 00:00 → Saturday 00:00 in the user's local zone (Asia/Shanghai here).
- If today is mid-week, say which range you are using (this week so far vs last full week) instead of guessing.

### 2. Pull the list

QwenNote MCP (registered as `qwennote`):

```bash
mcporter call --server qwennote --tool list_my_minutes \
  --args '{"pageSize":50,"createdAfter":<epoch_ms>,"createdBefore":<epoch_ms>}'
```

Or fetch everything for a range in one shot with `scripts/qwennote_fetch.py --from 2026-10-19 --to 2026-10-23 --out /tmp/qn`.

- Timestamps are **milliseconds** epoch — convert with the local zone, not UTC.
- `list_my_minutes` covers notes *I created*; voice memos are a separate tool (`list_audio_memos`). Check it when the week looks suspiciously empty.

### 3. Fetch substance per note

| Tool | Use |
|---|---|
| `get_minutes_ai_summary` | Markdown summary — the main body |
| `list_minutes_todos` | action items with content / assignee / dueDate |
| `get_minutes_keywords` | fast thematic grouping |
| `get_minutes_transcription` | only when you need the exact wording (speaker + timestamps) |

### 4. Write by theme, not by meeting

The user wants to understand the week, not read eight paraphrases. Fixed six-part shape:

1. **概览** — count, total duration, 2–3 main workstreams
2. **按主线归并** — merge the same project across meetings, tag each point with its date
3. **关键决策** — only what was actually decided, numbered
4. **关键时间节点** — chronological, marked past / today / upcoming
5. **风险与卡点** — ordered by severity
6. **下周开工建议** — at most three items

### 5. Close the loop on ownership

List the action items that have **neither an owner nor a due date** and state the count — that is where the week quietly falls apart, and the user cares about it. Then group the rest by owner so they can be dispatched directly.

## Recurring push (daily evening / weekly)

一次性任务用上面的流程；**常驻推送**要把「取数」和「成文」拆开：`scripts/minutes_digest.py` 负责拉取与清洗，prompt 负责归组与判断。

```bash
python3 scripts/minutes_digest.py --mode daily    # 当天 00:00 → 现在
python3 scripts/minutes_digest.py --mode weekly   # 本周一 00:00 → 现在
```

- **两种节奏、一份实现**：`--script` 不能传参，周报任务指向一个三行包装脚本（改 `sys.argv` 后 `runpy.run_path(实现, run_name="__main__")`），日报直接用实现文件。不要为两个节奏复制两份采集器。
- **建任务时把 model 一起钉住**：`hermes cron create "<cron>" "<prompt>" --script minutes_digest.py --model deepseek-v4-flash --provider opencode-go`。用 agent 的 cron 工具建出来 model/provider 是 null。
- **建在网关实际服务的 profile**：`hermes cron list` 说「No scheduled jobs」而用户坚持有任务，就是看错了 profile——查网关 plist 的 `HERMES_HOME` 和各 profile 的 `cron/jobs.json`，命令前缀 `HERMES_HOME=...`。建错 profile 的任务会安静地永不触发。
- **绝不用 `hermes cron run` 验证**：手动补跑会占掉下一个档期，次日同一时刻就不推了。只能「直接跑脚本看退出码与输出规模」+「核对 jobs.json 的 schedule / model / provider / next_run_at」。
- **取数前先刷新 token**：采集器在剩余不足 5 分钟时自行用 refresh_token 换新；刷新失败必须打出 `⚠️ 数据源异常`，绝不能让用户看到「今天没开会」。

自动化版的 prompt 按上面六段收紧写：

- **概览**：场次 + 总时长 + 最关键一件事（周报加三个关键词）
- **各子项目进展**：严格按实时索引的「大项目 > 小项目」分组；**只列纪要里真出现的小项目**，其余按大项目汇总成一行「其余 N 个子项目无纪要」——逐条列空项会把推送灌满
- **待办**：按截止时间排序，「做什么｜谁｜何时」；没负责人写待指定、没时间写待定、跨会重复项合并；周报把**逾期项置顶**
- **风险与卡点 / 下一步**：日报给「明天先做 3 件事」，周报给「下周关键节点（按日期）」
- 三条硬约束必须写进 prompt：只基于脚本数据、不编造；`⚠️ 数据源异常` 原样置顶；空区间只推一句话

## Pitfalls

- **An empty account is not an empty week.** If notes, memos, tags and hot words all return zero, the wrong account was almost certainly authorized — see the "wrong account" rule in `mcp-oauth-onboarding`. Ask for a re-auth instead of reporting "no meetings this week".
- **`todos[].content` can be a nested JSON string** (`{"mark":[],"value":"…"}`). Try `json.loads` and take `value`, or the output is all braces.
- **Strip rendering artifacts before writing**: `![图片](https://…oss…Signature=…)` covers and `{origin:12.34}` time anchors belong to the source app, never in a user-facing digest.
- **Durations are milliseconds.** Convert to minutes before quoting.
- **Feishu does not render Markdown tables** — use numbered lists, or attach a file for tabular output.
- **The index is alive, not a schema.** Sub-projects get added, renamed and promoted between quarters; read the index sheet on every run instead of caching it in the collector.
- **A weekly digest is not a status report.** Do not invent progress percentages; if a tracker states conflicting numbers, say they conflict.

## Verification

- [ ] Range matches "this week" and the boundary is stated explicitly.
- [ ] Every listed note yielded a summary; any failure is called out by name.
- [ ] Decisions contain only items that were actually decided.
- [ ] Unowned / undated action items are surfaced with a count.
- [ ] No Markdown tables, no OSS links, no `{origin}` anchors in the output.
- [ ] For a recurring push: `schedule` / `model` / `provider` / `next_run_at` were read back from `jobs.json`, and the job lives in the profile the gateway serves.
