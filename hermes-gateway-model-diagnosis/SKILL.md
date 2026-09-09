---
source: self-generated
name: hermes-gateway-model-diagnosis
description: 网关频道模型/API 报错排查，CLI正常但网关失败时优先怀疑网关进程跑旧代码。
tags: [hermes, gateway, model, provider, api-key, fallback, debugging]
---

# Hermes 网关模型/API 报错排查

## 触发场景
- 某个消息网关频道（飞书/Telegram/微信等）持续报模型错误：`Primary model failed — switching to fallback...`、`HTTP 401/400`、`api key ****xxxx is invalid`
- 同一模型在交互式 CLI 主对话正常，但网关频道失败
- 主模型失败后被 fallback 到另一个 provider，fallback 也报错（通常是 401 鉴权）

## 诊断步骤

### 1. 读出模型与 key 配置（永远只显示 key 尾号，绝不泄露完整 key）
```bash
# .env 中各 key 的尾号 + 长度
python3 - <<'EOF'
import re
for line in open('/root/.hermes/.env'):
    m = re.match(r'^([A-Z_]+)=\s*(\S+)', line.strip())
    if m and m.group(2) not in ('','""') and len(v:=m.group(2).strip('"\'')) > 8:
        print(f'{m.group(1):32s} ...{v[-4:]} (len={len(v)})')
EOF
```
config.yaml 看 `model.default/provider/base_url`、`fallback_model`、`model.api_key`。报错里的 `****ba34` 就是要找的尾号。

### 2. curl 直接验证可疑 key 是否失效（比猜快）
对着该 provider 的 base_url 打 `/models`（只花费一次鉴权，不烧 token）：
```bash
curl -s -o /tmp/r.json -w '%{http_code}\n' -H "Authorization: Bearer $KEY" $BASE_URL/models
cat /tmp/r.json
```
401 且 message 里含 `Authentication Fails ... is invalid` = key 确已吊销/过期。

### 3. 拆开日志里的两层失败
- `errors.log`：`Non-retryable client error ... 401/400` —— 具体 HTTP 错误和模型名
- `agent.log`：`Fallback activated: A → B (provider)` 映射 主模型→fallback 链路
- 关键：**主模型失败 和 fallback key 失效 是两层独立问题**。报错横幅 `Primary failed→switching to fallback: X via Y` 后跟 `401 on ****ba34`，表面上像同一个错，实际得分别修：修主模型的失败原因，同时替换/改指 fallback 的失效 key。死掉的 fallback key 会把主模型的小问题放大成频道整体不可用。

### 4. 极关键的坑：长驻网关进程跑的是旧代码★
网关进程常驻内存，跑的是**启动时加载的代码**。`hermes update` / git pull 拉到新 commit 只改了磁盘文件，**不会自动重启网关**。所以「更新后症状还在」往往是进程还是旧版本。

```bash
# 网关进程启动时间 vs 相关修复 commit 日期
ps -o pid,lstart,etimes -p <gateway_pid>
git -C /root/.hermes/hermes-agent show -s --format='%ad %s' --date=short <relevant_sha>
```

若进程启动时间早于相关修复的 commit 日期 → 进程在跑修复前的旧代码，就是这个根因。修复=重启网关加载新代码。这也解释了「CLI 正常（新进程）但网关失败（旧进程）」的典型分化。

## 修复
1. 修/换主 provider 的问题；若主 provider 有 provider 特有怪癖，见 `references/opencode-go-console.md`。
2. 替换失效的 fallback key，或把 fallback 停用/改指其他可用 provider。
3. 重启网关加载新代码：
```bash
hermes gateway restart
```
注意：`hermes gateway restart` 属于服务级状态变更，可能被安全机制拦截等待用户授权 —— 被拦后**不要强行重试**，把诊断结论交给用户让其确认/自行执行。

## 相关位置
- `/root/.hermes/logs/errors.log` — HTTP 错误
- `/root/.hermes/logs/agent.log` — fallback 链路、进程/会话日志
- `/root/.hermes/.env` — key（只读尾号）
- `/root/.hermes/state.db` 表 sessions（source/chat_type/model/started_at）判断失败会话归属
