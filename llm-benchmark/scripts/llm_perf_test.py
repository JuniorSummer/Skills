#!/usr/bin/env python3
"""
大模型性能测试脚本
用于测试LLM的推理速度、批量吞吐、并发性能、显存占用
支持MoE架构模型（如Qwen3.5-35B-A3B）的fallback模式
"""
import os
os.environ['USE_GROUPED_MM'] = '0'

import torch
import time
import json
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers.integrations.moe as moe_module

# 修补35B模型的grouped_mm问题
moe_module._can_use_grouped_mm = lambda *args: False

def load_model(model_path, gpu_id=0):
    """加载模型"""
    print(f"加载模型: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=torch.bfloat16,
        device_map=f"cuda:{gpu_id}",
        trust_remote_code=True,
    )
    print(f"模型加载完成")
    return model, tokenizer

def test_single_request(model, tokenizer, prompt, max_new_tokens=100):
    """测试单个请求"""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    start = time.time()
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id
        )
    end = time.time()

    input_len = input_ids.shape[1]
    output_len = output_ids.shape[1] - input_len
    latency = end - start

    return {
        "input_tokens": input_len,
        "output_tokens": output_len,
        "latency": latency,
        "throughput": output_len / latency if latency > 0 else 0
    }

def test_batch_inference(model, tokenizer, prompts, max_new_tokens=100):
    """测试批量推理"""
    inputs = tokenizer(prompts, return_tensors="pt", padding=True)
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    start = time.time()
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id
        )
    end = time.time()

    elapsed = end - start
    total_output_tokens = sum(
        o.shape[0] - i.shape[0]
        for i, o in zip(input_ids, outputs)
    )
    batch_size = len(prompts)

    return {
        "batch_size": batch_size,
        "total_output_tokens": total_output_tokens,
        "elapsed_time": elapsed,
        "throughput": total_output_tokens / elapsed if elapsed > 0 else 0,
        "avg_latency": elapsed / batch_size
    }

def test_concurrent_requests(model, tokenizer, prompt, num_requests, max_new_tokens=100):
    """测试并发请求"""
    def run_request(i):
        return test_single_request(model, tokenizer, prompt, max_new_tokens)

    start = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(run_request, i) for i in range(num_requests)]
        for future in as_completed(futures):
            results.append(future.result())
    end = time.time()

    elapsed = end - start
    total_output = sum(r["output_tokens"] for r in results)
    latencies = [r["latency"] for r in results]

    return {
        "num_requests": num_requests,
        "total_output_tokens": total_output,
        "total_time": elapsed,
        "throughput": total_output / elapsed if elapsed > 0 else 0,
        "avg_latency": statistics.mean(latencies),
        "p50_latency": statistics.median(latencies),
        "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
        "min_latency": min(latencies),
        "max_latency": max(latencies)
    }

def run_tests(model_path, model_name, gpu_id, output_file):
    """运行完整的性能测试"""
    results = {
        "model": model_name,
        "model_path": model_path,
        "gpu_id": gpu_id,
        "tests": {}
    }

    model, tokenizer = load_model(model_path, gpu_id)

    test_prompt = "请介绍一下人工智能的发展历史、应用现状和未来发展趋势，需要详细说明。"

    print(f"\n{'='*60}")
    print(f"测试模型: {model_name}")
    print(f"{'='*60}")

    # 测试1: 基础推理性能
    print("\n[测试1] 基础推理性能")
    for input_len_multiplier in [1, 5, 10]:
        prompt = test_prompt * input_len_multiplier
        result = test_single_request(model, tokenizer, prompt, max_new_tokens=100)
        key = f"input_x{input_len_multiplier}"
        results["tests"][key] = result
        print(f"  输入x{input_len_multiplier}: {result['output_tokens']} tokens, "
              f"延迟={result['latency']:.2f}s, 吞吐量={result['throughput']:.2f} tokens/s")

    # 测试2: 批量推理
    print("\n[测试2] 批量推理")
    for batch_size in [1, 2, 4, 8]:
        prompts = [test_prompt] * batch_size
        result = test_batch_inference(model, tokenizer, prompts, max_new_tokens=100)
        key = f"batch_{batch_size}"
        results["tests"][key] = result
        print(f"  batch={batch_size}: 吞吐量={result['throughput']:.2f} tokens/s, "
              f"平均延迟={result['avg_latency']:.2f}s")

    # 测试3: 并发请求
    print("\n[测试3] 并发请求")
    for num_concurrent in [1, 2, 4, 8, 16]:
        result = test_concurrent_requests(model, tokenizer, test_prompt, num_concurrent, 100)
        key = f"concurrent_{num_concurrent}"
        results["tests"][key] = result
        print(f"  并发{num_concurrent}: 吞吐量={result['throughput']:.2f} tokens/s, "
              f"平均延迟={result['avg_latency']:.2f}s, P99={result['p99_latency']:.2f}s")

    # 测试4: 显存测试
    print("\n[测试4] 显存占用")
    mem_allocated = torch.cuda.memory_allocated(gpu_id) / 1024**3
    mem_reserved = torch.cuda.memory_reserved(gpu_id) / 1024**3
    mem_max = torch.cuda.max_memory_allocated(gpu_id) / 1024**3
    results["tests"]["memory"] = {
        "allocated_gb": mem_allocated,
        "reserved_gb": mem_reserved,
        "max_allocated_gb": mem_max
    }
    print(f"  当前占用: {mem_allocated:.2f} GB")
    print(f"  峰值占用: {mem_max:.2f} GB")

    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到: {output_file}")

    return results

if __name__ == "__main__":
    import sys

    print("="*60)
    print("大模型性能测试")
    print("="*60)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, help='模型路径')
    parser.add_argument('--name', type=str, required=True, help='模型名称')
    parser.add_argument('--gpu', type=int, default=0, help='GPU ID')
    parser.add_argument('--output', type=str, required=True, help='输出文件路径')
    args = parser.parse_args()

    run_tests(args.model, args.name, args.gpu, args.output)