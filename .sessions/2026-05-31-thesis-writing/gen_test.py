#!/usr/bin/env python3
"""§1.2 Generation Test — 2×2×2 Full Factorial Experiment

Tests quality dimensions D4(问题前置), D2(递进评价), D1(落脚句) via controlled generation.
Uses llm.py (DeepSeek) for generation, pattern-based metrics for objective measurement.

Design:
  2×2×2 factorial (D4 × D2 × D1) × 3 rounds = 24 generations
  Pattern-based metrics (not LLM-judged) + human eval template
"""

import sys
import json
import re
import random
import time
from pathlib import Path
from itertools import product

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "workflows" / "shared"))
from llm import call_llm

OUTPUT_DIR = Path(__file__).resolve().parent / "gen-test-output"

# --- Source material (constant across all variants) ---
SOURCE_MATERIAL = """\
传统方法（基于导频辅助）：
- LS估计器：结构简单，无需信道先验知识。局限：低信噪比下噪声放大严重。
  在20dB平均信噪比下，NMSE为-19.6至-17.0 dB。引用：lixueliang2018
- MMSE估计器：利用信道二阶统计量抑制噪声，精度最优。
  局限：性能严重依赖信道统计先验知识的准确性。
- Kalman滤波：通过自回归(AR)模型跟踪信道时变特性，适合湍流信道慢衰落。
  局限：模型阶数选择直接影响跟踪性能。
- 共同局限：需要导频序列，导频开销5%-10%，SNR损失0.5-1dB。

深度学习方法：
- Amirabadi(2020)：神经网络无导频估计，弱湍流下仅差1.5-2dB。
- Elfiky/Rezzi(2024)：双输入NN，MSE≈MMSE，复杂度降15%。
- Mohammed(2026)：CNN+BiLSTM，强湍流下稳定。
- 泛化性边界：SNR>23dB时部分DL方法性能退化。

核心空白：NMSE→下游模块性能级联关系未建立，缺乏面向系统级性能的指导准则。
"""

BASE_PROMPT = """\
你是一个学术写作助手。请根据以下研究素材，撰写约400-500字的文献综述片段，主题为"大气湍流信道估计研究现状"。

## 研究素材
{source}

## 写作要求
1. 用规范学术中文，面向硕士学位论文绪论文献综述
2. 覆盖传统方法(LS/MMSE/Kalman)和深度学习方法
3. 最后1-2句指出研究空白
4. 不需要引出本文工作
5. 不出现具体公式
6. 引用标记用[@key]格式
{dimension_instructions}
请直接输出综述文本，不要加标题、不要加说明。"""

# --- Dimension instruction snippets (independent variables) ---
DIM_SNIPPETS = {
    "D4": """\

## 关键风格指令（问题前置）
在介绍每个方法之前，先指出当时面临的具体问题或现有方法的局限，再引出新方法如何针对这些问题提出改进。按"问题→方案"逻辑组织，不按时间线罗列。""",

    "D2": """\

## 关键风格指令（递进评价）
使用递进评价模式：每个新方法都是在解决前一个方法遗留的问题。格式如"A实现了X但受限于Y，B改进了Y但引入了Z"。每3-5篇文献后有一句综合评价。""",

    "D1": """\

## 关键风格指令（落脚句）
每个主题段落末尾用1-2句话衔接本文研究方向或指出该方向的研究空白，说明该方向与后续工作的关系。""",
}

# --- 2×2×2 Factorial Design ---
FACTORS = ["D4", "D2", "D1"]
CONDITIONS = list(product([False, True], repeat=len(FACTORS)))
ROUNDS = 3

def condition_label(d4: bool, d2: bool, d1: bool) -> str:
    parts = []
    if d4: parts.append("D4")
    if d2: parts.append("D2")
    if d1: parts.append("D1")
    return "+".join(parts) if parts else "baseline"

# --- Objective pattern-based metrics ---
def measure_patterns(text: str) -> dict:
    """Count objective structural patterns — NOT LLM-judged quality."""
    m = {}

    # D4 markers: problem-driven transitions (causal "to solve X" patterns)
    m['d4_causal_trans'] = len(re.findall(r'为[了解决抑制突破缓解应对克服]', text))
    m['d4_problem_words'] = len(re.findall(r'局限|瓶颈|不足|缺陷|困难|挑战', text))

    # D2 markers: progressive evaluation ("A but B" chains)
    m['d2_contrast_eval'] = len(re.findall(r'但.*?(?:引入|带来|存在|面临|暴露)', text))
    m['d2_progressive'] = len(re.findall(r'进一步|进而|为此|针对.*?(?:问题|局限|不足)', text))
    m['d2_summary_eval'] = len(re.findall(r'综合|总体|总体而言|综上|然而.*?也|不仅.*?还', text))

    # D1 markers: landing/transition sentences
    m['d1_landing'] = len(re.findall(r'本文|本研究|后续|仍需|有待|尚需|亟待', text))

    # Structural metrics
    m['total_chars'] = len(text)
    m['paragraphs'] = len([p for p in text.split('\n\n') if p.strip()])
    m['sentences'] = len(re.findall(r'[。！？]', text))

    # Composite scores
    m['d4_score'] = m['d4_causal_trans'] + m['d4_problem_words']
    m['d2_score'] = m['d2_contrast_eval'] + m['d2_progressive'] + m['d2_summary_eval']
    m['d1_score'] = m['d1_landing']

    return m

def generate(condition: tuple[bool, ...], round_num: int) -> str:
    """Generate one sample with controlled dimension instructions."""
    dims = [FACTORS[i] for i, present in enumerate(condition) if present]
    dim_text = "\n".join(DIM_SNIPPETS[d] for d in dims) if dims else ""
    prompt = BASE_PROMPT.format(source=SOURCE_MATERIAL, dimension_instructions=dim_text)

    return call_llm(prompt=prompt, system="你是学术写作助手。",
                     max_tokens=2048, temperature=0.7)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    random.seed(42)

    all_outputs = {}  # {label: [round0, round1, round2]}
    all_metrics = {}

    total = len(CONDITIONS) * ROUNDS
    done = 0

    print(f"=== 2×2×2 Factorial Generation Test ({len(CONDITIONS)} conditions × {ROUNDS} rounds = {total} samples) ===\n")

    # Phase 1: Generate
    for condition in CONDITIONS:
        label = condition_label(*condition)
        all_outputs[label] = []
        all_metrics[label] = []

        for r in range(ROUNDS):
            done += 1
            print(f"  [{done}/{total}] {label} round {r}...", end=" ", flush=True)
            try:
                output = generate(condition, r)
                all_outputs[label].append(output)

                metrics = measure_patterns(output)
                metrics['round'] = r
                all_metrics[label].append(metrics)

                # Save individual output
                (OUTPUT_DIR / f"{label}_r{r}.md").write_text(output, encoding='utf-8')

                print(f"OK ({metrics['total_chars']} chars, d4={metrics['d4_score']}, d2={metrics['d2_score']}, d1={metrics['d1_score']})")
            except Exception as e:
                print(f"FAILED: {e}")
                all_outputs[label].append("")
                all_metrics[label].append({'round': r, 'total_chars': 0, 'error': str(e)})

            time.sleep(0.5)

    # Phase 2: Aggregate metrics
    print(f"\n=== Aggregate Metrics (avg across {ROUNDS} rounds) ===\n")

    header = f"{'Condition':<20} {'Chars':>6} {'Sents':>5} {'Paras':>5} {'D4_score':>8} {'D2_score':>8} {'D1_score':>8} {'d4_causal':>9} {'d2_contrast':>11} {'d2_prog':>7} {'d1_land':>7}"
    print(header)
    print("-" * len(header))

    agg = {}
    for condition in CONDITIONS:
        label = condition_label(*condition)
        metrics_list = all_metrics.get(label, [])
        if not metrics_list or 'error' in metrics_list[0]:
            continue

        avg = {}
        numeric_keys = [k for k in metrics_list[0] if k != 'round' and k != 'error'
                        and isinstance(metrics_list[0][k], (int, float))]
        for k in numeric_keys:
            avg[k] = sum(m.get(k, 0) for m in metrics_list) / len(metrics_list)

        agg[label] = avg
        print(f"{label:<20} {avg['total_chars']:>6.0f} {avg['sentences']:>5.1f} {avg['paragraphs']:>5.1f} "
              f"{avg['d4_score']:>8.1f} {avg['d2_score']:>8.1f} {avg['d1_score']:>8.1f} "
              f"{avg['d4_causal_trans']:>9.1f} {avg['d2_contrast_eval']:>11.1f} "
              f"{avg['d2_progressive']:>7.1f} {avg['d1_landing']:>7.1f}")

    # Phase 3: Factorial analysis (main effects)
    print(f"\n=== Main Effects Analysis ===\n")

    for fi, factor in enumerate(FACTORS):
        present_scores = []
        absent_scores = []
        for condition in CONDITIONS:
            label = condition_label(*condition)
            if label not in agg:
                continue
            if condition[fi]:  # factor present
                present_scores.append(agg[label])
            else:
                absent_scores.append(agg[label])

        if not present_scores or not absent_scores:
            continue

        print(f"--- {factor} Main Effect ---")
        for metric in ['d4_score', 'd2_score', 'd1_score', 'total_chars']:
            p_avg = sum(s[metric] for s in present_scores) / len(present_scores)
            a_avg = sum(s[metric] for s in absent_scores) / len(absent_scores)
            delta = p_avg - a_avg
            direction = "↑" if delta > 0 else "↓" if delta < 0 else "="
            print(f"  {metric:>12}: present={p_avg:.1f}  absent={a_avg:.1f}  Δ={delta:+.1f} {direction}")
        print()

    # Phase 4: Human eval template
    samples_for_eval = []
    for condition in CONDITIONS:
        label = condition_label(*condition)
        for r in range(ROUNDS):
            if all_outputs.get(label) and all_outputs[label][r]:
                samples_for_eval.append((label, r, all_outputs[label][r]))

    random.shuffle(samples_for_eval)

    mapping = {}
    eval_lines = ["# §1.2 Generation Test — Human Evaluation\n"]
    eval_lines.append("## Scoring Template\n")
    eval_lines.append("Score each sample 1-5 on: logical progression, evaluation depth, problem-driven, info density\n")
    eval_lines.append("| # | Score(1-5) | Comments |")
    eval_lines.append("|---|-----------|----------|")
    for idx, (label, r, _) in enumerate(samples_for_eval):
        sid = f"S{idx+1:02d}"
        mapping[sid] = f"{label}_r{r}"
        eval_lines.append(f"| {sid} | | |")
    eval_lines.append("")

    eval_lines.append("## Samples\n")
    for idx, (label, r, output) in enumerate(samples_for_eval):
        sid = f"S{idx+1:02d}"
        eval_lines.append(f"### {sid}\n")
        eval_lines.append(output)
        eval_lines.append("\n---\n")

    eval_lines.append("\n## Answer Key (reveal after scoring)\n```")
    for sid, real in mapping.items():
        eval_lines.append(f"  {sid} = {real}")
    eval_lines.append("```")

    (OUTPUT_DIR / "human-eval.md").write_text("\n".join(eval_lines), encoding='utf-8')

    # Save metrics JSON
    with open(OUTPUT_DIR / "metrics.json", 'w', encoding='utf-8') as f:
        json.dump({"conditions": agg, "raw_metrics": {k: v for k, v in all_metrics.items()},
                    "answer_key": mapping}, f, ensure_ascii=False, indent=2)

    print(f"\nFiles saved to {OUTPUT_DIR}/")
    print(f"  - metrics.json        (aggregate + raw metrics)")
    print(f"  - human-eval.md       ({len(samples_for_eval)} samples, randomized, blind)")
    print(f"  - *.md                (individual outputs)")


if __name__ == "__main__":
    main()
