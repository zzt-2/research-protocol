# -*- coding: utf-8 -*-
"""A4 切换策略 — bug 修复版（三 bug 修复 + 公平对照重算）.

**修复背景**：原 `_a4_switch_30seed.py` 被主线审查发现三个 bug（详见
`_a4_switch_bugfix_report.md`），切换增益 +0.27~+0.48dB 全部不可信：
  Bug 1 (混合分母): NDA BER 除以全块 bit (1024)，DA BER 除以 data bit (768)，
        SWITCH BER 两套分母混用 → 三者不在同一口径，对比不公平。
  Bug 2 (判据脱钩): decide() 用 raw 信号算 cv/h，候选用均衡后信号。
        → 判据与本节论断：raw 信号足够估 γ_eff（交叉驱动量，见 report §1.1），
          不是 bug 驱动源（脱钩只损 SWITCH 不帮 SWITCH）。判据改"均衡后"
          反而泄漏决策（接收端选估计器前不可能先均衡）。**保留 raw + 文档说明**。
  Bug 3 (oracle 对照): switch_vs_max = 10·log10(min(nda,da)/sw)，
        min(nda,da) = per-seed 事后选赢家 = oracle 理想策略，非真实 baseline。
        → 盲判据不可能赢 oracle，+0.27~0.48dB 是这个 bug 造成的假增益。

**修复方案**：
  1. 统一"全块 bit"口径：NDA/DA/SWITCH BER 全部除以 Ns·BITS_PER_SYM (1024)。
     DA 错误数仍在 data 位算（pilot 是已知插入符号，不算信息错误，对齐
     主实验 `ber_da_awgn` 的 `is_data` 约定）；但分母用全块 bit，与 NDA 对齐。
     — 理由：这是主实验 net-gain 框架的口径（DA vs NDA 按 BER 比，pilot
       能量代价在 net-gain 里单独扣 1.25dB，不在 per-bit BER 里扣）。
  2. decide() 保留 raw 信号 + 文档说明（Bug 2 不是假增益驱动源）。
  3. 删除 max(DA,NDA) 对照。改报两个真实 baseline：
       - switch_vs_DA   = 10·log10(ber_DA_mean / ber_SW_mean)
       - switch_vs_NDA  = 10·log10(ber_NDA_mean / ber_SW_mean)
     正=SWITCH BER 更低（SWITCH 赢）。

**自检（TL-23 守门）**：SWITCH 是盲判据，理论下界 = 逐 seed 逐 block 都选错
（不可能赢 min）。因此逐 seed 的 ber_SW 必须 ≥ ber_min_per_seed(nda,da)。
若修复后 SW 仍系统性 < per-seed min → 修复还有 bug，停下来查。

**守 TL-29**：换口径后先校准——DA 全块口径 BER 应 ≈ DA data 口径 BER × (768/1024)
× 修正（data 位错误率本就代表全块信息错误率，因 pilot 是已知符号），量级一致才可信。
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
GAMMA_EFF_TH = 13.0
CV_MARGIN = 1.10

# 全块 bit 分母（Bug 1 修复：所有方法统一用此口径）
FULL_BITS_PER_BLOCK = P.N_DFT * P.BITS_PER_SYM   # 256 × 4 = 1024


def cv_awgn_theory(snr_db):
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def decide(rx_seg, gamma_db, gamma_lin):
    """两层切换判据（保留 raw 信号，见 Bug 2 说明）.

    判据用 raw 信号统计 CV + 盲 h：接收端选估计器前不可能先均衡（均衡要 h，
    选估计器要判 h 大小 → 鸡生蛋），所以判据必须在 raw 上做。
    CV/盲 h 直接估 γ_eff，而 γ_eff 正是 crossover 驱动量（report §1.1）。
    候选路径均衡后信号用于"产 BER"，是另一件事——判据选哪条路 ≠ 判据信号
    要等于候选输出信号。raw 判据与候选结果脱钩只损 SWITCH（判错选错路），
    不帮 SWITCH，因此 Bug 2 不是假增益 +0.27-0.48dB 的驱动源。
    """
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'


def per_block(rx_blind, rx_pilot, bits, tx_sym):
    """湍流 per-block：返回 ne_nda, ne_da（错误数）.

    Bug 1 修复：DA 错误数仍在 data 位算（pilot 是已知符号不算信息错误，对齐
    主实验 ber_da_awgn is_data 约定）。错误数返回后，调用处同时用两种口径算 BER：
      - data 口径（gross）：err / (n_data_bits=768) — DA 标准信息 BER，主实验口径
      - full 口径（net）：err / FULL_BITS_PER_BLOCK=1024 — 与 NDA 同分母，可公平对比
    两口径关系：DA_full = DA_data × (768/1024) = DA_data − 1.249dB（= pilot overhead），
    所以 full 口径本质是"已扣 pilot power penalty 的 net BER"。NDA 两口径相同
    （NDA 无 pilot，全 1024 bit 都是信息位）。
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
    print(f"A4 切换 [FIXED] {n_seeds} seed (geth{GAMMA_EFF_TH}_cvmar{CV_MARGIN}) — 统一全块 bit 口径 + 真实 baseline 对照")

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
                e_o += min(ne_n, ne_d)   # per-block oracle 上界（每个 block 事后选更优）
                c = decide(seg, snr, gl)
                if c == 'da':
                    e_s += ne_d
                else:
                    e_s += ne_n
            # 两套口径：full（net，与 NDA 同分母，公平对比）+ data（gross，DA 标准信息 BER）
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
                    e_o += min(ne_n, ne_d)   # per-block oracle 上界
                    c = decide(rx_raw, gdb, gl)   # Bug 2：保留 raw（见 decide docstring）
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

    # ============ 聚合：真实 baseline 对照（Bug 3 修复，删除 oracle max） ============
    n_violations = 0   # TL-23 自检：SW < per-seed per-block-oracle 的违例数
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
            # 公平对照：SW（full 口径）vs DA_full（full 口径，net）— 两边同分母同口径
            gain_vs_da_net = 10 * np.log10(m_d_full / m_sw) if m_sw > 0 and m_d_full > 0 else 0.0
            # 公平对照：SW（full 口径）vs NDA（full 口径）— 两边同分母同口径
            gain_vs_nda = 10 * np.log10(m_n / m_sw) if m_sw > 0 and m_n > 0 else 0.0
            # 参考：SW vs DA_data（gross 口径）— DA 占 1.25dB 便宜（pilot 不算错误），
            # 这个增益会比 net 口径低 1.25dB，仅作透明参考不作结论
            gain_vs_da_gross = 10 * np.log10(m_d_data / m_sw) if m_sw > 0 and m_d_data > 0 else 0.0
            # SW vs per-block oracle（可实现上界，正=oracle 更好；负=SW 超 oracle=不可能=bug）
            gain_oracle_vs_sw = 10 * np.log10(m_sw / m_o) if m_sw > 0 and m_o > 0 else 0.0
            # per-seed 增益（用于 CI），用 fair 的 net 口径
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
                # 公平对照（修复 Bug 3）——net 口径
                'switch_vs_da_net_db_mean': gain_vs_da_net,
                'switch_vs_da_net_db_ci95': [lo_gda, hi_gda],
                'switch_vs_nda_db_mean': gain_vs_nda,
                'switch_vs_nda_db_ci95': [lo_gnda, hi_gnda],
                # SW vs per-block oracle（TL-23 守门：可实现上界）
                'oracle_vs_switch_db_mean': gain_oracle_vs_sw,
                # 透明参考：gross 口径（DA 占便宜 1.25dB）
                'switch_vs_da_gross_db_mean': gain_vs_da_gross,
                'per_seed_switch_vs_da_db': g_da_seed,
                'per_seed_switch_vs_nda_db': g_nda_seed,
            })
            # TL-23 自检（正确边界）：SW 必须 ≥ per-seed per-block-oracle。
            # per-block oracle = 每块事后选 min(ne_n,ne_d) = 任何选择器的可实现上界。
            # SW 是盲判据，不可能赢 oracle。SW < oracle = 修复还有 bug。
            for o_v, s_v in zip(oracle, sw):
                if o_v > 0 and s_v < o_v * (1 - 1e-9):
                    n_violations += 1
        summary[sc] = {'snr_db': snrs, 'points': pts}

    out = {
        'meta': {
            'task': 'A4 切换 30 seed [BUGFIX]', 'n_seeds': n_seeds,
            'gamma_eff_th': GAMMA_EFF_TH, 'cv_margin': CV_MARGIN,
            'cv_model': 'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
            'ci_method': f't-dist 95% df={n_seeds - 1}',
            'elapsed_sec': float(elapsed),
            'bugs_fixed': {
                'bug1_mixed_denominator': '统一全块 bit (Ns*BITS_PER_SYM=1024) 口径，DA 错误数仍在 data 位算但分母用全块',
                'bug2_decide_decoupled': '保留 raw（脱钩只损 SWITCH 不帮 SWITCH，非假增益驱动源）；decide docstring 文档说明',
                'bug3_oracle_baseline': '删除 max(DA,NDA)，改报 switch_vs_DA / switch_vs_NDA 两个真实 baseline',
            },
            'ber_convention': (
                'NDA/DA_full/SW all on full-block bits (1024) — same denominator, fair compare. '
                'DA_data = DA errors / data bits (768) = standard info-BER (main-experiment gross). '
                'gain_vs_da_net uses DA_full (overhead-discounted); gain_vs_da_gross uses DA_data for reference. '
                'NDA has no pilot so full==data for NDA.'
            ),
            'selfcheck_min_violations': n_violations,
            'selfcheck_note': 'SW is a blind selector → per-seed SW BER must be >= per-seed per-block-oracle (=Σ_b min(ne_n_b,ne_d_b)/bits). Violations>0 means fix is still buggy. SW MAY beat frame-level min(NDA,DA) — that is the legitimate per-block selection gain, not a bug.',
        },
        'summary': summary,
    }
    suffix = '30seed' if n_seeds >= 30 else f'{n_seeds}seed'
    out_json = os.path.join(OUT_DIR, f'_a4_switch_{suffix}_fixed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False,
                  default=lambda x: float(x) if isinstance(x, (np.floating,)) else x)
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"[TL-23 自检] SW < per-seed per-block-oracle 违例数 = {n_violations}（应为 0；SW 可赢 frame-level min，那是合法 per-block 收益）")
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
