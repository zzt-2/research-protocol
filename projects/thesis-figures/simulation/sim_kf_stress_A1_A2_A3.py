#!/usr/bin/env python3
"""KF Stress Test A1+A2+A3 — 共享信道验证、多种子鲁棒性、统计显著性

A1: TL-13 共享信道验证 — 旧方式 vs 新方式增益对比
A2: 100 种子鲁棒性 — 均值/中位数/分位数
A3: Wilcoxon 符号秩检验 — p-value + 效应量

自包含脚本，只依赖 sim_kf_stress_common。
旧方式函数从 sim_ch4_kf_pilot_h.py 内联。
"""

from sim_kf_stress_common import *
import numpy as np
from scipy import stats
import sys

# ═══════════════════════════════════════════════════════════════
# 内联旧方式函数（从 sim_ch4_kf_pilot_h.py 复制）
# 这些函数各自生成独立信道（TL-13 违规），用于对比。
# ═══════════════════════════════════════════════════════════════
def _old_generate_signal_no_pilots(Ns, gamma_bar, turb_name, f_dot):
    """旧方式：无导频信号生成（含 MMSE 均衡）"""
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns*2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx = signal + noise
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar)
    rx_comp = amp_limit(rx_comp, 3.0)
    return rx_comp, bits, h, phi


def _old_generate_frame_with_pilots(Ns, gamma_bar, turb_name, f_dot, n_pilots_per_block=5):
    """旧方式：含导频帧信号生成（含 MMSE 均衡）"""
    a, b = TURB[turb_name]
    n_blocks = Ns // BLOCK

    pilots_all = get_pilots(n_pilots_per_block)
    n_data_per_block = BLOCK - n_pilots_per_block
    total_data_syms = n_blocks * n_data_per_block
    data_bits = np.random.randint(0, 2, total_data_syms * 2)
    data_syms = qpsk_mod(data_bits)

    tx_frame = np.zeros(Ns, dtype=complex)
    data_idx = 0
    data_indices = []
    pilot_indices = []

    for b_idx in range(n_blocks):
        base = b_idx * BLOCK
        for p in range(n_pilots_per_block):
            idx = base + p
            tx_frame[idx] = pilots_all[p]
            pilot_indices.append(idx)
        for d in range(n_data_per_block):
            idx = base + n_pilots_per_block + d
            tx_frame[idx] = data_syms[data_idx]
            data_idx += 1
            data_indices.append(idx)

    data_indices = np.array(data_indices)
    pilot_indices = np.array(pilot_indices)

    h_raw = gg_block(Ns, a, b)
    h_blocks = np.array([h_raw[b_idx * BLOCK] for b_idx in range(n_blocks)])
    h = h_raw.copy()

    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx_frame * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx = signal + noise

    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar)
    rx_comp = amp_limit(rx_comp, 3.0)

    h_med = np.median(h_blocks)

    return rx_comp, data_bits, data_indices, pilot_indices, h, h_blocks, h_med


# ═══════════════════════════════════════════════════════════════
# A1: TL-13 共享信道验证
# ═══════════════════════════════════════════════════════════════
def run_A1(Ns=10000, gamma_bar=GAMMA_BAR_DEFAULT, f_dot=DOPPLER_HIGH,
           n_trials=30, turb_list=None, n_pilots=5):
    if turb_list is None:
        turb_list = ['weak', 'moderate', 'strong']

    print("=" * 80)
    print("A1: TL-13 Shared Channel Verification")
    print(f"  Ns={Ns}, trials={n_trials}, SNR={10*np.log10(gamma_bar):.0f}dB, "
          f"f_dot={f_dot/1e6:.0f}MHz/s, n_pilots={n_pilots}")
    print("=" * 80)

    results = {'old': {}, 'new': {}}

    for turb in turb_list:
        old_gains = []
        new_gains = []

        for trial in range(n_trials):
            seed = 42 + trial

            # --- 旧方式：Fixed 和 KF pilot 各自生成信号 ---
            np.random.seed(seed)
            rx_comp_fixed, bits_fixed, h_fixed, phi_fixed = \
                _old_generate_signal_no_pilots(Ns, gamma_bar, turb, f_dot)
            ber_fixed_old = resolve_qpsk(carrier_recovery_fixed(rx_comp_fixed), bits_fixed)

            np.random.seed(seed)
            rx_comp_p, data_bits_p, data_idx_p, pilot_idx_p, h_p, h_blocks_p, h_med_p = \
                _old_generate_frame_with_pilots(Ns, gamma_bar, turb, f_dot, n_pilots)
            corrected_old, _ = kf_pilot_recovery(
                rx_comp_p, gamma_bar, turb, n_pilots, h_med_p, f_dot)
            ber_pilot_old = resolve_qpsk(corrected_old[data_idx_p], data_bits_p)

            gain_old = db_ratio(ber_fixed_old, ber_pilot_old)
            old_gains.append(gain_old)

            # --- 新方式：共享信道 ---
            shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)

            rx_fixed_new = run_fixed(shared, eq_mode='oracle')
            ber_fixed_new = resolve_qpsk(rx_fixed_new, shared['bits'])

            corrected_new, data_idx_n, data_bits_n, _ = run_kf_pilot(
                shared, n_pilots, eq_mode='oracle')
            ber_pilot_new = resolve_qpsk(corrected_new[data_idx_n], data_bits_n)

            gain_new = db_ratio(ber_fixed_new, ber_pilot_new)
            new_gains.append(gain_new)

        results['old'][turb] = {
            'gains': old_gains,
            'mean': float(np.mean(old_gains)),
            'std': float(np.std(old_gains)),
        }
        results['new'][turb] = {
            'gains': new_gains,
            'mean': float(np.mean(new_gains)),
            'std': float(np.std(new_gains)),
        }

        old_m = np.mean(old_gains)
        new_m = np.mean(new_gains)
        delta = new_m - old_m
        print(f"\n  {turb:10s}: old_gain={old_m:+.2f}dB  new_gain={new_m:+.2f}dB  "
              f"delta={delta:+.2f}dB")

    # PASS 判定
    pass_results = {}
    for turb in turb_list:
        new_mean = results['new'][turb]['mean']
        passed = new_mean > 5.0
        pass_results[turb] = passed
        status = "PASS" if passed else "FAIL"
        print(f"\n  A1 [{turb:10s}]: KF_pilot gain (shared) = {new_mean:+.2f}dB "
              f"[threshold >5dB] => {status}")

    return results, pass_results


# ═══════════════════════════════════════════════════════════════
# A2: 多种子鲁棒性
# ═══════════════════════════════════════════════════════════════
def run_A2(Ns=10000, gamma_bar=GAMMA_BAR_DEFAULT, f_dot=DOPPLER_HIGH,
           seed_start=1001, n_seeds=100, turb_list=None, n_pilots=5):
    if turb_list is None:
        turb_list = ['weak', 'moderate', 'strong']

    schemes = ['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']

    print("\n" + "=" * 80)
    print("A2: Multi-Seed Robustness")
    print(f"  Ns={Ns}, seeds={n_seeds} ({seed_start}..{seed_start+n_seeds-1}), "
          f"SNR={10*np.log10(gamma_bar):.0f}dB, f_dot={f_dot/1e6:.0f}MHz/s")
    print("=" * 80)

    results = {s: {t: [] for t in turb_list} for s in schemes}

    for turb in turb_list:
        print(f"\n  --- {turb} ---")
        for i in range(n_seeds):
            seed = seed_start + i
            trial = run_trial_shared(Ns, gamma_bar, turb, f_dot, seed,
                                     schemes=schemes, n_pilots=n_pilots, eq_mode='oracle')
            for s in schemes:
                results[s][turb].append(trial[s])

        # 统计
        print(f"\n  Scheme Statistics ({turb}):")
        print(f"  {'Scheme':>12s} | {'Mean':>10s} | {'Median':>10s} | {'Std':>10s} "
              f"| {'P5':>10s} | {'P95':>10s} | {'Min':>10s} | {'Max':>10s}")
        print("  " + "-" * 90)
        for s in schemes:
            arr = np.array(results[s][turb])
            print(f"  {s:>12s} | {np.mean(arr):10.6f} | {np.median(arr):10.6f} "
                  f"| {np.std(arr):10.6f} | {np.percentile(arr,5):10.6f} "
                  f"| {np.percentile(arr,95):10.6f} | {np.min(arr):10.6f} "
                  f"| {np.max(arr):10.6f}")

    # PASS 判定：>=90% 种子 kf_pilot 增益 > 3dB（中/强湍流）
    pass_results = {}
    for turb in turb_list:
        fixed_arr = np.array(results['fixed'][turb])
        pilot_arr = np.array(results['kf_pilot'][turb])
        # 逐种子计算增益（BER_fixed / BER_pilot > 2 => >3dB）
        gains_db = np.array([db_ratio(f, p) for f, p in zip(fixed_arr, pilot_arr)])
        frac_above_3db = np.mean(gains_db > 3.0)
        passed = frac_above_3db >= 0.9
        pass_results[turb] = {
            'passed': passed,
            'frac_above_3db': float(frac_above_3db),
            'mean_gain_db': float(np.mean(gains_db)),
            'median_gain_db': float(np.median(gains_db)),
        }
        status = "PASS" if passed else "FAIL"
        print(f"\n  A2 [{turb:10s}]: {frac_above_3db*100:.1f}% seeds >3dB "
              f"(mean gain={np.mean(gains_db):.2f}dB) "
              f"[threshold >=90%] => {status}")

    return results, pass_results


# ═══════════════════════════════════════════════════════════════
# A3: 统计显著性检验
# ═══════════════════════════════════════════════════════════════
def run_A3(a2_results, turb_list=None):
    if turb_list is None:
        turb_list = ['weak', 'moderate', 'strong']

    print("\n" + "=" * 80)
    print("A3: Wilcoxon Signed-Rank Test (fixed BER - pilot BER)")
    print("=" * 80)

    test_results = {}

    for turb in turb_list:
        fixed_arr = np.array(a2_results['fixed'][turb])
        pilot_arr = np.array(a2_results['kf_pilot'][turb])

        diff = fixed_arr - pilot_arr
        n_pos = int(np.sum(diff > 0))
        n_neg = int(np.sum(diff < 0))
        n_zero = int(np.sum(diff == 0))

        # 移除零差值（Wilcoxon 要求）
        diff_nz = diff[diff != 0]
        if len(diff_nz) < 10:
            print(f"\n  A3 [{turb:10s}]: Not enough non-zero differences ({len(diff_nz)})")
            test_results[turb] = {'passed': False, 'reason': 'insufficient_data'}
            continue

        try:
            stat_val, p_value = stats.wilcoxon(diff_nz, alternative='greater')
        except Exception as e:
            print(f"\n  A3 [{turb:10s}]: Wilcoxon failed: {e}")
            test_results[turb] = {'passed': False, 'reason': str(e)}
            continue

        # 效应量: rank-biserial correlation
        # scipy wilcoxon with alternative='greater' returns W = sum of positive ranks
        # r = W / (n*(n+1)/2), which is in [0, 1] when all diffs > 0
        n_nz = len(diff_nz)
        r_effect = stat_val / (n_nz * (n_nz + 1) / 2.0)

        passed = (p_value < 0.01) and (r_effect > 0.5)
        test_results[turb] = {
            'passed': passed,
            'p_value': float(p_value),
            'r_effect': float(r_effect),
            'statistic': float(stat_val),
            'n_pos': n_pos,
            'n_neg': n_neg,
            'n_zero': n_zero,
            'n_effective': n_nz,
        }

        status = "PASS" if passed else "FAIL"
        print(f"\n  A3 [{turb:10s}]:")
        print(f"    positive diffs: {n_pos}, negative: {n_neg}, zero: {n_zero}")
        print(f"    Wilcoxon stat = {stat_val:.2f}, p-value = {p_value:.2e}")
        print(f"    Rank-biserial r = {r_effect:.4f}")
        print(f"    [p<0.01 AND r>0.5] => {status}")

    return test_results


# ═══════════════════════════════════════════════════════════════
# 绘图
# ═══════════════════════════════════════════════════════════════
def make_figure(a1_results, a2_results, a3_results, turb_list, out_dir):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- (0,0) A1: Old vs New gain comparison ---
    ax = axes[0, 0]
    x_pos = np.arange(len(turb_list))
    width = 0.35
    old_means = [a1_results['old'][t]['mean'] for t in turb_list]
    new_means = [a1_results['new'][t]['mean'] for t in turb_list]
    old_stds = [a1_results['old'][t]['std'] for t in turb_list]
    new_stds = [a1_results['new'][t]['std'] for t in turb_list]

    ax.bar(x_pos - width/2, old_means, width, yerr=old_stds,
           label='Old (separate ch)', color='salmon', capsize=3, alpha=0.8)
    ax.bar(x_pos + width/2, new_means, width, yerr=new_stds,
           label='New (shared ch)', color='seagreen', capsize=3, alpha=0.8)
    ax.axhline(y=5.0, color='red', linestyle='--', alpha=0.5, label='5dB threshold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([t.capitalize() for t in turb_list])
    ax.set_ylabel('KF pilot gain over Fixed (dB)')
    ax.set_title('A1: TL-13 Shared Channel Verification')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # --- (0,1) A1: Per-trial scatter ---
    ax = axes[0, 1]
    colors_scatter = {'weak': '#3498db', 'moderate': '#e67e22', 'strong': '#e74c3c'}
    for turb in turb_list:
        old_g = a1_results['old'][turb]['gains']
        new_g = a1_results['new'][turb]['gains']
        ax.scatter(old_g, new_g, alpha=0.5, s=20, color=colors_scatter[turb], label=turb)
    lims = [ax.get_xlim()[0], ax.get_xlim()[1]]
    ax.plot(lims, lims, 'k--', alpha=0.3, label='y=x')
    ax.axhline(y=5.0, color='red', linestyle=':', alpha=0.5)
    ax.set_xlabel('Old gain (dB)')
    ax.set_ylabel('New gain (dB)')
    ax.set_title('A1: Per-Trial Old vs New Gain')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # --- (1,0) A2: Box plot of BER per scheme per turbulence ---
    ax = axes[1, 0]
    scheme_labels = ['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']
    display_labels = ['Fixed', 'KF oracle', 'KF frame', 'KF pilot']
    box_colors = ['steelblue', '#9b59b6', 'coral', '#2ecc71']

    all_box_data = []
    all_box_colors = []
    all_box_positions = []
    xtick_positions = []
    xtick_labels = []

    pos = 0
    for ti, turb in enumerate(turb_list):
        for si, s in enumerate(scheme_labels):
            all_box_data.append(a2_results[s][turb])
            all_box_colors.append(box_colors[si])
            all_box_positions.append(pos)
            pos += 1
        xtick_positions.append(np.mean(all_box_positions[-4:]))
        xtick_labels.append(turb.capitalize())
        pos += 1

    bp = ax.boxplot(all_box_data, positions=all_box_positions, widths=0.7,
                    patch_artist=True, showfliers=False, notch=False)
    for patch, color in zip(bp['boxes'], all_box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_labels)
    ax.set_ylabel('BER')
    ax.set_title('A2: BER Distribution (100 seeds)')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')

    from matplotlib.patches import Patch
    legend_elems = [Patch(facecolor=c, alpha=0.6, label=l)
                    for c, l in zip(box_colors, display_labels)]
    ax.legend(handles=legend_elems, fontsize=6, loc='upper right')

    # --- (1,1) A3: Gain distribution + significance markers ---
    ax = axes[1, 1]
    # Pre-collect all gains to determine y-range before annotations
    all_gains_for_ylim = []
    for turb in turb_list:
        fixed_arr = np.array(a2_results['fixed'][turb])
        pilot_arr = np.array(a2_results['kf_pilot'][turb])
        gains_db = np.array([db_ratio(f, p) for f, p in zip(fixed_arr, pilot_arr)])
        all_gains_for_ylim.append(gains_db)

    for ti, turb in enumerate(turb_list):
        gains_db = all_gains_for_ylim[ti]
        parts = ax.violinplot([gains_db], positions=[ti], showmeans=True, showmedians=True)
        for pc in parts['bodies']:
            pc.set_facecolor(colors_scatter[turb])
            pc.set_alpha(0.5)

    # Set y-axis limits based on data before adding text
    flat_gains = np.concatenate(all_gains_for_ylim)
    y_max = max(flat_gains.max() * 1.1, 20.0)
    y_min = min(flat_gains.min() * 0.9, -5.0)
    ax.set_ylim(y_min, y_max)

    for ti, turb in enumerate(turb_list):
        if turb in a3_results and 'p_value' in a3_results[turb]:
            p = a3_results[turb]['p_value']
            r = a3_results[turb]['r_effect']
            marker = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
            ax.text(ti, y_max * 0.95,
                    f'{marker}\np={p:.1e}\nr={r:.2f}',
                    ha='center', va='top', fontsize=7,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.axhline(y=3.0, color='orange', linestyle='--', alpha=0.5, label='3dB threshold')
    ax.set_xticks(range(len(turb_list)))
    ax.set_xticklabels([t.capitalize() for t in turb_list])
    ax.set_ylabel('KF pilot gain over Fixed (dB)')
    ax.set_title('A3: Gain Distribution + Significance')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('KF Stress Test: A1 (Shared Ch) + A2 (100 Seeds) + A3 (Wilcoxon)',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    save_path = os.path.join(out_dir, 'fig_kf_stress_A1A2A3.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nFigure saved to {save_path}")
    return save_path


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t_start = time.time()

    Ns = 10000
    gamma_bar = GAMMA_BAR_DEFAULT   # 100 = 20dB
    f_dot = DOPPLER_HIGH            # 150e6
    turb_list = ['weak', 'moderate', 'strong']
    n_pilots = 5

    # ---- A1 ----
    a1_results, a1_pass = run_A1(Ns, gamma_bar, f_dot, n_trials=30,
                                  turb_list=turb_list, n_pilots=n_pilots)

    # ---- A2 ----
    a2_results, a2_pass = run_A2(Ns, gamma_bar, f_dot, seed_start=1001,
                                  n_seeds=100, turb_list=turb_list, n_pilots=n_pilots)

    # ---- A3 ----
    a3_results = run_A3(a2_results, turb_list=turb_list)

    # ---- Figure ----
    fig_path = make_figure(a1_results, a2_results, a3_results, turb_list, OUT)

    # ═══════════════════════════════════════════════════════════
    # Final Summary Table
    # ═══════════════════════════════════════════════════════════
    dt = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"FINAL SUMMARY ({dt:.1f}s)")
    print("=" * 80)

    print("\n--- A1: TL-13 Shared Channel Verification ---")
    print(f"  {'Turbulence':>12s} | {'Old gain':>10s} | {'New gain':>10s} | {'Delta':>10s} | {'Result':>6s}")
    print("  " + "-" * 60)
    for turb in turb_list:
        om = a1_results['old'][turb]['mean']
        nm = a1_results['new'][turb]['mean']
        d = nm - om
        s = "PASS" if a1_pass[turb] else "FAIL"
        print(f"  {turb:>12s} | {om:+10.2f} | {nm:+10.2f} | {d:+10.2f} | {s:>6s}")

    print("\n--- A2: Multi-Seed Robustness (100 seeds) ---")
    print(f"  {'Turbulence':>12s} | {'Mean gain':>10s} | {'Median':>10s} | {'%>3dB':>8s} | {'Result':>6s}")
    print("  " + "-" * 55)
    for turb in turb_list:
        info = a2_pass[turb]
        s = "PASS" if info['passed'] else "FAIL"
        print(f"  {turb:>12s} | {info['mean_gain_db']:+10.2f} | "
              f"{info['median_gain_db']:+10.2f} | "
              f"{info['frac_above_3db']*100:7.1f}% | {s:>6s}")

    print("\n--- A3: Wilcoxon Signed-Rank Test ---")
    print(f"  {'Turbulence':>12s} | {'p-value':>12s} | {'r (effect)':>10s} | {'Result':>6s}")
    print("  " + "-" * 50)
    for turb in turb_list:
        r = a3_results[turb]
        if 'p_value' in r:
            s = "PASS" if r['passed'] else "FAIL"
            print(f"  {turb:>12s} | {r['p_value']:12.2e} | {r['r_effect']:10.4f} | {s:>6s}")
        else:
            print(f"  {turb:>12s} | {'N/A':>12s} | {'N/A':>10s} | {'FAIL':>6s}")

    # Overall
    all_a1 = all(a1_pass.values())
    all_a2 = all(v['passed'] for v in a2_pass.values())
    all_a3 = all(v.get('passed', False) for v in a3_results.values())
    overall = "ALL PASS" if (all_a1 and all_a2 and all_a3) else "SOME FAIL"
    print(f"\n  Overall: {overall}")

    # ═══════════════════════════════════════════════════════════
    # Save JSON
    # ═══════════════════════════════════════════════════════════
    save = {
        'config': {
            'Ns': Ns,
            'gamma_bar': gamma_bar,
            'gamma_db': float(10 * np.log10(gamma_bar)),
            'f_dot': f_dot,
            'turb_list': turb_list,
            'n_pilots': n_pilots,
            'a1_trials': 30,
            'a2_seeds': 100,
            'a2_seed_range': [1001, 1100],
        },
        'A1': {},
        'A2': {},
        'A3': {},
    }

    for turb in turb_list:
        save['A1'][turb] = {
            'old_mean_gain': a1_results['old'][turb]['mean'],
            'old_std_gain': a1_results['old'][turb]['std'],
            'new_mean_gain': a1_results['new'][turb]['mean'],
            'new_std_gain': a1_results['new'][turb]['std'],
            'pass': a1_pass[turb],
        }

    for turb in turb_list:
        for s in ['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']:
            arr = np.array(a2_results[s][turb])
            save['A2'].setdefault(turb, {})[s] = {
                'mean': float(np.mean(arr)),
                'median': float(np.median(arr)),
                'std': float(np.std(arr)),
                'p5': float(np.percentile(arr, 5)),
                'p95': float(np.percentile(arr, 95)),
                'min': float(np.min(arr)),
                'max': float(np.max(arr)),
                'per_seed': [float(x) for x in arr],
            }
        save['A2'][turb]['pass'] = a2_pass[turb]

    for turb in turb_list:
        r = a3_results[turb]
        save['A3'][turb] = r

    save['overall'] = {
        'A1_pass': bool(all_a1),
        'A2_pass': bool(all_a2),
        'A3_pass': bool(all_a3),
        'all_pass': bool(all_a1 and all_a2 and all_a3),
    }

    # Ensure all values are JSON-serializable (convert numpy types)
    def to_json_serializable(obj):
        if isinstance(obj, dict):
            return {k: to_json_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [to_json_serializable(v) for v in obj]
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    save = to_json_serializable(save)

    json_path = os.path.join(OUT, 'results_kf_stress_A1A2A3.json')
    with open(json_path, 'w') as f:
        json.dump(save, f, indent=2)
    print(f"\nResults saved to {json_path}")
    print(f"Total time: {dt:.1f}s")
    print("=" * 80)
