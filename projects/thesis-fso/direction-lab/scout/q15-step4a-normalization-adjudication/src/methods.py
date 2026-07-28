"""Q15 Step 4a Terminal Adjudication — correct-normalization comparators.

This module adds the CORRECT conventional normalization comparators that T020
was missing, plus a gated-scalar ablation that isolates M4's gate from its map.
Every method is a PURE FUNCTION over the calibration PREFIX (128 symbols),
applied to the disjoint eval suffix. Reuses T020's M2/M4 read-only by import.

THEORETICAL EXPECTATION (frozen in contract.yaml):
    z_prefix has power Pz_hat = robust_mean(|z_prefix|^2).
    Public 16QAM target power Ps = E|s|^2 = 1 (avg-power-normalized).
    The complex amplitude multiplier a satisfies |a|^2 * Pz_hat = Ps,
    so a = sqrt(Ps / Pz_hat).  Apply z' = a * z.
    T020 M1 used scale = Ps/Pz_hat (= a^2) and multiplied scale*z -> over-corrects.

Methods added here (all prefix-only, frozen, identity on degenerate prefix):
  - correct_pooled_sqrt_rms:   a = sqrt(Ps / robust_mean(|z_x|² ∪ |z_y|²)); both pols
  - correct_per_pol_sqrt_rms:  a_x = sqrt(Ps / robust_mean(|z_x|²)); a_y similarly
  - gated_scalar_ablation:     M4's prefix gate (identity vs scale), scale = correct sqrt
  - robust_scalar:             a = sqrt(Ps / median(|z_prefix|²)) (median, not trimmed mean)
"""

from __future__ import annotations

from typing import Any

import numpy as np

E_ABS2 = 1.0  # avg-power-normalized 16QAM: E|s|^2 = 1


def _hard_16qam(z: np.ndarray) -> np.ndarray:
    from common._modulation import hard_decision
    return np.asarray(hard_decision(np.asarray(z, dtype=np.complex128), mod="qam16"),
                      dtype=np.complex128)


def _robust_mean_abs2(z: np.ndarray, *, trim_frac: float = 0.1) -> float:
    """10%-trimmed mean of |z|^2 (same robust estimator family as T020 M1)."""
    p = np.abs(np.asarray(z, dtype=np.complex128).ravel()) ** 2
    if p.size == 0:
        return float("nan")
    arr = np.sort(p)
    n = arr.size
    k = int(np.floor(n * trim_frac))
    if 2 * k >= n:
        return float(np.mean(arr))
    return float(np.mean(arr[k:n - k])) if (n - k) > k else float(np.mean(arr))


def _median_abs2(z: np.ndarray) -> float:
    p = np.abs(np.asarray(z, dtype=np.complex128).ravel()) ** 2
    if p.size == 0:
        return float("nan")
    return float(np.median(p))


# ─── correct_pooled_sqrt_rms ─────────────────────────────────────────────────

def correct_pooled_sqrt_rms_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray,
                                    *, trim_frac: float = 0.1) -> dict[str, Any]:
    """a = sqrt(Ps / pooled_robust_mean(|z|²)); same a applied to both pols."""
    pooled = np.concatenate([np.ravel(z_prefix_x), np.ravel(z_prefix_y)])
    pz = _robust_mean_abs2(pooled, trim_frac=trim_frac)
    if not np.isfinite(pz) or pz <= 1e-9:
        return {"a": 1.0, "pz_hat": pz, "identity": True}
    a = float(np.sqrt(E_ABS2 / pz))
    return {"a": a, "pz_hat": pz, "identity": False}


def correct_pooled_sqrt_rms_apply_continuous(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    z = np.asarray(z_suffix, dtype=np.complex128)
    return float(frozen.get("a", 1.0)) * z


# ─── correct_per_pol_sqrt_rms ────────────────────────────────────────────────

def correct_per_pol_sqrt_rms_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray,
                                     *, trim_frac: float = 0.1) -> dict[str, Any]:
    """Per-pol: a_x = sqrt(Ps / robust_mean(|z_x|²)); a_y similarly."""
    px = _robust_mean_abs2(z_prefix_x, trim_frac=trim_frac)
    py = _robust_mean_abs2(z_prefix_y, trim_frac=trim_frac)
    ax = float(np.sqrt(E_ABS2 / px)) if (np.isfinite(px) and px > 1e-9) else 1.0
    ay = float(np.sqrt(E_ABS2 / py)) if (np.isfinite(py) and py > 1e-9) else 1.0
    identity = (ax == 1.0 and ay == 1.0)
    return {"a_x": ax, "a_y": ay, "px_hat": px, "py_hat": py, "identity": identity}


def correct_per_pol_sqrt_rms_apply_continuous(frozen: dict[str, Any],
                                              z_suffix_x: np.ndarray, z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    return ax * np.asarray(z_suffix_x, dtype=np.complex128), ay * np.asarray(z_suffix_y, dtype=np.complex128)


# ─── gated_scalar_ablation (M4's gate + CORRECT sqrt scale) ──────────────────

def gated_scalar_ablation_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray, *,
                                 collapse_threshold: float = 0.6,
                                 spread_threshold: float = 0.1,
                                 trim_frac: float = 0.1) -> dict[str, Any]:
    """Reuse M4's prefix-gate rule (identity on healthy, scale on collapsed),
    but when the gate OPENS, apply the CORRECT sqrt scale (per-pol) instead of
    M2/M3's map. Isolates 'gate value' from 'map value'."""
    pooled = np.concatenate([np.ravel(z_prefix_x), np.ravel(z_prefix_y)])
    p = np.abs(pooled)
    mean_abs2 = float(np.mean(p ** 2)) if p.size else 0.0
    mu_r = float(np.mean(p)) if p.size else 0.0
    spread = float(np.std(p) / (mu_r + 1e-9)) if p.size else 0.0
    # gate rule identical to T020 m4_gated_policy_freeze
    if mean_abs2 >= collapse_threshold and spread >= spread_threshold:
        policy = "identity"
    elif mean_abs2 < collapse_threshold and spread >= spread_threshold:
        policy = "scale"
    else:
        # low-spread single-mode: M4 picked M3; here we still apply correct scale
        # (ablation: we want to see what a correct scalar does in ALL gate branches)
        policy = "scale"
    # correct per-pol sqrt scale
    px = _robust_mean_abs2(z_prefix_x, trim_frac=trim_frac)
    py = _robust_mean_abs2(z_prefix_y, trim_frac=trim_frac)
    ax = float(np.sqrt(E_ABS2 / px)) if (np.isfinite(px) and px > 1e-9) else 1.0
    ay = float(np.sqrt(E_ABS2 / py)) if (np.isfinite(py) and py > 1e-9) else 1.0
    return {"policy": policy, "a_x": ax, "a_y": ay, "mean_abs2": mean_abs2,
            "spread": spread, "collapse_threshold": float(collapse_threshold),
            "spread_threshold": float(spread_threshold)}


def gated_scalar_ablation_apply_continuous(frozen: dict[str, Any],
                                           z_suffix_x: np.ndarray, z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    if frozen.get("policy") == "identity":
        return np.asarray(z_suffix_x, dtype=np.complex128), np.asarray(z_suffix_y, dtype=np.complex128)
    return ax * np.asarray(z_suffix_x, dtype=np.complex128), ay * np.asarray(z_suffix_y, dtype=np.complex128)


# ─── robust_scalar (median estimator) ────────────────────────────────────────

def robust_scalar_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray) -> dict[str, Any]:
    """a = sqrt(Ps / median(|z_prefix|²)) per-pol. Median is more robust than
    trimmed-mean to heavy collapse tails."""
    mx = _median_abs2(z_prefix_x)
    my = _median_abs2(z_prefix_y)
    ax = float(np.sqrt(E_ABS2 / mx)) if (np.isfinite(mx) and mx > 1e-9) else 1.0
    ay = float(np.sqrt(E_ABS2 / my)) if (np.isfinite(my) and my > 1e-9) else 1.0
    return {"a_x": ax, "a_y": ay, "mx_hat": mx, "my_hat": my}


def robust_scalar_apply_continuous(frozen: dict[str, Any],
                                   z_suffix_x: np.ndarray, z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    return ax * np.asarray(z_suffix_x, dtype=np.complex128), ay * np.asarray(z_suffix_y, dtype=np.complex128)


__all__ = [
    "correct_pooled_sqrt_rms_freeze", "correct_pooled_sqrt_rms_apply_continuous",
    "correct_per_pol_sqrt_rms_freeze", "correct_per_pol_sqrt_rms_apply_continuous",
    "gated_scalar_ablation_freeze", "gated_scalar_ablation_apply_continuous",
    "robust_scalar_freeze", "robust_scalar_apply_continuous",
]
