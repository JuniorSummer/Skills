# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [chinese-award-doc-parsing](./chinese-award-doc-parsing/) | Parse Chinese corporate award/recognition notification documents (.doc/.docx) to extract person names, awards, and units. Common in state-owned enterprises and telecom companies. | 2026-06-09 |
| [tencent-docs-spreadsheet](./tencent-docs-spreadsheet/) | Read and write Tencent Docs (腾讯文档) spreadsheets. Documents the correct approach (MCP server), pitfalls of scraping attempts, and available WPS alternatives. | 2026-06-07 |

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
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-06-14 22:01*
