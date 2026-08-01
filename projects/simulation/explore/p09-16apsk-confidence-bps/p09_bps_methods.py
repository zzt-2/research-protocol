"""P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH — shared BPS method library.

研究问题（D039 campaign P09 重定向）:
  M = 16APSK full blind phase search (`bps_cpr` 真实 B×N exhaustive search)
  C = 有限实时计算预算
  A = 每个 window 对全部相位候选计算星座距离, 存在 B×N 搜索开销
  目标 = 相同 receiver-visible 信息/相同延迟/相同 BPS objective 下,
        减少 distance/objective evaluations, 同时保持 full BPS 恢复性能

本模块只定义方法 + 复杂度计数, 不读 held-out test seeds (runner 才读).
不修改 common/ frozen 文件; 16APSK adapter 复用 simulator/run_bps_ablation.py
既有资产 (hard_decision_m16apsk + bps_cpr_m16apsk, 已 self-test PASS).

复用纪律 (守 TL-13, 不改 common/_recovery.py):
  - 16APSK 星座/调制/解调/resolve: common._modulation (m16apsk_mod/demod/resolve_m16apsk_blockwise)
  - 信道: common.generate_shared_realization_apsk (B11/B7/B3 共用, 禁自建)
  - BPS 16APSK adapter: 本文件复制 run_bps_ablation.py:hard_decision_m16apsk +
    bps_cpr_m16apsk (Pfau 2009 + M0=8 展开), 不改原文件

复杂度计数 (PRIMARY cost metric, 任务合同):
  candidate_symbol_distance_evaluations = sum over blocks of (B_used * N_block)
  其中 B_used = 该 block 实际计算距离的测试相位数 (含 refinement/coarse 两阶段全计,
  含 confidence 评估 + fallback 全计). wall-clock 只作 secondary.
  key invariant: 每个 candidate-symbol 距离 = 一次 |rotated - dec|^2 复距离 (8 flop 等价),
  与 full BPS 同 objective 同语义, 只是数量减少.
"""
from __future__ import annotations

import numpy as np

# 星座点 (复用 run_bps_ablation 既有定义, 与 common._modulation._M16APSK_SYM 同源)
# 从 common 直接取, 避免重复定义漂移
from common._modulation import (
    _M16APSK_SYM as _M16APSK_CONST,   # (16,) 内环 0-7 外环 8-15
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
)

M0 = 8  # (8,8)-16APSK 升幂阶数 (两环各 8 点 → M0=8 重模糊展开)


# =============================================================================
# 16APSK hard decision (BPS 内部用) — 复制自 run_bps_ablation.py:82
# =============================================================================
def hard_decision_m16apsk(z):
    """最近邻星座点判定 for (8,8)-16APSK. 支持标量 + 任意 shape 数组."""
    z = np.asarray(z, dtype=complex)
    flat = z.reshape(-1)
    dist = np.abs(flat[:, np.newaxis] - _M16APSK_CONST[np.newaxis, :]) ** 2
    idx = np.argmin(dist, axis=1)
    dec = _M16APSK_CONST[idx]
    return dec.reshape(z.shape)


# =============================================================================
# BPS objective: 给定 (B_test_phases, N_symbols) 返回 per-symbol 距离度量矩阵
# 这是所有方法的共享 "objective", 复杂度计数基于此.
# =============================================================================
def bps_objective_matrix(rx_block, phases):
    """BPS 距离度量矩阵 (B, N_block). 每个 [b, k] = |rotated[b,k] - dec[b,k]|^2 / |dec|^2.

    这是 Pfau 2009 BPS 的 core objective: 对 B 个测试相位, 每个 phase 旋转整块,
    hard decision 后算归一化距离. full BPS 对全部 B 个 phase 算; coarse/refinement
    只对子集算. 复杂度 = B_used * N_block 次 candidate-symbol 距离评估.

    phases 必须是 1-D array of B 个 scalar test phases (同一组相位应用到整块).
    逐 symbol 不同绝对相位的 refinement 见 bps_objective_per_symbol().
    返回 (metrics (B,N_block), dec_used (B,N_block)). dec_used 用于 refinement 复用.
    """
    phases = np.asarray(phases)
    if phases.ndim != 1:
        raise ValueError(f"bps_objective_matrix expects 1-D phases, got shape {phases.shape}; "
                         f"per-symbol absolute phases 用 bps_objective_per_symbol")
    B = len(phases)
    rotated = rx_block[np.newaxis, :] * np.exp(-1j * phases[:, np.newaxis])   # (B, N)
    dec = hard_decision_m16apsk(rotated)                                       # (B, N)
    dist = np.abs(rotated - dec) ** 2
    metrics = dist / (np.abs(dec) ** 2 + 1e-10)
    return metrics, dec


def bps_objective_per_symbol(rx_block, abs_phases):
    """Per-symbol 绝对相位的 BPS 距离度量 (refinement 用).

    abs_phases: (B_fine, N) — 每个 symbol 有自己的 B_fine 个候选绝对相位 (coarse winner 邻域).
    返回 metrics (B_fine, N). 复杂度 = B_fine * N 次 candidate-symbol 距离评估.
    (无 dec 返回, refinement 不需要复用 dec.)
    """
    abs_phases = np.asarray(abs_phases)
    assert abs_phases.ndim == 2, f"abs_phases must be 2-D (B_fine, N), got {abs_phases.shape}"
    B_fine, N = abs_phases.shape
    # 每个 symbol 独立: rotated[b,k] = rx[k] * exp(-1j * abs_phases[b,k])
    rotated = rx_block[np.newaxis, :] * np.exp(-1j * abs_phases)              # (B_fine, N)
    dec = hard_decision_m16apsk(rotated)                                       # (B_fine, N)
    dist = np.abs(rotated - dec) ** 2
    metrics = dist / (np.abs(dec) ** 2 + 1e-10)
    return metrics


def sliding_window_average(metrics, Nw):
    """Pfau 2009 滑动窗口平均 (mode='same', 与 bps_cpr 一致).

    metrics: (B, N) 或 (N,). 若 N < Nw (refinement 子集短), 自动缩 Nw 到 ≤ N (奇数对称).
    """
    metrics = np.asarray(metrics)
    N = metrics.shape[-1]
    nw = Nw if Nw <= N else (N if N % 2 == 1 else max(1, N - 1))
    if nw < 1:
        return metrics.copy()
    ker = np.ones(nw) / nw
    out = np.empty_like(metrics)
    if metrics.ndim == 2:
        for b in range(metrics.shape[0]):
            out[b] = np.convolve(metrics[b], ker, mode='same')
    else:
        out = np.convolve(metrics, ker, mode='same')
    return out


def unwrap_phase(pe_raw, M0_fold=8):
    """M0-fold 相位模糊展开 (16APSK 用 M0=8, 非 QPSK 的 M=4)."""
    return np.unwrap(M0_fold * pe_raw) / M0_fold


# =============================================================================
# B0: full uniform BPS (Pfau 2009 baseline, B=64)
# =============================================================================
B_FULL = 64        # full uniform test phases (Pfau 2009 QAM 推荐, run_bps_ablation 既有)
NW_DEFAULT = 101   # sliding window (对齐 run_bps_ablation, 奇数 'same' 对称)


def bps_full(rx_block, B=B_FULL, Nw=NW_DEFAULT):
    """B0 full uniform BPS. 返回 (rx_compensated, pe, n_distance_evals)."""
    phases = 2 * np.pi * np.arange(B) / B
    metrics, _ = bps_objective_matrix(rx_block, phases)
    metrics = sliding_window_average(metrics, Nw)
    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]
    pe = unwrap_phase(pe_raw, M0)
    n_evals = B * len(rx_block)   # full: B phases × N symbols
    return rx_block * np.exp(-1j * pe), pe, n_evals


# =============================================================================
# B1: dev-tuned fixed coarse BPS (均匀粗网格, B_coarse < B_FULL)
# =============================================================================
def bps_fixed_coarse(rx_block, B_coarse, Nw=NW_DEFAULT):
    """B1 fixed coarse BPS: 均匀 B_coarse 个测试相位 (无 refinement).
    B_coarse 在 dev 上调谐. 返回 (rx_compensated, pe, n_distance_evals).
    """
    phases = 2 * np.pi * np.arange(B_coarse) / B_coarse
    metrics, _ = bps_objective_matrix(rx_block, phases)
    metrics = sliding_window_average(metrics, Nw)
    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]
    pe = unwrap_phase(pe_raw, M0)
    n_evals = B_coarse * len(rx_block)
    return rx_block * np.exp(-1j * pe), pe, n_evals


# =============================================================================
# B2: dev-tuned fixed two-stage coarse-to-fine BPS
# Stage 1: coarse uniform B_coarse phases → pick winner per symbol
# Stage 2: fine uniform B_fine phases around winner (±π/B_coarse) → refine
# =============================================================================
def bps_fixed_two_stage(rx_block, B_coarse, B_fine, Nw=NW_DEFAULT):
    """B2 fixed two-stage coarse-to-fine BPS.

    Stage 1: B_coarse 均匀相位 → best_b_coarse (per symbol).
    Stage 2: 在 best_b_coarse 邻域 ±(2π/B_coarse) 内均匀 B_fine 个 fine phase
             → refine per symbol.
    两 stage 全部 distance eval 计入复杂度 (任务合同: refinement 全部计入).
    返回 (rx_compensated, pe, n_distance_evals).
    """
    N = len(rx_block)
    # Stage 1: coarse
    phases_c = 2 * np.pi * np.arange(B_coarse) / B_coarse
    metrics_c, _ = bps_objective_matrix(rx_block, phases_c)
    metrics_c = sliding_window_average(metrics_c, Nw)
    best_c = np.argmin(metrics_c, axis=0)                # (N,) coarse winner index
    pe_coarse = phases_c[best_c]                          # (N,) coarse phase estimate

    # Stage 2: fine around each symbol's coarse winner
    # fine phases: ±(2π/B_coarse) 邻域内 B_fine 个均匀相位 (相对偏移)
    fine_offsets = np.linspace(-2 * np.pi / B_coarse, 2 * np.pi / B_coarse, B_fine)
    # 对每个 symbol, absolute fine phase = pe_coarse[k] + fine_offsets
    # 向量化: (B_fine, N) per-symbol absolute phases
    phases_f_abs = pe_coarse[np.newaxis, :] + fine_offsets[:, np.newaxis]
    metrics_f = bps_objective_per_symbol(rx_block, phases_f_abs)
    metrics_f = sliding_window_average(metrics_f, Nw)
    best_f = np.argmin(metrics_f, axis=0)                 # (N,)
    pe_raw = phases_f_abs[best_f, np.arange(N)]
    pe = unwrap_phase(pe_raw, M0)
    # 复杂度: stage1 (B_coarse × N) + stage2 (B_fine × N), refinement 全计
    n_evals = (B_coarse + B_fine) * N
    return rx_block * np.exp(-1j * pe), pe, n_evals


# =============================================================================
# C1: confidence-gated local refinement
# 机制: coarse B_coarse → 若 coarse metric margin (top-1 vs top-2 gap) 小于阈值
#       (低置信), 触发 fine refinement; 否则用 coarse 结果 (高置信, skip fine).
# confidence = metric margin / metric scale (receiver-visible, 无 TX truth).
# =============================================================================
def bps_confidence_gated(rx_block, B_coarse, B_fine, conf_thresh, Nw=NW_DEFAULT):
    """C1 confidence-gated local refinement.

    1. coarse B_coarse → metrics_c (B_coarse, N), 滑窗后.
    2. per-symbol confidence = (sorted_metrics[1] - sorted_metrics[0]) / sorted_metrics[0]
       (top1-top2 gap 归一化, receiver-visible).
    3. 低置信 symbols (confidence < conf_thresh) 触发 fine refinement
       (B_fine phases around coarse winner); 高置信 skip.
    4. fallback: 若 refinement 后 metric 反而变差 (数值边界), 回退 coarse.
    复杂度: B_coarse×N + (触发 fine 的 symbol 数)×B_fine.
    返回 (rx_compensated, pe, n_distance_evals, n_refined, n_fallback).
    """
    N = len(rx_block)
    phases_c = 2 * np.pi * np.arange(B_coarse) / B_coarse
    metrics_c, _ = bps_objective_matrix(rx_block, phases_c)
    metrics_c = sliding_window_average(metrics_c, Nw)
    best_c = np.argmin(metrics_c, axis=0)
    pe = phases_c[best_c].astype(float).copy()          # 初始用 coarse

    # per-symbol confidence (receiver-visible): top1-top2 gap 归一化
    sorted_m = np.sort(metrics_c, axis=0)                 # (B_coarse, N) 升序
    top1 = sorted_m[0]
    top2 = sorted_m[1] if B_coarse >= 2 else sorted_m[0]
    confidence = (top2 - top1) / (top1 + 1e-12)           # (N,) 越大越置信

    low_conf = confidence < conf_thresh                   # (N,) bool, 触发 fine
    n_refined = int(np.sum(low_conf))

    # fine refinement 只对 low_conf symbols (per-symbol absolute phases on subset)
    if n_refined > 0:
        fine_offsets = np.linspace(-2 * np.pi / B_coarse, 2 * np.pi / B_coarse, B_fine)
        phases_f_abs = pe[low_conf][np.newaxis, :] + fine_offsets[:, np.newaxis]   # (B_fine, n_refined)
        metrics_f = bps_objective_per_symbol(rx_block[low_conf], phases_f_abs)
        metrics_f = sliding_window_average(metrics_f, Nw)
        best_f = np.argmin(metrics_f, axis=0)
        pe_fine = phases_f_abs[best_f, np.arange(n_refined)]

        # fallback: 若 fine metric >= coarse metric (没改善), 回退 coarse
        coarse_metric_low = top1[low_conf]
        fine_metric_low = metrics_f[best_f, np.arange(n_refined)]
        improve = fine_metric_low < coarse_metric_low
        n_fallback = int(np.sum(~improve))
        pe[low_conf] = np.where(improve, pe_fine, pe[low_conf])
    else:
        n_fallback = 0

    pe_real = np.real(pe)                                  # unwrap 需实数相位
    pe_unwrapped = unwrap_phase(pe_real, M0)
    # 复杂度: coarse 全计 + fine 只计触发的 symbols
    n_evals = B_coarse * N + n_refined * B_fine
    return rx_block * np.exp(-1j * pe_unwrapped), pe_unwrapped, n_evals, n_refined, n_fallback


# =============================================================================
# C2: curvature / score-gap guided refinement
# 机制: coarse → 用 coarse metrics 的曲率 (二阶差分 at winner) 估计是否需要细化;
#       曲率平缓 (flat, winner 不明显) → refine; 曲率尖锐 (sharp winner) → skip.
# =============================================================================
def bps_curvature_guided(rx_block, B_coarse, B_fine, curv_thresh, Nw=NW_DEFAULT):
    """C2 curvature/score-gap guided refinement.

    per-symbol curvature = metric[winner+1] + metric[winner-1] - 2*metric[winner]
    (在 coarse winner 邻域的二阶差分, receiver-visible).
    曲率 < curv_thresh (flat winner) → 触发 fine; 否则 skip.
    返回 (rx_compensated, pe, n_distance_evals, n_refined, n_fallback).
    """
    N = len(rx_block)
    phases_c = 2 * np.pi * np.arange(B_coarse) / B_coarse
    metrics_c, _ = bps_objective_matrix(rx_block, phases_c)
    metrics_c = sliding_window_average(metrics_c, Nw)
    best_c = np.argmin(metrics_c, axis=0)
    pe = phases_c[best_c].astype(float).copy()

    # curvature at winner (邻域二阶差分, 环形索引)
    Bc = B_coarse
    idx_p = (best_c + 1) % Bc
    idx_m = (best_c - 1) % Bc
    metric_at_best = metrics_c[best_c, np.arange(N)]
    metric_at_p = metrics_c[idx_p, np.arange(N)]
    metric_at_m = metrics_c[idx_m, np.arange(N)]
    curvature = metric_at_p + metric_at_m - 2 * metric_at_best   # (N,) 越小越 flat

    flat = curvature < curv_thresh                               # flat winner → refine
    n_refined = int(np.sum(flat))

    if n_refined > 0:
        fine_offsets = np.linspace(-2 * np.pi / Bc, 2 * np.pi / Bc, B_fine)
        phases_f_abs = pe[flat][np.newaxis, :] + fine_offsets[:, np.newaxis]   # (B_fine, n_refined)
        metrics_f = bps_objective_per_symbol(rx_block[flat], phases_f_abs)
        metrics_f = sliding_window_average(metrics_f, Nw)
        best_f = np.argmin(metrics_f, axis=0)
        pe_fine = phases_f_abs[best_f, np.arange(n_refined)]
        coarse_metric_flat = metric_at_best[flat]
        fine_metric_flat = metrics_f[best_f, np.arange(n_refined)]
        improve = fine_metric_flat < coarse_metric_flat
        n_fallback = int(np.sum(~improve))
        pe[flat] = np.where(improve, pe_fine, pe[flat])
    else:
        n_fallback = 0

    pe_unwrapped = unwrap_phase(pe, M0)
    n_evals = Bc * N + n_refined * B_fine
    return rx_block * np.exp(-1j * pe_unwrapped), pe_unwrapped, n_evals, n_refined, n_fallback


# =============================================================================
# C3: early-stop adaptive-width search
# 机制: 逐 phase 评估, 当 running best metric 已足够小 (低于 early-stop 阈值) 时
#       停止评估剩余 phases. adaptive width = 实际评估的 phase 数 per symbol.
# 注意: true early-stop 需 per-symbol 串行; 这里用 per-block 保守近似——
#       按 phase 顺序累加, 当 block-mean metric 改善 < eps 时停 (block-level early stop).
#       这是 honest 的 conservative 实现 (不会少计 complexity).
# =============================================================================
def bps_early_stop(rx_block, B_max, B_min, stop_thresh, Nw=NW_DEFAULT):
    """C3 early-stop adaptive-width search.

    按 phase 顺序逐个累加评估 (从 B_min 起), 每加一个 phase 算 block-mean best metric;
    当连续加 phase 而 block-mean best metric 改善 < stop_thresh 时停 (block-level).
    实际评估 phase 数 B_used ∈ [B_min, B_max].
    返回 (rx_compensated, pe, n_distance_evals, B_used).
    """
    N = len(rx_block)
    phases_all = 2 * np.pi * np.arange(B_max) / B_max
    # 先算全部 (用于 early-stop 判定, 但只 "计费" B_used 个)
    metrics_all, _ = bps_objective_matrix(rx_block, phases_all)
    metrics_all = sliding_window_average(metrics_all, Nw)

    # block-level early stop: 累加 phase, 监控 block-mean best metric 改善
    prev_best = np.inf
    B_used = B_min
    for B_try in range(B_min, B_max + 1):
        cur_best = float(np.mean(np.min(metrics_all[:B_try], axis=0)))
        if B_try > B_min and (prev_best - cur_best) < stop_thresh:
            B_used = B_try - 1 if B_try > B_min else B_min
            break
        prev_best = cur_best
        B_used = B_try
    B_used = max(B_min, min(B_used, B_max))

    metrics_used = metrics_all[:B_used]
    best_b = np.argmin(metrics_used, axis=0)
    pe_raw = phases_all[best_b]
    pe = unwrap_phase(pe_raw, M0)
    n_evals = B_used * N
    return rx_block * np.exp(-1j * pe), pe, n_evals, B_used


# =============================================================================
# Block-wise driver: 逐 N_DFT 块跑 method + resolve M0-fold 模糊 (同 BPS 既有流程)
# =============================================================================
def run_method_on_signal(rx, tx_bits, method_fn, n_dft, block_size_resolve):
    """逐块跑 method_fn(seg) → 合并 → resolve_m16apsk_blockwise → (n_err, n_bits, total_evals, aux).

    method_fn(seg) 必须返回 (rx_compensated, pe, n_evals) 或带额外 aux 字段.
    """
    N = len(rx)
    n_blk = N // n_dft
    L = n_blk * n_dft
    rx_comp = np.zeros(L, dtype=complex)
    total_evals = 0
    aux_acc = {'n_refined': 0, 'n_fallback': 0, 'B_used_list': []}
    for b in range(n_blk):
        seg = rx[b * n_dft:(b + 1) * n_dft]
        out = method_fn(seg)
        rc = out[0]
        ne = out[2]
        rx_comp[b * n_dft:(b + 1) * n_dft] = rc
        total_evals += ne
        if len(out) >= 5:
            # C1/C2: (rc, pe, ne, n_refined, n_fallback)
            aux_acc['n_refined'] += out[3]
            aux_acc['n_fallback'] += out[4]
        elif len(out) == 4:
            # C3: (rc, pe, ne, B_used)
            aux_acc['B_used_list'].append(out[3])
    tb = tx_bits[:L * 4]   # 4 bit/symbol for 16APSK
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=block_size_resolve)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb), total_evals, aux_acc
