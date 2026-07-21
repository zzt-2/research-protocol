"""Fairness Batch B01 candidates: C05, C08, C10, C11.

Implements four candidates / comparators for the fairness-batch-b01 contract
(``batch-contract.v1.yaml``). Each shares the CB1 modulation-generic closure
and the same channel contract as the CMA anchor and MMA comparator. They
differ only in the algorithm placed between ``rX/rY`` and the z-stream.

Provenance (per batch-contract.v1.yaml provenance_gate):
  - C05 CUSUM: Page 1954 Biometrika; Basseville-Nikiforov 1993 §2.2.
  - C08 LinUCB: Li, Chu, Langford, Schapire WWW 2010 §3.3.
  - C10 per-symbol CMA: Godard 1980 with block_size=1 (stochastic gradient).
  - C11 CMA + DD-LMS: Sato 1975 TCOM Eq.(4); Kikuchi JLT 2016 §IV.B.
  - CMA anchor (Godard-with-z): inherited from cb1_cell_runner.

Identity gates:
  - C10 / C11 stage-1 gradient stamp = "Godard-with-z" (same as anchor).
  - C10 differs ONLY in block_size (=1) and possibly mu (grid-tuned).
  - C11 stage-1 = anchor exactly; stage-2 = DD-LMS warm-start.
  - C05 / C08 do NOT touch the CMA weight update identity.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# =============================================================================
# C10: per-symbol stochastic-gradient CMA (Godard-with-z, block_size=1)
# =============================================================================
# Tests H021 (block-end bottleneck) directly. Same gradient as the CMA anchor
# but block_size=1 (one weight update per symbol). Also accepts a smaller mu
# to keep per-symbol updates stable (per-symbol gradients are higher variance).

def c10_per_symbol_cma(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-4,  # default smaller than anchor's 1e-3 (per-symbol)
    R2: float = 1.32,
) -> dict[str, Any]:
    """Per-symbol SGD CMA (Godard-with-z). block_size=1.

    Replicates standard_cma_godard_with_z EXACTLY except block_size=1: one
    weight update per symbol using the per-symbol Godard-with-z gradient
    Δw ∝ (R²-|z|²)·z·r*. Identity-gate gradient stamp = "Godard-with-z".

    Per batch-contract.v1.yaml sanity c10_smoke_clean_16qam: on a clean 16QAM
    input, converges to PI-SER ~ 0 within N=512.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half

    # Center-tap init — IDENTICAL to anchor (only block_size differs).
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    init_norm = _wnorm()

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)
    # For trace parity with anchor (per-block snapshots), record every
    # `trace_stride` symbols. Default = 64 to match anchor's block trace
    # density (so downstream feature extraction uses the same granularity).
    trace_stride = 64
    trace: list[dict[str, Any]] = []

    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3
    diverged = False
    diverge_idx = None

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1

    for i in range(n_valid):
        rx = rX_win[i]
        ry = rY_win[i]

        zx = np.vdot(wxx, rx) + np.vdot(wxy, ry)
        zy = np.vdot(wyx, rx) + np.vdot(wyy, ry)

        idx = i + half
        zX[idx] = zx
        zY[idx] = zy

        # Per-symbol Godard-with-z gradient (same form as anchor, block_size=1).
        eX = R2 - abs(zx) ** 2
        eY = R2 - abs(zy) ** 2
        gx = mu * eX * zx
        gy = mu * eY * zy
        wxx += gx * np.conj(rx)
        wxy += gx * np.conj(ry)
        wyx += gy * np.conj(rx)
        wyy += gy * np.conj(ry)

        # Per-symbol divergence check (per-symbol updates are higher variance
        # than block-end; check every symbol to catch runaway early).
        if not diverged:
            azx = abs(zx)
            azy = abs(zy)
            if (azx > z_amp_thresh or azy > z_amp_thresh
                    or not np.isfinite(azx) or not np.isfinite(azy)):
                diverged = True
                diverge_idx = idx
                break  # stop the per-symbol loop immediately on divergence

        if (i + 1) % trace_stride == 0:
            cur_norm = _wnorm()
            # Snapshot output power over the last trace_stride samples.
            s0 = max(0, idx + 1 - trace_stride)
            seg_x = zX[s0:idx + 1]
            seg_y = zY[s0:idx + 1]
            out_pow = float(np.mean(np.abs(seg_x) ** 2 + np.abs(seg_y) ** 2)) if len(seg_x) else float("nan")
            ratio = out_pow / (2.0 * R2) if R2 > 0 else float("nan")
            trace.append({
                "output_start": int(s0),
                "output_end": int(idx + 1),
                "cm_error": float(np.mean((R2 - np.abs(seg_x) ** 2) ** 2 + (R2 - np.abs(seg_y) ** 2) ** 2)) if len(seg_x) else float("nan"),
                "output_power": out_pow,
                "z2_over_R2_ratio": ratio,
                "update_norm": float(abs(gx) * np.sqrt(float(np.sum(np.abs(rx) ** 2)) + float(np.sum(np.abs(ry) ** 2)))),
                "w_norm": cur_norm,
                "z_amp_max": float(max(abs(zx), abs(zy))),
            })
            if not diverged:
                if (cur_norm > norm_thresh or not np.isfinite(cur_norm)
                        or abs(zx) > z_amp_thresh or abs(zy) > z_amp_thresh):
                    diverged = True
                    diverge_idx = idx

    return {
        "zX": zX,
        "zY": zY,
        "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(),
        "init_w_norm": init_norm,
        "trace": trace,
        "provenance": {
            "implementation": "b01_candidates.c10_per_symbol_cma",
            "entry": "per-symbol stochastic-gradient CMA (Godard 1980 with block_size=1)",
            "gradient": "Godard-with-z",  # identity gate match
            "block_size": 1,
            "mu": float(mu),
            "R2": float(R2),
        },
    }


# =============================================================================
# C11: CMA anchor (stage 1) + DD-LMS cascade (stage 2)
# =============================================================================
# Standard fiber-coherent two-stage: stage 1 = anchor (block_size=64) for
# coarse blind convergence; stage 2 = DD-LMS warm-started from stage-1 final
# weights, using nearest-16QAM hard decisions as the reference.
#
# Per Sato 1975 Eq.(4): DD cost J_DD = E[|s_hat(z) - z|^2], s_hat = hard(z).
# Gradient: Δw ∝ (s_hat - z)·r*.
#
# CRITICAL: on collapsed seeds (inner-ring z), hard decisions are wrong
# (inner-ring symbols), so DD-LMS should NOT recover them. This is the
# pre-registered hypothesis (batch-contract C11 purpose).

# Import the anchor lazily so this module is importable in any cwd.
def _import_anchor():
    import importlib.util
    from pathlib import Path
    here = Path(__file__).resolve()
    # here = .../fairness-batch-b01/b01_candidates.py
    anchor_path = here.parents[1] / "baseline-atlas" / "cb1_cell_runner.py"
    spec = importlib.util.spec_from_file_location("_b01_anchor_runner", anchor_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def c11_cma_dd_lms_cascade(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    cma_mu: float = 1e-3,
    cma_R2: float = 1.32,
    cma_block_size: int = 64,
    dd_step_size: float = 1e-3,
    dd_iterations: int = 1,
    hard_decision_fn,
) -> dict[str, Any]:
    """CMA anchor (stage 1) followed by DD-LMS refinement (stage 2).

    Stage 1: standard_cma_godard_with_z, unchanged. Produces z_stream_stage1
    and final weights (wxx, wxy, wyx, wyy).

    Stage 2: DD-LMS warm-started from stage-1 final weights. Uses nearest-
    16QAM hard decisions as reference (Sato 1975 Eq.(4)). `dd_iterations`
    passes over the full stream.

    `hard_decision_fn`: callable z -> hard-decision symbols (e.g.
    cb1_evaluator.hard_16qam). Injected to keep this module decoupled from
    the modulation module.
    """
    anchor = _import_anchor()
    stage1 = anchor.standard_cma_godard_with_z(
        rX, rY, n_tap=n_tap, mu=cma_mu, R2=cma_R2, block_size=cma_block_size,
    )

    if stage1["diverged"]:
        # Stage 2 cannot recover a diverged stage 1; return stage 1 as-is.
        stage1["provenance"] = {
            **stage1["provenance"],
            "implementation": "b01_candidates.c11_cma_dd_lms_cascade",
            "stage_2": "SKIPPED_stage_1_diverged",
        }
        return stage1

    # Recover stage-1 final weights by re-running the anchor's weight loop.
    # The anchor returns final_w_norm but not the weights themselves; we
    # reconstruct them deterministically by replaying the stage-1 update.
    # This is O(N) extra work but keeps the anchor module unchanged.
    # Alternative: refactor the anchor to return weights. We choose replay
    # to preserve protected-history byte-equivalence of the anchor module.
    rXa = np.asarray(rX, dtype=complex)
    rYa = np.asarray(rY, dtype=complex)
    Na = len(rXa)
    L = int(n_tap)
    half = L // 2
    center = half
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)
    rX_win = sliding_window_view(rXa, L)
    rY_win = sliding_window_view(rYa, L)
    n_valid = Na - L + 1
    bs = int(cma_block_size)
    n_blocks = n_valid // bs
    for blk in range(n_blocks):
        s = blk * bs
        e = s + bs
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy
        eX = cma_R2 - np.abs(zx_blk) ** 2
        eY = cma_R2 - np.abs(zy_blk) ** 2
        wxx += cma_mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += cma_mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += cma_mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += cma_mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)
    # End of stage-1 replay: wxx/wxy/wyx/wyy = stage-1 final weights.

    # Stage 2: DD-LMS refinement, per-symbol update using hard decisions.
    # Same per-symbol SGD structure as C10 but with DD cost (Sato Eq.(4)).
    zX = stage1["zX"].copy()
    zY = stage1["zY"].copy()
    norm_thresh = 10.0 * float(stage1["init_w_norm"])
    z_amp_thresh = 1e3
    diverged_2 = False
    diverge_idx_2 = None

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    for _ in range(int(dd_iterations)):
        for i in range(n_valid):
            rx = rX_win[i]
            ry = rY_win[i]
            zx = np.vdot(wxx, rx) + np.vdot(wxy, ry)
            zy = np.vdot(wyx, rx) + np.vdot(wyy, ry)
            # Hard decision on the per-symbol output.
            s_hat_x = complex(hard_decision_fn(np.array([zx]))[0])
            s_hat_y = complex(hard_decision_fn(np.array([zy]))[0])
            # DD gradient: (s_hat - z) * conj(r)
            err_x = s_hat_x - zx
            err_y = s_hat_y - zy
            gx = dd_step_size * err_x
            gy = dd_step_size * err_y
            wxx += gx * np.conj(rx)
            wxy += gx * np.conj(ry)
            wyx += gy * np.conj(rx)
            wyy += gy * np.conj(ry)
            idx = i + half
            zX[idx] = zx
            zY[idx] = zy
            cur_norm = _wnorm()
            if not diverged_2:
                if (cur_norm > norm_thresh or not np.isfinite(cur_norm)
                        or abs(zx) > z_amp_thresh or abs(zy) > z_amp_thresh):
                    diverged_2 = True
                    diverge_idx_2 = idx

    return {
        "zX": zX,
        "zY": zY,
        "diverged": bool(stage1["diverged"] or diverged_2),
        "divergence_symbol": diverge_idx_2 if diverged_2 else stage1["divergence_symbol"],
        "final_w_norm": _wnorm(),
        "init_w_norm": stage1["init_w_norm"],
        "trace": stage1["trace"],  # keep stage-1 trace; stage-2 trace omitted for budget
        "stage_1": {"diverged": bool(stage1["diverged"])},
        "stage_2": {"diverged": diverged_2, "dd_step_size": float(dd_step_size),
                    "dd_iterations": int(dd_iterations)},
        "provenance": {
            "implementation": "b01_candidates.c11_cma_dd_lms_cascade",
            "entry": "stage 1 standard-CMA Godard-with-z + stage 2 DD-LMS (Sato 1975)",
            "stage_1_gradient": "Godard-with-z",
            "stage_2_gradient": "DD-LMS (Sato 1975 Eq.(4))",
            "cma_mu": float(cma_mu),
            "dd_step_size": float(dd_step_size),
            "R2": float(cma_R2),
        },
    }


# =============================================================================
# C08: adaptive-mu contextual bandit (LinUCB) outer-loop selector
# =============================================================================
# Per Li et al. WWW 2010 LinUCB. At each "batch" of `block_size` symbols,
# the bandit observes the running CMA-trace context (output_power, w_norm,
# |z|^2/R^2 ratio), selects a mu from the candidate set, runs CMA for that
# batch with the selected mu, observes the reward (negative mean |z|^2 - R^2
# deviation on the batch), and updates LinUCB.
#
# NOTE: This is an ONLINE bandit, but it does NOT require an action-effect
# hook on the CMA weights. We re-init the CMA weights once (center-tap) and
# then update them per-batch with the bandit-selected mu. The bandit policy
# is the only adaptation; the CMA weight update rule is unchanged.

def c08_adaptive_mu_bandit(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    R2: float = 1.32,
    block_size: int = 64,
    mu_candidates: tuple[float, ...] = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2),
    alpha: float = 1.0,
) -> dict[str, Any]:
    """Adaptive-mu LinUCB contextual bandit driving CMA Godard-with-z.

    Context vector per batch (4 features, standardised online):
      [output_power, w_norm, |z|^2/R^2 ratio, update_norm]
    All features are derived from Causal CMA-trace — no oracle, no TX.
    Reward = -mean( | |z|^2 - R^2 | ) over the batch (dense proxy for PI-SER).

    LinUCB update per Li et al. WWW 2010 Eq.(9)-(11) with k arms (mu_candidates).
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    bs = int(block_size)

    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    init_norm = _wnorm()
    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)

    rX_win = sliding_window_view(rX, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // bs

    mus = np.asarray(mu_candidates, dtype=float)
    K = len(mus)
    # LinUCB per-arm parameters (Li WWW 2010 Eq.(9)): A_k, b_k.
    # Context dim = 4. Regularize with lambda=1.0 (ridge).
    ctx_dim = 4
    A = [np.eye(ctx_dim) for _ in range(K)]
    b = [np.zeros(ctx_dim) for _ in range(K)]
    # Online feature standardisation (running mean/var, Welford).
    feat_mean = np.zeros(ctx_dim)
    feat_var = np.ones(ctx_dim)
    feat_count = 0

    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3
    diverged = False
    diverge_idx = None

    trace: list[dict[str, Any]] = []
    arm_history: list[int] = []

    for blk in range(n_blocks):
        s = blk * bs
        e = s + bs
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]

        # Build context from PREVIOUS batch's trace snapshot.
        # For blk=0 there is no previous; use init (center-tap) features.
        if trace:
            prev = trace[-1]
            ctx_raw = np.array([
                prev["output_power"],
                prev["w_norm"],
                prev["z2_over_R2_ratio"],
                prev["update_norm"],
            ])
        else:
            # Cold-start context: output_power ~ R2, w_norm ~ init, ratio ~ 1.
            ctx_raw = np.array([R2, init_norm, 1.0, 0.0])
        # Welford standardisation.
        feat_count += 1
        delta = ctx_raw - feat_mean
        feat_mean += delta / feat_count
        feat_var += delta * (ctx_raw - feat_mean)
        ctx_std = (ctx_raw - feat_mean) / np.sqrt(np.maximum(feat_var / max(feat_count, 1), 1e-12))
        ctx = ctx_std

        # LinUCB arm selection (Li Eq.(11)): pick argmax theta_k^T ctx + alpha*||ctx||_{A_k^{-1}}.
        best_arm = 0
        best_score = -np.inf
        for k in range(K):
            A_inv = np.linalg.inv(A[k])
            theta_k = A_inv @ b[k]
            ucb = float(theta_k @ ctx) + alpha * float(np.sqrt(ctx @ A_inv @ ctx))
            if ucb > best_score:
                best_score = ucb
                best_arm = k
        mu = float(mus[best_arm])
        arm_history.append(int(best_arm))

        # Run one batch of CMA Godard-with-z with the selected mu.
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy
        idx = s + half
        zX[idx:idx + bs] = zx_blk
        zY[idx:idx + bs] = zy_blk

        eX = R2 - np.abs(zx_blk) ** 2
        eY = R2 - np.abs(zy_blk) ** 2
        gx = mu * eX * zx_blk
        gy = mu * eY * zy_blk
        wxx += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

        # Observe reward (negative mean |R^2 - |z|^2|).
        reward = -float(np.mean(np.abs(R2 - np.abs(zx_blk) ** 2) + np.abs(R2 - np.abs(zy_blk) ** 2)))
        # LinUCB update (Li Eq.(9)-(10)).
        A[best_arm] += np.outer(ctx, ctx)
        b[best_arm] += reward * ctx

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        out_pow = float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2))
        ratio = out_pow / (2.0 * R2) if R2 > 0 else float("nan")
        upd = float(np.sqrt(
            np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
            + np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
            + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
            + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
        ))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + bs),
            "arm": int(best_arm),
            "mu_selected": float(mu),
            "reward": float(reward),
            "output_power": out_pow,
            "z2_over_R2_ratio": ratio,
            "update_norm": upd,
            "w_norm": cur_norm,
            "z_amp_max": cur_zamp,
        })
        if not diverged:
            if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                    or not np.isfinite(cur_norm)):
                diverged = True
                diverge_idx = idx + bs - 1
                break

    return {
        "zX": zX,
        "zY": zY,
        "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(),
        "init_w_norm": init_norm,
        "trace": trace,
        "arm_history": arm_history,
        "mu_candidates": [float(m) for m in mus],
        "provenance": {
            "implementation": "b01_candidates.c08_adaptive_mu_bandit",
            "entry": "LinUCB adaptive mu bandit (Li et al. WWW 2010) over Godard-with-z",
            "cma_gradient": "Godard-with-z",
            "bandit": "LinUCB",
            "alpha": float(alpha),
            "mu_candidates": [float(m) for m in mus],
            "R2": float(R2),
        },
    }


# =============================================================================
# C05: conventional change-point / threshold detector (NON-ML)
# =============================================================================
# Per batch-contract.v1.yaml: takes the CMA-trace (output_power, |z|^2/R^2
# ratio per batch) and emits a binary collapse-imminent alert per batch.
# Two rules combined (for ablation):
#   (a) CUSUM on |z|^2/R^2 ratio with drift parameter `cusum_drift` (Page 1954);
#   (b) threshold on output_power < threshold `z2_ratio_threshold`.
# Either triggers an alert. Tuning grid over both parameters.

def c05_threshold_detector(
    trace: list[dict[str, Any]],
    *,
    z2_ratio_threshold: float = 0.4,
    cusum_drift: float = 0.05,
    cusum_threshold: float = 3.0,
    R2: float = 1.32,
) -> dict[str, Any]:
    """Conventional change-point / threshold detector on CMA-trace.

    `trace` is the per-block snapshot list emitted by the CMA anchor (or C08
    or C10). Each snapshot may carry EITHER `z2_over_R2_ratio` directly OR
    `output_power` (mean |z_x|^2 + |z_y|^2 over the block), from which the
    ratio is derived as output_power / (2*R2). For each block after a
    warmup (first 2 blocks), emit:
      - threshold_alert = 1 if ratio < z2_ratio_threshold
      - cusum_stat = max(0, prev + (baseline - ratio_t) - cusum_drift)
      - cusum_alert = 1 if cusum_stat >= cusum_threshold
      - alert = 1 if threshold_alert OR cusum_alert

    `baseline` = median of ratio over warmup blocks (causal, online-
    estimable from the early "healthy" trajectory). For a healthy 16QAM
    trajectory the ratio is ~1.0; collapse pulls it towards ~0.15 (inner
    ring: |z|^2 ~ 0.2 vs R^2 = 1.32).
    """
    ratios: list[float] = []
    for t in trace:
        if "z2_over_R2_ratio" in t and not np.isnan(t.get("z2_over_R2_ratio", float("nan"))):
            ratios.append(float(t["z2_over_R2_ratio"]))
        elif "output_power" in t and not np.isnan(t.get("output_power", float("nan"))):
            op = float(t["output_power"])
            ratios.append(op / (2.0 * R2) if R2 > 0 else float("nan"))
        else:
            ratios.append(float("nan"))
    ratios_arr = np.array(ratios)
    if len(ratios_arr) == 0 or np.all(np.isnan(ratios_arr)):
        return {"alerts": [], "labels": [], "metrics": {}, "baseline": float("nan"),
                "provenance": {"implementation": "b01_candidates.c05_threshold_detector", "no_data": True}}
    warmup = min(2, len(ratios_arr) - 1)
    warmup_ratios = ratios_arr[:warmup]
    valid_warmup = warmup_ratios[~np.isnan(warmup_ratios)]
    baseline = float(np.median(valid_warmup)) if len(valid_warmup) else 1.0

    cusum_stat = 0.0
    alerts: list[dict[str, Any]] = []
    for i, t in enumerate(trace):
        ratio = ratios_arr[i]
        if np.isnan(ratio):
            alerts.append({
                "block": i,
                "output_start": int(t.get("output_start", 0)),
                "threshold_alert": 0,
                "cusum_alert": 0,
                "alert": 0,
                "z2_ratio": float("nan"),
                "cusum_stat": float(cusum_stat),
            })
            continue
        threshold_alert = 1 if ratio < z2_ratio_threshold else 0
        cusum_stat = max(0.0, cusum_stat + (baseline - ratio) - cusum_drift)
        cusum_alert = 1 if cusum_stat >= cusum_threshold else 0
        alert = 1 if (threshold_alert or cusum_alert) else 0
        alerts.append({
            "block": i,
            "output_start": int(t.get("output_start", 0)),
            "threshold_alert": int(threshold_alert),
            "cusum_alert": int(cusum_alert),
            "alert": int(alert),
            "z2_ratio": float(ratio),
            "cusum_stat": float(cusum_stat),
        })

    return {
        "alerts": alerts,
        "baseline": baseline,
        "provenance": {
            "implementation": "b01_candidates.c05_threshold_detector",
            "entry": "CUSUM (Page 1954) + threshold on output_power/(2*R^2)",
            "cusum_drift": float(cusum_drift),
            "cusum_threshold": float(cusum_threshold),
            "z2_ratio_threshold": float(z2_ratio_threshold),
            "R2": float(R2),
        },
    }


def c05_label_from_oracle(per_seed_oracle_pi_ser: float, *, collapse_threshold: float = 0.3) -> int:
    """DERIVED_HERE: collapse label = 1 if oracle PI-SER > collapse_threshold.

    Used as the supervised label for detector AUROC evaluation. Per FR-14,
    oracle-derived labels are allowed for evaluation; the oracle is NOT a
    runtime input to the detector.
    """
    return 1 if float(per_seed_oracle_pi_ser) > float(collapse_threshold) else 0


__all__ = [
    "c10_per_symbol_cma",
    "c11_cma_dd_lms_cascade",
    "c08_adaptive_mu_bandit",
    "c05_threshold_detector",
    "c05_label_from_oracle",
]
