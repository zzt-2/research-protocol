from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


SIM_ROOT = Path(__file__).resolve().parents[3]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from common._modulation import m16apsk_demod, m16apsk_mod  # noqa: E402


def _constellation_by_label() -> np.ndarray:
    """Construct the normalized (8,8)-16APSK oracle independently."""
    gamma = 2.57
    r_inner = np.sqrt(2.0 / (1.0 + gamma**2))
    r_outer = gamma * r_inner
    physical_points = np.concatenate(
        [
            r_inner
            * np.exp(1j * (np.pi / 8.0 + np.arange(8) * np.pi / 4.0)),
            r_outer * np.exp(1j * np.arange(8) * np.pi / 4.0),
        ]
    )
    physical_labels = np.array(
        [
            0b0000,
            0b0001,
            0b0011,
            0b0010,
            0b0110,
            0b0111,
            0b0101,
            0b0100,
            0b1000,
            0b1001,
            0b1011,
            0b1010,
            0b1110,
            0b1111,
            0b1101,
            0b1100,
        ],
        dtype=int,
    )
    points = np.empty(16, dtype=np.complex128)
    points[physical_labels] = physical_points
    return points


def _labels_to_bits(labels: np.ndarray) -> np.ndarray:
    labels = np.asarray(labels, dtype=int)
    bits = np.empty(4 * labels.size, dtype=int)
    bits[0::4] = (labels >> 3) & 1
    bits[1::4] = (labels >> 2) & 1
    bits[2::4] = (labels >> 1) & 1
    bits[3::4] = labels & 1
    return bits


def _brute_force_labels(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    distances = np.abs(
        np.asarray(samples)[:, np.newaxis]
        - _constellation_by_label()[np.newaxis, :]
    ) ** 2
    return np.argmin(distances, axis=1), distances


def test_all_normalized_constellation_points_round_trip_their_labels():
    labels = np.arange(16, dtype=int)
    bits = _labels_to_bits(labels)

    np.testing.assert_array_equal(m16apsk_demod(m16apsk_mod(bits)), bits)


def test_frozen_inner_ray_counterexample_uses_global_euclidean_nearest():
    sample = np.array([0.9155 * np.exp(1j * np.pi / 8.0)])
    oracle_labels, _ = _brute_force_labels(sample)

    assert oracle_labels.tolist() == [0b0000]
    np.testing.assert_array_equal(
        m16apsk_demod(sample), _labels_to_bits(oracle_labels)
    )


def test_deterministic_off_boundary_cloud_matches_full_16_point_oracle():
    rng = np.random.default_rng(20260830)
    radii = rng.uniform(0.05, 1.85, size=512)
    phases = rng.uniform(-np.pi, np.pi, size=512)
    samples = radii * np.exp(1j * phases)
    oracle_labels, distances = _brute_force_labels(samples)

    ordered = np.sort(distances, axis=1)
    assert np.min(ordered[:, 1] - ordered[:, 0]) > 1e-6
    np.testing.assert_array_equal(
        m16apsk_demod(samples), _labels_to_bits(oracle_labels)
    )
