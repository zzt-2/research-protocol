# -*- coding: utf-8 -*-
"""A1 参数适配扫描: pilot_spacing (DA-ML) + intra_block_tracking K (NDA-ML).

任务 (adaptation-scan.md A1): 扫描两个关键参数, 看最优值是否随 SNR/湍流强度变化.
若最优值随条件变 → 自适应参数策略有空间 (A1 信号成立).

### 任务 1: DA-ML pilot_spacing 扫描
  pilot_spacing = 2/4/8/16 (50%/25%/12.5%/6.25% overhead).
  公平对照用 γ_tot = γ_d + overhead_dB 坐标. overhead_db(sp) = 10·log10(sp/(sp-1)).
  物理 (TL-20): 低 SNR 密 pilot 好 (每 pilot 信噪比不够, 多 pilot 平均降噪);
                 高 SNR 稀 pilot 好 (pilot 够干净, 少 pilot 省 overhead).

### 任务 2: NDA-ML intra_block_tracking K 扫描
  模式: none (K=1, 块常数 CPE) / segmented K=4/8/16 (块内分段跟踪).
  物理: AWGN segmented(K8) 好 (sandbox 已证); strong 湍流 none 好 (deep fade 致 seg 跟踪噪声).
  低 SNR 小 K (多平均降噪); 高 SNR 大 K (可负担少符号/段, 要细跟踪).

### 纪律
  - 守 TL-13: 核心算法 (信道/调制/resolve/da_ml_recovery/mmse_equalize/amp_limit/fft_foe) 全从 common/ 导入.
  - 不改 common/ / simulator/ (option A 适配: 参数扫描在脚本内传参).
    * intra_block_tracking 在 common/ 里 K 硬编码=8, 无法传 K → 本地复制分段数学 (bit-exact) 支持 K 参数.
    * pilot_spacing 在 ber_da_awgn/estimate_h_pilot_perblock 已参数化, 直接传参.
  - seed 派生同主实验 (run_awgn/run_turb): awgn seed = seed_base + int(snr*1000);
    turb per-block seed = seed0 + b. 多 seed = seed_base + i.

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/_a1_param_scan.py
"""
import os
import sys
import time
import json

import numpy as np

# --- 路径: simulation 根 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守 TL-13: 不重写算法)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402  (复用 awgn_wiener_channel / fft_foe_m0_omega / h 估计)
from params import SimulationConfig  # noqa: E402

# 复用主实验信道 + FOE + h 估计 (逻辑等价 MVE, 同 seed 派生)
awgn_wiener_channel = S.awgn_wiener_channel
fft_foe_m0_omega = S.fft_foe_m0_omega
estimate_h_blind_perblock = S.estimate_h_blind_perblock


# =============================================================================
# 扫描配置 (adaptation-scan.md A1)
# =============================================================================
PILOT_SPACINGS = [2, 4, 8, 16]
TRACKING_MODES = ['none', 'K4', 'K8', 'K16']   # K4/8/16 = segmented 段数
# overhead_db(sp) = 10·log10(sp/(sp-1)); sp=2→3.01, sp=4→1.25, sp=8→0.58, sp=16→0.28
def overhead_db(sp):
    """sp=2→3.01dB, sp=4→1.25dB, sp=8→0.58dB, sp=16→0.28dB."""
    return 10.0 * np.log10(float(sp) / (float(sp) - 1))

SNR_AWGN = [8.0, 14.0, 18.0, 20.0]    # 代表性 SNR (低-中-高; 18≈HD-FEC)
SNR_TURB = [10.0, 15.0, 20.0, 24.0]
TURB_LEVELS = ['weak', 'moderate', 'strong']
N_BLOCKS_SCAN = 200                    # 200×256=51200/点 (BER~1e-3 区统计足够)
N_SEEDS = 5


# =============================================================================
# NDA CPE 分段跟踪 (本地复制 common.nda_ml_recovery assume_df_zero 分支, 支持 K 参数)
# 数学 bit-exact 复制自 common/_recovery.py:nda_ml_recovery (intra_block_tracking='segmented'),
# 唯一区别: K 从硬编码 8 改为参数. 守 TL-13: 不改 common/, 本地复制等价数学.
# =============================================================================
def nda_cpe_segmented_K(rx_seg, M0, K):
    """块内分段 mean-angle CPE 估计 (assume_df_zero=True 分支, 支持任意 K).

    K=None 或 1: 整块 mean-angle → 块常数 CPE (等价 common 'none').
    K>=2: 切 K 段每段独立升幂 mean-angle, 段间 unwrap + 线性插值 → 逐符号相位轨迹.
    返回 rx_comp = rx * exp(-j·phi_est).
    """
    rx_seg = np.asarray(rx_seg, dtype=complex)
    N = len(rx_seg)
    raised = rx_seg ** M0
    if K is None or K <= 1:
        phi_raised = np.angle(raised.mean())          # 整块常相位
        phi_est = phi_raised / M0
    else:
        K = int(min(K, N))
        seg_len = N // K
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
    return rx_seg * np.exp(-1j * phi_est)


def _K_from_mode(mode):
    """'none'→None, 'K4'→4, 'K8'→8, 'K16'→16."""
    if mode == 'none':
        return None
    return int(mode[1:])


# =============================================================================
# BER 评估 — NDA (参数化 tracking K) + DA (参数化 pilot_spacing)
# =============================================================================
def ber_nda_awgn_K(rx, tx_bits, K):
    """NDA-ML AWGN: 逐块升幂 mean-angle CPE, tracking 模式由 K 控制.
    K=None 整块常相位; K>=2 分段. BER 含全块符号 (NDA 无 pilot)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_cpe_segmented_K(seg, P.M0, K)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_nda_turb_K(rx, tx_bits, K):
    """NDA-ML 湍流: 两阶段 (fft_foe + nda CPE), tracking 模式由 K 控制.
    (rx 已 per-block blind h 均衡). 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_cpe_segmented_K(seg_foe, P.M0, K)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def estimate_h_pilot_perblock_sp(rx_raw, tx_sym, gamma_bar, pilot_spacing):
    """per-block pilot h 估计, pilot_spacing 参数化 (复制自 S.estimate_h_pilot_perblock)."""
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    pilot_idx = np.arange(0, N, pilot_spacing)
    ratio_sq = np.abs(rx_raw[pilot_idx] / tx_sym[pilot_idx]) ** 2
    nb = (N + P.CH_BLOCK - 1) // P.CH_BLOCK
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        lo, hi = i * P.CH_BLOCK, min((i + 1) * P.CH_BLOCK, N)
        p_in_blk = (pilot_idx >= lo) & (pilot_idx < hi)
        h_blk = float(np.mean(ratio_sq[p_in_blk])) if np.any(p_in_blk) else 1.0
        h_est[lo:hi] = max(h_blk, 1e-6)
    return h_est


def ber_da_awgn_sp(rx, tx_bits, pilot_spacing):
    """DA-ML AWGN, pilot_spacing 参数化. BER 仅 data 符号 (pilot 不算信息 BER).
    复制自 S.ber_da_awgn, 改 pilot_spacing 参数."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    tx_sym = m16apsk_mod(tx_bits[:L * P.BITS_PER_SYM])
    pilot_idx_local = np.arange(0, P.N_DFT, pilot_spacing)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    rx_comp_full = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        s_blk = slice(b * P.N_DFT, (b + 1) * P.N_DFT)
        p_sym = tx_sym[b * P.N_DFT + pilot_idx_local]
        rc, _, _ = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                                  pilot_sym=p_sym, mod='m16apsk')
        rx_comp_full[s_blk] = rc
    demod_bits = m16apsk_demod(rx_comp_full)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    n_sym = L
    is_data_sym = np.zeros(n_sym, dtype=bool)
    for b in range(n_blk):
        base = b * P.N_DFT
        is_data_sym[base:base + P.N_DFT] = is_data
    tb_arr = tb.reshape(n_sym, P.BITS_PER_SYM)
    dm_arr = demod_bits.reshape(n_sym, P.BITS_PER_SYM)
    n_err_data = int(np.sum(tb_arr[is_data_sym] != dm_arr[is_data_sym]))
    n_bits_data = int(np.sum(is_data_sym) * P.BITS_PER_SYM)
    return n_err_data, n_bits_data


def ber_da_turb_sp(rx, tx_bits, pilot_spacing):
    """DA-ML 湍流, pilot_spacing 参数化. BER 仅 data 位置. (rx 已 per-block pilot h 均衡)
    DA ML 内含 FOE+CPE (pilot 线性回归), 无需额外 fft_foe. 等价 S.ber_da_turb 但参数化."""
    return ber_da_awgn_sp(rx, tx_bits, pilot_spacing)


# =============================================================================
# 扫描: AWGN
# =============================================================================
def scan_awgn(n_blocks, snr_points, seed_base):
    """AWGN: DA(pilot_spacing) + NDA(tracking K) × SNR. 返回 per-config per-snr BER.

    信道复用 awgn_wiener_channel (同主实验 seed 派生). 每个 SNR 只生成一次 rx, 多 config 共享.
    """
    N_sym = n_blocks * P.N_DFT
    # DA: {sp: {snr: ber}}, NDA: {mode: {snr: ber}}
    da_res = {sp: {} for sp in PILOT_SPACINGS}
    nda_res = {m: {} for m in TRACKING_MODES}
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, _ = awgn_wiener_channel(tx, snr, seed, sigma2_p=None)
        # DA pilot_spacing 扫描
        for sp in PILOT_SPACINGS:
            ne, nb = ber_da_awgn_sp(rx, bits, sp)
            da_res[sp][float(snr)] = ne / nb
        # NDA tracking 扫描
        for m in TRACKING_MODES:
            K = _K_from_mode(m)
            ne, nb = ber_nda_awgn_K(rx, bits, K)
            nda_res[m][float(snr)] = ne / nb
    return {'DA': da_res, 'NDA': nda_res}


# =============================================================================
# 扫描: 湍流
# =============================================================================
def scan_turb(turb_name, gamma_points, n_blocks, cfg, seed0, lw=None):
    """湍流: DA(pilot_spacing) + NDA(tracking K) × γ. 返回 per-config per-γ BER.

    共享信道 generate_shared_realization_apsk (守 TL-13). DA 用 pilot-spacing 对应 h 估计;
    NDA 用 blind h 估计 (与 K 无关, 每 γ 生成一次复用)."""
    Ns = P.N_DFT
    da_res = {sp: {float(g): 0.0 for g in gamma_points} for sp in PILOT_SPACINGS}
    nda_res = {m: {float(g): 0.0 for g in gamma_points} for m in TRACKING_MODES}
    # 累计错误 (多 block)
    da_ne = {sp: {float(g): 0 for g in gamma_points} for sp in PILOT_SPACINGS}
    da_nb = {sp: {float(g): 0 for g in gamma_points} for sp in PILOT_SPACINGS}
    nda_ne = {m: {float(g): 0 for g in gamma_points} for m in TRACKING_MODES}
    nda_nb = {m: {float(g): 0 for g in gamma_points} for m in TRACKING_MODES}
    for gamma_db in gamma_points:
        gamma_lin = 10 ** (gamma_db / 10)
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            tx_sym = r['tx']
            # NDA: blind per-block h (与 K 无关, 一次)
            h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            for m in TRACKING_MODES:
                K = _K_from_mode(m)
                ne, nb = ber_nda_turb_K(rx_blind, bits, K)
                nda_ne[m][float(gamma_db)] += ne
                nda_nb[m][float(gamma_db)] += nb
            # DA: 每个 pilot_spacing 独立 h 估计 (pilot 数随 sp 变)
            for sp in PILOT_SPACINGS:
                h_pilot = estimate_h_pilot_perblock_sp(rx_raw, tx_sym, gamma_lin, sp)
                rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
                ne, nb = ber_da_turb_sp(rx_pilot, bits, sp)
                da_ne[sp][float(gamma_db)] += ne
                da_nb[sp][float(gamma_db)] += nb
    for sp in PILOT_SPACINGS:
        for g in gamma_points:
            da_res[sp][float(g)] = da_ne[sp][float(g)] / max(da_nb[sp][float(g)], 1)
    for m in TRACKING_MODES:
        for g in gamma_points:
            nda_res[m][float(g)] = nda_ne[m][float(g)] / max(nda_nb[m][float(g)], 1)
    return {'DA': da_res, 'NDA': nda_res}


# =============================================================================
# 聚合 (多 seed mean)
# =============================================================================
def aggregate(per_seed, kind):
    """per_seed: list of {scene: {'DA':..., 'NDA':...}}. 返回 mean BER per config per snr per scene."""
    scenes = list(per_seed[0].keys())
    out = {sc: {'DA': {}, 'NDA': {}} for sc in scenes}
    for sc in scenes:
        # keys: spacings or modes
        da_sps = list(per_seed[0][sc]['DA'].keys())
        nda_modes = list(per_seed[0][sc]['NDA'].keys())
        for sp in da_sps:
            snrs = list(per_seed[0][sc]['DA'][sp].keys())
            out[sc]['DA'][sp] = {}
            for s in snrs:
                vals = [ps[sc]['DA'][sp][s] for ps in per_seed]
                out[sc]['DA'][sp][s] = float(np.mean(vals))
        for m in nda_modes:
            snrs = list(per_seed[0][sc]['NDA'][m].keys())
            out[sc]['NDA'][m] = {}
            for s in snrs:
                vals = [ps[sc]['NDA'][m][s] for ps in per_seed]
                out[sc]['NDA'][m][s] = float(np.mean(vals))
    return out


# =============================================================================
# 最优值分析 (A1 信号判定)
# =============================================================================
def find_optimal_ber(ber_dict, snrs):
    """ber_dict: {config: {snr: ber}}. 返回 {snr: (best_config, best_ber, all_bers)}."""
    res = {}
    for s in snrs:
        best_c, best_b = None, np.inf
        allb = {}
        for c, d in ber_dict.items():
            b = d[s]
            allb[c] = b
            if b < best_b:
                best_b, best_c = b, c
        res[s] = {'best': best_c, 'best_ber': best_b, 'all': allb}
    return res


def snr_to_gamma_tot_for_da(scene, gamma_or_snr):
    """对 DA: γ_tot = γ_d + overhead. 这里返回 overhead 映射用于公平分析 (在报告里做)."""
    return None


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    cfg = SimulationConfig()
    print("=" * 100)
    print(f"A1 参数适配扫描: DA pilot_spacing {PILOT_SPACINGS} + NDA tracking {TRACKING_MODES}")
    print(f"{N_SEEDS} seed × 4 场景 (awgn/weak/moderate/strong) × 代表性 SNR")
    print(f"N_blocks/点={N_BLOCKS_SCAN} ({N_BLOCKS_SCAN*P.N_DFT} sym), M0={P.M0}, "
          f"LW={P.LASER_LW/1e3:.0f}kHz")
    print(f"AWGN SNR={SNR_AWGN}, TURB γ={SNR_TURB}")
    print("=" * 100)

    per_seed = []
    for i in range(N_SEEDS):
        ts = time.time()
        seed_awgn = P.SEED_AWGN + i * 100000    # seed 偏移 (避免 seed 派生冲突)
        seed_turb = P.SEED_TURB0 + i * 100000
        scene_res = {}
        print(f"\n###### seed {i} (awgn_base={seed_awgn}, turb_base={seed_turb}) ######")
        # AWGN
        awgn = scan_awgn(N_BLOCKS_SCAN, SNR_AWGN, seed_awgn)
        scene_res['awgn'] = awgn
        # 湍流
        for turb in TURB_LEVELS:
            tr = scan_turb(turb, SNR_TURB, N_BLOCKS_SCAN, cfg, seed_turb, lw=None)
            scene_res[turb] = tr
        per_seed.append(scene_res)
        print(f"  seed {i} done: {time.time()-ts:.1f}s")

    # 聚合
    mean_ber = aggregate(per_seed, None)

    # 最优值分析
    print("\n" + "#" * 40 + " 最优值分析 " + "#" * 40)
    opt_da = {}
    opt_nda = {}
    for sc in mean_ber:
        snrs_da = sorted(mean_ber[sc]['DA'][PILOT_SPACINGS[0]].keys())
        snrs_nda = sorted(mean_ber[sc]['NDA'][TRACKING_MODES[0]].keys())
        opt_da[sc] = find_optimal_ber(mean_ber[sc]['DA'], snrs_da)
        opt_nda[sc] = find_optimal_ber(mean_ber[sc]['NDA'], snrs_nda)
        # 打印
        print(f"\n--- {sc} ---")
        print(f"  DA pilot_spacing 最优 (BER@γ_d, 注意: γ_tot 需 +overhead):")
        for s in snrs_da:
            o = opt_da[sc][s]
            alls = "  ".join(f"sp{c}={o['all'][c]:.3e}" for c in sorted(o['all'].keys()))
            print(f"    γ={s:>5.0f}dB → 最优 sp={o['best']} ({o['best_ber']:.3e})  | {alls}")
        print(f"  NDA tracking 最优:")
        for s in snrs_nda:
            o = opt_nda[sc][s]
            alls = "  ".join(f"{c}={o['all'][c]:.3e}" for c in TRACKING_MODES)
            print(f"    γ={s:>5.0f}dB → 最优 {o['best']} ({o['best_ber']:.3e})  | {alls}")

    # A1 信号判定
    print("\n" + "#" * 40 + " A1 信号判定 " + "#" * 40)
    # DA: 最优 sp 在各场景各 SNR 是否变? 公平用 γ_tot 坐标分析
    # 先看 γ_d 坐标趋势, 再 γ_tot 校正
    da_signal = {}
    nda_signal = {}
    for sc in mean_ber:
        snrs_da = sorted(opt_da[sc].keys())
        snrs_nda = sorted(opt_nda[sc].keys())
        da_best_sps = [opt_da[sc][s]['best'] for s in snrs_da]
        nda_best_modes = [opt_nda[sc][s]['best'] for s in snrs_nda]
        da_signal[sc] = {'snrs': snrs_da, 'best_sp': da_best_sps,
                         'varies': len(set(da_best_sps)) > 1}
        nda_signal[sc] = {'snrs': snrs_nda, 'best_mode': nda_best_modes,
                          'varies': len(set(nda_best_modes)) > 1}
        print(f"  {sc}: DA 最优 sp 随 SNR = {da_best_sps} (变={da_signal[sc]['varies']})")
        print(f"  {sc}: NDA 最优 mode 随 SNR = {nda_best_modes} (变={nda_signal[sc]['varies']})")

    # 落盘
    out = {
        'meta': {
            'task': 'A1 参数适配扫描 (adaptation-scan A1)',
            'description': ('扫描 DA pilot_spacing [2,4,8,16] + NDA intra_block_tracking '
                            '[none,K4,K8,K16], 看最优值是否随 SNR/湍流变 (A1 信号判定)'),
            'pilot_spacings': PILOT_SPACINGS,
            'tracking_modes': TRACKING_MODES,
            'overhead_db_per_sp': {str(sp): float(overhead_db(sp)) for sp in PILOT_SPACINGS},
            'n_seeds': N_SEEDS,
            'seed_awgn_base': P.SEED_AWGN,
            'seed_turb0_base': P.SEED_TURB0,
            'n_blocks': N_BLOCKS_SCAN,
            'n_sym_per_point': N_BLOCKS_SCAN * P.N_DFT,
            'snr_awgn': SNR_AWGN,
            'snr_turb': SNR_TURB,
            'turb_levels': TURB_LEVELS,
            'M0': P.M0,
            'laser_lw_hz': float(P.LASER_LW),
            'sigma2_p': float(P.SIGMA2_P),
            'hdfec': P.HDFEC,
            'algorithm_source': ('common/ (信道/调制/resolve/da_ml/mmse_equalize/amp_limit/fft_foe); '
                                 'nda_cpe_segmented_K 本地复制 common segmented 数学 (支持 K 参数); '
                                 'ber_da_*_sp 参数化 pilot_spacing'),
            'common_modified': False,
            'note_fair_compare': ('DA 公平对照用 γ_tot=γ_d+overhead_db(sp). '
                                  'sp=2→3.01dB, sp=4→1.25dB, sp=8→0.58dB, sp=16→0.28dB. '
                                  '报告里做 γ_tot 坐标校正后再判最优.'),
            'elapsed_sec': float(time.time() - t0),
            'python': sys.executable,
            'numpy_version': np.__version__,
        },
        'mean_ber': mean_ber,           # {scene: {'DA':{sp:{snr:ber}}, 'NDA':{mode:{snr:ber}}}}
        'optimal': {                    # {scene: {'DA':{snr:{best,best_ber,all}}, 'NDA':...}}
            'DA': opt_da, 'NDA': opt_nda,
        },
        'a1_signal': {
            'DA_pilot_spacing': {sc: {'snrs': v['snrs'], 'best_sp': v['best_sp'],
                                      'varies': v['varies']}
                                 for sc, v in da_signal.items()},
            'NDA_tracking': {sc: {'snrs': v['snrs'], 'best_mode': v['best_mode'],
                                  'varies': v['varies']}
                             for sc, v in nda_signal.items()},
        },
        'raw_per_seed': per_seed,
    }
    out_json = os.path.join(_HERE, '_a1_param_scan_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(_to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {time.time()-t0:.1f}s")


def _to_jsonable(o):
    if isinstance(o, dict):
        return {k: _to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return _to_jsonable(o.tolist())
    return o


if __name__ == '__main__':
    main()
