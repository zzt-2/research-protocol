from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import numpy as np
import pytest
import yaml


LAB_ROOT = Path(__file__).parents[1]
MODULE_PATH = LAB_ROOT / "scout" / "P03-U19-residual-headroom" / "z_window_adapter.py"
RUN_B001_PATH = LAB_ROOT / "tools" / "run_b001.py"


def _load(path: Path, name: str):
    assert path.is_file(), f"required component is absent: {path}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _adapter():
    return _load(MODULE_PATH, "direction_lab_p03_z_window_adapter")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _receiver_output(n: int = 4) -> dict:
    z_x = np.asarray([0.7 + 0.7j, -0.7 + 0.7j, -0.7 - 0.7j, 0.7 - 0.7j], dtype=np.complex128)[:n]
    z_y = z_x[::-1].copy()
    return {
        "zX": z_x,
        "zY": z_y,
        "valid_mask": np.ones(n, dtype=bool),
        "blind_trace": [{"output_start": 10, "output_end": 10 + n}],
        "diverged": False,
        "divergence_symbol": None,
        "provenance": {"implementation": "frozen-prompt013", "entry": "run_cma_diagnostic(mode='standard')"},
    }


def _adapt(output: dict, **overrides):
    kwargs = {
        "sequence_id": "p03-cell-001",
        "symbol_start": 10,
        "symbol_end": 10 + len(output["zX"]),
        "equalizer_taps": 11,
        "csi_access_class": "CSI_NONE",
        "source_id": "run_b001._default_runner",
        "source_hash": "a" * 64,
        "receiver_estimated_csi": None,
    }
    kwargs.update(overrides)
    return _adapter().adapt_standard_cma_output(output, **kwargs)


def test_adapter_emits_fixed_json_safe_schema_and_source_pointers() -> None:
    window = _adapt(_receiver_output())
    assert window["schema_version"] == "direction-lab.p03-z-window.v1"
    assert window["sequence_id"] == "p03-cell-001"
    assert window["symbol_range"] == {"start": 10, "end_exclusive": 14}
    assert window["decision_available_at_input_index"] == 19
    assert window["shape"] == [4, 2]
    assert window["dtype"] == "complex128_encoded_float64_pairs"
    assert window["unit"] == "normalized_complex_baseband_symbol"
    assert np.asarray(window["streams"]["zX"]).shape == (4, 2)
    assert np.asarray(window["streams"]["zY"]).shape == (4, 2)
    assert window["valid_mask"] == [True] * 4
    assert window["csi_access"]["class"] == "CSI_NONE"
    assert window["source_pointers"]["streams.zX"]["field"] == "zX"
    assert window["source_pointers"]["symbol_range"]["fields"] == ["output_start", "output_end"]
    assert set(window["source_pointers"]) == {
        "schema_version", "sequence_id", "symbol_range", "decision_available_at_input_index",
        "shape", "dtype", "unit", "streams.zX", "streams.zY", "valid_mask",
        "csi_access", "causal_boundary",
    }


@pytest.mark.parametrize(
    "forbidden",
    [
        "sX", "sY", "bitsX", "bitsY", "tx_bits", "h", "true_h", "theta",
        "true_jones", "oracle_csi", "fixed_label_ber", "pi_ber",
        "permutation_invariant_ber", "post_hoc_ber", "future_window",
    ],
)
def test_adapter_rejects_oracle_tx_posthoc_and_future_fields(forbidden: str) -> None:
    output = _receiver_output()
    output[forbidden] = np.ones(len(output["zX"]))
    with pytest.raises(ValueError, match="forbidden"):
        _adapt(output)


def test_adapter_rejects_nested_forbidden_or_unknown_receiver_fields() -> None:
    output = _receiver_output()
    output["provenance"]["future_window"] = [1.0]
    with pytest.raises(ValueError, match="forbidden"):
        _adapt(output)
    output = _receiver_output()
    output["mystery_state"] = 1
    with pytest.raises(ValueError, match="unsupported receiver output fields"):
        _adapt(output)


def test_csi_none_rejects_any_csi_payload() -> None:
    with pytest.raises(ValueError, match="CSI_NONE"):
        _adapt(_receiver_output(), receiver_estimated_csi={"estimator_id": "dd"})


def test_receiver_estimated_csi_requires_receiver_only_source_and_causal_time() -> None:
    csi = {
        "estimator_id": "decision-directed-affine-v1",
        "source_id": "receiver.past-z-only",
        "source_hash": "b" * 64,
        "available_at_input_index": 19,
        "gain_x": [1.0, 0.0],
        "gain_y": [1.0, 0.0],
        "noise_variance_x": 0.1,
        "noise_variance_y": 0.1,
    }
    window = _adapt(
        _receiver_output(),
        csi_access_class="RECEIVER_ESTIMATED_CSI",
        receiver_estimated_csi=csi,
    )
    assert window["csi_access"]["class"] == "RECEIVER_ESTIMATED_CSI"
    assert window["csi_access"]["estimate"]["estimator_id"] == csi["estimator_id"]
    with pytest.raises(ValueError, match="future"):
        _adapt(
            _receiver_output(),
            csi_access_class="RECEIVER_ESTIMATED_CSI",
            receiver_estimated_csi=dict(csi, available_at_input_index=20),
        )
    with pytest.raises(ValueError, match="oracle"):
        _adapt(
            _receiver_output(),
            csi_access_class="RECEIVER_ESTIMATED_CSI",
            receiver_estimated_csi=dict(csi, source_id="oracle.true-jones"),
        )


def test_adapter_consumes_authentic_deterministic_standard_cma_output() -> None:
    root = LAB_ROOT / "scout" / "P03-U19-residual-headroom"
    recovery = _load(root / "run_source_equivalence.py", "direction_lab_p03_recovery_adapter_test")
    contract = yaml.safe_load((root / "source-equivalence-contract.v1.yaml").read_text(encoding="utf-8"))
    with recovery.materialized_source(contract) as (source_tree, _):
        window, _ = recovery._generate_window(source_tree, contract, "adapter_test")
    assert window["shape"] == [256, 2]
    assert all(window["valid_mask"])
    assert np.isfinite(_adapter().decode_stream(window, "zX")).all()
    assert np.isfinite(_adapter().decode_stream(window, "zY")).all()
