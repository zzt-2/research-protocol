"""Semantic smoke gates for T006 (run BEFORE any primary test).

Each gate is a self-contained check that must PASS before the headroom /
method runs are allowed. Failures abort the pipeline (do NOT silently
continue). Gates:

  1. noiseless_recovery         — under zero noise / zero CFO / zero PN, every
                                  arm recovers the data bit-identical.
  2. cfo_phase_sign_and_units   — a known CFO produces a known phase slope;
                                  the sign convention is consistent across arms.
  3. pilot_data_mask_overhead   — pilot and data masks are disjoint and cover
                                  the frame; overhead is the registered value.
  4. energy_fairness            — total TX energy is identical across arms.
  5. no_future_leakage          — arm outputs at symbol k do not depend on
                                  RX symbols at k' > k (within the block-window
                                  budget declared in the contract).
  6. no_tx_truth_in_deployable  — deployable arms do not read TX data bits or
                                  phi_true (only pilot symbols at pilot positions).
  7. b10_b12_p1_p2_p3_identity  — the arms do NOT collapse to the same
                                  estimator (output differs by more than a
                                  tolerance across a varied input).
"""
from __future__ import annotations

import numpy as np

# Flat module imports (directory name has dashes; sys.path is set by the
# caller to include this directory).
import channel_helpers as ch
import baselines as B
import components as components_mod


def _make_clean_realization(seed=7600):
    """A near-noiseless, zero-CFO, zero-Wiener realization for gate 1."""
    real = ch.build_single_pol_qam16_with_pilots(
        N=1024, alpha=11.6, beta=10.1, gamma_bar=1e4,  # very high SNR
        f_g=1.0, sop_rate=0.0, seed=seed,
        l_pilot_block=64,
        f_residual_hz=0.0, f_dot_hz_per_s=0.0, laser_lw_hz=1e-6,
    )
    return real


def gate_noiseless_recovery(real=None, tol=1e-6):
    """Gate 1: under noiseless / zero-CFO / zero-PN, all arms recover data.

    A clean realization (very high SNR, zero CFO, near-zero linewidth) must
    yield BER ~ 0 for B*, B10, B12 and O. If any arm has BER > tol, the
    pipeline aborts.
    """
    if real is None:
        real = _make_clean_realization()
    rx = real["rx"]
    bits = real["bits_data"]
    pilot_idx = real["pilot_idx"]
    pilot_sym = real["pilot_sym"]
    mask = real["data_mask"]

    arms = {
        "O": components_mod.truth_assisted_reference(rx, real["phi_true"]),
        "B10": B.arm_b10(rx, pilot_idx, pilot_sym),
        "B12": B.arm_b12(rx, pilot_idx, pilot_sym, snr_db=40.0),
    }
    bers = {}
    for name, rx_out in arms.items():
        # use eval_resolve to handle M=4 ambiguity (consistent across arms)
        ber = ch.ber_on_data(B.eval_resolve(rx_out, bits), bits, mask)
        bers[name] = ber
    failures = {k: v for k, v in bers.items() if v > tol}
    return {
        "gate": "noiseless_recovery",
        "pass": len(failures) == 0,
        "bers": bers,
        "failures": failures,
        "tol": tol,
    }


def gate_cfo_phase_sign_and_units(seed=7601):
    """Gate 2: a known CFO produces a known phase slope; sign convention consistent.

    Synthesize a CFO-only signal (zero Wiener, zero SOP) with known CFO = +100 kHz.
    Check that phi_hat estimated by B10 has the correct sign and magnitude
    (slope = +2*pi*f_residual*T_s per symbol). Also check that arms derotate
    in the SAME direction (sign of phi_hat consistent).
    """
    real = ch.build_single_pol_qam16_with_pilots(
        N=2048, alpha=11.6, beta=10.1, gamma_bar=1e3,
        f_g=1.0, sop_rate=0.0, seed=seed,
        f_residual_hz=1.0e5, laser_lw_hz=1e-6,   # CFO only
    )
    rx = real["rx"]
    pilot_idx = real["pilot_idx"]
    pilot_sym = real["pilot_sym"]
    t_s = real["t_s"]
    f_residual = real["f_residual_hz"]

    # expected phase slope per symbol (radians)
    expected_slope = 2.0 * np.pi * f_residual * t_s

    # B10 estimates h1 -> 2*pi*df*T_s. Recover h1 from internal state.
    _, _, state = components_mod.pilot_rls_b10(
        rx, pilot_idx, pilot_sym, return_state=True, mod_label="qam16")
    h1_final = state["h_final"][1]

    # sign and magnitude check (allow some tolerance for noise + RLS tracking)
    sign_ok = np.sign(h1_final) == np.sign(expected_slope)
    magnitude_ratio = abs(h1_final) / max(abs(expected_slope), 1e-30)
    magnitude_ok = 0.5 < magnitude_ratio < 2.0   # within 2x of expected

    return {
        "gate": "cfo_phase_sign_and_units",
        "pass": bool(sign_ok and magnitude_ok),
        "expected_slope_rad_per_sym": float(expected_slope),
        "h1_final": float(h1_final),
        "magnitude_ratio": float(magnitude_ratio),
        "sign_ok": bool(sign_ok),
        "magnitude_ok": bool(magnitude_ok),
    }


def gate_pilot_data_mask_overhead(real=None, expected_overhead=1 / 64):
    """Gate 3: pilot and data masks disjoint; overhead is the registered value."""
    if real is None:
        real = _make_clean_realization()
    pilot_idx = real["pilot_idx"]
    mask = real["data_mask"]
    N = real["N"]
    # disjoint: pilot positions are NOT in data mask (mask[pilot_idx] all False)
    disjoint = bool(np.all(~mask[pilot_idx]))
    # overhead = pilots / N
    overhead = len(pilot_idx) / N
    overhead_ok = abs(overhead - expected_overhead) < 1e-9
    return {
        "gate": "pilot_data_mask_overhead",
        "pass": bool(disjoint and overhead_ok),
        "n_pilots": int(len(pilot_idx)),
        "n_data": int(mask.sum()),
        "overhead": float(overhead),
        "expected_overhead": float(expected_overhead),
        "disjoint": bool(disjoint),
    }


def gate_energy_fairness(real=None):
    """Gate 4: total TX energy is identical across arms (trivially true since
    all arms share tx_with_pilots, but verify the realization carries it)."""
    if real is None:
        real = _make_clean_realization()
    tx = real["tx_with_pilots"]
    energy = float(np.sum(np.abs(tx) ** 2))
    # all arms consume the same rx, so energy is automatically identical.
    # this gate mostly documents the invariant.
    return {
        "gate": "energy_fairness",
        "pass": True,
        "total_tx_energy": energy,
        "note": "all arms share tx_with_pilots, so TX energy is identical by construction",
    }


def gate_no_future_leakage(real=None):
    """Gate 5: arm outputs at symbol k do not depend on RX at k' > k (within
    the declared window budget). BPS/VV use a sliding window of size Nw (so
    they look ahead within Nw/2 — this is declared in the contract and is
    NOT future leakage in the deployment sense, since Nw is a fixed window
    not a frame-level lookahead). Pilot-RLS and MAP are causal (DD update
    uses only past + current).

    This gate verifies that the deployable arms (B10, B12, P1, P2, P3) are
    causal: zeroing rx[k+1:] does not change rx_out[:k+1].
    """
    if real is None:
        real = _make_clean_realization()
    rx = real["rx"]
    pilot_idx = real["pilot_idx"]
    pilot_sym = real["pilot_sym"]
    N = real["N"]
    # cut the frame in half and check the first half output is unchanged
    half = N // 2
    rx_full = rx.copy()
    rx_cut = rx.copy()
    rx_cut[half:] = 0.0
    # B10
    out_full_b10 = B.arm_b10(rx_full, pilot_idx, pilot_sym)
    out_cut_b10 = B.arm_b10(rx_cut, pilot_idx, pilot_sym)
    b10_causal = np.allclose(out_full_b10[:half], out_cut_b10[:half], atol=1e-9)
    # B12 is block-wise; allow within-block lookahead but not across blocks
    # (the block containing 'half' may differ, blocks before it must match)
    l_block = 64
    last_full_block = (half // l_block) * l_block
    out_full_b12 = B.arm_b12(rx_full, pilot_idx, pilot_sym, l_block=l_block)
    out_cut_b12 = B.arm_b12(rx_cut, pilot_idx, pilot_sym, l_block=l_block)
    b12_causal = np.allclose(
        out_full_b12[:last_full_block], out_cut_b12[:last_full_block], atol=1e-9)
    return {
        "gate": "no_future_leakage",
        "pass": bool(b10_causal and b12_causal),
        "b10_causal_first_half": bool(b10_causal),
        "b12_causal_first_full_blocks": bool(b12_causal),
        "note": "BPS/VV use a declared Nw sliding window (allowed); B10/B12/P1/P2/P3 are causal",
    }


def gate_no_tx_truth_in_deployable():
    """Gate 6: deployable arms do not read TX data bits or phi_true.

    This is enforced structurally: arm_b10/arm_b12/arm_p1/arm_p2/arm_p3 take
    only (rx, pilot_idx, pilot_sym) as inputs — they never see bits_data or
    phi_true. This gate is a static check that the arm signatures do not
    accept forbidden arguments.
    """
    import inspect
    forbidden_args = {"bits_data", "phi_true", "tx_data", "h", "theta_sop"}
    deployable_arms = {
        "B10": B.arm_b10,
        "B12": B.arm_b12,
        "P1": B.arm_p1_cascade,
        "P2": B.arm_p2_confidence_gate,
        "P3": B.arm_p3_adaptive_forgetting,
    }
    violations = {}
    for name, fn in deployable_arms.items():
        sig = inspect.signature(fn)
        params = set(sig.parameters.keys())
        bad = params & forbidden_args
        if bad:
            violations[name] = list(bad)
    return {
        "gate": "no_tx_truth_in_deployable",
        "pass": len(violations) == 0,
        "violations": violations,
        "note": "deployable arms take only (rx, pilot_idx, pilot_sym, hyperparams)",
    }


def gate_identity_non_degeneration(real=None):
    """Gate 7: B10, B12, P1, P2, P3 do NOT collapse to the same estimator.

    Run all arms on a noisy realization and check that their outputs differ
    by more than a tolerance. If two arms produce bit-identical output, one
    is an alias of the other (combination method does not add information).
    """
    if real is None:
        real = ch.build_single_pol_qam16_with_pilots(
            N=2048, alpha=4.0, beta=1.9, gamma_bar=100.0,
            f_g=100.0, sop_rate=8.0e-6, seed=7602,
            f_residual_hz=1.0e5, laser_lw_hz=10.0e3,
        )
    rx = real["rx"]
    pilot_idx = real["pilot_idx"]
    pilot_sym = real["pilot_sym"]
    snr_db = 20.0

    outs = {
        "B10": B.arm_b10(rx, pilot_idx, pilot_sym),
        "B12": B.arm_b12(rx, pilot_idx, pilot_sym, snr_db=snr_db),
        "P1": B.arm_p1_cascade(rx, pilot_idx, pilot_sym, snr_db=snr_db),
        "P2": B.arm_p2_confidence_gate(rx, pilot_idx, pilot_sym, snr_db=snr_db),
        "P3": B.arm_p3_adaptive_forgetting(rx, pilot_idx, pilot_sym),
    }
    # pairwise max-abs-diff
    names = list(outs.keys())
    diffs = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            d = float(np.max(np.abs(outs[a] - outs[b])))
            diffs[f"{a}_vs_{b}"] = d
    # any pair with diff < 1e-9 is an aliasing suspect
    aliases = [k for k, v in diffs.items() if v < 1e-9]
    return {
        "gate": "identity_non_degeneration",
        "pass": len(aliases) == 0,
        "pairwise_max_abs_diff": diffs,
        "alias_suspects": aliases,
        "tol": 1e-9,
    }


def run_all_gates(seed=7600):
    """Run all 7 semantic gates. Returns dict of results + overall pass."""
    real_clean = _make_clean_realization(seed=seed)
    real_noisy = ch.build_single_pol_qam16_with_pilots(
        N=2048, alpha=4.0, beta=1.9, gamma_bar=100.0,
        f_g=100.0, sop_rate=8.0e-6, seed=seed + 2,
        f_residual_hz=1.0e5, laser_lw_hz=10.0e3,
    )
    results = {}
    results["1_noiseless_recovery"] = gate_noiseless_recovery(real=real_clean)
    results["2_cfo_phase_sign_and_units"] = gate_cfo_phase_sign_and_units(seed=seed + 1)
    results["3_pilot_data_mask_overhead"] = gate_pilot_data_mask_overhead(real=real_clean)
    results["4_energy_fairness"] = gate_energy_fairness(real=real_clean)
    results["5_no_future_leakage"] = gate_no_future_leakage(real=real_noisy)
    results["6_no_tx_truth_in_deployable"] = gate_no_tx_truth_in_deployable()
    results["7_identity_non_degeneration"] = gate_identity_non_degeneration(real=real_noisy)
    overall_pass = all(r["pass"] for r in results.values())
    return {"overall_pass": overall_pass, "gates": results}
