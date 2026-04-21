#!/usr/bin/env python3
"""
大模型基准能力测试脚本
测试模型的知识问答、推理、数学、语言理解、阅读理解、代码生成能力
支持MoE架构模型的fallback模式
"""
import os
os.environ['USE_GROUPED_MM'] = '0'

import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers.integrations.moe as moe_module

# 修补grouped_mm
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
    return model, tokenizer

def generate_answer(model, tokenizer, prompt, max_tokens=200):
    """生成答案"""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=max_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False
        )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    answer = output_text[len(tokenizer.decode(input_ids[0], skip_special_tokens=True)):].strip()
    return answer

def test_knowledge(model, tokenizer):
    """测试知识问答能力"""
    questions = [
        "中国的首都是哪里？",
        "太阳系有几颗行星？",
        "水的化学式是什么？",
        "谁发明了电话？",
        "地球到月亮的距离大约是多少公里？",
    ]
    answers = []
    for q in questions:
        prompt = f"问：{q}\n答："
        answer = generate_answer(model, tokenizer, prompt, 100)
        answers.append({"question": q, "answer": answer})
    return answers

def test_reasoning(model, tokenizer):
    """测试推理能力"""
    questions = [
        "如果所有的猫都是动物，有些动物是黑色的，那么是否可以推断出有些猫是黑色的？请解释你的推理过程。",
        "小明有5个苹果，小红给了他3个，小明吃掉了2个，请问小明还剩多少个苹果？",
        "下列数列的下一个数字是什么：2, 4, 8, 16, ?",
    ]
    answers = []
    for q in questions:
        prompt = f"请解答以下问题：{q}\n答案："
        answer = generate_answer(model, tokenizer, prompt, 150)
        answers.append({"question": q, "answer": answer})
    return answers

def test_math(model, tokenizer):
    """测试数学能力"""
    problems = [
        "计算：123 + 456 = ?",
        "计算：789 - 234 = ?",
        "计算：12 × 14 = ?",
        "计算：156 ÷ 12 = ?",
        "一个长方形的长是10cm，宽是5cm，请问它的面积是多少？",
    ]
    answers = []
    for p in problems:
        prompt = f"请计算：{p}\n答案："
        answer = generate_answer(model, tokenizer, prompt, 100)
        answers.append({"problem": p, "answer": answer})
    return answers

def test_language_understanding(model, tokenizer):
    """测试语言理解能力"""
    tests = [
        ("请找出下列句子的主语和谓语：我正在学习人工智能。", "找出主语和谓语"),
        ("请把以下句子改成过去式：I eat an apple every day.", "改成过去式"),
        ("请解释这个句子的意思：The early bird catches the worm.", "解释句子意思"),
    ]
    results = []
    for prompt, task in tests:
        full_prompt = f"任务：{task}\n输入：{prompt}\n输出："
        answer = generate_answer(model, tokenizer, full_prompt, 100)
        results.append({"task": task, "answer": answer})
    return results

def test_reading_comprehension(model, tokenizer):
    """测试阅读理解能力"""
    passages = [
        {
            "passage": "人工智能是计算机科学的一个分支，致力于开发能够执行通常需要人类智能的任务的系统。这包括视觉感知、语音识别、决策制定和语言翻译等。",
            "question": "人工智能主要致力于开发什么？"
        },
        {
            "passage": "昨天小明去图书馆看书，他借了一本关于科学的书。今天他把书还给了图书馆。",
            "question": "小明昨天做了什么？"
        },
    ]
    results = []
    for item in passages:
        prompt = f"阅读以下段落：{item['passage']}\n问题：{item['question']}\n请根据段落回答问题："
        answer = generate_answer(model, tokenizer, prompt, 100)
        results.append({"question": item['question'], "answer": answer})
    return results

def test_code_generation(model, tokenizer):
    """测试代码生成能力"""
    tasks = [
        "请用Python写一个函数，计算一个列表的平均值。",
        "请用Python写一个函数，判断一个数是否为质数。",
    ]
    results = []
    for task in tasks:
        prompt = f"{task}\n请提供代码："
        answer = generate_answer(model, tokenizer, prompt, 200)
        results.append({"task": task, "code": answer})
    return results

def run_all_tests(model_path, model_name, gpu_id, output_file):
    """运行所有测试"""
    results = {
        "model": model_name,
        "model_path": model_path,
        "tests": {}
    }

    model, tokenizer = load_model(model_path, gpu_id)

    print("\n" + "="*60)
    print(f"开始测试模型: {model_name}")
    print("="*60)

    print("\n[测试1] 知识问答")
    results["tests"]["knowledge"] = test_knowledge(model, tokenizer)
    print("  完成")

    print("\n[测试2] 逻辑推理")
    results["tests"]["reasoning"] = test_reasoning(model, tokenizer)
    print("  完成")

    print("\n[测试3] 数学计算")
    results["tests"]["math"] = test_math(model, tokenizer)
    print("  完成")

    print("\n[测试4] 语言理解")
    results["tests"]["language"] = test_language_understanding(model, tokenizer)
    print("  完成")

    print("\n[测试5] 阅读理解")
    results["tests"]["reading"] = test_reading_comprehension(model, tokenizer)
    print("  完成")

    print("\n[测试6] 代码生成")
    results["tests"]["code"] = test_code_generation(model, tokenizer)
    print("  完成")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: {output_file}")
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--name', type=str, default='model')
    parser.add_argument('--gpu', type=int, default=0)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()

    run_all_tests(args.model, args.name, args.gpu, args.output)