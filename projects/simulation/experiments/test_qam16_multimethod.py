#!/usr/bin/env python3
"""Quick test: BPS-16QAM, DD-DPLL, KF-oracle-16QAM vs existing DD-DPLL baseline

Validates that BPS and KF can operate with 16-QAM decisions.
Short test: 3 turb × 3 seeds × 20dB, Ns=10000.
"""
import sys, os, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (
    TURB, BLOCK, T_S, F_RESIDUAL, DOPPLER_HIGH,
    gg_block, doppler_phase, qam16_mod,
    dpll_track_dd, bps_cpr, kf_unified, resolve_qam16,
    amp_limit, mmse_equalize, design_Q,
)

SNR_DB = 20
SEEDS = [0, 1, 2]
TURB_LEVELS = ['weak', 'moderate', 'strong']
NS = 10000
OMEGA_N = 20e6


def gen_signal(Ns, gamma_bar, turb, seed):
    np.random.seed(seed)
    a, b = TURB[turb]
    bits = np.random.randint(0, 2, size=4 * Ns)
    tx = qam16_mod(bits)
    h = gg_block(Ns, a, b, BLOCK)[:Ns]
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH)
    nv = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(nv) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx = np.sqrt(h) * tx * np.exp(1j * phi) + noise
    return bits, tx, rx, h, phi


def oracle_foe(rx, phi):
    """Remove known FO + Doppler phase (oracle)."""
    N = len(rx)
    phi_fo = 2 * np.pi * F_RESIDUAL * np.arange(N) * T_S
    return rx * np.exp(-1j * phi_fo)  # only remove FO, keep laser noise


def run_dpll(rx_foc, bits, omega_n):
    rx_out, _ = dpll_track_dd(rx_foc, omega_n=omega_n, mod='qam16')
    return resolve_qam16(rx_out, bits)


def run_bps(rx_foc, bits):
    rx_out, _ = bps_cpr(rx_foc, B=32, Nw=61, mod='qam16')
    return resolve_qam16(rx_out, bits)


def run_kf_oracle(rx_foc, h, bits, gamma_bar, turb):
    """KF oracle-h, block-by-block with 16-QAM decisions."""
    N = len(rx_foc)
    n_blocks = N // BLOCK
    Q = design_Q(turb, DOPPLER_HIGH)
    Q_fine = Q.copy()
    Q_fine[1, 1] = (50e3)**2 * T_S**2

    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i * BLOCK, (i + 1) * BLOCK
        h_val = h[s]
        phi_init = phi_full[s - 1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(
            rx_foc[s:e], h_val, gamma_bar, Q_fine,
            phi_init=phi_init, df_init=prev_df, P_init=prev_P, mod='qam16')
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    rx_out = rx_foc * np.exp(-1j * phi_full)
    return resolve_qam16(rx_out, bits)


def main():
    print("=" * 65)
    print("16-QAM Multi-Method Quick Test")
    print(f"  Methods: DD-DPLL, BPS-16QAM, KF-oracle-16QAM")
    print(f"  SNR={SNR_DB}dB, Seeds={SEEDS}, Ns={NS}")
    print("=" * 65)

    gamma_bar = 10 ** (SNR_DB / 10)

    for turb in TURB_LEVELS:
        print(f"\n--- {turb} ---")
        print(f"  {'seed':>4}  {'DD-DPLL':>12}  {'BPS-16Q':>12}  {'KF-orc':>12}")
        for seed in SEEDS:
            bits, tx, rx, h, phi = gen_signal(NS, gamma_bar, turb, seed)
            rx_eq = amp_limit(mmse_equalize(rx, h, gamma_bar), 3.0)
            rx_foc = oracle_foe(rx_eq, phi)

            ber_dpll = run_dpll(rx_foc, bits, OMEGA_N)
            ber_bps = run_bps(rx_foc, bits)
            ber_kf = run_kf_oracle(rx_foc, h, bits, gamma_bar, turb)

            print(f"  {seed:>4}  {ber_dpll:>12.4e}  {ber_bps:>12.4e}  {ber_kf:>12.4e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
