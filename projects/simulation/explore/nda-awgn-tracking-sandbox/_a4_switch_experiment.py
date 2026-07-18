# -*- coding: utf-8 -*-
"""A4 条件适配实验：DA/NDA 基于 per-block 有效 SNR 切换策略.

目标（adaptation-scan.md A4）：验证"DA/NDA 切换策略 > 始终 DA / 始终 NDA"
切换判据：per-block 有效 SNR γ_eff_est = γ_bar + 10log10(ĥ_blind)
  - γ_eff_est < 阈值 → 用 DA（低有效 SNR，pilot 显式参考可靠）
  - γ_eff_est ≥ 阈值 → 用 NDA（高有效 SNR，全 block 积分鲁棒 + 省过 pilot 能量）

判据可实现性：ĥ_blind = mean(|rx|²) − 1/(2γ)，接收端可测（estimate_h_blind_perblock 已有）
  不用 oracle 真 h（FR-26 证据链：common/_channel.py h 是真实信道，接收端不可知）。

baseline 结构（adaptation-scan.md §baseline 结构规则）：
  - 我们的方法 = 切换策略（per-block 自适应 DA/NDA）
  - 主 baseline = 始终 DA / 始终 NDA（取最强）
  - 参照 = VV / BPS / DPLL（主实验已有，不重跑）
  - 上界 = oracle（主实验已有）

TL-20 理论预期（详见报告）：
  1. 切换策略 ≈ max(DA, NDA) 全 SNR（取两者之长）— 这是下界（最保守）
  2. 切换策略可能 > max(DA, NDA) 在 crossover 区（per-block 选择比 per-SNR 选择更精细）
  3. 切换策略不应在任何 SNR 弱于 max(DA, NDA)（否则切换有损 = FAIL）

输出：_a4_switch_results.json + _a4_switch_report.md
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

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))

# 切换阈值（诊断 2：crossover 在 γ_eff 12-14 dB）
# 用 13 dB 作主阈值
GAMMA_EFF_TH_DB = 13.0

# 块内 CV 门控阈值（诊断 3/5：AWGN CV≈0.75, 湍流 CV≈1.0+）
# CV = std(|rx|²)/mean(|rx|²), per-block 可测
# CV < CV_TH → 无衰落（h 块内近似恒定）→ NDA（省 pilot overhead 永远对）
# CV ≥ CV_TH → 有衰落 → 按 γ_eff 切换 DA/NDA
CV_TH = 0.85


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    if n > 1:
        hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n)
    else:
        hw = 0.0
    return mean, std, hw, mean - hw, mean + hw


# =============================================================================
# per-block: 同时算 NDA + DA，返回各自 err/bits + 可测 γ_eff
# =============================================================================
def per_block_nda_da(rx_blind, rx_pilot, bits, tx_sym):
    """单 block 内分别跑 NDA 和 DA，返回 (ne_nda, nb_nda, ne_da, nb_da).

    NDA BER 算全部符号；DA BER 只算 data 符号（pilot 不算），与主实验公平对照一致。
    """
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
    # BER
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    resolved_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda = int(np.sum(tb != m16apsk_demod(resolved_nda)))
    nb_nda = P.N_DFT * P.BITS_PER_SYM
    # DA: only data symbols
    demod_da = m16apsk_demod(rc_da)
    is_data = np.ones(P.N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    tb_arr = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dm_arr = demod_da.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
    nb_da = int(np.sum(is_data) * P.BITS_PER_SYM)
    return ne_nda, nb_nda, ne_da, nb_da


def decide_switch(rx_raw_seg, gamma_db, gamma_lin, gamma_eff_th_db):
    """两层切换判据（全接收端可测，非 oracle）.

    返回 'nda' 或 'da'.

    第 1 层 CV 门控：CV = std(|rx|²)/mean(|rx|²)
      - CV < CV_TH → 无衰落（h 块内近似恒定）→ NDA（省 pilot overhead 永远对）
      - CV ≥ CV_TH → 有衰落 → 进第 2 层
    第 2 层 γ_eff 门控：γ_eff_est = γ_bar + 10log10(ĥ_blind)
      - γ_eff < th → DA（低有效 SNR，pilot 显式参考可靠）
      - γ_eff ≥ th → NDA（高有效 SNR，全 block 积分鲁棒 + 省 pilot 能量）
    """
    pwr = np.abs(rx_raw_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < CV_TH:
        return 'nda'  # 无衰落
    # 有衰落：用盲 h 估计判 γ_eff
    h_est_blk = float(np.mean(pwr) - 1.0 / (2 * gamma_lin))
    h_est_blk = max(h_est_blk, 1e-6)
    gamma_eff_est_db = gamma_db + 10 * np.log10(h_est_blk)
    return 'da' if gamma_eff_est_db < gamma_eff_th_db else 'nda'


def run_turb_switch(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0,
                    gamma_eff_th_db=GAMMA_EFF_TH_DB, lw=None):
    """湍流场景：切换策略 vs 始终DA vs 始终NDA BER 扫描.

    每 block 同时算 NDA 和 DA 两路 BER，再按两层判据（CV 门控 + γ_eff 门控）选一路计入切换策略。
    始终DA = 所有 block 累加 DA err/bits；始终NDA = 累加 NDA err/bits。
    切换 = 按判据选 NDA 或 DA 的 err/bits 累加。
    """
    Ns = P.N_DFT
    print(f"\n[{turb_name} γ_eff_th={gamma_eff_th_db}dB CV_th={CV_TH}] N={n_blocks*Ns}/点, "
          f"per-block h 均衡 + amp_limit(3.0), NDA 两阶段 fft_foe+nda CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'SWITCH':>12} "
          f"{'%NDA':>6} {'max(DA,NDA)':>12} {'SW-max':>10}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        e_nda = e_da = e_sw = 0
        b_nda = b_da = b_sw = 0
        n_nda_chosen = 0  # 切换策略选 NDA 的 block 数
        n_da_chosen = 0
        for blk in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + blk, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            tx_sym = r['tx']
            # 盲 h 估计（接收端可测，非 oracle）
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            # per-block BER 两路
            ne_nda, nb_nda, ne_da, nb_da = per_block_nda_da(
                rx_blind, rx_pilot, bits, tx_sym)
            # 累加 始终NDA / 始终DA
            e_nda += ne_nda; b_nda += nb_nda
            e_da += ne_da; b_da += nb_da
            # 两层切换判据
            choice = decide_switch(rx_raw, gamma_db, gamma_lin, gamma_eff_th_db)
            if choice == 'da':
                e_sw += ne_da; b_sw += nb_da
                n_da_chosen += 1
            else:
                e_sw += ne_nda; b_sw += nb_nda
                n_nda_chosen += 1
        ber_nda = e_nda / b_nda
        ber_da = e_da / b_da
        ber_sw = e_sw / b_sw
        ber_max = min(ber_nda, ber_da)  # max(DA,NDA) = 取 BER 低者（事后最优）
        pct_nda = 100.0 * n_nda_chosen / (n_nda_chosen + n_da_chosen)
        sw_vs_max = 10 * np.log10(ber_max / ber_sw) if ber_sw > 0 and ber_max > 0 else 0
        print(f"{gamma_db:>7.0f} {ber_nda:>12.4e} {ber_da:>12.4e} {ber_sw:>12.4e} "
              f"{pct_nda:>5.0f}% {ber_max:>12.4e} {sw_vs_max:>+9.2f}dB")
        per_snr.append({
            'snr_db': float(gamma_db),
            'nda_ml_ber': ber_nda, 'da_ml_ber': ber_da,
            'switch_ber': ber_sw,
            'pct_nda_chosen': pct_nda,
            'n_nda_chosen': n_nda_chosen, 'n_da_chosen': n_da_chosen,
            'max_nda_da_ber': ber_max,
            'switch_vs_max_db': float(sw_vs_max),
        })
    return per_snr


def run_awgn_switch(n_blocks, snr_points, seed_base, sigma2_p=None,
                    gamma_eff_th_db=GAMMA_EFF_TH_DB):
    """AWGN 场景切换策略. AWGN 无湍流 (h≡1), 块内 CV≈0.75<CV_TH → 全判无衰落→NDA.

    预期：CV 门控让 AWGN 全选 NDA ≈ NDA（AWGN 全 SNR NDA 全赢，切换在 AWGN 无增益空间，
    这是预期 — 验证切换不会在 AWGN 添乱）。
    """
    N_sym = n_blocks * P.N_DFT
    if sigma2_p is None:
        sigma2_p = P.SIGMA2_P
    print(f"\n[AWGN γ_eff_th={gamma_eff_th_db}dB CV_th={CV_TH}] N_sym={N_sym}/点")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'SWITCH':>12} "
          f"{'%NDA':>6} {'max(DA,NDA)':>12} {'SW-max':>10}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = S.awgn_wiener_channel(tx, snr, seed, sigma2_p=sigma2_p)
        # AWGN 逐块处理（与主实验 ber_nda_awgn/ber_da_awgn 一致）
        n_blk = N_sym // P.N_DFT
        e_nda = e_da = e_sw = 0
        b_nda = b_da = b_sw = 0
        n_nda_chosen = 0
        n_da_chosen = 0
        tx_sym = tx
        gamma_lin = 10 ** (snr / 10)
        for b in range(n_blk):
            seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
            tb_seg = bits[b * P.N_DFT * P.BITS_PER_SYM:(b + 1) * P.N_DFT * P.BITS_PER_SYM]
            # NDA
            rc_nda, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk',
                                              assume_df_zero=True,
                                              intra_block_tracking='segmented')
            resolved_nda = resolve_m16apsk_blockwise(rc_nda, tb_seg,
                                                     block_size=P.BLOCK_SIZE_RESOLVE)
            ne_nda = int(np.sum(tb_seg != m16apsk_demod(resolved_nda)))
            nb_nda = P.N_DFT * P.BITS_PER_SYM
            # DA
            pilot_idx_local = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
            p_sym = tx_sym[b * P.N_DFT + pilot_idx_local]
            rc_da, _, _ = da_ml_recovery(seg, pilot_idx=pilot_idx_local,
                                         pilot_sym=p_sym, mod='m16apsk')
            demod_da = m16apsk_demod(rc_da)
            is_data = np.ones(P.N_DFT, dtype=bool)
            is_data[pilot_idx_local] = False
            tb_arr = tb_seg.reshape(P.N_DFT, P.BITS_PER_SYM)
            dm_arr = demod_da.reshape(P.N_DFT, P.BITS_PER_SYM)
            ne_da = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
            nb_da = int(np.sum(is_data) * P.BITS_PER_SYM)
            e_nda += ne_nda; b_nda += nb_nda
            e_da += ne_da; b_da += nb_da
            # 两层切换判据（AWGN CV≈0.75<0.85 → 全判无衰落 → 全选 NDA）
            choice = decide_switch(seg, snr, gamma_lin, gamma_eff_th_db)
            if choice == 'da':
                e_sw += ne_da; b_sw += nb_da
                n_da_chosen += 1
            else:
                e_sw += ne_nda; b_sw += nb_nda
                n_nda_chosen += 1
        ber_nda = e_nda / b_nda
        ber_da = e_da / b_da
        ber_sw = e_sw / b_sw
        ber_max = min(ber_nda, ber_da)
        pct_nda = 100.0 * n_nda_chosen / (n_nda_chosen + n_da_chosen)
        sw_vs_max = 10 * np.log10(ber_max / ber_sw) if ber_sw > 0 and ber_max > 0 else 0
        print(f"{snr:>7.0f} {ber_nda:>12.4e} {ber_da:>12.4e} {ber_sw:>12.4e} "
              f"{pct_nda:>5.0f}% {ber_max:>12.4e} {sw_vs_max:>+9.2f}dB")
        per_snr.append({
            'snr_db': float(snr),
            'nda_ml_ber': ber_nda, 'da_ml_ber': ber_da,
            'switch_ber': ber_sw,
            'pct_nda_chosen': pct_nda,
            'n_nda_chosen': n_nda_chosen, 'n_da_chosen': n_da_chosen,
            'max_nda_da_ber': ber_max,
            'switch_vs_max_db': float(sw_vs_max),
        })
    return per_snr


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
    cfg = SimulationConfig()
    t0 = time.time()
    SCENES = ['awgn', 'weak', 'moderate', 'strong']

    print("=" * 110)
    print(f"A4 条件适配: DA/NDA 切换策略 (γ_eff_th={GAMMA_EFF_TH_DB}dB) vs 始终DA vs 始终NDA")
    print(f"5 seed × 4 场景, 判据=per-block γ_eff_est=γ_bar+10log10(ĥ_blind) [接收端可测]")
    print("=" * 110)

    raw = {sc: {} for sc in SCENES}
    # AWGN
    for i in range(N_SEEDS):
        sb = P.SEED_AWGN + i
        print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
        raw['awgn'][i] = run_awgn_switch(P.N_BLOCKS, P.SNR_AWGN_DB, sb)
    # 湍流
    for turb in P.TURB_LEVELS:
        for i in range(N_SEEDS):
            s0 = P.SEED_TURB0 + i * P.N_BLOCKS
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = run_turb_switch(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)

    elapsed = time.time() - t0

    # 聚合 5 seed
    summary = {}
    for sc in SCENES:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        points = []
        for j, snr in enumerate(snrs):
            nda = [per_seed[i][j]['nda_ml_ber'] for i in range(N_SEEDS)]
            da = [per_seed[i][j]['da_ml_ber'] for i in range(N_SEEDS)]
            sw = [per_seed[i][j]['switch_ber'] for i in range(N_SEEDS)]
            mx = [per_seed[i][j]['max_nda_da_ber'] for i in range(N_SEEDS)]
            swvmax = [per_seed[i][j]['switch_vs_max_db'] for i in range(N_SEEDS)]
            pct = [per_seed[i][j]['pct_nda_chosen'] for i in range(N_SEEDS)]
            m_nda, *_ = ci_t(nda)
            m_da, *_ = ci_t(da)
            m_sw, s_sw, hw_sw, lo_sw, hi_sw = ci_t(sw)
            m_mx, *_ = ci_t(mx)
            m_swvmax, s_swvmax, hw_swvmax, lo_sv, hi_sv = ci_t(swvmax)
            m_pct, *_ = ci_t(pct)
            points.append({
                'snr_db': float(snr),
                'per_seed': {
                    'nda_ml_ber': nda, 'da_ml_ber': da,
                    'switch_ber': sw, 'max_nda_da_ber': mx,
                    'switch_vs_max_db': swvmax,
                },
                'nda_ml_ber_mean': m_nda, 'da_ml_ber_mean': m_da,
                'switch_ber_mean': m_sw, 'switch_ber_ci95': [lo_sw, hi_sw],
                'max_nda_da_ber_mean': m_mx,
                'switch_vs_max_db_mean': m_swvmax,
                'switch_vs_max_db_ci95': [lo_sv, hi_sv],
                'pct_nda_chosen_mean': m_pct,
            })
        summary[sc] = {'snr_db': snrs, 'points': points}

    # 落盘
    out = {
        'meta': {
            'task': 'A4 条件适配: DA/NDA 切换策略',
            'adaptation_type': 'A4 (条件适配, per-block 有效 SNR 切换)',
            'criterion': '两层门控 (全接收端可测, 非 oracle): '
                         '(L1) 块内 CV=std(|rx|²)/mean(|rx|²) < CV_TH → 无衰落 → NDA; '
                         '(L2) CV≥CV_TH → 按 γ_eff_est=γ_bar+10log10(ĥ_blind) 切换, <th→DA, ≥th→NDA',
            'cv_threshold': CV_TH,
            'cv_source': '诊断 3/5: AWGN CV≈0.75, 湍流 CV≈1.0+, CV_TH=0.85 区分有无衰落',
            'gamma_eff_threshold_db': GAMMA_EFF_TH_DB,
            'gamma_eff_threshold_source': '诊断 2: crossover 汇聚在 γ_eff 12-14 dB',
            'rule': '(L1) CV<0.85→无衰落→NDA; (L2) CV≥0.85: γ_eff<13→DA(低有效SNR pilot可靠), γ_eff≥13→NDA(高有效SNR积分鲁棒)',
            'fairness': '判据用盲 h 估计 (DA/NDA 都能算, 不偏袒). DA BER 只算 data 符号 (pilot 不算), 与主实验公平对照一致',
            'no_oracle': '不用真 h (common/_channel.py h 是真实信道接收端不可知); 不用真 φ',
            'baseline_structure': {
                'our_method': 'per-block DA/NDA 切换策略',
                'main_baseline': '始终 DA / 始终 NDA (取最强 max(DA,NDA))',
                'reference': 'VV / BPS / DPLL (主实验已有)',
                'upper_bound': 'oracle (主实验已有)',
            },
            'n_seeds': N_SEEDS,
            'scenes': SCENES,
            'ci_method': f't-distribution 95% CI df=4 t={T05_4:.4f}',
            'elapsed_sec': float(elapsed),
            'python': sys.executable,
            'numpy_version': np.__version__,
        },
        'summary': to_jsonable(summary),
    }
    out_json = os.path.join(OUT_DIR, '_a4_switch_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {elapsed:.1f}s")

    # 控制台汇总
    print("\n" + "=" * 110)
    print(f"{'场景':>10} {'γd_dB':>7} {'NDA':>11} {'DA':>11} {'SWITCH':>11} "
          f"{'max(D,N)':>11} {'SW-max':>9} {'%NDA':>6}  PASS?")
    print("-" * 110)
    for sc in SCENES:
        for p in summary[sc]['points']:
            sv = p['switch_vs_max_db_mean']
            svci = p['switch_vs_max_db_ci95']
            # PASS 判据：切换不弱于 max(DA,NDA) → switch_vs_max >= 0 (CI 下界 >= 微小负容差)
            pass_flag = '✓' if svci[0] >= -0.05 else '✗'
            print(f"{sc:>10} {p['snr_db']:>7.0f} {p['nda_ml_ber_mean']:>11.3e} "
                  f"{p['da_ml_ber_mean']:>11.3e} {p['switch_ber_mean']:>11.3e} "
                  f"{p['max_nda_da_ber_mean']:>11.3e} {sv:>+8.2f}dB "
                  f"{p['pct_nda_chosen_mean']:>5.0f}%  {pass_flag}")


if __name__ == '__main__':
    main()
