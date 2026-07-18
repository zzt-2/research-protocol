#!/usr/bin/env python3
"""NMSE turbulence sweep: 3 turbulence levels x 2 noise models x multi-SNR.

Tests whether channel estimation error (NMSE) affects carrier recovery BER
consistently across weak, moderate, and strong turbulence.

Theoretical expectation (TL-20): NMSE impact on BER < 0.3 dB regardless of
turbulence intensity. MMSE weight W = sqrt(h)/(h+c) > 0 for all h > 0,
so QPSK sign(Re/Im) decision is immune to positive scaling.

Noise models:
  A: Multiplicative amplitude — h_noisy = |h*(1+noise)|, always real
  B: Additive — h_noisy = |h + sigma*|h|*noise|, may go negative near fades
  (Model C skipped — physically implausible, confirmed by TL-22)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import json

# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════
TURB_LEVELS = ['weak', 'moderate', 'strong']
NOISE_MODELS = ['A', 'B']
METHODS = ['DPLL', 'VV']

N_SEEDS = 10
SEEDS = list(range(1000, 1000 + N_SEEDS))
NS = 50000
F_DOT = DOPPLER_HIGH

SNR_DB = [0, 5, 10, 15, 20]
GAMMA_BARS = [10 ** (s / 10) for s in SNR_DB]

NMSE_DB = [-20, -10, -5, 0]

BER_FLOOR = 1e-7

# ═══════════════════════════════════════════════════════════════
# Noise models (A and B only — C is physically implausible per TL-22)
# ═══════════════════════════════════════════════════════════════

def noisy_model_A(h_true_blocks, nmse_db, rng):
    """Multiplicative amplitude: h_noisy = |h*(1+noise)|"""
    sigma = np.sqrt(10 ** (nmse_db / 10))
    n_real = rng.randn(len(h_true_blocks))
    n_imag = rng.randn(len(h_true_blocks))
    h_noisy = h_true_blocks * (1 + sigma * n_real + 1j * sigma * n_imag)
    return np.abs(h_noisy)


def noisy_model_B(h_true_blocks, nmse_db, rng):
    """Additive: h_noisy = |h + sigma*|h|*noise|"""
    sigma = np.sqrt(10 ** (nmse_db / 10))
    n_real = rng.randn(len(h_true_blocks))
    n_imag = rng.randn(len(h_true_blocks))
    h_abs = np.abs(h_true_blocks)
    h_noisy = h_true_blocks + sigma * h_abs * n_real + 1j * sigma * h_abs * n_imag
    return np.abs(h_noisy)


NOISE_MODEL_FNS = {
    'A': noisy_model_A,
    'B': noisy_model_B,
}


# ═══════════════════════════════════════════════════════════════
# Method runners
# ═══════════════════════════════════════════════════════════════

def run_dpll(rx_eq, bits):
    N = len(rx_eq)
    k = np.arange(N)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_out, _ = dpll_track(rx_foc, omega_n=20e6)
    return resolve_qpsk(rx_out, bits)


def run_vv(rx_eq, bits):
    N = len(rx_eq)
    k = np.arange(N)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_out, _ = vv_cpr(rx_foc, Nw=256)
    return resolve_qpsk(rx_out, bits)


METHOD_FNS = {
    'DPLL': lambda rx_eq, shared, h_noisy, gb: run_dpll(rx_eq, shared['bits']),
    'VV':    lambda rx_eq, shared, h_noisy, gb: run_vv(rx_eq, shared['bits']),
}


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    print("=" * 70)
    print("NMSE Turbulence Sweep: 3 turb levels x 2 noise models x multi-SNR")
    print("=" * 70)
    print(f"Turbulence levels: {TURB_LEVELS}")
    print(f"SNR: {SNR_DB} dB")
    print(f"NMSE: {NMSE_DB} dB")
    print(f"Methods: {METHODS}")
    print(f"Noise models: {NOISE_MODELS}  (A=multiplicative, B=additive)")
    print(f"Seeds: {SEEDS[0]}..{SEEDS[-1]} ({N_SEEDS}), Ns: {NS}")
    print()

    # results[turb][snr_db][model][nmse_db][method] = {mean, values}
    # results[turb][snr_db]['oracle'][method] = {mean, values}
    results = {}

    for turb_name in TURB_LEVELS:
        print(f"\n{'#'*70}")
        print(f"# TURBULENCE: {turb_name}  (a={TURB[turb_name][0]}, b={TURB[turb_name][1]})")
        print(f"{'#'*70}")
        results[turb_name] = {}

        for snr_db, gamma_bar in zip(SNR_DB, GAMMA_BARS):
            print(f"\n  {'='*56}")
            print(f"  SNR = {snr_db} dB (gamma_bar = {gamma_bar:.2f}), turb = {turb_name}")
            print(f"  {'='*56}")
            results[turb_name][snr_db] = {}

            # -- Oracle baselines (perfect h) --
            oracle_bers = {m: [] for m in METHODS}
            for sd in SEEDS:
                shared = generate_shared_realization(NS, gamma_bar, turb_name, F_DOT, seed=sd)
                rx_eq_oracle = equalize_oracle(shared)
                for m in METHODS:
                    oracle_bers[m].append(METHOD_FNS[m](rx_eq_oracle, shared, None, gamma_bar))

            oracle_means = {m: float(np.mean(v)) for m, v in oracle_bers.items()}
            results[turb_name][snr_db]['oracle'] = {
                m: {'mean': oracle_means[m], 'values': [float(x) for x in oracle_bers[m]]}
                for m in METHODS
            }
            print(f"  oracle: " + "  ".join(f"{m}={oracle_means[m]:.2e}" for m in METHODS))

            # -- Noise model sweep --
            for model in NOISE_MODELS:
                results[turb_name][snr_db][model] = {}
                noise_fn = NOISE_MODEL_FNS[model]

                for nmse_db in NMSE_DB:
                    bers = {m: [] for m in METHODS}

                    for sd in SEEDS:
                        shared = generate_shared_realization(NS, gamma_bar, turb_name,
                                                              F_DOT, seed=sd)
                        h_true_blocks = shared['h_blocks']
                        rng = np.random.RandomState(sd + 50000)
                        h_noisy_blocks = noise_fn(h_true_blocks, nmse_db, rng)

                        h_noisy_per_sym = np.repeat(h_noisy_blocks, BLOCK)[:NS]
                        rx_eq = amp_limit(
                            mmse_equalize(shared['rx_raw'], h_noisy_per_sym, gamma_bar), 3.0)

                        for m in METHODS:
                            bers[m].append(METHOD_FNS[m](rx_eq, shared, h_noisy_blocks, gamma_bar))

                    means = {m: max(float(np.mean(v)), BER_FLOOR) for m, v in bers.items()}
                    degrade = {m: float(db_ratio(means[m], oracle_means[m])) for m in METHODS}

                    results[turb_name][snr_db][model][nmse_db] = {
                        m: {'mean': means[m], 'values': [float(x) for x in bers[m]]}
                        for m in METHODS
                    }

                    tag = f"    model {model} NMSE={nmse_db:>3d}dB: "
                    tag += "  ".join(f"{m}={means[m]:.2e}(D{degrade[m]:+.1f}dB)"
                                    for m in METHODS)
                    print(tag)

    # -- Check for unexpected degradations (>1 dB) --
    print(f"\n{'='*70}")
    print("DEGRADATION CHECK (expectation: all < 0.5 dB)")
    print(f"{'='*70}")
    max_degrade_found = 0.0
    for turb_name in TURB_LEVELS:
        for snr_db in SNR_DB:
            oracle = results[turb_name][snr_db]['oracle']
            for model in NOISE_MODELS:
                for nmse_db in NMSE_DB:
                    for m in METHODS:
                        mean_ber = results[turb_name][snr_db][model][nmse_db][m]['mean']
                        d = float(db_ratio(mean_ber, oracle[m]['mean']))
                        max_degrade_found = max(max_degrade_found, d)
                        if abs(d) > 1.0:
                            print(f"  WARNING: {turb_name}/SNR={snr_db}/{model}/"
                                  f"NMSE={nmse_db}/{m}: D={d:+.2f} dB (>1 dB!)")
    print(f"  Max degradation across all conditions: {max_degrade_found:+.2f} dB")
    if max_degrade_found > 0.5:
        print("  *** Degradation exceeds 0.5 dB threshold — investigate! ***")

    # --- Save JSON ---
    out_dir = os.path.join(OUT, 'results')
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, 'nmse_turbulence_sweep.json')
    with open(json_path, 'w') as f:
        json.dump({
            'results': results,
            'meta': {
                'N_seeds': N_SEEDS, 'seeds': SEEDS, 'Ns': NS,
                'snr_db': SNR_DB, 'gamma_bars': [float(g) for g in GAMMA_BARS],
                'nmse_levels_db': NMSE_DB,
                'methods': METHODS,
                'noise_models': NOISE_MODELS,
                'turbulence_levels': TURB_LEVELS,
                'f_dot': F_DOT,
                'note': 'NMSE turbulence sweep: 3 turb levels x 2 noise models',
            }
        }, f, indent=2)
    print(f"\nJSON saved: {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plot: BER vs SNR — 3 rows (turbulence) x 2 columns (noise models)
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(3, 2, figsize=(14, 13), sharey=True)
    method_styles = {'DPLL': ('o', '#1f77b4'), 'VV': ('s', '#ff7f0e')}
    nmse_colors = {-20: '#2ca02c', -10: '#1f77b4', -5: '#ff7f0e', 0: '#d62728'}
    nmse_ls = {-20: ':', -10: '--', -5: '-.', 0: '-'}
    nmse_lw = {-20: 1.0, -10: 1.2, -5: 1.5, 0: 2.0}
    turb_labels = {'weak': 'Weak turbulence (a=4.0, b=3.0)',
                   'moderate': 'Moderate turbulence (a=2.5, b=1.8)',
                   'strong': 'Strong turbulence (a=1.5, b=0.8)'}
    model_labels = {'A': 'Model A: Multiplicative', 'B': 'Model B: Additive'}

    for row_idx, turb_name in enumerate(TURB_LEVELS):
        for col_idx, model in enumerate(NOISE_MODELS):
            ax = axes[row_idx, col_idx]

            # Oracle lines
            for m in METHODS:
                oracle_ber = [max(results[turb_name][s]['oracle'][m]['mean'], BER_FLOOR)
                              for s in SNR_DB]
                mk, col = method_styles[m]
                ax.semilogy(SNR_DB, oracle_ber, mk, color=col, lw=2.5, ms=7,
                            label=f'{m} (oracle)' if row_idx == 0 and col_idx == 0 else '',
                            alpha=0.8)

            # NMSE lines
            for nmse in NMSE_DB:
                for m in METHODS:
                    bers = [max(results[turb_name][s][model][nmse][m]['mean'], BER_FLOOR)
                            for s in SNR_DB]
                    mk, _ = method_styles[m]
                    ax.semilogy(SNR_DB, bers, mk, color=nmse_colors[nmse],
                                ls=nmse_ls[nmse], lw=nmse_lw[nmse], ms=4, alpha=0.85,
                                label=f'{m} NMSE={nmse}dB'
                                if row_idx == 0 and col_idx == 0 else '')

            ax.set_xlabel('SNR (dB)', fontsize=9)
            if col_idx == 0:
                ax.set_ylabel('BER', fontsize=9)
            if row_idx == 0:
                ax.set_title(model_labels[model], fontsize=10)
            # Row label on right
            if col_idx == 1:
                ax.annotate(turb_labels[turb_name], xy=(1.02, 0.5),
                            xycoords='axes fraction', rotation=270,
                            va='center', ha='left', fontsize=9)
            ax.grid(True, alpha=0.3, which='both')
            ax.set_ylim(bottom=1e-7)

    # Compact legend
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=7,
               bbox_to_anchor=(0.5, -0.03))

    plt.suptitle('BER vs SNR under Channel Estimation Error — Turbulence Sweep',
                 fontsize=12, y=1.01)
    plt.tight_layout()

    fig_dir_sim = os.path.join(OUT, 'figures')
    os.makedirs(fig_dir_sim, exist_ok=True)
    fig_path_sim = os.path.join(fig_dir_sim, 'nmse_turbulence_sweep.pdf')
    plt.savefig(fig_path_sim, dpi=150, bbox_inches='tight')

    thesis_fig_dir = os.path.join(os.path.dirname(os.path.dirname(OUT)),
                                   '毕设', '写作材料', 'figures')
    os.makedirs(thesis_fig_dir, exist_ok=True)
    fig_path_thesis = os.path.join(thesis_fig_dir, 'nmse_turbulence_sweep.pdf')
    plt.savefig(fig_path_thesis, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure saved: {fig_path_sim}")
    print(f"Figure saved: {fig_path_thesis}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
