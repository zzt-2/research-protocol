# -*- coding: utf-8 -*-
"""A4 切换策略 — per-regime crossover 阈值版（Q17 探索）.

**背景**：`_a4_switch_30seed_fixed.py` 的 decide() 用固定 GAMMA_EFF_TH=13.0 dB 跨所有
regime 统一。论文 W002 §III 声称 "γ_th is set to the measured crossover SNR, determined
separately for each regime"。两者不符。本脚本验证：把 decide() 改成 per-regime crossover
阈值后，选对率/增益怎么变。

**路径 A（保留 γ_eff 判据结构，threshold 改 per-regime）**:
- crossover 在 γ 轴（平均 SNR）测的；decide() 阈值作用在 γ_eff 轴（γ_eff = γ_db + 10·log10(h_blind)）。
- 换算依据：median(h_blind) ≈ 1（unit-normalized fading），所以 median(γ_eff) ≈ γ_db。
  实测（probe_h_dist）：各 regime median(h) 在 0.77~1.15，median(γ_eff) ≈ γ_db ± 1dB。
  → 直接令 GAMMA_EFF_TH[regime] = crossover_γ[regime] 是自然映射。

**per-regime 阈值**（来自 /tmp/verify_logic_chain.py 断言1，事后从 BER 数据线性插值）:
  - awgn     : 无 crossover（DA 全程输 NDA）→ 设高阈值（如 99）让 decide 永远选 NDA
  - weak     : 17.9 dB
  - moderate : 16.8 dB
  - strong   : 10.7 dB

**Q17 冷静期关键问题**：crossover 17.9/16.8/10.7 是事后从 BER 数据测的（数据相关，
"偷看结果"风险）。接收端真实部署时不可能先跑 BER 曲线再定阈值。本脚本只回答"如果
用了 per-regime crossover 当阈值，选对率/增益的上界是多少"——可实现性单结论在报告里。

**守纪律**:
- D005: data 口径才物理公平（DA 错误数/768 data bit），用 data 口径判选对率
- D002: 基于 _a4_switch_30seed_fixed.py（修复版），不用 buggy 版
- TL-22/TL-23: 震撼结果先查物理前提；SW ≥ per-seed per-block-oracle 自检 0 违例
- TL-29: 换口径/判据先校准
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
from scipy import stats

OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')
N_SEEDS_DEFAULT = 30
CV_MARGIN = 1.10

# per-regime crossover 阈值（路径 A：GAMMA_EFF_TH[regime] = crossover_γ[regime]）
# 来源：/tmp/verify_logic_chain.py 断言1（事后从 BER 数据线性插值 DA_data vs NDA 交叉点）
# awgn 无 crossover（DA 全程输 NDA）→ 设高阈值让 decide 永远选 NDA
GAMMA_EFF_TH_REGIME = {
    'awgn': 99.0,      # 无 crossover，DA 在 AWGN 全程输 → 永远选 NDA
    'weak': 17.9,      # crossover ≈ 17.9 dB
    'moderate': 16.8,  # crossover ≈ 16.8 dB
    'strong': 10.7,    # crossover ≈ 10.7 dB
}

# 全块 bit 分母（与 fixed 版一致：所有方法统一用此口径算 full BER）
FULL_BITS_PER_BLOCK = P.N_DFT * P.BITS_PER_SYM   # 256 × 4 = 1024


def cv_awgn_theory(snr_db):
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def decide(rx_seg, gamma_db, gamma_lin, regime):
    """两层切换判据（per-regime γ_eff 阈值版）.

    与 fixed 版唯一区别：γ_eff 阈值从固定 13.0 改成 per-regime crossover。
    CV 门控不变（CV 低 → 纯噪声 → NDA）。
    """
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    th = GAMMA_EFF_TH_REGIME.get(regime, 13.0)
    return 'da' if gamma_db + 10 * np.log10(h) < th else 'nda'


def per_block(rx_blind, rx_pilot, bits, tx_sym):
    """湍流 per-block：返回 ne_nda, ne_da（与 fixed 版完全一致，不改）."""
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                 pilot_sym=tx_sym[pidx], mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda = int(np.sum(tb != m16apsk_demod(res_nda)))
    dm = m16apsk_demod(rc_da)
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM); dma = dm.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tba[is_d] != dma[is_d]))   # data 位错误数（pilot 不计）
    return ne_nda, ne_da


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)); std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def main(n_seeds=N_SEEDS_DEFAULT):
    cfg = SimulationConfig()
    NB = P.N_BLOCKS; Ns = P.N_DFT
    t0 = time.time()
    ths = " / ".join(f"{k}:{v}" for k, v in GAMMA_EFF_TH_REGIME.items())
    print(f"A4 切换 [PER-REGIME] {n_seeds} seed (geth{{{ths}}}_cvmar{CV_MARGIN})")

    raw = {sc: [] for sc in ['awgn', 'weak', 'moderate', 'strong']}

    # ============ AWGN ============
    for i in range(n_seeds):
        sb = P.SEED_AWGN + i
        per_snr = []
        for snr in P.SNR_AWGN_DB:
            gl = 10 ** (snr / 10)
            seed = sb + int(snr * 1000)
            rng = np.random.default_rng(seed + 7)
            bits = rng.integers(0, 2, NB * Ns * P.BITS_PER_SYM)
            tx = m16apsk_mod(bits)
            rx, _ = S.awgn_wiener_channel(tx, snr, seed)
            e_n = e_d = e_s = e_o = 0
            for b in range(NB):
                seg = rx[b * Ns:(b + 1) * Ns]
                tb = bits[b * Ns * P.BITS_PER_SYM:(b + 1) * Ns * P.BITS_PER_SYM]
                rc_n, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk',
                                                assume_df_zero=True, intra_block_tracking='segmented')
                res = resolve_m16apsk_blockwise(rc_n, tb, block_size=P.BLOCK_SIZE_RESOLVE)
                ne_n = int(np.sum(tb != m16apsk_demod(res)))
                pidx = np.arange(0, Ns, P.DA_PILOT_SPACING)
                rc_d, _, _ = da_ml_recovery(seg, pilot_idx=pidx,
                                            pilot_sym=tx[b * Ns + pidx], mod='m16apsk')
                dm = m16apsk_demod(rc_d)
                isd = np.ones(Ns, dtype=bool); isd[pidx] = False
                tba = tb.reshape(Ns, P.BITS_PER_SYM); dma = dm.reshape(Ns, P.BITS_PER_SYM)
                ne_d = int(np.sum(tba[isd] != dma[isd]))
                e_n += ne_n; e_d += ne_d
                e_o += min(ne_n, ne_d)
                c = decide(seg, snr, gl, 'awgn')
                if c == 'da':
                    e_s += ne_d
                else:
                    e_s += ne_n
            n_blk_bits_full = NB * FULL_BITS_PER_BLOCK
            n_data_bits = NB * int((Ns - len(np.arange(0, Ns, P.DA_PILOT_SPACING))) * P.BITS_PER_SYM)
            per_snr.append({'snr_db': float(snr),
                            'nda': e_n / n_blk_bits_full,
                            'da_full': e_d / n_blk_bits_full,
                            'da_data': e_d / n_data_bits,
                            'sw': e_s / n_blk_bits_full,
                            'oracle': e_o / n_blk_bits_full})
        raw['awgn'].append(per_snr)
        if (i + 1) % 5 == 0:
            print(f"  awgn seed {i + 1}/{n_seeds} ({time.time() - t0:.0f}s)")

    # ============ 湍流 ============
    for turb in ['weak', 'moderate', 'strong']:
        for i in range(n_seeds):
            s0 = P.SEED_TURB0 + i * NB
            per_snr = []
            for gdb in P.SNR_TURB_DB:
                gl = 10 ** (gdb / 10)
                e_n = e_d = e_s = e_o = 0
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                                         mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
                    hb = S.estimate_h_blind_perblock(rx_raw, gl)
                    rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                    hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
                    rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
                    ne_n, ne_d = per_block(rxb, rxp, bits, txs)
                    e_n += ne_n; e_d += ne_d
                    e_o += min(ne_n, ne_d)
                    c = decide(rx_raw, gdb, gl, turb)
                    if c == 'da':
                        e_s += ne_d
                    else:
                        e_s += ne_n
                n_blk_bits_full = NB * FULL_BITS_PER_BLOCK
                n_data_bits = NB * int((Ns - len(np.arange(0, Ns, P.DA_PILOT_SPACING))) * P.BITS_PER_SYM)
                per_snr.append({'snr_db': float(gdb),
                                'nda': e_n / n_blk_bits_full,
                                'da_full': e_d / n_blk_bits_full,
                                'da_data': e_d / n_data_bits,
                                'sw': e_s / n_blk_bits_full,
                                'oracle': e_o / n_blk_bits_full})
            raw[turb].append(per_snr)
        print(f"  {turb} done ({time.time() - t0:.0f}s)")

    elapsed = time.time() - t0

    # ============ 聚合（与 fixed 版结构一致） ============
    n_violations = 0
    summary = {}
    for sc in ['awgn', 'weak', 'moderate', 'strong']:
        snrs = [p['snr_db'] for p in raw[sc][0]]
        pts = []
        for j, snr in enumerate(snrs):
            nda = [raw[sc][i][j]['nda'] for i in range(n_seeds)]
            da_full = [raw[sc][i][j]['da_full'] for i in range(n_seeds)]
            da_data = [raw[sc][i][j]['da_data'] for i in range(n_seeds)]
            sw = [raw[sc][i][j]['sw'] for i in range(n_seeds)]
            oracle = [raw[sc][i][j]['oracle'] for i in range(n_seeds)]
            m_n, *_ = ci_t(nda)
            m_d_full, *_ = ci_t(da_full)
            m_d_data, *_ = ci_t(da_data)
            m_sw, s_sw, hw_sw, lo_sw, hi_sw = ci_t(sw)
            m_o, *_ = ci_t(oracle)
            gain_vs_da_net = 10 * np.log10(m_d_full / m_sw) if m_sw > 0 and m_d_full > 0 else 0.0
            gain_vs_nda = 10 * np.log10(m_n / m_sw) if m_sw > 0 and m_n > 0 else 0.0
            gain_vs_da_gross = 10 * np.log10(m_d_data / m_sw) if m_sw > 0 and m_d_data > 0 else 0.0
            gain_oracle_vs_sw = 10 * np.log10(m_sw / m_o) if m_sw > 0 and m_o > 0 else 0.0
            g_da_seed = [10 * np.log10(d / s) if s > 0 and d > 0 else 0.0
                         for d, s in zip(da_full, sw)]
            g_nda_seed = [10 * np.log10(n / s) if s > 0 and n > 0 else 0.0
                          for n, s in zip(nda, sw)]
            m_gda, _, hw_gda, lo_gda, hi_gda = ci_t(g_da_seed)
            m_gnda, _, hw_gnda, lo_gnda, hi_gnda = ci_t(g_nda_seed)
            pts.append({
                'snr_db': float(snr),
                'nda_ber_mean': m_n,
                'da_ber_mean_full': m_d_full, 'da_ber_mean_data': m_d_data,
                'switch_ber_mean': m_sw, 'switch_ber_ci95': [lo_sw, hi_sw],
                'oracle_ber_mean': m_o,
                'switch_vs_da_net_db_mean': gain_vs_da_net,
                'switch_vs_da_net_db_ci95': [lo_gda, hi_gda],
                'switch_vs_nda_db_mean': gain_vs_nda,
                'switch_vs_nda_db_ci95': [lo_gnda, hi_gnda],
                'oracle_vs_switch_db_mean': gain_oracle_vs_sw,
                'switch_vs_da_gross_db_mean': gain_vs_da_gross,
                'per_seed_switch_vs_da_db': g_da_seed,
                'per_seed_switch_vs_nda_db': g_nda_seed,
            })
            for o_v, s_v in zip(oracle, sw):
                if o_v > 0 and s_v < o_v * (1 - 1e-9):
                    n_violations += 1
        summary[sc] = {'snr_db': snrs, 'points': pts}

    out = {
        'meta': {
            'task': 'A4 切换 30 seed [PER-REGIME crossover]', 'n_seeds': n_seeds,
            'gamma_eff_th_regime': GAMMA_EFF_TH_REGIME, 'cv_margin': CV_MARGIN,
            'cv_model': 'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
            'ci_method': f't-dist 95% df={n_seeds - 1}',
            'elapsed_sec': float(elapsed),
            'crossover_source': '事后从 BER 数据线性插值 DA_data vs NDA 交叉点 (/tmp/verify_logic_chain.py 断言1)',
            'path': 'A: 保留 γ_eff 判据结构，threshold 改 per-regime crossover',
            'measurability_note': (
                'crossover 17.9/16.8/10.7 是事后从 BER 数据测的——接收端真实部署时不可直接获得。'
                '本结果回答的是"用了 per-regime crossover 当阈值的选对率/增益上界"，可实现性单结论。'
            ),
            'ber_convention': (
                'NDA/DA_full/SW all on full-block bits (1024) — same denominator. '
                'DA_data = DA errors / data bits (768) = standard info-BER (physically fair, D005). '
                'NDA has no pilot so full==data for NDA.'
            ),
            'selfcheck_min_violations': n_violations,
        },
        'summary': summary,
    }
    suffix = '30seed' if n_seeds >= 30 else f'{n_seeds}seed'
    out_json = os.path.join(OUT_DIR, f'_a4_switch_{suffix}_per_regime.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False,
                  default=lambda x: float(x) if isinstance(x, (np.floating,)) else x)
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"[TL-23 自检] SW < per-seed per-block-oracle 违例数 = {n_violations}（应为 0）")
    print(f"\n{'场景':<9}{'γd':>5}{'NDA':>10}{'DAnet':>10}{'SW':>10}{'ORC':>10}{'SWvsDAnet':>11}{'[CI95]':>14}{'SWvsNDA':>9}{'[CI95]':>14}{'ORC-SW':>8}")
    for sc in ['awgn', 'weak', 'moderate', 'strong']:
        for p in summary[sc]['points']:
            gda = p['switch_vs_da_net_db_mean']; lo_d, hi_d = p['switch_vs_da_net_db_ci95']
            gnda = p['switch_vs_nda_db_mean']; lo_n, hi_n = p['switch_vs_nda_db_ci95']
            orc = p['oracle_vs_switch_db_mean']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{p['nda_ber_mean']:>10.2e}{p['da_ber_mean_full']:>10.2e}"
                  f"{p['switch_ber_mean']:>10.2e}{p['oracle_ber_mean']:>10.2e}"
                  f"{gda:>+10.2f}[{lo_d:+.1f},{hi_d:+.1f}]{gnda:>+8.2f}[{lo_n:+.1f},{hi_n:+.1f}]{orc:>+7.2f}")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=N_SEEDS_DEFAULT)
    a = ap.parse_args()
    main(n_seeds=a.seeds)
