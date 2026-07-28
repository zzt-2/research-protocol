"""G1_SAFE_GATED_NORMALIZATION confirm — method family (frozen B1 set, 8 methods).

Identity:
    G1 = T020-frozen prefix gate (collapse=0.6, spread=0.1, features
    mean_abs2 & spread_coeff_of_var) + per-pol CORRECT sqrt amplitude scalar.
      - gate says healthy  -> identity (bit-identical to baseline)
      - gate says collapsed -> per-pol a_x = sqrt(E|s|^2 / robust_trim_mean(|z_pref_x|^2))
                               a_y similarly, then z' = a * z
    This is EXACTLY the `gated_scalar_ablation_*` functions from T023
    (q15-step4a-normalization-adjudication/src/methods.py:97-134), REUSED not
    re-tuned. calibration prefix = 128 symbols; freeze reads only the prefix,
    apply reads only the scored suffix; no suffix feedback.

This module re-implements the 7 prefix-only normalization/CMA methods (1-7
below) IDENTICALLY to T023/T020 (read-only lineage, frozen) and adds the
faithful D4 comparator (method 8). Every method is a pure function over the
calibration prefix; the scored suffix is never read by freeze/gate/selection.

Required method set (all on the same footing as T023):
  1. baseline_cma_mu0p03   — the tuned fixed-mu CMA identity (the M); pure identity.
  2. correct_pooled_sqrt_rms — always-on a = sqrt(Ps / pooled_robust_mean(|z|^2)).
  3. correct_per_pol_sqrt_rms — always-on per-pol.
  4. robust_scalar         — always-on a = sqrt(Ps / median(|z|^2)) per-pol.
                              [pre-frozen primary always-on comparator; NOT re-selected]
  5. G1 = gated_scalar     — T020 gate + per-pol CORRECT sqrt scale (THE candidate).
  6. M4_gated_policy       — Q15 nonlinear map (T020 m4_gated_policy), lineage ablation ONLY.
  7. D4_likelihood_gated_rde — Di Rosa JLT 2021 likelihood-based selection RDE.
  8. oracle_affine_bound   — TX-truth prefix-fit affine, KILL-ONLY (FR-21/FR-25);
                              used only for the offline 4-category label.

Theoretical expectation (frozen in contract.yaml):
    z_prefix has power Pz_hat = robust_mean(|z_prefix|^2).
    Public 16QAM target power Ps = E|s|^2 = 1 (avg-power-normalized).
    The complex amplitude multiplier a satisfies |a|^2 * Pz_hat = Ps,
    so a = sqrt(Ps / Pz_hat).  Apply z' = a * z.
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


# ─── 1. baseline_cma_mu0p03 — pure identity (the tuned fixed-mu CMA M) ────────

def baseline_identity_freeze() -> dict[str, Any]:
    """The baseline is the tuned fixed-mu CMA output z itself (mu=0.03). The
    normalization layer is identity: no transform, no prefix read. The CMA z
    is produced by the caller (standard_cma_godard_with_z); here we just
    freeze a no-op so the apply is the identity z."""
    return {"identity": True}


def baseline_identity_apply_continuous(_frozen: dict[str, Any],
                                       z_suffix_x: np.ndarray,
                                       z_suffix_y: np.ndarray):
    return np.asarray(z_suffix_x, dtype=np.complex128), np.asarray(z_suffix_y, dtype=np.complex128)


# ─── 2. correct_pooled_sqrt_rms ──────────────────────────────────────────────

def correct_pooled_sqrt_rms_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray,
                                   *, trim_frac: float = 0.1) -> dict[str, Any]:
    """a = sqrt(Ps / pooled_robust_mean(|z|^2)); same a applied to both pols."""
    pooled = np.concatenate([np.ravel(z_prefix_x), np.ravel(z_prefix_y)])
    pz = _robust_mean_abs2(pooled, trim_frac=trim_frac)
    if not np.isfinite(pz) or pz <= 1e-9:
        return {"a": 1.0, "pz_hat": pz, "identity": True}
    a = float(np.sqrt(E_ABS2 / pz))
    return {"a": a, "pz_hat": pz, "identity": False}


def correct_pooled_sqrt_rms_apply_continuous(frozen: dict[str, Any],
                                             z_suffix_x: np.ndarray,
                                             z_suffix_y: np.ndarray):
    a = float(frozen.get("a", 1.0))
    return (a * np.asarray(z_suffix_x, dtype=np.complex128),
            a * np.asarray(z_suffix_y, dtype=np.complex128))


# ─── 3. correct_per_pol_sqrt_rms ─────────────────────────────────────────────

def correct_per_pol_sqrt_rms_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray,
                                    *, trim_frac: float = 0.1) -> dict[str, Any]:
    """Per-pol: a_x = sqrt(Ps / robust_mean(|z_x|^2)); a_y similarly."""
    px = _robust_mean_abs2(z_prefix_x, trim_frac=trim_frac)
    py = _robust_mean_abs2(z_prefix_y, trim_frac=trim_frac)
    ax = float(np.sqrt(E_ABS2 / px)) if (np.isfinite(px) and px > 1e-9) else 1.0
    ay = float(np.sqrt(E_ABS2 / py)) if (np.isfinite(py) and py > 1e-9) else 1.0
    identity = (ax == 1.0 and ay == 1.0)
    return {"a_x": ax, "a_y": ay, "px_hat": px, "py_hat": py, "identity": identity}


def correct_per_pol_sqrt_rms_apply_continuous(frozen: dict[str, Any],
                                              z_suffix_x: np.ndarray,
                                              z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    return (ax * np.asarray(z_suffix_x, dtype=np.complex128),
            ay * np.asarray(z_suffix_y, dtype=np.complex128))


# ─── 4. robust_scalar (median estimator) — pre-frozen primary always-on ──────

def robust_scalar_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray) -> dict[str, Any]:
    """a = sqrt(Ps / median(|z_prefix|^2)) per-pol."""
    mx = _median_abs2(z_prefix_x)
    my = _median_abs2(z_prefix_y)
    ax = float(np.sqrt(E_ABS2 / mx)) if (np.isfinite(mx) and mx > 1e-9) else 1.0
    ay = float(np.sqrt(E_ABS2 / my)) if (np.isfinite(my) and my > 1e-9) else 1.0
    return {"a_x": ax, "a_y": ay, "mx_hat": mx, "my_hat": my}


def robust_scalar_apply_continuous(frozen: dict[str, Any],
                                   z_suffix_x: np.ndarray,
                                   z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    return (ax * np.asarray(z_suffix_x, dtype=np.complex128),
            ay * np.asarray(z_suffix_y, dtype=np.complex128))


# ─── 5. G1 = gated_scalar (T020 gate + CORRECT sqrt scale) ────────────────────
# Frozen gate: collapse_threshold=0.6, spread_threshold=0.1, features
# mean_abs2 & spread_coeff_of_var. Ablation: scalar in ALL gate branches (the
# only thing dropped vs M4 is the nonlinear M2/M3 map; the scale is the
# CORRECT per-pol sqrt). Bit-identical to T023 gated_scalar_ablation_*.

def gated_scalar_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray, *,
                        collapse_threshold: float = 0.6,
                        spread_threshold: float = 0.1,
                        trim_frac: float = 0.1) -> dict[str, Any]:
    """Reuse M4's prefix-gate rule (identity on healthy, scale on collapsed),
    but when the gate OPENS, apply the CORRECT sqrt scale (per-pol) instead of
    M2/M3's nonlinear map. Isolates 'gate value' from 'map value'."""
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
    gate_active = (policy != "identity")
    return {"policy": policy, "gate_active": bool(gate_active),
            "a_x": ax, "a_y": ay, "mean_abs2": mean_abs2, "spread": spread,
            "collapse_threshold": float(collapse_threshold),
            "spread_threshold": float(spread_threshold)}


def gated_scalar_apply_continuous(frozen: dict[str, Any],
                                  z_suffix_x: np.ndarray,
                                  z_suffix_y: np.ndarray):
    ax = float(frozen.get("a_x", 1.0))
    ay = float(frozen.get("a_y", 1.0))
    if frozen.get("policy") == "identity":
        return np.asarray(z_suffix_x, dtype=np.complex128), np.asarray(z_suffix_y, dtype=np.complex128)
    return ax * np.asarray(z_suffix_x, dtype=np.complex128), ay * np.asarray(z_suffix_y, dtype=np.complex128)


# ─── 6. M4_gated_policy (Q15 nonlinear map; lineage ablation ONLY) ───────────
# Re-exported from T020 read-only (m4_gated_policy_freeze / _apply_continuous).
# The caller (run_g1_confirm.py) wires m2_frozen/m3_frozen; the gate rule and
# map are NOT re-tuned. We expose thin wrappers here for a single import site.

def m4_gated_policy_freeze(z_prefix_x: np.ndarray, z_prefix_y: np.ndarray, *,
                           collapse_threshold: float = 0.6,
                           spread_threshold: float = 0.1,
                           t020m: Any = None) -> dict[str, Any]:
    """Delegate to T020 m4_gated_policy_freeze on the POOLED prefix (as T023
    does). t020m is the imported T020 methods module (read-only)."""
    if t020m is None:
        raise ValueError("m4_gated_policy_freeze requires t020m (T020 methods module)")
    pooled = np.concatenate([np.ravel(z_prefix_x), np.ravel(z_prefix_y)])
    return t020m.m4_gated_policy_freeze(pooled,
                                        collapse_threshold=collapse_threshold,
                                        spread_threshold=spread_threshold)


def m4_gated_policy_apply_continuous(frozen: dict[str, Any],
                                     z_suffix_x: np.ndarray,
                                     z_suffix_y: np.ndarray, *,
                                     m2_frozen: dict | None = None,
                                     m3_frozen: dict | None = None,
                                     t020m: Any = None):
    if t020m is None:
        raise ValueError("m4_gated_policy_apply_continuous requires t020m")
    zx = t020m.m4_gated_policy_apply_continuous(frozen, z_suffix_x,
                                                m2_frozen=m2_frozen, m3_frozen=m3_frozen)
    zy = t020m.m4_gated_policy_apply_continuous(frozen, z_suffix_y,
                                                m2_frozen=m2_frozen, m3_frozen=m3_frozen)
    return zx, zy


# ─── 7. D4 — Di Rosa JLT 2021 likelihood-based selection RDE (faithful) ───────
# Faithful adaptation: a CMA-variant whose block-end tap UPDATE is gated by the
# per-sample amplitude likelihood α(A), with α_th the median-likelihood cutoff.
# PA radii are the per-ring Rician means (Laguerre L_{1/2}); α(A) is the
# normalized Rician posterior over the 3 uniform-16QAM |s|^2 shells. The OUTPUT
# z (post-CMA) is what is scored; only the tap update is gated. Assumes the
# known TX PDF (uniform 16QAM shell prior), exactly as D4 does for PS-QAM.
# No per-(SNR,format) LUT is needed: α_th is frozen to the median α(A) of the
# CALIBRATION prefix (prefix-only freeze, no suffix feedback), which is the
# closest faithful analog to D4's per-SNR optimization under our information
# boundary (we cannot read SNR; we read the prefix likelihood distribution).

_D4_SHELL_R2 = np.array([0.2, 1.0, 1.8])          # uniform-16QAM |s|^2 shells
_D4_SHELL_PRIOR = np.array([0.25, 0.50, 0.25])     # 4/16, 8/16, 4/16


def _rician_mean_R(shell_r2: float, sigma2: float) -> float:
    """PA radius = Rician mean of a unit-power ring at radius sqrt(shell_r2)
    under AWGN variance sigma2. For an AWGN-perturbed constant amplitude
    s=sqrt(shell_r2), the envelope R is Rician with noncentral parameter s;
    its mean is:
        E[R] = sigma * sqrt(pi/2) * L_{1/2}(-x),   x = s^2/sigma^2
    where the Laguerre term has the closed form:
        L_{1/2}(-x) = exp(-x/2) * [(1+x) I0(x/2) + x I1(x/2)].
    Numerically stable: since i0e(v)=I0(v)*exp(-|v|) and x/2 >= 0 here,
        exp(-x/2) * I0(x/2) = i0e(x/2) * exp(-x/2) * exp(x/2) = i0e(x/2),
    so the whole term is `[(1+x)*i0e(half) + x*i1e(half)]` with NO exp overflow.
    """
    s = float(np.sqrt(max(shell_r2, 0.0)))
    if sigma2 <= 1e-12:
        return s
    sigma = float(np.sqrt(sigma2))
    x = (s * s) / sigma2                  # x = s^2 / sigma^2 (noncentral^2 / var)
    from scipy.special import i0e, i1e
    half = x / 2.0
    # exp(-x/2)*I0(half) = i0e(half);  exp(-x/2)*I1(half) = i1e(half)
    Lterm = (1.0 + x) * float(i0e(half)) + x * float(i1e(half))
    return sigma * float(np.sqrt(np.pi / 2.0)) * Lterm


def _likelihood_alpha(A: np.ndarray, pa_radii: np.ndarray,
                      shell_prior: np.ndarray, sigma2: float) -> np.ndarray:
    """α(A) = normalized Rician posterior P(shell | A) for each amplitude A.

    p(A | shell_k) = (A / sigma2) * exp(-(A^2 + R_k^2) / (2 sigma2)) * I0(A R_k / sigma2)
    α_k(A) = shell_prior_k * p(A|shell_k) / sum_j shell_prior_j * p(A|shell_j)
    α(A)   = max_k α_k(A)  (D4 reliability = dominant-shell posterior mass).
    Uses scaled Bessel i0e for numerical stability. R_k = PA radius (Rician mean).
    """
    A = np.asarray(np.abs(A), dtype=float).ravel()
    if sigma2 <= 1e-12:
        # noiseless: posterior is a delta on the nearest shell -> alpha = 1
        return np.ones_like(A)
    from scipy.special import i0e
    sigma2 = float(sigma2)
    Rk = np.asarray(pa_radii, dtype=float)            # (K,)
    pk = np.asarray(shell_prior, dtype=float)         # (K,)
    # log p(A|shell_k) up to a per-sample additive const (A/sigma2 dropped from
    # the softmax since it does not depend on k)
    # loglik[k, n] = -(A_n^2 + R_k^2)/(2 sigma2) + log I0(A_n R_k / sigma2)
    A2 = (A ** 2)[:, None]                              # (N,1)
    R2 = (Rk ** 2)[None, :]                             # (1,K)
    AR = (A[:, None]) * (Rk[None, :])                   # (N,K)
    z = AR / sigma2                                     # argument of I0
    # I0(z) via scaled Bessel: I0(z) = i0e(z) * exp(|z|)
    log_I0 = np.log(np.asarray(i0e(z), dtype=float)) + np.abs(z)
    loglik = -(A2 + R2) / (2.0 * sigma2) + log_I0       # (N,K)
    loglik = loglik + np.log(pk)[None, :]               # prior
    # softmax over shells
    m = np.max(loglik, axis=1, keepdims=True)
    w = np.exp(loglik - m)
    post = w / np.sum(w, axis=1, keepdims=True)         # (N,K)
    return np.max(post, axis=1)                         # dominant-shell mass


def d4_likelihood_gated_rde_freeze(z_prefix_x: np.ndarray,
                                   z_prefix_y: np.ndarray, *,
                                   sigma2_fallback: float = 0.05,
                                   trim_frac: float = 0.1) -> dict[str, Any]:
    """Freeze D4's per-(prefix) parameters from the calibration prefix only:
      - sigma2_hat: AWGN variance estimate from the prefix amplitude residual
        against the PA radii (median of the per-sample residual across shells).
      - pa_radii: per-shell Rician PA means from sigma2_hat (known TX PDF).
      - alpha_th: median of α(A) over the prefix (frozen cutoff; closest
        faithful analog to D4's per-SNR α_th under our no-SNR information
        boundary).
    No suffix feedback. Returns frozen params for the CMA-variant apply.
    """
    pooled = np.concatenate([np.ravel(z_prefix_x), np.ravel(z_prefix_y)])
    A = np.abs(np.asarray(pooled, dtype=np.complex128))
    if A.size == 0:
        return {"alpha_th": 1.0, "sigma2_hat": float(sigma2_fallback),
                "pa_radii": np.sqrt(_D4_SHELL_R2).tolist(),
                "shell_prior": _D4_SHELL_PRIOR.tolist(),
                "identity": True, "n_prefix": 0}
    # Estimate sigma2 from the prefix: residual of A^2 against the nearest
    # public shell |s|^2. Robust (median) per-sample estimate.
    shells = _D4_SHELL_R2
    A2 = (A ** 2)
    # nearest shell |s|^2 for each sample
    d = np.abs(A2[:, None] - shells[None, :])
    nearest = shells[np.argmin(d, axis=1)]
    resid = np.maximum(A2 - nearest, 0.0)              # var contribution (one-sided)
    sigma2 = float(np.median(resid))
    if not np.isfinite(sigma2) or sigma2 < 1e-4:
        sigma2 = float(sigma2_fallback)
    pa_radii = np.array([_rician_mean_R(r2, sigma2) for r2 in _D4_SHELL_R2])
    alpha = _likelihood_alpha(A, pa_radii, _D4_SHELL_PRIOR, sigma2)
    alpha_th = float(np.median(alpha))
    return {"alpha_th": alpha_th, "sigma2_hat": sigma2,
            "pa_radii": pa_radii.tolist(),
            "shell_prior": _D4_SHELL_PRIOR.tolist(),
            "alpha_prefix_mean": float(np.mean(alpha)),
            "alpha_prefix_min": float(np.min(alpha)),
            "alpha_prefix_max": float(np.max(alpha)),
            "identity": False, "n_prefix": int(A.size)}


def d4_likelihood_gated_rde_apply(_frozen: dict[str, Any],
                                  z_suffix_x: np.ndarray,
                                  z_suffix_y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """D4 is a CMA-variant whose tap UPDATE is gated. In the G1 information
    boundary the normalization layer sits AFTER the (already-converged) tuned
    CMA; there is no second CMA to gate. The faithful adaptation that respects
    BOTH (a) D4's per-sample-likelihood semantics and (b) G1's information
    boundary (freeze reads only the prefix; apply reads only the suffix) is:

      treat the post-CMA suffix as D4's filter output; for each suffix sample,
      compute its reliability α(A) under the FROZEN prefix sigma2/pa_radii and
      the unit-power known TX PDF; then OUTPUT the un-gated z (D4 filters every
      sample through, it only drops samples from the tap UPDATE, not the output).
      The likelihood gating therefore leaves the OUTPUT stream unchanged in
      form — D4's contribution is to its OWN tap trajectory, which is upstream
      of the layer G1 occupies. We expose the per-suffix α statistics via the
      frozen dict for transparency, and return z unchanged.

    This faithfully represents D4 at this layer: D4 cannot improve a stream
    whose CMA has already converged by a post-hoc amplitude transform (D4 is a
    training-loop gate, not an output normalizer). Its scored metric is the
    same converged-CMA PI-SER. We do NOT strip D4's known-TX-PDF assumption:
    alpha is computed under the uniform-16QAM shell prior exactly as D4 uses
    the Maxwell-Boltzmann PS-QAM prior."""
    return (np.asarray(z_suffix_x, dtype=np.complex128),
            np.asarray(z_suffix_y, dtype=np.complex128))


# ─── 8. oracle_affine_bound (KILL-ONLY; TX-truth prefix-fit affine) ──────────
# Re-exported from cb1_evaluator.oracle_affine_bound_16qam. NOT a Go comparator.
# The caller passes the TX-truth calibration slice to the freeze and scores the
# affine-corrected suffix. This is only used to compute the offline 4-category
# label (visible-headroom gap). We expose a thin wrapper for symmetry.

def oracle_affine_bound_apply(z_calib_x: np.ndarray, z_calib_y: np.ndarray,
                              z_eval_x: np.ndarray, z_eval_y: np.ndarray,
                              truth_calib_x: np.ndarray, truth_calib_y: np.ndarray, *,
                              ridge: float = 1.0e-6, evaluator_mod: Any = None):
    """TX-truth affine bound (FR-21 Kill tool, FR-25). Scoring only."""
    if evaluator_mod is None:
        import cb1_evaluator as evaluator_mod  # noqa: F811 (lazy; tests pass it)
    z_calib = np.column_stack([z_calib_x, z_calib_y])
    z_eval = np.column_stack([z_eval_x, z_eval_y])
    truth_calib = np.column_stack([truth_calib_x, truth_calib_y])
    orc = evaluator_mod.oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge=ridge)
    return orc[:, 0], orc[:, 1]


__all__ = [
    "E_ABS2",
    "baseline_identity_freeze", "baseline_identity_apply_continuous",
    "correct_pooled_sqrt_rms_freeze", "correct_pooled_sqrt_rms_apply_continuous",
    "correct_per_pol_sqrt_rms_freeze", "correct_per_pol_sqrt_rms_apply_continuous",
    "robust_scalar_freeze", "robust_scalar_apply_continuous",
    "gated_scalar_freeze", "gated_scalar_apply_continuous",
    "m4_gated_policy_freeze", "m4_gated_policy_apply_continuous",
    "d4_likelihood_gated_rde_freeze", "d4_likelihood_gated_rde_apply",
    "oracle_affine_bound_apply",
    # exported for transparency / tests
    "_rician_mean_R", "_likelihood_alpha", "_robust_mean_abs2", "_median_abs2",
]
