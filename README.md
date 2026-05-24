# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 |
|------|------|
| [aihot](./aihot/) | AI HOT (aihot.virxact.com) 中文 AI 资讯查询 Skill。当用户想知道"今天 AI 圈有什么"、"AI 日报"、"AI HOT"、"AI 资讯"、"AI 热点"、"最近 AI"、"OpenAI/Anthropi... |
| [bilibili-video-analysis](./bilibili-video-analysis/) | Download and analyze Bilibili videos — extract metadata, comments, download video via API, extract frames with ffmpeg, a... |
| [clawhub-skill-installation](./clawhub-skill-installation/) | Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and ma... |
| [cn-price-data-scraping](./cn-price-data-scraping/) | 爬取国内价格数据网站 - 国际油价(guojiyoujia.com)和台州造价网(tzzj.cn) |
| [cron-dup-messages](./cron-dup-messages/) | Debug and fix duplicate cron job message推送问题 - 当定时任务同时发送重复消息时，分析并修复配置冲突 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 |
| [curl-chinese-web-search](./curl-chinese-web-search/) | Use curl to search Chinese content via search engines (Bing, DuckDuckGo). Handles URL encoding of Chinese characters, HT... |
| [gameplay-video-wiki-analysis](./gameplay-video-wiki-analysis/) | Analyze gameplay videos (e.g. Honor of Kings, League of Legends) by combining frame-by-frame visual analysis with a doma... |
| [github-trending](./github-trending/) | Fetch and analyze GitHub Trending repositories - daily, weekly, and monthly trending projects with AI-powered analysis. |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 |
| [hermes-skills-github-sync](./hermes-skills-github-sync/) | Sync Hermes Agent skills to a GitHub repo with automatic categorization, README generation, and weekly cron job. Self-ge... |
| [llm-technical-comparison](./llm-technical-comparison/) | Comparative analysis workflow for LLM technical reports - extract parameters, benchmarks, pricing, and unique features f... |
| [llm-wiki](./llm-wiki/) | Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. Ingest sources, query compil... |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序 |
| [ocr-and-documents](./ocr-and-documents/) | Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker... |
| [time-restricted-cron](./time-restricted-cron/) | 创建时间限制的定时任务模式 - 当复杂cron表达式不可用时，使用Python包装脚本实现时间范围限制 |
| [video-to-wiki-pipeline](./video-to-wiki-pipeline/) | Batch-analyze multiple videos and generate an interlinked LLM Wiki. End-to-end pipeline: download → extract frames → par... |
| [weread-skills](./weread-skills/) | 微信读书助手 — 搜索书籍、管理书架、查看笔记划线、浏览书评、阅读统计、发现推荐好书 |

## 📦 外部安装的 Skills (ClawHub/Community)

| 技能 | 描述 | 来源 |
|------|------|------|
| [baoyu-comic](./baoyu-comic/) | Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed pane... | ClawHub/Community |
| [baoyu-infographic](./baoyu-infographic/) | Generate professional infographics with 21 layout types and 21 visual styles. Analyzes content, recommends layout×style ... | ClawHub/Community |
| [blogwatcher](./blogwatcher/) | Monitor blogs and RSS/Atom feeds for updates using the blogwatcher-cli tool. Add blogs, scan for new articles, track rea... | ClawHub/Community |
| [creative-ideation](./creative-ideation/) | Generate project ideas through creative constraints. Use when the user says 'I want to build something', 'give me a proj... | ClawHub/Community |
| [himalaya](./himalaya/) | CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from ... | ClawHub/Community |
| [humanizer](./humanizer/) | | | ClawHub/Community |
| [london-gold-cny](./london-gold-cny/) | 查询伦敦金价格，并自动转换为人民币/克单位。适合需要以人民币计价、按克计算黄金价格的场景。 | ClawHub/Community |
| [maps](./maps/) | > | ClawHub/Community |
| [nano-pdf](./nano-pdf/) | Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make con... | ClawHub/Community |
| [notion](./notion/) | Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion wor... | ClawHub/Community |
| [openhue](./openhue/) | Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. Turn lights on/off, adjust brightness, color, color t... | ClawHub/Community |
| [pixel-art](./pixel-art/) | Convert images into retro pixel art with hardware-accurate palettes (NES, Game Boy, PICO-8, C64, etc.), and animate them... | ClawHub/Community |
| [playwright-scraper](./playwright-scraper/) | Use Playwright to scrape dynamic web pages with JavaScript rendering support. Ideal for scraping SPAs, infinite-scroll f... | ClawHub/Community |
| [songsee](./songsee/) | Generate spectrograms and audio feature visualizations (mel, chroma, MFCC, tempogram, etc.) from audio files via CLI. Us... | ClawHub/Community |
| [xurl](./xurl/) | Interact with X/Twitter via xurl, the official X API CLI. Use for posting, replying, quoting, searching, timelines, ment... | ClawHub/Community |

## 🏗️ 其他项目 Skills

| 技能 | 描述 |
|------|------|
| [llm-benchmark](./llm-benchmark/) | 大模型性能与能力基准测试工具 |
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Cron 任务环境变量故障排查 |

## 📂 Hermes 内置 Skills

Hermes Agent 自带的预装 skills 位于 [hermes_raw_skill/](./hermes_raw_skill/) 目录。
详见 [hermes_raw_skill/README.md](./hermes_raw_skill/README.md)。

---
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-05-24 22:31*
