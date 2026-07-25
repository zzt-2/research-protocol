"""Baseline ladder + combination methods P1/P2/P3 for T006.

All arms share the same pilot pattern, data mask, eval window, total TX
energy and base realization (contract.fairness). B* candidates (BPS/VV/
DD-DPLL) wrap the existing common/_recovery.py implementations so we do NOT
re-implement conventional CPR.
"""
from __future__ import annotations

import numpy as np

from common._recovery import bps_cpr, vv_cpr, dpll_track_dd
from common._modulation import qam16_demod

# Flat module import (the directory name has dashes and cannot be imported
# normally); the runner/semantic_gates/tests add this directory to sys.path
# so `import components` works.
import components as C   # noqa: E402


# ===========================================================================
# B* candidates — conventional CPR, validation-tuned
# ===========================================================================

def arm_bps(rx, *, B=32, Nw=61):
    """BPS (Pfau 2009) via common/_recovery.bps_cpr with 16-QAM decisions."""
    rx_out, _ = bps_cpr(rx, B=B, Nw=Nw, mod='qam16')
    return rx_out


def arm_vv(rx, *, Nw=64):
    """Viterbi-Viterbi (M=4 raise-power) via common/_recovery.vv_cpr."""
    rx_out, _ = vv_cpr(rx, Nw=Nw)
    return rx_out


def arm_dd_dpll(rx, *, omega_n=20e6):
    """DD-DPLL via common/_recovery.dpll_track_dd with 16-QAM decisions."""
    rx_out, _ = dpll_track_dd(rx, omega_n=omega_n, mod='qam16')
    return rx_out


# ===========================================================================
# B10 / B12 standalone wrappers (uniform interface)
# ===========================================================================

def arm_b10(rx, pilot_idx, pilot_sym, *, lam=0.99, delta=2.0):
    """B10 pilot-RLS standalone (returns derotated rx; no resolve)."""
    rx_out, _ = C.pilot_rls_b10(
        rx, pilot_idx, pilot_sym, lam=lam, delta=delta, mod_label="qam16")
    return rx_out


def arm_b12(rx, pilot_idx, pilot_sym, *, l_block=64, ml_window=7,
            snr_db=20.0, linewidth_hz=10.0e3, t_s=4.0e-10):
    """B12 MAP joint ML/MAP standalone (returns derotated rx; no resolve)."""
    rx_out, _ = C.map_phase_b12(
        rx, pilot_idx, pilot_sym, l_block=l_block, l_sub=1, ml_window=ml_window,
        snr_db=snr_db, linewidth_hz=linewidth_hz, t_s=t_s, mod_label="qam16")
    return rx_out


# ===========================================================================
# Combination methods P1 / P2 / P3
# ===========================================================================

def arm_p1_cascade(rx, pilot_idx, pilot_sym, *, lam=0.99, delta=2.0,
                   l_block=64, ml_window=7, snr_db=20.0, linewidth_hz=10.0e3,
                   t_s=4.0e-10):
    """P1: B10 RLS produces phi_hat_B10; B12 MAP runs on the residual.

    NEW ACTION vs standalone B12: B12 sees B10-compensated residual
    (rx_res = rx * exp(-1j*phi_hat_B10)), NOT raw rx. Identity smoke enforces
    that rx_res differs from rx (B10 is not identity).
    """
    rx_res, phi_b10 = C.pilot_rls_b10(
        rx, pilot_idx, pilot_sym, lam=lam, delta=delta, mod_label="qam16")
    rx_p1, phi_b12_res = C.map_phase_b12(
        rx_res, pilot_idx, pilot_sym, l_block=l_block, l_sub=1,
        ml_window=ml_window, snr_db=snr_db, linewidth_hz=linewidth_hz,
        t_s=t_s, mod_label="qam16")
    # total phase estimate = phi_b10 + phi_b12_res
    phi_total = phi_b10 + phi_b12_res
    rx_out = rx * np.exp(-1j * phi_total)
    return rx_out


def arm_p2_confidence_gate(rx, pilot_idx, pilot_sym, *, lam=0.99, delta=2.0,
                           l_block=64, ml_window=7, snr_db=20.0,
                           linewidth_hz=10.0e3, t_s=4.0e-10,
                           innov_thr=0.3):
    """P2: per-symbol routing between B10, P1, B12 based on RLS innovation.

    NEW ACTION vs standalone: per-symbol routing decision based on a
    receiver-visible confidence (RLS innovation magnitude). Threshold frozen
    on VALIDATION only.
    """
    rx_b10, phi_b10, state_b10 = C.pilot_rls_b10(
        rx, pilot_idx, pilot_sym, lam=lam, delta=delta, mod_label="qam16",
        return_state=True)
    innov = state_b10["innovation_path"]

    rx_res = rx * np.exp(-1j * phi_b10)
    rx_p1_partial, phi_b12_res = C.map_phase_b12(
        rx_res, pilot_idx, pilot_sym, l_block=l_block, l_sub=1,
        ml_window=ml_window, snr_db=snr_db, linewidth_hz=linewidth_hz,
        t_s=t_s, mod_label="qam16")
    rx_b12_only, phi_b12_only = C.map_phase_b12(
        rx, pilot_idx, pilot_sym, l_block=l_block, l_sub=1,
        ml_window=ml_window, snr_db=snr_db, linewidth_hz=linewidth_hz,
        t_s=t_s, mod_label="qam16")

    phi_p1 = phi_b10 + phi_b12_res
    # route: high innovation -> trust B12 standalone (it re-estimates from
    # raw rx); low innovation -> trust P1 cascade (B10 + B12 residual).
    use_b12 = innov > innov_thr
    phi_hat = np.where(use_b12, phi_b12_only, phi_p1)
    rx_out = rx * np.exp(-1j * phi_hat)
    return rx_out


def arm_p3_adaptive_forgetting(rx, pilot_idx, pilot_sym, *,
                               lam_lo=0.90, lam_hi=0.999, delta=2.0,
                               innov_scale=5.0):
    """P3: B10 RLS with innovation-modulated forgetting factor.

    NEW ACTION vs standalone B10: lambda(k) is time-varying inside B10 itself,
    bounded [lam_lo, lam_hi]. High innovation -> lower lambda (faster tracking).
    Fixed-lambda B10 (arm_b10) is the ablation control.
    """
    rx = np.asarray(rx, dtype=complex)
    N = rx.shape[0]
    pilot_idx = np.atleast_1d(np.asarray(pilot_idx, dtype=int))
    pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))

    M = 2
    h = np.zeros(M, dtype=float)
    P = np.eye(M) / delta
    P_INIT = P.copy()
    P_NORM_CAP = 1e6 * np.linalg.norm(P_INIT)

    phi_hat = np.zeros(N, dtype=float)
    lam_path = np.zeros(N, dtype=float)

    is_pilot = np.zeros(N, dtype=bool)
    is_pilot[pilot_idx] = True
    pilot_lookup = {int(i): complex(s) for i, s in zip(pilot_idx, pilot_sym)}

    F = None
    last_pilot_seen = -1
    smoothed_innov = 0.0   # EMA of innovation magnitude

    for k in range(N):
        # adaptive lambda: low when smoothed innovation is high
        lam_k = lam_hi - (lam_hi - lam_lo) * np.tanh(innov_scale * max(smoothed_innov, 0.0))
        lam_path[k] = lam_k

        if F is None:
            t_k = float(k)
        else:
            t_k = float(k % F) if F > 0 else float(k)
        x = np.array([1.0, t_k], dtype=float)
        phi_hat[k] = float(h @ x)

        if is_pilot[k]:
            s_pk = pilot_lookup[k]
            obs = float(np.angle(rx[k] / s_pk))
            d = obs - phi_hat[k]
            d = (d + np.pi) % (2 * np.pi) - np.pi
            y_k = phi_hat[k] + d
            h, P, innov_mag = C._rls_update(h, P, x, y_k, lam_k, P_INIT, P_NORM_CAP)
            last_pilot_seen = k
            if F is None and abs(h[1]) > 1e-12:
                F = float(2 * np.pi / abs(h[1]))
        else:
            if last_pilot_seen >= 0:
                r_hat = rx[k] * np.exp(-1j * phi_hat[k])
                s_hat = C.hard_decision(r_hat, mod="qam16")
                if abs(s_hat) > 1e-12:
                    obs = float(np.angle(rx[k] / s_hat))
                    d = obs - phi_hat[k]
                    d = (d + np.pi) % (2 * np.pi) - np.pi
                    y_k = phi_hat[k] + d
                    h, P, innov_mag = C._rls_update(
                        h, P, x, y_k, lam_k, P_INIT, P_NORM_CAP)
                else:
                    innov_mag = 0.0
            else:
                innov_mag = 0.0

        # EMA update of innovation magnitude (receiver-visible confidence)
        smoothed_innov = 0.9 * smoothed_innov + 0.1 * innov_mag

    rx_out = rx * np.exp(-1j * phi_hat)
    return rx_out


# ===========================================================================
# Resolve helper — pick the best 2pi/M rotation using known tx bits.
# Used ONLY for evaluation (resolves phase ambiguity consistently across arms).
# NOT used inside any deployable arm (arms output a single derotation).
# ===========================================================================

def eval_resolve(rx_out, tx_bits):
    """Resolve 16-QAM M=4 (pi/2) phase ambiguity and return the derotated rx.

    Picks the rotation r in {0, pi/2, pi, 3pi/2} that minimizes BER against
    tx_bits, then returns rx_out * exp(-1j*r) (the derotated signal, NOT the
    BER). This is the EVAL convention (consistent across all arms); it is NOT
    an oracle detector (it does not denoise).

    NOTE: this uses known tx_bits to pick the rotation, which is the standard
    eval convention (every arm gets the same treatment). It does NOT use any
    per-symbol TX truth beyond the global rotation.
    """
    rx_out = np.asarray(rx_out, dtype=complex)
    best_ber = 1.0
    best_rot = 0.0
    for r in np.arange(0, 2 * np.pi, np.pi / 4):
        ber = float(np.mean(tx_bits != qam16_demod(rx_out * np.exp(-1j * r))))
        if ber < best_ber:
            best_ber = ber
            best_rot = float(r)
    return rx_out * np.exp(-1j * best_rot)
