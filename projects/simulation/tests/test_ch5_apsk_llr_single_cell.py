from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest
import yaml


ROOT = Path(__file__).resolve().parents[3]
CELL_DIR = ROOT / "projects" / "simulation" / "explore" / "ch5-apsk-llr-calibration"
CORE = CELL_DIR / "single_cell.py"
MANIFEST = CELL_DIR / "single_cell_manifest.yaml"


def _target():
    assert CORE.exists(), "single_cell.py is not implemented"
    spec = importlib.util.spec_from_file_location("t077_single_cell", CORE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_manifest_freezes_single_cell_mapping_and_disjoint_splits():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["authority"] == "T077/D056/V031/CP018"
    assert manifest["cell"]["continuous_total_symbols"] == 260
    assert manifest["cell"]["gamma_gamma_block"] == 256
    assert manifest["cell"]["observation_symbols_in_first_gg_block"] == 252
    assert manifest["cell"]["observation_symbols_in_next_gg_block"] == 4
    assert manifest["cell"]["observation_symbols_per_polarization"] == 256
    assert manifest["splits"]["evaluation"]["evaluation_frames"] == 512
    assert manifest["ch3"]["pilot_indices"] == list(range(0, 256, 4))
    assert manifest["codeword"]["mapping"] == "pol_major_pol0_then_pol1"
    assert manifest["codeword"]["apsk_symbols"] == 384
    smoke = set(range(2900, 2908))
    calibration = set(range(3000, 3064))
    evaluation = set(range(4000, 4512))
    assert not smoke & calibration
    assert not smoke & evaluation
    assert not calibration & evaluation
    assert len(evaluation) == 512


def test_pair_identity_binds_codeword_receiver_input_and_received_observation():
    target = _target()
    coded = np.random.default_rng(79).integers(0, 2, size=1536, dtype=np.uint8)
    physical = target.generate_coded_physical_frame(seed=2902, coded_bits=coded)
    receipt = physical["physical_receipt"]
    assert receipt["codeword_sha256"] == target._array_sha256(coded)
    assert receipt["received_observation_sha256"] == target._array_sha256(
        physical["receiver"].rx
    )
    assert receipt["receiver_input_sha256"]
    original = target._physical_pair_identity(physical, coded)
    changed_codeword = coded.copy()
    changed_codeword[0] ^= 1
    assert target._physical_pair_identity(physical, changed_codeword) != original
    physical["receiver"].rx[0, 0] += 1e-12
    assert target._physical_pair_identity(physical, coded) != original


def test_one_codeword_fills_exactly_dp_nonpilot_slots_pol_major():
    target = _target()
    coded = np.resize(np.array([0, 0, 0, 0, 1, 1, 1, 1], dtype=np.uint8), 1536)
    frame = target.build_dp_symbol_frame(coded)
    pilot_indices = np.arange(0, 256, 4)
    nonpilot = np.setdiff1d(np.arange(256), pilot_indices)
    assert frame["symbols"].shape == (2, 256)
    assert frame["known_mask"].shape == (2, 256)
    assert np.array_equal(np.flatnonzero(frame["known_mask"][0]), pilot_indices)
    assert np.array_equal(np.flatnonzero(frame["known_mask"][1]), pilot_indices)
    groups = coded.reshape(384, 4)
    table_groups = frame["bits_by_label"][frame["point_labels"]]
    assert np.array_equal(table_groups[0, nonpilot], groups[:192])
    assert np.array_equal(table_groups[1, nonpilot], groups[192:])
    assert np.array_equal(target.extract_coded_bits(frame["point_labels"]), coded)
    assert frame["mapping_receipt"]["coded_bits"] == 1536
    assert frame["mapping_receipt"]["nonpilot_slots"] == 384
    assert frame["mapping_receipt"]["mapping"] == "pol-major:pol0[192],pol1[192]"


def test_mapping_hash_is_deterministic_and_bit_sensitive():
    target = _target()
    zeros = np.zeros(1536, dtype=np.uint8)
    first = target.build_dp_symbol_frame(zeros)
    second = target.build_dp_symbol_frame(zeros.copy())
    mutant = zeros.copy()
    mutant[767] = 1
    changed = target.build_dp_symbol_frame(mutant)
    assert first["mapping_receipt"] == second["mapping_receipt"]
    assert first["mapping_receipt"]["mapping_sha256"] != changed["mapping_receipt"]["mapping_sha256"]


def test_coded_physical_frame_preserves_t066_timing_and_mapping():
    target = _target()
    coded = np.random.default_rng(77).integers(0, 2, size=1536, dtype=np.uint8)
    first = target.generate_coded_physical_frame(seed=2900, coded_bits=coded)
    second = target.generate_coded_physical_frame(seed=2900, coded_bits=coded.copy())
    receipt = first["physical_receipt"]
    assert receipt["preamble_symbols"] == 4
    assert receipt["observation_symbols_per_polarization"] == 256
    assert receipt["continuous_total_symbols"] == 260
    assert receipt["gamma_gamma_block"] == 256
    assert receipt["observation_first_block_symbols"] == 252
    assert receipt["observation_next_block_symbols"] == 4
    assert first["receiver"].rx.shape == (2, 256)
    assert np.array_equal(
        target.extract_coded_bits(first["mapping"]["point_labels"]), coded
    )
    assert first["physical_receipt"] == second["physical_receipt"]
    assert np.array_equal(first["receiver"].rx, second["receiver"].rx)


def test_receiver_arms_have_truth_firewall_and_paired_hashes():
    target = _target()
    forbidden = {"true_snr", "true_noise", "payload_truth", "payload_bits", "decoder_truth"}
    assert forbidden.isdisjoint(inspect.signature(target.build_receiver_arms).parameters)
    coded = np.random.default_rng(78).integers(0, 2, size=1536, dtype=np.uint8)
    physical = target.generate_coded_physical_frame(seed=2901, coded_bits=coded)
    bridge = target.run_coded_receiver(physical["receiver"])
    first = target.build_receiver_arms(
        bridge["compensated"],
        physical["receiver"].pilot_symbols,
        physical["receiver"].known_mask,
        nominal_complex_noise_power=10.0 ** (-15.0 / 10.0),
        b1_scalar=1.0,
    )
    scorer_truth = physical["mapping"]["symbols"].copy()
    scorer_truth[:, target.NONPILOT_INDICES] *= -1
    second = target.build_receiver_arms(
        bridge["compensated"],
        physical["receiver"].pilot_symbols,
        physical["receiver"].known_mask,
        nominal_complex_noise_power=10.0 ** (-15.0 / 10.0),
        b1_scalar=1.0,
    )
    assert scorer_truth.shape == (2, 256)
    assert first["receiver_hashes"] == second["receiver_hashes"]
    assert all(value.shape == (1, 1536) for value in first["llrs"].values())
    assert first["physical_frame_scalars"] == 1


class _SmokeCodec:
    def __init__(self):
        self.calls = 0

    def encode(self, info_bits):
        info = np.asarray(info_bits, dtype=np.uint8)
        return np.resize(info, (info.shape[0], 1536)).astype(np.uint8)

    def decode_fresh(self, llr):
        self.calls += 1
        batch = np.asarray(llr).shape[0]
        return np.zeros((batch, 1024), dtype=np.uint8), {
            "restart": True,
            "configured_iterations": 20,
            "decode_fresh_clip": 30.0,
        }


def test_eight_frame_smoke_uses_frozen_seeds_and_fresh_paired_decodes():
    target = _target()
    result = target.run_correctness_smoke(write=False, codec_factory=_SmokeCodec)
    assert result["receipt"]["completed_frames"] == 8
    assert result["receipt"]["seeds"] == list(range(2900, 2908))
    assert result["receipt"]["mapping_firewall"] == "PASS"
    assert result["receipt"]["receiver_api_truth_exclusion"] == "PASS"
    assert result["receipt"]["truth_exclusion_evidence"] == (
        "receiver_api_signature_and_identical_input_replay"
    )
    assert result["receipt"]["paired_hashes"] == "PASS"
    assert result["receipt"]["fresh_decode_lifecycle"] == "PASS"
    assert result["receipt"]["unique_pair_hashes"] == 8
    assert result["receipt"]["codec"] == "_SmokeCodec"
    assert result["receipt"]["live_backend"] is False
    assert len(result["raw"]["frames"]) == 8
    for frame in result["raw"]["frames"]:
        assert set(frame["arms"]) == {"B0", "B1", "B2", "B3", "O1"}
        assert all(arm["restart"] for arm in frame["arms"].values())
        assert len({arm["pair_hash"] for arm in frame["arms"].values()}) == 1


def test_injected_smoke_codec_cannot_write_live_artifacts():
    target = _target()
    with pytest.raises(ValueError, match="injected codec"):
        target.run_correctness_smoke(write=True, codec_factory=_SmokeCodec)


def test_one_frame_live_target_codec_encode_physical_arms_decode_fresh():
    target = _target()
    result = target.run_live_integration_point_check(write=False, seed=2900)
    assert result["receipt"]["completed_frames"] == 1
    assert result["receipt"]["codec"] == "TargetApskCodec"
    assert result["receipt"]["fresh_live_decode"] == "PASS"
    assert result["receipt"]["physical_pair_hash"] == "PASS"
    assert set(result["raw"]["frames"][0]["arms"]) == {
        "B0",
        "B1",
        "B2",
        "B3",
        "O1",
    }


def test_b1_calibration_grid_and_deterministic_tie_break():
    target = _target()
    grid = target.b1_scalar_grid()
    assert np.array_equal(grid, 2.0 ** (np.arange(-8, 7) / 2.0))
    records = [
        {"scalar": 2.0, "fer": 3, "bit_errors": 20},
        {"scalar": 0.5, "fer": 2, "bit_errors": 10},
        {"scalar": 2.0 ** -0.5, "fer": 2, "bit_errors": 10},
        {"scalar": 2.0 ** 0.5, "fer": 2, "bit_errors": 10},
    ]
    selected = target.select_b1_scalar(records)
    assert selected["scalar"] == 2.0 ** -0.5
    assert selected["tie_break"] == ["fer", "ber", "abs_log_scalar", "scalar"]


def test_gate1_uses_frame_cluster_bootstrap_and_positive_lower_bound():
    target = _target()
    pilot = np.exp(np.linspace(-2.0, 2.0, 128))
    payload = pilot ** 1.1
    positive = target.gate1_metrics(pilot, payload, seed=1234, resamples=500)
    assert positive["rho"] > 0.0
    assert positive["ci_one_sided_lower"] > 0.0
    assert positive["pass"] is True
    assert positive["frames"] == 128
    negative = target.gate1_metrics(pilot, payload[::-1], seed=1234, resamples=500)
    assert negative["pass"] is False


def test_paired_ber_ci_clusters_whole_physical_frames():
    target = _target()
    first = np.full(128, 5, dtype=np.int64)
    second = np.full(128, 1, dtype=np.int64)
    result = target.paired_rate_difference_ci(
        first, second, denominator_per_frame=1024, seed=99, resamples=500
    )
    assert result["point"] == pytest.approx(4 / 1024)
    assert result["ci_lower"] == pytest.approx(4 / 1024)
    assert result["ci_upper"] == pytest.approx(4 / 1024)
    assert result["cluster"] == "physical_frame"


def test_gate2_terminal_order_headroom_no_headroom_and_insufficient():
    target = _target()
    first_bits = np.full(128, 10, dtype=np.int64)
    first_fer = np.ones(128, dtype=np.int64)
    second_bits = np.full(128, 1, dtype=np.int64)
    second_fer = np.zeros(128, dtype=np.int64)
    passed = target.gate2_decision(
        first_bits,
        first_fer,
        second_bits,
        second_fer,
        seed=101,
        resamples=500,
    )
    assert passed["gate2"] == "PASS"
    assert passed["terminal"] is None
    worse = target.gate2_decision(
        second_bits,
        second_fer,
        first_bits,
        first_fer,
        seed=101,
        resamples=500,
    )
    assert worse["terminal"] == "SINGLE_CELL_NO_HEADROOM"
    zeros = np.zeros(128, dtype=np.int64)
    insufficient = target.gate2_decision(
        zeros, zeros, zeros, zeros, seed=101, resamples=500
    )
    assert insufficient["terminal"] == "SINGLE_CELL_INSUFFICIENT_SENSITIVITY"


def test_audit_pair_receipt_is_raw_only_ordered_and_hash_sensitive():
    target = _target()
    frame = {
        "frame_index": 0,
        "seed": 4000,
        "info_bits_sha256": "i" * 64,
        "coded_bits_sha256": "c" * 64,
        "mapping_sha256": "m" * 64,
        "physical": {
            "codeword_sha256": "c" * 64,
            "mapping_sha256": "m" * 64,
            "receiver_input_sha256": "r" * 64,
            "received_observation_sha256": "o" * 64,
        },
        "realization_hash": "z" * 64,
        "bundle_hash": "b" * 64,
        "pair_hash": "p" * 64,
    }
    first = target.audit_pair_receipt(frame, manifest_hash="h" * 64)
    assert first["field_order"] == list(target.AUDIT_PAIR_FIELD_ORDER)
    assert len(first["audit_pair_sha256"]) == 64
    changed = dict(frame)
    changed["mapping_sha256"] = "x" * 64
    assert (
        target.audit_pair_receipt(changed, manifest_hash="h" * 64)[
            "audit_pair_sha256"
        ]
        != first["audit_pair_sha256"]
    )
