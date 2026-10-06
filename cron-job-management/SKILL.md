---
name: cron-job-management
description: 管理/创建/审计定时任务。model/provider 用 hermes cron edit CLI 设置。
source: self-generated
---

# Hermes 定时任务管理

## 何时用
创建、编辑、删除、审计定时任务；用户常检查「有没有任务不走 opencode-go」这类 provider 对齐问题，或要求新建提醒任务。

## 标准流程
1. **查看全部任务**：`cronjob_manage action=list`（或 `hermes cron list`）。审计时逐项看 `provider`/`model`/`schedule`/`deliver`/`enabled`/`last_status`。
2. **创建任务**：`cronjob_manage action=create`，schedule + prompt 必填。
   - 一次性提醒：绝对 ISO 时间 `2026-09-18T09:00:00`（本机 +08，调度器自动换算）
   - 周期性：自然语言（`every monday 9am`）或 cron 表达式
   - `deliver`：省略=创建时所在会话（origin，如当前微信 DM）；其他平台 `platform:chat_id`，如 `feishu:oc_...`
3. **补钉 model/provider（关键步骤）**：工具新建/更新的任务 model、provider 为空（null），而用户标准是全部任务显式钉在 deepseek-v4-flash / opencode-go。用 CLI 补：
   ```bash
   hermes cron edit <job_id> --model deepseek-v4-flash --provider opencode-go
   ```
   `hermes cron edit --help` 注明 model/provider 是 user-owned、agent 的 cronjob 工具无法设置 —— 只能走 CLI。
4. **改其他字段**（prompt/schedule/name/deliver/script/skills 等）：`cronjob_manage action=update` 或 `hermes cron edit`。
5. **验证落地**：重新 list，或直接解析存储文件确认字段：`~/.hermes/cron/jobs.json` 顶层 `jobs` 列表，每个 job 对象顶层就是 `model`/`provider` 字段。

## 存储与文件
- 任务定义：`~/.hermes/cron/jobs.json`
- 执行记录：`~/.hermes/cron/executions.db`
- 输出：`~/.hermes/cron/output/<job_id>/`

## 静默巡检任务（no_agent，推荐用于健康监控）

现状：job `59439a120017`「Cron 健康巡检（静默）」，**每日凌晨 03:00** → 飞书，脚本 `~/.hermes/scripts/cron_health_check.py`。

覆盖范围：只检查 03:00 之前已发生的运行（前一整天 + 当天 00:30 的日报），所以 07:30/08:00/09:00 那批早间任务的失败要等下一次 03:00 才被发现（滞后 18-24h）。要当天就发现早间故障，得再排一次 10:00。

```bash
hermes cron ...   # 或用 cronjob_manage action=create
#   schedule='0 3 * * *', script='cron_health_check.py'
#   no_agent=true, deliver='feishu:oc_...'
```

为什么必须是 `no_agent`：巡检如果本身是 LLM 任务，provider 一挂（如 403）它会跟着一起瞎，正好漏掉最需要发现的全域故障。no_agent 下 stdout 原样投递、**空 stdout 不发任何消息**（看门狗模式），所以脚本在“无新增问题”时必须什么都不输出。

巡检必须查三层，只查第一层等于白做（曾有任务 6 周静默故障、`last_status` 一直是 ok）：
1. 任务状态：`last_status != ok` / `last_delivery_error` / `last_fire_error` / `next_run_at` 过期未跑
2. **输出内容**：`FAILED` 头部、`## Error`、`(No response generated)`、`❌ (解析失败|ERROR|错误|异常|超时)`、`⚠️ 数据源异常`、`Traceback`
3. 去重：同一故障只报一次（状态文件 `~/.config/cron-health/reported.json`，键 = job_id → 当前活跃的 finding key 列表，自然消失的故障会被遗忘）

两个关键坑：
- **`❌`/`⚠️` 不能裸匹配**：正常内容里也会出现（如“❌ 已下榜”、“⚠️ 注意事项”），必须精确匹配错误语义，否则误报一堆。
- **门控跳过（`wakeAgent=false`）的任务无法从输出验证送达**：脚本自己直推平台的（如伦敦金价格），输出只有一行 gate 说明，巡检只能标注“无法验证”，别当故障报。

## 陷阱（补跑 / 状态字段）
- **手动补跑会占用「次日档期」**：`cronjob_manage action=run` 触发的那次执行，会被记在该任务 `next_run_at` 对应的档期上（通常是**次日**同一时刻），于是次日那一档被判为「已完成」而被调度器跳过 → **补跑当天有推送、第二天同一个推送凭空消失**，`next_run_at` 直接跳到后天。用户会来问「为什么早上没有结果」。判别（只读）：
  ```bash
  python3 -c "import sqlite3;c=sqlite3.connect('/root/.hermes/cron/executions.db');[print(r) for r in c.execute('select job_id,source,scheduled_instant,started_at,status from executions order by rowid desc limit 12')]"
  ```
  若某次 `source='direct'` 的补跑，其 `scheduled_instant` 比 `started_at` **晚一天**（日期 +1），即已吃掉次日档期。缺口会在**下一轮自然排期**时自愈；**不要靠「再补跑一次」解决** —— 补跑会再吃掉下一档，形成错位循环。provider 短暂抖动恢复后**优先等自然排期**；确实要补跑就提前告知用户次日会缺一次。
- **巡检/doctor 报的 `delivery_failed` 可能是「修复前的旧账」**：投递渠道改好后若该任务此后还没跑过，jobs.json 里的 `last_status` / `last_delivery_error` 仍是旧那次的，健康巡检与 `hermes cron doctor` 会继续列出（正常巡检模式下「新增 0 项」、只出现在「仍存在」区）。判据：错误里的目标与当前 `deliver` 是否一致（错误写 `weixin:`、当前已是 `feishu:` = 已自愈，下次运行自动转 ok）。不要为这类滞后状态反复救火。

## 陷阱
- cronjob_manage 不接收 model/provider 参数，传了也被忽略、job 仍为 null —— 不要用工具反复重试，直接切 CLI `hermes cron edit`。
- 每次用工具 create 后都要记得 CLI 补钉，新建任务不会自动带用户默认 provider。
- 审计时 `null` ≠ 未运行：null 表示跟随 cron.model/model.default 解析；用户要求的是**显式**钉住 opencode-go，报告时把 null 项列为「未显式钉住」即可，别断言它跑在别的 provider 上。（例外：`no_agent` 任务不需要 model，null 是正常的）
- **prompt 里不要写“忽略错误标记”**：曾为了让输出干净而写“忽略脚本输出中的 ❌ 解析失败”，结果数据源解析故障被屏蔽了 6 周没人发现。正确做法是让脚本输出显式异常标记（如 `__SOURCE_ERRORS__`/`⚠️ 数据源异常`），prompt 要求把该标记优先原样推送。
- 更新操作返回的 job 若与上次字节一致（byte-identical），说明没有实际变更 —— 核对字段而非继续叠加同参数调用。
- 改完涉及投递的字段后，检查 `last_delivery_error`：deliver=origin 的历史任务曾出现微信发送超时错误，属投递层问题，与 job 配置无关（见 hermes-gateway-cron-debug）。
