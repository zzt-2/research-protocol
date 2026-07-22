"""Legality / identity tests for the C04/C09 O1-corrected corrector Scout.

These are LEGALITY GATES (not scientific claims) and MUST PASS before any
training or evaluation. Adapted from
c04-c09-shared-corrector-v1/tests/test_corrector_identity.py with the training-
loss reference updated to the corrected O1 objective (_train_loss_o1).

They enforce:
  1. The candidate corrector NEVER reads TX truth in training or inference.
  2. The candidate's application to the eval slice IS affine (z_eval @ A.T + b).
  3. The shared adapter exposes a uniform input/output contract.
  4. Train/val/test seeds are pairwise disjoint (asserted in source).
  5. Training cells are disjoint from held-out test cells.
  6. Source-closure hash is recorded.
  7. The corrected O1 objective is in use (NOT the old soft expected-distance
     loss that caused constant-collapse / D016).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent                                  # .../src
BATCH_DIR = SRC_DIR.parent                             # .../c04-c09-o1-corrected-scout
CB1_ROOT = BATCH_DIR.parent                            # .../cb1-modulation-generic-closure
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
OLD_BATCH_DIR = CB1_ROOT / "c04-c09-shared-corrector-v1"  # reused adapter lives here
REPO_ROOT = HERE.parents[7]
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR), str(SRC_DIR),
          str(OLD_BATCH_DIR), str(OLD_BATCH_DIR / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _try_load_adapter():
    target = OLD_BATCH_DIR / "src" / "corrector_adapter.py"
    if not target.exists():
        return None
    return _load_module("_test_corrector_adapter", target)


def _try_load_runner():
    target = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
    if not target.exists():
        return None
    return _load_module("_test_o1_runner", target)


# =============================================================================
# Test 1: candidate does NOT read TX truth
# =============================================================================

class TestCandidateInformationBoundary:
    """Gate: candidate_does_not_read_tx_truth.

    The candidate's forward() takes calibration z and outputs an affine + offset.
    It MUST NOT accept a truth argument. Its training loss uses hard_16qam
    pseudo-labels (detached), not TX truth.
    """

    def test_adapter_module_has_no_truth_imports(self):
        adapter_path = OLD_BATCH_DIR / "src" / "corrector_adapter.py"
        if not adapter_path.exists():
            pytest.fail("corrector_adapter.py not found (REUSED from old batch)")
        src = adapter_path.read_text(encoding="utf-8")
        for bad in ["truth_calibration", "truth_eval", "sX", "sY", "bitsX", "bitsY"]:
            lines_with_bad = [l for l in src.splitlines() if bad in l
                              and not l.strip().startswith("#")]
            assert not lines_with_bad, (
                f"adapter references TX truth '{bad}' in code:\n  "
                + "\n  ".join(lines_with_bad[:3])
            )

    def test_forward_signature_has_no_truth_parameter(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not found")
        import inspect
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            assert hasattr(adapter, cls_name), f"adapter missing {cls_name}"
            cls = getattr(adapter, cls_name)
            assert hasattr(cls, "forward"), f"{cls_name} has no forward()"
            sig = inspect.signature(cls.forward)
            params = set(sig.parameters.keys())
            for p in params:
                assert not (p == "truth" or p.endswith("_truth")), (
                    f"{cls_name}.forward accepts forbidden parameter '{p}'"
                )

    def test_runner_loss_uses_hard_16qam_pseudo_labels_not_truth(self):
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # The O1 training loss must use hard_16qam-derived pseudo-labels.
        assert "hard_16qam" in src or "_torch_hard_16qam" in src, (
            "training loss must use hard_16qam-derived pseudo-labels"
        )
        # Find the O1 training-loss function and verify it does NOT reference
        # TX truth fields.
        m = re.search(
            r"def _train_loss_o1\([^)]*\):(.*?)(?=\ndef |\Z)",
            src, re.DOTALL,
        )
        assert m is not None, (
            "runner must define _train_loss_o1() (the corrected O1 objective)"
        )
        loss_body = m.group(1)
        for bad in ["truth", "sX", "sY", "bitsX", "bitsY"]:
            code_lines = [l.split("#")[0] for l in loss_body.splitlines()]
            code_body = "\n".join(code_lines)
            assert bad not in code_body, (
                f"O1 training loss body references '{bad}':\n{loss_body}"
            )


# =============================================================================
# Test 2: candidate application IS affine on the eval slice
# =============================================================================

class TestAffineApplicationForm:
    """Gate: candidate_application_is_affine_form_on_eval_slice."""

    def test_apply_affine_is_A_times_z_plus_b(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not found")
        assert hasattr(adapter, "apply_correction"), (
            "adapter must expose apply_correction(z_eval, A, b) -> z_corrected"
        )
        rng = np.random.default_rng(11)
        A = (rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2)))
        b = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        z_eval = (rng.standard_normal((50, 2)) + 1j * rng.standard_normal((50, 2)))
        z_corrected = adapter.apply_correction(z_eval, A, b)
        ref = (z_eval @ A.T) + b[None, :]
        assert np.allclose(z_corrected, ref, atol=1e-10), (
            f"apply_correction must be z @ A.T + b; max|Δ| = "
            f"{np.max(np.abs(z_corrected - ref))}"
        )


# =============================================================================
# Test 3: shared adapter uniform contract for both function classes
# =============================================================================

class TestSharedAdapterContract:
    """Gate: shared_adapter_produces_uniform_input_output_contract."""

    def test_both_classes_expose_same_interface(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not found")
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            cls = getattr(adapter, cls_name)
            for method in ("calibrate", "get_correction"):
                assert hasattr(cls, method), f"{cls_name} missing '{method}'"

    def test_both_classes_produce_2x2_complex_A_and_2_complex_b(self):
        adapter = _try_load_adapter()
        if adapter is None:
            pytest.fail("corrector_adapter.py not found")
        rng = np.random.default_rng(22)
        n = 64
        z_calib = (rng.standard_normal((n, 2)) + 1j * rng.standard_normal((n, 2)))
        for cls_name in ("MLPCorrector", "GRUCorrector"):
            cls = getattr(adapter, cls_name)
            try:
                instance = cls(hidden_dim=8)
            except TypeError:
                pytest.fail(f"{cls_name}.__init__ must accept hidden_dim")
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
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        assert "isdisjoint" in src, "runner must assert train/val/test seed disjointness"

    def test_train_val_test_seeds_are_disjoint(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        train = set(runner.TRAINING_SEEDS)
        val = set(runner.VALIDATION_SEEDS)
        test = set(runner.TEST_SEEDS)
        assert train.isdisjoint(val), f"train ∩ val != ∅: {train & val}"
        assert train.isdisjoint(test), f"train ∩ test != ∅: {train & test}"
        assert val.isdisjoint(test), f"val ∩ test != ∅: {val & test}"

    def test_train_val_seeds_disjoint_from_all_prior_batches(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        train_val = set(runner.TRAINING_SEEDS) | set(runner.VALIDATION_SEEDS)
        prior = set(range(11, 51)) | {61, 62, 63, 64, 65}
        overlap = train_val & prior
        assert not overlap, f"train/val seeds overlap prior batches: {overlap}"


# =============================================================================
# Test 5: training cells disjoint from held-out test cells
# =============================================================================

class TestCellIsolation:
    """Gate: training_cells_disjoint_from_held_out_test_cells_asserted."""

    def test_runner_training_and_test_cells_disjoint(self):
        runner = _try_load_runner()
        if runner is None:
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        train_cells = set(runner.TRAINING_CELL_IDS)
        test_cells = set(runner.HELD_OUT_CELL_IDS)
        overlap = train_cells & test_cells
        assert not overlap, f"training cells overlap test cells: {overlap}"


# =============================================================================
# Test 6: source-closure hash recorded
# =============================================================================

class TestSourceClosureHashRecorded:
    """Gate: source_closure_hash_recorded."""

    def test_runner_exposes_source_closure_hash_helper(self):
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        assert "def _source_closure_hashes(" in src
        assert "source_closure_sha256" in src

    def test_source_closure_includes_key_sources(self):
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        for needle in ["batch-contract.v1.yaml", "run_o1_corrected_scout.py",
                       "corrector_adapter.py", "cb1_evaluator.py",
                       "cb1_cell_runner.py", "_dual_pol_channel.py",
                       "_modulation.py", "test_o1_identity.py"]:
            assert needle in src, f"source closure missing {needle}"


# =============================================================================
# Test 7: the CORRECTED O1 objective is in use (not the old soft loss)
# =============================================================================

class TestCorrectedObjectiveInUse:
    """Gate: corrected_O1_objective_in_use (NOT the old soft loss that collapsed).

    The whole point of this Scout is the O1 correction. We verify:
      - The runner defines _train_loss_o1 with a DETACHED hard pseudo-label.
      - The runner does NOT use the old soft expected-distance loss form
        (softmax over negative squared distance to grid levels).
    """

    def test_runner_defines_o1_loss_with_detached_pseudo_label(self):
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        m = re.search(
            r"def _train_loss_o1\([^)]*\):(.*?)(?=\ndef |\Z)",
            src, re.DOTALL,
        )
        assert m is not None, "runner must define _train_loss_o1()"
        body = m.group(1)
        # The corrected loss MUST detach the hard-decision pseudo-label.
        assert ".detach()" in body, (
            "O1 loss must detach the hard_16qam pseudo-label (fixed target, "
            "not a gradient path through the non-differentiable hard decision)"
        )

    def test_runner_does_not_use_old_soft_loss(self):
        runner_path = BATCH_DIR / "src" / "run_o1_corrected_scout.py"
        if not runner_path.exists():
            pytest.fail("run_o1_corrected_scout.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # The old soft loss used torch.softmax over negative squared distance to
        # grid levels. The corrected loss must NOT use this form.
        assert "torch.softmax" not in src, (
            "runner must NOT use the old soft expected-distance loss "
            "(torch.softmax over grid distances -> input-independent constant "
            "optimum -> constant collapse, D016/V005)"
        )
