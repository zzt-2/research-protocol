"""Identity / legality tests for the C04/C09 shared corrector batch.

These MUST PASS before any training. They enforce:

  1. The candidate corrector NEVER reads TX truth in training or inference.
  2. The candidate's application to the eval slice IS affine (A @ z_eval + b).
  3. The shared adapter exposes a uniform input/output contract for both
     function classes (so C04 and C09 are comparable).
  4. Train/val/test seeds are pairwise disjoint (asserted in source).
  5. Training cells are disjoint from held-out test cells.
  6. Source-closure hash is recorded.

These are LEGALITY gates, not scientific claims.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve()
BATCH_DIR = HERE.parents[1]
CB1_ROOT = BATCH_DIR.parent
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR), str(BATCH_DIR / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _try_load_adapter():
    target = BATCH_DIR / "src" / "corrector_adapter.py"
    if not target.exists():
        return None
    return _load_module("_test_corrector_adapter", target)


def _try_load_runner():
    target = BATCH_DIR / "src" / "run_corrector_batch.py"
    if not target.exists():
        return None
    return _load_module("_test_corrector_runner", target)


# =============================================================================
# Test 1: candidate does NOT read TX truth
# =============================================================================

class TestCandidateInformationBoundary:
    """Gate: candidate_does_not_read_tx_truth.

    The candidate's forward() takes calibration z (and optionally the eval z
    for context) and outputs an affine + offset. It MUST NOT accept a truth
    argument. Its training loss uses pseudo-labels (hard_16qam), not TX truth.
    """

    def test_adapter_module_has_no_truth_imports(self):
        adapter_path = BATCH_DIR / "src" / "corrector_adapter.py"
        if not adapter_path.exists():
            pytest.fail("corrector_adapter.py not yet implemented (RED)")
        src = adapter_path.read_text(encoding="utf-8")
        # Must not reference TX truth fields
        for bad in ["truth_calibration", "truth_eval", "sX", "sY", "bitsX", "bitsY"]:
            # Allow these only in comments
            lines_with_bad = [l for l in src.splitlines() if bad in l
                              and not l.strip().startswith("#")]
            assert not lines_with_bad, (
                f"adapter references TX truth '{bad}' in code:\n  "
                + "\n  ".join(lines_with_bad[:3])
            )

    def test_forward_signature_has_no_truth_parameter(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not yet implemented (RED)")
        import inspect
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            assert hasattr(adapter, cls_name), f"adapter missing {cls_name}"
            cls = getattr(adapter, cls_name)
            assert hasattr(cls, "forward"), f"{cls_name} has no forward()"
            sig = inspect.signature(cls.forward)
            params = set(sig.parameters.keys())
            for bad in ("truth", "label", "sX", "sY", "tx"):
                # Allow the bad keyword as a substring only in non-truth params
                for p in params:
                    assert not (p == bad or p.endswith("_truth")), (
                        f"{cls_name}.forward accepts forbidden parameter '{p}'"
                    )

    def test_loss_uses_pseudo_labels_not_truth(self):
        runner_path = BATCH_DIR / "src" / "run_corrector_batch.py"
        if not runner_path.exists():
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # The training loss MUST call hard_16qam (pseudo-labels) on z_corrected.
        assert "hard_16qam" in src, (
            "training loss must use hard_16qam (pseudo-labels) on z_corrected"
        )
        # Find the training-loss function and verify it does NOT reference
        # truth. We locate the _train_loss_on_calib function body.
        import re
        m = re.search(
            r"def _train_loss_on_calib\([^)]*\):(.*?)(?=\ndef |\Z)",
            src, re.DOTALL,
        )
        assert m is not None, "runner must define _train_loss_on_calib()"
        loss_body = m.group(1)
        for bad in ["truth", "sX", "sY", "bitsX", "bitsY"]:
            # Strip comments from each line before checking.
            code_lines = [l.split("#")[0] for l in loss_body.splitlines()]
            code_body = "\n".join(code_lines)
            assert bad not in code_body, (
                f"training loss body references '{bad}':\n{loss_body}"
            )


# =============================================================================
# Test 2: candidate application IS affine on the eval slice
# =============================================================================

class TestAffineApplicationForm:
    """Gate: candidate_application_is_affine_form_on_eval_slice.

    The candidate outputs (A, b); the application MUST be z_corrected = A @ z_eval + b.
    We verify by constructing a tiny candidate with a known (A, b) and checking
    the application is exactly the affine map.
    """

    def test_apply_affine_is_A_times_z_plus_b(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not yet implemented (RED)")
        assert hasattr(adapter, "apply_correction"), (
            "adapter must expose apply_correction(z_eval, A, b) -> z_corrected"
        )
        rng = np.random.default_rng(11)
        # 2x2 complex A and 2 complex b; z_eval is [N, 2] complex.
        A = (rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2)))
        b = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        z_eval = (rng.standard_normal((50, 2)) + 1j * rng.standard_normal((50, 2)))
        z_corrected = adapter.apply_correction(z_eval, A, b)
        # Reference: each row z_eval[i] maps to A @ z_eval[i] + b
        ref = (z_eval @ A.T) + b[None, :]
        assert np.allclose(z_corrected, ref, atol=1e-10), (
            f"apply_correction must be A @ z + b; max|Δ| = "
            f"{np.max(np.abs(z_corrected - ref))}"
        )


# =============================================================================
# Test 3: shared adapter uniform contract for both function classes
# =============================================================================

class TestSharedAdapterContract:
    """Gate: shared_adapter_produces_same_input_output_contract_for_both_function_classes.

    MLPCorrector and GRUCorrector must expose the SAME interface:
      - __init__(hyperparameters)
      - calibrate(z_calib) -> sets internal state from calibration context
      - get_correction() -> (A, b) for the current calibration
      - apply_correction(z_eval, A, b) -> z_corrected (shared static method)

    Both must accept the same z_calib format (dual-pol complex array).
    """

    def test_both_classes_expose_same_interface(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not yet implemented (RED)")
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            cls = getattr(adapter, cls_name)
            for method in ("calibrate", "get_correction"):
                assert hasattr(cls, method), (
                    f"{cls_name} missing method '{method}'"
                )

    def test_both_classes_produce_2x2_complex_A_and_2_complex_b(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not yet implemented (RED)")
        rng = np.random.default_rng(22)
        n = 64
        z_calib = (rng.standard_normal((n, 2)) + 1j * rng.standard_normal((n, 2)))
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            cls = getattr(adapter, cls_name)
            # Construct with minimal hyperparams
            try:
                instance = cls(hidden_dim=8)
            except TypeError:
                pytest.fail(f"{cls_name}.__init__ must accept hidden_dim kwarg")
            instance.calibrate(z_calib)
            A, b = instance.get_correction()
            assert A.shape == (2, 2), f"{cls_name} A shape {A.shape}, expected (2,2)"
            assert np.iscomplexobj(A), f"{cls_name} A must be complex"
            assert b.shape == (2,), f"{cls_name} b shape {b.shape}, expected (2,)"
            assert np.iscomplexobj(b), f"{cls_name} b must be complex"


# =============================================================================
# Test 4: train/val/test seeds pairwise disjoint
# =============================================================================

class TestSeedIsolation:
    """Gate: train_val_test_seeds_pairwise_disjoint_asserted."""

    def test_runner_asserts_seed_disjoint(self):
        runner_path = BATCH_DIR / "src" / "run_corrector_batch.py"
        if not runner_path.exists():
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # Must contain explicit disjoint asserts
        assert "isdisjoint" in src or "set(" in src, (
            "runner must assert train/val/test seed disjointness"
        )

    def test_train_val_test_seeds_are_disjoint(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        train = set(runner.TRAINING_SEEDS)
        val = set(runner.VALIDATION_SEEDS)
        test = set(runner.TEST_SEEDS)
        assert train.isdisjoint(val), f"train ∩ val != ∅: {train & val}"
        assert train.isdisjoint(test), f"train ∩ test != ∅: {train & test}"
        assert val.isdisjoint(test), f"val ∩ test != ∅: {val & test}"

    def test_train_val_seeds_disjoint_from_all_prior_batches(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        train_val = set(runner.TRAINING_SEEDS) | set(runner.VALIDATION_SEEDS)
        # All prior-batch seeds: 11-50 (B01/B01-R/c11-legality), 61-65 (adjudication val).
        prior = set(range(11, 51)) | {61, 62, 63, 64, 65}
        overlap = train_val & prior
        assert not overlap, (
            f"train/val seeds overlap prior batches: {overlap}"
        )


# =============================================================================
# Test 5: training cells disjoint from held-out test cells
# =============================================================================

class TestCellIsolation:
    """Gate: training_cells_disjoint_from_held_out_test_cells_asserted."""

    def test_runner_training_and_test_cells_disjoint(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        train_cells = set(runner.TRAINING_CELL_IDS)
        test_cells = set(runner.HELD_OUT_CELL_IDS)
        overlap = train_cells & test_cells
        assert not overlap, (
            f"training cells overlap test cells: {overlap}"
        )


# =============================================================================
# Test 6: source-closure hash recorded
# =============================================================================

class TestSourceClosureHashRecorded:
    """Gate: source_closure_hash_recorded."""

    def test_runner_exposes_source_closure_hash_helper(self):
        runner_path = BATCH_DIR / "src" / "run_corrector_batch.py"
        if not runner_path.exists():
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        assert "def _source_closure_hashes(" in src
        assert "source_closure_sha256" in src

    def test_source_closure_includes_key_sources(self):
        runner_path = BATCH_DIR / "src" / "run_corrector_batch.py"
        if not runner_path.exists():
            pytest.fail("run_corrector_batch.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        for needle in ["batch-contract.v1.yaml", "corrector_adapter.py",
                       "run_corrector_batch.py", "cb1_evaluator.py",
                       "cb1_cell_runner.py", "_dual_pol_channel.py"]:
            assert needle in src, f"source closure missing {needle}"
