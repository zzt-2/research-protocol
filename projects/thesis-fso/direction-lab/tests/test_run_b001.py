from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).parents[1] / "tools" / "run_b001.py"
spec = importlib.util.spec_from_file_location("run_b001", MODULE_PATH)
run_b001 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run_b001)


def _contract():
    return {
        "n_symbols": 256,
        "block_size": 64,
        "alpha": 4.2,
        "beta": 1.4,
        "f_g_hz": 30.0,
        "snr_db": 20.0,
        "modulation": "QPSK",
        "cma_mu": 0.001,
        "cma_taps": 11,
        "rates": [4e-6, 1e-5],
        "train_seeds": [11],
        "test_seeds": [41],
    }


def _generator_calls():
    calls = []

    def generator(n, alpha, beta, f_g, rate, seed, block):
        calls.append((n, alpha, beta, f_g, rate, seed, block))
        s = np.ones(n, dtype=complex)
        return {"rX": s, "rY": s, "sX": s, "sY": s, "h": np.ones(n)}

    return calls, generator


def _runner(realization, cfg, variant="baseline", return_blind_trace=True):
    n = len(realization["rX"])
    trace = []
    for block in range(0, n, 64):
        trace.append({"output_start": block, "cm_error": 0.1 + block / n,
                      "output_power": 1.0, "update_norm": 0.01})
    return {"zX": realization["sX"].copy(), "zY": realization["sY"].copy(),
            "valid_mask": np.ones(n, dtype=bool), "blind_trace": trace,
            "diverged": False, "divergence_symbol": None}


def test_paired_cell_generates_once_runs_standard_cma_once_and_excludes_forbidden_features():
    calls, generator = _generator_calls()
    result = run_b001.run_paired_cell(4e-6, 11, _contract(),
                                      realization_generator=generator,
                                      baseline_runner=_runner)
    assert len(calls) == 1
    assert result["baseline_calls"] == 1
    assert result["summary"]["rate"] == 4e-6
    assert result["rows"]
    assert all(not {"h", "theta", "sX", "sY"}.intersection(row["features"])
               for row in result["rows"])
    assert all("fixed_label_ber" in row and "pi_ber" in row for row in result["rows"])


def test_dataset_keeps_train_test_boundary_and_fits_three_mechanisms():
    calls, generator = _generator_calls()
    result = run_b001.run_dataset(_contract(), realization_generator=generator,
                                  baseline_runner=_runner)
    assert len(calls) == 4  # two rates x one train/test seed each
    assert {row["split"] for row in result["rows"]} == {"train", "test"}
    assert set(result["detectors"]) == {"logistic", "mlp", "autoencoder"}
    for detector in result["detectors"].values():
        assert detector["training_splits"] == ["train"]
        assert detector["threshold_source"] == "control-rate-train-scores"


def test_run_governed_accepts_run_receipt_and_never_promotes(tmp_path):
    calls, generator = _generator_calls()
    queue_path = tmp_path / "batch-queue.yaml"
    map_path = tmp_path / "candidate-map.yaml"
    shutil.copy(Path(__file__).parents[1] / "batch-queue.yaml", queue_path)
    shutil.copy(Path(__file__).parents[1] / "candidate-map.yaml", map_path)
    queue_text = queue_path.read_text(encoding="utf-8").replace("status: GATE_PENDING", "status: PASS").replace("  verdict: PENDING", "  verdict: PASS")
    map_text = map_path.read_text(encoding="utf-8").replace("status: GATE_PENDING", "status: PASS").replace("  verdict: PENDING", "  verdict: PASS")
    queue_path.write_text(queue_text, encoding="utf-8")
    map_path.write_text(map_text, encoding="utf-8")
    result = run_b001.run_governed(
        queue_path=queue_path,
        output_dir=tmp_path,
        realization_generator=generator,
        baseline_runner=_runner,
        contract_override=_contract(),
    )
    assert result["gate"]["accepted"] is True
    assert result["manifest"]["promotion_allowed"] is False
    assert result["manifest"]["sandbox_only"] is True
    assert result["manifest"]["component_id"].startswith("component.ml_degradation_detector")
    assert result["manifest"]["candidate_ids"] == ["C24-SL-LINEAR", "C24-SL-MLP", "C24-SSL-AE"]
    assert result["manifest"]["primary_metrics"]
    assert result["manifest"]["family_id"] == "F05"
    assert (tmp_path / "evidence_ledger.jsonl").exists()


def test_run_governed_blocks_pending_queue_or_map_before_override(tmp_path):
    calls, generator = _generator_calls()
    queue_path = tmp_path / "batch-queue.yaml"
    map_path = tmp_path / "candidate-map.yaml"
    shutil.copy(Path(__file__).parents[1] / "batch-queue.yaml", queue_path)
    shutil.copy(Path(__file__).parents[1] / "candidate-map.yaml", map_path)
    queue_path.write_text(queue_path.read_text(encoding="utf-8").replace("status: PASS", "status: GATE_PENDING").replace("  verdict: PASS", "  verdict: PENDING"), encoding="utf-8")
    map_path.write_text(map_path.read_text(encoding="utf-8").replace("status: PASS", "status: GATE_PENDING").replace("  verdict: PASS", "  verdict: PENDING"), encoding="utf-8")
    try:
        run_b001.run_governed(
            queue_path=queue_path,
            output_dir=tmp_path,
            realization_generator=generator,
            baseline_runner=_runner,
            contract_override=_contract(),
        )
    except RuntimeError as exc:
        assert "gate" in str(exc).lower()
    else:
        raise AssertionError("PENDING queue/map gate must block RUN")


def test_default_baseline_adapter_points_to_prompt013_not_batch1():
    runner, _ = run_b001._default_runner(run_b001.DEFAULT_SOURCE_ROOT)
    assert "prompt013_swap_mechanism_q2.py" in runner._source_files[0]
    assert "batch1_fade_methods.py" not in runner._source_files[0]


def test_default_baseline_adapter_emits_online_trace_from_prompt013():
    runner, config_factory = run_b001._default_runner(run_b001.DEFAULT_SOURCE_ROOT)
    n = 256
    cfg = config_factory(mu=0.001, taps=11, r2=1.0, block_size=64,
                         eval_start=0, eval_end=n)
    s = np.ones(n, dtype=complex)
    output = runner({"rX": s, "rY": s}, cfg, variant="baseline", return_blind_trace=True)
    assert output["provenance"]["entry"].startswith("run_cma_diagnostic")
    assert output["blind_trace"]
    assert all({"cm_error", "output_power", "update_norm"}.issubset(row) for row in output["blind_trace"])
