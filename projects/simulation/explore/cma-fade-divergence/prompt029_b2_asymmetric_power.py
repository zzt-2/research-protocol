"""PROMPT-029 (Tier 0 - B2): 非对称功率分配 — swap 触发率 vs 功率比曲线

> 方向: S032 机制 B (内生不对称) / B2 治本候选 | 状态: WIP | 修订: 双均衡器目标
> 来源: S032 §F 执行图 Tier 0 (物理前提验证)
> 组织规范: ../../SIM-ORG.md

===========================================================================
 TL;DR / 物理假设 (TL-20 理论先行)
===========================================================================
S032 §C B2 核心洞察: "若两流不对称, CMA 恒模代价对'正确盆地'和'交换盆地'不再
等价 → swap 多解可能消失 (治本)". 绕开"盲方法注定 KILL"约束 (前提双流对称).

【关键事实校正 — 2026-07-16 H1 smoke 后】
新参数域 strong=4.2/1.4 下:
  - CMA standard (在线): 5/5 clean, 0 swap (CMA 跟上 SOP)
  - ML fixed-weight (离线): 5/5 clean-swap late (D015/D018 铁证, fixed≈0.5)
swap 载体 = ML fixed-weight. CMA 在本域不 swap.

B2 的两难 (必须诚实测, TL-22):
  1. B2 原理 (CMA 恒模盆地不再等价) 适用于 CMA, 但 CMA 在 4.2/1.4 域不 swap
     → B2 对 CMA 可能"治无病" (没 swap 可防), 也可能因单 R²=1.0 对非对称两流
     错配反而引发 swap
  2. ML swap 的根因是 SOP 泛化失败 (D015: 57° 累积旋转超训练域), 非恒模盆地模糊
     → B2 非对称功率对 ML 可能无效 (机制错配); 但也可能因训练时学到的功率差
     给 ML 一个可辨识特征帮助区分 X/Y, 须测

→ 本 MVE 双均衡器都测, 分别报告 (不预设哪个有效).

PASS 标准 (预注册):
  - ML: 非对称功率下 late clean-swap 触发率随 |功率比-1| 下降, 某档→0 且 fixed BER 接近 oracle
  - 或 CMA: 非对称功率下 swap 触发率下降 (虽然 CMA 对称时本就不 swap, 若非对称
    反而引发 swap 则 B2 对 CMA 负面)
FAIL 标准:
  - ML swap 触发率不随功率比变化 (ML swap 由 SOP 泛化驱动, 与功率对称性正交)
  - 非对称功率伤 BER (trade-off 不可接受, 功率失衡本身降 SNR)

===========================================================================
 约束 (硬约束)
===========================================================================
1. strong GG = 4.2/1.4 (params.py 当前正确值). 不硬编码旧 1.5/0.8.
2. fixed-label BER 是 swap 真记分牌 (PI-BER 失明).
3. 隔离原则: 不改 common/, 不改 ml_long_seq_failure.py.

===========================================================================
 实验设计
===========================================================================
参数域: N=5M, strong (4.2/1.4 动态读), F_G=30, SOP=4e-7, 20dB
late [4.375M,5M), seeds 1000-1004
功率比扫描: power_ratio = p_Y/p_X ∈ [0.25, 0.5, 1.0, 2.0, 4.0]
  (总功率归一 p_X^2+p_Y^2=2, 1.0 对称作 baseline)
均衡器: (a) ML fixed-weight (run_ml_trial, swap 真正载体)
        (b) CMA standard (对照, B2 原始机制适用对象)
度量: fixed BER, PI BER, swap 分类 (clean/clean_swap/degraded)
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
    F_G, GAMMA_BAR, N_TAP, MU_SAFE, R2_QPSK, SOP_RATE,
    compute_ber_phase_corrected, gen_qpsk, oracle_equalize,
    run_ml_trial, test_late_slice,
)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs, _abs_corr


N_SYMBOLS = 5_000_000
LATE_START, LATE_END = test_late_slice(N_SYMBOLS)
CMA_BLOCK_SIZE = 64
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]
POWER_RATIOS = [0.25, 0.5, 1.0, 2.0, 4.0]

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt029_b2_asymmetric_power.json"
)

cfg = SimulationConfig()


def gen_channel_asymmetric(N, alpha, beta, f_g, sop_rate, seed, power_ratio):
    """双偏振 GG + SOP 信道, 两流非对称功率 (B2). 总功率归一 p_X^2+p_Y^2=2."""
    from common._gg_time import gg_time_envelope
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=cfg.system.T_S,
                         method='gar', seed=seed)
    sX, _ = gen_qpsk(N, rng)
    sY, _ = gen_qpsk(N, rng)
    theta = sop_rate * np.arange(N)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    nv = 1.0 / (2 * GAMMA_BAR)
    p_Y = np.sqrt(2.0 * power_ratio**2 / (1.0 + power_ratio**2))
    p_X = np.sqrt(2.0 / (1.0 + power_ratio**2))
    rX = p_X * np.sqrt(h) * (cos_t * sX + sin_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY = p_Y * np.sqrt(h) * (-sin_t * sX + cos_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY, sX, sY, h, theta, (float(p_X), float(p_Y))


class StandardCMA2x2:
    """Standard complex CMA 2×2 (Godard 1980 含 z, D022 合法 baseline)."""
    def __init__(self, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK):
        self.n_tap = n_tap; self.mu = mu; self.R2 = R2
        c = n_tap // 2
        self.wxx = np.zeros(n_tap, dtype=complex); self.wxx[c] = 1.0
        self.wxy = np.zeros(n_tap, dtype=complex)
        self.wyx = np.zeros(n_tap, dtype=complex)
        self.wyy = np.zeros(n_tap, dtype=complex); self.wyy[c] = 1.0

    def equalize(self, rX, rY, block_size=CMA_BLOCK_SIZE):
        n = len(rX)
        zX = np.zeros(n, dtype=complex); zY = np.zeros(n, dtype=complex)
        pad = self.n_tap // 2
        for k in range(n):
            lo, hi = max(0, k - pad), min(n, k + pad + 1)
            rXs = np.zeros(self.n_tap, dtype=complex)
            rYs = np.zeros(self.n_tap, dtype=complex)
            rXs[:hi - lo] = rX[lo:hi]; rYs[:hi - lo] = rY[lo:hi]
            zXk = np.dot(self.wxx, rXs) + np.dot(self.wxy, rYs)
            zYk = np.dot(self.wyx, rXs) + np.dot(self.wyy, rYs)
            zX[k], zY[k] = zXk, zYk
            ex = self.R2 - abs(zXk)**2; ey = self.R2 - abs(zYk)**2
            self.wxx += self.mu * ex * zXk * np.conj(rXs)
            self.wxy += self.mu * ex * zXk * np.conj(rYs)
            self.wyx += self.mu * ey * zYk * np.conj(rXs)
            self.wyy += self.mu * ey * zYk * np.conj(rYs)
        return zX, zY


def classify(c_xx, c_xy, c_yy, c_yx):
    if c_xx > c_xy and c_yy > c_yx:
        return 'clean'
    if c_xy > c_xx and c_yx > c_yy:
        return 'clean_swap'
    return 'degraded'


def run_trial(power_ratio, seed):
    turb = cfg.turbulence.as_dict()
    alpha, beta = turb["strong"]
    rX, rY, sX, sY, h, theta, (pX, pY) = gen_channel_asymmetric(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed, power_ratio)

    out = {}
    # (a) ML fixed-weight
    zX_ml, zY_ml, _, _ = run_ml_trial(rX, rY, sX, sY)
    zXl, zYl = zX_ml[LATE_START:LATE_END], zY_ml[LATE_START:LATE_END]
    sXl, sYl = sX[LATE_START:LATE_END], sY[LATE_START:LATE_END]
    res = evaluate_outputs(zXl, zYl, sXl, sYl, diverged=False)
    c_xx = res['abs_corr']['zX_sX']; c_xy = res['abs_corr']['zX_sY']
    c_yy = res['abs_corr']['zY_sY']; c_yx = res['abs_corr']['zY_sX']
    out['ml'] = {
        'fixed_ber': float(res['fixed_label_ber']['mean']),
        'pi_ber': float(res['permutation_invariant_ber']['mean']),
        'swap_class': classify(c_xx, c_xy, c_yy, c_yx),
        'corr': [[c_xx, c_xy], [c_yx, c_yy]],
    }

    # (b) CMA standard
    cma = StandardCMA2x2()
    zX_c, zY_c = cma.equalize(rX, rY)
    zXl, zYl = zX_c[LATE_START:LATE_END], zY_c[LATE_START:LATE_END]
    res = evaluate_outputs(zXl, zYl, sXl, sYl, diverged=False)
    c_xx = res['abs_corr']['zX_sX']; c_xy = res['abs_corr']['zX_sY']
    c_yy = res['abs_corr']['zY_sY']; c_yx = res['abs_corr']['zY_sX']
    out['cma'] = {
        'fixed_ber': float(res['fixed_label_ber']['mean']),
        'pi_ber': float(res['permutation_invariant_ber']['mean']),
        'swap_class': classify(c_xx, c_xy, c_yy, c_yx),
        'corr': [[c_xx, c_xy], [c_yx, c_yy]],
    }

    # oracle (非对称功率信道)
    h_l = h[LATE_START:LATE_END]; th_l = theta[LATE_START:LATE_END]
    rX_l = rX[LATE_START:LATE_END]; rY_l = rY[LATE_START:LATE_END]
    zX_or, zY_or = oracle_equalize(rX_l, rY_l, h_l, th_l, GAMMA_BAR)
    res_or = evaluate_outputs(zX_or, zY_or, sXl, sYl, diverged=False)
    out['oracle'] = {
        'fixed_ber': float(res_or['fixed_label_ber']['mean']),
        'pi_ber': float(res_or['permutation_invariant_ber']['mean']),
    }

    out.update({'power_ratio': power_ratio, 'seed': seed, 'p_X': pX, 'p_Y': pY,
                'alpha': alpha, 'beta': beta})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--seeds', default='5')
    args = ap.parse_args()

    seeds = SEEDS_5 if args.seeds == '5' else list(range(1000, 1000 + int(args.seeds)))
    ratios = [1.0, 0.25, 4.0] if args.smoke else POWER_RATIOS

    t0 = time.time()
    trials = []
    for pr in ratios:
        for sd in seeds:
            print(f"  pr={pr} seed={sd} ...", flush=True)
            t1 = time.time()
            tr = run_trial(pr, sd)
            tr['runtime_s'] = round(time.time() - t1, 1)
            trials.append(tr)
            print(f"    ML: fixed={tr['ml']['fixed_ber']:.4f} swap={tr['ml']['swap_class']} | "
                  f"CMA: fixed={tr['cma']['fixed_ber']:.4f} swap={tr['cma']['swap_class']} | "
                  f"oracle_fixed={tr['oracle']['fixed_ber']:.4e}", flush=True)

    summary = {}
    for pr in ratios:
        tp = [t for t in trials if t['power_ratio'] == pr]
        for eq in ['ml', 'cma']:
            n_swap = sum(1 for t in tp if t[eq]['swap_class'] == 'clean_swap')
            summary.setdefault(str(pr), {})[eq] = {
                'n_seeds': len(tp),
                'mean_fixed_ber': float(np.mean([t[eq]['fixed_ber'] for t in tp])),
                'mean_pi_ber': float(np.mean([t[eq]['pi_ber'] for t in tp])),
                'swap_trigger_rate': n_swap / len(tp) if tp else 0.0,
                'swap_dist': {c: sum(1 for t in tp if t[eq]['swap_class'] == c)
                              for c in ['clean', 'clean_swap', 'degraded']},
            }
        summary[str(pr)]['mean_oracle_fixed'] = float(
            np.mean([t['oracle']['fixed_ber'] for t in tp]))

    result = {
        'experiment': 'PROMPT-029 Tier0-B2 asymmetric power (ML + CMA dual target)',
        'hypothesis': 'S032 §C B2: 非对称功率破坏 X/Y 对称 → swap 多解消失 (治本)',
        'key_correction': 'swap 载体=ML fixed-weight; CMA 在 4.2/1.4 域不 swap. 双均衡器都测.',
        'params': {
            'N': N_SYMBOLS, 'alpha': 'dynamic params.py strong (4.2/1.4)',
            'f_G': F_G, 'sop_rate': SOP_RATE, 'gamma_bar': GAMMA_BAR,
            'late_slice': [LATE_START, LATE_END], 'seeds': seeds,
            'power_ratios': ratios,
        },
        'pass_criterion': 'ML: swap 触发率随 |功率比-1| 下降且 fixed BER 接近 oracle',
        'fail_criterion': 'ML swap 触发率不随功率比变 (SOP 泛化驱动) 或非对称伤 BER',
        'summary_by_power_ratio': summary,
        'trials': trials,
        'total_runtime_s': round(time.time() - t0, 1),
    }
    save_results(result, RESULT_PATH, script_name="prompt029_b2_asymmetric_power")

    print("\n" + "=" * 80)
    print("B2 非对称功率 — swap 触发率 vs 功率比 (ML & CMA)")
    print("=" * 80)
    print(f"{'pr':>6} | {'ML fixed':>9} {'ML swap%':>9} | {'CMA fixed':>10} {'CMA swap%':>9} | {'oracle':>10}")
    for pr in ratios:
        s = summary[str(pr)]
        print(f"{pr:>6.2f} | {s['ml']['mean_fixed_ber']:>9.4f} "
              f"{s['ml']['swap_trigger_rate']*100:>8.0f}% | "
              f"{s['cma']['mean_fixed_ber']:>10.4f} "
              f"{s['cma']['swap_trigger_rate']*100:>8.0f}% | "
              f"{s['mean_oracle_fixed']:>10.2e}")
    print("=" * 80)
    print(f"结果: {RESULT_PATH} | 总耗时: {result['total_runtime_s']}s")


if __name__ == "__main__":
    main()
