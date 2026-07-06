# -*- coding: utf-8 -*-
"""VV CFR (Viterbi-Viterbi Carrier Phase Recovery) 对比消融 (FR baseline-legitimacy).

回答: VV CFR (Viterbi 1983) 是 NDA 载波同步经典方法, 所有 NDA-ML 论文都引用.
方法上 VV CFR 是 NDA-ML 的"退化版": VV = 升幂 + 滑窗 mean-angle 取角;
NDA-ML = 升幂 + 单正弦 ML 闭式. 理论上 NDA-ML 应优于 VV (ML 闭式比 mean-angle 更优).
如果 NDA-ML 输给 VV CFR → 方向崩了 (危险信号).

VV 现状 (common/_recovery.py:vv_cpr): 已实现 Viterbi 1983 版, 但硬编码 M=4 (QPSK/16-QAM
用), 需适配成 M0=8 ((8,8)-16APSK 升幂阶数, params.py M0_POWER=8, B11 行 75-77).

适配 (选项 A: 不改 common/_recovery.py, 适配在本消融脚本内):
  (1) vv_cpr_m16apsk(rx, Nw): 复制 common.vv_cpr, 改 M=4 升幂 → M0=8 升幂,
      改 M=4 相位模糊展开 → M0=8 展开 (pe = np.unwrap(angle)/M0).

公平性 (§2.4 关键纪律):
  - VV CFR 无 pilot overhead (盲估, 同 NDA): NDA vs VV 公平对照用 γ_d 坐标.
  - VV vs DA 用 γ_tot 坐标 (DA 有 1.249 dB pilot overhead, VV 无 → γ_tot=γ_d).
  - resolve M0-fold 模糊同 NDA-ML 流程 (resolve_m16apsk_blockwise, per-block 选最优旋转).

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0).
  AWGN: seed_base_i = SEED_AWGN + i
  湍流: seed0_i = SEED_TURB0 + i·N_BLOCKS (5 seed 块范围互斥)

信道实现 bit-exact 复现主实验 (守 TL-13): NDA/DA/oracle 不读 results/sc_nda_ml_main/,
而是用同 seed 同 generate_shared_realization_apsk 调用重算 (与 BPS 消融同做法).

运行: cd projects/simulation && python simulator/run_vv_ablation.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 核心算法全从 common/ 导入 (守 TL-13, 不准 import explore/, 不改 sc_nda_ml_sim.py 核心)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402  (复用其公开信道/h 估计 API)
from fair_comparison import analyze_fair_gain, snr_at_ber  # noqa: E402
from params import SimulationConfig  # noqa: E402
from scipy import stats  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_vv_ablation')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# =============================================================================
# VV CFR M16APSK 适配 (选项 A: 在本消融脚本内, 不改 common/_recovery.py)
# =============================================================================
# 滑窗 Nw: common/_recovery.py:vv_cpr 默认 Nw=64. 对齐 N_DFT=256 块内 Nw=64.
# (VV 滑窗 mean-angle 与 BPS Nw 不同尺度: BPS 是距离度量滑窗需更密; VV 是角度均值滑窗,
#  Nw=64 是 common 默认 + Viterbi 1983 推荐量级, 直接用.)
NW_VV_M16 = 64


def vv_cpr_m16apsk(rx, Nw=NW_VV_M16):
    """VV CFR 适配 (8,8)-16APSK (复制 common.vv_cpr, 改 M=4→M0=8).

    升 M0=8 次幂去调制 → 滑窗 mean (→ mean-angle 取角) → unwrap/M0 解 M0-fold 模糊.
    关键: M0=8 unwrap (非 M=4). 来源 common/_recovery.py:vv_cpr, M0=8 依据
    B11 行 75-77 升幂阶数 + params.py M0_POWER=8.
    返回 (rx_compensated, pe).
    """
    M0 = 8
    raised = rx ** M0
    # 幅值保护 (同 common vv_cpr)
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg)) / M0   # M0=8 unwrap (非 M=4)
    return rx * np.exp(-1j * pe), pe


# =============================================================================
# VV BER 评估 (AWGN + 湍流)
# =============================================================================
def ber_vv_awgn(rx, tx_bits):
    """VV-M16APSK AWGN: 逐块 VV-CPR + resolve M0-fold 模糊. 返回 (n_err, n_bits).

    逐块 (N_DFT) 跑 vv_cpr_m16apsk, 再 resolve_m16apsk_blockwise 解 M0=8 模糊
    (同 NDA-ML 流程, per-block 选最优旋转). VV 无 pilot overhead.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _ = vv_cpr_m16apsk(seg)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_vv_turb_eval(rx, tx_bits):
    """VV-M16APSK 湍流: 逐块 VV-CPR (rx 已 per-block h 均衡) + resolve. 返回 (n_err, n_bits).

    同 BPS 消融做法: 先 fft_foe_m0_omega (M0=8 升幂 FOE, 同 NDA-ML 湍流两阶段第一阶段),
    再 per-block VV CPE. 公平: VV 用与 NDA 相同的 FOE 前端 (两阶段对称).
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _ = vv_cpr_m16apsk(seg_foe)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# SNR 扫描: AWGN + 湍流 (VV + 复用主实验 NDA/DA/oracle 重算, bit-exact 守 TL-13)
# =============================================================================
def run_awgn_vv(n_blocks, snr_points, seed_base):
    """AWGN: VV + NDA + DA + oracle BER 扫描. 复用 awgn_wiener_channel (同 seed 派生)."""
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN VV] N_sym={N_sym}/点, Nw={NW_VV_M16}, M0=8 unwrap")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'VV_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = S.awgn_wiener_channel(tx, snr, seed)
        ne_nda, nb_nda = S.ber_nda_awgn(rx, bits)
        ne_da, nb_da = S.ber_da_awgn(rx, bits)
        ne_vv, nb_vv = ber_vv_awgn(rx, bits)
        ne_or, nb_or = S.ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_vv = ne_vv / nb_vv
        b_or = ne_or / nb_or
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_vv:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_vv': float(snr),   # VV 无 pilot overhead
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'vv_ber': b_vv, 'oracle_ber': b_or,
        })
    return per_snr


def run_turb_vv(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0):
    """湍流: VV + NDA + DA + oracle BER 扫描. 复用 generate_shared_realization_apsk."""
    Ns = P.N_DFT
    print(f"[{turb_name} VV] N_sym={n_blocks*Ns}/点, per-block h 均衡 + VV 两阶段 fft_foe+VV CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'VV_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = ne_da = ne_vv = ne_or = 0
        nb_nda = nb_da = nb_vv = nb_or = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (per-block h, 同主实验): VV 用盲 h 估计 (同 NDA, 公平)
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            ne, nb = S.ber_nda_turb_eval(rx_blind, bits)
            ne_nda += ne; nb_nda += nb
            ne, nb = S.ber_da_turb(rx_pilot, bits)
            ne_da += ne; nb_da += nb
            ne, nb = ber_vv_turb_eval(rx_blind, bits)
            ne_vv += ne; nb_vv += nb
            ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
            ne_or += ne; nb_or += nb
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_vv = ne_vv / nb_vv
        b_or = ne_or / nb_or
        print(f"{gamma_db:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_vv:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_vv': float(gamma_db),
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'vv_ber': b_vv, 'oracle_ber': b_or,
        })
    return per_snr


# =============================================================================
# seed 策略 (同主实验)
# =============================================================================
def seed_base_awgn(i):
    return P.SEED_AWGN + i


def seed0_turb(i):
    return P.SEED_TURB0 + i * P.N_BLOCKS


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    if n > 1:
        tval = float(stats.t.ppf(0.975, n - 1))
        hw = tval * std / np.sqrt(n)
    else:
        hw = 0.0
    return mean, std, hw, mean - hw, mean + hw


# =============================================================================
# VV vs NDA / DA 公平 gain 分析
# =============================================================================
def analyze_vv_gain(per_snr, hdfec, pilot_overhead_db):
    """VV vs NDA (γ_d 坐标, 都无 pilot) + VV vs DA (γ_tot 坐标, VV 无 pilot).

    fair_gain_VV_vs_NDA = (VV γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正 = NDA 赢 VV.
    fair_gain_VV_vs_DA  = (DA γ_tot @ HD-FEC) − (VV γ_tot @ HD-FEC)
                          = (DA γ_d @ HD-FEC + overhead) − (VV γ_d @ HD-FEC); 正 = VV 赢 DA.
    """
    snrs = np.array([p['snr_db'] for p in per_snr])
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_vv = np.array([p['vv_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])

    s_nda = snr_at_ber(snrs, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs, b_da, hdfec)
    s_vv = snr_at_ber(snrs, b_vv, hdfec)
    s_or = snr_at_ber(snrs, b_or, hdfec)

    # VV vs NDA (γ_d 坐标, 都无 pilot overhead): 正 = NDA 赢
    gain_vv_vs_nda = None
    if s_vv is not None and s_nda is not None:
        gain_vv_vs_nda = s_vv - s_nda
    # VV vs DA (γ_tot 坐标): 正 = VV 赢 DA
    gain_vv_vs_da = None
    if s_vv is not None and s_da_d is not None:
        gain_vv_vs_da = (s_da_d + pilot_overhead_db) - s_vv

    # 逐点 (γ_d 坐标): VV 达 NDA BER 所需 γ_d − NDA γ_d
    per_point_vv_vs_nda = []
    for i, gd in enumerate(snrs):
        ber_nda_at = b_nda[i]
        s_vv_needed = snr_at_ber(snrs, b_vv, ber_nda_at)
        if s_vv_needed is not None:
            per_point_vv_vs_nda.append({
                'gamma_d_db': float(gd),
                'ber_nda': float(ber_nda_at),
                'snr_vv_needed_db': float(s_vv_needed),
                'vv_vs_nda_gain_db': float(s_vv_needed - gd),   # 正 = NDA 赢 VV
            })

    hdfec_reachable = (s_vv is not None and s_nda is not None)

    return {
        'snr_nda_d_at_hdfec': s_nda,
        'snr_da_tot_at_hdfec': (s_da_d + pilot_overhead_db) if s_da_d is not None else None,
        'snr_vv_d_at_hdfec': s_vv,
        'snr_oracle_at_hdfec': s_or,
        'gain_vv_vs_nda_db': gain_vv_vs_nda,      # 正 = NDA 赢 VV
        'gain_vv_vs_da_db': gain_vv_vs_da,         # 正 = VV 赢 DA
        'hdfec_reachable': hdfec_reachable,
        'per_point_vv_vs_nda': per_point_vv_vs_nda,
        'min_vv_ber': float(np.min(b_vv)),
    }


# =============================================================================
# 主
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


def run_all(t_start, time_budget=840.0):
    """跑全部场景. time_budget=840s (14 min, 留 1 min 缓冲 < 15 min 上限).
    若超时, 跑完当前场景即停 (返回 partial=True)."""
    cfg = SimulationConfig()
    raw = {sc: {} for sc in SCENES}
    scenes_done = []

    print("=" * 100)
    print(f"VV CFR M-APSK 迁移消融: {N_SEEDS} seed × {len(SCENES)} 场景")
    print(f"Nw={NW_VV_M16}, M0=8 unwrap (非 M=4)")
    print(f"AWGN seed_base: {[seed_base_awgn(i) for i in range(N_SEEDS)]}")
    print(f"湍流 seed0   : {[seed0_turb(i) for i in range(N_SEEDS)]}")
    print("=" * 100)

    # --- AWGN ---
    for i in range(N_SEEDS):
        if time.time() - t_start > time_budget:
            print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 AWGN seed {i}")
            return raw, scenes_done, True
        sb = seed_base_awgn(i)
        print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
        raw['awgn'][i] = run_awgn_vv(P.N_BLOCKS, P.SNR_AWGN_DB, sb)
    scenes_done.append('awgn')

    # --- 湍流 ---
    for turb in TURB_LEVELS:
        for i in range(N_SEEDS):
            if time.time() - t_start > time_budget:
                print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 {turb} seed {i}")
                return raw, scenes_done, True
            s0 = seed0_turb(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = run_turb_vv(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)
        scenes_done.append(turb)
    return raw, scenes_done, False


def aggregate(raw, scenes_done):
    summary = {}
    for sc in scenes_done:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        n_sd = len(per_seed)
        points = []
        for j, snr in enumerate(snrs):
            nda = [per_seed[i][j]['nda_ml_ber'] for i in range(n_sd)]
            da = [per_seed[i][j]['da_ml_ber'] for i in range(n_sd)]
            vv = [per_seed[i][j]['vv_ber'] for i in range(n_sd)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(n_sd)]
            m_nda, s_nda, hw_nda, lo_nda, hi_nda = ci_t(nda)
            m_da, s_da, hw_da, lo_da, hi_da = ci_t(da)
            m_vv, s_vv, hw_vv, lo_vv, hi_vv = ci_t(vv)
            m_or, s_or, hw_or, lo_or, hi_or = ci_t(orc)
            points.append({
                'snr_db': float(snr),
                'nda_ml_ber_mean': m_nda, 'nda_ml_ber_std': s_nda,
                'nda_ml_ber_ci95': [lo_nda, hi_nda],
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'da_ml_ber_ci95': [lo_da, hi_da],
                'vv_ber_mean': m_vv, 'vv_ber_std': s_vv,
                'vv_ber_ci95': [lo_vv, hi_vv],
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
                'oracle_ber_ci95': [lo_or, hi_or],
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def vv_gain_per_seed(raw, scenes_done):
    out = {}
    for sc in scenes_done:
        per_seed = raw[sc]
        n_sd = len(per_seed)
        gains_vv_nda = []
        gains_vv_da = []
        wr_vv_vs_nda = {}   # strong 工作区 per-point
        for i in range(n_sd):
            per_snr = per_seed[i]
            fg = analyze_vv_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            gains_vv_nda.append(fg['gain_vv_vs_nda_db'])
            gains_vv_da.append(fg['gain_vv_vs_da_db'])
            for p in fg['per_point_vv_vs_nda']:
                if p['gamma_d_db'] >= 15.0:
                    wr_vv_vs_nda.setdefault(p['gamma_d_db'], []).append(
                        float(p['vv_vs_nda_gain_db']))
        entry = {
            'per_seed_gain_vv_vs_nda_db': [None if g is None else float(g) for g in gains_vv_nda],
            'per_seed_gain_vv_vs_da_db': [None if g is None else float(g) for g in gains_vv_da],
        }
        v_nda = [g for g in gains_vv_nda if g is not None]
        v_da = [g for g in gains_vv_da if g is not None]
        if len(v_nda) >= 2:
            m, s, hw, lo, hi = ci_t(v_nda)
            entry.update({'gain_vv_vs_nda_mean_db': m, 'gain_vv_vs_nda_std_db': s,
                          'gain_vv_vs_nda_ci95_db': [lo, hi], 'n_valid_nda': len(v_nda)})
        else:
            entry.update({'gain_vv_vs_nda_mean_db': None, 'gain_vv_vs_nda_std_db': None,
                          'gain_vv_vs_nda_ci95_db': [None, None], 'n_valid_nda': len(v_nda)})
        if len(v_da) >= 2:
            m, s, hw, lo, hi = ci_t(v_da)
            entry.update({'gain_vv_vs_da_mean_db': m, 'gain_vv_vs_da_std_db': s,
                          'gain_vv_vs_da_ci95_db': [lo, hi], 'n_valid_da': len(v_da)})
        else:
            entry.update({'gain_vv_vs_da_mean_db': None, 'gain_vv_vs_da_std_db': None,
                          'gain_vv_vs_da_ci95_db': [None, None], 'n_valid_da': len(v_da)})
        # strong 工作区 per-point
        if sc == 'strong' and wr_vv_vs_nda:
            wr_points = []
            all_wr = []
            for gd in sorted(wr_vv_vs_nda.keys()):
                col = wr_vv_vs_nda[gd]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({'gamma_d_db': float(gd), 'n_seeds': len(col),
                                  'vv_vs_nda_gain_mean_db': m, 'vv_vs_nda_gain_std_db': s,
                                  'vv_vs_nda_gain_ci95_db': [lo, hi]})
                all_wr.extend(col)
            entry['workregion_vv_vs_nda_per_point'] = wr_points
            gm, gs, ghw, glo, ghi = ci_t(all_wr)
            entry['workregion_vv_vs_nda_grand_mean_db'] = gm
            entry['workregion_vv_vs_nda_grand_std_db'] = gs
            entry['workregion_vv_vs_nda_grand_ci95_db'] = [glo, ghi]
        out[sc] = entry
    return out


def consistency_check(summary, vv_gain, scenes_done):
    """MVE 一致性自检 (守 TL-23):
      (1) VV BER 应全程 ≥ oracle (如果 < oracle 一定 bug)
      (2) VV BER 应全程 ≥ NDA-ML (理论上 NDA-ML 优于 VV)
      (3) VV BER @ 18dB AWGN 合理范围: 跟 BPS 同量级 (0.003-0.005)
    返回 dict of check results.
    """
    checks = {}
    # (1) VV >= oracle (逐 SNR, 逐场景)
    for sc in scenes_done:
        pts = summary[sc]['points']
        violations_oracle = []
        for p in pts:
            vv_m = p['vv_ber_mean']
            or_m = p['oracle_ber_mean']
            # VV 应 >= oracle (允许统计噪声小裕度: VV 均值不低于 oracle 均值的 0.9)
            if vv_m < or_m * 0.9:
                violations_oracle.append({
                    'snr_db': p['snr_db'],
                    'vv_ber': vv_m, 'oracle_ber': or_m,
                    'ratio': vv_m / or_m if or_m > 0 else None,
                })
        checks.setdefault('vv_ge_oracle', {})[sc] = {
            'pass': len(violations_oracle) == 0,
            'n_violations': len(violations_oracle),
            'violations': violations_oracle[:5],
        }
    # (2) VV >= NDA (逐 SNR, 逐场景)
    for sc in scenes_done:
        pts = summary[sc]['points']
        violations_nda = []
        for p in pts:
            vv_m = p['vv_ber_mean']
            nda_m = p['nda_ml_ber_mean']
            # VV 应 >= NDA (允许统计噪声小裕度: VV 均值不低于 NDA 均值的 0.9)
            if vv_m < nda_m * 0.9:
                violations_nda.append({
                    'snr_db': p['snr_db'],
                    'vv_ber': vv_m, 'nda_ber': nda_m,
                    'ratio': vv_m / nda_m if nda_m > 0 else None,
                })
        checks.setdefault('vv_ge_nda', {})[sc] = {
            'pass': len(violations_nda) == 0,
            'n_violations': len(violations_nda),
            'violations': violations_nda[:5],
        }
    # (3) VV @ 18dB AWGN 量级检查
    vv_at_18 = None
    if 'awgn' in summary:
        for p in summary['awgn']['points']:
            if abs(p['snr_db'] - 18.0) < 1e-6:
                vv_at_18 = p['vv_ber_mean']
    checks['vv_at_18db_awgn'] = {
        'value': vv_at_18,
        'expected_range': [0.003, 0.005],
        'pass': (vv_at_18 is not None and 0.001 <= vv_at_18 <= 0.01),   # 宽 10x 容差 (BPS 同量级)
    }
    all_pass = (all(checks['vv_ge_oracle'][sc]['pass'] for sc in scenes_done)
                and all(checks['vv_ge_nda'][sc]['pass'] for sc in scenes_done)
                and checks['vv_at_18db_awgn']['pass'])
    checks['all_pass'] = all_pass
    return checks


def plot_curves(summary, scenes_done, vv_gain):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    titles = {'awgn': 'AWGN', 'weak': 'weak (α4/β3)',
              'moderate': 'moderate (α2.5/β1.8)', 'strong': 'strong (α1.5/β0.8)'}
    n = len(scenes_done)
    fig, axes = plt.subplots(1, n, figsize=(5.5 * n, 5.2))
    if n == 1:
        axes = [axes]
    for ax, sc in zip(axes, scenes_done):
        pts = summary[sc]['points']
        gts = [p['snr_db'] for p in pts]
        nda_m = np.array([p['nda_ml_ber_mean'] for p in pts])
        da_m = np.array([p['da_ml_ber_mean'] for p in pts])
        vv_m = np.array([p['vv_ber_mean'] for p in pts])
        or_m = np.array([p['oracle_ber_mean'] for p in pts])
        nda_lo = np.array([p['nda_ml_ber_ci95'][0] for p in pts])
        nda_hi = np.array([p['nda_ml_ber_ci95'][1] for p in pts])
        vv_lo = np.array([p['vv_ber_ci95'][0] for p in pts])
        vv_hi = np.array([p['vv_ber_ci95'][1] for p in pts])
        ax.semilogy(gts, nda_m, 'o-', color='C0', label='NDA-ML (M0=8)', lw=1.8)
        ax.fill_between(gts, np.maximum(nda_lo, 1e-6), nda_hi, color='C0', alpha=0.18)
        ax.semilogy(gts, da_m, 's-', color='C1', label='DA ML (sp=4)', lw=1.8)
        ax.semilogy(gts, vv_m, 'D-', color='C3', label=f'VV CFR (Nw={NW_VV_M16})', lw=1.8)
        ax.fill_between(gts, np.maximum(vv_lo, 1e-6), vv_hi, color='C3', alpha=0.18)
        ax.semilogy(gts, or_m, '^--', color='C2', label='oracle', lw=1.6)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        fg = vv_gain[sc]
        if fg.get('gain_vv_vs_nda_mean_db') is not None:
            ttl = (f"{titles[sc]}\nVV vs NDA: {fg['gain_vv_vs_nda_mean_db']:+.2f}"
                   f"±{fg['gain_vv_vs_nda_std_db']:.2f} dB (正=NDA赢)")
        elif sc == 'strong':
            ttl = (f"{titles[sc]}\n工作区 VV vs NDA: "
                   f"{fg.get('workregion_vv_vs_nda_grand_mean_db', 0):+.2f} dB")
        else:
            ttl = titles[sc]
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7.5, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('VV CFR 迁移消融: NDA-ML vs DA ML vs VV CFR vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=11, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_vv_ablation_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return png


def main():
    t0 = time.time()
    print("=" * 100)
    print("VV CFR (Viterbi-Viterbi Carrier Phase Recovery) M-APSK 迁移对比消融")
    print(f"M0={P.M0}, Nw={NW_VV_M16}, pilot_overhead={P.PILOT_OVERHEAD_DB:.3f} dB, HDFEC={P.HDFEC}")
    print(f"common/_recovery.py 未改动 (选项 A, 适配在本脚本内)")
    print("=" * 100)

    # --- 跑 ---
    raw, scenes_done, partial = run_all(t0)
    elapsed = time.time() - t0

    # --- 聚合 ---
    summary = aggregate(raw, scenes_done)
    vv_gain = vv_gain_per_seed(raw, scenes_done)

    # --- MVE 一致性自检 ---
    checks = consistency_check(summary, vv_gain, scenes_done)
    print("\n" + "=" * 100)
    print("MVE 一致性自检 (守 TL-23):")
    print(f"  VV >= oracle (全场景): {all(checks['vv_ge_oracle'][sc]['pass'] for sc in scenes_done)}")
    for sc in scenes_done:
        c = checks['vv_ge_oracle'][sc]
        if not c['pass']:
            print(f"    [{sc}] 违反 {c['n_violations']} 点: {c['violations']}")
    print(f"  VV >= NDA (全场景): {all(checks['vv_ge_nda'][sc]['pass'] for sc in scenes_done)}")
    for sc in scenes_done:
        c = checks['vv_ge_nda'][sc]
        if not c['pass']:
            print(f"    [{sc}] 违反 {c['n_violations']} 点: {c['violations']}")
    v18 = checks['vv_at_18db_awgn']
    print(f"  VV @ 18dB AWGN = {v18['value']}, 合理范围 {v18['expected_range']}: {v18['pass']}")
    print(f"  ALL PASS: {checks['all_pass']}")

    # --- 画图 ---
    try:
        png_path = plot_curves(summary, scenes_done, vv_gain)
        print(f"\n[PNG] {png_path}")
    except Exception as e:
        print(f"(PNG skipped: {e})")
        png_path = None

    # --- 落盘 _vv_ablation_5seed.json ---
    out = {
        'meta': {
            'task': 'VV CFR (Viterbi-Viterbi) M-APSK 迁移对比消融 (5 seed 多种子统计)',
            'purpose': '验证 NDA-ML 优于 VV CFR (NDA-ML 退化版). 输给 VV = 方向崩了',
            'metric': 'BER 曲线 + VV vs NDA (γ_d) + VV vs DA (γ_tot) fair gain @ HD-FEC + 95% CI',
            'n_seeds': N_SEEDS,
            'scenes_done': scenes_done,
            'partial_run': partial,
            'vv_adaptation': {
                'vv_cpr_m16apsk': '复制 common.vv_cpr, 改 M=4 升幂 → M0=8 升幂',
                'M0_unwrap': 'M0=8 (非 M=4), pe=unwrap(angle)/M0 (B11 行 75-77 升幂阶数)',
                'Nw_window': NW_VV_M16,
                'Nw_choice_reason': 'common/_recovery.py:vv_cpr 默认 Nw=64 + Viterbi 1983 推荐量级',
                'common_recovery_modified': False,
            },
            'fairness': {
                'vv_vs_nda': 'γ_d 坐标 (都无 pilot overhead, 同类盲估)',
                'vv_vs_da': 'γ_tot 坐标 (DA 有 1.249 dB pilot overhead, VV 无)',
                'resolve': 'resolve_m16apsk_blockwise (per-block M0-fold 模糊, 同 NDA-ML 流程)',
                'channel_bit_exact': 'NDA/DA/oracle 同 seed 同 generate_shared_realization_apsk 重算 (守 TL-13)',
            },
            'seed_strategy': {
                'awgn': 'seed_base_i = SEED_AWGN + i',
                'turbulence': 'seed0_i = SEED_TURB0 + i*N_BLOCKS (5 seed 块范围互斥)',
                'note': 'seed 0 = MVE seed (可复现)',
            },
            'M0': P.M0,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'hdfec': P.HDFEC,
            'ci_method': f't-distribution 95% CI, df=n-1 (5 seed→df=4, t={T05_4:.4f})',
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'summary': to_jsonable(summary),
        'vv_gain_per_seed': to_jsonable(vv_gain),
        'consistency_checks': to_jsonable(checks),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_vv_ablation_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 落盘 _vv_ablation_summary.json (精简) ---
    fair_short = {}
    for sc in scenes_done:
        e = vv_gain[sc]
        entry = {
            'scene': sc,
            'gain_vv_vs_nda_mean_db': e.get('gain_vv_vs_nda_mean_db'),
            'gain_vv_vs_nda_std_db': e.get('gain_vv_vs_nda_std_db'),
            'gain_vv_vs_nda_ci95_db': e.get('gain_vv_vs_nda_ci95_db'),
            'per_seed_gain_vv_vs_nda_db': e.get('per_seed_gain_vv_vs_nda_db'),
            'gain_vv_vs_da_mean_db': e.get('gain_vv_vs_da_mean_db'),
            'gain_vv_vs_da_std_db': e.get('gain_vv_vs_da_std_db'),
            'gain_vv_vs_da_ci95_db': e.get('gain_vv_vs_da_ci95_db'),
            'per_seed_gain_vv_vs_da_db': e.get('per_seed_gain_vv_vs_da_db'),
            'n_valid_nda': e.get('n_valid_nda'),
            'n_valid_da': e.get('n_valid_da'),
        }
        if sc == 'strong':
            entry['note'] = 'HD-FEC 物理不可达 (oracle 也不可达); 用工作区 (γ_d≥15dB) per-point'
            entry['workregion_vv_vs_nda_grand_mean_db'] = e.get('workregion_vv_vs_nda_grand_mean_db')
            entry['workregion_vv_vs_nda_grand_std_db'] = e.get('workregion_vv_vs_nda_grand_std_db')
            entry['workregion_vv_vs_nda_grand_ci95_db'] = e.get('workregion_vv_vs_nda_grand_ci95_db')
            entry['workregion_vv_vs_nda_per_point'] = e.get('workregion_vv_vs_nda_per_point')
        fair_short[sc] = entry
    summary_json = {
        'meta': {
            'task': 'VV CFR M-APSK 迁移消融 fair gain 汇总 (5 seed)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': {
                'vv_vs_nda': 'fair_gain = (VV γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正=NDA赢VV',
                'vv_vs_da': 'fair_gain = (DA γ_tot @ HD-FEC) − (VV γ_tot @ HD-FEC); 正=VV赢DA',
            },
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'scenes_done': scenes_done,
            'partial_run': partial,
            'Nw_window': NW_VV_M16,
            'M0_unwrap': 8,
            'common_recovery_modified': False,
            'consistency_all_pass': checks['all_pass'],
            'elapsed_sec': float(elapsed),
        },
        'fair_gain': fair_short,
        'consistency_checks': to_jsonable(checks),
    }
    sj_path = os.path.join(OUT_DIR, '_vv_ablation_summary.json')
    with open(sj_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(summary_json), f, indent=2, ensure_ascii=False)
    print(f"[保存] {sj_path}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("VV CFR 迁移消融 fair gain @ HD-FEC (5 seed):")
    print(f"{'场景':>10} {'VV vs NDA':>22} {'VV反超NDA?':>14} {'VV vs DA':>22} {'VV赢DA?':>12}")
    for sc in scenes_done:
        e = vv_gain[sc]
        gn = e.get('gain_vv_vs_nda_mean_db')
        gd = e.get('gain_vv_vs_da_mean_db')
        if gn is not None:
            ci_n = e['gain_vv_vs_nda_ci95_db']
            overtake = '是⚠️' if gn < 0 else '否'
            print(f"{sc:>10} {gn:>+10.3f}±{e['gain_vv_vs_nda_std_db']:.2f} "
                  f"[{ci_n[0]:>+6.2f},{ci_n[1]:>+6.2f}] {overtake:>14}", end='')
        elif sc == 'strong':
            wr = e.get('workregion_vv_vs_nda_grand_mean_db', 0)
            wrs = e.get('workregion_vv_vs_nda_grand_std_db', 0)
            overtake = '是⚠️' if wr < 0 else '否'
            print(f"{sc:>10} 工作区{wr:>+7.3f}±{wrs:.2f} dB {overtake:>20}", end='')
        if gd is not None:
            ci_d = e['gain_vv_vs_da_ci95_db']
            vv_win_da = '是' if gd > 0 else '否'
            print(f" {gd:>+10.3f}±{e['gain_vv_vs_da_std_db']:.2f} "
                  f"[{ci_d[0]:>+6.2f},{ci_d[1]:>+6.2f}] {vv_win_da:>12}")
        else:
            print()
    if partial:
        print(f"\n[部分运行] 仅完成场景: {scenes_done} (time-box 触发)")
    print(f"\n[一致性自检] ALL PASS = {checks['all_pass']}")
    print(f"[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
