#!/usr/bin/env python3
"""Bridge experiment: Ch3→Ch4 — Channel estimation error impact on carrier sync BER.

Question: At what NMSE level can carrier sync tolerate channel estimation error?

Uses new common.py (corrected VV formula). Tests FOE+VV, FOE+DPLL, Fixed (FOE+DPLL+VV).
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
NS = 10000
GAMMA_BAR = GAMMA_BAR_DEFAULT  # 100 (20 dB)
NMSE_DB = [None, -5, -10, -15, -20]
NMSE_LABELS = ['oracle', '-5dB', '-10dB', '-15dB', '-20dB']
SCHEMES = ['FOE+VV', 'FOE+DPLL', 'Fixed']
DEGRADE_THRESH_DB = 1.0


def noisy_h(h_true, nmse_db, seed):
    """Generate noisy channel estimate. h is real-valued irradiance."""
    if nmse_db is None:
        return h_true.copy()
    rng = np.random.RandomState(seed)
    nmse = 10 ** (nmse_db / 10)
    h_hat = h_true + np.sqrt(nmse) * rng.randn(len(h_true))
    return np.maximum(h_hat, 0.01)


def run_trial(shared, h_hat, scheme):
    """Run single scheme with given h_hat for equalization."""
    rx_eq = amp_limit(mmse_equalize(shared['rx_raw'], h_hat, shared['gamma_bar']), 3.0)
    N = len(rx_eq)
    k = np.arange(N)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)

    if scheme == 'FOE+VV':
        rx_out, _ = vv_cpr(rx_foc, Nw=64)
    elif scheme == 'FOE+DPLL':
        rx_out, _ = dpll_track(rx_foc, omega_n=8e6, zeta=np.sqrt(2)/2)
    elif scheme == 'Fixed':
        rx_pll, _ = dpll_track(rx_foc, omega_n=8e6, zeta=np.sqrt(2)/2)
        rx_out, _ = vv_cpr(rx_pll, Nw=64)

    return resolve_qpsk(rx_out, shared['bits'])


def main():
    t0 = time.time()
    print("=" * 70)
    print("BRIDGE EXPERIMENT: Ch3->Ch4 Channel Estimation Error Impact")
    print("=" * 70)
    print(f"Methods: {SCHEMES}")
    print(f"NMSE levels: {NMSE_LABELS}")
    print(f"Seeds: {N_SEEDS}, Ns: {NS}, gamma_bar: {GAMMA_BAR} ({10*np.log10(GAMMA_BAR):.0f} dB)")
    print()

    results = {}

    for turb in TURB_NAMES:
        print(f"\n{'─'*50}")
        print(f"  {turb.upper()} turbulence")
        print(f"{'─'*50}")
        results[turb] = {}

        # Oracle baseline
        oracle_bers = {s: [] for s in SCHEMES}
        for sd in range(N_SEEDS):
            shared = generate_shared_realization(NS, GAMMA_BAR, turb, DOPPLER_HIGH, seed=sd)
            for s in SCHEMES:
                oracle_bers[s].append(run_trial(shared, shared['h'], s))

        oracle_means = {s: float(np.mean(v)) for s, v in oracle_bers.items()}
        results[turb]['oracle'] = {
            s: {'mean': oracle_means[s], 'values': [float(v) for v in oracle_bers[s]]}
            for s in SCHEMES
        }
        print(f"  {'oracle':>8s}: " + "  ".join(f"{s}={oracle_means[s]:.6f}" for s in SCHEMES))

        # Sweep NMSE levels
        for nmse_db, nmse_lbl in zip(NMSE_DB[1:], NMSE_LABELS[1:]):
            bers = {s: [] for s in SCHEMES}
            for sd in range(N_SEEDS):
                shared = generate_shared_realization(NS, GAMMA_BAR, turb, DOPPLER_HIGH, seed=sd)
                h_hat = noisy_h(shared['h'], nmse_db, seed=sd + 10000)
                for s in SCHEMES:
                    bers[s].append(run_trial(shared, h_hat, s))

            means = {s: float(np.mean(v)) for s, v in bers.items()}
            degrade = {s: float(db_ratio(means[s], oracle_means[s])) for s in SCHEMES}

            results[turb][nmse_lbl] = {
                s: {'mean': means[s], 'degrade_db': degrade[s],
                    'values': [float(v) for v in bers[s]]}
                for s in SCHEMES
            }

            print(f"  {nmse_lbl:>8s}: " + "  ".join(
                f"{s}={means[s]:.4e}(Δ{degrade[s]:+.1f}dB)"
                for s in SCHEMES))

    # ─── Safe threshold analysis ───
    print(f"\n{'='*70}")
    print("SAFE THRESHOLD (BER degradation < 1 dB vs oracle)")
    print(f"{'='*70}")

    safe_thresholds = {}
    for turb in TURB_NAMES:
        safe_thresholds[turb] = {}
        for s in SCHEMES:
            threshold = None
            for nmse_db, nmse_lbl in zip(NMSE_DB[1:], NMSE_LABELS[1:]):
                if results[turb][nmse_lbl][s]['degrade_db'] < DEGRADE_THRESH_DB:
                    threshold = nmse_lbl
                    break
            safe_thresholds[turb][s] = threshold
            print(f"  {turb:>8s}/{s:12s}: safe at NMSE >= {threshold or 'NONE'}")

    # ─── Save results ───
    out_dir = os.path.join(OUT, 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'bridge_ch3_ch4_results.json')
    with open(out_path, 'w') as f:
        json.dump({
            'results': results,
            'safe_thresholds': safe_thresholds,
            'meta': {
                'N_seeds': N_SEEDS, 'Ns': NS, 'gamma_bar': GAMMA_BAR,
                'degrade_thresh_db': DEGRADE_THRESH_DB,
                'nmse_levels': NMSE_LABELS,
                'schemes': SCHEMES,
                'note': 'Bridge Ch3->Ch4: channel estimation error impact on carrier sync BER'
            }
        }, f, indent=2, default=str)
    print(f"\nResults saved: {out_path}")

    # ─── Plot ───
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    x_ticks = list(range(len(NMSE_LABELS)))
    markers = {'FOE+VV': 'o-', 'FOE+DPLL': 's-', 'Fixed': '^-'}

    for idx, turb in enumerate(TURB_NAMES):
        ax = axes[idx]
        for s in SCHEMES:
            bers = [results[turb][lbl][s]['mean'] for lbl in NMSE_LABELS]
            ax.semilogy(x_ticks, bers, markers[s], label=s, ms=6, lw=1.5)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(NMSE_LABELS, fontsize=8)
        ax.set_xlabel('h estimation NMSE')
        if idx == 0:
            ax.set_ylabel('BER')
        ax.set_title(f'{turb.capitalize()} turbulence')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.suptitle('Carrier Sync BER vs Channel Estimation Error ($\\bar{\\gamma}$=20dB)', fontsize=12)
    plt.tight_layout()
    fig_path = os.path.join(OUT, 'figs', 'fig_bridge_ber_vs_nmse.png')
    os.makedirs(os.path.dirname(fig_path), exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Figure saved: {fig_path}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
