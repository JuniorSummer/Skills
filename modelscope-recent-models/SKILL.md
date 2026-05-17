---
name: modelscope-recent-models
description: 获取ModelScope魔搭社区最近更新的模型列表，按下载量排序
trigger: 获取ModelScope新模型|modelscope最近模型|ModelScope本周开源
---

# ModelScope 最近模型获取指南

## 关键发现
1. **OpenAPI 可用** — `/openapi/v1/models` 和 `/openapi/v1/datasets` 支持 GET 请求
2. **snap Chromium 不可用** — AppArmor 限制导致 ProcessSingleton socket 创建失败，Playwright 浏览器抓取方案不可行
3. **Python SDK 的 `list_models` 只能按 owner/org 查询**，不支持全局排序
4. **Studios API 不存在** — `/openapi/v1/studios` 返回 404
5. **首页是纯 SPA** — HTML 中无数据，必须用 API

## 推荐方案: OpenAPI 直接调用（无需 Playwright/浏览器）

### 模型 API
```
GET https://www.modelscope.cn/openapi/v1/models
参数: page_number, page_size, sort
sort 可选值: downloads | likes | last_modified
```

### 数据集 API
```
GET https://www.modelscope.cn/openapi/v1/datasets
参数: page_number, page_size, sort
sort 可选值: default | downloads | likes | last_modified
```

### Python 示例
```python
import requests

BASE = 'https://www.modelscope.cn'

# 热门模型 TOP 10
r = requests.get(f'{BASE}/openapi/v1/models', params={
    'page_number': 1, 'page_size': 10, 'sort': 'downloads'
})
models = r.json()['data']['models']

# 最近更新模型
r = requests.get(f'{BASE}/openapi/v1/models', params={
    'page_number': 1, 'page_size': 10, 'sort': 'last_modified'
})

# 热门数据集
r = requests.get(f'{BASE}/openapi/v1/datasets', params={
    'page_number': 1, 'page_size': 5, 'sort': 'downloads'
})
```

### 返回字段（models 和 datasets 通用）
- `id`: 完整路径如 `"iic/SenseVoiceSmall"`
- `display_name`: 显示名称
- `description`: 描述
- `downloads`: 下载量（整数）
- `likes`: 点赞数
- `last_modified`: ISO 时间如 `"2026-05-15T01:09:19Z"`
- `created_at`: 创建时间
- `license`: 许可证
- `tasks`: 任务标签列表

## 旧方案（已废弃）: Python SDK + Playwright
~~使用 `modelscope.hub.api.HubApi.list_models(owner_or_group='modelscope')` 只能查单个 org。~~
~~Playwright 抓取首页因 snap Chromium AppArmor 限制不可用（ProcessSingleton socket 创建失败）。~~

## 环境注意
- 必须使用 hermes venv: `/root/.hermes/hermes-agent/venv/bin/python`
- snap Chromium 因 AppArmor 限制无法启动（ProcessSingleton socket 目录创建失败）
- 如果需要浏览器渲染，需安装 Playwright 自带的 Chromium（`playwright install chromium`，~167MB）

## 输出格式

```
🤖 ModelScope 本周热门模型 TOP 10

1️⃣ 模型名称 | ⭐下载数 | 🔗 org/model-name
   简介...

--- 
数据来源: ModelScope OpenAPI | 采集时间: YYYY-MM-DD
```

## 注意事项
- 无需认证即可获取公开模型和数据集
- `last_modified` 格式: ISO 8601 如 `2026-05-15T01:09:19Z`
- 下载量数值大，需格式化（2.5亿、5862.3万等）
- Studios/workflows API 不存在，无法获取
- sort 仅支持: `downloads`、`likes`、`last_modified`，无"本周"维度排序