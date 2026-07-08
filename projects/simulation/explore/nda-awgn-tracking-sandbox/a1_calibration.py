# -*- coding: utf-8 -*-
"""A1 参数适配标定实验: 找"可测量判据 → 最优 K"的映射关系.

目的 (adaptation-scan.md A1): NDA-ML segmented 块内跟踪, 参数 K=块内分段数.
已知最优 K 随线宽/湍流强度变化 (D-009 K 扫描). 本实验找: 用什么**可测量判据**
(不需 oracle 真值) 能预测最优 K, 从而设计"自适应 K 策略".

方法: 阶段 1 标定. 在多条件下算 4 个判据值 + 全 K 扫描找真实最优 K,
输出判据 vs 最优 K 的 Spearman/Pearson 相关性.

最高纪律 (同 parity_tuning_sweep.py):
  1. 只改本 explore/nda-awgn-tracking-sandbox/ 目录, 绝不改 common/simulator/params.
  2. 复用 parity_tuning_sweep.py 的函数: nda_segmented_eq_k / ber_nda_seg_k_awgn /
     ber_nda_seg_k_eval. import 方式同 parity 脚本头.
  3. 不用 dpll_track (4 次方鉴相器对 16APSK 不对).
  4. 信道必须共享: AWGN 用 S.awgn_wiener_channel, 湍流用 generate_shared_realization_apsk.
  5. 只跑数字不做方向判断, 不写"建议/结论".

4 判据 (每 N_DFT=256 块算, 跨块取中位数 robust):
  J1 升幂后归一化幅值方差: Var(|rx^M0|) / mean(|rx^M0|)^2
  J2 scintillation index:   Var(|rx|^2) / mean(|rx|^2)^2
  J3 盲 SNR (dB):           mean(|rx|^2) / Var(rx - hard_decision(rx))
  J4 升幂后相位差分方差:    Var(diff(unwrap(angle(rx^M0))))

场景矩阵 (单 seed, 标定用, 35 点):
  AWGN: 线宽 [10,50,100,200,500,1000]kHz × SNR [14,16,18,20,22]dB = 30 点
  湍流下行: weak(12dB)/moderate(16dB)/strong(20dB) @ 10kHz = 3 点
  湍流上行: uplink_moderate(16dB)/uplink_strong(20dB) @ 10kHz = 2 点

每点流程:
  1. 生成 rx (AWGN: awgn_wiener_channel; 湍流: generate_shared_realization_apsk + 盲 h 均衡)
  2. 逐 N_DFT 块算 4 判据, 取所有块中位数
  3. 全 K 扫描 [1,2,4,8,16,32] 找真实最优 K
  4. 记录 {场景, J1-J4, 最优K, 最优BER, 各K的BER}

运行: cd projects/simulation && python explore/nda-awgn-tracking-sandbox/a1_calibration.py
"""
import os
import sys
import json
import time
import datetime

import numpy as np

# --- 路径: simulation 根 (与 parity_tuning_sweep.py 同构) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守纪律 1: 不改 common/simulator/params)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402  (参数只读)
import sc_nda_ml_sim as S  # noqa: E402  (复用 fft_foe / awgn_wiener_channel / estimate_h)
from params import SimulationConfig  # noqa: E402

# 复用 parity_tuning_sweep.py 的函数 (守纪律 2: 不重写, import 同目录脚本)
# 注: parity 脚本顶层 KS 含 [1,2,4,8,16,32,64,128], 但其函数 ber_nda_seg_k_*(K) 接受任意 K,
# 本脚本只传本实验所需的 K 值 [1,2,4,8,16,32].
from parity_tuning_sweep import (  # noqa: E402
    nda_segmented_eq_k,
    ber_nda_seg_k_awgn,
    ber_nda_seg_k_eval,
)

# 本实验 K 扫描范围 (设计文档: [1,2,4,8,16,32], A1 标定用)
KS = [1, 2, 4, 8, 16, 32]
UPLINK_SEED_OFFSET = 500000     # 同 run_uplink_experiment / parity 脚本 (错开下行 seed)

# (8,8)-16APSK 16 个星座点 (从 m16apsk_mod 重建, 同 run_bps_ablation.py, 用于 J3 硬判决).
# 不改 common, 在本脚本内重建 (纪律 1).
_BITS_ALL_LABELS = np.zeros(16 * 4, dtype=int)
for _lab in range(16):
    _BITS_ALL_LABELS[_lab * 4 + 0] = (_lab >> 3) & 1
    _BITS_ALL_LABELS[_lab * 4 + 1] = (_lab >> 2) & 1
    _BITS_ALL_LABELS[_lab * 4 + 2] = (_lab >> 1) & 1
    _BITS_ALL_LABELS[_lab * 4 + 3] = _lab & 1
_M16APSK_CONST = m16apsk_mod(_BITS_ALL_LABELS)   # (16,) 16 个星座点


# =============================================================================
# J3 辅助: 最近邻硬判决 (返回复星座点, 同 run_bps_ablation.hard_decision_m16apsk)
# =============================================================================
def hard_decision_m16apsk(z):
    """最近邻 (8,8)-16APSK 星座点 (欧氏距离最小). 向量化."""
    z = np.asarray(z, dtype=complex)
    flat = z.reshape(-1)
    dist = np.abs(flat[:, np.newaxis] - _M16APSK_CONST[np.newaxis, :]) ** 2
    idx = np.argmin(dist, axis=1)
    return _M16APSK_CONST[idx].reshape(z.shape)


# =============================================================================
# 4 判据计算 (逐 N_DFT 块, 返回每块一个标量; 调用方取跨块中位数)
# =============================================================================
def criteria_block(block, M0):
    """对单个 N_DFT 块算 4 判据. 返回 dict {J1,J2,J3,J4} (J3 线性, 输出时转 dB).

    所有判据只基于 rx (接收信号), 不需 oracle 真值 (tx/bits).
    """
    rx = np.asarray(block, dtype=complex)
    # J1: 升幂后归一化幅值方差
    raised = rx ** M0
    ra = np.abs(raised)
    j1 = np.var(ra) / (np.mean(ra) ** 2) if np.mean(ra) > 0 else np.nan
    # J2: scintillation index (归一化功率方差)
    pwr = np.abs(rx) ** 2
    j2 = np.var(pwr) / (np.mean(pwr) ** 2) if np.mean(pwr) > 0 else np.nan
    # J3: 盲 SNR = mean(|rx|^2) / Var(rx - decision)  (判决点离散度估噪声)
    decision = hard_decision_m16apsk(rx)
    resid = rx - decision
    noise_var = np.var(resid)  # 复噪声方差 = |.|^2 期望
    sig_pwr = np.mean(pwr)
    j3_lin = sig_pwr / noise_var if noise_var > 0 else np.nan
    # J4: 升幂后相位差分方差 (线宽代理)
    phase = np.unwrap(np.angle(raised))
    dphase = np.diff(phase)
    j4 = np.var(dphase)
    return {'J1': float(j1), 'J2': float(j2), 'J3': float(j3_lin), 'J4': float(j4)}


def criteria_median_over_blocks(rx, M0, n_dft):
    """逐 N_DFT 块算 4 判据, 跨块取中位数 (robust).

    返回 dict {J1,J2,J3_db,J4} (J3 转 dB).
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // n_dft
    L = n_blk * n_dft
    acc = {'J1': [], 'J2': [], 'J3': [], 'J4': []}
    for b in range(n_blk):
        block = rx[b * n_dft:(b + 1) * n_dft]
        c = criteria_block(block, M0)
        for k in acc:
            if not np.isnan(c[k]):
                acc[k].append(c[k])
    out = {}
    out['J1'] = float(np.median(acc['J1'])) if acc['J1'] else np.nan
    out['J2'] = float(np.median(acc['J2'])) if acc['J2'] else np.nan
    j3_lin_med = float(np.median(acc['J3'])) if acc['J3'] else np.nan
    out['J3_db'] = float(10.0 * np.log10(j3_lin_med)) if (j3_lin_med and not np.isnan(j3_lin_med)) else np.nan
    out['J4'] = float(np.median(acc['J4'])) if acc['J4'] else np.nan
    return out


# =============================================================================
# 全 K 扫描找真实最优 K
# =============================================================================
def best_k_awgn(rx, bits, M0, ks=KS):
    """AWGN: 扫 K 找最优 (无 FOE). 返回 (bers_by_k dict, best_k, best_ber)."""
    bers = {}
    for K in ks:
        ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, K)
        bers[K] = ne / nb
    best_k = min(bers, key=lambda k: bers[k])
    return bers, int(best_k), float(bers[best_k])


def best_k_turb(rx_blind, bits, M0, ks=KS):
    """湍流: 扫 K 找最优 (含 fft_foe + blind h 已在 rx_blind 内). 返回同上."""
    bers = {}
    for K in ks:
        ne, nb = ber_nda_seg_k_eval(rx_blind, bits, M0, K)
        bers[K] = ne / nb
    best_k = min(bers, key=lambda k: bers[k])
    return bers, int(best_k), float(bers[best_k])


# =============================================================================
# 场景点: AWGN (单 SNR/线宽)
# =============================================================================
def run_awgn_point(lw_hz, snr_db, M0, n_blocks, seed_base):
    """单 AWGN 场景点: 生成 rx → 4 判据 (整段) → K 扫描最优. 返回 dict."""
    N_sym = n_blocks * P.N_DFT
    sigma2_p = 2 * np.pi * lw_hz * P.T_S
    seed = seed_base + int(snr_db * 1000)
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, _phi = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
    # 4 判据 (整段 rx, 跨块中位数)
    crit = criteria_median_over_blocks(rx, M0, P.N_DFT)
    # K 扫描最优
    bers, best_k, best_ber = best_k_awgn(rx, bits, M0)
    return {
        'scene': 'awgn',
        'linewidth_khz': float(lw_hz / 1e3),
        'snr_db': float(snr_db),
        'J1': crit['J1'], 'J2': crit['J2'],
        'J3_db': crit['J3_db'], 'J4': crit['J4'],
        'best_k': best_k, 'best_ber': best_ber,
        'bers_by_k': {str(k): float(v) for k, v in bers.items()},
    }


# =============================================================================
# 场景点: 湍流 (下行/上行)
# =============================================================================
def run_turb_point(turb_name, snr_db, lw_hz, M0, n_blocks, seed0, is_uplink):
    """单湍流场景点: 逐块 generate_shared_realization_apsk + 盲 h 均衡
    → 拼 rx_blind → 4 判据 → K 扫描最优. 返回 dict.

    rx_blind 的生成与 parity sweep_turbulence 完全一致 (公平同信道):
      for b: r=generate_shared_realization_apsk(...); h_blind=estimate_h_blind_perblock;
             rx_blind_b = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
    判据/BER 都在这份 rx_blind 上算 (整段拼接后跨块).
    """
    cfg = SimulationConfig()
    Ns = P.N_DFT
    gamma_lin = 10 ** (snr_db / 10.0)
    rx_blind_all = np.zeros(n_blocks * Ns, dtype=complex)
    bits_all = np.zeros(n_blocks * Ns * P.BITS_PER_SYM, dtype=int)
    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
            seed=seed0 + b, lw=lw_hz)
        rx_raw = r['rx_raw']
        bits = r['bits']
        h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind_b = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        rx_blind_all[b * Ns:(b + 1) * Ns] = rx_blind_b
        bits_all[b * Ns * P.BITS_PER_SYM:(b + 1) * Ns * P.BITS_PER_SYM] = bits[:Ns * P.BITS_PER_SYM]
    # 4 判据 (整段 rx_blind, 跨块中位数)
    crit = criteria_median_over_blocks(rx_blind_all, M0, Ns)
    # K 扫描最优 (湍流用 eval 含 fft_foe)
    bers, best_k, best_ber = best_k_turb(rx_blind_all, bits_all, M0)
    return {
        'scene': ('turb_uplink' if is_uplink else 'turb_downlink'),
        'turbulence': turb_name,
        'snr_db': float(snr_db),
        'linewidth_khz': float(lw_hz / 1e3),
        'J1': crit['J1'], 'J2': crit['J2'],
        'J3_db': crit['J3_db'], 'J4': crit['J4'],
        'best_k': best_k, 'best_ber': best_ber,
        'bers_by_k': {str(k): float(v) for k, v in bers.items()},
    }


# =============================================================================
# 相关性分析: Spearman ρ + Pearson r (判据 vs 最优 K)
# =============================================================================
def spearman_rho(x, y):
    """Spearman 秩相关系数 (单调关系, 稳健). NaN 自动跳过."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float('nan')
    rx_ = np.argsort(np.argsort(x)).astype(float)
    ry_ = np.argsort(np.argsort(y)).astype(float)
    rx_ -= rx_.mean(); ry_ -= ry_.mean()
    denom = np.sqrt(np.sum(rx_**2) * np.sum(ry_**2))
    return float(np.sum(rx_ * ry_) / denom) if denom > 0 else float('nan')


def pearson_r(x, y):
    """Pearson 线性相关系数. NaN 自动跳过."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float('nan')
    xm, ym = x - x.mean(), y - y.mean()
    denom = np.sqrt(np.sum(xm**2) * np.sum(ym**2))
    return float(np.sum(xm * ym) / denom) if denom > 0 else float('nan')


def criterion_by_best_k(points, key):
    """判据值在每个 best_k 档的中位数 ± IQR (看能否分桶). 返回 dict {k: (med, q1, q3, n)}."""
    from collections import defaultdict
    by_k = defaultdict(list)
    for p in points:
        by_k[p['best_k']].append(p[key])
    out = {}
    for k in sorted(by_k):
        arr = np.asarray(by_k[k], dtype=float)
        arr = arr[~np.isnan(arr)]
        if len(arr) == 0:
            continue
        q1, med, q3 = np.percentile(arr, [25, 50, 75])
        out[int(k)] = {'median': float(med), 'q1': float(q1), 'q3': float(q3),
                       'iqr': float(q3 - q1), 'n': int(len(arr))}
    return out


def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return to_jsonable(o.tolist())
    return o


# =============================================================================
# 主流程
# =============================================================================
def main():
    t0 = time.time()
    M0 = P.M0
    n_blocks = P.N_BLOCKS
    print("=" * 100)
    print("A1 参数适配标定实验: 可测量判据 → 最优 K 映射")
    print(f"M0={M0}, N_DFT={P.N_DFT}, N_BLOCKS={n_blocks} (N_sym={n_blocks*P.N_DFT}/点)")
    print(f"K 扫描 {KS} | 判据 J1(升幂幅值方差) J2(scint) J3(盲SNR dB) J4(升幂相位差分方差)")
    print(f"AWGN seed_base=P.SEED_AWGN={P.SEED_AWGN}, 湍流 seed_base=P.SEED_TURB0={P.SEED_TURB0}")
    print("纪律: 只跑数字+相关性, 不做方向判断; 同信道 (AWGN awgn_wiener_channel / 湍流 generate_shared_realization)")
    print("=" * 100)

    points = []

    # --- AWGN: 线宽 × SNR (30 点) ---
    linewidths = [10e3, 50e3, 100e3, 200e3, 500e3, 1000e3]
    snrs_awgn = [14.0, 16.0, 18.0, 20.0, 22.0]
    print("\n" + "#" * 30 + " AWGN 线宽 × SNR (30 点) " + "#" * 30)
    hdr = (f"{'lw_kHz':>7} {'SNR':>4} | {'J1':>9} {'J2':>9} {'J3dB':>7} {'J4':>11} | "
           f"{'bestK':>5} {'bestBER':>10}")
    print(hdr)
    for snr_db in snrs_awgn:
        for lw in linewidths:
            p = run_awgn_point(lw, snr_db, M0, n_blocks, P.SEED_AWGN)
            points.append(p)
            print(f"{lw/1e3:>7.0f} {snr_db:>4.0f} | {p['J1']:>9.4f} {p['J2']:>9.4f} "
                  f"{p['J3_db']:>7.2f} {p['J4']:>11.3e} | {p['best_k']:>5} {p['best_ber']:>10.3e}")

    # --- 湍流下行: weak/moderate/strong @ 10kHz (3 点) ---
    print("\n" + "#" * 30 + " 湍流下行 @ 10kHz (3 点) " + "#" * 30)
    print(hdr)
    turb_down = [
        ('weak', 12.0), ('moderate', 16.0), ('strong', 20.0),
    ]
    for turb, snr_db in turb_down:
        p = run_turb_point(turb, snr_db, 10e3, M0, n_blocks, P.SEED_TURB0, is_uplink=False)
        points.append(p)
        print(f"{p['turbulence'][:7]:>7} {snr_db:>4.0f} | {p['J1']:>9.4f} {p['J2']:>9.4f} "
              f"{p['J3_db']:>7.2f} {p['J4']:>11.3e} | {p['best_k']:>5} {p['best_ber']:>10.3e}")

    # --- 湍流上行: uplink_moderate/uplink_strong @ 10kHz (2 点) ---
    print("\n" + "#" * 30 + " 湍流上行 @ 10kHz (2 点) " + "#" * 30)
    print(hdr)
    turb_up = [
        ('uplink_moderate', 16.0), ('uplink_strong', 20.0),
    ]
    seed0_up = P.SEED_TURB0 + UPLINK_SEED_OFFSET
    for turb, snr_db in turb_up:
        p = run_turb_point(turb, snr_db, 10e3, M0, n_blocks, seed0_up, is_uplink=True)
        points.append(p)
        print(f"{p['turbulence'][:7]:>7} {snr_db:>4.0f} | {p['J1']:>9.4f} {p['J2']:>9.4f} "
              f"{p['J3_db']:>7.2f} {p['J4']:>11.3e} | {p['best_k']:>5} {p['best_ber']:>10.3e}")

    # --- 相关性分析 ---
    best_ks = np.array([p['best_k'] for p in points], dtype=float)
    crit_keys = [('J1', 'J1'), ('J2', 'J2'), ('J3_db', 'J3 (dB)'), ('J4', 'J4')]
    correlation = {}
    print("\n" + "#" * 30 + " 判据 vs 最优 K 相关性 (n=%d) " % len(points) + "#" * 30)
    print(f"{'判据':<10} | {'Spearman ρ':>11} | {'Pearson r':>10}")
    for ckey, clabel in crit_keys:
        cvals = np.array([p[ckey] for p in points], dtype=float)
        rho = spearman_rho(cvals, best_ks)
        r = pearson_r(cvals, best_ks)
        correlation[ckey] = {'spearman_rho': rho, 'pearson_r': r}
        print(f"{clabel:<10} | {rho:>11.4f} | {r:>10.4f}")

    # 每判据在各 best_k 档的中位数 ± IQR
    buckets = {ckey: criterion_by_best_k(points, ckey) for ckey, _ in crit_keys}

    # 最优 K 随线宽单调性 (AWGN @ 18dB)
    awgn_18 = [p for p in points if p['scene'] == 'awgn' and abs(p['snr_db'] - 18.0) < 1e-6]
    awgn_18.sort(key=lambda p: p['linewidth_khz'])
    best_k_vs_lw = [(p['linewidth_khz'], p['best_k']) for p in awgn_18]

    elapsed = time.time() - t0

    # 最强判据 (|Spearman| 最大)
    rho_abs = {ck: abs(correlation[ck]['spearman_rho']) for ck, _ in crit_keys
               if not np.isnan(correlation[ck]['spearman_rho'])}
    strongest = max(rho_abs, key=rho_abs.get) if rho_abs else None
    summary = (f"最强判据 (|Spearman ρ| 最大): {strongest} "
               f"(ρ={correlation[strongest]['spearman_rho']:.4f})") if strongest else "n/a"

    out = {
        'meta': {
            'task': 'A1 参数适配标定: 可测量判据 → 最优 K 映射',
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'n_points': len(points),
            'K_values': KS,
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_BLOCKS': P.N_BLOCKS,
            'T_S': float(P.T_S),
            'n_seeds': 1,
            'criteria': {
                'J1': '升幂后归一化幅值方差 Var(|rx^M0|)/mean(|rx^M0|)^2',
                'J2': 'scintillation index Var(|rx|^2)/mean(|rx|^2)^2',
                'J3_db': '盲 SNR (dB) mean(|rx|^2)/Var(rx-hard_decision)',
                'J4': '升幂后相位差分方差 Var(diff(unwrap(angle(rx^M0))))',
            },
            'criteria_aggregation': '逐 N_DFT 块算, 跨块取中位数 (robust)',
            'fairness': 'AWGN 同 awgn_wiener_channel; 湍流同 generate_shared_realization_apsk + 盲 h 均衡',
            'reused_functions': ['parity_tuning_sweep.nda_segmented_eq_k',
                                 'parity_tuning_sweep.ber_nda_seg_k_awgn',
                                 'parity_tuning_sweep.ber_nda_seg_k_eval',
                                 'S.awgn_wiener_channel', 'S.fft_foe_m0_omega',
                                 'S.estimate_h_blind_perblock',
                                 'generate_shared_realization_apsk', 'mmse_equalize',
                                 'amp_limit', 'resolve_m16apsk_blockwise'],
            'common_or_simulator_or_params_modified': False,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'points': points,
        'correlation': correlation,
        'criteria_by_best_k': buckets,
        'best_k_vs_linewidth_18dB': [{'linewidth_khz': lk, 'best_k': bk}
                                     for lk, bk in best_k_vs_lw],
        'summary': summary,
    }
    out_json = os.path.join(_HERE, '_a1_calibration.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    print("\n" + "=" * 100)
    print(f"汇总: {len(points)} 点 | 最优 K 分布 {sorted(set(int(p['best_k']) for p in points))}")
    print(summary)
    print("最优 K 随线宽 (@18dB AWGN): " +
          ", ".join(f"{lk:.0f}kHz→K{bk}" for lk, bk in best_k_vs_lw))
    print(f"[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
