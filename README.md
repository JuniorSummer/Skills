# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [bilibili-video-analysis](./bilibili-video-analysis/) | Download and analyze Bilibili videos — extract metadata, comments, download video via API, extract frames with ffmpeg, a... | 2026-05-02 |
| [clawhub-skill-installation](./clawhub-skill-installation/) | Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and ma... | 2026-04-29 |
| [cron-dup-messages](./cron-dup-messages/) | Debug and fix duplicate cron job message推送问题 - 当定时任务同时发送重复消息时，分析并修复配置冲突 | 2026-04-29 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 | 2026-05-02 |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 | 2026-04-29 |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序 | 2026-04-29 |
| [playwright-scraper](./playwright-scraper/) | Use Playwright to scrape dynamic web pages with JavaScript rendering support. Ideal for scraping SPAs, infinite-scroll f... | 2026-04-29 |

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
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-05-03 22:01*
