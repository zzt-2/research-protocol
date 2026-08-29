"""T060 correctness tests for the receiver-visible Ch4 -> per-pol Ch3 bridge."""

from __future__ import annotations

import importlib
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest


SIM_ROOT = Path(__file__).resolve().parents[1]
SEAM = SIM_ROOT / "explore" / "ch5-apsk-structured-covariance"
for path in (SIM_ROOT, SEAM):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


bridge = importlib.import_module("post_ch4_ch3_bridge")
methods = importlib.import_module("methods")
metrics = importlib.import_module("codec_metrics")


def _config(**overrides):
    base = bridge.BridgeConfig.correctness_fixture(
        seed=60060,
        n_symbols=160,
        observation_stop=128,
        snr_db=120.0,
        turbulence_alpha=1.0e12,
        turbulence_beta=1.0e12,
        gamma_gamma_block=16,
        f_residual_hz=0.0,
        f_dot_hz_per_s=0.0,
        linewidth_hz=0.0,
    )
    return replace(base, **overrides)


def _arm():
    return bridge.FrozenCh4Arm.fixture_plain(mu=0.0)


def test_identity_noiseless_bridge_residual_is_zero():
    receiver, _truth = bridge.generate_correctness_fixture(
        _config(), identity_jones=True, noiseless=True
    )
    bundle = bridge.run_bridge(receiver, _arm())

    np.testing.assert_allclose(bundle.e, 0.0, atol=2e-12, rtol=0.0)
    assert bundle.cpr_mode == "DA"
    assert bundle.ch4_summary["arm_id"] == "fixture-plain-mu0"
    assert bundle.scope == (
        "BRIDGE_CORRECTNESS_ONLY",
        "TARGET_OCCURRENCE_NOT_RUN",
        "NO_METHOD_SIGNAL",
    )


@pytest.mark.parametrize("rotation_index", range(8))
def test_all_eight_apsk_rotations_are_uniquely_resolved_from_known_pilots(rotation_index):
    symbols, _ = metrics.apsk16_table()
    labels = np.arange(16, dtype=np.int64)
    pilot = symbols[labels]
    rotated = pilot * np.exp(1j * 2.0 * np.pi * rotation_index / 8.0)

    resolved, selected, scores = bridge.resolve_pilot_only_ambiguity(
        rotated, pilot, np.arange(pilot.size)
    )

    assert selected == rotation_index
    assert np.count_nonzero(np.isclose(scores, scores.min(), atol=1e-14)) == 1
    np.testing.assert_allclose(resolved, pilot, atol=2e-15, rtol=0.0)


def test_payload_truth_mutation_cannot_change_bridge_or_hash():
    receiver, truth = bridge.generate_correctness_fixture(
        _config(snr_db=34.0), identity_jones=False, noiseless=False
    )
    first = bridge.run_bridge(receiver, _arm())
    truth.payload_labels[:] = (truth.payload_labels + 7) % 16
    truth.payload_bits[:] ^= 1
    truth.true_jones[:] = 17.0 - 9.0j
    truth.true_phase[:] = -123.0
    truth.true_snr_db = -999.0
    second = bridge.run_bridge(receiver, _arm())

    assert first.bundle_hash == second.bundle_hash
    np.testing.assert_array_equal(first.ambiguity_index, second.ambiguity_index)
    np.testing.assert_array_equal(first.ch4_W, second.ch4_W)
    np.testing.assert_array_equal(first.z_pilot, second.z_pilot)


def test_polarization_swap_is_equivariant_without_cross_pol_pooling():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=38.0), identity_jones=True, noiseless=False
    )
    original = bridge.run_bridge(receiver, _arm())
    swapped = bridge.run_bridge(bridge.swap_polarizations(receiver), _arm())

    np.testing.assert_allclose(swapped.z_pilot, original.z_pilot[::-1], atol=2e-12)
    np.testing.assert_allclose(swapped.e, original.e[::-1], atol=2e-12)
    np.testing.assert_array_equal(swapped.per_pol_point_counts, original.per_pol_point_counts[::-1])
    np.testing.assert_array_equal(swapped.ambiguity_index, original.ambiguity_index[::-1])


def test_call_order_is_ch4_then_two_independent_da_cpr_calls():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(), identity_jones=True, noiseless=True
    )
    events: list[str] = []

    def ch4_runner(rx, w0, frozen_arm):
        events.append("ch4")
        return bridge.run_frozen_ch4_arm(rx, w0, frozen_arm)

    def da_runner(rx, pilot_idx, pilot_sym, mod="m16apsk"):
        events.append(f"da:{len(events)}")
        return bridge.da_ml_recovery(rx, pilot_idx, pilot_sym, mod=mod)

    bridge.run_bridge(receiver, _arm(), ch4_runner=ch4_runner, da_runner=da_runner)

    assert events == ["ch4", "da:1", "da:2"]


def test_bundle_labels_counts_mask_and_residual_are_exact():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=36.0), identity_jones=True, noiseless=False
    )
    bundle = bridge.run_bridge(receiver, _arm())

    np.testing.assert_array_equal(bundle.known_mask, receiver.known_mask[:, : receiver.observation_stop])
    np.testing.assert_array_equal(bundle.point_labels, receiver.pilot_labels)
    np.testing.assert_array_equal(bundle.ring_labels, receiver.pilot_labels >= 8)
    np.testing.assert_allclose(bundle.e, bundle.z_pilot - bundle.x_pilot, atol=0.0, rtol=0.0)
    expected = np.stack(
        [np.bincount(receiver.pilot_labels[pol], minlength=16) for pol in range(2)]
    )
    np.testing.assert_array_equal(bundle.per_pol_point_counts, expected)
    np.testing.assert_array_equal(bundle.per_point_counts, expected.sum(axis=0))


def test_observation_window_is_causal_and_cpr_never_pools_polarizations():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=35.0), identity_jones=True, noiseless=False
    )
    first = bridge.run_bridge(receiver, _arm())
    mutated = receiver.with_future_rx(receiver.rx[:, receiver.observation_stop :] * (11.0 + 7.0j))
    second = bridge.run_bridge(mutated, _arm())

    assert first.bundle_hash == second.bundle_hash
    np.testing.assert_array_equal(first.z_pilot, second.z_pilot)
    assert first.cpr_state_scope == "per-polarization/observation-window-only"
    assert first.cross_polarization_pooling is False


def test_gg_linewidth_and_frequency_sentinels_are_consumed_but_truth_is_not_exported():
    base, _ = bridge.generate_correctness_fixture(
        _config(), identity_jones=True, noiseless=True
    )
    gg, _ = bridge.generate_correctness_fixture(
        _config(turbulence_alpha=3.1, turbulence_beta=2.4), identity_jones=True, noiseless=True
    )
    linewidth, _ = bridge.generate_correctness_fixture(
        _config(linewidth_hz=2.0e4), identity_jones=True, noiseless=True
    )
    ramp, _ = bridge.generate_correctness_fixture(
        _config(f_residual_hz=8.0e5, f_dot_hz_per_s=2.0e8), identity_jones=True, noiseless=True
    )

    hashes = {bridge.run_bridge(item, _arm()).bundle_hash for item in (base, gg, linewidth, ramp)}
    assert len(hashes) == 4
    exported = bridge.run_bridge(ramp, _arm()).deployable_dict()
    forbidden = {"payload_labels", "payload_bits", "true_jones", "true_phase", "true_snr"}
    assert forbidden.isdisjoint(exported)


def test_bundle_feeds_all_covariance_arms_and_circular_control_degenerates_correctly():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=36.0), identity_jones=True, noiseless=False
    )
    bundle = bridge.run_bridge(receiver, _arm())
    symbols, _ = metrics.apsk16_table()

    for pol in range(2):
        arms = methods.estimate_covariance_arms(
            bundle.z_pilot[pol],
            bundle.point_labels[pol],
            symbols,
            floor=1e-10,
            kappa=7.0,
            b3_shrinkage=0.1,
        )
        for covariance in arms.values():
            assert np.all(np.isfinite(covariance))
            assert np.allclose(covariance, covariance.swapaxes(-1, -2))
            assert np.min(np.linalg.eigvalsh(covariance)) > 0.0

    circular_z, circular_labels = bridge.circular_control_pilots(symbols)
    circular = methods.estimate_covariance_arms(
        circular_z, circular_labels, symbols, floor=1e-12, kappa=7.0, b3_shrinkage=0.1
    )
    for arm in ("B2", "C1"):
        assert np.max(np.abs(circular[arm][:, 0, 1])) < 1e-12
        diagonal = np.diagonal(circular[arm], axis1=1, axis2=2)
        assert np.max(np.abs(diagonal[:, 0] - diagonal[:, 1])) < 1e-12


def test_hash_is_stable_and_changes_with_receiver_visible_input():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=35.0), identity_jones=True, noiseless=False
    )
    first = bridge.run_bridge(receiver, _arm())
    repeated = bridge.run_bridge(receiver, _arm())
    changed = receiver.with_visible_rx_delta(pol=0, index=17, delta=1e-4 + 2e-4j)
    changed_bundle = bridge.run_bridge(changed, _arm())

    assert first.bundle_hash == repeated.bundle_hash
    assert first.realization_hash == repeated.realization_hash
    assert changed_bundle.bundle_hash != first.bundle_hash
    assert changed_bundle.realization_hash != first.realization_hash


def test_frozen_arm_snapshot_is_complete_and_changes_only_bundle_hash():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=35.0), identity_jones=True, noiseless=False
    )
    first_arm = bridge.FrozenCh4Arm(
        arm_id="same-id",
        mode="candidate",
        mu=0.0,
        ring_threshold=0.0,
        decision_threshold=0.0,
    )
    observed_snapshots = []

    def capturing_runner(rx, w0, frozen_arm):
        observed_snapshots.append(frozen_arm.canonical_snapshot())
        return bridge.run_frozen_ch4_arm(rx, w0, frozen_arm)

    first = bridge.run_bridge(receiver, first_arm, ch4_runner=capturing_runner)

    expected = {
        "arm_id": "same-id",
        "mode": "candidate",
        "mu": 0.0,
        "ring_threshold": 0.0,
        "decision_threshold": 0.0,
    }
    assert observed_snapshots == [expected]
    assert first.deployable_dict()["frozen_ch4_snapshot"] == expected
    assert first.ch4_summary["frozen_arm_snapshot"] == expected
    for changed_arm in (
        replace(first_arm, mu=1.0e-5),
        replace(first_arm, ring_threshold=1.0e9),
        replace(first_arm, decision_threshold=1.0e9),
    ):
        changed = bridge.run_bridge(receiver, changed_arm)
        assert first.bundle_hash != changed.bundle_hash
        assert first.realization_hash == changed.realization_hash

    plain = bridge.run_bridge(receiver, _arm())
    assert plain.deployable_dict()["frozen_ch4_snapshot"] == {
        "arm_id": "fixture-plain-mu0",
        "mode": "plain",
        "mu": 0.0,
        "ring_threshold": None,
        "decision_threshold": None,
    }


def test_acquisition_and_observation_share_one_continuous_scalar_realization():
    base_receiver, _ = bridge.generate_correctness_fixture(
        _config(), identity_jones=True, noiseless=True
    )
    impaired_receiver, truth = bridge.generate_correctness_fixture(
        _config(
            turbulence_alpha=3.1,
            turbulence_beta=2.4,
            f_residual_hz=8.0e5,
            f_dot_hz_per_s=2.0e8,
            linewidth_hz=2.0e4,
        ),
        identity_jones=True,
        noiseless=True,
    )
    base = bridge.run_bridge(base_receiver, _arm())
    impaired = bridge.run_bridge(impaired_receiver, _arm())

    assert np.max(np.abs(impaired_receiver.ch4_pilot_rx - base_receiver.ch4_pilot_rx)) > 1e-3
    assert np.max(np.abs(impaired.ch4_W - base.ch4_W)) > 1e-6
    assert impaired.deployable_dict()["realization_timing"] == {
        "continuous_scalar": True,
        "preamble_length": impaired_receiver.config.ch4_pilot_count,
        "observation_length": impaired_receiver.config.n_symbols,
        "observation_start": impaired_receiver.config.ch4_pilot_count,
        "total_length": impaired_receiver.config.ch4_pilot_count
        + impaired_receiver.config.n_symbols,
    }
    assert truth.true_phase.shape == (
        impaired_receiver.config.ch4_pilot_count + impaired_receiver.config.n_symbols,
    )


def test_bridge_contract_contains_all_required_receiver_visible_fields():
    receiver, _ = bridge.generate_correctness_fixture(
        _config(snr_db=35.0), identity_jones=True, noiseless=False
    )
    exported = bridge.run_bridge(receiver, _arm()).deployable_dict()
    required = {
        "z_pilot", "x_pilot", "e", "pilot_indices", "point_labels",
        "ring_labels", "per_pol_point_counts", "per_point_counts", "known_mask",
        "cpr_mode", "estimated_phase", "estimated_frequency_hz", "ambiguity_index",
        "ch4_arm", "frozen_ch4_snapshot", "ch4_W", "ch4_gate_summary",
        "realization_timing", "cell_id", "seed", "window_id",
        "config_id", "source_id", "realization_hash", "bundle_hash",
    }
    assert required.issubset(exported)
