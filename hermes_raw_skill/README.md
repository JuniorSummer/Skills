# Hermes Agent 内置 Skills

Hermes Agent 预装的技能集合。

## 目录

- [🤖 AI Agent 自治框架](#autonomous-ai-agents)
- [🎨 创意内容生成](#creative)
- [📊 数据科学](#data-science)
- [⚙️ DevOps & 自动化](#devops)
- [🎮 游戏](#gaming)
- [🐙 GitHub 工作流](#github)
- [🎬 媒体处理](#media)
- [🧠 MLOps & 模型训练](#mlops)
- [📝 笔记管理](#note-taking)
- [💼 生产力工具](#productivity)
- [🔴 红队测试](#red-teaming)
- [📚 学术研究](#research)
- [💻 软件开发](#software-development)

---

## 🤖 AI Agent 自治框架 {#autonomous-ai-agents}

| 技能 | 描述 |
|------|------|
| [claude-code](./claude-code/) | Delegate coding tasks to Claude Code (Anthropic's CLI agent). Use for building features, refactoring, PR reviews, and iterative coding. Requires the claude CLI installed. |
| [codex](./codex/) | Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fixing. Requires the codex CLI and a git repository. |
| [hermes-agent](./hermes-agent/) | Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. Load this skill when helping users configure Hermes, troubleshoot issues, spawn agent instances, or make code contributions. |
| [opencode](./opencode/) | Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonomous sessions. Requires the opencode CLI installed and authenticated. |

## 🎨 创意内容生成 {#creative}

| 技能 | 描述 |
|------|------|
| [architecture-diagram](./architecture-diagram/) | Generate dark-themed SVG diagrams of software systems and cloud infrastructure as standalone HTML files with inline SVG graphics. Semantic component colors (cyan=frontend, emerald=backend, violet=database, amber=cloud/AWS, rose=security, orange=message bus), JetBrains Mono font, grid background. Best suited for software architecture, cloud/VPC topology, microservice maps, service-mesh diagrams, database + API layer diagrams, security groups, message buses — anything that fits a tech-infra deck with a dark aesthetic. If a more specialized diagramming skill exists for the subject (scientific, educational, hand-drawn, animated, etc.), prefer that — otherwise this skill can also serve as a general-purpose SVG diagram fallback. Based on Cocoon AI's architecture-diagram-generator (MIT). |
| [ascii-art](./ascii-art/) | Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs (asciified, ascii.co.uk), and LLM fallback. No API keys required. |
| [ascii-video](./ascii-video/) | Production pipeline for ASCII art video — any format. Converts video/audio/images/generative input into colored ASCII character video output (MP4, GIF, image sequence). Covers: video-to-ASCII conversion, audio-reactive music visualizers, generative ASCII art animations, hybrid video+audio reactive, text/lyrics overlays, real-time terminal rendering. Use when users request: ASCII video, text art video, terminal-style video, character art animation, retro text visualization, audio visualizer in ASCII, converting video to ASCII art, matrix-style effects, or any animated ASCII output. |
| [design-md](./design-md/) | Author, validate, diff, and export DESIGN.md files — Google's open-source format spec that gives coding agents a persistent, structured understanding of a design system (tokens + rationale in one file). Use when building a design system, porting style rules between projects, generating UI with consistent brand, or auditing accessibility/contrast. |
| [excalidraw](./excalidraw/) | Create hand-drawn style diagrams using Excalidraw JSON format. Generate .excalidraw files for architecture diagrams, flowcharts, sequence diagrams, concept maps, and more. Files can be opened at excalidraw.com or uploaded for shareable links. |
| [manim-video](./manim-video/) | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style explainer videos, algorithm visualizations, equation derivations, architecture diagrams, and data stories. Use when users request: animated explanations, math animations, concept visualizations, algorithm walkthroughs, technical explainers, 3Blue1Brown style videos, or any programmatic animation with geometric/mathematical content. |
| [p5js](./p5js/) | Production pipeline for interactive and generative visual art using p5.js. Creates browser-based sketches, generative art, data visualizations, interactive experiences, 3D scenes, audio-reactive visuals, and motion graphics — exported as HTML, PNG, GIF, MP4, or SVG. Covers: 2D/3D rendering, noise and particle systems, flow fields, shaders (GLSL), pixel manipulation, kinetic typography, WebGL scenes, audio analysis, mouse/keyboard interaction, and headless high-res export. Use when users request: p5.js sketches, creative coding, generative art, interactive visualizations, canvas animations, browser-based visual art, data viz, shader effects, or any p5.js project. |
| [popular-web-designs](./popular-web-designs/) | > |
| [songwriting-and-ai-music](./songwriting-and-ai-music/) | > |

## 📊 数据科学 {#data-science}

| 技能 | 描述 |
|------|------|
| [jupyter-live-kernel](./jupyter-live-kernel/) | > |

## ⚙️ DevOps & 自动化 {#devops}

| 技能 | 描述 |
|------|------|
| [dogfood](./dogfood/) | Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports |
| [native-mcp](./native-mcp/) | Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers them as native Hermes Agent tools. Supports stdio and HTTP transports with automatic reconnection, security filtering, and zero-config tool injection. |
| [webhook-subscriptions](./webhook-subscriptions/) | Create and manage webhook subscriptions for event-driven agent activation, or for direct push notifications (zero LLM cost). Use when the user wants external services to trigger agent runs OR push notifications to chats. |

## 🎮 游戏 {#gaming}

| 技能 | 描述 |
|------|------|
| [minecraft-modpack-server](./minecraft-modpack-server/) | Set up a modded Minecraft server from a CurseForge/Modrinth server pack zip. Covers NeoForge/Forge install, Java version, JVM tuning, firewall, LAN config, backups, and launch scripts. |
| [pokemon-player](./pokemon-player/) | Play Pokemon games autonomously via headless emulation. Starts a game server, reads structured game state from RAM, makes strategic decisions, and sends button inputs — all from the terminal. |

## 🐙 GitHub 工作流 {#github}

| 技能 | 描述 |
|------|------|
| [codebase-inspection](./codebase-inspection/) | Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. Use when asked to check lines of code, repo size, language composition, or codebase stats. |
| [github-auth](./github-auth/) | Set up GitHub authentication for the agent using git (universally available) or the gh CLI. Covers HTTPS tokens, SSH keys, credential helpers, and gh auth — with a detection flow to pick the right method automatically. |
| [github-code-review](./github-code-review/) | Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-issues](./github-issues/) | Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-pr-workflow](./github-pr-workflow/) | Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge. Works with gh CLI or falls back to git + GitHub REST API via curl. |
| [github-repo-management](./github-repo-management/) | Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works with gh CLI or falls back to git + GitHub REST API via curl. |

## 🎬 媒体处理 {#media}

| 技能 | 描述 |
|------|------|
| [gif-search](./gif-search/) | Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. Useful for finding reaction GIFs, creating visual content, and sending GIFs in chat. |
| [heartmula](./heartmula/) | Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + tags with multilingual support. |
| [spotify](./spotify/) | Control Spotify — play music, search the catalog, manage playlists and library, inspect devices and playback state. Loads when the user asks to play/pause/queue music, search tracks/albums/artists, manage playlists, or check what's playing. Assumes the Hermes Spotify toolset is enabled and `hermes auth spotify` has been run. |
| [youtube-content](./youtube-content/) | > |

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
| [obsidian](./obsidian/) | Read, search, and create notes in the Obsidian vault. |

## 💼 生产力工具 {#productivity}

| 技能 | 描述 |
|------|------|
| [apple-notes](./apple-notes/) | Manage Apple Notes via the memo CLI on macOS (create, view, search, edit). |
| [apple-reminders](./apple-reminders/) | Manage Apple Reminders via remindctl CLI (list, add, complete, delete). |
| [claude-code-plugins](./claude-code-plugins/) | Install, manage, and troubleshoot Claude Code plugins from GitHub marketplaces. Covers marketplace setup, plugin installation, common errors, and workarounds. |
| [cms-find-skills](./cms-find-skills/) | 用于"安装 Skill / 下载 Skill / 找一个能做 X 的 Skill / 把某个 Skill 装到本地 / 列出平台 Skill"。从 CMS 平台搜索已有 Skill 并按 downloadUrl 下载 ZIP 解压到本地 ~/.claude/skills。仅负责查找与安装，不负责创建或发布 |
| [feynman-coach](./feynman-coach/) | | |
| [findmy](./findmy/) | Track Apple devices and AirTags via FindMy.app on macOS using AppleScript and screen capture. |
| [google-workspace](./google-workspace/) | Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the Google Workspace CLI (`gws`) when available for broader API coverage, and falls back to the Python client libraries otherwise. |
| [imessage](./imessage/) | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| [kaze-12-prompts](./kaze-12-prompts/) | 12 个通用 AI 提示词模板库,覆盖 5 大场景(问清问题/学习/解决问题/决策/认识自己)。当用户需要理清困惑、学习新概念、拆解优秀案例、研究陌生领域、核查事实、解决复杂问题、做决策、挖掘天赋、规划人生时,自动推荐并生成对应 prompt 模板。触发信号:苏格拉底提问、双层解释、反向拆解、横纵分析、事实核查、专家会诊、第一性原理、跨领域借解、钢人论证、最小实验、天赋挖掘、人生设计,以及"帮我理清/讲讲/解释下/怎么选/纠结/选哪个/学一下/分析这个/靠谱吗/真的假的/我适合什么"等相近表达。命中意图时先推荐模板,用户确认后替换【】占位符输出完整可复制 prompt。 |
| [knowledge-base](./knowledge-base/) | (无描述) |
| [linear](./linear/) | Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key auth (no OAuth needed). All operations via curl — no dependencies. |
| [notes](./notes/) | (无描述) |
| [powerpoint](./powerpoint/) | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill. |
| [remotion](./remotion/) | Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays |
| [skills](./skills/) | (无描述) |

## 🔴 红队测试 {#red-teaming}

| 技能 | 描述 |
|------|------|
| [godmode](./godmode/) | Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC system prompt templates, ULTRAPLINIAN multi-model racing, encoding escalation, and Hermes-native prefill/system prompt integration. Use when a user wants to bypass safety filters, jailbreak a model, or red-team model robustness. |

## 📚 学术研究 {#research}

| 技能 | 描述 |
|------|------|
| [arxiv](./arxiv/) | Search and retrieve academic papers from arXiv using their free REST API. No API key needed. Search by keyword, author, category, or ID. Combine with web_extract or the ocr-and-documents skill to read full paper content. |
| [polymarket](./polymarket/) | Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. Read-only via public REST APIs, no API key needed. |
| [research-paper-writing](./research-paper-writing/) | End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and submission. Covers NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Integrates automated experiment monitoring, statistical analysis, iterative writing, and citation verification. |

## 💻 软件开发 {#software-development}

| 技能 | 描述 |
|------|------|
| [plan](./plan/) | Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work. |
| [requesting-code-review](./requesting-code-review/) | > |
| [subagent-driven-development](./subagent-driven-development/) | Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review (spec compliance then code quality). |
| [systematic-debugging](./systematic-debugging/) | Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation — NO fixes without understanding the problem first. |
| [test-driven-development](./test-driven-development/) | Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle with test-first approach. |
| [writing-plans](./writing-plans/) | Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. |

---
*内置 skills，最后更新: 2026-08-30 22:00*
