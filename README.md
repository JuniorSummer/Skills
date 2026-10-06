# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [agent-cli-orchestration](./agent-cli-orchestration/) | Drive external coding-agent CLIs and verify their output. | 2026-10-04 |
| [cron-job-failure-diagnosis](./cron-job-failure-diagnosis/) | Diagnose cron job failures by checking job status, analyzing output logs, and identifying root cause (script vs LLM vs delivery). | 2026-09-30 |
| [cron-job-management](./cron-job-management/) | 管理/创建/审计定时任务。model/provider 用 hermes cron edit CLI 设置。 | 2026-09-30 |
| [macos-userland-provisioning](./macos-userland-provisioning/) | Install macOS apps and CLI tools without sudo/Homebrew. | 2026-10-04 |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序 | 2026-10-02 |
| [monthly-report-organizer](./monthly-report-organizer/) | 整理月报 - 将零散的月度工作记录整理成结构化月报格式 | 2026-10-06 |
| [tencent-docs-spreadsheet](./tencent-docs-spreadsheet/) | Read and write Tencent Docs (腾讯文档) spreadsheets. Documents the correct approach (MCP server), pitfalls of scraping attempts, and available WPS alternatives. | 2026-10-06 |
| [used-mac-hardware-check](./used-mac-hardware-check/) | Verify a second-hand Mac's hardware (二手 Mac 验机). | 2026-10-04 |
| [zsxq-daily-report-cron](./zsxq-daily-report-cron/) | 创建知识星球每日日报定时任务的完整方案。使用 zsxq-cli 采集前一天的主题和评论，通过 Python 脚本预处理后注入 cron prompt，由 LLM 整理成日报并发送到飞书。当需要设置知识星球内容监控、日报、周报等定时推送任务时使用。 | 2026-10-02 |

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
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-10-06 23:53*
