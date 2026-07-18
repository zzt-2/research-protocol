#!/usr/bin/env python3
"""补充 nw_sweep 中间点，合并到现有 JSON"""

import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    GAMMA_BAR_DEFAULT, DOPPLER_HIGH,
    generate_shared_realization, equalize_oracle, fft_foe,
    vv_cpr, bps_cpr, resolve_qpsk,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(BASE, 'results', 'nw_sweep.json')

# Existing: [16, 32, 64, 128, 256, 512, 1024]
# Add low-Nw dense points:
NEW_NW = [18, 20, 22, 28, 36, 40, 44, 56]
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['VV', 'BPS']
SEEDS = list(range(1000, 1010))
NS = 50000
GAMMA_BAR = GAMMA_BAR_DEFAULT
F_DOT = DOPPLER_HIGH
BER_FLOOR = 1e-7
FAIL_THRESH = 0.10


def run_single_trial(nw, method, turb, seed):
    shared = generate_shared_realization(NS, GAMMA_BAR, turb, F_DOT, seed=seed)
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=1024)
    rx_foc = rx_eq * np.exp(-1j * fo_est * np.arange(NS))
    if method == 'VV':
        rx_cpr, _ = vv_cpr(rx_foc, Nw=nw)
    else:
        rx_cpr, _ = bps_cpr(rx_foc, Nw=nw)
    ber = resolve_qpsk(rx_cpr, shared['bits'])
    return max(ber, BER_FLOOR)


def main():
    # Load existing
    with open(OUT_JSON) as f:
        data = json.load(f)

    t0 = time.time()
    total = len(TURB_LEVELS) * len(METHODS) * len(NEW_NW) * len(SEEDS)
    done = 0

    for turb in TURB_LEVELS:
        for method in METHODS:
            for nw in NEW_NW:
                nw_s = str(nw)
                if nw_s in data['results'][turb][method]:
                    done += len(SEEDS)
                    continue
                ber_list = []
                for sd in SEEDS:
                    ber = run_single_trial(nw, method, turb, sd)
                    ber_list.append(ber)
                    done += 1
                    if done % 50 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] {turb} {method} Nw={nw} "
                              f"BER={ber:.2e} ({elapsed:.0f}s)")
                ber_arr = np.array(ber_list)
                data['results'][turb][method][nw_s] = {
                    'ber_mean': float(np.mean(ber_arr)),
                    'ber_std': float(np.std(ber_arr)),
                    'ber_values': [float(b) for b in ber_arr],
                    'fail_rate': float(np.mean(ber_arr > FAIL_THRESH)),
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")

    with open(OUT_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUT_JSON}")


if __name__ == '__main__':
    main()
