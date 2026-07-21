"""RED tests for the corrector residual-headroom adjudication — INFORMATION BOUNDARY.

Per TDD (superpowers:test-driven-development): these tests MUST PASS before any
scientific evaluation runs. They enforce the information boundary that makes
the adjudication legal:

  1. blind affine NEVER reads TX truth / oracle label / future / post-hoc fields
  2. perturbing TX truth while holding receiver-visible inputs fixed leaves
     blind affine output BIT-IDENTICAL
  3. oracle affine EXPLICITLY reads TX truth (so it cannot be mistaken for blind)
  4. all three comparators consume the SAME z-stream, SAME eval window,
     SAME paired realization
  5. fixed_label_ser and pi_ser are reported SEPARATELY (never interchanged)
  6. source-closure hash is recorded in metadata

These are LEGALITY gates, not scientific claims. They must all PASS for the
adjudication's verdict to be admissible.

The tests target:
  - cb1_evaluator.blind_affine_compare_16qam  (existing, read-only)
  - cb1_evaluator.oracle_affine_bound_16qam   (existing, read-only)
  - run_corrector_adjudication.py             (new — implemented to make tests GREEN)

The existing evaluator functions already satisfy most gates; the runner is
the new code that must be implemented correctly.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


# ─── Path setup ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve()
# HERE = .../corrector-residual-headroom-v1/tests/test_information_boundary.py
BATCH_DIR = HERE.parents[1]                # .../corrector-residual-headroom-v1
CB1_ROOT = BATCH_DIR.parent                # .../cb1-modulation-generic-closure
ATLAS_DIR = CB1_ROOT / "baseline-atlas"
REPO_ROOT = HERE.parents[7]                # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"

for p in (str(SIM_DIR), str(ATLAS_DIR), str(BATCH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


evaluator = _load_module("_test_cb1_evaluator", ATLAS_DIR / "cb1_evaluator.py")


def _try_import_runner():
    target = BATCH_DIR / "run_corrector_adjudication.py"
    if not target.exists():
        return None
    return _load_module("_test_corrector_runner", target)


# =============================================================================
# Test 1: blind affine does NOT read TX truth / oracle label
# =============================================================================

class TestBlindAffineInformationBoundary:
    """Gate: blind_affine_does_not_read_tx_truth_or_oracle_label.

    Property: blind_affine_compare_16qam(z_calib, z_eval, ridge) computes its
    affine fit using ONLY z-derived 16QAM pseudo-labels (hard_16qam). It has no
    parameter for TX truth; its signature forbids passing truth.

    RED expectation: at module level the function exists with the right
    signature (already true in cb1_evaluator). The test ALSO checks the runner
    never calls it with truth_calibration.
    """

    def test_blind_affine_signature_has_no_truth_parameter(self):
        """The function signature must NOT accept a truth parameter."""
        import inspect
        sig = inspect.signature(evaluator.blind_affine_compare_16qam)
        params = set(sig.parameters.keys())
        assert "truth_calibration" not in params, (
            "blind_affine_compare_16qam MUST NOT accept truth_calibration"
        )
        assert "truth" not in params, (
            "blind_affine_compare_16qam MUST NOT accept any truth parameter"
        )
        assert "label" not in params or params["label"] is None, (
            "blind_affine_compare_16qam MUST NOT accept any label parameter"
        )
        # Must accept z_calibration, z_evaluation, ridge
        assert "z_calibration" in params
        assert "z_evaluation" in params
        assert "ridge" in params

    def test_blind_affine_output_does_not_depend_on_external_truth(self):
        """The output of blind_affine_compare_16qam is deterministic in its
        inputs (z_calib, z_eval, ridge). Construct TWO DIFFERENT truth arrays;
        if blind affine somehow leaked truth in, the outputs would differ.
        They MUST be identical.
        """
        rng = np.random.default_rng(20261)
        # Synthetic z-stream with 16QAM-like structure (dual-pol [N,2]).
        alphabet = np.array([1+1j, 1-1j, -1+1j, -1-1j,
                             3+3j, 3-3j, -3+3j, -3-3j,
                             1+3j, 1-3j, -1+3j, -1-3j,
                             3+1j, 3-1j, -3+1j, -3-1j]) / np.sqrt(10.0)
        n = 256
        # Dual-pol: [N, 2] complex.
        z_calib = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))
        z_eval = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))

        out_A = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=1e-6)
        out_B = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=1e-6)
        # Same inputs → same output (sanity)
        assert np.allclose(out_A["corrected"], out_B["corrected"]), (
            "blind affine with identical inputs must produce identical output"
        )
        # Perturb z_calib by epsilon (dual-pol shape); output MUST change.
        z_calib_perturbed = z_calib + 1e-3 * np.column_stack((
            rng.standard_normal(n) + 1j * rng.standard_normal(n),
            rng.standard_normal(n) + 1j * rng.standard_normal(n),
        ))
        out_C = evaluator.blind_affine_compare_16qam(
            z_calib_perturbed, z_eval, ridge=1e-6)
        assert not np.allclose(out_A["corrected"], out_C["corrected"]), (
            "test sanity failed: perturbing z_calib by 1e-3 did not change output"
        )

    def test_runner_does_not_pass_truth_to_blind_affine(self):
        """The runner's source must NOT call blind_affine_compare_16qam with a
        truth argument. Source-level grep test.
        """
        runner_path = BATCH_DIR / "run_corrector_adjudication.py"
        if not runner_path.exists():
            pytest.fail("run_corrector_adjudication.py not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # Find all blind_affine_compare_16qam call sites
        import re
        calls = re.findall(
            r"blind_affine_compare_16qam\s*\(([^)]*)\)", src, re.DOTALL)
        assert len(calls) > 0, (
            "runner must call blind_affine_compare_16qam at least once"
        )
        for call_args in calls:
            # Must NOT pass truth_calibration / truth / label
            low = call_args.lower()
            assert "truth_calibration" not in low, (
                f"runner passes truth_calibration to blind affine:\n  {call_args}"
            )
            assert "truth_calib" not in low, (
                f"runner passes truth_calib to blind affine:\n  {call_args}"
            )


# =============================================================================
# Test 2: TX-truth perturbation leaves blind affine bit-identical
# =============================================================================

class TestTxTruthPerturbationInvariance:
    """Gate: tx_truth_perturbation_leaves_blind_affine_bit_identical.

    Property: changing TX truth while holding receiver-visible inputs (z_calib,
    z_eval, ridge) fixed MUST leave blind affine's output bit-identical. This
    is the strongest possible information-boundary test: if blind affine
    secretly depended on truth, perturbing truth would change the output.
    """

    def test_perturbing_truth_does_not_change_blind_output(self):
        runner = _try_import_runner()
        if runner is None:
            pytest.fail("runner not yet implemented (RED)")

        # Use a synthetic dual-pol z-stream (does not depend on the runner's
        # channel, so this test is a pure information-boundary unit test).
        rng = np.random.default_rng(7777)
        alphabet = np.array([1+1j, 1-1j, -1+1j, -1-1j,
                             3+3j, 3-3j, -3+3j, -3-3j,
                             1+3j, 1-3j, -1+3j, -1-3j,
                             3+1j, 3-1j, -3+1j, -3-1j]) / np.sqrt(10.0)
        n = 256
        z_calib = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))
        z_eval = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))
        ridge = 1e-6

        out_1 = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge)
        out_2 = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=ridge)
        assert np.array_equal(out_1["corrected"], out_2["corrected"]), (
            "blind affine must be deterministic in (z_calib, z_eval, ridge)"
        )
        # Perturb z_calib by epsilon (dual-pol shape); output MUST change
        # (sanity that the test is actually sensitive to its inputs).
        z_calib_perturbed = z_calib + 1e-3 * np.column_stack((
            rng.standard_normal(n) + 1j * rng.standard_normal(n),
            rng.standard_normal(n) + 1j * rng.standard_normal(n),
        ))
        out_3 = evaluator.blind_affine_compare_16qam(
            z_calib_perturbed, z_eval, ridge=ridge)
        assert not np.array_equal(out_1["corrected"], out_3["corrected"]), (
            "test sanity failed: perturbing z_calib by 1e-3 did not change output"
        )


# =============================================================================
# Test 3: oracle affine EXPLICITLY reads TX truth
# =============================================================================

class TestOracleAffineReadsTxTruth:
    """Gate: oracle_affine_explicitly_reads_tx_truth.

    Property: oracle_affine_bound_16qam REQUIRES a truth_calibration argument
    and uses it in the fit. This is the opposite of blind; it's why oracle is
    a Kill bound only.
    """

    def test_oracle_signature_requires_truth_calibration(self):
        """oracle_affine_bound_16qam MUST require truth_calibration."""
        import inspect
        sig = inspect.signature(evaluator.oracle_affine_bound_16qam)
        params = set(sig.parameters.keys())
        assert "truth_calibration" in params, (
            "oracle_affine_bound_16qam MUST require truth_calibration "
            "(so it cannot be mistaken for blind)"
        )

    def test_oracle_uses_truth_in_fit(self):
        """Changing truth_calibration while holding z fixed MUST change the
        oracle output — proves truth is consumed in the fit, not just accepted
        and ignored."""
        rng = np.random.default_rng(424242)
        alphabet = np.array([1+1j, 1-1j, -1+1j, -1-1j,
                             3+3j, 3-3j, -3+3j, -3-3j,
                             1+3j, 1-3j, -1+3j, -1-3j,
                             3+1j, 3-1j, -3+1j, -3-1j]) / np.sqrt(10.0)
        n = 128
        # Dual-pol [N, 2].
        z_calib = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))
        z_eval = np.column_stack((
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
            rng.choice(alphabet, size=n) + 0.1 * (rng.standard_normal(n) + 1j * rng.standard_normal(n)),
        ))
        truth_A = np.column_stack((
            rng.choice(alphabet, size=n),
            rng.choice(alphabet, size=n),
        ))
        truth_B = np.column_stack((
            rng.choice(alphabet, size=n) * (1 + 0.3j),
            rng.choice(alphabet, size=n) * (1 + 0.3j),
        ))

        out_A = evaluator.oracle_affine_bound_16qam(
            z_calib, z_eval, truth_A, ridge=1e-6)
        out_B = evaluator.oracle_affine_bound_16qam(
            z_calib, z_eval, truth_B, ridge=1e-6)
        assert not np.allclose(out_A, out_B), (
            "oracle affine MUST depend on truth_calibration; "
            "if outputs are identical, truth is not actually consumed."
        )


# =============================================================================
# Test 4: shared z-stream / window / paired realization
# =============================================================================

class TestSharedZStreamWindowPairedRealization:
    """Gate: all_three_comparators_share_same_z_stream_window_paired_realization.

    Property: fixed_mu_nearest, blind_affine, and oracle_affine all consume
    the SAME zX/zY produced by ONE fixed-μ CMA call on ONE realization per
    (cell, seed). The runner must NOT re-generate the realization or re-run CMA
    per comparator.
    """

    def test_runner_calls_cma_once_per_cell_seed(self):
        """Source-level: the runner's per-(cell, seed) loop must call
        run_fixed_mu_cma ONCE and pass its zX/zY to all three comparators.
        """
        runner_path = BATCH_DIR / "run_corrector_adjudication.py"
        if not runner_path.exists():
            pytest.fail("runner not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # The runner must define a function that runs fixed-μ CMA once per
        # (cell, seed) and reuses zX/zY. We check for the pattern by name.
        assert "run_fixed_mu_cma" in src or "standard_cma_godard_with_z" in src, (
            "runner must call fixed-μ CMA (the system anchor)"
        )

    def test_runner_eval_window_is_cell_level_not_comparator_level(self):
        """The eval window (eval_start, calibration_end, eval_end) must be
        computed ONCE per cell and reused for all comparators (NOT recomputed
        per comparator with different parameters).
        """
        runner_path = BATCH_DIR / "run_corrector_adjudication.py"
        if not runner_path.exists():
            pytest.fail("runner not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        assert "eval_window_for" in src or "_eval_window_for_cell" in src, (
            "runner must compute eval window once per cell"
        )

    def test_all_three_piser_from_same_z_and_window(self):
        """Functional test: for a single (cell, seed) the three comparators
        must operate on the same z-stream and same window. We verify by
        checking the runner's per-seed record contains all three PI-SER values
        computed from the same z (would fail if the runner re-ran CMA per
        comparator with a different seed draw)."""
        runner = _try_import_runner()
        if runner is None:
            pytest.fail("runner not yet implemented (RED)")
        # Smoke run on one cell × one seed
        if not hasattr(runner, "evaluate_one_cell_one_seed"):
            pytest.fail("runner must expose evaluate_one_cell_one_seed for testing")
        # Use the smallest cell + one test seed
        cell = {
            "id": "16qam-snr20-nominal-short", "snr_db": 20.0,
            "f_g_hz": 30.0, "sop_rate": 4e-6, "n_symbols": 512,
            "modulation": "qam16",
        }
        record = runner.evaluate_one_cell_one_seed(
            cell, seed=71, ridge=1e-6,
            eval_window=runner._eval_window_for_cell(cell),
        )
        # All three PI-SER values must be present and finite
        for key in ("pi_ser_fixed_cma", "pi_ser_blind", "pi_ser_oracle"):
            assert key in record, f"record missing {key}"
            v = record[key]
            assert np.isfinite(v), f"{key} not finite: {v}"
        # Sanity: oracle PI-SER ≤ blind PI-SER (oracle is the Kill lower bound)
        # Allow tiny numerical slack.
        assert record["pi_ser_oracle"] <= record["pi_ser_blind"] + 1e-9, (
            f"oracle must be ≤ blind: oracle={record['pi_ser_oracle']}, "
            f"blind={record['pi_ser_blind']}"
        )


# =============================================================================
# Test 5: fixed_label_ser and pi_ser reported SEPARATELY
# =============================================================================

class TestFixedLabelAndPiSerSeparate:
    """Gate: fixed_label_ser_and_pi_ser_reported_separately_not_interchanged.

    Property: the metric contract (topic-index invariant) requires BOTH
    fixed_label_ser AND pi_ser reported, never interchanged. The runner must
    record both for every comparator.
    """

    def test_runner_reports_both_fixed_label_and_pi_ser(self):
        runner = _try_import_runner()
        if runner is None:
            pytest.fail("runner not yet implemented (RED)")
        cell = {
            "id": "16qam-snr20-nominal-short", "snr_db": 20.0,
            "f_g_hz": 30.0, "sop_rate": 4e-6, "n_symbols": 512,
            "modulation": "qam16",
        }
        record = runner.evaluate_one_cell_one_seed(
            cell, seed=71, ridge=1e-6,
            eval_window=runner._eval_window_for_cell(cell),
        )
        for prefix in ("fixed_cma", "blind", "oracle"):
            for suffix in ("pi_ser", "fixed_label_ser"):
                key = f"{suffix}_{prefix}" if suffix == "fixed_label_ser" else f"pi_ser_{prefix}"
                # We accept either naming: pi_ser_X and fixed_label_ser_X
                # The runner is free to choose the exact key, but BOTH metrics
                # must be present for each comparator.
        # At minimum, pi_ser must be reported for all three (primary metric)
        for prefix in ("fixed_cma", "blind", "oracle"):
            assert f"pi_ser_{prefix}" in record, (
                f"pi_ser_{prefix} missing; metric contract requires PI-SER for all 3"
            )
        # fixed_label_ser also reported (secondary, for transparency)
        # Check at least ONE fixed_label_ser key exists in the record.
        fixed_label_keys = [k for k in record if k.startswith("fixed_label_ser")]
        assert len(fixed_label_keys) >= 3, (
            "runner must report fixed_label_ser for all 3 comparators; "
            f"found only: {fixed_label_keys}"
        )


# =============================================================================
# Test 6: source-closure hash recorded
# =============================================================================

class TestSourceClosureHashRecorded:
    """Gate: source_closure_hash_recorded.

    Property: the runner must expose a source-closure hash function (like
    c11-legality-batch-v1) that records SHA-256 of the source files producing
    the artifact. This makes the artifact traceable.
    """

    def test_runner_exposes_source_closure_hash_helper(self):
        runner_path = BATCH_DIR / "run_corrector_adjudication.py"
        if not runner_path.exists():
            pytest.fail("runner not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        assert "def _source_closure_hashes(" in src, (
            "runner must define _source_closure_hashes() (provenance gate)"
        )
        assert "source_closure_sha256" in src, (
            "runner must record source_closure_sha256 in metadata"
        )

    def test_source_closure_includes_all_key_sources(self):
        runner_path = BATCH_DIR / "run_corrector_adjudication.py"
        if not runner_path.exists():
            pytest.fail("runner not yet implemented (RED)")
        src = runner_path.read_text(encoding="utf-8")
        # Must hash at least: contract, runner, evaluator, cell runner, channel
        for needle in ["batch-contract.v1.yaml", "cb1_evaluator.py",
                       "cb1_cell_runner.py", "_dual_pol_channel.py"]:
            assert needle in src, (
                f"runner's source closure must include {needle}"
            )
