#!/usr/bin/env python3
"""补充 dpll_omega_sweep 中间点，合并到现有 JSON"""

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

# Existing: [2e6, 5e6, 10e6, 20e6, 50e6, 100e6]
# Add intermediates:
NEW_OMEGA = [3e6, 7e6, 15e6, 30e6, 70e6]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_POINTS = [10, 15, 20]
SEEDS = list(range(1000, 1010))
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
    total = len(SNR_POINTS) * len(TURB_LEVELS) * len(NEW_OMEGA) * len(SEEDS)
    done = 0

    for snr_db in SNR_POINTS:
        gamma_bar = 10 ** (snr_db / 10)
        snr_s = str(snr_db)
        for turb in TURB_LEVELS:
            for omega_n in NEW_OMEGA:
                om_s = str(int(omega_n))
                if om_s in data['results'][snr_s][turb]:
                    done += len(SEEDS)
                    continue
                ber_list = []
                for sd in SEEDS:
                    ber = run_single_trial(omega_n, turb, gamma_bar, sd)
                    ber_list.append(ber)
                    done += 1
                    if done % 50 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] SNR={snr_db} {turb} "
                              f"ω_n={omega_n/1e6:.0f}M BER={ber:.2e} ({elapsed:.0f}s)")
                ber_arr = np.array(ber_list)
                data['results'][snr_s][turb][om_s] = {
                    'ber_mean': float(np.mean(ber_arr)),
                    'ber_std': float(np.std(ber_arr)),
                    'ber_values': [float(b) for b in ber_arr],
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")

    with open(OUT_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUT_JSON}")


if __name__ == '__main__':
    main()
