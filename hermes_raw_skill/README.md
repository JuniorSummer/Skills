# Hermes Agent 内置 Skills

Hermes Agent 预装的技能集合。

## 目录

- [🤖 AI Agent 自治框架](#autonomous-ai-agents)
- [🎨 创意内容生成](#creative)
- [📊 数据科学](#data-science)
- [⚙️ DevOps & 自动化](#devops)
- [📧 邮件管理](#email)
- [🎮 游戏](#gaming)
- [🐙 GitHub 工作流](#github)
- [🎬 媒体处理](#media)
- [🧠 MLOps & 模型训练](#mlops)
- [📝 笔记管理](#note-taking)
- [💼 生产力工具](#productivity)
- [🔴 红队测试](#red-teaming)
- [📚 学术研究](#research)
- [📱 社交媒体](#social-media)
- [💻 软件开发](#software-development)

---

## 🤖 AI Agent 自治框架 {#autonomous-ai-agents}

| 技能 | 描述 |
|------|------|
| [claude-code](./claude-code/) | Delegate coding to Claude Code CLI (features, PRs). |
| [codex](./codex/) | Delegate coding to OpenAI Codex CLI (features, PRs). |
| [hermes-agent](./hermes-agent/) | Use, configure, theme, extend, and orchestrate Hermes Agent. |
| [opencode](./opencode/) | Delegate coding to OpenCode CLI (features, PR review). |

## 🎨 创意内容生成 {#creative}

| 技能 | 描述 |
|------|------|
| [architecture-diagram](./architecture-diagram/) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| [ascii-art](./ascii-art/) | Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs (asciified, ascii.co.uk), and LLM fallback. No API keys required. |
| [ascii-video](./ascii-video/) | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| [baoyu-infographic](./baoyu-infographic/) | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| [design-md](./design-md/) | Author/validate/export Google's DESIGN.md token spec files. |
| [excalidraw](./excalidraw/) | Create hand-drawn style diagrams using Excalidraw JSON format. Generate .excalidraw files for architecture diagrams, flowcharts, sequence diagrams, concept maps, and more. Files can be opened at excalidraw.com or uploaded for shareable links. |
| [manim-video](./manim-video/) | Manim CE animations: 3Blue1Brown math/algo videos. |
| [p5js](./p5js/) | p5.js sketches: gen art, shaders, interactive, 3D. |
| [popular-web-designs](./popular-web-designs/) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| [songwriting-and-ai-music](./songwriting-and-ai-music/) | Songwriting craft and Suno AI music prompts. |

## 📊 数据科学 {#data-science}

| 技能 | 描述 |
|------|------|
| [jupyter-live-kernel](./jupyter-live-kernel/) | > |

## ⚙️ DevOps & 自动化 {#devops}

| 技能 | 描述 |
|------|------|
| [dogfood](./dogfood/) | Exploratory QA of web apps: find bugs, evidence, reports. |
| [native-mcp](./native-mcp/) | Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers them as native Hermes Agent tools. Supports stdio and HTTP transports with automatic reconnection, security filtering, and zero-config tool injection. |
| [webhook-subscriptions](./webhook-subscriptions/) | Create and manage webhook subscriptions for event-driven agent activation, or for direct push notifications (zero LLM cost). Use when the user wants external services to trigger agent runs OR push notifications to chats. |

## 📧 邮件管理 {#email}

| 技能 | 描述 |
|------|------|
| [himalaya](./himalaya/) | Himalaya CLI: IMAP/SMTP email from terminal. |

## 🎮 游戏 {#gaming}

| 技能 | 描述 |
|------|------|
| [minecraft-modpack-server](./minecraft-modpack-server/) | Set up a modded Minecraft server from a CurseForge/Modrinth server pack zip. Covers NeoForge/Forge install, Java version, JVM tuning, firewall, LAN config, backups, and launch scripts. |
| [pokemon-player](./pokemon-player/) | Play Pokemon games autonomously via headless emulation. Starts a game server, reads structured game state from RAM, makes strategic decisions, and sends button inputs — all from the terminal. |

## 🐙 GitHub 工作流 {#github}

| 技能 | 描述 |
|------|------|
| [codebase-inspection](./codebase-inspection/) | Inspect codebases w/ pygount: LOC, languages, ratios. |
| [github-auth](./github-auth/) | Set up GitHub authentication for the agent using git (universally available) or the gh CLI. Covers HTTPS tokens, SSH keys, credential helpers, and gh auth — with a detection flow to pick the right method automatically. |
| [github-code-review](./github-code-review/) | Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-issues](./github-issues/) | Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-pr-workflow](./github-pr-workflow/) | Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-repo-management](./github-repo-management/) | Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works with gh CLI or falls back to git + GitHub REST API via curl. |

## 🎬 媒体处理 {#media}

| 技能 | 描述 |
|------|------|
| [gif-search](./gif-search/) | Search/download GIFs from Tenor via curl + jq. |
| [heartmula](./heartmula/) | Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + tags with multilingual support. |
| [songsee](./songsee/) | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| [spotify](./spotify/) | Control Spotify — play music, search the catalog, manage playlists and library, inspect devices and playback state. Loads when the user asks to play/pause/queue music, search tracks/albums/artists, manage playlists, or check what's playing. Assumes the Hermes Spotify toolset is enabled and `hermes auth spotify` has been run. |
| [youtube-content](./youtube-content/) | YouTube transcripts to summaries, threads, blogs. |

## 🧠 MLOps & 模型训练 {#mlops}

| 技能 | 描述 |
|------|------|
| [audiocraft](./audiocraft/) | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text descriptions, create sound effects, or perform melody-conditioned music generation. |
| [axolotl](./axolotl/) | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support |
| [dspy](./dspy/) | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming |
| [huggingface-hub](./huggingface-hub/) | Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints, manage Spaces and buckets. |
| [llama-cpp](./llama-cpp/) | llama.cpp local GGUF inference + HF Hub model discovery. |
| [lm-evaluation-harness](./lm-evaluation-harness/) | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs. |
| [obliteratus](./obliteratus/) | Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-means, SVD, whitened SVD, LEACE, SAE decomposition, etc.) to excise guardrails while preserving reasoning. 9 CLI methods, 28 analysis modules, 116 model presets across 5 compute tiers, tournament evaluation, and telemetry-driven recommendations. Use when a user wants to uncensor, abliterate, or remove refusal from an LLM. |
| [outlines](./outlines/) | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library |
| [segment-anything](./segment-anything/) | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image. |
| [trl-fine-tuning](./trl-fine-tuning/) | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers. |
| [unsloth](./unsloth/) | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization |
| [vllm](./vllm/) | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism. |
| [weights-and-biases](./weights-and-biases/) | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform |

## 📝 笔记管理 {#note-taking}

| 技能 | 描述 |
|------|------|
| [obsidian](./obsidian/) | Read, search, create, and edit notes in the Obsidian vault. |

## 💼 生产力工具 {#productivity}

| 技能 | 描述 |
|------|------|
| [agent-config-export](./agent-config-export/) | Export AI agent config as a sanitized read-only package. |
| [airtable](./airtable/) | Airtable REST API via curl. Records CRUD, filters, upserts. |
| [apple-notes](./apple-notes/) | Manage Apple Notes via memo CLI: create, search, edit. |
| [apple-reminders](./apple-reminders/) | Apple Reminders via remindctl: add, list, complete. |
| [blocked-page-recovery](./blocked-page-recovery/) | Use when a fetch fails: 403/429, paywall, WAF, bot wall. |
| [box](./box/) | Box manages cloud files, sharing, search, and metadata. |
| [claude-code-plugins](./claude-code-plugins/) | Install, manage, and troubleshoot Claude Code plugins from GitHub marketplaces. Covers marketplace setup, plugin installation, common errors, and workarounds. |
| [claude-design](./claude-design/) | Design one-off HTML artifacts (landing, deck, prototype). |
| [cms-find-skills](./cms-find-skills/) | 用于"安装 Skill / 下载 Skill / 找一个能做 X 的 Skill / 把某个 Skill 装到本地 / 列出平台 Skill"。从 CMS 平台搜索已有 Skill 并按 downloadUrl 下载 ZIP 解压到本地 ~/.claude/skills。仅负责查找与安装，不负责创建或发布 |
| [coding-agent-delegation](./coding-agent-delegation/) | Use when delegating work to a coding agent; verify results. |
| [competitor-news-monitor](./competitor-news-monitor/) | Watch named companies for material news; cited digests. |
| [computer-use](./computer-use/) | Drive the desktop background-first; escalate on signal. |
| [delegated-agent-runs](./delegated-agent-runs/) | Use when delegating a long job to an agent CLI. |
| [delegating-to-coding-agents](./delegating-to-coding-agents/) | Use when delegating work to a coding-agent CLI. |
| [delivery-readiness-review](./delivery-readiness-review/) | Use when judging delivery progress from an issue log. |
| [document-to-action-items](./document-to-action-items/) | Extract cited obligations, deadlines, tasks from documents. |
| [docx](./docx/) | Create, read, edit, template, and review Word .docx files. |
| [email-inbox-triage](./email-inbox-triage/) | Triage an inbox: prioritize threads, draft replies safely. |
| [feishu-docs](./feishu-docs/) | Use when the user links a Feishu doc or 智能纪要. |
| [feynman-coach](./feynman-coach/) | | |
| [findmy](./findmy/) | Track Apple devices/AirTags via FindMy.app on macOS. |
| [github](./github/) | GitHub via gh CLI: PRs, issues, reviews, repos, auth. |
| [google-workspace](./google-workspace/) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| [grounded-citations](./grounded-citations/) | Ground answers and documents in cited, verifiable sources. |
| [hermes-agent-skill-authoring](./hermes-agent-skill-authoring/) | Author in-repo SKILL.md files: frontmatter and structure. |
| [hermes-migration](./hermes-migration/) | Use when migrating a Hermes install between machines or cutting jobs over. |
| [humanizer](./humanizer/) | Humanize text: strip AI-isms and add real voice. |
| [hyperframes](./hyperframes/) | Render MP4/WebM videos from HTML compositions. |
| [imessage](./imessage/) | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| [inspecting-hermes-desktop-dom](./inspecting-hermes-desktop-dom/) | Read the live Hermes desktop DOM/CSS over CDP. |
| [kaze-12-prompts](./kaze-12-prompts/) | 12 个通用 AI 提示词模板库,覆盖 5 大场景(问清问题/学习/解决问题/决策/认识自己)。当用户需要理清困惑、学习新概念、拆解优秀案例、研究陌生领域、核查事实、解决复杂问题、做决策、挖掘天赋、规划人生时,自动推荐并生成对应 prompt 模板。触发信号:苏格拉底提问、双层解释、反向拆解、横纵分析、事实核查、专家会诊、第一性原理、跨领域借解、钢人论证、最小实验、天赋挖掘、人生设计,以及"帮我理清/讲讲/解释下/怎么选/纠结/选哪个/学一下/分析这个/靠谱吗/真的假的/我适合什么"等相近表达。命中意图时先推荐模板,用户确认后替换【】占位符输出完整可复制 prompt。 |
| [knowledge-base](./knowledge-base/) | (无描述) |
| [linear](./linear/) | Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All operations via curl — no dependencies. |
| [mac-hardware-verification](./mac-hardware-verification/) | Use when verifying a used Mac or its hardware health. |
| [macos-host-provisioning](./macos-host-provisioning/) | Use when setting up a Mac host or installing without admin. |
| [macos-local-dev-stack](./macos-local-dev-stack/) | Use when installing tools on a mac without admin rights. |
| [maps](./maps/) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| [mcp-oauth-onboarding](./mcp-oauth-onboarding/) | Use when an MCP server needs OAuth or returns 401. |
| [meeting-action-items](./meeting-action-items/) | Turn meeting notes into cited decisions, owners, tickets. |
| [meeting-minutes-digest](./meeting-minutes-digest/) | Use when digesting meeting minutes daily or weekly. |
| [node-inspect-debugger](./node-inspect-debugger/) | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| [notes](./notes/) | (无描述) |
| [notion](./notion/) | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| [pdf](./pdf/) | PDF files: create, read, merge, fill, OCR, edit text. |
| [powerpoint](./powerpoint/) | Create, read, edit .pptx decks with python-pptx. |
| [product-price-monitor](./product-price-monitor/) | Watch product, flight, or listing prices; alert on target. |
| [python-debugpy](./python-debugpy/) | Debug Python: pdb REPL + debugpy remote (DAP). |
| [reddit-reading](./reddit-reading/) | Read Reddit: subreddits, search, threads, users. No browser. |
| [remotion](./remotion/) | Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays |
| [rss-feeds](./rss-feeds/) | Read RSS, Atom, JSON feeds; discover feeds behind a page. |
| [sdlc-review](./sdlc-review/) | Review Kanban handoffs and route verified outcomes. |
| [simplify-code](./simplify-code/) | Parallel 4-agent cleanup of recent code changes. |
| [skills](./skills/) | (无描述) |
| [spike](./spike/) | Throwaway experiments to validate an idea before build. |
| [teams-meeting-pipeline](./teams-meeting-pipeline/) | Teams meeting summaries, job replay, Graph subscriptions. |
| [verify-offline-html](./verify-offline-html/) | Use when verifying a self-contained HTML tool really works. |
| [weekly-review-planning](./weekly-review-planning/) | Weekly reset: commitments, stalled work, next-week plan. |
| [xlsx](./xlsx/) | Create, read, edit Excel .xlsx workbooks and CSVs. |

## 🔴 红队测试 {#red-teaming}

| 技能 | 描述 |
|------|------|
| [godmode](./godmode/) | Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC system prompt templates, ULTRAPLINIAN multi-model racing, encoding escalation, and Hermes-native prefill/system prompt integration. Use when a user wants to bypass safety filters, jailbreak a model, or red-team model robustness. |

## 📚 学术研究 {#research}

| 技能 | 描述 |
|------|------|
| [arxiv](./arxiv/) | Search arXiv papers by keyword, author, category, or ID. |
| [llm-wiki](./llm-wiki/) | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| [polymarket](./polymarket/) | Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. Read-only via public REST APIs, no API key needed. |
| [research-paper-writing](./research-paper-writing/) | End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and submission. Covers NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Integrates automated experiment monitoring, statistical analysis, iterative writing, and citation verification. |

## 📱 社交媒体 {#social-media}

| 技能 | 描述 |
|------|------|
| [xurl](./xurl/) | X/Twitter via xurl CLI: raw post search, posting, DM, media. |

## 💻 软件开发 {#software-development}

| 技能 | 描述 |
|------|------|
| [plan](./plan/) | Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work. |
| [requesting-code-review](./requesting-code-review/) | Pre-commit review: security scan, quality gates, auto-fix. |
| [subagent-driven-development](./subagent-driven-development/) | Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review (spec compliance then code quality). |
| [systematic-debugging](./systematic-debugging/) | 4-phase root cause debugging: understand bugs before fixing. |
| [test-driven-development](./test-driven-development/) | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [writing-plans](./writing-plans/) | Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. |

---
*内置 skills，最后更新: 2026-10-25 22:03*
