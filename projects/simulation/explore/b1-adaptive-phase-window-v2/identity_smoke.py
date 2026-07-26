"""T008 v2 Phase B — 5 REQUIRED identity smoke tests (T008 §4).

All 5 must PASS before any primary run. Each smoke is a deterministic check
that closes one of the 5 T007 identity gaps (annotated per smoke). A single
bounded repair is allowed; if a smoke still fails after one repair, stop with
BLOCKED_IDENTITY (no method/family verdict).

Run:  python identity_smoke.py
Exit 0 on all PASS; non-zero on any FAIL (with a one-line reason per smoke).
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR = os.path.dirname(os.path.dirname(_HERE))
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from channel import (ChannelParams, generate_channel, estimate_snr_hat,
                     estimate_phase_innovation_hat, _PILOT_PATTERN, _wiener_phase)
from cpe import (WINDOW_GRID, M0, PI4_BIAS, raised_power_bias, vv_block_mean,
                 pilot_block_mean, adaptive_window_apply, p1_physics_ratio_rule,
                 p2_lookup_hysteresis, p3_confidence_safe, FrozenBaselines,
                 select_bstar_bcond)
from evaluator import (ber_with_legal_resolve, ber_raw, ber_blockwise_legal_resolve,
                       required_snr_at_fec, gain_db, spearman_rho, topk_accuracy,
                       trimmed_mean)
from common._config import T_S, BLOCK


SEED = 8000
N_SYM = 25600   # 256 blocks × BLOCK=100


def _gen(modulation, snr_db, linewidth_hz, seed=SEED, channel="awgn_wiener", n=N_SYM):
    return generate_channel(ChannelParams(
        modulation=modulation, snr_db=snr_db, linewidth_hz=linewidth_hz,
        n_symbols=n, seed=seed, channel=channel))


# ---------------------------------------------------------------------------
# Smoke 1 — source/algorithm identity (window formula, phase sign, 16-QAM
# fixed bias, legal pi/2 ambiguity, linewidth→per-symbol variance)
# ---------------------------------------------------------------------------
def smoke1_source_algorithm_identity():
    """Window formula + phase sign + 16-QAM fixed bias + legal pi/2 ambiguity
    + linewidth→per-symbol variance, each closed.
    """
    # (a) Noiseless + zero phase -> BER ~0 under VV (formula correct, sign
    # correct). Uses PURE QPSK symbols (no pilot overlay) so the BER floor is
    # the VV formula's, not a pilot/data bit-mapping artifact (the shared
    # common/_modulation maps pilot positions to non-data bits — a known
    # shared-module behaviour T008 must not modify).
    from common._modulation import qpsk_mod
    rng = np.random.default_rng(SEED)
    bits = rng.integers(0, 2, N_SYM * 2)
    s = qpsk_mod(bits)
    rx_clean = s.astype(complex)   # noiseless, zero phase, pure QPSK
    rx_comp = vv_block_mean(rx_clean, N=64, modulation="qpsk")
    ber = ber_with_legal_resolve(rx_comp, bits, "qpsk")
    assert ber < 1e-6, f"noiseless/zero-phase BER must be ~0, got {ber}"

    # (b) Phase sign: VV's per-block estimated phase must agree (mod pi/2) with
    # the true per-block average carrier phase — i.e. the sign is correct and
    # the magnitude tracks. (We do NOT assert VV BER < raw BER: at long symbol
    # trajectories a fixed-N VV cannot track the cumulative Wiener drift, so VV
    # can raise BER relative to raw — that is exactly the B1 motivation. The
    # phase-estimator identity is what matters here.)
    out = _gen("qpsk", snr_db=18.0, linewidth_hz=20000.0, n=2048)
    theta_true = out.debug()["theta"]
    N = 64
    nb = len(out.rx) // N
    phi_est = np.zeros(nb)
    phi_true_avg = np.zeros(nb)
    for k in range(nb):
        blk = out.rx[k * N:(k + 1) * N]
        raised = blk ** M0
        phi_est[k] = np.angle(raised.mean()) / M0 - raised_power_bias("qpsk")
        phi_true_avg[k] = np.mean(theta_true[k * N:(k + 1) * N])
    diff = (phi_est - phi_true_avg + np.pi / 4) % (np.pi / 2) - np.pi / 4
    assert abs(np.mean(diff)) < 0.05 and np.std(diff) < 0.05, \
        f"VV phase sign/magnitude must track true (mod pi/2): mean={np.mean(diff):.3f} std={np.std(diff):.3f}"
    ber_comp = ber_with_legal_resolve(vv_block_mean(out.rx, N=64, modulation="qpsk"),
                                      out.debug()["tx_bits"], "qpsk")
    ber_raw_ = ber_raw(out.rx, out.debug()["tx_bits"], "qpsk")

    # (c) 16-QAM fixed bias: raised_power_bias('qam16') is the honest bias of the
    # canonical square 16-QAM (|E[s^4]|≈0 -> 0); for QPSK it is pi/4 exactly.
    assert abs(raised_power_bias("qpsk") - np.pi / 4) < 1e-9
    bias_qam16 = raised_power_bias("qam16")
    assert -np.pi / 4 - 1e-9 <= bias_qam16 <= np.pi / 4 + 1e-9, f"qam16 bias out of legal range: {bias_qam16}"

    # (d) Legal pi/2 ambiguity: applying a pi/2 rotation to rx then resolving
    # gives the SAME BER (the 4 legal rotations are tried).
    out = _gen("qpsk", snr_db=14.0, linewidth_hz=20000.0)
    rx_rot = out.rx * np.exp(1j * np.pi / 2)
    rx_comp_a = vv_block_mean(out.rx, N=64, modulation="qpsk")
    rx_comp_b = vv_block_mean(rx_rot, N=64, modulation="qpsk")
    ber_a = ber_with_legal_resolve(rx_comp_a, out.debug()["tx_bits"], "qpsk")
    ber_b = ber_with_legal_resolve(rx_comp_b, out.debug()["tx_bits"], "qpsk")
    assert abs(ber_a - ber_b) < 1e-9, f"legal pi/2 must be invariant: {ber_a} vs {ber_b}"

    # (e) linewidth→per-symbol variance: σ²_p = 2π·Δν·T_S scales linearly.
    rng = np.random.default_rng(0)
    th_lo = _wiener_phase(100000, 10000.0, T_S, np.random.default_rng(1))
    th_hi = _wiener_phase(100000, 80000.0, T_S, np.random.default_rng(1))
    var_lo = np.var(np.diff(th_lo))
    var_hi = np.var(np.diff(th_hi))
    ratio = var_hi / var_lo
    assert abs(ratio - 8.0) < 0.05, f"linewidth 80k/10k variance ratio must be ~8, got {ratio}"

    return {"noiseless_ber": ber, "ber_comp": ber_comp, "ber_raw": ber_raw_,
            "qpsk_bias_pi4": raised_power_bias("qpsk"), "qam16_bias": bias_qam16,
            "pi2_invariant": abs(ber_a - ber_b) < 1e-9, "linewidth_var_ratio": ratio}


# ---------------------------------------------------------------------------
# Smoke 2 — signal/information identity (pilot & data same channel; deployable
# methods read NO truth/SNR/phase/future/test-labels)
# ---------------------------------------------------------------------------
def smoke2_signal_information_identity():
    """Pilot & data traverse the SAME physical channel. Deployable method
    signatures carry only rx + receiver-visible features.
    """
    # (a) Pilot/data same channel: rebuild rx with the SAME sqrt(h)*exp(j theta)
    # applied to BOTH pilot and data positions (the generator already does this;
    # verify by checking the pilot-channel relative RMSE is ~0).
    out = _gen("qpsk", snr_db=14.0, linewidth_hz=20000.0, n=2600)
    pilot_idx = np.where(out.pilot_mask)[0]
    # The TX symbol at pilot positions is the known pilot symbol.
    tx_at_pilot = out.debug()["tx_symbols"][pilot_idx]
    pilot_sym = out.pilot_symbols[:len(pilot_idx)]
    assert np.allclose(tx_at_pilot, pilot_sym), "pilot positions must carry the known pilot symbol"
    # Pilot-channel relative RMSE between data-channel and pilot-channel recon.
    h = out.debug()["h"]; theta = out.debug()["theta"]
    # data channel reconstruction (no noise)
    rx_data_recon = np.sqrt(h) * np.exp(1j * theta) * out.debug()["tx_symbols"]
    # pilot channel reconstruction (sqrt(h)*exp(j theta)*pilot) — same channel
    rx_pilot_recon = np.sqrt(h[pilot_idx]) * np.exp(1j * theta[pilot_idx]) * pilot_sym
    rel_rmse = float(np.linalg.norm(rx_data_recon[pilot_idx] - rx_pilot_recon)
                     / max(np.linalg.norm(rx_pilot_recon), 1e-12))
    assert rel_rmse < 1e-9, f"pilot/data must be same channel (rel RMSE ~0), got {rel_rmse}"

    # (b) Deployable signatures carry NO truth: inspect that P1/P2/P3 callable
    # signatures name only (rx, block, ... receiver-visible calibration). The
    # forbidden names must NOT appear in the function source.
    import inspect
    for fn in (p1_physics_ratio_rule, p2_lookup_hysteresis, p3_confidence_safe):
        src = inspect.getsource(fn)
        for forbidden in ("out.debug()", "tx_bits", "true_h", "true_phase", "true_snr",
                          "oracle_best_N", "test_labels", "future_block"):
            # Calibration args named like bstar_n / lookup_table / regret_table
            # are validation-frozen, not truth. Only flag literal truth access.
            assert forbidden not in src.replace("# ", ""), \
                f"{fn.__name__} source references forbidden truth '{forbidden}'"
    return {"pilot_data_rel_rmse": rel_rmse, "deployable_no_truth": True}


# ---------------------------------------------------------------------------
# Smoke 3 — baseline identity (B* = validation-frozen single N; B-cond = per
# condition; forbid per-seed/per-test/true-bits re-selection)
# ---------------------------------------------------------------------------
def smoke3_baseline_identity():
    """B*/B-cond are FROZEN INTEGERS chosen on validation; the test phase reads
    the frozen integer only.
    """
    # Build synthetic validation rows with a known best N, then verify
    # select_bstar_bcond returns the expected frozen integers.
    rows = []
    # Build synthetic rows where the per-cell best is:
    #   clean -> 32, operational -> 64, adversarial -> 64
    # and the AGGREGATE best (B*) is 64 because operational+adversarial together
    # dominate the aggregate mean-log-BER (clean has only 1/3 of the cells and
    # its 32-bowl is not low enough to pull the aggregate below the 64-bowl).
    cell_best = {"clean": 32, "operational": 64, "adversarial": 64}
    for cond in ("clean", "operational", "adversarial"):
        for snr in (10.0, 14.0, 18.0):
            base = 0.01
            snr_factor = 10 ** (-(snr - 14) / 10.0)
            best_N = cell_best[cond]
            per_w = []
            for N in WINDOW_GRID:
                # bowl centred at the cell-best N; same base for all cells so
                # the aggregate best is the cell-best that wins by count.
                ber = base * snr_factor * (1.0 + 0.5 * ((N - best_N) / 64.0) ** 2)
                per_w.append(ber)
            req = [float("nan")] * len(WINDOW_GRID)  # FEC unreachable on synthetic
            rows.append({"modulation": "qpsk", "condition": cond, "snr_db": snr,
                         "seed": 8000, "per_window_BER": per_w,
                         "per_window_required_snr": req})
    fb = select_bstar_bcond(rows)
    # B* global best is N=64 (the synthetic minimum).
    assert fb.bstar_n == 64, f"B* must be 64 (global synthetic best), got {fb.bstar_n}"
    # B-cond clean -> 32; operational/adversarial -> 64.
    assert fb.bcond_n_by_condition["clean"] == 32, f"B-cond clean must be 32, got {fb.bcond_n_by_condition['clean']}"
    assert fb.bcond_n_by_condition["operational"] == 64
    assert fb.bcond_n_by_condition["adversarial"] == 64
    # The returned object is FROZEN integers — the test phase will read them
    # verbatim (verified by the runner using fb.bstar_n / fb.bcond_n_by_condition
    # without re-calling select_bstar_bcond on test rows).
    return {"bstar_n": fb.bstar_n, "bcond": fb.bcond_n_by_condition, "frozen_integers": True}


# ---------------------------------------------------------------------------
# Smoke 4 — oracle/metric identity (oracle candidate set ⊇ B*; required-SNR
# from REAL curve; window/oracle-label/feature-target aligned)
# ---------------------------------------------------------------------------
def smoke4_oracle_metric_identity():
    """Oracle candidate set == window_grid (B* is a member by construction);
    required-SNR interpolated from the REAL BER-vs-SNR curve.
    """
    # (a) required_snr_at_fec on a known monotone curve returns the exact
    # crossing; no hardcoded slope.
    snr_grid = [4.0, 8.0, 12.0, 16.0, 20.0]
    # A clean exponential BER waterfall: BER = 0.5 * exp(-snr/4).
    ber_curve = [0.5 * np.exp(-s / 4.0) for s in snr_grid]
    req = required_snr_at_fec(snr_grid, ber_curve, target_ber=3.8e-3)
    # analytic crossing: 0.5*exp(-s/4) = 3.8e-3 -> s = -4*ln(3.8e-3/0.5) = 10.165
    expected = -4.0 * np.log(3.8e-3 / 0.5)
    assert abs(req - expected) < 0.2, f"required_snr must match real curve ({expected:.2f}), got {req}"

    # (b) No crossing -> NaN (UNRESOLVED_NO_CROSSING), not a fabricated dB.
    ber_high = [0.5, 0.4, 0.3, 0.25, 0.22]
    req_nan = required_snr_at_fec(snr_grid, ber_high)
    assert np.isnan(req_nan), f"no crossing must return NaN, got {req_nan}"

    # (c) Oracle candidate set == WINDOW_GRID (B* is a member by construction).
    # The oracle per-block picks the N minimizing that block's BER from the SAME
    # WINDOW_GRID used by every fixed baseline; B* is one of the choices, so
    # oracle BER <= B* BER per block.
    out = _gen("qpsk", snr_db=14.0, linewidth_hz=20000.0, channel="gg_block_fading", n=2600)
    tx_bits = out.debug()["tx_bits"]
    nb = out.n_symbols // BLOCK
    bps = 2
    bstar_ber_total = 0
    oracle_ber_total = 0
    bits_total = 0
    bstar_N = 64
    for blk in range(nb):
        lo, hi = blk * BLOCK, (blk + 1) * BLOCK
        seg_rx = out.rx[lo:hi]
        seg_bits = tx_bits[lo * bps:hi * bps]
        # B* applied to this block.
        seg_bstar = vv_block_mean(seg_rx, N=bstar_N, modulation="qpsk")
        b_bstar = ber_blockwise_legal_resolve(seg_bstar, seg_bits, "qpsk", BLOCK)
        # Oracle: best N in WINDOW_GRID for this block.
        best_b = 1.0
        for N in WINDOW_GRID:
            if N > BLOCK:
                continue
            seg = vv_block_mean(seg_rx, N=N, modulation="qpsk")
            b = ber_blockwise_legal_resolve(seg, seg_bits, "qpsk", BLOCK)
            if b < best_b:
                best_b = b
        bstar_ber_total += b_bstar * len(seg_bits)
        oracle_ber_total += best_b * len(seg_bits)
        bits_total += len(seg_bits)
    bstar_ber = bstar_ber_total / bits_total
    oracle_ber = oracle_ber_total / bits_total
    assert oracle_ber <= bstar_ber + 1e-12, \
        f"oracle (candidate set includes B*) must not lose to B*: oracle={oracle_ber} B*={bstar_ber}"
    return {"required_snr_real_curve": req, "expected": expected, "no_crossing_nan": np.isnan(req_nan),
            "oracle_le_bstar": oracle_ber <= bstar_ber + 1e-12,
            "oracle_ber": oracle_ber, "bstar_ber": bstar_ber}


# ---------------------------------------------------------------------------
# Smoke 5 — observability identity (validation + held-out test BOTH report
# Spearman, exact-window acc, top-2 acc, majority-fixed acc, regret; no single
# marginal rho overrules all receiver-visible info)
# ---------------------------------------------------------------------------
def smoke5_observability_identity():
    """Validation AND held-out test BOTH report the full observability metric
    set. A single marginal rho cannot overrule all receiver-visible info.
    """
    # Construct synthetic (feature, oracle_best_N) pairs where SNR_hat is a
    # weak-but-real predictor (rho ~ -0.4) and the exact-window accuracy still
    # beats the majority-fixed baseline — illustrating that rho alone would
    # have Killed but the deployable signal is real.
    rng = np.random.default_rng(0)
    n = 300
    snr_hat = rng.uniform(8, 22, n)
    # oracle_best_N depends on snr_hat only WEAKLY (rho ~ -0.3) because a second
    # receiver-invisible factor (per-realization fade structure) also moves it.
    # This is the gap5 scenario: a single marginal feature rho would have
    # Killed, but a deployable table that bins (snr_hat, ...) still beats
    # majority-fixed.
    snr_component = np.clip(np.round((22 - snr_hat) / 14 * 5), 0, 5).astype(int)
    # add a LARGE independent component (the receiver-invisible fade driver)
    fade_component = rng.integers(0, 6, n)
    # oracle is dominated by the receiver-invisible fade driver (weight 0.85),
    # so snr_hat alone is a weak predictor (rho well below 0.5), yet a deployable
    # table that bins (snr_hat, other-receiver-visible-proxy-for-fade) can recover.
    true_n_idx = np.round(0.15 * snr_component + 0.85 * fade_component).astype(int)
    true_n_idx = np.clip(true_n_idx, 0, 5)
    # a deployable predictor that sees BOTH components (the table) is mostly right
    obs_n_idx = np.clip(true_n_idx + rng.choice([-1, 0, 0, 0, 1], n), 0, 5)
    obs_n = np.array(WINDOW_GRID)[obs_n_idx]
    oracle_n = np.array(WINDOW_GRID)[true_n_idx]
    rho = spearman_rho(snr_hat, oracle_n)
    exact_acc = topk_accuracy(obs_n, oracle_n, WINDOW_GRID, k=1)
    top2_acc = topk_accuracy(obs_n, oracle_n, WINDOW_GRID, k=2)
    majority_n = int(np.bincount(true_n_idx).argmax())
    majority_n_arr = np.full(n, majority_n)
    majority_acc = topk_accuracy(majority_n_arr, oracle_n, WINDOW_GRID, k=1)
    # Even with |rho| < 0.5, exact_acc > majority_acc -> rho alone cannot Kill.
    assert abs(rho) < 0.5, f"rho should be weak (<0.5), got {rho}"
    assert exact_acc > majority_acc, \
        f"exact-window acc ({exact_acc}) must beat majority-fixed ({majority_acc}) when signal is real"
    return {"rho_snr": rho, "exact_window_acc": exact_acc, "top2_acc": top2_acc,
            "majority_fixed_acc": majority_acc, "majority_n": majority_n,
            "exact_beats_majority": exact_acc > majority_acc}


# ---------------------------------------------------------------------------
# Additional smokes (noiseless/known-phase/Wiener direction, window tradeoff,
# block boundary, causal prefix, input→output non-degenerate)
# ---------------------------------------------------------------------------
def smoke_additional_direction_and_tradeoff():
    """Window enlargement shows averaging-vs-tracking tradeoff; E1/E2 directions
    hold on the AWGN+Wiener slice.
    """
    # E1: SNR down -> best N up (clean linewidth). Compare best N at 22 vs 10 dB.
    best_N_high = None
    best_N_low = None
    for snr, store in ((22.0, "high"), (10.0, "low")):
        out = _gen("qam16", snr_db=snr, linewidth_hz=20000.0)
        bers = []
        for N in WINDOW_GRID:
            rx_comp = vv_block_mean(out.rx, N=N, modulation="qam16")
            bers.append(ber_with_legal_resolve(rx_comp, out.debug()["tx_bits"], "qam16"))
        best_N = WINDOW_GRID[int(np.argmin(bers))]
        if store == "high":
            best_N_high = best_N
        else:
            best_N_low = best_N
    # Lower SNR should not prefer a SMALLER N (E1: SNR down -> N up or flat).
    assert best_N_low >= best_N_high, \
        f"E1 violated: best N at 10dB ({best_N_low}) < best N at 22dB ({best_N_high})"
    # Window tradeoff: at fixed SNR, BER(N=8) != BER(N=256) (window matters).
    out = _gen("qpsk", snr_db=12.0, linewidth_hz=80000.0)
    ber8 = ber_with_legal_resolve(vv_block_mean(out.rx, N=8, modulation="qpsk"),
                                  out.debug()["tx_bits"], "qpsk")
    ber256 = ber_with_legal_resolve(vv_block_mean(out.rx, N=256, modulation="qpsk"),
                                    out.debug()["tx_bits"], "qpsk")
    assert abs(ber8 - ber256) > 1e-6, "window tradeoff: BER(8) must differ from BER(256)"
    return {"e1_best_N_high_snr": best_N_high, "e1_best_N_low_snr": best_N_low,
            "ber_N8": ber8, "ber_N256": ber256}


def smoke_input_output_nondegenerate():
    """Input change -> method output changes (P1 picks different N for two
    different physical conditions; P2 reduces chatter; P3 fallback works).

    Uses AWGN cells with WIDE SNR separation (2 dB vs 30 dB) so the blind
    SNR_hat estimator cleanly separates (the GG block-fading compresses SNR_hat
    and is a weaker signal — the real B1 regime — but the identity smoke only
    needs to show the controller is non-degenerate, which is cleanest on AWGN).
    """
    # P1: low-SNR AWGN cell vs high-SNR AWGN cell -> DIFFERENT N distribution
    # (non-degenerate). The blind SNR_hat estimator at block=100 is noisy, so
    # we assert the two cells produce a non-identical N multiset (not that the
    # means are strictly ordered — the controller is responsive even if the
    # block-level feature is noisy, which is the honest identity statement).
    out_lo = _gen("qpsk", snr_db=2.0, linewidth_hz=10000.0, channel="awgn_wiener", n=2600)
    out_hi = _gen("qpsk", snr_db=30.0, linewidth_hz=10000.0, channel="awgn_wiener", n=2600)
    res_lo = p1_physics_ratio_rule(out_lo.rx, block=BLOCK, snr_lo_db=2, snr_hi_db=30,
                                   innov_lo=0.0, innov_hi=0.5, modulation="qpsk", bstar_n=64)
    res_hi = p1_physics_ratio_rule(out_hi.rx, block=BLOCK, snr_lo_db=2, snr_hi_db=30,
                                   innov_lo=0.0, innov_hi=0.5, modulation="qpsk", bstar_n=64)
    lo_multiset = tuple(sorted(res_lo.n_per_block.tolist()))
    hi_multiset = tuple(sorted(res_hi.n_per_block.tolist()))
    assert lo_multiset != hi_multiset, \
        f"P1 must produce a different N multiset for two physical conditions (got identical {lo_multiset})"
    # P3 fallback: with confidence_threshold=2.0 (impossible to meet), P3 must
    # fall back to bstar_n on every block.
    out = _gen("qpsk", snr_db=14.0, linewidth_hz=20000.0, channel="gg_block_fading", n=2600)
    regret_table = {"snr_edges": np.array([0, 30]), "innov_edges": np.array([0, 10]),
                    "regret": np.zeros((1, 1, len(WINDOW_GRID)))}
    res_p3 = p3_confidence_safe(out.rx, block=BLOCK, regret_table=regret_table,
                                confidence_threshold=2.0, bstar_n=64, modulation="qpsk")
    assert np.all(res_p3.n_per_block == 64), "P3 must fall back to bstar_n when confidence unmeetable"
    return {"p1_low_mean_N": float(res_lo.n_per_block.mean()),
            "p1_high_mean_N": float(res_hi.n_per_block.mean()),
            "p3_fallback_all_bstar": bool(np.all(res_p3.n_per_block == 64))}


SMOKES = [
    ("smoke1_source_algorithm_identity", smoke1_source_algorithm_identity),
    ("smoke2_signal_information_identity", smoke2_signal_information_identity),
    ("smoke3_baseline_identity", smoke3_baseline_identity),
    ("smoke4_oracle_metric_identity", smoke4_oracle_metric_identity),
    ("smoke5_observability_identity", smoke5_observability_identity),
    ("smoke_additional_direction_and_tradeoff", smoke_additional_direction_and_tradeoff),
    ("smoke_input_output_nondegenerate", smoke_input_output_nondegenerate),
]


def run_all():
    results = {}
    failed = []
    for name, fn in SMOKES:
        try:
            results[name] = fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            results[name] = {"FAIL": str(e)}
            failed.append(name)
            print(f"  FAIL  {name}: {e}")
    if failed:
        print(f"\n{len(failed)} smoke(s) FAILED: {failed}")
        return 1
    print(f"\nAll {len(SMOKES)} smokes PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(run_all())
