# Hermes Agent 内置 Skills

Hermes Agent 预装的技能集合，涵盖 AI Agent、开发工具、MLOps、创意内容等多个领域。共 78 个 skills。

## 目录

- [🤖 AI Agent 自治框架](#ai-agent)
- [🎨 创意内容生成](#creative)
- [📊 数据科学](#data-science)
- [⚙️ DevOps & 自动化](#devops)
- [📧 邮件管理](#email)
- [🛠️ 工程实践](#engineering)
- [🎮 游戏](#gaming)
- [🐙 GitHub 工作流](#github)
- [🎬 媒体处理](#media)
- [🧠 MLOps & 模型训练](#mlops)
- [📝 笔记管理](#note-taking)
- [💼 生产力工具](#productivity)
- [🔴 红队测试](#red-teaming)
- [📚 学术研究](#research)
- [🏠 智能家居](#smart-home)
- [📱 社交媒体](#social-media)
- [💻 软件开发](#software-development)

---

## 🤖 AI Agent 自治框架 {#ai-agent}

| 技能 | 描述 |
|------|------|
| [claude-code](./claude-code/) | 将编码任务委派给 Claude Code (Anthropic CLI Agent) |
| [codex](./codex/) | 将编码任务委派给 OpenAI Codex CLI Agent |
| [hermes-agent](./hermes-agent/) | Hermes Agent 完整使用指南 — CLI、配置、网关、技能、语音 |
| [opencode](./opencode/) | 将编码任务委派给 OpenCode CLI Agent |

## 🎨 创意内容生成 {#creative}

| 技能 | 描述 |
|------|------|
| [architecture-diagram](./architecture-diagram/) | 生成深色主题 SVG 软件架构图 |
| [ascii-art](./ascii-art/) | 使用 pyfiglet (571字体)、cowsay 等生成 ASCII 艺术 |
| [ascii-video](./ascii-video/) | ASCII 艺术视频生产管线 — 任意格式转换 |
| [baoyu-comic](./baoyu-comic/) | 知识漫画创作，支持多种画风和风格 |
| [baoyu-infographic](./baoyu-infographic/) | 专业信息图生成，21种布局×21种视觉风格 |
| [design-md](./design-md/) | Google DESIGN.md 规范 — 设计系统管理 |
| [excalidraw](./excalidraw/) | 手绘风格图表，支持架构图、流程图、概念图 |
| [creative-ideation](./creative-ideation/) | 通过创意约束生成项目灵感 |
| [manim-video](./manim-video/) | 3Blue1Brown 风格数学动画生产管线 |
| [p5js](./p5js/) | p5.js 交互式生成艺术与数据可视化 |
| [pixel-art](./pixel-art/) | 图像转复古像素画 (NES/Game Boy/PICO-8 等) |
| [popular-web-designs](./popular-web-designs/) | 54 套生产级网站设计系统模板 |
| [songwriting-and-ai-music](./songwriting-and-ai-music/) | 歌曲创作技巧与 AI 音乐生成 (Suno) |

## 📊 数据科学 {#data-science}

| 技能 | 描述 |
|------|------|
| [jupyter-live-kernel](./jupyter-live-kernel/) | 有状态 Jupyter 内核，用于迭代式 Python 执行 |

## ⚙️ DevOps & 自动化 {#devops}

| 技能 | 描述 |
|------|------|
| [dogfood](./dogfood/) | Web 应用系统化探索性 QA 测试 |
| [native-mcp](./native-mcp/) | MCP 协议客户端 — 连接外部 MCP 服务器并注册为原生工具 |
| [webhook-subscriptions](./webhook-subscriptions/) | Webhook 订阅管理，事件驱动 Agent 激活 |
| [time-restricted-cron](./time-restricted-cron/) | 时间限制的定时任务模式 |

## 📧 邮件管理 {#email}

| 技能 | 描述 |
|------|------|
| [himalaya](./himalaya/) | IMAP/SMTP 邮件管理 CLI — 收发、搜索、组织邮件 |

## 🛠️ 工程实践 {#engineering}

| 技能 | 描述 |
|------|------|
| [diagnose](./diagnose/) | 严格诊断循环 — 复现→最小化→假设→插桩→修复→回归测试 |
| [improve-codebase-architecture](./improve-codebase-architecture/) | 代码库架构改进建议 |
| [tdd](./tdd/) | 测试驱动开发 (红-绿-重构) |
| [to-issues](./to-issues/) | 将计划/PRD 拆解为独立 Issues |
| [to-prd](./to-prd/) | 从对话上下文生成 PRD |
| [triage](./triage/) | Issue 分诊状态机 |
| [zoom-out](./zoom-out/) | 拉远视角，获取更广泛的上下文 |

## 🎮 游戏 {#gaming}

| 技能 | 描述 |
|------|------|
| [minecraft-modpack-server](./minecraft-modpack-server/) | 从 CurseForge/Modrinth 搭建模组服务器 |
| [pokemon-player](./pokemon-player/) | 通过无头模拟器自主玩 Pokemon |

## 🐙 GitHub 工作流 {#github}

| 技能 | 描述 |
|------|------|
| [codebase-inspection](./codebase-inspection/) | 使用 pygount 检查代码库 (LOC/语言/注释比) |
| [github-auth](./github-auth/) | GitHub 认证设置 — HTTPS/SSH/gh CLI |
| [github-code-review](./github-code-review/) | 代码审查 — 分析 diff 并留行内评论 |
| [github-issues](./github-issues/) | GitHub Issue 创建、管理、分诊 |
| [github-pr-workflow](./github-pr-workflow/) | 完整 PR 生命周期 — 分支→提交→CI→合并 |
| [github-repo-management](./github-repo-management/) | GitHub 仓库克隆、创建、配置、管理 |
| [github-trending](./github-trending/) | GitHub Trending 项目抓取与分析 |

## 🎬 媒体处理 {#media}

| 技能 | 描述 |
|------|------|
| [gif-search](./gif-search/) | 通过 Tenor 搜索和下载 GIF |
| [heartmula](./heartmula/) | HeartMuLa 开源音乐生成 (类 Suno) |
| [songsee](./songsee/) | 音频频谱图与特征可视化 |
| [spotify](./spotify/) | Spotify 控制 — 播放、搜索、播放列表管理 |
| [youtube-content](./youtube-content/) | YouTube 视频字幕获取与结构化内容生成 |

## 🧠 MLOps & 模型训练 {#mlops}

| 技能 | 描述 |
|------|------|
| [audiocraft](./audiocraft/) | PyTorch 音频生成 — MusicGen/AudioGen |
| [axolotl](./axolotl/) | LLM 微调框架 — LoRA/QLoRA/DPO/GRPO |
| [dspy](./dspy/) | Stanford DSPy 声明式 LM 编程框架 |
| [huggingface-hub](./huggingface-hub/) | Hugging Face Hub CLI — 模型/数据集管理 |
| [llama-cpp](./llama-cpp/) | llama.cpp 本地 GGUF 推理 |
| [lm-evaluation-harness](./lm-evaluation-harness/) | 60+ 学术基准测试 (MMLU/HumanEval/GSM8K) |
| [obliteratus](./obliteratus/) | 移除开源 LLM 拒绝行为 (机械可解释性) |
| [outlines](./outlines/) | 结构化生成 — 保证 JSON/XML/代码有效性 |
| [segment-anything](./segment-anything/) | SAM 图像分割基础模型 (零样本) |
| [trl-fine-tuning](./trl-fine-tuning/) | TRL 强化学习微调 — SFT/DPO/PPO/GRPO |
| [unsloth](./unsloth/) | 快速微调 — 2-5x 加速，50-80% 内存节省 |
| [vllm](./vllm/) | vLLM 高吞吐 LLM 推理服务 |
| [weights-and-biases](./weights-and-biases/) | W&B 实验跟踪与超参优化 |

## 📝 笔记管理 {#note-taking}

| 技能 | 描述 |
|------|------|
| [obsidian](./obsidian/) | Obsidian 笔记读取、搜索和创建 |

## 💼 生产力工具 {#productivity}

| 技能 | 描述 |
|------|------|
| [apple-notes](./apple-notes/) | macOS Apple Notes 管理 (memo CLI) |
| [apple-reminders](./apple-reminders/) | macOS Apple Reminders 管理 (remindctl CLI) |
| [findmy](./findmy/) | Apple 设备/AirTag 追踪 |
| [google-workspace](./google-workspace/) | Gmail/Calendar/Drive/Sheets/Docs 集成 |
| [imessage](./imessage/) | iMessage/SMS 发送接收 |
| [linear](./linear/) | Linear Issue/项目/团队管理 (GraphQL) |
| [maps](./maps/) | 位置智能 — 地理编码/导航/POI 搜索 (OSM) |
| [nano-pdf](./nano-pdf/) | 自然语言编辑 PDF |
| [notion](./notion/) | Notion API — 页面/数据库/Block 管理 |
| [ocr-and-documents](./ocr-and-documents/) | PDF/扫描件文字提取 (OCR) |
| [powerpoint](./powerpoint/) | PowerPoint 演示文稿创建与编辑 |

## 🔴 红队测试 {#red-teaming}

| 技能 | 描述 |
|------|------|
| [godmode](./godmode/) | G0DM0D3 越狱技术 — 33种输入混淆+系统提示模板 |

## 📚 学术研究 {#research}

| 技能 | 描述 |
|------|------|
| [arxiv](./arxiv/) | arXiv 论文搜索与获取 (免费 REST API) |
| [blogwatcher](./blogwatcher/) | 博客/RSS/Atom 订阅监控 |
| [llm-wiki](./llm-wiki/) | Karpathy's LLM Wiki — 持久化互链知识库 |
| [polymarket](./polymarket/) | Polymarket 预测市场数据查询 |
| [research-paper-writing](./research-paper-writing/) | ML/AI 论文写作全流程 (NeurIPS/ICML/ICLR) |
| [video-to-wiki-pipeline](./video-to-wiki-pipeline/) | 批量视频分析→互链 Wiki 生成 |

## 🏠 智能家居 {#smart-home}

| 技能 | 描述 |
|------|------|
| [openhue](./openhue/) | Philips Hue 灯光控制 (OpenHue CLI) |

## 📱 社交媒体 {#social-media}

| 技能 | 描述 |
|------|------|
| [xurl](./xurl/) | X/Twitter 交互 — 发帖/搜索/DM/时间线 (xurl CLI) |

## 💻 软件开发 {#software-development}

| 技能 | 描述 |
|------|------|
| [plan](./plan/) | 规划模式 — 检查上下文并写入计划文件 |
| [requesting-code-review](./requesting-code-review/) | 提交前验证管线 — 安全扫描+质量门禁 |
| [subagent-driven-development](./subagent-driven-development/) | 子 Agent 驱动开发 — 独立任务分发+两阶段审查 |
| [systematic-debugging](./systematic-debugging/) | 系统化调试 — 4阶段根因调查 |
| [test-driven-development](./test-driven-development/) | TDD 测试驱动开发 (红-绿-重构) |
| [writing-plans](./writing-plans/) | 从需求生成完整实施计划 |

---

*共 78 个内置 skills，随 Hermes Agent 版本更新。*
