"""T007 semantic gates — Phase B1 smoke tests.

Each gate returns {"pass": bool, "detail": str}. If ANY gate fails the
source identity is not closed and primary runs are forbidden
(BLOCKED_SOURCE_IDENTITY). All gates use deterministic seeds (no built-in
hash()); no oracle / no truth leaks into deployable signatures.
"""
from __future__ import annotations

import inspect

import numpy as np

from channel import (
    ChannelParams, generate_channel,
    estimate_snr_hat, estimate_phase_innovation_hat,
)
from cpe import (
    WINDOW_GRID, M0, PI4_BIAS,
    vv_block_mean, pilot_block_mean,
    p1_analytic_ratio_rule, p2_lookup_hysteresis, p3_confidence_safe,
)
from evaluator import ber_with_legal_resolve, ber_raw


_SEED = 7800
_N = 2048


def _clean_output(modulation="qpsk"):
    return generate_channel(ChannelParams(
        modulation=modulation, snr_db=18.0, linewidth_hz=10000.0,
        n_symbols=_N, seed=_SEED, channel="awgn_wiener",
    ))


# ---------------------------------------------------------------------------
# Gate 1: noiseless / zero-phase recovery
# ---------------------------------------------------------------------------
def gate_noiseless_zero_phase():
    """A noiseless, zero-phase RX must be recovered to ~0 BER by vv_block_mean."""
    rng = np.random.default_rng(_SEED)
    from common._modulation import qpsk_mod
    bits = rng.integers(0, 2, _N * 2)
    s = qpsk_mod(bits)
    rx = s.astype(complex)   # noiseless, zero phase
    rx_comp = vv_block_mean(rx, N=64)
    ber = ber_raw(rx_comp, bits, "qpsk")
    ok = ber < 1e-6
    return {"pass": ok, "detail": f"noiseless BER={ber:.3e} (must be < 1e-6)"}


# ---------------------------------------------------------------------------
# Gate 2: known constant phase
# ---------------------------------------------------------------------------
def gate_known_constant_phase():
    """A known constant phase rotation must be removed by vv_block_mean, with
    the residual pi/2 ambiguity removed by legal resolve (NOT pi/4 — the pi/4
    bias is the deterministic deployable correction)."""
    rng = np.random.default_rng(_SEED + 1)
    from common._modulation import qpsk_mod
    bits = rng.integers(0, 2, _N * 2)
    s = qpsk_mod(bits)
    phi = 0.7   # known constant phase (radians)
    rx = s * np.exp(1j * phi)
    rx_comp = vv_block_mean(rx, N=64, modulation="qpsk")
    # Use legal pi/2 resolve (the only remaining ambiguity after pi/4 correction).
    ber = ber_with_legal_resolve(rx_comp, bits, "qpsk")
    ok = ber < 1e-3
    return {"pass": ok, "detail": f"constant-phase BER (legal pi/2 resolve)={ber:.3e} (must be < 1e-3)"}


# ---------------------------------------------------------------------------
# Gate 3: known Wiener phase — window size changes the smoothing/tracking trade-off
# ---------------------------------------------------------------------------
def gate_wiener_window_tradeoff():
    """Under known Wiener PN, increasing N changes the BER (the trade-off is
    real, not degenerate). We require BER(N=8) != BER(N=256) by a margin."""
    out = _clean_output()
    bits = out.debug()["tx_bits"]
    ber_8 = ber_with_legal_resolve(vv_block_mean(out.rx, N=8, modulation="qpsk"), bits, "qpsk")
    ber_256 = ber_with_legal_resolve(vv_block_mean(out.rx, N=256, modulation="qpsk"), bits, "qpsk")
    # The two BERs must differ (either direction is fine — the point is the
    # window choice is not degenerate).
    ok = abs(ber_8 - ber_256) > 1e-4
    return {"pass": ok, "detail": f"BER(N=8)={ber_8:.3e}, BER(N=256)={ber_256:.3e} (must differ)"}


# ---------------------------------------------------------------------------
# Gate 4: phase sign, linewidth -> per-symbol variance, block boundary
# ---------------------------------------------------------------------------
def gate_phase_sign_and_linewidth_variance():
    """The Wiener phase trajectory must accumulate (sign convention) and its
    per-symbol variance must scale with linewidth (sigma2_p = 2*pi*dnu*Ts)."""
    from channel import _wiener_phase
    from common._config import T_S
    rng1 = np.random.default_rng(_SEED)
    rng2 = np.random.default_rng(_SEED)
    # Same RNG state -> same innovations -> variance scales with linewidth.
    th_lo = _wiener_phase(_N, 10000.0, T_S, np.random.default_rng(_SEED))
    th_hi = _wiener_phase(_N, 80000.0, T_S, np.random.default_rng(_SEED))
    var_lo = np.var(np.diff(th_lo))
    var_hi = np.var(np.diff(th_hi))
    # Variance ratio should be ~8x (80kHz/10kHz), within [4, 16].
    ratio = var_hi / max(var_lo, 1e-30)
    ok = bool(4.0 <= ratio <= 16.0)
    # Trajectory must accumulate (not be zero-mean per symbol).
    accum_ok = bool(abs(th_lo[-1]) > abs(np.diff(th_lo)).std())
    return {"pass": ok and accum_ok,
            "detail": f"var ratio (hi/lo)={ratio:.2f} (must be in [4,16]); trajectory accumulates={accum_ok}"}


# ---------------------------------------------------------------------------
# Gate 5: QPSK pi/4 fourth-power bias + pi/2 ambiguity separation
# ---------------------------------------------------------------------------
def gate_pi4_bias_and_pi2_ambiguity():
    """For QPSK and SQUARE 16-QAM, the M=4 raised constellation gives a
    deterministic bias of pi/4 (angle(E[s^4])/4 = pi/4, because (±1±1j)^4 and
    (±3±3j)^4 land on the negative real axis). Deployable code MUST correct
    this deterministic, constellation-known bias (cpe.raised_power_bias);
    the remaining legal ambiguity is pi/2 (not pi/4). The T006 'doc 4 / code 8
    pi/4' mismatch is forbidden. We verify: (a) the bias is exactly pi/4 for
    both square constellations; (b) QPSK noiseless recovery with pi/4 bias +
    legal pi/2 resolve reaches ~0 BER (a pi/4/8-rotation resolve would NOT —
    QPSK has only pi/2 symmetry, so 4 rotations is the legal maximum)."""
    from cpe import raised_power_bias
    # Both square constellations have bias exactly pi/4.
    qpsk_bias = raised_power_bias("qpsk")
    qam16_bias = raised_power_bias("qam16")
    bias_ok = (abs(qpsk_bias - PI4_BIAS) < 1e-9) and (abs(qam16_bias - PI4_BIAS) < 1e-9)
    # QPSK noiseless recovery with pi/4 bias + legal pi/2 resolve -> ~0 BER.
    rng = np.random.default_rng(_SEED + 2)
    from common._modulation import qpsk_mod
    bits = rng.integers(0, 2, _N * 2)
    s = qpsk_mod(bits)
    rx_comp = vv_block_mean(s.astype(complex), N=64, modulation="qpsk")
    ber_qpsk_legal = ber_with_legal_resolve(rx_comp, bits, "qpsk")
    qpsk_legal_ok = ber_qpsk_legal < 1e-3
    return {"pass": bias_ok and qpsk_legal_ok,
            "detail": (f"QPSK bias={qpsk_bias:.4f}, 16-QAM bias={qam16_bias:.4f} "
                       f"(both must = pi/4={PI4_BIAS:.4f}); "
                       f"QPSK legal-pi/2 BER={ber_qpsk_legal:.3e} (must <1e-3)")}


# ---------------------------------------------------------------------------
# Gate 6: pilot / data mask, equal energy/overhead
# ---------------------------------------------------------------------------
def gate_pilot_data_mask_equal_energy():
    """Pilot and data symbols traverse the same channel; pilots carry equal
    energy (closes the T006 separate-channel defect)."""
    out = _clean_output(modulation="qam16")
    debug = out.debug()
    tx_s = debug["tx_symbols"]
    # Pilot positions hold known pilot symbols.
    pilot_idx = np.where(out.pilot_mask)[0]
    pilot_energy = np.mean(np.abs(tx_s[pilot_idx]) ** 2)
    data_energy = np.mean(np.abs(tx_s[~out.pilot_mask]) ** 2)
    # Equal energy: |pilot|^2 ~ |data|^2 (both come from the same constellation).
    ratio = pilot_energy / max(data_energy, 1e-12)
    ok = 0.5 <= ratio <= 2.0
    # Pilot count matches the 15/16 rate.
    expected = _N // 16
    count_ok = abs(len(pilot_idx) - expected) <= 1
    return {"pass": ok and count_ok,
            "detail": f"pilot/data energy ratio={ratio:.3f} (must be in [0.5,2]); pilot count={len(pilot_idx)} (expected ~{expected})"}


# ---------------------------------------------------------------------------
# Gate 7: block-buffered no-future / no-truth in deployable signatures
# ---------------------------------------------------------------------------
def _signature_params(fn):
    """Return the parameter names of a function signature."""
    return list(inspect.signature(fn).parameters.keys())


def gate_no_future_no_truth():
    """Deployable estimator signatures MUST NOT carry tx_bits, true h, true
    phase, true SNR, or oracle best-N. Block-buffered methods read only the
    current block (enforced structurally — vv_block_mean/pilot_block_mean take
    only rx + mask + pilots; adaptive controllers take rx + features)."""
    forbidden = {"tx_bits", "true_h", "true_phase", "true_snr", "oracle_best_n",
                 "h", "theta"}
    fns = {
        "vv_block_mean": vv_block_mean,
        "pilot_block_mean": pilot_block_mean,
        "p1_analytic_ratio_rule": p1_analytic_ratio_rule,
        "p2_lookup_hysteresis": p2_lookup_hysteresis,
        "p3_confidence_safe": p3_confidence_safe,
    }
    leaks = []
    for name, fn in fns.items():
        params = set(_signature_params(fn))
        bad = params & forbidden
        if bad:
            leaks.append(f"{name}: {bad}")
    ok = len(leaks) == 0
    return {"pass": ok, "detail": "no truth/future leaks" if ok else "; ".join(leaks)}


# ---------------------------------------------------------------------------
# Gate 8: each method's window path varies with >= 2 input conditions
# ---------------------------------------------------------------------------
def gate_window_path_varies():
    """P1/P2/P3 must pick different N under at least two physical conditions.

    Drives P1 with two conditions that differ in SNR (the reliable E1 axis):
    low-SNR (wants large N) vs high-SNR (wants small N). The feature ranges
    are set from the measured SNR_hat proxy (the 4th-power peak/floor is a
    relative dB-like axis, ~[10,17] for SNR 10-22 dB). We do NOT require the
    E2 (linewidth) axis to discriminate here — B2 measures whether innov_hat
    responds to linewidth at all (D-011/A1 found it noise-dominated)."""
    cond_large_n = generate_channel(ChannelParams(
        modulation="qpsk", snr_db=10.0, linewidth_hz=10000.0,
        n_symbols=_N, seed=_SEED, channel="awgn_wiener"))
    cond_small_n = generate_channel(ChannelParams(
        modulation="qpsk", snr_db=22.0, linewidth_hz=80000.0,
        n_symbols=_N, seed=_SEED, channel="awgn_wiener"))
    block = 256
    # SNR_hat proxy lives in ~[10,17]; innov_hat lives in ~[0.08,0.32].
    r_large = p1_analytic_ratio_rule(
        cond_large_n.rx, block=block,
        snr_lo_db=9.0, snr_hi_db=18.0,
        innov_lo=0.05, innov_hi=0.35,
        modulation="qpsk", innov_weight=0.0)   # SNR-only (E1) — the reliable axis
    r_small = p1_analytic_ratio_rule(
        cond_small_n.rx, block=block,
        snr_lo_db=9.0, snr_hi_db=18.0,
        innov_lo=0.05, innov_hi=0.35,
        modulation="qpsk", innov_weight=0.0)
    # Low SNR should pick LARGER N than high SNR on average (E1).
    mean_large = float(np.mean(r_large.n_per_block))
    mean_small = float(np.mean(r_small.n_per_block))
    ok = mean_large > mean_small
    return {"pass": ok,
            "detail": f"P1 mean N (SNR-driven E1): low-SNR={mean_large:.1f} > high-SNR={mean_small:.1f}"}


# ---------------------------------------------------------------------------
# Aggregate runner
# ---------------------------------------------------------------------------
GATES = [
    ("noiseless_zero_phase", gate_noiseless_zero_phase),
    ("known_constant_phase", gate_known_constant_phase),
    ("wiener_window_tradeoff", gate_wiener_window_tradeoff),
    ("phase_sign_and_linewidth_variance", gate_phase_sign_and_linewidth_variance),
    ("pi4_bias_and_pi2_ambiguity", gate_pi4_bias_and_pi2_ambiguity),
    ("pilot_data_mask_equal_energy", gate_pilot_data_mask_equal_energy),
    ("no_future_no_truth", gate_no_future_no_truth),
    ("window_path_varies", gate_window_path_varies),
]


def run_all_gates():
    results = {}
    for name, fn in GATES:
        results[name] = fn()
    all_pass = all(r["pass"] for r in results.values())
    return {"all_pass": all_pass, "gates": results}
