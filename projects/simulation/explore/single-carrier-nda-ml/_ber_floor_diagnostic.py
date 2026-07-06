"""BER floor 根因诊断脚本 (单载波 NDA-ML 湍流场景).

任务 brief 要求诊断湍流下 NDA-ML BER floor (0.08-0.14) 太高的根因.

三个候选原因 (TL-22 物理前提先查):
  D1. assume_df_zero=True 在星地湍流场景误用: 信道注入 F_RESIDUAL=1MHz CFO
      (0.64 rad 线性相位斜坡 / 256-sym 块) + f_dot=150MHz/s Doppler, 但 NDA-ML
      assume_df_zero=True 只估常相位 CPE, 跳过 FOE → 残余 CFO 斜坡致 CPE 跟踪失败.
  D2. h_med MMSE 均衡残差: 用中位数 h (标量) 均衡所有块, deep fade 块 (h<<h_med)
      残差大. 即使 oracle (真相位) 也有 BER floor → 物理上限.
  D3. CLW=500kHz (仅 AWGN 场景 awgn_wiener_channel 用, 湍流信道用 LASER_LW=10kHz
      单端) → 湍流场景 CLW 不适用, D3 对湍流 BER floor 无影响 (排除).

诊断方法:
  对每 (turb, SNR), 对比:
    (a) oracle (真相位) + h_med 均衡       → 量化 D2 (h_med 残差, 物理上限)
    (b) oracle (真相位) + per-block 真h 均衡  → 真 h 上限 (D2 消除后)
    (c) NDA-ML assume_df_zero=True (现状)   → 量化 D1+C2 总残差
    (d) NDA-ML assume_df_zero=False (FFT-df) → 量化 D1 修复后
    (e) NDA-ML two-stage: fft_foe(M0=8) 粗估 FOE + nda_ml CPE → 修复方案 B
    (f) DA-ML (pilot FOE+CPE) + per-block pilot h → 公平参考

  关键比较:
    - (a) vs (b): h_med 残差贡献 (D2)
    - (c) vs (d)/(e): CFO 残差贡献 (D1)
    - (b) vs (d)+(per-block h): NDA-ML 离真 h oracle 多远

运行: cd projects/simulation && python explore/single-carrier-nda-ml/_ber_floor_diagnostic.py
时间预算: ≤ 300 s (诊断, 非全扫)
N≥100000 符号/点 (守 FR-21)
"""
import os
import sys
import time
import json

import numpy as np

_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common import (
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
    T_S, F_RESIDUAL, DOPPLER_HIGH, LASER_LW, BLOCK,
)
from common._modulation import _R1_16, _R2_16
from params import SimulationConfig


# =============================================================================
# 实验参数 (与 _time_domain_crlb.py 一致)
# =============================================================================
N_DFT = 256
M0 = 8
BITS_PER_SYM = 4
HDFEC = 3.8e-3
DA_PILOT_SPACING = 4
BLOCK_SIZE_RESOLVE = 256


# =============================================================================
# per-block 真实 h 均衡 (oracle 幅度, 诊断 D2 上限)
# =============================================================================
def equalize_perblock_trueh(rx_raw, h, gamma_bar):
    """用每块真实 h 做 MMSE 均衡 (oracle 幅度, 诊断 D2 消除后上限).
    h 是 per-symbol (BLOCK=100 内恒定), 直接 per-symbol MMSE."""
    return amp_limit(mmse_equalize(rx_raw, h, gamma_bar), 3.0)


# =============================================================================
# 盲 per-block h 估计 (NDA-ML, 无 pilot): 块内硬判决幅值平均
# =============================================================================
_CONST_POW_INNER = _R1_16 ** 2          # 内环功率 (B11 星座)
_CONST_POW_OUTER = _R2_16 ** 2          # 外环功率
_AVG_POW = (_CONST_POW_INNER * 8 + _CONST_POW_OUTER * 8) / 16  # =1.0 (归一化)


def estimate_h_blind_perblock(rx_raw, gamma_bar, block=BLOCK):
    """盲 per-block h 估计 (NDA-ML, 无 pilot).
    方法: 块内 |rx|² 平均 ≈ h·E[|s|²] + σ². E[|s|²]=1 (归一化), σ²=1/(2γ).
    → ĥ = mean(|rx|²) − 1/(2γ).  截断 ≥ 0.
    对齐信道 BLOCK (100 sym 内 h 恒定)."""
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        s = slice(i * block, min((i + 1) * block, N))
        seg = rx_raw[s]
        # |rx|² = h·|s|² + |noise|² + cross terms (均值). E[|s|²]=1.
        p_rx = float(np.mean(np.abs(seg) ** 2))
        h_blk = p_rx - 1.0 / (2.0 * gamma_bar)
        h_est[s] = max(h_blk, 1e-6)
    return h_est


# =============================================================================
# NDA-ML two-stage: fft_foe(M0 升幂) 粗估 FOE + nda_ml CPE (修复方案 B)
# =============================================================================
def fft_foe_m0(rx, M0_power, N_fft=None):
    """M0 升幂 FOE: rx^M0 去调制 → FFT 找频峰 → /M0 还原 CFO.
    与 nda_ml_recovery 内部 FFT-df 同逻辑, 但独立返回 df_est (rad/sample)."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    k = np.arange(N)
    if N_fft is None:
        N_fft = min(N, 4096)
    N_fft = min(N_fft, N)
    raised = rx ** M0_power
    seg = raised[:N_fft]
    win = np.hanning(N_fft)
    R = np.fft.fftshift(np.fft.fft(seg * win, n=N_fft * 8))
    freqs = np.fft.fftshift(np.fft.fftfreq(N_fft * 8, d=T_S))
    idx = np.argmax(np.abs(R))
    if 1 <= idx < len(R) - 1:
        a_v, b_v, g_v = np.abs(R[idx - 1]), np.abs(R[idx]), np.abs(R[idx + 1])
        if b_v + a_v - 2 * g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2 * b_v + g_v)
            df_raised = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            df_raised = freqs[idx]
    else:
        df_raised = freqs[idx]
    df_est_hz = df_raised / M0_power
    # 转换为 rad/sample (用于 exp(-j·omega·k) 补偿)
    omega_est = 2 * np.pi * df_est_hz * T_S
    return omega_est, df_est_hz


def ber_nda_twostage(seg, tb, omega_foe):
    """两阶段 NDA-ML: 先用 fft_foe 估的 omega 补偿 FOE, 再 nda_ml CPE (assume_df_zero=True).
    单块用全 8 个 M0 旋转 resolve (MVE 风格, 已知 tb)."""
    k = np.arange(len(seg))
    seg_foe = seg * np.exp(-1j * omega_foe * k)
    rc, _, _, _ = nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)
    # 单块 resolve M0=8 fold 模糊
    best_ber = 1.0
    for r in np.arange(0, 2 * np.pi, np.pi / 4):
        ber = np.mean(tb != m16apsk_demod(rc * np.exp(-1j * r)))
        if ber < best_ber:
            best_ber = ber
    return int(best_ber * len(tb)), len(tb)


def ber_nda_block(seg, tb, assume_df_zero):
    """单块 NDA-ML (逐块). 返回 (n_err, n_bits). 单块 resolve M0=8 fold 模糊."""
    if assume_df_zero:
        rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True)
    else:
        rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=False)
    best_ber = 1.0
    for r in np.arange(0, 2 * np.pi, np.pi / 4):
        ber = np.mean(tb != m16apsk_demod(rc * np.exp(-1j * r)))
        if ber < best_ber:
            best_ber = ber
    return int(best_ber * len(tb)), len(tb)


def ber_oracle(seg, tb, phi_seg):
    """Oracle: 真相位补偿 → 解调."""
    rc = seg * np.exp(-1j * phi_seg)
    return int(np.sum(tb != m16apsk_demod(rc))), len(tb)


def ber_da_block(seg, tb, tx_sym_seg, pilot_spacing=DA_PILOT_SPACING):
    """单块 DA-ML: pilot-aided FOE+CPE. BER 仅 data 位置."""
    pilot_idx = np.arange(0, len(seg), pilot_spacing)
    p_sym = tx_sym_seg[pilot_idx]
    rc, _, _ = da_ml_recovery(seg, pilot_idx=pilot_idx, pilot_sym=p_sym, mod='m16apsk')
    is_data = np.ones(len(seg), dtype=bool)
    is_data[pilot_idx] = False
    tb_arr = tb.reshape(len(seg), BITS_PER_SYM)
    dm_arr = m16apsk_demod(rc).reshape(len(seg), BITS_PER_SYM)
    n_err = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
    n_bits = int(np.sum(is_data) * BITS_PER_SYM)
    return n_err, n_bits


def estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_bar, pilot_spacing=DA_PILOT_SPACING, block=BLOCK):
    """per-block pilot h 估计 (DA-ML): pilot 位置 r(p)=s(p)√h, → ĥ=|r(p)/s(p)|² 块内平均.
    对齐信道 BLOCK (100 sym 内 h 恒定)."""
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    pilot_idx = np.arange(0, N, pilot_spacing)
    ratio_sq = np.abs(rx_raw[pilot_idx] / tx_sym[pilot_idx]) ** 2
    # 把 pilot 估的 h 映射回 per-symbol (块内恒定)
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        lo, hi = i * block, min((i + 1) * block, N)
        # 该块内的 pilot
        p_in_blk = (pilot_idx >= lo) & (pilot_idx < hi)
        if np.any(p_in_blk):
            h_blk = float(np.mean(ratio_sq[p_in_blk]))
        else:
            h_blk = 1.0  # fallback
        h_est[lo:hi] = max(h_blk, 1e-6)
    return h_est


# =============================================================================
# 主诊断
# =============================================================================
def main():
    t0 = time.time()
    cfg = SimulationConfig()

    # 诊断配置: 聚焦高 SNR (20 dB) 看 BER floor, 加 15dB 看趋势
    N_BLOCKS = 400  # 400×256 = 102400 ≥ 1e5 ✓
    DIAG_SNRS = [15.0, 20.0]
    TURB_LEVELS = ['weak', 'moderate', 'strong']
    SEED0 = 2000

    print("=" * 110)
    print("BER floor 根因诊断 (单载波 NDA-ML 湍流)")
    print(f"N_sym={N_BLOCKS * N_DFT}/点, M0={M0}, F_RESIDUAL={F_RESIDUAL/1e6:.1f}MHz, "
          f"f_dot={DOPPLER_HIGH/1e6:.0f}MHz/s, LASER_LW={LASER_LW/1e3:.0f}kHz (单端)")
    print(f"CFO 相位斜坡 / 256-sym 块 = 2π·{F_RESIDUAL/1e6:.1f}MHz·256·T_S = "
          f"{2*np.pi*F_RESIDUAL*256*T_S:.3f} rad")
    print("=" * 110)

    results = {'meta': {
        'N_per_point': N_BLOCKS * N_DFT,
        'M0': M0,
        'F_RESIDUAL_Hz': F_RESIDUAL,
        'DOPPLER_HIGH_Hz_s': DOPPLER_HIGH,
        'LASER_LW_Hz': LASER_LW,
        'cfo_phase_ramp_per_256blk_rad': float(2 * np.pi * F_RESIDUAL * 256 * T_S),
        'diagnoses': {
            'D1': 'assume_df_zero=True 跳过 FOE, 残余 CFO (1MHz) 斜坡 0.64rad/块 致 CPE 失败',
            'D2': 'h_med 标量均衡 deep fade 块残差 (oracle 也有 floor)',
            'D3': 'CLW=500kHz 仅 AWGN 场景, 湍流用 LASER_LW=10kHz → 对湍流 BER floor 无影响',
        },
    }, 'points': []}

    for turb in TURB_LEVELS:
        for gamma_db in DIAG_SNRS:
            gamma_lin = 10 ** (gamma_db / 10)
            # 累计各方案 BER
            schemes = {
                'oracle_hmed': [0, 0],       # (a) 真相位 + h_med
                'oracle_trueh': [0, 0],      # (b) 真相位 + per-block 真h
                'nda_df0': [0, 0],           # (c) NDA assume_df_zero=True (现状)
                'nda_fftdf': [0, 0],         # (d) NDA assume_df_zero=False (FFT-df)
                'nda_twostage': [0, 0],      # (e) two-stage fft_foe + nda CPE
                'da_hmed': [0, 0],           # (f) DA-ML + h_med
                # === 修复方案验证 (phase two-stage + per-block h) ===
                'fix_nda_twostage_blindh': [0, 0],   # (g) NDA two-stage + 盲per-block h (NDA盲, 公平)
                'fix_nda_twostage_trueh': [0, 0],    # (h) NDA two-stage + 真per-block h (oracle幅度上限)
                'fix_da_piloth': [0, 0],             # (i) DA-ML pilot FOE+CPE + pilot per-block h
            }
            foe_est_err = []  # FFT-df 估的 omega vs 真 CFO omega
            for b in range(N_BLOCKS):
                r = generate_shared_realization_apsk(
                    N_DFT, gamma_lin, turb, cfg.doppler.DOPPLER_HIGH,
                    mod='m16apsk', seed=SEED0 + b)
                rx_raw = r['rx_raw']
                bits = r['bits']
                phi = r['phi']
                tx_sym = r['tx']
                h = r['h']
                h_med = r['h_med']
                tb = bits[:N_DFT * BITS_PER_SYM]
                tx_sym_seg = tx_sym[:N_DFT]
                phi_seg = phi[:N_DFT]

                # (a) oracle + h_med
                rx_hmed = amp_limit(mmse_equalize(rx_raw, h_med, gamma_lin), 3.0)
                ne, nb = ber_oracle(rx_hmed, tb, phi_seg)
                schemes['oracle_hmed'][0] += ne; schemes['oracle_hmed'][1] += nb
                # (b) oracle + per-block true h
                rx_trueh = equalize_perblock_trueh(rx_raw, h, gamma_lin)
                ne, nb = ber_oracle(rx_trueh, tb, phi_seg)
                schemes['oracle_trueh'][0] += ne; schemes['oracle_trueh'][1] += nb
                # (c) NDA assume_df_zero=True (现状, 无 FOE)
                ne, nb = ber_nda_block(rx_hmed, tb, assume_df_zero=True)
                schemes['nda_df0'][0] += ne; schemes['nda_df0'][1] += nb
                # (d) NDA assume_df_zero=False (FFT-df 内部估 FOE)
                ne, nb = ber_nda_block(rx_hmed, tb, assume_df_zero=False)
                schemes['nda_fftdf'][0] += ne; schemes['nda_fftdf'][1] += nb
                # (e) two-stage: fft_foe(M0) + nda CPE
                omega_est, df_hz = fft_foe_m0(rx_hmed, M0)
                ne, nb = ber_nda_twostage(rx_hmed, tb, omega_est)
                schemes['nda_twostage'][0] += ne; schemes['nda_twostage'][1] += nb
                # (f) DA-ML + h_med
                ne, nb = ber_da_block(rx_hmed, tb, tx_sym_seg)
                schemes['da_hmed'][0] += ne; schemes['da_hmed'][1] += nb

                # === 修复方案验证 ===
                # (g) NDA two-stage + 盲 per-block h (NDA 盲, 公平, 无 pilot)
                h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
                rx_blindh = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
                omega_b, _ = fft_foe_m0(rx_blindh, M0)
                ne, nb = ber_nda_twostage(rx_blindh, tb, omega_b)
                schemes['fix_nda_twostage_blindh'][0] += ne
                schemes['fix_nda_twostage_blindh'][1] += nb
                # (h) NDA two-stage + 真per-block h (oracle 幅度上限)
                rx_trueh = equalize_perblock_trueh(rx_raw, h, gamma_lin)
                omega_t, _ = fft_foe_m0(rx_trueh, M0)
                ne, nb = ber_nda_twostage(rx_trueh, tb, omega_t)
                schemes['fix_nda_twostage_trueh'][0] += ne
                schemes['fix_nda_twostage_trueh'][1] += nb
                # (i) DA-ML + pilot per-block h
                h_pilot = estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
                rx_piloth = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
                ne, nb = ber_da_block(rx_piloth, tb, tx_sym_seg)
                schemes['fix_da_piloth'][0] += ne
                schemes['fix_da_piloth'][1] += nb
                # FOE 估计误差 (真 CFO omega = 2π·F_RESIDUAL·T_S)
                foe_est_err.append(df_hz)

            ber = {k: (v[0] / v[1] if v[1] > 0 else float('nan')) for k, v in schemes.items()}
            df_mean = float(np.mean(foe_est_err))
            df_std = float(np.std(foe_est_err))

            print(f"\n[{turb} @ {gamma_db:.0f}dB]  "
                  f"FOE 估 (FFT-df on h_med): {df_mean/1e6:.3f}±{df_std/1e6:.3f} MHz "
                  f"(真 CFO={F_RESIDUAL/1e6:.1f} MHz)")
            print(f"  {'方案':<28} {'BER':>12}   说明")
            print(f"  {'oracle_trueh':<28} {ber['oracle_trueh']:>12.4e}   (b) 真相位+per-block真h (D2 消除上限)")
            print(f"  {'oracle_hmed':<28} {ber['oracle_hmed']:>12.4e}   (a) 真相位+h_med (D2 残差)")
            print(f"  {'nda_df0':<28} {ber['nda_df0']:>12.4e}   (c) NDA df=0 现状 (D1+C2 总残差)")
            print(f"  {'nda_fftdf':<28} {ber['nda_fftdf']:>12.4e}   (d) NDA FFT-df (D1 内部修复)")
            print(f"  {'nda_twostage':<28} {ber['nda_twostage']:>12.4e}   (e) two-stage fft_foe+nda CPE")
            print(f"  {'da_hmed':<28} {ber['da_hmed']:>12.4e}   (f) DA-ML pilot FOE+CPE + h_med")
            print(f"  {'--- FIX (two-stage+perblk h) ---':<28}")
            print(f"  {'fix_nda_twostage_blindh':<28} {ber['fix_nda_twostage_blindh']:>12.4e}   (g) NDA two-stage+盲per-blk h [NDA盲公平]")
            print(f"  {'fix_nda_twostage_trueh':<28} {ber['fix_nda_twostage_trueh']:>12.4e}   (h) NDA two-stage+真per-blk h [上限]")
            print(f"  {'fix_da_piloth':<28} {ber['fix_da_piloth']:>12.4e}   (i) DA-ML + pilot per-blk h")
            hdfec_tag = '  *** HD-FEC (3.8e-3) REACHABLE' if any(
                ber[k] < HDFEC for k in
                ['oracle_trueh', 'oracle_hmed', 'fix_nda_twostage_blindh',
                 'fix_nda_twostage_trueh', 'fix_da_piloth']) else ''
            print(f"  {hdfec_tag}")

            results['points'].append({
                'turb': turb, 'snr_db': gamma_db,
                'ber': ber,
                'foe_est_mhz_mean': df_mean / 1e6,
                'foe_est_mhz_std': df_std / 1e6,
                'true_cfo_mhz': F_RESIDUAL / 1e6,
            })

    elapsed = time.time() - t0
    results['meta']['elapsed_sec'] = float(elapsed)

    # 诊断结论
    print("\n" + "=" * 110)
    print("诊断结论:")
    for p in results['points']:
        turb, snr = p['turb'], p['snr_db']
        b = p['ber']
        d2_resid = b['oracle_hmed'] / max(b['oracle_trueh'], 1e-9)
        d1_resid_df0 = b['nda_df0'] / max(b['oracle_hmed'], 1e-9)
        d1_fixed_fftdf = b['nda_fftdf'] / max(b['oracle_hmed'], 1e-9)
        d1_fixed_2stage = b['nda_twostage'] / max(b['oracle_hmed'], 1e-9)
        print(f"  [{turb}@{snr:.0f}dB] D2(h_med残差) oracle_hmed/oracle_trueh={d2_resid:.2f}x | "
              f"D1(CFO) nda_df0/oracle_hmed={d1_resid_df0:.2f}x "
              f"→ FFT-df={d1_fixed_fftdf:.2f}x, two-stage={d1_fixed_2stage:.2f}x")
    print(f"\n[耗时] {elapsed:.1f} s")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(out_dir, '_ber_floor_diagnostic.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[保存] {out_json}")


if __name__ == '__main__':
    main()
