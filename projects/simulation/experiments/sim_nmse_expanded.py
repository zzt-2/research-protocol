#!/usr/bin/env python3
"""NMSE expanded verification: 3 noise models x multi-SNR x 3 methods.

Tests whether channel estimation error (NMSE) affects carrier recovery BER
under different noise models:
  A: Multiplicative amplitude (existing) — h_noisy = |h*(1+noise)|, always real
  B: Additive — h_noisy = |h + sigma*|h|*noise|, may go negative near fades
  C: Complex (no abs) — h_noisy = h*(1+noise), complex-valued -> W becomes complex

Key question: Model C makes MMSE weight W complex. Does the resulting phase
rotation from equalization corrupt carrier recovery?
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import json

# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════
TURB_NAME = 'moderate'
N_SEEDS = 10
SEEDS = list(range(1000, 1000 + N_SEEDS))
NS = 50000
F_DOT = DOPPLER_HIGH

SNR_DB = [0, 5, 10, 15, 20]
GAMMA_BARS = [10 ** (s / 10) for s in SNR_DB]

NMSE_DB = [-20, -10, -5, 0]

METHODS = ['DPLL', 'VV', 'KF_pilot']
NOISE_MODELS = ['A', 'B', 'C']

BER_FLOOR = 1e-7

# ═══════════════════════════════════════════════════════════════
# Noise models
# ═══════════════════════════════════════════════════════════════

def noisy_model_A(h_true_blocks, nmse_db, rng):
    """Multiplicative amplitude (existing): h_noisy = |h*(1+noise)|"""
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


def noisy_model_C(h_true_blocks, nmse_db, rng):
    """Complex (no abs): h_noisy = h*(1+noise), complex-valued."""
    sigma = np.sqrt(10 ** (nmse_db / 10))
    n_real = rng.randn(len(h_true_blocks))
    n_imag = rng.randn(len(h_true_blocks))
    return h_true_blocks * (1 + sigma * n_real + 1j * sigma * n_imag)


NOISE_MODEL_FNS = {
    'A': noisy_model_A,
    'B': noisy_model_B,
    'C': noisy_model_C,
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


def run_kf_pilot_nmse(shared, h_noisy_blocks, gamma_bar):
    """KF pilot with noisy h affecting only MMSE equalization."""
    n_pilots = 5
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)

    n_blocks = NS // BLOCK
    h_noisy_per_symbol = np.repeat(h_noisy_blocks, BLOCK)[:NS]

    rx_eq = amp_limit(mmse_equalize(rx_pilot, h_noisy_per_symbol, gamma_bar), 3.0)

    corrected, _ = kf_pilot_recovery(
        rx_eq, gamma_bar, TURB_NAME, n_pilots,
        shared['h_med'], F_DOT)

    return resolve_qpsk(corrected[data_idx], data_bits)


METHOD_FNS = {
    'DPLL': lambda rx_eq, shared, h_noisy, gb: run_dpll(rx_eq, shared['bits']),
    'VV':    lambda rx_eq, shared, h_noisy, gb: run_vv(rx_eq, shared['bits']),
    'KF_pilot': lambda rx_eq, shared, h_noisy, gb: run_kf_pilot_nmse(shared, h_noisy, gb),
}


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    print("=" * 70)
    print("NMSE Expanded Verification: 3 noise models x multi-SNR")
    print("=" * 70)
    print(f"SNR: {SNR_DB} dB")
    print(f"NMSE: {NMSE_DB} dB")
    print(f"Methods: {METHODS}")
    print(f"Noise models: {NOISE_MODELS}  (A=multiplicative, B=additive, C=complex)")
    print(f"Turbulence: {TURB_NAME}")
    print(f"Seeds: {SEEDS[0]}..{SEEDS[-1]} ({N_SEEDS}), Ns: {NS}")
    print()

    # results structure: results[snr_db][model][nmse_db][method] = {mean, values}
    # also results[snr_db]['oracle'][method] = {mean, values}
    results = {}

    for snr_db, gamma_bar in zip(SNR_DB, GAMMA_BARS):
        print(f"\n{'='*60}")
        print(f"  SNR = {snr_db} dB (gamma_bar = {gamma_bar:.2f})")
        print(f"{'='*60}")
        results[snr_db] = {}

        # ── Oracle baselines (perfect h, all methods) ──
        oracle_bers = {m: [] for m in METHODS}
        for sd in SEEDS:
            shared = generate_shared_realization(NS, gamma_bar, TURB_NAME, F_DOT, seed=sd)
            rx_eq_oracle = equalize_oracle(shared)
            oracle_bers['DPLL'].append(run_dpll(rx_eq_oracle, shared['bits']))
            oracle_bers['VV'].append(run_vv(rx_eq_oracle, shared['bits']))
            oracle_bers['KF_pilot'].append(
                run_kf_pilot_nmse(shared, shared['h_blocks'], gamma_bar))

        oracle_means = {m: float(np.mean(v)) for m, v in oracle_bers.items()}
        results[snr_db]['oracle'] = {
            m: {'mean': oracle_means[m], 'values': [float(x) for x in oracle_bers[m]]}
            for m in METHODS
        }
        print(f"  oracle: " + "  ".join(f"{m}={oracle_means[m]:.2e}" for m in METHODS))

        # ── Noise model sweep ──
        for model in NOISE_MODELS:
            results[snr_db][model] = {}
            noise_fn = NOISE_MODEL_FNS[model]

            for nmse_db in NMSE_DB:
                bers = {m: [] for m in METHODS}

                for sd in SEEDS:
                    shared = generate_shared_realization(NS, gamma_bar, TURB_NAME,
                                                          F_DOT, seed=sd)
                    h_true_blocks = shared['h_blocks']
                    rng = np.random.RandomState(sd + 50000)
                    h_noisy_blocks = noise_fn(h_true_blocks, nmse_db, rng)

                    # For DPLL/VV: equalize with noisy h then recover
                    h_noisy_per_sym = np.repeat(h_noisy_blocks, BLOCK)[:NS]
                    rx_eq = amp_limit(
                        mmse_equalize(shared['rx_raw'], h_noisy_per_sym, gamma_bar), 3.0)

                    for m in ['DPLL', 'VV']:
                        bers[m].append(METHOD_FNS[m](rx_eq, shared, h_noisy_blocks, gamma_bar))
                    bers['KF_pilot'].append(
                        METHOD_FNS['KF_pilot'](rx_eq, shared, h_noisy_blocks, gamma_bar))

                means = {m: max(float(np.mean(v)), BER_FLOOR) for m, v in bers.items()}
                degrade = {m: float(db_ratio(means[m], oracle_means[m])) for m in METHODS}

                results[snr_db][model][nmse_db] = {
                    m: {'mean': means[m], 'values': [float(x) for x in bers[m]]}
                    for m in METHODS
                }

                tag = f"  model {model} NMSE={nmse_db:>3d}dB: "
                tag += "  ".join(f"{m}={means[m]:.2e}(D{degrade[m]:+.1f}dB)"
                                for m in METHODS)
                print(tag)

    # ─── Save JSON ───
    out_dir = os.path.join(OUT, 'results')
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, 'nmse_expanded.json')
    with open(json_path, 'w') as f:
        json.dump({
            'results': results,
            'meta': {
                'N_seeds': N_SEEDS, 'seeds': SEEDS, 'Ns': NS,
                'snr_db': SNR_DB, 'gamma_bars': [float(g) for g in GAMMA_BARS],
                'nmse_levels_db': NMSE_DB,
                'methods': METHODS,
                'noise_models': NOISE_MODELS,
                'turbulence': TURB_NAME,
                'f_dot': F_DOT,
                'note': 'Expanded NMSE: 3 noise models x multi-SNR x 3 methods',
            }
        }, f, indent=2)
    print(f"\nJSON saved: {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plot 1: BER vs SNR — 3 panels (one per noise model)
    # ═══════════════════════════════════════════════════════════
    fig1, axes1 = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    model_labels = {'A': 'Model A: Multiplicative', 'B': 'Model B: Additive',
                    'C': 'Model C: Complex (no abs)'}
    method_styles = {'DPLL': ('o', '#1f77b4'), 'VV': ('s', '#ff7f0e'),
                     'KF_pilot': ('D', '#d62728')}
    nmse_colors = {-20: '#2ca02c', -10: '#1f77b4', -5: '#ff7f0e', 0: '#d62728'}
    nmse_lw = {-20: 1.0, -10: 1.2, -5: 1.5, 0: 2.0}
    nmse_ls = {-20: ':', -10: '--', -5: '-.', 0: '-'}

    for panel_idx, model in enumerate(NOISE_MODELS):
        ax = axes1[panel_idx]

        # Oracle line (no NMSE, just per-SNR)
        for m in METHODS:
            oracle_ber = [max(results[s]['oracle'][m]['mean'], BER_FLOOR)
                          for s in SNR_DB]
            mk, col = method_styles[m]
            ax.semilogy(SNR_DB, oracle_ber, mk, color=col, lw=2.5, ms=7,
                        label=f'{m} (oracle)', alpha=0.8)

        # NMSE lines
        for nmse in NMSE_DB:
            for m in METHODS:
                bers = [max(results[s][model][nmse][m]['mean'], BER_FLOOR)
                        for s in SNR_DB]
                mk, _ = method_styles[m]
                ax.semilogy(SNR_DB, bers, mk, color=nmse_colors[nmse],
                            ls=nmse_ls[nmse], lw=nmse_lw[nmse], ms=4, alpha=0.85,
                            label=f'{m} NMSE={nmse}dB' if panel_idx == 0 else '')

        ax.set_xlabel('SNR (dB)', fontsize=10)
        if panel_idx == 0:
            ax.set_ylabel('BER', fontsize=10)
        ax.set_title(model_labels[model], fontsize=11)
        ax.grid(True, alpha=0.3, which='both')
        ax.set_ylim(bottom=1e-7)

    # Compact legend for rightmost panel
    handles, labels = axes1[0].get_legend_handles_labels()
    fig1.legend(handles, labels, loc='lower center', ncol=4, fontsize=7,
                bbox_to_anchor=(0.5, -0.08))

    plt.suptitle('BER vs SNR under Channel Estimation Error '
                 '(moderate turbulence)', fontsize=12, y=1.02)
    plt.tight_layout()

    fig_dir_sim = os.path.join(OUT, 'figures')
    os.makedirs(fig_dir_sim, exist_ok=True)
    fig_path_sim = os.path.join(fig_dir_sim, 'nmse_expanded.pdf')
    plt.savefig(fig_path_sim, dpi=150, bbox_inches='tight')

    thesis_fig_dir = os.path.join(os.path.dirname(os.path.dirname(OUT)),
                                   '毕设', '写作材料', 'figures')
    os.makedirs(thesis_fig_dir, exist_ok=True)
    fig_path_thesis = os.path.join(thesis_fig_dir, 'nmse_expanded.pdf')
    plt.savefig(fig_path_thesis, dpi=150, bbox_inches='tight')
    plt.close(fig1)
    print(f"Figure saved: {fig_path_sim}")
    print(f"Figure saved: {fig_path_thesis}")

    # ═══════════════════════════════════════════════════════════
    # Plot 2: BER vs NMSE at 20 dB SNR — 3 noise model curves
    # ═══════════════════════════════════════════════════════════
    fig2, ax2 = plt.subplots(1, 1, figsize=(7, 5))
    snr_20 = 20

    for m in METHODS:
        # Oracle
        oracle_ber = max(results[snr_20]['oracle'][m]['mean'], BER_FLOOR)
        ax2.axhline(y=oracle_ber, color=method_styles[m][1], ls=':', alpha=0.5,
                     lw=1)

        for model in NOISE_MODELS:
            bers = [max(results[snr_20][model][nmse][m]['mean'], BER_FLOOR)
                    for nmse in NMSE_DB]
            mk, _ = method_styles[m]
            model_ls = {'A': '-', 'B': '--', 'C': '-.'}[model]
            model_label = {'A': 'A(mult)', 'B': 'B(add)', 'C': 'C(cplx)'}[model]
            ax2.semilogy(NMSE_DB, bers, mk, ls=model_ls,
                         color=method_styles[m][1], lw=1.5, ms=6,
                         label=f'{m} {model_label}')

    ax2.set_xlabel('Channel Estimation NMSE (dB)', fontsize=10)
    ax2.set_ylabel('BER', fontsize=10)
    ax2.set_title(f'BER vs NMSE at SNR={snr_20} dB (moderate turbulence)', fontsize=11)
    ax2.legend(fontsize=7, ncol=3, loc='upper left')
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim(bottom=1e-7)

    plt.tight_layout()

    fig_path_sim2 = os.path.join(fig_dir_sim, 'nmse_expanded_snr20.pdf')
    plt.savefig(fig_path_sim2, dpi=150, bbox_inches='tight')
    fig_path_thesis2 = os.path.join(thesis_fig_dir, 'nmse_expanded_snr20.pdf')
    plt.savefig(fig_path_thesis2, dpi=150, bbox_inches='tight')
    plt.close(fig2)
    print(f"Figure saved: {fig_path_sim2}")
    print(f"Figure saved: {fig_path_thesis2}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
