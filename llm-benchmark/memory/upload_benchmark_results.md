---
name: upload_benchmark_results
description: 提醒上传LLM基准测试结果到GitHub
type: feedback
---

每次完成 evalscope 测试后，提醒用户是否要将测试结果上传到 GitHub 仓库 https://github.com/JuniorSummer/ClaudeProject

**如何应用:**
- 用户运行 llm_benchmark 或 llm_perf_test.py 测试后
- 测试结果通常保存在 /root/evalscope_results/ 目录
- 确认后再执行上传操作