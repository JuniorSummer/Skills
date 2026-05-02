# Skills

Claude Code / Hermes Agent 自定义技能集合。

## 技能列表

### DevOps & Cron

| 技能 | 描述 |
|------|------|
| [cron-dup-messages](./cron-dup-messages/) | Debug and fix duplicate cron job message推送问题 - 当定时任务同时发送重复消息时，分析并修复配置冲突 |
| [cron-script-output-handling](./cron-script-output-handling/) | Cron Job 脚本输出处理模式 - 控制是否让 LLM 处理脚本输出，还是直接发送原始输出 |
| [cronjob-env-troubleshooting](./cronjob-env-troubleshooting/) | Debug and fix cron jobs that appear to succeed but produce no output. Covers why terminal-exported variables don't persist, why ~/.bashrc doesn't help, and how to properly configure env vars in cron jobs. |
| [hermes-gateway-cron-debug](./hermes-gateway-cron-debug/) | Hermes Gateway 进程卡死导致定时任务失效的排查与修复 |
| [time-restricted-cron](./time-restricted-cron/) | 创建时间限制的定时任务模式 - 当复杂cron表达式不可用时，使用Python包装脚本实现时间范围限制 |

### Research & Data Science

| 技能 | 描述 |
|------|------|
| [llm-technical-comparison](./llm-technical-comparison/) | Comparative analysis workflow for LLM technical reports - extract parameters, benchmarks, pricing, and unique features from multiple models |
| [llm-wiki](./llm-wiki/) | Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. Ingest sources, query compiled knowledge, and lint for consistency. |
| [modelscope-recent-models](./modelscope-recent-models/) | 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序 |
| [video-to-wiki-pipeline](./video-to-wiki-pipeline/) | Batch-analyze multiple videos and generate an interlinked LLM Wiki. End-to-end pipeline: download → extract frames → parallel vision analysis → wiki pages with cross-references. |

### Productivity

| 技能 | 描述 |
|------|------|
| [london-gold-cny](./london-gold-cny/) | 查询伦敦金价格，并自动转换为人民币/克单位。适合需要以人民币计价、按克计算黄金价格的场景。 |
| [playwright-scraper](./playwright-scraper/) | Use Playwright to scrape dynamic web pages with JavaScript rendering support. Ideal for scraping SPAs, infinite-scroll feeds, lazy-loaded content, and sites requiring authentication or interaction. |

### Software Development

| 技能 | 描述 |
|------|------|
| [clawhub-skill-installation](./clawhub-skill-installation/) | Install skills from ClawHub mirrors when standard hermes methods fail. Covers API discovery, fallback strategies, and manual skill installation. |

### Media

| 技能 | 描述 |
|------|------|
| [bilibili-video-analysis](./bilibili-video-analysis/) | Download and analyze Bilibili videos — extract metadata, comments, download video via API, extract frames with ffmpeg, and analyze with vision AI. Use when a user shares a Bilibili video URL and wants content analysis, game review, or visual breakdown. |

### GitHub

| 技能 | 描述 |
|------|------|
| [github-auth](./github-auth/) | Set up GitHub authentication for the agent using git (universally available) or the gh CLI. Covers HTTPS tokens, SSH keys, credential helpers, and gh auth — with a detection flow to pick the right method automatically. |
| [github-code-review](./github-code-review/) | Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-issues](./github-issues/) | Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-pr-workflow](./github-pr-workflow/) | Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-repo-management](./github-repo-management/) | Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-trending](./github-trending/) | Fetch and analyze GitHub Trending repositories - daily, weekly, and monthly trending projects with AI-powered analysis. |

### Other

| 技能 | 描述 |
|------|------|
| [apple-notes](./apple-notes/) | Manage Apple Notes via the memo CLI on macOS (create, view, search, edit). |
| [apple-reminders](./apple-reminders/) | Manage Apple Reminders via remindctl CLI (list, add, complete, delete). |
| [architecture-diagram](./architecture-diagram/) | Generate dark-themed SVG diagrams of software systems and cloud infrastructure as standalone HTML files with inline SVG graphics. Semantic component colors (cyan=frontend, emerald=backend, violet=database, amber=cloud/AWS, rose=security, orange=message bus), JetBrains Mono font, grid background. Best suited for software architecture, cloud/VPC topology, microservice maps, service-mesh diagrams, database + API layer diagrams, security groups, message buses — anything that fits a tech-infra deck with a dark aesthetic. If a more specialized diagramming skill exists for the subject (scientific, educational, hand-drawn, animated, etc.), prefer that — otherwise this skill can also serve as a general-purpose SVG diagram fallback. Based on Cocoon AI's architecture-diagram-generator (MIT). |
| [arxiv](./arxiv/) | Search and retrieve academic papers from arXiv using their free REST API. No API key needed. Search by keyword, author, category, or ID. Combine with web_extract or the ocr-and-documents skill to read full paper content. |
| [ascii-art](./ascii-art/) | Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs (asciified, ascii.co.uk), and LLM fallback. No API keys required. |
| [ascii-video](./ascii-video/) | Production pipeline for ASCII art video — any format. Converts video/audio/images/generative input into colored ASCII character video output (MP4, GIF, image sequence). Covers: video-to-ASCII conversion, audio-reactive music visualizers, generative ASCII art animations, hybrid video+audio reactive, text/lyrics overlays, real-time terminal rendering. Use when users request: ASCII video, text art video, terminal-style video, character art animation, retro text visualization, audio visualizer in ASCII, converting video to ASCII art, matrix-style effects, or any animated ASCII output. |
| [audiocraft](./audiocraft/) | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text descriptions, create sound effects, or perform melody-conditioned music generation. |
| [axolotl](./axolotl/) | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support |
| [baoyu-comic](./baoyu-comic/) | Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation. Use when user asks to create "知识漫画", "教育漫画", "biography comic", "tutorial comic", or "Logicomix-style comic". |
| [baoyu-infographic](./baoyu-infographic/) | Generate professional infographics with 21 layout types and 21 visual styles. Analyzes content, recommends layout×style combinations, and generates publication-ready infographics. Use when user asks to create "infographic", "visual summary", "信息图", "可视化", or "高密度信息大图". |
| [blogwatcher](./blogwatcher/) | Monitor blogs and RSS/Atom feeds for updates using the blogwatcher-cli tool. Add blogs, scan for new articles, track read status, and filter by category. |
| [claude-code](./claude-code/) | Delegate coding tasks to Claude Code (Anthropic's CLI agent). Use for building features, refactoring, PR reviews, and iterative coding. Requires the claude CLI installed. |
| [codebase-inspection](./codebase-inspection/) | Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. Use when asked to check lines of code, repo size, language composition, or codebase stats. |
| [codex](./codex/) | Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fixing. Requires the codex CLI and a git repository. |
| [creative-ideation](./creative-ideation/) | Generate project ideas through creative constraints. Use when the user says 'I want to build something', 'give me a project idea', 'I'm bored', 'what should I make', 'inspire me', or any variant of 'I have tools but no direction'. Works for code, art, hardware, writing, tools, and anything that can be made. |
| [design-md](./design-md/) | Author, validate, diff, and export DESIGN.md files — Google's open-source format spec that gives coding agents a persistent, structured understanding of a design system (tokens + rationale in one file). Use when building a design system, porting style rules between projects, generating UI with consistent brand, or auditing accessibility/contrast. |
| [dogfood](./dogfood/) | Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports |
| [dspy](./dspy/) | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming |
| [excalidraw](./excalidraw/) | Create hand-drawn style diagrams using Excalidraw JSON format. Generate .excalidraw files for architecture diagrams, flowcharts, sequence diagrams, concept maps, and more. Files can be opened at excalidraw.com or uploaded for shareable links. |
| [findmy](./findmy/) | Track Apple devices and AirTags via FindMy.app on macOS using AppleScript and screen capture. |
| [gif-search](./gif-search/) | Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. Useful for finding reaction GIFs, creating visual content, and sending GIFs in chat. |
| [godmode](./godmode/) | Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC system prompt templates, ULTRAPLINIAN multi-model racing, encoding escalation, and Hermes-native prefill/system prompt integration. Use when a user wants to bypass safety filters, jailbreak a model, or red-team model robustness. |
| [google-workspace](./google-workspace/) | Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the Google Workspace CLI (`gws`) when available for broader API coverage, and falls back to the Python client libraries otherwise. |
| [heartmula](./heartmula/) | Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + tags with multilingual support. |
| [hermes-agent](./hermes-agent/) | Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. Load this skill when helping users configure Hermes, troubleshoot issues, spawn agent instances, or make code contributions. |
| [himalaya](./himalaya/) | CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language). |
| [huggingface-hub](./huggingface-hub/) | Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints, manage Spaces and buckets. |
| [imessage](./imessage/) | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| [jupyter-live-kernel](./jupyter-live-kernel/) | > |
| [linear](./linear/) | Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All operations via curl — no dependencies. |
| [llama-cpp](./llama-cpp/) | llama.cpp local GGUF inference + HF Hub model discovery. |
| [lm-evaluation-harness](./lm-evaluation-harness/) | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs. |
| [manim-video](./manim-video/) | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style explainer videos, algorithm visualizations, equation derivations, architecture diagrams, and data stories. Use when users request: animated explanations, math animations, concept visualizations, algorithm walkthroughs, technical explainers, 3Blue1Brown style videos, or any programmatic animation with geometric/mathematical content. |
| [maps](./maps/) | > |
| [minecraft-modpack-server](./minecraft-modpack-server/) | Set up a modded Minecraft server from a CurseForge/Modrinth server pack zip. Covers NeoForge/Forge install, Java version, JVM tuning, firewall, LAN config, backups, and launch scripts. |
| [nano-pdf](./nano-pdf/) | Edit PDFs with natural-language instructions using the nano-pdf CLI. Modify text, fix typos, update titles, and make content changes to specific pages without manual editing. |
| [native-mcp](./native-mcp/) | Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers them as native Hermes Agent tools. Supports stdio and HTTP transports with automatic reconnection, security filtering, and zero-config tool injection. |
| [notion](./notion/) | Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query Notion workspaces directly from the terminal. |
| [obliteratus](./obliteratus/) | Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-means, SVD, whitened SVD, LEACE, SAE decomposition, etc.) to excise guardrails while preserving reasoning. 9 CLI methods, 28 analysis modules, 116 model presets across 5 compute tiers, tournament evaluation, and telemetry-driven recommendations. Use when a user wants to uncensor, abliterate, or remove refusal from an LLM. |
| [obsidian](./obsidian/) | Read, search, and create notes in the Obsidian vault. |
| [ocr-and-documents](./ocr-and-documents/) | Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill. |
| [opencode](./opencode/) | Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonomous sessions. Requires the opencode CLI installed and authenticated. |
| [openhue](./openhue/) | Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. Turn lights on/off, adjust brightness, color, color temperature, and activate scenes. |
| [outlines](./outlines/) | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library |
| [p5js](./p5js/) | Production pipeline for interactive and generative visual art using p5.js. Creates browser-based sketches, generative art, data visualizations, interactive experiences, 3D scenes, audio-reactive visuals, and motion graphics — exported as HTML, PNG, GIF, MP4, or SVG. Covers: 2D/3D rendering, noise and particle systems, flow fields, shaders (GLSL), pixel manipulation, kinetic typography, WebGL scenes, audio analysis, mouse/keyboard interaction, and headless high-res export. Use when users request: p5.js sketches, creative coding, generative art, interactive visualizations, canvas animations, browser-based visual art, data viz, shader effects, or any p5.js project. |
| [pixel-art](./pixel-art/) | Convert images into retro pixel art with hardware-accurate palettes (NES, Game Boy, PICO-8, C64, etc.), and animate them into short videos. Presets cover arcade, SNES, and 10+ era-correct looks. Use `clarify` to let the user pick a style before generating. |
| [plan](./plan/) | Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work. |
| [pokemon-player](./pokemon-player/) | Play Pokemon games autonomously via headless emulation. Starts a game server, reads structured game state from RAM, makes strategic decisions, and sends button inputs — all from the terminal. |
| [polymarket](./polymarket/) | Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. Read-only via public REST APIs, no API key needed. |
| [popular-web-designs](./popular-web-designs/) | > |
| [powerpoint](./powerpoint/) | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill. |
| [requesting-code-review](./requesting-code-review/) | > |
| [research-paper-writing](./research-paper-writing/) | End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and submission. Covers NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Integrates automated experiment monitoring, statistical analysis, iterative writing, and citation verification. |
| [segment-anything](./segment-anything/) | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image. |
| [songsee](./songsee/) | Generate spectrograms and audio feature visualizations (mel, chroma, MFCC, tempogram, etc.) from audio files via CLI. Useful for audio analysis, music production debugging, and visual documentation. |
| [songwriting-and-ai-music](./songwriting-and-ai-music/) | > |
| [spotify](./spotify/) | Control Spotify — play music, search the catalog, manage playlists and library, inspect devices and playback state. Loads when the user asks to play/pause/queue music, search tracks/albums/artists, manage playlists, or check what's playing. Assumes the Hermes Spotify toolset is enabled and `hermes auth spotify` has been run. |
| [subagent-driven-development](./subagent-driven-development/) | Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review (spec compliance then code quality). |
| [systematic-debugging](./systematic-debugging/) | Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation — NO fixes without understanding the problem first. |
| [test-driven-development](./test-driven-development/) | Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle with test-first approach. |
| [trl-fine-tuning](./trl-fine-tuning/) | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers. |
| [unsloth](./unsloth/) | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization |
| [vllm](./vllm/) | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism. |
| [webhook-subscriptions](./webhook-subscriptions/) | Create and manage webhook subscriptions for event-driven agent activation, or for direct push notifications (zero LLM cost). Use when the user wants external services to trigger agent runs OR push notifications to chats. |
| [weights-and-biases](./weights-and-biases/) | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform |
| [writing-plans](./writing-plans/) | Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. |
| [xurl](./xurl/) | Interact with X/Twitter via xurl, the official X API CLI. Use for posting, replying, quoting, searching, timelines, mentions, likes, reposts, bookmarks, follows, DMs, media upload, and raw v2 endpoint access. |
| [youtube-content](./youtube-content/) | > |

---
*自动同步自 Hermes Agent skills 目录，最后更新: 2026-05-02 18:46*
