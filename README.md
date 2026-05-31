# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [aihot](./aihot/) | AI HOT (aihot.virxact.com) 中文 AI 资讯查询 Skill。当用户想知道"今天 AI 圈有什么"、"AI 日报"、"AI HOT"、"AI 资讯"、"AI 热点"、"最近 AI"、"OpenAI/Anthropic/Google 最近发布了什么"、"AI hot today"、"AI news today"、"看一下 AI 行业动态"、"今天有什么大模型发布"、"昨天 AI 圈"、"看下精选条目"、"AI HOT 精选"、"最近一周的 AI 论文"、"AI 模型发布"、"AI 产品发布"、"AI 行业动态"、"AI 技巧与观点" 等任何中文 AI 资讯查询时使用。即使用户只说"AI 圈"、"AI 新闻"、"AI 日报"，或者只是问"今天发生了什么"且上下文是 AI / 大模型 / LLM / 创业领域，也应该触发本 Skill。Skill 会直接 curl 公开 REST API 拉数据并整理成中文 markdown 简报，不需要用户配置任何 API Key 或 MCP server。**不要 undertrigger**——用户问 AI 资讯而你不调本 Skill 就是把过时的训练数据当作今日新闻，对用户有害。 | 2026-05-24 |
| [batch-file-desensitization](./batch-file-desensitization/) | Batch rename files to remove sensitive info — company names, person names, dates, document numbers. Typical for Chinese corporate document desensitization. | 2026-05-31 |
| [bilibili-video-analysis](./bilibili-video-analysis/) | Download and analyze Bilibili videos — extract metadata, comments, download video via API, extract frames with ffmpeg, and analyze with vision AI. Use when a user shares a Bilibili video URL and wants content analysis, game review, or visual breakdown. | 2026-05-24 |
| [clawhub-skill-installation](./clawhub-skill-installation/) | Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and manual skill installation. | 2026-05-24 |
| [cn-price-data-scraping](./cn-price-data-scraping/) | 爬取国内价格数据网站 - 国际油价(guojiyoujia.com)和台州造价网(tzzj.cn) | 2026-05-24 |
| [corporate-docs-to-wiki](./corporate-docs-to-wiki/) | Extract content from mixed corporate documents (PDF/DOCX/XLSX/PPTX) and generate a structured policy wiki for quick understanding of company policies, strategies, and trends. | 2026-05-31 |
| [cron-dup-messages](./cron-dup-messages/) | Debug and fix duplicate cron job message推送问题 - 当定时任务同时发送重复消息时，分析并修复配置冲突 | 2026-05-24 |
| [cron-job-failure-diagnosis](./cron-job-failure-diagnosis/) | Diagnose cron job failures by checking job status, analyzing output logs, and identifying root cause (script vs LLM vs delivery). | 2026-05-28 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 | 2026-05-24 |
| [curl-chinese-web-search](./curl-chinese-web-search/) | Use curl to search Chinese content via search engines (Bing, DuckDuckGo). Handles URL encoding of Chinese characters, HTML parsing, and article fetching. Use when web_search/browser tools are unavailable or timing out, and you need to search for Chinese-language content. | 2026-05-24 |
| [gameplay-video-wiki-analysis](./gameplay-video-wiki-analysis/) | Analyze gameplay videos (e.g. Honor of Kings, League of Legends) by combining frame-by-frame visual analysis with a domain-specific wiki knowledge base. Synthesize findings into actionable improvement advice and file as a wiki query page. | 2026-05-24 |
| [github-trending](./github-trending/) | Fetch and analyze GitHub Trending repositories - daily, weekly, and monthly trending projects with AI-powered analysis. | 2026-05-24 |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 | 2026-05-24 |
| [hermes-skills-github-sync](./hermes-skills-github-sync/) | Sync Hermes Agent skills to a GitHub repo with automatic categorization, README generation, and weekly cron job. Self-generated skills at root, pre-installed skills in subfolder. | 2026-05-24 |
| [llm-technical-comparison](./llm-technical-comparison/) | Comparative analysis workflow for LLM technical reports - extract parameters, benchmarks, pricing, and unique features from multiple models | 2026-05-24 |
| [llm-wiki](./llm-wiki/) | Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. Ingest sources, query compiled knowledge, and lint for consistency. | 2026-05-24 |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序 | 2026-05-24 |
| [nbs-economic-data](./nbs-economic-data/) | Fetch official Chinese macroeconomic data from National Bureau of Statistics (NBS/国家统计局). Access monthly economic reports, spokesperson Q&As, and data interpretations directly from stats.gov.cn. | 2026-05-31 |
| [ocr-and-documents](./ocr-and-documents/) | Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill. | 2026-05-24 |
| [time-restricted-cron](./time-restricted-cron/) | 创建时间限制的定时任务模式 - 当复杂cron表达式不可用时，使用Python包装脚本实现时间范围限制 | 2026-05-24 |
| [video-to-wiki-pipeline](./video-to-wiki-pipeline/) | Batch-analyze multiple videos and generate an interlinked LLM Wiki. End-to-end pipeline: download → extract frames → parallel vision analysis → wiki pages with cross-references. | 2026-05-24 |
| [weread-skills](./weread-skills/) | 微信读书助手 — 搜索书籍、管理书架、查看笔记划线、浏览书评、阅读统计、发现推荐好书 | 2026-05-24 |

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
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-05-31 22:00*
