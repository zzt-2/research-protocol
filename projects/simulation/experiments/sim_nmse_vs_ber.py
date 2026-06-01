#!/usr/bin/env python3
"""NMSE vs BER curve for Ch3 — channel estimation error impact on carrier recovery BER.

Sweeps NMSE of channel estimate from -25 dB to 0 dB, measures resulting BER
after MMSE equalization with noisy h + carrier recovery.

Uses new common.py (corrected VV formula). Methods: DPLL, VV, Fixed, KF_pilot.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import json

# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════
TURB_NAMES = ['weak', 'moderate', 'strong']
N_SEEDS = 10
SEEDS = list(range(1000, 1000 + N_SEEDS))
NS = 50000
GAMMA_BAR = GAMMA_BAR_DEFAULT  # 100 (20 dB)
F_DOT = DOPPLER_HIGH

NMSE_DB = [-25, -22, -20, -18, -15, -12, -10, -8, -5, -3, 0]

SCHEMES = ['DPLL', 'VV', 'Fixed', 'KF_pilot']

BER_FLOOR = 1e-7  # replace BER=0 for log axis


def noisy_h_multiplicative(h_true_blocks, nmse_db, rng):
    """Generate noisy per-block channel estimate with multiplicative error.

    h_hat = h * (1 + n_I + j*n_Q), where n_I,n_Q ~ N(0, sqrt(NMSE)).
    Takes |h_hat| to keep real-valued irradiance.
    """
    noise_power = 10 ** (nmse_db / 10)
    sigma = np.sqrt(noise_power)
    n_real = rng.randn(len(h_true_blocks))
    n_imag = rng.randn(len(h_true_blocks))
    h_noisy = h_true_blocks * (1 + sigma * n_real + 1j * sigma * n_imag)
    return np.abs(h_noisy)


def run_non_pilot_method(rx_eq, scheme, bits, cfg_optimal=None):
    """Run DPLL/VV/Fixed on equalized signal, return BER (oracle mode)."""
    N = len(rx_eq)
    k = np.arange(N)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)

    if scheme == 'DPLL':
        rx_out, _ = dpll_track(rx_foc, omega_n=20e6)
    elif scheme == 'VV':
        rx_out, _ = vv_cpr(rx_foc, Nw=256)
    elif scheme == 'Fixed':
        if cfg_optimal is not None:
            rx_pll, _ = dpll_track(rx_foc, omega_n=cfg_optimal['omega_n'],
                                   zeta=cfg_optimal['zeta'])
            rx_out, _ = vv_cpr(rx_pll, Nw=cfg_optimal['M_vv'])
        else:
            rx_pll, _ = dpll_track(rx_foc, omega_n=20e6)
            rx_out, _ = vv_cpr(rx_pll, Nw=256)
    else:
        raise ValueError(f"Unknown non-pilot scheme: {scheme}")

    return resolve_qpsk(rx_out, bits)


def run_kf_pilot_method(shared, h_noisy_blocks, gamma_bar, turb_name):
    """Run KF pilot with noisy h estimate, return BER on data symbols."""
    n_pilots = 5
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)

    # Expand noisy per-block h to per-symbol for equalization
    block_size = NS // len(h_noisy_blocks)
    h_noisy_per_symbol = np.repeat(h_noisy_blocks, block_size)
    # Trim to actual length (Ns may not divide evenly)
    h_noisy_per_symbol = h_noisy_per_symbol[:NS]

    rx_eq = amp_limit(mmse_equalize(rx_pilot, h_noisy_per_symbol, gamma_bar), 3.0)

    # KF pilot uses h_med from shared (original), not noisy h
    # The noisy h only affects equalization
    corrected, _ = kf_pilot_recovery(
        rx_eq, gamma_bar, turb_name, n_pilots,
        shared['h_med'], F_DOT)

    ber = resolve_qpsk(corrected[data_idx], data_bits)
    return ber


def main():
    t0 = time.time()
    print("=" * 70)
    print("NMSE vs BER: Channel estimation error impact on carrier recovery")
    print("=" * 70)
    print(f"Methods: {SCHEMES}")
    print(f"NMSE sweep: {NMSE_DB} dB")
    print(f"Seeds: {SEEDS[0]}..{SEEDS[-1]} ({N_SEEDS}), Ns: {NS}")
    print(f"SNR: {10*np.log10(GAMMA_BAR):.0f} dB")
    print()

    results = {}

    for turb in TURB_NAMES:
        print(f"\n{'─'*60}")
        print(f"  {turb.upper()} turbulence")
        print(f"{'─'*60}")
        results[turb] = {}
        cfg_opt = FIXED_CFG_OPTIMAL[turb]

        # ── Oracle baseline (perfect h) ──
        oracle_bers = {s: [] for s in SCHEMES}
        for sd in SEEDS:
            shared = generate_shared_realization(NS, GAMMA_BAR, turb, F_DOT, seed=sd)

            # Non-pilot methods with oracle h
            rx_eq_oracle = equalize_oracle(shared)
            for s in ['DPLL', 'VV', 'Fixed']:
                oracle_bers[s].append(run_non_pilot_method(rx_eq_oracle, s,
                                                            shared['bits'], cfg_opt))
            # KF pilot with oracle h
            oracle_bers['KF_pilot'].append(
                run_kf_pilot_method(shared, shared['h_blocks'], GAMMA_BAR, turb))

        oracle_means = {s: float(np.mean(v)) for s, v in oracle_bers.items()}
        results[turb]['oracle'] = {
            s: {'mean': oracle_means[s],
                'values': [float(v) for v in oracle_bers[s]]}
            for s in SCHEMES
        }
        print(f"  {'oracle':>8s}: " +
              "  ".join(f"{s}={oracle_means[s]:.6f}" for s in SCHEMES))

        # ── NMSE sweep ──
        for nmse_db in NMSE_DB:
            bers = {s: [] for s in SCHEMES}
            for sd in SEEDS:
                shared = generate_shared_realization(NS, GAMMA_BAR, turb, F_DOT, seed=sd)
                h_true_blocks = shared['h_blocks']

                # Generate noisy h (multiplicative model)
                rng = np.random.RandomState(sd + 50000)
                h_noisy_blocks = noisy_h_multiplicative(h_true_blocks, nmse_db, rng)

                # Expand per-block noisy h to per-symbol
                block_size = NS // len(h_true_blocks)
                h_noisy_per_symbol = np.repeat(h_noisy_blocks, block_size)[:NS]

                # MMSE equalize with noisy h
                rx_eq = amp_limit(mmse_equalize(shared['rx_raw'], h_noisy_per_symbol,
                                                 GAMMA_BAR), 3.0)

                # Non-pilot methods
                for s in ['DPLL', 'VV', 'Fixed']:
                    bers[s].append(run_non_pilot_method(rx_eq, s,
                                                        shared['bits'], cfg_opt))

                # KF pilot — needs its own equalization path (insert_pilots changes rx)
                bers['KF_pilot'].append(
                    run_kf_pilot_method(shared, h_noisy_blocks, GAMMA_BAR, turb))

            means = {s: max(float(np.mean(v)), BER_FLOOR) for s, v in bers.items()}
            results[turb][f'nmse_{nmse_db}'] = {
                s: {'mean': means[s],
                    'values': [float(v) for v in bers[s]]}
                for s in SCHEMES
            }

            degrade = {s: float(db_ratio(means[s], oracle_means[s]))
                       for s in SCHEMES}
            print(f"  {nmse_db:>4d} dB: " +
                  "  ".join(f"{s}={means[s]:.4e}(Δ{degrade[s]:+.1f}dB)"
                            for s in SCHEMES))

    # ─── Save JSON results ───
    out_dir = os.path.join(OUT, 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'nmse_vs_ber.json')
    with open(out_path, 'w') as f:
        json.dump({
            'results': results,
            'meta': {
                'N_seeds': N_SEEDS, 'seeds': SEEDS, 'Ns': NS,
                'gamma_bar': GAMMA_BAR, 'f_dot': F_DOT,
                'nmse_levels_db': NMSE_DB,
                'schemes': SCHEMES,
                'turbulence': TURB_NAMES,
                'note': 'Ch3: NMSE vs BER — channel estimation error impact on carrier recovery'
            }
        }, f, indent=2)
    print(f"\nResults saved: {out_path}")

    # ─── Plot ───
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    markers = {'DPLL': 'o-', 'VV': 's-', 'Fixed': '^-', 'KF_pilot': 'D-'}
    colors = {'DPLL': '#1f77b4', 'VV': '#ff7f0e', 'Fixed': '#2ca02c',
              'KF_pilot': '#d62728'}

    for idx, turb in enumerate(TURB_NAMES):
        ax = axes[idx]
        turb_title = {'weak': 'Weak', 'moderate': 'Moderate', 'strong': 'Strong'}

        for s in SCHEMES:
            bers = [results[turb]['oracle'][s]['mean']]
            for nmse_db in NMSE_DB:
                val = results[turb][f'nmse_{nmse_db}'][s]['mean']
                bers.append(max(val, BER_FLOOR))

            # Plot oracle as leftmost point (NMSE=-30 as proxy for "perfect")
            x_plot = [-30] + NMSE_DB
            ax.semilogy(x_plot, bers, markers[s], label=s, lw=1.5,
                        color=colors[s], ms=4)

        ax.set_xlabel('Channel estimation NMSE (dB)', fontsize=10)
        if idx == 0:
            ax.set_ylabel('BER', fontsize=10)
        ax.set_title(f'{turb_title[turb]} turbulence', fontsize=11)
        ax.legend(fontsize=8, loc='upper left')
        ax.grid(True, alpha=0.3, which='both')
        ax.set_xlim(-32, 2)
        # Add vertical line separating oracle region
        ax.axvline(x=-27, color='gray', linestyle=':', alpha=0.5)
        ax.text(-29, ax.get_ylim()[1] * 0.5, 'Oracle', fontsize=7,
                color='gray', ha='center', rotation=90)

    plt.suptitle('Carrier Recovery BER vs Channel Estimation Error '
                 '($\\bar{\\gamma}$=20 dB)', fontsize=12, y=1.02)
    plt.tight_layout()

    # Save to both locations
    fig_dir_sim = os.path.join(OUT, 'figures')
    os.makedirs(fig_dir_sim, exist_ok=True)
    fig_path_sim = os.path.join(fig_dir_sim, 'nmse_vs_ber.pdf')
    plt.savefig(fig_path_sim, dpi=150, bbox_inches='tight')

    thesis_fig_dir = os.path.join(os.path.dirname(os.path.dirname(OUT)),
                                   '毕设', '写作材料', 'figures')
    os.makedirs(thesis_fig_dir, exist_ok=True)
    fig_path_thesis = os.path.join(thesis_fig_dir, 'nmse_vs_ber.pdf')
    plt.savefig(fig_path_thesis, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Figure saved: {fig_path_sim}")
    print(f"Figure saved: {fig_path_thesis}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
