#!/usr/bin/env python3
"""DPLL omega_n design curve: 50 seeds, 13 omega points x 3 turbulence, SNR=20dB.

Fig 3 data: BER vs omega_n for weak/moderate/strong turbulence.
Outputs: dpll_omega_50seed.json
Usage: python sim_dpll_omega_50seed.py [--quick]
"""

import sys, os, json, time, argparse
import numpy as np
from multiprocessing import Pool, cpu_count

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '..', '..', '..', 'projects', 'simulation'))
from common import (
    DOPPLER_HIGH, generate_shared_realization, equalize_oracle, fft_foe,
    dpll_track, resolve_qpsk,
)

OMEGA_MHZ = [1, 2, 5, 7, 10, 15, 20, 25, 30, 40, 50, 75, 100]
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_DB = 20
NS = 50000
F_DOT = DOPPLER_HIGH
ZETA = np.sqrt(2) / 2
BER_FLOOR = 1e-7


def trial(args):
    omega_hz, turb_name, seed = args
    gamma_bar = 10 ** (SNR_DB / 10)
    shared = generate_shared_realization(NS, gamma_bar, turb_name, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo * np.arange(NS))
    rx_out, _ = dpll_track(rx_foc, omega_n=omega_hz, zeta=ZETA)
    return max(resolve_qpsk(rx_out, shared['bits']), BER_FLOOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='2 seeds, 3 omega, 1 turb')
    args = parser.parse_args()

    omega_mhz = [2, 20, 100] if args.quick else OMEGA_MHZ
    seeds = list(range(1000, 1002)) if args.quick else list(range(1000, 1050))
    turb_levels = ['moderate'] if args.quick else TURB_LEVELS

    t0 = time.time()
    results = {}
    n_workers = max(1, cpu_count() - 1)

    total = len(omega_mhz) * len(turb_levels) * len(seeds)
    done = 0

    for omega in omega_mhz:
        omega_hz = omega * 1e6
        key = str(omega)
        results[key] = {}

        for turb in turb_levels:
            arg_list = [(omega_hz, turb, sd) for sd in seeds]
            with Pool(n_workers) as pool:
                bers = pool.map(trial, arg_list)
            ber_arr = np.array(bers)
            results[key][turb] = {
                'ber_mean': float(np.mean(ber_arr)),
                'ber_std': float(np.std(ber_arr)),
                'ber_values': [float(b) for b in ber_arr],
            }
            done += len(seeds)
            print(f"[{done}/{total}] wn={omega:3d}MHz {turb:9s}: "
                  f"BER={np.mean(ber_arr):.2e} +/- {np.std(ber_arr):.2e}")

    out = {
        'meta': {
            'omega_mhz': omega_mhz, 'n_seeds': len(seeds), 'seeds': seeds,
            'snr_db': SNR_DB, 'turb_levels': turb_levels, 'Ns': NS,
            'zeta': float(ZETA),
        },
        'results': results,
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'dpll_omega_50seed.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time() - t0:.1f}s")


if __name__ == '__main__':
    main()
