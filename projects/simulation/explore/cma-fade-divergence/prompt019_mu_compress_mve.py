"""PROMPT-019: Q-DP3 维度 D MVE 生死验证 — 压μ（非冻结）能否救 BER

> 方向: Q-DP3 (预测性 fade 检测驱动跨帧 DSP 恢复) | 状态: WIP | 创建: 2026-07-14
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)

三对照:
  A = CMA 常规 μ=1e-3 (无压μ) — standard-CMA (Godard 1980, 含 z 因子, D022 合法 baseline)
  B = CMA fade 期间压 μ=1e-4 (功率阈值触发 h<thr) — 本任务核心
  C = oracle (fade 期间完美 MMSE) — 上界参照

双口径 (D018 强制):
  fixed-label BER: 固定 zX→sX, zY→sY
  PI-BER: 完整 2! 消歧后最优匹配 (需 pilot/帧头开销, 非免费)

理论预期 (TL-20, Step 0):
  PASS 机制 (可能性较低): R1 漂移模型 drift=μ·R²·σ_n·√(AFD/(block·T_S)) 线性正比于 μ,
    压μ降 fade 期间权重漂移 → 若 BER 恶化主因是 fade 期间权重漂移 → 应降 BER
  FAIL 机制 (可能性较高, R7 阴影 + D014 真因):
    1. R7 冻结(μ→0, 漂移→0)都没救回 BER(ΔP_div=0 全 24 组合) → fade 期间漂移非主因
    2. D014: CMA BER 恶化主因 = SOP 驱动极化串扰(polarization lock swap), 非 fade 期间漂移
    3. 压μ期间 SOP 同样旋转 → 极化串扰依旧 → 压μ可能无效
    最可能死因: 压μ降的是 fade 期间漂移, 但 BER 恶化来自 SOP 极化串扰, 两者正交

  预定义 PASS 标准: 压μ PI-BER 显著低于常规μ (配对 Wilcoxon p<0.05, ≥5 seeds), 且接近 oracle
  预定义 FAIL 标准: 压μ与常规μ无显著差异 (像 R7 冻结), 或压μ反而更差

C6 公式核对:
  standard-CMA 梯度 (Godard 1980 Eq.10): w += μ · (R² − |z|²) · z · r*
  压μ实现: fade 期间 (h_block < threshold) μ → μ/k (k=10 即 1e-3→1e-4), 非压期间恢复 μ
  不是完全冻结 (μ→0), 是减速 (μ→μ/k). 对照 R7 冻结 (跳过梯度更新) 的区别:
    R7 freeze: is_frozen → skip gradient entirely (μ_eff=0)
    压μ: is_faded → μ_eff = μ/k (梯度仍算, 只是步长小)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.stats import wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

from common._config import BLOCK
from common._experiment import save_results
from ml_long_seq_failure import (
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    T_S,
    compute_ber_phase_corrected,
    gen_channel,
    gen_qpsk,
    oracle_equalize,
)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs


# ─── 实验参数 (FR-20 溯源) ──────────────────────────────────

N_SYMBOLS = 5_000_000          # 5M (与 D022 一致, late slice [4.375M, 5M))
TURBULENCE = "strong"          # α=1.5, β=0.8 (GG 强湍流)
F_G = 100.0                    # 100Hz (PROMPT-018 AFD 实测点: AFD=10.12µs)
LATE_START = 4_375_000
LATE_END = 5_000_000
CMA_BLOCK_SIZE = 64            # sat.1553 §6.3 L756 并行化因子
COMPRESS_K = 10                # 压μ因子: μ → μ/k = 1e-3/10 = 1e-4
COMPRESS_THRESHOLD_DEFAULT = 0.3   # h_block < 0.3 → 压μ (PROMPT-019 默认)
COMPRESS_THRESHOLDS = [0.2, 0.3, 0.5]   # 阈值敏感性扫描
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]
SEEDS_30 = list(range(1000, 1030))

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt019_mu_compress.json"
)


# ─── Standard CMA (含 z 因子, Godard 1980, D022 合法 baseline) ──
# 复制自 prompt013_swap_mechanism_q2.py run_cma_diagnostic standard 分支
# 核心: w += μ · (R² − |z|²) · z · r*  (标准 Godard, 非 _cma.py 的 scalar-error)

class StandardCMA2x2:
    """Standard complex CMA 2×2 butterfly (Godard 1980, 含 z 因子).

    与 common/_cma.py CMAEqualizer2x2 的唯一区别:
      _cma.py:  w += μ · (R² − |z|²) · r*        (scalar-error, 缺 z)
      standard: w += μ · (R² − |z|²) · z · r*    (Godard 1980, 有 z)

    D022 证明 standard-CMA 是合法经典 CMA baseline.
    中心初始化: wxx/wyy 中心=1, wxy/wyx=0 (Qin 2025 L283).
    """

    def __init__(self, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK):
        self.n_tap = n_tap
        self.mu = mu
        self.R2 = R2
        center = n_tap // 2
        self.wxx = np.zeros(n_tap, dtype=complex)
        self.wxy = np.zeros(n_tap, dtype=complex)
        self.wyx = np.zeros(n_tap, dtype=complex)
        self.wyy = np.zeros(n_tap, dtype=complex)
        self.wxx[center] = 1.0
        self.wyy[center] = 1.0
        self._init_norm = self._norm()

    def _norm(self):
        return float(np.sqrt(
            np.sum(np.abs(self.wxx)**2) + np.sum(np.abs(self.wxy)**2) +
            np.sum(np.abs(self.wyx)**2) + np.sum(np.abs(self.wyy)**2)
        ))

    def equalize(self, rX, rY, h_block_series=None, theta_series=None,
                 block_size=CMA_BLOCK_SIZE, compress_threshold=None,
                 compress_k=COMPRESS_K):
        """块级 standard CMA 均衡, 可选压μ.

        参数
        ----
        rX, rY : ndarray (N,)
            双偏振接收信号.
        h_block_series : ndarray (n_blocks,) or None
            块级信道增益. None = 不压μ (常规 CMA).
        theta_series : ndarray (N,) or None
            符号级 SOP 旋转角. 用于记录压μ期间 SOP 漂移 (R7 阴影对照).
        compress_threshold : float or None
            h_block < 此值 → 压μ (μ→μ/k). None = 不压μ.
        compress_k : float
            压μ因子 (μ→μ/k).

        返回
        ----
        result : dict (zX/zY/diverged/n_compressed_blocks/compress_fraction/...)
        """
        from numpy.lib.stride_tricks import sliding_window_view
        N = len(rX)
        L = self.n_tap
        half = L // 2

        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)

        rX_win = sliding_window_view(rX, L)
        rY_win = sliding_window_view(rY, L)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None
        n_valid = N - L + 1
        n_blocks = n_valid // block_size

        n_compressed_blocks = 0
        n_total_blocks = 0
        compress_segments = []
        cur_compress_start = None

        compress_enabled = (h_block_series is not None and
                            compress_threshold is not None)
        if compress_enabled:
            h_blk_arr = h_block_series[:n_blocks]

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break
            n_total_blocks += 1

            # 判断是否压μ
            is_compressed = False
            mu_eff = self.mu
            if compress_enabled:
                h_blk_val = h_blk_arr[blk]
                if h_blk_val < compress_threshold:
                    is_compressed = True
                    mu_eff = self.mu / compress_k
                    n_compressed_blocks += 1
                    if cur_compress_start is None:
                        cur_compress_start = s + half

            # 块内向量化滤波: sat.1553 Eq.(28)
            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # 块末梯度更新: standard Godard 1980 w += μ·e·z·r*
            # (与 _cma.py 的区别: 多了 z 因子)
            eX = self.R2 - np.abs(zx_blk) ** 2
            eY = self.R2 - np.abs(zy_blk) ** 2
            self.wxx += mu_eff * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += mu_eff * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += mu_eff * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += mu_eff * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

            # 记录压μ段结束
            if is_compressed:
                pass
            else:
                if cur_compress_start is not None:
                    compress_segments.append((cur_compress_start, idx + block_size - 1))
                    cur_compress_start = None

            # 发散检测
            cur_norm = self._norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        # 关闭末尾未结束的压μ段
        if cur_compress_start is not None:
            compress_segments.append((cur_compress_start, idx + block_size - 1))

        # 算压μ期间 SOP 漂移 (与 R7 对照)
        compress_sop_drift = 0.0
        if theta_series is not None and compress_segments:
            for (fs_idx, fe_idx) in compress_segments:
                if fe_idx < len(theta_series) and fs_idx < len(theta_series):
                    drift = abs(float(theta_series[min(fe_idx, len(theta_series)-1)]
                                     - theta_series[fs_idx]))
                    compress_sop_drift += drift

        return {
            'zX': zX, 'zY': zY,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self._norm(),
            'init_w_norm': self._init_norm,
            'n_compressed_blocks': n_compressed_blocks,
            'n_total_blocks': n_total_blocks,
            'compress_fraction': n_compressed_blocks / max(n_total_blocks, 1),
            'compress_segments': compress_segments,
            'compress_sop_drift_rad': compress_sop_drift,
        }


# ─── 块级 h 计算 (复用 r7_freeze_quantification.py 逻辑) ─────

def compute_h_block_series(h, n_blocks, block_size=CMA_BLOCK_SIZE):
    """符号级 h → 块级 h_block_series (块内均值)."""
    h_block = np.zeros(n_blocks)
    n_valid = len(h)
    for blk in range(n_blocks):
        s = blk * block_size
        e = min(s + block_size, n_valid)
        h_block[blk] = np.mean(h[s:e]) if e > s else 0.0
    return h_block


# ─── 单次 trial: 三对照 (A 常规 / B 压μ / C oracle) ──────────

def run_single_seed(seed, n_symbols=N_SYMBOLS, f_g=F_G,
                    compress_threshold=COMPRESS_THRESHOLD_DEFAULT,
                    compress_k=COMPRESS_K, label=''):
    """跑一次三对照 trial.

    参数: f_G=100Hz (PROMPT-018 AFD 实测点), strong, N=5M, QPSK, 20dB, SOP=4e-7.
    late slice [4.375M, 5M) (与 D022 一致).
    """
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(n_symbols, alpha, beta, f_g,
                                           SOP_RATE, int(seed))

    n_valid = n_symbols - N_TAP + 1
    n_blocks = n_valid // CMA_BLOCK_SIZE
    h_block_series = compute_h_block_series(h, n_blocks, CMA_BLOCK_SIZE)

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    # ── A: standard-CMA 常规 μ (无压μ) ──
    eq_a = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_a = eq_a.equalize(rX, rY, h_block_series=None,  # 不压μ
                          block_size=CMA_BLOCK_SIZE)

    # ── B: standard-CMA fade 期间压μ ──
    eq_b = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_b = eq_b.equalize(rX, rY, h_block_series=h_block_series,
                          theta_series=theta,
                          block_size=CMA_BLOCK_SIZE,
                          compress_threshold=compress_threshold,
                          compress_k=compress_k)

    # ── C: oracle (完美 CSI MMSE) ──
    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    # ── 双口径 BER 评估 (D018) ──
    # SOP drift 已在 equalize 内部从 compress_segments 算好
    compress_sop_drift_b = res_b.get('compress_sop_drift_rad', 0.0)

    trial = {
        "seed": int(seed),
        "late_slice": [LATE_START, LATE_END],
        "elapsed_s": time.time() - started,
        "params": {
            "f_g": float(f_g),
            "turbulence": TURBULENCE,
            "n_symbols": int(n_symbols),
            "gamma_bar": float(GAMMA_BAR),
            "sop_rate": float(SOP_RATE),
            "mu_safe": float(MU_SAFE),
            "n_tap": int(N_TAP),
            "compress_threshold": float(compress_threshold) if compress_threshold else None,
            "compress_k": float(compress_k),
        },
        "methods": {
            "A_standard_cma": evaluate_outputs(
                res_a['zX'][late], res_a['zY'][late], source_x, source_y,
                res_a['diverged']),
            "B_compress_mu": evaluate_outputs(
                res_b['zX'][late], res_b['zY'][late], source_x, source_y,
                res_b['diverged']),
            "C_oracle": evaluate_outputs(
                oracle_x[late], oracle_y[late], source_x, source_y, False),
        },
        "artifacts": {
            "A_standard_cma": {
                "diverged": res_a['diverged'],
                "diverge_idx": res_a['diverge_idx'],
                "final_w_norm": float(res_a['final_w_norm']),
            },
            "B_compress_mu": {
                "diverged": res_b['diverged'],
                "diverge_idx": res_b['diverge_idx'],
                "final_w_norm": float(res_b['final_w_norm']),
                "n_compressed_blocks": int(res_b['n_compressed_blocks']),
                "n_total_blocks": int(res_b['n_total_blocks']),
                "compress_fraction": float(res_b['compress_fraction']),
                "compress_sop_drift_rad": float(compress_sop_drift_b),
                "compress_sop_drift_deg": float(np.degrees(compress_sop_drift_b)),
            },
        },
    }

    # 附加 excess PI-BER vs oracle
    oracle_pi = float(trial["methods"]["C_oracle"]["permutation_invariant_ber"]["mean"])
    for name in ("A_standard_cma", "B_compress_mu"):
        pi = float(trial["methods"][name]["permutation_invariant_ber"]["mean"])
        trial["methods"][name]["excess_pi_ber_vs_oracle"] = pi - oracle_pi

    return trial


# ─── 统计判定 ───────────────────────────────────────────────

def _paired_wilcoxon(values_a, values_b):
    """配对 Wilcoxon (双侧精确). values_a - values_b."""
    diffs = np.asarray(values_a, dtype=float) - np.asarray(values_b, dtype=float)
    wins_a = int(np.sum(diffs < 0))   # a < b: a 更好 (BER 更低)
    wins_b = int(np.sum(diffs > 0))   # b < a: b 更好
    ties = int(np.sum(diffs == 0))
    effective = diffs[diffs != 0]
    if len(effective) == 0:
        return {"statistic": 0.0, "pvalue": 1.0, "method": "exact",
                "wins_first": wins_a, "wins_second": wins_b, "ties": ties,
                "differences": diffs.tolist()}
    result = wilcoxon(diffs, alternative="two-sided", zero_method="wilcox",
                      correction=False, method="exact", nan_policy="raise")
    return {
        "method": "exact",
        "statistic": float(result.statistic),
        "pvalue": float(result.pvalue),
        "wins_first": wins_a,
        "wins_second": wins_b,
        "ties": ties,
        "differences": diffs.tolist(),
    }


def summarize_trials(trials):
    """汇总三对照 + 配对统计."""
    trials = sorted(trials, key=lambda t: int(t["seed"]))
    seeds = [int(t["seed"]) for t in trials]
    n = len(trials)

    methods = ("A_standard_cma", "B_compress_mu", "C_oracle")
    summaries = {}
    for m in methods:
        pi_vals = [float(t["methods"][m]["permutation_invariant_ber"]["mean"]) for t in trials]
        fixed_vals = [float(t["methods"][m]["fixed_label_ber"]["mean"]) for t in trials]
        summaries[m] = {
            "pi_ber": {"mean": float(np.mean(pi_vals)), "std": float(np.std(pi_vals)),
                       "values": pi_vals},
            "fixed_ber": {"mean": float(np.mean(fixed_vals)), "std": float(np.std(fixed_vals)),
                          "values": fixed_vals},
        }
        if m != "C_oracle":
            excess = [float(t["methods"][m]["excess_pi_ber_vs_oracle"]) for t in trials]
            summaries[m]["excess_pi_ber"] = {
                "mean": float(np.mean(excess)), "std": float(np.std(excess)), "values": excess}

    # 配对: A vs B (常规 vs 压μ) — 核心判定
    a_excess = summaries["A_standard_cma"]["excess_pi_ber"]["values"]
    b_excess = summaries["B_compress_mu"]["excess_pi_ber"]["values"]
    # diffs = A - B: 正=B更好(压μ降了 BER), 负=A更好
    a_vs_b = _paired_wilcoxon(a_excess, b_excess)
    # wins_second = B 赢的次数 (B_excess < A_excess)
    b_wins = a_vs_b["wins_second"]
    a_wins = a_vs_b["wins_first"]

    # PASS 标准: B PI-BER 显著低于 A (p<0.05), 且 B 接近 oracle
    oracle_pi = summaries["C_oracle"]["pi_ber"]["mean"]
    b_pi = summaries["B_compress_mu"]["pi_ber"]["mean"]
    a_pi = summaries["A_standard_cma"]["pi_ber"]["mean"]
    b_close_to_oracle = b_pi <= oracle_pi * 3 or b_pi - oracle_pi < 0.01

    pass_criteria = {
        "b_significantly_lower_than_a": bool(a_vs_b["pvalue"] < 0.05 and b_wins >= 4),
        "b_wins_vs_a": int(b_wins),
        "a_wins_vs_b": int(a_wins),
        "pvalue": float(a_vs_b["pvalue"]),
        "b_close_to_oracle": bool(b_close_to_oracle),
        "b_pi_minus_oracle": float(b_pi - oracle_pi),
        "a_pi_minus_oracle": float(a_pi - oracle_pi),
    }
    verdict = "PASS" if (pass_criteria["b_significantly_lower_than_a"]
                         and pass_criteria["b_close_to_oracle"]) else "FAIL"

    # 压μ统计
    compress_fracs = [float(t["artifacts"]["B_compress_mu"]["compress_fraction"]) for t in trials]
    compress_sop_drifts = [float(t["artifacts"]["B_compress_mu"]["compress_sop_drift_deg"]) for t in trials]
    b_diverged = sum(1 for t in trials if t["artifacts"]["B_compress_mu"]["diverged"])
    a_diverged = sum(1 for t in trials if t["artifacts"]["A_standard_cma"]["diverged"])

    return {
        "n_seeds": n,
        "seeds": seeds,
        "method_summaries": summaries,
        "paired_A_vs_B": a_vs_b,
        "pass_criteria": pass_criteria,
        "verdict": verdict,
        "compress_stats": {
            "mean_compress_fraction": float(np.mean(compress_fracs)),
            "mean_compress_sop_drift_deg": float(np.mean(compress_sop_drifts)),
            "max_compress_sop_drift_deg": float(np.max(compress_sop_drifts)),
            "n_B_diverged": int(b_diverged),
            "n_A_diverged": int(a_diverged),
        },
    }


# ─── 阈值敏感性扫描 ─────────────────────────────────────────

def run_threshold_sensitivity(seeds, thresholds=COMPRESS_THRESHOLDS):
    """阈值敏感性: h<0.2/0.3/0.5 三档对比."""
    results = {}
    for thr in thresholds:
        print(f"\n  [threshold {thr}] running {len(seeds)} seeds...")
        trials = []
        for seed in seeds:
            t = run_single_seed(seed, compress_threshold=thr, label=f'thr{thr}')
            trials.append(t)
        s = summarize_trials(trials)
        results[f"thr_{thr}"] = {
            "threshold": float(thr),
            "summary": s,
            "trials": trials,
        }
        print(f"  [threshold {thr}] verdict={s['verdict']} "
              f"B_pi={s['method_summaries']['B_compress_mu']['pi_ber']['mean']:.4f} "
              f"A_pi={s['method_summaries']['A_standard_cma']['pi_ber']['mean']:.4f} "
              f"oracle={s['method_summaries']['C_oracle']['pi_ber']['mean']:.4f} "
              f"B_wins={s['pass_criteria']['b_wins_vs_a']}/{len(seeds)}")
    return results


# ─── 主入口 ─────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(description='PROMPT-019: 压μ MVE 生死验证')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 seed, 500K symbols)')
    parser.add_argument('--threshold-scan', action='store_true',
                        help='阈值敏感性扫描 (h<0.2/0.3/0.5)')
    parser.add_argument('--n-seeds', type=int, default=5)
    parser.add_argument('--seeds', nargs='*', type=int, default=None)
    args = parser.parse_args(argv)

    t_global = time.time()

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (验证压μ实现正确性)")
        print("=" * 60)
        n_sym = 500_000
        late_start = int(n_sym * 0.875)
        late_end = n_sym
        global LATE_START, LATE_END
        LATE_START, LATE_END = late_start, late_end
        seeds = [1000]
        n_sym_use = n_sym
    else:
        seeds = args.seeds or (SEEDS_5 if args.n_seeds == 5 else SEEDS_30[:args.n_seeds])
        n_sym_use = N_SYMBOLS

    if args.threshold_scan and not args.smoke:
        print("=" * 60)
        print("PROMPT-019: 阈值敏感性扫描")
        print("=" * 60)
        thr_results = run_threshold_sensitivity(seeds, COMPRESS_THRESHOLDS)
        payload = {
            "experiment": "PROMPT-019 threshold sensitivity",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "params": {"f_g": F_G, "turbulence": TURBULENCE, "n_symbols": N_SYMBOLS,
                       "mu_safe": MU_SAFE, "compress_k": COMPRESS_K},
            "threshold_results": thr_results,
            "elapsed_s": time.time() - t_global,
        }
        out_path = (SIM_DIR / "results" / "cma-fade-divergence"
                    / "prompt019_threshold_scan.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nThreshold scan saved to: {out_path}")
        print(f"总耗时: {time.time() - t_global:.0f}s")
        return payload

    # 主实验: 三对照 × n_seeds
    print("=" * 60)
    print(f"PROMPT-019: 压μ MVE 生死验证 ({len(seeds)} seeds)")
    print(f"参数: f_G={F_G}, {TURBULENCE}, N={n_sym_use}, QPSK, "
          f"SNR={10*np.log10(GAMMA_BAR):.0f}dB, SOP={SOP_RATE}")
    print(f"压μ: threshold={COMPRESS_THRESHOLD_DEFAULT}, k={COMPRESS_K} "
          f"(μ={MU_SAFE}→{MU_SAFE/COMPRESS_K})")
    print("=" * 60)

    trials = []
    for i, seed in enumerate(seeds):
        print(f"\n[seed {seed} {i+1}/{len(seeds)}] running...")
        t = run_single_seed(seed, n_symbols=n_sym_use)
        trials.append(t)
        a_pi = t["methods"]["A_standard_cma"]["permutation_invariant_ber"]["mean"]
        b_pi = t["methods"]["B_compress_mu"]["permutation_invariant_ber"]["mean"]
        c_pi = t["methods"]["C_oracle"]["permutation_invariant_ber"]["mean"]
        cf = t["artifacts"]["B_compress_mu"]["compress_fraction"]
        sd = t["artifacts"]["B_compress_mu"]["compress_sop_drift_deg"]
        elapsed = t["elapsed_s"]
        print(f"  A(常规)={a_pi:.4f}  B(压μ)={b_pi:.4f}  C(oracle)={c_pi:.4f}"
              f"  | 压μ占比={cf*100:.1f}%  SOP漂移={sd:.1f}°  [{elapsed:.0f}s]")

    summary = summarize_trials(trials)

    payload = {
        "experiment": "PROMPT-019 mu-compress MVE",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "params": {
            "f_g": float(F_G), "turbulence": TURBULENCE,
            "n_symbols": int(n_sym_use), "gamma_bar": float(GAMMA_BAR),
            "sop_rate": float(SOP_RATE), "mu_safe": float(MU_SAFE),
            "n_tap": int(N_TAP), "r2": float(R2_QPSK),
            "compress_threshold": float(COMPRESS_THRESHOLD_DEFAULT),
            "compress_k": float(COMPRESS_K),
            "late_slice": [LATE_START, LATE_END],
        },
        "trials": trials,
        "summary": summary,
        "elapsed_s": time.time() - t_global,
    }

    out_path = RESULT_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")

    # 打印汇总
    print("\n" + "=" * 60)
    print(f"PROMPT-019 汇总: 压μ MVE 生死验证 ({len(seeds)} seeds)")
    print("=" * 60)
    ms = summary["method_summaries"]
    print(f"\n{'对照':>12} {'PI-BER mean':>12} {'fixed BER':>12} {'excess PI':>12}")
    print("-" * 60)
    for m in ("A_standard_cma", "B_compress_mu", "C_oracle"):
        pi = ms[m]["pi_ber"]["mean"]
        fx = ms[m]["fixed_ber"]["mean"]
        ex = ms[m].get("excess_pi_ber", {}).get("mean", 0.0)
        print(f"{m:>12} {pi:>12.4f} {fx:>12.4f} {ex:>12.4f}")

    pc = summary["pass_criteria"]
    cs = summary["compress_stats"]
    print(f"\n配对 A vs B: B 赢 {pc['b_wins_vs_a']}/{summary['n_seeds']}, "
          f"p={pc['pvalue']:.4f}")
    print(f"B 接近 oracle: {pc['b_close_to_oracle']} "
          f"(B-oracle={pc['b_pi_minus_oracle']:.4f}, A-oracle={pc['a_pi_minus_oracle']:.4f})")
    print(f"压μ占比: {cs['mean_compress_fraction']*100:.1f}%  "
          f"SOP 漂移: {cs['mean_compress_sop_drift_deg']:.1f}° (max {cs['max_compress_sop_drift_deg']:.1f}°)")
    print(f"发散: A={cs['n_A_diverged']}/{summary['n_seeds']}  B={cs['n_B_diverged']}/{summary['n_seeds']}")
    print(f"\n>>> 判定: {summary['verdict']} <<<")
    print(f"\n总耗时: {time.time() - t_global:.0f}s")

    return payload


if __name__ == '__main__':
    main()
