---
name: kdocs-milestone-weekly-report
description: Use when 包1里程碑周报 needed. Kdocs sheet → fixed weekly report.
source: self-generated
---

# 包1 里程碑周报（金山文档取数）

## When to Use（何时用）
用户提到「包1 里程碑」「里程碑周报」「发给客户的周报」「和厂商对里程碑」时。也用于解释/维护每周五的自动汇总任务。

## 数据源与取数
- 在线表：`https://www.kdocs.cn/l/calE1favyKet`（《包1-里程碑.xlsx》，单表 Sheet1，file_id `EypHjAcLgrMzyRp8139hrxBXhhFZqi4YW`）
- 读表用 **kdocs-cli**（`~/.local/bin/kdocs-cli`，已认证到系统钥匙链；**不要**去开浏览器，kdocs 链接会 302 到登录页）：
  ```bash
  kdocs-cli drive read-file url="https://www.kdocs.cn/l/calE1favyKet"
  ```
  返回 `status=pending` 时，用同响应里的 `task_id` 再调一次（`file_id=... task_id=...`）。中文参数用 `--file`/stdin，别用 key=value。
- 列结构：`分类 | 里程碑 | 状态 | 责任人 | 联系方式 | 目标 | 完成时间 | 生态 | <日期>进展`。**续行**（分类与里程碑为空的行）要并入上一条的目标/进展。
- 表内联系人手机号/邮箱**不出现在客户周报里**。

## 口径（用户 2026-10-11 手工改定，勿改回）
1. **不做高/中风险分级**，也不写「建议动作」。
2. **只摘录表内明确标注的内容**（进展/目标里带「风险点／重大风险点」的才算风险），其余不做推断；像「等合同签署后发货」「需 AI 公司排期」这类只是进展描述，不列为风险。注意「风险态势模块」是产品名，不能命中。
3. **不单列「需协调事项」章节**（早期版本有，用户删了）。
4. 进展列**原文照录**；仅剔除内部强调语（`重点：要尽快`、`要软硬件都算上`）——脚本里的 NOISE 列表。数据表本身不改。
5. 维度顺序固定 `IaaS → PaaS → MaaS → 应用`；IaaS 章节标题写作「交付期最近的IaaS」（脚本里 `DIM_LABEL`，其他维度暂无修饰词，用户可能会要求同款）。
6. 章节序号用中文数字 + `、`，条目用 `1、2、3、`，不用 markdown 表格；结尾附注说明状态口径（OSS/ES/Redis 状态「已完成」但目标列写「Almost Done」，建议统一）。

## 出稿方式
```bash
python3 ~/.hermes/scripts/milestone_weekly_report.py     # stdout = 周报正文，同时落盘 周报-最新.md
```
脚本自包含（stdlib + kdocs-cli），不依赖 LLM；产物目录 `/Users/spike/Documents/projects/96-hermes/workspaces/包1里程碑周报/`。

**文件命名（用户要求，便于逐周跟踪变化）**：`<YYYYMMDD>周报.md`，日期取表格**进展列表头**（`10月10日进展`→`20261010周报.md`；`10-30进展`、`2026/10/24进展` 也能解析），表头没有日期时退回当天；同时写一份 `周报-最新.md` 方便引用。因此**建议用户每周更新表时把进展列名改成当周日期**，否则文件名不刷新、会覆盖上一周。周报首行「截至」也用同一个日期（表达数据快照口径，比跑批日更准）。取数失败时输出以 `⚠️ 数据源异常` 开头并 exit 0，务必原样推送。

## 每周五定时任务（default profile → 飞书 oc_30288b0665…）
| job_id | 时间 | 作用 |
|---|---|---|
| `7e55d638da0c` | 周五 12:00 | 提醒用户先更新在线表（进展/状态/目标时间三项） |
| `c079fc6463aa` | 周五 13:00 | `no_agent` 跑脚本，stdout 原样投递周报，供 13 点会前报领导 |

## 坑
- **不要用 `cronjob_manage action=run` 试跑周期性任务**：补跑会占用 `next_run_at` 那一档，导致下周五那一次凭空消失。要验证就本地 `python3` 跑脚本。
- 脚本里必须显式找 `kdocs-cli` 绝对路径（`~/.local/bin`）：gateway/cron 的 PATH 只有 `/usr/bin:/bin`，直接用 `kdocs-cli` 会 FileNotFoundError。验证方法：`env -i HOME="$HOME" PATH=/usr/bin:/bin /usr/bin/python3 ~/.hermes/scripts/milestone_weekly_report.py`。
- 周报正文只在表格「进展」列有内容时才有信息量：周五 12:00 提醒用户更新后再汇总，否则 13:00 的稿子就是上周内容。
