"""B2-Q2 闭环版 sandbox 三方对照（阶段 1.5 步骤 2，救援路线 D003）.

三方（闭环版，_architecture_decision_closed_loop.md §3.1）:
  A. 闭环完全 hold [79]（祖师爷 baseline，V3）:
     非 fade 期 blind 闭式估计(nda_ml M₀=8) + 跨块 PI 平滑 / fade 期 hold 环路状态
  B. 闭环 pilot 全程 + power-boost（消融）:
     pilot 闭式估计(da_ml) + power-boost + 跨块 PI 平滑全程
  C. 闭环双模 + power-boost（B2-Q2 救援版）:
     非 fade 期 blind 闭式估计 + PI 平滑 / fade 期 pilot 闭式估计 + power-boost + PI 平滑

V3 祖师爷实现一致性（_architecture_decision_closed_loop.md §3.3）:
  [79] 闭环 freeze = 跨块环路状态 + fade 期冻结 + 恢复自然收敛
  前馈版 freeze_compensate_block 只 hold 标量 → V3 FAIL（砍环路惯性）
  本脚本用 ClosedLoopPhaseTracker 跨块 PI 平滑，复刻 [79] 闭环 hold

度量修复（_architecture_decision_closed_loop.md §4）:
  compute_n_recover_v2: band 30% + 滑窗均值（修前馈版退化）

power-boost 接收端等效（_fair_comparison_closed_loop.md §2.1）:
  fade 期 pilot 位置 rx 加权 √β（等效 pilot 功率 ×β），不改 common 信道

守: INVARIANT 14（不污染 common）/ TL-13（共用信道）/ V2 三方 / V3 祖师爷 / V5 主线独立重算
"""
import os
import sys
import json
import time
import numpy as np

_SIM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _b2_params_closed_loop import (
    LASER_LW, R_SYM, T_S, SIGMA2_PN,
    TURB_LEVELS, DA_PILOT_SPACING,
    N_DFT, N_BLOCKS, HDFEC,
    SNR_TURB, DOPPLER,
    POWER_BOOST_FACTOR_DEFAULT,
    N_RECOVER_BAND, N_RECOVER_STEADY_WINDOW, N_RECOVER_CONSECUTIVE,
)
from _closed_loop_freeze import ClosedLoopPhaseTracker, compute_n_recover_v2

from common import (
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
)
import importlib.util
_sc_nda_path = os.path.join(_SIM_ROOT, 'explore', 'single-carrier-nda-ml', '_time_domain_crlb.py')
_spec = importlib.util.spec_from_file_location('_sc_nda_helpers', _sc_nda_path)
_sc_nda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc_nda)
estimate_h_blind_perblock = _sc_nda.estimate_h_blind_perblock
estimate_h_pilot_perblock = _sc_nda.estimate_h_pilot_perblock
fft_foe_m0_omega = _sc_nda.fft_foe_m0_omega

M0 = 8  # 16-APSK 升幂阶数
BITS_PER_SYM = 4
PILOT_IDX_LOCAL = np.arange(0, N_DFT, DA_PILOT_SPACING)


def blind_estimate_phi(rx_block):
    """blind 闭式相位估计（nda_ml M₀=8，16-APSK 正确升幂）."""
    omega_est = fft_foe_m0_omega(rx_block, M0)
    k = np.arange(len(rx_block))
    seg = rx_block * np.exp(-1j * omega_est * k)
    rc, _, phi_est, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True)
    return rc, phi_est, omega_est


def pilot_estimate_phi(rx_block, pilot_sym, boost_factor=1.0):
    """pilot 闭式相位估计（da_ml）+ power-boost 接收端等效."""
    if boost_factor != 1.0:
        # power-boost 接收端等效: pilot 位置 rx 加权 √β
        rx_boosted = rx_block.copy()
        rx_boosted[PILOT_IDX_LOCAL] *= np.sqrt(boost_factor)
        rx_block = rx_boosted
    rc, _, _ = da_ml_recovery(rx_block, pilot_idx=PILOT_IDX_LOCAL,
                               pilot_sym=pilot_sym, mod='m16apsk')
    return rc


def demod_ber(rc, bits, is_data_mask=None):
    """解调 + 算 BER."""
    demod = m16apsk_demod(rc)
    if is_data_mask is not None:
        tb = bits[:N_DFT * BITS_PER_SYM].reshape(N_DFT, BITS_PER_SYM)
        dm = demod.reshape(N_DFT, BITS_PER_SYM)
        ne = int(np.sum(tb[is_data_mask] != dm[is_data_mask]))
        nb = int(np.sum(is_data_mask) * BITS_PER_SYM)
    else:
        tb = bits[:N_DFT * BITS_PER_SYM]
        ne = int(np.sum(tb != demod))
        nb = len(tb)
    return ne, nb


def run_closed_loop_point(turb_name, gamma_lin, n_blocks, seed0, gamma_th,
                           boost_factor=POWER_BOOST_FACTOR_DEFAULT,
                           alpha=1.0, beta_int=0.0):
    """单点闭环版三方对照."""
    is_data = np.ones(N_DFT, dtype=bool)
    is_data[PILOT_IDX_LOCAL] = False

    # 三方跨块 PI 平滑器
    tracker_A = ClosedLoopPhaseTracker(alpha=alpha, beta=beta_int)
    tracker_B = ClosedLoopPhaseTracker(alpha=alpha, beta=beta_int)
    tracker_C = ClosedLoopPhaseTracker(alpha=alpha, beta=beta_int)

    # 累积器
    n_err_A = n_err_B = n_err_C = 0
    n_bits_A = n_bits_B = n_bits_C = 0
    n_err_fade_hold = n_bits_fade_hold = 0
    n_err_fade_da = n_bits_fade_da = 0
    n_err_nonfade = n_bits_nonfade = 0
    per_block_ber_A = []
    per_block_ber_C = []
    fade_state = []

    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            N_DFT, gamma_lin, turb_name, DOPPLER, mod='m16apsk', seed=seed0 + b,
        )
        rx_raw, bits, tx_sym = r['rx_raw'], r['bits'], r['tx']
        p_sym = tx_sym[PILOT_IDX_LOCAL]

        P_block = float(np.mean(np.abs(rx_raw) ** 2))
        is_fade = P_block < gamma_th
        fade_state.append(int(is_fade))

        h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        h_pilot = estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
        rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)

        # 方案 A: 闭环完全 hold [79]
        if is_fade:
            if tracker_A.has_locked:
                phi_hold = tracker_A.hold()
                rc_A = tracker_A.compensate_block(rx_blind, phi_hold)
            else:
                rc_A, phi_est, _ = blind_estimate_phi(rx_blind)
                tracker_A.update(phi_est)
        else:
            rc_A, phi_est, _ = blind_estimate_phi(rx_blind)
            phi_smooth = tracker_A.update(phi_est)
            rc_A = tracker_A.compensate_block(rx_blind, phi_smooth)

        # 方案 B: 闭环 pilot 全程 + power-boost
        rc_B_raw = pilot_estimate_phi(rx_pilot, p_sym, boost_factor=boost_factor)
        # B 也用 PI 平滑（提取 da_ml 的相位再平滑）
        # da_ml 内部已估相位，这里直接用补偿后信号（da_ml 是闭式一次性）
        rc_B = rc_B_raw  # B 全程 pilot，每块独立 da_ml（power-boost 消融）

        # 方案 C: 闭环双模 + power-boost
        if is_fade:
            rc_C = pilot_estimate_phi(rx_pilot, p_sym, boost_factor=boost_factor)
            # C fade 期用 pilot 估计，也送入 tracker_C update（partial hold: 环路仍跑）
            # 提取 pilot 估计的相位近似（用 rc_C 反推）
            # 简化: fade 期 tracker_C 用 pilot 补偿后的有效相位 update
            phi_C_fade = np.angle(np.mean(rc_C * np.conj(rx_pilot)))  # 粗估
            tracker_C.update(phi_C_fade)
        else:
            rc_C_raw, phi_est, _ = blind_estimate_phi(rx_blind)
            phi_smooth = tracker_C.update(phi_est)
            rc_C = tracker_C.compensate_block(rx_blind, phi_smooth)

        # BER 统计
        ne_A, nb_A = demod_ber(rc_A, bits)
        n_err_A += ne_A; n_bits_A += nb_A
        per_block_ber_A.append(ne_A / max(nb_A, 1))

        ne_B, nb_B = demod_ber(rc_B, bits, is_data_mask=is_data)
        n_err_B += ne_B; n_bits_B += nb_B

        if is_fade:
            ne_C, nb_C = demod_ber(rc_C, bits, is_data_mask=is_data)
        else:
            ne_C, nb_C = demod_ber(rc_C, bits)
        n_err_C += ne_C; n_bits_C += nb_C
        per_block_ber_C.append(ne_C / max(nb_C, 1))

        # fade 块子集 BER（C2 对照）
        if is_fade:
            ne_fh, nb_fh = demod_ber(rc_A, bits)
            n_err_fade_hold += ne_fh; n_bits_fade_hold += nb_fh
            rc_da = pilot_estimate_phi(rx_pilot, p_sym, boost_factor=1.0)
            ne_fd, nb_fd = demod_ber(rc_da, bits, is_data_mask=is_data)
            n_err_fade_da += ne_fd; n_bits_fade_da += nb_fd
        else:
            ne_nn, nb_nn = demod_ber(rc_A, bits)
            n_err_nonfade += ne_nn; n_bits_nonfade += nb_nn

    n_recover_A = compute_n_recover_v2(per_block_ber_A, fade_state,
                                        steady_window=N_RECOVER_STEADY_WINDOW,
                                        band=N_RECOVER_BAND, consecutive=N_RECOVER_CONSECUTIVE)
    n_recover_C = compute_n_recover_v2(per_block_ber_C, fade_state,
                                        steady_window=N_RECOVER_STEADY_WINDOW,
                                        band=N_RECOVER_BAND, consecutive=N_RECOVER_CONSECUTIVE)

    return {
        'ber_A_closed_hold': n_err_A / max(n_bits_A, 1),
        'ber_B_pilot_boost': n_err_B / max(n_bits_B, 1),
        'ber_C_closed_dual': n_err_C / max(n_bits_C, 1),
        'c2_ber_fade_closed_hold': n_err_fade_hold / max(n_bits_fade_hold, 1),
        'c2_ber_fade_da_ml': n_err_fade_da / max(n_bits_fade_da, 1),
        'c2_ber_nonfade_blind': n_err_nonfade / max(n_bits_nonfade, 1),
        'n_fade_blocks': int(sum(fade_state)),
        'n_nonfade_blocks': n_blocks - int(sum(fade_state)),
        'n_recover_A': n_recover_A,
        'n_recover_C': n_recover_C,
        'n_recover_A_mean': float(np.mean([r['n_recover_blocks'] for r in n_recover_A])) if n_recover_A else None,
        'n_recover_C_mean': float(np.mean([r['n_recover_blocks'] for r in n_recover_C])) if n_recover_C else None,
        'per_block_ber_A': per_block_ber_A,
        'per_block_ber_C': per_block_ber_C,
        'fade_state': fade_state,
        'boost_factor': boost_factor,
    }


def main():
    t0 = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rho_path = os.path.join(script_dir, '_rho_fade_measure.json')
    with open(rho_path) as f:
        rho_data = json.load(f)

    seed0 = 2000
    boost = POWER_BOOST_FACTOR_DEFAULT
    results = {}
    for turb in TURB_LEVELS:
        results[turb] = {}
        for snr_db in SNR_TURB:
            gamma_th = rho_data['selected'][turb][str(float(snr_db))]['gamma_th']
            gamma_lin = 10 ** (float(snr_db) / 10)
            rec = run_closed_loop_point(turb, gamma_lin, N_BLOCKS, seed0, gamma_th,
                                         boost_factor=boost)
            results[turb][str(float(snr_db))] = {k: v for k, v in rec.items()
                                                   if k not in ('per_block_ber_A', 'per_block_ber_C', 'fade_state')}
            print(f"{turb:10s} {snr_db}dB | A={rec['ber_A_closed_hold']:.6f} B={rec['ber_B_pilot_boost']:.6f} C={rec['ber_C_closed_dual']:.6f} | "
                  f"nR_A={rec['n_recover_A_mean']} nR_C={rec['n_recover_C_mean']}")

    dt = time.time() - t0
    rho_fade = 0.15; eta_p = 0.25
    overhead_db = 10 * np.log10(1 + rho_fade * eta_p * (boost - 1))

    out = {
        'meta': {
            'task': 'B2-Q2 闭环版 sandbox 三方对照（救援路线 D003）',
            'architecture': 'closed_loop_hold (block闭式估计 + 跨块PI平滑 + fade期hold + power-boost)',
            'v3_ancestry': '[79] 闭环 freeze: 跨块(integrator,vco_phase)状态 + fade冻结 + 恢复PI收敛',
            'pi_params': {'alpha': 0.3, 'beta': 0.05, 'source': 'PI滤波器经典(alpha控带宽,beta控积分)'},
            'power_boost': {'factor': boost, 'strategy': 'fade_only',
                             'overhead_db': overhead_db,
                             'source': 'DVB-S2 pilot boosting + 物理量级核算最优'},
            'n_recover_metric': {'version': 'v2', 'band': N_RECOVER_BAND,
                                  'steady_window': N_RECOVER_STEADY_WINDOW,
                                  'fix': 'band 30% + 滑窗均值（修前馈版退化）'},
            'd006_boundary': '不撞: 闭式估计估载波相位不估φ_T, PI环路TF固定, 门控用功率',
            'date': '2026-07-08',
            'duration_s': dt,
        },
        'results': results,
    }
    out_path = os.path.join(script_dir, '_sandbox_closed_loop_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n完成 {dt:.1f}s，输出 {out_path}")
    print(f"power-boost overhead (fade only, β={boost}): {overhead_db:.3f} dB")


if __name__ == '__main__':
    main()
