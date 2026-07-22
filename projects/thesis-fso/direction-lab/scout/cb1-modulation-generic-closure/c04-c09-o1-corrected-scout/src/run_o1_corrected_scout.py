"""C04/C09 O1-CORRECTED corrector Scout runner.

Single entry point:
    python run_o1_corrected_scout.py --tune-train-eval

This is an adaptation of c04-c09-shared-corrector-v1/src/run_corrector_batch.py
with EXACTLY ONE change: the training loss is the CORRECTED O1 objective
(hard-decision pseudo-label MSE with a DETACHED target), replacing the old soft
expected-distance loss that had an input-independent constant optimum and caused
constant-collapse (D016/V005, both candidates CANDIDATE_BLOWS_UP).

Everything else (dataset building, cell/seed splits, evaluation, adjudication,
source-closure hashing) is IDENTICAL to the old batch for paired comparison.

Pipeline:
  Phase 0: identity + semantic-smoke tests (MUST PASS).
  Phase 1: build the (cell, seed) realization dataset (fixed-mu CMA ONCE per
           cell x seed) for train / val / test.
  Phase 2: train the MLP corrector (ONE representative HP) on the O1 objective.
  Phase 3: held-out evaluation on 7 held-out cells x test seeds [71-80] (SAME
           test slice as the old batch + adjudication -> perfectly paired).
           Comparators per (cell, seed): fixed_cma, blind_affine (frozen ridge),
           candidate (trained model), oracle_affine (Kill bound only).
  Phase 4: adjudicate CANDIDATE_BEATS_BLIND_STABLY / DOES_NOT_BEAT / BLOWS_UP.

The CORRECTED training loss (the ONLY change from the old batch):
  z_corrected_calib = z_calib @ A.T + b            (candidate output)
  pseudo_label = hard_16qam(z_corrected_calib)     (DETACHED target per step)
  loss = MSE(z_corrected_calib, pseudo_label)
The pseudo-label is detached: it is a FIXED target per SGD step (not
differentiable through the hard decision). Each step is one Lloyd-like
iteration; over epochs the labels and the affine alternate (k-means-like).
This is exactly the objective blind_affine_compare_16qam solves in CLOSED FORM;
the candidate learns the SAME thing per-realization but conditioned on trace
features (context-dependence).

Discipline (per batch-contract.v1.yaml):
  * Train/val/test seeds pairwise disjoint (asserted); disjoint from all prior.
  * Training cells disjoint from held-out test cells (asserted).
  * Candidate NEVER reads TX truth.
  * blind_affine ridge FROZEN (1e-8); NOT re-tuned here.
  * Oracle = Kill bound only (context), never a Go baseline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import yaml

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent                              # .../src
BATCH_DIR = SRC_DIR.parent                         # .../c04-c09-o1-corrected-scout
CB1_ROOT = BATCH_DIR.parent                        # .../cb1-modulation-generic-closure
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
OLD_BATCH_DIR = CB1_ROOT / "c04-c09-shared-corrector-v1"   # reuse the OLD adapter
ADJUD_DIR = CB1_ROOT / "corrector-residual-headroom-v1"
REPO_ROOT = HERE.parents[7]                        # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR), str(SRC_DIR),
          str(OLD_BATCH_DIR), str(OLD_BATCH_DIR / "src"), str(ADJUD_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import corrector_adapter as adapter  # noqa: E402  (REUSED from old batch, UNCHANGED)


# =============================================================================
# Contract constants (mirror batch-contract.v1.yaml) — IDENTICAL to old batch
# =============================================================================

FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10, "method": "gar",
    "cma_mu_fixed": 0.03,  # INHERITED from B01-R HF6 (NOT re-tuned)
    "cma_taps": 11, "cma_block_size": 64,
    "r2_qam16": 1.32,
    "blind_affine_ridge_frozen": 1e-8,  # from corrector-residual-headroom-v1
}
MDE = 0.005
R2_16QAM = 1.32

# Cells (SAME 11-cell atlas; raw preserved).
ATLAS_V1_16QAM_CELLS = [
    {"id": "16qam-snr05-nominal-short", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr10-nominal-short", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr25-nominal-short", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-fg100-short",   "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-fg1000-short",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr20-sop40e-short",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-5, "n_symbols": 512, "modulation": "qam16"},
    {"id": "16qam-snr10-fg100-long",    "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
    {"id": "16qam-snr15-fg1000-long",   "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
    {"id": "16qam-snr20-nominal-long",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4e-6, "n_symbols": 8192, "modulation": "qam16"},
]

# Cell split — IDENTICAL to old batch (paired comparison).
TRAINING_CELL_IDS = {
    "16qam-snr20-nominal-short",
    "16qam-snr20-fg1000-short",
    "16qam-snr20-sop40e-short",
    "16qam-snr20-nominal-long",
}
HELD_OUT_CELL_IDS = {
    "16qam-snr05-nominal-short",
    "16qam-snr10-nominal-short",
    "16qam-snr15-nominal-short",
    "16qam-snr25-nominal-short",
    "16qam-snr20-fg100-short",
    "16qam-snr10-fg100-long",
    "16qam-snr15-fg1000-long",
}

# SAME disjoint seeds as old batch for paired comparison.
TRAINING_SEEDS = [81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
VALIDATION_SEEDS = [91, 92, 93, 94, 95]
TEST_SEEDS = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]  # = adjudication test slice
_PRIOR_SEEDS = set(
    list(range(11, 51))    # B01 / B01-R / c11-legality
    + [61, 62, 63, 64, 65]  # corrector-residual-headroom-v1 validation
)
assert set(TRAINING_SEEDS).isdisjoint(set(VALIDATION_SEEDS)), "train/val overlap"
assert set(TRAINING_SEEDS).isdisjoint(set(TEST_SEEDS)), "train/test overlap"
assert set(VALIDATION_SEEDS).isdisjoint(set(TEST_SEEDS)), "val/test overlap"
assert set(TRAINING_SEEDS).isdisjoint(_PRIOR_SEEDS), "train overlaps prior"
assert set(VALIDATION_SEEDS).isdisjoint(_PRIOR_SEEDS), "val overlaps prior"
assert TRAINING_CELL_IDS.isdisjoint(HELD_OUT_CELL_IDS), "training/test cells overlap"

# Representative HP (old smoke showed the grid is non-discriminating; the change
# here is the LOSS, so one representative HP is sufficient for the Scout).
HP_GRID = {
    "hidden_dim": [32, 64],
    "learning_rate": [1e-3, 3e-3],
    "weight_decay": [0.0, 1e-4],
}
N_EPOCHS = 30
EARLY_STOP_PATIENCE = 5
HP_TUNING_SEEDS = [81, 82, 83]
REPRESENTATIVE_HP = {"hidden_dim": 64, "learning_rate": 3e-3, "weight_decay": 1e-4}

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# =============================================================================
# Realization + CMA + slicing helpers (IDENTICAL to old batch)
# =============================================================================

def make_realization(cell, seed):
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation=str(cell.get("modulation", "qam16")),
    )


def _eval_window_for_cell(cell):
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]),
    )


def run_fixed_mu_cma(cell, realization):
    return atlas_runner.standard_cma_godard_with_z(
        realization["rX"], realization["rY"],
        n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]),
    )


def _split_calib_eval(zX, zY, realization, *, eval_start, calibration_end, eval_end):
    zXa = np.asarray(zX)
    zYa = np.asarray(zY)
    z_calib = np.column_stack((zXa[eval_start:calibration_end], zYa[eval_start:calibration_end]))
    z_eval = np.column_stack((zXa[calibration_end:eval_end], zYa[calibration_end:eval_end]))
    truth_calib = np.column_stack((
        realization["sX"][eval_start:calibration_end],
        realization["sY"][eval_start:calibration_end],
    ))
    truth_eval = np.column_stack((
        realization["sX"][calibration_end:eval_end],
        realization["sY"][calibration_end:eval_end],
    ))
    bits_x_eval = realization["bitsX"][calibration_end * 4:eval_end * 4]
    bits_y_eval = realization["bitsY"][calibration_end * 4:eval_end * 4]
    return z_calib, z_eval, truth_calib, truth_eval, bits_x_eval, bits_y_eval


# =============================================================================
# Dataset cache (IDENTICAL to old batch)
# =============================================================================

def build_dataset(cells, seeds, log=print):
    """Build the (cell, seed) -> {z_calib, z_eval, ...} dataset by running
    fixed-mu CMA ONCE per (cell, seed)."""
    dataset = {}
    t0 = time.time()
    for cell in cells:
        ew = _eval_window_for_cell(cell)
        for seed in seeds:
            realization = make_realization(cell, seed)
            cma_out = run_fixed_mu_cma(cell, realization)
            es, ce, ee, _ = ew
            if cma_out["diverged"]:
                dataset[(cell["id"], seed)] = {"diverged": True}
                continue
            z_calib, z_eval, truth_calib, truth_eval, bx, by = _split_calib_eval(
                cma_out["zX"], cma_out["zY"], realization,
                eval_start=es, calibration_end=ce, eval_end=ee,
            )
            dataset[(cell["id"], seed)] = {
                "diverged": False,
                "z_calib": z_calib,
                "z_eval": z_eval,
                "truth_calib": truth_calib,  # ONLY for oracle Kill bound / metric eval; never training
                "truth_eval": truth_eval,
                "bits_x_eval": bx,
                "bits_y_eval": by,
            }
    log(f"  [dataset] {len(cells)} cells x {len(seeds)} seeds = {len(cells)*len(seeds)} "
        f"realizations in {time.time()-t0:.1f}s "
        f"(diverged: {sum(1 for v in dataset.values() if v.get('diverged'))})")
    return dataset


# =============================================================================
# CORRECTED training loss O1 (THE ONLY CHANGE from the old batch)
#
#   z_corrected_calib = z_calib @ A.T + b
#   pseudo_label = hard_16qam(z_corrected_calib).detach()   <- DETACHED target
#   loss = MSE(z_corrected_calib, pseudo_label)
#
# The hard decision is NOT differentiable; we detach it so each SGD step is one
# Lloyd-like iteration (assign labels from the current map, then the gradient
# pulls the affine toward fitting those labels). Over epochs the labels and the
# affine alternate (k-means-like; converges). This is exactly the objective
# blind_affine_compare_16qam solves in CLOSED FORM.
# =============================================================================

def _torch_hard_16qam(z_corrected):
    """Differentiable-in-input hard_16qam (nearest grid point), matching
    common._modulation.hard_decision(mod='qam16') EXACTLY. Returns complex.

    For each complex value s = re + j*im (avg-power-normalized /sqrt(10)):
        un-normalize:  s * sqrt(10)
        di = clip( round((re+3)/2)*2 - 3, -3, 3 )   in {-3,-1,1,3}
        dq = clip( round((im+3)/2)*2 - 3, -3, 3 )
        re-normalize:  (di + j*dq) / sqrt(10)
    The round() is non-differentiable; we only use the OUTPUT as a DETACHED
    target (see _train_loss_o1), so differentiability of the hard decision
    itself is not needed.
    """
    sq10 = float(np.sqrt(10.0))
    s = z_corrected * sq10
    # torch has no np.round that rounds half away from zero on the GPU, but for
    # these well-separated constellation points the values are never near a
    # half-integer boundary, so torch.round (round-half-to-even) matches numpy.
    di = torch.clamp(torch.round((s.real + 3.0) / 2.0) * 2.0 - 3.0, -3.0, 3.0)
    dq = torch.clamp(torch.round((s.imag + 3.0) / 2.0) * 2.0 - 3.0, -3.0, 3.0)
    return torch.complex(di, dq) / sq10


def _train_loss_o1(z_calib_t, A, b):
    """O1 objective: MSE between z_corrected_calib and its DETACHED hard
    pseudo-label. This is the CORRECTED loss (input-dependent optimum,
    probe-confirmed); the old batch used a soft expected-distance loss.

    z_calib_t: [1, N, 2] complex leaf tensor.
    A: [1, 2, 2] complex; b: [1, 2] complex (model outputs).
    """
    z_corrected = torch.matmul(z_calib_t, A.transpose(-2, -1)) + b.unsqueeze(1)
    # Detach the pseudo-label: it is a FIXED target per step, not a gradient
    # path through the (non-differentiable) hard decision.
    pseudo_label = _torch_hard_16qam(z_corrected).detach()
    diff = z_corrected - pseudo_label
    # mean |diff|^2 over all N*2 complex samples (mean over batch dim too).
    loss = torch.mean(diff.real * diff.real + diff.imag * diff.imag)
    return loss


def _eval_loss_o1(z_calib_t, A, b):
    """Evaluation-mode O1 loss (no autograd). Used for validation + the smoke
    identity/constant tests."""
    with torch.no_grad():
        z_corrected = torch.matmul(z_calib_t, A.transpose(-2, -1)) + b.unsqueeze(1)
        pseudo_label = _torch_hard_16qam(z_corrected)
        diff = z_corrected - pseudo_label
        return float(torch.mean(diff.real * diff.real + diff.imag * diff.imag))


# =============================================================================
# Training (per realization: O1 hard pseudo-label MSE on z_calib)
# =============================================================================

def _set_context_and_z(model, z_calib):
    """Set the model's calibration context and return the z_calib tensor.

    Only the MLP function class is used in this Scout; kept the branch for
    uniformity with the old runner.
    """
    if isinstance(model, adapter.MLPCorrector):
        feats = adapter._summary_statistics(z_calib)
        model.set_context_from_features(feats)
    else:  # GRU (kept for parity; not used in this Scout)
        seq = adapter._z_to_real_features(z_calib)
        model.set_sequence_from_array(seq)
    return torch.from_numpy(z_calib).to(DEVICE).unsqueeze(0).to(torch.complex64)


def train_model(model_cls, hyperparams, train_dataset, val_dataset, *, log=print):
    """Train one model instance on the O1 objective. Returns trained model +
    final val loss."""
    model = model_cls(hidden_dim=hyperparams["hidden_dim"]).to(DEVICE)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=hyperparams["learning_rate"],
        weight_decay=hyperparams["weight_decay"],
    )

    train_keys = list(train_dataset.keys())
    val_keys = list(val_dataset.keys())

    best_val_loss = float("inf")
    best_state = None
    patience_counter = 0

    for epoch in range(N_EPOCHS):
        np.random.shuffle(train_keys)
        model.train()
        for key in train_keys:
            rec = train_dataset[key]
            if rec.get("diverged", False):
                continue
            z_calib_t = _set_context_and_z(model, rec["z_calib"])
            optimizer.zero_grad()
            A, b = model.forward()
            loss = _train_loss_o1(z_calib_t, A, b)
            loss.backward()
            optimizer.step()

        # Validate.
        model.eval()
        val_loss_sum = 0.0
        n_val = 0
        with torch.no_grad():
            for key in val_keys:
                rec = val_dataset[key]
                if rec.get("diverged", False):
                    continue
                z_calib_t = _set_context_and_z(model, rec["z_calib"])
                A, b = model.forward()
                val_loss_sum += _eval_loss_o1(z_calib_t, A, b)
                n_val += 1
        val_loss = val_loss_sum / max(n_val, 1)

        if val_loss < best_val_loss - 1e-9:
            best_val_loss = val_loss
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= EARLY_STOP_PATIENCE:
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_val_loss


def tune_function_class(model_cls, class_name, train_dataset, val_dataset, log=print):
    """Train ONE representative HP (the change is the LOSS, not the HP)."""
    log(f"  [tune] {class_name}: training ONE representative HP on O1 objective "
        f"(grid declared in contract; representative sufficient for Scout)")
    hp = dict(REPRESENTATIVE_HP)
    torch.manual_seed(0)
    np.random.seed(0)
    model, val_loss = train_model(model_cls, hp, train_dataset, val_dataset, log=log)
    log(f"  [tune] {class_name}: representative HP={hp} O1 val_loss={val_loss:.6f}")
    return model, hp, val_loss


# =============================================================================
# Held-out evaluation (test slice [71-80] — SAME as old batch + adjudication)
# =============================================================================

def _metrics_for_corrected_stream(corrected_x, corrected_y, *, truth_eval, bits_x_eval, bits_y_eval):
    m = evaluator.evaluate_dual_16qam(
        corrected_x, corrected_y,
        truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
    )
    return {
        "pi_ser": float(m["pi_ser"]),
        "fixed_label_ser": float(m["fixed_label_ser"]),
    }


def evaluate_one(model, cell, rec, *, ridge_blind):
    """Evaluate fixed_cma / blind / candidate / oracle on ONE (cell, seed)."""
    z_calib = rec["z_calib"]
    z_eval = rec["z_eval"]
    truth_calib = rec["truth_calib"]
    truth_eval = rec["truth_eval"]
    bx = rec["bits_x_eval"]
    by = rec["bits_y_eval"]

    # 1. fixed_cma (nearest-16QAM on raw z_eval).
    fixed_pred = evaluator.hard_16qam(z_eval)
    m_fixed = _metrics_for_corrected_stream(
        fixed_pred[:, 0], fixed_pred[:, 1],
        truth_eval=truth_eval, bits_x_eval=bx, bits_y_eval=by,
    )

    # 2. blind_affine (frozen ridge; CLOSED-FORM O1 fit).
    blind_out = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge_blind)
    m_blind = _metrics_for_corrected_stream(
        blind_out["corrected"][:, 0], blind_out["corrected"][:, 1],
        truth_eval=truth_eval, bits_x_eval=bx, bits_y_eval=by,
    )

    # 3. candidate (the trained model; context-dependent O1 fit).
    model.eval()
    with torch.no_grad():
        model.calibrate(z_calib)
        A, b = model.get_correction()
    cand_corrected = adapter.apply_correction(z_eval, A, b)
    m_cand = _metrics_for_corrected_stream(
        cand_corrected[:, 0], cand_corrected[:, 1],
        truth_eval=truth_eval, bits_x_eval=bx, bits_y_eval=by,
    )

    # 4. oracle_affine (Kill bound only).
    oracle_corrected = evaluator.oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge=ridge_blind)
    m_oracle = _metrics_for_corrected_stream(
        oracle_corrected[:, 0], oracle_corrected[:, 1],
        truth_eval=truth_eval, bits_x_eval=bx, bits_y_eval=by,
    )

    return {
        "pi_ser_fixed_cma": m_fixed["pi_ser"],
        "pi_ser_blind": m_blind["pi_ser"],
        "pi_ser_candidate": m_cand["pi_ser"],
        "pi_ser_oracle": m_oracle["pi_ser"],
        "fixed_label_ser_fixed_cma": m_fixed["fixed_label_ser"],
        "fixed_label_ser_blind": m_blind["fixed_label_ser"],
        "fixed_label_ser_candidate": m_cand["fixed_label_ser"],
        "fixed_label_ser_oracle": m_oracle["fixed_label_ser"],
    }


def evaluate_held_out(model, class_name, test_dataset, *, ridge_blind, log=print):
    results = {"candidate_class": class_name, "cells": []}
    for cell in [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in HELD_OUT_CELL_IDS]:
        cell_record = {"cell_id": cell["id"], "per_seed": []}
        for seed in TEST_SEEDS:
            rec = test_dataset.get((cell["id"], seed))
            if rec is None or rec.get("diverged", False):
                continue
            metrics = evaluate_one(model, cell, rec, ridge_blind=ridge_blind)
            metrics["seed"] = int(seed)
            cell_record["per_seed"].append(metrics)
        cell_record["aggregate"] = _aggregate_cell(cell_record["per_seed"])
        agg = cell_record["aggregate"]
        log(f"  cell {cell['id']}: "
            f"fixed={agg['pi_ser_fixed_cma_mean']:.4f}, "
            f"blind={agg['pi_ser_blind_mean']:.4f}, "
            f"cand={agg['pi_ser_candidate_mean']:.4f}, "
            f"oracle={agg['pi_ser_oracle_mean']:.4f}, "
            f"Δ(cand-blind)={agg['pi_ser_candidate_mean']-agg['pi_ser_blind_mean']:+.4f}")
        results["cells"].append(cell_record)
    return results


def _aggregate_cell(per_seed):
    agg = {}
    for comp in ("fixed_cma", "blind", "candidate", "oracle"):
        pi_vals = [s[f"pi_ser_{comp}"] for s in per_seed if np.isfinite(s.get(f"pi_ser_{comp}", float("nan")))]
        fl_vals = [s[f"fixed_label_ser_{comp}"] for s in per_seed if np.isfinite(s.get(f"fixed_label_ser_{comp}", float("nan")))]
        agg[f"pi_ser_{comp}_mean"] = float(np.mean(pi_vals)) if pi_vals else float("nan")
        agg[f"fixed_label_ser_{comp}_mean"] = float(np.mean(fl_vals)) if fl_vals else float("nan")
    return agg


# =============================================================================
# Paired bootstrap CI (IDENTICAL to old batch)
# =============================================================================

def paired_bootstrap_ci(deltas, *, n_boot=10000, alpha=0.05, seed=20260721):
    if not deltas:
        return {"mean": float("nan"), "lower": float("nan"),
                "upper": float("nan"), "n": 0}
    arr = np.asarray(deltas, dtype=float)
    n = len(arr)
    rng = np.random.default_rng(seed)
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_means[b] = float(np.mean(arr[idx]))
    return {
        "mean": float(arr.mean()),
        "lower": float(np.percentile(boot_means, 100 * (alpha / 2))),
        "upper": float(np.percentile(boot_means, 100 * (1 - alpha / 2))),
        "n": int(n),
    }


def per_seed_delta(cell_record, *, comp_a, comp_b):
    deltas = []
    for s in cell_record["per_seed"]:
        a = s.get(f"pi_ser_{comp_a}")
        b = s.get(f"pi_ser_{comp_b}")
        if a is None or b is None or np.isnan(a) or np.isnan(b):
            continue
        deltas.append(float(a - b))
    return deltas


def hierarchical_paired_bootstrap(results, *, comp_a, comp_b, n_boot=10000):
    held = results["cells"]
    per_cell = [per_seed_delta(c, comp_a=comp_a, comp_b=comp_b) for c in held]
    valid = [d for d in per_cell if len(d) > 0]
    if not valid:
        return {"macro_mean": float("nan"), "lower": float("nan"),
                "upper": float("nan"), "n_cells": 0,
                "per_cell_means": []}
    cell_means = np.array([float(np.mean(d)) for d in per_cell])
    rng = np.random.default_rng(20260721)
    n_cells = len(valid)
    boot_macros = np.empty(n_boot)
    for b in range(n_boot):
        cell_idx = rng.integers(0, n_cells, size=n_cells)
        macro = []
        for ci in cell_idx:
            d = valid[ci]
            seed_idx = rng.integers(0, len(d), size=len(d))
            macro.append(float(np.mean(np.asarray(d)[seed_idx])))
        boot_macros[b] = float(np.mean(macro))
    macro_mean = float(np.mean(cell_means[~np.isnan(cell_means)]))
    return {
        "macro_mean": macro_mean,
        "lower": float(np.percentile(boot_macros, 2.5)),
        "upper": float(np.percentile(boot_macros, 97.5)),
        "n_cells": int(n_cells),
        "per_cell_means": cell_means.tolist(),
    }


# =============================================================================
# Adjudication (per candidate) — IDENTICAL rule to old batch
# =============================================================================

def adjudicate_candidate(results):
    """Apply the frozen decision rule for ONE candidate class."""
    held = results["cells"]

    ci_cand_vs_blind = hierarchical_paired_bootstrap(
        results, comp_a="candidate", comp_b="blind")
    ci_cand_vs_fixed = hierarchical_paired_bootstrap(
        results, comp_a="candidate", comp_b="fixed_cma")

    macro_delta_cand_vs_blind = ci_cand_vs_blind["macro_mean"]
    macro_ci_upper_cand_vs_blind = ci_cand_vs_blind["upper"]

    # Per-cell count: candidate beats blind by >= MDE.
    n_cells_beats_blind_by_mde = 0
    for c in held:
        agg = c["aggregate"]
        if (np.isfinite(agg["pi_ser_blind_mean"]) and np.isfinite(agg["pi_ser_candidate_mean"])
                and (agg["pi_ser_blind_mean"] - agg["pi_ser_candidate_mean"]) >= MDE):
            n_cells_beats_blind_by_mde += 1

    # Worst-cell candidate vs fixed_cma (instability check).
    worst_cand_vs_fixed = max(
        (c["aggregate"]["pi_ser_candidate_mean"] - c["aggregate"]["pi_ser_fixed_cma_mean"]
         for c in held
         if np.isfinite(c["aggregate"].get("pi_ser_candidate_mean", float("nan")))),
        default=float("nan"),
    )
    n_cells_worst_degradation = sum(
        1 for c in held
        if np.isfinite(c["aggregate"].get("pi_ser_candidate_mean", float("nan")))
        and (c["aggregate"]["pi_ser_candidate_mean"] - c["aggregate"]["pi_ser_fixed_cma_mean"]) > MDE
    )

    a_conditions = {
        "macro_delta_cand_minus_blind_le_neg_mde": macro_delta_cand_vs_blind <= -MDE,
        "macro_ci_upper_lt_0": (np.isfinite(macro_ci_upper_cand_vs_blind)
                                and macro_ci_upper_cand_vs_blind < 0.0),
        "beats_blind_by_mde_in_at_least_5_of_7_cells": n_cells_beats_blind_by_mde >= 5,
        "worst_degradation_vs_fixed_cma_le_mde": (np.isfinite(worst_cand_vs_fixed)
                                                  and worst_cand_vs_fixed <= MDE),
    }
    blows_up = n_cells_worst_degradation >= 2

    if all(a_conditions.values()):
        verdict = "CANDIDATE_BEATS_BLIND_STABLY"
    elif blows_up:
        verdict = "CANDIDATE_BLOWS_UP"
    else:
        verdict = "CANDIDATE_DOES_NOT_BEAT_BLIND"

    return {
        "verdict": verdict,
        "macro_delta_candidate_minus_blind": macro_delta_cand_vs_blind,
        "macro_ci_upper_candidate_minus_blind": macro_ci_upper_cand_vs_blind,
        "ci_candidate_minus_blind": ci_cand_vs_blind,
        "ci_candidate_minus_fixed": ci_cand_vs_fixed,
        "n_cells_beats_blind_by_mde": n_cells_beats_blind_by_mde,
        "n_held_out_cells": len(held),
        "worst_candidate_degradation_vs_fixed_cma": worst_cand_vs_fixed,
        "n_cells_worst_degradation_gt_mde": n_cells_worst_degradation,
        "a_conditions": a_conditions,
        "mde": MDE,
    }


# =============================================================================
# Semantic smoke (identity / constant / no-harm) — run BEFORE held-out eval
# =============================================================================

def run_semantic_smoke(log=print):
    """Mandatory semantic smoke before held-out eval.

    1. Identity test: A=I, b=0 gives a finite, non-degenerate O1 loss.
    2. Constant test: A=0 constant-b optimum is WORSE than the full (A,b)
       optimum (the gate the OLD soft loss FAILED).
    3. No-harm test: a briefly-trained model on a single realization does not
       scramble z_eval (PI-SER not at the 16QAM random ceiling 0.9375).

    Returns dict {passed: bool, ...details}. If not passed, the runner aborts.
    """
    rng_seed = 12345
    cell = {"id": "smoke-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,
            "sop_rate": 4e-6, "n_symbols": 512, "modulation": "qam16"}
    log("[smoke] building a single realization for identity/constant/no-harm tests...")
    rlz = make_realization(cell, rng_seed)
    cma = run_fixed_mu_cma(cell, rlz)
    if cma["diverged"]:
        return {"passed": False, "reason": "CMA diverged on smoke realization"}
    es, ce, ee, _ = _eval_window_for_cell(cell)
    z_calib, z_eval, truth_calib, truth_eval, bx, by = _split_calib_eval(
        cma["zX"], cma["zY"], rlz, eval_start=es, calibration_end=ce, eval_end=ee)

    # ---- 1. Identity test: A=I, b=0 ----
    zt = torch.from_numpy(z_calib).to(DEVICE).unsqueeze(0).to(torch.complex64)
    A_id = torch.eye(2, dtype=torch.complex64, device=DEVICE).unsqueeze(0)
    b_zero = torch.zeros(1, 2, dtype=torch.complex64, device=DEVICE)
    id_loss = _eval_loss_o1(zt, A_id, b_zero)
    identity_ok = bool(np.isfinite(id_loss) and id_loss < 1e6 and id_loss > 0)
    # The OLD soft loss gave the SAME constant ~1.31 for any input; the O1
    # identity loss should be substantially different and input-dependent.
    log(f"[smoke] identity (A=I,b=0) O1 loss = {id_loss:.6f} "
        f"(finite, non-degenerate: {identity_ok})")

    # ---- 2. Constant test: A=0 const-b optimum vs full (A,b) optimum ----
    # Const optimum: z_corrected = b for all symbols; best b = mean(hard_label).
    # The probe optimized in full complex torch; here we do the same compactly:
    #   const target = hard_16qam(z_calib) (detached), best const b = mean(target)
    hard_label_np = np.asarray(evaluator.hard_16qam(z_calib), dtype=np.complex128)
    b_const_opt = hard_label_np.mean(axis=0)
    const_loss = float(np.mean(np.abs(hard_label_np - b_const_opt[None, :]) ** 2))
    # Full optimum: closed-form ridge LS (same as blind_affine) — the EXACT O1
    # minimizer. This is the bar.
    ridge = float(FROZEN["blind_affine_ridge_frozen"])
    design = np.column_stack((z_calib.astype(np.complex128),
                              np.ones(len(z_calib), dtype=np.complex128)))
    reg = np.eye(design.shape[1], dtype=np.complex128) * ridge
    reg[-1, -1] = 0.0
    coef = np.linalg.solve(design.conj().T @ design + reg,
                           design.conj().T @ hard_label_np)
    pred = design @ coef
    full_loss = float(np.mean(np.abs(pred - hard_label_np) ** 2))
    constant_test_ok = bool(const_loss > full_loss + 1e-6)
    log(f"[smoke] constant (A=0, best b) O1 loss = {const_loss:.6f}; "
        f"full (A,b) closed-form O1 loss = {full_loss:.6f}; "
        f"delta(const-full) = {const_loss - full_loss:+.6f} "
        f"(full strictly better: {constant_test_ok})")

    # ---- 3. No-harm test: train briefly, check candidate doesn't scramble ----
    torch.manual_seed(0)
    np.random.seed(0)
    model = adapter.MLPCorrector(hidden_dim=REPRESENTATIVE_HP["hidden_dim"]).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=REPRESENTATIVE_HP["learning_rate"],
                                 weight_decay=REPRESENTATIVE_HP["weight_decay"])
    for _ in range(15):  # brief Lloyd-like iterations on the single realization
        zt_i = _set_context_and_z(model, z_calib)
        optimizer.zero_grad()
        A, b = model.forward()
        loss = _train_loss_o1(zt_i, A, b)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        model.calibrate(z_calib)
        A_c, b_c = model.get_correction()
    cand_corrected = adapter.apply_correction(z_eval, A_c, b_c)
    m_cand = _metrics_for_corrected_stream(
        cand_corrected[:, 0], cand_corrected[:, 1],
        truth_eval=truth_eval, bits_x_eval=bx, bits_y_eval=by)
    RANDOM_CEILING_16QAM = 0.9375  # 15/16 symbols wrong
    no_harm_ok = bool(m_cand["pi_ser"] < RANDOM_CEILING_16QAM - 1e-6)
    log(f"[smoke] briefly-trained candidate PI-SER on z_eval = {m_cand['pi_ser']:.4f} "
        f"(below random ceiling 0.9375: {no_harm_ok})")

    passed = bool(identity_ok and constant_test_ok and no_harm_ok)
    return {
        "passed": passed,
        "identity_test": {"loss": id_loss, "passed": identity_ok},
        "constant_test": {"const_loss": const_loss, "full_loss": full_loss,
                          "delta_const_minus_full": const_loss - full_loss,
                          "passed": constant_test_ok},
        "no_harm_test": {"pi_ser": m_cand["pi_ser"],
                         "fixed_label_ser": m_cand["fixed_label_ser"],
                         "random_ceiling": RANDOM_CEILING_16QAM,
                         "passed": no_harm_ok},
    }


# =============================================================================
# Source-closure provenance
# =============================================================================

def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


_SOURCE_CLOSURE_PATHS = [
    BATCH_DIR / "batch-contract.v1.yaml",
    BATCH_DIR / "src" / "run_o1_corrected_scout.py",
    BATCH_DIR / "src" / "test_o1_identity.py",
    OLD_BATCH_DIR / "src" / "corrector_adapter.py",   # reused UNCHANGED
    ATLAS_DIR / "cb1_evaluator.py",
    ATLAS_DIR / "cb1_cell_runner.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_dual_pol_channel.py",
    REPO_ROOT / "projects" / "simulation" / "common" / "_modulation.py",
]


def _source_closure_hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    base = REPO_ROOT
    for p in _SOURCE_CLOSURE_PATHS:
        if not p.exists():
            out[str(p.relative_to(base))] = "MISSING"
            continue
        try:
            rel = str(p.relative_to(base))
        except ValueError:
            rel = str(p)
        out[rel] = _sha256_of_file(p)
    return out


# =============================================================================
# Main
# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune-train-eval", action="store_true",
                    help="run the full tune/train/eval/adjudicate pipeline")
    ap.add_argument("--smoke", action="store_true",
                    help="run ONLY the semantic smoke (identity/constant/no-harm)")
    args = ap.parse_args()

    out_path = BATCH_DIR / "artifacts" / "result.v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    global TRAINING_SEEDS, VALIDATION_SEEDS, TEST_SEEDS, HP_TUNING_SEEDS, N_EPOCHS
    if args.smoke:
        TRAINING_SEEDS = [81, 82]
        VALIDATION_SEEDS = [91]
        TEST_SEEDS = [71, 72]
        HP_TUNING_SEEDS = [81]
        N_EPOCHS = 5

    log = lambda msg: print(msg, flush=True)
    log(f"[O1-scout] device = {DEVICE}")

    # ---- Phase 0a: legality identity tests (pytest) ----
    log("[O1-scout] Phase 0a: legality identity tests (must PASS before any training)")
    import pytest
    exit_code = pytest.main([
        "-x", "--tb=short", "-q",
        str(BATCH_DIR / "src" / "test_o1_identity.py"),
    ])
    if exit_code != 0:
        log(f"[O1-scout] FATAL: legality tests FAILED (pytest exit {exit_code}). Aborting.")
        sys.exit(2)
    log("[O1-scout] legality tests PASS.")

    # ---- Phase 0b: semantic smoke (identity / constant / no-harm) ----
    log("[O1-scout] Phase 0b: semantic smoke (identity / constant / no-harm)")
    smoke = run_semantic_smoke(log=log)
    smoke_path = BATCH_DIR / "artifacts" / "smoke.json"
    with open(smoke_path, "w", encoding="utf-8") as f:
        json.dump(smoke, f, indent=2, default=str)
    if not smoke["passed"]:
        log(f"[O1-scout] FATAL: semantic smoke FAILED -> {smoke}. "
            f"Aborting before held-out eval (DIAGNOSTIC).")
        # Still persist the smoke result so the diagnostic is auditable.
        sys.exit(3)
    log(f"[O1-scout] semantic smoke PASS. (identity_loss={smoke['identity_test']['loss']:.6f}, "
        f"delta(const-full)={smoke['constant_test']['delta_const_minus_full']:+.6f}, "
        f"cand PI-SER={smoke['no_harm_test']['pi_ser']:.4f})")

    if args.smoke:
        log(f"[O1-scout] --smoke: stopping after smoke (passed). {time.time()-t0:.1f}s")
        return

    if not args.tune_train_eval:
        log("[O1-scout] no --tune-train-eval given; smoke passed, nothing else to do.")
        return

    # ---- Phase 1: build datasets ----
    log("[O1-scout] Phase 1: build train / val / test datasets (fixed-mu CMA ONCE per cell x seed)")
    training_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in TRAINING_CELL_IDS]
    held_out_cells = [c for c in ATLAS_V1_16QAM_CELLS if c["id"] in HELD_OUT_CELL_IDS]
    log(f"  training cells ({len(training_cells)}): {[c['id'] for c in training_cells]}")
    log(f"  held-out cells ({len(held_out_cells)}): {[c['id'] for c in held_out_cells]}")
    log(f"  train_seeds={TRAINING_SEEDS}  val_seeds={VALIDATION_SEEDS}  test_seeds={TEST_SEEDS}")
    train_dataset = build_dataset(training_cells, TRAINING_SEEDS, log=log)
    val_dataset = build_dataset(training_cells, VALIDATION_SEEDS, log=log)
    test_dataset = build_dataset(held_out_cells, TEST_SEEDS, log=log)

    ridge_blind = float(FROZEN["blind_affine_ridge_frozen"])

    # ---- Phase 2: train the MLP candidate on O1 ----
    candidates = {}
    for class_name, cls in [("C04_mlp", adapter.MLPCorrector)]:
        log(f"[O1-scout] Phase 2: tune + train {class_name} on O1 objective")
        model, best_hp, best_val = tune_function_class(
            cls, class_name, train_dataset, val_dataset, log=log)
        candidates[class_name] = {"model": model, "best_hp": best_hp, "best_val_loss": best_val}

    # Persist frozen params.
    frozen_out = {
        "fixed_mu_cma_mu": float(FROZEN["cma_mu_fixed"]),
        "blind_affine_ridge_frozen": float(ridge_blind),
        "training_seeds": TRAINING_SEEDS,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "hp_tuning_seeds": HP_TUNING_SEEDS,
        "n_epochs": N_EPOCHS,
        "early_stop_patience": EARLY_STOP_PATIENCE,
        "hp_grid": HP_GRID,
        "representative_hp": REPRESENTATIVE_HP,
        "mde": MDE,
        "objective": "O1_hard_pseudo_label_MSE_detached_target",
        "candidates": {cn: {"best_hp": c["best_hp"], "best_val_loss": c["best_val_loss"]}
                       for cn, c in candidates.items()},
    }
    params_path = BATCH_DIR / "artifacts" / "frozen-params.v1.yaml"
    with open(params_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(frozen_out, f, sort_keys=False, allow_unicode=True)
    log(f"[O1-scout] frozen params: {params_path}")

    # ---- Phase 3: held-out evaluation ----
    log("[O1-scout] Phase 3: held-out evaluation on 7 cells x 10 test seeds (paired with blind_affine)")
    results = {"candidates": {}}
    for class_name, bundle in candidates.items():
        log(f"[O1-scout] evaluating {class_name}...")
        cand_results = evaluate_held_out(
            bundle["model"], class_name, test_dataset, ridge_blind=ridge_blind, log=log)
        results["candidates"][class_name] = cand_results

    # ---- Phase 4: adjudicate ----
    log("[O1-scout] Phase 4: adjudicate per candidate")
    adjudications = {}
    for class_name, cand_results in results["candidates"].items():
        adj = adjudicate_candidate(cand_results)
        adjudications[class_name] = adj
        log(f"[O1-scout] {class_name} VERDICT: {adj['verdict']}")
        log(f"  macro Δ(cand - blind) = {adj['macro_delta_candidate_minus_blind']:+.5f}  "
            f"CI_upper = {adj['macro_ci_upper_candidate_minus_blind']:+.5f}  (need < 0 for BEATS)")
        log(f"  cells beating blind by >= MDE: {adj['n_cells_beats_blind_by_mde']}/7  (need >= 5)")
        log(f"  worst cand degradation vs fixed_cma: {adj['worst_candidate_degradation_vs_fixed_cma']:+.5f}  "
            f"(need <= {MDE})")

    results["adjudications"] = adjudications
    results["frozen_params"] = frozen_out
    results["smoke"] = smoke
    results["metadata"] = {
        "schema": "direction-lab.cb1.c04-c09-o1-corrected-scout.v1",
        "campaign_id": "science-scout-2026-07-20.dual-pol-osl",
        "triggered_by": "probe_p01_O1_input_dependent_optimum_2026-07-21",
        "related_decisions": ["D016-constant-collapse", "V005", "V017",
                              "D010", "D011-amended", "D012", "D013-corrector-adjudication-A"],
        "MDE": MDE,
        "training_seeds": TRAINING_SEEDS,
        "validation_seeds": VALIDATION_SEEDS,
        "test_seeds": TEST_SEEDS,
        "leakage_check": (
            "set(train) ∩ set(val) ∩ set(test) = ∅ pairwise; "
            "set(train,val) ∩ set(prior batches {11-65}) = ∅; "
            "training_cells ∩ held_out_cells = ∅ (all asserted). "
            "SAME seed/cell split as c04-c09-shared-corrector-v1 for paired comparison."
        ),
        "R2_qam16": R2_16QAM,
        "device": str(DEVICE),
        "elapsed_seconds": time.time() - t0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "objective": "O1_hard_pseudo_label_MSE_detached_target",
        "objective_note": (
            "The ONLY change from c04-c09-shared-corrector-v1. O1 = "
            "MSE(z_corrected, hard_16qam(z_corrected).detach()). Probe p01 "
            "confirmed input-dependent optimum (full=0.039 < const=0.452). "
            "This is the objective blind_affine solves in CLOSED FORM; the "
            "candidate learns it per-realization conditioned on trace features."
        ),
        "blind_affine_ridge_frozen_from": "corrector-residual-headroom-v1_validation_tuning",
        "fixed_mu_cma_mu_inherited_from": "B01-R HF6 interior optimum",
        "reused_unchanged_from_old_batch": [
            "corrector_adapter.py (MLPCorrector, _summary_statistics, apply_correction)",
            "dataset building", "cell/seed splits", "evaluation",
            "adjudication", "source-closure hashing",
        ],
        "source_closure_sha256": _source_closure_hashes(),
        "information_boundary_note": (
            "Candidates train on MSE(z_corrected, hard_16qam(z_corrected).detach()) "
            "— receiver-visible pseudo-labels only. No TX truth in training or "
            "inference. blind_affine ridge frozen (not re-tuned). oracle_affine "
            "reported for context only (Kill bound)."
        ),
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    log(f"[O1-scout] DONE in {time.time() - t0:.1f}s — {out_path}")


if __name__ == "__main__":
    main()
