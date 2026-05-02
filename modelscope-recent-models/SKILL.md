---
name: modelscope-recent-models
description: 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序
trigger: 获取ModelScope新模型|modelscope最近模型|ModelScope本周开源
---

# ModelScope 最近模型获取指南

## 关键发现
1. **ModelScope API endpoint都不工作** - 直接HTTP请求全部返回404
2. **必须使用Python SDK** - `pip install modelscope`
3. **使用LastUpdatedTime而非created_at** - `created_at`字段不反映实际最近更新

## 正确的 API 用法

```python
from modelscope.hub.api import HubApi

api = HubApi()

# 获取模型列表 - 注意参数签名
result = api.list_models(
    owner_or_group='modelscope',  # 必需参数
    page_number=1,
    page_size=100
)

# 返回格式是 dict，不是 list
# {'Models': [...], 'TotalCount': N}
models = result.get('Models', [])

# 排序取 TOP 10
models.sort(key=lambda x: x.get('Downloads', 0), reverse=True)
for m in models[:10]:
    print(f"{m.get('Name')}: {m.get('Downloads')} downloads")
```

## 字段映射参考
- 模型名称: `m.get('Name')`
- 下载量: `m.get('Downloads')`
- Star数: `m.get('Stars')`
- 机构: `m.get('Organization', {}).get('FullName', '')`

## 热门数据抓取 (This Week's Trending)
使用 Playwright 从首页抓取:

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch(
        executable_path='/snap/bin/chromium',
        headless=True,
        args=['--no-sandbox']
    )
    page = await browser.new_page()
    await page.goto('https://www.modelscope.cn/home', 
                   wait_until='domcontentloaded', timeout=30000)
    await page.wait_for_timeout(10000)
    lines = await page.evaluate('''() => {
        return document.body.innerText.split('\\n');
    }''')
```

## 环境注意
- 必须使用 hermes venv: `/root/.hermes/hermes-agent/venv/bin/python`
- 系统 Python 被锁定，无法安装额外包
- 脚本开头需要切换 Python 解释器

## 输出格式

```
🤖 ModelScope 本周新开源模型 TOP 10

1️⃣ 模型名称 | 机构 | ⭐下载数
   简介...
   适合场景: xxx

---
数据来源: ModelScope | 采集时间: YYYY-MM-DD
```

## 注意事项
- 无需认证即可获取公开模型
- `LastUpdatedTime` 格式: `2026-04-29T10:30:00Z`
- 下载量数值大，需格式化（229万+）
- 本周通常有30+个模型更新

## 验证
```bash
pip install modelscope
python -c "from modelscope.hub.api import HubApi; print('OK')"
```