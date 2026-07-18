# -*- coding: utf-8 -*-
"""A4 诊断：crossover 的物理条件是 SNR-driven 还是 fade-driven?

目的：设计切换判据前，必须确认 crossover 到底随什么条件变。
- SNR-driven：全局 SNR 高 NDA 赢，SNR 低 DA 赢 → 判据用 SNR 估计
- fade-driven：per-block h 小(deep fade) NDA 赢，h 大 DA 赢 → 判据用 fade 深度检测
- 或两者交叉

方法：在 weak/moderate/strong 三场景，多个 SNR 点，把每个 block 按 h 分桶，
分别统计各桶内 DA BER vs NDA BER，看赢家随 h 怎么变。

这是诊断脚本，不追求 5 seed 统计，只看物理趋势（1-2 seed 够看趋势）。
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


def per_block_nda_da_ber(rx_blind, rx_pilot, bits, tx_sym):
    """单 block 内分别跑 NDA 和 DA，返回各自的 (n_err, n_bits)."""
    # NDA: fft_foe + nda CPE
    omega_est = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    seg_foe = rx_blind * np.exp(-1j * omega_est * k)
    rc_nda, _, _, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
    # DA: pilot FOE+CPE
    pilot_idx_local = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    p_sym = tx_sym[pilot_idx_local]
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pilot_idx_local,
                                 pilot_sym=p_sym, mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    resolved_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda = int(np.sum(tb != m16apsk_demod(resolved_nda)))
    # DA BER only on data symbols
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
    Ns = P.N_DFT

    # 测试点：weak/moderate/strong × 几个 SNR
    test_cases = [
        ('weak', 15.0), ('weak', 20.0), ('weak', 22.0),
        ('moderate', 15.0), ('moderate', 20.0), ('moderate', 22.0),
        ('strong', 15.0), ('strong', 20.0),
    ]

    print("=" * 100)
    print("A4 诊断：crossover 是 SNR-driven 还是 fade-driven?")
    print("=" * 100)

    for turb_name, gamma_db in test_cases:
        gamma_lin = 10 ** (gamma_db / 10)
        # h 分桶边界（log10 h），从 deep fade 到正常
        # 收集所有 block 的 h, NDA BER, DA BER
        h_list = []
        nda_bits_list = []
        da_bits_list = []
        seed0 = P.SEED_TURB0  # seed 0 够看趋势

        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            tx_sym = r['tx']
            h_true = r['h']
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            ne_nda, nb_nda, ne_da, nb_da = per_block_nda_da_ber(
                rx_blind, rx_pilot, bits, tx_sym)
            # block 的代表 h（取块内均值，block 内 h 恒定）
            h_blk = float(np.mean(h_true[:Ns]))
            h_list.append(h_blk)
            nda_bits_list.append((ne_nda, nb_nda))
            da_bits_list.append((ne_da, nb_da))

        h_arr = np.array(h_list)
        # 按 h 分桶（dB）：-20..0 dB h（相对），步长 2dB
        h_db = 10 * np.log10(np.maximum(h_arr, 1e-6))
        bins = np.arange(-20, 0.1, 2.0)

        print(f"\n--- {turb_name} @ γ={gamma_db}dB ---")
        print(f"  h 范围: [{h_db.min():.1f}, {h_db.max():.1f}] dB, median={np.median(h_db):.1f}dB")
        print(f"  {'h_bin(dB)':>10} {'n_blk':>6} {'NDA_BER':>10} {'DA_BER':>10} {'winner':>8} {'margin(dB)':>10}")

        # 全局对照
        tot_nda = sum(ne for ne, _ in nda_bits_list)
        tot_nb_nda = sum(nb for _, nb in nda_bits_list)
        tot_da = sum(ne for ne, _ in da_bits_list)
        tot_nb_da = sum(nb for _, nb in da_bits_list)
        g_nda = tot_nda / tot_nb_nda
        g_da = tot_da / tot_nb_da
        winner_g = 'NDA' if g_nda < g_da else 'DA'
        print(f"  {'GLOBAL':>10} {n_blocks:>6} {g_nda:>10.4e} {g_da:>10.4e} {winner_g:>8}")

        for lo in bins:
            hi = lo + 2.0
            mask = (h_db >= lo) & (h_db < hi)
            if mask.sum() < 5:
                continue
            s_nda = sum(nda_bits_list[i][0] for i in np.where(mask)[0])
            sb_nda = sum(nda_bits_list[i][1] for i in np.where(mask)[0])
            s_da = sum(da_bits_list[i][0] for i in np.where(mask)[0])
            sb_da = sum(da_bits_list[i][1] for i in np.where(mask)[0])
            if sb_nda == 0 or sb_da == 0:
                continue
            ber_nda = s_nda / sb_nda
            ber_da = s_da / sb_da
            winner = 'NDA' if ber_nda < ber_da else ('DA' if ber_da < ber_nda else 'tie')
            # margin in dB (BER ratio → approx dB, rough)
            if ber_nda > 0 and ber_da > 0:
                ratio = ber_nda / ber_da
                margin_db = 10 * np.log10(ratio) if winner == 'NDA' else -10 * np.log10(1 / ratio) if ratio != 1 else 0
                margin_db = 10 * np.log10(max(ber_nda, ber_da) / min(ber_nda, ber_da)) if ber_nda != ber_da else 0
                sign = '+' if winner == 'NDA' else '-'
            else:
                margin_db = 0
                sign = '?'
            print(f"  [{lo:>5.0f},{hi:>3.0f}) {int(mask.sum()):>6} {ber_nda:>10.4e} {ber_da:>10.4e} "
                  f"{winner:>8} {sign}{margin_db:>8.2f}")


if __name__ == '__main__':
    diagnose()
