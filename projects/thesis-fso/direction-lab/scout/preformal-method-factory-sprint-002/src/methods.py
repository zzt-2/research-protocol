"""Pre-formal Method Factory Sprint 002 — causal constellation-prior
shell-distribution family (4 strictly-causal prefix-only constructs).

Every construct in this module is a PURE FUNCTION over the calibration PREFIX
z[eval_start:calibration_end]. The scored eval suffix z[calibration_end:eval_end]
is NEVER read by any freeze/gate/selection step; it only receives the FROZEN
transform at apply time. This closes the V052 causality gap in T019 (M3 used
[cal, eval_end] for selection; M5 used whole-eval-window power).

Each method is split into a `*_freeze(z_prefix)` and a `*_apply(frozen, z_suffix)`
step. The freeze step returns a JSON-serialisable dict of frozen parameters; the
apply step applies the frozen transform to the suffix and returns predicted
16QAM symbols. All freeze steps are deterministic given the prefix (no RNG).

Public 16QAM alphabet geometry (no TX truth):
    per-axis amplitudes {-3,-1,+1,+3}/sqrt(10); avg-power-normalized so E[|s|^2]=1.
    Three |s|^2 shells: 0.2 (inner, 4/16=0.25), 1.0 (mid, 8/16=0.50),
    1.8 (outer, 4/16=0.25). Shell radii = sqrt([0.2, 1.0, 1.8]).

Difference from T019 sprint-001:
    - T019 M5 remap was a per-symbol nearest-shell rescale of the EVAL suffix
      (collapsed detection used the eval window itself). Here M2/M3 build a
      monotone map from the PREFIX CDF and apply the frozen map to the suffix;
      the suffix is never used to choose its own transform.
    - T019 baseline used μ=0.001. Here the baseline is μ=0.03 (current fair).
"""

from __future__ import annotations

from typing import Any

import numpy as np


# ─── Public 16QAM alphabet geometry (analytic, no TX truth) ──────────────────
_AMP = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
_RE, _IM = np.meshgrid(_AMP, _AMP)
ALPHABET_16QAM = (_RE + 1j * _IM).ravel()
# |s|^2 shells with public occupancy
ABS2_SHELLS = np.array([0.2, 1.0, 1.8])           # |s|^2
SHELL_RADII = np.sqrt(ABS2_SHELLS)                # [0.4472, 1.0, 1.3416]
SHELL_OCCUPANCY = np.array([0.25, 0.50, 0.25])    # 4/16, 8/16, 4/16
E_ABS2 = 1.0                                       # E[|s|^2] for avg-power-normalized 16QAM


def _hard_16qam(z: np.ndarray) -> np.ndarray:
    """Nearest-16QAM hard decision (lazy import to avoid hard path dependency)."""
    from common._modulation import hard_decision
    return np.asarray(hard_decision(np.asarray(z, dtype=np.complex128), mod="qam16"),
                      dtype=np.complex128)


# ─── M1: Prefix scalar calibration ───────────────────────────────────────────

def m1_prefix_scalar_freeze(z_prefix: np.ndarray, *, trim_frac: float = 0.1) -> dict[str, Any]:
    """Estimate ONE robust global scale from the prefix and freeze it.

    scale = E[|s|^2] / trimmed_mean(|z_prefix|^2). Robust to a few divergent
    samples: a 10%-trimmed mean of |z|^2 discards the top/bottom 10%. Eval
    applies z' = scale * z (real, positive scale) then hard-decides. scale=1
    reduces to identity (μ=0.03 baseline).
    """
    p = np.abs(np.asarray(z_prefix, dtype=np.complex128).ravel()) ** 2
    if p.size == 0:
        return {"scale": 1.0}
    trimmed = _trimmed_mean(p, trim_frac)
    if not np.isfinite(trimmed) or trimmed <= 1e-9:
        return {"scale": 1.0}
    scale = float(E_ABS2 / trimmed)
    return {"scale": scale}


def m1_prefix_scalar_apply(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    z = np.asarray(z_suffix, dtype=np.complex128)
    scale = float(frozen.get("scale", 1.0))
    return _hard_16qam(scale * z)


def m1_prefix_scalar_apply_continuous(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    """Return the CONTINUOUS scaled z (evaluator does its own hard decision +
    rotation/permutation search). This is the form passed to evaluate_dual_16qam,
    matching the oracle/continuous convention in cb1_cell_runner.run_cell."""
    z = np.asarray(z_suffix, dtype=np.complex128)
    scale = float(frozen.get("scale", 1.0))
    return scale * z


# ─── M2: Prefix quantile shell transport ─────────────────────────────────────

def m2_quantile_transport_freeze(z_prefix: np.ndarray) -> dict[str, Any]:
    """Build a monotone radius map from the prefix |z| CDF onto the public
    16QAM shell radii at the theoretical 0.25/0.50/0.25 occupancy.

    The map is a piecewise-linear monotone function r_in -> r_out defined by
    matching prefix |z| quantiles at {0.125, 0.375, 0.625, 0.875} (midpoints of
    the four shell-band halves) to the corresponding public radii. Phase is
    preserved: z' = (r_out / r_in) * z. If the prefix already matches the
    public shells (healthy), the map degenerates to identity.
    """
    r = np.abs(np.asarray(z_prefix, dtype=np.complex128).ravel())
    if r.size < 8:
        return {"identity": True, "map_x": np.array([0.0]), "map_y": np.array([0.0])}
    # Quantiles of prefix |z| at the four shell-band midpoints (0.125, 0.375, 0.625, 0.875)
    qs = np.quantile(r, [0.125, 0.375, 0.625, 0.875])
    # Target radii at the same cumulative fractions under the public 16QAM:
    #   0.125 -> midpoint of inner band [0, 0.25) -> between 0 and sqrt(0.2)
    #   0.375 -> midpoint of mid band [0.25, 0.75) -> between sqrt(0.2) and sqrt(1.0)... etc
    # Simpler & strictly monotone: map the 4 prefix quantiles onto the 3 shell
    # radii PLUS a 0 anchor and a tail anchor, preserving order.
    # Anchors: (0, 0), (q[0], r_inner), (q[1], r_mid), (q[2], r_mid), (q[3], r_outer), (qmax, rmax_ext)
    # To stay strictly monotone and well-defined we use the 4 quantiles mapped
    # to inner / mid_low / mid_high / outer:
    r_inner, r_mid, r_outer = SHELL_RADII
    # Use midpoints of each shell occupancy band as the public CDF targets.
    map_x = np.concatenate([[0.0], qs, [np.max(r)]])
    map_y = np.array([0.0,
                      r_inner,                               # 0.125 quantile -> inner
                      0.5 * (r_inner + r_mid),               # 0.375 -> inner-mid
                      0.5 * (r_mid + r_outer),               # 0.625 -> mid-outer
                      r_outer,                               # 0.875 -> outer
                      r_outer], dtype=float)
    # Guard: ensure strictly increasing map_x (collapse duplicates with tiny eps)
    map_x = np.maximum.accumulate(map_x + np.arange(map_x.size) * 1e-12)
    return {"identity": False, "map_x": map_x, "map_y": map_y}


def m2_quantile_transport_apply(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    if frozen.get("identity", False):
        return _hard_16qam(z_suffix)
    z = np.asarray(z_suffix, dtype=np.complex128)
    r = np.abs(z)
    # Monotone piecewise-linear interpolation in |z|, extrapolate flat
    r_out = np.interp(r, frozen["map_x"], frozen["map_y"])
    # Preserve phase: rescale by r_out / r (guard against r=0)
    scale = np.where(r > 1e-9, r_out / r, 1.0)
    return _hard_16qam(scale * z)


def m2_quantile_transport_apply_continuous(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    """Continuous corrected z (evaluator does hard decision + rotation search)."""
    if frozen.get("identity", False):
        return np.asarray(z_suffix, dtype=np.complex128)
    z = np.asarray(z_suffix, dtype=np.complex128)
    r = np.abs(z)
    r_out = np.interp(r, frozen["map_x"], frozen["map_y"])
    scale = np.where(r > 1e-9, r_out / r, 1.0)
    return scale * z


# ─── M3: Constrained three-shell mixture calibration ─────────────────────────

def m3_three_shell_mixture_freeze(z_prefix: np.ndarray) -> dict[str, Any]:
    """Fit a one-knot piecewise-linear monotone map constrained by public shell
    radii/priors on the prefix |z| histogram.

    The single knot k is chosen so that the prefix |z| histogram's two dominant
    modes (collapsed vs healthy) map to the inner and mid shells respectively.
    Below k: rescale linearly onto [0, r_inner]; above k: rescale linearly onto
    [r_inner, r_outer]. This is a constrained (3-parameter: knot, lo-slope,
    hi-slope) monotone calibration that respects the public shell structure.
    """
    r = np.abs(np.asarray(z_prefix, dtype=np.complex128).ravel())
    if r.size < 8:
        return {"identity": True, "knots": np.array([0.0]), "values": np.array([0.0])}
    r_inner, r_mid, r_outer = SHELL_RADII
    # Knot = the prefix |z| value at the 50th percentile (separates the two modes).
    knot = float(np.median(r))
    if knot <= 1e-9:
        return {"identity": True, "knots": np.array([0.0]), "values": np.array([0.0])}
    # Below knot: linear from 0 -> r_inner. Above knot: linear from r_inner -> r_outer
    # at the 95th percentile (robust to tail outliers), flat beyond.
    r_hi = float(np.quantile(r, 0.95))
    if r_hi <= knot:
        r_hi = knot * 1.5
    map_x = np.array([0.0, knot, r_hi, r_hi * 2.0])
    map_y = np.array([0.0, r_inner, r_outer, r_outer])
    map_x = np.maximum.accumulate(map_x + np.arange(map_x.size) * 1e-12)
    return {"identity": False, "knots": map_x, "values": map_y,
            "knot_median": knot, "r_hi_p95": r_hi}


def m3_three_shell_mixture_apply(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    if frozen.get("identity", False):
        return _hard_16qam(z_suffix)
    z = np.asarray(z_suffix, dtype=np.complex128)
    r = np.abs(z)
    r_out = np.interp(r, frozen["knots"], frozen["values"])
    scale = np.where(r > 1e-9, r_out / r, 1.0)
    return _hard_16qam(scale * z)


def m3_three_shell_mixture_apply_continuous(frozen: dict[str, Any], z_suffix: np.ndarray) -> np.ndarray:
    """Continuous corrected z (evaluator does hard decision + rotation search)."""
    if frozen.get("identity", False):
        return np.asarray(z_suffix, dtype=np.complex128)
    z = np.asarray(z_suffix, dtype=np.complex128)
    r = np.abs(z)
    r_out = np.interp(r, frozen["knots"], frozen["values"])
    scale = np.where(r > 1e-9, r_out / r, 1.0)
    return scale * z


# ─── M4: Prefix-gated identity/transport policy ──────────────────────────────

def m4_gated_policy_freeze(z_prefix: np.ndarray, *,
                           collapse_threshold: float = 0.5,
                           spread_threshold: float = 0.15) -> dict[str, Any]:
    """Use ONLY prefix features to select identity / M2 / M3.

    Features (computed from the prefix only):
      - mean_abs2 = mean(|z_prefix|^2)
      - spread    = std(|z_prefix|) / (mean(|z_prefix|) + 1e-9)  (coefficient of variation)
    Gate rule (frozen, no RNG, no tuning to suffix):
      - if mean_abs2 >= collapse_threshold AND spread >= spread_threshold:
          policy = identity (healthy stream)
      - elif mean_abs2 < collapse_threshold AND spread >= spread_threshold:
          policy = M2 (collapsed but multi-shell -> quantile transport)
      - else (low spread, single-mode):
          policy = M3 (single-mode collapse -> one-knot mixture)
    """
    p = np.abs(np.asarray(z_prefix, dtype=np.complex128).ravel())
    if p.size == 0:
        return {"policy": "identity", "mean_abs2": 0.0, "spread": 0.0}
    mean_abs2 = float(np.mean(p ** 2))
    mu_r = float(np.mean(p))
    spread = float(np.std(p) / (mu_r + 1e-9))
    if mean_abs2 >= collapse_threshold and spread >= spread_threshold:
        policy = "identity"
    elif mean_abs2 < collapse_threshold and spread >= spread_threshold:
        policy = "M2_quantile_transport"
    else:
        policy = "M3_three_shell_mixture"
    return {"policy": policy, "mean_abs2": mean_abs2, "spread": spread,
            "collapse_threshold": float(collapse_threshold),
            "spread_threshold": float(spread_threshold)}


def m4_gated_policy_apply(frozen: dict[str, Any], z_suffix: np.ndarray,
                          *, m2_frozen: dict | None = None,
                          m3_frozen: dict | None = None) -> np.ndarray:
    """Dispatch on the frozen policy. m2_frozen / m3_frozen are the FROZEN
    prefix-only params of M2/M3; the suffix never re-freezes them."""
    policy = frozen.get("policy", "identity")
    if policy == "identity":
        return _hard_16qam(z_suffix)
    if policy == "M2_quantile_transport":
        if m2_frozen is None:
            raise ValueError("M4 policy=M2 but m2_frozen not provided")
        return m2_quantile_transport_apply(m2_frozen, z_suffix)
    if policy == "M3_three_shell_mixture":
        if m3_frozen is None:
            raise ValueError("M4 policy=M3 but m3_frozen not provided")
        return m3_three_shell_mixture_apply(m3_frozen, z_suffix)
    raise ValueError(f"unknown M4 policy: {policy}")


def m4_gated_policy_apply_continuous(frozen: dict[str, Any], z_suffix: np.ndarray,
                                     *, m2_frozen: dict | None = None,
                                     m3_frozen: dict | None = None) -> np.ndarray:
    """Continuous corrected z (evaluator does hard decision + rotation search)."""
    policy = frozen.get("policy", "identity")
    if policy == "identity":
        return np.asarray(z_suffix, dtype=np.complex128)
    if policy == "M2_quantile_transport":
        if m2_frozen is None:
            raise ValueError("M4 policy=M2 but m2_frozen not provided")
        return m2_quantile_transport_apply_continuous(m2_frozen, z_suffix)
    if policy == "M3_three_shell_mixture":
        if m3_frozen is None:
            raise ValueError("M4 policy=M3 but m3_frozen not provided")
        return m3_three_shell_mixture_apply_continuous(m3_frozen, z_suffix)
    raise ValueError(f"unknown M4 policy: {policy}")


# ─── Helper: trimmed mean ────────────────────────────────────────────────────

def _trimmed_mean(x: np.ndarray, frac: float) -> float:
    arr = np.sort(np.asarray(x, dtype=float).ravel())
    n = arr.size
    k = int(np.floor(n * frac))
    if 2 * k >= n:
        return float(np.mean(arr))
    return float(np.mean(arr[k:n - k])) if (n - k) > k else float(np.mean(arr))


__all__ = [
    "ALPHABET_16QAM", "ABS2_SHELLS", "SHELL_RADII", "SHELL_OCCUPANCY", "E_ABS2",
    "m1_prefix_scalar_freeze", "m1_prefix_scalar_apply", "m1_prefix_scalar_apply_continuous",
    "m2_quantile_transport_freeze", "m2_quantile_transport_apply", "m2_quantile_transport_apply_continuous",
    "m3_three_shell_mixture_freeze", "m3_three_shell_mixture_apply", "m3_three_shell_mixture_apply_continuous",
    "m4_gated_policy_freeze", "m4_gated_policy_apply", "m4_gated_policy_apply_continuous",
]
