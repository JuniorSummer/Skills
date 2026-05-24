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
| [claude-code](./claude-code/) | Delegate coding tasks to Claude Code (Anthropic's CLI agent). Use for building features, refactoring, PR reviews, and it... |
| [codex](./codex/) | Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fix... |
| [hermes-agent](./hermes-agent/) | Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gatewa... |
| [opencode](./opencode/) | Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonom... |

## 🎨 创意内容生成 {#creative}

| 技能 | 描述 |
|------|------|
| [architecture-diagram](./architecture-diagram/) | Generate dark-themed SVG diagrams of software systems and cloud infrastructure as standalone HTML files with inline SVG ... |
| [ascii-art](./ascii-art/) | Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs (asciified, ascii.co.u... |
| [ascii-video](./ascii-video/) | Production pipeline for ASCII art video — any format. Converts video/audio/images/generative input into colored ASCII ch... |
| [design-md](./design-md/) | Author, validate, diff, and export DESIGN.md files — Google's open-source format spec that gives coding agents a persist... |
| [excalidraw](./excalidraw/) | Create hand-drawn style diagrams using Excalidraw JSON format. Generate .excalidraw files for architecture diagrams, flo... |
| [manim-video](./manim-video/) | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style e... |
| [p5js](./p5js/) | Production pipeline for interactive and generative visual art using p5.js. Creates browser-based sketches, generative ar... |
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
| [native-mcp](./native-mcp/) | Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers... |
| [webhook-subscriptions](./webhook-subscriptions/) | Create and manage webhook subscriptions for event-driven agent activation, or for direct push notifications (zero LLM co... |

## 🎮 游戏 {#gaming}

| 技能 | 描述 |
|------|------|
| [minecraft-modpack-server](./minecraft-modpack-server/) | Set up a modded Minecraft server from a CurseForge/Modrinth server pack zip. Covers NeoForge/Forge install, Java version... |
| [pokemon-player](./pokemon-player/) | Play Pokemon games autonomously via headless emulation. Starts a game server, reads structured game state from RAM, make... |

## 🐙 GitHub 工作流 {#github}

| 技能 | 描述 |
|------|------|
| [codebase-inspection](./codebase-inspection/) | Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. Use when a... |
| [github-auth](./github-auth/) | Set up GitHub authentication for the agent using git (universally available) or the gh CLI. Covers HTTPS tokens, SSH key... |
| [github-code-review](./github-code-review/) | Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. Wor... |
| [github-issues](./github-issues/) | Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Wor... |
| [github-pr-workflow](./github-pr-workflow/) | Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge... |
| [github-repo-management](./github-repo-management/) | Clone, create, fork, configure, and manage GitHub repositories. Manage remotes, secrets, releases, and workflows. Works ... |

## 🎬 媒体处理 {#media}

| 技能 | 描述 |
|------|------|
| [gif-search](./gif-search/) | Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. Useful for finding reaction GIFs, cr... |
| [heartmula](./heartmula/) | Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + ... |
| [spotify](./spotify/) | Control Spotify — play music, search the catalog, manage playlists and library, inspect devices and playback state. Load... |
| [youtube-content](./youtube-content/) | > |

## 🧠 MLOps & 模型训练 {#mlops}

| 技能 | 描述 |
|------|------|
| [audiocraft](./audiocraft/) | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need ... |
| [axolotl](./axolotl/) | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal... |
| [dspy](./dspy/) | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and ag... |
| [huggingface-hub](./huggingface-hub/) | Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, dep... |
| [llama-cpp](./llama-cpp/) | llama.cpp local GGUF inference + HF Hub model discovery. |
| [lm-evaluation-harness](./lm-evaluation-harness/) | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking mod... |
| [obliteratus](./obliteratus/) | Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques (diff-in-mean... |
| [outlines](./outlines/) | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local mode... |
| [segment-anything](./segment-anything/) | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using... |
| [trl-fine-tuning](./trl-fine-tuning/) | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRP... |
| [unsloth](./unsloth/) | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization |
| [vllm](./vllm/) | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM ... |
| [weights-and-biases](./weights-and-biases/) | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and ... |

## 📝 笔记管理 {#note-taking}

| 技能 | 描述 |
|------|------|
| [obsidian](./obsidian/) | Read, search, and create notes in the Obsidian vault. |

## 💼 生产力工具 {#productivity}

| 技能 | 描述 |
|------|------|
| [apple-notes](./apple-notes/) | Manage Apple Notes via the memo CLI on macOS (create, view, search, edit). |
| [apple-reminders](./apple-reminders/) | Manage Apple Reminders via remindctl CLI (list, add, complete, delete). |
| [claude-code-plugins](./claude-code-plugins/) | Install, manage, and troubleshoot Claude Code plugins from GitHub marketplaces. Covers marketplace setup, plugin install... |
| [findmy](./findmy/) | Track Apple devices and AirTags via FindMy.app on macOS using AppleScript and screen capture. |
| [google-workspace](./google-workspace/) | Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the... |
| [imessage](./imessage/) | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| [linear](./linear/) | Manage Linear issues, projects, and teams via the GraphQL API. Create, update, search, and organize issues. Uses API key... |
| [powerpoint](./powerpoint/) | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide d... |
| [remotion](./remotion/) | Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays |

## 🔴 红队测试 {#red-teaming}

| 技能 | 描述 |
|------|------|
| [godmode](./godmode/) | Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC sys... |

## 📚 学术研究 {#research}

| 技能 | 描述 |
|------|------|
| [arxiv](./arxiv/) | Search and retrieve academic papers from arXiv using their free REST API. No API key needed. Search by keyword, author, ... |
| [polymarket](./polymarket/) | Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. Read-only via publi... |
| [research-paper-writing](./research-paper-writing/) | End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and... |

## 💻 软件开发 {#software-development}

| 技能 | 描述 |
|------|------|
| [plan](./plan/) | Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, an... |
| [requesting-code-review](./requesting-code-review/) | > |
| [subagent-driven-development](./subagent-driven-development/) | Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage r... |
| [systematic-debugging](./systematic-debugging/) | Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation — NO fixes without... |
| [test-driven-development](./test-driven-development/) | Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle with ... |
| [writing-plans](./writing-plans/) | Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-siz... |

---
*内置 skills，最后更新: 2026-05-24 22:31*
