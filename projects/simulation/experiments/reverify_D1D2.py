#!/usr/bin/env python3
"""Re-verify D1/D2 with new common.py — compare against old stress_common results.

Only re-runs D1 comparison (known optimal configs) + D2 ablation.
Skips D1 grid search (configs already known from old results).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import json

# ═══════════════════════════════════════════════════════════════
# Config (same as old)
# ═══════════════════════════════════════════════════════════════
TURB_NAMES = ['weak', 'moderate', 'strong']
N_SEEDS = 30
NS = 10000
GAMMA_BAR = 100

OLD_RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', 'thesis-figures', 'simulation', 'results_kf_stress_D1D2.json'
)

# ═══════════════════════════════════════════════════════════════
# D1: KF pilot vs optimal Fixed (skip grid search, use known configs)
# ═══════════════════════════════════════════════════════════════
def d1_comparison(turb_name, cfg):
    bers_fixed = []
    bers_kf = []
    for sd in range(N_SEEDS):
        sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
        # Optimal Fixed
        rx_eq = equalize_oracle(sh)
        rx_fixed = carrier_recovery_fixed(rx_eq, cfg=cfg)
        bers_fixed.append(resolve_qpsk(rx_fixed, sh['bits']))
        # KF pilot
        corrected, data_idx, data_bits, _ = run_kf_pilot(sh, n_pilots=5, eq_mode='oracle')
        bers_kf.append(resolve_qpsk(corrected[data_idx], data_bits))
    return np.mean(bers_fixed), np.mean(bers_kf)

# Also run with default config for reference
def d1_default(turb_name):
    bers = []
    for sd in range(N_SEEDS):
        sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
        rx_eq = equalize_oracle(sh)
        rx_fixed = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG)
        bers.append(resolve_qpsk(rx_fixed, sh['bits']))
    return np.mean(bers)


# ═══════════════════════════════════════════════════════════════
# D2: Ablation (exact same logic as old script)
# ═══════════════════════════════════════════════════════════════
D2_SCHEMES = ['FOE_only', 'FOE+VV', 'FOE+DPLL', 'KF_frame', 'KF_pilot']

def d2_trial(shared):
    rx_eq = equalize_oracle(shared)
    N = len(rx_eq)
    k = np.arange(N)
    results = {}

    # 1) FOE only
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foe = rx_eq * np.exp(-1j * fo_est * k)
    results['FOE_only'] = resolve_qpsk(rx_foe, shared['bits'])

    # 2) FOE + VV (Nw=64, same as old)
    fo_est2 = fft_foe(rx_eq, N_fft=1024)
    rx_foc2 = rx_eq * np.exp(-1j * fo_est2 * k)
    rx_vv, _ = vv_cpr(rx_foc2, Nw=64)
    results['FOE+VV'] = resolve_qpsk(rx_vv, shared['bits'])

    # 3) FOE + DPLL (default params, same as old)
    fo_est3 = fft_foe(rx_eq, N_fft=1024)
    rx_foc3 = rx_eq * np.exp(-1j * fo_est3 * k)
    rx_pll, _ = dpll_track(rx_foc3, omega_n=8e6, zeta=np.sqrt(2)/2)
    results['FOE+DPLL'] = resolve_qpsk(rx_pll, shared['bits'])

    # 4) KF frame-h
    rx_kf_frame = run_kf_frame_h(shared, eq_mode='oracle')
    results['KF_frame'] = resolve_qpsk(rx_kf_frame, shared['bits'])

    # 5) KF pilot
    corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots=5, eq_mode='oracle')
    results['KF_pilot'] = resolve_qpsk(corrected[data_idx], data_bits)

    return results


def d2_run(turb_name):
    all_results = {s: [] for s in D2_SCHEMES}
    for sd in range(N_SEEDS):
        sh = generate_shared_realization(NS, GAMMA_BAR, turb_name, DOPPLER_HIGH, seed=sd)
        trial = d2_trial(sh)
        for s in D2_SCHEMES:
            all_results[s].append(trial[s])
    return {s: np.mean(v) for s, v in all_results.items()}


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()

    # Load old results for comparison
    with open(OLD_RESULTS_PATH) as f:
        old = json.load(f)

    print("=" * 70)
    print("D1/D2 RE-VERIFICATION: new common.py vs old stress_common")
    print("=" * 70)
    print(f"VV formula: new common.py = unwrap(angle)/M")
    print(f"            old stress_common = unwrap(angle*M)/M")
    print(f"Seeds: {N_SEEDS}, Ns: {NS}, gamma_bar: {GAMMA_BAR}")
    print()

    # ---- D1 ----
    print("=" * 60)
    print("D1: KF pilot vs Optimal Fixed")
    print("=" * 60)
    d1_new = {}
    for turb in TURB_NAMES:
        cfg = FIXED_CFG_OPTIMAL[turb]
        ber_fixed, ber_kf = d1_comparison(turb, cfg)
        gain_db = db_ratio(ber_fixed, ber_kf)
        d1_new[turb] = {'fixed_opt': ber_fixed, 'kf_pilot': ber_kf, 'gain_db': gain_db}

        old_d1 = old['D1_comparison'][turb]
        print(f"\n  {turb.upper()}:")
        print(f"    {'':12s} {'NEW':>12s} {'OLD':>12s} {'Ratio':>8s}")
        print(f"    {'Fixed_opt':12s} {ber_fixed:12.6f} {old_d1['fixed_opt_ber']:12.6f} {ber_fixed/old_d1['fixed_opt_ber']:8.3f}")
        print(f"    {'KF_pilot':12s} {ber_kf:12.6f} {old_d1['kf_pilot_ber']:12.6f} {ber_kf/old_d1['kf_pilot_ber']:8.3f}")
        print(f"    {'Gain_dB':12s} {gain_db:12.2f} {old_d1['gain_db']:12.2f}")

    # Default Fixed reference
    print("\n--- Default Fixed reference ---")
    for turb in TURB_NAMES:
        ber_def = d1_default(turb)
        old_def = old['D1_comparison'][turb]['default_fixed_ber']
        print(f"  {turb}: NEW={ber_def:.6f}  OLD={old_def:.6f}  ratio={ber_def/old_def:.3f}")

    # ---- D2 ----
    print("\n" + "=" * 60)
    print("D2: Gain Attribution Ablation")
    print("=" * 60)
    d2_new = {}
    for turb in TURB_NAMES:
        print(f"\n  {turb.upper()}:")
        d2_new[turb] = d2_run(turb)
        print(f"    {'Scheme':12s} {'NEW':>12s} {'OLD':>12s} {'Ratio':>8s}")
        for s in D2_SCHEMES:
            new_val = d2_new[turb][s]
            old_val = old['D2_ablation'][turb][s]
            ratio = new_val / old_val if old_val > 0 else float('inf')
            marker = " ***" if abs(ratio - 1.0) > 0.05 else ""
            print(f"    {s:12s} {new_val:12.6f} {old_val:12.6f} {ratio:8.3f}{marker}")

    # ---- Summary ----
    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"SUMMARY (elapsed {elapsed:.1f}s)")
    print(f"{'=' * 60}")

    max_deviation = 0.0
    print("\nD1 deviations (NEW/OLD):")
    for turb in TURB_NAMES:
        for key in ['fixed_opt', 'kf_pilot']:
            ratio = d1_new[turb][key] / old['D1_comparison'][turb][
                'fixed_opt_ber' if key == 'fixed_opt' else 'kf_pilot_ber']
            max_deviation = max(max_deviation, abs(ratio - 1.0))
            print(f"  {turb}/{key}: {ratio:.4f}")

    print(f"\nD2 max deviations (NEW/OLD):")
    for turb in TURB_NAMES:
        for s in D2_SCHEMES:
            ratio = d2_new[turb][s] / old['D2_ablation'][turb][s]
            max_deviation = max(max_deviation, abs(ratio - 1.0))
            if abs(ratio - 1.0) > 0.05:
                print(f"  {turb}/{s}: {ratio:.4f} ***")

    print(f"\nMax absolute deviation from 1.0: {max_deviation:.4f}")
    if max_deviation < 0.05:
        print("VERDICT: PASS — new common.py produces consistent results")
    elif max_deviation < 0.15:
        print("VERDICT: MINOR DEVIATION — expected from VV formula fix")
    else:
        print("VERDICT: INVESTIGATE — significant deviation detected")

    # Save new results
    out_path = os.path.join(OUT, 'results', 'reverify_D1D2_new_common.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump({'D1_new': {t: {k: float(v) for k, v in d.items()}
                              for t, d in d1_new.items()},
                   'D2_new': d2_new,
                   'meta': {'N_seeds': N_SEEDS, 'Ns': NS, 'gamma_bar': GAMMA_BAR,
                            'note': 'new common.py with VV fix unwrap(angle)/M'}},
                  f, indent=2, default=str)
    print(f"\nResults saved: {out_path}")
