"""B11 NDA-ML vs DA ML BER 层 oracle 上界 — 星地湍流信道 (FR-21 重做).

重做背景: 上一轮 CRB 层 FR-21 被用户判定 **物理量错配** — B11 +2dB 是 BER @ 7% HD-FEC
threshold (行 181/191), 不是相位 CRB; DA ML 劣势来自 decision-aided 实现缺陷 (高阶星座
判决错误传播), 非信息论下界. 本轮改用 **BER 层 oracle 上界** 重做 FR-21.

信号模型 (B11 行 33, 迁星地湍流):
  r(k) = s(k) · exp(jθ(k)) · sqrt(h(k)) + n(k),  s(k) ∈ (8,8)-16APSK
  θ(k) = φ_CPE + 2πΔf·k·T_s + θ_laser(k) (Wiener) + π·f_dot·(kT_s)² (Doppler ramp)
  h(k) = Gamma-Gamma 块衰落 (BLOCK=100 sym 块内恒定)

三方案 (每点 N_sym ≥ 1e5):
  1. NDA-ML (B11 锚): 升 M₀=8 次幂盲去调制 → 单正弦 ML → 估 CPE+FOE → 补偿解调 → BER
     (M₀=8 相位模糊用 resolve_m16apsk 8 旋转 brute-force 消除, 非 oracle)
  2. DA ML (B11 baseline): pilot (spacing=32) 估 CPE+FOE → 补偿解调 → BER
  3. genie-aided oracle (信息论上界参考): 用真实 θ(k) 补偿 → 解调 → BER
     (NDA/DA 不可能超过 oracle)

==============================================================================
重要方法学决策 (TL-23 验证后发现, 必须显式记录):
==============================================================================
A. **逐块恢复 (Nblock=256=B11 DFT_SIZE)**:
   全帧 (N=1e5 一气恢复) 在本信道下 *失效* — Wiener PN 累积漂移 (LW=10kHz, 累积 ~0.9 rad
   rms over 1e5 sym) 使 NDA/DA 的线性 (φ,Δf) 模型无法跟踪. B11 原文即按 DFT_SIZE=256 块处理
   (行 155 N=256). 本轮严格逐块恢复, 块内 Wiener 漂移 ~0.08 rad (可被线性模型近似).

B. **幅度处理**: (8,8)-16APSK 解调用半径判环, 对 sqrt(h) 幅度衰落敏感. DA/NDA 载波恢复器
   只估相位+频偏, 不估幅度. 故幅度必须独立处理 (正交模块, AGC/均衡, DVB-S2 标准做法).
   本轮跑 **两套** 幅度方案以增强结论稳健性:
     (a) h_med MMSE 均衡 + amp_limit(3.0) — 真实公平 (equalize_hmed, 非 oracle)
     (b) oracle 幅度归一 (rx/sqrt(h)) — 隔离相位恢复能力 (三方案同公平, 但幅度用了 oracle)
   若两套都显示 NDA 劣于 DA, 结论稳健.

C. **HD-FEC 阈值 (3.8e-3) 不可达**:
   因 GG 块衰落 + h_med 均衡残差 (块内 h 方差), 三方案 BER 在 20dB 弱湍流仍只到 ~4e-2,
   永远达不到 3.8e-3. 故 *不能* 按 TL-20 原设想在 HD-FEC 阈值处算 gain_at_hdfec.
   改用: (i) 多 SNR 工作点 NDA vs DA BER 趋势比较; (ii) 在可达 BER 水平 (取各湍流实测
   可达下限 BER_achievable) 处做 NDA/DA 等效 SNR 差 (linear interp). 显式标注非 HD-FEC.

TL-20 物理预期 (BER 层重写, 跑前对照):
  weak     : 1-3 dB (近 B11 +2dB, 湍流弱不破坏 NDA-ML 优势)
  moderate : 0.5-2 dB (DA pilot 受 fade 决策错误传播放大)
  strong   : AMBIGUOUS -1~1 dB (deep fade 致 NDA 升幂噪声放大 vs DA pilot 崩溃)

偏离即查:
  - weak gain < 0.5 → 可疑 (B11 +2dB 应大致保持)
  - 任一湍流 gain > 4 → 可疑
  - strong gain 强负 (< -2) → B11 星地迁移失效

运行: cd projects/simulation && python explore/b11-nda-ml-sto-cpe/_ber_oracle_upperbound.py
依赖: from common import generate_shared_realization_apsk, da_ml_recovery, nda_ml_recovery,
                       m16apsk_demod, ber_count_m16apsk, resolve_m16apsk, mmse_equalize, amp_limit
"""
import os
import sys
import time
import json

import numpy as np

# 从 simulation 根导入 common (TL-13 共用同一信道)
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common import (
    generate_shared_realization_apsk,
    m16apsk_demod, ber_count_m16apsk, resolve_m16apsk,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
)
from params import SimulationConfig


# =============================================================================
# 单点 BER 评估 (逐块, N_sym = Nblock × Nblocks ≥ 1e5)
# =============================================================================

def ber_point(turb_name, snr_db, cfg, n_blocks, n_per_block, pilot_spacing,
              amp_mode='h_med', seed0=2000):
    """单 (turb, SNR) 点三方案 BER.

    amp_mode:
      'h_med'   — MMSE 均衡用块中位 h_med + amp_limit(3.0) (真实公平, 非 oracle)
      'oracle'  — rx / sqrt(h) (oracle 幅度归一, 隔离相位, 三方案同公平)
    返回 (ber_nda, ber_da, ber_oracle).
    """
    M0 = cfg.b11.M0_POWER
    Ns = n_per_block
    n_err_nda = 0   # 累计错误比特 (避免存全 bits, 省内存)
    n_err_da = 0
    n_err_oracle = 0
    n_bits_total = 0

    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            Ns, 10 ** (snr_db / 10), turb_name, cfg.doppler.DOPPLER_HIGH,
            mod='m16apsk', seed=seed0 + b)
        rx_raw = r['rx_raw']
        bits = r['bits']
        phi = r['phi']
        tx = r['tx']
        h = r['h']
        h_med = r['h_med']
        gamma = r['gamma_bar']

        # 幅度处理 (正交模块, 三方案统一)
        if amp_mode == 'h_med':
            rx = amp_limit(mmse_equalize(rx_raw, h_med, gamma), 3.0)
        elif amp_mode == 'oracle':
            rx = rx_raw / np.sqrt(h)
        else:
            raise ValueError(f"Unknown amp_mode: {amp_mode}")

        # --- genie-aided oracle (真实 θ 补偿) ---
        rx_oracle = rx * np.exp(-1j * phi)
        n_err_oracle += int(np.sum(bits != m16apsk_demod(rx_oracle)))

        # --- NDA-ML (升 M₀=8, resolve 消 M₀-fold 模糊) ---
        try:
            rxn, _, _, _ = nda_ml_recovery(rx, M0, mod='m16apsk')
            ber_nda = resolve_m16apsk(rxn, bits)
            # resolve 返回 BER (float), 还原为错误比特数
            n_err_nda += int(round(ber_nda * len(bits)))
        except Exception:
            n_err_nda += len(bits)  # 估计器失效 → 全错 (悲观)

        # --- DA ML (pilot spacing=32, 线性 (φ,Δf) 模型) ---
        pidx = np.arange(0, Ns, pilot_spacing)
        psym = tx[pidx]
        try:
            rxd, _, _ = da_ml_recovery(rx, pidx, psym, mod='m16apsk')
            n_err_da += int(np.sum(bits != m16apsk_demod(rxd)))
        except Exception:
            n_err_da += len(bits)

        n_bits_total += len(bits)

    ber_nda = n_err_nda / n_bits_total
    ber_da = n_err_da / n_bits_total
    ber_oracle = n_err_oracle / n_bits_total
    return ber_nda, ber_da, ber_oracle


def snr_at_ber(snr_list, ber_list, ber_target):
    """线性插值 (SNR 轴) 找 BER 曲线达 ber_target 的 SNR.
    返回 None 若 ber_target 不在 [min,max] 范围内 (不可达).
    SNR 升 BER 降 (单调假设), 找相邻 (ber_hi@snr_lo, ber_lo@snr_hi) 跨越 target.
    """
    snr_list = np.asarray(snr_list, dtype=float)
    ber_list = np.asarray(ber_list, dtype=float)
    # 按 SNR 升序
    order = np.argsort(snr_list)
    snr_list = snr_list[order]
    ber_list = ber_list[order]
    # 找相邻跨越 target 的对
    for i in range(len(snr_list) - 1):
        b_hi = ber_list[i]      # 低 SNR → 高 BER
        b_lo = ber_list[i + 1]  # 高 SNR → 低 BER
        if b_hi >= ber_target >= b_lo and b_hi > b_lo:
            # log-linear 插值 (BER 跨数量级, log 轴更准)
            t = (np.log(b_hi) - np.log(ber_target)) / (np.log(b_hi) - np.log(b_lo))
            return float(snr_list[i] + t * (snr_list[i + 1] - snr_list[i]))
    return None  # 不可达


def equiv_snr_gap(snr_list, ber_ref, ber_test):
    """等效 SNR gap: ber_test 曲线达 ber_ref 曲线在 ref_snr 处的 BER 所需的额外 SNR.
    返回 (ref_snr, test_snr, gap_db) 三组 (仅对可达的 SNR 点).
    gap_db > 0 = test (NDA) 需更高 SNR → test 劣 (DA 赢).
    """
    out = []
    snr_list = np.asarray(snr_list, dtype=float)
    ber_ref = np.asarray(ber_ref, dtype=float)
    ber_test = np.asarray(ber_test, dtype=float)
    order = np.argsort(snr_list)
    snr_list, ber_ref, ber_test = snr_list[order], ber_ref[order], ber_test[order]
    for i, sref in enumerate(snr_list):
        bref = ber_ref[i]
        # 在 test 曲线找达 bref 的 SNR
        stest = snr_at_ber(snr_list, ber_test, bref)
        if stest is not None:
            out.append((float(sref), float(stest), float(stest - sref)))
    return out


def main():
    t0 = time.time()
    cfg = SimulationConfig()
    M0 = cfg.b11.M0_POWER

    # 实验配置 (守 FR-21: N_sym ≥ 1e5; 守时间预算 < 900s)
    N_PER_BLOCK = cfg.b11.DFT_SIZE          # 256 (B11 行 155, 决策 A)
    N_BLOCKS = 400                          # 400×256 = 102400 ≥ 1e5 ✓
    PILOT_SPACING = cfg.b7.PSA_PILOT_SPACING  # 32 (DVB-S2, B7 默认)
    SNR_POINTS = [0.0, 4.0, 8.0, 12.0, 16.0, 20.0]
    TURB_LEVELS = ['weak', 'moderate', 'strong']
    AMP_MODES = ['h_med', 'oracle']         # 决策 B: 两套幅度方案
    HDFEC_BER = 3.8e-3                      # 7% HD-FEC (B11 行 181/191)

    print(f"B11 NDA-ML vs DA ML BER 层 oracle 上界 (逐块 Nblock={N_PER_BLOCK}, "
          f"N_sym={N_PER_BLOCK*N_BLOCKS}/点)")
    print(f"M0={M0}, pilot_spacing={PILOT_SPACING}, amp_modes={AMP_MODES}")
    print("=" * 100)

    results = {
        'meta': {
            'task': 'B11 NDA-ML STO+CPE BER-layer oracle upper bound vs DA ML (star-ground turb)',
            'source': 'B11 IEEE PTL 2025 doi:10.1109_LPT.2024.3523478',
            'redo_reason': (
                '上一轮 CRB 层 FR-21 物理量错配: B11 +2dB 是 BER @ HD-FEC 不是相位 CRB; '
                'DA ML 劣势是 decision-aided 实现缺陷非信息论下界. 本轮 BER 层重做.'
            ),
            'metric': 'BER @ (8,8)-16APSK, M0-fold ambiguity resolved by resolve_m16apsk (8 rotations)',
            'methodology_decisions': {
                'A_block_recovery': (
                    f'逐块恢复 Nblock={N_PER_BLOCK}=B11 DFT_SIZE. 全帧恢复因 Wiener PN 累积漂移 '
                    f'(LW={cfg.system.LASER_LW/1e3:.0f}kHz, ~0.9rad rms over 1e5 sym) 失效. '
                    f'B11 原文即按 DFT_SIZE=256 块处理 (行 155).'
                ),
                'B_amplitude': (
                    '(8,8)-16APSK 解调对 sqrt(h) 幅度敏感; DA/NDA 只估相位. 跑两套: '
                    'h_med=h_med MMSE+amp_limit(3.0) (真实公平非oracle); '
                    'oracle=rx/sqrt(h) (隔离相位,三方案同公平).'
                ),
                'C_hdfec_unreachable': (
                    f'GG 块衰落+h_med 残差致 BER floor, 三方案 20dB 弱湍流仍 ~4e-2, '
                    f'达不到 {HDFEC_BER} HD-FEC 阈值. 改用多工作点 BER 趋势 + 可达 BER 水平等效 SNR 差.'
                ),
            },
            'N_per_point': N_PER_BLOCK * N_BLOCKS,
            'N_blocks': N_BLOCKS,
            'N_per_block': N_PER_BLOCK,
            'M0': M0,
            'pilot_spacing': PILOT_SPACING,
            'snr_points_dB': SNR_POINTS,
            'turb_levels': TURB_LEVELS,
            'amp_modes': AMP_MODES,
            'hdfec_ber': HDFEC_BER,
            'verdict_thresholds': {
                'go_mve': '>=0.5 dB (NDA-ML 优于 DA ML)',
                'conditional': '0.3-0.5 dB (薄增益)',
                'kill': '<0.3 dB (或 NDA-ML 劣于 DA ML)',
            },
        },
        'expected_TL20': {
            'weak': '1-3 dB (近 B11 +2dB, NDA 全帧积分优势)',
            'moderate': '0.5-2 dB (DA pilot 受 fade 决策错误传播放大)',
            'strong': 'AMBIGUOUS -1~1 dB (deep fade + 升幂噪声放大)',
            'deviation_rules': [
                'weak gain < 0.5 → 可疑',
                '任一湍流 gain > 4 → 可疑',
                'strong gain < -2 → B11 星地迁移失效',
            ],
        },
        'turbulence': {},   # amp_mode -> turb -> [per-snr]
        'gain_analysis': {},  # amp_mode -> turb -> equiv gap stats
    }

    for amp_mode in AMP_MODES:
        print(f"\n{'='*30} amp_mode = {amp_mode} {'='*30}")
        results['turbulence'][amp_mode] = {}
        results['gain_analysis'][amp_mode] = {}
        for turb in TURB_LEVELS:
            print(f"\n--- {turb} ---")
            print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'ORACLE_BER':>12} "
                  f"{'NDA/DA':>9} {'NDA/Oracle':>11}")
            per_snr = []
            for snr_db in SNR_POINTS:
                ber_nda, ber_da, ber_oracle = ber_point(
                    turb, snr_db, cfg, N_BLOCKS, N_PER_BLOCK,
                    PILOT_SPACING, amp_mode=amp_mode, seed0=2000)
                ratio_nda_da = ber_nda / ber_da if ber_da > 0 else float('inf')
                ratio_nda_oracle = ber_nda / ber_oracle if ber_oracle > 0 else float('inf')
                print(f"{snr_db:>7.0f} {ber_nda:>12.4e} {ber_da:>12.4e} {ber_oracle:>12.4e} "
                      f"{ratio_nda_da:>9.3f} {ratio_nda_oracle:>11.3f}")
                per_snr.append({
                    'snr_db': snr_db,
                    'nda_ml_ber': ber_nda,
                    'da_ml_ber': ber_da,
                    'oracle_ber': ber_oracle,
                    'ratio_nda_over_da': ratio_nda_da,
                    'ratio_nda_over_oracle': ratio_nda_oracle,
                })
            results['turbulence'][amp_mode][turb] = per_snr

            # 等效 SNR gap 分析 (NDA vs DA, NDA vs oracle)
            snrs = [p['snr_db'] for p in per_snr]
            ber_nda_arr = [p['nda_ml_ber'] for p in per_snr]
            ber_da_arr = [p['da_ml_ber'] for p in per_snr]
            ber_oracle_arr = [p['oracle_ber'] for p in per_snr]

            # NDA 达 DA 同 BER 所需额外 SNR (gap>0 = NDA 劣)
            gap_nda_vs_da = equiv_snr_gap(snrs, ber_da_arr, ber_nda_arr)
            # NDA 达 oracle 同 BER 所需额外 SNR
            gap_nda_vs_oracle = equiv_snr_gap(snrs, ber_oracle_arr, ber_nda_arr)

            # gain_at_hdfec (原 TL-20 设想): 尝试插值, 大概率 None (不可达)
            snr_nda_hdfec = snr_at_ber(snrs, ber_nda_arr, HDFEC_BER)
            snr_da_hdfec = snr_at_ber(snrs, ber_da_arr, HDFEC_BER)
            gain_hdfec = (snr_da_hdfec - snr_nda_hdfec) \
                if (snr_nda_hdfec is not None and snr_da_hdfec is not None) else None
            # gain_db > 0 = NDA 赢 (DA 需更高 SNR); 注意符号: snr_da - snr_nda

            # 可达 BER 水平的等效 SNR 差 (取 NDA 最低可达 BER 作为 target)
            min_nda_ber = min(ber_nda_arr)
            snr_nda_at_min = snr_at_ber(snrs, ber_nda_arr, min_nda_ber)
            snr_da_at_nda_min = snr_at_ber(snrs, ber_da_arr, min_nda_ber)
            equiv_gain_at_achievable = (
                snr_da_at_nda_min - snr_nda_at_min
                if (snr_nda_at_min is not None and snr_da_at_nda_min is not None) else None)

            results['gain_analysis'][amp_mode][turb] = {
                'gap_nda_vs_da': gap_nda_vs_da,           # list of (snr_da, snr_nda_needed, gap)
                'gap_nda_vs_da_mean_db': (
                    float(np.mean([g[2] for g in gap_nda_vs_da])) if gap_nda_vs_da else None),
                'gap_nda_vs_da_at_minber_db': (
                    gap_nda_vs_da[-1][2] if gap_nda_vs_da else None),
                'gap_nda_vs_oracle_mean_db': (
                    float(np.mean([g[2] for g in gap_nda_vs_oracle]))
                    if gap_nda_vs_oracle else None),
                'gain_at_hdfec_db': gain_hdfec,           # None if unreachable
                'hdfec_reachable': gain_hdfec is not None,
                'equiv_gain_at_achievable_db': equiv_gain_at_achievable,
                'min_nda_ber': min_nda_ber,
                'note': (
                    'gap_nda_vs_da > 0 = NDA 劣 (NDA 需更高 SNR 达 DA 同 BER). '
                    'gain_at_hdfec 符号相反: >0 = NDA 赢.')
            }
            m = results['gain_analysis'][amp_mode][turb]
            print(f"  → NDA-vs-DA 等效 SNR gap 均值: "
                  f"{m['gap_nda_vs_da_mean_db']:+.2f} dB "
                  f"(正=NDA劣), HD-FEC gap: "
                  f"{('%.2f' % gain_hdfec) if gain_hdfec is not None else 'N/A(不可达)'}")

    # =========================================================================
    # 判定 (主用 h_med 真实方案, oracle 幅度方案作稳健性交叉验证)
    # =========================================================================
    primary = 'h_med'
    g_primary = results['gain_analysis'][primary]
    # 主判据: 三湍流 NDA-vs-DA 等效 SNR gap (正=NDA劣). 取最大湍流 gap (最严苛 NDA 劣势).
    # 转 "gain" 语义: gain = -gap (正=NDA 赢)
    gains = {}
    for turb in TURB_LEVELS:
        gap_mean = g_primary[turb]['gap_nda_vs_da_mean_db']
        # gain_at_minBER: 取最高 SNR 处的 gap (NDA 最接近 DA 的工作点) 的负值
        gap_minber = g_primary[turb]['gap_nda_vs_da_at_minber_db']
        # 用 minBER 处的 gap 作主判据 (高 SNR 工作点, 接近 B11 论文 15-20dB 区)
        gains[turb] = -gap_minber if gap_minber is not None else None

    # Go/Kill: 取三湍流最小 gain (保守)
    valid_gains = [g for g in gains.values() if g is not None]
    min_gain = min(valid_gains) if valid_gains else None
    if min_gain is None:
        overall = 'INCONCLUSIVE'
    elif min_gain >= 0.5:
        overall = 'GO_MVE'
    elif min_gain >= 0.3:
        overall = 'CONDITIONAL'
    elif min_gain >= 0:
        overall = 'THIN_KILL'
    else:
        overall = 'KILL'   # NDA 劣于 DA

    results['overall_verdict'] = {
        'verdict': overall,
        'basis': f'主判据: amp_mode={primary}, 三湍流最小 gain (保守), '
                 f'gain = -(NDA-vs-DA 等效SNR gap @ 最高SNR工作点)',
        'gains_dB': gains,   # 正 = NDA 赢
        'min_gain_dB': min_gain,
        'note': ('gain > 0 = NDA-ML 优于 DA ML. 主判据取最高 SNR 工作点的等效 SNR gap '
                 '(接近 B11 论文 15-20dB 区, 避开低 SNR 估计器失效区).'),
    }

    # =========================================================================
    # TL-20 偏离检查
    # =========================================================================
    expected = {'weak': (0.5, 3.0), 'moderate': (0.5, 2.0), 'strong': (-1.0, 1.0)}
    dev_check = []
    for turb in TURB_LEVELS:
        g = gains[turb]
        lo, hi = expected[turb]
        if g is None:
            dev_check.append(f"{turb}: gain=N/A (估计器全失效或不可达) — INCONCLUSIVE")
            continue
        if g < lo - 0.3:
            reason = ('强湍迁移失效' if (turb == 'strong' and g < -2)
                      else 'NDA 劣于预期, 与 B11 +2dB 论文值不符 (但符合 CRB 层 M0² 升幂惩罚物理)')
            dev_check.append(
                f"{turb}: gain={g:+.2f}dB < TL-20 下限 {lo:+.1f}dB → {reason} → DEVIATION")
        elif g > hi + 0.5:
            dev_check.append(f"{turb}: gain={g:+.2f}dB > TL-20 上限 {hi:+.1f}dB → SUSPICIOUS → DEVIATION")
        else:
            dev_check.append(f"{turb}: gain={g:+.2f}dB ∈ TL-20 [{lo:+.1f},{hi:+.1f}] → PASS")
    results['tl20_deviation_check'] = dev_check

    # 稳健性: oracle 幅度方案是否一致
    robust = {}
    for turb in TURB_LEVELS:
        g_hmed = gains[turb]
        go = results['gain_analysis']['oracle'][turb]['gap_nda_vs_da_at_minber_db']
        g_oracle = -go if go is not None else None
        robust[turb] = {
            'gain_h_med_db': g_hmed,
            'gain_oracle_amp_db': g_oracle,
            'consistent': (
                bool((g_hmed is not None and g_oracle is not None and
                 (g_hmed > 0) == (g_oracle > 0)))
                if (g_hmed is not None and g_oracle is not None) else None),
        }
    results['robustness_crosscheck'] = robust

    elapsed = time.time() - t0
    results['meta']['elapsed_sec'] = float(elapsed)

    print("\n" + "=" * 100)
    print("TL-20 物理预期偏离检查 (主判据 h_med):")
    for line in dev_check:
        print(f"  {line}")
    print(f"\n稳健性交叉验证 (oracle 幅度方案 gain 符号是否一致):")
    for turb, r in robust.items():
        print(f"  {turb}: h_med={r['gain_h_med_db']}, oracle_amp={r['gain_oracle_amp_db']}, "
              f"consistent={r['consistent']}")
    print(f"\n主判定 (保守, 三湍流最小 gain): {overall} (min gain = "
          f"{min_gain:+.2f} dB)" if min_gain is not None else f"\n主判定: {overall}")
    print(f"耗时: {elapsed:.1f}s")

    # 写 JSON
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(out_dir, '_ber_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n结果已写: {out_json}")


if __name__ == '__main__':
    main()
