"""P08-R2 Phase A gate — H9 fix: a priori-registered MDE, no min(B1,B2),
honest evidence_insufficient terminal state.

Per D049 / user P08-R2 instruction §4-5 (correct power design):
  - MDE is a PRIORI-registered (graduation-value FER delta), NOT a post-hoc
    power threshold computed after fixing n. Power analysis becomes "given the
    a-priori MDE, compute required n; sample to that n; no early stopping".
  - The old per-trajectory min(B1,B2) cherry-pick is REMOVED. A single
    conventional comparator is pre-registered (B2 — LLR clipping + decoder
    normalization/offset tuning; B1 = B0/temperature has no numerical effect on
    this dataset so it is not the comparator), AND two independent deltas
    (B0-B2, B0-B1) are reported separately.
  - CI_lo = 0 is reported HONESTLY. If CI half-width > MDE/2 the terminal state
    is `EVIDENCE_INSUFFICIENT` (not PROBLEM_ABSENT). "Absent" requires both
    CI_lo ≤ 0 AND CI half-width ≤ MDE/2 (i.e. the data rule out an effect as
    large as the MDE).

Terminal states (per user §6 + D049):
  EXECUTION_INVALID                                        — metamorphic / identity gate FAIL
  EVIDENCE_INSUFFICIENT                                    — CI too wide to decide (CI_hw > MDE/2)
  PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE — headroom < MDE and CI excludes MDE
  PROBLEM_RESOLVED_BY_LLR_CLIP_AND_DECODER_TUNING          — B2 reaches O1/O2 within MDE
  PROBLEM_SURVIVES_CONVENTIONAL_BASELINE_PROCEED_TO_BC     — headroom ≥ MDE + receiver-visible features
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

from p08r2_chain import (
    get_gg_scenes, CodedContractR, CodecAdapterR, CalibrationPrefix,
    CodedRealizationR2, split_prefix_data, estimate_sigma2_from_prefix,
    oracle_sigma2_global, oracle_sigma2_block, oracle_sigma2_finer,
)
from p08_coded_chain import maxlog_soft_demap_16qam


# =============================================================================
# H9 fix — re-frozen metric contract with a-priori MDE
# =============================================================================

@dataclass
class MetricContractR2:
    """Re-frozen metric contract for P08-R2 (H9 fix). MDE is a-priori."""
    # fresh dev AND test seeds (NEW blocks 9000-9019 dev / 8000-8039 test;
    # both disjoint from ALL campaign history including P08-R's observed
    # 6000-6019/7000-7039). User instruction: observed seeds must not be reused.
    # history: P01-P07 0-99/200-239/300-334/500-540/1000-1014/1100-1129;
    #          P08-R dev 6000-6019 / test 7000-7039 (OBSERVED — excluded).
    dev_seeds: Tuple[int, ...] = tuple(range(9000, 9020))   # NEW dev block
    test_seeds: Tuple[int, ...] = tuple(range(8000, 8040))  # NEW test block
    dev_tune_seeds: Tuple[int, ...] = tuple(range(9000, 9010))
    dev_holdout_seeds: Tuple[int, ...] = tuple(range(9010, 9020))

    scenes: Tuple[str, ...] = ("weak", "moderate", "strong")
    f_G_Hz: Tuple[float, ...] = (100.0, 1000.0)
    dev_snr_dB: Tuple[float, ...] = (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0)
    n_cw_per_pol: int = 16
    eval_block: int = 100
    o2_block: int = 16

    # ---- H9 fix: a-priori MDE (registered BEFORE seeing test data) ----
    # Rationale for MDE_fer = 0.05: under D005 务实路线, a coded-LLR-calibration
    # method must move trajectory-level FER by at least ~0.05 to be worth
    # promoting (5% absolute FER = meaningful at the operating point ~0.1-0.2).
    # Smaller effects are below the graduation-value bar even if statistically
    # detectable. This is an a-priori scientific threshold, NOT a power calc.
    mde_fer: float = 0.05                # a-priori registered FER-delta MDE
    primary_metric_choice: str = "B_fixed_snr_paired_fer"  # Primary B (fixed-SNR paired FER)
    fer_target: float = 0.1              # candidate target (Primary A — only if all cross)
    mde_snr_dB: float = 0.15             # required-SNR MDE (Primary A only)
    fixed_snr_dB_primaryB: Tuple[float, ...] = ()  # frozen on dev
    chosen_cell: Tuple = ()              # (scene, fG, SNR) frozen on dev
    # Pre-registered single conventional comparator (H9③ fix: no min(B1,B2)).
    # B2 = LLR clipping + decoder normalization/offset tuning. B1 = B0/T has no
    # numerical effect on this dataset (P08-R confirmed mean FER B0=B1=0.1148),
    # so B2 is the meaningful conventional comparator.
    conventional_comparator: str = "B2"
    # Power planning: required n at the a-priori MDE (reported for transparency,
    # NOT used to redefine MDE). For paired FER delta at power 0.8 two-sided 0.05,
    # n_required ≈ (z_{0.975}+z_{0.8})² · 2·p·(1-p) / MDE². With p≈0.17, MDE=0.05:
    # n ≈ 7.85 · 0.28 / 0.0025 ≈ 879. This exceeds our budget; the test therefore
    # runs at n=40 and reports EVIDENCE_INSUFFICIENT if CI_hw > MDE/2 (honest).
    n_test_planned: int = 40

    b1_temperature_grid: Tuple[float, ...] = (0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0)
    b2_alpha_grid: Tuple[float, ...] = (0.625, 0.75, 0.875)
    b2_offset_grid: Tuple[float, ...] = (0.0, 0.1, 0.2)
    b2_llr_clip_grid: Tuple[float, ...] = (20.0, 30.0)

    sop_rate: float = 1e-5
    n_prefix_symbols: int = 32

    def to_dict(self) -> dict:
        return asdict(self)


def bootstrap_ci(deltas: np.ndarray, n_boot: int = 2000, alpha: float = 0.05) -> Tuple[float, float, float]:
    """Bootstrap mean and (1-alpha) CI of a 1D array of per-trajectory deltas.
    Returns (mean, ci_lo, ci_hi)."""
    deltas = np.asarray(deltas, dtype=np.float64)
    if deltas.size == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(20260802)
    n = deltas.size
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = float(np.mean(deltas[idx]))
    mean = float(np.mean(deltas))
    lo = float(np.percentile(boot_means, 100 * alpha / 2))
    hi = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    return mean, lo, hi


def ci_half_width(ci: Tuple[float, float, float]) -> float:
    """Half-width of a bootstrap CI (mean ± hw)."""
    return float(0.5 * (ci[2] - ci[1]))


# =============================================================================
# method decoders (unchanged scoring; H7 fix is in equalize, not here)
# =============================================================================

def llr_per_cw_from_eq(eq_data: np.ndarray, sigma2, contract: CodedContractR) -> np.ndarray:
    """Soft-demap equalized data symbols to LLR, grouped per codeword (reused
    from p08r_phaseA — no H9 issue here)."""
    n_sym = eq_data.size
    n_sym_per_cw = contract.n // 4
    n_cw = n_sym // n_sym_per_cw
    if np.isscalar(sigma2) or np.ndim(sigma2) == 0:
        llr = maxlog_soft_demap_16qam(eq_data, float(sigma2))
    else:
        sigma2 = np.asarray(sigma2, dtype=np.float64)
        llr = np.empty((n_sym, 4), dtype=np.float32)
        i = 0
        tol = 1e-12
        while i < n_sym:
            j = i + 1
            while j < n_sym and abs(sigma2[j] - sigma2[i]) <= tol * max(1.0, abs(sigma2[i])):
                j += 1
            llr[i:j] = maxlog_soft_demap_16qam(eq_data[i:j], float(sigma2[i]))
            i = j
    return llr.reshape(n_cw, contract.n)


def method_B0(real, eq, contract, codec, prefix):
    """B0: receiver-visible GLOBAL σ² from calibration prefix (post-eq, demapper)."""
    sigs = {}; us = {}
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        sig2 = estimate_sigma2_from_prefix(eqp, sp)
        sigs[pol] = sig2
        llr = llr_per_cw_from_eq(eqd, sig2, contract)
        uhat, _ = codec.decode(llr)
        us[pol] = uhat
    return us, {"sigma2_X": sigs["X"], "sigma2_Y": sigs["Y"]}


def method_B1(real, eq, contract, codec, prefix, temperature: float):
    """B1: B0 σ² but LLR divided by a dev-tuned scalar temperature (test-frozen)."""
    us = {}; sigs = {}
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        sig2 = estimate_sigma2_from_prefix(eqp, sp) / temperature
        sigs[pol] = sig2
        llr = llr_per_cw_from_eq(eqd, sig2, contract)
        uhat, _ = codec.decode(llr)
        us[pol] = uhat
    return us, {"sigma2_X": sigs["X"], "sigma2_Y": sigs["Y"], "temperature": temperature}


def method_B2(real, eq, contract_template, prefix, alpha_d, offset_d, llr_clip_d):
    """B2: global LLR clipping + decoder normalization/offset tuning (test-frozen)."""
    c2 = CodedContractR(alpha=alpha_d, offset=offset_d, llr_clip=llr_clip_d)
    codec2 = CodecAdapterR(c2)
    us = {}; sigs = {}
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        sig2 = estimate_sigma2_from_prefix(eqp, sp)
        sigs[pol] = sig2
        llr = maxlog_soft_demap_16qam(eqd, sig2, llr_clip=llr_clip_d)
        n_cw = eqd.size // (c2.n // 4)
        llr_cw = llr.reshape(n_cw, c2.n)
        uhat, _ = codec2.decode(llr_cw)
        us[pol] = uhat
    return us, {"sigma2_X": sigs["X"], "sigma2_Y": sigs["Y"],
                "alpha": alpha_d, "offset": offset_d, "llr_clip": llr_clip_d}


def method_oracle(real, eq, contract, codec, prefix, level: str, o2_block: int = 16):
    """Oracle ladder O0/O1/O2 — PRIVILEGED, scoring/headroom only."""
    us = {}; sig_meta = {}
    block_O1 = 100
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, sd = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        if level == "O0":
            sig2 = oracle_sigma2_global(eqd, sd)
        elif level == "O1":
            sig2 = oracle_sigma2_block(eqd, sd, block=block_O1)
        elif level == "O2":
            sig2 = oracle_sigma2_finer(eqd, sd, block=o2_block)
        else:
            raise ValueError(level)
        llr = llr_per_cw_from_eq(eqd, sig2, contract)
        uhat, _ = codec.decode(llr)
        us[pol] = uhat
        sig_meta[f"sigma2_{pol}_mean"] = float(np.mean(sig2))
    return us, sig_meta


def score_trajectory(real, us, contract) -> dict:
    """Score one trajectory. FER per-pol over n_cw codewords; trajectory FER =
    mean of two pols. Independent unit = trajectory/seed (H6, unchanged)."""
    out = {}
    for pol in ("X", "Y"):
        uhat = us[pol]
        info_true = getattr(real, f"cw_info_{pol}")
        cw_err = np.any(uhat != info_true, axis=1)
        out[f"fer_{pol}"] = float(np.mean(cw_err))
        out[f"n_cw_err_{pol}"] = int(cw_err.sum())
        out[f"n_cw_{pol}"] = int(cw_err.size)
        out[f"post_ber_{pol}"] = float(np.mean(uhat != info_true))
    out["fer_traj"] = 0.5 * (out["fer_X"] + out["fer_Y"])
    return out


def trajectory_evidence(real, eq) -> dict:
    """H6: per-trajectory + per-cw evidence (h, fade, position) for raw rows.
    evaluation-only truth fields flagged with '_truth' suffix. NEW in R2:
    records the receiver-visible sigma2_pre + gamma_vis (H7 fix diagnostics)."""
    _, hX_data = split_prefix_data(eq["h_use_X"], real.n_prefix)
    _, hY_data = split_prefix_data(eq["h_use_Y"], real.n_prefix)
    h_true_data = split_prefix_data(real.h, real.n_prefix)[1]
    return {
        "h_use_X_mean": float(np.mean(hX_data)), "h_use_X_min": float(np.min(hX_data)),
        "h_use_Y_mean": float(np.mean(hY_data)), "h_use_Y_min": float(np.min(hY_data)),
        "h_truth_mean": float(np.mean(h_true_data)),   # _truth flagged
        "h_truth_min": float(np.min(h_true_data)),     # evaluation-only
        "h_truth_max": float(np.max(h_true_data)),
        "sigma2_pre": float(eq.get("sigma2_pre", float("nan"))),  # receiver-visible (H7 fix)
        "gamma_vis": float(eq.get("gamma_vis", float("nan"))),    # = 1/sigma2_pre
    }


__all__ = [
    "MetricContractR2", "bootstrap_ci", "ci_half_width",
    "method_B0", "method_B1", "method_B2", "method_oracle",
    "score_trajectory", "trajectory_evidence", "llr_per_cw_from_eq",
]
