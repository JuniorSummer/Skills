# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [cron-dup-messages](./cron-dup-messages/) | 定时任务重复消息调试 - 当定时任务同时发送重复消息时，分析并修复配置冲突 | 2026-04-29 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 | 2026-04-29 |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 | 2026-04-29 |
| [clawhub-skill-installation](./clawhub-skill-installation/) | ClawHub 镜像安装 skill 降级方案 - 当标准安装方法失败时的 API 发现、降级策略和手动安装 | 2026-04-29 |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取 ModelScope 魔搭社区最近更新的模型列表，按下载量排序 | 2026-04-29 |
| [llm-technical-comparison](./llm-technical-comparison/) | LLM 技术报告对比分析 - 提取参数、基准测试、定价和独特功能进行多模型比较 | 2026-04-26 |
| [playwright-scraper](./playwright-scraper/) | Playwright 动态网页抓取 - 支持 SPA、无限滚动、懒加载、需要认证交互的网站 | 2026-04-29 |

## 📦 外部安装的 Skills

| 技能 | 描述 | 来源 |
|------|------|------|
| [london-gold-cny](./london-gold-cny/) | 伦敦金人民币价格查询 - 自动将伦敦金价格转换为人民币/克单位 | [JuniorSummer/Skills](https://github.com/JuniorSummer/Skills) |

## 🏗️ 其他项目 Skills

| 技能 | 描述 |
|------|------|
| [llm-benchmark](./llm-benchmark/) | 大模型性能与能力基准测试工具 - 支持推理速度、批量吞吐、并发性能、显存占用测试 |
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Cron 任务环境变量故障排查 - 解决定时任务中环境变量丢失、文件权限问题 |

## 📂 Hermes 内置 Skills

Hermes Agent 自带的 78 个预装 skills 位于 [hermes_raw_skill/](./hermes_raw_skill/) 目录，涵盖 DevOps、Research、MLOps、Creative、Productivity 等多个领域。详见 [hermes_raw_skill/README.md](./hermes_raw_skill/README.md)。

---

*自动同步自 Hermes Agent skills 目录，每周日 22:00 更新。*
