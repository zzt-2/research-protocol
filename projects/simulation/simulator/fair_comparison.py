# -*- coding: utf-8 -*-
"""公平对照框架 (γ_tot 坐标) — Formal 正式仿真器独立实现.

公平对照坐标 = 总能量 SNR γ_tot:
  NDA-ML: γ_tot = γ_d (0% pilot overhead)
  DA-ML:  γ_tot = γ_d + PILOT_OVERHEAD_DB (25% overhead, DA 须多发 1/spacing pilot)

物理依据 (MVE-SPEC §4 + _time_domain_crlb.py CRLB 推导):
  相同信息吞吐量 R_info 下, DA-ML 须多发 1/spacing 比例 pilot → 总能量多
  10·log10(spacing/(spacing-1)). spacing=4: 1.249 dB.

BER 曲线仍按数据有效 SNR γ_d 跑 (两方案同信道同符号率公平);
gain@HD-FEC 报告时 DA 的 γ_d + 1.249 dB = 等效总能量 γ_tot.

公式 (design.md §3.4 + _time_domain_crlb.py:36-44):
  γ_d (data SNR) → BER 跑此
  γ_tot_nda = γ_d
  γ_tot_da  = γ_d + PILOT_OVERHEAD_DB
  fair_gain@target_BER = (γ_tot_da @ target) - (γ_tot_nda @ target)   正 = NDA 赢

可独立于 explore/ (此处是 Formal 实现, 公式同 MVE-SPEC §4 但代码独立写).
"""
import numpy as np

from _b11_params import PILOT_OVERHEAD_DB, DA_PILOT_SPACING


def da_total_snr_db(gamma_d_db):
    """DA 总能量 SNR γ_tot = γ_d + pilot overhead (1.249 dB @ spacing=4).

    Parameters
    ----------
    gamma_d_db : float or array
        DA 数据有效 SNR (dB), BER 曲线跑此 SNR.
    Returns
    -------
    gamma_tot_db : 同型, DA 等效总能量 SNR (含 pilot 能量代价).
    """
    return np.asarray(gamma_d_db, dtype=float) + PILOT_OVERHEAD_DB


def nda_total_snr_db(gamma_d_db):
    """NDA 总能量 SNR γ_tot = γ_d (0% overhead, 无 pilot)."""
    return np.asarray(gamma_d_db, dtype=float)


def snr_at_ber(snr_list, ber_list, ber_target):
    """线性插值 (SNR 轴, log BER) 找 ber_target 处 SNR. 返回 None 若不可达.

    单调降假设: SNR 升 BER 降. 同 MVE `_time_domain_crlb.py:snr_at_ber` 公式, 独立写.
    """
    snr_list = np.asarray(snr_list, dtype=float)
    ber_list = np.asarray(ber_list, dtype=float)
    order = np.argsort(snr_list)
    snr_list, ber_list = snr_list[order], ber_list[order]
    for i in range(len(snr_list) - 1):
        b_hi = ber_list[i]
        b_lo = ber_list[i + 1]
        if b_hi >= ber_target >= b_lo and b_hi > b_lo:
            t = (np.log(b_hi) - np.log(ber_target)) / (np.log(b_hi) - np.log(b_lo))
            return float(snr_list[i] + t * (snr_list[i + 1] - snr_list[i]))
    return None


def equiv_snr_gap(snr_list, ber_ref, ber_test):
    """等效 SNR gap: test 曲线达 ref 曲线在 ref_snr 处 BER 所需额外 SNR.

    gap>0 = test 劣 (需更高 SNR). 返回 list of (ref_snr, test_snr, gap).
    """
    out = []
    snr_list = np.asarray(snr_list, dtype=float)
    ber_ref = np.asarray(ber_ref, dtype=float)
    ber_test = np.asarray(ber_test, dtype=float)
    order = np.argsort(snr_list)
    snr_list, ber_ref, ber_test = snr_list[order], ber_ref[order], ber_test[order]
    for i, sref in enumerate(snr_list):
        bref = ber_ref[i]
        stest = snr_at_ber(snr_list, ber_test, bref)
        if stest is not None:
            out.append((float(sref), float(stest), float(stest - sref)))
    return out


def analyze_fair_gain(per_snr, hdfec, pilot_overhead_db=PILOT_OVERHEAD_DB):
    """公平 gain@HD-FEC 分析 (γ_tot 坐标, 主判据).

    输入 per_snr: list of dict, 含 'snr_db' (γ_d), 'nda_ml_ber', 'da_ml_ber', 'oracle_ber'.

    公平 gain 定义 (design.md §3.4):
      gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC)
                  = (γ_d_da@HD-FEC + overhead) − γ_d_nda@HD-FEC
      正 = NDA 赢 (DA 需更高总能量才达 HD-FEC).

    若 HD-FEC 不可达 (BER floor), 用可达 BER 水平的等效总能量差 (取 NDA 最低 BER 为 target).

    与 MVE `_time_domain_crlb.py:analyze_fair_gain` 公式一致, 独立写.
    """
    snrs_d = np.array([p['snr_db'] for p in per_snr])           # 数据有效 SNR
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])

    s_nda_d = snr_at_ber(snrs_d, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs_d, b_da, hdfec)
    s_or_d = snr_at_ber(snrs_d, b_or, hdfec)
    gain_hdfec = None
    hdfec_reachable = False
    if s_nda_d is not None and s_da_d is not None:
        gain_hdfec = (s_da_d + pilot_overhead_db) - s_nda_d
        hdfec_reachable = True

    # 可达 BER 水平的等效 SNR 差 (HD-FEC 不可达时用)
    min_nda_ber = float(np.min(b_nda))
    s_nda_min = snr_at_ber(snrs_d, b_nda, min_nda_ber)
    s_da_at_nda_min = snr_at_ber(snrs_d, b_da, min_nda_ber)
    equiv_gain_achievable = None
    if s_nda_min is not None and s_da_at_nda_min is not None:
        equiv_gain_achievable = (s_da_at_nda_min + pilot_overhead_db) - s_nda_min

    # 逐 SNR 公平比较 (总能量 γ_tot 坐标): 在总能量 γ_tot 下 NDA 跑 γ_d=γ_tot,
    # DA 跑 γ_d=γ_tot−overhead. 公平 gain @ 每工作点 = DA 达 NDA(γ_tot) BER 所需总能量 − γ_tot.
    per_point_fair = []
    for i, gtot in enumerate(snrs_d):   # NDA γ_tot = γ_d
        ber_nda_at_gtot = b_nda[i]
        s_da_d_needed = snr_at_ber(snrs_d, b_da, ber_nda_at_gtot)
        if s_da_d_needed is not None:
            fair_gain = (s_da_d_needed + pilot_overhead_db) - float(gtot)
            per_point_fair.append({
                'gamma_tot_db': float(gtot),
                'ber_nda': float(ber_nda_at_gtot),
                'snr_da_d_needed_db': float(s_da_d_needed),
                'fair_gain_db': float(fair_gain),   # 正 = NDA 赢
            })
    fair_gain_high_snr = per_point_fair[-1]['fair_gain_db'] if per_point_fair else None
    fair_gain_mean = (float(np.mean([p['fair_gain_db'] for p in per_point_fair]))
                      if per_point_fair else None)

    # NDA vs oracle gap (NDA 离信息论极限多远; oracle 相位完美无 overhead 调整)
    gap_nda_vs_oracle = equiv_snr_gap(snrs_d, b_or, b_nda)
    gap_or_mean = (float(np.mean([g[2] for g in gap_nda_vs_oracle]))
                   if gap_nda_vs_oracle else None)

    return {
        'snr_nda_tot_at_hdfec': s_nda_d,
        'snr_da_tot_at_hdfec': (s_da_d + pilot_overhead_db) if s_da_d is not None else None,
        'snr_oracle_at_hdfec': s_or_d,
        'gain_nda_vs_da_fair_db': gain_hdfec,
        'gain_nda_vs_da_naive_db': ((s_da_d - s_nda_d) if (s_da_d is not None and s_nda_d is not None) else None),
        'hdfec_reachable': hdfec_reachable,
        'equiv_gain_at_achievable_db': equiv_gain_achievable,
        'per_point_fair_gain': per_point_fair,
        'fair_gain_high_snr_db': fair_gain_high_snr,
        'fair_gain_mean_db': fair_gain_mean,
        'min_nda_ber': min_nda_ber,
        'gap_nda_vs_oracle_mean_db': gap_or_mean,
        'pilot_overhead_db': float(pilot_overhead_db),
    }
