---
name: benchmark-leaderboard-monitor
description: |
  监控 AI Benchmark 排行榜网站的变化并定时推送。
  当用户想追踪某个评测榜单（如 Terminal-Bench、SWE-bench、DeepSWE 等）的模型跑分变化，
  或需要定期抓取 SSR 渲染的排行榜/数据表格并检测变化时使用。
  核心技术：curl 抓取 + SSR 框架数据解析（Next.js / TanStack Router）+ 快照对比 + cron 推送。
source: self-generated
---

# Benchmark Leaderboard Monitor

监控 AI 评测排行榜变化，每日对比快照并推送差异到飞书。

## 核心文件

- 监控脚本：`~/.hermes/scripts/benchmark_monitor.py`
- 快照文件：`~/.config/benchmark-monitor/snapshot.json`
- Cron Job ID: `c658e4a56cce`（每天 9:00 → 飞书）

## 已监控的数据源

### 1. Terminal-Bench 2.1（终端 Agent 能力评测）
- URL: `https://www.datalearner.com/benchmarks/terminal-bench-2-1`
- 框架：Next.js SSR
- 解析方法见下方

### 2. DeepSWE（代码修复 Agent 评测）
- URL: `https://deepswe.datacurve.ai/`
- 框架：TanStack Router SSR
- 解析方法见下方

## SSR 数据解析技术（关键）

### Next.js（datalearner.com 等）

Next.js SSR 页面把数据嵌入 `self.__next_f.push([1,"..."])` 调用中。

```python
import re, json

pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.DOTALL)
for p in pushes:
    # 第一步：反转义 unicode
    try:
        decoded = p.encode().decode('unicode_escape')
    except:
        decoded = p
    # 第二步：Latin-1 → UTF-8（中文乱码修复，关键！）
    try:
        decoded = decoded.encode('latin-1').decode('utf-8')
    except:
        pass
    # 第三步：正则提取目标 JSON
    m = re.search(r'"results":\s*(\[.*?\])\s*,\s*"(?:benchmarkCode|total)', decoded, re.DOTALL)
    if m:
        data = json.loads(m.group(1))
```

**⚠️ 编码陷阱**：必须先 `unicode_escape` 再 `latin-1→utf-8`，否则中文全是乱码。这是因为 Next.js 把 UTF-8 字节按 Latin-1 编码后嵌入 JS 字符串。

### TanStack Router（deepswe.datacurve.ai 等）

TanStack Router SSR 把数据嵌入 `<script>` 标签中的 `$R` 数组。数据条目形如：
```
$R[247]={model:"claude-opus-5",harness:"mini-swe-agent",reasoning_effort:"max",pass_rate:0.736,...}
```

```python
import re

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for script in scripts:
    if len(script) < 1000:
        continue
    entries = re.findall(
        r'model:"([^"]+)".*?reasoning_effort:"([^"]*)".*?'
        r'pass_rate:([\d.]+).*?pass_at_1:([\d.]+).*?pass_at_4:([\d.]+)',
        script
    )
```

## 添加新数据源的步骤

1. 用 `curl -sL -A "Mozilla/5.0" <url>` 抓取 HTML 到本地文件
2. 检查 SSR 框架类型：
   - `__next_f` / `__NEXT_DATA__` → Next.js
   - `$_TSR` / `$R[` → TanStack Router
   - 其他 → 检查 `<script>` 中的 JS 变量或 API 调用
3. 用正则提取嵌入的 JSON 数据，注意编码处理
4. 在 `benchmark_monitor.py` 中新增 `parse_xxx()` 函数 + 对比函数
5. 在 `main()` 中加入抓取+对比逻辑
6. 在 `format_output()` 中加入输出格式

## 快照对比机制

```python
# 每次运行保存完整快照到 ~/.config/benchmark-monitor/snapshot.json
# 下次运行时与旧快照对比，输出：
#   🆕 新上榜模型
#   📊 分数变化（↑/↓ + 差值）
#   ❌ 已下榜模型
# 无变化时仅输出 Top 15 概览
```

## Cron 配置要点

- `script` 字段填 `benchmark_monitor.py`（只填脚本文件名！系统会自动在 ~/.hermes/scripts/ 下解析并用 python3 运行。若填完整命令如 `python3 ~/.hermes/scripts/benchmark_monitor.py 2>&1`，python3 会被错误拼接进路径导致 Script not found）
- `prompt` 指示"直接输出脚本结果不做分析"
- `deliver` 设为飞书
- `schedule` 为 `0 9 * * *`（每天早上 9 点）
- 推送范围：有变化时推送变化详情 + Top 15 排行；无变化时只推送「无变化」两个字（用户指定，不展示 Top 15 概览）
- 脚本末尾输出 `__HAS_CHANGES__:true/false` 标记供 prompt 判断

## 常见问题

- **curl 超时**：加 `--max-time 25` 和 `-A` UA 头
- **Next.js 中文乱码**：见上方编码陷阱说明
- **页面改版导致解析失败**：重新抓 HTML，检查 `__next_f.push` 或 `$R` 格式是否变化
- **首次运行**：必须用 `--init` 参数，只存快照不对比
