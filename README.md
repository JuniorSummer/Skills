# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [agenthub-harness-sync](./agenthub-harness-sync/) | Use when AgentHub sync or harness proposals are in scope. | 2026-10-05 |
| [benchmark-leaderboard-monitor](./benchmark-leaderboard-monitor/) | | | 2026-10-08 |
| [cron-job-management](./cron-job-management/) | 管理/创建/审计定时任务。model/provider 用 hermes cron edit CLI 设置。 | 2026-10-08 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 | 2026-10-08 |
| [hermes-skills-github-sync](./hermes-skills-github-sync/) | Sync Hermes Agent skills to a GitHub repo with automatic categorization, README generation, and weekly cron job. Self-generated skills at root, pre-installed skills in subfolder. | 2026-10-04 |
| [kdocs-milestone-weekly-report](./kdocs-milestone-weekly-report/) | Use when 包1里程碑周报 needed. Kdocs sheet → fixed weekly report. | 2026-10-11 |
| [project-milestone-reporting](./project-milestone-reporting/) | 统计项目里程碑状态，生成客户版进展周报（含风险清单）。 | 2026-10-11 |

## 📦 外部安装的 Skills

| 技能 | 描述 | 来源 |
|------|------|------|
| [london-gold-cny](./london-gold-cny/) | 伦敦金人民币价格查询 - 自动将伦敦金价格转换为人民币/克单位 | JuniorSummer/Skills |

## 🏗️ 其他项目 Skills

| 技能 | 描述 |
|------|------|
| [llm-benchmark](./llm-benchmark/) | 大模型性能与能力基准测试工具 |
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Cron 任务环境变量故障排查 |

## 📂 Hermes 内置 Skills

Hermes Agent 自带的预装 skills 位于 [hermes_raw_skill/](./hermes_raw_skill/) 目录。
详见 [hermes_raw_skill/README.md](./hermes_raw_skill/README.md)。

---
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-10-11 22:26*
