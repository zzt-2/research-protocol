import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "explore" / "cma-fade-divergence" / "vae_vs_cma_blind.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("vae_vs_cma_blind", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metric(pi):
    return {
        "fixed_label_ber": {"mean": pi + 0.1},
        "permutation_invariant_ber": {"mean": pi},
        "abs_corr": {},
        "abs_corr_zX_zY": 0.0,
        "classification": "normal",
        "diverged": False,
    }


def test_run_cell_uses_one_shared_realization_and_blind_vq(monkeypatch):
    m = load_module()
    n = 10_240
    shared = {
        key: np.arange(n, dtype=np.float64).astype(np.complex128) + offset
        for offset, key in enumerate(("rX", "rY", "sX", "sY"))
    }
    shared.update(h=np.ones(n), theta=np.zeros(n))
    calls = {"channel": 0, "eval": 0}

    def channel(*args, **kwargs):
        calls["channel"] += 1
        return shared

    class FakeCMA:
        def __init__(self, **kwargs):
            pass

        def equalize(self, x, y, block_size=64):
            assert x is shared["rX"] and y is shared["rY"]
            assert block_size == 64
            return {"zX": x, "zY": y, "diverged": False,
                    "diverge_idx": None, "final_w_norm": 1.0,
                    "init_w_norm": 1.0}

    class FakeVQ:
        def __init__(self, **kwargs):
            pass

        def fit(self, x, y, n_iterations, verbose=False):
            # This interface cannot receive transmitted symbols/bits/labels.
            assert np.shares_memory(x, shared["rX"])
            assert np.shares_memory(y, shared["rY"])
            assert len(x) == n // 2
            return {"total_loss": [2.0, 1.0], "usage": 1.0, "finite": True}

        def equalize(self, x, y, chunk_size):
            assert x is shared["rX"] and y is shared["rY"]
            return {"zX": x, "zY": y}

    def ml(x, y, sx, sy, ml_params=None):
        assert x is shared["rX"] and y is shared["rY"]
        assert sx is shared["sX"] and sy is shared["sY"]
        return x, y, n // 2, {"diverged": False}

    def oracle(x, y, h, theta, gamma_bar):
        assert x is shared["rX"] and y is shared["rY"]
        return x, y

    def evaluate(zx, zy, sx, sy, diverged):
        calls["eval"] += 1
        assert len(zx) == len(sx) == n // 2
        return metric(0.1)

    monkeypatch.setattr(m, "generate_shared_realization_dp", channel)
    monkeypatch.setattr(m, "CMAEqualizer2x2", FakeCMA)
    monkeypatch.setattr(m, "VQVAEEqualizer2x2", FakeVQ)
    monkeypatch.setattr(m, "run_ml_trial", ml)
    monkeypatch.setattr(m, "oracle_equalize", oracle)
    monkeypatch.setattr(m, "evaluate_outputs", evaluate)

    trial = m.run_cell(30.0, 1000, n_symbols=n, device="cpu", updates=2)
    assert calls == {"channel": 1, "eval": 5}
    assert set(trial["methods"]) == {"raw_naive", "cma", "vqvae", "ml", "oracle"}
    assert trial["vqvae"]["updates"] == 2
    assert trial["vqvae"]["sanity"]["all"] is True


def test_checkpoint_validation_rejects_signature_or_sha_mismatch():
    m = load_module()
    checkpoint = {"experiment_signature": {"N": 1}, "script_sha256": "abc"}
    m.validate_checkpoint(checkpoint, {"N": 1}, "abc")
    with pytest.raises(ValueError, match="signature"):
        m.validate_checkpoint(checkpoint, {"N": 2}, "abc")
    with pytest.raises(ValueError, match="SHA"):
        m.validate_checkpoint(checkpoint, {"N": 1}, "def")


def test_composite_sha_covers_every_component(tmp_path):
    m = load_module()
    paths = []
    for i, name in enumerate((
        "script", "vae", "channel", "evaluation", "cma", "ml", "ml_driver"
    )):
        path = tmp_path / f"{name}.py"
        path.write_text(str(i), encoding="utf-8")
        paths.append(path)
    for path in paths:
        before = m.composite_sha256(paths)
        original = path.read_text(encoding="utf-8")
        path.write_text(original + "changed", encoding="utf-8")
        assert m.composite_sha256(paths) != before
        path.write_text(original, encoding="utf-8")


def complete_trials(m):
    trials = []
    for f_g in m.DEFAULT_F_G:
        for seed in m.DEFAULT_SEEDS:
            trials.append({
                "f_G": f_g, "seed": seed,
                "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
                "vqvae": {"sanity": {"all": True}},
            })
    return trials


def test_gate_is_incomplete_until_exact_30_cells_exist():
    m = load_module()
    one = {"f_G": 30.0, "seed": 1000,
           "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
           "vqvae": {"sanity": {"all": True}}}
    assert m.summarize_and_gate([one])["status"] == "INCOMPLETE"

    trials = complete_trials(m)
    result = m.summarize_and_gate(trials)
    assert result["status"] == "PASS"
    assert all(row["paired_wins"] == 10 for row in result["by_f_G"].values())


def test_gate_rejects_duplicate_extra_and_failed_sanity_cells():
    m = load_module()
    trials = complete_trials(m)
    duplicate = trials + [trials[0]]
    assert m.summarize_and_gate(duplicate)["status"] == "INVALID"

    extra = trials + [{
        "f_G": 999.0, "seed": 9999,
        "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
        "vqvae": {"sanity": {"all": True}},
    }]
    assert m.summarize_and_gate(extra)["status"] == "INVALID"

    failed = complete_trials(m)
    failed[3]["vqvae"]["sanity"]["all"] = False
    result = m.summarize_and_gate(failed)
    assert result["status"] == "INVALID"
    assert result["failed_sanity_cells"] == [[30.0, 1003]]


def test_parameters_capture_implicit_runtime_choices():
    m = load_module()
    assert [path.name for path in m._component_paths()] == [
        "vae_vs_cma_blind.py", "_vae_equalizer.py", "_dual_pol_channel.py",
        "prompt012_longseq_audit.py", "_cma.py", "_ml_equalizer.py",
        "ml_long_seq_failure.py",
    ]
    params = m._parameters(m.DEFAULT_F_G, m.DEFAULT_SEEDS, 10_000, "cpu", None, 128, 4096)
    assert params["dp_method"] == m.SimulationConfig().gg_time.AR1_METHOD
    assert params["cma"]["block_size"] == 64
    assert params["supervised_ml"]["val_split"] == 0.2


def test_run_checkpoints_each_cell_with_save_results(monkeypatch, tmp_path):
    m = load_module()
    saved = []
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: {
        "f_G": f_g, "seed": seed,
        "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
    })
    monkeypatch.setattr(m, "save_results", lambda payload, path, script: saved.append(
        (len(payload["trials"]), Path(path), script)
    ))
    output = tmp_path / "result.json"
    payload = m.run(f_g_values=[30.0], seeds=[1000, 1001], n_symbols=10_240,
                    device="cpu", output=output, resume=False, updates=1)
    assert [item[0] for item in saved] == [1, 2]
    assert payload["gate"]["status"] == "INCOMPLETE"


def test_max_cells_batches_pending_work_without_changing_signature(monkeypatch, tmp_path):
    m = load_module()
    saves = []
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: {
        "f_G": f_g, "seed": seed,
        "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
        "vqvae": {"sanity": {"all": True}},
    })

    def persist(payload, path, script):
        saves.append(len(payload["trials"]))
        Path(path).write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(m, "save_results", persist)
    output = tmp_path / "resume.json"
    first = m.run(n_symbols=10_240, device="cpu", output=output, updates=1,
                  resume=True, max_cells=1)
    second = m.run(n_symbols=10_240, device="cpu", output=output, updates=1,
                   resume=True, max_cells=1)
    assert len(first["trials"]) == 1
    assert len(second["trials"]) == 2
    assert first["experiment_signature"] == second["experiment_signature"]
    assert len(second["parameters"]["requested_cells"]) == 30
    assert "max_cells" not in second["parameters"]
    assert saves == [1, 2]


def _fake_trial(f_g, seed):
    return {
        "f_G": f_g, "seed": seed,
        "methods": {"vqvae": metric(0.1), "cma": metric(0.2)},
        "vqvae": {"sanity": {"all": True}},
    }


def test_cell_indices_create_disjoint_checkpoints_with_identical_signature(
        monkeypatch, tmp_path):
    m = load_module()
    executed = []
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: (
        executed.append((f_g, seed)) or _fake_trial(f_g, seed)
    ))

    def persist(payload, path, script):
        Path(path).write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(m, "save_results", persist)
    groups = [list(range(0, 10)), list(range(10, 20)), list(range(20, 30))]
    payloads = []
    for group_no, indices in enumerate(groups):
        payloads.append(m.run(
            n_symbols=10_240, device="cpu", updates=1, resume=False,
            output=tmp_path / f"part{group_no}.json", cell_indices=indices,
        ))
    assert all(
        payload["experiment_signature"] == payloads[0]["experiment_signature"]
        for payload in payloads
    )
    requested = [tuple(x) for x in payloads[0]["parameters"]["requested_cells"]]
    assert executed == [requested[i] for group in groups for i in group]
    assert [len(payload["trials"]) for payload in payloads] == [10, 10, 10]
    assert "cell_indices" not in payloads[0]["parameters"]


def test_cell_indices_then_resume_filter_then_max_cells(monkeypatch, tmp_path):
    m = load_module()
    executed = []
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: (
        executed.append((f_g, seed)) or _fake_trial(f_g, seed)
    ))
    monkeypatch.setattr(m, "save_results", lambda payload, path, script:
                        Path(path).write_text(json.dumps(payload), encoding="utf-8"))
    output = tmp_path / "ordered-resume.json"
    first = m.run(n_symbols=10_240, device="cpu", updates=1, output=output,
                  cell_indices=[2, 0], max_cells=1)
    second = m.run(n_symbols=10_240, device="cpu", updates=1, output=output,
                   cell_indices=[2, 0, 1], max_cells=1)
    grid = [tuple(cell) for cell in first["parameters"]["requested_cells"]]
    assert executed == [grid[2], grid[0]]
    assert len(second["trials"]) == 2


@pytest.mark.parametrize("indices", [[-1], [30], [0, 0], [True]])
def test_cell_indices_reject_invalid_selection(indices, tmp_path):
    m = load_module()
    with pytest.raises(ValueError, match="cell_indices"):
        m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
              output=tmp_path / "x.json", cell_indices=indices)


def test_merge_three_disjoint_checkpoints_to_complete_pass(monkeypatch, tmp_path):
    m = load_module()
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: _fake_trial(f_g, seed))
    saves = []

    def persist(payload, path, script):
        saves.append((Path(path), script, len(payload["trials"])))
        Path(path).write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(m, "save_results", persist)
    inputs = []
    for group_no, indices in enumerate((range(0, 10), range(10, 20), range(20, 30))):
        path = tmp_path / f"merge-part{group_no}.json"
        inputs.append(path)
        m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
              output=path, cell_indices=list(indices))
    output = tmp_path / "merged.json"
    merged = m.merge_checkpoints(inputs, output)
    assert len(merged["trials"]) == 30
    assert merged["gate"]["status"] == "PASS"
    assert saves[-1] == (output, "vae_vs_cma_blind_merge", 30)


@pytest.mark.parametrize("mutation", ["duplicate", "signature", "sha"])
def test_merge_rejects_duplicate_or_contract_mismatch(monkeypatch, tmp_path, mutation):
    m = load_module()
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: _fake_trial(f_g, seed))
    monkeypatch.setattr(m, "save_results", lambda payload, path, script:
                        Path(path).write_text(json.dumps(payload), encoding="utf-8"))
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
          output=first, cell_indices=[0])
    m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
          output=second, cell_indices=[1])
    data = json.loads(second.read_text(encoding="utf-8"))
    if mutation == "duplicate":
        data["trials"] = json.loads(first.read_text(encoding="utf-8"))["trials"]
    elif mutation == "signature":
        data["experiment_signature"]["parameters"]["N"] += 1
    else:
        data["script_sha256"] = "bad"
    second.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate|signature|SHA"):
        m.merge_checkpoints([first, second], tmp_path / "merged.json")


@pytest.mark.parametrize("mutation", ["parameters", "sha"])
def test_merge_rejects_checkpoint_internal_contract_mismatch(
        monkeypatch, tmp_path, mutation):
    m = load_module()
    monkeypatch.setattr(m, "run_cell", lambda f_g, seed, **kwargs: _fake_trial(f_g, seed))
    monkeypatch.setattr(m, "save_results", lambda payload, path, script:
                        Path(path).write_text(json.dumps(payload), encoding="utf-8"))
    checkpoint = tmp_path / "internal.json"
    m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
          output=checkpoint, cell_indices=[0])
    data = json.loads(checkpoint.read_text(encoding="utf-8"))
    if mutation == "parameters":
        data["parameters"]["N"] += 1
    else:
        data["script_sha256"] = "internally-wrong"
    checkpoint.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="internal contract"):
        m.merge_checkpoints([checkpoint], tmp_path / "merged.json")


@pytest.mark.parametrize("axes", [
    {"f_g_values": [30.0, 30.0]},
    {"seeds": [1000, 1000]},
])
def test_run_rejects_duplicate_grid_axes(axes, tmp_path):
    m = load_module()
    with pytest.raises(ValueError, match="duplicate"):
        m.run(n_symbols=10_240, device="cpu", updates=1, resume=False,
              output=tmp_path / "duplicate-axis.json", **axes)


@pytest.mark.parametrize("kwargs", [
    {"n_symbols": 10239}, {"batch_size": 0}, {"chunk_size": -1},
    {"updates": 0}, {"max_cells": 0},
])
def test_runtime_integer_validation(kwargs, tmp_path):
    m = load_module()
    base = dict(n_symbols=10_240, device="cpu", output=tmp_path / "x.json",
                updates=1, resume=False)
    base.update(kwargs)
    with pytest.raises(ValueError, match="positive|at least"):
        m.run(**base)
