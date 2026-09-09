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

## 陷阱
- cronjob_manage 不接收 model/provider 参数，传了也被忽略、job 仍为 null —— 不要用工具反复重试，直接切 CLI `hermes cron edit`。
- 每次用工具 create 后都要记得 CLI 补钉，新建任务不会自动带用户默认 provider。
- 审计时 `null` ≠ 未运行：null 表示跟随 cron.model/model.default 解析；用户要求的是**显式**钉住 opencode-go，报告时把 null 项列为「未显式钉住」即可，别断言它跑在别的 provider 上。
- 更新操作返回的 job 若与上次字节一致（byte-identical），说明没有实际变更 —— 核对字段而非继续叠加同参数调用。
- 改完涉及投递的字段后，检查 `last_delivery_error`：deliver=origin 的历史任务曾出现微信发送超时错误，属投递层问题，与 job 配置无关（见 hermes-gateway-cron-debug）。
