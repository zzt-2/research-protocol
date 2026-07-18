# -*- coding: utf-8 -*-
"""NDA-ML 加权版 (修 D-008 双 bug) vs 等权版 vs VV — 三方对照 sandbox.

任务 (HANDOFF brief): 验证 "补对 ML 加权 (|R(k)|²) + 归一化升幂" 后, 加权版能否在
strong 湍流场景 vs VV 拉开差距 (AWGN 低线宽样本 SNR 均匀, 预期拉不开).

修的两个 bug (D-008, 数学已验证):
  Bug 1 (漏 ML 加权): B11 Eq.16 是加权 mean-angle (权重 |R(k)|²), 现 nda_ml_recovery raised.mean() 等权.
  Bug 2 (升幂未归一化): B11 Eq.5 是 (R/|R|)^M0, 现 rx**M0.

加权版公式逐字按 brief §2 (none + segmented 两种). 严格只改本 explore/ 目录,
不改 common/ / simulator/ (守纪律 1).

三方公平 (守纪律 3): 同 seed / 同 tx_bits / 同 awgn_wiener_channel / 同 generate_shared_realization_apsk
/ 同 rx_blind (湍流). 单 seed 快跑.

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/ml_weighting_check.py
  可选 --no-plot
"""
import os
import sys
import json
import time
import argparse

import numpy as np

# --- 路径: simulation 根 (与 sc_nda_ml_sim.py / run_vv_ablation.py 同构) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守 TL-13 + 纪律 1, 2: 复用, 不重写信道/调制/VV/resolve)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402  (参数全溯源, 纪律 3)
import sc_nda_ml_sim as S  # noqa: E402  (复用 awgn_wiener_channel / ber_nda_* / estimate_h_*_perblock / fft_foe_m0_omega)
import run_vv_ablation as VV  # noqa: E402  (复用 ber_vv_awgn / ber_vv_turb_eval)
from params import SimulationConfig  # noqa: E402


# =============================================================================
# NDA-ML 加权版恢复 (修 D-008 双 bug). 公式逐字按 brief §2.
# =============================================================================
def nda_weighted_recovery(seg, M0, mode='segmented'):
    """加权 NDA-ML 块内 CPE 恢复 (修 D-008 Bug1 漏加权 + Bug2 升幂未归一化).

    公式逐字 brief §2:
      mag = |rx| (保护下界 1e-12)
      yn  = (rx/mag)**M0          # 归一化升幂 (B11 Eq.5, 去幅度, 修 Bug2)
      w   = mag**2                # ML 权重 w_k = |R(k)|² (B11 Eq.16, 修 Bug1)
      phi_est = angle((w*yn).sum()) / M0   # 加权 mean-angle (B11 Eq.16)

    mode='none': 整块加权 mean-angle → 块常数 CPE.
    mode='segmented': 块内 K=8 段, 段内加权 mean-angle (循环里先 /M0), 段间 unwrap+interp
                      得逐符号相位 (对齐主实验 nda_ml_recovery segmented 分支逻辑).

    返回 rx_comp = seg * exp(-1j * phi_est).
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    # --- 预计算 mag / yn / w (整块) ---
    mag = np.abs(seg)
    mag[mag < 1e-12] = 1e-12
    yn = (seg / mag) ** M0          # 归一化升幂 (修 Bug2, B11 Eq.5)
    w = mag ** 2                    # ML 权重 (修 Bug1, B11 Eq.16)

    if mode == 'segmented':
        K = 8                       # 溯源: 与主实验 nda_ml_recovery segmented 一致
        seg_len = N // K
        seg_phi = np.empty(K)
        seg_center = np.empty(K)
        for k in range(K):
            lo, hi = k * seg_len, (k + 1) * seg_len
            # 段内加权 mean-angle, 循环里先 /M0 (还原后相位域, 对齐 brief §2)
            seg_phi[k] = np.angle((w[lo:hi] * yn[lo:hi]).sum()) / M0
            seg_center[k] = (lo + hi) / 2.0
        seg_phi_unw = np.unwrap(seg_phi)              # 在还原后相位上 unwrap
        t = np.arange(N)
        phi_est = np.interp(t, seg_center, seg_phi_unw)
    else:  # 'none'
        phi_est = np.angle((w * yn).sum()) / M0       # 整块加权 mean-angle
    rx_comp = seg * np.exp(-1j * phi_est)
    return rx_comp


# =============================================================================
# 加权版 BER 评估 (AWGN + 湍流). 结构对齐 sc_nda_ml_sim 的等权版 (保公平).
# =============================================================================
def ber_nda_weighted_awgn(rx, tx_bits, mode='segmented'):
    """加权 NDA-ML AWGN: 逐块加权 CPE + resolve M0-fold 模糊. 返回 (n_err, n_bits).

    结构逐字对齐 S.ber_nda_awgn (逐 N_DFT 块, resolve_m16apsk_blockwise).
    AWGN 等权版用 segmented, 故默认 mode='segmented' 与之对齐.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_weighted_recovery(seg, P.M0, mode=mode)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_nda_weighted_turb_eval(rx, tx_bits, mode='none'):
    """加权 NDA-ML 湍流: 逐块 fft_foe (两阶段第一步) + 加权 CPE + resolve. 返回 (n_err, n_bits).

    结构逐字对齐 S.ber_nda_turb_eval / ber_nda_turb: 每 N_DFT 块先 fft_foe_m0_omega 补 CFO,
    再 CPE. 湍流等权版用 'none', 故默认 mode='none' 与之对齐.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_weighted_recovery(seg_foe, P.M0, mode=mode)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 三方对照 sweep (单 seed). 三方共用同一 rx (公平前提).
# =============================================================================
def run_awgn_three_way(n_blocks, snr_points, seed_base):
    """AWGN 三方对照 (等权 segmented / 加权 segmented / 加权 none / VV), 单 seed.

    三方共用同一 rx (同 awgn_wiener_channel 调用). seed 派生对齐 S.run_awgn.
    返回 list[dict], 每 SNR 点含三/四方法 BER + 加权 vs VV 差值.
    """
    N_sym = n_blocks * P.N_DFT
    print(f"\n[AWGN 三方] N_sym={N_sym}/点, M0={P.M0}, seed_base={seed_base}")
    print(f"{'SNR_dB':>7} {'NDA_eq(seg)':>13} {'NDA_w(seg)':>13} {'NDA_w(none)':>13} {'VV':>13}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        # 同一 rx 给三方 (公平前提)
        rx, _phi_true = S.awgn_wiener_channel(tx, snr, seed)
        ne_eq, nb_eq = S.ber_nda_awgn(rx, bits)                       # 等权 segmented (现状)
        ne_wseg, nb_wseg = ber_nda_weighted_awgn(rx, bits, mode='segmented')  # 加权 segmented (主)
        ne_wnone, nb_wnone = ber_nda_weighted_awgn(rx, bits, mode='none')     # 加权 none (参考)
        ne_vv, nb_vv = VV.ber_vv_awgn(rx, bits)
        b_eq = ne_eq / nb_eq
        b_wseg = ne_wseg / nb_wseg
        b_wnone = ne_wnone / nb_wnone
        b_vv = ne_vv / nb_vv
        print(f"{snr:>7.0f} {b_eq:>13.4e} {b_wseg:>13.4e} {b_wnone:>13.4e} {b_vv:>13.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'ber_eq_segmented': b_eq,
            'ber_weighted_segmented': b_wseg,
            'ber_weighted_none': b_wnone,
            'ber_vv': b_vv,
            'weighted_seg_vs_vv_rel': float((b_wseg - b_vv) / b_vv) if b_vv > 0 else None,
        })
    return per_snr


def run_turb_three_way(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0):
    """湍流三方对照 (等权 none / 加权 none / 加权 segmented / VV), 单 seed.

    三方共用同一 rx_blind (同 generate_shared_realization_apsk + 同 estimate_h_blind_perblock
    + 同 mmse_equalize + 同 amp_limit). seed 派生对齐 S.run_turb.
    返回 list[dict].
    """
    Ns = P.N_DFT
    print(f"\n[{turb_name} 三方] N_sym={n_blocks*Ns}/点, seed0={seed0}")
    print(f"{'γd_dB':>7} {'NDA_eq(none)':>14} {'NDA_w(none)':>14} {'NDA_w(seg)':>14} {'VV':>14}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_eq = ne_wnone = ne_wseg = ne_vv = 0
        nb_eq = nb_wnone = nb_wseg = nb_vv = 0
        for b in range(n_blocks):
            # 同一信道实现给三方 (公平前提)
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            ne, nb = S.ber_nda_turb_eval(rx_blind, bits)              # 等权 none (现状)
            ne_eq += ne; nb_eq += nb
            ne, nb = ber_nda_weighted_turb_eval(rx_blind, bits, mode='none')     # 加权 none (主)
            ne_wnone += ne; nb_wnone += nb
            ne, nb = ber_nda_weighted_turb_eval(rx_blind, bits, mode='segmented')  # 加权 seg (参考)
            ne_wseg += ne; nb_wseg += nb
            ne, nb = VV.ber_vv_turb_eval(rx_blind, bits)
            ne_vv += ne; nb_vv += nb
        b_eq = ne_eq / nb_eq
        b_wnone = ne_wnone / nb_wnone
        b_wseg = ne_wseg / nb_wseg
        b_vv = ne_vv / nb_vv
        print(f"{gamma_db:>7.0f} {b_eq:>14.4e} {b_wnone:>14.4e} {b_wseg:>14.4e} {b_vv:>14.4e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'ber_eq_none': b_eq,
            'ber_weighted_none': b_wnone,
            'ber_weighted_segmented': b_wseg,
            'ber_vv': b_vv,
            'weighted_none_vs_vv_rel': float((b_wnone - b_vv) / b_vv) if b_vv > 0 else None,
        })
    return per_snr


# =============================================================================
# 判定 (brief §5): 加权 vs VV 在 strong 湍流是否拉开差距 + 加权是否反比等权差
# =============================================================================
def verdict(strong_pts):
    """对 strong 湍流点做判定 (brief §5)."""
    max_better = 0.0   # 加权 vs VV 最大相对改善 (负 = 加权 BER 低 = 加权赢)
    max_worse_vs_eq = 0.0   # 加权 vs 等权 最大相对恶化 (正 = 加权 BER 高 = 加权差)
    for p in strong_pts:
        b_w = p['ber_weighted_none']
        b_vv = p['ber_vv']
        b_eq = p['ber_eq_none']
        rel_wvv = (b_w - b_vv) / b_vv if b_vv > 0 else 0.0
        rel_weq = (b_w - b_eq) / b_eq if b_eq > 0 else 0.0
        max_better = min(max_better, rel_wvv)   # 最负值
        max_worse_vs_eq = max(max_worse_vs_eq, rel_weq)
    # 加权 vs VV: BER 差 ≥10% 且加权赢 (rel ≤ -0.10) → 拉开差距
    weighted_beats_vv = any((p['ber_weighted_none'] - p['ber_vv']) / p['ber_vv'] <= -0.10
                            for p in strong_pts if p['ber_vv'] > 0)
    # 加权 vs VV: 全程差 <5% → 持平
    all_close = all(abs((p['ber_weighted_none'] - p['ber_vv']) / p['ber_vv']) < 0.05
                    for p in strong_pts if p['ber_vv'] > 0)
    # 加权反比等权差 (中位恶化 > 5%) → 实现可能错
    worse_vs_eq = max_worse_vs_eq > 0.05
    if all_close:
        cat = 'tie'   # 持平, 低线宽掩盖
    elif weighted_beats_vv:
        cat = 'gap'   # 加权拉开差距, 有效
    else:
        cat = 'mixed'
    return {
        'category': cat,
        'weighted_beats_vv_10pct': bool(weighted_beats_vv),
        'all_within_5pct_of_vv': bool(all_close),
        'weighted_worse_than_equalweight_5pct': bool(worse_vs_eq),
        'max_rel_improvement_vs_vv': float(max_better),
        'max_rel_worse_vs_equalweight': float(max_worse_vs_eq),
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-plot', action='store_true')
    args = ap.parse_args()

    t0 = time.time()
    cfg = SimulationConfig()
    print("=" * 100)
    print("NDA-ML 加权版 (修 D-008 双 bug) vs 等权版 vs VV — 三方对照 sandbox")
    print(f"M0={P.M0}, LASER_LW={P.LASER_LW/1e3:.0f}kHz, SIGMA2_P={P.SIGMA2_P:.3e}, "
          f"single seed, N_BLOCKS={P.N_BLOCKS}")
    print(f"加权公式: yn=(rx/|rx|)^M0, w=|rx|², phi=angle(sum(w*yn))/M0 (brief §2, D-008)")
    print("=" * 100)

    # --- AWGN 三方对照 (单 seed = P.SEED_AWGN) ---
    awgn_pts = run_awgn_three_way(P.N_BLOCKS, P.SNR_AWGN_DB, P.SEED_AWGN)

    # --- strong 湍流三方对照 (单 seed = P.SEED_TURB0) ---
    strong_pts = run_turb_three_way('strong', P.SNR_TURB_DB, P.N_BLOCKS, cfg, P.SEED_TURB0)

    # --- 判定 ---
    v = verdict(strong_pts)
    print("\n" + "=" * 100)
    print("判定 (brief §5, 基于 strong 湍流, 加权 none vs VV):")
    print(f"  category                        = {v['category']}  (gap=拉开差距 / tie=持平 / mixed)")
    print(f"  weighted vs VV: 任一点 BER 改善≥10%   = {v['weighted_beats_vv_10pct']}")
    print(f"  weighted vs VV: 全程差<5% (持平)      = {v['all_within_5pct_of_vv']}")
    print(f"  weighted 反比等权版差 >5% (实现可疑)  = {v['weighted_worse_than_equalweight_5pct']}")
    print(f"  max rel improvement vs VV (越负越好)  = {v['max_rel_improvement_vs_vv']*100:+.1f}%")
    print(f"  max rel worse vs equalweight (越正越差)= {v['max_rel_worse_vs_equalweight']*100:+.1f}%")

    # --- 画图 (可选) ---
    png_path = None
    if not args.no_plot:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
            # AWGN
            ax = axes[0]
            gts = [p['snr_db'] for p in awgn_pts]
            ax.semilogy(gts, [p['ber_eq_segmented'] for p in awgn_pts], 'o-', label='NDA 等权 segmented (现状/bug)')
            ax.semilogy(gts, [p['ber_weighted_segmented'] for p in awgn_pts], 's-', label='NDA 加权 segmented (修 D-008, 主)')
            ax.semilogy(gts, [p['ber_weighted_none'] for p in awgn_pts], 'x--', label='NDA 加权 none (参考)', alpha=0.7)
            ax.semilogy(gts, [p['ber_vv'] for p in awgn_pts], 'D-', label='VV CFR')
            ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
            ax.set_title('AWGN (三方对照, 单 seed)')
            ax.set_xlabel('SNR (dB)')
            ax.set_ylabel('BER')
            ax.grid(True, which='both', alpha=0.3)
            ax.legend(fontsize=8)
            # strong 湍流
            ax = axes[1]
            gts = [p['snr_db'] for p in strong_pts]
            ax.semilogy(gts, [p['ber_eq_none'] for p in strong_pts], 'o-', label='NDA 等权 none (现状/bug)')
            ax.semilogy(gts, [p['ber_weighted_none'] for p in strong_pts], 's-', label='NDA 加权 none (修 D-008, 主)')
            ax.semilogy(gts, [p['ber_weighted_segmented'] for p in strong_pts], 'x--', label='NDA 加权 segmented (参考)', alpha=0.7)
            ax.semilogy(gts, [p['ber_vv'] for p in strong_pts], 'D-', label='VV CFR')
            ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
            ax.set_title('strong 湍流 (α1.5/β0.8, 三方对照, 单 seed)')
            ax.set_xlabel(r'$\gamma_d$ (dB)')
            ax.set_ylabel('BER')
            ax.grid(True, which='both', alpha=0.3)
            ax.legend(fontsize=8)
            fig.tight_layout()
            png_path = os.path.join(_HERE, '_ml_weighting_curves.png')
            fig.savefig(png_path, dpi=120)
            plt.close(fig)
            print(f"\n[PNG] {png_path}")
        except Exception as e:
            print(f"(PNG skipped: {e})")
            png_path = None

    # --- 落盘 JSON ---
    elapsed = time.time() - t0
    out = {
        'meta': {
            'task': 'NDA-ML 加权版 (修 D-008 Bug1 漏ML加权 + Bug2 升幂未归一化) vs 等权版 vs VV 三方对照',
            'weighting_formula': {
                'yn': '(rx/|rx|)^M0   (归一化升幂, B11 Eq.5, 修 Bug2)',
                'w': '|rx|^2          (ML 权重, B11 Eq.16, 修 Bug1)',
                'phi_none': 'angle(sum(w*yn)) / M0   (整块加权 mean-angle)',
                'phi_segmented': 'per K=8 段 angle(sum(w*yn))/M0 → unwrap → interp (brief §2)',
            },
            'fairness': '三方同 seed / 同 tx_bits / 同 awgn_wiener_channel / 同 generate_shared_realization_apsk / 同 rx_blind',
            'M0': P.M0,
            'LASER_LW_Hz': float(P.LASER_LW),
            'SIGMA2_P': float(P.SIGMA2_P),
            'TURB_strong_alpha_beta': list(P.TURB_ALPHA_BETA['strong']),
            'N_BLOCKS': P.N_BLOCKS,
            'seed_awgn': P.SEED_AWGN,
            'seed_turb0': P.SEED_TURB0,
            'HDFEC': P.HDFEC,
            'n_seeds': 1,
            'common_or_simulator_modified': False,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'awgn': awgn_pts,
        'strong_turbulence': strong_pts,
        'verdict_strong': v,
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(_HERE, '_ml_weighting_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
