"""Tests for the Pilot-Jones component TEMPORAL SEMANTICS adjudication (T005).

Three test populations:

  PHASE-A-FAILURE-REPRODUCTION: prove the IMMUTABLE T004 implementation exhibits
    the four V039/D065 closure defects (per-block temporal redraw, hash()
    non-determinism, contract N/seed/SHA mismatch, and the fixed-component
    counterfactual that collapses the 0.77-0.99 dB signal). These import the
    IMMUTABLE T004 modules and assert the failure exists; they are NOT allowed to
    make the legacy failure disappear by editing T004 code.

  PHASE-B-SEMANTIC-GATES: prove the T005 fixed-component model satisfies the
    semantic gates (passive PDL, fixed-across-frame, deterministic seed,
    DGD=0 degeneracy, noise untouched, noiseless reference recovery for M0/M2/M3).

  DETERMINISM + CLOSURE: cross-process bit-identical fingerprints (two
    subprocesses with different PYTHONHASHSEED agree for T005, disagree for
    T004), and the contract grid / N / seed pools / SHA closure asserted in code.

The legacy T004 tests (test_pilot_jones_complex_repair.py) are NOT touched.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
SIM = HERE.parent
T005_DIR = SIM / "explore" / "pilot-jones-temporal-adjudication"
sys.path.insert(0, str(SIM))
sys.path.insert(0, str(SIM / "explore" / "pilot-jones-complex-repair"))  # immutable T004


def _load(name, filename):
    """Load a T005 module by file path under a unique module name, so the legacy
    T003 salvage `run_all` (same filename, immutable) keeps its import priority
    when the T004 test file does a bare `import run_all` in the same pytest
    session. We never insert the T005 dir onto sys.path globally."""
    import importlib.util
    modname = f"t005_{name}"
    if modname in sys.modules:
        return sys.modules[modname]
    spec = importlib.util.spec_from_file_location(modname, T005_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    # the T005 modules import each other by bare name (e.g. `import temporal_channel`);
    # register them under those names too, but ONLY for the duration we need.
    # To keep the salvage `run_all` intact, we do NOT register t005 run_all as
    # `run_all`.
    spec.loader.exec_module(mod)
    return mod


# Pre-load T005 modules under their bare names too, but ONLY the ones that do
# not collide with T003/T004 module names. run_all collides -> loaded via
# _load_run_all() in the closure tests. This is done in a try/except so that if
# a later legacy test removed them we still work.
def _bootstrap_t005():
    import importlib.util
    for name, fn in (("temporal_channel", "temporal_channel.py"),
                     ("baselines_and_oracle", "baselines_and_oracle.py"),
                     ("run_probe", "run_probe.py")):
        if name in sys.modules:
            continue
        # only register if NOT already a legacy module (defensive)
        spec = importlib.util.spec_from_file_location(name, T005_DIR / fn)
        if spec is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:
            sys.modules.pop(name, None)
            raise


_bootstrap_t005()
import run_probe                                       # noqa: E402
import temporal_channel as tc                          # noqa: E402
import baselines_and_oracle as bao                     # noqa: E402


def _load_run_all():
    """Load the T005 run_all by file path (collides with salvage run_all)."""
    return _load("run_all", "run_all.py")


# ===========================================================================
# PHASE A: V039/D065 failure reproduction (T004 immutable)
# ===========================================================================

def test_t004_blockwise_redraw_reproduced():
    """T004 build_jones_truth redraws U/V every 64 symbols (25.6 ns jumps)."""
    r = run_probe.repro_t004_blockwise_redraw()
    assert r["reproduced"], "T004 per-block redraw NOT reproduced"
    assert r["block_duration_ns"] == 25.6
    assert not r["all_blocks_identical"]


def test_t004_hash_nondeterminism_source_reproduced():
    """T004 seed formula uses built-in hash(model_id) (source-level)."""
    r = run_probe.repro_t004_hash_nondeterminism_local()
    assert r["reproduced"], "T004 hash(model_id) use NOT reproduced"
    assert r["uses_hash_model_id"] is True
    assert "hash(model_id)" in r["seed_formula_snippet"]


def test_t004_contract_closure_reproduced():
    """T004 contract N/seeds/SHA do not match the runner/raw."""
    r = run_probe.repro_t004_contract_closure()
    assert r["reproduced"], "T004 contract closure defect NOT reproduced"
    assert r["contract_N"] == 50000 and r["runner_N"] == 20000
    assert r["contract_test_seeds_count"] == 10
    assert r["runner_test_seeds_count"] == 8
    assert r["is_real_sha256"] is False


def test_fixed_counterfactual_reproduced():
    """V039 fixed-component counterfactual: impairment-added headroom << 0.5 dB."""
    r = run_probe.repro_fixed_counterfactual(seeds=(7500, 7501, 7502, 7503, 7504))
    assert r["reproduced"], "fixed-component counterfactual NOT reproduced"
    assert r["mean_impairment_added_over_M0_dB"] < 0.5
    assert r["t004_iid_block_headroom_dB_reported"] == 0.77


# ===========================================================================
# PHASE B: T005 fixed-component semantic gates
# ===========================================================================

def test_passive_pdl():
    g = run_probe.semantic_passive_pdl()
    assert g["pass"]
    assert np.isclose(g["sigma_max"], 1.0)


def test_fixed_component_across_frame():
    g = run_probe.semantic_fixed_component_across_frame(seed=7500)
    assert g["pass"]
    assert g["is_single_fixed_matrix"]


def test_deterministic_seed_in_process():
    g = run_probe.semantic_deterministic_seed_in_process()
    assert g["pass"]
    assert g["reproducible"]


def test_dgd0_degeneracy():
    g = run_probe.semantic_dgd0_degeneracy(seed=7500)
    assert g["pass"]
    assert g["max_abs_diff_clean_vs_component"] < 1e-10


def test_noise_untouched():
    g = run_probe.semantic_noise_untouched(seed=7500)
    assert g["pass"]
    assert g["max_abs_diff"] < 1e-10


def test_reference_recovery_m0_noiseless():
    g = run_probe.semantic_reference_recovery_m0(seed=7500)
    assert g["pass"]
    assert g["mean_abs_recovery_err_M0_noiseless"] < 1e-9


def test_reference_recovery_m2_m3_noiseless():
    """Reference is a LEGAL ceiling for M2 (rotation-then-component) and M3."""
    g = run_probe.semantic_reference_recovery_m2_m3(seed=7500)
    assert g["pass"]
    assert g["M2"]["mean_abs_recovery_err_noiseless"] < 1e-9
    assert g["M3"]["mean_abs_recovery_err_noiseless"] < 1e-4  # MMSE reg at g=1e6


def test_reference_forward_ordering_m2():
    """M2 reference must match the TRUE forward ordering
    (clean_atm = sqrt(h) R(theta) s; r = J @ clean_atm). A wrong ordering
    (sqrt(h) R(theta) J s) must NOT recover the symbols noiselessly."""
    real = run_probe._canonical(2000, 7500, alpha=2.0, beta=1.0, gamma_bar=50.0)
    ri = tc.build_impaired_realization(real, model_id="M2", block_size=64,
                                       seed=7500, pdl_db=1.0, dgd_ps=0.0, t_s=4e-10)
    ri["rX"] = np.asarray(ri["clean_component"])[0].copy()
    ri["rY"] = np.asarray(ri["clean_component"])[1].copy()
    pilot = bao.inject_pre_channel_pilots(real, ri, block_size=64, n_pilots=6)
    ri_nl = dict(ri)
    ri_nl["rX"] = np.asarray(pilot["clean_pilot_component"])[0].copy()
    ri_nl["rY"] = np.asarray(pilot["clean_pilot_component"])[1].copy()
    pilot_nl = dict(pilot)
    pilot_nl["rX"] = ri_nl["rX"].copy()
    pilot_nl["rY"] = ri_nl["rY"].copy()
    ref = bao.reference_m0_m2(ri_nl, pilot_nl, block_size=64, gamma_bar=1e6)
    em = pilot["eval_mask"]
    err = float(np.mean(np.abs(ref["rX"][em] - real["sX"][em]))
                + np.mean(np.abs(ref["rY"][em] - real["sY"][em])))
    assert err < 1e-9, "M2 reference ordering broken (not a legal ceiling)"


# ===========================================================================
# DETERMINISM: cross-process bit-identical fingerprints
# ===========================================================================

def _run_crossproc(which, env_hashseed):
    env = {**__import__("os").environ, "PYTHONHASHSEED": env_hashseed}
    py = sys.executable
    helper = (SIM / "explore" / "pilot-jones-temporal-adjudication"
              / "_crossproc_fingerprint.py")
    out = subprocess.run([py, str(helper), which, "7500", "M2", "1.0"],
                         capture_output=True, text=True, env=env,
                         cwd=str(SIM.parent.parent))
    assert out.returncode == 0, f"subprocess failed: {out.stderr}"
    return json.loads(out.stdout.splitlines()[-1])


def test_t004_crossprocess_disagrees():
    """T004: two subprocesses with DIFFERENT PYTHONHASHSEED -> DIFFERENT
    fingerprints (hash(model_id) non-determinism reproduced)."""
    a = _run_crossproc("t004", "0")
    b = _run_crossproc("t004", "12345")
    assert a["fingerprint"] != b["fingerprint"], \
        "T004 fingerprints agreed across PYTHONHASHSEED (non-determinism NOT reproduced)"
    assert a["hash_model_id"] != b["hash_model_id"]


def test_t005_crossprocess_agrees():
    """T005: two subprocesses with DIFFERENT PYTHONHASHSEED -> IDENTICAL
    fingerprints (deterministic seed proven)."""
    a = _run_crossproc("t005", "0")
    b = _run_crossproc("t005", "99999")
    assert a["fingerprint"] == b["fingerprint"], \
        "T005 fingerprints disagreed across PYTHONHASHSEED (determinism FAILED)"
    assert a["component_seed"] == b["component_seed"] == 1232502


# ===========================================================================
# CLOSURE: contract grid / N / seed pools / SHA asserted in code
# ===========================================================================

def test_contract_runner_closure():
    """The frozen contract grid must match the runner (V039 closure fix)."""
    run_all = _load_run_all()
    run_all._assert_closure()   # raises AssertionError on any mismatch


def test_real_contract_sha():
    """result.json contract_sha256 must be a real 64-hex SHA256, not a filename."""
    rj = json.loads((SIM / "results" / "pilot-jones-temporal-adjudication"
                     / "result.json").read_text())
    csha = rj["contract_sha256"]
    assert isinstance(csha, str) and len(csha) == 64
    assert all(ch in "0123456789abcdef" for ch in csha)
    # must equal the actual file hash
    run_all = _load_run_all()
    assert csha == run_all.contract_sha()


def test_seeds_disjoint_from_t002_t003_t004():
    """T005 seed pools must be disjoint from T002/T003/T004 observed seeds."""
    run_all = _load_run_all()
    import yaml
    with open(SIM / "explore" / "pilot-jones-temporal-adjudication"
              / "contract.yaml") as f:
        c = yaml.safe_load(f)
    excl = set(c["seed_plan"]["excluded"])
    assert set(run_all.VAL_SEEDS).isdisjoint(excl)
    assert set(run_all.TEST_SEEDS).isdisjoint(excl)
    assert set(run_all.VAL_SEEDS).isdisjoint(set(run_all.TEST_SEEDS))
