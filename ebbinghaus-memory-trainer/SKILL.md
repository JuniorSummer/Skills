---
name: ebbinghaus-memory-trainer
description: 艾宾浩斯记忆曲线训练系统 — 创建定时任务每天推送记忆训练内容，支持新学和复习的双向测试。覆盖设置跟踪文件、配置每日推送cron、处理图像型docx内容提取。
source: self-generated
---

# 艾宾浩斯记忆曲线训练系统

基于艾宾浩斯遗忘曲线的每日记忆训练系统，每天早上/晚上推送训练内容到飞书。

## 触发条件

- 用户想建立记忆训练系统
- 用户提到"艾宾浩斯"、"记忆曲线"、"记忆训练"、"编码记忆"
- 用户分享了记忆材料（docx/txt/json）并想转为定时训练

## 整体架构

```
记忆材料（docx/txt） → OCR/解析 → tracker.json → 每日cron → 飞书推送
                                                    ↓
                                              用户交互测试
```

## 步骤

### 1. 创建跟踪文件

位置：`~/.hermes/data/ebbinghaus_memory_tracker.json`

```json
{
  "version": "1.0",
  "created": "YYYY-MM-DD",
  "total_items": 0,
  "learned_count": 0,
  "mastered_count": 0,
  "items": [],
  "settings": {
    "daily_new": 5,
    "review_intervals": [1, 2, 4, 7, 15, 30],
    "mastery_threshold": 6
  }
}
```

每个 item 结构：
```json
{
  "key": "编码键值",
  "item": "对应物品",
  "method": "记忆方法说明",
  "method_type": "外形看一看|读音谐一谐|字面想一想|节日找一找",
  "learn_date": null,
  "review_history": [],
  "correct_streak": 0,
  "mastered": false,
  "memory_hint": null
}
```

**`memory_hint` 字段（可选）：** 为弱谐音编码额外添加的画面加固策略。格式为简短的视觉联想描述，如"数字2是鳄鱼张开的嘴，1是被咬住的棍子"。策略：弱谐音 + 画面联想 = 双重记忆通道。cron 推送时自动在对应项下方展示 `💡 记忆提示：...`。

### 2. 填充记忆库

**A. 从 docx 文档提取（图像型）：**

如果记忆材料是图像型 docx（每页截图/思维导图，XML 无文本），使用 OCR 提取：

```bash
# 提取图片
python3 -c "
import zipfile, os
os.makedirs('/tmp/memory_doc', exist_ok=True)
with zipfile.ZipFile('docx_path') as z:
    for n in z.namelist():
        if n.startswith('word/media/'):
            z.extract(n, '/tmp/memory_doc/')
"

# Tesseract OCR（中文）
for img in /tmp/memory_doc/*.png; do
    python3 -c "
from PIL import Image
import pytesseract
img = Image.open('$img').convert('L')
img = img.resize((img.width*3, img.height*3), Image.LANCZOS)
img = img.point(lambda x: 0 if x < 140 else 255)
print(pytesseract.image_to_string(img, lang='chi_sim+eng', config='--psm 6'))
"
done
```

Pitfall: docx 图像 OCR 时需放大 3x + 二值化阈值处理，否则中文识别率极低。

**B. 从结构化文本解析：**

使用正则 `r'(\d+)\s*[→\s]+\s*(.+?)\s*[→\s]+\s*(.+)'` 解析"键值 → 物品 → 方法"格式的行。

### 3. 创建每日推送 Cron

**多记忆库模式（2026-08-20 起）：一个脚本，多个 tracker**

同一套艾宾浩斯机制支持多个独立记忆库（如数字编码、马斯克第一性原理等），每个库独立 tracker + 独立 cron，互不干扰。

- 通用脚本 `~/.hermes/scripts/memory_training_daily.py` 支持 `--tracker <path>` 参数（默认数字编码库）
- 每个额外记忆库建一个薄 wrapper 脚本（如 `memory_training_musk_daily.py`），调用通用脚本并传 `--tracker`
- wrapper 脚本模式：
  ```python
  import subprocess, sys
  TRACKER = "/root/.hermes/data/ebbinghaus_memory_tracker_musk.json"
  MAIN = "/root/.hermes/scripts/memory_training_daily.py"
  result = subprocess.run([sys.executable, MAIN, "--tracker", TRACKER], capture_output=True, text=True)
  sys.stdout.write(result.stdout)
  if result.stderr: sys.stderr.write(result.stderr)
  sys.exit(result.returncode)
  ```
- 新 tracker 文件结构同标准 tracker，可加 `"name"` 字段标识主题
- 每个库各自创建 cron（schedule 可相同如 `0 12 * * *`，各自推送）
- 用户偏好：不同主题内容（如马斯克学习、数字编码）分开推送，不要混在一个 tracker

**推荐方案（2026-07-31 起使用）：Python 脚本确定性计算**

脚本位置：`~/.hermes/scripts/memory_training_daily.py`

Cron 配置：
```python
cronjob(
    action="create",
    name="每日记忆训练",
    schedule="0 20 * * *",
    deliver="feishu:oc_xxxxx",
    script="memory_training_daily.py",           # 脚本确定性计算
    enabled_toolsets=["terminal"],
    prompt="直接输出下面的数据，不要做任何分析、总结或解释。如果数据格式有问题才报告错误。"
)
```

脚本功能（确定性，无 LLM 参与）：
1. 读取 tracker.json（自动清除控制字符）
2. 构建 learn_date → 学习日序号映射（非自然日）
3. 按 review_intervals 计算每个已学项的到期 interval
4. 检查 review_history 中已完成 interval，未完成的加入待复习
5. 获取下 5 个未学项作为新学展示
6. 输出格式化训练内容（列表格式，适配飞书渲染，不含 markdown 表格）

**历史方案（已废弃，保留供参考）：**

LLM prompt 脑算方式（容易出错，特别是 60+ 项 × 6 interval = 360 组合）：
- 已于 2026-07-31 替换为脚本方案
- 根因：LLM 脑算在数据量大时容易从 20 项暴增到 95 项（自然日 vs 学习日混淆）

**关键变更历史：**
- 2026-07-24: Cron 不再自动写 tracker（不标记 learn_date，不加 review_history）
- 2026-07-31: 复习计算从 LLM 脑算改为 Python 脚本确定性计算
- 2026-08-19: 实际部署推送时间从 20:00 改为 12:00（cron 配置示例中的 `0 20 * * *` 相应调整）

### 4. 交互式测试模式

当用户说"开始记忆测试"/"开始复习"时：

1. **获取本次测试题源**：用户回复 cron 推送时，消息里往往只有截断的部分内容。从 cron 会话文件提取完整推送：
   ```bash
   ls -t ~/.hermes/sessions/ | grep <cron_job_id> | head -1   # 取最新会话
   ```
   读取该 JSON，找到 role=assistant 且 content 含"记忆训练"的消息，解析出**新学项 + 待复习项**完整列表。
2. 读取 tracker，获取当前活跃的学习项（learned 但未 mastered）
3. 双向测试，**打乱顺序**提高难度：
   - **正向**：给键值 → 用户回忆物品
   - **反向**：给物品 → 用户回忆键值（约各一半）
   - **易混镜像对相邻出题**：如 34狮子↔43雪山 这类镜像数字，测试时应放一起对比（用户明确偏好）。谐音相近对也要注意：53武术衫↔54武士（用户实际答错过，53谐音"武衫"、54谐音"武士"）。2026-08-30 实测新发现的易混对：59兀鹫↔49狮子狗（答反成49，个位十位混淆）、32扇儿↔53武术衫（32答成"衫儿"，"扇/衫"谐音且受53的"衫"字干扰）——这两个配对测试时应相邻对比
   - 新学项+复习项**合并一次性出完**，不分两轮（用户明确偏好）
4. 对错误/遗忘标记，记录到 review_history（correct=false）
4. **不确定标记**：用户用【】包裹答案表示不确定（如【零食】），虽正确但需标记 `"uncertain": true` 到对应 review_history 记录，下次 cron 推送时用 ⚠️ 标注优先复习
   - **⚠️ 标注须绑定"最近一次复习"而非当前 interval**：若 uncertain 只挂在单个 interval 记录上，该 interval 复习完成后（如 53 从 interval 1 推进到 interval 2），标记即丢失。正确做法：脚本读取该 item 最近一条 review_history 的 uncertain 字段决定是否显示 ⚠️，持续到用户下次明确答对（correct=true 且不带【】）为止。
6. 更新 correct_streak，6次连续正确标记 mastered
7. 汇报本次测试结果，重点提示不确定和错误的项

### 5. 进度查询

用户说"记忆进度"时，读取 tracker 输出：
- 已学 X/总数 Y
- 已掌握 Z 项
- 连续学习天数
- 下次需复习的项数

## 四种记忆方法

文档中的记忆方法分类：外形看一看、读音谐一谐、字面想一想、节日找一找。

## 复习计算逻辑（重要）— 按"学习日"而非自然日

**核心原则：所有复习间隔以"学习日序号"计算，不是日历日。** 跳过没有学习的日历日不算。

### 学习日定义

从 tracker 中提取所有 item 的 learn_date（去重排序），每个日期是一个"学习日"：
- 学习日1 = 最早 learn_date
- 学习日2 = 第二个 learn_date
- ...

例：learn_dates = [7/12, 7/13, 7/14, 7/15, 7/17, 7/20, 7/21, 7/24]
- 7/12=学习日1, 7/13=学习日2, 7/24=学习日8

### 复习间隔计算

对每个 item（learn_date 对应学习日 N）：
- interval 1 → 学习日 N+1
- interval 2 → 学习日 N+2
- interval 4 → 学习日 N+4
- interval 7 → 学习日 N+7
- interval 15 → 学习日 N+15
- interval 30 → 学习日 N+30

如果 N+interval 超出了已有学习日总数，则该 interval 尚未到期。

### review_history 格式

**格式A（早期，无 interval 字段）：**
```json
{"date": "2026-07-13", "result": "pass"}
```
→ 视为在学习日 (对应日期) 完成了复习。

**格式B（有 interval 字段）：**
```json
{"date": "2026-07-20", "result": "reviewed", "interval": 4, "target_date": "2026-07-16"}
```

**算法：** 对每个已学 item，汇总已有复习记录覆盖的 interval，然后检查哪些 interval 的 学习日 ≤ 当前最大学习日 且未复习，加入复习列表。

## 错题分析与记忆加固

当用户完成多轮训练后（建议积累 5+ 错题），分析出错规律：

1. **按 method_type 统计出错率**：计算每种记忆类型的 `出错数 / 已学数`
2. **识别弱项类型**：通常规律是「联想类（多层转换）」>「弱谐音」>「字面」>「外形」
3. **为弱谐音编码添加 memory_hint**：挑出谐音关联较弱的编码，编写画面加固策略
   - 原则：把抽象的谐音转化为具体的视觉场景
   - 例：21鳄鱼 → "数字2是鳄鱼张开的嘴，1是被咬住的棍子"
   - 例：25二胡 → "老爷爷拉二胡，琴弦上刻着25"
4. **同时为同类未学编码预置 memory_hint**：如果某类谐音模式容易出错（如3X开头的"山"系列），提前为未学项预写加固策略

更新 cron 推送脚本时，需在 `calc_review` 和新学展示部分传递 `memory_hint` 字段，并在输出格式中追加 `💡 记忆提示` 行。

## Cron 输出格式要求

- **新学展示按编码数字顺序排列**（升序，如 9→19→20→21→22），不按创建顺序或随机排列
- **复习展示按学习日+编码顺序**，优先展示需要立即复习的项
- 这与交互测试不同——测试时打乱顺序提高难度，cron 报告用数字顺序便于阅读

## Pitfalls

1. **docx 图像 OCR 前必须预处理**：直接 OCR 几乎无输出，需放大 3x + 二值化（阈值 140）
2. **Tesseract 中文语言包**：需 `apt install tesseract-ocr-chi-sim`
3. **cron 测试分离**：cron 只推送内容，不交互测试。测试由用户在聊天中触发
4. **tracker JSON 格式**：review_history 记录 `{date, type: "forward"|"reverse", correct: bool}`
5. **read_file 返回带行号前缀**：使用 execute_code 的 read_file 时，内容每行带 `     1|` 前缀，需用 `line.split('|', 1)[1]` 剥离后再解析 JSON
6. **cron 执行用脚本文件**：不要用 `cat file | python3 -c`（会触发安全拦截），改用 `write_file` + `terminal python3 script.py`
7. **tracker JSON 含控制字符**：review_history 中可能有非法控制字符（如 `\x00`），导致 `json.loads(strict=False)` 也失败。`json_parse`（hermes_tools）同样无法处理。必须用二进制方式读取后逐字节过滤：`clean = bytearray(b for b in raw if b >= 32 or b in (10, 13, 9))`，再 `json.loads(clean.decode('utf-8'))`。最佳实践：用 `write_file` 写独立 .py 脚本，在脚本内 `open(path, 'rb')` 读取并清洗。
8. **复习计算验证方法**：验证 cron 输出是否正确时，按学习日计算应得出远少于自然日的结果（本例：20项 vs 95项，4.8倍差距）。验证脚本模式：提取所有 learn_date 去重排序 → 建日期到学习日序号的映射 → 对每个已学 item 检查各 interval 的目标学习日是否已存在且未复习。
9. **飞书不支持 Markdown 表格**：飞书消息渲染只支持粗体、斜体、代码块、链接，**不支持** `| col | col |` 表格语法。脚本输出若含 markdown 表格，飞书会原样显示 `|` 和 `---` 等标记字符。必须改用列表格式：`**编码** 物品（间隔·学习日）— 记忆方法`，每项一行。已修复于 2026-08-02。
10. **同项多间隔到期去重**：同一 item 的多个 interval 可能同时到期（如学习日13的item在第15天时，1天和2天间隔都已到期）。必须在脚本中按 item key 去重，只保留最小的到期 interval。不去重会导致推送中同一项重复出现（40项变45项等）。修复于 2026-08-09。
11. **交互测试 review_history 须带 interval 字段**：测试通过后标记已复习时，必须同时写入所有已到期间隔（`interval` 字段），否则下次 cron 推送会重复列出这些间隔。格式B记录需包含所有已完成的 interval。
12. **错题记录不带 interval 字段（保持间隔未完成，下次推送加强复习）**：交互测试答错的项，写入 `{"date": ..., "type": "interactive_test", "direction": ..., "correct": false}` 记录，**不带 interval 字段**，这样该 interval 仍视为未复习，下次 cron 推送会继续列出该错题（符合用户"错题提前加强复习"偏好）。同时将 `correct_streak` 重置为 0。
13. **实现陷阱：不要用 `interval=None` 同时充当"新学项跳过"和"错题不写间隔"的哨兵**。批量更新脚本中若写 `if interval is None: continue`，会把答错的复习项（interval 为 None）一起跳过，导致失败记录完全没写入、streak 不归零。正确做法：区分三类——新学项（learn_date 未设置 → 设置 learn_date + 写测试记录）、答对项（带 interval 的 reviewed 记录 + streak+1）、答错项（不带 interval 的 correct:false 记录 + streak 归零），三者都要写。更新后务必运行 `memory_training_daily.py` 验证错题是否出现在下次复习列表。
14. **空 tracker（无任何 learn_date）会报错**：`calc_review` 中 `max(date_to_day.values())` 在无已学项时抛 ValueError。需改为 `max(date_to_day.values()) if date_to_day else 0`（2026-08-20 修复，马斯克 tracker 首次运行触发）。
15. **弱谐音编码加双重通道 memory_hint**：如 48=丝瓜（谐音弱，用户反馈难记），加"8横躺像丝瓜+4像藤架"外形画面 + "48≈是吧"菜市场场景，双重通道更稳。用户主动求助难记编码时，给出画面+场景两种联想，写入 memory_hint 后 cron 自动展示。
