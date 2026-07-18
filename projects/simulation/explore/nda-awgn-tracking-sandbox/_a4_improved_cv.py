# -*- coding: utf-8 -*-
"""A4 改进：SNR 自适应 CV 阈值 + 阈值敏感性扫描.

问题：固定 CV_TH=0.85 在低 SNR 误判（AWGN@5dB 理论 CV=0.855，被误判有衰落）。
解决：CV 阈值随 SNR 自适应——CV_th(snr) = AWGN理论CV(snr) × margin。

AWGN 理论 CV 标定（无衰落基准）：
  CV_awgn(snr) ≈ 0.74 + 0.12×exp(-snr/5)  （拟合标定数据）
  SNR=5: 0.855, SNR=10: 0.787, SNR=15: 0.756, SNR=20: 0.744

判据改进：CV_normalized = CV_measured / CV_awgn(snr)
  - CV_normalized < 1.1 → 无衰落 → NDA
  - CV_normalized ≥ 1.1 → 有衰落 → 按 γ_eff 切换

同时做阈值敏感性扫描：γ_eff_th ∈ {11, 13, 15}, CV margin ∈ {1.05, 1.1, 1.15}
确认结论鲁棒。

只跑 3 seed 快速验证（5 seed 太慢，敏感性扫描 9 组×3seed）。
"""
import os
import sys
import json
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

import _b11_params as P
import sc_nda_ml_sim as S
from common import (
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    nda_ml_recovery, da_ml_recovery,
    mmse_equalize, amp_limit,
    generate_shared_realization_apsk,
)
from params import SimulationConfig

OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')

# AWGN 理论 CV 模型（从标定数据拟合）
def cv_awgn_theory(snr_db):
    """无衰落 (h=1, AWGN+Wiener) 块内 CV 理论值. 16APSK."""
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def per_block_nda_da(rx_blind, rx_pilot, bits, tx_sym):
    omega_est = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    seg_foe = rx_blind * np.exp(-1j * omega_est * k)
    rc_nda, _, _, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
    pilot_idx_local = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    p_sym = tx_sym[pilot_idx_local]
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pilot_idx_local,
                                 pilot_sym=p_sym, mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    resolved_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda = int(np.sum(tb != m16apsk_demod(resolved_nda)))
    nb_nda = P.N_DFT * P.BITS_PER_SYM
    demod_da = m16apsk_demod(rc_da)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    tb_arr = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dm_arr = demod_da.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
    nb_da = int(np.sum(is_data) * P.BITS_PER_SYM)
    return ne_nda, nb_nda, ne_da, nb_da


def decide_switch_v2(rx_raw_seg, gamma_db, gamma_lin, gamma_eff_th, cv_margin):
    """改进判据 v2: SNR 自适应 CV 阈值."""
    pwr = np.abs(rx_raw_seg) ** 2
    cv_meas = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    cv_th = cv_awgn_theory(gamma_db) * cv_margin
    if cv_meas < cv_th:
        return 'nda'  # 无衰落
    h_est_blk = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    gamma_eff_est_db = gamma_db + 10 * np.log10(h_est_blk)
    return 'da' if gamma_eff_est_db < gamma_eff_th else 'nda'


def run_scene_switch(scene, snr_list, n_blocks, seed_list, cfg,
                     gamma_eff_th, cv_margin, is_awgn=False):
    """跑切换 vs NDA vs DA，返回 per_snr list（multi-seed mean）."""
    Ns = P.N_DFT
    per_snr = []
    for snr in snr_list:
        gamma_lin = 10 ** (snr / 10)
        all_nda = []; all_da = []; all_sw = []
        for si, seed_base in enumerate(seed_list):
            e_nda = e_da = e_sw = 0
            b_nda = b_da = b_sw = 0
            if is_awgn:
                seed = seed_base + int(snr * 1000)
                rng = np.random.default_rng(seed + 7)
                bits = rng.integers(0, 2, n_blocks * Ns * P.BITS_PER_SYM)
                tx = m16apsk_mod(bits)
                rx, _ = S.awgn_wiener_channel(tx, snr, seed)
                for b in range(n_blocks):
                    seg = rx[b*Ns:(b+1)*Ns]
                    tb_seg = bits[b*Ns*P.BITS_PER_SYM:(b+1)*Ns*P.BITS_PER_SYM]
                    rc_nda, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk',
                                                      assume_df_zero=True,
                                                      intra_block_tracking='segmented')
                    resolved = resolve_m16apsk_blockwise(rc_nda, tb_seg, block_size=P.BLOCK_SIZE_RESOLVE)
                    ne_nda = int(np.sum(tb_seg != m16apsk_demod(resolved)))
                    pilot_idx = np.arange(0, Ns, P.DA_PILOT_SPACING)
                    p_sym = tx[b*Ns + pilot_idx]
                    rc_da, _, _ = da_ml_recovery(seg, pilot_idx=pilot_idx, pilot_sym=p_sym, mod='m16apsk')
                    dm = m16apsk_demod(rc_da)
                    is_data = np.ones(Ns, dtype=bool); is_data[pilot_idx] = False
                    tb_a = tb_seg.reshape(Ns, P.BITS_PER_SYM)
                    dm_a = dm.reshape(Ns, P.BITS_PER_SYM)
                    ne_da = int(np.sum(tb_a[is_data] != dm_a[is_data]))
                    nb_da = int(np.sum(is_data) * P.BITS_PER_SYM)
                    e_nda += ne_nda; b_nda += Ns*P.BITS_PER_SYM
                    e_da += ne_da; b_da += nb_da
                    choice = decide_switch_v2(seg, snr, gamma_lin, gamma_eff_th, cv_margin)
                    if choice == 'da': e_sw += ne_da; b_sw += nb_da
                    else: e_sw += ne_nda; b_sw += Ns*P.BITS_PER_SYM
            else:
                seed0 = seed_base
                for b in range(n_blocks):
                    r = generate_shared_realization_apsk(
                        Ns, gamma_lin, scene, cfg.doppler.DOPPLER_HIGH,
                        mod='m16apsk', seed=seed0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']; tx_sym = r['tx']
                    h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
                    rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
                    h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
                    rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
                    ne_nda, nb_nda, ne_da, nb_da = per_block_nda_da(rx_blind, rx_pilot, bits, tx_sym)
                    e_nda += ne_nda; b_nda += nb_nda
                    e_da += ne_da; b_da += nb_da
                    choice = decide_switch_v2(rx_raw, snr, gamma_lin, gamma_eff_th, cv_margin)
                    if choice == 'da': e_sw += ne_da; b_sw += nb_da
                    else: e_sw += ne_nda; b_sw += nb_nda
            all_nda.append(e_nda/b_nda); all_da.append(e_da/b_da); all_sw.append(e_sw/b_sw)
        ber_nda = np.mean(all_nda); ber_da = np.mean(all_da); ber_sw = np.mean(all_sw)
        ber_max = min(ber_nda, ber_da)
        sw_vs_max = 10*np.log10(ber_max/ber_sw) if ber_sw > 0 and ber_max > 0 else 0
        per_snr.append({
            'snr_db': float(snr), 'nda_ber': float(ber_nda), 'da_ber': float(ber_da),
            'switch_ber': float(ber_sw), 'max_ber': float(ber_max),
            'switch_vs_max_db': float(sw_vs_max),
            'per_seed_switch_vs_max_db': [float(10*np.log10(min(n,d)/s)) if s>0 else 0
                                          for n,d,s in zip(all_nda, all_da, all_sw)],
        })
    return per_snr


def main():
    cfg = SimulationConfig()
    N_SEEDS = 3
    seed_awgn = [P.SEED_AWGN + i for i in range(N_SEEDS)]
    seed_turb = [P.SEED_TURB0 + i * P.N_BLOCKS for i in range(N_SEEDS)]
    N_BLOCKS = 400

    # 敏感性扫描
    configs = [
        (13.0, 1.10),  # 基准
        (11.0, 1.10), (15.0, 1.10),  # γ_eff_th 敏感性
        (13.0, 1.05), (13.0, 1.15),  # CV margin 敏感性
    ]

    print("=" * 110)
    print("A4 改进: SNR 自适应 CV 阈值 + 敏感性扫描 (3 seed)")
    print("=" * 110)

    all_results = {}
    for gamma_eff_th, cv_margin in configs:
        key = f"geth{gamma_eff_th}_cvmar{cv_margin}"
        print(f"\n##### {key} #####")
        results = {}
        results['awgn'] = run_scene_switch('awgn', P.SNR_AWGN_DB, N_BLOCKS,
                                           seed_awgn, cfg, gamma_eff_th, cv_margin, is_awgn=True)
        for turb in ['weak', 'moderate', 'strong']:
            results[turb] = run_scene_switch(turb, P.SNR_TURB_DB, N_BLOCKS,
                                             seed_turb, cfg, gamma_eff_th, cv_margin)
        all_results[key] = results
        # 打印汇总
        print(f"  {'场景':<10} {'γd':>5} {'SW-max':>9}")
        n_fail = 0
        for sc in ['awgn','weak','moderate','strong']:
            for p in results[sc]:
                svm = p['switch_vs_max_db']
                flag = ' FAIL' if svm < -0.1 else ''
                if svm < -0.1: n_fail += 1
                print(f"  {sc:<10} {p['snr_db']:>5.0f} {svm:>+8.2f}dB{flag}")
        print(f"  → FAIL 点数: {n_fail}/{sum(len(results[s]) for s in results)}")

    # 落盘
    out = {
        'meta': {
            'task': 'A4 改进: SNR 自适应 CV 阈值 + 敏感性扫描',
            'cv_model': 'CV_awgn(snr) = 0.74 + 0.12*exp(-snr/5)',
            'criterion_v2': 'CV_normalized = CV_measured / CV_awgn(snr); <margin→无衰落→NDA; ≥margin→按γ_eff切',
            'n_seeds': N_SEEDS,
            'configs_scanned': [str(c) for c in configs],
        },
        'results': all_results,
    }
    out_json = os.path.join(OUT_DIR, '_a4_improved_cv_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=lambda x: float(x) if isinstance(x, (np.floating,)) else x)
    print(f"\n[保存] {out_json}")


if __name__ == '__main__':
    t0 = time.time()
    main()
    print(f"[耗时] {time.time()-t0:.1f}s")
