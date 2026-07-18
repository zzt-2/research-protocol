#!/usr/bin/env python3
"""补充 SNR sweep 奇数 dB 点，合并到现有 JSON"""

import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    DOPPLER_HIGH, TURB,
    generate_shared_realization, equalize_oracle, fft_foe,
    vv_cpr, bps_cpr, dpll_track, resolve_qpsk,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWEEP_JSON = os.path.join(BASE, 'results', 'sweep_20260601_181320.json')
BPS_JSON = os.path.join(BASE, 'results', 'sweep_bps_10seed.json')

NEW_SNR = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SEEDS = list(range(1000, 1010))
NS = 100000
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7


def run_trial(method_name, turb, gamma_bar, seed):
    shared = generate_shared_realization(NS, gamma_bar, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    k = np.arange(NS)
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)

    if method_name == 'VV':
        rx_cpr, _ = vv_cpr(rx_foc, Nw=64)
    elif method_name == 'BPS':
        rx_cpr, _ = bps_cpr(rx_foc)
    elif method_name == 'DPLL':
        rx_cpr, _ = dpll_track(rx_foc, omega_n=8e6, zeta=np.sqrt(2)/2)

    ber = resolve_qpsk(rx_cpr, shared['bits'])
    return max(ber, BER_FLOOR)


def add_points(json_path, methods):
    """Add new SNR points to a sweep JSON."""
    with open(json_path) as f:
        data = json.load(f)

    total = len(methods) * len(TURB_LEVELS) * len(NEW_SNR) * len(SEEDS)
    done = 0
    t0 = time.time()

    for method in methods:
        for turb in TURB_LEVELS:
            key = f'{method}_{turb}'
            pts = data['results'][key]['snr_points']
            existing_snr = {p['snr_db'] for p in pts}

            for snr_db in NEW_SNR:
                if snr_db in existing_snr:
                    done += len(SEEDS)
                    continue

                gamma_bar = 10 ** (snr_db / 10)
                per_seed = []
                for sd in SEEDS:
                    ber = run_trial(method, turb, gamma_bar, sd)
                    per_seed.append(ber)
                    done += 1
                    if done % 100 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] {method}_{turb} SNR={snr_db}dB ({elapsed:.0f}s)")

                ber_arr = np.array(per_seed)
                ci = [float(np.percentile(ber_arr, 2.5)),
                      float(np.percentile(ber_arr, 97.5))]
                pts.append({
                    'snr_db': float(snr_db),
                    'ber_mean': float(np.mean(ber_arr)),
                    'ber_std': float(np.std(ber_arr)),
                    'ci_95': ci,
                    'fail_rate': float(np.mean(ber_arr > 0.10)),
                    'per_seed_ber': [float(b) for b in ber_arr],
                })

            # Re-sort by SNR
            pts.sort(key=lambda p: p['snr_db'])

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {json_path}")


if __name__ == '__main__':
    print("=== VV + DPLL sweep ===")
    add_points(SWEEP_JSON, ['VV', 'DPLL'])
    print("\n=== BPS sweep ===")
    add_points(BPS_JSON, ['BPS'])
