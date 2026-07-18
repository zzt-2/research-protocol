"""PROMPT-029 (Tier 0 - H1): CRC 检测翻转标签 — swap 后翻 X/Y 能否恢复

> 方向: S032 机制 H / H1 | 状态: WIP | 创建: 2026-07-16, 修订: ML swap 目标
> 来源: S032 §F 执行图 Tier 0 (物理前提验证)
> 组织规范: ../../SIM-ORG.md

===========================================================================
 TL;DR / 物理假设 (TL-20 理论先行)
===========================================================================
S032 §C H1: "swap 永久锁定且可被 CRC 检测 → 翻 X/Y 标签 → BER 恢复". 开销≈0.

【关键事实校正 — 2026-07-16 smoke 后】
swap 在新参数域 strong=4.2/1.4 下:
  - CMA standard (在线跟踪): 5/5 clean, 0 swap (CMA 跟上 SOP, 见 smoke 结果)
  - ML fixed-weight (离线训练一次): late 段 clean-swap (D015/D018 铁证, fixed≈0.5)
→ swap 问题的真正载体 = ML fixed-weight (Q-CMA-FADE 方法层目标).
→ H1/B2 必须在 ML fixed-weight 输出上测, 不是 CMA.

D018/D028: N=5M ML late 是 clean-swap (10/10, fixed≈0.5, PI≈0.005). clean-swap 时
zX 主要含 sY, zY 主要含 sX → 翻标签应把 BER 从 0.5 恢复到 PI 量级 (~0.005).

PASS: clean-swap seeds 翻标签 BER ≈ PI-BER ≈ oracle (从 0.5 降到 ~0.005)
FAIL: 翻标签 BER 仍 ~0.5 (swap 伴随相位/权重偏移, 单翻标签不够) 或 degraded 占比高

===========================================================================
 约束 (硬约束)
===========================================================================
1. strong GG = 4.2/1.4 (params.py 当前正确值). 不硬编码旧 1.5/0.8.
2. fixed-label BER 是 swap 真记分牌 (PI-BER 失明).
3. 隔离原则: 不改 common/, 不改 ml_long_seq_failure.py.
4. swap 目标 = ML fixed-weight late 输出 (复用 run_ml_trial, D022 域).

===========================================================================
 实验设计
===========================================================================
参数域 (D022 注册域):
  N = 5M, TURBULENCE=strong (4.2/1.4 动态读 params.py), F_G=30, SOP=4e-7, 20dB
  late slice [4.375M, 5M), seeds 1000-1004
  ML: run_ml_trial (前 50% 训练, 全段推理, 复用 D022 L0 路径)

对照 (per seed):
  - fixed BER (zX→sX, zY→sY)     [swap 真记分, clean-swap 时=0.5]
  - flip BER (zX→sY, zY→sX)      [H1 核心动作: 翻标签]
  - PI BER (2!×4×4 消歧最优)      [理论上界 = min(fixed, flip)]
  - oracle BER                    [perfect CSI 上界]
  - swap 分类 (clean/clean_swap/degraded)

block 级 swap 时序 (验证 D028 两阶段: 间歇期 + 永久锁定):
  - 永久锁定起始 block
  - 分段翻标签 BER (swap 前 vs swap 后)
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
from common._experiment import save_results
from ml_long_seq_failure import (
    F_G, GAMMA_BAR, SOP_RATE, compute_ber_phase_corrected,
    gen_channel, oracle_equalize, run_ml_trial, test_late_slice,
)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs, _abs_corr


N_SYMBOLS = 5_000_000
LATE_START, LATE_END = test_late_slice(N_SYMBOLS)   # [4.375M, 5M) for train_frac=0.5
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]
SWAP_DETECT_WINDOW = 500
SWAP_DETECT_STRIDE = 64

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt029_h1_crc_flip_label.json"
)

cfg = SimulationConfig()


def compute_block_corr_series(zX, zY, sX, sY,
                              window=SWAP_DETECT_WINDOW, stride=SWAP_DETECT_STRIDE):
    n = len(zX)
    starts = list(range(0, n - window + 1, stride)) or [0]
    series = []
    for s in starts:
        e = min(s + window, n)
        c_xx = _abs_corr(zX[s:e], sX[s:e])
        c_xy = _abs_corr(zX[s:e], sY[s:e])
        c_yy = _abs_corr(zY[s:e], sY[s:e])
        c_yx = _abs_corr(zY[s:e], sX[s:e])
        series.append({
            'start': s, 'end': e,
            'c_xx': c_xx, 'c_xy': c_xy, 'c_yy': c_yy, 'c_yx': c_yx,
            'is_swap': bool((c_xy > c_xx) and (c_yx > c_yy)),
        })
    return series


def detect_swap_phases(corr_series):
    n = len(corr_series)
    swap_flags = np.array([c['is_swap'] for c in corr_series])
    run_len = 0
    perm_lock_start = None
    for i, f in enumerate(swap_flags):
        if f:
            run_len += 1
            if run_len >= 1000 and perm_lock_start is None:
                perm_lock_start = i - 999
        else:
            run_len = 0
    if perm_lock_start is not None:
        n_int = int(swap_flags[:perm_lock_start].sum())
        frac_int = n_int / max(perm_lock_start, 1)
        frac_perm = (n - perm_lock_start) / n
    else:
        n_int = int(swap_flags.sum())
        frac_int = n_int / n
        frac_perm = 0.0
    return {
        'n_windows': n,
        'n_swap_windows': int(swap_flags.sum()),
        'frac_swap': float(swap_flags.mean()),
        'perm_lock_start_window': perm_lock_start,
        'n_intermittent_windows': n_int,
        'frac_intermittent': float(frac_int),
        'frac_perm_lock': float(frac_perm),
    }


def run_trial(seed):
    turb = cfg.turbulence.as_dict()
    alpha, beta = turb["strong"]    # 动态读 params.py (当前 4.2/1.4)
    rX, rY, sX, sY, h, theta = gen_channel(N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)

    # ML fixed-weight (D022 L0 路径, swap 真正载体)
    zX_ml, zY_ml, n_train, _ = run_ml_trial(rX, rY, sX, sY)

    zX_late = zX_ml[LATE_START:LATE_END]
    zY_late = zY_ml[LATE_START:LATE_END]
    sX_late = sX[LATE_START:LATE_END]
    sY_late = sY[LATE_START:LATE_END]
    h_late = h[LATE_START:LATE_END]
    theta_late = theta[LATE_START:LATE_END]
    rX_late = rX[LATE_START:LATE_END]
    rY_late = rY[LATE_START:LATE_END]

    res = evaluate_outputs(zX_late, zY_late, sX_late, sY_late, diverged=False)
    fixed_ber = float(res['fixed_label_ber']['mean'])
    pi_ber = float(res['permutation_invariant_ber']['mean'])

    # H1 核心: 翻标签 BER (zX→sY, zY→sX), 含 4 旋转校正
    flip_ber = float(np.mean([
        compute_ber_phase_corrected(zX_late, sY_late),
        compute_ber_phase_corrected(zY_late, sX_late),
    ]))

    c_xx = float(res['abs_corr']['zX_sX']); c_xy = float(res['abs_corr']['zX_sY'])
    c_yy = float(res['abs_corr']['zY_sY']); c_yx = float(res['abs_corr']['zY_sX'])
    if c_xx > c_xy and c_yy > c_yx:
        cls = 'clean'
    elif c_xy > c_xx and c_yx > c_yy:
        cls = 'clean_swap'
    else:
        cls = 'degraded'

    zX_or, zY_or = oracle_equalize(rX_late, rY_late, h_late, theta_late, GAMMA_BAR)
    res_or = evaluate_outputs(zX_or, zY_or, sX_late, sY_late, diverged=False)
    oracle_fixed = float(res_or['fixed_label_ber']['mean'])

    corr_series = compute_block_corr_series(zX_late, zY_late, sX_late, sY_late)
    swap_phases = detect_swap_phases(corr_series)

    # 分段: 永久锁定前 vs 后
    preswap_fixed = preswap_flip = swap_fixed = swap_flip = None
    pl_sym_range = None
    if swap_phases['perm_lock_start_window'] is not None:
        i0 = swap_phases['perm_lock_start_window']
        pl_s = corr_series[i0]['start']
        pl_e = corr_series[-1]['end']
        pl_sym_range = [pl_s, pl_e]
        if pl_e - pl_s > 100:
            zX_pre, zY_pre = zX_late[:pl_s], zY_late[:pl_s]
            sX_pre, sY_pre = sX_late[:pl_s], sY_late[:pl_s]
            zX_sw, zY_sw = zX_late[pl_s:pl_e], zY_late[pl_s:pl_e]
            sX_sw, sY_sw = sX_late[pl_s:pl_e], sY_late[pl_s:pl_e]
            preswap_fixed = float(np.mean([
                compute_ber_phase_corrected(zX_pre, sX_pre),
                compute_ber_phase_corrected(zY_pre, sY_pre)]))
            preswap_flip = float(np.mean([
                compute_ber_phase_corrected(zX_pre, sY_pre),
                compute_ber_phase_corrected(zY_pre, sX_pre)]))
            swap_fixed = float(np.mean([
                compute_ber_phase_corrected(zX_sw, sX_sw),
                compute_ber_phase_corrected(zY_sw, sY_sw)]))
            swap_flip = float(np.mean([
                compute_ber_phase_corrected(zX_sw, sY_sw),
                compute_ber_phase_corrected(zY_sw, sX_sw)]))

    return {
        'seed': seed, 'alpha': alpha, 'beta': beta,
        'fixed_ber': fixed_ber, 'flip_ber': flip_ber, 'pi_ber': pi_ber,
        'oracle_fixed': oracle_fixed, 'swap_class': cls,
        'corr_matrix': [[c_xx, c_xy], [c_yx, c_yy]],
        'swap_phases': swap_phases,
        'segmented': {
            'preswap_fixed': preswap_fixed, 'preswap_flip': preswap_flip,
            'swap_fixed': swap_fixed, 'swap_flip': swap_flip,
            'perm_lock_sym_range': pl_sym_range,
        },
    }


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
        print(f"    class={tr['swap_class']} fixed={tr['fixed_ber']:.4f} "
              f"flip={tr['flip_ber']:.4e} pi={tr['pi_ber']:.4e} "
              f"oracle={tr['oracle_fixed']:.4e}", flush=True)
        seg = tr['segmented']
        if seg['swap_fixed'] is not None:
            print(f"      preswap fixed={seg['preswap_fixed']:.4e} flip={seg['preswap_flip']:.4e} | "
                  f"swap fixed={seg['swap_fixed']:.4e} flip={seg['swap_flip']:.4e}", flush=True)

    clean_swap = [t for t in trials if t['swap_class'] == 'clean_swap']
    clean = [t for t in trials if t['swap_class'] == 'clean']
    degraded = [t for t in trials if t['swap_class'] == 'degraded']

    def agg(ts, key):
        return float(np.mean([t[key] for t in ts])) if ts else None

    summary = {
        'n_seeds': len(seeds),
        'class_dist': {'clean': len(clean), 'clean_swap': len(clean_swap), 'degraded': len(degraded)},
        'clean_swap_seeds': {
            'n': len(clean_swap),
            'mean_fixed_ber': agg(clean_swap, 'fixed_ber'),
            'mean_flip_ber': agg(clean_swap, 'flip_ber'),
            'mean_pi_ber': agg(clean_swap, 'pi_ber'),
            'mean_oracle_fixed': agg(clean_swap, 'oracle_fixed'),
            'flip_recovery_factor': (
                agg(clean_swap, 'fixed_ber') / agg(clean_swap, 'flip_ber')
                if clean_swap and agg(clean_swap, 'flip_ber') > 0 else None),
        },
        'clean_seeds': {
            'n': len(clean),
            'mean_fixed_ber': agg(clean, 'fixed_ber'),
            'mean_flip_ber': agg(clean, 'flip_ber'),
        },
    }

    result = {
        'experiment': 'PROMPT-029 Tier0-H1 CRC flip-label recovery (ML fixed-weight target)',
        'hypothesis': 'S032 §C H1: ML late clean-swap 后翻 X/Y 标签, BER 应从 0.5 恢复到 PI≈oracle',
        'key_correction': 'swap 载体 = ML fixed-weight late (D015/D018), 非 CMA. CMA 在 4.2/1.4 域 5/5 clean.',
        'params': {
            'N': N_SYMBOLS, 'alpha': 'dynamic params.py strong', 'beta': 'dynamic params.py strong',
            'f_G': F_G, 'sop_rate': SOP_RATE, 'gamma_bar': GAMMA_BAR,
            'late_slice': [LATE_START, LATE_END], 'seeds': seeds,
            'equalizer': 'ML fixed-weight (run_ml_trial, D022 L0 path)',
        },
        'pass_criterion': 'clean-swap seeds: flip_ber ≈ oracle (从 0.5 降到 oracle 量级)',
        'fail_criterion': 'flip_ber 仍高 (伴随相位/权重偏移) 或 degraded 占比高',
        'summary': summary, 'trials': trials,
        'total_runtime_s': round(time.time() - t0, 1),
    }
    save_results(result, RESULT_PATH, script_name="prompt029_h1_crc_flip_label")

    print("\n" + "=" * 70)
    print("H1 CRC 翻转标签 (ML fixed-weight 目标)")
    print("=" * 70)
    print(f"class 分布: clean={summary['class_dist']['clean']} "
          f"clean_swap={summary['class_dist']['clean_swap']} "
          f"degraded={summary['class_dist']['degraded']}")
    cs = summary['clean_swap_seeds']
    if cs['n'] > 0:
        print(f"\nclean-swap seeds (n={cs['n']}):")
        print(f"  fixed BER (无翻)  : {cs['mean_fixed_ber']:.4f}")
        print(f"  flip BER  (翻标签): {cs['mean_flip_ber']:.4e}")
        print(f"  oracle BER        : {cs['mean_oracle_fixed']:.4e}")
        print(f"  PI BER (对照)     : {cs['mean_pi_ber']:.4e}")
        if cs['flip_recovery_factor']:
            print(f"  翻标签恢复因子     : {cs['flip_recovery_factor']:.1f}× (fixed→flip)")
    print("=" * 70)
    print(f"结果: {RESULT_PATH} | 总耗时: {result['total_runtime_s']}s")


if __name__ == "__main__":
    main()
