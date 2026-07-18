#!/usr/bin/env python3
"""扩展 nw_sweep 到 50 seeds（补充 seed 1010-1049）"""

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

NW_ALL = [16, 18, 20, 22, 24, 28, 32, 36, 40, 44, 48, 56, 64, 96, 128, 192, 256, 384, 512, 768, 1024]
TURB_LEVELS = ['weak', 'moderate', 'strong']
METHODS = ['VV', 'BPS']
NEW_SEEDS = list(range(1010, 1050))  # 40 new seeds
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
    with open(OUT_JSON) as f:
        data = json.load(f)

    t0 = time.time()
    total = len(TURB_LEVELS) * len(METHODS) * len(NW_ALL) * len(NEW_SEEDS)
    done = 0

    for turb in TURB_LEVELS:
        for method in METHODS:
            for nw in NW_ALL:
                nw_s = str(nw)
                existing = data['results'][turb][method][nw_s]['ber_values']
                new_bers = []
                for sd in NEW_SEEDS:
                    ber = run_single_trial(nw, method, turb, sd)
                    new_bers.append(ber)
                    done += 1
                    if done % 200 == 0 or done == total:
                        elapsed = time.time() - t0
                        print(f"[{done}/{total}] {turb} {method} Nw={nw} ({elapsed:.0f}s)")

                all_bers = existing + [float(b) for b in new_bers]
                all_arr = np.array(all_bers)
                data['results'][turb][method][nw_s] = {
                    'ber_mean': float(np.mean(all_arr)),
                    'ber_std': float(np.std(all_arr)),
                    'ber_values': [float(b) for b in all_bers],
                    'fail_rate': float(np.mean(all_arr > FAIL_THRESH)),
                }

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s ({total} new trials)")

    with open(OUT_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUT_JSON}")


if __name__ == '__main__':
    main()
