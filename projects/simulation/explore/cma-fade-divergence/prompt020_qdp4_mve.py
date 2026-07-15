"""PROMPT-020: Q-DP4 (SOP 驱动 lock swap 防跳变) 维度 D MVE

> 方向: Q-DP4 (SOP 驱动 polarization lock swap 防跳变) | 状态: WIP | 创建: 2026-07-14
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)
> 隔离原则: 不改 common/, 复用 prompt019 StandardCMA2x2 + ml_long_seq_failure + prompt012 evaluate_outputs

## 背景 (主控修正后的增量定位, S021)

D014 证明 BER 真因 = SOP 驱动 polarization lock swap (2×2 蝶形 CMA 收敛后因 SOP 旋转
权重跳到混淆 X/Y 次优解). D018 双口径修正: standard-CMA PI-BER 0.03174 (vs oracle 7.5×),
ML PI-BER 0.00523 (接近 oracle), 两者 fixed BER ≈0.5 (都 swap 10/10).

6× PI-BER 差距 (CMA 0.03174 vs ML 0.00523) 是 Q-DP4 Go/Kill 的关键 hinge:
  - 定位 A (防 swap 本身) 增量小 (省帧头 <1%)
  - 定位 B (降 CMA PI-BER 6× 残余差距) 增量大 — 须 MVE 分解这 6× 来源

## 三个验证 (按 hinge 优先级)

验证1 (最高优先, Go/Kill hinge): 6× PI-BER 差距来源分解
  问题: standard-CMA swap 消歧后 PI-BER 0.03174 仍比 ML 0.00523 差 6×, 主要来自什么?
  分解:
    B0 = standard-CMA PI-BER (baseline, 已知 ≈0.03174)
    B1 = CMA 在 late_slice 上用 identity 重新初始化在线跟踪 (测 CMA 跟踪能力是否够)
    B2 = per-block LS 最优 PI-BER (完美 CSI 下线性接收机下界)
    B3 = CMA 用 early-segment 收敛权重固定不更新 (纯固定权重参考)
  PASS: 残余 BER 主要来自权重漂移 (B0 >> B2, 且 B1 接近 oracle) → 定位 B 成立
  FAIL: 残余 BER 主要来自跟踪滞后或瞬态 → 定位 B 不成立

验证2 (Go/Kill 前置): 改步长证否
  问题: 改步长 (大μ/小μ) 能否消除 SOP=4e-7 下 1.9-7.9× BER 退化?
  SOP×f_G 矩阵, standard-CMA 步长 μ∈{1e-4, 1e-3, 5e-3}, 看 PI-BER 比值 (CMA/oracle)
  是否随步长变化消除 SOP 引入的退化.
  PASS: 步长不消除 SOP 退化 (B'类不占 Q-DP4)
  FAIL: 某步长能显著降 SOP 退化 → Q-DP4 增量空间被压缩

验证3 (方法效果, 仅 1+2 PASS 才做): 形态2 预防性约束 (J_XCA 互相关惩罚持续运行版)
  问题: 在 CMA 代价加 α·J_XCA 能否降 swap 概率 + 降 PI-BER?
  α 扫 {0, 0.1, 0.5, 1.0}, 对照 standard-CMA (α=0) / oracle
  PASS: α>0 时 swap 概率↓ + PI-BER↓ (至少降 2×) + 跟踪能力不显著恶化
  FAIL: J_XCA 引噪声压过收益 或 约束伤跟踪

## 理论预期 (TL-20, 实验前写)

验证1 预期: B0 (0.03174) >> B2 (≈oracle 0.004-0.01), B1 接近 oracle → 残余 = 权重漂移 (a)
  物理依据: SOP 持续旋转下恒模代价让 CMA 权重在 swap 盆地附近晃动, FIR 系数偏;
  ML 固定 LS 权重覆盖全 SOP 范围 → 残余小. CMA 跟踪能力本身够 (D014 SOP=0 时 = oracle).

验证2 预期: FAIL (步长不消除 SOP 退化)
  物理依据: swap 是恒模多解离散事件非步长可消除连续漂移. μ 太小→跟踪滞后; μ 太大→
  漂入错解更快. SOP=0 对照 ratio=1.0 (D014), SOP=4e-7 升 1.9-7.9× 与 μ 选择正交.

验证3 预期: 不确定/谨慎 (CA-CMA 自承 J_XCA 引噪声不适合持续运行)
  小 α 可能降 swap 概率适度; 大 α 可能伤跟踪 (J_XCA 强制对角优势 vs SOP 旋转需权重更新).

## 参数溯源 (FR-20)
  sop_rate=4e-7: sat.1553 §6.3 L778 仿真值 (1 krad/s 真实 OSL 速率)
  f_G=30: D022 注册域; f_G=100/1000: D014 SOP×f_G 矩阵
  N=5M: D022 注册域; late [4.375M, 5M): D022/D018 一致
  μ=1e-3: D006 安全区低风险 (D018 收紧); μ sweep {1e-4,5e-3}: 验证2 扩展
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from itertools import permutations

import numpy as np
from scipy.stats import wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common._config import BLOCK
from ml_long_seq_failure import (
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    T_S,
    compute_ber_phase_corrected,
    gen_channel,
    oracle_equalize,
)
from params import SimulationConfig
from prompt019_mu_compress_mve import StandardCMA2x2, compute_h_block_series
from prompt012_longseq_audit import evaluate_outputs, _abs_corr, classify_failure


# ─── 实验参数 (FR-20 溯源) ──────────────────────────────────

N_SYMBOLS = 5_000_000          # 5M (D022 注册域)
TURBULENCE = "strong"          # α=1.5, β=0.8 (GG 强湍流)
F_G_PRIMARY = 30.0             # D022 注册域
LATE_START = 4_375_000
LATE_END = 5_000_000
CMA_BLOCK_SIZE = 64            # sat.1553 §6.3 L756 并行化因子
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]

# 验证2: SOP×f_G 矩阵 (D014 设置) × μ 扫描
SOP_VALUES = [0.0, 4e-7]       # SOP=0 对照 + SOP=4e-7 (1krad/s sat.1553)
FG_VALUES = [30.0, 100.0, 1000.0]   # D014 SOP×f_G 矩阵三频点
MU_VALUES = [1e-4, 1e-3, 5e-3]      # 验证2 步长扫描

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt020_qdp4_mve.json"
)


# ═══════════════════════════════════════════════════════════
#  验证1: 6× PI-BER 差距来源分解
# ═══════════════════════════════════════════════════════════

def per_block_ls_optimal(rX, rY, sX, sY, h, theta, late_start, late_end,
                         gamma_bar, n_tap=N_TAP, block_size=CMA_BLOCK_SIZE):
    """Per-block LS 最优 2×2 蝶形 FIR (完美 CSI 下界).

    每个 block 用完美 CSI (h, theta 已知) 求最优 wxx/wxy/wyx/wyy:
    撤销 SOP 旋转后, 最优 = 单 tap MMSE + 噪声白化. 这里用闭式最小二乘
    在每 block 上拟合 FIR 系数 (用已知 sX/sY 做 LS 监督), 得线性接收机下界.

    返回 late 段 zX/zY.
    """
    N = len(rX)
    L = n_tap
    half = L // 2
    from numpy.lib.stride_tricks import sliding_window_view

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // block_size

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    for blk in range(n_blocks):
        s = blk * block_size
        e = s + block_size
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]    # (block_size, L)
        rY_blk = rY_win[s:e]
        # 目标 (中心对齐): sX[s+half : s+half+block_size]
        tgt_s = s + half
        tgt_e = tgt_s + block_size
        sX_blk = sX[tgt_s:tgt_e]
        sY_blk = sY[tgt_s:tgt_e]

        # LS 解 2×2 蝶形: zX = wxx∗rX + wxy∗rY, 最小化 |zX - sX|²
        # 复值 LS: 构建实值增广矩阵
        ns = block_size
        # zX 的系数 [wxx(L), wxy(L)] 共 2L 复系数
        # 拆实虚: 4L 实系数
        A = np.empty((2 * ns, 4 * L))
        A[:ns, :L] = rX_blk.real
        A[:ns, L:2*L] = -rX_blk.imag
        A[:ns, 2*L:3*L] = rY_blk.real
        A[:ns, 3*L:] = -rY_blk.imag
        A[ns:, :L] = rX_blk.imag
        A[ns:, L:2*L] = rX_blk.real
        A[ns:, 2*L:3*L] = rY_blk.imag
        A[ns:, 3*L:] = rY_blk.real
        y = np.concatenate([sX_blk.real, sX_blk.imag])
        w, *_ = np.linalg.lstsq(A, y, rcond=None)
        # 推理本 block
        z_blk = (A @ w)[:ns] + 1j * (A @ w)[ns:]
        zX[tgt_s:tgt_e] = z_blk

        # zY 同理 (目标 sY)
        A2 = A.copy()
        y2 = np.concatenate([sY_blk.real, sY_blk.imag])
        w2, *_ = np.linalg.lstsq(A2, y2, rcond=None)
        z_blk2 = (A2 @ w2)[:ns] + 1j * (A2 @ w2)[ns:]
        zY[tgt_s:tgt_e] = z_blk2

    return zX, zY


def run_v1_decomposition(seed, f_g=F_G_PRIMARY, n_symbols=N_SYMBOLS, label='',
                         run_ml=True):
    """验证1: 单 seed 的 4-way 分解 (B0/B1/B2/B3 + oracle + ML).

    B0 = standard-CMA PI-BER (baseline)
    B1 = CMA identity 重新初始化, 仅在 late_slice 在线跟踪 (测 CMA 跟踪能力)
    B2 = per-block LS 最优 PI-BER (完美 CSI 线性下界)
    B3 = CMA 用 early-segment 收敛权重固定不更新 (纯固定权重参考)
    + oracle + ML (可选, 复用 ml_long_seq_failure; D022 已知 ML PI≈0.00523)
    """
    from ml_long_seq_failure import run_ml_trial, ML_TRAIN_FRAC
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        n_symbols, alpha, beta, f_g, SOP_RATE, int(seed))

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    # ── B0: standard-CMA (常规, 复用 prompt019) ──
    eq_b0 = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_b0 = eq_b0.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)

    # ── B1: CMA identity 重新初始化, 仅 late 段在线跟踪 ──
    # 目的: 测 CMA 在正确盆地 (identity = 未 swap) 从 late_start 开始在线跟踪
    # SOP 漂移的能力. 如果 BER 接近 oracle → CMA 跟踪能力够, 问题是它漂到错解.
    eq_b1 = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    # 只跑 late 段 (identity 初始化 = 正确盆地)
    rX_late = rX[LATE_START:LATE_END]
    rY_late = rY[LATE_START:LATE_END]
    res_b1 = eq_b1.equalize(rX_late, rY_late, block_size=CMA_BLOCK_SIZE)
    # B1 输出对齐 late 段内部
    zX_b1 = res_b1['zX']
    zY_b1 = res_b1['zY']

    # ── B2: per-block LS 最优 (完美 CSI 下界) ──
    zX_b2, zY_b2 = per_block_ls_optimal(
        rX, rY, sX, sY, h, theta, LATE_START, LATE_END, GAMMA_BAR)

    # ── B3: CMA 用 early 收敛权重固定不更新 ──
    # 先在 early [0, LATE_START) 收敛, 然后固定权重前馈推理 late 段
    eq_b3 = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    # 跑 early 段让权重收敛 (但 early 段也含 SOP, 可能已 swap — 这是诊断目的)
    rX_early = rX[:LATE_START]
    rY_early = rY[:LATE_START]
    res_b3_train = eq_b3.equalize(rX_early, rY_early, block_size=CMA_BLOCK_SIZE)
    # 用收敛后的固定权重前馈推理 late 段
    from numpy.lib.stride_tricks import sliding_window_view
    L = N_TAP
    rX_late_win = sliding_window_view(rX_late, L)
    rY_late_win = sliding_window_view(rY_late, L)
    half = L // 2
    zX_b3 = np.zeros(LATE_END - LATE_START, dtype=complex)
    zY_b3 = np.zeros(LATE_END - LATE_START, dtype=complex)
    zX_b3[half:half + len(rX_late_win)] = rX_late_win @ eq_b3.wxx + rY_late_win @ eq_b3.wxy
    zY_b3[half:half + len(rX_late_win)] = rX_late_win @ eq_b3.wyx + rY_late_win @ eq_b3.wyy

    # ── oracle ──
    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    # ── ML (复用, 可选 — D022 已知 ML PI≈0.00523 作参考) ──
    ml_ok = False
    ml_res = {'skipped': True}
    zX_ml = np.zeros(n_symbols, dtype=complex)
    zY_ml = np.zeros(n_symbols, dtype=complex)
    if run_ml:
        try:
            zX_ml, zY_ml, n_train, ml_res = run_ml_trial(rX, rY, sX, sY)
            ml_ok = True
        except Exception as ex:
            ml_res = {'error': str(ex)}

    # ── 双口径 BER 评估 (D018) ──
    trial = {
        "seed": int(seed),
        "elapsed_s": time.time() - started,
        "params": {
            "f_g": float(f_g), "turbulence": TURBULENCE, "n_symbols": int(n_symbols),
            "gamma_bar": float(GAMMA_BAR), "sop_rate": float(SOP_RATE),
            "mu": float(MU_SAFE), "n_tap": int(N_TAP),
            "late_slice": [LATE_START, LATE_END],
        },
        "methods": {
            "B0_standard_cma": evaluate_outputs(
                res_b0['zX'][late], res_b0['zY'][late], source_x, source_y,
                res_b0['diverged']),
            "B1_cma_identity_late": evaluate_outputs(
                zX_b1, zY_b1, source_x, source_y, res_b1['diverged']),
            "B2_per_block_ls": evaluate_outputs(
                zX_b2[late], zY_b2[late], source_x, source_y, False),
            "B3_cma_frozen_early": evaluate_outputs(
                zX_b3, zY_b3, source_x, source_y, res_b3_train['diverged']),
            "oracle": evaluate_outputs(
                oracle_x[late], oracle_y[late], source_x, source_y, False),
        },
        "artifacts": {
            "B0_standard_cma": {
                "diverged": res_b0['diverged'], "final_w_norm": float(res_b0['final_w_norm'])},
            "B1_cma_identity_late": {
                "diverged": res_b1['diverged'], "final_w_norm": float(res_b1['final_w_norm'])},
            "B3_cma_frozen_early": {
                "diverged": res_b3_train['diverged'],
                "final_w_norm": float(eq_b3._norm())},
        },
    }
    if ml_ok:
        trial["methods"]["ml_fixed"] = evaluate_outputs(
            zX_ml[late], zY_ml[late], source_x, source_y, False)

    # excess PI vs oracle
    oracle_pi = float(trial["methods"]["oracle"]["permutation_invariant_ber"]["mean"])
    for name in trial["methods"]:
        pi = float(trial["methods"][name]["permutation_invariant_ber"]["mean"])
        trial["methods"][name]["excess_pi_ber_vs_oracle"] = pi - oracle_pi

    return trial


def summarize_v1(trials):
    """汇总验证1 分解结果."""
    methods = ("B0_standard_cma", "B1_cma_identity_late", "B2_per_block_ls",
               "B3_cma_frozen_early", "oracle", "ml_fixed")
    summaries = {}
    for m in methods:
        vals = [float(t["methods"][m]["permutation_invariant_ber"]["mean"])
                for t in trials if m in t["methods"]]
        if not vals:
            continue
        fixed_vals = [float(t["methods"][m]["fixed_label_ber"]["mean"])
                      for t in trials if m in t["methods"]]
        excess = [float(t["methods"][m].get("excess_pi_ber_vs_oracle", 0.0))
                  for t in trials if m in t["methods"]]
        summaries[m] = {
            "pi_ber": {"mean": float(np.mean(vals)), "std": float(np.std(vals)),
                       "values": vals},
            "fixed_ber": {"mean": float(np.mean(fixed_vals)), "std": float(np.std(fixed_vals)),
                          "values": fixed_vals},
            "excess_pi_ber": {"mean": float(np.mean(excess)), "values": excess},
        }

    # 分解判定
    b0_pi = summaries.get("B0_standard_cma", {}).get("pi_ber", {}).get("mean", 0)
    b1_pi = summaries.get("B1_cma_identity_late", {}).get("pi_ber", {}).get("mean", 0)
    b2_pi = summaries.get("B2_per_block_ls", {}).get("pi_ber", {}).get("mean", 0)
    b3_pi = summaries.get("B3_cma_frozen_early", {}).get("pi_ber", {}).get("mean", 0)
    oracle_pi = summaries.get("oracle", {}).get("pi_ber", {}).get("mean", 0)
    ml_pi = summaries.get("ml_fixed", {}).get("pi_ber", {}).get("mean", 0)

    # PASS 标准: B0 >> B2 (残余 = 权重漂移非信息限制) 且 B1 接近 oracle (跟踪能力够)
    b0_vs_b2_ratio = b0_pi / max(b2_pi, 1e-6)
    b1_vs_oracle_ratio = b1_pi / max(oracle_pi, 1e-6)
    # 定位 B 成立条件: 残余主要来自权重漂移 (a), 非跟踪滞后 (b) 非瞬态 (c)
    # (a) B0 >> B2: CMA 远离 per-block 最优 = 权重漂移
    # (b) B1 接近 oracle: 从正确盆地跟踪 SOP, BER 低 = 跟踪能力够 (滞后不是主因)
    # (c) B3 (固定 early 权重): 若 B3 ≈ B0 则权重在 early 已锁定错解; 若 B3 < B0 则在线更新推坏
    pass_a = b0_vs_b2_ratio > 2.0   # CMA 远离 LS 最优 = 权重漂移显著
    pass_b = b1_vs_oracle_ratio < 3.0   # CMA 从正确盆地跟踪能力够

    verdict = "PASS" if (pass_a and pass_b) else "FAIL"

    return {
        "method_summaries": summaries,
        "decomposition": {
            "B0_pi": b0_pi, "B1_pi": b1_pi, "B2_pi": b2_pi, "B3_pi": b3_pi,
            "oracle_pi": oracle_pi, "ml_pi": ml_pi,
            "B0_vs_B2_ratio": b0_vs_b2_ratio,
            "B1_vs_oracle_ratio": b1_vs_oracle_ratio,
            "residual_source_interpretation": {
                "a_weight_drift_dominant": pass_a,
                "b_tracking_lag_minor": pass_b,
                "c_transient": "B3 vs B0 对比判断在线更新是否推坏",
            },
        },
        "verdict": verdict,
    }


# ═══════════════════════════════════════════════════════════
#  验证2: 改步长证否 (SOP×f_G 矩阵 × μ 扫描)
# ═══════════════════════════════════════════════════════════

def run_v2_stepsize_cell(seed, sop_rate, f_g, mu, n_symbols=N_SYMBOLS):
    """验证2: 单 cell (sop, f_g, mu) 的 CMA + oracle PI-BER."""
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        n_symbols, alpha, beta, f_g, sop_rate, int(seed))

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    eq = StandardCMA2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
    res = eq.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)

    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    cma_eval = evaluate_outputs(
        res['zX'][late], res['zY'][late], source_x, source_y, res['diverged'])
    oracle_eval = evaluate_outputs(
        oracle_x[late], oracle_y[late], source_x, source_y, False)

    return {
        "seed": int(seed),
        "sop_rate": float(sop_rate),
        "f_g": float(f_g),
        "mu": float(mu),
        "elapsed_s": time.time() - started,
        "cma_pi": float(cma_eval["permutation_invariant_ber"]["mean"]),
        "cma_fixed": float(cma_eval["fixed_label_ber"]["mean"]),
        "cma_diverged": bool(res['diverged']),
        "oracle_pi": float(oracle_eval["permutation_invariant_ber"]["mean"]),
        "cma_oracle_ratio": float(cma_eval["permutation_invariant_ber"]["mean"]
                                  / max(oracle_eval["permutation_invariant_ber"]["mean"], 1e-6)),
    }


def run_v2_stepsize_matrix(seeds, sops=SOP_VALUES, fgs=FG_VALUES, mus=MU_VALUES):
    """验证2: 完整 SOP×f_G×μ 矩阵."""
    results = {}
    total = len(sops) * len(fgs) * len(mus) * len(seeds)
    done = 0
    for sop in sops:
        for fg in fgs:
            for mu in mus:
                key = f"sop{sop}_fg{int(fg)}_mu{mu}"
                trials = []
                for seed in seeds:
                    t = run_v2_stepsize_cell(seed, sop, fg, mu)
                    trials.append(t)
                    done += 1
                    print(f"  [v2 {done}/{total}] sop={sop} fg={int(fg)} "
                          f"μ={mu} seed={seed}: ratio={t['cma_oracle_ratio']:.2f} "
                          f"cma_pi={t['cma_pi']:.4f} orc={t['oracle_pi']:.4f} "
                          f"div={t['cma_diverged']}", flush=True)
                pi_vals = [t["cma_pi"] for t in trials]
                orc_vals = [t["oracle_pi"] for t in trials]
                ratio_vals = [t["cma_oracle_ratio"] for t in trials]
                results[key] = {
                    "sop_rate": float(sop), "f_g": float(fg), "mu": float(mu),
                    "cma_pi_mean": float(np.mean(pi_vals)),
                    "cma_pi_std": float(np.std(pi_vals)),
                    "oracle_pi_mean": float(np.mean(orc_vals)),
                    "ratio_mean": float(np.mean(ratio_vals)),
                    "ratio_std": float(np.std(ratio_vals)),
                    "n_diverged": sum(1 for t in trials if t["cma_diverged"]),
                    "trials": trials,
                }
    return results


def summarize_v2(matrix_results):
    """验证2 判定: 步长能否消除 SOP 退化."""
    # 按 (sop, fg) 分组, 看不同 μ 下 ratio 是否能降到 SOP=0 水平
    by_cell = {}
    for key, v in matrix_results.items():
        cell = (v["sop_rate"], v["f_g"])
        by_cell.setdefault(cell, []).append((v["mu"], v["ratio_mean"]))

    # PASS: SOP=4e-7 下, 任何 μ 的 ratio 都 ≥ SOP=0 对应 ratio 的 1.5× (步长不消除退化)
    # FAIL: 存在某 μ 使 SOP=4e-7 ratio 接近 SOP=0 (步长可消除)
    verdict_analysis = []
    for fg in FG_VALUES:
        sop0_min_ratio = min(r for (mu, r) in by_cell.get((0.0, fg), [(0, 1)]))
        sop4_min_ratio = min(r for (mu, r) in by_cell.get((4e-7, fg), [(0, 999)]))
        best_mu_sop4 = [mu for (mu, r) in by_cell.get((4e-7, fg), [])
                        if r == sop4_min_ratio]
        eliminated = sop4_min_ratio < max(sop0_min_ratio * 1.5, 1.5)
        verdict_analysis.append({
            "f_g": fg,
            "sop0_min_ratio": float(sop0_min_ratio),
            "sop4_min_ratio": float(sop4_min_ratio),
            "best_mu_sop4": best_mu_sop4,
            "step_size_eliminated_sop_degradation": bool(eliminated),
        })

    # 整体: 任一 fg 下步长消除退化 → FAIL (B'类占点)
    any_eliminated = any(v["step_size_eliminated_sop_degradation"]
                         for v in verdict_analysis)
    verdict = "FAIL_QDP4" if any_eliminated else "PASS_stepsize_no_help"

    return {
        "by_cell_min_ratios": {str(k): v for k, v in by_cell.items()},
        "verdict_analysis": verdict_analysis,
        "verdict": verdict,
        "interpretation": (
            "PASS (步长不消除 SOP 退化 → 风险1 排除, B'类不占 Q-DP4)"
            if not any_eliminated else
            "FAIL (某步长消除 SOP 退化 → Q-DP4 增量被压缩)"
        ),
    }


# ═══════════════════════════════════════════════════════════
#  验证3: 形态2 预防性约束 — 仅 1+2 PASS 才做
# ═══════════════════════════════════════════════════════════

class CMAwithXCA(StandardCMA2x2):
    """Standard CMA + α·J_XCA (输出互相关惩罚) 持续运行版.

    J_XCA = |E[zX · zY*]|²  (CA-CMA 2025 互相关代价, R008 精读确认)
    梯度: ∂J_XCA/∂wxx ∝ E[zX* · zY] · ∂zX/∂wxx ... 简化为块均值互相关反推.
    持续运行 (非 CA-CMA 的预收敛后切换), 测能否防 swap.

    代价 = J_CM(zX) + J_CM(zY) + α·|E[zX·zY*]|²
    更新: w += μ·(grad_CM - α·grad_XCA)
    """

    def __init__(self, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK, alpha_xca=0.0):
        super().__init__(n_tap=n_tap, mu=mu, R2=R2)
        self.alpha_xca = alpha_xca

    def equalize(self, rX, rY, h_block_series=None, theta_series=None,
                 block_size=CMA_BLOCK_SIZE):
        """块级 CMA + J_XCA 均衡."""
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

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break

            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # CMA 梯度 (standard Godard): e = R² − |z|²
            eX = self.R2 - np.abs(zx_blk) ** 2
            eY = self.R2 - np.abs(zy_blk) ** 2
            grad_wxx = np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            grad_wxy = np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
            grad_wyx = np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
            grad_wyy = np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

            # J_XCA 梯度: J_XCA = |E[zX·zY*]|²
            #   ∂J_XCA/∂wxx = 2·Re(E[zX·zY*]) · ∂Re(E[zX·zY*])/∂wxx ...
            #   简化 (块均值): c = mean(zx · conj(zy)); 惩罚方向 = 推 zX 远离 zY
            #   grad_XCA_wxx = c* · conj(rX_blk) 均值 (推 zX), 对 wyx 加 c · conj(rX) (推 zY 远)
            c = np.mean(zx_blk * np.conj(zy_blk))   # 复互相关
            # ∂(zx·conj(zy))/∂wxx = rX · conj(zy) → grad on wxx
            grad_xca_wxx = np.mean(np.conj(zy_blk)[:, None] * np.conj(rX_blk), axis=0) * c
            grad_xca_wxy = np.mean(np.conj(zy_blk)[:, None] * np.conj(rY_blk), axis=0) * c
            # ∂(zx·conj(zy))/∂wyx = zx · conj(rX) → 对 wyx
            grad_xca_wyx = np.mean(zx_blk)[:, None] * np.conj(rX_blk) if False else \
                np.mean(np.broadcast_to(zx_blk[:, None], (block_size, L)) * np.conj(rX_blk), axis=0) * np.conj(c)
            grad_xca_wyy = np.mean(np.broadcast_to(zx_blk[:, None], (block_size, L)) * np.conj(rY_blk), axis=0) * np.conj(c)

            # 合并更新 (J_XCA 对 wxx/wxy 用 +α·c·conj(zy)·conj(rX) 方向 = 增大 |c| 时惩罚)
            self.wxx += self.mu * (grad_wxx - self.alpha_xca * grad_xca_wxx)
            self.wxy += self.mu * (grad_wxy - self.alpha_xca * grad_xca_wxy)
            self.wyx += self.mu * (grad_wyx - self.alpha_xca * grad_xca_wyx)
            self.wyy += self.mu * (grad_wyy - self.alpha_xca * grad_xca_wyy)

            # 发散检测
            cur_norm = self._norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        return {
            'zX': zX, 'zY': zY,
            'diverged': diverged, 'diverge_idx': diverge_idx,
            'final_w_norm': self._norm(), 'init_w_norm': self._init_norm,
        }


class CMAwithDiagConstraint(StandardCMA2x2):
    """Standard CMA + α·J_diag (交叉 FIR 权重惩罚) 防跳变约束.

    关键发现 (V3 初测): J_XCA (输出互相关) 对 clean swap 无效 — swap 时 zX=sY, zY=sX
    仍是独立 QPSK, 互相关≈0, J_XCA 梯度≈0. CA-CMA J_XCA 是为静态 same-source singularity
    设计 (两输出锁同一源, 高互相关), 不适合 SOP 驱动的 clean swap.

    正确机制: 惩罚交叉 FIR 权重 wxy/wyx (非对角项). swap 的物理 = wxy/wyx 从 0 增长
    到与 wxx/wyy 可比 (X 路开始从 rY 取信号). 约束交叉权重小 = 强制对角优势 = 防 swap.

    J_diag = ||wxy||² + ||wyx||²  (交叉 FIR L2 惩罚)
    梯度: ∂J_diag/∂wxy = 2·wxy; ∂J_diag/∂wyx = 2·wyx (简单, 不依赖输入)
    更新: wxy += μ·(grad_CM_wxy - α·2·wxy); wyx += μ·(grad_CM_wyx - α·2·wyx)
    wxx/wyy 不受约束 (保持对角自由度跟踪 SOP 相位).
    """

    def __init__(self, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK, alpha_diag=0.0):
        super().__init__(n_tap=n_tap, mu=mu, R2=R2)
        self.alpha_diag = alpha_diag

    def equalize(self, rX, rY, h_block_series=None, theta_series=None,
                 block_size=CMA_BLOCK_SIZE):
        """块级 CMA + J_diag 约束均衡."""
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

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break

            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # CMA 梯度 (standard Godard)
            eX = self.R2 - np.abs(zx_blk) ** 2
            eY = self.R2 - np.abs(zy_blk) ** 2
            self.wxx += self.mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * (np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
                                    - self.alpha_diag * 2 * self.wxy)
            self.wyx += self.mu * (np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
                                    - self.alpha_diag * 2 * self.wyx)
            self.wyy += self.mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

            cur_norm = self._norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        return {
            'zX': zX, 'zY': zY,
            'diverged': diverged, 'diverge_idx': diverge_idx,
            'final_w_norm': self._norm(), 'init_w_norm': self._init_norm,
            'final_wxy_norm': float(np.linalg.norm(self.wxy)),
            'final_wyx_norm': float(np.linalg.norm(self.wyx)),
        }


def run_v3_constraint_trial(seed, alpha, constraint_type='diag', f_g=F_G_PRIMARY):
    """验证3: 单 seed × α × 约束类型 trial.

    constraint_type: 'xca' = J_XCA 输出互相关 (CA-CMA 机制, 预期对 clean swap 无效)
                     'diag' = J_diag 交叉 FIR 权重惩罚 (正确机制, 防 swap)
    """
    started = time.time()
    cfg = SimulationConfig()
    alpha_turb, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha_turb, beta, f_g, SOP_RATE, int(seed))

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    if constraint_type == 'xca':
        eq = CMAwithXCA(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK, alpha_xca=alpha)
    else:
        eq = CMAwithDiagConstraint(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK, alpha_diag=alpha)
    res = eq.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)

    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    cma_eval = evaluate_outputs(
        res['zX'][late], res['zY'][late], source_x, source_y, res['diverged'])
    oracle_eval = evaluate_outputs(
        oracle_x[late], oracle_y[late], source_x, source_y, False)

    result = {
        "seed": int(seed),
        "alpha": float(alpha),
        "constraint_type": constraint_type,
        "elapsed_s": time.time() - started,
        "pi_ber": float(cma_eval["permutation_invariant_ber"]["mean"]),
        "fixed_ber": float(cma_eval["fixed_label_ber"]["mean"]),
        "classification": cma_eval.get("classification", "unknown"),
        "diverged": bool(res['diverged']),
        "oracle_pi": float(oracle_eval["permutation_invariant_ber"]["mean"]),
        "abs_corr_zX_zY": float(cma_eval.get("abs_corr_zX_zY", 0.0)),
    }
    if constraint_type == 'diag':
        result["final_wxy_norm"] = float(res.get('final_wxy_norm', 0))
        result["final_wyx_norm"] = float(res.get('final_wyx_norm', 0))
    return result
    """验证3: 单 seed × α 的 J_XCA 约束 trial."""
    started = time.time()
    cfg = SimulationConfig()
    alpha_turb, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha_turb, beta, f_g, SOP_RATE, int(seed))

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    eq = CMAwithXCA(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK, alpha_xca=alpha)
    res = eq.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)

    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    cma_eval = evaluate_outputs(
        res['zX'][late], res['zY'][late], source_x, source_y, res['diverged'])
    oracle_eval = evaluate_outputs(
        oracle_x[late], oracle_y[late], source_x, source_y, False)

    return {
        "seed": int(seed),
        "alpha_xca": float(alpha),
        "elapsed_s": time.time() - started,
        "pi_ber": float(cma_eval["permutation_invariant_ber"]["mean"]),
        "fixed_ber": float(cma_eval["fixed_label_ber"]["mean"]),
        "classification": cma_eval.get("classification", "unknown"),
        "diverged": bool(res['diverged']),
        "oracle_pi": float(oracle_eval["permutation_invariant_ber"]["mean"]),
        "abs_corr_zX_zY": float(cma_eval.get("abs_corr_zX_zY", 0.0)),
    }


def run_v3_xca_sweep(seeds, alphas=(0.0, 0.1, 0.5, 1.0), constraint_type='diag'):
    """验证3: α 扫 {0, 0.1, 0.5, 1.0}, constraint_type ∈ {'diag', 'xca'}."""
    results = {}
    total = len(alphas) * len(seeds)
    done = 0
    for alpha in alphas:
        trials = []
        for seed in seeds:
            t = run_v3_constraint_trial(seed, alpha, constraint_type=constraint_type)
            trials.append(t)
            done += 1
            extra = ""
            if constraint_type == 'diag':
                extra = f" wxy={t.get('final_wxy_norm',0):.3f}"
            print(f"  [v3 {constraint_type} {done}/{total}] α={alpha} seed={seed}: "
                  f"pi={t['pi_ber']:.4f} class={t['classification']} "
                  f"div={t['diverged']} corr_zXzY={t['abs_corr_zX_zY']:.3f}{extra}", flush=True)
        pi_vals = [t["pi_ber"] for t in trials]
        swap_count = sum(1 for t in trials if "swap" in t["classification"])
        results[f"alpha_{alpha}"] = {
            "alpha": float(alpha),
            "constraint_type": constraint_type,
            "pi_ber_mean": float(np.mean(pi_vals)),
            "pi_ber_std": float(np.std(pi_vals)),
            "pi_ber_values": pi_vals,
            "fixed_ber_mean": float(np.mean([t["fixed_ber"] for t in trials])),
            "swap_count": swap_count,
            "swap_fraction": float(swap_count / len(seeds)),
            "n_diverged": sum(1 for t in trials if t["diverged"]),
            "mean_corr_zX_zY": float(np.mean([t["abs_corr_zX_zY"] for t in trials])),
            "trials": trials,
        }
    return results


def summarize_v3(xca_results):
    """验证3 判定."""
    alpha0_pi = xca_results.get("alpha_0.0", {}).get("pi_ber_mean", 0)
    best_alpha = None
    best_pi = alpha0_pi
    for key, v in xca_results.items():
        if v["alpha"] > 0 and v["pi_ber_mean"] < best_pi:
            best_pi = v["pi_ber_mean"]
            best_alpha = v["alpha"]

    # PASS: α>0 时 swap 概率↓ + PI-BER↓ (至少降 2×) + 不发散
    improvement_ratio = alpha0_pi / max(best_pi, 1e-6) if best_alpha else 1.0
    alpha0_swap = xca_results.get("alpha_0.0", {}).get("swap_fraction", 0)
    best_swap = xca_results.get(f"alpha_{best_alpha}", {}).get("swap_fraction", 1) if best_alpha else 1
    best_diverged = xca_results.get(f"alpha_{best_alpha}", {}).get("n_diverged", 0) if best_alpha else 0

    pass_criteria = (best_alpha is not None and improvement_ratio >= 2.0
                     and best_swap < alpha0_swap and best_diverged == 0)
    verdict = "PASS" if pass_criteria else "FAIL"

    return {
        "alpha0_pi": alpha0_pi,
        "best_alpha": best_alpha,
        "best_pi": best_pi,
        "improvement_ratio": float(improvement_ratio),
        "alpha0_swap_fraction": alpha0_swap,
        "best_swap_fraction": best_swap,
        "verdict": verdict,
        "interpretation": (
            f"PASS: α={best_alpha} 降 PI-BER {improvement_ratio:.1f}× + 降 swap + 无发散"
            if pass_criteria else
            f"FAIL: J_XCA 约束未达 2× 改善或伤跟踪/引噪声 (最佳 α={best_alpha}, ratio={improvement_ratio:.1f})"
        ),
    }


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def main(argv=None):
    parser = argparse.ArgumentParser(description='PROMPT-020: Q-DP4 维度 D MVE')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 seed, 500K symbols)')
    parser.add_argument('--v1-only', action='store_true',
                        help='只跑验证1 (Go/Kill hinge)')
    parser.add_argument('--v2-only', action='store_true',
                        help='只跑验证2 (改步长证否)')
    parser.add_argument('--v3-only', action='store_true',
                        help='只跑验证3 (J_XCA, 须 1+2 PASS)')
    parser.add_argument('--no-ml', action='store_true',
                        help='跳过 ML (D022 已知 ML PI≈0.00523), 加速 V1')
    parser.add_argument('--seeds', nargs='*', type=int, default=None)
    args = parser.parse_args(argv)

    t_global = time.time()

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (验证实现正确性, 1 seed 500K)")
        print("=" * 60)
        global LATE_START, LATE_END, N_SYMBOLS
        n_sym = 500_000
        LATE_START = int(n_sym * 0.875)
        LATE_END = n_sym
        N_SYMBOLS = n_sym
        seeds = [1000]
        # smoke: 只验证1 快速
        print("\n--- V1 smoke ---")
        trials = [run_v1_decomposition(s, n_symbols=n_sym) for s in seeds]
        s1 = summarize_v1(trials)
        print(f"V1 verdict: {s1['verdict']}")
        for m, v in s1["method_summaries"].items():
            print(f"  {m}: pi={v['pi_ber']['mean']:.4f}")
        return

    seeds = args.seeds or SEEDS_5
    payload = {
        "experiment": "PROMPT-020 Q-DP4 dimension D MVE",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "params": {
            "f_g_primary": F_G_PRIMARY, "turbulence": TURBULENCE,
            "n_symbols": N_SYMBOLS, "gamma_bar": GAMMA_BAR,
            "sop_rate": SOP_RATE, "mu_safe": MU_SAFE, "n_tap": N_TAP,
            "late_slice": [LATE_START, LATE_END],
            "seeds": seeds,
        },
        "tl20_expectations": {
            "v1": "B0(0.03174) >> B2(≈oracle) + B1接近oracle → 残余=权重漂移(a) → 定位B成立",
            "v2": "FAIL (步长不消除SOP退化) → 风险1排除, B'类不占Q-DP4",
            "v3": "不确定/谨慎 (CA-CMA自承J_XCA引噪声; 小α可能适度降swap, 大α伤跟踪)",
        },
    }

    run_v1 = not (args.v2_only or args.v3_only)
    run_v2 = not (args.v1_only or args.v3_only)
    run_v3 = args.v3_only or (not (args.v1_only or args.v2_only))

    # ── 验证1: 6× PI-BER 差距分解 (Go/Kill hinge) ──
    if run_v1:
        print("=" * 60)
        print(f"PROMPT-020 验证1: 6× PI-BER 差距来源分解 ({len(seeds)} seeds)")
        print(f"参数: f_G={F_G_PRIMARY}, SOP={SOP_RATE}, N={N_SYMBOLS}, μ={MU_SAFE}")
        print("=" * 60)
        t1 = time.time()
        v1_trials = []
        for i, seed in enumerate(seeds):
            print(f"\n[v1 seed {seed} {i+1}/{len(seeds)}] running...")
            t = run_v1_decomposition(seed, run_ml=not args.no_ml)
            v1_trials.append(t)
            ms = t["methods"]
            print(f"  B0(stdCMA)={ms['B0_standard_cma']['permutation_invariant_ber']['mean']:.4f}  "
                  f"B1(identity)={ms['B1_cma_identity_late']['permutation_invariant_ber']['mean']:.4f}  "
                  f"B2(LS)={ms['B2_per_block_ls']['permutation_invariant_ber']['mean']:.4f}  "
                  f"B3(frozen)={ms['B3_cma_frozen_early']['permutation_invariant_ber']['mean']:.4f}  "
                  f"oracle={ms['oracle']['permutation_invariant_ber']['mean']:.4f}  "
                  f"[{t['elapsed_s']:.0f}s]")
        v1_summary = summarize_v1(v1_trials)
        payload["v1_decomposition"] = {"trials": v1_trials, "summary": v1_summary,
                                       "elapsed_s": time.time() - t1}
        print(f"\nV1 判定: {v1_summary['verdict']}")
        d = v1_summary["decomposition"]
        print(f"  B0={d['B0_pi']:.4f} B1={d['B1_pi']:.4f} B2={d['B2_pi']:.4f} "
              f"B3={d['B3_pi']:.4f} oracle={d['oracle_pi']:.4f}")
        print(f"  B0/B2={d['B0_vs_B2_ratio']:.1f}× B1/oracle={d['B1_vs_oracle_ratio']:.1f}×")

    # ── 验证2: 改步长证否 (SOP×f_G 矩阵) ──
    if run_v2:
        print("\n" + "=" * 60)
        print(f"PROMPT-020 验证2: 改步长证否 (SOP×f_G×μ, {len(seeds)} seeds)")
        print("=" * 60)
        t2 = time.time()
        v2_matrix = run_v2_stepsize_matrix(seeds)
        v2_summary = summarize_v2(v2_matrix)
        payload["v2_stepsize"] = {"matrix": v2_matrix, "summary": v2_summary,
                                  "elapsed_s": time.time() - t2}
        print(f"\nV2 判定: {v2_summary['verdict']}")
        for va in v2_summary["verdict_analysis"]:
            print(f"  fg={va['f_g']}: sop0_min={va['sop0_min_ratio']:.2f} "
                  f"sop4_min={va['sop4_min_ratio']:.2f} "
                  f"eliminated={va['step_size_eliminated_sop_degradation']}")

    # ── 验证3: J_XCA (仅 1+2 PASS 或 --v3-only) ──
    if run_v3:
        # 检查前置: 1+2 是否 PASS (除非 --v3-only 强制)
        if not args.v3_only:
            v1_pass = payload.get("v1_decomposition", {}).get("summary", {}).get("verdict") == "PASS"
            v2_pass = "PASS" in payload.get("v2_stepsize", {}).get("summary", {}).get("verdict", "")
            if not (v1_pass and v2_pass):
                print("\n" + "=" * 60)
                print("验证3 跳过: 验证1 或 验证2 未 PASS (前置门控)")
                print(f"  V1={payload.get('v1_decomposition',{}).get('summary',{}).get('verdict','N/A')} "
                      f"V2={payload.get('v2_stepsize',{}).get('summary',{}).get('verdict','N/A')}")
                print("  (用 --v3-only 强制跑验证3)")
                payload["v3_xca"] = {"skipped": True,
                                     "reason": "v1 or v2 not PASS"}
            else:
                run_v3 = True
            if not (v1_pass and v2_pass):
                run_v3 = False

        if run_v3:
            print("\n" + "=" * 60)
            print(f"PROMPT-020 验证3: J_XCA 防跳变约束 (α sweep, {len(seeds)} seeds)")
            print("=" * 60)
            t3 = time.time()
            v3_results = run_v3_xca_sweep(seeds)
            v3_summary = summarize_v3(v3_results)
            payload["v3_xca"] = {"sweep": v3_results, "summary": v3_summary,
                                 "elapsed_s": time.time() - t3}
            print(f"\nV3 判定: {v3_summary['verdict']}")
            print(f"  {v3_summary['interpretation']}")

    payload["elapsed_s"] = time.time() - t_global

    # ── 保存 ──
    out_path = RESULT_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果保存: {out_path}")
    print(f"总耗时: {payload['elapsed_s']:.0f}s")

    # ── 汇总打印 ──
    print("\n" + "=" * 60)
    print("PROMPT-020 Q-DP4 维度 D MVE 汇总")
    print("=" * 60)
    if "v1_decomposition" in payload:
        v1 = payload["v1_decomposition"]["summary"]
        print(f"验证1 (6×差距分解): {v1['verdict']}")
    if "v2_stepsize" in payload:
        v2 = payload["v2_stepsize"]["summary"]
        print(f"验证2 (改步长证否): {v2['verdict']}")
    if "v3_xca" in payload and not payload["v3_xca"].get("skipped"):
        v3 = payload["v3_xca"]["summary"]
        print(f"验证3 (J_XCA约束): {v3['verdict']}")

    return payload


if __name__ == '__main__':
    main()
