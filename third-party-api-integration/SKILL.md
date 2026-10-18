---
source: self-generated
name: third-party-api-integration
description: Use when integrating or migrating a third-party REST API.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [api, integration, migration, cron, vendor]
    related_skills: [cron-job-failure-diagnosis, webhook-subscriptions]
triggers:
  - 旧接口停用 / 接口换代 / endpoint sunset / API migration
  - 第三方 API 接入 / vendor API integration
  - 同步第三方数据到本地 / mirror an external API
  - 定时任务抓第三方数据
  - 字段映射 url→links.original / take→limit 这类迁移改写
---

# 第三方 API 接入与版本迁移

让脚本/cron 长期、低流量地消费第三方 API，并在对方换版/停服时把调用方改完、验证完。

## When to Use

- 用户说某家接口要停用/换代，要把调用方改到新版
- 新接一个 vendor API（要定请求节奏、分页、缓存策略）
- 要维护“本地完整副本”（全量快照 + 增量）
- 排查“任务状态 ok 但数据不对/老死不变的接口”，或旧域名即将只做跳转
- 定时任务报 401/403/Permission denied 这类凭据问题

## 1. 先确认到底有没有 API，别把页面抓取当 API

改别人的“接口”之前，先用 `search_files`（content 模式）按 vendor 域名扫一遍，把**真实调用点**列出来（文件:行号），并区分两类：

- **真·API 调用**（URL 里带 `/api/…`）：拿到结构化字段，按下面第 2–4 节处理
- **HTML 页面抓取**（如 `…/leaderboard`）：vendor 换版时页面结构会一起变，报错形式是“解析失败”而不是 HTTP 错误。**别把停服通知当成它的病因**——两者分开修

把清单连同“文件:行号 + 旧地址”交给用户。顺手分三类：活跃代码/配置（要改）、另一个 profile 的副本（要问用户）、归档备份（一般不动）。

## 2. 请求纪律（按响应头办事，不凭感觉）

- **压缩**：所有请求带压缩（`curl --compressed` / `Accept-Encoding: gzip`）。JSON 压后约为原来 1/4–1/8
- **条件请求**：保存响应 `ETag`，下次带 `If-None-Match`；没变就是 `304` 空正文，直接复用上次结果，**不要重新解析/总结**
  - curl 拿 ETag 要显式落盘响应头：`curl -s --compressed -D /tmp/h.txt -w '\n%{http_code}' <url>`，再从头文件读 `etag:`
- **轮询间隔**：以响应的 `Cache-Control: s-maxage` 为下限（常见 60s）。更密只会拿到同一份共享缓存
- **429 / 503**：读 `Retry-After` 等待后重试**一次**，不要并发重试（单 IP 常见上限约 60 次/分钟）
- **只取变化**：追新条目时用 cursor 往回翻，翻到已见过的 id 就停，不要每次重扫整个时间窗
- **状态文件按“API 版本”标记**：state 里存下 `api_base`；发现版本/域名变了就把旧 `cursor`/`etag` 一并作废（见第 4 节）

## 3. 完整镜像：snapshot + changes

要“本地保存对方全部精选/条目”时，**不要用带时间窗的列表端点**（窗口滚动，早于窗口的条目会静默消失）：

1. 先取一次**全量快照**，按分页参数翻到 `hasMore=false`
2. 快照响应同时给出**同步 cursor**；存下来
3. 之后每轮只请求**增量端点**（changes），只应用 upsert / remove

别人的分页语义各不相同，必须看文档而不是猜。真实坑：同一家 API 里 `snapshot` 用 `page=` 分页、`changes` 用 `cursor=`；给 snapshot 传 `cursor` 会被 400 `invalid_request: Unknown query parameter`；同步 cursor 要取**第一页**返回的那个。

现成实现：`~/.hermes/scripts/aihot_selected_sync.py`（含 ETag/304、gzip、分端点节流、429 退避、snapshot/changes 双模式）。

## 4. 版本/停服迁移

1. **读 vendor 的机器可读说明**（`llms.txt` / `openapi*.json` / 迁移页），不凭旧记忆改；并抓一次真实响应对字段，比只看 schema 更稳
2. **先写字段映射表再动手**：旧路径/参数 → 新路径/参数、旧字段 → 新字段（常见形态：`url→links.original`、`permalink→links.aihot`、`title_en→originalTitle`、`source→source.name`、`take→limit`、时间窗参数化）。嵌套层也可能变（如详情统一挪到 `report` 下）——**改完必须用真实响应回读验证**
3. **域名替换**：并行期过后旧域名只做跳转；把代码、配置、**cron prompt**、skill 文档里的旧域名全换掉，最后用 `search_files` 再扫一遍旧域名，确认只剩“已停用”说明文字
4. **作废旧缓存状态**：不复用旧 cursor / ETag / 本地游标，重新取一次全量快照
5. **按迁移文档补请求特性**（压缩、条件请求、轮询下限）——新版本常把“建议”变成硬要求
6. **端到端实测再收工**：新命令真跑一遍（拿到新版响应 + 消费方脚本跑通），核对投放/落库结果；只改完不实测不算完成

**交付物格式（用户明确要这几项）**：调用点清单 → 改动汇总 → 端到端实测证据 → **需要用户人工确认的清单**（另一个 profile 的副本、归档备份、任务时刻/频率是否要调、许可与授权边界、外部系统/同事脚本是否也要改）。

## 5. 计划任务里的凭据必须“无交互可用”

cron/gateway 跑在 launchd/systemd 里：**没有 TTY，也没有 `SSH_AUTH_SOCK`**。在交互会话里能用 ≠ 任务里能用。

- 典型陷阱：把密钥 `ssh-add` 进 agent 后终端测通了，任务照样 `Permission denied`。验证：`env -u SSH_AUTH_SOCK <原命令>`，失败即说明它只依赖 agent
- 三种 `Permission denied (publickey)` 要分开：① 密钥未注册（没有 `Server accepts key`）；② 已注册但带密码短语无人解锁（有 `Server accepts key`，紧接着 `read_passphrase: can't open /dev/tty`）；③ 已注册但无权限（`ERROR: Repository not found.` 之类）
- 定位哪把密钥已注册：逐把 `ssh -T -o IdentitiesOnly=yes -o BatchMode=yes -i ~/.ssh/<key> <host>`
- 修法：给任务专用**无密码短语**密钥 + host 别名（`IdentityFile` + `IdentitiesOnly yes`）+ 服务端登记公钥

## 6. 交给用户的外部步骤要可验证

让用户去控制台/网页完成一步时，同时给**可核对的指纹**（公钥指纹、开关名、绑定的仓库/账号），并说明单位（仓库级/账号级）。用户回“已完成”后，**拿那把具体产物去实测**，而不是重跑原命令——用户很容易做了相邻但不等价的事（例如解锁了另一把旧密钥），据此宣布修好会把坑埋到下一次自动运行。

## Pitfalls

- **旧 cursor / ETag 不能跨版本复用**：分页游标不透明且与版本/查询绑定，换版后必须重取全量快照
- **同一家 API 不同端点的分页参数可能不同**：改前对每个端点读一遍参数表（`page` vs `cursor` vs `nextPage`），别一个写法套全局
- **列表端点的时间窗会静默丢历史**：用 `mode=all&window=7d` 这类端点维护“完整副本”会漏；完整副本用 snapshot + changes
- **页面抓取源要主动做健康校验**：解析失败时若照旧输出“无变化”，故障会被静默吞掉数周。脚本要对每个源做条目数下限/骤降检查，异常时把警示行作为输出第一行
- **拿不到字段时别当成解析失败**：新版/V2 去掉某个展示字段是结构变化，应按可用键（如 slug）关联另一节点或回退显示该键，而不是判定抓取失败
- **飞书不支持 markdown 表格**：给用户看的报告用列表；表格只写在 markdown 文件里

## 参考

- `references/aihot-api.md` — AIHOT 公开 `/api/v1` 的端点/字段/迁移映射（本 skill 做法在一家真实 vendor 上的完整落地）
