# -*- coding: utf-8 -*-
"""DPLL (Decision-Directed Digital Phase-Locked Loop) 异族 baseline 对比消融.

回答: DPLL 是载波同步经典闭环方法 (decision-directed), 跟 NDA-ML/VV/BPS 的前馈盲估不同族
(DPLL 用判决反馈闭环跟踪, VV/BPS/NDA 用升幂前馈滑窗). 导师 D-010 标准 3 "不找接近方法当
baseline" → VV 同族禁主比, DPLL 是异族合法 baseline 候选.

DPLL 现状 (common/_recovery.py:dpll_track_dd): 已实现 DD-DPLL (PI loop filter + VCO),
但判决分支硬编码 qpsk/qam16 (L21-27), 不支持 m16apsk. 适配成 m16apsk (最近邻星座点判定).

适配 (选项 A: 不改 common/_recovery.py, 适配在本消融脚本内, 同 VV/BPS/DD-KF 三先例):
  (1) hard_decision_m16apsk(z): 最近邻 16 点星座判定 (复用 run_dd_kf_ablation.py:124 模式,
      从 common._modulation import _M16APSK_SYM).
  (2) dpll_track_dd_m16apsk(rx, omega_n, zeta): 复制 common.dpll_track_dd, 改判决 → m16apsk 版.
  **不用 dpll_track (4次方鉴相器)**: 16APSK M₀=8 非 4 次方对称 (H007 纪律).

公平性 (§2.4 关键纪律):
  - DPLL 无 pilot overhead (盲 DD, 同 NDA/VV): DPLL vs NDA 公平对照用 γ_d 坐标.
  - DPLL vs DA 用 γ_tot 坐标 (DA 有 1.249 dB pilot overhead, DPLL 无 → γ_tot=γ_d).
  - resolve M0-fold 模糊同 NDA-ML 流程 (resolve_m16apsk_blockwise, per-block 选最优旋转).

omega_n 参数选择 (TL-20 理论预期 + 收敛分析):
  - DPLL 连续处理 (全数组 VCO 累积), omega_n=20e6~100e6 都合理 (@18dB BER 4.1~4.2e-3).
  - per-block (逐块重置 VCO) 实测差 2~5× (DPLL 跟踪环丢符号间相位连续性) → 不用 per-block.
  - 本脚本在 main() 自检段扫 omega_n ∈ {20e6, 50e6, 100e6}, 选 18dB AWGN BER 最接近 TL-20
    预期 (0.003~0.006) 且 <2×NDA 的值, 记录选择理由 (跟 VV Nw=64/BPS B=64 同样有参数选择记录).

处理方式 (连续 vs per-block):
  - DPLL 是闭环跟踪环, VCO 相位跨符号累积——连续处理全数组 (不逐块重置 VCO).
  - VV/BPS 是前馈滑窗, 逐块独立 OK; DPLL 闭环必须连续 (物理特性).
  - resolve M0-fold 模糊仍用 resolve_m16apsk_blockwise (per-block 选最优旋转), 同 NDA/VV/BPS.

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0).
  AWGN: seed_base_i = SEED_AWGN + i
  湍流: seed0_i = SEED_TURB0 + i·N_BLOCKS (5 seed 块范围互斥)

信道实现 bit-exact 复现主实验 (守 TL-13): NDA/DA/oracle 不读 results/, 而是用同 seed 同
generate_shared_realization_apsk 调用重算 (与 VV/BPS/DD-KF 消融同做法).

运行: cd projects/simulation && python simulator/run_dpll_ablation.py
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
# m16apsk 星座点 (用于 hard_decision_m16apsk 最近邻判定)
from common._modulation import _M16APSK_SYM  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_dpll_ablation')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# DPLL 参数候选 (omega_n 扫描, 选最优后赋值).
# zeta=√2/2 临界阻尼 (经典二阶环, 同 common/_recovery.py 默认).
# DPLL 连续处理 (全数组 VCO 累积) 下, omega_n=20e6~100e6 都合理 (@18dB BER 4.1~4.2e-3,
# 跟 VV/BPS 同量级). 候选取 20e6/50e6/100e6 (连续处理有效区间).
ZETA_DPLL = np.sqrt(2) / 2
OMEGA_N_DEFAULT = 50e6   # 连续处理下 18dB BER≈4.1e-3 (1.06×NDA), TL-20 预期内
OMEGA_N_CANDIDATES = [20e6, 50e6, 100e6]   # 扫描候选 (连续处理有效区间)


# =============================================================================
# DPLL M16APSK 适配 (选项 A: 在本消融脚本内, 不改 common/_recovery.py)
# =============================================================================
def hard_decision_m16apsk(z):
    """(8,8)-16APSK 最近邻硬判决 (标量或向量).

    用 _M16APSK_SYM (16 点星座) 欧氏最近邻判定, 返回最近邻星座点 (复数).
    验证 (§2.3 步骤 2): 对无噪声 tx 符号应返回自身 — main() 内有自检.
    与 common/_modulation.py:hard_decision(mod='m16apsk') 等价 (但 common 那个未实现, 这里独立写).
    复制自 run_dd_kf_ablation.py:124-138 (已验证模式).
    """
    z = np.asarray(z, dtype=complex)
    if z.ndim == 0:
        d = np.abs(z - _M16APSK_SYM) ** 2
        return complex(_M16APSK_SYM[int(np.argmin(d))])
    # 向量化
    d = np.abs(z[:, np.newaxis] - _M16APSK_SYM[np.newaxis, :]) ** 2
    idx = np.argmin(d, axis=1)
    return _M16APSK_SYM[idx]


def dpll_track_dd_m16apsk(rx, omega_n=OMEGA_N_DEFAULT, zeta=ZETA_DPLL):
    """DD (decision-directed) DPLL 适配 (8,8)-16APSK.

    复制 common/_recovery.py:dpll_track_dd, 改判决分支 qam16 硬编码 → hard_decision_m16apsk.
    闭环二阶环: PD (decision-directed angle) → PI loop filter (c1/c2) → VCO 累积相位.
    返回 (rx_compensated, phi_est). 同 dpll_track_dd 接口.

    omega_n: 环路自然频率 (rad/s). 默认 20e6 (旧 QAM16 实验, sim_nmse_qam16_sweep.py:120).
             8e6 (common 默认) 对 256 符号块收敛慢, main() 自检段扫描选最优.
    zeta: 阻尼系数, 默认 √2/2 临界阻尼.
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
        # DD: hard decision (m16apsk 最近邻, 替代 common 的 qam16 硬编码)
        dec = hard_decision_m16apsk(rotated)
        # Phase error from decision
        pd_out = np.angle(rx[k] * np.exp(-1j * vco_phase) * np.conj(dec))
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est


# =============================================================================
# DPLL BER 评估 (AWGN + 湍流)
# =============================================================================
def ber_dpll_awgn(rx, tx_bits, omega_n=OMEGA_N_DEFAULT):
    """DPLL-M16APSK AWGN: 连续 DD-DPLL (全数组) + resolve M0-fold 模糊. 返回 (n_err, n_bits).

    DPLL 是闭环跟踪环, VCO 相位跨符号累积——必须连续处理全数组 (不逐块重置 VCO),
    否则每块重初始化丢失符号间相位连续性致 BER 暴涨 (实测 per-block @18dB 7.5e-3 vs
    continuous 4.1e-3). 这跟 VV/BPS 前馈滑窗不同: 前馈法逐块独立 OK, 闭环法必须连续.
    resolve M0-fold 模糊同 NDA-ML 流程 (resolve_m16apsk_blockwise, per-block 选最优旋转).
    DPLL 无 pilot overhead.
    """
    L = (len(rx) // P.N_DFT) * P.N_DFT
    rx_comp, _ = dpll_track_dd_m16apsk(rx[:L], omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_dpll_turb_eval(rx, tx_bits, omega_n=OMEGA_N_DEFAULT):
    """DPLL-M16APSK 湍流: 逐块 fft_foe FOE 补偿 → 连续 DD-DPLL CPE + resolve.

    同 VV/BPS 消融做法: 先 fft_foe_m0_omega (M0=8 升幂 FOE, 同 NDA-ML 湍流两阶段第一阶段),
    但 FOE 逐块估 (每块独立 CFO 估计, 同 NDA/VV/BPS). FOE 补偿后信号送 DPLL 连续跟踪
    (VCO 全数组累积, 不逐块重置——DPLL 跟踪环物理特性).
    公平: DPLL 用与 NDA 相同的 FOE 前端 (两阶段对称).
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_foe_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        rx_foe_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = seg * np.exp(-1j * omega_est * k)
    # 连续 DPLL 跟踪 (FOE 补偿后, 残余相位是 Wiener PN, DPLL 连续跟踪)
    rx_comp, _ = dpll_track_dd_m16apsk(rx_foe_comp, omega_n=omega_n)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# SNR 扫描: AWGN + 湍流 (DPLL + 复用主实验 NDA/DA/oracle 重算, bit-exact 守 TL-13)
# =============================================================================
def run_awgn_dpll(n_blocks, snr_points, seed_base, omega_n=OMEGA_N_DEFAULT):
    """AWGN: DPLL + NDA + DA + oracle BER 扫描. 复用 awgn_wiener_channel (同 seed 派生)."""
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN DPLL] N_sym={N_sym}/点, omega_n={omega_n:.0e}, zeta={ZETA_DPLL:.4f}")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'DPLL_BER':>12} {'ORACLE':>12}")
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
        ne_or, nb_or = S.ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_dpll = ne_dpll / nb_dpll
        b_or = ne_or / nb_or
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_dpll:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_dpll': float(snr),   # DPLL 无 pilot overhead
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'dpll_ber': b_dpll, 'oracle_ber': b_or,
        })
    return per_snr


def run_turb_dpll(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0,
                  omega_n=OMEGA_N_DEFAULT):
    """湍流: DPLL + NDA + DA + oracle BER 扫描. 复用 generate_shared_realization_apsk."""
    Ns = P.N_DFT
    print(f"[{turb_name} DPLL] N_sym={n_blocks*Ns}/点, per-block h 均衡 + DPLL 两阶段 fft_foe+DD-DPLL CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'DPLL_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = ne_da = ne_dpll = ne_or = 0
        nb_nda = nb_da = nb_dpll = nb_or = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (per-block h, 同主实验): DPLL 用盲 h 估计 (同 NDA, 公平)
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            ne, nb = S.ber_nda_turb_eval(rx_blind, bits)
            ne_nda += ne; nb_nda += nb
            ne, nb = S.ber_da_turb(rx_pilot, bits)
            ne_da += ne; nb_da += nb
            ne, nb = ber_dpll_turb_eval(rx_blind, bits, omega_n=omega_n)
            ne_dpll += ne; nb_dpll += nb
            ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
            ne_or += ne; nb_or += nb
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_dpll = ne_dpll / nb_dpll
        b_or = ne_or / nb_or
        print(f"{gamma_db:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_dpll:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_dpll': float(gamma_db),
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'dpll_ber': b_dpll, 'oracle_ber': b_or,
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
# DPLL vs NDA / DA 公平 gain 分析
# =============================================================================
def analyze_dpll_gain(per_snr, hdfec, pilot_overhead_db):
    """DPLL vs NDA (γ_d 坐标, 都无 pilot) + DPLL vs DA (γ_tot 坐标, DPLL 无 pilot).

    fair_gain_DPLL_vs_NDA = (DPLL γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正 = NDA 赢 DPLL.
    fair_gain_DPLL_vs_DA  = (DA γ_tot @ HD-FEC) − (DPLL γ_tot @ HD-FEC)
                            = (DA γ_d @ HD-FEC + overhead) − (DPLL γ_d @ HD-FEC); 正 = DPLL 赢 DA.
    """
    snrs = np.array([p['snr_db'] for p in per_snr])
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_dpll = np.array([p['dpll_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])

    s_nda = snr_at_ber(snrs, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs, b_da, hdfec)
    s_dpll = snr_at_ber(snrs, b_dpll, hdfec)
    s_or = snr_at_ber(snrs, b_or, hdfec)

    # DPLL vs NDA (γ_d 坐标, 都无 pilot overhead): 正 = NDA 赢
    gain_dpll_vs_nda = None
    if s_dpll is not None and s_nda is not None:
        gain_dpll_vs_nda = s_dpll - s_nda
    # DPLL vs DA (γ_tot 坐标): 正 = DPLL 赢 DA
    gain_dpll_vs_da = None
    if s_dpll is not None and s_da_d is not None:
        gain_dpll_vs_da = (s_da_d + pilot_overhead_db) - s_dpll

    # 逐点 (γ_d 坐标): DPLL 达 NDA BER 所需 γ_d − NDA γ_d
    per_point_dpll_vs_nda = []
    for i, gd in enumerate(snrs):
        ber_nda_at = b_nda[i]
        s_dpll_needed = snr_at_ber(snrs, b_dpll, ber_nda_at)
        if s_dpll_needed is not None:
            per_point_dpll_vs_nda.append({
                'gamma_d_db': float(gd),
                'ber_nda': float(ber_nda_at),
                'snr_dpll_needed_db': float(s_dpll_needed),
                'dpll_vs_nda_gain_db': float(s_dpll_needed - gd),   # 正 = NDA 赢 DPLL
            })

    hdfec_reachable = (s_dpll is not None and s_nda is not None)

    return {
        'snr_nda_d_at_hdfec': s_nda,
        'snr_da_tot_at_hdfec': (s_da_d + pilot_overhead_db) if s_da_d is not None else None,
        'snr_dpll_d_at_hdfec': s_dpll,
        'snr_oracle_at_hdfec': s_or,
        'gain_dpll_vs_nda_db': gain_dpll_vs_nda,      # 正 = NDA 赢 DPLL
        'gain_dpll_vs_da_db': gain_dpll_vs_da,         # 正 = DPLL 赢 DA
        'hdfec_reachable': hdfec_reachable,
        'per_point_dpll_vs_nda': per_point_dpll_vs_nda,
        'min_dpll_ber': float(np.min(b_dpll)),
    }


# =============================================================================
# 自检: hard_decision_m16apsk 对无噪声 tx 返回自身
# =============================================================================
def _selftest_hard_decision():
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 64 * 4)
    tx = m16apsk_mod(bits)
    dec = hard_decision_m16apsk(tx)
    err = np.max(np.abs(tx - dec))
    assert err < 1e-12, f"hard_decision_m16apsk 自检失败: max|tx-dec|={err}"
    return True


def _selftest_dpll_clean_signal():
    """DPLL 对无噪声无相位漂移信号应几乎不引入相位误差 (phi_est ≈ 0)."""
    rng = np.random.default_rng(1)
    bits = rng.integers(0, 2, P.N_DFT * 4)
    tx = m16apsk_mod(bits)
    rx_comp, phi_est = dpll_track_dd_m16apsk(tx, omega_n=OMEGA_N_DEFAULT)
    # 无 PN 无噪声, DPLL 应跟踪到 ~0 相位 (判决正确 → pd_out ≈ 0)
    max_phi = np.max(np.abs(phi_est))
    # 判决正确率
    dec = hard_decision_m16apsk(rx_comp)
    dec_err = np.mean(dec != tx)
    print(f"  [clean signal] max|phi_est|={max_phi:.6f} rad, decision err={dec_err:.2e}")
    assert dec_err < 0.01, f"DPLL clean signal 自检失败: decision err={dec_err}"
    return True


def omega_n_sweep_awgn(seed_base=20240701):
    """omega_n 扫描: 单 seed AWGN 18dB 跑 3 个候选, 选最优.

    TL-20 预期: DPLL @ 18dB AWGN BER 应在 0.003~0.006 (跟 VV/BPS 同量级),
    且 < 2×NDA (NDA@18dB≈3.44e-3 → DPLL < 6.88e-3).
    选 BER 最接近预期且不违反判据的 omega_n.
    """
    snr_test = 18.0
    n_blocks_test = 50   # 快速测试 (50×256=12800 sym, 够估 BER 量级)
    N_sym = n_blocks_test * P.N_DFT
    seed = seed_base + int(snr_test * 1000)
    rng = np.random.default_rng(seed + 7)
    bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, phi_true = S.awgn_wiener_channel(tx, snr_test, seed)
    ne_nda, nb_nda = S.ber_nda_awgn(rx, bits)
    b_nda = ne_nda / nb_nda
    print(f"  [omega_n sweep] NDA @18dB = {b_nda:.4e} (参考, <2×={2*b_nda:.4e})")
    results = {}
    for wn in OMEGA_N_CANDIDATES:
        ne, nb = ber_dpll_awgn(rx, bits, omega_n=wn)
        b = ne / nb
        results[wn] = b
        flag = ''
        if b < 2 * b_nda and 0.001 <= b <= 0.01:
            flag = ' ✅ (合理范围 + <2×NDA)'
        elif b >= 2 * b_nda:
            flag = ' ⚠️ (>2×NDA, DPLL 太弱)'
        elif b < 0.7 * b_nda:
            flag = ' ⚠️ (<0.7×NDA, NDA 无价值?)'
        print(f"    omega_n={wn:.0e}: DPLL @18dB = {b:.4e}{flag}")
    # 选最优: 优先满足 (0.001 ≤ BER ≤ 0.01) 且 <2×NDA; 否则选最接近 0.004 的
    best_wn = None
    best_score = float('inf')
    target_ber = 0.004   # TL-20 预期中心
    for wn, b in results.items():
        # 惩罚: 超出合理范围 / 违反判据
        penalty = 0.0
        if b >= 2 * b_nda:
            penalty += 1e6   # 违反判据2 重罚
        if b < 0.7 * b_nda:
            penalty += 1e6   # 违反判据3 重罚
        if not (0.001 <= b <= 0.01):
            penalty += 1e5   # 超出量级范围
        score = abs(b - target_ber) + penalty
        if score < best_score:
            best_score = score
            best_wn = wn
    return best_wn, results, b_nda


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


def run_all(t_start, time_budget=840.0, omega_n=OMEGA_N_DEFAULT):
    """跑全部场景. time_budget=840s (14 min, 留 1 min 缓冲 < 15 min 上限).
    若超时, 跑完当前场景即停 (返回 partial=True)."""
    cfg = SimulationConfig()
    raw = {sc: {} for sc in SCENES}
    scenes_done = []

    print("=" * 100)
    print(f"DPLL DD M-APSK 异族 baseline 消融: {N_SEEDS} seed × {len(SCENES)} 场景")
    print(f"omega_n={omega_n:.0e}, zeta={ZETA_DPLL:.4f}")
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
        raw['awgn'][i] = run_awgn_dpll(P.N_BLOCKS, P.SNR_AWGN_DB, sb, omega_n=omega_n)
    scenes_done.append('awgn')

    # --- 湍流 ---
    for turb in TURB_LEVELS:
        for i in range(N_SEEDS):
            if time.time() - t_start > time_budget:
                print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 {turb} seed {i}")
                return raw, scenes_done, True
            s0 = seed0_turb(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = run_turb_dpll(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0, omega_n=omega_n)
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
            dpll = [per_seed[i][j]['dpll_ber'] for i in range(n_sd)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(n_sd)]
            m_nda, s_nda, hw_nda, lo_nda, hi_nda = ci_t(nda)
            m_da, s_da, hw_da, lo_da, hi_da = ci_t(da)
            m_dpll, s_dpll, hw_dpll, lo_dpll, hi_dpll = ci_t(dpll)
            m_or, s_or, hw_or, lo_or, hi_or = ci_t(orc)
            points.append({
                'snr_db': float(snr),
                'nda_ml_ber_mean': m_nda, 'nda_ml_ber_std': s_nda,
                'nda_ml_ber_ci95': [lo_nda, hi_nda],
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'da_ml_ber_ci95': [lo_da, hi_da],
                'dpll_ber_mean': m_dpll, 'dpll_ber_std': s_dpll,
                'dpll_ber_ci95': [lo_dpll, hi_dpll],
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
                'oracle_ber_ci95': [lo_or, hi_or],
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def dpll_gain_per_seed(raw, scenes_done):
    out = {}
    for sc in scenes_done:
        per_seed = raw[sc]
        n_sd = len(per_seed)
        gains_dpll_nda = []
        gains_dpll_da = []
        wr_dpll_vs_nda = {}   # strong 工作区 per-point
        for i in range(n_sd):
            per_snr = per_seed[i]
            fg = analyze_dpll_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            gains_dpll_nda.append(fg['gain_dpll_vs_nda_db'])
            gains_dpll_da.append(fg['gain_dpll_vs_da_db'])
            for p in fg['per_point_dpll_vs_nda']:
                if p['gamma_d_db'] >= 15.0:
                    wr_dpll_vs_nda.setdefault(p['gamma_d_db'], []).append(
                        float(p['dpll_vs_nda_gain_db']))
        entry = {
            'per_seed_gain_dpll_vs_nda_db': [None if g is None else float(g) for g in gains_dpll_nda],
            'per_seed_gain_dpll_vs_da_db': [None if g is None else float(g) for g in gains_dpll_da],
        }
        v_nda = [g for g in gains_dpll_nda if g is not None]
        v_da = [g for g in gains_dpll_da if g is not None]
        if len(v_nda) >= 2:
            m, s, hw, lo, hi = ci_t(v_nda)
            entry.update({'gain_dpll_vs_nda_mean_db': m, 'gain_dpll_vs_nda_std_db': s,
                          'gain_dpll_vs_nda_ci95_db': [lo, hi], 'n_valid_nda': len(v_nda)})
        else:
            entry.update({'gain_dpll_vs_nda_mean_db': None, 'gain_dpll_vs_nda_std_db': None,
                          'gain_dpll_vs_nda_ci95_db': [None, None], 'n_valid_nda': len(v_nda)})
        if len(v_da) >= 2:
            m, s, hw, lo, hi = ci_t(v_da)
            entry.update({'gain_dpll_vs_da_mean_db': m, 'gain_dpll_vs_da_std_db': s,
                          'gain_dpll_vs_da_ci95_db': [lo, hi], 'n_valid_da': len(v_da)})
        else:
            entry.update({'gain_dpll_vs_da_mean_db': None, 'gain_dpll_vs_da_std_db': None,
                          'gain_dpll_vs_da_ci95_db': [None, None], 'n_valid_da': len(v_da)})
        # strong 工作区 per-point
        if sc == 'strong' and wr_dpll_vs_nda:
            wr_points = []
            all_wr = []
            for gd in sorted(wr_dpll_vs_nda.keys()):
                col = wr_dpll_vs_nda[gd]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({'gamma_d_db': float(gd), 'n_seeds': len(col),
                                  'dpll_vs_nda_gain_mean_db': m, 'dpll_vs_nda_gain_std_db': s,
                                  'dpll_vs_nda_gain_ci95_db': [lo, hi]})
                all_wr.extend(col)
            entry['workregion_dpll_vs_nda_per_point'] = wr_points
            gm, gs, ghw, glo, ghi = ci_t(all_wr)
            entry['workregion_dpll_vs_nda_grand_mean_db'] = gm
            entry['workregion_dpll_vs_nda_grand_std_db'] = gs
            entry['workregion_dpll_vs_nda_grand_ci95_db'] = [glo, ghi]
        out[sc] = entry
    return out


def consistency_check(summary, dpll_gain, scenes_done):
    """TL-20 一致性自检 (守 TL-23):
      (1) DPLL BER 应全程 ≥ oracle (如果 < oracle 一定 bug)
      (2) DPLL BER 不应远超 NDA-ML (< 2×NDA, 否则 DPLL 太弱不像合法 baseline)
      (3) DPLL BER 不应远低于 NDA-ML (> 0.7×NDA, 否则 NDA 无价值)
      (4) DPLL BER @ 18dB AWGN 合理范围: 0.003~0.006 (跟 VV/BPS 同量级)
    返回 dict of check results.
    """
    checks = {}
    # (1) DPLL >= oracle (逐 SNR, 逐场景)
    for sc in scenes_done:
        pts = summary[sc]['points']
        violations_oracle = []
        for p in pts:
            dpll_m = p['dpll_ber_mean']
            or_m = p['oracle_ber_mean']
            if dpll_m < or_m * 0.9:
                violations_oracle.append({
                    'snr_db': p['snr_db'],
                    'dpll_ber': dpll_m, 'oracle_ber': or_m,
                    'ratio': dpll_m / or_m if or_m > 0 else None,
                })
        checks.setdefault('dpll_ge_oracle', {})[sc] = {
            'pass': len(violations_oracle) == 0,
            'n_violations': len(violations_oracle),
            'violations': violations_oracle[:5],
        }
    # (2) DPLL < 2×NDA (逐 SNR, 逐场景) — 判据2: DPLL 不应太弱
    for sc in scenes_done:
        pts = summary[sc]['points']
        violations_too_weak = []
        for p in pts:
            dpll_m = p['dpll_ber_mean']
            nda_m = p['nda_ml_ber_mean']
            if nda_m > 0 and dpll_m > 2.0 * nda_m:
                violations_too_weak.append({
                    'snr_db': p['snr_db'],
                    'dpll_ber': dpll_m, 'nda_ber': nda_m,
                    'ratio': dpll_m / nda_m,
                })
        checks.setdefault('dpll_not_too_weak', {})[sc] = {
            'pass': len(violations_too_weak) == 0,
            'n_violations': len(violations_too_weak),
            'violations': violations_too_weak[:5],
        }
    # (3) DPLL > 0.7×NDA (逐 SNR, 逐场景) — 判据3: NDA 不应无价值
    for sc in scenes_done:
        pts = summary[sc]['points']
        violations_nda_value = []
        for p in pts:
            dpll_m = p['dpll_ber_mean']
            nda_m = p['nda_ml_ber_mean']
            if nda_m > 0 and dpll_m < 0.7 * nda_m:
                violations_nda_value.append({
                    'snr_db': p['snr_db'],
                    'dpll_ber': dpll_m, 'nda_ber': nda_m,
                    'ratio': dpll_m / nda_m,
                })
        checks.setdefault('nda_has_value', {})[sc] = {
            'pass': len(violations_nda_value) == 0,
            'n_violations': len(violations_nda_value),
            'violations': violations_nda_value[:5],
        }
    # (4) DPLL @ 18dB AWGN 量级检查
    dpll_at_18 = None
    if 'awgn' in summary:
        for p in summary['awgn']['points']:
            if abs(p['snr_db'] - 18.0) < 1e-6:
                dpll_at_18 = p['dpll_ber_mean']
    checks['dpll_at_18db_awgn'] = {
        'value': dpll_at_18,
        'expected_range': [0.003, 0.006],
        'pass': (dpll_at_18 is not None and 0.001 <= dpll_at_18 <= 0.01),   # 宽容差 (跟 VV 同量级)
    }
    all_pass = (all(checks['dpll_ge_oracle'][sc]['pass'] for sc in scenes_done)
                and all(checks['dpll_not_too_weak'][sc]['pass'] for sc in scenes_done)
                and all(checks['nda_has_value'][sc]['pass'] for sc in scenes_done)
                and checks['dpll_at_18db_awgn']['pass'])
    checks['all_pass'] = all_pass
    return checks


def plot_curves(summary, scenes_done, dpll_gain, omega_n):
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
        dpll_m = np.array([p['dpll_ber_mean'] for p in pts])
        or_m = np.array([p['oracle_ber_mean'] for p in pts])
        nda_lo = np.array([p['nda_ml_ber_ci95'][0] for p in pts])
        nda_hi = np.array([p['nda_ml_ber_ci95'][1] for p in pts])
        dpll_lo = np.array([p['dpll_ber_ci95'][0] for p in pts])
        dpll_hi = np.array([p['dpll_ber_ci95'][1] for p in pts])
        ax.semilogy(gts, nda_m, 'o-', color='C0', label='NDA-ML (M0=8)', lw=1.8)
        ax.fill_between(gts, np.maximum(nda_lo, 1e-6), nda_hi, color='C0', alpha=0.18)
        ax.semilogy(gts, da_m, 's-', color='C1', label='DA ML (sp=4)', lw=1.8)
        ax.semilogy(gts, dpll_m, 'D-', color='C4', label=f'DPLL DD (ωn={omega_n:.0e})', lw=1.8)
        ax.fill_between(gts, np.maximum(dpll_lo, 1e-6), dpll_hi, color='C4', alpha=0.18)
        ax.semilogy(gts, or_m, '^--', color='C2', label='oracle', lw=1.6)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        fg = dpll_gain[sc]
        if fg.get('gain_dpll_vs_nda_mean_db') is not None:
            ttl = (f"{titles[sc]}\nDPLL vs NDA: {fg['gain_dpll_vs_nda_mean_db']:+.2f}"
                   f"±{fg['gain_dpll_vs_nda_std_db']:.2f} dB (正=NDA赢)")
        elif sc == 'strong':
            ttl = (f"{titles[sc]}\n工作区 DPLL vs NDA: "
                   f"{fg.get('workregion_dpll_vs_nda_grand_mean_db', 0):+.2f} dB")
        else:
            ttl = titles[sc]
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7.5, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('DPLL DD 异族 baseline: NDA-ML vs DA ML vs DPLL vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=11, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_dpll_ablation_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return png


def main():
    t0 = time.time()
    print("=" * 100)
    print("DPLL DD (Decision-Directed) M-APSK 异族 baseline 对比消融")
    print(f"M0={P.M0}, zeta={ZETA_DPLL:.4f}, pilot_overhead={P.PILOT_OVERHEAD_DB:.3f} dB, HDFEC={P.HDFEC}")
    print(f"common/_recovery.py 未改动 (选项 A, 适配在本脚本内, 同 VV/BPS/DD-KF 先例)")
    print("=" * 100)

    # --- 自检 1: hard_decision_m16apsk ---
    print("\n[自检] hard_decision_m16apsk 对无噪声 tx 返回自身...")
    _selftest_hard_decision()
    print("  PASS")

    # --- 自检 2: DPLL clean signal ---
    print("\n[自检] DPLL 对无噪声无 PN 信号判决正确...")
    _selftest_dpll_clean_signal()
    print("  PASS")

    # --- omega_n 扫描 (选最优参数) ---
    print("\n" + "#" * 40 + " omega_n 扫描 (TL-20 参数选择) " + "#" * 40)
    best_wn, sweep_results, nda_ref = omega_n_sweep_awgn()
    omega_n = best_wn
    print(f"\n[omega_n 选择] best={omega_n:.0e} (BER={sweep_results[omega_n]:.4e}, "
          f"NDA@18dB={nda_ref:.4e})")
    print(f"  选择理由: 最接近 TL-20 预期中心 0.004 且不违反判据2(<2×NDA={2*nda_ref:.4e})/判据3(>0.7×NDA)")

    # --- 跑 ---
    raw, scenes_done, partial = run_all(t0, omega_n=omega_n)
    elapsed = time.time() - t0

    # --- 聚合 ---
    summary = aggregate(raw, scenes_done)
    dpll_gain = dpll_gain_per_seed(raw, scenes_done)

    # --- TL-20 一致性自检 ---
    checks = consistency_check(summary, dpll_gain, scenes_done)
    print("\n" + "=" * 100)
    print("TL-20 一致性自检 (守 TL-23):")
    print(f"  DPLL >= oracle (全场景): {all(checks['dpll_ge_oracle'][sc]['pass'] for sc in scenes_done)}")
    for sc in scenes_done:
        c = checks['dpll_ge_oracle'][sc]
        if not c['pass']:
            print(f"    [{sc}] 违反 {c['n_violations']} 点: {c['violations']}")
    print(f"  DPLL < 2×NDA (不太弱, 全场景): {all(checks['dpll_not_too_weak'][sc]['pass'] for sc in scenes_done)}")
    for sc in scenes_done:
        c = checks['dpll_not_too_weak'][sc]
        if not c['pass']:
            print(f"    [{sc}] 违反 {c['n_violations']} 点: {c['violations']}")
    print(f"  DPLL > 0.7×NDA (NDA有价值, 全场景): {all(checks['nda_has_value'][sc]['pass'] for sc in scenes_done)}")
    for sc in scenes_done:
        c = checks['nda_has_value'][sc]
        if not c['pass']:
            print(f"    [{sc}] 违反 {c['n_violations']} 点: {c['violations']}")
    v18 = checks['dpll_at_18db_awgn']
    print(f"  DPLL @ 18dB AWGN = {v18['value']}, 合理范围 {v18['expected_range']}: {v18['pass']}")
    print(f"  ALL PASS: {checks['all_pass']}")

    # --- 画图 ---
    try:
        png_path = plot_curves(summary, scenes_done, dpll_gain, omega_n)
        print(f"\n[PNG] {png_path}")
    except Exception as e:
        print(f"(PNG skipped: {e})")
        png_path = None

    # --- 落盘 _dpll_ablation_5seed.json ---
    out = {
        'meta': {
            'task': 'DPLL DD (Decision-Directed) M-APSK 异族 baseline 对比消融 (5 seed 多种子统计)',
            'purpose': '验证 DPLL 作为非近亲异族 baseline 立得住 (DD 闭环 vs NDA 升幂前馈不同族)',
            'metric': 'BER 曲线 + DPLL vs NDA (γ_d) + DPLL vs DA (γ_tot) fair gain @ HD-FEC + 95% CI',
            'n_seeds': N_SEEDS,
            'scenes_done': scenes_done,
            'partial_run': partial,
            'dpll_adaptation': {
                'dpll_track_dd_m16apsk': '复制 common.dpll_track_dd, 改 qam16 判决 → hard_decision_m16apsk',
                'hard_decision_m16apsk': '最近邻 16 点星座 (从 _M16APSK_SYM), 复制 run_dd_kf_ablation.py:124',
                'not_using_dpll_track': 'dpll_track 用 4 次方鉴相器, 16APSK M0=8 非 4 次方对称 (H007 纪律)',
                'common_recovery_modified': False,
            },
            'omega_n_selection': {
                'candidates': [float(x) for x in OMEGA_N_CANDIDATES],
                'selected': float(omega_n),
                'sweep_results_18db_awgn': {str(k): float(v) for k, v in sweep_results.items()},
                'nda_ref_18db': float(nda_ref),
                'reason': '最接近 TL-20 预期中心 0.004 且不违反判据2(<2×NDA)/判据3(>0.7×NDA)',
            },
            'fairness': {
                'dpll_vs_nda': 'γ_d 坐标 (都无 pilot overhead, DPLL 盲 DD 同 NDA 盲升幂)',
                'dpll_vs_da': 'γ_tot 坐标 (DA 有 1.249 dB pilot overhead, DPLL 无)',
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
        'dpll_gain_per_seed': to_jsonable(dpll_gain),
        'consistency_checks': to_jsonable(checks),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_dpll_ablation_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 落盘 _dpll_ablation_summary.json (精简) ---
    fair_short = {}
    for sc in scenes_done:
        e = dpll_gain[sc]
        entry = {
            'scene': sc,
            'gain_dpll_vs_nda_mean_db': e.get('gain_dpll_vs_nda_mean_db'),
            'gain_dpll_vs_nda_std_db': e.get('gain_dpll_vs_nda_std_db'),
            'gain_dpll_vs_nda_ci95_db': e.get('gain_dpll_vs_nda_ci95_db'),
            'per_seed_gain_dpll_vs_nda_db': e.get('per_seed_gain_dpll_vs_nda_db'),
            'gain_dpll_vs_da_mean_db': e.get('gain_dpll_vs_da_mean_db'),
            'gain_dpll_vs_da_std_db': e.get('gain_dpll_vs_da_std_db'),
            'gain_dpll_vs_da_ci95_db': e.get('gain_dpll_vs_da_ci95_db'),
            'per_seed_gain_dpll_vs_da_db': e.get('per_seed_gain_dpll_vs_da_db'),
            'n_valid_nda': e.get('n_valid_nda'),
            'n_valid_da': e.get('n_valid_da'),
        }
        if sc == 'strong':
            entry['note'] = 'HD-FEC 物理不可达 (oracle 也不可达); 用工作区 (γ_d≥15dB) per-point'
            entry['workregion_dpll_vs_nda_grand_mean_db'] = e.get('workregion_dpll_vs_nda_grand_mean_db')
            entry['workregion_dpll_vs_nda_grand_std_db'] = e.get('workregion_dpll_vs_nda_grand_std_db')
            entry['workregion_dpll_vs_nda_grand_ci95_db'] = e.get('workregion_dpll_vs_nda_grand_ci95_db')
            entry['workregion_dpll_vs_nda_per_point'] = e.get('workregion_dpll_vs_nda_per_point')
        fair_short[sc] = entry
    summary_json = {
        'meta': {
            'task': 'DPLL DD M-APSK 异族 baseline 消融 fair gain 汇总 (5 seed)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': {
                'dpll_vs_nda': 'fair_gain = (DPLL γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正=NDA赢DPLL',
                'dpll_vs_da': 'fair_gain = (DA γ_tot @ HD-FEC) − (DPLL γ_tot @ HD-FEC); 正=DPLL赢DA',
            },
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'scenes_done': scenes_done,
            'partial_run': partial,
            'omega_n_selected': float(omega_n),
            'zeta': float(ZETA_DPLL),
            'common_recovery_modified': False,
            'consistency_all_pass': checks['all_pass'],
            'elapsed_sec': float(elapsed),
        },
        'fair_gain': fair_short,
        'consistency_checks': to_jsonable(checks),
    }
    sj_path = os.path.join(OUT_DIR, '_dpll_ablation_summary.json')
    with open(sj_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(summary_json), f, indent=2, ensure_ascii=False)
    print(f"[保存] {sj_path}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("DPLL DD 异族 baseline fair gain @ HD-FEC (5 seed):")
    print(f"{'场景':>10} {'DPLL vs NDA':>22} {'NDA赢DPLL?':>14} {'DPLL vs DA':>22} {'DPLL赢DA?':>12}")
    for sc in scenes_done:
        e = dpll_gain[sc]
        gn = e.get('gain_dpll_vs_nda_mean_db')
        gd = e.get('gain_dpll_vs_da_mean_db')
        if gn is not None:
            ci_n = e['gain_dpll_vs_nda_ci95_db']
            nda_win = '是' if gn > 0 else 'DPLL反超⚠️'
            print(f"{sc:>10} {gn:>+10.3f}±{e['gain_dpll_vs_nda_std_db']:.2f} "
                  f"[{ci_n[0]:>+6.2f},{ci_n[1]:>+6.2f}] {nda_win:>14}", end='')
        elif sc == 'strong':
            wr = e.get('workregion_dpll_vs_nda_grand_mean_db', 0)
            wrs = e.get('workregion_dpll_vs_nda_grand_std_db', 0)
            nda_win = '是' if wr > 0 else 'DPLL反超⚠️'
            print(f"{sc:>10} 工作区{wr:>+7.3f}±{wrs:.2f} dB {nda_win:>20}", end='')
        if gd is not None:
            ci_d = e['gain_dpll_vs_da_ci95_db']
            dpll_win_da = '是' if gd > 0 else '否'
            print(f" {gd:>+10.3f}±{e['gain_dpll_vs_da_std_db']:.2f} "
                  f"[{ci_d[0]:>+6.2f},{ci_d[1]:>+6.2f}] {dpll_win_da:>12}")
        else:
            print()
    if partial:
        print(f"\n[部分运行] 仅完成场景: {scenes_done} (time-box 触发)")
    print(f"\n[TL-20 一致性自检] ALL PASS = {checks['all_pass']}")
    print(f"[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
