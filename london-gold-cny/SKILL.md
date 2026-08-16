---
source: clawhub
name: "伦敦金人民币价格查询"
description: 查询伦敦金价格，并自动转换为人民币/克单位。适合需要以人民币计价、按克计算黄金价格的场景。
metadata: { "openclaw": { "emoji": "💰", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": null } }
---

# 伦敦金人民币价格查询

查询伦敦金（现货黄金）价格，自动输出 **人民币/克** 和 **美元/盎司** 双单位价格。

## 何时使用

当用户询问以下主题时触发：
- 伦敦金人民币价格
- 国际金价换算成人民币
- 伦敦金多少钱一克（人民币）
- 现货黄金人民币计价

## 技术前提

- Python 3
- **必需**：配置 `JISU_API_KEY` 环境变量（极速数据 API Key）

## 数据源

- **金价数据**：极速数据 JisuAPI（通过 `gold.py london` 接口获取 `/gold/london`）
- **汇率数据**：open.er-api.com

## 故障排查

⚠️ **重要**：原脚本 `london_gold_cny.py` 使用的 `/gold/now` 接口已失效(404)，必须改用 `gold.py london` 获取数据。

## 使用方式

```bash
# 方式一：使用 gold.py 脚本（推荐）
python3 ~/.hermes/skills/gold/gold.py london

# 方式二：手动获取汇率后计算
# 汇率: curl -s "https://open.er-api.com/v6/latest/USD"
# 换算: 人民币/克 = (美元/盎司 × 汇率) / 31.1034768
```

需要先配置环境变量：
```bash
export JISU_API_KEY="your_appkey_here"
```

## 返回结果示例

```json
{
  "品种": "伦敦金",
  "更新时间": "2026-04-21 19:11:45",
  "汇率": {
    "美元兑人民币": 6.8314
  },
  "美元价格(美元/盎司)": {
    "当前价": 4781.79,
    "开盘价": 4824.56,
    "最高价": 4832.94,
    "最低价": 4782.14,
    "昨收价": 4820.63
  },
  "人民币价格(元/克)": {
    "当前价": 1050.25,
    "开盘价": 1059.64,
    "最高价": 1061.48,
    "最低价": 1050.32
  },
  "涨跌": {
    "涨跌额": "-38.84",
    "涨跌幅": "-0.81%"
  },
  "单位说明": "人民币/克 (按当前汇率换算，仅供参考)",
  "数据来源": "极速数据 JisuAPI /gold/london"
}
```

## 单位转换说明

### CNY/gram ↔ USD/ounce 转换公式

```
人民币/克 = (美元/盎司 × 美元兑人民币汇率) / 31.1034768
美元/盎司 = (人民币/克 × 31.1034768) / 美元兑人民币汇率
```

其中：
- 1 盎司 = 31.1034768 克
- 汇率使用实时美元兑人民币汇率

## 前置配置

### 获取 JisuAPI Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 申请黄金价格 API
3. 获取 AppKey 并配置到环境变量

### 配置环境变量

```bash
# 方式一：临时生效
export JISU_API_KEY="your_appkey_here"

# 方式二：持久化（添加到 ~/.profile 或 ~/.local/bin/env）
echo 'export JISU_API_KEY="your_appkey_here"' >> ~/.local/bin/env
```

## 注意事项

- 汇率使用实时市场汇率，可能存在轻微延迟
- 换算结果仅供参考，实际交易价格请以银行/交易所为准
- 本 skill 不存储任何汇率或价格历史数据
- 未配置 JISU_API_KEY 时会返回错误提示

## 已知数据质量问题与修复（2026-08-12 诊断）

### ❌ minprice 字段失真（已移除）

JisuAPI 的 `minprice` 对**伦敦金/伦敦银**恒等于 `price + 0.35`，并非日内最低价（可能是点差或买入报价）。铂金/钯金的 minprice 则正常。

**修复**：`london_gold_cny.py` 已移除 minprice/最低价字段，不再输出。推送脚本 `gold_price_to_feishu.py` 同步移除。

### ❌ 免费汇率 API 返回错误汇率（已加校验）

`exchangerate-api.com` 和 `open.er-api.com` 同时返回 USD/CNY = 6.76（实际应 7.1~7.3），导致人民币/克价格偏低约 7%。

**修复**：新增汇率校验 + 每周缓存机制（`get_usd_cny_rate()` 函数）：
- API 返回值超出 [6.8, 7.5] → 拒绝，回退到缓存
- 汇率写入 `.rate_cache.json`，7 天内不重复请求 API
- 缓存过期才刷新，API 异常时用旧缓存兜底，无缓存时用默认 7.2
- 同时用两个 API 源做冗余

### 诊断方法（可复用）

批量分析 cron 输出目录 `~/.hermes/cron/output/<job_id>/` 中的历史文件，提取每次推送的价格字段做对比：
- 对比 `minprice` 与 `price` 的差值是否恒定 → 识别字段语义异常
- 对比 `汇率` 字段是否在合理区间 → 识别 API 返回异常
- 用 `execute_code` 批量提取正则匹配 + 汇总统计，效率远高于逐条人工查看

## 故障排查记录 (2026-04-21)

| 接口 | 状态 | 说明 |
|------|------|------|
| `/gold/now` | ❌ 404 | 已失效，勿用 |
| `/gold/london` | ✅ 正常 | 当前可用 |
| metals.dev | ❌ 401 | 需要有效API Key |
| goldapi.io | ❌ 403 | 需要有效API Key |
| Yahoo Finance | ❌ 403 | 反爬虫拦截 |
| 新浪财经 | ❌ 403/404 | 接口已下线 |
| 东方财富 | ❌ 失败 | 反爬虫拦截 |