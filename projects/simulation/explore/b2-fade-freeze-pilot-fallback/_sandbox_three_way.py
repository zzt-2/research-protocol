"""B2-Q2 sandbox 三方对照（阶段 1，首次写代码，守 V2 三方对照 + V3 祖师爷警报）.

三方（阶段 0.4 §1.1 三方对照矩阵 + V2）:
  A. 纯 blind freeze [79] Matsuda（祖师爷 baseline，V3）:
     非 fade 期 fft_foe_m0_omega + nda_ml CPE / fade 期 hold 上一估计（freeze）
  B. 纯 pilot-aided（step4a DA ML 全程，复现 fade 崩溃）:
     da_ml_recovery 全程
  C. B2-Q2 双模切换（本候选）:
     非 fade 期 fft_foe_m0_omega + nda_ml / fade 期 da_ml（+ psa_foe 备选测维度 C2）

两个必答问题:
  必答 1（维度 C2 红线）: 所有 pilot-aided 变体（da_ml/psa_foe）在 fade 块是否都输 NDA-ML？
    判据: fade 块 BER(pilot) vs fade 块 BER(blind, 非 freeze 的正常 nda_ml)
    全输 → 红线警报转 Kill / 有赢 → C2 不成立命题可继续
  必答 2（动态恢复时间）: B2-Q2 双模切换 N_recover vs 纯 blind freeze N_recover
    测度: fade 结束后滑窗 BER 回稳态 ±10% 所需符号数

公平对照（阶段 0.4 §3）:
  - 三方同信道同符号率（generate_shared_realization_apsk 共享实现，守 TL-13）
  - pilot overhead: A=0% / B=全帧 1.249dB / C=ρ_fade×1.249dB（摊薄）
  - BER 计算位置: A 全块 / B data 位置 / C 分块（非fade全块+fade data位置）
  - per-block h 均衡: 跟估计器匹配（非fade盲估/fade pilot估）

fade 检测（阶段 0.3 §5.2 前馈化 INVARIANT）:
  - 粒度: N_DFT 块级（256 符号，跟逐块恢复块对齐）
  - γ_th: 从 _rho_fade_measure.json 读（ρ_fade=0.15 反推，sandbox 第一步实测）
  - 开环功率阈值 g(P)=1[P<γ_th]，不闭环不误差驱动

输出:
  - _sandbox_results.json: 三方 BER + 维度 C2 红线结果 + 动态恢复时间（meta 字段强制）
"""
import os
import sys
import json
import time
import numpy as np

_SIM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

# 同目录 import B2Params + step4a 锚脚本的 fft_foe_m0_omega
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _b2_params_draft import (
    LASER_LW, R_SYM, T_S, SIGMA2_PN,
    TURB_LEVELS, GG_ALPHA_BETA,
    DA_PILOT_SPACING, PILOT_OVERHEAD_DB_FULL,
    N_DFT, CH_BLOCK, N_BLOCKS, HDFEC,
    SNR_TURB, SEED_TURB0, DOPPLER, M0,
)

from common import (
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery, psa_foe_recovery,
    mmse_equalize, amp_limit,
)
# step4a 锚脚本自带 fft_foe_m0_omega（升 M₀=8 版，_recovery.py:37 fft_foe 是 QPSK M=4 专用不适用 16-APSK）
# + estimate_h_blind_perblock / estimate_h_pilot_perblock（per-block h 均衡 helper）
# 用 importlib 加载（文件名 _ 前缀，避免命名耦合，复用 step4a 已验证实现，守 TL-13 共用 + 不重复造轮子）
import importlib.util
_sc_nda_path = os.path.join(_SIM_ROOT, 'explore', 'single-carrier-nda-ml', '_time_domain_crlb.py')
_spec = importlib.util.spec_from_file_location('_sc_nda_helpers', _sc_nda_path)
_sc_nda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc_nda)
fft_foe_m0_omega = _sc_nda.fft_foe_m0_omega
estimate_h_blind_perblock = _sc_nda.estimate_h_blind_perblock
estimate_h_pilot_perblock = _sc_nda.estimate_h_pilot_perblock


# =============================================================================
# 估计器路径（三方对照核心，复用 step4a 湍流路径）
# =============================================================================
BITS_PER_SYM = 4  # (8,8)-16APSK
PILOT_IDX_LOCAL = np.arange(0, N_DFT, DA_PILOT_SPACING)  # 块内 pilot 位置 [0,4,...,252]，64 pilot/块


def blind_estimate_block(rx_block):
    """blind 估计单块（非 fade 期，step4a 湍流路径同款两阶段）.

    fft_foe_m0_omega 粗估 CFO → nda_ml CPE 估残余 → 返回 (rx_comp, phi_est, omega_est).
    用于方案 A 非 fade 期 + 方案 C 非 fade 期.
    """
    omega_est = fft_foe_m0_omega(rx_block, M0)
    k = np.arange(N_DFT)
    seg_foe = rx_block * np.exp(-1j * omega_est * k)
    rc, _, phi_est, _ = nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)
    return rc, phi_est, omega_est


def pilot_estimate_block_da(rx_block, pilot_sym):
    """pilot-aided DA ML 估计单块（fade 期，step4a 锚 da_ml）.

    da_ml_recovery 线性回归闭式 (φ, Δf). 返回 rx_comp.
    用于方案 B 全程 + 方案 C fade 期主选.
    """
    rc, _, _ = da_ml_recovery(rx_block, pilot_idx=PILOT_IDX_LOCAL,
                              pilot_sym=pilot_sym, mod='m16apsk')
    return rc


def pilot_estimate_block_psa(rx_block, pilot_sym):
    """pilot-aided PSA FOE 估计单块（fade 期备选，测维度 C2）.

    psa_foe_recovery 差分相位最小二乘，只估 FOE 不估 CPE.
    返回 rx_comp（注意: psa_foe 只补 FOE，CPE 残留 → BER 会比 da_ml 高，这是预期差异）.
    用于维度 C2 红线测试（≥2 pilot-aided 变体）.
    """
    rc, _ = psa_foe_recovery(rx_block, pilot_idx=PILOT_IDX_LOCAL, pilot_sym=pilot_sym)
    return rc


def freeze_compensate_block(rx_block, phi_last, omega_last):
    """freeze 机制（[79] Matsuda）：用上一非 fade 块的估计补偿当前 fade 块.

    hold (phi_last, omega_last) → rx_comp = rx * exp(-j*(phi_last + omega_last*k)).
    用于方案 A fade 期.
    """
    k = np.arange(N_DFT)
    return rx_block * np.exp(-1j * (phi_last + omega_last * k))


# =============================================================================
# 三方 BER 评估（每点跑 N_BLOCKS 块，逐块估计 + 全局 BER 统计）
# =============================================================================
def run_three_way_for_point(turb_name, gamma_lin, n_blocks, seed0, gamma_th,
                            pilot_estimator_fade='da_ml'):
    """单点（turb × snr）三方对照 + 维度 C2 红线测试.

    返回 dict:
      n_err/n_bits 三方（A/B/C）+ fade 块子集 BER（维度 C2）+ fade/nonfade 块索引
      pilot_estimator_fade: 'da_ml'（主）/ 'psa_foe'（备，测维度 C2）
    """
    # 累积器
    n_err_A = n_err_B = n_err_C = 0
    n_bits_A = n_bits_B = n_bits_C = 0
    # 维度 C2: fade 块内分估计器 BER
    n_err_fade_da = n_err_fade_psa = n_err_fade_blind = 0
    n_bits_fade_da = n_bits_fade_psa = n_bits_fade_blind = 0
    # 非 fade 块 BER（基准对照，C2 判读用）
    n_err_nonfade_blind = n_bits_nonfade_blind = 0
    # 动态恢复: 记录每块 BER + fade 状态（后处理算 N_recover）
    per_block_ber_A = []  # 方案 A 每块 BER
    per_block_ber_C = []  # 方案 C 每块 BER
    fade_state = []       # 每块是否 fade（0/1）

    # 方案 A freeze 状态（hold 上一非 fade 块估计）
    phi_last_A = 0.0
    omega_last_A = 0.0
    has_valid_estimate_A = False  # 是否已有非 fade 估计可 freeze

    # 块内 data 位置 mask（pilot 位置不算 BER，公平对照）
    is_data = np.ones(N_DFT, dtype=bool)
    is_data[PILOT_IDX_LOCAL] = False

    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            N_DFT, gamma_lin, turb_name, DOPPLER, mod='m16apsk', seed=seed0 + b,
        )
        rx_raw, bits, tx_sym = r['rx_raw'], r['bits'], r['tx']
        p_sym = tx_sym[PILOT_IDX_LOCAL]

        # 块级功率 + fade 判定（前馈开环，INVARIANT）
        P_block = float(np.mean(np.abs(rx_raw) ** 2))
        is_fade = P_block < gamma_th
        fade_state.append(int(is_fade))

        # per-block h 均衡（跟估计器匹配，公平对照核心）
        # 公平原则: h 均衡方式跟当前方案是否有 pilot 一致
        #   - A 纯 blind: 全程 blind h（fade 块也 blind h，freeze 只 freeze 相位不 freeze h）
        #   - B 纯 pilot: 全程 pilot h
        #   - C 双模: 非 fade 期 blind h（无 pilot）/ fade 期 pilot h（有 pilot）
        h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        h_pilot = estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
        rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)

        if is_fade:
            # A: blind h + freeze 相位; B: pilot h; C: pilot h（fade 期有 pilot）
            rx_for_A = rx_blind
            rx_for_B = rx_pilot
            rx_for_C = rx_pilot
        else:
            # A: blind h; B: pilot h; C: blind h（非 fade 期无 pilot）
            rx_for_A = rx_blind
            rx_for_B = rx_pilot
            rx_for_C = rx_blind

        # 方案 A: 纯 blind freeze [79]
        if is_fade:
            if has_valid_estimate_A:
                rc_A = freeze_compensate_block(rx_for_A, phi_last_A, omega_last_A)
            else:
                # 还没有非 fade 估计（开头就 fade），用盲估兜底
                rc_A, _, _ = blind_estimate_block(rx_for_A)
        else:
            rc_A, phi_est, omega_est = blind_estimate_block(rx_for_A)
            phi_last_A = phi_est
            omega_last_A = omega_est
            has_valid_estimate_A = True

        # 方案 B: 纯 pilot-aided（da_ml 全程）
        rc_B = pilot_estimate_block_da(rx_for_B, p_sym)

        # 方案 C: B2-Q2 双模切换
        if is_fade:
            if pilot_estimator_fade == 'da_ml':
                rc_C = pilot_estimate_block_da(rx_for_C, p_sym)
            else:  # 'psa_foe'
                rc_C = pilot_estimate_block_psa(rx_for_C, p_sym)
        else:
            rc_C, _, _ = blind_estimate_block(rx_for_C)

        # 维度 C2 红线测试：fade 块内各估计器 BER（只 fade 块）
        # 公平: 各估计器配匹配的 h 均衡（pilot 估计器用 pilot h，blind 用 blind h）
        if is_fade:
            tb = bits[:N_DFT * BITS_PER_SYM]
            tb_arr = tb.reshape(N_DFT, BITS_PER_SYM)
            nb_data = int(np.sum(is_data) * BITS_PER_SYM)
            # da_ml: pilot 估计器 → pilot h（rx_pilot），BER 算 data 位置
            rc_fade_da = pilot_estimate_block_da(rx_pilot, p_sym)
            demod_da = m16apsk_demod(rc_fade_da).reshape(N_DFT, BITS_PER_SYM)
            ne = int(np.sum(tb_arr[is_data] != demod_da[is_data]))
            n_err_fade_da += ne; n_bits_fade_da += nb_data
            # psa_foe: pilot 估计器 → pilot h，BER 算 data 位置
            rc_fade_psa = pilot_estimate_block_psa(rx_pilot, p_sym)
            demod_psa = m16apsk_demod(rc_fade_psa).reshape(N_DFT, BITS_PER_SYM)
            ne = int(np.sum(tb_arr[is_data] != demod_psa[is_data]))
            n_err_fade_psa += ne; n_bits_fade_psa += nb_data
            # blind_nda: blind 估计器 → blind h（rx_blind），BER 算全块
            rc_fade_blind, _, _ = blind_estimate_block(rx_blind)
            demod_blind = m16apsk_demod(rc_fade_blind)
            ne = int(np.sum(tb != demod_blind))
            n_err_fade_blind += ne; n_bits_fade_blind += len(tb)
        else:
            # 非 fade 块 blind BER（基准，blind h）
            rc_nonfade_blind, _, _ = blind_estimate_block(rx_blind)
            tb = bits[:N_DFT * BITS_PER_SYM]
            demod = m16apsk_demod(rc_nonfade_blind)
            ne = int(np.sum(tb != demod))
            n_err_nonfade_blind += ne; n_bits_nonfade_blind += len(tb)

        # 三方全局 BER（A 全块 / B data 位置 / C 分块）
        tb = bits[:N_DFT * BITS_PER_SYM]
        # 方案 A: 全块 BER（blind 非 fade 全符号 + freeze fade 全符号）
        demod_A = m16apsk_demod(rc_A)
        ne_A = int(np.sum(tb != demod_A))
        n_err_A += ne_A; n_bits_A += len(tb)
        per_block_ber_A.append(ne_A / len(tb))
        # 方案 B: data 位置 BER（pilot 全程，data 位置才算）
        demod_B = m16apsk_demod(rc_B)
        tb_arr = tb.reshape(N_DFT, BITS_PER_SYM)
        dm_arr = demod_B.reshape(N_DFT, BITS_PER_SYM)
        ne_B = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
        nb_B = int(np.sum(is_data) * BITS_PER_SYM)
        n_err_B += ne_B; n_bits_B += nb_B
        # 方案 C: 非 fade 全块 + fade data 位置（公平：fade 期有 pilot 只算 data）
        demod_C = m16apsk_demod(rc_C)
        dm_arr = demod_C.reshape(N_DFT, BITS_PER_SYM)
        if is_fade:
            ne_C = int(np.sum(tb_arr[is_data] != dm_arr[is_data]))
            nb_C = int(np.sum(is_data) * BITS_PER_SYM)
        else:
            ne_C = int(np.sum(tb != demod_C))
            nb_C = len(tb)
        n_err_C += ne_C; n_bits_C += nb_C
        per_block_ber_C.append(ne_C / nb_C if nb_C > 0 else 0.0)

    return {
        # 三方全局 BER
        'ber_A_blind_freeze': n_err_A / max(n_bits_A, 1),
        'ber_B_pilot_da': n_err_B / max(n_bits_B, 1),
        'ber_C_b2q2_dual': n_err_C / max(n_bits_C, 1),
        'n_bits_A': n_bits_A, 'n_bits_B': n_bits_B, 'n_bits_C': n_bits_C,
        # 维度 C2: fade 块内各估计器 BER
        'ber_fade_da_ml': n_err_fade_da / max(n_bits_fade_da, 1),
        'ber_fade_psa_foe': n_err_fade_psa / max(n_bits_fade_psa, 1),
        'ber_fade_blind_nda': n_err_fade_blind / max(n_bits_fade_blind, 1),
        'ber_nonfade_blind_nda': n_err_nonfade_blind / max(n_bits_nonfade_blind, 1),
        'n_fade_blocks': int(sum(fade_state)),
        'n_nonfade_blocks': n_blocks - int(sum(fade_state)),
        # 动态恢复: 每块 BER + fade 状态（用于 N_recover 后处理）
        'per_block_ber_A': per_block_ber_A,
        'per_block_ber_C': per_block_ber_C,
        'fade_state': fade_state,
        'pilot_estimator_fade': pilot_estimator_fade,
    }


def compute_n_recover(per_block_ber, fade_state, steady_state_window=50):
    """算动态恢复时间 N_recover.

    定义（阶段 0.4 §2.2）: fade 结束（fade 块后第一个非 fade 块）后，
    滑窗 BER 回到稳态 BER ±10% 所需块数.

    稳态 BER = 所有非 fade 块的平均 BER（排除前 steady_state_window 块热身）.

    返回 list of (fade_end_block_idx, n_recover_blocks)（每个 fade→非fade 转换一个）.
    """
    n = len(fade_state)
    if n == 0:
        return []
    # 稳态 BER（非 fade 块平均，排除热身）
    nonfade_idx = [i for i in range(n) if not fade_state[i] and i >= steady_state_window]
    if not nonfade_idx:
        return []
    steady_ber = float(np.mean([per_block_ber[i] for i in nonfade_idx]))
    if steady_ber <= 0:
        return []
    threshold_hi = steady_ber * 1.10  # +10%
    threshold_lo = steady_ber * 0.90  # -10%

    # 找所有 fade→非fade 转换点
    transitions = []
    for i in range(1, n):
        if fade_state[i - 1] == 1 and fade_state[i] == 0:
            transitions.append(i)

    n_recover_list = []
    for trans_idx in transitions:
        # 从 trans_idx 开始往后扫，找连续 BER 回到 [threshold_lo, threshold_hi] 的块数
        recover_count = 0
        for j in range(trans_idx, n):
            if fade_state[j] == 1:
                break  # 又进入 fade，停止本次恢复统计
            ber_j = per_block_ber[j]
            if threshold_lo <= ber_j <= threshold_hi:
                recover_count += 1
                if recover_count >= 3:  # 连续 3 块在稳态带内算恢复
                    break
            else:
                recover_count = 0
        n_recover = j - trans_idx + 1 if recover_count >= 3 else (n - trans_idx)
        n_recover_list.append({
            'fade_end_block': trans_idx,
            'n_recover_blocks': int(n_recover),
            'n_recover_symbols': int(n_recover * N_DFT),
        })
    return n_recover_list


def main():
    t0 = time.time()

    # 读 sandbox 第一步实测的 γ_th（每 turb × snr）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rho_path = os.path.join(script_dir, '_rho_fade_measure.json')
    with open(rho_path) as f:
        rho_data = json.load(f)
    rho_selected = rho_data['selected']

    print("=" * 100)
    print("B2-Q2 sandbox 三方对照（V2 三方 + V3 祖师爷 [79] + 维度 C2 红线 + 动态恢复）")
    print(f"N_BLOCKS/点={N_BLOCKS}, N_DFT={N_DFT}, γ_th 来自 _rho_fade_measure.json (ρ_fade=0.15)")
    print(f"pilot_overhead: A=0% / B=全帧{PILOT_OVERHEAD_DB_FULL:.3f}dB / C=ρ_fade×{PILOT_OVERHEAD_DB_FULL:.3f}dB")
    print("=" * 100)

    results = {}
    print(f"\n{'turb':10s} {'γd_dB':>6s} {'γ_th':>10s} {'A_freeze':>10s} {'B_pilot':>10s} "
          f"{'C_dual':>10s} | {'fade块':>6s} {'C2:da':>10s} {'C2:psa':>10s} {'C2:blind':>10s} {'C2:非f':>10s}")
    print("-" * 110)

    for turb in TURB_LEVELS:
        results[turb] = {}
        for gamma_db in SNR_TURB:
            gamma_lin = 10 ** (gamma_db / 10)
            gamma_th = rho_selected[turb][f'{gamma_db:.1f}']['gamma_th']
            rho_fade = rho_selected[turb][f'{gamma_db:.1f}']['rho_fade']

            # 方案 C 主跑: fade 期 da_ml
            rec = run_three_way_for_point(turb, gamma_lin, N_BLOCKS, SEED_TURB0, gamma_th,
                                          pilot_estimator_fade='da_ml')
            # 动态恢复（方案 A vs C）
            n_recover_A = compute_n_recover(rec['per_block_ber_A'], rec['fade_state'])
            n_recover_C = compute_n_recover(rec['per_block_ber_C'], rec['fade_state'])
            mean_n_rec_A = float(np.mean([x['n_recover_blocks'] for x in n_recover_A])) if n_recover_A else None
            mean_n_rec_C = float(np.mean([x['n_recover_blocks'] for x in n_recover_C])) if n_recover_C else None

            results[turb][f'{gamma_db:.1f}'] = {
                'gamma_th': float(gamma_th),
                'rho_fade': float(rho_fade),
                'ber_A_blind_freeze': rec['ber_A_blind_freeze'],
                'ber_B_pilot_da': rec['ber_B_pilot_da'],
                'ber_C_b2q2_dual_da': rec['ber_c_b2q2_dual' if False else 'ber_C_b2q2_dual'],
                # 维度 C2 红线（fade 块内各估计器）
                'c2_ber_fade_da_ml': rec['ber_fade_da_ml'],
                'c2_ber_fade_psa_foe': rec['ber_fade_psa_foe'],
                'c2_ber_fade_blind_nda': rec['ber_fade_blind_nda'],
                'c2_ber_nonfade_blind_nda': rec['ber_nonfade_blind_nda'],
                'n_fade_blocks': rec['n_fade_blocks'],
                'n_nonfade_blocks': rec['n_nonfade_blocks'],
                # 动态恢复
                'n_recover_A_mean_blocks': mean_n_rec_A,
                'n_recover_C_mean_blocks': mean_n_rec_C,
                'n_recover_transitions': len(n_recover_A),
            }
            print(f"{turb:10s} {gamma_db:>6.0f} {gamma_th:>10.3e} "
                  f"{rec['ber_A_blind_freeze']:>10.4f} {rec['ber_B_pilot_da']:>10.4f} "
                  f"{rec['ber_C_b2q2_dual']:>10.4f} | {rec['n_fade_blocks']:>6d} "
                  f"{rec['ber_fade_da_ml']:>10.4f} {rec['ber_fade_psa_foe']:>10.4f} "
                  f"{rec['ber_fade_blind_nda']:>10.4f} {rec['ber_nonfade_blind_nda']:>10.4f}")

    elapsed = time.time() - t0
    print(f"\n[耗时] {elapsed:.1f}s")

    # 保存结果（meta 字段强制，仿 step4a _time_domain_crlb.py:592-597）
    out = {
        'meta': {
            'task': 'B2-Q2 sandbox 三方对照（阶段 1）',
            'purpose': '回答两个必答问题: 维度C2红线(所有pilot-aided在fade是否输NDA-ML) + 动态恢复时间',
            'three_way': {
                'A': '纯 blind freeze [79] Matsuda (祖师爷baseline, V3): 非 fade fft_foe+nda_ml / fade hold上一估计',
                'B': '纯 pilot-aided da_ml 全程 (step4a 锚, 复现 fade 崩溃)',
                'C': 'B2-Q2 双模切换 (本候选): 非 fade fft_foe+nda_ml / fade da_ml',
            },
            'params': {
                'N_BLOCKS': N_BLOCKS, 'N_DFT': N_DFT, 'CH_BLOCK': CH_BLOCK,
                'DA_PILOT_SPACING': DA_PILOT_SPACING,
                'PILOT_OVERHEAD_DB_FULL': float(PILOT_OVERHEAD_DB_FULL),
                'SNR_TURB': SNR_TURB, 'TURB_LEVELS': TURB_LEVELS,
                'GG_ALPHA_BETA': {k: list(v) for k, v in GG_ALPHA_BETA.items()},
                'SIGMA2_PN': float(SIGMA2_PN),
                'LASER_LW': float(LASER_LW), 'R_SYM': float(R_SYM), 'T_S': float(T_S),
                'DOPPLER': float(DOPPLER), 'SEED_TURB0': SEED_TURB0, 'M0': M0,
            },
            'gamma_th_source': '_rho_fade_measure.json (sandbox 第一步实测, ρ_fade=0.15 反推)',
            'fairness': {
                'pilot_overhead': 'A=0% / B=全帧1.249dB / C=ρ_fade×1.249dB (阶段0.4 §3.2 摊薄)',
                'ber_counting': 'A 全块 / B data位置 / C 分块(非fade全块+fade data位置)',
                'per_block_h_equalize': '跟估计器匹配: 非fade盲估/fade pilot估',
                'channel': 'generate_shared_realization_apsk 共享实现 (TL-13)',
            },
            'c2_redline_test': 'fade 块内 da_ml / psa_foe / blind_nda 三方 BER 对照',
            'dynamic_recovery_metric': 'fade→非fade 转换后 BER 回稳态±10% 所需块数 (阶段0.4 §2.2)',
            'architecture': '前馈化 INVARIANT (4估计器全前馈闭式 + 开环γ_th门控, 不撞D006)',
            'elapsed_s': float(elapsed),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        'results': results,
    }
    out_path = os.path.join(script_dir, '_sandbox_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[saved] {out_path}")


if __name__ == '__main__':
    main()
