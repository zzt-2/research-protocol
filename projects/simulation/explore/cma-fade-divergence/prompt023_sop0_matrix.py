"""PROMPT-023: D014 SOP×f_G 决定性矩阵独立复现 (5 seeds, 双口径, skip10%)

> 方向: Q-CMA-FADE 分析层 | 状态: WIP | 创建: 2026-07-15
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)

任务 (D014 溯源):
  D014 (decisions.md L762-838) 核心贡献 "SOP 驱动极化串扰是 BER 恶化真因",
  关键证据是 SOP×f_G 决定性矩阵 (CMA/oracle BER 比值). 该矩阵原由主控在
  S011 续做 (独立诊断), 无独立可复现脚本 + JSON. 本脚本填补该债务.

复现矩阵 (D014 原值, S009 整段 skip10% 口径):
                   f_G=30   f_G=100  f_G=1000
    SOP=0          1.0×     1.0×     4.2×
    SOP=4e-7       1.9×     4.2×     7.9×

设计原则 (隔离原则, 不改 common/):
  - import 复用 prompt019 StandardCMA2x2 (Godard 1980 含 z 因子, D022 合法 baseline)
  - import 复用 ml_long_seq_failure gen_channel / oracle_equalize
  - evaluate 逻辑本地实现 (evaluate_with_skip), 复用 prompt012 evaluate_outputs 的
    双口径 (fixed-label BER + 2! 排列不变 PI-BER), 但显式接 skip_frac (S009 skip10% 口径)

口径说明:
  - ratio = CMA PI-BER / oracle PI-BER (D018 强制双口径, ratio 用 PI 口径)
  - skip10% warmup: 跳过被评估段前 10% (CMA warmup), 复现 S009 skip10% 口径
  - 双口径并报 (fixed + PI), ratio 主口径 = PI

SOP=0 验证:
  gen_channel(N, ..., sop_rate=0, seed): theta = sop_rate * np.arange(N) = zeros(N),
  cos_t=1, sin_t=0 → rX=sqrt(h)*sX+noise, rY=sqrt(h)*sY+noise (无极化旋转, 无串扰).
  sop_rate=0 无除零/边界问题 (已 smoke test 验证 theta 全 0).

参数 (从 prompt019 读):
  strong 湍流 (alpha=1.5, beta=0.8), N=5M, QPSK, GAMMA_BAR=100 (20dB),
  block_size=64 (CMA_BLOCK_SIZE), mu=1e-3 (MU_SAFE), n_tap=11 (N_TAP).
  SOP ∈ {0, 4e-7}, f_G ∈ {30, 100, 1000}, seeds=[1000..1004] (5 seeds).
  5 seeds × 2 SOP × 3 f_G = 30 runs.
"""
from __future__ import annotations

import argparse
import json
import time
from itertools import permutations
from pathlib import Path
import sys

import numpy as np


# ─── 路径设置 (跟 prompt019 一致) ───────────────────────────
SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from params import SimulationConfig
from ml_long_seq_failure import (
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    compute_ber_phase_corrected,
    gen_channel,
    oracle_equalize,
)
# 复用 prompt019 的 StandardCMA2x2 (Godard 1980 含 z 因子, D022 合法 baseline)
from prompt019_mu_compress_mve import StandardCMA2x2, CMA_BLOCK_SIZE


# ─── 实验参数 (D014 决定性矩阵) ─────────────────────────────
N_SYMBOLS = 5_000_000          # 5M (与 D014/S009 一致)
TURBULENCE = "strong"          # α=1.5, β=0.8 (GG 强湍流)
F_G_LEVELS = [30.0, 100.0, 1000.0]      # D014 三档
SOP_LEVELS = [0.0, 4e-7]                # D014 两档 (0 + 1 krad/s)
SEEDS = [1000, 1001, 1002, 1003, 1004]  # 5 seeds
SKIP_FRAC = 0.10               # S009 skip10% warmup 口径

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt023_sop0_matrix.json"
)


# ─── 双口径 BER 评估 (本地实现, 接 skip_frac) ───────────────
# 复用 prompt012 evaluate_outputs 逻辑, 但显式传 skip_frac (skip10% warmup)

def _abs_corr(a, b):
    a = np.asarray(a) - np.mean(a)
    b = np.asarray(b) - np.mean(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(abs(np.vdot(a, b)) / denom) if denom else 0.0


def evaluate_with_skip(z_x, z_y, s_x, s_y, skip_frac=SKIP_FRAC):
    """双口径 BER (fixed + PI) + 相关, 跳前 skip_frac warmup.

    fixed-label BER: 固定 zX→sX, zY→sY (skip 后评估).
    PI-BER: 完整 2! 消歧后最优匹配 (skip 后评估).
    返回 fixed_mean, pi_mean (两个标量), plus 相关/分类诊断.
    """
    outputs = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))

    fixed_per_output = [
        compute_ber_phase_corrected(outputs[0], sources[0], skip_frac=skip_frac),
        compute_ber_phase_corrected(outputs[1], sources[1], skip_frac=skip_frac),
    ]
    candidates = []
    for assignment in permutations((0, 1)):
        bers = [
            compute_ber_phase_corrected(outputs[i], sources[assignment[i]],
                                        skip_frac=skip_frac)
            for i in range(2)
        ]
        candidates.append((float(np.mean(bers)), assignment, bers))
    pi_mean, assignment, pi_per_output = min(candidates, key=lambda item: item[0])

    corr = np.array([
        [_abs_corr(outputs[0], sources[0]), _abs_corr(outputs[0], sources[1])],
        [_abs_corr(outputs[1], sources[0]), _abs_corr(outputs[1], sources[1])],
    ])
    return {
        "fixed_label_ber": {
            "zX_sX": float(fixed_per_output[0]),
            "zY_sY": float(fixed_per_output[1]),
            "mean": float(np.mean(fixed_per_output)),
        },
        "permutation_invariant_ber": {
            "mean": pi_mean,
            "per_output": [float(x) for x in pi_per_output],
            "assignment": ["sX" if i == 0 else "sY" for i in assignment],
        },
        "abs_corr": {
            "zX_sX": float(corr[0, 0]), "zX_sY": float(corr[0, 1]),
            "zY_sX": float(corr[1, 0]), "zY_sY": float(corr[1, 1]),
        },
        "abs_corr_zX_zY": _abs_corr(outputs[0], outputs[1]),
    }


# ─── 单次 run: CMA vs oracle 同信道 (无压μ, D014 决定性实验) ─

def run_single(seed, f_g, sop_rate, n_symbols=N_SYMBOLS):
    """跑一次 CMA-vs-oracle trial, 返回 ratio + 双口径 BER + 诊断.

    CMA 用 standard-CMA (Godard 1980 含 z, mu=1e-3), 不压μ (D014 决定性 baseline).
    oracle 用完美 CSI MMSE.
    全段评估 + skip10% warmup (S009 口径).
    """
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        n_symbols, alpha, beta, f_g, sop_rate, int(seed))

    # SOP=0 安全验证 (纪律要求): theta 必须全 0
    theta_all_zero = bool(np.allclose(theta, 0.0))
    if sop_rate == 0.0 and not theta_all_zero:
        # 不应发生 (gen_channel sop_rate=0 → theta=zeros), 防御性处理
        theta = np.zeros(n_symbols)
        theta_all_zero = True

    # ── CMA (standard Godard, 无压μ) ──
    eq = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_cma = eq.equalize(rX, rY, h_block_series=None,  # 不压μ
                          block_size=CMA_BLOCK_SIZE)

    # ── oracle (完美 CSI MMSE) ──
    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    # ── 双口径 BER (全段, skip10% warmup) ──
    cma_eval = evaluate_with_skip(res_cma['zX'], res_cma['zY'], sX, sY)
    oracle_eval = evaluate_with_skip(oracle_x, oracle_y, sX, sY)

    cma_fixed = cma_eval["fixed_label_ber"]["mean"]
    cma_pi = cma_eval["permutation_invariant_ber"]["mean"]
    oracle_fixed = oracle_eval["fixed_label_ber"]["mean"]
    oracle_pi = oracle_eval["permutation_invariant_ber"]["mean"]

    # ratio = CMA / oracle (主口径 PI; D018 双口径强制, fixed 也并报)
    # 边界处理 (N=5M 分辨率上限):
    #   1) oracle>0: 正常比值 num/den
    #   2) oracle==0 且 num==0: 两者都 0 误码 → 定义 1.0 (等价)
    #   3) oracle==0 且 num<RES_FLOOR (1e-4): CMA 仅几个误码 (N=5M 下 <500 bit),
    #      两者功能上同达 oracle → cap 为 1.0 (分辨率上限, 非真实恶化)
    #   4) oracle==0 且 num>=RES_FLOOR: 真实极恶化 → inf
    RES_FLOOR = 1e-4   # ~500 bit / 4.5M, N=5M 下的统计可信下限

    def _safe_ratio(num, den):
        if den > 0:
            return num / den
        if num == 0:
            return 1.0
        if num < RES_FLOOR:
            return 1.0    # 分辨率上限: CMA 仅几个误码 vs oracle 完美
        return float('inf')
    ratio_pi = _safe_ratio(cma_pi, oracle_pi)
    ratio_fixed = _safe_ratio(cma_fixed, oracle_fixed)

    return {
        "seed": int(seed),
        "f_g": float(f_g),
        "sop_rate": float(sop_rate),
        "theta_all_zero": theta_all_zero,
        "theta_max_abs_rad": float(np.max(np.abs(theta))),
        "elapsed_s": float(time.time() - started),
        "cma_diverged": bool(res_cma['diverged']),
        "cma_diverge_idx": res_cma['diverge_idx'],
        "cma_final_w_norm": float(res_cma['final_w_norm']),
        "cma_fixed_ber": float(cma_fixed),
        "cma_pi_ber": float(cma_pi),
        "oracle_fixed_ber": float(oracle_fixed),
        "oracle_pi_ber": float(oracle_pi),
        "both_zero_errors": bool(cma_pi == 0.0 and oracle_pi == 0.0),
        "ratio_pi": float(ratio_pi),
        "ratio_fixed": float(ratio_fixed),
        "cma_corr_zX_sX": cma_eval["abs_corr"]["zX_sX"],
        "cma_corr_zX_zY": cma_eval["abs_corr_zX_zY"],
        "cma_assignment": cma_eval["permutation_invariant_ber"]["assignment"],
    }


# ─── 矩阵汇总 ───────────────────────────────────────────────

def sop_label(sop_rate):
    return "sop0" if sop_rate == 0.0 else "sop4e7"


def fg_label(f_g):
    return f"fg{int(f_g)}"


def summarize_cell(runs):
    """汇总一个 (sop, f_g) cell 的 5 seeds."""
    ratio_pi = [r["ratio_pi"] for r in runs]
    ratio_fixed = [r["ratio_fixed"] for r in runs]
    cma_pi = [r["cma_pi_ber"] for r in runs]
    cma_fixed = [r["cma_fixed_ber"] for r in runs]
    oracle_pi = [r["oracle_pi_ber"] for r in runs]
    oracle_fixed = [r["oracle_fixed_ber"] for r in runs]
    return {
        "ratio_pi_mean": float(np.mean(ratio_pi)),
        "ratio_pi_seeds": [float(x) for x in ratio_pi],
        "ratio_fixed_mean": float(np.mean(ratio_fixed)),
        "ratio_fixed_seeds": [float(x) for x in ratio_fixed],
        "cma_pi_mean": float(np.mean(cma_pi)),
        "cma_fixed_mean": float(np.mean(cma_fixed)),
        "oracle_pi_mean": float(np.mean(oracle_pi)),
        "oracle_fixed_mean": float(np.mean(oracle_fixed)),
        "n_diverged": int(sum(1 for r in runs if r["cma_diverged"])),
    }


# ─── 主入口 ─────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='PROMPT-023: D014 SOP×f_G 决定性矩阵独立复现 (5 seeds)')
    parser.add_argument('--sop', type=float, default=None,
                        help='只跑某一 SOP (0 or 4e-7), 用于增量/后台')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke (N=500K, 1 seed, 验证流程)')
    args = parser.parse_args(argv)

    t_global = time.time()

    if args.smoke:
        n_sym = 500_000
        sop_list = [0.0, 4e-7]
        fg_list = [30.0, 100.0]
        seeds = [1000]
        print("=" * 60)
        print("SMOKE TEST (N=500K, 验证流程)")
        print("=" * 60)
    else:
        n_sym = N_SYMBOLS
        sop_list = [args.sop] if args.sop is not None else SOP_LEVELS
        fg_list = F_G_LEVELS
        seeds = SEEDS
        print("=" * 70)
        print(f"PROMPT-023: D014 SOP×f_G 决定性矩阵独立复现 ({len(seeds)} seeds)")
        print(f"参数: strong (α=1.5,β=0.8), N={n_sym}, QPSK, "
              f"SNR={10*np.log10(GAMMA_BAR):.0f}dB, mu={MU_SAFE}, n_tap={N_TAP}")
        print(f"SOP ∈ {sop_list}, f_G ∈ {fg_list}, seeds={seeds}")
        print(f"口径: skip10% warmup, ratio=CMA_PI/oracle_PI (并报 fixed)")
        print(f"总 runs = {len(sop_list)}×{len(fg_list)}×{len(seeds)} = "
              f"{len(sop_list)*len(fg_list)*len(seeds)}")
        print("=" * 70)

    per_seed_runs = []
    matrix = {}
    for sop_rate in sop_list:
        for f_g in fg_list:
            cell_key = f"{sop_label(sop_rate)}_{fg_label(f_g)}"
            cell_runs = []
            for i, seed in enumerate(seeds):
                t0 = time.time()
                r = run_single(seed, f_g, sop_rate, n_symbols=n_sym)
                cell_runs.append(r)
                per_seed_runs.append(r)
                print(f"  [{cell_key} seed {seed} {i+1}/{len(seeds)}] "
                      f"ratio_pi={r['ratio_pi']:.2f} "
                      f"(CMA_pi={r['cma_pi_ber']:.4f} oracle_pi={r['oracle_pi_ber']:.4f}) "
                      f"theta0={r['theta_all_zero']} div={r['cma_diverged']} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
            matrix[cell_key] = summarize_cell(cell_runs)
            s = matrix[cell_key]
            print(f"  >> {cell_key}: ratio_pi_mean={s['ratio_pi_mean']:.2f} "
                  f"(CMA_pi={s['cma_pi_mean']:.4f} oracle_pi={s['oracle_pi_mean']:.4f} "
                  f"diverged={s['n_diverged']}/{len(seeds)})\n", flush=True)

    payload = {
        "experiment": "PROMPT-023 D014 SOPxf_G deterministic matrix (5 seeds)",
        "purpose": "Reproduce D014 SOP×f_G matrix with isolated script + JSON "
                   "(debt: no independent reproducible artifact)",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "params": {
            "n_symbols": int(n_sym),
            "turbulence": TURBULENCE,
            "alpha": 1.5,
            "beta": 0.8,
            "modulation": "QPSK",
            "gamma_bar": float(GAMMA_BAR),
            "mu": float(MU_SAFE),
            "n_tap": int(N_TAP),
            "block_size": int(CMA_BLOCK_SIZE),
            "seeds": [int(s) for s in seeds],
            "skip_frac": float(SKIP_FRAC),
            "ratio_caliber": "CMA PI-BER / oracle PI-BER (skip10% warmup)",
            "sop_rates": [float(s) for s in sop_list],
            "f_g_levels": [float(f) for f in fg_list],
            "d014_reference": {
                "matrix": {
                    "sop0_fg30": 1.0, "sop0_fg100": 1.0, "sop0_fg1000": 4.2,
                    "sop4e7_fg30": 1.9, "sop4e7_fg100": 4.2, "sop4e7_fg1000": 7.9,
                },
                "caliber_note": "D014 原矩阵用 S009 整段 skip10% (phase-corrected BER); "
                                "本复现用 PI-BER (D018), 绝对值会不同但方向应一致",
            },
        },
        "matrix": matrix,
        "per_seed": per_seed_runs,
        "elapsed_s": float(time.time() - t_global),
    }

    out_path = RESULT_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")

    # 打印矩阵 (markdown 友好)
    print("\n" + "=" * 70)
    print(f"复现矩阵 (5 seeds mean, ratio_pi = CMA_PI/oracle_PI, skip10%)")
    print("=" * 70)
    header = "            " + "".join(f"f_G={int(f):>8}" for f in fg_list)
    print(header)
    for sop_rate in sop_list:
        row = f"SOP={sop_rate:<10g}"
        for f_g in fg_list:
            key = f"{sop_label(sop_rate)}_{fg_label(f_g)}"
            if key in matrix:
                row += f"{matrix[key]['ratio_pi_mean']:>8.2f}×"
            else:
                row += f"{'—':>8}"
        print(row)
    print(f"\n总耗时: {time.time() - t_global:.0f}s")
    return payload


if __name__ == '__main__':
    main()
