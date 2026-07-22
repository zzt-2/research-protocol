"""F1-A0 strict-causal observability repair — shared infrastructure.

Frozen contract: ../probe-contract.v1.yaml (governed by D020/D021/S013).

This module is the shared substrate for the F1-A0 repair Probe. It wires the SAME
channel / evaluator / runner imports as the sibling info-source-portfolio-probe
``probe_shared.py`` (so the repaired Probe is on the identical physical substrate
as the F1-A it repairs), but it sits one directory deeper
(repair-f1a0/src/ vs info-source-portfolio-probe/src/), so REPO_ROOT is
``HERE.parents[7]`` (verified: ``parents[6]`` is the worktree root).

Differences from probe_shared (the scientific repair, D021):
  - VAL_SEEDS / TEST_SEEDS are the NEW disjoint split 151-155 / 161-170
    (141-150 were already observed by D020 and are forbidden as final test).
  - assert_seed_discipline additionally checks test disjoint from 141-150.
  - grouped_bootstrap_ci_by_cell bootstraps over CELL means (macro), not pooled.
  - source_closure_hashes keys every src/*.py by ``src/<name>``.
  - reconstruct_jones / mmse helpers are NOT re-exported as the default path;
    the repair defines its own E1 (pure-CSI inverse) and reuses the legacy
    mmse_equalize_oracle signature only inside E3 (the privileged genie).
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent                       # .../repair-f1a0/src
REPAIR_DIR = SRC_DIR.parent                 # .../repair-f1a0
BATCH_DIR = REPAIR_DIR.parent               # .../info-source-portfolio-probe
SCOUT_DIR = BATCH_DIR.parent                # .../direction-lab/scout
CB1_ROOT = SCOUT_DIR / "cb1-modulation-generic-closure"
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
MMA_DIR = CB1_ROOT / "baseline-adjudication-batch"
C12_DIR = CB1_ROOT / "c12-gmi-soft-output-scout" / "src"
# repair-f1a0/src is one level deeper than info-source-portfolio-probe/src, so
# the worktree root is parents[7] (parents[6] = .../direction-lab-capability-atlas
# is the worktree root; verified by checking _dual_pol_channel.py resolves there).
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"
for _p in (str(SIM_DIR), str(ATLAS_DIR), str(MMA_DIR), str(C12_DIR), str(SRC_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402

# ─── Frozen contract constants (identical physical substrate to probe_shared) ───
FROZEN = {
    "alpha": 4.2, "beta": 1.4, "block": 100, "t_s": 4e-10,
    "method": "gar", "cma_mu_fixed": 0.03, "cma_taps": 11,
    "cma_block_size": 64, "r2_qam16": 1.32,
}
BLOCK = 100                       # the GG block; per-block prediction horizon
R2_16QAM = 1.32
RANDOM_CEILING = 0.9375           # 16QAM random PI-SER (15/16)
AFFINE_RIDGE = 0.01

# NEW disjoint seed split (D021 / contract data_split). 141-150 are OBSERVED by
# D020 and are forbidden as the final test; 71-80 are prohibited outright.
VAL_SEEDS = [151, 152, 153, 154, 155]
TEST_SEEDS = list(range(161, 171))           # 161..170 inclusive
PRIOR_USED_DO_NOT_REUSE = [
    "11-20", "21-30", "31-35", "41-50", "61-65",
    "71-80", "81-95", "101-105", "121-130",
]
# NOTE: 141-150 are observed by D020 but intentionally NOT in PRIOR_USED_DO_NOT_REUSE;
# the seed-discipline test checks test disjoint from 141-150 separately.
FORBIDDEN_FINAL_TEST_141_150 = list(range(141, 151))

ATLAS_CELLS = [
    {"id": "16qam-snr05-nominal-short", "snr_db": 5.0,  "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr10-nominal-short", "snr_db": 10.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr15-nominal-short", "snr_db": 15.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-nominal-short", "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr25-nominal-short", "snr_db": 25.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg100-short",   "snr_db": 20.0, "f_g_hz": 100.0, "sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-fg1000-short",  "snr_db": 20.0, "f_g_hz": 1000.0,"sop_rate": 4.0e-6, "n_symbols": 512},
    {"id": "16qam-snr20-sop40e-short",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-5, "n_symbols": 512},
    {"id": "16qam-snr10-fg100-long",    "snr_db": 10.0, "f_g_hz": 100.0, "sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr15-fg1000-long",   "snr_db": 15.0, "f_g_hz": 1000.0,"sop_rate": 4.0e-6, "n_symbols": 8192},
    {"id": "16qam-snr20-nominal-long",  "snr_db": 20.0, "f_g_hz": 30.0,  "sop_rate": 4.0e-6, "n_symbols": 8192},
]


def assert_seed_discipline():
    """Assert val/test disjoint, both disjoint from all prior batches, AND test
    disjoint from 141-150 (D020-observed, forbidden as final test)."""
    val = set(VAL_SEEDS)
    test = set(TEST_SEEDS)
    assert not (val & test), f"validation ∩ test = {val & test}"
    prior = set()
    for span in PRIOR_USED_DO_NOT_REUSE:
        lo, hi = map(int, span.split("-"))
        prior |= set(range(lo, hi + 1))
    assert not (val & prior), f"validation ∩ prior = {val & prior}"
    assert not (test & prior), f"test ∩ prior = {test & prior}"
    observed_141_150 = set(FORBIDDEN_FINAL_TEST_141_150)
    assert test.isdisjoint(observed_141_150), (
        f"test ∩ 141-150(D020-observed) = {test & observed_141_150}")


def make_realization(cell, seed):
    """Build ONE shared realization (paired across all methods per (cell,seed)).

    Same frozen params as probe_shared (alpha=4.2, beta=1.4, block=100, t_s=4e-10,
    method=gar, modulation 16qam). h and theta are PER-SAMPLE arrays (length N);
    theta = sop_rate * arange(N) is produced by the generator.
    """
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    return generate_shared_realization_dp(
        int(cell["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(cell["f_g_hz"]), sop_rate=float(cell["sop_rate"]), seed=int(seed),
        gamma_bar=gamma_bar, block=int(FROZEN["block"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation="qam16")


def eval_window(cell):
    """Return (eval_start, calibration_end, eval_end, half_taps)."""
    return atlas_runner.eval_window_for(
        int(cell["n_symbols"]), int(FROZEN["cma_taps"]),
        window_symbols=256, block_size=int(FROZEN["cma_block_size"]))


def metrics(zX, zY, truth_eval, bx, by):
    """pi_ser (primary) + fixed_label_ser (secondary) via cb1_evaluator."""
    m = evaluator.evaluate_dual_16qam(
        zX, zY, truth_eval[:, 0], truth_eval[:, 1], bx, by)
    return {"pi_ser": float(m["pi_ser"]), "fixed_label_ser": float(m["fixed_label_ser"])}


def run_cma_anchor(rX, rY):
    """Canonical anchor: standard_cma_godard_with_z at fixed mu=0.03."""
    return atlas_runner.standard_cma_godard_with_z(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu_fixed"]),
        R2=R2_16QAM, block_size=int(FROZEN["cma_block_size"]))


def reconstruct_jones(h, theta):
    """Reconstruct the real 2x2 SOP Jones from per-sample state (analytic).

    J = sqrt(h) * [[cos, sin],[-sin, cos]] (matches _dual_pol_channel.py:127-132).
    ORACLE/privileged construction — scoring-only (E1/E2/E3), never receiver-visible.
    Returns stacked per-sample (a, b, c, d).
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    sh = np.sqrt(h)
    return sh * cos_t, sh * sin_t, -sh * sin_t, sh * cos_t


# ─── Statistics: grouped (cell) bootstrap CI over cell means ──────────────────

def grouped_bootstrap_ci_by_cell(per_cell_values, n_boot=2000, alpha=0.05, rng_seed=0):
    """Bootstrap over CELL means (macro unit = cell), NOT pooled samples.

    ``per_cell_values`` is a dict {cell_id: list_of_per_seed_values} OR a list of
    cell-mean scalars. Returns (macro, lo, hi) where macro = mean of cell means.
    """
    if isinstance(per_cell_values, dict):
        cell_means = [float(np.mean(v)) for v in per_cell_values.values() if len(v)]
    else:
        cell_means = [float(x) for x in per_cell_values]
    cell_means = np.asarray(cell_means, dtype=float)
    n = len(cell_means)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    macro = float(np.mean(cell_means))
    if n == 1:
        return macro, macro, macro
    rng = np.random.default_rng(rng_seed)
    means = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        means[i] = float(np.mean(cell_means[idx]))
    lo = float(np.quantile(means, alpha / 2))
    hi = float(np.quantile(means, 1 - alpha / 2))
    return macro, lo, hi


# ─── Source-closure hashing of every src/*.py ─────────────────────────────────

def _sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def source_closure_hashes(src_dir=None):
    """SHA-256 of every .py in src/, keyed by ``src/<name>`` (CURRENT hashes)."""
    d = Path(src_dir) if src_dir is not None else SRC_DIR
    out = {}
    for p in sorted(d.glob("*.py")):
        if "__pycache__" in p.name:
            continue
        out["src/" + p.name] = _sha256_of_file(p)
    return out


# ─── Legacy privileged MMSE (reproduces the F1-A 0.133 genie; E3 ONLY) ────────
# Re-implemented locally (not imported from probe_shared) so the repair is
# self-contained and so the source-closure hash covers every src file used.

def mmse_equalize_privileged_tx_truth(rX, rY, h, theta, sX_calib, sY_calib, es, ce, ee):
    """Legacy F1-A oracle: true h/theta (analytic SOP de-rotation) + TX-truth LS
    calibration. PRIVILEGED GENIE — attribution only (E3). Never receiver-visible.

    Reproduces probe_shared.mmse_equalize_oracle exactly.
    """
    a, b, c, d = reconstruct_jones(h, theta)
    inv_det = 1.0 / (a * d - b * c + 1e-30)
    inv_a = d * inv_det
    inv_b = -b * inv_det
    inv_c = -c * inv_det
    inv_d = a * inv_det
    rX_derot = inv_a * rX + inv_b * rY
    rY_derot = inv_c * rX + inv_d * rY
    R_eval = np.vstack([rX_derot[ce:ee], rY_derot[ce:ee]])
    R_cal = np.vstack([rX_derot[es:ce], rY_derot[es:ce]])
    S_cal = np.vstack([sX_calib, sY_calib])
    W, *_ = np.linalg.lstsq(R_cal.T, S_cal.T, rcond=1e-10)
    Z_eval = W.T @ R_eval
    return Z_eval[0], Z_eval[1]
