# -*- coding: utf-8 -*-
"""NDA-ML (加权/等权) vs VV 三方参数扫描体检.

任务 (brief): 跑 3 扫描 (线宽 / 调制阶数 / 湍流), 查 NDA-加权 vs VV 的 BER 差距
会不会随参数拉开. 只跑数字 + 机械分类, 不判断方向不建议.

最高纪律 (brief §0):
  1. 只改本 explore/nda-awgn-tracking-sandbox/ 目录, 绝不改 common/ / simulator/ / params.py.
  2. NDA-ML 加权版公式按 brief §3: unwrap 在升幂域, 最后 /M0.
  3. 三方 (NDA-加权 / NDA-等权 / VV) 同信道同 seed 同 tx_bits.
  4. 只跑数字 + 机械分类.

3 扫描 (brief §2):
  扫描1 线宽: AWGN, (8,8)-16APSK, 18dB, 线宽 [10,50,100,200,500]kHz, sigma2_p=2*pi*lw*T_S.
  扫描2 调制阶数: AWGN, 10kHz, 18dB, [8psk_M4, 8psk_M8, m16apsk_M8].
  扫描3 湍流: 10kHz, (8,8)-16APSK, weak 12dB / moderate 16dB / strong 20dB, NDA intra='none'.

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/vv_vs_nda_checkup.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 (与 sc_nda_ml_sim.py / run_vv_ablation.py 同构) ---
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
    apsk8_mod, apsk8_demod,
    resolve_apsk8_blockwise,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402  (参数全溯源, 只读不改)
import sc_nda_ml_sim as S  # noqa: E402  (复用 awgn_wiener_channel / nda_ml 等权 / estimate_h / fft_foe)
import run_vv_ablation as VV  # noqa: E402  (复用 vv_cpr_m16apsk / ber_vv_*)
from params import SimulationConfig  # noqa: E402


# =============================================================================
# NDA-ML 加权版恢复 (brief §3): unwrap 在升幂域, 最后 /M0.
# =============================================================================
def nda_weighted_recovery(seg, M0, mode='segmented'):
    """加权 NDA-ML 块内 CPE 恢复 (brief §3 公式逐字).

    mag = |rx| (保护下界 1e-12)
    yn  = (rx/mag)**M0       # 归一化升幂 (brief §3)
    w   = mag**2             # ML 权重
    none:        phi_est = angle((w*yn).sum()) / M0
    segmented:   seg_phi[k] = angle((w[lo:hi]*yn[lo:hi]).sum())   # 不 /M0 (升幂域)
                 seg_phi_unw = np.unwrap(seg_phi)                  # 升幂域 unwrap
                 phi_raised  = np.interp(arange(N), seg_center, seg_phi_unw)
                 phi_est     = phi_raised / M0                     # 最后 /M0
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    mag = np.abs(seg)
    mag[mag < 1e-12] = 1e-12
    yn = (seg / mag) ** M0          # 归一化升幂 (brief §3)
    w = mag ** 2                    # ML 权重 (brief §3)

    if mode == 'segmented':
        K = 8                       # brief §3: K=8
        seg_len = N // K
        seg_phi = np.empty(K)
        seg_center = np.empty(K)
        for k in range(K):
            lo, hi = k * seg_len, (k + 1) * seg_len
            seg_phi[k] = np.angle((w[lo:hi] * yn[lo:hi]).sum())   # 不 /M0 (升幂域, brief §3)
            seg_center[k] = (lo + hi) / 2.0
        seg_phi_unw = np.unwrap(seg_phi)              # 升幂域 unwrap (brief §3)
        t = np.arange(N)
        phi_raised = np.interp(t, seg_center, seg_phi_unw)
        phi_est = phi_raised / M0                     # 最后 /M0 (brief §3)
    else:  # 'none'
        phi_est = np.angle((w * yn).sum()) / M0       # 整块加权 mean-angle (brief §3)
    rx_comp = seg * np.exp(-1j * phi_est)
    return rx_comp


def nda_equalweight_recovery(seg, M0, mode='segmented'):
    """等权 NDA-ML 块内 CPE 恢复 (brief §3 等权版: (w*yn).sum() -> (rx**M0)[lo:hi].mean()).

    unwrap 顺序与加权版一致 (升幂域 unwrap, 最后 /M0). 复用 common nda_ml_recovery 逻辑:
    对 'segmented' 与 'none' 两种 intra 模式, raised=rx**M0 (未归一化升幂, 等权).
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    raised = seg ** M0              # 等权升幂 (未归一化, 与 common nda_ml_recovery 一致)

    if mode == 'segmented':
        K = 8
        seg_len = N // K
        seg_phi = np.empty(K)
        seg_center = np.empty(K)
        for k in range(K):
            lo, hi = k * seg_len, (k + 1) * seg_len
            seg_phi[k] = np.angle(raised[lo:hi].mean())   # 等权 mean-angle (升幂域)
            seg_center[k] = (lo + hi) / 2.0
        seg_phi_unw = np.unwrap(seg_phi)
        t = np.arange(N)
        phi_raised = np.interp(t, seg_center, seg_phi_unw)
        phi_est = phi_raised / M0                         # 最后 /M0
    else:  # 'none'
        phi_est = np.angle(raised.mean()) / M0
    rx_comp = seg * np.exp(-1j * phi_est)
    return rx_comp


# =============================================================================
# VV CFR 适配 (brief §3: 调 run_vv_ablation.vv_cpr_m16apsk; 8psk 时复制逻辑改 M).
# =============================================================================
def vv_cpr_generic(rx, M0, Nw=64):
    """VV CFR 通用版 (复制 run_vv_ablation.vv_cpr_m16apsk, M0 可变, brief §3).

    升 M0 次幂去调制 → 滑窗 mean → unwrap/M0 解 M0-fold 模糊.
    M0=8 时与 VV.vv_cpr_m16apsk 完全等价 (brief §3: m16apsk 默认 Nw=64, M0=8).
    """
    raised = rx ** M0
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg)) / M0    # M0 unwrap (brief §3: VV 的 M 跟 NDA 的 M0 一致)
    return rx * np.exp(-1j * pe), pe


# =============================================================================
# BER 外壳 (三方统一, brief §4): 逐 N_DFT=256 块 recovery_fn -> resolve_*_blockwise
# -> demod -> 数错误位. 调制匹配 (apsk8 用 apsk8_*, m16apsk 用 m16apsk_*).
# =============================================================================
def ber_eval(rx, tx_bits, recovery_fn, mod, M0, n_dft=None, block_size=None,
             intra_foe=False):
    """三方统一 BER 外壳.

    recovery_fn(seg) -> rx_comp; 逐 n_dft 块 (默认 P.N_DFT); 末尾 resolve_*_blockwise
    (block_size 默认 P.BLOCK_SIZE_RESOLVE) -> demod -> 数错误位.
    mod: 'apsk8' / 'm16apsk'. M0: 升幂阶数.
    intra_foe: 湍流场景为 True 时先 fft_foe_m0_omega 补 CFO (两阶段第一步).
    返回 (n_err, n_bits).
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if n_dft is None:
        n_dft = P.N_DFT
    if block_size is None:
        block_size = P.BLOCK_SIZE_RESOLVE
    n_blk = N // n_dft
    L = n_blk * n_dft
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * n_dft:(b + 1) * n_dft]
        if intra_foe:
            omega_est = S.fft_foe_m0_omega(seg, M0)
            k = np.arange(n_dft)
            seg = seg * np.exp(-1j * omega_est * k)
        rx_comp[b * n_dft:(b + 1) * n_dft] = recovery_fn(seg)
    if mod == 'apsk8':
        bits_per_sym = 3
        tb = tx_bits[:L * bits_per_sym]
        resolved = resolve_apsk8_blockwise(rx_comp, tb, block_size=block_size)
        n_err = int(np.sum(tb != apsk8_demod(resolved)))
    else:  # 'm16apsk'
        bits_per_sym = 4
        tb = tx_bits[:L * bits_per_sym]
        resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=block_size)
        n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 机械分类 (brief §5): NDA-加权 vs VV / NDA-加权 vs NDA-等权.
# =============================================================================
def classify(b_weighted, b_ref):
    """机械分类 (brief §5).

    rel = (ber_weighted - ber_ref)/ber_ref.
    rel <= -10%: 拉开 (加权赢)
    |rel| < 10%: 持平
    rel >= +10%: 反超 (VV/等权赢)
    """
    if b_ref is None or b_ref == 0 or b_weighted is None:
        return None, None
    rel = (b_weighted - b_ref) / b_ref
    if rel <= -0.10:
        cat = 'weighted_wins'      # 拉开 (加权 BER 低 = 加权赢)
    elif rel < 0.10:
        cat = 'tie'                # 持平
    else:
        cat = 'weighted_loses'     # 反超 (加权 BER 高 = VV/等权赢)
    return cat, rel


# =============================================================================
# 扫描1 线宽扫描 (AWGN, (8,8)-16APSK, 18dB). brief §2.
# sigma2_p 派生 = 2*pi*lw*T_S (T_S=4e-10, 不读 params 的 SIGMA2_P).
# =============================================================================
def sweep_linewidth(linewidths_hz, snr_db=18.0, n_blocks=None, seed_base=None):
    """线宽扫描: 三方 BER. 信道 S.awgn_wiener_channel(tx, snr, seed, sigma2_p=...).

    三方共用同一 rx (公平前提, brief 纪律 3). sigma2_p=2*pi*lw*T_S (派生, 不读 params).
    AWGN 加权/等权用 segmented (brief §3: segmented 模式 AWGN 用, K=8).
    """
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed_base is None:
        seed_base = P.SEED_AWGN
    N_sym = n_blocks * P.N_DFT
    M0 = P.M0                       # (8,8)-16APSK -> M0=8
    mod = 'm16apsk'
    T_S = P.T_S                     # 4e-10 (brief §2)
    seed = seed_base + int(snr_db * 1000)
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    print(f"\n[扫描1 线宽] AWGN, (8,8)-16APSK, SNR={snr_db}dB, N_sym={N_sym}, seed={seed}")
    print(f"{'线宽(kHz)':>10} {'sigma2_p':>12} {'加权(seg)':>12} {'等权(seg)':>12} {'VV':>12}")
    rows = []
    for lw in linewidths_hz:
        sigma2_p = 2 * np.pi * lw * T_S          # 派生 (brief §2, 不读 params SIGMA2_P)
        rx, _phi_true = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
        ne_w, nb_w = ber_eval(rx, bits,
                              lambda seg: nda_weighted_recovery(seg, M0, mode='segmented'),
                              mod, M0)
        ne_eq, nb_eq = ber_eval(rx, bits,
                                lambda seg: nda_equalweight_recovery(seg, M0, mode='segmented'),
                                mod, M0)
        ne_vv, nb_vv = ber_eval(rx, bits,
                                lambda seg: vv_cpr_generic(seg, M0, Nw=64)[0],
                                mod, M0)
        b_w = ne_w / nb_w
        b_eq = ne_eq / nb_eq
        b_vv = ne_vv / nb_vv
        cat_vv, rel_vv = classify(b_w, b_vv)
        cat_eq, rel_eq = classify(b_w, b_eq)
        print(f"{lw/1e3:>10.0f} {sigma2_p:>12.3e} {b_w:>12.4e} {b_eq:>12.4e} {b_vv:>12.4e}")
        rows.append({
            'linewidth_hz': float(lw),
            'linewidth_khz': float(lw / 1e3),
            'sigma2_p': float(sigma2_p),
            'snr_db': float(snr_db),
            'ber_weighted': float(b_w),
            'ber_equalweight': float(b_eq),
            'ber_vv': float(b_vv),
            'weighted_vs_vv_rel': rel_vv,
            'weighted_vs_vv_cat': cat_vv,
            'weighted_vs_equalweight_rel': rel_eq,
            'weighted_vs_equalweight_cat': cat_eq,
        })
    return rows


# =============================================================================
# 扫描2 调制阶数扫描 (AWGN, 10kHz, 18dB). brief §2.
# 8psk_M4: apsk8 + resolve_apsk8, VV M=4. 8psk_M8: apsk8 + resolve_apsk8, VV M=8.
# m16apsk_M8: m16apsk + resolve_m16apsk, VV M=8.
# =============================================================================
def sweep_modulation(mod_cases, snr_db=18.0, n_blocks=None, seed_base=None,
                     lw=10e3):
    """调制阶数扫描: 三方 BER. AWGN, lw=10kHz, SNR=18dB.

    三方共用同一 rx (同 awgn_wiener_channel, sigma2_p 从 lw 派生). 每调制 case 用其
    (mod_fn, demod_fn, resolve_fn, bits_per_sym, M0). VV 的 M 跟 NDA 的 M0 一致 (brief §3).
    """
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed_base is None:
        seed_base = P.SEED_AWGN
    T_S = P.T_S
    sigma2_p = 2 * np.pi * lw * T_S
    seed = seed_base + int(snr_db * 1000)
    N_sym = n_blocks * P.N_DFT
    print(f"\n[扫描2 调制阶数] AWGN, lw={lw/1e3:.0f}kHz, SNR={snr_db}dB, N_sym={N_sym}, seed={seed}")
    print(f"{'调制':>14} {'M0':>4} {'加权(seg)':>12} {'等权(seg)':>12} {'VV':>12}")
    rows = []
    for case in mod_cases:
        name = case['name']
        M0 = case['M0']
        mod = case['mod']             # 'apsk8' / 'm16apsk'
        mod_fn = case['mod_fn']
        bits_per_sym = case['bits_per_sym']
        # 每 case 独立 bits/tx/seed 派生 (bits 量不同)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * bits_per_sym)
        tx = mod_fn(bits)
        rx, _phi_true = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
        ne_w, nb_w = ber_eval(rx, bits,
                              lambda seg: nda_weighted_recovery(seg, M0, mode='segmented'),
                              mod, M0)
        ne_eq, nb_eq = ber_eval(rx, bits,
                                lambda seg: nda_equalweight_recovery(seg, M0, mode='segmented'),
                                mod, M0)
        ne_vv, nb_vv = ber_eval(rx, bits,
                                lambda seg: vv_cpr_generic(seg, M0, Nw=64)[0],
                                mod, M0)
        b_w = ne_w / nb_w
        b_eq = ne_eq / nb_eq
        b_vv = ne_vv / nb_vv
        cat_vv, rel_vv = classify(b_w, b_vv)
        cat_eq, rel_eq = classify(b_w, b_eq)
        print(f"{name:>14} {M0:>4d} {b_w:>12.4e} {b_eq:>12.4e} {b_vv:>12.4e}")
        rows.append({
            'modulation': name,
            'M0': int(M0),
            'snr_db': float(snr_db),
            'linewidth_hz': float(lw),
            'sigma2_p': float(sigma2_p),
            'ber_weighted': float(b_w),
            'ber_equalweight': float(b_eq),
            'ber_vv': float(b_vv),
            'weighted_vs_vv_rel': rel_vv,
            'weighted_vs_vv_cat': cat_vv,
            'weighted_vs_equalweight_rel': rel_eq,
            'weighted_vs_equalweight_cat': cat_eq,
        })
    return rows


# =============================================================================
# 扫描3 湍流场景 (10kHz, (8,8)-16APSK). brief §2.
# weak 12dB / moderate 16dB / strong 20dB. NDA-ML intra='none' (brief §2 湍流设定).
# =============================================================================
def sweep_turbulence(turb_specs, n_blocks=None, seed0=None, lw=10e3):
    """湍流扫描: 三方 BER. (8,8)-16APSK, lw=10kHz. NDA intra='none'.

    三方共用同一 rx_blind (同 generate_shared_realization_apsk + 同 estimate_h_blind_perblock
    + 同 mmse_equalize + 同 amp_limit). NDA intra='none' (brief §2).
    """
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed0 is None:
        seed0 = P.SEED_TURB0
    cfg = SimulationConfig()
    Ns = P.N_DFT
    M0 = P.M0                       # (8,8)-16APSK -> M0=8
    mod = 'm16apsk'
    print(f"\n[扫描3 湍流] (8,8)-16APSK, lw={lw/1e3:.0f}kHz, N_sym={n_blocks*Ns}/点, seed0={seed0}")
    print(f"  NDA intra='none' (brief §2 湍流设定)")
    print(f"{'湍流':>10} {'SNR_dB':>7} {'加权(none)':>12} {'等权(none)':>12} {'VV':>12}")
    rows = []
    for spec in turb_specs:
        turb_name = spec['name']
        gamma_db = spec['snr_db']
        gamma_lin = 10 ** (gamma_db / 10)
        ne_w = ne_eq = ne_vv = 0
        nb_w = nb_eq = nb_vv = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            ne, nb = ber_eval(rx_blind, bits,
                              lambda seg: nda_weighted_recovery(seg, M0, mode='none'),
                              mod, M0, intra_foe=True)
            ne_w += ne; nb_w += nb
            ne, nb = ber_eval(rx_blind, bits,
                              lambda seg: nda_equalweight_recovery(seg, M0, mode='none'),
                              mod, M0, intra_foe=True)
            ne_eq += ne; nb_eq += nb
            ne, nb = ber_eval(rx_blind, bits,
                              lambda seg: vv_cpr_generic(seg, M0, Nw=64)[0],
                              mod, M0, intra_foe=True)
            ne_vv += ne; nb_vv += nb
        b_w = ne_w / nb_w
        b_eq = ne_eq / nb_eq
        b_vv = ne_vv / nb_vv
        cat_vv, rel_vv = classify(b_w, b_vv)
        cat_eq, rel_eq = classify(b_w, b_eq)
        print(f"{turb_name:>10} {gamma_db:>7.0f} {b_w:>12.4e} {b_eq:>12.4e} {b_vv:>12.4e}")
        rows.append({
            'turbulence': turb_name,
            'snr_db': float(gamma_db),
            'alpha_beta': list(P.TURB_ALPHA_BETA[turb_name]),
            'linewidth_hz': float(lw),
            'ber_weighted': float(b_w),
            'ber_equalweight': float(b_eq),
            'ber_vv': float(b_vv),
            'weighted_vs_vv_rel': rel_vv,
            'weighted_vs_vv_cat': cat_vv,
            'weighted_vs_equalweight_rel': rel_eq,
            'weighted_vs_equalweight_cat': cat_eq,
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
    print("NDA-ML (加权/等权) vs VV 三方参数扫描体检")
    print(f"M0={P.M0}, T_S={P.T_S}, LASER_LW={P.LASER_LW/1e3:.0f}kHz, SIGMA2_P={P.SIGMA2_P:.3e}")
    print(f"N_BLOCKS={P.N_BLOCKS}, N_DFT={P.N_DFT}, BLOCK_SIZE_RESOLVE={P.BLOCK_SIZE_RESOLVE}")
    print(f"加权公式 (brief §3): unwrap 在升幂域, 最后 /M0 (K=8 segmented)")
    print(f"三方公平: 同信道同 seed 同 tx_bits; 只跑数字 + 机械分类, 不判断方向不建议")
    print("=" * 100)

    # --- 扫描1 线宽 (brief §2) ---
    linewidths_hz = [10e3, 50e3, 100e3, 200e3, 500e3]
    sweep1 = sweep_linewidth(linewidths_hz, snr_db=18.0)

    # --- 扫描2 调制阶数 (brief §2) ---
    mod_cases = [
        {'name': '8psk_M4', 'M0': 4, 'mod': 'apsk8', 'mod_fn': apsk8_mod,
         'bits_per_sym': 3},
        {'name': '8psk_M8', 'M0': 8, 'mod': 'apsk8', 'mod_fn': apsk8_mod,
         'bits_per_sym': 3},
        {'name': 'm16apsk_M8', 'M0': 8, 'mod': 'm16apsk', 'mod_fn': m16apsk_mod,
         'bits_per_sym': 4},
    ]
    sweep2 = sweep_modulation(mod_cases, snr_db=18.0, lw=10e3)

    # --- 扫描3 湍流 (brief §2) ---
    turb_specs = [
        {'name': 'weak', 'snr_db': 12.0},
        {'name': 'moderate', 'snr_db': 16.0},
        {'name': 'strong', 'snr_db': 20.0},
    ]
    sweep3 = sweep_turbulence(turb_specs, lw=10e3)

    # --- 汇总分类 (brief §5) ---
    summary = {
        'sweep1_weighted_vs_vv_cats': [r['weighted_vs_vv_cat'] for r in sweep1],
        'sweep2_weighted_vs_vv_cats': [r['weighted_vs_vv_cat'] for r in sweep2],
        'sweep3_weighted_vs_vv_cats': [r['weighted_vs_vv_cat'] for r in sweep3],
        'sweep1_weighted_vs_eq_cats': [r['weighted_vs_equalweight_cat'] for r in sweep1],
        'sweep2_weighted_vs_eq_cats': [r['weighted_vs_equalweight_cat'] for r in sweep2],
        'sweep3_weighted_vs_eq_cats': [r['weighted_vs_equalweight_cat'] for r in sweep3],
    }

    elapsed = time.time() - t0
    out = {
        'meta': {
            'task': 'NDA-ML (加权/等权) vs VV 三方参数扫描体检 (brief, 只跑数字+机械分类)',
            'weighting_formula': {
                'yn': '(rx/|rx|)^M0   (归一化升幂, brief §3)',
                'w': '|rx|^2          (ML 权重, brief §3)',
                'none': 'angle(sum(w*yn)) / M0   (整块加权 mean-angle)',
                'segmented': ('seg_phi[k]=angle(sum(w[lo:hi]*yn[lo:hi]))  [不/M0, 升幂域]; '
                              'unwrap(seg_phi); interp; phi_est=phi_raised/M0  [最后/M0]'),
                'unwrap_order': 'unwrap 在升幂域, 最后 /M0 (brief §3)',
            },
            'equalweight_formula': ('(w*yn).sum() -> (rx**M0)[lo:hi].mean(); '
                                    'unwrap 顺序与加权版一致 (brief §3)'),
            'vv_formula': '复制 VV.vv_cpr_m16apsk, M 可变; unwrap(angle)/M0 (brief §3)',
            'fairness': '三方同信道同 seed 同 tx_bits (AWGN 同 awgn_wiener_channel; '
                        '湍流同 generate_shared_realization_apsk + 同 rx_blind)',
            'classification': ('rel=(ber_weighted-ber_ref)/ber_ref; '
                               'rel<=-10% weighted_wins / |rel|<10% tie / rel>=+10% weighted_loses'),
            'intra_block_tracking': 'AWGN=segmented(K=8); 湍流=none (brief §2)',
            'mod_match': 'apsk8->apsk8_mod/demod/resolve_apsk8_blockwise; '
                         'm16apsk->m16apsk_mod/demod/resolve_m16apsk_blockwise',
            'sigma2p_linewidth': '派生 2*pi*lw*T_S (T_S=4e-10, 不读 params SIGMA2_P)',
            'vv_M_matches_NDA_M0': True,
            'M0_default': P.M0,
            'LASER_LW_Hz': float(P.LASER_LW),
            'T_S': float(P.T_S),
            'N_BLOCKS': P.N_BLOCKS,
            'N_DFT': P.N_DFT,
            'BLOCK_SIZE_RESOLVE': P.BLOCK_SIZE_RESOLVE,
            'SEED_AWGN': P.SEED_AWGN,
            'SEED_TURB0': P.SEED_TURB0,
            'HDFEC': P.HDFEC,
            'TURB_ALPHA_BETA': {k: list(v) for k, v in P.TURB_ALPHA_BETA.items()},
            'n_seeds': 1,
            'common_or_simulator_or_params_modified': False,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'sweep1_linewidth': sweep1,
        'sweep2_modulation': sweep2,
        'sweep3_turbulence': sweep3,
        'summary_classification': summary,
    }
    out_json = os.path.join(_HERE, '_vv_vs_nda_checkup.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 控制台汇总 (机械分类, 不判断) ---
    print("\n" + "=" * 100)
    print("机械分类汇总 (rel=(加权-参考)/参考; 拉开=加权赢 / 持平 / 反超=加权输):")
    print("--- 扫描1 线宽 (加权 vs VV):", summary['sweep1_weighted_vs_vv_cats'])
    print("--- 扫描1 线宽 (加权 vs 等权):", summary['sweep1_weighted_vs_eq_cats'])
    print("--- 扫描2 调制 (加权 vs VV):", summary['sweep2_weighted_vs_vv_cats'])
    print("--- 扫描2 调制 (加权 vs 等权):", summary['sweep2_weighted_vs_eq_cats'])
    print("--- 扫描3 湍流 (加权 vs VV):", summary['sweep3_weighted_vs_vv_cats'])
    print("--- 扫描3 湍流 (加权 vs 等权):", summary['sweep3_weighted_vs_eq_cats'])
    print(f"\n[耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
