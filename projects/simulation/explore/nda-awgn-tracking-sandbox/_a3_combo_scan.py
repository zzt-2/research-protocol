# -*- coding: utf-8 -*-
"""A3 组合适配扫描 — combo scan (adaptation-scan A3, 第 2 轮: 互补性再验).

任务 (仿真执行 agent / A3): 验证 2 种组合的互补性, 看组合是否优于单一方法:
  组合 1 (b) 级联 NDA→DPLL: NDA 补偿大块相位 → DPLL_track_dd 连续跟踪残余
  组合 2 (可选) NDA→VV:      NDA 升幂粗估 CFO/块常数 → VV 滑窗精修

背景/约束 (读上下文得到):
  - common/_recovery.py: nda_ml_recovery / dpll_track_dd / vv_cpr (但 vv_cpr 硬编码 M=4,
    对 16APSK M0=8 错; VV-ablation 提供 vv_cpr_m16apsk M0=8 版).
  - sc_nda_ml_sim.py: awgn_wiener_channel / ber_nda_awgn / ber_nda_turb_eval / fft_foe_m0_omega.
  - run_dpll_ablation.py: dpll_track_dd_m16apsk + hard_decision_m16apsk (S011, omega_n=50e6).
  - run_vv_ablation.py: vv_cpr_m16apsk (M0=8 unwrap, Nw=64).
  - D-009: NDA vs VV 同族 (升幂类) → NDA+VV 组合可能冗余. 本脚本直接测.

已有结果 (不动, 仅对照):
  - run_a3_hybrid_ablation.py (5-seed, 6 场景) 结论: NDA+DPLL **FAIL** (冗余, ±0.06dB 内,
    CI 跨 0; strong 反输 DPLL 0.046dB). 物理根因: σ²_p=2.51e-5 极小, NDA 块常数 ≈ DPLL 跟踪精度.

本脚本增量价值:
  (1) NDA+DPLL 级联: 用 2 seed 快速复现确认现有 5-seed 结论 (在 AWGN + weak 两代表性场景).
      互补判据: combo BER < min(NDA, DPLL) → 互补成立 (预期 FAIL, 与既有结论一致).
  (2) NDA+VV 级联 [新]: 既有代码未做. 测 NDA 粗估后送 VV 精修 vs 单一 NDA / 单一 VV.
      同族冗余假设: 组合 ≈ max(NDA, VV), 无增量.

纪律:
  - 先 2 seed 看趋势; 若有信号 (combo < min 单一) 再扩 seed.
  - DPLL 连续处理 (全数组 VCO 累积, 不 per-block 重置, 守 S011).
  - 16APSK M0=8: VV 用 M0=8 unwrap (vv_cpr_m16apsk), DPLL 用 DD 版 (dpll_track_dd_m16apsk).
  - 守 TL-13: 信道实现 bit-exact 复用 sc_nda_ml_sim (同 seed 同 generate_shared_realization_apsk).
  - 时间 ≤15 min.

运行: cd projects/simulation && python explore/nda-awgn-tracking-sandbox/_a3_combo_scan.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守 TL-13)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    nda_ml_recovery,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402  (复用其公开信道/h 估计/FOE API)
# 异族方法从各自 ablation 脚本复用 (已验证 M0=8 适配)
from run_dpll_ablation import dpll_track_dd_m16apsk, hard_decision_m16apsk  # noqa: E402
from run_vv_ablation import vv_cpr_m16apsk  # noqa: E402
from params import SimulationConfig  # noqa: E402


# =============================================================================
# 全局参数
# =============================================================================
N_SEEDS = 2              # 纪律: 先 2 seed 看趋势
SCENES = ['awgn', 'weak']          # 代表性场景 (AWGN 无 fade / weak 有轻湍流)
TURB_SCENES = ['weak']
# 代表性 SNR: AWGN 18-20dB (工作区), weak 20-22dB (工作区). 少点多 seed 快速看趋势.
SNR_REPR = {
    'awgn': [16.0, 18.0, 20.0],
    'weak': [18.0, 20.0, 22.0],
}
# DPLL 参数 (S011 选定 omega_n=50e6, zeta=√2/2)
OMEGA_N_DPLL = 50e6
ZETA_DPLL = np.sqrt(2) / 2
# VV 参数 (VV-ablation Nw=64)
NW_VV = 64


# =============================================================================
# 组合 1 (b): NDA→DPLL 级联 (NDA 粗估块常数 → DPLL 连续跟踪残余)
# =============================================================================
def ber_combo_nda_dpll_awgn(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """级联 NDA→DPLL AWGN.

    step1: NDA-ML per-block segmented 升幂估块常数 CPE, 补偿得 rx_nda (去块常数相位).
    step2: DPLL DD 连续跟踪 rx_nda 的残余漂移 (全数组 VCO 累积, 守 S011).
    step3: resolve_m16apsk_blockwise 解 M0=8-fold 模糊.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_nda = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk',
                                      assume_df_zero=True,
                                      intra_block_tracking='segmented')
        rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    # 连续 DPLL 跟踪残余 (不 per-block 重置)
    rx_comp, _ = dpll_track_dd_m16apsk(rx_nda, omega_n=omega_n, zeta=ZETA_DPLL)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_combo_nda_dpll_turb_eval(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """级联 NDA→DPLL 湍流: 两阶段 (per-block fft_foe → NDA 块常数 → 连续 DPLL 跟踪残余)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_nda = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _, _, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
        rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    rx_comp, _ = dpll_track_dd_m16apsk(rx_nda, omega_n=omega_n, zeta=ZETA_DPLL)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 组合 2: NDA→VV 级联 (NDA 升幂粗估 CFO/块常数 → VV 滑窗精修) [新, D-009 同族冗余测试]
# =============================================================================
def ber_combo_nda_vv_awgn(rx, tx_bits):
    """级联 NDA→VV AWGN.

    step1: NDA-ML per-block segmented 估块常数 CPE (assume_df_zero=True), 补偿得 rx_nda.
    step2: VV-CPR M0=8 滑窗精修 rx_nda 残余相位 (per-block, 跟 ber_vv_awgn 同结构).
    step3: resolve_m16apsk_blockwise 解 M0=8-fold 模糊.

    D-009 假设: NDA 和 VV 同属升幂类 (M0=8), 组合冗余 → 预期 ≈ max(NDA, VV) 无增量.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_nda = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk',
                                      assume_df_zero=True,
                                      intra_block_tracking='segmented')
        rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    # VV 精修 rx_nda (per-block, 同 ber_vv_awgn 结构)
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _ = vv_cpr_m16apsk(seg, Nw=NW_VV)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_combo_nda_vv_turb_eval(rx, tx_bits):
    """级联 NDA→VV 湍流: 两阶段 (per-block fft_foe → NDA 块常数 → per-block VV 精修)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_nda = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _, _, _ = nda_ml_recovery(seg_foe, P.M0, mod='m16apsk', assume_df_zero=True)
        rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx_nda[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _ = vv_cpr_m16apsk(seg, Nw=NW_VV)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 单一 baseline 评估 (对照) — 复用 sc_nda_ml_sim + ablation, bit-exact 守 TL-13
# =============================================================================
def ber_nda_awgn(rx, tx_bits):
    """单一 NDA-ML AWGN (segmented intra_block_tracking, 同 ber_nda_awgn)."""
    return S.ber_nda_awgn(rx, tx_bits)


def ber_nda_turb_eval(rx, tx_bits):
    return S.ber_nda_turb_eval(rx, tx_bits)


def ber_dpll_awgn(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """单一 DPLL AWGN (连续 DD-DPLL, 复用 run_dpll_ablation)."""
    from run_dpll_ablation import ber_dpll_awgn as _bda
    return _bda(rx, tx_bits, omega_n=omega_n)


def ber_dpll_turb_eval(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    from run_dpll_ablation import ber_dpll_turb_eval as _bdt
    return _bdt(rx, tx_bits, omega_n=omega_n)


def ber_vv_awgn(rx, tx_bits):
    """单一 VV AWGN (per-block VV-CPR, 复用 run_vv_ablation)."""
    from run_vv_ablation import ber_vv_awgn as _bva
    return _bva(rx, tx_bits)


def ber_vv_turb_eval(rx, tx_bits):
    from run_vv_ablation import ber_vv_turb_eval as _bvt
    return _bvt(rx, tx_bits)


# =============================================================================
# 信道实现 (AWGN + 湍流, 同 seed 派生, bit-exact 复现主实验)
# =============================================================================
def make_awgn_realization(snr, seed):
    """AWGN 信道 (复用 S.awgn_wiener_channel). 返回 (rx, bits, phi_true)."""
    N_sym = P.N_BLOCKS * P.N_DFT
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, phi_true = S.awgn_wiener_channel(tx, snr, seed)
    return rx, bits, phi_true


def make_turb_realization(turb_name, gamma_lin, seed, cfg):
    """湍流信道 (复用 generate_shared_realization_apsk), 盲 h 均衡 (同 NDA-ML).
    返回 (rx_blind, bits, phi, tx_sym, h_true)."""
    Ns = P.N_DFT
    r = generate_shared_realization_apsk(
        Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
        mod='m16apsk', seed=seed)
    rx_raw = r['rx_raw']
    bits = r['bits']
    phi = r['phi']
    tx_sym = r['tx']
    h_true = r['h']
    h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
    rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
    return rx_blind, bits, phi, tx_sym, h_true


# =============================================================================
# 评估调度: 单场景 × 多 SNR × N_SEEDS → BER 表
# =============================================================================
def eval_awgn_seed(snr, seed):
    """AWGN 单 seed: 跑 NDA / DPLL / VV / NDA+DPLL / NDA+VV, 返回各方法 BER dict."""
    rx, bits, _ = make_awgn_realization(snr, seed)
    out = {}
    # 单一 baseline
    ne, nb = ber_nda_awgn(rx, bits); out['nda'] = ne / nb
    ne, nb = ber_dpll_awgn(rx, bits); out['dpll'] = ne / nb
    ne, nb = ber_vv_awgn(rx, bits); out['vv'] = ne / nb
    # 组合
    ne, nb = ber_combo_nda_dpll_awgn(rx, bits); out['nda_dpll'] = ne / nb
    ne, nb = ber_combo_nda_vv_awgn(rx, bits); out['nda_vv'] = ne / nb
    return out


def eval_turb_seed(turb_name, gamma_db, seed, cfg):
    """湍流单 seed: 跑 NDA / DPLL / VV / NDA+DPLL / NDA+VV, 返回各方法 BER dict."""
    gamma_lin = 10 ** (gamma_db / 10)
    rx_blind, bits, phi, tx_sym, h_true = make_turb_realization(
        turb_name, gamma_lin, seed, cfg)
    # oracle h 均衡 (仅 oracle 参照, 公平上界)
    rx_trueh = amp_limit(mmse_equalize(
        generate_shared_realization_apsk(
            P.N_DFT, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
            mod='m16apsk', seed=seed)['rx_raw'], h_true, gamma_lin), 3.0)
    out = {}
    # 单一 baseline
    ne, nb = ber_nda_turb_eval(rx_blind, bits); out['nda'] = ne / nb
    ne, nb = ber_dpll_turb_eval(rx_blind, bits); out['dpll'] = ne / nb
    ne, nb = ber_vv_turb_eval(rx_blind, bits); out['vv'] = ne / nb
    # 组合
    ne, nb = ber_combo_nda_dpll_turb_eval(rx_blind, bits); out['nda_dpll'] = ne / nb
    ne, nb = ber_combo_nda_vv_turb_eval(rx_blind, bits); out['nda_vv'] = ne / nb
    # oracle 上界
    ne_or, nb_or = S.ber_oracle_turb(rx_trueh, bits, phi)
    out['oracle'] = ne_or / nb_or
    return out


def run_scene(scene, cfg, t_start, time_budget=840.0):
    """单场景 × SNR × seeds → 结果表 (mean over seeds)."""
    snrs = SNR_REPR[scene]
    print(f"\n[{scene}] seeds={N_SEEDS}, SNR={snrs}")
    header = f"{'SNR':>6} " + ' '.join(f'{m:>9}' for m in
             ['NDA', 'DPLL', 'VV', 'NDA+DPLL', 'NDA+VV', 'oracle'])
    print(header)
    per_snr = []
    for snr in snrs:
        if time.time() - t_start > time_budget:
            print(f"  [TIME-BOX] 超 {time_budget}s, 停在 {scene} SNR {snr}")
            return per_snr, True
        seed_list = []
        for i in range(N_SEEDS):
            if scene == 'awgn':
                seed = P.SEED_AWGN + i
                d = eval_awgn_seed(snr, seed)
            else:
                seed0 = P.SEED_TURB0 + i * P.N_BLOCKS
                d = eval_turb_seed(scene, snr, seed0, cfg)
            seed_list.append(d)
        # mean over seeds
        mean_d = {k: float(np.mean([d[k] for d in seed_list])) for k in seed_list[0]}
        print(f"{snr:>6.0f} " + ' '.join(
            f'{mean_d.get(m, float("nan")):>9.3e}' for m in
            ['nda', 'dpll', 'vv', 'nda_dpll', 'nda_vv', 'oracle']))
        per_snr.append({
            'snr_db': float(snr),
            **{f'{k}_ber_mean': v for k, v in mean_d.items()},
            'per_seed': seed_list,
        })
    return per_snr, False


# =============================================================================
# 互补性判定
# =============================================================================
def complementarity_judgement(per_snr, combo_key, baselines):
    """逐 SNR: combo < min(baselines) → 互补成立该点. 返回 (n_win, n_total, worst_ratio)."""
    n_win = 0
    n_total = 0
    ratios = []  # combo / min(baseline); <1 = combo 赢
    for p in per_snr:
        combo = p.get(f'{combo_key}_ber_mean')
        if combo is None:
            continue
        base_vals = [p.get(f'{b}_ber_mean') for b in baselines]
        base_vals = [v for v in base_vals if v is not None]
        if not base_vals:
            continue
        min_base = min(base_vals)
        n_total += 1
        ratio = combo / min_base if min_base > 0 else float('inf')
        ratios.append(ratio)
        if combo < min_base:
            n_win += 1
    worst_ratio = max(ratios) if ratios else None
    best_ratio = min(ratios) if ratios else None
    return n_win, n_total, worst_ratio, best_ratio


# =============================================================================
# 工具
# =============================================================================
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
    t0 = time.time()
    cfg = SimulationConfig()
    print("=" * 100)
    print(f"A3 组合适配扫描 (combo scan): NDA+DPLL (cross-check) + NDA+VV (new, D-009 同族)")
    print(f"seeds={N_SEEDS}, scenes={SCENES}, DPLL ω_n={OMEGA_N_DPLL:.0e}, VV Nw={NW_VV}")
    print(f"代表性 SNR: {SNR_REPR}")
    print(f"既有对照: run_a3_hybrid_ablation.py (5-seed) 结论 NDA+DPLL FAIL (冗余)")
    print("=" * 100)

    # 自检: hard_decision_m16apsk 对无噪声 tx 返回自身 (守 run_dpll_ablation 模式)
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 64 * 4)
    tx = m16apsk_mod(bits)
    dec = hard_decision_m16apsk(tx)
    assert np.max(np.abs(tx - dec)) < 1e-12, "hard_decision_m16apsk 自检失败"
    print("[自检] hard_decision_m16apsk: PASS")

    results = {}
    partial = False
    for scene in SCENES:
        per_snr, timed_out = run_scene(scene, cfg, t0)
        results[scene] = per_snr
        if timed_out:
            partial = True
            break

    # 互补性判定
    print("\n" + "#" * 40 + " 互补性判定 " + "#" * 40)
    judge = {}
    for combo_key, baselines, label in [
        ('nda_dpll', ['nda', 'dpll'], 'NDA+DPLL vs min(NDA, DPLL)'),
        ('nda_vv', ['nda', 'vv'], 'NDA+VV vs min(NDA, VV)'),
    ]:
        per_combo = {}
        for scene, per_snr in results.items():
            if not per_snr:
                continue
            n_win, n_tot, worst, best = complementarity_judgement(per_snr, combo_key, baselines)
            per_combo[scene] = {
                'n_win_points': n_win, 'n_total_points': n_tot,
                'worst_ratio_combo_over_minbase': worst,
                'best_ratio_combo_over_minbase': best,
                'complementarity': 'WIN' if (n_tot > 0 and n_win == n_tot and (worst or 1) < 1.0) else
                                    ('PARTIAL' if n_win > 0 else 'NO_SIGNAL'),
            }
            print(f"  [{scene}] {label}: win {n_win}/{n_tot} pts, "
                  f"ratio worst={worst:.4f}/best={best:.4f} → {per_combo[scene]['complementarity']}")
        judge[combo_key] = per_combo

    elapsed = time.time() - t0

    # --- 落盘 ---
    out = {
        'meta': {
            'task': 'A3 组合适配扫描 (combo scan): NDA+DPLL 级联 (cross-check) + NDA+VV 级联 (new)',
            'purpose': '验证 NDA+DPLL / NDA+VV 组合是否优于单一 (互补性判据: combo < min 单一)',
            'combos': {
                'nda_dpll': '级联 NDA(块常数粗估)→DPLL(连续跟踪残余), 思路 (b)',
                'nda_vv': '级联 NDA(升幂粗估)→VV(M0=8 滑窗精修), D-009 同族冗余测试',
            },
            'n_seeds': N_SEEDS,
            'scenes': SCENES,
            'snr_repr': SNR_REPR,
            'dpll_params': {'omega_n': OMEGA_N_DPLL, 'zeta': ZETA_DPLL, 'source': 'S011 选定'},
            'vv_params': {'Nw': NW_VV, 'M0': 8, 'source': 'run_vv_ablation vv_cpr_m16apsk'},
            'nda_intra_tracking': {'awgn': 'segmented', 'turb': 'none'},
            'complementarity_criterion': 'combo BER < min(NDA, baseline) 该点互补成立; '
                                         'WIN=全部点赢, PARTIAL=部分点赢, NO_SIGNAL=无点赢',
            'prior_art': 'run_a3_hybrid_ablation.py (5-seed, 6 场景) 结论 NDA+DPLL FAIL (冗余)',
            'channel_bit_exact': '同 seed 同 generate_shared_realization_apsk 重算 (守 TL-13)',
            'M0': P.M0,
            'hdfec': P.HDFEC,
            'partial_run': partial,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'results': to_jsonable(results),
        'complementarity_judgement': to_jsonable(judge),
    }
    out_json = os.path.join(_HERE, '_a3_combo_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 汇总 ---
    print("\n" + "=" * 100)
    print("互补性判定汇总 (combo BER vs min 单一):")
    for combo_key, per in judge.items():
        all_no = all(v['complementarity'] == 'NO_SIGNAL' for v in per.values())
        tag = 'NO_SIGNAL (冗余)' if all_no else '有信号' 
        print(f"  {combo_key}: {tag}")
        for scene, v in per.items():
            print(f"    [{scene}] {v['complementarity']}: {v['n_win_points']}/{v['n_total_points']} pts win, "
                  f"ratio worst={v['worst_ratio_combo_over_minbase']:.4f}")
    print(f"\n[总耗时] {elapsed:.1f} s")
    if partial:
        print(f"[部分运行] time-box 触发")


if __name__ == '__main__':
    main()
