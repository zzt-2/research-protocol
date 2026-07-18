#!/usr/bin/env python3
"""Method applicability matrix: 50 seeds, 3 methods x 3 turbulence, SNR=20dB.

Fig 2 data: VV(Nw=64) vs VV(Nw=256) vs DPLL(omega_n=20M).
Outputs: method_matrix_50seed.json
Usage: python sim_method_matrix_50seed.py [--quick]
"""

import sys, os, json, time, argparse
import numpy as np
from multiprocessing import Pool, cpu_count

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '..', '..', '..', 'projects', 'simulation'))
from common import (
    DOPPLER_HIGH, TURB, BLOCK, FIXED_CFG_OPTIMAL,
    generate_shared_realization, equalize_oracle, fft_foe,
    dpll_track, vv_cpr, resolve_qpsk,
)

SNR_DB = 20
NS = 50000
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['vv64', 'vv256', 'dpll20m']


def trial(args):
    method, turb_name, seed = args
    gamma_bar = 10 ** (SNR_DB / 10)
    shared = generate_shared_realization(NS, gamma_bar, turb_name, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    N = len(rx_eq)

    if method == 'vv64':
        fo = fft_foe(rx_eq, N_fft=1024)
        rx_foc = rx_eq * np.exp(-1j * fo * np.arange(N))
        rx_pll, _ = dpll_track(rx_foc, omega_n=8e6)
        rx_cpr, _ = vv_cpr(rx_pll, Nw=64)
        return max(resolve_qpsk(rx_cpr, shared['bits']), BER_FLOOR)

    elif method == 'vv256':
        cfg = FIXED_CFG_OPTIMAL[turb_name]
        fo = fft_foe(rx_eq, N_fft=cfg['N_fft'])
        rx_foc = rx_eq * np.exp(-1j * fo * np.arange(N))
        rx_pll, _ = dpll_track(rx_foc, omega_n=cfg['omega_n'])
        rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
        return max(resolve_qpsk(rx_cpr, shared['bits']), BER_FLOOR)

    elif method == 'dpll20m':
        fo = fft_foe(rx_eq, N_fft=1024)
        rx_foc = rx_eq * np.exp(-1j * fo * np.arange(N))
        rx_out, _ = dpll_track(rx_foc, omega_n=20e6)
        return max(resolve_qpsk(rx_out, shared['bits']), BER_FLOOR)

    else:
        raise ValueError(f"Unknown method: {method}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='2 seeds, 1 turb, 1 method')
    args = parser.parse_args()

    seeds = list(range(1000, 1002)) if args.quick else list(range(1000, 1050))
    turb_levels = ['moderate'] if args.quick else TURB_LEVELS
    methods = ['vv64'] if args.quick else METHODS

    t0 = time.time()
    results = {}
    n_workers = max(1, cpu_count() - 1)

    total = len(methods) * len(turb_levels) * len(seeds)
    done = 0

    for method in methods:
        results[method] = {}
        for turb in turb_levels:
            arg_list = [(method, turb, sd) for sd in seeds]
            with Pool(n_workers) as pool:
                bers = pool.map(trial, arg_list)
            ber_arr = np.array(bers)
            results[method][turb] = {
                'ber_mean': float(np.mean(ber_arr)),
                'ber_std': float(np.std(ber_arr)),
                'ber_values': [float(b) for b in ber_arr],
            }
            done += len(seeds)
            print(f"[{done}/{total}] {method:8s} / {turb:9s}: "
                  f"BER={np.mean(ber_arr):.2e} +/- {np.std(ber_arr):.2e}")

    out = {
        'meta': {
            'n_seeds': len(seeds), 'seeds': seeds, 'snr_db': SNR_DB,
            'methods': methods, 'turb_levels': turb_levels, 'Ns': NS,
        },
        'results': results,
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'method_matrix_50seed.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time() - t0:.1f}s")


if __name__ == '__main__':
    main()
