---
name: "time-restricted-cron"
description: 创建时间限制的定时任务模式 - 当复杂cron表达式不可用时，使用Python包装脚本实现时间范围限制
---

# 时间限制的定时任务模式

当需要创建在特定时间范围内执行的定时任务（如每天9:00-21:00），但复杂的cron表达式（如 `0,30 9-21 * * *`）无法使用时，可以采用Python包装脚本模式。

## 问题场景

- 复杂cron表达式需要croniter库支持
- 有时croniter检测失败或表达式解析出错
- 需要在特定时间范围内执行任务

## 解决方案

创建一个Python包装脚本，在执行前检查当前时间：

```python
#!/usr/bin/env python3
"""
任务包装脚本 - 带时间限制
只在指定时间范围内执行
"""
import sys
from datetime import datetime

# 检查时间是否在范围内
now = datetime.now()
hour = now.hour

# 设置时间范围 (示例: 9:00-21:00)
START_HOUR = 9
END_HOUR = 21

if hour < START_HOUR or hour > END_HOUR:
    print(f"当前时间 {now.strftime('%H:%M')} 不在执行范围 ({START_HOUR}:00-{END_HOUR}:00) 内，跳过")
    sys.exit(0)

# 在时间范围内，执行实际任务
# 方式1: 执行命令
# import subprocess
# subprocess.run(['your', 'command', 'here'])

# 方式2: 导入并运行模块
# import your_module
# your_module.main()

# 方式3: 设置环境变量后执行
import os
os.environ['YOUR_API_KEY'] = 'your_key_here'
exec(open('/path/to/your/script.py').read())
```

## 使用步骤

1. 创建包装脚本 `wrapper.py`
2. 设置定时任务使用简单间隔格式：
   ```
   schedule: every 30m
   ```
3. 在cronjob prompt中调用包装脚本

## 实际案例

伦敦金价格查询任务（9:00-21:00每30分钟）：

```python
#!/usr/bin/env python3
import sys
import os
from datetime import datetime

now = datetime.now()
hour = now.hour

if hour < 9 or hour > 21:
    print(f"当前时间 {now.strftime('%H:%M')} 不在查询时间范围 (9:00-21:00) 内，跳过执行")
    sys.exit(0)

os.environ['JISU_API_KEY'] = 'your_api_key'
exec(open(os.path.expanduser('~/.hermes/skills/london-gold-cny/london_gold_cny.py')).read())
```

Cron配置：
```
schedule: every 30m
prompt: |
  执行脚本获取数据：
  python3 ~/.hermes/skills/london-gold-cny/query_with_time_check.py
  
  如果返回了数据，整理推送给用户。
  如果返回"跳过执行"，无需推送。
```

## 注意事项

- 时间检查使用24小时制
- `END_HOUR=21` 表示21:00是最后可执行时间，21:30不会执行
- 如需包含21:30，设置 `END_HOUR=21` 并检查 `hour > 21 or (hour == 21 and now.minute > 30)`
- 包装脚本需要可执行权限: `chmod +x wrapper.py`

## 依赖

- Python 3
- 无需额外依赖（使用标准库）
