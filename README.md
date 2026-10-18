# Skills

Hermes Agent 自定义技能集合。本仓库存储 Hermes Agent 在使用过程中自主创建的 skills，以及从外部安装的 skills。

## 🚀 Hermes 自主生成的 Skills

以下是 Hermes Agent 在解决实际问题过程中自主编写和沉淀的技能：

| 技能 | 描述 | 创建日期 |
|------|------|---------|
| [agenthub-harness-sync](./agenthub-harness-sync/) | Use when AgentHub sync or harness proposals are in scope. | 2026-10-14 |
| [hermes-skills-github-sync](./hermes-skills-github-sync/) | Sync Hermes Agent skills to a GitHub repo with automatic categorization, README generation, and weekly cron job. Self-generated skills at root, pre-installed skills in subfolder. | 2026-10-11 |
| [kdocs-milestone-weekly-report](./kdocs-milestone-weekly-report/) | Use when 包1里程碑周报 needed. Kdocs sheet → fixed weekly report. | 2026-10-12 |
| [third-party-api-integration](./third-party-api-integration/) | Use when integrating or migrating a third-party REST API. | 2026-10-11 |

## 📦 外部安装的 Skills

| 技能 | 描述 | 来源 |
|------|------|------|
| [aihot](./aihot/) | 查询 AIHOT（aihot.news）的中文 AI 资讯。用户问今天或最近 AI 圈发生了什么、AI 新闻和 AI 日报、大模型与 AI 产品发布、OpenAI／Anthropic／Google 等公司或某个 AI 话题的最新消息、当前最热的 AI 事件及来龙去脉、AI 模型排行、Codex 额度重置，或其它 AI 行业动态时使用。必须实时查询 AIHOT，不凭训练记忆回答新闻；匿名只读，无需 API Key。 | https://aihot.news/aihot-skill/ |
| [baoyu-comic](./baoyu-comic/) | Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation. Use when user asks to create "知识漫画", "教育漫画", "biography comic", "tutorial comic", or "Logicomix-style comic". | 外部安装 |
| [baoyu-infographic](./baoyu-infographic/) | Generate professional infographics with 21 layout types and 21 visual styles. Analyzes content, recommends layout×style combinations, and generates publication-ready infographics. Use when user asks to create "infographic", "visual summary", "信息图", "可视化", or "高密度信息大图". | 外部安装 |
| [blogwatcher](./blogwatcher/) | Monitor blogs and RSS/Atom feeds for updates using the blogwatcher-cli tool. Add blogs, scan for new articles, track read status, and filter by category. | 外部安装 |
| [creative-ideation](./creative-ideation/) | Generate project ideas through creative constraints. Use when the user says 'I want to build something', 'give me a project idea', 'I'm bored', 'what should I make', 'inspire me', or any variant of 'I have tools but no direction'. Works for code, art, hardware, writing, tools, and anything that can be made. | 外部安装 |
| [himalaya](./himalaya/) | CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language). | 外部安装 |
| [humanizer](./humanizer/) | | | 外部安装 |
| [kdocs](./kdocs/) | 操作金山文档（WPS 云文档 / Kdocs / 365.kdocs.cn / www.kdocs.cn）云文档的官方 Skill。核心能力覆盖云端新建、读取、编辑、搜索、分享、整理在线文档（智能文档、Word、Excel、PDF、PPT、演示文稿、智能表格、多维表格）及个人知识库。当用户的任务涉及云文档操作时使用，包括但不限于：写周报/日报/工作汇报、处理合同/发票、创建报名表/登记表、网页剪藏、接龙转表格、信息收集、文档总结与内容生成、改写仿写、翻译、AI PPT生成、PDF拆分导出、标签分类归档、收藏管理、碎片笔记整理、表格美化、回收站还原、知识库管理。 | 外部安装 |
| [kill-ai-slop](./kill-ai-slop/) | >- | 外部安装 |
| [london-gold-cny](./london-gold-cny/) | 查询伦敦金价格，并自动转换为人民币/克单位。适合需要以人民币计价、按克计算黄金价格的场景。 | JuniorSummer/Skills |
| [maps](./maps/) | > | 外部安装 |
| [nano-pdf](./nano-pdf/) | Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make content changes to specific pages without manual editing. | 外部安装 |
| [notion](./notion/) | Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion workspaces directly from the terminal. | 外部安装 |
| [openhue](./openhue/) | Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. Turn lights on/off, adjust brightness, color, color temperature, and activate scenes. | 外部安装 |
| [pixel-art](./pixel-art/) | Convert images into retro pixel art with hardware-accurate palettes (NES, Game Boy, PICO-8, C64, etc.), and animate them into short videos. Presets cover arcade, SNES, and 10+ era-correct looks. Use `clarify` to let the user pick a style before generating. | 外部安装 |
| [playwright-scraper](./playwright-scraper/) | Use Playwright to scrape dynamic web pages with JavaScript rendering support. Ideal for scraping SPAs, infinite-scroll feeds, lazy-loaded content, and sites requiring authentication or interaction. | 外部安装 |
| [songsee](./songsee/) | Generate spectrograms and audio feature visualizations (mel, chroma, MFCC, tempogram, etc.) from audio files via CLI. Useful for audio analysis, music production debugging, and visual documentation. | 外部安装 |
| [tencent-docs](./tencent-docs/) | 腾讯文档（docs.qq.com）-在线云文档平台，是创建、编辑、管理文档的首选 skill。涉及"新建/创建/编辑/读取/查看/搜索文档"、"保存文件"、"云文档"、"腾讯文档"、"docs.qq.com"等操作，请优先使用本 skill。支持能力：(1) 创建各类在线文档（文档/Word/Excel/幻灯片/思维导图/流程图/智能表格/收集表）(2) 管理知识库空间（创建空间、查询空间列表）(3) 管理空间节点、文件夹结构 (4) 读取/搜索文档内容 (5) 编辑操作智能表 (6) 编辑操作在线文档 (7) 文件管理（重命名、移动、删除、复制、导入导出）(8) 网页剪藏、本地文件/文档上云。 | 外部安装 |
| [xurl](./xurl/) | Interact with X/Twitter via xurl, the official X API CLI. Use for posting, replying, quoting, searching, timelines, mentions, likes, reposts, bookmarks, follows, DMs, media upload, and raw v2 endpoint access. | 外部安装 |

## 🏗️ 其他项目 Skills

| 技能 | 描述 |
|------|------|
| [llm-benchmark](./llm-benchmark/) | 大模型性能与能力基准测试工具 |
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Cron 任务环境变量故障排查 |

## 📂 Hermes 内置 Skills

Hermes Agent 自带的预装 skills 位于 [hermes_raw_skill/](./hermes_raw_skill/) 目录。
详见 [hermes_raw_skill/README.md](./hermes_raw_skill/README.md)。

---
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-10-18 22:00*
