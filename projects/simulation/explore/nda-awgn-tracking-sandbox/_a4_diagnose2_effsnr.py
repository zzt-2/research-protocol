# -*- coding: utf-8 -*-
"""A4 诊断 2：crossover 是否由 per-block 有效 SNR (γ_eff = γ·h) 决定?

诊断 1 发现 deep fade 在不同全局 SNR 下赢家相反，说明单纯 fade 深度不够。
假设：真正的判据是 per-block 有效 SNR γ_eff_dB = γ_dB + 10log10(h)。
- γ_eff 低 → DA 赢（pilot 显式参考比盲升幂好）
- γ_eff 高 → NDA 赢（全 block 积分鲁棒 + pilot overhead 惩罚）

如果假设成立，所有场景所有 SNR 点的赢家切换应汇聚到同一个 γ_eff 阈值附近。
"""
import os
import sys

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
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    nda_ml_recovery, da_ml_recovery,
    mmse_equalize, amp_limit,
)
from params import SimulationConfig


def per_block_ber(rx_blind, rx_pilot, bits, tx_sym):
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
    demod_da = m16apsk_demod(rc_da)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    tb_arr = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dm_arr = demod_da.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
    nb_da = int(np.sum(is_data) * P.BITS_PER_SYM)
    return ne_nda, P.N_DFT * P.BITS_PER_SYM, ne_da, nb_da


def diagnose():
    cfg = SimulationConfig()
    n_blocks = 400

    # 汇总所有场景所有 SNR 的 (γ_eff_dB, NDA_err, DA_err)
    all_points = []  # (gamma_eff_db, nda_err, nda_nb, da_err, da_nb)

    cases = [
        ('weak', [10.0, 15.0, 20.0, 22.0, 24.0]),
        ('moderate', [10.0, 15.0, 20.0, 22.0, 24.0]),
        ('strong', [10.0, 15.0, 20.0, 22.0, 24.0]),
    ]

    print("=" * 110)
    print("A4 诊断 2：赢家是否由 per-block 有效 SNR γ_eff = γ·h 决定?")
    print("（若成立，所有场景/全局SNR 的赢家切换应汇聚到同一 γ_eff 阈值）")
    print("=" * 110)

    for turb_name, snr_list in cases:
        for gamma_db in snr_list:
            gamma_lin = 10 ** (gamma_db / 10)
            seed0 = P.SEED_TURB0
            # 按 γ_eff_dB 桶收集
            bucket = {}  # gamma_eff_bin -> [nda_err, nda_nb, da_err, da_nb]
            for b in range(n_blocks):
                r = generate_shared_realization_apsk(
                    P.N_DFT, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                    mod='m16apsk', seed=seed0 + b)
                rx_raw = r['rx_raw']; bits = r['bits']; tx_sym = r['tx']
                h_true = r['h']
                h_blk = float(np.mean(h_true[:P.N_DFT]))
                gamma_eff_db = gamma_db + 10 * np.log10(max(h_blk, 1e-6))
                # 桶宽 2dB
                bin_key = round(gamma_eff_db / 2.0) * 2.0
                h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
                rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
                h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
                rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
                ne_nda, nb_nda, ne_da, nb_da = per_block_ber(rx_blind, rx_pilot, bits, tx_sym)
                if bin_key not in bucket:
                    bucket[bin_key] = [0, 0, 0, 0]
                bucket[bin_key][0] += ne_nda; bucket[bin_key][1] += nb_nda
                bucket[bin_key][2] += ne_da; bucket[bin_key][3] += nb_da

            print(f"\n--- {turb_name} @ γ={gamma_db}dB ---")
            print(f"  {'γ_eff(dB)':>9} {'n_blk':>6} {'NDA_BER':>10} {'DA_BER':>10} {'winner':>7} {'margin':>8}")
            for bin_key in sorted(bucket.keys()):
                ne_nda, nb_nda, ne_da, nb_da = bucket[bin_key]
                n_blk = nb_nda // (P.N_DFT * P.BITS_PER_SYM)
                ber_nda = ne_nda / nb_nda if nb_nda else 0
                ber_da = ne_da / nb_da if nb_da else 0
                if ber_nda < ber_da:
                    winner = 'NDA'; margin = 10*np.log10(ber_da/ber_nda) if ber_nda > 0 else float('inf')
                elif ber_da < ber_nda:
                    winner = 'DA'; margin = 10*np.log10(ber_nda/ber_da) if ber_da > 0 else float('inf')
                else:
                    winner = 'tie'; margin = 0
                print(f"  {bin_key:>9.0f} {n_blk:>6} {ber_nda:>10.3e} {ber_da:>10.3e} {winner:>7} {margin:>7.2f}dB")


if __name__ == '__main__':
    diagnose()
