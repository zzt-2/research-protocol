from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
import sys

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = SIMULATION_ROOT / "explore" / "ch5-apsk-llr-calibration"
TARGET_MODULE = TARGET_ROOT / "correctness.py"
CODEC_METRICS = (
    SIMULATION_ROOT
    / "explore"
    / "ch5-apsk-structured-covariance"
    / "codec_metrics.py"
)

if str(SIMULATION_ROOT) not in sys.path:
    sys.path.insert(0, str(SIMULATION_ROOT))


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _target():
    return _load(TARGET_MODULE, "_t076_correctness")


def _codec_metrics():
    return _load(CODEC_METRICS, "_t076_codec_metrics_test")


def test_c0_joint_fingerprint_mapper_sign_and_noise_factor():
    target = _target()
    metrics = _codec_metrics()
    from common._modulation import m16apsk_mod

    symbols, bits = target.apsk16_table()
    expected_symbols, expected_bits = metrics.apsk16_table()
    np.testing.assert_array_equal(symbols, expected_symbols)
    np.testing.assert_array_equal(bits, expected_bits)
    assert target.apsk16_identity().table_sha256 == metrics.apsk16_identity().table_sha256
    np.testing.assert_array_equal(m16apsk_mod(bits.reshape(-1)), symbols)

    n0 = 1e-4
    llr = target.exact_app_llr(symbols, complex_noise_power=n0, clip=None)
    np.testing.assert_array_equal(llr > 0.0, bits.astype(bool))
    assert target.per_real_covariance(0.04) == pytest.approx(0.02, abs=0.0)

    origin = target.exact_app_llr(
        np.array([0.0 + 0.0j]), complex_noise_power=0.04, clip=None
    )[0]
    r1_sq = 2.0 / (1.0 + 2.57**2)
    r2_sq = 2.57**2 * r1_sq
    expected_ring = -(r2_sq - r1_sq) / 0.04
    wrong_n0_over_2_factor = -(r2_sq - r1_sq) / 0.02
    assert origin[0] == pytest.approx(expected_ring, abs=1e-12)
    np.testing.assert_allclose(origin[1:], 0.0, rtol=0.0, atol=1e-12)
    assert origin[0] != pytest.approx(wrong_n0_over_2_factor, abs=1e-12)


def test_c1_unclipped_maxlog_b2_equals_b3_float64():
    target = _target()
    symbols, _ = target.apsk16_table()
    grid = np.concatenate(
        (
            symbols,
            np.array(
                [
                    0.0 + 0.0j,
                    0.8 + 0.0j,
                    -0.3 + 0.6j,
                    0.41 - 0.27j,
                    -1.2 - 0.15j,
                ],
                dtype=np.complex128,
            ),
        )
    )
    for nominal_n0, estimated_n0 in ((0.04, 0.02), (0.07, 0.11), (0.2, 0.05)):
        b0 = target.maxlog_llr(grid, complex_noise_power=nominal_n0, clip=None)
        b2 = (nominal_n0 / estimated_n0) * b0
        b3 = target.maxlog_llr(grid, complex_noise_power=estimated_n0, clip=None)
        assert np.max(np.abs(b2 - b3)) <= 1e-12


def test_c2_exact_app_origin_control_and_per_bit_nonidentity():
    target = _target()
    receipt = target.exact_app_identity_receipt()
    assert receipt["origin_max_abs"] <= 1e-12
    assert receipt["variance_pairs"] >= 3
    assert receipt["sample_classes"] == (
        "constellation",
        "origin",
        "ring_midpoint",
        "axis",
        "off_axis",
    )
    assert set(receipt["bit_status"]) == {0, 1, 2, 3}
    assert any(value == "NONIDENTITY" for value in receipt["bit_status"].values())
    for value in receipt["bit_max_abs"].values():
        assert np.isfinite(value)


def test_c3_minimal_nms_is_messagewise_positive_homogeneous():
    target = _target()
    base = target.minimal_nms_trace(np.array([1.25, -0.8, 0.45, -1.7]))
    for scale in (0.25, 0.5, 2.0, 4.0):
        scaled = target.minimal_nms_trace(
            scale * np.array([1.25, -0.8, 0.45, -1.7])
        )
        for left, right in zip(base["messages"], scaled["messages"], strict=True):
            np.testing.assert_allclose(right, scale * left, rtol=0.0, atol=1e-12)
        np.testing.assert_array_equal(scaled["hard"], base["hard"])


def test_c3_target_placement_and_fixed_boundaries_are_nonhomogeneous():
    target = _target()
    receipt = target.target_nonlinearity_receipt()
    assert receipt["placement"] == (
        "apsk_demapper_clip30 -> b2_scale -> decode_fresh_clip30 -> "
        "backend_input_clip20 -> decoder_out_int_inv -> "
        "rate_recovery_fixed_bit0_filler_minus20 -> bp_internal_clip20"
    )
    assert receipt["s_lt_1_checked"] is True
    assert receipt["s_ge_1_checked"] is True
    assert receipt["input_clip_breaks_homogeneity"] is True
    assert receipt["fixed_filler_breaks_homogeneity"] is True
    assert receipt["alpha_075_is_homogeneous"] is True
    assert receipt["interleaver_is_homogeneous"] is True
    assert receipt["punctured_zero_is_homogeneous"] is True
    assert receipt["fixed_iterations_are_homogeneous"] is True


def _frame_inputs(target):
    symbols, _ = target.apsk16_table()
    pilots = np.tile(symbols[:8], (2, 1))
    residual = np.array(
        [
            [0.03 + 0.01j, -0.02 + 0.04j, 0.01 - 0.03j, -0.04 - 0.01j,
             0.02 + 0.02j, -0.01 - 0.02j, 0.04 - 0.03j, -0.03 + 0.02j],
            [-0.02 + 0.01j, 0.04 + 0.02j, -0.01 - 0.04j, 0.03 - 0.02j,
             -0.04 + 0.03j, 0.02 - 0.01j, 0.01 + 0.04j, -0.03 - 0.02j],
        ],
        dtype=np.complex128,
    )
    payload = np.tile(symbols[:6], (2, 2, 1))
    return pilots + residual, pilots, np.ones_like(pilots, dtype=bool), payload


def test_c4_one_scalar_shared_across_polarizations_and_codewords():
    target = _target()
    pilot_rx, pilot_ref, known_mask, payload = _frame_inputs(target)
    actions = target.build_frame_actions(
        pilot_rx,
        pilot_ref,
        known_mask,
        payload,
        nominal_complex_noise_power=0.04,
        runtime_fixed_scalar=0.75,
    )
    assert actions["b0"].shape == (2, 2, 6, 4)
    assert actions["b1"].shape == actions["b0"].shape
    assert actions["b2"].shape == actions["b0"].shape
    assert actions["b3"].shape == actions["b0"].shape
    assert actions["scale_matrix"].shape == (2, 2)
    np.testing.assert_array_equal(
        actions["scale_matrix"],
        np.full((2, 2), actions["scalar"], dtype=np.float64),
    )
    np.testing.assert_allclose(
        actions["b2"], actions["scalar"] * actions["b0"], rtol=0.0, atol=0.0
    )
    np.testing.assert_allclose(actions["b1"], 0.75 * actions["b0"], rtol=0.0, atol=0.0)
    assert actions["runtime_fixed_scalar"] == pytest.approx(0.75, abs=0.0)

    matched = target.build_frame_actions(
        pilot_rx,
        pilot_ref,
        known_mask,
        payload,
        nominal_complex_noise_power=actions["estimated_n0"],
        runtime_fixed_scalar=0.75,
    )
    np.testing.assert_allclose(matched["b0"], matched["b2"], rtol=0.0, atol=1e-12)
    np.testing.assert_allclose(matched["b0"], matched["b3"], rtol=0.0, atol=1e-12)


def test_c5_receiver_api_truth_firewall_is_byte_stable():
    target = _target()
    forbidden = {
        "true_noise",
        "snr",
        "payload_bits",
        "payload_labels",
        "decoder_truth",
        "future_samples",
    }
    assert forbidden.isdisjoint(inspect.signature(target.build_frame_actions).parameters)
    pilot_rx, pilot_ref, known_mask, payload = _frame_inputs(target)
    before = target.build_frame_actions(
        pilot_rx,
        pilot_ref,
        known_mask,
        payload,
        nominal_complex_noise_power=0.04,
        runtime_fixed_scalar=0.75,
    )
    scorer_only_truth_mutant = {
        "true_noise": np.full(payload.shape, 1e99 + 1e99j),
        "snr": -999.0,
        "payload_bits": np.ones((2, 2, 1536), dtype=np.uint8),
        "payload_labels": np.zeros(payload.shape, dtype=np.uint8),
        "decoder_truth": np.ones((2, 2, 1024), dtype=np.uint8),
        "future_samples": np.full(payload.shape, -1e99 - 1e99j),
    }
    # API isolation: scorer truth has no receiver parameter and is never passed.
    assert scorer_only_truth_mutant
    after = target.build_frame_actions(
        pilot_rx,
        pilot_ref,
        known_mask,
        payload,
        nominal_complex_noise_power=0.04,
        runtime_fixed_scalar=0.75,
    )
    for arm in ("b0", "b1", "b2", "b3"):
        assert before[arm].tobytes() == after[arm].tobytes()


def test_c6_live_codec_receipt_interleaver_clip_and_filler():
    target = _target()
    codec = target.TargetApskCodec()
    receipt = codec.live_receipt()
    assert receipt["sionna_version"] == "2.0.1"
    assert receipt["base_graph"] == "bg2"
    assert receipt["lifting_size"] == 104
    assert receipt["k"] == 1024
    assert receipt["n"] == 1536
    assert receipt["q_m"] == 4
    assert receipt["k_ldpc"] == 1040
    assert receipt["filler_count"] == 16
    assert receipt["filler_value"] == -20.0
    assert receipt["filler_bit"] == 0
    assert receipt["demapper_clip"] == 30.0
    assert receipt["decode_fresh_clip"] == 30.0
    assert receipt["backend_input_clip"] == 20.0
    assert receipt["decoder_internal_clip"] == 20.0
    assert receipt["backend_input_clip_receipted"] is True
    assert receipt["decoder_internal_clip_receipted"] is True
    assert receipt["decoder_rate_recovery_before_bp_clip_receipted"] is True
    assert receipt["backend_input_clip_observed_min"] == -20.0
    assert receipt["backend_input_clip_observed_max"] == 20.0
    assert receipt["seam_applies_out_int_inv"] is False
    assert receipt["decoder_applies_out_int_inv"] is True
    assert receipt["out_int_sha256"] == (
        "96e1b21c6ec75a66cbe865e5f86c6342b224e49ffcfb44c13317c837a9774919"
    )
    assert receipt["out_int_inv_sha256"] == (
        "6e914d73d48086475228d0d7b18fec59d9e60f8f0137085a500f113f56137516"
    )


def test_c6_four_case_target_apsk_ldpc_roundtrip_receipt():
    target = _target()
    codec = target.TargetApskCodec()
    receipt = codec.roundtrip_receipt()
    assert receipt["cases"] == ("all_zero", "single_one", "walking_label", "random")
    assert receipt["bit_errors"] == {
        "all_zero": 0,
        "single_one": 0,
        "walking_label": 0,
        "random": 0,
    }
    assert receipt["encoded_shape"] == (4, 1536)
    assert receipt["coded_group_shape"] == (4, 384, 4)
    assert receipt["mapped_shape"] == (4, 384)
    assert receipt["flatten_shape"] == (4, 1536)
    assert receipt["coded_to_llr_sign_errors"] == {
        "all_zero": 0,
        "single_one": 0,
        "walking_label": 0,
        "random": 0,
    }
    assert len(receipt["grouping_sha256"]) == 64
    assert receipt["decoder_calls"] == 1
    assert receipt["configured_iterations"] == 20
    assert receipt["restart"] is True
    assert receipt["all_finite"] is True
    assert len(receipt["hard_output_sha256"]) == 64


class _FreshSpyBackend:
    def __init__(self):
        self.calls = []

    def decode(self, llr, *, message_state=None, warm_state=None):
        self.calls.append((np.asarray(llr).copy(), message_state, warm_state))
        return np.zeros((np.asarray(llr).shape[0], 1024), dtype=np.uint8)


def test_c4_c6_each_arm_is_fresh_and_uses_identical_call_budget():
    target = _target()
    spy = _FreshSpyBackend()
    codec = target.TargetApskCodec(backend=spy)
    arms = {
        "B0": np.full((4, 1536), 10.0),
        "B1": np.full((4, 1536), 20.0),
        "B2": np.full((4, 1536), 40.0),
        "B3": np.full((4, 1536), -40.0),
    }
    receipt = codec.decode_arms_fresh(arms)
    assert receipt["decoder_calls"] == {arm: 1 for arm in arms}
    assert receipt["configured_iterations"] == {arm: 20 for arm in arms}
    assert receipt["restart"] == {arm: True for arm in arms}
    assert len(spy.calls) == 4
    for llr, message_state, warm_state in spy.calls:
        assert message_state is None and warm_state is None
        assert np.max(np.abs(llr)) <= 30.0
