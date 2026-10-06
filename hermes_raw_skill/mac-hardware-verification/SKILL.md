---
name: mac-hardware-verification
description: "Use when verifying a used Mac or its hardware health."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macOS, Hardware, Diagnostics, SecondHand, Verification]
    related_skills: [macos-host-provisioning, macos-local-dev-stack]
---

# Mac 硬件体检与二手验机

回答「这台 Mac 硬件正不正常 / 二手买来的能不能放心」这类问题。全程用 macOS 自带工具，
不需要装任何第三方软件 —— 也没有第三方软件能拿到系统不暴露的数据。

## When to use

- 用户说「检测/体检一下这台 Mac」「这机器硬件有没有问题」「二手买的，想验一下」
- 用户问某款手机工具（爱思助手之类）能不能检测 Mac、有没有类似的 Mac 工具
- 一台机器要作为常驻主机上线前，留一份硬件基线

## Step 0 — 先校正前提，再决定装不装

- **iPhone 设备管理工具检测不了 Mac。** 爱思助手/i4Tools 这类工具的对象是通过数据线连上的
  iOS 设备（电池循环、零件序列号、翻新识别）；官网功能列表里没有「给电脑做体检」。被问到
  「能不能检测 Mac」时答案是不行，并且**不要**为了迁就这个前提去把软件装上 —— 先纠正前提，
  再给出真正能满足目的的做法。装一个干不了这活的第三方闭源软件，换来的是隐私暴露和一个用不上的图标。
- **Mac 侧没有等价于「验机报告」的工具**，因为 Apple 不向 macOS 暴露零件级计数器（更换记录、
  屏幕/摄像头序列号核对、翻新史都读不到）。能量到的只够判断「正不正常 / 是否原装」，不够判断
  「内部零件有没有被换过」—— 这句话要明说，别让用户以为一次体检等于验机报告。

## Step 1 — 一次批量只读采集

```bash
system_profiler SPHardwareDataType | grep -E "Model Name|Model Identifier|Chip|Total Number of Cores|Memory|Serial Number|System Firmware|Hardware UUID|Activation Lock"
system_profiler SPDisplaysDataType | grep -E "Chipset Model|Total Number of Cores|Metal|Resolution"
system_profiler SPNVMeDataType | grep -E "Model|Capacity|Revision|Serial" | head -6
system_profiler SPPowerDataType | grep -E "Cycle Count|Condition|Maximum Capacity|Full Charge|Design Capacity"   # 仅笔记本有
system_profiler SPThunderboltDataType | grep -E "Bus|Status|Speed"
diskutil info disk0 | grep -E "Device / Media Name|Disk Size|SMART|Solid State|Protocol"
pmset -g therm; pmset -g batt
ls /Library/Logs/DiagnosticReports/*.panic 2>/dev/null | wc -l
profiles status -type enrollment      # MDM/DEP，二手机器必查
csrutil status; fdesetup status; /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
sysctl -n vm.swapusage; memory_pressure | tail -1; df -h /
```

字段含义、阈值与台式机/笔记本差异：`references/hardware-checks.md`。

## Step 2 — 怎么读这些数字

- **SMART**：Apple 自家 SSD（Apple Fabric）只给总评 `Verified`，`Not Supported` 也会出现；
  **磨损度 / TBW / 通电小时数读不到**。所以只能说「SMART 总评 Verified」，不要说「SSD 健康度 100%」。
- **电池（仅 MacBook）**：`Cycle Count` + `Maximum Capacity` + `Condition` 是二手验机最值钱的一项。
  参考：Apple 把 1000 次循环内、容量 ≥80% 视为正常；循环数远超机器年龄要警惕换过电池。
- **`Activation Lock Status: Enabled`**：系统上仍有 Apple ID 开着「查找」。二手机器必须让用户确认
  那是自己的账号，否则将来重装/转手会卡死。
- **MDM**：`profiles status -type enrollment` 报 `Enrolled via DEP: Yes` / `MDM enrollment: Yes`
  说明机器仍挂在某组织名下、可被远程抹除 —— 二手 MacBook 第一该查的就是它。
- **0 个 `.panic` + `pmset -g therm` 全为「未记录」** = 此前无内核崩溃、无热降频历史。
- **接口**：`SPThunderboltDataType` 看总线数与协商速率（40 Gb/s = TB4/USB4 满速）。

## Step 3 — 满载压力测试（最容易做错的一步）

目的：确认散热与供电能稳定压满全部核心、不降频、不崩。

- 用 `subprocess.Popen(["sh", "-c", "while :; do :; done"])` × 核数起负载；每 30 秒采样
  `uptime` 与 `pmset -g therm`；结束时逐个 `terminate()`（再 `kill` 兜底），并确认负载回落。
- **不要用裸 multiprocessing 起进程**：缺 `if __name__ == "__main__":` 守卫时，spawn 的子进程会
  重新执行整个脚本 → 输出爆炸、CPU 根本没压上去（负载停在 1~2），你会得到一份看起来「很干净」的
  假报告。要嘛补守卫，要嘛用上面的 Popen 写法。
- 判定看三件事：负载能到核数量级、全程无热/性能警告、结束后负载回落。
- **只读体检不要顺手做重 IO**：几 GB 的 `dd` 写入会触发 macOS 的「disk writes 超预算」记录并
  把写入量记到某个常驻服务名下（`.diag` 里 `Event: disk writes`，`Action taken: none`），
  既污染诊断目录又要向用户解释。

## Step 4 — 必须人工测的（软件替代不了，列成清单交给用户）

键盘全键 / 触控板与手势 / 屏幕坏点与涂层 / 摄像头·麦克风·扬声器 / 每个接口各插一次 /
Wi-Fi 两个频段 + 蓝牙 / 合盖睡眠唤醒 / 满载时风扇异响与温度 / 外壳磕碰·螺丝划痕·底面平整
（电池鼓包）/ 机身序列号与系统内是否一致。

## Step 5 — 权威结论只有两条路（都不是 agent 能代跑的）

1. **Apple 官方诊断**：关机后按住电源键进入启动选项 → `Command-D`，做内存/存储/GPU/Wi-Fi 的
   官方级检测并给错误码。需要人在机器前；agent 不要代跑，也不要引导远程重启。
2. **序列号官网核对**：https://checkcoverage.apple.com 查机型与保修；查不到或机型不符要警惕
   翻新/换壳。序列号取自 `SPHardwareDataType`。

## Step 6 — 给够不着的机器交付脚本

远端 Mac（笔记本）跑不了时，给一个**双击即可运行**的 `.command`：只用系统自带工具、不装软件、
不改设置、报告写到桌面并在终端打印路径，让用户把报告发回来。起点用 `templates/mac-report.command`。要点：

- 写桌面失败要回退到 `$HOME`、再回退到当前目录，**并检查文件真的存在**再报成功；
- 报告末尾附 Step 4 的手工清单，用户跑一次就有全套结论；
- 交付前 `bash -n` 过语法并在本机先跑一遍；本机是台式机时电池段会走「未检测到电池」分支，
  正好验证分支存在。

## Pitfalls

- 别把 `.diag` 当崩溃：`/Library/Logs/DiagnosticReports/` 里除 `.ips`/`.panic` 外还有
  microstackshots、signpost、`disk writes` 之类的资源记账文件，都不表示故障。
- 别只用「负载压上去了」当通过标准，还要看热警告与压测后回落。
- 只做体检就只做体检：FileVault / 防火墙 / 备份这些**只报告、不代改**。
- 磁盘吞吐数字受页缓存影响极大，只能当「没有明显异常」的参考，不要当跑分报给用户。
- 报告里带序列号等标识时写进文件，聊天只给结论 —— 聊天记录是长期留存的。

## Reporting

- 结论先行：**硬件层面是否发现异常**，然后才是证据与待办。
- 用户看清单不看日志：整机 / 存储 / 电池 / 故障痕迹 / 安全项 / 手工清单，每条后面跟实测值。
- 文件交付（报告 + 可运行脚本），聊天里给摘要和附件；不要粘贴命令输出。
