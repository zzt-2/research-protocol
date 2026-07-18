#!/usr/bin/env python3
"""NMSE sensitivity sweep: 50 seeds, 9 NMSE points, moderate turbulence, SNR=20dB.

Fig 1 data: QPSK (DPLL) vs 16-QAM (DD-DPLL) BER under imperfect CSI.
Outputs: nmse_50seed.json
Usage: python sim_nmse_50seed.py [--quick]
"""

import sys, os, json, time, argparse
import numpy as np
from multiprocessing import Pool, cpu_count

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '..', '..', '..', 'projects', 'simulation'))
from common import (
    DOPPLER_HIGH, TURB, BLOCK, F_RESIDUAL, T_S,
    generate_shared_realization, fft_foe,
    dpll_track, dpll_track_dd, resolve_qpsk, resolve_qam16,
    mmse_equalize, amp_limit, qam16_mod, gg_block, doppler_phase,
)

NMSE_POINTS = [-20, -17.5, -15, -12.5, -10, -7.5, -5, -2.5, 0]
TURB_NAME = 'moderate'
SNR_DB = 20
NS = 50000
F_DOT = DOPPLER_HIGH
OMEGA_N = 20e6
BER_FLOOR = 1e-7


def noisy_h(h_blocks, nmse_db, rng):
    sigma = np.sqrt(10 ** (nmse_db / 10))
    h_noisy = h_blocks * (1 + sigma * (rng.randn(len(h_blocks))
                                        + 1j * rng.randn(len(h_blocks))))
    return np.abs(h_noisy)


def trial_qpsk(args):
    nmse_db, seed = args
    gamma_bar = 10 ** (SNR_DB / 10)
    shared = generate_shared_realization(NS, gamma_bar, TURB_NAME, F_DOT, seed=seed)

    rng = np.random.RandomState(seed + 50000)
    h_noisy = noisy_h(shared['h_blocks'], nmse_db, rng)
    h_noisy_sym = np.repeat(h_noisy, BLOCK)[:NS]

    rx_eq = amp_limit(mmse_equalize(shared['rx_raw'], h_noisy_sym, gamma_bar), 3.0)
    fo = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo * np.arange(NS))
    rx_out, _ = dpll_track(rx_foc, omega_n=OMEGA_N)
    return max(resolve_qpsk(rx_out, shared['bits']), BER_FLOOR)


def trial_qam16(args):
    nmse_db, seed = args
    gamma_bar = 10 ** (SNR_DB / 10)
    np.random.seed(seed)
    alpha, beta = TURB[TURB_NAME]
    bits = np.random.randint(0, 2, size=4 * NS)
    tx = qam16_mod(bits)
    h = gg_block(NS, alpha, beta, BLOCK)[:NS]
    h_blocks = np.array([h[i * BLOCK] for i in range(NS // BLOCK)])
    phi = doppler_phase(NS, f_res=F_RESIDUAL, f_dot=F_DOT)
    noise = np.sqrt(1 / (2 * gamma_bar)) * (np.random.randn(NS) + 1j * np.random.randn(NS))
    rx_raw = np.sqrt(h) * tx * np.exp(1j * phi) + noise

    rng = np.random.RandomState(seed + 50000)
    h_noisy = noisy_h(h_blocks, nmse_db, rng)
    h_noisy_sym = np.repeat(h_noisy, BLOCK)[:NS]

    rx_eq = amp_limit(mmse_equalize(rx_raw, h_noisy_sym, gamma_bar), 3.0)
    phi_fo = 2 * np.pi * F_RESIDUAL * np.arange(NS) * T_S
    rx_foc = rx_eq * np.exp(-1j * phi_fo)
    rx_out, _ = dpll_track_dd(rx_foc, omega_n=OMEGA_N, mod='qam16')
    return max(resolve_qam16(rx_out, bits), BER_FLOOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='2 seeds, 3 NMSE points')
    args = parser.parse_args()

    nmse_pts = [-20, -10, 0] if args.quick else NMSE_POINTS
    seeds = list(range(1000, 1002)) if args.quick else list(range(1000, 1050))

    t0 = time.time()
    results = {'qpsk': {}, 'qam16': {}}
    n_workers = max(1, cpu_count() - 1)

    for mod_name, trial_fn in [('qpsk', trial_qpsk), ('qam16', trial_qam16)]:
        print(f"\n{'=' * 60}")
        print(f"{mod_name}: {len(nmse_pts)} NMSE x {len(seeds)} seeds ({n_workers} workers)")
        print(f"{'=' * 60}")

        for nmse_db in nmse_pts:
            key = str(nmse_db)
            arg_list = [(nmse_db, sd) for sd in seeds]
            with Pool(n_workers) as pool:
                bers = pool.map(trial_fn, arg_list)
            ber_arr = np.array(bers)
            results[mod_name][key] = {
                'ber_mean': float(np.mean(ber_arr)),
                'ber_std': float(np.std(ber_arr)),
                'ber_values': [float(b) for b in ber_arr],
            }
            print(f"  NMSE={nmse_db:+6.1f}dB  BER={np.mean(ber_arr):.2e} +/- {np.std(ber_arr):.2e}")

    out = {
        'meta': {
            'nmse_db': nmse_pts, 'n_seeds': len(seeds), 'seeds': seeds,
            'snr_db': SNR_DB, 'turbulence': TURB_NAME, 'Ns': NS,
            'omega_n_hz': OMEGA_N,
        },
        **results,
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nmse_50seed.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time() - t0:.1f}s")


if __name__ == '__main__':
    main()
