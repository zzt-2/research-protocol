#!/usr/bin/env python3
"""DPLL ζ（阻尼系数）× ω_n 联合扫参实验

验证 ζ=√2/2 是否在所有湍流条件下近最优，还是存在更优阻尼系数。
这是 R002 方向 1 "P_frame→ω_n 解析设计公式" 的前置实验：
  - 如果 ζ 有显著效应 → 方向 1 升级为二维 (ζ, ω_n) 设计公式
  - 如果 ζ 无显著效应 → 方向 1 维持一维 (ω_n) 设计公式，独立成立

TL-25 checklist:
  1. 共享信道: generate_shared_realization ✅
  2. 重生信道: 物理参数不变（仅调 DPLL 参数）✅
  3. 从 common.py 导入: 全部导入 ✅
  4. 基线已优化: ζ=√2/2 基线来自 dpll_omega_sweep ✅
  5. 先写理论预期: 见下方 ✅
  6. 输出含元数据: save_results ✅

理论预期（TL-20）:

  1. 噪声带宽与 ζ 的关系:
     B_L = ω_n * (1 + 4ζ²) / (8ζ)
     ζ=0.5  → B_L = 0.500 * ω_n  (最窄)
     ζ=0.707 → B_L = 0.530 * ω_n  (当前)
     ζ=1.0  → B_L = 0.625 * ω_n  (最宽)
     噪声带宽变化 ±12%，效应温和。

  2. 瞬态响应:
     ζ < √2/2: 欠阻尼，跟踪快但有振铃
     ζ = √2/2: Butterworth（最平坦）
     ζ > √2/2: 过阻尼，跟踪慢但平滑

  3. 预测（强湍流 15dB, ω_n=20MHz）:
     - 弱湍流: ζ 无显著效应（信号质量好，瞬态不重要）
     - 中等湍流: ζ 可能略有影响，但 <1.5x BER 变化
     - 强湍流: ζ 可能有 1.5-3x BER 变化
       - 如果高 ζ 更好: 说明过阻尼有助于从深衰落恢复
       - 如果低 ζ 更好: 说明快速跟踪更重要
     - 如果 ζ 效应 <1.5x → ζ 不构成独立设计维度

  4. 量化锚点:
     - BER 变化 >3x → ζ 是重要设计参数
     - BER 变化 1.5-3x → ζ 有意义但非核心
     - BER 变化 <1.5x → ζ 无独立设计价值
     - 最优 ζ 如果跨湍流/SNR 一致 → 固定 ζ 合理
     - 最优 ζ 如果随条件变化 → 需要设计准则

  5. 已知安全检查:
     - ζ 过低 (<0.3): 环路可能不稳定（不在本实验范围内）
     - ζ 过高 (>2.0): 环路过于迟钝（不在本实验范围内）
     - 实验范围 [0.5, 1.0] 是工程常用范围

信号模型铁律: r = sqrt(h) * s * exp(j*phi) + n, gamma = gamma_bar * h
措辞: ω_n 单位 rad/s, h 叫"归一化辐照度", ζ 叫"阻尼系数"
"""

import sys, os
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    dpll_track, resolve_qpsk, save_results,
)

# ── 实验参数 ─────────────────────────────────────────────────
ZETA_VALUES = [0.5, 0.6, np.sqrt(2)/2, 0.8, 1.0]
OMEGA_N_VALUES = [5e6, 10e6, 20e6, 50e6]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_POINTS = [10, 15, 20]  # dB
SEEDS = list(range(1000, 1010))
NS = 50000
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7

# ── 路径 ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'dpll_zeta_sweep.json')
OUT_PDF_THESIS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(BASE))),
    '毕设', '写作材料', 'figures', 'dpll_zeta_sweep.pdf',
)

# ── 单次试验 ────────────────────────────────────────────────
def run_single_trial(omega_n, zeta, turb, gamma_bar, seed):
    """FOE + DPLL(omega_n, zeta) 单次试验"""
    shared = generate_shared_realization(NS, gamma_bar, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * np.arange(NS))
    rx_out, _ = dpll_track(rx_foc, omega_n=omega_n, zeta=zeta)
    ber = resolve_qpsk(rx_out, shared['bits'])
    return max(ber, BER_FLOOR)


# ── 主循环 ───────────────────────────────────────────────────
def main():
    t0 = time.time()
    results = {}

    total = (len(SNR_POINTS) * len(TURB_LEVELS)
             * len(OMEGA_N_VALUES) * len(ZETA_VALUES) * len(SEEDS))
    done = 0

    for snr_db in SNR_POINTS:
        gamma_bar = 10 ** (snr_db / 10)
        results[str(snr_db)] = {}

        for turb in TURB_LEVELS:
            results[str(snr_db)][turb] = {}

            for omega_n in OMEGA_N_VALUES:
                omega_key = str(int(omega_n))
                results[str(snr_db)][turb][omega_key] = {}

                for zeta in ZETA_VALUES:
                    zeta_key = f"{zeta:.4f}"
                    ber_list = []

                    for sd in SEEDS:
                        ber = run_single_trial(omega_n, zeta, turb, gamma_bar, sd)
                        ber_list.append(ber)
                        done += 1
                        if done % 100 == 0 or done == total:
                            elapsed = time.time() - t0
                            print(f"[{done}/{total}] SNR={snr_db}dB turb={turb} "
                                  f"ω_n={omega_n/1e6:.0f}MHz ζ={zeta:.3f} "
                                  f"seed={sd} BER={ber:.2e}  ({elapsed:.1f}s)")

                    ber_arr = np.array(ber_list)
                    results[str(snr_db)][turb][omega_key][zeta_key] = {
                        'ber_mean': float(np.mean(ber_arr)),
                        'ber_std': float(np.std(ber_arr)),
                        'ber_values': [float(b) for b in ber_arr],
                    }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} trials)")

    # ── 理论预期验证 ──────────────────────────────────────────
    verify_expectations(results)

    # ── 保存 JSON（含元数据） ─────────────────────────────────
    meta = {
        'zeta_values': [float(z) for z in ZETA_VALUES],
        'omega_n_values': [int(o) for o in OMEGA_N_VALUES],
        'turb_levels': TURB_LEVELS,
        'snr_points': SNR_POINTS,
        'seeds': SEEDS,
        'Ns': NS,
        'f_dot': float(F_DOT),
        'theory': {
            'bl_omega_ratio': {
                f'zeta={z:.3f}': float((1 + 4*z**2) / (8*z))
                for z in ZETA_VALUES
            },
            'baseline_zeta': float(np.sqrt(2)/2),
            'expected_effect': '<1.5x BER variation across zeta',
        },
    }

    output = {'meta': meta, 'results': results}
    save_results(output, OUT_JSON, 'sim_dpll_zeta_sweep')
    print(f"JSON saved: {OUT_JSON}")

    # ── 绘图 ─────────────────────────────────────────────────
    plot_results(results, meta)


def verify_expectations(results):
    """TL-20: 与理论预期对比，偏离即报告"""
    print("\n" + "=" * 72)
    print("理论预期验证（TL-20）")
    print("=" * 72)

    baseline_zeta = f"{np.sqrt(2)/2:.4f}"

    for turb in TURB_LEVELS:
        for snr_db in SNR_POINTS:
            for omega_n in OMEGA_N_VALUES:
                omega_key = str(int(omega_n))
                try:
                    zeta_data = results[str(snr_db)][turb][omega_key]
                except KeyError:
                    continue

                bers = {}
                for zeta_key, data in zeta_data.items():
                    bers[float(zeta_key)] = data['ber_mean']

                if not bers:
                    continue

                best_zeta = min(bers, key=bers.get)
                worst_zeta = max(bers, key=bers.get)
                baseline_ber = bers.get(float(baseline_zeta), None)

                if baseline_ber and baseline_ber > 0 and worst_zeta > 0:
                    ratio = bers[worst_zeta] / max(bers[best_zeta], BER_FLOOR)

                    # 检查锚点
                    alert = ""
                    if ratio > 3.0:
                        alert = " ⚠️ >3x! ζ 是重要设计参数!"
                    elif ratio > 1.5:
                        alert = " ⚡ 1.5-3x, ζ 有意义"

                    print(f"  {turb:>10} {snr_db:>3}dB ω={omega_n/1e6:>3.0f}M: "
                          f"best_ζ={best_zeta:.3f} worst_ζ={worst_zeta:.3f} "
                          f"ratio={ratio:.2f}x baseline={baseline_ber:.2e}"
                          f"{alert}")


# ═══════════════════════════════════════════════════════════════
# 绘图
# ═══════════════════════════════════════════════════════════════
def plot_results(results, meta):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    zeta_labels = [f'{z:.3f}' for z in ZETA_VALUES]
    zeta_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    turb_labels = {
        'weak': 'Weak Turbulence',
        'moderate': 'Moderate Turbulence',
        'strong': 'Strong Turbulence',
    }

    # ── 图1: BER vs ζ, 每面板一个 (turb, SNR), 多 ω_n 曲线 ──
    fig, axes = plt.subplots(3, 3, figsize=(15, 12), sharex=True, sharey='row')

    for col, snr_db in enumerate(SNR_POINTS):
        for row, turb in enumerate(TURB_LEVELS):
            ax = axes[row, col]

            for oi, omega_n in enumerate(OMEGA_N_VALUES):
                omega_key = str(int(omega_n))
                try:
                    zeta_data = results[str(snr_db)][turb][omega_key]
                except KeyError:
                    continue

                bers = []
                for zeta in ZETA_VALUES:
                    zk = f"{zeta:.4f}"
                    if zk in zeta_data:
                        bers.append(zeta_data[zk]['ber_mean'])
                    else:
                        bers.append(None)

                valid_x = [z for z, b in zip(ZETA_VALUES, bers) if b is not None]
                valid_y = [b for b in bers if b is not None]
                if valid_x:
                    ax.semilogy(valid_x, valid_y, 'o-',
                               label=f'ω={omega_n/1e6:.0f}M',
                               color=zeta_colors[oi % len(zeta_colors)],
                               markersize=4, linewidth=1.2)

            # 标记基线 ζ=√2/2
            ax.axvline(np.sqrt(2)/2, color='gray', linestyle=':', alpha=0.5,
                      label='ζ=√2/2 (baseline)')

            if row == 0:
                ax.set_title(f'SNR={snr_db} dB')
            if row == 2:
                ax.set_xlabel('Damping ratio ζ')
            if col == 0:
                ax.set_ylabel(f'{turb_labels[turb]}\nMean BER')
            ax.grid(True, which='both', alpha=0.3)
            if col == 2:
                ax.legend(fontsize=6, loc='best')

    fig.suptitle('DPLL Damping Ratio ζ Sweep: BER vs ζ\n'
                 '(FOE + DPLL, 50k symbols, 10 seeds per point)',
                 fontsize=12, y=1.02)
    fig.tight_layout()

    d = os.path.dirname(OUT_PDF_THESIS)
    if d:
        os.makedirs(d, exist_ok=True)
    fig.savefig(OUT_PDF_THESIS, bbox_inches='tight', dpi=300)
    print(f"PDF saved: {OUT_PDF_THESIS}")
    plt.close(fig)

    # ── 图2: 强湍流热力图 (ζ × ω_n), 分 SNR ────────────────
    fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4))

    zeta_strs = [f'{z:.3f}' for z in ZETA_VALUES]
    omega_strs = [f'{o/1e6:.0f}M' for o in OMEGA_N_VALUES]

    for col, snr_db in enumerate(SNR_POINTS):
        ax = axes2[col]
        matrix = np.zeros((len(ZETA_VALUES), len(OMEGA_N_VALUES)))

        for zi, zeta in enumerate(ZETA_VALUES):
            for oi, omega_n in enumerate(OMEGA_N_VALUES):
                zk = f"{zeta:.4f}"
                ok = str(int(omega_n))
                try:
                    matrix[zi, oi] = results[str(snr_db)]['strong'][ok][zk]['ber_mean']
                except KeyError:
                    matrix[zi, oi] = np.nan

        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
        ax.set_xticks(range(len(OMEGA_N_VALUES)))
        ax.set_xticklabels(omega_strs)
        ax.set_yticks(range(len(ZETA_VALUES)))
        ax.set_yticklabels(zeta_strs)
        ax.set_xlabel('ω_n')
        ax.set_ylabel('ζ')
        ax.set_title(f'Strong turb, SNR={snr_db}dB')

        for i in range(len(ZETA_VALUES)):
            for j in range(len(OMEGA_N_VALUES)):
                val = matrix[i, j]
                if not np.isnan(val):
                    ax.text(j, i, f'{val:.1e}', ha='center', va='center',
                           fontsize=7, fontweight='bold',
                           color='white' if val > np.nanmax(matrix)*0.6 else 'black')

        plt.colorbar(im, ax=ax, label='Mean BER')

    fig2.suptitle('Strong Turbulence: BER Heatmap (ζ × ω_n)', fontsize=12)
    fig2.tight_layout()

    pdf2 = OUT_PDF_THESIS.replace('.pdf', '_heatmap.pdf')
    fig2.savefig(pdf2, bbox_inches='tight', dpi=300)
    print(f"Heatmap saved: {pdf2}")
    plt.close(fig2)


if __name__ == '__main__':
    main()
