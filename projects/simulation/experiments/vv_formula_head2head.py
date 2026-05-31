#!/usr/bin/env python3
"""VV CPR Formula Head-to-Head Comparison

Isolates the effect of the VV phase extraction formula on IDENTICAL data.
  Formula A (correct): np.unwrap(np.angle(avg)) / M
  Formula B (buggy):   np.unwrap(np.angle(avg) * M) / M

For each turbulence level x 30 seeds:
  1. Generate shared realization (Ns=10000, gamma_bar=100)
  2. FOE + equalize_oracle
  3. VV with Formula A -> resolve_qpsk -> BER
  4. VV with Formula B -> resolve_qpsk -> BER
  5. DPLL (no VV) as third comparison
"""

import sys, os, time
import numpy as np

sys.path.insert(0, '/mnt/d/code/study/research-protocol/projects/simulation')
from common import (
    TURB, BLOCK, DOPPLER_HIGH, F_RESIDUAL, T_S, LASER_LW, GAMMA_BAR_DEFAULT,
    generate_shared_realization, equalize_oracle, fft_foe,
    resolve_qpsk, amp_limit, dpll_track,
    gg_block, qpsk_mod, doppler_phase, mmse_equalize,
)

# ── VV implementations with the two formulas ──────────────────────

def vv_cpr_formula_A(rx, Nw=64):
    """Formula A (correct): np.unwrap(np.angle(avg)) / M"""
    M = 4
    raised = rx ** M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg)) / M          # <-- Formula A
    return rx * np.exp(-1j * pe), pe


def vv_cpr_formula_B(rx, Nw=64):
    """Formula B (buggy): np.unwrap(np.angle(avg) * M) / M"""
    M = 4
    raised = rx ** M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg) * M) / M      # <-- Formula B
    return rx * np.exp(-1j * pe), pe


# ── Pipeline helper ───────────────────────────────────────────────

def run_pipeline(shared, vv_func, N_fft=1024, M_vv=64,
                 omega_n=8e6, zeta=np.sqrt(2)/2):
    """FOE -> DPLL -> VV -> resolve_qpsk"""
    rx_eq = equalize_oracle(shared)

    # FOE
    fo_est = fft_foe(rx_eq, N_fft=N_fft)
    rx_comp = rx_eq * np.exp(-1j * fo_est * np.arange(len(rx_eq)))

    # DPLL
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=zeta)

    # VV
    rx_vv, _ = vv_func(rx_pll, Nw=M_vv)

    # BER (resolve QPSK ambiguity)
    return resolve_qpsk(rx_vv, shared['bits'])


def run_dpll_only(shared, N_fft=1024, omega_n=8e6, zeta=np.sqrt(2)/2):
    """FOE -> DPLL only (no VV) -> resolve_qpsk"""
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq, N_fft=N_fft)
    rx_comp = rx_eq * np.exp(-1j * fo_est * np.arange(len(rx_eq)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=zeta)
    return resolve_qpsk(rx_pll, shared['bits'])


# ── Main experiment ───────────────────────────────────────────────

N_SEEDS = 30
Ns = 10000
gamma_bar = 100  # 20 dB
turb_levels = ['weak', 'moderate', 'strong']
f_dot = DOPPLER_HIGH

print("=" * 80)
print("VV CPR Formula Head-to-Head:  Formula A (correct)  vs  Formula B (buggy)")
print("=" * 80)
print(f"Ns={Ns}, gamma_bar={gamma_bar} ({10*np.log10(gamma_bar):.1f} dB), "
      f"f_dot={f_dot/1e6:.0f} MHz, seeds={N_SEEDS}")
print(f"Pipeline: FOE(N_fft=1024) -> DPLL(omega_n=8MHz) -> VV(Nw=64) -> resolve_qpsk")
print()

header = (f"{'Turb':>10s} | {'Formula A BER':>14s} | {'Formula B BER':>14s} | "
          f"{'DPLL-only BER':>14s} | {'Ratio B/A':>10s} | {'Ratio B/DPLL':>12s}")
print(header)
print("-" * len(header))

for turb in turb_levels:
    bers_A = []
    bers_B = []
    bers_D = []

    for seed in range(N_SEEDS):
        shared = generate_shared_realization(
            Ns=Ns, gamma_bar=gamma_bar,
            turb_name=turb, f_dot=f_dot, seed=seed
        )

        ber_A = run_pipeline(shared, vv_cpr_formula_A)
        ber_B = run_pipeline(shared, vv_cpr_formula_B)
        ber_D = run_dpll_only(shared)

        bers_A.append(ber_A)
        bers_B.append(ber_B)
        bers_D.append(ber_D)

    mean_A = np.mean(bers_A)
    mean_B = np.mean(bers_B)
    mean_D = np.mean(bers_D)

    ratio_BA = mean_B / mean_A if mean_A > 0 else float('inf')
    ratio_BD = mean_B / mean_D if mean_D > 0 else float('inf')

    print(f"{turb:>10s} | {mean_A:14.6e} | {mean_B:14.6e} | "
          f"{mean_D:14.6e} | {ratio_BA:10.2f}x | {ratio_BD:12.2f}x")

    # Per-seed detail for outliers
    any_big = any(b / a > 100 if a > 0 else False for a, b in zip(bers_A, bers_B))
    if any_big:
        print(f"  Per-seed ratios (B/A): ", end="")
        ratios = [b/a if a > 0 else float('inf') for a, b in zip(bers_A, bers_B)]
        print(f"median={np.median(ratios):.1f}x  "
              f"min={min(ratios):.1f}x  max={max(ratios):.1f}x")

print()
print("=" * 80)
print("INTERPRETATION:")
print("  Formula A:  pe = np.unwrap(np.angle(avg)) / M      <- correct")
print("  Formula B:  pe = np.unwrap(np.angle(avg) * M) / M  <- buggy")
print("  Ratio B/A >> 1  =>  Formula B degrades BER significantly")
print("=" * 80)
