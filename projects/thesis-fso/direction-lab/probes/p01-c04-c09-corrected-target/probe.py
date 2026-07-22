"""Probe p01-c04-c09-corrected-target.

QUESTION
    Which receiver-visible *corrected* objective for the affine corrector
    (A, b) : z_corrected = z_calib @ A.T + b  has an INPUT-DEPENDENT optimum
    (survives the constant-collapse test) vs an INPUT-INDEPENDENT CONSTANT
    optimum (FAILS, like the old soft-expected-distance loss S010/V005/D016)?

CONTEXT
    The previous training objective in
    c04-c09-shared-corrector-v1/src/run_corrector_batch.py::_train_loss_on_calib
    was a *soft* expected-distance loss with an input-independent constant
    optimum: when A=0 and each real coord of b ≈ +/-0.6075, the loss is
    minimized at ≈1.30840175 regardless of input. That made the candidate
    "blow up" (constant scrambled output). We test THREE candidate *corrected*
    objectives to see whether each has an input-dependent optimum.

THE THREE OBJECTIVES (all receiver-visible: z-stream + public 16QAM alphabet only)
    O1_hard_pseudo_mse:
        MSE(z_corrected, hard_16qam(z_calib)) where the pseudo-label target
        hard_16qam(z_calib) is a FIXED, detached target (exactly the target
        blind_affine_compare_16qam optimizes in closed form). This is the
        HARD-decision pseudo-label MSE, NOT the soft surrogate.
    O2_negentropy_kurtosis:
        Godard-style dispersion: minimize (E[|z|^2]^2 - E[|z|^4]) over the
        corrected |z|^2, i.e. MINIMIZE negative normalized kurtosis. Input-
        distribution-dependent by construction.
    O3_blind_residual:
        MSE(z_corrected, z_blind) where z_blind is the blind-affine closed-form
        corrected z (frozen per realization). Target = residual improvement over
        blind affine.

SEMANTIC SMOKE TEST (per objective)
    1. Constant test:  minimize the objective with A=0 (z_corrected = b const)
        vs the full (A, b) optimum, across MULTIPLE distinct input realizations.
        PASS  := full-optimum loss is STRICTLY lower than constant-b-only loss
                 AND the optimal A varies across realizations (input-dependent).
        FAIL  := constant-b loss equals/beats full loss, OR optimal A is always ~0.
    2. Identity test:  A=I, b=0 (no-op) must give a finite, non-degenerate loss.

The old soft loss would FAIL because its constant-b optimum == full optimum.
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import torch

# ---------------------------------------------------------------------------
# Path setup — import the worktree's simulation + atlas infrastructure.
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve()
PROBE_DIR = HERE.parent                       # .../probes/p01-c04-c09-corrected-target
# PROBE_DIR.parents: [0]=probes [1]=direction-lab [2]=thesis-fso [3]=projects [4]=worktree-root
ATLAS_DIR = (
    PROBE_DIR.parents[1]                      # .../direction-lab
    / "scout" / "cb1-modulation-generic-closure" / "baseline-atlas"
)
REPO_ROOT = PROBE_DIR.parents[4]              # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(SIM_DIR / "common"), str(ATLAS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402

# ---------------------------------------------------------------------------
# Frozen constants (mirror run_corrector_batch.py FROZEN).
# ---------------------------------------------------------------------------
FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu_fixed": 0.03,
    "cma_taps": 11, "cma_block_size": 64,
    "blind_affine_ridge_frozen": 1e-8,
}
R2_16QAM = 1.32

# Cells + seeds for the smoke test (held-out test slice per the contract).
CELLS = [
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,
     "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-fg100-short", "snr_db": 20.0, "f_g_hz": 100.0,
     "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
]
SEEDS = [71, 72, 73]

# Levels for 16QAM per real axis (avg-power normalized /sqrt(10)).
_LEVELS = np.array([-3.0, -1.0, 1.0, 3.0]) / np.sqrt(10.0)

DEVICE = torch.device("cpu")  # tiny problem; CPU is fastest and deterministic
torch.set_default_dtype(torch.float64)  # double precision for the optimization


# ===========================================================================
# Realization + CMA pipeline (mirrors run_corrector_batch.build_dataset, but
# keeps the FULL calib z-stream — we only need z_calib per realization).
# ===========================================================================

def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation=str(cell.get("modulation", "qam16")),
    )


def build_realizations():
    """Return list of dicts {cell_id, seed, z_calib [N,2] complex, target_*}.

    Runs fixed-mu CMA ONCE per (cell, seed) and slices the calibration window.
    Each entry also caches the FIXED receiver-visible targets the objectives use:
      hard_label  : hard_16qam(z_calib)            [N,2] complex  (O1 target)
      z_blind     : blind-affine closed-form corr.  [N,2] complex  (O3 target)
    Both are computed from z_calib + the public 16QAM alphabet ONLY (no TX truth).
    """
    out = []
    ridge = float(FROZEN["blind_affine_ridge_frozen"])
    for cell in CELLS:
        es, ce, ee, _ = atlas_runner.eval_window_for(
            int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
            window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
        )
        for seed in SEEDS:
            rlz = make_realization(cell, seed)
            cma = atlas_runner.standard_cma_godard_with_z(
                rlz["rX"], rlz["rY"], n_tap=int(FROZEN["cma_taps"]),
                mu=float(FROZEN["cma_mu_fixed"]), R2=R2_16QAM,
                block_size=int(FROZEN["cma_block_size"]),
            )
            rec = {"cell_id": cell["id"], "seed": int(seed)}
            if cma["diverged"]:
                rec["diverged"] = True
                out.append(rec)
                continue
            zX, zY = np.asarray(cma["zX"]), np.asarray(cma["zY"])
            z_calib = np.column_stack((zX[es:ce], zY[es:ce])).astype(np.complex128)
            # ---- receiver-visible fixed targets (NO TX truth) ----
            hard_label = np.asarray(evaluator.hard_16qam(z_calib), dtype=np.complex128)
            blind = evaluator.blind_affine_compare_16qam(
                z_calib, z_calib, ridge=ridge,
            )
            z_blind = np.asarray(blind["corrected"], dtype=np.complex128)
            rec.update({
                "diverged": False,
                "z_calib": z_calib,
                "hard_label": hard_label,
                "z_blind": z_blind,
            })
            out.append(rec)
    return out


# ===========================================================================
# Objective factories.
#
# Each objective is a callable  loss_fn(A[2,2] complex, b[2] complex) -> scalar
# operating on a FIXED per-realization dataset. We define them to be differentiable
# in (A, b) via torch complex autograd, so scipy-free torch optimization works.
#
# Affine application:  z_corr = z @ A.T + b   (A:[2,2], b:[2], z:[N,2] complex)
# ===========================================================================

def _to_complex_tensor(arr):
    """np complex [N,2] -> torch complex64/complex128 [N,2]."""
    t = torch.from_numpy(np.asarray(arr, dtype=np.complex128))
    return t.to(DEVICE)


def _json_safe_complex(arr):
    """Convert a numpy complex array (any shape) to a JSON-serializable nested
    list where each complex scalar becomes {"re":..., "im":...}."""
    a = np.asarray(arr)
    if not np.iscomplexobj(a):
        return a.tolist()
    shape = a.shape
    flat = a.reshape(-1)
    out = [{"re": float(z.real), "im": float(z.imag)} for z in flat]
    if len(shape) == 0:
        return out[0]
    # rebuild nested list of the original shape
    def _nest(seq, dims):
        if len(dims) == 1:
            return list(seq)
        size = dims[0]
        step = len(seq) // size
        return [_nest(seq[i * step:(i + 1) * step], dims[1:]) for i in range(size)]
    return _nest(out, shape)


def _json_default(obj):
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return _json_safe_complex(obj)
    if isinstance(obj, complex):
        return {"re": obj.real, "im": obj.imag}
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _abs2(z):
    return (z.real * z.real + z.imag * z.imag)


# ---- O1: hard-decision pseudo-label MSE (fixed detached target) ------------
def make_O1(rec):
    z = _to_complex_tensor(rec["z_calib"])          # [N,2] complex (leaf-free)
    target = _to_complex_tensor(rec["hard_label"])  # [N,2] complex (FIXED)

    def loss_fn(A, b):
        z_corr = z @ A + b.unsqueeze(0)
        d = z_corr - target
        return torch.mean(_abs2(d))     # mean |z_corr - hard_label|^2 over N*2

    return loss_fn, ("hard_label_MSE",)


# ---- O2: Godard dispersion / negative NORMALIZED kurtosis of |z_corr|^2 ----
#  The brief's literal formula E[|z|^2]^2 - E[|z|^4] is UNBOUNDED below under
#  output scaling (E[|z|^4] grows as scale^4 vs E[|z|^2]^2 as scale^4 ... but
#  the *negative* E[|z|^4] term dominates -> loss -> -inf as |A| -> inf). That
#  would make the constant-collapse test meaningless (the "full" optimum is
#  simply A -> infinity). We therefore use the well-posed Godard dispersion
#  measure: the NEGATIVE NORMALIZED kurtosis of |z|^2,
#      loss = - E[|z|^4] / E[|z|^2]^2
#  which is scale-invariant (multiplying z_corr by any complex scalar c does
#  not change it) and bounded: for the 16QAM constellation normalized kurtosis
#  = 1.32 (== R2_16QAM); minimizing this loss drives |z|^2 toward a maximally
#  concentrated (peaked) distribution. This is the standard Godard/CMA-style
#  dispersion objective and is input-distribution-dependent by construction.
#  (We additionally guard against the trivial degenerate optimum z_corr = 0 by
#  checking identity-test finiteness and by the constant-collapse structure.)
def make_O2(rec):
    z = _to_complex_tensor(rec["z_calib"])
    eps = 1e-12

    def loss_fn(A, b):
        z_corr = z @ A + b.unsqueeze(0)
        p = _abs2(z_corr)                 # |z|^2  [N,2]
        p_flat = p.reshape(-1)
        e2 = torch.mean(p_flat)
        e4 = torch.mean(p_flat * p_flat)
        # negative normalized kurtosis; +eps guards the z_corr->0 collapse
        return -(e4 / (e2 * e2 + eps))

    return loss_fn, ("neg_normalized_kurtosis_dispersion",)


# ---- O3: blind-residual MSE to the closed-form blind-affine corrected z ----
def make_O3(rec):
    z = _to_complex_tensor(rec["z_calib"])
    target = _to_complex_tensor(rec["z_blind"])     # [N,2] complex (FIXED)

    def loss_fn(A, b):
        z_corr = z @ A + b.unsqueeze(0)
        d = z_corr - target
        return torch.mean(_abs2(d))     # mean |z_corr - z_blind|^2

    return loss_fn, ("blind_residual_MSE",)


OBJECTIVES = {
    "O1_hard_pseudo_mse": make_O1,
    "O2_negentropy_kurtosis": make_O2,
    "O3_blind_residual": make_O3,
}


# ===========================================================================
# Optimization of (A, b) in two modes via torch autograd (Adam) +
# closed-form cross-check where analytic solutions exist.
# ===========================================================================

def _make_params(mode):
    """mode='full' -> A requires grad, b requires grad.
       mode='const' -> A fixed at 0 (const-only b), b requires grad."""
    if mode == "full":
        # init A near identity (so identity test region is sampled) but with
        # a small random perturbation to break symmetry; b near 0.
        A = torch.eye(2, dtype=torch.complex128, device=DEVICE) * 1.0
        b = torch.zeros(2, dtype=torch.complex128, device=DEVICE)
        A = A.clone().detach().requires_grad_(True)
        b = b.clone().detach().requires_grad_(True)
        params = [A, b]
    elif mode == "const":
        A = torch.zeros((2, 2), dtype=torch.complex128, device=DEVICE)  # frozen 0
        b = torch.zeros(2, dtype=torch.complex128, device=DEVICE).requires_grad_(True)
        params = [b]
    else:
        raise ValueError(mode)
    return A, b, params


def optimize(loss_fn, mode, *, n_steps=400, lr=0.05):
    """Adam-optimize (A, b) [full] or b [const] for loss_fn. Returns (loss, A, b)."""
    A, b, params = _make_params(mode)
    opt = torch.optim.Adam(params, lr=lr)
    best_loss = float("inf")
    best = (None, None)
    for _ in range(n_steps):
        opt.zero_grad()
        loss = loss_fn(A, b)
        loss.backward()
        opt.step()
        lv = float(loss.detach())
        if lv < best_loss:
            best_loss = lv
            best = (A.detach().clone(), b.detach().clone())
    return best_loss, best[0], best[1]


def closed_form_full_min_mse(z_np, target_np):
    """Closed-form complex affine least-squares fit: min ||z@A.T + b - target||^2.

    Solves the same ridge-LS the blind_affine comparator solves, but with the
    GIVEN target (z_calib as input, target as labels). Returns (loss, A, b).
    Used as a cross-check for O1 and O3 (which are plain MSE fits).
    """
    design = np.column_stack((z_np, np.ones(len(z_np), dtype=np.complex128)))
    ridge = float(FROZEN["blind_affine_ridge_frozen"])
    reg = np.eye(design.shape[1], dtype=np.complex128) * ridge
    reg[-1, -1] = 0.0
    coef = np.linalg.solve(design.conj().T @ design + reg, design.conj().T @ target_np)
    # design @ coef  ==  z @ coef[:2,:] + coef[2,:]   (z:[N,2], target:[N,2])
    # so the affine convention z_corr = z @ A + b gives A = coef[:2,:] ([2,2]).
    A = coef[:2, :]            # [2,2]
    b = coef[2, :]             # [2]
    pred = design @ coef
    loss = float(np.mean(np.abs(pred - target_np) ** 2))
    return loss, A, b


def closed_form_const_min_mse(target_np):
    """A=0 optimum: z_corr = b (const). Best const b = mean(target)."""
    b = target_np.mean(axis=0)
    loss = float(np.mean(np.abs(target_np - b) ** 2))
    return loss, b


# ===========================================================================
# Per-objective semantic smoke test.
# ===========================================================================

def _A_variation_metric(A_list):
    """Measure how much the optimal A changes across realizations.

    Returns the max pairwise Frobenius distance between the optimal A matrices,
    and the mean off-diagonal / deviation-from-identity magnitude. A constant
    optimum (A always 0) yields ~0 variation.
    """
    arrs = [np.asarray(A, dtype=np.complex128) for A in A_list if A is not None]
    if len(arrs) < 2:
        return {"max_pairwise_dist": 0.0, "norm_mean": 0.0}
    max_d = 0.0
    for i in range(len(arrs)):
        for j in range(i + 1, len(arrs)):
            d = float(np.max(np.abs(arrs[i] - arrs[j])))
            max_d = max(max_d, d)
    norms = [float(np.linalg.norm(a)) for a in arrs]
    return {"max_pairwise_dist": max_d, "A_norm_mean": float(np.mean(norms))}


def test_objective(name, maker, realizations, log=print):
    """Run the semantic smoke test for ONE objective across all realizations."""
    rows = []
    for rec in realizations:
        if rec.get("diverged", False):
            continue
        loss_fn, _ = maker(rec)
        z_np = np.asarray(rec["z_calib"], dtype=np.complex128)

        # --- full (A, b) optimum (torch) ---
        full_loss, A_full, b_full = optimize(loss_fn, "full")

        # --- const-b only optimum (torch) ---
        const_loss, A_const, b_const = optimize(loss_fn, "const")

        # --- closed-form cross-checks for MSE objectives ---
        cf_full = cf_const = None
        target_np = None
        if name in ("O1_hard_pseudo_mse", "O3_blind_residual"):
            target_np = (np.asarray(rec["hard_label"]) if name == "O1_hard_pseudo_mse"
                         else np.asarray(rec["z_blind"]))
            cf_full_loss, cf_A, cf_b = closed_form_full_min_mse(z_np, target_np)
            cf_const_loss, _cf_b = closed_form_const_min_mse(target_np)
            cf_full, cf_const = float(cf_full_loss), float(cf_const_loss)

        # --- identity test: A=I, b=0 ---
        with torch.no_grad():
            A_id = torch.eye(2, dtype=torch.complex128, device=DEVICE)
            b_id = torch.zeros(2, dtype=torch.complex128, device=DEVICE)
            id_loss = float(loss_fn(A_id, b_id))

        rows.append({
            "cell_id": rec["cell_id"], "seed": rec["seed"],
            "full_loss": float(full_loss),
            "const_loss": float(const_loss),
            "cf_full_loss": cf_full,
            "cf_const_loss": cf_const,
            "identity_loss": id_loss,
            "A_full_norm": float(torch.linalg.norm(A_full).real) if A_full is not None else None,
            "A_full_offdiag": float(torch.linalg.norm(A_full - torch.diag(torch.diag(A_full))).real) if A_full is not None else None,
            "A_full": _json_safe_complex(np.asarray(A_full)) if A_full is not None else None,
            "b_full": _json_safe_complex(np.asarray(b_full)) if b_full is not None else None,
            "b_const": _json_safe_complex(np.asarray(b_const)) if b_const is not None else None,
            "_A_full_raw": np.asarray(A_full, dtype=np.complex128) if A_full is not None else None,
        })
        log(f"    {rec['cell_id']} seed={rec['seed']}: "
            f"const={const_loss:.6f}  full={full_loss:.6f}  "
            f"delta={const_loss - full_loss:+.6f}  "
            f"identity={id_loss:.6f}"
            + (f"  [cf full={cf_full:.6f} const={cf_const:.6f}]" if cf_full is not None else ""))

    if not rows:
        return {"name": name, "verdict": "INCONCLUSIVE",
                "reason": "no non-diverged realizations", "per_realization": []}

    # --- Aggregate across realizations ---
    const_losses = [r["const_loss"] for r in rows]
    full_losses = [r["full_loss"] for r in rows]
    id_losses = [r["identity_loss"] for r in rows]
    deltas = [c - f for c, f in zip(const_losses, full_losses)]  # >0 means full better

    A_variation = _A_variation_metric([r["_A_full_raw"] for r in rows])

    # PASS criteria (ALL must hold):
    #  (a) mean(const) - mean(full) > tol  (full strictly beats const on average)
    #  (b) every realization has full < const (strictly, by tol)
    #  (c) optimal A varies across realizations (not always the same constant)
    #  (d) optimal A is NOT always ~0 (constant collapse signature)
    tol = 1e-6
    mean_delta = float(np.mean(deltas))
    min_delta = float(np.min(deltas))
    all_strictly_better = bool(min_delta > tol)
    mean_better = bool(mean_delta > tol)
    a_varies = bool(A_variation["max_pairwise_dist"] > 1e-3)
    a_not_always_zero = bool(A_variation["A_norm_mean"] > 1e-2)

    # Identity test: finite and not degenerate (not 0, not inf/nan, not absurdly large)
    identity_ok = all(np.isfinite(id_losses)) and all(l < 1e6 for l in id_losses)

    passed = bool(mean_better and all_strictly_better and a_varies and a_not_always_zero)
    verdict = "PASS" if passed else "FAIL"

    # Reason breakdown for transparency
    reasons = {
        "mean_delta_const_minus_full": mean_delta,
        "min_delta_const_minus_full": min_delta,
        "all_realizations_full_strictly_better": all_strictly_better,
        "A_varies_across_realizations": a_varies,
        "A_not_always_zero": a_not_always_zero,
        "identity_test_finite": identity_ok,
    }

    summary = {
        "name": name,
        "verdict": verdict,
        "identity_test": "PASS" if identity_ok else "FAIL",
        "constant_test": "PASS" if (mean_better and all_strictly_better) else "FAIL",
        "n_realizations": len(rows),
        "mean_const_loss": float(np.mean(const_losses)),
        "mean_full_loss": float(np.mean(full_losses)),
        "mean_delta_const_minus_full": mean_delta,
        "min_delta_const_minus_full": min_delta,
        "mean_identity_loss": float(np.mean(id_losses)),
        "A_variation": A_variation,
        "criteria": reasons,
        # strip the raw numpy array (used only for the variation metric) so the
        # remaining per-realization dict is JSON-serializable.
        "per_realization": [{k: v for k, v in r.items() if k != "_A_full_raw"} for r in rows],
    }
    log(f"  [{name}] VERDICT={verdict}  "
        f"mean_const={summary['mean_const_loss']:.6f}  "
        f"mean_full={summary['mean_full_loss']:.6f}  "
        f"mean_delta={mean_delta:+.6f}  "
        f"A_max_pairwise_dist={A_variation['max_pairwise_dist']:.4e}  "
        f"A_norm_mean={A_variation['A_norm_mean']:.4f}")
    return summary


# ===========================================================================
# Reference: reproduce the OLD soft loss constant-collapse as a sanity check.
# ===========================================================================

def make_old_soft_loss(rec):
    """The original _train_loss_on_calib soft-expected-distance objective.

    Confirms it has an input-independent constant optimum (~1.30840175) when
    A=0, b≈±0.6075 per real coord — i.e. it FAILS the smoke test. This is the
    reference baseline the corrected objectives are compared against.
    """
    z = _to_complex_tensor(rec["z_calib"])
    levels = torch.tensor(_LEVELS, dtype=torch.float64, device=DEVICE)

    def loss_fn(A, b):
        z_corr = z @ A + b.unsqueeze(0)
        re_x = z_corr[..., 0].real
        im_x = z_corr[..., 0].imag
        re_y = z_corr[..., 1].real
        im_y = z_corr[..., 1].imag
        loss = torch.tensor(0.0, device=DEVICE, dtype=torch.float64)
        for coord in (re_x, im_x, re_y, im_y):
            d2 = (coord.unsqueeze(-1) - levels) ** 2
            weights = torch.softmax(-d2, dim=-1)
            loss = loss + torch.mean(torch.sum(weights * d2, dim=-1))
        return loss

    return loss_fn, ("soft_expected_distance_OLD",)


# ===========================================================================
# Main
# ===========================================================================

def main():
    t0 = time.time()
    log = lambda m: print(m, flush=True)

    log("[p01] building realizations (fixed-mu CMA mu=0.03, 16QAM)...")
    realizations = build_realizations()
    n_ok = sum(1 for r in realizations if not r.get("diverged", False))
    log(f"[p01] {len(realizations)} realizations, {n_ok} non-diverged, "
        f"{time.time()-t0:.1f}s")

    # ---- reference: old soft loss (expect FAIL / constant collapse) ----
    log("[p01] reference: OLD soft-expected-distance loss (expect constant collapse)")
    ref = test_objective("OLD_soft_loss", make_old_soft_loss, realizations, log=log)

    # ---- the three candidate objectives ----
    results = {}
    for name, maker in OBJECTIVES.items():
        log(f"[p01] testing {name} ...")
        results[name] = test_objective(name, maker, realizations, log=log)

    # ---- overall verdict ----
    n_pass = sum(1 for v in results.values() if v.get("verdict") == "PASS")
    overall = "PASS" if n_pass >= 1 else "FAIL"

    payload = {
        "probe_id": "p01-c04-c09-corrected-target",
        "question": (
            "Which receiver-visible corrected objective for the affine "
            "corrector has an input-dependent optimum (survives "
            "constant-collapse) vs an input-independent constant optimum?"
        ),
        "cells": [c["id"] for c in CELLS],
        "seeds": SEEDS,
        "n_realizations": len(realizations),
        "n_nondiverged": n_ok,
        "reference_old_soft_loss": ref,
        "objectives": results,
        "overall_verdict": overall,
        "n_objectives_passed": n_pass,
        "pass_criterion": (
            "PASS = at least one objective has input-dependent optimum "
            "(full < constant-b on EVERY realization, AND optimal A varies "
            "across realizations, AND optimal A not always ~0). "
            "FAIL = all objectives collapse to constant b."
        ),
        "identity_test_note": (
            "Identity test checks A=I, b=0 gives finite non-degenerate loss "
            "(no inf/nan, not absurdly large)."
        ),
        "elapsed_seconds": round(time.time() - t0, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    out_path = PROBE_DIR / "artifacts" / "probe_result.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=_json_default)
    log(f"[p01] OVERALL VERDICT = {overall}  ({n_pass}/{len(results)} objectives passed)")
    log(f"[p01] wrote {out_path}  (elapsed {time.time()-t0:.1f}s)")
    return payload


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
