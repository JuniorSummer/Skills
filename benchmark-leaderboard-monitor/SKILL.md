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

### 3. AIHOT 大模型排行榜（AIHOT 共识分）
- URL: `https://aihot.news/leaderboard`（旧域名 aihot.virxact.com 2026-10-31 起只做跳转）
- 框架：**2026-09 起已由 Next.js RSC 改为 React Router turbo-stream**（旧 `__next_f.push` 解析法从 2026-08-18 起 100% 失败）
- **2026-10 页面又改了一层**：综合榜条目只剩 `{slug, rank, score, sourceCount, coverage}`，**模型名/厂商拆到了独立的模型元数据节点**（`{slug, name, provider, ...}`）→ 必须按 `slug` 关联；同时页面结构变成 `{board:{key:"overall"}, entries:[…30], filterEntries:[…]}`（总榜 + 长尾，要合并两个数组）。只认 `board.key == "overall"`（旧写法“把所有含 rank 的节点当总榜”现在会把 5 个分榜混在一起）
- 解析方法：见下方「React Router turbo-stream」章节；完整实现见 `~/.hermes/scripts/benchmark_monitor.py:parse_aihot()`
- 更新时间：结构里的 `run.generatedAt`（UTC ISO）→ +8 小时转北京时间
- ⚠️ 排行榜**没有 API**（`/api/v1` 只覆盖 items / hot-topics / dailies 等，不含 leaderboard），只能解析 SSR 页面
- 变化检测：新上榜 / 分数变化(≥0.1) / 排名变化(rank 不同) / 下榜

## 三榜单独立处理机制（2026-08-17 起）

- 三个榜单（Terminal-Bench / DeepSWE / AIHOT）各自独立对比、独立输出
- 有变化的榜单：输出变化详情 + Top 15 列表
- 无变化的榜单：只输出「无变化」，**不带 Top 15**
- 脚本输出四个标记行：`__TB_HAS_CHANGES__` / `__DSWE_HAS_CHANGES__` / `__AIHOT_HAS_CHANGES__` / `__HAS_CHANGES__`（全局）
- cron prompt 指示 LLM 直接透传三个【】区块，忽略日志和标记行

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

### React Router turbo-stream（aihot.news/leaderboard 2026-09 起）

页面数据在 `<script>window.__reactRouterContext.streamController.enqueue("[...]")</script>` 里，
解出来是**扁平引用表**（不是嵌套 JSON）：

- 表里每个元素是标量（字符串/数字）或容器（dict/list）
- 容器里的**整数是索引**，指向表中另一元素；索引指向的标量就是字面量（**不要再解一次**）
- 键名形如 `"_47"` 表示「键名 = table[47]」，值同理
- 结构里**有循环引用**，递归必须设深度上限，否则爆栈/超时

```python
import re, json

m = re.search(r'streamController\.enqueue\("(.*?)"\)\s*;?\s*</script>', html, re.DOTALL)
table = json.loads(json.loads('"' + m.group(1) + '"'))   # 双层 json.loads 反转义

def key_name(k):                       # "_47" -> table[47]
    if isinstance(k, str) and k.startswith("_") and k[1:].isdigit():
        i = int(k[1:])
        if 0 <= i < len(table) and isinstance(table[i], str):
            return table[i]
    return k

def resolve(ref, depth=0):             # 有界递归解引用
    if depth > 8 or ref is None or isinstance(ref, (str, float, bool)):
        return ref
    if isinstance(ref, int):
        if ref < 0 or ref >= len(table):
            return None
        node = table[ref]
        return resolve(node, depth + 1) if isinstance(node, (dict, list)) else node
    if isinstance(ref, dict):
        return {key_name(k): resolve(v, depth + 1) for k, v in ref.items()}
    if isinstance(ref, list):
        return [resolve(x, depth + 1) for x in ref]
    return None
```

**取数不要依赖固定下标**（索引会随数据量变化）：遍历整张表，对每个 dict 解引用后筛出
`有 rank 且 model.name` 的字典即为榜单条目，再按 rank 排序。
更新时间取 `generatedAt`（UTC ISO）→ +8 小时转北京时间。2026-09 实测：30 条、rank 1-30 连续。

## 添加新数据源的步骤

1. 用 `curl -sL -A "Mozilla/5.0" <url>` 抓取 HTML 到本地文件
2. 检查 SSR 框架类型：
   - `__next_f` / `__NEXT_DATA__` → Next.js
   - `$_TSR` / `$R[` → TanStack Router
   - `streamController.enqueue` → React Router turbo-stream（扁平引用表，见上方章节）
   - 其他 → 检查 `<script>` 中的 JS 变量或 API 调用
3. 用正则提取嵌入的 JSON 数据，注意编码处理
4. 在 `benchmark_monitor.py` 中新增 `parse_xxx()` 函数 + 对比函数
5. 在 `main()` 中加入抓取+对比逻辑
6. 在 `format_output()` 中加入输出格式

## 数据源异常必须显式上报（2026-09 教训）

曾经 cron prompt 里写着“忽略脚本输出中的抓取日志（…/❌ 解析失败）”，结果 AIHOT 源挂了 6 周、44 次跑挂 41 次都没人发现——因为输出一直显示“无变化”、job 状态一直 ok。

脚本侧（已实现）：`check_source()` 做健康校验，异常时输出标记 + 在正文最前面加警示行：
- 绝对值：条目数 < `MIN_ENTRIES`（TB 15 / DSWE 30 / AIHOT 15）→ `条目数异常`
- 相对值：比上次快照少一半以上 → `条目数骤降`
- 输出 `__SOURCE_ERRORS__:AIHOT(解析失败)`，正文首行 `⚠️ 数据源异常：AIHOT(解析失败)`

prompt 侧（已改）：绝不能再说“忽略 ❌ 解析失败”；要写明“⚠️ 数据源异常警示行必须作为回复第一行原样输出，即使三个区块都显示『无变化』也要输出，且不要自己编造数据补上”。

排查口径：`grep -c "解析失败" ~/.hermes/cron/output/c658e4a56cce/*` 失败率不为 0 就要重抓 HTML 检查结构。

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
- **解析失败会静默变成「无变化」（最大的坑）**：`parse_xxx()` 返回 None 时脚本塞空数据，该榜单照样输出「无变化」、job 状态还是 ok，不看日志根本发现不了。定期核对：`grep -c 解析失败 ~/.hermes/cron/output/<job_id>/*`，失败率不为 0 就重抓 HTML 检查结构。
- **turbo-stream 递归必须有深度上限**：引用表里有循环引用，无界递归会直接卡死（实测 180s 超时）。
- **页面改版后快照会“全部新增”**：解析恢复的那一次会把整张榜当成新上榜；跑一次让快照落盘，后续就正常对比了。
- **Next.js 中文乱码**：见上方编码陷阱说明
- **页面改版导致解析失败**：重新抓 HTML，检查 `__next_f.push` 或 `$R` 格式是否变化
- **首次运行**：必须用 `--init` 参数，只存快照不对比
