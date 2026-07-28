"""Pre-formal Method Factory Sprint 001 — five mechanism-distinct constructs.

All constructs are PURE FUNCTIONS over receiver-visible, causal inputs. None
consumes TX truth, the true channel/Jones, the future window, or oracle affine
coefficients. Each returns predicted 16QAM symbols on the eval slice, scored
by ``cb1_evaluator.evaluate_dual_16qam`` (PI-SER, lower is better).

Shared failure mechanism (from baseline-adjudication synthesis):
    block-end gradient-descent CMA collapses ~40-60% of seeds to an inner-ring
    local minimum (|z|^2 ~ 0.16-0.3) on 16QAM. The information is recoverable
    (oracle affine -> PI-SER ~ 0); the failure is in the adaptive trajectory.

Lever points (each construct targets a distinct one):
    M1 cost surface (reduced-modulus CMA)
    M2 update trigger (trace-driven causal re-init)
    M3 initialization + selection (multi-start + alphabet-geometry pick)
    M4 post-eq affine cascade (conditional DD affine)
    M5 output remap (radius-shell remap)

Identity notes
--------------
M1/M2/M3 RE-RUN a block-end CMA equalizer (their deployable action is an
equalization choice), so they return a fresh z-stream. M4/M5 take an ALREADY-
converged baseline z-stream and post-process it (their deployable action is a
post-processor). Both classes share the frozen (cell, seed) realization.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ─── Public 16QAM alphabet geometry (analytic, no TX truth) ──────────────────
# Per-axis amplitudes {-3,-1,+1,+3}/sqrt(10); avg-power-normalized.
_AMP = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)
_RE, _IM = np.meshgrid(_AMP, _AMP)
ALPHABET_16QAM = (_RE + 1j * _IM).ravel()
ABS2_SHELLS = np.array([0.2, 1.0, 1.8])           # |s|^2 shells
SHELL_RADII = np.sqrt(ABS2_SHELLS)                # [0.447, 1.0, 1.342]
R2_GODARD_FULL = 1.32                             # E[|s|^4]/E[|s|^2], full alphabet
R2_INNER = 0.2                                    # reduced-modulus target (inner shell)


# ─── Block-end CMA core (reused by M1/M2/M3 with different cost/init/trigger) ─

def _blockwise_cma(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int,
    mu: float,
    R2: float,
    block_size: int,
    init_xx: np.ndarray | None = None,
    init_yy: np.ndarray | None = None,
    init_xy: np.ndarray | None = None,
    init_yx: np.ndarray | None = None,
    max_reinits: int = 0,
    reinit_trigger: str | None = None,
    reinit_threshold: float | None = None,
    reinit_consecutive: int = 3,
) -> dict[str, Any]:
    """Blockwise constant-modulus CMA with optional causal re-init (M2 lever).

    ``init_*`` default to center-tap. ``max_reinits>0`` enables M2's trace-driven
    re-init: if ``reinit_trigger=='output_power_ratio'`` and the block output
    power stays below ``reinit_threshold * R2`` for ``reinit_consecutive``
    blocks, reset weights to a fixed off-center diversity perturbation.
    Returns zX/zY and the per-block trace (receiver-visible, causal).

    The cost is the Godard-with-z gradient
        Dw ∝ (R2 - |z|^2) · z · r*
    identical to the frozen baseline when R2 = R2_GODARD_FULL and center-tap init.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    bs = int(block_size)

    def _default_init():
        w = np.zeros(L, dtype=complex); w[center] = 1.0
        return w

    wxx = init_xx.copy() if init_xx is not None else _default_init()
    wyy = init_yy.copy() if init_yy is not None else _default_init()
    wxy = init_xy.copy() if init_xy is not None else np.zeros(L, dtype=complex)
    wyx = init_yx.copy() if init_yx is not None else np.zeros(L, dtype=complex)

    init_norm = float(np.sqrt(
        np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
        + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
    ))
    norm_thresh = 10.0 * init_norm if init_norm > 0 else 10.0
    z_amp_thresh = 1e3

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)
    trace: list[dict[str, Any]] = []

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // bs

    diverged = False
    diverge_idx = None
    reinit_count = 0
    collapse_streak = 0

    def _diversity_perturbation(seed_idx: int):
        """Fixed, frozen diversity init perturbations for M3 / M2 re-init."""
        w = np.zeros(L, dtype=complex)
        w[center] = 1.0
        # 3 frozen off-center perturbations (no RNG, no tuning to seeds)
        if seed_idx == 0:
            pass  # center-tap (identity)
        elif seed_idx == 1:
            w[center] = 0.8; w[center - 1] = 0.6j   # +off-center phase
        elif seed_idx == 2:
            w[center] = 0.8; w[center + 1] = 0.6    # +off-center real
        else:
            w[center] = 0.8; w[center] = -0.8        # anti-center (sign flip)
        return w

    for blk in range(n_blocks):
        s = blk * bs
        e = s + bs
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]

        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        idx = s + half
        zX[idx:idx + bs] = zx_blk
        zY[idx:idx + bs] = zy_blk

        eX = R2 - np.abs(zx_blk) ** 2
        eY = R2 - np.abs(zy_blk) ** 2
        wxx += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))
        out_power = float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2) / 2.0)
        cm_err = float(np.mean((R2 - np.abs(zx_blk) ** 2) ** 2
                               + (R2 - np.abs(zy_blk) ** 2) ** 2))
        trace.append({
            "block": int(blk),
            "output_start": int(idx),
            "output_end": int(idx + bs),
            "cm_error": cm_err,
            "output_power": out_power,
            "w_norm": cur_norm,
        })

        # Divergence guard (frozen baseline criterion)
        if not diverged:
            if (cur_norm > norm_thresh or out_power > z_amp_thresh
                    or not np.isfinite(cur_norm)):
                diverged = True
                diverge_idx = idx + bs - 1
                break

        # M2 causal re-init trigger (receiver-visible, no look-ahead)
        if (reinit_trigger == "output_power_ratio" and max_reinits > 0
                and reinit_threshold is not None and not diverged):
            if out_power < reinit_threshold * R2:
                collapse_streak += 1
            else:
                collapse_streak = 0
            if collapse_streak >= reinit_consecutive and reinit_count < max_reinits:
                # Diversity re-init (frozen perturbation index)
                wxx = _diversity_perturbation(1 + reinit_count).copy()
                wyy = _diversity_perturbation(1 + reinit_count).copy()
                wxy = np.zeros(L, dtype=complex)
                wyx = np.zeros(L, dtype=complex)
                reinit_count += 1
                collapse_streak = 0

    return {
        "zX": zX,
        "zY": zY,
        "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": cur_norm,
        "init_w_norm": init_norm,
        "trace": trace,
        "reinit_count": reinit_count,
        "provenance": {
            "implementation": "methods._blockwise_cma",
            "gradient": "Godard-with-z",
            "R2": float(R2),
        },
    }


# ─── M1: Reduced-modulus CMA (cost-surface lever) ────────────────────────────

def m1_reduced_modulus_cma(
    realization: dict[str, Any],
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
) -> dict[str, Any]:
    """Block-end CMA targeting the inner 16QAM shell (R² = 0.2).

    Removes the inner-ring spurious attractor of the full-modulus Godard cost
    (R²=1.32) by pulling the cost minimum onto the inner shell. Same μ, n_tap,
    block_size, center-tap init as the frozen baseline. R_inner² is analytic
    (E[|s_inner|^4]/E[|s_inner|^2] = 0.2), NOT tuned.
    """
    raw = _blockwise_cma(
        realization["rX"], realization["rY"],
        n_tap=n_tap, mu=mu, R2=R2_INNER, block_size=block_size,
    )
    raw["construct"] = "M1_reduced_modulus_cma"
    raw["mechanism"] = "cost_surface_reduced_modulus"
    raw["deployable_action"] = "block-end Godard-with-z CMA with R2=0.2 (inner shell)"
    return raw


# ─── M2: Trace-driven causal re-init (update-trigger lever) ───────────────────

def m2_trace_reinit_cma(
    realization: dict[str, Any],
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
    reinit_threshold: float = 0.5,
    max_reinits: int = 2,
) -> dict[str, Any]:
    """Block-end CMA with causal trace-driven diversity re-init.

    Full-modulus cost (R²=1.32, = frozen baseline), but when output_power stays
    below ``reinit_threshold * R2`` (= 0.66, i.e. below the inner shell) for
    >= 3 consecutive blocks, reset weights to a frozen diversity perturbation.
    Threshold is frozen from the alphabet geometry (mid shell is 1.0; collapse
    signature is out_power < 0.5*1.32 = 0.66, between inner and mid), NOT tuned.
    """
    raw = _blockwise_cma(
        realization["rX"], realization["rY"],
        n_tap=n_tap, mu=mu, R2=R2_GODARD_FULL, block_size=block_size,
        max_reinits=max_reinits,
        reinit_trigger="output_power_ratio",
        reinit_threshold=reinit_threshold,
        reinit_consecutive=3,
    )
    raw["construct"] = "M2_trace_reinit_cma"
    raw["mechanism"] = "update_trigger_causal_reinit"
    raw["deployable_action"] = (
        "block-end Godard-with-z CMA (R2=1.32) with causal output-power collapse "
        "detector and frozen diversity re-init (max 2)"
    )
    return raw


# ─── M3: Multi-start CMA + alphabet-geometry selection (init+select lever) ───

def _alphabet_geometry_score(z_eval: np.ndarray) -> float:
    """Receiver-visible consistency of |z| with the public 16QAM |s|² shells.

    Lower = more consistent. Uses only the public alphabet's |s|² distribution
    moments (mean=1.0, the three shells) — NO TX truth. A collapsed z-stream
    has |z|² clustered near 0.2 (one shell over-populated) and will score worse
    on the spread match than a properly-converged stream using all three shells.
    """
    a = np.asarray(z_eval, dtype=complex).ravel()
    p = np.abs(a) ** 2
    # Per-shell population: fraction of points nearest each shell
    d = np.abs(p[:, None] - ABS2_SHELLS[None, :])
    nearest = np.argmin(d, axis=1)
    frac = np.array([np.mean(nearest == k) for k in range(3)])
    # Public-alphabet expected fractions: inner 4/16=0.25, mid 8/16=0.5, outer 4/16=0.25
    expected = np.array([0.25, 0.5, 0.25])
    # Total-variation distance (lower = more alphabet-consistent)
    tv = 0.5 * np.sum(np.abs(frac - expected))
    # Plus a mean-power term (E[|s|^2] = 1.0)
    mean_pen = abs(float(np.mean(p)) - 1.0)
    return float(tv + mean_pen)


def m3_multistart_select_cma(
    realization: dict[str, Any],
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    block_size: int = 64,
    K: int = 4,
    eval_slice: tuple[int, int] | None = None,
) -> dict[str, Any]:
    """K parallel block-end CMA runs (diversity inits) + alphabet-geometry pick.

    Inits (frozen, no RNG): center-tap, +off-center-phase, +off-center-real,
    anti-center. Selection = argmin receiver-visible alphabet-geometry score on
    the calibration-equivalent slice. No TX truth at selection time.
    """
    L = n_tap
    center = L // 2
    inits = []
    # init 0: center-tap
    w0 = np.zeros(L, dtype=complex); w0[center] = 1.0
    inits.append((w0.copy(), w0.copy()))
    # init 1: +off-center phase
    w1 = np.zeros(L, dtype=complex); w1[center] = 0.8; w1[center - 1] = 0.6j
    inits.append((w1.copy(), w1.copy()))
    # init 2: +off-center real
    w2 = np.zeros(L, dtype=complex); w2[center] = 0.8; w2[center + 1] = 0.6
    inits.append((w2.copy(), w2.copy()))
    # init 3: anti-center
    w3 = np.zeros(L, dtype=complex); w3[center] = -0.8; w3[center] = -0.8
    inits.append((w3.copy(), w3.copy()))

    candidates = []
    for k, (ixx, iyy) in enumerate(inits[:K]):
        raw = _blockwise_cma(
            realization["rX"], realization["rY"],
            n_tap=n_tap, mu=mu, R2=R2_GODARD_FULL, block_size=block_size,
            init_xx=ixx, init_yy=iyy,
        )
        if eval_slice is not None and not raw["diverged"]:
            s, e = eval_slice
            z = np.concatenate([raw["zX"][s:e], raw["zY"][s:e]])
            score = _alphabet_geometry_score(z)
        else:
            score = float("inf") if raw["diverged"] else _alphabet_geometry_score(
                np.concatenate([raw["zX"], raw["zY"]])
            )
        candidates.append({"k": k, "raw": raw, "score": score})

    # Pick best non-diverged by alphabet-geometry score
    valid = [c for c in candidates if not c["raw"]["diverged"]]
    if not valid:
        best = candidates[0]
    else:
        best = min(valid, key=lambda c: c["score"])

    out = dict(best["raw"])
    out["construct"] = "M3_multistart_select_cma"
    out["mechanism"] = "init_select_alphabet_geometry"
    out["deployable_action"] = (
        f"K={K} parallel block-end Godard-with-z CMA (R2=1.32) with diversity "
        "inits + receiver-visible alphabet-geometry selection"
    )
    out["m3_selected_k"] = best["k"]
    out["m3_all_scores"] = [float(c["score"]) for c in candidates]
    out["m3_all_diverged"] = [bool(c["raw"]["diverged"]) for c in candidates]
    return out


# ─── M4: Conditional DD affine cascade (post-eq cascade lever) ────────────────

def _affine_fit_z(z_cal: np.ndarray, target: np.ndarray, ridge: float) -> np.ndarray:
    """Complex 2x2 affine least-squares fit (reuses cb1_evaluator machinery)."""
    import importlib.util
    from pathlib import Path
    here = Path(__file__).resolve()
    scout_root = here.parents[3]
    p03 = scout_root / "P03-U19-residual-headroom" / "probe_evaluator.py"
    if not p03.exists():
        # fall back: direct LS
        Z = np.column_stack([z_cal, np.ones(z_cal.shape[0])])
        coef = np.linalg.lstsq(Z, target, rcond=None)[0]
        return coef
    spec = importlib.util.spec_from_file_location("m4_p03_probe", p03)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._affine_fit(z_cal, target, ridge)


def m4_conditional_dd_affine(
    z_calib: np.ndarray,
    z_eval: np.ndarray,
    *,
    ridge: float = 1e-6,
    collapse_threshold: float = 0.5,
) -> dict[str, Any]:
    """Trace-gated decision-directed affine refinement.

    Fits a 2x2 complex affine map z -> hard_16qam(z) on the calibration slice
    (DD pseudo-labels = public alphabet, no TX truth), applies to eval.
    Conditional: the gate is the receiver-visible calibration-slice collapse
    score (mean |z|^2 / E[|s|^2]); if the stream is NOT collapsed
    (>= collapse_threshold), pass through identity (= frozen baseline). So M4
    cannot hurt clean cells. Threshold 0.5 frozen from alphabet geometry.
    """
    from common._modulation import hard_decision
    cal = np.asarray(z_calib, dtype=complex)
    eva = np.asarray(z_eval, dtype=complex)

    # Receiver-visible collapse gate on calibration slice
    cal_power = float(np.mean(np.abs(cal) ** 2))
    gate_open = cal_power < collapse_threshold  # collapsed if power < 0.5

    if not gate_open:
        # Identity pass-through = frozen baseline behavior on clean cells
        return {
            "construct": "M4_conditional_dd_affine",
            "mechanism": "post_eq_conditional_cascade",
            "deployable_action": "identity (gate closed; clean cell)",
            "gate_open": False,
            "cal_power": cal_power,
            "predicted": hard_decision(np.asarray(eva, dtype=np.complex128), mod="qam16"),
            "coefficients": None,
        }

    # DD pseudo-labels from public alphabet
    pseudo = hard_decision(np.asarray(cal, dtype=np.complex128), mod="qam16")
    coef = _affine_fit_z(cal, pseudo, ridge)

    # Apply DD affine to eval, then hard-decide
    Z = np.column_stack([eva, np.ones(eva.shape[0])])
    corrected = Z @ coef
    predicted = hard_decision(np.asarray(corrected, dtype=np.complex128), mod="qam16")
    return {
        "construct": "M4_conditional_dd_affine",
        "mechanism": "post_eq_conditional_cascade",
        "deployable_action": (
            "decision-directed 2x2 affine fit on z-derived 16QAM pseudo-labels, "
            "applied only when calibration-slice collapse gate opens"
        ),
        "gate_open": True,
        "cal_power": cal_power,
        "predicted": predicted,
        "coefficients": coef,
    }


# ─── M5: Radius-shell remap (output-remap lever) ─────────────────────────────

def m5_radius_shell_remap(z_eval: np.ndarray) -> dict[str, Any]:
    """Closed-form radius-shell remap of collapsed z to nearest valid shell.

    Estimates the receiver-visible collapsed radius r_collapse = median(|z|),
    then per symbol scales z onto the nearest public 16QAM shell radius via a
    2-step fixed-point iteration. No adaptive loop, no TX truth. Pure post-proc.
    Accepts 1D (single pol) or 2D (N, n_pol) input; operates elementwise on |z|.
    """
    from common._modulation import hard_decision
    z = np.asarray(z_eval, dtype=complex).copy()
    orig_shape = z.shape
    flat = z.ravel()
    r = np.abs(flat)

    # If the stream already spans the alphabet (not collapsed), remap is identity.
    # Collapse signature (from baseline-adjudication diagnosis): mean|z|^2
    # collapses to ~0.16-0.3 (inner shell) vs the alphabet's E[|s|^2]=1.0.
    # Gate on mean|z|^2: collapsed if < 0.5*E[|s|^2] = 0.5 (frozen from alphabet).
    mean_p = float(np.mean(r ** 2))
    span = float(np.std(r))
    collapsed = mean_p < 0.5
    if not collapsed:
        return {
            "construct": "M5_radius_shell_remap",
            "mechanism": "output_remap_radius_shell",
            "deployable_action": "identity (stream not collapsed; mean|z|^2 healthy)",
            "collapsed": False,
            "r_span": span,
            "mean_abs2": mean_p,
            "predicted": np.asarray(hard_decision(z, mod="qam16")).reshape(orig_shape),
        }

    # Collapsed: pull each symbol's radius to nearest shell (2 fixed-point steps)
    remapped = flat.copy()
    for _ in range(2):
        rr = np.abs(remapped)
        # nearest shell radius (elementwise over the flat array)
        target = SHELL_RADII[np.argmin(np.abs(rr[:, None] - SHELL_RADII[None, :]), axis=1)]
        scale = np.where(rr > 1e-9, target / rr, 1.0)
        remapped = remapped * scale

    predicted = np.asarray(hard_decision(remapped, mod="qam16")).reshape(orig_shape)
    return {
        "construct": "M5_radius_shell_remap",
        "mechanism": "output_remap_radius_shell",
        "deployable_action": (
            "closed-form per-symbol radius rescaling to nearest public 16QAM shell "
            "(2 fixed-point steps), gated on receiver-visible mean|z|^2 < 0.5"
        ),
        "collapsed": True,
        "r_span": span,
        "mean_abs2": mean_p,
        "predicted": predicted,
    }


__all__ = [
    "ALPHABET_16QAM", "ABS2_SHELLS", "SHELL_RADII",
    "R2_GODARD_FULL", "R2_INNER",
    "m1_reduced_modulus_cma",
    "m2_trace_reinit_cma",
    "m3_multistart_select_cma",
    "m4_conditional_dd_affine",
    "m5_radius_shell_remap",
    "_alphabet_geometry_score",
]
