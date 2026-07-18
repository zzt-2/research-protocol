# -*- coding: utf-8 -*-
"""上行 NDA-ML vs VV/BPS 对照 + VV Nw 扫描 (查 "segmented 拉开 VV 是真机制还是 VV 参数没调好").

3 实验 (brief §2):
  实验 1: 上行 uplink_moderate/uplink_strong × NDA(none) / VV(Nw=64) / BPS / DA / oracle
          (5 个一起跑, 三方同信道同 seed). SNR=P.SNR_TURB_DB, 5 seed = seed0_uplink(i).
  实验 2: AWGN (8,8)-16APSK, SNR=18dB, 线宽 [200,500]kHz, VV Nw=[8,16,32,64,128] 扫描
          vs NDA-segmented(等权 K=8). 查 VV 调 Nw 能否追上 segmented.
  实验 3: 上行 uplink_strong SNR=20dB, 同 VV Nw 扫描 vs NDA-segmented.

最高纪律 (brief §0):
  1. 只改本 explore/nda-awgn-tracking-sandbox/ 目录, 绝不改 common/simulator/params.
  2. 复用已有函数 (S.run_turb 思路 / S.ber_nda_turb_eval / VV.ber_vv_turb_eval /
     BPS.ber_bps_turb_eval / generate_shared_realization_apsk), 不重写.
  3. 三方同信道同 seed (公平对照): NDA/VV/BPS/DA/oracle 用同一 rx.
  4. 只跑数字 + 机械分类, 不判断方向不建议.

机制要点 (brief §3 + 已知陷阱):
  - 实验 1 上行 NDA 用 'none' 模式 (湍流主实验设定, 非 segmented). S.ber_nda_turb_eval 默认 none.
  - 实验 2/3 NDA-segmented 自己写 nda_segmented_eq(seg, M0, K=8): unwrap 在升幂域, 等权.
  - VV Nw 扫描: 改 VV.vv_cpr_m16apsk(seg, Nw=X) 的 X.
  - 信道公平: 湍流场景 NDA/VV/BPS 用同一 rx_blind (同 h_blind 估计 + 同 mmse_equalize + amp_limit).

运行: cd projects/simulation && python explore/nda-awgn-tracking-sandbox/uplink_vv_check.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径: simulation 根 (与 sc_nda_ml_sim.py / run_vv_ablation.py 同构) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守纪律 1: 不改 common/simulator/params)
from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402  (参数只读)
import sc_nda_ml_sim as S  # noqa: E402  (复用 ber_nda_turb_eval / ber_da_turb / ber_oracle_turb / estimate_h / fft_foe)
import run_vv_ablation as VV  # noqa: E402  (复用 vv_cpr_m16apsk / ber_vv_turb_eval)
import run_bps_ablation as BPS  # noqa: E402  (复用 bps_cpr_m16apsk / ber_bps_turb_eval)
from fair_comparison import snr_at_ber  # noqa: E402
from params import SimulationConfig  # noqa: E402
from scipy import stats  # noqa: E402

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764
UPLINK_SEED_OFFSET = 500000   # 同 run_uplink_experiment.py (错开下行 seed 范围)


# =============================================================================
# 上行 seed (同 run_uplink_experiment.seed0_uplink, 保证与上行主实验 seed 一致可比)
# =============================================================================
def seed0_uplink(i):
    return P.SEED_TURB0 + UPLINK_SEED_OFFSET + i * P.N_BLOCKS


# =============================================================================
# NDA-segmented 等权恢复 (brief §3): unwrap 在升幂域, 最后 /M0. K=8.
# 用于实验 2/3 高线宽对照 (D-009 segmented 在高线宽拉开 VV).
# 数学 bit-exact 对齐 common/_recovery.py:224-229 (segmented 分支) + vv_vs_nda_checkup 等权版.
# =============================================================================
def nda_segmented_eq(seg, M0, K=8):
    """NDA-segmented 等权块内 CPE 恢复 (brief §3).

    raised = rx**M0 (等权升幂, 未归一化)
    每段 s_k: seg_phi[k] = angle(raised[lo:hi].mean())   # 升幂域, 不 /M0
    seg_phi_unw = np.unwrap(seg_phi)                     # 升幂域 unwrap (段间可能跨 2π)
    phi_raised  = np.interp(arange(N), seg_center, seg_phi_unw)  # 段中心间线性插值
    phi_est = phi_raised / M0                            # 最后 /M0
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    seg_len = N // K
    raised = seg ** M0
    seg_phi = np.empty(K)
    seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k * seg_len, (k + 1) * seg_len
        seg_phi[k] = np.angle(raised[lo:hi].mean())   # 等权 mean-angle (升幂域)
        seg_center[k] = (lo + hi) / 2.0
    seg_phi_unw = np.unwrap(seg_phi)                   # 升幂域 unwrap
    t = np.arange(N)
    phi_raised = np.interp(t, seg_center, seg_phi_unw)
    phi_est = phi_raised / M0                           # 最后 /M0
    return seg * np.exp(-1j * phi_est)


def ber_nda_seg_eval(rx, tx_bits, M0, K=8):
    """NDA-segmented 等权 BER 评估: 逐 N_DFT 块 recovery + resolve. 返回 (n_err, n_bits).

    与 S.ber_nda_turb_eval 同结构 (fft_foe 两阶段 + per-block CPE), 区别仅在 CPE 用
    nda_segmented_eq 而非 common nda_ml_recovery intra='none'.
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_segmented_eq(seg_foe, M0, K=K)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# VV BER 评估 (可调 Nw): 逐块 fft_foe + VV(Nw) + resolve. 返回 (n_err, n_bits).
# 复用 VV.vv_cpr_m16apsk(seg, Nw=X) + VV.ber_vv_turb_eval 结构.
# =============================================================================
def ber_vv_turb_nw(rx, tx_bits, Nw):
    """VV BER (可调 Nw). 逐块 fft_foe + vv_cpr_m16apsk(seg, Nw) + resolve."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _ = VV.vv_cpr_m16apsk(seg_foe, Nw=Nw)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 统计工具
# =============================================================================
def ci_t(data):
    """95% CI 半宽 (t 分布, df=n-1). 返回 (mean, std, ci_halfwidth, ci_low, ci_high)."""
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


def fair_gain_dB_from_ber(snrs_d, ber_test, ber_ref, target=None):
    """等效 SNR gain (γ_d 坐标, test vs ref 都无 pilot overhead): 正 = ref 赢 test.

    在 target BER 处: test 达 ref 所需 γ_d − ref γ_d.
    target=None: 取 ref 最低可达 BER (HD-FEC 不可达时). 返回 (gain, target_used, s_test, s_ref).
    """
    snrs_d = np.asarray(snrs_d, dtype=float)
    ber_test = np.asarray(ber_test, dtype=float)
    ber_ref = np.asarray(ber_ref, dtype=float)
    if target is None:
        target = float(np.min(ber_ref))   # ref 最低 BER (per-point 取 min)
    s_test = snr_at_ber(snrs_d, ber_test, target)
    s_ref = snr_at_ber(snrs_d, ber_ref, target)
    gain = (s_test - s_ref) if (s_test is not None and s_ref is not None) else None
    return gain, target, s_test, s_ref


# =============================================================================
# 实验 1: 上行 + VV/BPS 对照 (核心). 5 seed × 2 场景 × 7 SNR, 5 方法同信道同 seed.
# NDA 用 'none' 模式 (S.ber_nda_turb_eval, 湍流主实验设定, 非 segmented).
# =============================================================================
def run_experiment1():
    cfg = SimulationConfig()
    Ns = P.N_DFT
    scenes = list(P.UPLINK_LEVELS)
    # raw[scene][seed_i] = per_snr list of dict
    raw = {sc: {} for sc in scenes}
    print("\n" + "#" * 30 + " 实验 1: 上行 NDA(none)/VV(Nw=64)/BPS/DA/oracle (5 seed × 2 场景) " + "#" * 30)
    print(f"场景: {scenes}")
    print(f"  α/β: { {k: list(v) for k, v in P.UPLINK_ALPHA_BETA.items()} }")
    print(f"SNR 点 (γ_tot dB): {P.SNR_TURB_DB}")
    for sc in scenes:
        print(f"  {sc} seed0: {[seed0_uplink(i) for i in range(N_SEEDS)]}")
    for turb in scenes:
        for i in range(N_SEEDS):
            s0 = seed0_uplink(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            print(f"{'γd_dB':>7} {'NDA':>11} {'VV':>11} {'BPS':>11} {'DA':>11} {'ORACLE':>11}")
            per_snr = []
            for gamma_db in P.SNR_TURB_DB:
                gamma_lin = 10 ** (gamma_db / 10)
                ne_nda = ne_vv = ne_bps = ne_da = ne_or = 0
                nb_nda = nb_vv = nb_bps = nb_da = nb_or = 0
                for b in range(P.N_BLOCKS):
                    r = generate_shared_realization_apsk(
                        Ns, gamma_lin, turb, cfg.doppler.DOPPLER_HIGH,
                        mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']
                    bits = r['bits']
                    phi = r['phi']
                    tx_sym = r['tx']
                    h_true = r['h']
                    # 幅度处理 (per-block h, 同主实验/VV/BPS ablation): NDA/VV/BPS 用盲 h (公平),
                    # DA 用 pilot h, oracle 用真 h. 三方同信道 (同一 generate_shared_realization).
                    h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
                    rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
                    h_pilot = S.estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
                    rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
                    rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
                    ne, nb = S.ber_nda_turb_eval(rx_blind, bits)   # NDA none 模式 (默认)
                    ne_nda += ne; nb_nda += nb
                    ne, nb = VV.ber_vv_turb_eval(rx_blind, bits)   # VV Nw=64 默认
                    ne_vv += ne; nb_vv += nb
                    ne, nb = BPS.ber_bps_turb_eval(rx_blind, bits)
                    ne_bps += ne; nb_bps += nb
                    ne, nb = S.ber_da_turb(rx_pilot, bits)
                    ne_da += ne; nb_da += nb
                    ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
                    ne_or += ne; nb_or += nb
                b_nda = ne_nda / nb_nda
                b_vv = ne_vv / nb_vv
                b_bps = ne_bps / nb_bps
                b_da = ne_da / nb_da
                b_or = ne_or / nb_or
                print(f"{gamma_db:>7.0f} {b_nda:>11.4e} {b_vv:>11.4e} {b_bps:>11.4e} "
                      f"{b_da:>11.4e} {b_or:>11.4e}")
                per_snr.append({
                    'snr_db': float(gamma_db),
                    'nda_ber': b_nda, 'vv_ber': b_vv, 'bps_ber': b_bps,
                    'da_ber': b_da, 'oracle_ber': b_or,
                })
            raw[turb][i] = per_snr
    return raw


def aggregate_exp1(raw):
    """每场景每 SNR: 5 seed BER 均值 ± 95% CI (NDA/VV/BPS/DA/oracle)."""
    summary = {}
    for sc in P.UPLINK_LEVELS:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        points = []
        for j, snr in enumerate(snrs):
            nda = [per_seed[i][j]['nda_ber'] for i in range(N_SEEDS)]
            vv = [per_seed[i][j]['vv_ber'] for i in range(N_SEEDS)]
            bps = [per_seed[i][j]['bps_ber'] for i in range(N_SEEDS)]
            da = [per_seed[i][j]['da_ber'] for i in range(N_SEEDS)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(N_SEEDS)]
            entry = {'snr_db': float(snr)}
            for key, vals in [('nda', nda), ('vv', vv), ('bps', bps), ('da', da), ('oracle', orc)]:
                m, s, hw, lo, hi = ci_t(vals)
                entry[f'{key}_ber_mean'] = m
                entry[f'{key}_ber_ci95'] = [lo, hi]
                entry[f'{key}_ber_per_seed'] = [float(x) for x in vals]
            points.append(entry)
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def fair_gain_exp1(summary):
    """工作区 (γ_tot≥15dB) per-point fair gain (dB, 正=NDA赢): NDA vs VV / NDA vs BPS / NDA vs DA.

    NDA/VV/BPS 都无 pilot overhead → γ_d 坐标 fair (gain = test达NDA BER所需γ_d − NDA γ_d).
    NDA vs DA 用 γ_tot 坐标 (DA 有 pilot overhead). 用 5 seed 平均曲线算 per-point.
    上行 HD-FEC 物理不可达 → 用工作区 per-point gain 作主判据 (同 run_uplink_experiment).
    """
    out = {}
    pilot_oh = float(P.PILOT_OVERHEAD_DB)
    for sc in P.UPLINK_LEVELS:
        pts = summary[sc]['points']
        snrs = np.array([p['snr_db'] for p in pts])
        b_nda = np.array([p['nda_ber_mean'] for p in pts])
        b_vv = np.array([p['vv_ber_mean'] for p in pts])
        b_bps = np.array([p['bps_ber_mean'] for p in pts])
        b_da = np.array([p['da_ber_mean'] for p in pts])
        # per-point gain (γ_d 坐标): test 达 NDA 该点 BER 所需 γ_d − NDA γ_d (正=NDA赢)
        wr_vv, wr_bps, wr_da = [], [], []
        for i, gd in enumerate(snrs):
            if gd < 15.0:
                continue
            ber_nda_at = b_nda[i]
            s_vv = snr_at_ber(snrs, b_vv, ber_nda_at)
            s_bps = snr_at_ber(snrs, b_bps, ber_nda_at)
            s_da_d = snr_at_ber(snrs, b_da, ber_nda_at)
            wr_vv.append(float(s_vv - gd) if s_vv is not None else None)
            wr_bps.append(float(s_bps - gd) if s_bps is not None else None)
            wr_da.append(float((s_da_d + pilot_oh) - gd) if s_da_d is not None else None)
        def _stat(col):
            valid = [x for x in col if x is not None]
            pp = [None if x is None else float(x) for x in col]
            if len(valid) >= 1:
                m, s, hw, lo, hi = ci_t(valid) if len(valid) > 1 else (float(np.mean(valid)), 0.0, 0.0, float(np.mean(valid)), float(np.mean(valid)))
                return {'mean': m, 'std': s, 'ci95': [lo, hi], 'n': len(valid), 'per_point': pp}
            return {'mean': None, 'std': None, 'ci95': [None, None], 'n': 0, 'per_point': pp}
        out[sc] = {
            'workregion_gamma_db': [float(gd) for gd in snrs if gd >= 15.0],
            'nda_vs_vv_gain_db': _stat(wr_vv),
            'nda_vs_bps_gain_db': _stat(wr_bps),
            'nda_vs_da_gain_db': _stat(wr_da),
        }
    return out


# =============================================================================
# 实验 2: VV Nw 扫描 (下行 AWGN 高线宽, 防虚高). 线宽 [200,500]kHz × Nw [8,16,32,64,128]
# vs NDA-segmented(等权 K=8). SNR=18dB. 三方同信道同 seed (AWGN 无 h, 同 awgn_wiener_channel).
# =============================================================================
def run_experiment2(linewidths_hz, nws, snr_db=18.0, n_blocks=None, seed_base=None):
    """实验 2: AWGN, (8,8)-16APSK, SNR=18dB. 每线宽: NDA-seg + VV(Nw 扫描) BER.

    sigma2_p = 2*pi*lw*T_S 派生 (高线宽对照, 不读 params LASER_LW=10kHz).
    三方共用同一 rx (awgn_wiener_channel, sigma2_p 注入). NDA-seg 等权 K=8.
    """
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed_base is None:
        seed_base = P.SEED_AWGN
    N_sym = n_blocks * P.N_DFT
    M0 = P.M0
    mod = 'm16apsk'
    T_S = P.T_S
    print("\n" + "#" * 30 + f" 实验 2: VV Nw 扫描 (AWGN, SNR={snr_db}dB, 高线宽) " + "#" * 30)
    print(f"N_sym={N_sym}/点, M0={M0}, NDA-segmented K=8 (等权), VV Nw∈{nws}")
    print(f"{'线宽(kHz)':>10} {'NDA-seg':>12}" + "".join(f"{f'VV Nw{nw}':>12}" for nw in nws))
    rows = []
    for lw in linewidths_hz:
        sigma2_p = 2 * np.pi * lw * T_S
        seed = seed_base + int(snr_db * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, _phi_true = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
        # NDA-seg 等权 (AWGN 无 CFO 无 h, 直接逐块 recovery + resolve)
        N = len(rx)
        n_blk = N // P.N_DFT
        L = n_blk * P.N_DFT
        rx_comp_seg = np.zeros(L, dtype=complex)
        for b in range(n_blk):
            seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
            rx_comp_seg[b * P.N_DFT:(b + 1) * P.N_DFT] = nda_segmented_eq(seg, M0, K=8)
        tb = bits[:L * P.BITS_PER_SYM]
        resolved = resolve_m16apsk_blockwise(rx_comp_seg, tb, block_size=P.BLOCK_SIZE_RESOLVE)
        ne_seg = int(np.sum(tb != m16apsk_demod(resolved)))
        b_seg = ne_seg / len(tb)
        # VV Nw 扫描 (AWGN 无 CFO, 逐块直接 vv_cpr_m16apsk(seg, Nw) + resolve)
        b_vv_by_nw = {}
        for nw in nws:
            rx_comp_vv = np.zeros(L, dtype=complex)
            for b in range(n_blk):
                seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
                rc, _ = VV.vv_cpr_m16apsk(seg, Nw=nw)
                rx_comp_vv[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
            resolved = resolve_m16apsk_blockwise(rx_comp_vv, tb, block_size=P.BLOCK_SIZE_RESOLVE)
            ne_vv = int(np.sum(tb != m16apsk_demod(resolved)))
            b_vv_by_nw[nw] = ne_vv / len(tb)
        line = f"{lw/1e3:>10.0f} {b_seg:>12.4e}" + "".join(f"{b_vv_by_nw[nw]:>12.4e}" for nw in nws)
        print(line)
        # 机械分类: VV vs NDA-seg (rel = (vv - seg)/seg)
        cls = {}
        for nw in nws:
            rel = (b_vv_by_nw[nw] - b_seg) / b_seg if b_seg > 0 else None
            cat = ('VV追上' if (rel is not None and abs(rel) < 0.05)
                   else 'VV仍差' if (rel is not None and rel >= 0.10)
                   else '中间' if rel is not None else None)
            cls[nw] = {'ber_vv': float(b_vv_by_nw[nw]), 'rel_vs_seg': rel, 'cat': cat}
        rows.append({
            'linewidth_hz': float(lw),
            'linewidth_khz': float(lw / 1e3),
            'sigma2_p': float(sigma2_p),
            'snr_db': float(snr_db),
            'ber_nda_seg': float(b_seg),
            'vv_by_nw': {int(nw): float(v) for nw, v in b_vv_by_nw.items()},
            'classification': {int(nw): cls[nw] for nw in nws},
            'overall_cat': _overall_cat(rows_cls={int(nw): cls[nw]['cat'] for nw in nws}),
        })
    return rows


# =============================================================================
# 实验 3: VV Nw 扫描 (上行 uplink_strong SNR=20dB). vs NDA-segmented(等权 K=8).
# 三方同信道同 seed (湍流 generate_shared_realization + 同 rx_blind).
# =============================================================================
def run_experiment3(nws, snr_db=20.0, n_blocks=None, seed0=None, lw=10e3):
    """实验 3: uplink_strong, (8,8)-16APSK, SNR=20dB, lw=10kHz. NDA-seg(K=8) + VV Nw 扫描.

    NDA-seg 湍流两阶段 (fft_foe + seg CPE), VV 湍流两阶段 (fft_foe + VV CPE).
    """
    if n_blocks is None:
        n_blocks = P.N_BLOCKS
    if seed0 is None:
        seed0 = seed0_uplink(0)   # 与上行主实验 seed 一致
    cfg = SimulationConfig()
    Ns = P.N_DFT
    M0 = P.M0
    turb = 'uplink_strong'
    gamma_lin = 10 ** (snr_db / 10)
    print("\n" + "#" * 30 + f" 实验 3: VV Nw 扫描 (上行 {turb}, SNR={snr_db}dB, lw={lw/1e3:.0f}kHz) " + "#" * 30)
    print(f"N_sym={n_blocks*Ns}, M0={M0}, NDA-segmented K=8 (等权), VV Nw∈{nws}, seed0={seed0}")
    print(f"{'NDA-seg':>12}" + "".join(f"{f'VV Nw{nw}':>12}" for nw in nws))
    ne_seg = 0
    nb_seg = 0
    ne_vv = {nw: 0 for nw in nws}
    nb_vv = {nw: 0 for nw in nws}
    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            Ns, gamma_lin, turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk',
            seed=seed0 + b, lw=lw)
        rx_raw = r['rx_raw']
        bits = r['bits']
        h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
        rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
        # NDA-seg (两阶段 fft_foe + seg CPE)
        ne, nb = ber_nda_seg_eval(rx_blind, bits, M0, K=8)
        ne_seg += ne; nb_seg += nb
        # VV Nw 扫描 (两阶段 fft_foe + VV CPE)
        for nw in nws:
            ne, nb = ber_vv_turb_nw(rx_blind, bits, Nw=nw)
            ne_vv[nw] += ne; nb_vv[nw] += nb
    b_seg = ne_seg / nb_seg
    b_vv_by_nw = {nw: ne_vv[nw] / nb_vv[nw] for nw in nws}
    print(f"{b_seg:>12.4e}" + "".join(f"{b_vv_by_nw[nw]:>12.4e}" for nw in nws))
    cls = {}
    for nw in nws:
        rel = (b_vv_by_nw[nw] - b_seg) / b_seg if b_seg > 0 else None
        cat = ('VV追上' if (rel is not None and abs(rel) < 0.05)
               else 'VV仍差' if (rel is not None and rel >= 0.10)
               else '中间' if rel is not None else None)
        cls[nw] = {'ber_vv': float(b_vv_by_nw[nw]), 'rel_vs_seg': rel, 'cat': cat}
    return {
        'turbulence': turb,
        'alpha_beta': list(P.UPLINK_ALPHA_BETA[turb]),
        'snr_db': float(snr_db),
        'linewidth_hz': float(lw),
        'ber_nda_seg': float(b_seg),
        'vv_by_nw': {int(nw): float(v) for nw, v in b_vv_by_nw.items()},
        'classification': {int(nw): cls[nw] for nw in nws},
        'overall_cat': _overall_cat({int(nw): cls[nw]['cat'] for nw in nws}),
    }


def _overall_cat(rows_cls):
    """机械分类总判: 任一 Nw 下 VV追上 → 'VV追上'; 否则所有 Nw 都 VV仍差 → 'VV仍差'; 其余 '中间'."""
    cats = [c for c in rows_cls.values() if c is not None]
    if any(c == 'VV追上' for c in cats):
        return 'VV追上'
    if cats and all(c == 'VV仍差' for c in cats):
        return 'VV仍差'
    return '中间'


# =============================================================================
# JSON 落盘
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


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    print("=" * 100)
    print("上行 NDA-ML vs VV/BPS 对照 + VV Nw 扫描 (查 segmented 拉开 VV 真机制/参数)")
    print(f"M0={P.M0}, N_DFT={P.N_DFT}, N_BLOCKS={P.N_BLOCKS}, HDFEC={P.HDFEC}")
    print(f"上行场景: {P.UPLINK_LEVELS}, α/β: {{k: list(v) for k,v in P.UPLINK_ALPHA_BETA.items()}}")
    print(f"纪律: 只改本 explore 目录; 复用 S/VV/BPS; 三方同信道同 seed; 只跑数字+机械分类")
    print("=" * 100)

    # --- 实验 1: 上行 + VV/BPS 对照 (核心) ---
    exp1_raw = run_experiment1()
    exp1_summary = aggregate_exp1(exp1_raw)
    exp1_gain = fair_gain_exp1(exp1_summary)

    # --- 实验 2: VV Nw 扫描 (AWGN 高线宽) ---
    linewidths2 = [200e3, 500e3]
    nws = [8, 16, 32, 64, 128]
    exp2 = run_experiment2(linewidths2, nws, snr_db=18.0)

    # --- 实验 3: VV Nw 扫描 (上行 uplink_strong) ---
    exp3 = run_experiment3(nws, snr_db=20.0)

    elapsed = time.time() - t0

    # --- 落盘 JSON ---
    out = {
        'meta': {
            'task': '上行 NDA vs VV/BPS 对照 + VV Nw 扫描 (segmented 拉开 VV 真机制/参数)',
            'purpose': ('回答两问: (1) 上行 NDA(none) 能否拉开 VV/BPS; '
                        '(2) VV 调 Nw 能否追上 segmented (高线宽).'),
            'experiments': {
                'exp1': '上行 uplink_moderate/strong × NDA(none)/VV(Nw64)/BPS/DA/oracle, 5 seed, SNR_TURB_DB',
                'exp2': 'AWGN (8,8)-16APSK SNR=18dB, 线宽[200,500]kHz, VV Nw扫 vs NDA-seg(K=8)',
                'exp3': '上行 uplink_strong SNR=20dB, lw=10kHz, VV Nw扫 vs NDA-seg(K=8)',
            },
            'modulation': '(8,8)-16APSK, M0=8',
            'nda_modes': {
                'exp1': "湍流 intra='none' (主实验设定, 非 segmented) — S.ber_nda_turb_eval",
                'exp2_exp3': "NDA-segmented 等权 K=8 (高线宽对照, unwrap 在升幂域最后 /M0)",
            },
            'vv': 'VV.vv_cpr_m16apsk(seg, Nw=X); Nw 扫描改 X. 默认 64',
            'bps': 'BPS.ber_bps_turb_eval (B=64, Nw=101, M0=8 unwrap)',
            'fairness': ('三方同信道同 seed: 湍流 NDA/VV/BPS 用同一 rx_blind (同 h_blind 估计 '
                         '+ mmse_equalize + amp_limit), DA 用 pilot h, oracle 用真 h. '
                         'AWGN NDA-seg/VV 用同一 awgn_wiener_channel rx.'),
            'seed_strategy': {
                'exp1_exp3': 'seed0_uplink(i) = SEED_TURB0 + 500000 + i*N_BLOCKS (同 run_uplink_experiment)',
                'exp2': 'seed = SEED_AWGN + int(18*1000) (单 seed, 同主实验 AWGN)',
            },
            'n_seeds_exp1': N_SEEDS,
            'ci_method': f't-distribution 95% CI, df=n-1 (5 seed→df=4, t={T05_4:.4f})',
            'classification': {
                'fair_gain': ('拉开: gain>=0.3dB 且 CI 不跨零; 持平: |gain|<0.1dB 或 CI 跨零; '
                              '中间: 0.1<=gain<0.3dB'),
                'vv_nw_scan': ('VV追上: 某 Nw 下 VV BER 跟 NDA-seg 差<5%; '
                               'VV仍差: 所有 Nw 下 VV BER 比 NDA-seg 高>=10%'),
            },
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_BLOCKS': P.N_BLOCKS,
            'LASER_LW_Hz': float(P.LASER_LW),
            'T_S': float(P.T_S),
            'HDFEC': P.HDFEC,
            'PILOT_OVERHEAD_DB': float(P.PILOT_OVERHEAD_DB),
            'UPLINK_ALPHA_BETA': {k: list(v) for k, v in P.UPLINK_ALPHA_BETA.items()},
            'SNR_TURB_DB': P.SNR_TURB_DB,
            'SEED_TURB0': P.SEED_TURB0,
            'SEED_AWGN': P.SEED_AWGN,
            'UPLINK_SEED_OFFSET': UPLINK_SEED_OFFSET,
            'common_or_simulator_or_params_modified': False,
            'reused_functions': ['S.ber_nda_turb_eval', 'S.ber_da_turb', 'S.ber_oracle_turb',
                                 'S.estimate_h_blind_perblock', 'S.estimate_h_pilot_perblock',
                                 'S.fft_foe_m0_omega', 'S.awgn_wiener_channel',
                                 'VV.vv_cpr_m16apsk', 'VV.ber_vv_turb_eval',
                                 'BPS.ber_bps_turb_eval', 'generate_shared_realization_apsk',
                                 'mmse_equalize', 'amp_limit', 'resolve_m16apsk_blockwise'],
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'experiment1_uplink_vs_vv_bps': {
            'summary_5seed': to_jsonable(exp1_summary),
            'fair_gain_workregion': to_jsonable(exp1_gain),
            'raw_per_seed': to_jsonable(exp1_raw),
        },
        'experiment2_vv_nw_awgn_high_lw': to_jsonable(exp2),
        'experiment3_vv_nw_uplink': to_jsonable(exp3),
    }
    out_json = os.path.join(_HERE, '_uplink_vv_check.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("实验 1 工作区 fair gain (5 seed, γ_tot≥15dB, 正=NDA赢):")
    print(f"{'场景':>18} {'NDA vs VV':>16} {'NDA vs BPS':>16} {'NDA vs DA':>16}")
    for sc in P.UPLINK_LEVELS:
        g = exp1_gain[sc]
        def _fmt(d):
            m = d['mean']
            ci = d['ci95']
            return f"{m:>+7.3f}dB[{ci[0]:+5.2f},{ci[1]:+5.2f}]" if m is not None else f"{'n/a':>16}"
        print(f"{sc:>18} {_fmt(g['nda_vs_vv_gain_db']):>16} "
              f"{_fmt(g['nda_vs_bps_gain_db']):>16} {_fmt(g['nda_vs_da_gain_db']):>16}")
    print("\n实验 2 VV Nw 扫描 (AWGN 高线宽) overall_cat:")
    for r in exp2:
        print(f"  {r['linewidth_khz']:.0f}kHz: NDA-seg={r['ber_nda_seg']:.4e}  "
              f"overall={r['overall_cat']}  "
              f"(VV Nw8={r['vv_by_nw'][8]:.3e}, Nw64={r['vv_by_nw'][64]:.3e})")
    print(f"\n实验 3 VV Nw 扫描 (上行 uplink_strong 20dB) overall_cat:")
    print(f"  NDA-seg={exp3['ber_nda_seg']:.4e}  overall={exp3['overall_cat']}  "
          f"(VV Nw8={exp3['vv_by_nw'][8]:.3e}, Nw64={exp3['vv_by_nw'][64]:.3e})")
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
