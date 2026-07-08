# -*- coding: utf-8 -*-
"""A1 参数适配验证实验: 自适应 K 策略 vs 固定 K (5 seed).

目的 (adaptation-scan.md A1 阶段2): 验证"自适应 K 策略"是否优于"固定 K"。
标定 (a1_calibration.py) 发现无判据 Spearman ρ≥0.6, 固定 K=16 在 35 点中 25 点
跟 oracle 持平 (71%). 本实验用能找到的最好映射做自适应 K, 跟固定 K 对比.

本实验测两种自适应 + 参照:
  策略1 oracle:  每场景用真实最优 K (非可实现上界, 连这个都不赢固定 K=16 则自适应无救).
  策略2 J4:      修正-J4 阈值二分段映射 (可实现, in-sample 拟合有乐观偏差).
  策略3 SNR:     SNR 三分段映射 (J3 盲 SNR, AWGN 跨 SNR 有 K 变化).
  参照 VV:       VV Nw=64, 证明自适应是普适思路.

J4 修正 (必改, 标定 J4 有 bug): 标定用 np.unwrap 对 M0=8 升幂相位路径错乱.
  修正: mod 2π 相位增量, 不 unwrap:
    raised = rx**M0; ang = np.angle(raised); dang = np.diff(ang)
    dang = (dang+pi) % (2pi) - pi; j4 = var(dang)

最高纪律 (同 a1_calibration.py):
  1. 只改本 explore/nda-awgn-tracking-sandbox/ 目录, 绝不改 common/simulator/params.
  2. 复用 parity_tuning_sweep.py 函数 (nda_segmented_eq_k / ber_nda_seg_k_awgn /
     ber_nda_seg_k_eval / ber_vv_nw_eval). import 方式同 a1_calibration.py.
  3. 不用 dpll_track (4 次方鉴相器对 16APSK 不对).
  4. 信道必须共享: AWGN 用 S.awgn_wiener_channel, 湍流用 generate_shared_realization_apsk.
  5. 5 seed (TL-29), 主结果 mean ± 95% CI.
  6. 只跑数字不做方向判断.

PASS/FAIL 判据 (主线定, 子 agent 只填数字):
  - 自适应-J4 (可实现版) 在 8 点中至少 2 点 CI 显著赢 K=16 (gain<0 且 CI 上界<0)
  - AND aggregate gain_vs_k16 < 0 (自适应平均不输 K16)
  满足 = PASS, 否则 = FAIL.

场景矩阵 (5 seed 主结果, 8 点):
  AWGN: 线宽 [10,100,1000]kHz × SNR 18dB = 3 点 (低/中/高线宽)
  湍流 @10kHz: weak(12dB)/moderate(16dB)/strong(20dB)/uplink_moderate(16dB)/
              uplink_strong(20dB) = 5 点
对比方法 (每点全跑): adaptive_oracle / adaptive_j4 / adaptive_snr /
  fixed_k1 / fixed_k8 / fixed_k16 / fixed_k32 / vv_nw64.

运行: cd projects/simulation && python explore/nda-awgn-tracking-sandbox/a1_validation.py
"""
import os
import sys
import json
import time
import datetime

import numpy as np

# --- 路径: simulation 根 (与 a1_calibration.py / parity_tuning_sweep.py 同构) ---
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
import sc_nda_ml_sim as S  # noqa: E402  (复用 awgn_wiener_channel / fft_foe / estimate_h)
from params import SimulationConfig  # noqa: E402

# 复用 parity_tuning_sweep.py 的函数 (守纪律 2: 不重写, import 同目录脚本)
from parity_tuning_sweep import (  # noqa: E402
    ber_nda_seg_k_awgn,
    ber_nda_seg_k_eval,
    ber_vv_nw_eval,
)

# 本实验常量
N_SEEDS = 5                       # TL-29: 5 seed 主结果
UPLINK_SEED_OFFSET = 500000       # 同 a1_calibration / parity 脚本 (错开下行 seed)
VV_NW = 64                        # VV 默认窗 (参照线, parity 脚本 NWS 中点)
FIXED_KS = [1, 8, 16, 32]         # 固定 K 对比组 (含标定最强普适 K=16)
ORACLE_KS = [1, 2, 4, 8, 16, 32]  # oracle 扫描范围 (同标定 KS)

# SNR-based 映射 (策略3): SNR<16→K4, 16-20→K8, >20→K16
SNR_K_MAP = [(16.0, 4), (20.0, 8)]   # (上界_dB, K); 默认 K=16


# =============================================================================
# J4 修正计算 (标定 J4 bug: unwrap 对 M0=8 升幂相位路径错乱 → 改 mod 2π 增量)
# =============================================================================
def j4_fixed_block(block, M0):
    """修正 J4: 升幂后 mod 2π 相位增量方差 (不 unwrap)."""
    rx = np.asarray(block, dtype=complex)
    raised = rx ** M0
    ang = np.angle(raised)                    # [-pi, pi], 不 unwrap
    dang = np.diff(ang)
    dang = (dang + np.pi) % (2 * np.pi) - np.pi   # wrap to [-pi, pi]
    return float(np.var(dang))


def j4_fixed_median(rx, M0, n_dft):
    """逐 N_DFT 块算修正 J4, 跨块取中位数 (robust, 同标定聚合方式)."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // n_dft
    acc = []
    for b in range(n_blk):
        acc.append(j4_fixed_block(rx[b * n_dft:(b + 1) * n_dft], M0))
    return float(np.median(acc)) if acc else float('nan')


# =============================================================================
# J3 盲 SNR (用于 SNR 映射, 直接从 rx 估, 不需 oracle)
# (复用 a1_calibration 硬判决思路; 此处仅 SNR 映射用, 整段估一个值即可)
# =============================================================================
_BITS_ALL_LABELS = np.zeros(16 * 4, dtype=int)
for _lab in range(16):
    _BITS_ALL_LABELS[_lab * 4 + 0] = (_lab >> 3) & 1
    _BITS_ALL_LABELS[_lab * 4 + 1] = (_lab >> 2) & 1
    _BITS_ALL_LABELS[_lab * 4 + 2] = (_lab >> 1) & 1
    _BITS_ALL_LABELS[_lab * 4 + 3] = _lab & 1
_M16APSK_CONST = m16apsk_mod(_BITS_ALL_LABELS)


def hard_decision_m16apsk(z):
    z = np.asarray(z, dtype=complex)
    flat = z.reshape(-1)
    dist = np.abs(flat[:, np.newaxis] - _M16APSK_CONST[np.newaxis, :]) ** 2
    idx = np.argmin(dist, axis=1)
    return _M16APSK_CONST[idx].reshape(z.shape)


def blind_snr_db(rx):
    """整段盲 SNR (dB): mean(|rx|^2)/Var(rx-decision)."""
    rx = np.asarray(rx, dtype=complex)
    pwr = np.abs(rx) ** 2
    decision = hard_decision_m16apsk(rx)
    noise_var = np.var(rx - decision)
    sig_pwr = np.mean(pwr)
    lin = sig_pwr / noise_var if noise_var > 0 else float('nan')
    return float(10.0 * np.log10(lin)) if (lin and not np.isnan(lin)) else float('nan')


# =============================================================================
# 映射策略: SNR → K, J4 → K
# =============================================================================
def snr_to_k(snr_db):
    """SNR-based 映射: SNR<16→K4, 16-20→K8, >20→K16."""
    for upper, k in SNR_K_MAP:
        if snr_db < upper:
            return k
    return 16


def j4_to_k(j4_val, threshold, default_k=16, high_j4_k=32):
    """J4-based 映射: J4 < threshold → default_k(16), J4 >= threshold → high_j4_k(32)."""
    return high_j4_k if j4_val >= threshold else default_k


# =============================================================================
# CI 辅助: 95% CI (t 分布, n=5)
# =============================================================================
def mean_ci95(x):
    """返回 (mean, ci95=half-width). n=5 用 t_{0.975,4}=2.776."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    m = float(np.mean(x))
    if n < 2:
        return m, float('nan')
    s = float(np.std(x, ddof=1))
    try:
        from scipy import stats
        tval = float(stats.t.ppf(0.975, n - 1))
    except Exception:
        tval = 2.776  # n=5 fallback
    return m, float(tval * s / np.sqrt(n))


# =============================================================================
# J4 阈值拟合 (在标定 35 点上, 重算修正 J4 + best_k, 网格搜阈值最大化正确率)
# =============================================================================
def fit_j4_threshold(cal_j4, cal_best_k, default_k=16, high_j4_k=32):
    """网格搜 J4 阈值, 使 'J4>=thr→K32 else K16' 与 best_k 匹配率最高.

    注: 仅把 best_k∈{16,32} 的点视为可分 (其余点 K=1/2/4/8 视为不属于该二分段,
    映射必错). 返回 (best_thr, best_acc, n_eval).
    诚实标注: in-sample 拟合, 有乐观偏差.
    """
    cal_j4 = np.asarray(cal_j4, dtype=float)
    cal_best_k = np.asarray(cal_best_k, dtype=int)
    # 候选阈值: 唯一 J4 值之间中点
    uniq = np.unique(cal_j4)
    cands = [(uniq[i] + uniq[i + 1]) / 2.0 for i in range(len(uniq) - 1)]
    cands = [float(np.min(cal_j4)) - 1e-9] + cands + [float(np.max(cal_j4)) + 1e-9]
    best_thr, best_acc = None, -1.0
    best_cm = None
    for thr in cands:
        pred = np.where(cal_j4 >= thr, high_j4_k, default_k)
        acc = float(np.mean(pred == cal_best_k))
        if acc > best_acc:
            best_acc = acc
            best_thr = float(thr)
            # 混淆: 只看 best_k∈{default_k,high_j4_k} 的子集
            mask = np.isin(cal_best_k, [default_k, high_j4_k])
            if mask.sum() > 0:
                sub_pred = pred[mask]
                sub_true = cal_best_k[mask]
                best_cm = {
                    'n_subset': int(mask.sum()),
                    'subset_correct': int(np.sum(sub_pred == sub_true)),
                    'subset_acc': float(np.mean(sub_pred == sub_true)),
                    'default_k_true_count': int(np.sum(sub_true == default_k)),
                    'high_k_true_count': int(np.sum(sub_true == high_j4_k)),
                }
            else:
                best_cm = {'n_subset': 0}
    return best_thr, best_acc, best_cm


# =============================================================================
# 单场景: 生成 5 seed 的 rx (AWGN / 湍流) + 返回每 seed 的 rx + bits
# =============================================================================
def gen_awgn_seeds(lw_hz, snr_db, M0, n_blocks, n_seeds, seed_base):
    """5 seed AWGN: 每 seed 独立 rx. 返回 list[(rx, bits)]."""
    N_sym = n_blocks * P.N_DFT
    sigma2_p = 2 * np.pi * lw_hz * P.T_S
    out = []
    for i in range(n_seeds):
        seed = seed_base + i + int(snr_db * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, _phi = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
        out.append((rx, bits))
    return out


def gen_turb_seeds(turb_name, snr_db, lw_hz, M0, n_blocks, n_seeds, seed0_base):
    """5 seed 湍流: 每 seed 独立逐块 generate_shared_realization + 盲 h 均衡.
    返回 list[(rx_blind_all, bits_all)] (同 parity sweep_turbulence 公平同信道)."""
    cfg = SimulationConfig()
    Ns = P.N_DFT
    gamma_lin = 10 ** (snr_db / 10.0)
    out = []
    for i in range(n_seeds):
        seed0 = seed0_base + i
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
        out.append((rx_blind_all, bits_all))
    return out


# =============================================================================
# 每 seed 算各方法 BER (返回 dict method→BER)
# =============================================================================
def eval_methods_awgn(rx, bits, M0):
    """AWGN: 算 oracle/j4/snr/fixed_k1..32/vv. 返回 (bers dict, per_seed_j4, per_seed_snr)."""
    bers = {}
    # 修正 J4 (整段 rx, 跨块中位数) + 盲 SNR → 自适应 K
    j4 = j4_fixed_median(rx, M0, P.N_DFT)
    snr = blind_snr_db(rx)
    return bers, j4, snr


def run_awgn_point(lw_hz, snr_db, M0, n_blocks, n_seeds, seed_base, j4_threshold):
    """单 AWGN 场景点: 5 seed × 各方法 BER. 返回 dict (含 bers/gain_vs_k16)."""
    seeds_rx = gen_awgn_seeds(lw_hz, snr_db, M0, n_blocks, n_seeds, seed_base)
    methods = ['adaptive_oracle', 'adaptive_j4', 'adaptive_snr',
               'fixed_k1', 'fixed_k8', 'fixed_k16', 'fixed_k32', 'vv_nw64']
    by_seed = {m: [] for m in methods}
    per_seed_j4, per_seed_snr = [], []
    for (rx, bits) in seeds_rx:
        # 修正 J4 + 盲 SNR
        j4 = j4_fixed_median(rx, M0, P.N_DFT)
        snr = blind_snr_db(rx)
        per_seed_j4.append(j4)
        per_seed_snr.append(snr)
        k_j4 = j4_to_k(j4, j4_threshold)
        k_snr = snr_to_k(snr)
        # oracle: 扫描找最优 (每 seed 独立真值最优)
        orb_bers = {}
        for K in ORACLE_KS:
            ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, K)
            orb_bers[K] = ne / nb
        k_oracle = min(orb_bers, key=lambda k: orb_bers[k])
        # 各方法 BER
        for K in FIXED_KS:
            ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, K)
            by_seed['fixed_k%d' % K].append(ne / nb)
        ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, k_oracle)
        by_seed['adaptive_oracle'].append(ne / nb)
        ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, k_j4)
        by_seed['adaptive_j4'].append(ne / nb)
        ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, k_snr)
        by_seed['adaptive_snr'].append(ne / nb)
        ne, nb = ber_vv_nw_eval(rx, bits, VV_NW, intra_foe=False)
        by_seed['vv_nw64'].append(ne / nb)
    return _assemble_result('awgn', lw_hz, snr_db, None, methods, by_seed,
                            per_seed_j4, per_seed_snr)


def run_turb_point(turb_name, snr_db, lw_hz, M0, n_blocks, n_seeds,
                   seed0_base, is_uplink, j4_threshold):
    """单湍流场景点: 5 seed × 各方法 BER (湍流用 eval 含 fft_foe). 返回 dict."""
    seeds_rx = gen_turb_seeds(turb_name, snr_db, lw_hz, M0, n_blocks, n_seeds, seed0_base)
    methods = ['adaptive_oracle', 'adaptive_j4', 'adaptive_snr',
               'fixed_k1', 'fixed_k8', 'fixed_k16', 'fixed_k32', 'vv_nw64']
    by_seed = {m: [] for m in methods}
    per_seed_j4, per_seed_snr = [], []
    for (rx, bits) in seeds_rx:
        j4 = j4_fixed_median(rx, M0, P.N_DFT)
        snr = blind_snr_db(rx)
        per_seed_j4.append(j4)
        per_seed_snr.append(snr)
        k_j4 = j4_to_k(j4, j4_threshold)
        k_snr = snr_to_k(snr)
        orb_bers = {}
        for K in ORACLE_KS:
            ne, nb = ber_nda_seg_k_eval(rx, bits, M0, K)
            orb_bers[K] = ne / nb
        k_oracle = min(orb_bers, key=lambda k: orb_bers[k])
        for K in FIXED_KS:
            ne, nb = ber_nda_seg_k_eval(rx, bits, M0, K)
            by_seed['fixed_k%d' % K].append(ne / nb)
        ne, nb = ber_nda_seg_k_eval(rx, bits, M0, k_oracle)
        by_seed['adaptive_oracle'].append(ne / nb)
        ne, nb = ber_nda_seg_k_eval(rx, bits, M0, k_j4)
        by_seed['adaptive_j4'].append(ne / nb)
        ne, nb = ber_nda_seg_k_eval(rx, bits, M0, k_snr)
        by_seed['adaptive_snr'].append(ne / nb)
        ne, nb = ber_vv_nw_eval(rx, bits, VV_NW, intra_foe=True, M0=M0)
        by_seed['vv_nw64'].append(ne / nb)
    return _assemble_result(('turb_uplink' if is_uplink else 'turb_downlink'),
                            lw_hz, snr_db, turb_name, methods, by_seed,
                            per_seed_j4, per_seed_snr)


def _assemble_result(scene, lw_hz, snr_db, turb_name, methods, by_seed,
                     per_seed_j4, per_seed_snr):
    """聚合 5 seed → mean ± ci95; 算 gain_vs_k16. 返回 dict (JSON-ready)."""
    bers_out = {}
    mean_of = {}
    for m in methods:
        arr = by_seed[m]
        m_mean, m_ci = mean_ci95(arr)
        bers_out[m] = {'mean': m_mean, 'ci95': m_ci, 'by_seed': [float(v) for v in arr]}
        mean_of[m] = m_mean
    # gain_vs_k16_db = 10*log10(BER_method / BER_k16), 负=好
    base = mean_of['fixed_k16']
    gain_db = {}
    for m in methods:
        if m == 'fixed_k16':
            continue
        bm = mean_of[m]
        gain_db[m] = float(10.0 * np.log10(bm / base)) if (base > 0 and bm > 0) else float('nan')
    # CI 显著性 (gain<0 且 CI 上界<0): 用 per-seed BER ratio 的 CI 简化判定.
    # 严格: gain 95% CI = 10*log10 比值的 CI. 这里用 bootstrap-free 近似:
    # 显著赢 iff mean(method) < mean(k16) 且 (mean(method)+ci95(method)) < mean(k16)
    # (保守单侧, method 的上界 < k16 的均值). 标记显著点.
    sig_win = {}
    for m in ['adaptive_oracle', 'adaptive_j4', 'adaptive_snr', 'vv_nw64'] + \
              ['fixed_k%d' % k for k in [1, 8, 32]]:
        hi = bers_out[m]['mean'] + bers_out[m]['ci95']
        sig_win[m] = bool(hi < base and base > 0)
    return {
        'scene': scene,
        'turbulence': turb_name,
        'linewidth_khz': float(lw_hz / 1e3),
        'snr_db': float(snr_db),
        'per_seed_j4_fixed': [float(v) for v in per_seed_j4],
        'per_seed_j4_fixed_mean': float(np.mean(per_seed_j4)),
        'per_seed_snr_db': [float(v) for v in per_seed_snr],
        'per_seed_snr_db_mean': float(np.mean(per_seed_snr)),
        'bers': bers_out,
        'gain_vs_k16_db': gain_db,
        'sig_win_vs_k16': sig_win,
    }


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
# 重算标定 35 点修正 J4 (拟合阈值用). 复用 a1_calibration 场景矩阵.
# =============================================================================
def recompute_calibration_j4_and_bestk(M0, n_blocks):
    """复现标定 35 点 rx, 重算修正 J4 (整段跨块中位数) + 读 best_k.
    返回 (cal_j4_list, cal_bestk_list, cal_meta_list)."""
    cal_path = os.path.join(_HERE, '_a1_calibration.json')
    with open(cal_path, encoding='utf-8') as f:
        cal = json.load(f)
    bkmap = {(p['scene'], p.get('linewidth_khz'), p.get('snr_db'),
              p.get('turbulence')): p['best_k'] for p in cal['points']}
    cal_j4, cal_bestk, cal_meta = [], [], []
    cfg = SimulationConfig()
    # AWGN 30 点
    for snr_db in [14.0, 16.0, 18.0, 20.0, 22.0]:
        for lw in [10e3, 50e3, 100e3, 200e3, 500e3, 1000e3]:
            N_sym = n_blocks * P.N_DFT
            sigma2_p = 2 * np.pi * lw * P.T_S
            seed = P.SEED_AWGN + int(snr_db * 1000)
            rng = np.random.default_rng(seed + 7)
            bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
            tx = m16apsk_mod(bits)
            rx, _ = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
            j4 = j4_fixed_median(rx, M0, P.N_DFT)
            bk = bkmap[('awgn', lw / 1e3, snr_db, None)]
            cal_j4.append(j4)
            cal_bestk.append(int(bk))
            cal_meta.append({'scene': 'awgn', 'lw_khz': lw / 1e3, 'snr': snr_db, 'turb': None})
    # 湍流下行 3 点
    for turb, snr_db in [('weak', 12.0), ('moderate', 16.0), ('strong', 20.0)]:
        Ns = P.N_DFT
        rx_a = np.zeros(n_blocks * Ns, dtype=complex)
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, 10 ** (snr_db / 10), turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
                seed=P.SEED_TURB0 + b, lw=10e3)
            hb = S.estimate_h_blind_perblock(r['rx_raw'], 10 ** (snr_db / 10))
            rb = amp_limit(mmse_equalize(r['rx_raw'], hb, 10 ** (snr_db / 10)), 3.0)
            rx_a[b * Ns:(b + 1) * Ns] = rb
        j4 = j4_fixed_median(rx_a, M0, P.N_DFT)
        bk = bkmap[('turb_downlink', 10.0, snr_db, turb)]
        cal_j4.append(j4)
        cal_bestk.append(int(bk))
        cal_meta.append({'scene': 'turb_downlink', 'lw_khz': 10.0, 'snr': snr_db, 'turb': turb})
    # 湍流上行 2 点
    s0_up = P.SEED_TURB0 + UPLINK_SEED_OFFSET
    for turb, snr_db in [('uplink_moderate', 16.0), ('uplink_strong', 20.0)]:
        Ns = P.N_DFT
        rx_a = np.zeros(n_blocks * Ns, dtype=complex)
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, 10 ** (snr_db / 10), turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
                seed=s0_up + b, lw=10e3)
            hb = S.estimate_h_blind_perblock(r['rx_raw'], 10 ** (snr_db / 10))
            rb = amp_limit(mmse_equalize(r['rx_raw'], hb, 10 ** (snr_db / 10)), 3.0)
            rx_a[b * Ns:(b + 1) * Ns] = rb
        j4 = j4_fixed_median(rx_a, M0, P.N_DFT)
        bk = bkmap[('turb_uplink', 10.0, snr_db, turb)]
        cal_j4.append(j4)
        cal_bestk.append(int(bk))
        cal_meta.append({'scene': 'turb_uplink', 'lw_khz': 10.0, 'snr': snr_db, 'turb': turb})
    return cal_j4, cal_bestk, cal_meta


# =============================================================================
# 主流程
# =============================================================================
def main():
    t0 = time.time()
    M0 = P.M0
    n_blocks = P.N_BLOCKS
    print("=" * 100)
    print("A1 参数适配验证实验: 自适应 K 策略 vs 固定 K (5 seed)")
    print(f"M0={M0}, N_DFT={P.N_DFT}, N_BLOCKS={n_blocks} (N_sym={n_blocks*P.N_DFT}/seed)")
    print(f"5 seed | 固定 K{FIXED_KS} | oracle K{ORACLE_KS} | VV Nw={VV_NW}")
    print(f"J4 修正 (mod 2π 增量, 不 unwrap) | 信道共享 (AWGN awgn_wiener / 湍流 generate_shared)")
    print("=" * 100)

    # --- 1. J4 阈值拟合 (标定 35 点, 重算修正 J4) ---
    print("\n[1] J4 阈值拟合 (标定 35 点, 重算修正 J4)...")
    cal_j4, cal_bestk, cal_meta = recompute_calibration_j4_and_bestk(M0, n_blocks)
    thr, acc, cm = fit_j4_threshold(cal_j4, cal_bestk, default_k=16, high_j4_k=32)
    print(f"    拟合阈值 thr={thr:.4e} | 正确率={acc:.3f} (35点)")
    print(f"    映射: J4>={thr:.3e}→K32, else→K16 | 子集{{K16,K32}}混淆: {cm}")
    # 验证集 8 点的 J4 预测正确率也报 (in-sample 同分布, 仍记)
    print(f"    注: in-sample 拟合, 有乐观偏差 (标定=验证同分布).")
    # 修正 J4 vs best_k Spearman
    def spearman(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(y)).astype(float)
        rx -= rx.mean(); ry -= ry.mean()
        d = np.sqrt(np.sum(rx**2) * np.sum(ry**2))
        return float(np.sum(rx * ry) / d) if d > 0 else float('nan')
    rho_j4 = spearman(cal_j4, cal_bestk)
    print(f"    修正-J4 vs best_k Spearman ρ = {rho_j4:.4f}")

    # --- 2. 8 场景点 × 5 seed ---
    results = []
    # AWGN: 线宽 [10,100,1000]kHz × 18dB
    print("\n[2] AWGN 场景点 (线宽 [10,100,1000]kHz × 18dB, 5 seed)...")
    for lw in [10e3, 100e3, 1000e3]:
        t1 = time.time()
        r = run_awgn_point(lw, 18.0, M0, n_blocks, N_SEEDS, P.SEED_AWGN, thr)
        results.append(r)
        print(f"    awgn lw={lw/1e3:.0f}kHz SNR=18dB done "
              f"({time.time()-t1:.1f}s) | K16 BER={r['bers']['fixed_k16']['mean']:.3e}")

    # 湍流下行 3 点 @10kHz
    print("\n[3] 湍流下行 @10kHz (weak12/moderate16/strong20, 5 seed)...")
    for turb, snr_db in [('weak', 12.0), ('moderate', 16.0), ('strong', 20.0)]:
        t1 = time.time()
        r = run_turb_point(turb, snr_db, 10e3, M0, n_blocks, N_SEEDS,
                           P.SEED_TURB0, is_uplink=False, j4_threshold=thr)
        results.append(r)
        print(f"    turb_dl {turb} SNR={snr_db:.0f}dB done "
              f"({time.time()-t1:.1f}s) | K16 BER={r['bers']['fixed_k16']['mean']:.3e}")

    # 湍流上行 2 点 @10kHz
    print("\n[4] 湍流上行 @10kHz (uplink_moderate16/uplink_strong20, 5 seed)...")
    s0_up = P.SEED_TURB0 + UPLINK_SEED_OFFSET
    for turb, snr_db in [('uplink_moderate', 16.0), ('uplink_strong', 20.0)]:
        t1 = time.time()
        r = run_turb_point(turb, snr_db, 10e3, M0, n_blocks, N_SEEDS,
                           s0_up, is_uplink=True, j4_threshold=thr)
        results.append(r)
        print(f"    turb_ul {turb} SNR={snr_db:.0f}dB done "
              f"({time.time()-t1:.1f}s) | K16 BER={r['bers']['fixed_k16']['mean']:.3e}")

    # --- 5. 汇总 ---
    # aggregate gain (8 点 mean of gain_vs_k16_db)
    agg_methods = ['adaptive_oracle', 'adaptive_j4', 'adaptive_snr',
                   'fixed_k1', 'fixed_k8', 'fixed_k32', 'vv_nw64']
    agg_gain = {}
    for m in agg_methods:
        vals = [res['gain_vs_k16_db'].get(m, float('nan')) for res in results]
        vals = [v for v in vals if not np.isnan(v)]
        agg_gain[m] = float(np.mean(vals)) if vals else float('nan')
    # 自适应-J4 CI 显著赢 K16 的点
    j4_sig_points = []
    for res in results:
        if res['sig_win_vs_k16'].get('adaptive_j4', False):
            j4_sig_points.append(_point_label(res))
    n_j4_sig = len(j4_sig_points)
    # PASS/FAIL 判据 (主线定, 只填数字)
    cond1 = n_j4_sig >= 2
    cond2 = agg_gain['adaptive_j4'] < 0
    if cond1 and cond2:
        verdict = (f"PASS: 自适应-J4 在 {n_j4_sig}/8 点 CI 显著赢 K16 (≥2), "
                   f"aggregate gain_vs_k16 = {agg_gain['adaptive_j4']:.3f} dB (<0).")
    elif cond1:
        verdict = (f"FAIL: 自适应-J4 显著赢 {n_j4_sig}/8 点 (≥2 达标), 但 aggregate "
                   f"gain_vs_k16 = {agg_gain['adaptive_j4']:.3f} dB (≥0, 未达标).")
    elif cond2:
        verdict = (f"FAIL: aggregate gain_vs_k16 = {agg_gain['adaptive_j4']:.3f} dB (<0 达标), "
                   f"但自适应-J4 仅 {n_j4_sig}/8 点 CI 显著赢 (<2).")
    else:
        verdict = (f"FAIL: 自适应-J4 仅 {n_j4_sig}/8 点显著赢 (<2), aggregate gain "
                   f"{agg_gain['adaptive_j4']:.3f} dB (≥0). 两判据均不满足.")

    elapsed = time.time() - t0

    out = {
        'meta': {
            'task': 'A1 validation: 自适应 K 策略 vs 固定 K',
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'n_seeds': N_SEEDS,
            'n_points': len(results),
            'j4_fixed': True,
            'j4_fix_note': '标定 J4 unwrap bug → mod 2π 相位增量 (不 unwrap)',
            'fixed_ks': FIXED_KS,
            'oracle_ks': ORACLE_KS,
            'vv_nw': VV_NW,
            'snr_k_map': SNR_K_MAP,
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_BLOCKS': P.N_BLOCKS,
            'fairness': 'AWGN 同 awgn_wiener_channel; 湍流同 generate_shared_realization_apsk + 盲 h 均衡',
            'reused_functions': ['parity_tuning_sweep.ber_nda_seg_k_awgn',
                                 'parity_tuning_sweep.ber_nda_seg_k_eval',
                                 'parity_tuning_sweep.ber_vv_nw_eval',
                                 'S.awgn_wiener_channel', 'S.estimate_h_blind_perblock',
                                 'generate_shared_realization_apsk', 'mmse_equalize',
                                 'amp_limit', 'resolve_m16apsk_blockwise'],
            'common_or_simulator_or_params_modified': False,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'j4_mapping': {
            'threshold': thr,
            'default_k': 16,
            'high_j4_k': 32,
            'accuracy_on_calibration': acc,
            'subset_confusion': cm,
            'fixed_j4_spearman_vs_best_k': rho_j4,
            'in_sample_note': 'in-sample 拟合 (标定=验证同分布), 有乐观偏差',
        },
        'results': results,
        'summary': {
            'aggregate_gain_vs_k16_db': agg_gain,
            'n_points_adaptive_j4_beats_k16': n_j4_sig,
            'j4_sig_win_points': j4_sig_points,
            'verdict': verdict,
        },
    }
    out_json = os.path.join(_HERE, '_a1_adaptive_k_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 控制台汇总表 ---
    print("\n" + "=" * 100)
    print("8 点 × 自适应-oracle / 自适应-J4 / 固定-K16 mean BER (5 seed)")
    print("-" * 100)
    hdr = (f"{'点':>4} {'scene':<14} {'lw_kHz':>7} {'SNR':>4} {'turb':<18} | "
           f"{'oracle':>11} {'adapt-J4':>11} {'K16':>11} {'gainJ4_dB':>9}")
    print(hdr)
    for i, res in enumerate(results):
        bo = res['bers']['adaptive_oracle']['mean']
        bj = res['bers']['adaptive_j4']['mean']
        b16 = res['bers']['fixed_k16']['mean']
        gj = res['gain_vs_k16_db'].get('adaptive_j4', float('nan'))
        turb = res['turbulence'] or '-'
        print(f"{i+1:>4} {res['scene']:<14} {res['linewidth_khz']:>7.0f} "
              f"{res['snr_db']:>4.0f} {turb:<18} | {bo:>11.3e} {bj:>11.3e} {b16:>11.3e} {gj:>9.3f}")
    print("-" * 100)
    print("aggregate gain_vs_k16 (8 点 mean, dB, 负=好):")
    for m in ['adaptive_oracle', 'adaptive_j4', 'adaptive_snr',
              'fixed_k1', 'fixed_k8', 'fixed_k32', 'vv_nw64']:
        print(f"    {m:<16} {agg_gain[m]:>+8.3f}")
    print(f"\n自适应-J4 CI 显著赢 K16 的点: {n_j4_sig}/8  → {j4_sig_points}")
    print(f"\nVERDICT: {verdict}")
    print(f"[总耗时] {elapsed:.1f} s")


def _point_label(res):
    turb = res['turbulence'] or '-'
    return f"{res['scene']}/{turb}/lw{res['linewidth_khz']:.0f}kHz/SNR{res['snr_db']:.0f}"


if __name__ == '__main__':
    main()
