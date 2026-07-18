#!/usr/bin/env python3
"""扩展 dpll_omega_sweep 到 50 seeds（补充 seed 1010-1049）"""

import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    dpll_track, resolve_qpsk,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'dpll_omega_sweep.json')

OMEGA_ALL = [2e6, 3e6, 5e6, 7e6, 10e6, 15e6, 20e6, 30e6, 50e6, 70e6, 100e6]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_POINTS = [10, 15, 20]
NEW_SEEDS = list(range(1010, 1050))
NS = 50000
F_DOT = DOPPLER_HIGH
ZETA = np.sqrt(2) / 2
BER_FLOOR = 1e-7


def run_single_trial(omega_n, turb, gamma_bar, seed):
    shared = generate_shared_realization(NS, gamma_bar, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * np.arange(NS))
    rx_out, _ = dpll_track(rx_foc, omega_n=omega_n, zeta=ZETA)
    ber = resolve_qpsk(rx_out, shared['bits'])
    return max(ber, BER_FLOOR)


def main():
    with open(OUT_JSON) as f:
        data = json.load(f)

    t0 = time.time()
    total = len(SNR_POINTS) * len(TURB_LEVELS) * len(OMEGA_ALL) * len(NEW_SEEDS)
    done = 0

    for snr_db in SNR_POINTS:
        gamma_bar = 10 ** (snr_db / 10)
        snr_s = str(snr_db)
        for turb in TURB_LEVELS:
            for omega_n in OMEGA_ALL:
                om_s = str(int(omega_n))
                existing = data['results'][snr_s][turb][om_s]['ber_values']
                new_bers = []
                for sd in NEW_SEEDS:
                    ber = run_single_trial(omega_n, turb, gamma_bar, sd)
                    new_bers.append(ber)
                    done += 1
                    if done % 200 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] SNR={snr_db} {turb} ω={omega_n/1e6:.0f}M ({elapsed:.0f}s)")

                all_bers = existing + [float(b) for b in new_bers]
                all_arr = np.array(all_bers)
                data['results'][snr_s][turb][om_s] = {
                    'ber_mean': float(np.mean(all_arr)),
                    'ber_std': float(np.std(all_arr)),
                    'ber_values': [float(b) for b in all_bers],
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} new trials)")

    with open(OUT_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUT_JSON}")


if __name__ == '__main__':
    main()
