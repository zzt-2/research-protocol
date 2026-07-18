# -*- coding: utf-8 -*-
"""A4 切换策略 — common-768 公平口径探测（5seed × 9点，探索性）.

**目的（R004 §3/§5）**：验证 selector 在 common-768 公平口径下的真实增益。
Fig.5 现有 mixed 口径有问题（R004 G4）：selector 选 DA 时错误计数在 768 解码数据
位上累加，选 NDA 时在 1024 全部位上累加，两边都除 1024 但比值约掉，实际是
branch-dependent error-count ratio，不是公平 BER。R004 §3 病态退化证明：即使
selector 毫无本事，只要选了 DA 窗也会机械白送最多 1.249 dB。

本探针把口径改成 common-768（NDA 和 selector 都只在 DA 评的那 192 个非 pilot
symbol = 768 bit 上算错误），看真实增益是多少。

**common-768 mask 定义（R004 §3 已验证，不重新定义）**：
  - pilot symbol 位置：np.arange(0,256,4)，共 64 个
  - 非 pilot symbol：其余 192 个，每个 4 bit = 768 bit
  - DA 本身只评这 768 位（ne_da 就是 common-768），DA 不重算
  - NDA 评全部 1024 位 → 新增 ne_nda_common768 = NDA demod 结果在 192 非 pilot
    symbol 上的错误数
  - selector common-768：选 DA 窗用 ne_da（=common-768），选 NDA 窗用 ne_nda_common768

**纪律（brief）**：
  - 不改 estimate/decide/demod 逻辑（只加位计数，不重新估计）
  - 不改图/不改判据/不改参数/改正文
  - 5seed 探索性，CI 很宽，只看趋势；mixed 口径应复现现有 2.3/2.0/1.3 附近
    （sanity check，若不复现说明改错了）
  - TL-23 守门：5seed 结果不外传不写论文，只作内部决策依据

**两口径增益定义**（gain 正=selector 错误更少=selector 赢）：
  - mixed 口径（现有 = _a4_switch_30seed_fixed.py 的 switch_vs_nda_db_mean）：
      gain_mixed = 10·log10(Σ ne_nda_all1024 / Σ ne_sw_mixed)
    与 NDA/selector 全除 1024 等价（分母约掉）。
  - common768 口径（新）：
      gain_c768 = 10·log10(Σ ne_nda_common768 / Σ ne_sw_common768)
    NDA 和 selector 都除 (N_win × 768)，公平同口径。

**基于** `_a4_switch_30seed_fixed.py`，改 4 处：
  1. seed 数 30 → 5（PROBE_N_SEEDS）
  2. 缩减：只跑 weak/moderate/strong × {5,10,15} dB = 9 点（跳过 AWGN 省时间；
     AWGN common-768 计数逻辑与湍流对称，但不在 9 点探测范围内，故省略）
  3. per_block() 加一行算 ne_nda_common768（NDA demod reshape 取 is_d mask）
  4. 湍流循环加累加器 e_n_c768/e_s_c768；聚合段新增 common768 口径 BER + gain
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
N_SEEDS_DEFAULT = 5                # brief: 30 → 5（最小切片）
GAMMA_EFF_TH = 13.0
CV_MARGIN = 1.10

# 全块 bit 分母（Bug 1 修复：mixed 口径所有方法统一用此口径）
FULL_BITS_PER_BLOCK = P.N_DFT * P.BITS_PER_SYM          # 256 × 4 = 1024
# common-768 mask：192 非 pilot symbol × 4 bit = 768 bit
N_PILOT = P.N_DFT // P.DA_PILOT_SPACING                  # 256/4 = 64 pilot symbol
COMMON768_SYMS = P.N_DFT - N_PILOT                        # 192 非 pilot symbol
COMMON768_BITS_PER_BLOCK = COMMON768_SYMS * P.BITS_PER_SYM   # 192 × 4 = 768

# 探测点缩减：weak/moderate/strong × {5,10,15} dB = 9 点（brief）
PROBE_SCENES = ['weak', 'moderate', 'strong']
PROBE_SNR_DB = [5.0, 10.0, 15.0]


def cv_awgn_theory(snr_db):
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def decide(rx_seg, gamma_db, gamma_lin):
    """两层切换判据（保留 raw 信号，见 _a4_switch_30seed_fixed.py decide docstring）.

    不改判据逻辑（brief 纪律）。判据用 raw 信号统计 CV + 盲 h。
    """
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'


def per_block(rx_blind, rx_pilot, bits, tx_sym):
    """湍流 per-block：返回 ne_nda, ne_da, ne_nda_common768（错误数）.

    不改 estimate/decide/demod 逻辑（brief 纪律），仅新增 ne_nda_common768。
      - ne_nda：NDA demod 在全部 1024 bit 上错误数（mixed 口径 NDA 分子）
      - ne_da：DA demod 在 192 非 pilot symbol = 768 bit 上错误数（= common-768，
        DA 只评这些位，pilot 不算信息错误）
      - ne_nda_common768：NDA demod 在同一 192 非 pilot symbol = 768 bit 上错误数
        （common-768 口径 NDA 分子）= 新增计数
    """
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                 pilot_sym=tx_sym[pidx], mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    dm_nda = m16apsk_demod(res_nda)                       # NDA demod（全部 256 symbol）
    ne_nda = int(np.sum(tb != dm_nda))                    # 全部 1024 bit 错误数（mixed）
    dm = m16apsk_demod(rc_da)
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dma_nda = dm_nda.reshape(P.N_DFT, P.BITS_PER_SYM)     # 新增：NDA demod reshape
    dma = dm.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tba[is_d] != dma[is_d]))           # data 位错误数 = common-768
    # 新增：NDA 在同一 192 非 pilot symbol 上的错误数 = common-768 口径 NDA 分子
    ne_nda_common768 = int(np.sum(tba[is_d] != dma_nda[is_d]))
    return ne_nda, ne_da, ne_nda_common768


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
    print(f"A4 切换 [common-768 PROBE] {n_seeds} seed × {len(PROBE_SCENES)}场景 × "
          f"{len(PROBE_SNR_DB)}点 = {n_seeds * len(PROBE_SCENES) * len(PROBE_SNR_DB)} seed-point")

    raw = {sc: [] for sc in PROBE_SCENES}

    # AWGN 跳过（不在 9 点探测范围，省时间；common-768 计数逻辑与湍流对称）

    # ============ 湍流（仅 weak/moderate/strong × {5,10,15} dB）============
    for turb in PROBE_SCENES:
        for i in range(n_seeds):
            s0 = P.SEED_TURB0 + i * NB
            per_snr = []
            for gdb in PROBE_SNR_DB:
                gl = 10 ** (gdb / 10)
                e_n = e_d = e_s = e_o = 0
                e_n_c768 = e_s_c768 = 0     # 新增：common-768 累加器
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                                         mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
                    hb = S.estimate_h_blind_perblock(rx_raw, gl)
                    rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                    hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
                    rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
                    ne_n, ne_d, ne_n_c768 = per_block(rxb, rxp, bits, txs)   # 新增第三返回值
                    e_n += ne_n; e_d += ne_d
                    e_n_c768 += ne_n_c768                     # 新增
                    e_o += min(ne_n, ne_d)                     # per-block oracle 上界
                    c = decide(rx_raw, gdb, gl)
                    if c == 'da':
                        e_s += ne_d
                        e_s_c768 += ne_d                        # 新增：DA 窗 = common-768（ne_d 本就是）
                    else:
                        e_s += ne_n
                        e_s_c768 += ne_n_c768                   # 新增：NDA 窗 = common-768
                n_blk_bits_full = NB * FULL_BITS_PER_BLOCK
                n_data_bits = NB * int((Ns - len(np.arange(0, Ns, P.DA_PILOT_SPACING))) * P.BITS_PER_SYM)
                n_c768_bits = NB * COMMON768_BITS_PER_BLOCK     # 新增：400 × 768
                per_snr.append({'snr_db': float(gdb),
                                # mixed 口径（同 _a4_switch_30seed_fixed.py）
                                'nda': e_n / n_blk_bits_full,
                                'da_full': e_d / n_blk_bits_full,
                                'da_data': e_d / n_data_bits,
                                'sw': e_s / n_blk_bits_full,
                                'oracle': e_o / n_blk_bits_full,
                                # 新增：common-768 口径 BER
                                'nda_c768': e_n_c768 / n_c768_bits,
                                'sw_c768': e_s_c768 / n_c768_bits,
                                # 新增：raw 错误计数（供建议主控验证）
                                'raw_ne_nda_all1024': int(e_n),
                                'raw_ne_sw_mixed': int(e_s),
                                'raw_ne_nda_common768': int(e_n_c768),
                                'raw_ne_da': int(e_d),       # DA = common-768
                                'raw_ne_sw_common768': int(e_s_c768),
                                })
            raw[turb].append(per_snr)
        print(f"  {turb} done ({time.time() - t0:.0f}s)")

    elapsed = time.time() - t0

    # ============ 聚合：mixed 口径 + common-768 口径增益对照 ============
    n_violations = 0   # TL-23 自检：SW 必须 ≥ per-seed per-block-oracle
    summary = {}
    for sc in PROBE_SCENES:
        snrs = [p['snr_db'] for p in raw[sc][0]]
        pts = []
        for j, snr in enumerate(snrs):
            nda = [raw[sc][i][j]['nda'] for i in range(n_seeds)]
            da_full = [raw[sc][i][j]['da_full'] for i in range(n_seeds)]
            da_data = [raw[sc][i][j]['da_data'] for i in range(n_seeds)]
            sw = [raw[sc][i][j]['sw'] for i in range(n_seeds)]
            oracle = [raw[sc][i][j]['oracle'] for i in range(n_seeds)]
            nda_c768 = [raw[sc][i][j]['nda_c768'] for i in range(n_seeds)]
            sw_c768 = [raw[sc][i][j]['sw_c768'] for i in range(n_seeds)]

            m_n, *_ = ci_t(nda)
            m_d_full, *_ = ci_t(da_full)
            m_d_data, *_ = ci_t(da_data)
            m_sw, s_sw, hw_sw, lo_sw, hi_sw = ci_t(sw)
            m_o, *_ = ci_t(oracle)
            m_n_c768, *_ = ci_t(nda_c768)
            m_sw_c768, s_sw_c768, hw_sw_c768, lo_sw_c768, hi_sw_c768 = ci_t(sw_c768)

            # mixed 口径增益（= switch_vs_nda_db_mean，应复现 2.3/2.0/1.3 附近）
            # 两者同除 1024，等价于 10log10(Σe_NDA / Σe_SW)
            gain_mixed = 10 * np.log10(m_n / m_sw) if m_sw > 0 and m_n > 0 else 0.0
            # common-768 口径增益（新）：NDA 和 selector 都除 (N_win×768)，公平同口径
            gain_c768 = 10 * np.log10(m_n_c768 / m_sw_c768) if m_sw_c768 > 0 and m_n_c768 > 0 else 0.0
            # SW vs per-block oracle（TL-23 守门：可实现上界）
            gain_oracle_vs_sw = 10 * np.log10(m_sw / m_o) if m_sw > 0 and m_o > 0 else 0.0
            # per-seed 增益（粗 CI，5seed 很宽）
            g_nda_seed = [10 * np.log10(n / s) if s > 0 and n > 0 else 0.0
                          for n, s in zip(nda, sw)]
            g_c768_seed = [10 * np.log10(n / s) if s > 0 and n > 0 else 0.0
                           for n, s in zip(nda_c768, sw_c768)]
            _, _, _, lo_m, hi_m = ci_t(g_nda_seed)
            _, _, _, lo_c, hi_c = ci_t(g_c768_seed)

            # raw 计数总和（跨 seed，供建议主控验证）
            sum_ne_nda_all1024 = int(sum(raw[sc][i][j]['raw_ne_nda_all1024'] for i in range(n_seeds)))
            sum_ne_sw_mixed = int(sum(raw[sc][i][j]['raw_ne_sw_mixed'] for i in range(n_seeds)))
            sum_ne_nda_c768 = int(sum(raw[sc][i][j]['raw_ne_nda_common768'] for i in range(n_seeds)))
            sum_ne_da = int(sum(raw[sc][i][j]['raw_ne_da'] for i in range(n_seeds)))
            sum_ne_sw_c768 = int(sum(raw[sc][i][j]['raw_ne_sw_common768'] for i in range(n_seeds)))

            pts.append({
                'snr_db': float(snr),
                # mixed 口径（现有）
                'mixed': {
                    'nda_ber_mean': m_n, 'sw_ber_mean': m_sw,
                    'gain_db': gain_mixed, 'gain_ci95': [lo_m, hi_m],
                },
                # common-768 口径（新）
                'common768': {
                    'nda_ber_mean': m_n_c768, 'sw_ber_mean': m_sw_c768,
                    'gain_db': gain_c768, 'gain_ci95': [lo_c, hi_c],
                },
                'da_ber_mean_full': m_d_full, 'da_ber_mean_data': m_d_data,
                'oracle_ber_mean': m_o,
                'switch_ber_ci95': [lo_sw, hi_sw],
                'oracle_vs_switch_db_mean': gain_oracle_vs_sw,
                # raw 计数（跨 seed 总和，供建议主控验证）
                'raw_counts': {
                    'ne_nda_all1024': sum_ne_nda_all1024,
                    'ne_sw_mixed': sum_ne_sw_mixed,
                    'ne_nda_common768': sum_ne_nda_c768,
                    'ne_da': sum_ne_da,
                    'ne_sw_common768': sum_ne_sw_c768,
                },
                'per_seed_mixed_gain_db': g_nda_seed,
                'per_seed_c768_gain_db': g_c768_seed,
            })
            # TL-23 自检：SW 是盲判据，不可能赢 per-block oracle
            for o_v, s_v in zip(oracle, sw):
                if o_v > 0 and s_v < o_v * (1 - 1e-9):
                    n_violations += 1
        summary[sc] = {'snr_db': snrs, 'points': pts}

    out = {
        'meta': {
            'task': 'A4 切换 common-768 公平口径探测', 'n_seeds': n_seeds,
            'scenes': PROBE_SCENES, 'snr_db': PROBE_SNR_DB,
            'n_points': len(PROBE_SCENES) * len(PROBE_SNR_DB),
            'gamma_eff_th': GAMMA_EFF_TH, 'cv_margin': CV_MARGIN,
            'cv_model': 'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
            'ci_method': f't-dist 95% df={n_seeds - 1}',
            'elapsed_sec': float(elapsed),
            'caliber_definition': {
                'mixed': 'selector 选 DA 窗累加 ne_da(768-pop)，选 NDA 窗累加 ne_nda(1024-pop)，'
                         'NDA/selector 都除 (N_win×1024)。等价于 branch-dependent error-count ratio，'
                         '不是公平 BER（R004 §3 病态退化：选 DA 窗机械白送最多 1.249 dB）。',
                'common768': 'selector 选 DA 窗累加 ne_da(768)，选 NDA 窗累加 ne_nda_common768(768)，'
                             'NDA/selector 都除 (N_win×768)。两边在同一 768-bit 冻结 population 上，公平同口径。',
                'common768_mask': f'192 非 pilot symbol (pilot at np.arange(0,256,4)) × {P.BITS_PER_SYM} bit = 768 bit/block',
                'note': 'DA 的 ne_da 本身就是 common-768（DA 只评 192 非 pilot 位）；'
                        '新增 ne_nda_common768 = NDA demod 在同一 192 非 pilot 位的错误数。'
                        'estimate/decide/demod 逻辑未改，只加位计数。',
            },
            'sanity_check': 'mixed gain 应复现现有 2.3(weak@10)/2.0(moderate@10)/1.3(strong@5) 附近；'
                            '若不复现说明改错了。',
            'selfcheck_min_violations': n_violations,
            'selfcheck_note': 'SW 是盲判据 → per-seed SW BER 必须 >= per-seed per-block-oracle。违例>0 = 还有 bug。',
            'awgn_note': 'AWGN 场景跳过（不在 9 点探测范围，省时间）；common-768 计数逻辑与湍流对称。',
        },
        'summary': summary,
    }
    out_json = os.path.join(OUT_DIR, '_a4_switch_common768_probe.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False,
                  default=lambda x: float(x) if isinstance(x, (np.floating,)) else x)
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"[TL-23 自检] SW < per-seed per-block-oracle 违例数 = {n_violations}（应为 0）")

    # ============ 打印对照表（核心交付）============
    print(f"\n{'='*92}")
    print(f"{'场景':<9}{'γd':>5}{'mixed gain':>12}{'[CI95]':>14}{'c768 gain':>12}{'[CI95]':>14}{'差值':>9}{'oracle-SW':>11}")
    print(f"{'-'*92}")
    for sc in PROBE_SCENES:
        for p in summary[sc]['points']:
            gm = p['mixed']['gain_db']; lo_m, hi_m = p['mixed']['gain_ci95']
            gc = p['common768']['gain_db']; lo_c, hi_c = p['common768']['gain_ci95']
            orc = p['oracle_vs_switch_db_mean']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{gm:>+10.3f}dB[{lo_m:+.1f},{hi_m:+.1f}]"
                  f"{gc:>+10.3f}dB[{lo_c:+.1f},{hi_c:+.1f}]{(gm - gc):>+8.3f}{orc:>+10.2f}")
    print(f"{'='*92}")

    # raw 计数（供建议主控验证）
    print(f"\n{'='*92}")
    print("raw 错误计数（跨 {0} seed 总和，每 seed 400 block）:".format(n_seeds))
    print(f"{'场景':<9}{'γd':>5}{'nda_1024':>10}{'sw_mixed':>10}{'nda_c768':>10}{'ne_da':>8}{'sw_c768':>9}")
    print(f"{'-'*92}")
    for sc in PROBE_SCENES:
        for p in summary[sc]['points']:
            r = p['raw_counts']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{r['ne_nda_all1024']:>10}{r['ne_sw_mixed']:>10}"
                  f"{r['ne_nda_common768']:>10}{r['ne_da']:>8}{r['ne_sw_common768']:>9}")
    print(f"{'='*92}")
    print(f"mixed 口径 BER 验算：gain_mixed = 10log10(nda_1024/sw_mixed)")
    print(f"common768 口径 BER 验算：gain_c768 = 10log10(nda_c768/sw_c768)")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=N_SEEDS_DEFAULT)
    a = ap.parse_args()
    main(n_seeds=a.seeds)
