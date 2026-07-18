from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


LAB_ROOT = Path(__file__).parents[1]
SCOUT_ROOT = LAB_ROOT / "scout" / "P03-U19-residual-headroom"


def _load(path: Path, name: str):
    assert path.is_file(), f"required component is absent: {path}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _modules():
    adapter = _load(SCOUT_ROOT / "z_window_adapter.py", "p03_adapter_for_comparator_test")
    comparator = _load(SCOUT_ROOT / "analytic_comparator.py", "p03_analytic_comparator_test")
    return adapter, comparator


def _window(z_x: np.ndarray, z_y: np.ndarray, *, csi_class: str = "CSI_NONE") -> dict:
    adapter, _ = _modules()
    n = len(z_x)
    output = {
        "zX": np.asarray(z_x, dtype=np.complex128),
        "zY": np.asarray(z_y, dtype=np.complex128),
        "valid_mask": np.ones(n, dtype=bool),
        "blind_trace": [{"output_start": 20, "output_end": 20 + n}],
        "diverged": False,
        "divergence_symbol": None,
        "provenance": {"implementation": "test-standard-cma"},
    }
    csi = None
    if csi_class == "RECEIVER_ESTIMATED_CSI":
        csi = {
            "estimator_id": "receiver-past-z-v1",
            "source_id": "receiver.past-z-only",
            "source_hash": "b" * 64,
            "available_at_input_index": 20 + n + 5,
            "gain_x": [1.0, 0.0],
            "gain_y": [1.0, 0.0],
            "noise_variance_x": 0.1,
            "noise_variance_y": 0.1,
        }
    return adapter.adapt_standard_cma_output(
        output,
        sequence_id="comparator-test",
        symbol_start=20,
        symbol_end=20 + n,
        equalizer_taps=11,
        csi_access_class=csi_class,
        source_id="standard-cma-test-seam",
        source_hash="a" * 64,
        receiver_estimated_csi=csi,
    )


def test_csi_none_qpsk_comparator_has_aligned_finite_deterministic_output() -> None:
    _, comparator = _modules()
    z_x = np.asarray([0.8 + 0.6j, -0.9 + 0.5j, -0.6 - 0.8j, 0.6 - 0.9j])
    z_y = z_x[::-1]
    window = _window(z_x, z_y)
    kwargs = {"constellation_amplitude": 1.0 / np.sqrt(2.0)}
    first = comparator.compare_qpsk_csi_none(window, **kwargs)
    second = comparator.compare_qpsk_csi_none(window, **kwargs)
    assert first == second
    assert first["schema_version"] == "direction-lab.p03-analytic-comparator.v1"
    assert first["comparator_id"] == "analytic.qpsk-nearest.csi-none.v1"
    assert first["csi_access_class"] == "CSI_NONE"
    assert first["symbol_range"] == window["symbol_range"]
    assert first["shape"] == [4, 2]
    for stream in ("zX", "zY"):
        predicted = np.asarray(first["predicted_mean"][stream])
        distance = np.asarray(first["squared_distance"][stream])
        assert predicted.shape == (4, 2)
        assert distance.shape == (4,)
        assert np.isfinite(predicted).all()
        assert np.isfinite(distance).all()
        assert (distance >= 0).all()


def test_zero_tie_rule_is_explicit_positive_qpsk_corner() -> None:
    _, comparator = _modules()
    window = _window(np.asarray([0.0 + 0.0j]), np.asarray([0.0 + 0.0j]))
    amplitude = 1.0 / np.sqrt(2.0)
    result = comparator.compare_qpsk_csi_none(window, constellation_amplitude=amplitude)
    assert result["predicted_mean"]["zX"] == [[amplitude, amplitude]]
    assert result["tie_rule"] == "real_or_imag_equal_to_zero_maps_to_positive_amplitude"


def test_distance_is_monotone_when_samples_move_toward_same_decision() -> None:
    _, comparator = _modules()
    amplitude = 1.0 / np.sqrt(2.0)
    far = _window(np.asarray([0.1 + 0.1j]), np.asarray([0.2 + 0.2j]))
    close = _window(np.asarray([0.6 + 0.6j]), np.asarray([0.65 + 0.65j]))
    far_result = comparator.compare_qpsk_csi_none(far, constellation_amplitude=amplitude)
    close_result = comparator.compare_qpsk_csi_none(close, constellation_amplitude=amplitude)
    assert close_result["aggregate_mean_squared_distance"] < far_result["aggregate_mean_squared_distance"]


def test_comparator_fails_closed_for_unbound_estimated_csi_and_bad_amplitude() -> None:
    _, comparator = _modules()
    estimated = _window(np.asarray([1 + 1j]), np.asarray([1 + 1j]), csi_class="RECEIVER_ESTIMATED_CSI")
    with pytest.raises(ValueError, match="declared but not bound"):
        comparator.compare_qpsk_csi_none(estimated, constellation_amplitude=1 / np.sqrt(2))
    plain = _window(np.asarray([1 + 1j]), np.asarray([1 + 1j]))
    with pytest.raises(ValueError, match="amplitude"):
        comparator.compare_qpsk_csi_none(plain, constellation_amplitude=0.0)


def test_comparator_has_no_hidden_constellation_default_or_evaluation_fields() -> None:
    _, comparator = _modules()
    window = _window(np.asarray([1 + 1j]), np.asarray([1 + 1j]))
    with pytest.raises(TypeError):
        comparator.compare_qpsk_csi_none(window)
    result = comparator.compare_qpsk_csi_none(window, constellation_amplitude=1 / np.sqrt(2))
    serialized = repr(result).lower()
    for forbidden in ("tx_bits", "true_h", "true_jones", "fixed_label_ber", "pi_ber", "oracle"):
        assert forbidden not in serialized
    assert result["complexity"]["distance_evaluations_per_dual_pol_symbol"] == 8
    assert result["receiver_state_changed"] is False
