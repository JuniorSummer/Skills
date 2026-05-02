# Skills

Claude Code / Hermes Agent 自定义技能集合。

## 技能列表

### DevOps & Cron

| 技能 | 描述 |
|------|------|
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Cron 任务环境变量故障排查 - 解决定时任务中环境变量丢失、文件权限问题 |
| [cron-dup-messages](./cron-dup-messages/) | 定时任务重复消息调试 - 当定时任务同时发送重复消息时，分析并修复配置冲突 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 |

### Research & Data Science

| 技能 | 描述 |
|------|------|
| [llm-benchmark](./llm-benchmark/) | 大模型性能与能力基准测试工具 - 支持推理速度、批量吞吐、并发性能、显存占用测试 |
| [llm-technical-comparison](./llm-technical-comparison/) | LLM 技术报告对比分析 - 提取参数、基准测试、定价和独特功能进行多模型比较 |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取 ModelScope 魔搭社区最近更新的模型列表，按下载量排序 |

### Productivity

| 技能 | 描述 |
|------|------|
| [london-gold-cny](./london-gold-cny/) | 伦敦金人民币价格查询 - 自动将伦敦金价格转换为人民币/克单位 |
| [playwright-scraper](./playwright-scraper/) | Playwright 动态网页抓取 - 支持 SPA、无限滚动、懒加载、需要认证交互的网站 |

### Software Development

| 技能 | 描述 |
|------|------|
| [clawhub-skill-installation](./clawhub-skill-installation/) | ClawHub 镜像安装 skill 降级方案 - 当标准安装方法失败时的 API 发现、降级策略和手动安装 |

---

*自动同步自 Hermes Agent skills 目录，每周日 22:00 更新。*
