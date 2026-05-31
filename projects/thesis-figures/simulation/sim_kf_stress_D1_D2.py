#!/usr/bin/env python3
"""KF Stress Test D1+D2: Fixed baseline fairness & gain attribution

D1: Sequential grid search for optimal Fixed params, then KF gain residual
D2: Ablation — incremental BER contribution of each component
"""

from sim_kf_stress_common import *

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════
TURB_NAMES = ['weak', 'moderate', 'strong']
N_SEEDS = 30
NS = 10000
GAMMA_BAR = 100  # 20 dB

FOE_NFFT_GRID = [256, 512, 1024, 2048, 4096]
VV_MVV_GRID   = [16, 32, 64, 128, 256]
DPLL_OMEGA_GRID = [1e6, 2e6, 5e6, 8e6, 10e6, 15e6, 20e6]

D2_SCHEMES = ['FOE_only', 'FOE+VV', 'FOE+DPLL', 'KF_frame', 'KF_pilot']


# ═══════════════════════════════════════════════════════════════
# D1: Fixed baseline parameter search
# ═══════════════════════════════════════════════════════════════
def fixed_ber_with_cfg(shared, cfg):
    """Run Fixed baseline with a given config and return BER."""
    rx_eq = equalize_oracle(shared)
    rx_rec = carrier_recovery_fixed(rx_eq, cfg=cfg)
    return resolve_qpsk(rx_rec, shared['bits'])


def d1_sequential_search(turb_name):
    """Three-step sequential search for optimal Fixed params."""
    seeds = range(N_SEEDS)

    # --- Step 1: sweep FOE N_fft ---
    print(f"  D1 Step 1: scanning FOE N_fft ({turb_name})")
    bers_nfft = {}
    for nfft in FOE_NFFT_GRID:
        cfg = {'N_fft': nfft, 'M_vv': 64, 'omega_n': 8e6, 'zeta': np.sqrt(2)/2}
        bers = []
        for sd in seeds:
            sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
            bers.append(fixed_ber_with_cfg(sh, cfg))
        bers_nfft[nfft] = np.mean(bers)
        print(f"    N_fft={nfft:>5d}  BER={np.mean(bers):.6f}")
    best_nfft = min(bers_nfft, key=bers_nfft.get)
    print(f"    => best N_fft = {best_nfft} (BER={bers_nfft[best_nfft]:.6f})")

    # --- Step 2: sweep VV M_vv ---
    print(f"  D1 Step 2: scanning VV M_vv ({turb_name})")
    bers_mvv = {}
    for mvv in VV_MVV_GRID:
        cfg = {'N_fft': best_nfft, 'M_vv': mvv, 'omega_n': 8e6, 'zeta': np.sqrt(2)/2}
        bers = []
        for sd in seeds:
            sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
            bers.append(fixed_ber_with_cfg(sh, cfg))
        bers_mvv[mvv] = np.mean(bers)
        print(f"    M_vv={mvv:>4d}  BER={np.mean(bers):.6f}")
    best_mvv = min(bers_mvv, key=bers_mvv.get)
    print(f"    => best M_vv = {best_mvv} (BER={bers_mvv[best_mvv]:.6f})")

    # --- Step 3: sweep DPLL omega_n ---
    print(f"  D1 Step 3: scanning DPLL omega_n ({turb_name})")
    bers_omega = {}
    for omega in DPLL_OMEGA_GRID:
        cfg = {'N_fft': best_nfft, 'M_vv': best_mvv, 'omega_n': omega, 'zeta': np.sqrt(2)/2}
        bers = []
        for sd in seeds:
            sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
            bers.append(fixed_ber_with_cfg(sh, cfg))
        bers_omega[omega] = np.mean(bers)
        print(f"    omega_n={omega/1e6:>5.1f} MHz  BER={np.mean(bers):.6f}")
    best_omega = min(bers_omega, key=bers_omega.get)
    print(f"    => best omega_n = {best_omega/1e6:.1f} MHz (BER={bers_omega[best_omega]:.6f})")

    best_cfg = {'N_fft': best_nfft, 'M_vv': best_mvv, 'omega_n': best_omega, 'zeta': np.sqrt(2)/2}
    return best_cfg, bers_nfft, bers_mvv, bers_omega


def d1_kf_vs_optimal_fixed(turb_name, best_cfg):
    """Compare optimal Fixed vs KF pilot (n_pilots=5)."""
    seeds = range(N_SEEDS)
    bers_fixed = []
    bers_kf = []
    for sd in seeds:
        sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
        # Optimal Fixed
        rx_eq = equalize_oracle(sh)
        rx_fixed = carrier_recovery_fixed(rx_eq, cfg=best_cfg)
        bers_fixed.append(resolve_qpsk(rx_fixed, sh['bits']))
        # KF pilot
        corrected, data_idx, data_bits, _ = run_kf_pilot(sh, n_pilots=5, eq_mode='oracle')
        bers_kf.append(resolve_qpsk(corrected[data_idx], data_bits))

    return np.mean(bers_fixed), np.mean(bers_kf)


# ═══════════════════════════════════════════════════════════════
# D2: Gain attribution ablation
# ═══════════════════════════════════════════════════════════════
def d2_ablation_trial(shared):
    """Run all 5 ablation schemes on a single shared realization."""
    rx_eq = equalize_oracle(shared)
    N = len(rx_eq)
    k = np.arange(N)
    results = {}

    # 1) FOE only: FFT-based FOE, no VV/DPLL
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foe = rx_eq * np.exp(-1j * fo_est * k)
    results['FOE_only'] = resolve_qpsk(rx_foe, shared['bits'])

    # 2) FOE + VV
    fo_est2 = fft_foe(rx_eq, N_fft=1024)
    rx_foc2 = rx_eq * np.exp(-1j * fo_est2 * k)
    rx_vv, _ = vv_cpr(rx_foc2, Nw=64)
    results['FOE+VV'] = resolve_qpsk(rx_vv, shared['bits'])

    # 3) FOE + DPLL (use default best params)
    cfg_dpll = {'N_fft': 1024, 'M_vv': 64, 'omega_n': 8e6, 'zeta': np.sqrt(2)/2}
    fo_est3 = fft_foe(rx_eq, N_fft=cfg_dpll['N_fft'])
    rx_foc3 = rx_eq * np.exp(-1j * fo_est3 * k)
    rx_pll, _ = dpll_track(rx_foc3, omega_n=cfg_dpll['omega_n'], zeta=cfg_dpll['zeta'])
    results['FOE+DPLL'] = resolve_qpsk(rx_pll, shared['bits'])

    # 4) KF frame-level h (no pilots, use h_med)
    rx_kf_frame = run_kf_frame_h(shared, eq_mode='oracle')
    results['KF_frame'] = resolve_qpsk(rx_kf_frame, shared['bits'])

    # 5) KF pilot (full scheme, 5% pilots)
    corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots=5, eq_mode='oracle')
    results['KF_pilot'] = resolve_qpsk(corrected[data_idx], data_bits)

    return results


def d2_run(turb_name):
    """Run D2 ablation across seeds for one turbulence."""
    seeds = range(N_SEEDS)
    all_results = {s: [] for s in D2_SCHEMES}
    for sd in seeds:
        sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
        trial = d2_ablation_trial(sh)
        for s in D2_SCHEMES:
            all_results[s].append(trial[s])
    return {s: np.mean(v) for s, v in all_results.items()}


# ═══════════════════════════════════════════════════════════════
# Plotting
# ═══════════════════════════════════════════════════════════════
def plot_results(d1_data, d2_data, save_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    colors_turb = {'weak': '#2ecc71', 'moderate': '#f39c12', 'strong': '#e74c3c'}

    # --- D1 subplot: parameter sweep curves ---
    turb_list = list(d1_data.keys())
    n_turb = len(turb_list)

    # Sub-grids: 3 panels (N_fft, M_vv, omega_n)
    inner_gs = ax1.get_subplotspec()
    ax1.remove()
    sub_axes = fig.add_gridspec(1, 3, wspace=0.35,
                                 left=0.06, right=0.97, top=0.88, bottom=0.12)
    ax1a = fig.add_subplot(sub_axes[0, 0])
    ax1b = fig.add_subplot(sub_axes[0, 1])
    ax1c = fig.add_subplot(sub_axes[0, 2])

    for turb in turb_list:
        dd = d1_data[turb]
        c = colors_turb[turb]
        label = turb.capitalize()

        # N_fft scan
        nfft_vals = list(dd['bers_nfft'].keys())
        nfft_bers = [dd['bers_nfft'][v] for v in nfft_vals]
        ax1a.semilogy(nfft_vals, nfft_bers, 'o-', color=c, label=label, markersize=5)
        # mark best
        bi = np.argmin(nfft_bers)
        ax1a.plot(nfft_vals[bi], nfft_bers[bi], '*', color=c, markersize=12)

        # M_vv scan
        mvv_vals = list(dd['bers_mvv'].keys())
        mvv_bers = [dd['bers_mvv'][v] for v in mvv_vals]
        ax1b.semilogy(mvv_vals, mvv_bers, 's-', color=c, label=label, markersize=5)
        bi = np.argmin(mvv_bers)
        ax1b.plot(mvv_vals[bi], mvv_bers[bi], '*', color=c, markersize=12)

        # omega_n scan
        omega_vals_mhz = [v / 1e6 for v in dd['bers_omega'].keys()]
        omega_bers = list(dd['bers_omega'].values())
        ax1c.semilogy(omega_vals_mhz, omega_bers, '^-', color=c, label=label, markersize=5)
        bi = np.argmin(omega_bers)
        ax1c.plot(omega_vals_mhz[bi], omega_bers[bi], '*', color=c, markersize=12)

    ax1a.set_xlabel('FOE $N_{fft}$')
    ax1a.set_ylabel('BER')
    ax1a.set_title('(a) FOE FFT Length')
    ax1a.legend(fontsize=8)
    ax1a.grid(True, alpha=0.3)

    ax1b.set_xlabel('VV $M_{vv}$')
    ax1b.set_ylabel('BER')
    ax1b.set_title('(b) VV Window Length')
    ax1b.legend(fontsize=8)
    ax1b.grid(True, alpha=0.3)

    ax1c.set_xlabel('DPLL $\\omega_n$ (MHz)')
    ax1c.set_ylabel('BER')
    ax1c.set_title('(c) DPLL Bandwidth')
    ax1c.legend(fontsize=8)
    ax1c.grid(True, alpha=0.3)

    fig.suptitle('D1: Fixed Baseline Parameter Optimization (Sequential Search)',
                 fontsize=13, fontweight='bold', y=0.98)

    # --- D2 subplot: ablation bar chart ---
    x_pos = np.arange(len(D2_SCHEMES))
    bar_w = 0.25

    for i, turb in enumerate(turb_list):
        bers = [d2_data[turb][s] for s in D2_SCHEMES]
        ax2.bar(x_pos + i * bar_w, bers, bar_w,
                color=colors_turb[turb], label=turb.capitalize(), alpha=0.85,
                edgecolor='black', linewidth=0.5)

        # Annotate incremental gains
        for j in range(len(D2_SCHEMES)):
            if j > 0:
                delta = bers[j-1] - bers[j]
                if delta > 0:
                    ax2.annotate(f'-{delta:.4f}',
                                 xy=(x_pos[j] + i * bar_w, bers[j]),
                                 xytext=(0, -12), textcoords='offset points',
                                 ha='center', fontsize=6, color=colors_turb[turb])

    ax2.set_xticks(x_pos + bar_w)
    ax2.set_xticklabels(D2_SCHEMES, fontsize=9, rotation=15)
    ax2.set_ylabel('BER')
    ax2.set_title('D2: Gain Attribution Ablation', fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.set_yscale('log')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure saved: {save_path}")


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    json_out = {}

    # ---------- D1: parameter search ----------
    print("=" * 60)
    print("D1: Fixed Baseline Parameter Optimization")
    print("=" * 60)
    d1_data = {}
    d1_comparison = {}

    for turb in TURB_NAMES:
        print(f"\n--- {turb.upper()} turbulence ---")
        best_cfg, bers_nfft, bers_mvv, bers_omega = d1_sequential_search(turb)
        print(f"\n  Optimal Fixed config: {best_cfg}")

        ber_fixed_opt, ber_kf = d1_kf_vs_optimal_fixed(turb, best_cfg)
        gain_db = db_ratio(ber_fixed_opt, ber_kf)
        gain_ratio = ber_fixed_opt / ber_kf if ber_kf > 0 else float('inf')

        print(f"\n  Optimal Fixed BER:  {ber_fixed_opt:.6f}")
        print(f"  KF pilot BER:       {ber_kf:.6f}")
        print(f"  KF gain:            {gain_ratio:.3f}x ({gain_db:.2f} dB)")

        d1_data[turb] = {
            'best_cfg': best_cfg,
            'bers_nfft': {int(k): v for k, v in bers_nfft.items()},
            'bers_mvv': {int(k): v for k, v in bers_mvv.items()},
            'bers_omega': {float(k): v for k, v in bers_omega.items()},
        }
        d1_comparison[turb] = {
            'fixed_opt_ber': float(ber_fixed_opt),
            'kf_pilot_ber': float(ber_kf),
            'gain_ratio': float(gain_ratio),
            'gain_db': float(gain_db),
            'best_cfg': {k: (int(v) if isinstance(v, (np.integer,)) else
                             float(v) if isinstance(v, (np.floating,)) else v)
                         for k, v in best_cfg.items()},
        }

    # Default Fixed BER for reference
    print("\n--- Default Fixed reference ---")
    default_cfg = FIXED_CFG
    for turb in TURB_NAMES:
        bers = []
        for sd in range(N_SEEDS):
            sh = generate_shared_realization(NS, GAMMA_BAR, turb, DOPPLER_HIGH, seed=sd)
            bers.append(fixed_ber_with_cfg(sh, default_cfg))
        d1_comparison[turb]['default_fixed_ber'] = float(np.mean(bers))
        d1_comparison[turb]['default_cfg'] = {k: (int(v) if isinstance(v, (np.integer,)) else
                                                    float(v) if isinstance(v, (np.floating,)) else v)
                                               for k, v in default_cfg.items()}
        print(f"  {turb}: default Fixed BER = {np.mean(bers):.6f}, "
              f"optimal Fixed BER = {d1_comparison[turb]['fixed_opt_ber']:.6f}, "
              f"improvement = {d1_comparison[turb]['default_fixed_ber']/d1_comparison[turb]['fixed_opt_ber']:.3f}x")

    # ---------- D2: ablation ----------
    print("\n" + "=" * 60)
    print("D2: Gain Attribution Ablation")
    print("=" * 60)
    d2_data = {}

    for turb in TURB_NAMES:
        print(f"\n--- {turb.upper()} turbulence ---")
        d2_data[turb] = d2_run(turb)
        for scheme in D2_SCHEMES:
            print(f"  {scheme:>12s}: BER = {d2_data[turb][scheme]:.6f}")

    # ---------- Save JSON ----------
    json_out['D1_sequential_search'] = d1_data
    json_out['D1_comparison'] = d1_comparison
    json_out['D2_ablation'] = d2_data
    json_out['meta'] = {
        'N_seeds': N_SEEDS, 'Ns': NS, 'gamma_bar': GAMMA_BAR,
        'turbulence': TURB_NAMES, 'f_dot': DOPPLER_HIGH,
    }

    json_path = os.path.join(OUT, 'results_kf_stress_D1D2.json')
    with open(json_path, 'w') as f:
        json.dump(json_out, f, indent=2, default=str)
    print(f"\nJSON saved: {json_path}")

    # ---------- Plot ----------
    fig_path = os.path.join(OUT, 'fig_kf_stress_D1D2.png')
    plot_results(d1_data, d2_data, fig_path)

    # ---------- Summary ----------
    elapsed = time.time() - t0
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Elapsed: {elapsed:.1f}s\n")

    print("D1: Fixed Baseline Fairness")
    print("-" * 40)
    for turb in TURB_NAMES:
        dc = d1_comparison[turb]
        print(f"  {turb:>10s}:")
        print(f"    Default Fixed BER: {dc['default_fixed_ber']:.6f}")
        print(f"    Optimal Fixed BER: {dc['fixed_opt_ber']:.6f} "
              f"(cfg: N_fft={dc['best_cfg']['N_fft']}, M_vv={dc['best_cfg']['M_vv']}, "
              f"omega_n={dc['best_cfg']['omega_n']/1e6:.1f}MHz)")
        print(f"    KF pilot BER:      {dc['kf_pilot_ber']:.6f}")
        print(f"    KF gain over opt:  {dc['gain_ratio']:.3f}x ({dc['gain_db']:.2f} dB)")

    print(f"\nD2: Incremental Gain Attribution")
    print("-" * 40)
    for turb in TURB_NAMES:
        print(f"  {turb:>10s}:")
        prev = None
        for s in D2_SCHEMES:
            ber = d2_data[turb][s]
            delta = f"  (delta={prev - ber:.5f})" if prev is not None and prev > ber else ""
            print(f"    {s:>12s}: {ber:.6f}{delta}")
            prev = ber

    # Key question
    print("\n" + "=" * 60)
    print("KEY QUESTION: How much KF gain remains with optimal Fixed?")
    print("=" * 60)
    for turb in TURB_NAMES:
        dc = d1_comparison[turb]
        opt_improvement = dc['default_fixed_ber'] / dc['fixed_opt_ber']
        kf_residual = dc['gain_ratio']
        print(f"  {turb}: Opt Fixed improves default by {opt_improvement:.2f}x; "
              f"KF still provides {kf_residual:.2f}x gain over optimal Fixed "
              f"({dc['gain_db']:.2f} dB)")
