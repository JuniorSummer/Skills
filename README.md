# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [benchmark-leaderboard-monitor](./benchmark-leaderboard-monitor/) | | | 2026-08-17 |
| [clawhub-skill-installation](./clawhub-skill-installation/) | Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and manual skill installation. | 2026-08-18 |
| [ebbinghaus-memory-trainer](./ebbinghaus-memory-trainer/) | 艾宾浩斯记忆曲线训练系统 — 创建定时任务每天推送记忆训练内容，支持新学和复习的双向测试。覆盖设置跟踪文件、配置每日推送cron、处理图像型docx内容提取。 | 2026-08-20 |
| [weekly-report-organizer](./weekly-report-organizer/) | 整理周报 - 将零散的周进度笔记整理成结构化周报格式 | 2026-08-22 |

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
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-08-23 22:00*
