# -*- coding: utf-8 -*-
"""BPS (Blind Phase Search) M-APSK 迁移对比消融 (FR baseline-legitimacy 反转验证).

回答用户担心 (baseline 合法性): 光纤 square-QAM 子领域 CPR 主流基准是 BPS
(Blind Phase Search, Pfau 2009 JLT; Diniz'19 / Blatter'25 都显式对比 BPS).
reviewer 来自 fiber 背景会问 "为何不跟 BPS 比". 本消融测 BPS 在 (8,8)-16APSK +
星地湍流场景下 vs NDA-ML / DA ML.

BPS 现状 (common/_recovery.py:bps_cpr): 已实现 Pfau 2009 版, 但默认 mod='qpsk'/'qam16',
hard_decision 不支持 m16apsk, 且 M=4 相位模糊展开 (QPSK 用). 本任务核心 = 适配
m16apsk + M0=8 模糊展开.

适配 (选项 A: 不改 common/_recovery.py, 适配在本消融脚本内):
  (1) hard_decision_m16apsk(z): 最近邻星座点判定 (从 m16apsk_mod 的 16 点集找).
  (2) bps_cpr_m16apsk(rx, B, Nw): 复制 bps_cpr, 改 hard_decision → m16apsk 版,
      改 M=4 模糊展开 → M0=8 展开 (pe = np.unwrap(8*pe_raw)/8).
  (3) B (测试相位数): Pfau 2009 推荐 B=32 (QPSK) / B=64 (QAM); M-APSK 用 B=64
      (单调制阶数高 → 测试相位网格更密; 主辅).

公平性 (§2.4 关键纪律):
  - BPS 无 pilot overhead (盲估, 同 NDA): NDA vs BPS 公平对照用 γ_d 坐标.
  - BPS vs DA 用 γ_tot 坐标 (DA 有 1.249 dB pilot overhead, BPS 无 → γ_tot=γ_d).
  - resolve M0-fold 模糊同 NDA-ML 流程 (resolve_m16apsk_blockwise, per-block 选最优旋转).

种子 (§2.3 纪律 3): 5 seed, 第 0 seed = MVE seed (SEED_AWGN/SEED_TURB0).
  AWGN: seed_base_i = SEED_AWGN + i
  湍流: seed0_i = SEED_TURB0 + i·N_BLOCKS (5 seed 块范围互斥)

运行: cd projects/simulation && python simulator/run_bps_ablation.py
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
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_bps_ablation')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# =============================================================================
# BPS-M16APSK 适配 (选项 A: 在本消融脚本内, 不改 common/_recovery.py)
# =============================================================================
# 从 m16apsk_mod 重建 (8,8)-16APSK 星座点集 (16 个点, _M16APK_SYM 等价).
_BITS_ALL_LABELS = np.zeros(16 * 4, dtype=int)
for _lab in range(16):
    _BITS_ALL_LABELS[_lab * 4 + 0] = (_lab >> 3) & 1
    _BITS_ALL_LABELS[_lab * 4 + 1] = (_lab >> 2) & 1
    _BITS_ALL_LABELS[_lab * 4 + 2] = (_lab >> 1) & 1
    _BITS_ALL_LABELS[_lab * 4 + 3] = _lab & 1
_M16APSK_CONST = m16apsk_mod(_BITS_ALL_LABELS)   # (16,) 16 个星座点 (按 label 0..15 排序)


def hard_decision_m16apsk(z):
    """最近邻星座点判定 for (8,8)-16APSK (BPS 内部用).

    对每符号独立算到 16 个星座点的欧氏距离, 返回最近星座点 (复数).
    等价于 m16apsk_demod 的距离判定但返回星座点 (非 bits).
    支持标量 + 任意 shape 数组 (返回同 shape).
    验证: 对 tx 符号 (无噪声) 应返回自身.
    """
    z = np.asarray(z, dtype=complex)
    flat = z.reshape(-1)
    # 距离矩阵 (N, 16)
    dist = np.abs(flat[:, np.newaxis] - _M16APSK_CONST[np.newaxis, :]) ** 2
    idx = np.argmin(dist, axis=1)
    dec = _M16APSK_CONST[idx]
    return dec.reshape(z.shape)


# BPS 测试相位数: Pfau 2009 推荐 B=32 (QPSK) / B=64 (QAM). (8,8)-16APSK 调制阶数高
# (16 点, 接近 16-QAM), 测试相位网格需更密 → B=64 (Pfau 2009 QAM 推荐, 记录理由).
B_BPS_M16 = 64
# 滑窗 Nw: Pfau 2009 推荐 Nw ~ 数十. 对齐 N_DFT=256 块内, Nw=101 (奇数, 'same' 模式对称).
NW_BPS_M16 = 101


def bps_cpr_m16apsk(rx, B=B_BPS_M16, Nw=NW_BPS_M16):
    """BPS-CPR 适配 (8,8)-16APSK (复制 common.bps_cpr, 改 hard_decision + M0=8 展开).

    B 个测试相位, Nw 符号滑动窗口平均距离度量. 用 M0=8 相位模糊展开解 (8,8)-16APSK
    重模糊 (QPSK 用 M=4; (8,8)-16APSK 两环各 8 点 → 升幂等效 M0=8 重模糊).

    来源: Pfau 2009 JLT (common/_recovery.py:bps_cpr), M0=8 展开依据
          B11 行 75-77 升幂阶数 + params.py M0_POWER=8.
    返回 (rx_compensated, pe).
    """
    N = len(rx)
    phases = 2 * np.pi * np.arange(B) / B
    rotated = rx[np.newaxis, :] * np.exp(-1j * phases[:, np.newaxis])
    dec = hard_decision_m16apsk(rotated)
    dist = np.abs(rotated - dec) ** 2
    metrics = dist / (np.abs(dec) ** 2 + 1e-10)   # 归一化距离 (避免幅度偏置, 同 bps_cpr QAM 分支)
    # 滑窗平均
    ker = np.ones(Nw) / Nw
    for b in range(B):
        metrics[b] = np.convolve(metrics[b], ker, mode='same')
    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]
    # M0=8 相位模糊展开 (关键: 不是 M=4): 乘 8 → unwrap 2π 跳变 → 除 8
    pe = np.unwrap(8 * pe_raw) / 8
    return rx * np.exp(-1j * pe), pe


# =============================================================================
# 验证: hard_decision_m16apsk 对无噪声 tx 应返回自身
# =============================================================================
def _selftest_hard_decision():
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 64 * 4)
    tx = m16apsk_mod(bits)
    dec = hard_decision_m16apsk(tx)
    err = np.max(np.abs(tx - dec))
    assert err < 1e-12, f"hard_decision_m16apsk 自检失败: max|tx-dec|={err}"
    return True


# =============================================================================
# BPS BER 评估 (AWGN + 湍流)
# =============================================================================
def ber_bps_awgn(rx, tx_bits):
    """BPS-M16APSK AWGN: 逐块 BPS-CPR + resolve M0-fold 模糊. 返回 (n_err, n_bits).

    逐块 (N_DFT) 跑 bps_cpr_m16apsk, 再 resolve_m16apsk_blockwise 解 M0=8 模糊
    (同 NDA-ML 流程, per-block 选最优旋转). BPS 无 pilot overhead.
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _ = bps_cpr_m16apsk(seg)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_bps_turb_eval(rx, tx_bits):
    """BPS-M16APSK 湍流: 逐块 BPS-CPR (rx 已 per-block h 均衡) + resolve. 返回 (n_err, n_bits).

    注: BPS 对湍流场景假设两阶段 (fft_foe + BPS CPE), 但 fft_foe 是 4 次幂法 (QPSK 专用,
    M0≠4 不适用). 此处用 fft_foe_m0_omega (M0=8 升幂 FOE, 同 NDA-ML 湍流两阶段第一阶段),
    再 per-block BPS CPE. 公平: BPS 用与 NDA 相同的 FOE 前端 (两阶段对称).
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
        rc, _ = bps_cpr_m16apsk(seg_foe)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# SNR 扫描: AWGN + 湍流 (BPS + 复用主实验 NDA/DA/oracle)
# =============================================================================
def run_awgn_bps(n_blocks, snr_points, seed_base):
    """AWGN: BPS + NDA + DA + oracle BER 扫描. 复用 awgn_wiener_channel (同 seed 派生)."""
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN BPS] N_sym={N_sym}/点, B={B_BPS_M16}, Nw={NW_BPS_M16}, M0=8 unwrap")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'BPS_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = S.awgn_wiener_channel(tx, snr, seed)
        ne_nda, nb_nda = S.ber_nda_awgn(rx, bits)
        ne_da, nb_da = S.ber_da_awgn(rx, bits)
        ne_bps, nb_bps = ber_bps_awgn(rx, bits)
        ne_or, nb_or = S.ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_bps = ne_bps / nb_bps
        b_or = ne_or / nb_or
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_bps:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_bps': float(snr),   # BPS 无 pilot overhead
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'bps_ber': b_bps, 'oracle_ber': b_or,
        })
    return per_snr


def run_turb_bps(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0):
    """湍流: BPS + NDA + DA + oracle BER 扫描. 复用 generate_shared_realization_apsk."""
    Ns = P.N_DFT
    print(f"[{turb_name} BPS] N_sym={n_blocks*Ns}/点, per-block h 均衡 + BPS 两阶段 fft_foe+BPS CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'BPS_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = ne_da = ne_bps = ne_or = 0
        nb_nda = nb_da = nb_bps = nb_or = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (per-block h, 同主实验): BPS 用盲 h 估计 (同 NDA, 公平)
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            ne, nb = S.ber_nda_turb_eval(rx_blind, bits)
            ne_nda += ne; nb_nda += nb
            ne, nb = S.ber_da_turb(rx_pilot, bits)
            ne_da += ne; nb_da += nb
            ne, nb = ber_bps_turb_eval(rx_blind, bits)
            ne_bps += ne; nb_bps += nb
            ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
            ne_or += ne; nb_or += nb
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_bps = ne_bps / nb_bps
        b_or = ne_or / nb_or
        print(f"{gamma_db:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_bps:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + P.PILOT_OVERHEAD_DB,
            'snr_db_total_bps': float(gamma_db),
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'bps_ber': b_bps, 'oracle_ber': b_or,
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
# BPS vs NDA / DA 公平 gain 分析
# =============================================================================
def analyze_bps_gain(per_snr, hdfec, pilot_overhead_db):
    """BPS vs NDA (γ_d 坐标, 都无 pilot) + BPS vs DA (γ_tot 坐标, BPS 无 pilot).

    fair_gain_BPS_vs_NDA = (BPS γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正 = NDA 赢 BPS.
    fair_gain_BPS_vs_DA  = (DA γ_tot @ HD-FEC) − (BPS γ_tot @ HD-FEC)
                          = (DA γ_d @ HD-FEC + overhead) − (BPS γ_d @ HD-FEC); 正 = BPS 赢 DA.
    """
    snrs = np.array([p['snr_db'] for p in per_snr])
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_bps = np.array([p['bps_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])

    s_nda = snr_at_ber(snrs, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs, b_da, hdfec)
    s_bps = snr_at_ber(snrs, b_bps, hdfec)
    s_or = snr_at_ber(snrs, b_or, hdfec)

    # BPS vs NDA (γ_d 坐标, 都无 pilot overhead): 正 = NDA 赢
    gain_bps_vs_nda = None
    if s_bps is not None and s_nda is not None:
        gain_bps_vs_nda = s_bps - s_nda
    # BPS vs DA (γ_tot 坐标): 正 = BPS 赢 DA
    gain_bps_vs_da = None
    if s_bps is not None and s_da_d is not None:
        gain_bps_vs_da = (s_da_d + pilot_overhead_db) - s_bps

    # 逐点 (γ_d 坐标): BPS 达 NDA BER 所需 γ_d − NDA γ_d
    per_point_bps_vs_nda = []
    for i, gd in enumerate(snrs):
        ber_nda_at = b_nda[i]
        s_bps_needed = snr_at_ber(snrs, b_bps, ber_nda_at)
        if s_bps_needed is not None:
            per_point_bps_vs_nda.append({
                'gamma_d_db': float(gd),
                'ber_nda': float(ber_nda_at),
                'snr_bps_needed_db': float(s_bps_needed),
                'bps_vs_nda_gain_db': float(s_bps_needed - gd),   # 正 = NDA 赢 BPS
            })

    hdfec_reachable = (s_bps is not None and s_nda is not None)

    return {
        'snr_nda_d_at_hdfec': s_nda,
        'snr_da_tot_at_hdfec': (s_da_d + pilot_overhead_db) if s_da_d is not None else None,
        'snr_bps_d_at_hdfec': s_bps,
        'snr_oracle_at_hdfec': s_or,
        'gain_bps_vs_nda_db': gain_bps_vs_nda,      # 正 = NDA 赢 BPS
        'gain_bps_vs_da_db': gain_bps_vs_da,         # 正 = BPS 赢 DA
        'hdfec_reachable': hdfec_reachable,
        'per_point_bps_vs_nda': per_point_bps_vs_nda,
        'min_bps_ber': float(np.min(b_bps)),
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
    print(f"BPS M-APSK 迁移消融: {N_SEEDS} seed × {len(SCENES)} 场景")
    print(f"B={B_BPS_M16} (Pfau 2009 QAM 推荐), Nw={NW_BPS_M16}, M0=8 unwrap (非 M=4)")
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
        raw['awgn'][i] = run_awgn_bps(P.N_BLOCKS, P.SNR_AWGN_DB, sb)
    scenes_done.append('awgn')

    # --- 湍流 ---
    for turb in TURB_LEVELS:
        for i in range(N_SEEDS):
            if time.time() - t_start > time_budget:
                print(f"\n[TIME-BOX] 超 {time_budget}s, 停在 {turb} seed {i}")
                return raw, scenes_done, True
            s0 = seed0_turb(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = run_turb_bps(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)
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
            bps = [per_seed[i][j]['bps_ber'] for i in range(n_sd)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(n_sd)]
            m_nda, s_nda, hw_nda, lo_nda, hi_nda = ci_t(nda)
            m_da, s_da, hw_da, lo_da, hi_da = ci_t(da)
            m_bps, s_bps, hw_bps, lo_bps, hi_bps = ci_t(bps)
            m_or, s_or, hw_or, lo_or, hi_or = ci_t(orc)
            points.append({
                'snr_db': float(snr),
                'nda_ml_ber_mean': m_nda, 'nda_ml_ber_std': s_nda,
                'nda_ml_ber_ci95': [lo_nda, hi_nda],
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'da_ml_ber_ci95': [lo_da, hi_da],
                'bps_ber_mean': m_bps, 'bps_ber_std': s_bps,
                'bps_ber_ci95': [lo_bps, hi_bps],
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
                'oracle_ber_ci95': [lo_or, hi_or],
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def bps_gain_per_seed(raw, scenes_done):
    out = {}
    for sc in scenes_done:
        per_seed = raw[sc]
        n_sd = len(per_seed)
        gains_bps_nda = []
        gains_bps_da = []
        wr_bps_vs_nda = {}   # strong 工作区 per-point
        for i in range(n_sd):
            per_snr = per_seed[i]
            fg = analyze_bps_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            gains_bps_nda.append(fg['gain_bps_vs_nda_db'])
            gains_bps_da.append(fg['gain_bps_vs_da_db'])
            for p in fg['per_point_bps_vs_nda']:
                if p['gamma_d_db'] >= 15.0:
                    wr_bps_vs_nda.setdefault(p['gamma_d_db'], []).append(
                        float(p['bps_vs_nda_gain_db']))
        entry = {
            'per_seed_gain_bps_vs_nda_db': [None if g is None else float(g) for g in gains_bps_nda],
            'per_seed_gain_bps_vs_da_db': [None if g is None else float(g) for g in gains_bps_da],
        }
        v_nda = [g for g in gains_bps_nda if g is not None]
        v_da = [g for g in gains_bps_da if g is not None]
        if len(v_nda) >= 2:
            m, s, hw, lo, hi = ci_t(v_nda)
            entry.update({'gain_bps_vs_nda_mean_db': m, 'gain_bps_vs_nda_std_db': s,
                          'gain_bps_vs_nda_ci95_db': [lo, hi], 'n_valid_nda': len(v_nda)})
        else:
            entry.update({'gain_bps_vs_nda_mean_db': None, 'gain_bps_vs_nda_std_db': None,
                          'gain_bps_vs_nda_ci95_db': [None, None], 'n_valid_nda': len(v_nda)})
        if len(v_da) >= 2:
            m, s, hw, lo, hi = ci_t(v_da)
            entry.update({'gain_bps_vs_da_mean_db': m, 'gain_bps_vs_da_std_db': s,
                          'gain_bps_vs_da_ci95_db': [lo, hi], 'n_valid_da': len(v_da)})
        else:
            entry.update({'gain_bps_vs_da_mean_db': None, 'gain_bps_vs_da_std_db': None,
                          'gain_bps_vs_da_ci95_db': [None, None], 'n_valid_da': len(v_da)})
        # strong 工作区 per-point
        if sc == 'strong' and wr_bps_vs_nda:
            wr_points = []
            all_wr = []
            for gd in sorted(wr_bps_vs_nda.keys()):
                col = wr_bps_vs_nda[gd]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({'gamma_d_db': float(gd), 'n_seeds': len(col),
                                  'bps_vs_nda_gain_mean_db': m, 'bps_vs_nda_gain_std_db': s,
                                  'bps_vs_nda_gain_ci95_db': [lo, hi]})
                all_wr.extend(col)
            entry['workregion_bps_vs_nda_per_point'] = wr_points
            gm, gs, ghw, glo, ghi = ci_t(all_wr)
            entry['workregion_bps_vs_nda_grand_mean_db'] = gm
            entry['workregion_bps_vs_nda_grand_std_db'] = gs
            entry['workregion_bps_vs_nda_grand_ci95_db'] = [glo, ghi]
        out[sc] = entry
    return out


def plot_curves(summary, scenes_done, bps_gain):
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
        bps_m = np.array([p['bps_ber_mean'] for p in pts])
        or_m = np.array([p['oracle_ber_mean'] for p in pts])
        nda_lo = np.array([p['nda_ml_ber_ci95'][0] for p in pts])
        nda_hi = np.array([p['nda_ml_ber_ci95'][1] for p in pts])
        bps_lo = np.array([p['bps_ber_ci95'][0] for p in pts])
        bps_hi = np.array([p['bps_ber_ci95'][1] for p in pts])
        ax.semilogy(gts, nda_m, 'o-', color='C0', label='NDA-ML (M0=8)', lw=1.8)
        ax.fill_between(gts, np.maximum(nda_lo, 1e-6), nda_hi, color='C0', alpha=0.18)
        ax.semilogy(gts, da_m, 's-', color='C1', label='DA ML (sp=4)', lw=1.8)
        ax.semilogy(gts, bps_m, 'D-', color='C3', label=f'BPS (B={B_BPS_M16})', lw=1.8)
        ax.fill_between(gts, np.maximum(bps_lo, 1e-6), bps_hi, color='C3', alpha=0.18)
        ax.semilogy(gts, or_m, '^--', color='C2', label='oracle', lw=1.6)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
        fg = bps_gain[sc]
        if fg.get('gain_bps_vs_nda_mean_db') is not None:
            ttl = (f"{titles[sc]}\nBPS vs NDA: {fg['gain_bps_vs_nda_mean_db']:+.2f}"
                   f"±{fg['gain_bps_vs_nda_std_db']:.2f} dB (正=NDA赢)")
        elif sc == 'strong':
            ttl = (f"{titles[sc]}\n工作区 BPS vs NDA: "
                   f"{fg.get('workregion_bps_vs_nda_grand_mean_db', 0):+.2f} dB")
        else:
            ttl = titles[sc]
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7.5, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('BPS M-APSK 迁移消融: NDA-ML vs DA ML vs BPS vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=11, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_bps_ablation_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    plt.close(fig)
    return png


def main():
    t0 = time.time()
    print("=" * 100)
    print("BPS (Blind Phase Search) M-APSK 迁移对比消融")
    print(f"M0={P.M0}, B={B_BPS_M16} (Pfau 2009 QAM 推荐), Nw={NW_BPS_M16}, "
          f"pilot_overhead={P.PILOT_OVERHEAD_DB:.3f} dB, HDFEC={P.HDFEC}")
    print(f"common/_recovery.py 未改动 (选项 A, 适配在本脚本内)")
    print("=" * 100)

    # --- 自检 ---
    print("\n[自检] hard_decision_m16apsk 对无噪声 tx 返回自身...")
    _selftest_hard_decision()
    print("  PASS ✅ (max|tx-dec|<1e-12)")

    # --- 跑 ---
    raw, scenes_done, partial = run_all(t0)
    elapsed = time.time() - t0

    # --- 聚合 ---
    summary = aggregate(raw, scenes_done)
    bps_gain = bps_gain_per_seed(raw, scenes_done)

    # --- 画图 ---
    try:
        png_path = plot_curves(summary, scenes_done, bps_gain)
        print(f"\n[PNG] {png_path}")
    except Exception as e:
        print(f"(PNG skipped: {e})")
        png_path = None

    # --- 落盘 _bps_ablation_5seed.json ---
    out = {
        'meta': {
            'task': 'BPS M-APSK 迁移对比消融 (5 seed 多种子统计)',
            'purpose': '回答 reviewer baseline 合法性: BPS (光纤主流) 迁移到 M-APSK vs NDA-ML',
            'metric': 'BER 曲线 + BPS vs NDA (γ_d) + BPS vs DA (γ_tot) fair gain @ HD-FEC + 95% CI',
            'n_seeds': N_SEEDS,
            'scenes_done': scenes_done,
            'partial_run': partial,
            'bps_adaptation': {
                'hard_decision_m16apsk': '最近邻 16 点星座 (从 m16apsk_mod 重建 _M16APSK_CONST)',
                'M0_unwrap': 'M0=8 (非 M=4), pe=unwrap(8*pe_raw)/8 (B11 行 75-77 升幂阶数)',
                'B_test_phases': B_BPS_M16,
                'B_choice_reason': 'Pfau 2009 推荐 B=64 for QAM; (8,8)-16APSK 调制阶数高→网格更密',
                'Nw_window': NW_BPS_M16,
                'Nw_choice_reason': 'Pfau 2009 Nw~数十; 对齐 N_DFT=256 块内, Nw=101 (奇数对称)',
                'common_recovery_modified': False,
            },
            'fairness': {
                'bps_vs_nda': 'γ_d 坐标 (都无 pilot overhead, 同类盲估)',
                'bps_vs_da': 'γ_tot 坐标 (DA 有 1.249 dB pilot overhead, BPS 无)',
                'resolve': 'resolve_m16apsk_blockwise (per-block M0-fold 模糊, 同 NDA-ML 流程)',
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
        'bps_gain_per_seed': to_jsonable(bps_gain),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_bps_ablation_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 落盘 _bps_ablation_summary.json (精简) ---
    fair_short = {}
    for sc in scenes_done:
        e = bps_gain[sc]
        entry = {
            'scene': sc,
            'gain_bps_vs_nda_mean_db': e.get('gain_bps_vs_nda_mean_db'),
            'gain_bps_vs_nda_std_db': e.get('gain_bps_vs_nda_std_db'),
            'gain_bps_vs_nda_ci95_db': e.get('gain_bps_vs_nda_ci95_db'),
            'per_seed_gain_bps_vs_nda_db': e.get('per_seed_gain_bps_vs_nda_db'),
            'gain_bps_vs_da_mean_db': e.get('gain_bps_vs_da_mean_db'),
            'gain_bps_vs_da_std_db': e.get('gain_bps_vs_da_std_db'),
            'gain_bps_vs_da_ci95_db': e.get('gain_bps_vs_da_ci95_db'),
            'per_seed_gain_bps_vs_da_db': e.get('per_seed_gain_bps_vs_da_db'),
            'n_valid_nda': e.get('n_valid_nda'),
            'n_valid_da': e.get('n_valid_da'),
        }
        if sc == 'strong':
            entry['note'] = 'HD-FEC 物理不可达 (oracle 也不可达); 用工作区 (γ_d≥15dB) per-point'
            entry['workregion_bps_vs_nda_grand_mean_db'] = e.get('workregion_bps_vs_nda_grand_mean_db')
            entry['workregion_bps_vs_nda_grand_std_db'] = e.get('workregion_bps_vs_nda_grand_std_db')
            entry['workregion_bps_vs_nda_grand_ci95_db'] = e.get('workregion_bps_vs_nda_grand_ci95_db')
            entry['workregion_bps_vs_nda_per_point'] = e.get('workregion_bps_vs_nda_per_point')
        fair_short[sc] = entry
    summary_json = {
        'meta': {
            'task': 'BPS M-APSK 迁移消融 fair gain 汇总 (5 seed)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': {
                'bps_vs_nda': 'fair_gain = (BPS γ_d @ HD-FEC) − (NDA γ_d @ HD-FEC); 正=NDA赢BPS',
                'bps_vs_da': 'fair_gain = (DA γ_tot @ HD-FEC) − (BPS γ_tot @ HD-FEC); 正=BPS赢DA',
            },
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'scenes_done': scenes_done,
            'partial_run': partial,
            'B_test_phases': B_BPS_M16,
            'M0_unwrap': 8,
            'common_recovery_modified': False,
            'elapsed_sec': float(elapsed),
        },
        'fair_gain': fair_short,
    }
    sj_path = os.path.join(OUT_DIR, '_bps_ablation_summary.json')
    with open(sj_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(summary_json), f, indent=2, ensure_ascii=False)
    print(f"[保存] {sj_path}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("BPS M-APSK 迁移消融 fair gain @ HD-FEC (5 seed):")
    print(f"{'场景':>10} {'BPS vs NDA':>22} {'BPS反超NDA?':>14} {'BPS vs DA':>22} {'BPS赢DA?':>12}")
    for sc in scenes_done:
        e = bps_gain[sc]
        gn = e.get('gain_bps_vs_nda_mean_db')
        gd = e.get('gain_bps_vs_da_mean_db')
        if gn is not None:
            ci_n = e['gain_bps_vs_nda_ci95_db']
            overtake = '是⚠️' if gn < 0 else '否'
            print(f"{sc:>10} {gn:>+10.3f}±{e['gain_bps_vs_nda_std_db']:.2f} "
                  f"[{ci_n[0]:>+6.2f},{ci_n[1]:>+6.2f}] {overtake:>14}", end='')
        elif sc == 'strong':
            wr = e.get('workregion_bps_vs_nda_grand_mean_db', 0)
            wrs = e.get('workregion_bps_vs_nda_grand_std_db', 0)
            overtake = '是⚠️' if wr < 0 else '否'
            print(f"{sc:>10} 工作区{wr:>+7.3f}±{wrs:.2f} dB {overtake:>20}", end='')
        if gd is not None:
            ci_d = e['gain_bps_vs_da_ci95_db']
            bps_win_da = '是' if gd > 0 else '否'
            print(f" {gd:>+10.3f}±{e['gain_bps_vs_da_std_db']:.2f} "
                  f"[{ci_d[0]:>+6.2f},{ci_d[1]:>+6.2f}] {bps_win_da:>12}")
        else:
            print()
    if partial:
        print(f"\n[部分运行] 仅完成场景: {scenes_done} (time-box 触发)")
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
