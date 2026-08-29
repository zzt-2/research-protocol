"""Correctness-only tests for the Ch5 APSK structured-covariance seam."""

from __future__ import annotations

import importlib
import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest


SIM_ROOT = Path(__file__).resolve().parents[1]
SEAM = SIM_ROOT / "explore" / "ch5-apsk-structured-covariance"
for path in (SIM_ROOT, SEAM):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def _load_modules():
    try:
        fixture = importlib.import_module("post_ch4_fixture")
        methods = importlib.import_module("methods")
        metrics = importlib.import_module("codec_metrics")
    except ModuleNotFoundError as exc:
        pytest.fail(f"T054 seam is not implemented: {exc}")
    return fixture, methods, metrics


def _deterministic_circular_pilots(symbols: np.ndarray, repeats: int = 4):
    offsets = np.array([0.02, -0.02, 0.02j, -0.02j], dtype=np.complex128)
    labels = np.repeat(np.arange(16), repeats)
    z = np.repeat(symbols, repeats) + np.tile(offsets, 16)
    return z, labels


def test_apsk_labeling_partition_and_noiseless_llr_roundtrip():
    _, _, metrics = _load_modules()
    symbols, bits = metrics.apsk16_table()
    covariances = np.repeat(np.eye(2)[None, :, :] * 1e-4, 16, axis=0)

    llr = metrics.mahalanobis_logdet_llr(symbols, symbols, covariances, clip=30.0)

    assert symbols.shape == (16,)
    assert bits.shape == (16, 4)
    assert np.unique(bits, axis=0).shape[0] == 16
    assert np.array_equal((llr >= 0).astype(np.uint8), bits)
    for bit_index in range(4):
        assert np.count_nonzero(bits[:, bit_index] == 0) == 8
        assert np.count_nonzero(bits[:, bit_index] == 1) == 8


def test_all_covariance_arms_share_floor_and_are_symmetric_pd():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=54)
    symbols, _ = metrics.apsk16_table()
    floor = 2e-6

    arms = methods.estimate_covariance_arms(
        pair.train.z,
        pair.train.pilot_labels,
        symbols,
        floor=floor,
        kappa=7.0,
        b3_shrinkage=0.1,
    )

    assert set(arms) == {"B1", "B2", "B3", "C1"}
    for covariances in arms.values():
        assert covariances.shape == (16, 2, 2)
        assert np.all(np.isfinite(covariances))
        assert np.allclose(covariances, np.swapaxes(covariances, -1, -2))
        assert np.min(np.linalg.eigvalsh(covariances)) >= floor * (1.0 - 1e-10)


def test_radial_tangential_covariances_rotate_equivariantly():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=91)
    symbols, _ = metrics.apsk16_table()
    angle = 0.371
    phasor = np.exp(1j * angle)
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )

    original = methods.estimate_covariance_arms(
        pair.train.z, pair.train.pilot_labels, symbols,
        floor=1e-8, kappa=5.0, b3_shrinkage=0.15,
    )
    rotated = methods.estimate_covariance_arms(
        pair.train.z * phasor, pair.train.pilot_labels, symbols * phasor,
        floor=1e-8, kappa=5.0, b3_shrinkage=0.15,
    )

    for arm in ("B2", "B3", "C1"):
        expected = np.einsum("ab,kbc,dc->kad", rotation, original[arm], rotation)
        assert np.allclose(rotated[arm], expected, rtol=1e-10, atol=1e-12)


def test_circular_residual_degenerates_b2_and_c1_to_scalar():
    _, methods, metrics = _load_modules()
    symbols, _ = metrics.apsk16_table()
    z, labels = _deterministic_circular_pilots(symbols)

    arms = methods.estimate_covariance_arms(
        z, labels, symbols, floor=1e-10, kappa=11.0, b3_shrinkage=0.2,
    )
    expected_unbiased_variance = 2.0 * 0.02**2 / 3.0

    for arm in ("B2", "C1"):
        diagonal = np.diagonal(arms[arm], axis1=1, axis2=2)
        assert np.allclose(diagonal[:, 0], diagonal[:, 1], atol=1e-14)
        assert np.allclose(arms[arm][:, 0, 1], 0.0, atol=1e-14)
    assert np.allclose(np.diagonal(arms["B1"], axis1=1, axis2=2), expected_unbiased_variance)
    assert np.allclose(np.diagonal(arms["B2"], axis1=1, axis2=2), expected_unbiased_variance)


def test_c1_kappa_zero_is_local_and_large_kappa_tends_to_b2():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=12)
    symbols, _ = metrics.apsk16_table()

    local = methods.estimate_covariance_arms(
        pair.train.z, pair.train.pilot_labels, symbols,
        floor=1e-10, kappa=0.0, b3_shrinkage=0.1,
    )
    almost_pooled = methods.estimate_covariance_arms(
        pair.train.z, pair.train.pilot_labels, symbols,
        floor=1e-10, kappa=1e15, b3_shrinkage=0.1,
    )
    expected_local = methods.point_local_rt_covariances(
        pair.train.z, pair.train.pilot_labels, symbols, floor=1e-10,
    )

    assert np.allclose(local["C1"], expected_local, rtol=1e-12, atol=1e-14)
    assert np.allclose(almost_pooled["C1"], almost_pooled["B2"], rtol=1e-11, atol=1e-13)


def test_c1_matches_closed_form_shrinkage_for_one_point():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=31)
    symbols, _ = metrics.apsk16_table()
    kappa = 9.0
    details = methods.estimate_structured_details(
        pair.train.z, pair.train.pilot_labels, symbols, floor=1e-12, kappa=kappa,
    )
    point = 3
    lam = kappa / (details.counts[point] + kappa)
    expected = (1.0 - lam) * details.local_variances[point] + lam * details.ring_targets[point]

    assert np.allclose(details.shrunk_variances[point], expected, rtol=0.0, atol=1e-15)


def test_c1_supports_unequal_per_point_pilot_counts():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=44)
    symbols, _ = metrics.apsk16_table()
    keep = np.ones(pair.train.z.size, dtype=bool)
    keep[np.flatnonzero(pair.train.pilot_labels == 0)[:3]] = False

    details = methods.estimate_structured_details(
        pair.train.z[keep],
        pair.train.pilot_labels[keep],
        symbols,
        floor=1e-10,
        kappa=4.0,
    )

    assert details.counts[0] == details.counts[1] - 3
    assert details.covariances.shape == (16, 2, 2)
    assert np.all(np.linalg.eigvalsh(details.covariances) > 0.0)


def test_mahalanobis_logdet_llr_matches_bruteforce_reference():
    _, _, metrics = _load_modules()
    symbols, bits = metrics.apsk16_table()
    covariances = np.empty((16, 2, 2), dtype=np.float64)
    for index in range(16):
        theta = np.angle(symbols[index])
        rotation = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )
        covariances[index] = rotation @ np.diag([0.015 + index * 2e-4, 0.006]) @ rotation.T
    z = symbols[[0, 5, 9, 14]] + np.array([0.01 + 0.02j, -0.02j, 0.015, -0.01 + 0.01j])

    actual = metrics.mahalanobis_logdet_llr(z, symbols, covariances, clip=1000.0)
    reference = np.empty_like(actual)
    for row, sample in enumerate(z):
        xy = np.array([sample.real, sample.imag])
        logp = np.empty(16)
        for index, mean in enumerate(symbols):
            delta = xy - np.array([mean.real, mean.imag])
            sign, logdet = np.linalg.slogdet(covariances[index])
            assert sign > 0
            logp[index] = -0.5 * (delta @ np.linalg.solve(covariances[index], delta) + logdet)
        for bit_index in range(4):
            one = np.logaddexp.reduce(logp[bits[:, bit_index] == 1])
            zero = np.logaddexp.reduce(logp[bits[:, bit_index] == 0])
            reference[row, bit_index] = one - zero

    assert np.allclose(actual, reference, rtol=1e-12, atol=1e-12)


def test_truth_firewall_and_paired_fixture_contract():
    fixture, methods, _ = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=7)

    assert pair.train.realization_hash == pair.eval.realization_hash == pair.realization_hash
    assert "SYNTHETIC_CORRECTNESS_ONLY" in pair.train.flags
    assert "NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL" in pair.train.flags
    assert np.all(pair.train.pilot_mask)
    assert not np.any(pair.eval.pilot_mask)
    assert np.all(pair.eval.pilot_labels == -1)
    assert not np.shares_memory(pair.train.z, pair.eval.z)
    assert "eval_bits" not in methods.estimate_covariance_arms.__code__.co_varnames
    assert "tx_residual" not in methods.estimate_covariance_arms.__code__.co_varnames


def test_all_arms_share_one_pilot_estimated_mean_consumed_by_llr():
    fixture, methods, metrics = _load_modules()
    pair = fixture.make_synthetic_correctness_pair(seed=19)
    symbols, _ = metrics.apsk16_table()

    models = methods.estimate_gaussian_arms(
        pair.train.z,
        pair.train.pilot_labels,
        symbols,
        floor=1e-8,
        kappa=7.0,
        b3_shrinkage=0.1,
    )
    shared_mean = models["B1"].means
    expected = np.array(
        [pair.train.z[pair.train.pilot_labels == point].mean() for point in range(16)]
    )

    assert all(model.means is shared_mean for model in models.values())
    assert np.allclose(shared_mean, expected)
    for model in models.values():
        llr = metrics.mahalanobis_logdet_llr(
            pair.eval.z[:8], model.means, model.covariances, clip=30.0
        )
        assert llr.shape == (8, 4)
        assert np.all(np.isfinite(llr))


def test_bundle_modulation_identity_is_fingerprinted_from_common_mapping():
    fixture, _, metrics = _load_modules()
    symbols, bits = metrics.apsk16_table()
    identity = metrics.apsk16_identity()
    digest = hashlib.sha256()
    digest.update(symbols.view(np.float64).tobytes())
    digest.update(bits.tobytes())
    expected_hash = digest.hexdigest()
    pair = fixture.make_synthetic_correctness_pair(seed=23)

    assert identity.source == "common._modulation.m16apsk_mod"
    assert identity.table_sha256 == expected_hash
    assert pair.train.constellation_id == identity.constellation_id
    assert pair.train.labeling_id == identity.labeling_id
    assert expected_hash[:16] in pair.train.constellation_id
    assert expected_hash[:16] in pair.train.labeling_id


def test_gmi_identity_only_prefers_correct_llr_to_flipped_or_zero():
    _, _, metrics = _load_modules()
    _, bits = metrics.apsk16_table()
    bits = np.tile(bits, (32, 1))
    correct = (2.0 * bits - 1.0) * 20.0

    good = metrics.gmi_analytic(correct, bits)
    flipped = metrics.gmi_analytic(-correct, bits)
    zero = metrics.gmi_analytic(np.zeros_like(correct), bits)

    assert good > 3.99
    assert good > zero >= flipped
    assert zero == pytest.approx(0.0, abs=1e-12)


def test_smoke_receipt_is_explicitly_correctness_only():
    _load_modules()
    try:
        smoke = importlib.import_module("run_smoke")
    except ModuleNotFoundError as exc:
        pytest.fail(f"T054 smoke runner is not implemented: {exc}")

    receipt = smoke.run_smoke(seed=54)
    identity = importlib.import_module("codec_metrics").apsk16_identity()

    assert receipt["scope"] == [
        "CORRECTNESS_ONLY",
        "SYNTHETIC_RESIDUAL",
        "NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL",
    ]
    assert receipt["label_roundtrip_bit_errors"] == 0
    assert receipt["shared_pilot_mean_object"] is True
    assert receipt["constellation_id"] == identity.constellation_id
    assert receipt["labeling_id"] == identity.labeling_id
    assert receipt["minimum_covariance_eigenvalue"] > 0.0
    assert receipt["circular_b2_scalar_gap"] < 1e-12
    assert receipt["circular_c1_scalar_gap"] < 1e-12
    assert receipt["rotation_equivariance_max_abs_error"] < 1e-12
    assert receipt["kappa_zero_local_max_abs_error"] < 1e-12
    assert receipt["kappa_large_b2_max_abs_error"] < 1e-10
    assert receipt["gmi_correct"] > receipt["gmi_zero"] >= receipt["gmi_flipped"]
