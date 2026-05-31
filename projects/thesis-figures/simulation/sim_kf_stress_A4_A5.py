#!/usr/bin/env python3
"""KF Stress Test A4 + A5
A4: SNR 全扫描 — BER vs SNR 曲线，3 种湍流
A5: 序列长度影响 — BER vs Ns 曲线，3 种湍流
"""

from sim_kf_stress_common import *
import itertools

# ═══════════════════════════════════════════════════════════════
# 参数配置
# ═══════════════════════════════════════════════════════════════
SEEDS = list(range(1001, 1031))  # 30 seeds
TURB_NAMES = ['weak', 'moderate', 'strong']

# A4 参数
A4_SNR_DB = [0, 5, 10, 15, 20, 25, 30]
A4_NS = 10000
A4_F_DOT = 150e6
A4_SCHEMES = ['fixed', 'kf_pilot', 'kf_oracle']
A4_N_PILOTS = 5

# A5 参数
A5_NS_LIST = [1000, 2000, 5000, 10000, 20000, 50000]
A5_GAMMA_BAR = 100  # 20 dB
A5_F_DOT = 150e6
A5_SCHEMES = ['fixed', 'kf_pilot']
A5_N_PILOTS = 5

EQ_MODE = 'oracle'


def run_a4():
    """A4: SNR 全扫描"""
    print("=" * 60)
    print("A4: SNR 全扫描")
    print(f"  SNR_dB = {A4_SNR_DB}")
    print(f"  seeds = {SEEDS[0]}~{SEEDS[-1]} ({len(SEEDS)})")
    print(f"  Ns={A4_NS}, f_dot={A4_F_DOT/1e6:.0f} MHz")
    print(f"  schemes = {A4_SCHEMES}")
    print(f"  turbulences = {TURB_NAMES}")
    n_trials = len(A4_SNR_DB) * len(SEEDS) * len(TURB_NAMES) * len(A4_SCHEMES)
    print(f"  总试验数 = {n_trials}")
    print("=" * 60)

    results = {}
    t0 = time.time()
    count = 0

    for turb in TURB_NAMES:
        for snr_db in A4_SNR_DB:
            gamma_bar = 10 ** (snr_db / 10)
            bers = {s: [] for s in A4_SCHEMES}
            for seed in SEEDS:
                trial = run_trial_shared(
                    A4_NS, gamma_bar, turb, A4_F_DOT, seed,
                    schemes=A4_SCHEMES, n_pilots=A4_N_PILOTS, eq_mode=EQ_MODE)
                for s in A4_SCHEMES:
                    bers[s].append(trial[s])
                count += len(A4_SCHEMES)

            key = (turb, snr_db)
            results[key] = {s: np.mean(bers[s]) for s in A4_SCHEMES}

            elapsed = time.time() - t0
            print(f"  [{count}/{n_trials}] {turb:>8s} SNR={snr_db:2d}dB | "
                  + " | ".join(f"{s}: {results[key][s]:.2e}" for s in A4_SCHEMES)
                  + f"  ({elapsed:.0f}s)")

    print(f"A4 完成: {time.time()-t0:.1f}s")
    return results


def run_a5():
    """A5: 序列长度影响"""
    print("\n" + "=" * 60)
    print("A5: 序列长度影响")
    print(f"  Ns = {A5_NS_LIST}")
    print(f"  gamma_bar = {A5_GAMMA_BAR} (20 dB), f_dot = {A5_F_DOT/1e6:.0f} MHz")
    print(f"  seeds = {SEEDS[0]}~{SEEDS[-1]} ({len(SEEDS)})")
    print(f"  schemes = {A5_SCHEMES}")
    print(f"  turbulences = {TURB_NAMES}")
    n_trials = len(A5_NS_LIST) * len(SEEDS) * len(TURB_NAMES) * len(A5_SCHEMES)
    print(f"  总试验数 = {n_trials}")
    print("=" * 60)

    results = {}
    t0 = time.time()
    count = 0

    for turb in TURB_NAMES:
        for ns in A5_NS_LIST:
            bers = {s: [] for s in A5_SCHEMES}
            for seed in SEEDS:
                trial = run_trial_shared(
                    ns, A5_GAMMA_BAR, turb, A5_F_DOT, seed,
                    schemes=A5_SCHEMES, n_pilots=A5_N_PILOTS, eq_mode=EQ_MODE)
                for s in A5_SCHEMES:
                    bers[s].append(trial[s])
                count += len(A5_SCHEMES)

            key = (turb, ns)
            results[key] = {s: np.mean(bers[s]) for s in A5_SCHEMES}

            elapsed = time.time() - t0
            print(f"  [{count}/{n_trials}] {turb:>8s} Ns={ns:6d} | "
                  + " | ".join(f"{s}: {results[key][s]:.2e}" for s in A5_SCHEMES)
                  + f"  ({elapsed:.0f}s)")

    print(f"A5 完成: {time.time()-t0:.1f}s")
    return results


# ═══════════════════════════════════════════════════════════════
# 判定
# ═══════════════════════════════════════════════════════════════
def check_a4_floor(a4_results):
    """A4 PASS: 20dB 以上 KF BER 持续下降（无 floor）"""
    print("\n--- A4 Floor 检查 ---")
    all_pass = True
    for turb in TURB_NAMES:
        for scheme in ['kf_pilot', 'kf_oracle']:
            bers_20plus = []
            for snr in [20, 25, 30]:
                key = (turb, snr)
                bers_20plus.append(a4_results[key][scheme])
            # 检查严格单调下降
            is_decreasing = all(bers_20plus[i] > bers_20plus[i+1]
                                for i in range(len(bers_20plus)-1))
            # 或者允许非严格但无回升（相邻差 < 10% 视为 floor）
            diffs = [(bers_20plus[i] - bers_20plus[i+1]) / max(bers_20plus[i], 1e-12)
                     for i in range(len(bers_20plus)-1)]
            has_floor = any(d < 0.05 for d in diffs)  # 下降 <5% 视为 floor
            status = "PASS" if is_decreasing or not has_floor else "FAIL"
            if has_floor and not is_decreasing:
                status = "FAIL"
                all_pass = False
            elif not is_decreasing:
                status = "WARN (non-strict)"
            print(f"  {turb:>8s} {scheme:10s}: "
                  + " -> ".join(f"{b:.2e}" for b in bers_20plus)
                  + f"  diffs={[f'{d:.3f}' for d in diffs]}  {status}")
    return all_pass


def check_a5_convergence(a5_results):
    """A5 PASS: Ns>=5000 后 BER 变异系数 <20%"""
    print("\n--- A5 收敛检查 ---")
    all_pass = True
    for turb in TURB_NAMES:
        for scheme in A5_SCHEMES:
            bers_stable = [a5_results[(turb, ns)][scheme]
                           for ns in A5_NS_LIST if ns >= 5000]
            mean_ber = np.mean(bers_stable)
            std_ber = np.std(bers_stable)
            cv = std_ber / mean_ber if mean_ber > 0 else float('inf')
            status = "PASS" if cv < 0.20 else "FAIL"
            if cv >= 0.20:
                all_pass = False
            print(f"  {turb:>8s} {scheme:10s}: "
                  + " | ".join(f"{b:.2e}" for b in bers_stable)
                  + f"  CV={cv:.3f}  {status}")

            # 额外检查短序列
            bers_short = [a5_results[(turb, ns)][scheme]
                          for ns in A5_NS_LIST if ns < 5000]
            bers_long = [a5_results[(turb, ns)][scheme]
                         for ns in A5_NS_LIST if ns >= 5000]
            if bers_short:
                print(f"             short Ns BER: "
                      + " | ".join(f"{b:.2e}" for b in bers_short))
    return all_pass


# ═══════════════════════════════════════════════════════════════
# 画图
# ═══════════════════════════════════════════════════════════════
SCHEME_COLORS = {
    'fixed': '#888888',
    'kf_pilot': '#2196F3',
    'kf_oracle': '#4CAF50',
}
SCHEME_LABELS = {
    'fixed': 'Fixed (FOE+DPLL+VV)',
    'kf_pilot': 'KF Pilot (n=5)',
    'kf_oracle': 'KF Oracle-h',
}
TURB_COLORS = {'weak': '#4CAF50', 'moderate': '#FF9800', 'strong': '#F44336'}


def plot_results(a4_results, a5_results):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # --- A4: BER vs SNR ---
    ax = axes[0]
    markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}
    for turb in TURB_NAMES:
        for scheme in A4_SCHEMES:
            bers = [a4_results[(turb, snr)][scheme] for snr in A4_SNR_DB]
            label = f"{turb} - {SCHEME_LABELS[scheme]}"
            style = markers[turb] if scheme != 'fixed' else markers[turb]
            ls = '-' if scheme == 'fixed' else ('--' if scheme == 'kf_pilot' else '-.')
            ax.semilogy(A4_SNR_DB, bers, ls, color=SCHEME_COLORS[scheme],
                        marker=style, markersize=4, label=label, alpha=0.8)
    ax.set_xlabel('SNR (dB)', fontsize=12)
    ax.set_ylabel('BER', fontsize=12)
    ax.set_title('A4: BER vs SNR (Ns=10000, f_dot=150 MHz)', fontsize=13)
    ax.legend(fontsize=7, ncol=2, loc='upper right')
    ax.grid(True, which='both', alpha=0.3)
    ax.set_ylim([1e-6, 1])
    ax.set_xlim([0, 30])

    # --- A5: BER vs Ns ---
    ax = axes[1]
    for turb in TURB_NAMES:
        for scheme in A5_SCHEMES:
            bers = [a5_results[(turb, ns)][scheme] for ns in A5_NS_LIST]
            label = f"{turb} - {SCHEME_LABELS[scheme]}"
            ls = '-' if scheme == 'fixed' else '--'
            ax.semilogy(A5_NS_LIST, bers, ls, color=TURB_COLORS[turb],
                        marker='o', markersize=4, label=label,
                        alpha=0.8 if scheme == 'kf_pilot' else 0.5,
                        linewidth=2 if scheme == 'kf_pilot' else 1)
    ax.set_xlabel('Sequence Length Ns', fontsize=12)
    ax.set_ylabel('BER', fontsize=12)
    ax.set_title('A5: BER vs Ns (SNR=20dB, f_dot=150 MHz)', fontsize=13)
    ax.set_xscale('log')
    ax.legend(fontsize=8, ncol=2, loc='best')
    ax.grid(True, which='both', alpha=0.3)
    ax.set_ylim([1e-4, 1])

    plt.tight_layout()
    fig_path = os.path.join(OUT, 'fig_kf_stress_A4A5.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"\n图已保存: {fig_path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════
# BER 表格打印
# ═══════════════════════════════════════════════════════════════
def print_ber_tables(a4_results, a5_results):
    print("\n" + "=" * 70)
    print("A4 BER 表格 (BER vs SNR)")
    print("=" * 70)
    header = f"{'Turb':>8s} | {'SNR':>4s} | " + " | ".join(f"{s:>10s}" for s in A4_SCHEMES)
    print(header)
    print("-" * len(header))
    for turb in TURB_NAMES:
        for snr in A4_SNR_DB:
            key = (turb, snr)
            vals = " | ".join(f"{a4_results[key][s]:10.2e}" for s in A4_SCHEMES)
            print(f"{turb:>8s} | {snr:4d} | {vals}")
        print()

    print("\n" + "=" * 70)
    print("A5 BER 表格 (BER vs Ns)")
    print("=" * 70)
    header = f"{'Turb':>8s} | {'Ns':>6s} | " + " | ".join(f"{s:>10s}" for s in A5_SCHEMES)
    print(header)
    print("-" * len(header))
    for turb in TURB_NAMES:
        for ns in A5_NS_LIST:
            key = (turb, ns)
            vals = " | ".join(f"{a5_results[key][s]:10.2e}" for s in A5_SCHEMES)
            print(f"{turb:>8s} | {ns:6d} | {vals}")
        print()


# ═══════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════
def main():
    t_start = time.time()

    # 运行 A4
    a4_results = run_a4()

    # 运行 A5
    a5_results = run_a5()

    # 打印表格
    print_ber_tables(a4_results, a5_results)

    # 判定
    a4_pass = check_a4_floor(a4_results)
    a5_pass = check_a5_convergence(a5_results)

    print("\n" + "=" * 60)
    print(f"A4 (SNR 全扫描, 无 BER floor): {'PASS' if a4_pass else 'FAIL'}")
    print(f"A5 (序列长度收敛):             {'PASS' if a5_pass else 'FAIL'}")
    print(f"总耗时: {time.time()-t_start:.1f}s")
    print("=" * 60)

    # 保存 JSON
    json_out = {'A4': {}, 'A5': {}}
    for (turb, snr), vals in a4_results.items():
        key = f"{turb}_snr{snr}"
        json_out['A4'][key] = {s: float(v) for s, v in vals.items()}
    for (turb, ns), vals in a5_results.items():
        key = f"{turb}_ns{ns}"
        json_out['A5'][key] = {s: float(v) for s, v in vals.items()}
    json_out['A4_pass'] = a4_pass
    json_out['A5_pass'] = a5_pass

    json_path = os.path.join(OUT, 'results_kf_stress_A4A5.json')
    with open(json_path, 'w') as f:
        json.dump(json_out, f, indent=2)
    print(f"JSON 已保存: {json_path}")

    # 画图
    plot_results(a4_results, a5_results)

    return {
        'A4_pass': a4_pass,
        'A5_pass': a5_pass,
        'total_time': time.time() - t_start,
    }


if __name__ == '__main__':
    summary = main()
