---
source: self-generated
name: hermes-gateway-crash-loop-diagnosis
description: "Gateway crash-loop: all channels drop, restarts climb."
tags: [hermes, gateway, crash-loop, startup, watchdog, uv, pypi, debugging]
---

# Hermes Gateway 崩溃重启(crash-loop)排查

## 触发场景
- 微信、飞书、telegram 等所有信道**同时**断连(不是单个频道掉线)
- 定时任务也一并失效
- `systemctl status hermes-gateway` 里 restart counter 不断攀升(如重启 17 次), 状态反复 failed

## 判定特征(三连确认就是 crash-loop)
1. journalctl/日志末尾: `Main process exited, code=exited, status=75/TEMPFAIL` 且 `Failed with result 'exit-code'`
2. gateway.log 出现 `gateway.shutdown_watchdog: ... missing 3 consecutive liveness probes; dumping all thread stacks and exiting with code 75 so the service supervisor can restart it`
3. gateway.log 里某一行**带时间戳反复重复**, 典型是 `Platform 'Feishu / Lark' dependencies missing — attempting install...`

**关键认知**: `exit 75/TEMPFAIL` 是**看门狗判定事件循环失活**而主动杀进程, 不是进程真的死了。它只在启动阶段某个**同步调用阻塞了事件循环**约 2 分钟时触发。systemd 立刻拉起它 → 又在同一步卡住 → 无限循环。

## 诊断步骤
```bash
# 1. 服务状态: 重启计数 + 最近失败
systemctl status hermes-gateway
# 2. 看门狗杀进程时转储的线程栈 = 阻塞点(最有用)
journalctl -u hermes-gateway --no-pager -n 60 | grep -vE "WAL-reset|vulnerable"
#   栈里停在哪一行/哪个函数, 就是启动在等什么
# 3. gateway.log 重复行
grep -iE "dependencies missing|attempting install|shutdown_watchdog" ~/.hermes/logs/gateway.log | tail
```
线程栈里出现 `subprocess.communicate` / `_run_installer` / `lazy_deps._venv_pip_install`, 且被 `adapter.check_*_requirements` → `platform_registry._probe` 调用 → 就是这条根因: 网关启动时为某平台装可选依赖, 同步 `subprocess.run(uv pip install ...)` 阻塞了 asyncio 事件循环。

## 根因: uv 不读 pip.conf → 连不上国内镜像
网关启动时 `lazy_deps.ensure()` 用 **uv** 装依赖(如飞书 lark-oapi)。但:**uv 不读 pip.conf 里的 index-url** → 直接连 pypi.org → 国内服务器访问超时 → `uv pip install` 永久卡住 → 事件循环被堵 2 分钟 → 看门狗杀 → 循环。而 `venv/bin/pip` 因配了腾讯云镜像 `mirrors.tencentyun.com` 是秒通的。

验证 uv 是被网络卡住还是成功:
```bash
# 若这条秒回 → uv 已能用镜像; 若挂住 → 就是被 pypi.org 卡
/root/.local/bin/uv pip install lark-oapi==1.6.8 --dry-run
```

## 修复(两步, 先解阻塞, 再根治镜像)

### 第 1 步: 让 uv 走国内镜像(根治)
创建 `~/.config/uv/uv.toml`, 指向与 pip 相同的镜像; 网关以 root 跑则放 `/root/.config/uv/uv.toml`:
```ini
[[index]]
url = "http://mirrors.tencentyun.com/pypi/simple"
default = true
```
uv 的默认索引源由这个文件接管, 不再硬连 pypi.org。

### 第 2 步: 预装依赖到网关 venv(立即解除阻塞)
装好后再启动, 启动时的 `ensure()` 检测到已满足会**瞬时返回**, 不再触发安装:
```bash
cd /root/.hermes/hermes-agent && ./venv/bin/pip install lark-oapi==1.6.8 qrcode==7.4.2
# 验证: missing 为空 + ensure 秒回(<1s)
cd /root/.hermes/hermes-agent && time ./venv/bin/python -c "
from tools.lazy_deps import ensure, feature_missing
print('missing:', feature_missing('platform.feishu'))
print('ensure:', ensure('platform.feishu', prompt=False))
"
```
`feature_missing` 返回空元组 `()`、`ensure` 0.1s 内返回 → 依赖探测是空操作, 网关启动不会再卡。对应平台的具体 pin 版本在 `tools/lazy_deps.py` 的 `LAZY_DEPS` 字典里(如 `platform.feishu` = `lark-oapi==1.6.8`, `qrcode==7.4.2`)。

## 坑
- **重启网关服务属于服务级状态变更, 会被安全机制拦截等待用户授权。被拦后不要强行重试**, 把诊断结论交给用户让其确认/自行执行 `systemctl start hermes-gateway`。
- 看门狗约 2 分钟才杀进程, 所以 crash 间隔稳定在 ~2 分钟——这是判断「启动阻塞」而非「真死」的节奏信号。
- `lark_oapi` 已装但版本不对也会被当缺失触发重装(pin 严格 `==`)。改完版本后务必验证 `feature_missing()` 为空。
- 每个启动周期日志只有几行且不断被截断, 不要只读 gateway.log 头部; 用 journalctl 看线程栈和退出码更可靠。

## 相关位置
- `~/.hermes/logs/gateway.log`, `journalctl -u hermes-gateway`
- `/root/.hermes/hermes-agent/tools/lazy_deps.py`(LAZY_DEPS 字典、ensure/is_available)
- `/root/.hermes/hermes-agent/plugins/platforms/<name>/adapter.py`(check_*_requirements)
- 相关: 网关卡死(定时任务失效)见 hermes-gateway-cron-debug; 网关模型/API 报错见 hermes-gateway-model-diagnosis
