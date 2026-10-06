---
source: self-generated
author: Hermes Agent
license: MIT
name: used-mac-hardware-check
description: "Verify a second-hand Mac's hardware (二手 Mac 验机)."
version: 1.0.0
metadata:
  hermes:
    tags: [macos, diagnostics, hardware, second-hand, verification]
---

# 二手 Mac 验机（硬件体检）

## When to Use

- 用户买了二手 Mac，想知道硬件是否正常、是否被翻新或换过件。
- 用户问某个手机管理工具（爱思助手 / i4Tools 类）能不能“检测 Mac 的情况”。
- 任何需要给一台 Mac 出一份硬件体检报告的场合。

## 0. 先纠正前提：没有 Mac 版“爱思助手”

爱思助手这类工具的检测对象是**数据线连上去的 iPhone/iPad**（验机报告 = 电池循环、屏幕/摄像头零件序列号、翻新识别、刷机/备份/投屏）。**Mac 侧 Apple 不暴露零件级计数器与维修记录，不存在对等的一键验机工具。**

不要因此直接告诉用户“做不到”，给替代路径：

1. 系统自带工具（下面步骤 1~4）——免费、最全面
2. **Apple Diagnostics**（关机→按住电源键→启动选项→Command-D）——官方硬件自检，需人在机器前
3. 序列号官网核对（checkcoverage.apple.com）——查机型一致性与保修
4. 第三方（DriveDx 读 SSD 磨损、Sensei 综合、iStat Menus 温度/风扇，均付费）——只有它们能补 Apple 不开放的传感器/磨损数据

## 1. 先跑模板脚本

`templates/mac-hardware-check.command`：拷到目标 Mac 上双击运行（首次可能要在「系统设置→隐私与安全性」里允许），会在桌面生成一份 markdown 报告。
它覆盖：机型/芯片/内存/序列号、内置 SSD 与 SMART、崩溃计数、热警告、Thunderbolt 总线、电池（笔记本）、MDM、SIP/FileVault、内存与交换、以及一份“必须手动测”勾选单。
让用户把报告发回来，再依据下面的判读规则下结论。

## 2. 二手专项：先查这三项

- **MDM 注册**：`profiles status -type enrollment` → 出现 `Enrolled via DEP: Yes` 或 `MDM enrollment: Yes` 意味着机器仍受某组织管理，可能被远程抹除。**二手 MacBook 第一个要查的就是它**。
- **激活锁**：`system_profiler SPHardwareDataType | grep "Activation Lock"` → `Enabled` 表示当前系统上有 Apple ID 开着“查找”。是卖家的账号就必须先让卖家退出，否则将来重装/转手会卡死。
- **序列号核对**：给用户 https://checkcoverage.apple.com 与序列号，让他自己刷（agent 不代填表单）。查不到或机型不符 → 警惕翻新/换壳。

## 3. 笔记本特有：电池

`system_profiler SPPowerDataType` → `Cycle Count` / `Maximum Capacity` / `Condition`。判读：1000 次循环内且容量 ≥80% 视为正常；循环数远高于机龄要警惕（可能换过电池或长期插电）。台式机（Studio/mini）没有电池项，报“未检测到电池”即可，不要说成异常。

## 4. 满载压测：起负载与判读

- 起负载：`subprocess.Popen(["sh", "-c", "while :; do :; done"])` × 核数，定时采样 `uptime` 与 `pmset -g therm`，结束后自己 `terminate()`。
- **不要**用 Python `multiprocessing` 直接 spawn：子进程会重新 import 主模块，缺 `if __name__ == "__main__":` 守卫时会把整个脚本再跑 N 遍（输出爆炸、CPU 根本没压上去）。
- 判读：10 核 M1 Max 上负载应爬到 8~12；全程 `pmset -g therm` 无 “thermal warning / performance warning has been recorded” 即散热与供电正常。
- 负载是**滑动平均**，压测结束后回落要一两分钟，别当场当成异常；再用 `pgrep` 确认没有残留负载进程。
- 压测后复查 `.panic` 计数没新增。

## 5. 结果判读的坑

- `diskutil info disk0` 的 SMART 在 Apple 内建 SSD 上时而报 `Verified`、时而报 `Not Supported`，
  两者都不等于故障；Apple Fabric SSD 不向系统暴露磨损度/TBW，想要百分比只能靠第三方工具。
- `/Library/Logs/DiagnosticReports/*.diag` 里的 `disk writes` 条目是 macOS 的**写入预算记账**（进程组累计写入超阈值就落一条），
  不是崩溃；只有 `.panic` 才是内核崩溃。别把工作负载造成的记录写成“硬件异常”。
- 并发跑同一套 dump 会拿到不一致结果（同时多次 `diskutil` 会得到不同 SMART 字样），一次跑一遍。
- 内存要看 `swap` 与内存压力百分比一起看：`swap = 0` 且内存压力自评 90% 空闲就是健康，“可用内存只剩 1GB”是份量口径，不是告警。

## 6. 只能人工的项（写进报告让用户做）

Apple Diagnostics（Command-D）；逐个插口（Thunderbolt、USB-A、HDMI、网口、SD）；键盘/触控板/屏幕坏点与涂层/摄像头/麦克风/扬声器；合盖睡眠与唤醒；外壳四角、背面螺丝是否被拆过、底面是否平整（电池鼓包）。
任何软件都替代不了这几项，报告里要写清。

## 7. 报告形状

结论先行（有没有异常）→ 分项数据 → **需要用户手动做的清单** → **查不到的项**（明确说清）。
用短列表分条，不要用 markdown 表格（飞书不渲染表格）；数据要带具体数字，不要只写“正常”。
