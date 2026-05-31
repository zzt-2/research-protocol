#!/usr/bin/env python3
"""Carrier sync verification script — 5 checks for potential bugs.

Runs:
  V1: AWGN baseline — BER vs theory Q(sqrt(2*gamma))
  V2: FOE-only BER analysis — residual phase statistics
  V3: VV on known linear-phase signal (no noise, no turbulence)
  V4: resolve_qpsk vs direct demod comparison
  V5: D2 ablation with direct demod (no resolve_qpsk)
"""

import numpy as np
from scipy.special import erfc
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sim_ch4_systematic_analysis import (
    generate_signal, generate_signal_awgn,
    chain_foe_vv, chain_foe_bps, chain_foe_dpll,
    ber_count, resolve_qpsk, qpsk_mod, qpsk_demod,
    fft_foe, vv_cpr, dpll_track, amp_limit,
    doppler_phase, apply_foe,
    R_SYM, T_S, F_RES, F_DOT, LASER_LW, TURB, DEF_NFFT, DEF_MVV, DEF_NW_BPS, DEF_WN, ZETA,
)

np.set_printoptions(precision=6, suppress=True)

SEP = "=" * 70

# ═══════════════════════════════════════════════════════════════
# V1: AWGN baseline
# ═══════════════════════════════════════════════════════════════
def verify_v1():
    print(SEP)
    print("V1: AWGN Baseline — BER vs Theory")
    print(SEP)

    Ns = 10000
    snrs_db = [10, 15, 20]

    print(f"\n{'SNR(dB)':>8} | {'VV BER':>12} | {'BPS BER':>12} | {'DPLL BER':>12} | {'Theory':>12} | {'VV/Theory':>10}")
    print("-" * 80)

    for snr_db in snrs_db:
        gamma = 10**(snr_db / 10)
        # Theory: Q(sqrt(2*gamma)) = 0.5 * erfc(sqrt(gamma))
        ber_theory = 0.5 * erfc(np.sqrt(gamma))

        n_trials = 20
        bers_vv, bers_bps, bers_dpll = [], [], []
        for t in range(n_trials):
            rx, bits = generate_signal_awgn(Ns, snr_db, seed=100+t)

            rx_vv = chain_foe_vv(rx)
            rx_bps = chain_foe_bps(rx)
            rx_dpll = chain_foe_dpll(rx)

            bers_vv.append(ber_count(bits, rx_vv))
            bers_bps.append(ber_count(bits, rx_bps))
            bers_dpll.append(ber_count(bits, rx_dpll))

        mean_vv = np.mean(bers_vv)
        mean_bps = np.mean(bers_bps)
        mean_dpll = np.mean(bers_dpll)

        ratio = mean_vv / ber_theory if ber_theory > 0 else float('inf')

        print(f"{snr_db:>8} | {mean_vv:>12.6e} | {mean_bps:>12.6e} | {mean_dpll:>12.6e} | {ber_theory:>12.6e} | {ratio:>10.3f}")

    print("\nExpected: BER close to theory (within ~2x for finite Ns).")
    print("If BER >> theory, CPR is corrupting the signal.")

    # Also test: raw signal with known phase removed (oracle)
    print("\n--- Oracle test: remove exact phase, no CPR ---")
    for snr_db in [10, 15, 20]:
        gamma = 10**(snr_db / 10)
        ber_theory = 0.5 * erfc(np.sqrt(gamma))
        bers = []
        for t in range(20):
            np.random.seed(100+t)
            bits = np.random.randint(0, 2, 2*Ns)
            tx = qpsk_mod(bits)
            # Same doppler_phase as generate_signal_awgn
            phi = doppler_phase(Ns)
            # AWGN noise
            noise = np.sqrt(1/(2*gamma)) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
            rx = tx * np.exp(1j * phi) + noise
            # Oracle: remove exact phase
            rx_oracle = rx * np.exp(-1j * phi)
            bers.append(ber_count(bits, rx_oracle))
        print(f"  SNR={snr_db}dB: oracle BER = {np.mean(bers):.6e}, theory = {ber_theory:.6e}, ratio = {np.mean(bers)/ber_theory:.3f}")


# ═══════════════════════════════════════════════════════════════
# V2: FOE-only BER analysis
# ═══════════════════════════════════════════════════════════════
def verify_v2():
    print(f"\n{SEP}")
    print("V2: FOE-only BER Analysis — Residual Phase Statistics")
    print(SEP)

    Ns = 10000
    gamma_bar_db = 20

    # Generate signal with turbulence
    for turb_name in ['weak', 'strong']:
        print(f"\n--- {turb_name} turbulence ---")
        n_trials = 20
        bers_foe = []
        phase_residuals_all = []

        for t in range(n_trials):
            rx, bits = generate_signal(Ns, turb_name, gamma_bar_db, seed=200+t)

            # FOE only
            fo_est = fft_foe(rx, N_fft=DEF_NFFT)
            k = np.arange(Ns)
            rx_foe = rx * np.exp(-1j * fo_est * k)

            ber = ber_count(bits, rx_foe)
            bers_foe.append(ber)

            # Compute residual phase error
            # Get true tx constellation points
            tx = qpsk_mod(bits)
            # Residual phase = angle(rx_foe / tx) — but tx has sqrt(h) factor
            # For FOE-only, the residual phase includes: laser PN + Doppler quadratic + turbulence effects
            # We can only check what FOE estimated vs what it should have estimated

        mean_ber = np.mean(bers_foe)
        print(f"  FOE-only BER = {mean_ber:.6f} ({mean_ber*100:.2f}%)")

    # Analytical check: what happens with FOE-only?
    print(f"\n--- Analytical: FOE-only residual phase accumulation ---")
    f_res = F_RES  # 1 MHz
    f_dot = F_DOT  # 150 MHz/s
    Ns = 10000
    T_s = T_S

    # FOE estimates a single frequency offset
    # True phase = 2*pi*f_res*k*T_s + pi*f_dot*(k*T_s)^2 + laser_PN
    # FOE estimates f_res (approximately), but:
    #   - Doppler quadratic term is NOT compensated
    #   - Laser phase noise is NOT compensated
    #   - Turbulence-induced phase is NOT compensated

    k = np.arange(Ns)
    phi_linear = 2 * np.pi * f_res * k * T_s
    phi_quadratic = np.pi * f_dot * (k * T_s)**2

    print(f"  f_res = {f_res/1e6:.1f} MHz, f_dot = {f_dot/1e6:.1f} MHz/s")
    print(f"  T_s = {T_s*1e12:.1f} ps, Ns = {Ns}")
    print(f"  Total linear phase at end: {phi_linear[-1]/(2*np.pi):.1f} cycles = {phi_linear[-1]:.1f} rad")
    print(f"  Total quadratic phase at end: {phi_quadratic[-1]/(2*np.pi):.1f} cycles = {phi_quadratic[-1]:.1f} rad")
    print(f"  Max quadratic phase deviation from linear: {np.max(np.abs(phi_quadratic)):.4f} rad")

    # After FOE removes linear estimate, residual is mainly quadratic
    # Quadratic phase at end of sequence
    phi_q_end = phi_quadratic[-1]
    print(f"  Quadratic phase drift over {Ns} symbols: {phi_q_end:.4f} rad = {np.degrees(phi_q_end):.2f} deg")

    # Simulate: what BER does pure quadratic phase cause?
    print(f"\n  Simulating pure quadratic phase (no noise, no turbulence, no laser PN)...")
    np.random.seed(42)
    bits = np.random.randint(0, 2, 2*Ns)
    tx = qpsk_mod(bits)
    phi = np.pi * f_dot * (k * T_s)**2  # only quadratic
    rx = tx * np.exp(1j * phi)
    ber_quad = ber_count(bits, rx)
    print(f"  BER from quadratic phase alone (no noise) = {ber_quad:.6f} ({ber_quad*100:.2f}%)")

    # Also check linear phase alone
    phi_lin_only = 2 * np.pi * f_res * k * T_s
    rx_lin = tx * np.exp(1j * phi_lin_only)
    ber_lin = ber_count(bits, rx_lin)
    print(f"  BER from linear phase alone (f_res={f_res/1e6}MHz, no noise) = {ber_lin:.6f} ({ber_lin*100:.2f}%)")


# ═══════════════════════════════════════════════════════════════
# V3: VV on known linear-phase signal
# ═══════════════════════════════════════════════════════════════
def verify_v3():
    print(f"\n{SEP}")
    print("V3: VV on Known Linear-Phase Signal (No Noise, No Turbulence)")
    print(SEP)

    Ns = 10000

    # Test with different residual frequencies
    f_res_vals = [0.5e6, 1e6, 2e6, 5e6]

    print(f"\n{'f_res(MHz)':>12} | {'BER(VV)':>12} | {'BER(DPLL)':>12} | {'BER(BPS)':>12} | {'BER(FOE+VV)':>12}")
    print("-" * 75)

    for f_res in f_res_vals:
        np.random.seed(42)
        bits = np.random.randint(0, 2, 2*Ns)
        tx = qpsk_mod(bits)

        k = np.arange(Ns)
        phi = 2 * np.pi * f_res * k * T_S  # pure linear phase
        rx = tx * np.exp(1j * phi)

        # VV directly (no FOE)
        rx_vv, pe_vv = vv_cpr(rx, Nw=DEF_MVV)
        ber_vv = ber_count(bits, rx_vv)

        # DPLL directly (no FOE)
        rx_dpll, pe_dpll = dpll_track(rx, omega_n=DEF_WN)
        ber_dpll = ber_count(bits, rx_dpll)

        # BPS directly (no FOE)
        from sim_ch4_systematic_analysis import bps_cpr
        rx_bps, pe_bps = bps_cpr(rx, Nw=DEF_NW_BPS)
        ber_bps = ber_count(bits, rx_bps)

        # FOE + VV
        rx_foe_vv = chain_foe_vv(rx)
        ber_foe_vv = ber_count(bits, rx_foe_vv)

        print(f"{f_res/1e6:>12.1f} | {ber_vv:>12.6e} | {ber_dpll:>12.6e} | {ber_bps:>12.6e} | {ber_foe_vv:>12.6e}")

    # Also test: VV phase estimation quality
    print(f"\n--- VV phase estimation quality (f_res=1MHz) ---")
    np.random.seed(42)
    bits = np.random.randint(0, 2, 2*Ns)
    tx = qpsk_mod(bits)
    k = np.arange(Ns)
    f_res = 1e6
    phi_true = 2 * np.pi * f_res * k * T_S
    rx = tx * np.exp(1j * phi_true)

    rx_vv, pe_vv = vv_cpr(rx, Nw=DEF_MVV)
    phase_err = np.angle(rx_vv * np.conj(tx))  # residual phase after VV
    print(f"  VV residual phase: mean={np.mean(phase_err):.6f} rad, std={np.std(phase_err):.6f} rad")
    print(f"  VV residual phase: max={np.max(np.abs(phase_err)):.6f} rad")
    print(f"  True phase range: [{phi_true[0]:.4f}, {phi_true[-1]:.4f}] rad = {phi_true[-1]/(2*np.pi):.1f} cycles")

    # Check: does np.unwrap handle 4th-power ambiguity correctly?
    # VV does: raised = rx^4, avg, then unwrap(angle(avg))/4
    # For pure linear phase at 1MHz over 10000 symbols at 2.5Gsps:
    total_phase = 2 * np.pi * f_res * (Ns-1) * T_S
    print(f"\n  Total phase rotation: {total_phase:.2f} rad = {total_phase/(2*np.pi):.2f} cycles")
    print(f"  After x4: {total_phase*4:.2f} rad = {total_phase*4/(2*np.pi):.2f} cycles")
    print(f"  Number of 2pi wraps in 4th power: {total_phase*4/(2*np.pi):.1f}")
    print(f"  Number of pi/4 (45 deg) boundaries in true phase: {total_phase/(np.pi/4):.1f}")

    # Test with resolve_qpsk
    ber_resolve = resolve_qpsk(rx_vv, bits)
    ber_direct = ber_count(bits, rx_vv)
    print(f"\n  VV BER with resolve_qpsk: {ber_resolve:.6e}")
    print(f"  VV BER with direct demod: {ber_direct:.6e}")


# ═══════════════════════════════════════════════════════════════
# V4: resolve_qpsk vs direct demod
# ═══════════════════════════════════════════════════════════════
def verify_v4():
    print(f"\n{SEP}")
    print("V4: resolve_qpsk vs Direct Demod Comparison")
    print(SEP)

    Ns = 10000

    # Test on turbulent signal at 20dB
    for turb_name in ['weak', 'strong']:
        print(f"\n--- {turb_name} turbulence, 20dB ---")
        n_trials = 10
        for method_name, chain_fn in [('FOE+VV', chain_foe_vv),
                                       ('FOE+DPLL', chain_foe_dpll)]:
            bers_resolve = []
            bers_direct = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, turb_name, 20, seed=300+t)
                rx_rec = chain_fn(rx)
                bers_resolve.append(resolve_qpsk(rx_rec, bits))
                bers_direct.append(ber_count(bits, rx_rec))

            r_mean = np.mean(bers_resolve)
            d_mean = np.mean(bers_direct)
            print(f"  {method_name:>10}: resolve_qpsk={r_mean:.6f}, direct={d_mean:.6f}, ratio={d_mean/r_mean if r_mean > 0 else float('inf'):.3f}")

    # Also test FOE-only
    print(f"\n--- FOE-only ---")
    for turb_name in ['weak', 'strong']:
        bers_resolve = []
        bers_direct = []
        for t in range(10):
            rx, bits = generate_signal(Ns, turb_name, 20, seed=300+t)
            rx_foe = apply_foe(rx, DEF_NFFT)
            bers_resolve.append(resolve_qpsk(rx_foe, bits))
            bers_direct.append(ber_count(bits, rx_foe))

        r_mean = np.mean(bers_resolve)
        d_mean = np.mean(bers_direct)
        print(f"  {turb_name:>10}: resolve_qpsk={r_mean:.6f}, direct={d_mean:.6f}, ratio={d_mean/r_mean if r_mean > 0 else float('inf'):.3f}")


# ═══════════════════════════════════════════════════════════════
# V5: D2 ablation with direct demod
# ═══════════════════════════════════════════════════════════════
def verify_v5():
    print(f"\n{SEP}")
    print("V5: D2 Ablation with Direct Demod (No resolve_qpsk)")
    print(SEP)

    Ns = 10000
    gamma_bar_db = 20
    n_trials = 20

    from sim_kf_stress_common import (
        generate_shared_realization, equalize_oracle, run_kf_pilot,
        fft_foe as fft_foe_stress, vv_cpr as vv_cpr_stress,
        dpll_track as dpll_track_stress, DOPPLER_HIGH, F_RESIDUAL,
        GAMMA_BAR_DEFAULT,
    )

    for turb_name in ['weak', 'moderate', 'strong']:
        print(f"\n--- {turb_name} turbulence ---")
        schemes = {
            'FOE_only': [],
            'FOE+VV': [],
            'FOE+DPLL': [],
        }

        for t in range(n_trials):
            # Use systematic analysis generate for consistency
            rx, bits = generate_signal(Ns, turb_name, gamma_bar_db, seed=500+t)
            k = np.arange(Ns)

            # FOE only
            fo_est = fft_foe(rx, N_fft=DEF_NFFT)
            rx_foe = rx * np.exp(-1j * fo_est * k)
            schemes['FOE_only'].append(ber_count(bits, rx_foe))

            # FOE + VV
            rx_vv, _ = vv_cpr(rx_foe, Nw=DEF_MVV)
            schemes['FOE+VV'].append(ber_count(bits, rx_vv))

            # FOE + DPLL
            rx_dpll, _ = dpll_track(rx_foe, omega_n=DEF_WN)
            schemes['FOE+DPLL'].append(ber_count(bits, rx_dpll))

        # Print results
        print(f"  {'Scheme':>12} | {'BER (direct)':>12} | {'BER (resolve)':>12}")
        print(f"  {'-'*12}-+-{'-'*12}-+-{'-'*12}")

        # Also compute with resolve_qpsk for comparison
        for scheme_name in ['FOE_only', 'FOE+VV', 'FOE+DPLL']:
            ber_direct = np.mean(schemes[scheme_name])
            # Rerun with resolve_qpsk
            bers_resolve = []
            for t in range(n_trials):
                rx, bits = generate_signal(Ns, turb_name, gamma_bar_db, seed=500+t)
                k = np.arange(Ns)
                fo_est = fft_foe(rx, N_fft=DEF_NFFT)
                rx_foe = rx * np.exp(-1j * fo_est * k)

                if scheme_name == 'FOE_only':
                    rx_rec = rx_foe
                elif scheme_name == 'FOE+VV':
                    rx_rec, _ = vv_cpr(rx_foe, Nw=DEF_MVV)
                elif scheme_name == 'FOE+DPLL':
                    rx_rec, _ = dpll_track(rx_foe, omega_n=DEF_WN)

                bers_resolve.append(resolve_qpsk(rx_rec, bits))

            ber_resolve = np.mean(bers_resolve)
            print(f"  {scheme_name:>12} | {ber_direct:>12.6f} | {ber_resolve:>12.6f}")


# ═══════════════════════════════════════════════════════════════
# V3b: Detailed VV bug investigation
# ═══════════════════════════════════════════════════════════════
def verify_v3b():
    """Deeper investigation of VV phase unwrapping."""
    print(f"\n{SEP}")
    print("V3b: VV Phase Unwrapping Investigation")
    print(SEP)

    Ns = 1000  # shorter for detailed inspection
    np.random.seed(42)
    bits = np.random.randint(0, 2, 2*Ns)
    tx = qpsk_mod(bits)
    k = np.arange(Ns)

    # Test: slowly varying phase (VV should handle)
    f_res = 1e6
    phi_true = 2 * np.pi * f_res * k * T_S
    rx = tx * np.exp(1j * phi_true)

    # Apply VV manually to inspect
    M = 4
    raised = rx**M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8

    Nw = 64
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')

    # Check: what does the 4th power phase look like?
    phase_4th = np.angle(avg)
    phase_4th_unwrapped = np.unwrap(phase_4th)

    # VV estimate: unwrap(angle) / M
    pe_vv = np.unwrap(np.angle(avg)) / M

    # True phase (for comparison, VV should recover this)
    # True 4th power phase = 4 * phi_true (mod 2pi)
    true_4th_phase = 4 * phi_true
    true_4th_phase_wrapped = (true_4th_phase + np.pi) % (2*np.pi) - np.pi

    print(f"\n  Phase at k=0:   true={phi_true[0]:.6f}, VV_est={pe_vv[0]:.6f}")
    print(f"  Phase at k=100: true={phi_true[100]:.6f}, VV_est={pe_vv[100]:.6f}")
    print(f"  Phase at k=500: true={phi_true[500]:.6f}, VV_est={pe_vv[500]:.6f}")
    print(f"  Phase at k=999: true={phi_true[999]:.6f}, VV_est={pe_vv[999]:.6f}")

    # Residual phase
    residual = pe_vv - phi_true
    # Wrap to [-pi, pi]
    residual_wrapped = (residual + np.pi) % (2*np.pi) - np.pi
    print(f"\n  Residual (VV - true): mean={np.mean(residual_wrapped):.6f}, std={np.std(residual_wrapped):.6f}")
    print(f"  Residual max abs: {np.max(np.abs(residual_wrapped)):.6f}")

    # Now check: after VV correction, what is the BER?
    rx_corrected = rx * np.exp(-1j * pe_vv)
    ber = ber_count(bits, rx_corrected)
    print(f"\n  BER after VV correction (no noise): {ber:.6f}")

    # Check if VV has a constant phase offset
    # For QPSK, VV recovers phase mod pi/2, so there's a pi/2 ambiguity
    # resolve_qpsk should handle this
    ber_resolve = resolve_qpsk(rx_corrected, bits)
    print(f"  BER after VV + resolve_qpsk: {ber_resolve:.6f}")

    # Check: is the VV phase tracking the true phase with a constant offset?
    # If so, resolve_qpsk should give BER=0
    phase_offset = residual_wrapped[Ns//2]  # sample from middle
    print(f"\n  Mid-sequence phase offset: {phase_offset:.6f} rad = {np.degrees(phase_offset):.2f} deg")
    print(f"  Closest pi/2 multiple: {round(phase_offset / (np.pi/2)) * np.pi/2:.6f}")

    # Now test with noise added
    print(f"\n--- VV with AWGN at 20dB ---")
    gamma = 10**(20/10)
    noise = np.sqrt(1/(2*gamma)) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_noisy = rx + noise

    rx_vv, pe_vv_noisy = vv_cpr(rx_noisy, Nw=Nw)
    ber_noisy = ber_count(bits, rx_vv)
    ber_noisy_resolve = resolve_qpsk(rx_vv, bits)
    print(f"  BER (direct): {ber_noisy:.6e}")
    print(f"  BER (resolve): {ber_noisy_resolve:.6e}")

    # Compare: how does VV in common module differ?
    print(f"\n--- Comparing sim_ch4 vs sim_kf_stress VV implementations ---")
    from sim_kf_stress_common import vv_cpr as vv_stress

    np.random.seed(42)
    bits2 = np.random.randint(0, 2, 2*Ns)
    tx2 = qpsk_mod(bits2)
    phi2 = 2 * np.pi * 1e6 * np.arange(Ns) * T_S
    rx2 = tx2 * np.exp(1j * phi2)

    rx_vv1, pe1 = vv_cpr(rx2, Nw=64)
    rx_vv2, pe2 = vv_stress(rx2, Nw=64)

    ber1 = ber_count(bits2, rx_vv1)
    ber2 = ber_count(bits2, rx_vv2)
    print(f"  sim_ch4 VV BER (direct): {ber1:.6e}")
    print(f"  sim_kf_stress VV BER (direct): {ber2:.6e}")
    print(f"  Phase estimates equal? {np.allclose(pe1, pe2)}")
    if not np.allclose(pe1, pe2):
        diff = pe1 - pe2
        print(f"  Max phase diff: {np.max(np.abs(diff)):.6e}")
        # Check which formula is used
        print(f"\n  sim_ch4 VV: np.unwrap(np.angle(avg)) / M")
        print(f"  sim_kf_stress VV: np.unwrap(np.angle(avg) * M) / M")
        print(f"  These are DIFFERENT formulas!")
        print(f"  sim_ch4 divides first, then... no, it's unwrap(angle)/M")
        print(f"  sim_kf_stress does unwrap(angle*M)/M")
        print(f"  For large phases, unwrap(angle*M)/M != unwrap(angle)/M")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip', nargs='*', default=[], help='Tests to skip (v1-v5,v3b)')
    args = parser.parse_args()

    print("Carrier Sync Verification Script")
    print(f"Python: {sys.executable}")

    if 'v1' not in args.skip: verify_v1()
    if 'v2' not in args.skip: verify_v2()
    if 'v3' not in args.skip: verify_v3()
    if 'v4' not in args.skip: verify_v4()
    if 'v5' not in args.skip: verify_v5()
    if 'v3b' not in args.skip: verify_v3b()

    print(f"\n{SEP}")
    print("ALL VERIFICATIONS COMPLETE")
    print(SEP)
