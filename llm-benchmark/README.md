# LLM Benchmark Skill

大模型性能与能力基准测试工具。

## 功能

- **性能测试**: 推理速度、批量吞吐、并发性能、显存占用
- **能力测试**: 知识问答、逻辑推理、数学计算、语言理解、阅读理解、代码生成
- **支持MoE模型**: 自动修补transformers的grouped_mm兼容性问题

## 使用方法

### 1. 性能测试

```bash
python scripts/llm_perf_test.py \
    --model /path/to/model \
    --name "Model Name" \
    --gpu 0 \
    --output results.json
```

参数说明:
- `--model`: 模型目录路径
- `--name`: 模型名称（用于报告）
- `--gpu`: GPU ID (默认0)
- `--output`: 输出JSON文件路径

### 2. 基准能力测试

```bash
python scripts/llm_benchmark_test.py \
    --model /path/to/model \
    --name "Model Name" \
    --gpu 0 \
    --output benchmark_results.json
```

## 测试项目

### 性能测试
1. **基础推理性能**: 不同输入长度的吞吐量
2. **批量推理**: batch=1/2/4/8的吞吐量
3. **并发请求**: 1/2/4/8/16并发的吞吐量和延迟
4. **显存占用**: 当前、预留、峰值显存

### 能力测试
1. **知识问答**: 5道常识题
2. **逻辑推理**: 3道推理题
3. **数学计算**: 5道数学题
4. **语言理解**: 主语谓语识别、时态转换、句子解释
5. **阅读理解**: 2篇阅读理解
6. **代码生成**: 2道编程题

## 输出示例

### 性能测试结果 (JSON)
```json
{
  "model": "Qwen3.5-35B-A3B",
  "tests": {
    "input_x1": {"throughput": 18.89, "latency": 5.29},
    "batch_8": {"throughput": 176.96, "avg_latency": 0.57},
    "concurrent_16": {"throughput": 16.19, "p99_latency": 98.81},
    "memory": {"max_allocated_gb": 67.42}
  }
}
```

### 基准能力测试结果
- knowledge: 知识问答结果列表
- reasoning: 逻辑推理结果列表
- math: 数学计算结果列表
- language: 语言理解结果列表
- reading: 阅读理解结果列表
- code: 代码生成结果列表

## 注意事项

1. **MoE模型支持**: 自动修补torch._grouped_mm的CC=9.0限制问题
2. **显存要求**: 35B模型需要约70GB显存，27B模型需要约52GB
3. **测试时间**: 完整测试约需10-15分钟
4. **网络要求**: 使用evalscope官方数据集需要网络访问

## 故障排除

### 问题: torch._grouped_mm错误
**解决**: 脚本已自动修补，无需手动处理

### 问题: 显存不足
**解决**: 减少batch_size或并发数

### 问题: 模型加载慢
**解决**: 首次加载需要下载模型权重，后续会缓存