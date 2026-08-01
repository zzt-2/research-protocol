"""P08-R Phase A gate — re-frozen metric contract (H4) + trajectory-cluster stats (H6).

Per user P08-R instruction §8-9:
  - old P08 test seeds are OBSERVED, must not be reused → fresh dev/test seeds
    disjoint from campaign history.
  - dev first to find an achievable SNR/FER workspace, THEN freeze test.
  - Primary A (req-SNR @ frozen FER) only if ALL methods cross FER target in the
    sweep; else pre-frozen Primary B (fixed-SNR paired FER / failure probability).
    Never switch A→B after reading test data.
  - MDE: required-SNR uses 0.15 dB; FER/failure-probability MDE frozen on dev per
    graduation value + statistical power; record the conversion.
  - statistical unit = trajectory/seed cluster (NOT codeword).
  - power/precision planning from dev event rate; freeze max sample + stopping rule;
    no early stopping for favorable results; CI half-width too wide ⇒ evidence
    insufficient (not "absent").

Phase A compares (per §9): B0 (receiver-visible global σ² from prefix), B1 (scalar
temperature on dev/test-frozen), B2 (global LLR clipping + decoder norm/offset
tuning), and the O0/O1/O2 oracle ladder. Terminal order (§9):
  A. identity/provenance/information/metric illegal → EXECUTION_INVALID, not P08.
  B. O1/O2 no coded headroom → PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE.
  C. B1/B2 reach O1/O2 or compress gap into MDE → PROBLEM_RESOLVED_BY_TEMPERATURE_AND_DECODER_TUNING.
  D. O1/O2 ≥MDE headroom AND receiver-visible local features observable → Phase B/C.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch

torch.set_default_device("cpu")

from p08r_chain import (
    get_gg_scenes, CodedContractR, CodecAdapterR, CalibrationPrefix,
    estimate_sigma2_from_prefix, oracle_sigma2_global, oracle_sigma2_block,
    oracle_sigma2_finer, CodedRealizationR, split_prefix_data,
)
from p08_coded_chain import maxlog_soft_demap_16qam


# =============================================================================
# H4 — re-frozen metric contract
# =============================================================================

@dataclass
class MetricContractR:
    """Re-frozen metric contract for P08-R (H4 fix)."""
    # fresh seeds, disjoint from campaign history
    # history: P01-P07 used 0-99/200-239/300-334/500-540/1000-1014(dev)/1100-1129(test)
    # P08-R uses a NEW disjoint block: dev 6000-6019, test 7000-7039 (40 test trajectories)
    dev_seeds: Tuple[int, ...] = tuple(range(6000, 6020))      # 20 dev trajectories
    test_seeds: Tuple[int, ...] = tuple(range(7000, 7040))     # 40 test trajectories
    # dev-only sub-grid for tuning B1/B2 (subset of dev)
    dev_tune_seeds: Tuple[int, ...] = tuple(range(6000, 6010))  # 10 for B1/B2 tuning
    dev_holdout_seeds: Tuple[int, ...] = tuple(range(6010, 6020))  # 10 dev holdout

    scenes: Tuple[str, ...] = ("weak", "moderate", "strong")  # labels; (α,β) from params
    f_G_Hz: Tuple[float, ...] = (100.0, 1000.0)
    # dev sweep grid — wider, to find achievable workspace (H4)
    dev_snr_dB: Tuple[float, ...] = (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0)
    n_cw_per_pol: int = 16          # codewords per polarization, shared fade (H6: cluster unit)
    eval_block: int = 100           # equalize + O1 block size
    o2_block: int = 16              # O2 finer partition (pre-frozen)

    # metric (chosen on dev, frozen before test)
    primary_metric_choice: str = "UNFROZEN"   # 'A_required_snr' or 'B_fixed_snr_paired_fer' — frozen on dev
    fer_target: float = 0.1          # candidate FER target for Primary A
    mde_snr_dB: float = 0.15         # MDE for required-SNR (Primary A)
    mde_fer: float = -1.0            # MDE for FER/failure-prob (Primary B), frozen on dev
    fixed_snr_dB_primaryB: Tuple[float, ...] = ()  # frozen on dev if Primary B chosen

    # B1/B2 dev tuning grids
    b1_temperature_grid: Tuple[float, ...] = (0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0)
    b2_alpha_grid: Tuple[float, ...] = (0.625, 0.75, 0.875)
    b2_offset_grid: Tuple[float, ...] = (0.0, 0.1, 0.2)
    b2_llr_clip_grid: Tuple[float, ...] = (20.0, 30.0)

    sop_rate: float = 1e-5
    n_prefix_symbols: int = 32       # calibration prefix length (H2), same for all methods

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def bootstrap_ci(deltas: np.ndarray, n_boot: int = 2000, alpha: float = 0.05) -> Tuple[float, float, float]:
    """Bootstrap mean and (1-alpha) CI of a 1D array of per-trajectory deltas.
    Returns (mean, ci_lo, ci_hi)."""
    deltas = np.asarray(deltas, dtype=np.float64)
    if deltas.size == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(20260801)
    n = deltas.size
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = float(np.mean(deltas[idx]))
    mean = float(np.mean(deltas))
    lo = float(np.percentile(boot_means, 100 * alpha / 2))
    hi = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    return mean, lo, hi


# =============================================================================
# method decoders — each takes (eq_data, sigma2) and returns (llr_per_cw)
# =============================================================================

def llr_per_cw_from_eq(eq_data: np.ndarray, sigma2, contract: CodedContractR) -> np.ndarray:
    """Soft-demap equalized data symbols to LLR, grouped per codeword.
    sigma2 may be a scalar (global) or a per-symbol array (oracle O1/O2). The
    underlying demap only accepts scalar σ², so for per-symbol σ² we demap in
    contiguous runs of equal σ² (oracle partitions are piecewise-constant)."""
    n_sym = eq_data.size
    n_sym_per_cw = contract.n // 4
    n_cw = n_sym // n_sym_per_cw
    if np.isscalar(sigma2) or np.ndim(sigma2) == 0:
        llr = maxlog_soft_demap_16qam(eq_data, float(sigma2))
    else:
        sigma2 = np.asarray(sigma2, dtype=np.float64)
        llr = np.empty((n_sym, 4), dtype=np.float32)
        # demap in contiguous runs where σ² is (approx) constant
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
    """B0: receiver-visible GLOBAL σ² from calibration prefix (H2 fix)."""
    sigs = {}
    us = {}
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        sig2 = estimate_sigma2_from_prefix(eqp, sp)  # global scalar
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
        sig2 = estimate_sigma2_from_prefix(eqp, sp) / temperature  # T>1 inflates σ² ⇒ softer LLR
        sigs[pol] = sig2
        llr = llr_per_cw_from_eq(eqd, sig2, contract)
        uhat, _ = codec.decode(llr)
        us[pol] = uhat
    return us, {"sigma2_X": sigs["X"], "sigma2_Y": sigs["Y"], "temperature": temperature}


def method_B2(real, eq, contract_template, prefix, alpha_d, offset_d, llr_clip_d):
    """B2: global LLR clipping + decoder normalization/offset tuning (test-frozen).
    Builds a temporary codec with the tuned (alpha, offset, llr_clip)."""
    c2 = CodedContractR(alpha=alpha_d, offset=offset_d, llr_clip=llr_clip_d)
    codec2 = CodecAdapterR(c2)
    us = {}; sigs = {}
    for pol in ("X", "Y"):
        eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
        sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
        sig2 = estimate_sigma2_from_prefix(eqp, sp)
        sigs[pol] = sig2
        # soft demap with the tuned llr_clip
        llr = maxlog_soft_demap_16qam(eqd, sig2, llr_clip=llr_clip_d)
        n_cw = eqd.size // (c2.n // 4)
        llr_cw = llr.reshape(n_cw, c2.n)
        uhat, _ = codec2.decode(llr_cw)
        us[pol] = uhat
    return us, {"sigma2_X": sigs["X"], "sigma2_Y": sigs["Y"],
                "alpha": alpha_d, "offset": offset_d, "llr_clip": llr_clip_d}


def method_oracle(real, eq, contract, codec, prefix, level: str, o2_block: int = 16):
    """Oracle ladder (H3). level in {'O0','O1','O2'}. PRIVILEGED — scoring/headroom only."""
    us = {}; sig_meta = {}
    block_O1 = contract and 100  # eval_block
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


# =============================================================================
# per-trajectory scoring (H6: trajectory/seed is the cluster unit)
# =============================================================================

def score_trajectory(real, us, contract) -> dict:
    """Score one trajectory. FER computed per-pol over n_cw codewords, then the
    trajectory-level FER is the mean of the two pols (or treat each pol-trajectory
    as a cluster unit — we record both). Independent unit = trajectory/seed."""
    out = {}
    for pol in ("X", "Y"):
        uhat = us[pol]
        info_true = getattr(real, f"cw_info_{pol}")
        cw_err = np.any(uhat != info_true, axis=1)  # (n_cw,) bool
        out[f"fer_{pol}"] = float(np.mean(cw_err))              # per-pol trajectory FER
        out[f"n_cw_err_{pol}"] = int(cw_err.sum())
        out[f"n_cw_{pol}"] = int(cw_err.size)
        # pre-FEC BER (hard demap of eq vs cw bits) — skipped here, post-FEC is primary
        out[f"post_ber_{pol}"] = float(np.mean(uhat != info_true))
    # trajectory-level FER (cluster unit): mean of two pols
    out["fer_traj"] = 0.5 * (out["fer_X"] + out["fer_Y"])
    return out


def trajectory_evidence(real, eq) -> dict:
    """H6: per-trajectory + per-cw evidence (h, fade, position) for raw rows.
    evaluation-only truth fields flagged with '_truth' suffix."""
    _, hX_data = split_prefix_data(eq["h_use_X"], real.n_prefix)
    _, hY_data = split_prefix_data(eq["h_use_Y"], real.n_prefix)
    h_true_data = split_prefix_data(real.h, real.n_prefix)[1]
    return {
        "h_use_X_mean": float(np.mean(hX_data)), "h_use_X_min": float(np.min(hX_data)),
        "h_use_Y_mean": float(np.mean(hY_data)), "h_use_Y_min": float(np.min(hY_data)),
        "h_truth_mean": float(np.mean(h_true_data)),   # _truth flagged
        "h_truth_min": float(np.min(h_true_data)),     # evaluation-only
        "h_truth_max": float(np.max(h_true_data)),
    }


__all__ = [
    "MetricContractR", "bootstrap_ci",
    "method_B0", "method_B1", "method_B2", "method_oracle",
    "score_trajectory", "trajectory_evidence",
    "llr_per_cw_from_eq",
]
