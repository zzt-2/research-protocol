"""PROMPT-031 (方向 2): CMA + H1 组合 — CMA 在线均衡 + fixed-label BER 判 swap 后翻标签

> 方向: S032 机制 H (接受 swap 让它无害) / CMA+H1 组合 | 状态: WIP
> 来源: S033 §F 方法层下一步方向 2（执行 agent D039 只测了 ML+H1，CMA+H1 未测）
> 组织规范: ../../SIM-ORG.md

===========================================================================
 TL;DR / 物理假设 (TL-20 理论先行)
===========================================================================
S033 不变量 9 坐实：swap 是 SOP 累积旋转的物理现象，CMA 和 ML 都 100% swap
（D022 域 N=5M/SOP=4e-7 late [4.375M,5M)）。执行 agent D039 只测了 ML+H1：
ML fixed-weight late 5/5 clean-swap，翻标签 fixed BER 0.4996→8.9e-5（5591×），
但这等于 PI-BER（D018 已证），trivial。

【CMA+H1 是独立方法】：
  - CMA 在线均衡（在线跟 SOP，不是固定权重）
  - late 段 CMA 也 swap（S033 Phase 1 新域 4.2/1.4 CMA 10/10 swap fixed_ber=0.488）
  - 若用 fixed-label BER 判 swap（不变量 10：PI-BER 失明，fixed 才是真记分牌）
    → 检测 swap → 翻转 X/Y 标签 → 重算 BER
  - 这是"CMA 在线均衡 + 事后检测翻转"的组合，可能是独立有效方法

【为什么 CMA+H1 ≠ ML+H1 trivial】：
  - ML fixed-weight + H1 = PI-BER（D018/D039 已证）—— 因为 ML 推理输出本身就
    swap 完成的，翻标签只是选最优排列，等于排列不变口径
  - CMA 在线 + H1 ≠ PI-BER —— CMA 在线更新，输出随 SOP 持续演化，fixed-label
    的 0.5 来自 swap 锁定，翻标签是把"CMA 锁错"在 post-hoc 翻回，机制不同于
    "选最优排列"
  - 但物理上两者结果可能相近（都是翻标签救 0.5），须 MVE 实证

PASS 标准 (预注册, 用 fixed-label BER 作 Go 判据 — 不变量 10):
  - CMA+H1 late fixed-label BER 显著优于纯 CMA late fixed-label BER
    （0.488 → 接近 oracle 或至少 < 0.1）
  - 翻标签在 clean_swap 上有效（D039 已证 ML 上有效，CMA 待证）

FAIL 标准:
  - CMA+H1 fixed BER ≈ 纯 CMA fixed BER（翻标签对 CMA 无效）
  - 或 CMA+H1 fixed BER 改善但仍在高位（如 0.2，只 degraded_swap 部分救回）

===========================================================================
 约束 (硬约束)
===========================================================================
1. strong GG = 4.2/1.4（D022 域，params.py 当前正确值）。不硬编码旧 1.5/0.8。
2. swap 分类用 correlation 口径（prompt030 classify_swap，threshold=0.5）。
   不用 divergence trigger 口径（S033 §F 已证在 SOP=4e-7 失灵）。
3. Go 判据用 fixed-label BER（不变量 10：PI-BER 对 swap 失明）。但 fixed/PI 双口径并报（守 D018）。
4. 隔离原则：不改 common/，不改 ml_long_seq_failure.py，不改 prompt030。

===========================================================================
 实验设计
===========================================================================
参数域: N=5M, strong (4.2/1.4 动态读), F_G=30, SOP=4e-7, 20dB, QPSK
late [4.375M,5M), seeds 1000-1004（D022 域，与 prompt024/029/030 一致）

四方法同信道对比：
  (A) CMA-only:        StandardCMA2x2 在线均衡全段 → late fixed/PI BER
  (B) CMA+H1:          (A) 输出 → late classify_swap → 若 swap 则翻 zX↔zY + 4 旋转校正
  (C) oracle:          完美 CSI 下界
  (D) ML+H1:           对照（D039 已测，复跑确认 5591× 恢复，验证基建一致）

度量: fixed BER, PI BER, swap 分类, 翻标签后 fixed BER（flip_ber）
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

from common._config import BLOCK
from common._cma import CMAEqualizer2x2
from common._experiment import save_results
from ml_long_seq_failure import (
    F_G, GAMMA_BAR, N_TAP, MU_SAFE, R2_QPSK, SOP_RATE,
    compute_ber_phase_corrected, gen_qpsk, oracle_equalize,
    run_ml_trial, test_late_slice,
)
from params import SimulationConfig
from prompt030_domain_swap_audit import classify_swap, gen_channel, cma_equalize


N_SYMBOLS = 5_000_000
LATE_START, LATE_END = test_late_slice(N_SYMBOLS)
CMA_BLOCK_SIZE = 64
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt031_cma_h1_combo.json"
)

cfg = SimulationConfig()


def flip_labels(zX, zY, sX, sY, swapped):
    """H1: 若 swapped 则翻 zX↔zY 后算 BER（+ 4 旋转校正）。

    返回 (flip_ber, flipped): flip_ber 是翻转后的 BER；flipped=True/False。
    """
    if swapped:
        # 翻标签：zX 解 sY, zY 解 sX
        ber = min(
            compute_ber_phase_corrected(zX, sY),
            compute_ber_phase_corrected(zY, sX),
        )
        # 取两路最小（单流口径，等价 D039 flip_ber）
        mean_flip = 0.5 * (
            compute_ber_phase_corrected(zX, sY)
            + compute_ber_phase_corrected(zY, sX)
        )
        return float(mean_flip), True
    # 未 swap：正常算
    return float(0.5 * (
        compute_ber_phase_corrected(zX, sX)
        + compute_ber_phase_corrected(zY, sY)
    )), False


def run_trial(seed):
    """单 seed 四方法对比。返回 dict。"""
    turb = cfg.turbulence.as_dict()
    alpha, beta = turb["strong"]
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)

    sXl = sX[LATE_START:LATE_END]
    sYl = sY[LATE_START:LATE_END]
    h_l = h[LATE_START:LATE_END]
    th_l = theta[LATE_START:LATE_END]

    out = {'seed': seed, 'alpha': alpha, 'beta': beta}

    # (A) CMA-only + (B) CMA+H1
    # 用 prompt030 的 cma_equalize（common/_cma.py CMAEqualizer2x2, 块级, 与 S033 一致）
    zX_c_full, zY_c_full, _cma_div = cma_equalize(rX, rY, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    zX_c = zX_c_full[LATE_START:LATE_END]
    zY_c = zY_c_full[LATE_START:LATE_END]
    cls_c = classify_swap(zX_c, zY_c, sXl, sYl, threshold=0.5)
    fixed_c = float(0.5 * (
        compute_ber_phase_corrected(zX_c, sXl)
        + compute_ber_phase_corrected(zY_c, sYl)
    ))
    pi_c = float(min(
        compute_ber_phase_corrected(zX_c, sXl),
        compute_ber_phase_corrected(zX_c, sYl),
    ))
    # CMA+H1：判 swap → 翻标签
    is_swap = cls_c in ('clean_swap', 'degraded_swap')
    flip_ber_c, flipped_c = flip_labels(zX_c, zY_c, sXl, sYl, is_swap)
    out['cma'] = {
        'fixed_ber': fixed_c,
        'pi_ber': pi_c,
        'swap_class': cls_c,
        'flip_ber': flip_ber_c,
        'flipped': flipped_c,
    }

    # (C) oracle
    zX_or, zY_or = oracle_equalize(
        rX[LATE_START:LATE_END], rY[LATE_START:LATE_END], h_l, th_l, GAMMA_BAR)
    out['oracle'] = {
        'fixed_ber': float(0.5 * (
            compute_ber_phase_corrected(zX_or, sXl)
            + compute_ber_phase_corrected(zY_or, sYl)
        )),
    }

    # (D) ML+H1（对照，验证 D039 5591× 恢复）
    zX_ml_full, zY_ml_full, _, _ = run_ml_trial(rX, rY, sX, sY)
    zX_m = zX_ml_full[LATE_START:LATE_END]
    zY_m = zY_ml_full[LATE_START:LATE_END]
    cls_m = classify_swap(zX_m, zY_m, sXl, sYl, threshold=0.5)
    fixed_m = float(0.5 * (
        compute_ber_phase_corrected(zX_m, sXl)
        + compute_ber_phase_corrected(zY_m, sYl)
    ))
    pi_m = float(min(
        compute_ber_phase_corrected(zX_m, sXl),
        compute_ber_phase_corrected(zX_m, sYl),
    ))
    is_swap_m = cls_m in ('clean_swap', 'degraded_swap')
    flip_ber_m, flipped_m = flip_labels(zX_m, zY_m, sXl, sYl, is_swap_m)
    out['ml_h1'] = {
        'fixed_ber': fixed_m,
        'pi_ber': pi_m,
        'swap_class': cls_m,
        'flip_ber': flip_ber_m,
        'flipped': flipped_m,
    }

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--seeds', default='5')
    args = ap.parse_args()

    seeds = SEEDS_5 if args.seeds == '5' else list(range(1000, 1000 + int(args.seeds)))
    if args.smoke:
        seeds = [1000]

    t0 = time.time()
    trials = []
    for sd in seeds:
        print(f"  seed={sd} ...", flush=True)
        t1 = time.time()
        tr = run_trial(sd)
        tr['runtime_s'] = round(time.time() - t1, 1)
        trials.append(tr)
        print(
            f"    CMA: fixed={tr['cma']['fixed_ber']:.4f} swap={tr['cma']['swap_class']} "
            f"flip={tr['cma']['flip_ber']:.4e} | "
            f"ML+H1: fixed={tr['ml_h1']['fixed_ber']:.4f} swap={tr['ml_h1']['swap_class']} "
            f"flip={tr['ml_h1']['flip_ber']:.4e} | "
            f"oracle={tr['oracle']['fixed_ber']:.4e}",
            flush=True,
        )

    summary = {
        'cma_only': {
            'mean_fixed_ber': float(np.mean([t['cma']['fixed_ber'] for t in trials])),
            'mean_pi_ber': float(np.mean([t['cma']['pi_ber'] for t in trials])),
            'swap_dist': {c: sum(1 for t in trials if t['cma']['swap_class'] == c)
                          for c in ['clean', 'normal', 'clean_swap', 'degraded_swap', 'degraded', 'mixed']},
        },
        'cma_h1': {
            'mean_flip_ber': float(np.mean([t['cma']['flip_ber'] for t in trials])),
            'mean_fixed_ber': float(np.mean([t['cma']['fixed_ber'] for t in trials])),
            'n_flipped': sum(1 for t in trials if t['cma']['flipped']),
        },
        'ml_h1': {
            'mean_flip_ber': float(np.mean([t['ml_h1']['flip_ber'] for t in trials])),
            'mean_fixed_ber': float(np.mean([t['ml_h1']['fixed_ber'] for t in trials])),
            'swap_dist': {c: sum(1 for t in trials if t['ml_h1']['swap_class'] == c)
                          for c in ['clean', 'normal', 'clean_swap', 'degraded_swap', 'degraded', 'mixed']},
        },
        'oracle': {
            'mean_fixed_ber': float(np.mean([t['oracle']['fixed_ber'] for t in trials])),
        },
    }

    # Go/Kill 判定（预注册）
    cma_only_fixed = summary['cma_only']['mean_fixed_ber']
    cma_h1_flip = summary['cma_h1']['mean_flip_ber']
    improvement = cma_only_fixed / max(cma_h1_flip, 1e-12)
    summary['go_kill'] = {
        'cma_h1_vs_cma_only_improvement': float(improvement),
        'verdict': 'PASS' if cma_h1_flip < 0.1 and improvement > 10 else 'FAIL',
        'criterion': 'CMA+H1 fixed<0.1 且 改善>10×',
    }

    result = {
        'experiment': 'PROMPT-031 方向2 CMA+H1 combo (CMA 在线 + fixed-label 判 swap 翻标签)',
        'hypothesis': 'CMA 在线均衡也 swap; fixed-label BER 判 swap 后翻标签可能救回 (区别于 ML+H1=PI-BER trivial)',
        'invariants': [
            'swap 是 SOP 物理现象 CMA/ML 都 swap (S033 不变量 9)',
            'PI-BER 失明 fixed-label 是真记分牌 (不变量 10)',
            'swap 分类用 correlation 口径 (不用 divergence trigger)',
        ],
        'params': {
            'N': N_SYMBOLS, 'alpha': 'dynamic params.py strong (4.2/1.4)',
            'f_G': F_G, 'sop_rate': SOP_RATE, 'gamma_bar': GAMMA_BAR,
            'late_slice': [LATE_START, LATE_END], 'seeds': seeds,
        },
        'pass_criterion': 'CMA+H1 flip_ber < 0.1 且 改善 > 10× vs CMA-only fixed',
        'fail_criterion': 'CMA+H1 flip_ber ≈ CMA-only fixed (翻标签对 CMA 无效)',
        'summary': summary,
        'trials': trials,
        'total_runtime_s': round(time.time() - t0, 1),
    }
    save_results(result, RESULT_PATH, script_name="prompt031_cma_h1_combo")

    print("\n" + "=" * 80)
    print("CMA+H1 组合 — late [4.375M,5M) 四方法对比")
    print("=" * 80)
    print(f"{'方法':<12} | {'fixed BER':>12} | {'flip BER':>12} | 备注")
    print("-" * 80)
    print(f"{'CMA-only':<12} | {summary['cma_only']['mean_fixed_ber']:>12.4e} | {'--':>12} | "
          f"swap={summary['cma_only']['swap_dist']}")
    print(f"{'CMA+H1':<12} | {summary['cma_h1']['mean_fixed_ber']:>12.4e} | "
          f"{summary['cma_h1']['mean_flip_ber']:>12.4e} | "
          f"flipped {summary['cma_h1']['n_flipped']}/{len(trials)}")
    print(f"{'ML+H1':<12} | {summary['ml_h1']['mean_fixed_ber']:>12.4e} | "
          f"{summary['ml_h1']['mean_flip_ber']:>12.4e} | "
          f"swap={summary['ml_h1']['swap_dist']}")
    print(f"{'oracle':<12} | {summary['oracle']['mean_fixed_ber']:>12.4e} | {'--':>12} | CSI 下界")
    print("-" * 80)
    print(f"判定: {summary['go_kill']['verdict']} "
          f"(改善 {summary['go_kill']['cma_h1_vs_cma_only_improvement']:.1f}×)")
    print("=" * 80)
    print(f"结果: {RESULT_PATH} | 总耗时: {result['total_runtime_s']}s")


if __name__ == "__main__":
    main()
