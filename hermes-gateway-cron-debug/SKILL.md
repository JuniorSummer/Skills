---
name: hermes-gateway-cron-debug
description: Hermes Gateway 进程卡死导致定时任务失效的排查与修复
tags: [hermes, gateway, cron, process, deadlock, debugging]
---

# Hermes Gateway 进程卡死导致定时任务失效

## 问题症状
- 定时任务（cron job）停止推送
- 在日志中没有看到任何 "scheduler" 或 "Running job" 的记录
- cron job 配置看起来正常，但任务就是不执行

## 根因分析
Hermes Gateway 进程（负责定时任务调度）可能因为以下原因卡死：
- 长时间运行的进程内存泄漏
- 异步任务阻塞
- 数据库连接问题
- 外部依赖超时

## 诊断步骤

### 1. 检查 cron job 配置和状态
```bash
cronjob action=list
```
查看：
- `last_run_at` 最后运行时间
- `last_status` 最后状态
- `next_run_at` 下次运行时间

### 2. 检查 Gateway 进程状态
```bash
ps aux | grep "hermes.*gateway"
```
查看进程运行时间（`etime`），如果运行时间异常长（如超过24小时）且无活动，说明可能卡住了。

### 3. 检查调度日志
```bash
grep -E "scheduler|scheduled job|due" ~/.hermes/logs/agent.log | tail -30
```
如果没有今天的调度记录，说明调度器未工作。

### 4. 检查进程的最后活动时间
```bash
ls -la /proc/<PID>/fd
```
查看进程打开的文件描述符，最后修改时间可以判断进程是否还有活动。

## 修复方案

### 步骤1: 终止卡住的进程
```bash
kill <gateway_pid>
```

### 步骤2: 重启 Gateway
```bash
# 使用 background 模式启动
terminal(background=true, command="/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace")
```

### 步骤3: 验证恢复
```bash
# 手动触发一个 cron job 测试
cronjob action=run job_id=<job_id>
```

### 步骤4: 确认日志中有调度记录
```bash
grep "scheduler" ~/.hermes/logs/agent.log | tail -10
```

## 预防措施
- 定期检查 Gateway 进程状态
- 可以设置定时任务（如每天凌晨）自动重启 Gateway：
  ```bash
  # 每天 4:00 重启 Gateway（可选）
  0 4 * * * pkill -f "hermes.*gateway" && nohup /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace > /dev/null 2>&1 &
  ```

## 相关日志位置
- `/root/.hermes/logs/agent.log` - 主日志，包含调度信息
- `/root/.hermes/logs/errors.log` - 错误日志