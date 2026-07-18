# -*- coding: utf-8 -*-
"""A2 对等调参实验 (handoff H006 第一项任务): NDA 扫 K vs VV 扫 Nw.

目的 (handoff): 回答"加定语找特长"——NDA-segmented 扫 K=[1,4,8,16,32], VV 扫
Nw=[8,16,32,64,128], 每场景同信道同 seed, 找是否存在"某 K 下 NDA 最优 BER < VV 最优 Nw BER"
的精度特长场景 (防御性材料, 备被问"这俩不一样吗"时掏出来).

最高纪律 (同 uplink_vv_check.py / vv_vs_nda_checkup.py):
  1. 只改本 explore/nda-awgn-tracking-sandbox/ 目录, 绝不改 common/simulator/params.
  2. 复用已有函数 (nda_segmented_eq / ber_vv_turb_nw / VV.vv_cpr_m16apsk /
     S.awgn_wiener_channel / generate_shared_realization_apsk / estimate_h_blind_perblock).
  3. 三方 (NDA 每个 K / VV 每个 Nw) 同信道同 seed (公平对照).
  4. 只跑数字 + 机械分类, 不判断方向不建议.

K=1 含义: nda_segmented_eq(seg, M0, K=1) 等价整块 mean-angle (none 模式), 作 NDA 的
"无块内跟踪" baseline, 跟 segmented (K>=4) 对照.

机械分类 (每场景):
  - nda_best: min over K of ber_nda(K)
  - vv_best:  min over Nw of ber_vv(Nw)
  - rel = (nda_best - vv_best) / vv_best
    rel < -5%:  'NDA赢'   (NDA 最优 K 的 BER 比 VV 最优 Nw 低 5%+)
    |rel| <= 5%: '持平'
    rel > +5%:  'VV赢'

场景 (handoff A2, 全场景无死角):
  扫描1 AWGN 线宽: (8,8)-16APSK, 18dB, 线宽 [10,50,100,200,500]kHz
  扫描2 湍流:      (8,8)-16APSK, 10kHz, weak 12dB / moderate 16dB / strong 20dB
  扫描3 上行:      (8,8)-16APSK, 10kHz, uplink_moderate 16dB / uplink_strong 20dB

运行: cd projects/simulation && python explore/nda-awgn-tracking-sandbox/parity_tuning_sweep.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 (与 uplink_vv_check.py 同构) ---
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
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402  (参数只读)
import sc_nda_ml_sim as S  # noqa: E402  (复用 fft_foe_m0_omega / awgn_wiener_channel / estimate_h)
import run_vv_ablation as VV  # noqa: E402  (复用 vv_cpr_m16apsk)
from params import SimulationConfig  # noqa: E402

# 扩大参数范围 (用户要求"扫全一些"): K 上界 128 (N_DFT=256 每段 2 样本),
# Nw 上界 256 (整块窗), 覆盖理论可达全区间.
KS = [1, 2, 4, 8, 16, 32, 64, 128]   # NDA 段数扫描 (K=1 = none 整块模式)
NWS = [4, 8, 16, 32, 64, 128, 256]   # VV 滑窗长度扫描
UPLINK_SEED_OFFSET = 500000     # 同 run_uplink_experiment (错开下行 seed)


# =============================================================================
# NDA-segmented 等权块内 CPE 恢复 (参数化 K). 复用 uplink_vv_check.nda_segmented_eq.
# K=1 时 seg_len=N, 等价整块 mean-angle (none 模式).
# =============================================================================
def nda_segmented_eq_k(seg, M0, K):
    """NDA-segmented 等权块内 CPE 恢复 (K 可变). unwrap 在升幂域, 最后 /M0.

    raised = rx**M0 (等权升幂, 未归一化)
    每段 s_k: seg_phi[k] = angle(raised[lo:hi].mean())   # 升幂域, 不 /M0
    seg_phi_unw = np.unwrap(seg_phi)                     # 升幂域 unwrap
    phi_raised  = np.interp(arange(N), seg_center, seg_phi_unw)
    phi_est     = phi_raised / M0                        # 最后 /M0
    K=1: seg_len=N, 单段 mean-angle (等价 none).
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    seg_len = N // K
    raised = seg ** M0
    seg_phi = np.empty(K)
    seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k * seg_len, (k + 1) * seg_len
        seg_phi[k] = np.angle(raised[lo:hi].mean())
        seg_center[k] = (lo + hi) / 2.0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_raised = np.interp(t, seg_center, seg_phi_unw)
    phi_est = phi_raised / M0
    return seg * np.exp(-1j * phi_est)


def ber_nda_seg_k_eval(rx, tx_bits, M0, K):
    """NDA-segmented(K) BER: 逐 N_DFT 块 fft_foe + nda_segmented_eq_k(K) + resolve."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, M0)
        k_idx = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k_idx)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_segmented_eq_k(seg_foe, M0, K)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_nda_seg_k_awgn(rx, tx_bits, M0, K):
    """NDA-segmented(K) BER (AWGN, 无 CFO 无 h): 逐块 nda_segmented_eq_k + resolve."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_segmented_eq_k(seg, M0, K)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_vv_nw_eval(rx, tx_bits, Nw, intra_foe=False, M0=None):
    """VV(Nw) BER: 逐 N_DFT 块 (可选 fft_foe) + vv_cpr_m16apsk(Nw) + resolve."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        if intra_foe:
            omega_est = S.fft_foe_m0_omega(seg, M0)
            k_idx = np.arange(P.N_DFT)
            seg = seg * np.exp(-1j * omega_est * k_idx)
        rc, _ = VV.vv_cpr_m16apsk(seg, Nw=Nw)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 机械分类
# =============================================================================
def classify_nda_vs_vv(nda_bers_by_k, vv_bers_by_nw):
    """找 NDA 最优 K 和 VV 最优 Nw, 比较 BER.

    返回 dict: nda_best_k, nda_best_ber, vv_best_nw, vv_best_ber, rel, cat.
    rel = (nda_best - vv_best) / vv_best
    rel < -5%: 'NDA赢'; |rel|<=5%: '持平'; rel>+5%: 'VV赢'.
    """
    nda_best_k = min(nda_bers_by_k, key=lambda k: nda_bers_by_k[k])
    nda_best = nda_bers_by_k[nda_best_k]
    vv_best_nw = min(vv_bers_by_nw, key=lambda nw: vv_bers_by_nw[nw])
    vv_best = vv_bers_by_nw[vv_best_nw]
    rel = (nda_best - vv_best) / vv_best if vv_best > 0 else None
    if rel is None:
        cat = 'n/a'
    elif rel < -0.05:
        cat = 'NDA赢'
    elif rel <= 0.05:
        cat = '持平'
    else:
        cat = 'VV赢'
    return {
        'nda_best_k': int(nda_best_k),
        'nda_best_ber': float(nda_best),
        'vv_best_nw': int(vv_best_nw),
        'vv_best_ber': float(vv_best),
        'rel': (float(rel) if rel is not None else None),
        'cat': cat,
    }


# =============================================================================
# 扫描1 AWGN 线宽扫描: NDA(K扫) vs VV(Nw扫). 同信道同 seed.
# =============================================================================
def sweep_awgn_linewidth(linewidths_hz, snr_db=18.0, n_blocks=None, seed_base=None):
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed_base is None:
        seed_base = P.SEED_AWGN
    N_sym = n_blocks * P.N_DFT
    M0 = P.M0
    T_S = P.T_S
    print("\n" + "#" * 30 + f" 扫描1 AWGN 线宽 (SNR={snr_db}dB, (8,8)-16APSK) " + "#" * 30)
    print(f"N_sym={N_sym}/点, M0={M0}, NDA K∈{KS}, VV Nw∈{NWS}")
    hdr = (f"{'线宽kHz':>8} |" + "".join(f"{f'NDA K{k}':>11}" for k in KS) + " |"
           + "".join(f"{f'VV Nw{nw}':>11}" for nw in NWS) + " | " + f"{'cat':>6}")
    print(hdr)
    rows = []
    for lw in linewidths_hz:
        sigma2_p = 2 * np.pi * lw * T_S
        seed = seed_base + int(snr_db * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, _phi = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
        # NDA 每个 K
        nda_bers = {}
        for K in KS:
            ne, nb = ber_nda_seg_k_awgn(rx, bits, M0, K)
            nda_bers[K] = ne / nb
        # VV 每个 Nw
        vv_bers = {}
        for nw in NWS:
            ne, nb = ber_vv_nw_eval(rx, bits, nw, intra_foe=False)
            vv_bers[nw] = ne / nb
        cls = classify_nda_vs_vv(nda_bers, vv_bers)
        line = (f"{lw/1e3:>8.0f} |" + "".join(f"{nda_bers[k]:>11.3e}" for k in KS) + " |"
                + "".join(f"{vv_bers[nw]:>11.3e}" for nw in NWS) + " | " + f"{cls['cat']:>6}")
        print(line)
        rows.append({
            'linewidth_hz': float(lw), 'linewidth_khz': float(lw / 1e3),
            'sigma2_p': float(sigma2_p), 'snr_db': float(snr_db),
            'nda_bers_by_k': {int(k): float(v) for k, v in nda_bers.items()},
            'vv_bers_by_nw': {int(n): float(v) for n, v in vv_bers.items()},
            **cls,
        })
    return rows


# =============================================================================
# 扫描2 湍流 (下行): NDA(K扫) vs VV(Nw扫). 10kHz, (8,8)-16APSK.
# weak 12dB / moderate 16dB / strong 20dB. 两阶段 fft_foe + CPE.
# =============================================================================
def sweep_turbulence(turb_specs, n_blocks=None, seed0=None, lw=10e3):
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed0 is None:
        seed0 = P.SEED_TURB0
    cfg = SimulationConfig()
    Ns = P.N_DFT
    M0 = P.M0
    print("\n" + "#" * 30 + f" 扫描2 湍流 (下行, lw={lw/1e3:.0f}kHz, (8,8)-16APSK) " + "#" * 30)
    print(f"N_sym={n_blocks*Ns}/点, M0={M0}, NDA K∈{KS}, VV Nw∈{NWS}")
    rows = []
    for spec in turb_specs:
        turb = spec['name']
        gamma_db = spec['snr_db']
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = {k: 0 for k in KS}
        nb_nda = {k: 0 for k in KS}
        ne_vv = {nw: 0 for nw in NWS}
        nb_vv = {nw: 0 for nw in NWS}
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
                seed=seed0 + b, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            for K in KS:
                ne, nb = ber_nda_seg_k_eval(rx_blind, bits, M0, K)
                ne_nda[K] += ne; nb_nda[K] += nb
            for nw in NWS:
                ne, nb = ber_vv_nw_eval(rx_blind, bits, nw, intra_foe=True, M0=M0)
                ne_vv[nw] += ne; nb_vv[nw] += nb
        nda_bers = {k: ne_nda[k] / nb_nda[k] for k in KS}
        vv_bers = {nw: ne_vv[nw] / nb_vv[nw] for nw in NWS}
        cls = classify_nda_vs_vv(nda_bers, vv_bers)
        line = (f"{turb:>16} {gamma_db:>5.0f}dB | "
                + f"NDA best K{cls['nda_best_k']}={cls['nda_best_ber']:.3e}  "
                + f"VV best Nw{cls['vv_best_nw']}={cls['vv_best_ber']:.3e}  "
                + f"rel={cls['rel']:+.3f}  {cls['cat']}")
        print(line)
        rows.append({
            'turbulence': turb, 'snr_db': float(gamma_db),
            'alpha_beta': list(P.TURB_ALPHA_BETA[turb]),
            'linewidth_hz': float(lw),
            'nda_bers_by_k': {int(k): float(v) for k, v in nda_bers.items()},
            'vv_bers_by_nw': {int(n): float(v) for n, v in vv_bers.items()},
            **cls,
        })
    return rows


# =============================================================================
# 扫描3 上行湍流: NDA(K扫) vs VV(Nw扫). 10kHz, (8,8)-16APSK.
# uplink_moderate 16dB / uplink_strong 20dB. 两阶段 fft_foe + CPE.
# =============================================================================
def sweep_uplink(turb_specs, n_blocks=None, seed0_base=None, lw=10e3):
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed0_base is None:
        seed0_base = P.SEED_TURB0 + UPLINK_SEED_OFFSET
    cfg = SimulationConfig()
    Ns = P.N_DFT
    M0 = P.M0
    print("\n" + "#" * 30 + f" 扫描3 上行湍流 (lw={lw/1e3:.0f}kHz, (8,8)-16APSK) " + "#" * 30)
    print(f"N_sym={n_blocks*Ns}/点/场景, M0={M0}, NDA K∈{KS}, VV Nw∈{NWS}")
    rows = []
    for spec in turb_specs:
        turb = spec['name']
        gamma_db = spec['snr_db']
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = {k: 0 for k in KS}
        nb_nda = {k: 0 for k in KS}
        ne_vv = {nw: 0 for nw in NWS}
        nb_vv = {nw: 0 for nw in NWS}
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
                seed=seed0_base + b, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            for K in KS:
                ne, nb = ber_nda_seg_k_eval(rx_blind, bits, M0, K)
                ne_nda[K] += ne; nb_nda[K] += nb
            for nw in NWS:
                ne, nb = ber_vv_nw_eval(rx_blind, bits, nw, intra_foe=True, M0=M0)
                ne_vv[nw] += ne; nb_vv[nw] += nb
        nda_bers = {k: ne_nda[k] / nb_nda[k] for k in KS}
        vv_bers = {nw: ne_vv[nw] / nb_vv[nw] for nw in NWS}
        cls = classify_nda_vs_vv(nda_bers, vv_bers)
        line = (f"{turb:>20} {gamma_db:>5.0f}dB | "
                + f"NDA best K{cls['nda_best_k']}={cls['nda_best_ber']:.3e}  "
                + f"VV best Nw{cls['vv_best_nw']}={cls['vv_best_ber']:.3e}  "
                + f"rel={cls['rel']:+.3f}  {cls['cat']}")
        print(line)
        rows.append({
            'turbulence': turb, 'snr_db': float(gamma_db),
            'alpha_beta': list(P.UPLINK_ALPHA_BETA[turb]),
            'linewidth_hz': float(lw),
            'nda_bers_by_k': {int(k): float(v) for k, v in nda_bers.items()},
            'vv_bers_by_nw': {int(n): float(v) for n, v in vv_bers.items()},
            **cls,
        })
    return rows


# =============================================================================
# JSON 落盘
# =============================================================================
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


def main():
    t0 = time.time()
    print("=" * 100)
    print("A2 对等调参实验 (handoff H006): NDA 扫 K vs VV 扫 Nw")
    print(f"M0={P.M0}, N_DFT={P.N_DFT}, N_BLOCKS={P.N_BLOCKS}, HDFEC={P.HDFEC}")
    print(f"NDA K∈{KS} (K=1=none模式), VV Nw∈{NWS}")
    print(f"三方公平: 同信道同 seed; 只跑数字+机械分类")
    print(f"分类: rel=(NDAbest-VVbest)/VVbest; <-5% NDA赢 / |rel|<=5% 持平 / >+5% VV赢")
    print("=" * 100)

    # --- 扫描1 AWGN 线宽 × SNR (用户要求扩大范围, 之前只 18dB 单点违反 C1) ---
    linewidths = [10e3, 50e3, 100e3, 200e3, 500e3, 1000e3]
    snrs_awgn = [14.0, 16.0, 18.0, 20.0, 22.0]
    sweep1 = []
    for snr_db in snrs_awgn:
        sweep1.extend(sweep_awgn_linewidth(linewidths, snr_db=snr_db))

    # --- 扫描2 下行湍流 ---
    turb_specs = [
        {'name': 'weak', 'snr_db': 12.0},
        {'name': 'moderate', 'snr_db': 16.0},
        {'name': 'strong', 'snr_db': 20.0},
    ]
    sweep2 = sweep_turbulence(turb_specs, lw=10e3)

    # --- 扫描3 上行湍流 ---
    uplink_specs = [
        {'name': 'uplink_moderate', 'snr_db': 16.0},
        {'name': 'uplink_strong', 'snr_db': 20.0},
    ]
    sweep3 = sweep_uplink(uplink_specs, lw=10e3)

    elapsed = time.time() - t0

    # --- 汇总 ---
    all_cats = ([r['cat'] for r in sweep1]
                + [r['cat'] for r in sweep2]
                + [r['cat'] for r in sweep3])
    summary = {
        'total_points': len(all_cats),
        'nda_wins': sum(1 for c in all_cats if c == 'NDA赢'),
        'ties': sum(1 for c in all_cats if c == '持平'),
        'vv_wins': sum(1 for c in all_cats if c == 'VV赢'),
        'sweep1_cats': [r['cat'] for r in sweep1],
        'sweep2_cats': [r['cat'] for r in sweep2],
        'sweep3_cats': [r['cat'] for r in sweep3],
    }

    out = {
        'meta': {
            'task': 'A2 对等调参实验: NDA 扫 K vs VV 扫 Nw (handoff H006 第一项任务)',
            'purpose': ('回答"加定语找特长": NDA-segmented 扫 K, VV 扫 Nw, '
                        '找"某 K 下 NDA 最优 BER < VV 最优 Nw BER"的精度特长场景'),
            'nda_mode': 'NDA-segmented 等权 (K 段, unwrap 升幂域最后 /M0); K=1=none 整块',
            'vv_mode': 'VV.vv_cpr_m16apsk(seg, Nw=X); 滑窗 mean unwrap/M0',
            'fairness': '三方同信道同 seed (AWGN 同 awgn_wiener_channel; '
                        '湍流同 generate_shared_realization_apsk + 同 rx_blind)',
            'classification': ('每场景: nda_best=min_K ber, vv_best=min_Nw ber; '
                               'rel=(nda_best-vv_best)/vv_best; '
                               '<-5% NDA赢 / |rel|<=5% 持平 / >+5% VV赢'),
            'K_values': KS,
            'Nw_values': NWS,
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_BLOCKS': P.N_BLOCKS,
            'LASER_LW_Hz': float(P.LASER_LW),
            'T_S': float(P.T_S),
            'HDFEC': P.HDFEC,
            'n_seeds': 1,
            'common_or_simulator_or_params_modified': False,
            'reused_functions': ['nda_segmented_eq (uplink_vv_check)',
                                 'VV.vv_cpr_m16apsk', 'S.fft_foe_m0_omega',
                                 'S.awgn_wiener_channel', 'S.estimate_h_blind_perblock',
                                 'generate_shared_realization_apsk', 'mmse_equalize',
                                 'amp_limit', 'resolve_m16apsk_blockwise'],
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'sweep1_awgn_linewidth': sweep1,
        'sweep2_turbulence_downlink': sweep2,
        'sweep3_turbulence_uplink': sweep3,
        'summary': summary,
    }
    out_json = os.path.join(_HERE, '_parity_tuning_sweep.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    print("\n" + "=" * 100)
    print(f"汇总: 共 {summary['total_points']} 个场景点")
    print(f"  NDA赢: {summary['nda_wins']}  持平: {summary['ties']}  VV赢: {summary['vv_wins']}")
    print(f"  扫描1 (AWGN 线宽): {summary['sweep1_cats']}")
    print(f"  扫描2 (下行湍流): {summary['sweep2_cats']}")
    print(f"  扫描3 (上行湍流): {summary['sweep3_cats']}")
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
