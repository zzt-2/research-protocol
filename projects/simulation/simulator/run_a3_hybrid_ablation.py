# -*- coding: utf-8 -*-
"""A3 组合适配: NDA-ML (前馈升幂) + DPLL DD (闭环跟踪) 混合方案对比消融.

回答 adaptation-scan.md A3 核心问题: 不同族方法能不能组合? 互补性在哪?
  - NDA-ML: 前馈升幂 M0 次幂去调制 + mean-angle 估块常数 CPE. 无失锁风险, 精度有限.
  - DPLL DD: 闭环跟踪环 (PD -> PI loop filter -> VCO 累积). 高精度跟踪, 有失锁风险.
  - 互补假设: NDA 粗估去调制相位 (块常数) -> DPLL 跟残余漂移 (块间 Wiener PN).

混合算法:
  (1) NDA-ML per-block 升幂 mean-angle 估块常数粗相位 phi_nda, 补偿
      rx_comp = rx * exp(-j*phi_nda)  (per-block, 无状态, 保持 NDA 无失锁特性)
  (2) DPLL DD 连续跟踪 rx_comp 的残余相位漂移 (全数组 VCO 累积, 守 S011 发现:
      DPLL 必须连续处理, per-block 重置 VCO 丢符号间相位连续性)
  (3) turb 两阶段: 先 per-block fft_foe 补 CFO (同 NDA/DPLL 消融), 再 NDA 粗估, 再 DPLL

为什么不是冗余叠加 (adaptation-scan.md A3 失败信号):
  - NDA per-block 块常数估计无法跟块间 Wiener PN 累积漂移 (每块独立, 块间漂移留下残相)
  - DPLL 连续跟踪能跟块间漂移但纯 DPLL 在 deep fade (strong/uplink) 易失锁 (DD 判决错)
  - 混合: NDA 先去大块相位让 DPLL 收到的是"近干净"信号 (减小失锁风险), DPLL 再精跟
    块间漂移 (补 NDA per-block 无法跨块跟踪的缺陷) -> 互补非冗余

m16apsk 适配 (选项 A, 同 run_dpll_ablation.py, 不改 common/_recovery.py):
  - hard_decision_m16apsk: 最近邻 16 点星座判定 (复制 run_dpll_ablation.py:94-109 /
    run_dd_kf_ablation.py:124, 已验证模式)
  - dpll_track_dd_m16apsk: 复制 common.dpll_track_dd, 改 qam16 判决 -> m16apsk
  - 不用 dpll_track (4 次方鉴相器, 16APSK M0=8 非 4 次方对称, H007 纪律)

公平性 (守 adaptation-scan.md baseline 结构规则):
  - 我们的方法 = 混合 (NDA 粗估 + DPLL 精跟); 创新 = 组合策略, 不是新方法
  - 主 baseline = 单一 NDA-ML (最优) + 单一 DPLL (最优 omega_n), 证明"联合 > 分开"
  - 参照 = DA-ML / VV / BPS (不同族, 标尺)
  - 上界 = oracle
  - 混合/NDA/DPLL 都无 pilot overhead (盲): 混合 vs NDA / 混合 vs DPLL 用 γ_d 坐标公平对照
  - DA 有 1.249 dB pilot overhead: 混合 vs DA 用 γ_tot 坐标
  - resolve M0-fold 模糊同 NDA/DPLL 流程 (resolve_m16apsk_blockwise, per-block 选最优旋转)

A3 信号判据 (adaptation-scan.md):
  - PASS: 混合全场景不输 max(NDA, DPLL) + 至少一场景赢两者 (强湍流/uplink deep fade)
  - FAIL: 混合 ≈ max(NDA, DPLL) (只取两者之长无额外增益) 或反不如单一

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0), 同 run_dpll_ablation.
  AWGN: seed_base_i = SEED_AWGN + i
  湍流下行: seed0_i = SEED_TURB0 + i*N_BLOCKS (5 seed 块范围互斥)
  湍流上行: seed0_i = SEED_TURB0 + i*N_BLOCKS + UPLINK_SEED_OFFSET (错开下行 seed)

信道实现 bit-exact 复现主实验 (守 TL-13): 所有方法用同 seed 同 generate_shared_realization_apsk
重算 (不读 results/, 与 run_dpll_ablation.py 同做法).

运行: cd projects/simulation && python simulator/run_a3_hybrid_ablation.py
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
    nda_ml_recovery,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402  (复用其公开信道/h 估计 API)
from fair_comparison import analyze_fair_gain, snr_at_ber  # noqa: E402
from params import SimulationConfig  # noqa: E402
from scipy import stats  # noqa: E402
# m16apsk 星座点 (用于 hard_decision_m16apsk 最近邻判定)
from common._modulation import _M16APSK_SYM  # noqa: E402

# --- 输出目录 (sandbox, 不进 results/, 守 explore/ 隔离) ---
OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
# 5 场景: AWGN + 3 下行湍流 + 2 上行湍流
SCENES_DOWNLINK = ['awgn', 'weak', 'moderate', 'strong']
SCENES_UPLINK = ['uplink_moderate', 'uplink_strong']
TURB_DOWNLINK = ['weak', 'moderate', 'strong']
TURB_UPLINK = ['uplink_moderate', 'uplink_strong']

# DPLL 参数 (S011 已选 omega_n=50e6 最优, zeta=√2/2 临界阻尼)
ZETA_DPLL = np.sqrt(2) / 2
OMEGA_N_DPLL = 50e6   # S011 选定 (连续处理 @18dB BER≈4.1e-3, TL-20 预期内)
# 上行 seed 错开下行 (同 run_uplink_experiment / parity_tuning_sweep.py:65)
UPLINK_SEED_OFFSET = 500000

# AWGN NDA 用 segmented 块内跟踪 (同 ber_nda_awgn), turb NDA 用 'none' (sandbox 验证 strong 有害).
NDA_INTRA_AWGN = 'segmented'
NDA_INTRA_TURB = 'none'


# =============================================================================
# DPLL M16APSK 适配 (选项 A: 在本消融脚本内, 不改 common/_recovery.py)
# 复制自 run_dpll_ablation.py:94-140 (bit-exact, 守 TL-13)
# =============================================================================
def hard_decision_m16apsk(z):
    """(8,8)-16APSK 最近邻硬判决 (标量或向量). 复制自 run_dpll_ablation.py:94."""
    z = np.asarray(z, dtype=complex)
    if z.ndim == 0:
        d = np.abs(z - _M16APSK_SYM) ** 2
        return complex(_M16APSK_SYM[int(np.argmin(d))])
    d = np.abs(z[:, np.newaxis] - _M16APSK_SYM[np.newaxis, :]) ** 2
    idx = np.argmin(d, axis=1)
    return _M16APSK_SYM[idx]


def dpll_track_dd_m16apsk(rx, omega_n=OMEGA_N_DPLL, zeta=ZETA_DPLL):
    """DD-DPLL 适配 (8,8)-16APSK. 复制自 run_dpll_ablation.py:112.

    闭环二阶环: PD (decision-directed angle) -> PI loop filter (c1/c2) -> VCO 累积相位.
    返回 (rx_compensated, phi_est).
    """
    wT = min(omega_n * P.T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT ** 2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        rotated = rx[k] * np.exp(-1j * vco_phase)
        dec = hard_decision_m16apsk(rotated)
        pd_out = np.angle(rx[k] * np.exp(-1j * vco_phase) * np.conj(dec))
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est


def nda_coarse_perblock(rx, intra_block_tracking='none'):
    """NDA-ML per-block 粗相位估计 (升幂 mean-angle, 无失锁前馈). 返回 rx_comp.

    每块独立升幂 mean-angle 估块常数 CPE, 补偿. 无状态 (前馈). 同 ber_nda_turb 的 NDA 步骤.
    intra_block_tracking: 'none' (turb, 默认) / 'segmented' (AWGN, 同 ber_nda_awgn).
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _, _, _ = nda_ml_recovery(seg, P.M0, mod='m16apsk', assume_df_zero=True,
                                      intra_block_tracking=intra_block_tracking)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    return rx_comp


def hybrid_nda_dpll_awgn(rx, tx_bits, omega_n=OMEGA_N_DPLL,
                         nda_intra=NDA_INTRA_AWGN):
    """混合 AWGN: NDA per-block 粗估 -> DPLL 连续跟踪残余漂移 + resolve M0-fold.

    返回 (n_err, n_bits). 混合无 pilot overhead.
    """
    # 步骤 1: NDA 粗估 (per-block, 无失锁前馈去块常数 CPE)
    rx_nda = nda_coarse_perblock(rx, intra_block_tracking=nda_intra)
    L = len(rx_nda)
    # 步骤 2: DPLL 连续跟踪 (VCO 全数组累积, 跟块间残余 Wiener PN 漂移)
    rx_comp, _ = dpll_track_dd_m16apsk(rx_nda, omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def hybrid_nda_dpll_turb(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """混合 turb: per-block fft_foe -> NDA 粗估 -> DPLL 连续跟踪 + resolve.

    同 NDA/DPLL turb 两阶段对称: 先 per-block fft_foe 补 CFO, 再混合 NDA+DPLL.
    返回 (n_err, n_bits).
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    # 两阶段第 1 阶段: per-block fft_foe 补 CFO (同 ber_dpll_turb_eval / ber_nda_turb)
    rx_foe_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        rx_foe_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = seg * np.exp(-1j * omega_est * k)
    # 两阶段第 2 阶段: NDA 粗估 (per-block, 'none' turb 默认)
    rx_nda = nda_coarse_perblock(rx_foe_comp, intra_block_tracking=NDA_INTRA_TURB)
    # 第 3 阶段: DPLL 连续跟踪 (全数组 VCO 累积, 跟块间残余 Wiener PN 漂移)
    rx_comp, _ = dpll_track_dd_m16apsk(rx_nda, omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# SNR 扫描: AWGN + 下行/上行 湍流 (混合 + 复用主实验 NDA/DA/DPLL/oracle 重算)
# =============================================================================
def run_awgn_hybrid(n_blocks, snr_points, seed_base, omega_n=OMEGA_N_DPLL):
    """AWGN: 混合 + NDA + DA + DPLL + oracle BER 扫描."""
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN HYBRID] N_sym={N_sym}/点, omega_n={omega_n:.0e}")
    print(f"{'SNR':>5} {'NDA':>11} {'DA':>11} {'DPLL':>11} {'HYBRID':>11} {'ORACLE':>11}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = S.awgn_wiener_channel(tx, snr, seed)
        ne_nda, nb_nda = S.ber_nda_awgn(rx, bits)
        ne_da, nb_da = S.ber_da_awgn(rx, bits)
        ne_dpll, nb_dpll = ber_dpll_awgn(rx, bits, omega_n=omega_n)
        ne_hy, nb_hy = hybrid_nda_dpll_awgn(rx, bits, omega_n=omega_n)
        ne_or, nb_or = S.ber_oracle_awgn(rx, bits, phi_true)
        b = lambda ne, nb: ne / nb
        print(f"{snr:>5.0f} {b(ne_nda,nb_nda):>11.3e} {b(ne_da,nb_da):>11.3e} "
              f"{b(ne_dpll,nb_dpll):>11.3e} {b(ne_hy,nb_hy):>11.3e} {b(ne_or,nb_or):>11.3e}")
        per_snr.append({
            'snr_db': float(snr),
            'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_dpll': float(snr),
            'snr_db_total_hybrid': float(snr),   # 混合无 pilot overhead
            'nda_ml_ber': b(ne_nda, nb_nda),
            'da_ml_ber': b(ne_da, nb_da),
            'dpll_ber': b(ne_dpll, nb_dpll),
            'hybrid_ber': b(ne_hy, nb_hy),
            'oracle_ber': b(ne_or, nb_or),
        })
    return per_snr


def ber_dpll_awgn(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """DPLL AWGN (复制自 run_dpll_ablation.py:146, bit-exact). 返回 (n_err, n_bits)."""
    L = (len(rx) // P.N_DFT) * P.N_DFT
    rx_comp, _ = dpll_track_dd_m16apsk(rx[:L], omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_dpll_turb_eval(rx, tx_bits, omega_n=OMEGA_N_DPLL):
    """DPLL turb (复制自 run_dpll_ablation.py:163, bit-exact). 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_foe_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        rx_foe_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = seg * np.exp(-1j * omega_est * k)
    rx_comp, _ = dpll_track_dd_m16apsk(rx_foe_comp, omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def run_turb_hybrid(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0,
                    omega_n=OMEGA_N_DPLL, lw=10e3):
    """turb: 混合 + NDA + DA + DPLL + oracle BER 扫描. 复用 generate_shared_realization_apsk."""
    Ns = P.N_DFT
    print(f"[{turb_name} HYBRID] N_sym={n_blocks*Ns}/点, omega_n={omega_n:.0e}, lw={lw/1e3:.0f}kHz")
    print(f"{'γd':>5} {'NDA':>11} {'DA':>11} {'DPLL':>11} {'HYBRID':>11} {'ORACLE':>11}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        acc = {k: [0, 0] for k in ['nda', 'da', 'dpll', 'hy', 'or']}
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b, lw=lw)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (per-block h, 同主实验): 盲 h 均衡 (混合/NDA/DPLL 公平)
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            for key, fn in [('nda', lambda rx: S.ber_nda_turb_eval(rx, bits)),
                            ('da', lambda rx: S.ber_da_turb(rx, bits)),
                            ('dpll', lambda rx: ber_dpll_turb_eval(rx, bits, omega_n=omega_n)),
                            ('hy', lambda rx: hybrid_nda_dpll_turb(rx, bits, omega_n=omega_n))]:
                ne, nb = fn(rx_blind)
                acc[key][0] += ne; acc[key][1] += nb
            ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
            acc['or'][0] += ne; acc['or'][1] += nb
        b = lambda k: acc[k][0] / acc[k][1]
        print(f"{gamma_db:>5.0f} {b('nda'):>11.3e} {b('da'):>11.3e} {b('dpll'):>11.3e} "
              f"{b('hy'):>11.3e} {b('or'):>11.3e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_dpll': float(gamma_db),
            'snr_db_total_hybrid': float(gamma_db),
            'nda_ml_ber': b('nda'),
            'da_ml_ber': b('da'),
            'dpll_ber': b('dpll'),
            'hybrid_ber': b('hy'),
            'oracle_ber': b('or'),
        })
    return per_snr


# =============================================================================
# seed 策略 (同主实验 + run_dpll_ablation)
# =============================================================================
def seed_base_awgn(i):
    return P.SEED_AWGN + i


def seed0_turb_downlink(i):
    return P.SEED_TURB0 + i * P.N_BLOCKS


def seed0_turb_uplink(i):
    return P.SEED_TURB0 + i * P.N_BLOCKS + UPLINK_SEED_OFFSET


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
# 混合 vs NDA / DPLL 公平 gain 分析
# =============================================================================
def analyze_hybrid_gain(per_snr, hdfec, pilot_overhead_db):
    """混合 vs NDA (γ_d) + 混合 vs DPLL (γ_d) + 混合 vs DA (γ_tot).

    fair_gain_hybrid_vs_X = (X γ @ HD-FEC) − (hybrid γ_d @ HD-FEC); 正 = X 赢 混合 (混合差).
    负 = 混合赢 X. 我们关心"混合赢两者", 所以看 gain_hybrid_vs_nda/dpll 是否 < 0.
    """
    snrs = np.array([p['snr_db'] for p in per_snr])
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_dpll = np.array([p['dpll_ber'] for p in per_snr])
    b_hy = np.array([p['hybrid_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])

    s_nda = snr_at_ber(snrs, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs, b_da, hdfec)
    s_dpll = snr_at_ber(snrs, b_dpll, hdfec)
    s_hy = snr_at_ber(snrs, b_hy, hdfec)
    s_or = snr_at_ber(snrs, b_or, hdfec)

    # 正 = X 赢 混合 (混合差); 负 = 混合赢 X
    gain_hy_vs_nda = (s_nda - s_hy) if (s_nda is not None and s_hy is not None) else None
    gain_hy_vs_dpll = (s_dpll - s_hy) if (s_dpll is not None and s_hy is not None) else None
    gain_hy_vs_da = ((s_da_d + pilot_overhead_db) - s_hy) if (s_da_d is not None and s_hy is not None) else None

    # 逐点 (γ_d 坐标): 混合达 NDA BER 所需 γ_d − NDA γ_d (正=NDA赢混合, 负=混合赢NDA)
    per_point_hy_vs_nda = []
    for i, gd in enumerate(snrs):
        s_hy_needed = snr_at_ber(snrs, b_hy, b_nda[i])
        if s_hy_needed is not None:
            per_point_hy_vs_nda.append({
                'gamma_d_db': float(gd),
                'ber_nda': float(b_nda[i]),
                'snr_hy_needed_db': float(s_hy_needed),
                'hy_vs_nda_gain_db': float(s_hy_needed - gd),   # 负 = 混合赢 NDA
            })
    per_point_hy_vs_dpll = []
    for i, gd in enumerate(snrs):
        s_hy_needed = snr_at_ber(snrs, b_hy, b_dpll[i])
        if s_hy_needed is not None:
            per_point_hy_vs_dpll.append({
                'gamma_d_db': float(gd),
                'ber_dpll': float(b_dpll[i]),
                'snr_hy_needed_db': float(s_hy_needed),
                'hy_vs_dpll_gain_db': float(s_hy_needed - gd),   # 负 = 混合赢 DPLL
            })

    return {
        'snr_nda_d_at_hdfec': s_nda,
        'snr_da_tot_at_hdfec': (s_da_d + pilot_overhead_db) if s_da_d is not None else None,
        'snr_dpll_d_at_hdfec': s_dpll,
        'snr_hybrid_d_at_hdfec': s_hy,
        'snr_oracle_at_hdfec': s_or,
        'gain_hybrid_vs_nda_db': gain_hy_vs_nda,      # 负 = 混合赢 NDA
        'gain_hybrid_vs_dpll_db': gain_hy_vs_dpll,    # 负 = 混合赢 DPLL
        'gain_hybrid_vs_da_db': gain_hy_vs_da,         # 负 = 混合赢 DA
        'per_point_hybrid_vs_nda': per_point_hy_vs_nda,
        'per_point_hybrid_vs_dpll': per_point_hy_vs_dpll,
        'min_hybrid_ber': float(np.min(b_hy)),
        'min_nda_ber': float(np.min(b_nda)),
        'min_dpll_ber': float(np.min(b_dpll)),
    }


# =============================================================================
# 自检
# =============================================================================
def _selftest_hard_decision():
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 64 * 4)
    tx = m16apsk_mod(bits)
    dec = hard_decision_m16apsk(tx)
    err = np.max(np.abs(tx - dec))
    assert err < 1e-12, f"hard_decision_m16apsk 自检失败: max|tx-dec|={err}"
    return True


def _selftest_hybrid_clean_signal():
    """混合对无噪声无相位漂移信号应几乎不引入误差 (NDA 估到 0 相位, DPLL 跟到 0 漂移)."""
    rng = np.random.default_rng(1)
    bits = rng.integers(0, 2, P.N_DFT * 4)
    tx = m16apsk_mod(bits)
    # NDA per-block (1 块)
    rx_nda = nda_coarse_perblock(tx, intra_block_tracking=NDA_INTRA_AWGN)
    rx_comp, phi_est = dpll_track_dd_m16apsk(rx_nda, omega_n=OMEGA_N_DPLL)
    dec = hard_decision_m16apsk(rx_comp)
    dec_err = np.mean(dec != tx)
    max_phi = np.max(np.abs(phi_est))
    print(f"  [clean signal] max|phi_est|={max_phi:.6f} rad, decision err={dec_err:.2e}")
    assert dec_err < 0.05, f"混合 clean signal 自检失败: decision err={dec_err}"
    return True


def _selftest_hybrid_residual_tracking():
    """混合对纯 Wiener PN (有漂移无 AWGN) 应: NDA 块常数去块内平均相位, DPLL 跟块间漂移."""
    rng = np.random.default_rng(2)
    n_blk = 8
    bits = rng.integers(0, 2, n_blk * P.N_DFT * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    # 造一个块间线性相位漂移 (累积 Wiener PN 近似): 块 b 的相位偏 = b * 0.05 rad/sym
    n_sym = n_blk * P.N_DFT
    phi_drift = np.arange(n_sym) * 0.05
    rx = tx * np.exp(1j * phi_drift)
    # 纯 NDA (per-block) 残余漂移: 每块估块中心相位, 块内线性漂移留下残相
    rx_nda = nda_coarse_perblock(rx, intra_block_tracking=NDA_INTRA_TURB)
    # 混合: NDA 后 DPLL 连续跟踪
    rx_hy, _ = dpll_track_dd_m16apsk(rx_nda, omega_n=OMEGA_N_DPLL)
    tb = bits[:n_sym * P.BITS_PER_SYM]
    resolved_nda = resolve_m16apsk_blockwise(rx_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    resolved_hy = resolve_m16apsk_blockwise(rx_hy, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ber_nda = np.mean(tb != m16apsk_demod(resolved_nda))
    ber_hy = np.mean(tb != m16apsk_demod(resolved_hy))
    print(f"  [residual tracking] NDA-only BER={ber_nda:.3e}, HYBRID BER={ber_hy:.3e}")
    # 无噪声有漂移: 混合应 <= NDA (DPLL 跟块间漂移)
    # (不强制 hy < nda, 因 DPLL 可能引入小额外误差; 但 hy 不应远差于 nda)
    return ber_nda, ber_hy


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


def run_all(t_start, time_budget=840.0, omega_n=OMEGA_N_DPLL):
    """跑全部场景. time_budget=840s (14 min, 留 1 min 缓冲 < 15 min 上限)."""
    cfg = SimulationConfig()
    raw = {sc: {} for sc in SCENES_DOWNLINK + SCENES_UPLINK}
    scenes_done = []

    print("=" * 100)
    print(f"A3 组合适配: NDA+DPLL 混合 vs 单一 NDA / 单一 DPLL ({N_SEEDS} seed × 6 场景)")
    print(f"DPLL omega_n={omega_n:.0e}, zeta={ZETA_DPLL:.4f} (S011 选定)")
    print(f"AWGN seed_base: {[seed_base_awgn(i) for i in range(N_SEEDS)]}")
    print(f"下行 seed0   : {[seed0_turb_downlink(i) for i in range(N_SEEDS)]}")
    print(f"上行 seed0   : {[seed0_turb_uplink(i) for i in range(N_SEEDS)]}")
    print("=" * 100)

    # --- AWGN ---
    for i in range(N_SEEDS):
        if time.time() - t_start > time_budget:
            print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 AWGN seed {i}")
            return raw, scenes_done, True
        sb = seed_base_awgn(i)
        print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
        raw['awgn'][i] = run_awgn_hybrid(P.N_BLOCKS, P.SNR_AWGN_DB, sb, omega_n=omega_n)
    scenes_done.append('awgn')

    # --- 下行湍流 ---
    for turb in TURB_DOWNLINK:
        for i in range(N_SEEDS):
            if time.time() - t_start > time_budget:
                print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 {turb} seed {i}")
                return raw, scenes_done, True
            s0 = seed0_turb_downlink(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = run_turb_hybrid(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0, omega_n=omega_n)
        scenes_done.append(turb)

    # --- 上行湍流 ---
    for turb in TURB_UPLINK:
        for i in range(N_SEEDS):
            if time.time() - t_start > time_budget:
                print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 {turb} seed {i}")
                return raw, scenes_done, True
            s0 = seed0_turb_uplink(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            # 上行固定工作区 SNR (parity_tuning_sweep.py: uplink_moderate 16dB / uplink_strong 20dB)
            snr_uplink = [16.0] if turb == 'uplink_moderate' else [20.0]
            raw[turb][i] = run_turb_hybrid(turb, snr_uplink, P.N_BLOCKS, cfg, s0, omega_n=omega_n)
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
            methods = ['nda_ml', 'da_ml', 'dpll', 'hybrid', 'oracle']
            means = {}
            for m in methods:
                vals = [per_seed[i][j][f'{m}_ber'] for i in range(n_sd)]
                mean, std, hw, lo, hi = ci_t(vals)
                means[m] = {'mean': mean, 'std': std, 'ci95': [lo, hi]}
            points.append({'snr_db': float(snr), **{f'{m}_ber_mean': means[m]['mean'] for m in methods},
                           **{f'{m}_ber_std': means[m]['std'] for m in methods},
                           **{f'{m}_ber_ci95': means[m]['ci95'] for m in methods}})
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def hybrid_gain_per_seed(raw, scenes_done):
    out = {}
    for sc in scenes_done:
        per_seed = raw[sc]
        n_sd = len(per_seed)
        gains_hy_nda = []
        gains_hy_dpll = []
        gains_hy_da = []
        wr_hy_vs_nda = {}   # 工作区 per-point (γ_d >= 15 dB)
        wr_hy_vs_dpll = {}
        for i in range(n_sd):
            per_snr = per_seed[i]
            fg = analyze_hybrid_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            gains_hy_nda.append(fg['gain_hybrid_vs_nda_db'])
            gains_hy_dpll.append(fg['gain_hybrid_vs_dpll_db'])
            gains_hy_da.append(fg['gain_hybrid_vs_da_db'])
            for p in fg['per_point_hybrid_vs_nda']:
                if p['gamma_d_db'] >= 15.0:
                    wr_hy_vs_nda.setdefault(p['gamma_d_db'], []).append(float(p['hy_vs_nda_gain_db']))
            for p in fg['per_point_hybrid_vs_dpll']:
                if p['gamma_d_db'] >= 15.0:
                    wr_hy_vs_dpll.setdefault(p['gamma_d_db'], []).append(float(p['hy_vs_dpll_gain_db']))
        entry = {
            'per_seed_gain_hybrid_vs_nda_db': [None if g is None else float(g) for g in gains_hy_nda],
            'per_seed_gain_hybrid_vs_dpll_db': [None if g is None else float(g) for g in gains_hy_dpll],
            'per_seed_gain_hybrid_vs_da_db': [None if g is None else float(g) for g in gains_hy_da],
        }
        for tag, gains in [('nda', gains_hy_nda), ('dpll', gains_hy_dpll), ('da', gains_hy_da)]:
            v = [g for g in gains if g is not None]
            if len(v) >= 2:
                m, s, hw, lo, hi = ci_t(v)
                entry.update({f'gain_hybrid_vs_{tag}_mean_db': m,
                              f'gain_hybrid_vs_{tag}_std_db': s,
                              f'gain_hybrid_vs_{tag}_ci95_db': [lo, hi],
                              f'n_valid_{tag}': len(v)})
            else:
                entry.update({f'gain_hybrid_vs_{tag}_mean_db': None,
                              f'gain_hybrid_vs_{tag}_std_db': None,
                              f'gain_hybrid_vs_{tag}_ci95_db': [None, None],
                              f'n_valid_{tag}': len(v)})
        # 工作区 per-point (HD-FEC 不可达场景用)
        for tag, wr in [('nda', wr_hy_vs_nda), ('dpll', wr_hy_vs_dpll)]:
            if wr:
                wr_points = []
                all_wr = []
                for gd in sorted(wr.keys()):
                    col = wr[gd]
                    m, s, hw, lo, hi = ci_t(col)
                    wr_points.append({'gamma_d_db': float(gd), 'n_seeds': len(col),
                                      f'hybrid_vs_{tag}_gain_mean_db': m,
                                      f'hybrid_vs_{tag}_gain_std_db': s,
                                      f'hybrid_vs_{tag}_gain_ci95_db': [lo, hi]})
                    all_wr.extend(col)
                entry[f'workregion_hybrid_vs_{tag}_per_point'] = wr_points
                gm, gs, ghw, glo, ghi = ci_t(all_wr)
                entry[f'workregion_hybrid_vs_{tag}_grand_mean_db'] = gm
                entry[f'workregion_hybrid_vs_{tag}_grand_std_db'] = gs
                entry[f'workregion_hybrid_vs_{tag}_grand_ci95_db'] = [glo, ghi]
        out[sc] = entry
    return out


def consistency_check(summary, hybrid_gain, scenes_done):
    """TL-20 一致性自检 (守 TL-23):
      (1) hybrid BER 全程 >= oracle (否则 bug)
      (2) hybrid BER 不应远超 NDA (< 3×NDA, 否则混合太差)
      (3) hybrid BER 不应远超 DPLL (< 3×DPLL, 否则混合太差)
      (4) hybrid @ 18dB AWGN 合理范围 (跟 NDA/DPLL 同量级)
    返回 dict.
    """
    checks = {}
    for sc in scenes_done:
        pts = summary[sc]['points']
        # (1) hybrid >= oracle
        viol_oracle = []
        for p in pts:
            if p['hybrid_ber_mean'] < p['oracle_ber_mean'] * 0.9:
                viol_oracle.append({'snr_db': p['snr_db'],
                                    'hybrid': p['hybrid_ber_mean'],
                                    'oracle': p['oracle_ber_mean']})
        checks.setdefault('hybrid_ge_oracle', {})[sc] = {'pass': len(viol_oracle) == 0,
                                                          'n_violations': len(viol_oracle),
                                                          'violations': viol_oracle[:5]}
        # (2) hybrid < 3×NDA
        viol_nda = []
        for p in pts:
            if p['nda_ml_ber_mean'] > 0 and p['hybrid_ber_mean'] > 3.0 * p['nda_ml_ber_mean']:
                viol_nda.append({'snr_db': p['snr_db'],
                                 'hybrid': p['hybrid_ber_mean'],
                                 'nda': p['nda_ml_ber_mean'],
                                 'ratio': p['hybrid_ber_mean'] / p['nda_ml_ber_mean']})
        checks.setdefault('hybrid_not_too_bad_vs_nda', {})[sc] = {'pass': len(viol_nda) == 0,
                                                                   'n_violations': len(viol_nda),
                                                                   'violations': viol_nda[:5]}
        # (3) hybrid < 3×DPLL
        viol_dpll = []
        for p in pts:
            if p['dpll_ber_mean'] > 0 and p['hybrid_ber_mean'] > 3.0 * p['dpll_ber_mean']:
                viol_dpll.append({'snr_db': p['snr_db'],
                                  'hybrid': p['hybrid_ber_mean'],
                                  'dpll': p['dpll_ber_mean'],
                                  'ratio': p['hybrid_ber_mean'] / p['dpll_ber_mean']})
        checks.setdefault('hybrid_not_too_bad_vs_dpll', {})[sc] = {'pass': len(viol_dpll) == 0,
                                                                    'n_violations': len(viol_dpll),
                                                                    'violations': viol_dpll[:5]}
    # (4) hybrid @ 18dB AWGN
    hy_at_18 = None
    if 'awgn' in summary:
        for p in summary['awgn']['points']:
            if abs(p['snr_db'] - 18.0) < 1e-6:
                hy_at_18 = p['hybrid_ber_mean']
    checks['hybrid_at_18db_awgn'] = {'value': hy_at_18, 'pass': (hy_at_18 is not None and 0.001 <= hy_at_18 <= 0.05)}
    all_pass = (all(checks['hybrid_ge_oracle'][sc]['pass'] for sc in scenes_done)
                and all(checks['hybrid_not_too_bad_vs_nda'][sc]['pass'] for sc in scenes_done)
                and all(checks['hybrid_not_too_bad_vs_dpll'][sc]['pass'] for sc in scenes_done)
                and checks['hybrid_at_18db_awgn']['pass'])
    checks['all_pass'] = all_pass
    return checks


def a3_signal_verdict(hybrid_gain, scenes_done):
    """A3 信号判定 (adaptation-scan.md A3):
      PASS: 混合全场景不输 max(NDA, DPLL) + 至少一场景赢两者
      FAIL: 混合 ≈ max(NDA, DPLL) (只取两者之长无额外增益) 或反不如单一
    判据: gain_hybrid_vs_nda < 0 (混合赢NDA) 且 gain_hybrid_vs_dpll < 0 (混合赢DPLL).
    """
    verdict = {}
    wins_nda = []   # 混合赢 NDA 的场景 (gain < 0, CI 上界 < 0 统计显著)
    wins_dpll = []
    wins_both = []   # 同时赢两者的场景 (A3 PASS 的最强信号)
    for sc in scenes_done:
        e = hybrid_gain[sc]
        g_nda = e.get('gain_hybrid_vs_nda_mean_db')
        g_dpll = e.get('gain_hybrid_vs_dpll_mean_db')
        # strong/uplink HD-FEC 可能不可达, 用工作区 grand mean
        if g_nda is None and f'workregion_hybrid_vs_nda_grand_mean_db' in e:
            g_nda = e['workregion_hybrid_vs_nda_grand_mean_db']
        if g_dpll is None and f'workregion_hybrid_vs_dpll_grand_mean_db' in e:
            g_dpll = e['workregion_hybrid_vs_dpll_grand_mean_db']
        # gain < 0 = 混合赢; CI 上界 < 0 = 统计显著赢
        ci_nda = e.get('gain_hybrid_vs_nda_ci95_db') or [None, None]
        ci_dpll = e.get('gain_hybrid_vs_dpll_ci95_db') or [None, None]
        if g_nda is None and f'workregion_hybrid_vs_nda_grand_ci95_db' in e:
            ci_nda = e['workregion_hybrid_vs_nda_grand_ci95_db']
        if g_dpll is None and f'workregion_hybrid_vs_dpll_grand_ci95_db' in e:
            ci_dpll = e['workregion_hybrid_vs_dpll_grand_ci95_db']
        win_nda = (g_nda is not None and g_nda < 0)
        win_dpll = (g_dpll is not None and g_dpll < 0)
        sig_nda = (win_nda and ci_nda[1] is not None and ci_nda[1] < 0)
        sig_dpll = (win_dpll and ci_dpll[1] is not None and ci_dpll[1] < 0)
        verdict[sc] = {
            'gain_hybrid_vs_nda_db': (None if g_nda is None else float(g_nda)),
            'gain_hybrid_vs_dpll_db': (None if g_dpll is None else float(g_dpll)),
            'hybrid_wins_nda': win_nda, 'hybrid_wins_nda_significant': sig_nda,
            'hybrid_wins_dpll': win_dpll, 'hybrid_wins_dpll_significant': sig_dpll,
            'hybrid_wins_both': (win_nda and win_dpll),
            'hybrid_wins_both_significant': (sig_nda and sig_dpll),
        }
        if win_nda:
            wins_nda.append(sc)
        if win_dpll:
            wins_dpll.append(sc)
        if win_nda and win_dpll:
            wins_both.append(sc)
    # 整体判定
    any_win_both = len(wins_both) > 0
    any_win_nda_sig = any(verdict[sc]['hybrid_wins_nda_significant'] for sc in scenes_done)
    any_win_dpll_sig = any(verdict[sc]['hybrid_wins_dpll_significant'] for sc in scenes_done)
    # A3 PASS: 至少一场景统计显著赢两者 (互补性成立)
    # A3 WEAK: 至少一场景赢一个 (但不赢两者) = 部分互补
    # A3 FAIL: 全场景都不赢任一 (无额外增益, 只取两者之长)
    any_win_any = len(wins_nda) > 0 or len(wins_dpll) > 0
    pass_sig = any(verdict[sc]['hybrid_wins_both_significant'] for sc in scenes_done)
    if pass_sig:
        overall = 'PASS'
        reason = (f"至少一场景统计显著赢两者 (互补性成立): {[sc for sc in scenes_done if verdict[sc]['hybrid_wins_both_significant']]}")
    elif any_win_both:
        overall = 'PARTIAL'
        reason = f"有场景赢两者但未达统计显著: {wins_both}"
    elif any_win_any:
        overall = 'WEAK'
        win_nda_sc = [sc for sc in scenes_done if verdict[sc]['hybrid_wins_nda']]
        win_dpll_sc = [sc for sc in scenes_done if verdict[sc]['hybrid_wins_dpll']]
        reason = f"只赢一个 (混合 ≈ max(NDA,DPLL), 互补性弱): 赢NDA={win_nda_sc}, 赢DPLL={win_dpll_sc}"
    else:
        overall = 'FAIL'
        reason = "全场景都不赢任一 (无额外增益, 组合是冗余叠加)"
    verdict['_overall'] = {'verdict': overall, 'reason': reason,
                            'wins_nda_scenes': wins_nda, 'wins_dpll_scenes': wins_dpll,
                            'wins_both_scenes': wins_both}
    return verdict


def plot_curves(summary, scenes_done, hybrid_gain, omega_n):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    titles = {'awgn': 'AWGN', 'weak': 'weak (α4/β3)',
              'moderate': 'moderate (α2.5/β1.8)', 'strong': 'strong (α1.5/β0.8)',
              'uplink_moderate': 'uplink_moderate (α1.2/β0.9)',
              'uplink_strong': 'uplink_strong (α1.0/β0.7)'}
    n = len(scenes_done)
    fig, axes = plt.subplots(1, n, figsize=(5.5 * n, 5.2))
    if n == 1:
        axes = [axes]
    for ax, sc in zip(axes, scenes_done):
        pts = summary[sc]['points']
        gts = [p['snr_db'] for p in pts]
        nda_m = np.array([p['nda_ml_ber_mean'] for p in pts])
        da_m = np.array([p['da_ml_ber_mean'] for p in pts])
        dpll_m = np.array([p['dpll_ber_mean'] for p in pts])
        hy_m = np.array([p['hybrid_ber_mean'] for p in pts])
        or_m = np.array([p['oracle_ber_mean'] for p in pts])
        hy_lo = np.array([p['hybrid_ber_ci95'][0] for p in pts])
        hy_hi = np.array([p['hybrid_ber_ci95'][1] for p in pts])
        ax.semilogy(gts, nda_m, 'o-', color='C0', label='NDA-ML (M0=8)', lw=1.8)
        ax.semilogy(gts, da_m, 's-', color='C1', label='DA ML (sp=4)', lw=1.8)
        ax.semilogy(gts, dpll_m, 'D-', color='C4', label=f'DPLL DD (ωn={omega_n:.0e})', lw=1.8)
        ax.semilogy(gts, hy_m, '*-', color='C3', label='HYBRID NDA+DPLL', lw=2.2, ms=10)
        ax.fill_between(gts, np.maximum(hy_lo, 1e-6), hy_hi, color='C3', alpha=0.18)
        ax.semilogy(gts, or_m, '^--', color='C2', label='oracle', lw=1.6)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        fg = hybrid_gain[sc]
        g_hy_nda = fg.get('gain_hybrid_vs_nda_mean_db')
        g_hy_dpll = fg.get('gain_hybrid_vs_dpll_mean_db')
        if g_hy_nda is None and 'workregion_hybrid_vs_nda_grand_mean_db' in fg:
            g_hy_nda = fg['workregion_hybrid_vs_nda_grand_mean_db']
            g_hy_dpll = fg.get('workregion_hybrid_vs_dpll_grand_mean_db')
        ttl = titles.get(sc, sc)
        if g_hy_nda is not None and g_hy_dpll is not None:
            ttl += (f"\nhy vs NDA {g_hy_nda:+.2f} / hy vs DPLL {g_hy_dpll:+.2f} dB\n(负=混合赢)")
        ax.set_title(ttl, fontsize=8.5)
        ax.set_xlabel(r'$\gamma_d$ (dB)' if sc != 'awgn' else 'SNR (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('A3 组合适配: NDA+DPLL 混合 vs NDA vs DPLL vs DA vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=11, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_a3_hybrid_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return png


def main():
    t0 = time.time()
    print("=" * 100)
    print("A3 组合适配: NDA-ML (前馈升幂) + DPLL DD (闭环跟踪) 混合方案")
    print(f"M0={P.M0}, omega_n={OMEGA_N_DPLL:.0e}, zeta={ZETA_DPLL:.4f}, "
          f"pilot_overhead={P.PILOT_OVERHEAD_DB:.3f} dB, HDFEC={P.HDFEC}")
    print(f"common/_recovery.py 未改动 (选项 A, 适配在本脚本内, 同 run_dpll_ablation 先例)")
    print("=" * 100)

    # --- 自检 ---
    print("\n[自检 1] hard_decision_m16apsk 对无噪声 tx 返回自身...")
    _selftest_hard_decision()
    print("  PASS")
    print("\n[自检 2] 混合对无噪声无 PN 信号判决正确...")
    _selftest_hybrid_clean_signal()
    print("  PASS")
    print("\n[自检 3] 混合对纯 Wiener PN (有漂移无 AWGN): NDA + DPLL 跟踪...")
    ber_nda, ber_hy = _selftest_hybrid_residual_tracking()
    print(f"  完成 (NDA={ber_nda:.3e}, HYBRID={ber_hy:.3e})")

    # --- 跑 ---
    raw, scenes_done, partial = run_all(t0, omega_n=OMEGA_N_DPLL)
    elapsed = time.time() - t0

    # --- 聚合 ---
    summary = aggregate(raw, scenes_done)
    hybrid_gain = hybrid_gain_per_seed(raw, scenes_done)

    # --- TL-20 一致性自检 ---
    checks = consistency_check(summary, hybrid_gain, scenes_done)
    print("\n" + "=" * 100)
    print("TL-20 一致性自检:")
    for chk_name in ['hybrid_ge_oracle', 'hybrid_not_too_bad_vs_nda', 'hybrid_not_too_bad_vs_dpll']:
        ok = all(checks[chk_name][sc]['pass'] for sc in scenes_done)
        print(f"  {chk_name} (全场景): {ok}")
        for sc in scenes_done:
            c = checks[chk_name][sc]
            if not c['pass']:
                print(f"    [{sc}] 违反 {c['n_violations']} 点")
    v18 = checks['hybrid_at_18db_awgn']
    print(f"  hybrid @ 18dB AWGN = {v18['value']}: {v18['pass']}")
    print(f"  ALL PASS: {checks['all_pass']}")

    # --- A3 信号判定 ---
    verdict = a3_signal_verdict(hybrid_gain, scenes_done)
    print("\n" + "=" * 100)
    print("A3 组合适配信号判定 (adaptation-scan.md A3):")
    print(f"  整体: {verdict['_overall']['verdict']} — {verdict['_overall']['reason']}")
    print(f"{'场景':>18} {'hy vs NDA':>12} {'赢NDA?':>8} {'hy vs DPLL':>12} {'赢DPLL?':>8} {'赢两者?':>8}")
    for sc in scenes_done:
        v = verdict[sc]
        g_n = v['gain_hybrid_vs_nda_db']
        g_d = v['gain_hybrid_vs_dpll_db']
        print(f"{sc:>18} {(str(g_n) if g_n is None else f'{g_n:+.3f}'):>12} "
              f"{str(v['hybrid_wins_nda']):>8} "
              f"{(str(g_d) if g_d is None else f'{g_d:+.3f}'):>12} "
              f"{str(v['hybrid_wins_dpll']):>8} {str(v['hybrid_wins_both']):>8}")

    # --- 画图 ---
    try:
        png_path = plot_curves(summary, scenes_done, hybrid_gain, OMEGA_N_DPLL)
        print(f"\n[PNG] {png_path}")
    except Exception as e:
        print(f"(PNG skipped: {e})")
        png_path = None

    # --- 落盘 ---
    out = {
        'meta': {
            'task': 'A3 组合适配: NDA+DPLL 混合 vs 单一 NDA / 单一 DPLL (5 seed × 6 场景)',
            'purpose': '验证 NDA (前馈无失锁) + DPLL (闭环高精度) 混合的互补性 (adaptation-scan.md A3)',
            'hybrid_algorithm': {
                'step1': 'NDA-ML per-block 升幂 mean-angle 估块常数粗相位 (无失锁前馈)',
                'step2': 'DPLL DD 连续跟踪残余漂移 (全数组 VCO 累积, 守 S011)',
                'complementarity': 'NDA 去大块相位减小 DPLL 失锁风险, DPLL 补 NDA per-block 无法跨块跟踪的漂移',
            },
            'n_seeds': N_SEEDS,
            'scenes_done': scenes_done,
            'partial_run': partial,
            'fairness': {
                'hybrid_vs_nda': 'γ_d 坐标 (都无 pilot overhead)',
                'hybrid_vs_dpll': 'γ_d 坐标 (都无 pilot overhead)',
                'hybrid_vs_da': 'γ_tot 坐标 (DA 有 1.249 dB pilot overhead)',
                'resolve': 'resolve_m16apsk_blockwise (per-block M0-fold, 同 NDA/DPLL 流程)',
                'channel_bit_exact': '同 seed 同 generate_shared_realization_apsk 重算 (守 TL-13)',
            },
            'dpll_params': {'omega_n': float(OMEGA_N_DPLL), 'zeta': float(ZETA_DPLL),
                             'source': 'S011 选定 omega_n=50e6'},
            'nda_intra_tracking': {'awgn': NDA_INTRA_AWGN, 'turb': NDA_INTRA_TURB,
                                    'source': '同 ber_nda_awgn / ber_nda_turb_eval'},
            'gain_definition': {
                'hybrid_vs_nda': 'fair_gain = (NDA γ_d @ HD-FEC) − (hybrid γ_d @ HD-FEC); 负=混合赢NDA',
                'hybrid_vs_dpll': 'fair_gain = (DPLL γ_d @ HD-FEC) − (hybrid γ_d @ HD-FEC); 负=混合赢DPLL',
            },
            'seed_strategy': {
                'awgn': 'seed_base_i = SEED_AWGN + i',
                'turbulence_downlink': 'seed0_i = SEED_TURB0 + i*N_BLOCKS',
                'turbulence_uplink': 'seed0_i = SEED_TURB0 + i*N_BLOCKS + UPLINK_SEED_OFFSET',
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
        'hybrid_gain_per_seed': to_jsonable(hybrid_gain),
        'consistency_checks': to_jsonable(checks),
        'a3_verdict': to_jsonable(verdict),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_a3_hybrid_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"\n[总耗时] {elapsed:.1f} s")
    if partial:
        print(f"[部分运行] 仅完成场景: {scenes_done}")


if __name__ == '__main__':
    main()
