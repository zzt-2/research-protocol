from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest


SEAM = Path(__file__).resolve().parents[1]
MODULE_PATH = SEAM / "scaled_unitary.py"


def _module():
    spec = importlib.util.spec_from_file_location("t069_scaled_unitary", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _balanced_pilots(n_pilots: int) -> np.ndarray:
    if n_pilots == 2:
        return np.array([[1, 1], [1, -1]], dtype=np.complex128)
    if n_pilots == 4:
        return np.array(
            [[1, 1, 1, 1], [1, 1j, -1, -1j]], dtype=np.complex128
        )
    raise ValueError(n_pilots)


def _unitary(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(raw)
    phase = np.diag(r)
    return q @ np.diag(np.conj(phase) / np.abs(phase))


def test_c0_no_noise_exact_recovery():
    m = _module()
    rng = np.random.default_rng(100)
    pilots = _balanced_pilots(4)
    payload = rng.normal(size=(2, 19)) + 1j * rng.normal(size=(2, 19))
    channel = 0.73 * _unitary(101)
    result = m.candidate_receiver(pilots, channel @ pilots, channel @ payload)

    assert np.allclose(result.z, payload, rtol=0.0, atol=2e-12)
    assert np.isclose(result.g_hat, 0.73, rtol=0.0, atol=2e-12)
    assert np.isclose(result.rho, 1.0, rtol=0.0, atol=2e-12)


def test_c1_balanced_direct_and_post_ls_are_equivalent():
    m = _module()
    rng = np.random.default_rng(110)
    for n_pilots in (2, 4):
        pilots = _balanced_pilots(n_pilots)
        y_pilots = (
            0.91 * _unitary(111) @ pilots
            + 0.02
            * (rng.normal(size=pilots.shape) + 1j * rng.normal(size=pilots.shape))
        )
        h_ls = m.plain_ls(pilots, y_pilots)
        post = m.project_scaled_unitary(h_ls)
        direct = m.direct_balanced_scaled_unitary(pilots, y_pilots)

        assert np.allclose(post.h_projected, direct.h_projected, atol=3e-12)
        assert np.isclose(post.g_hat, direct.g_hat, atol=3e-12)
        post_objective = np.linalg.norm(y_pilots - post.h_projected @ pilots) ** 2
        direct_objective = np.linalg.norm(y_pilots - direct.h_projected @ pilots) ** 2
        assert np.isclose(post_objective, direct_objective, atol=1e-13)


def test_c2_biunitary_equivariance_and_complex_scale_identities():
    m = _module()
    h = np.array(
        [[1.3 + 0.2j, -0.4 + 0.7j], [0.1 - 0.8j, 0.9 + 0.5j]],
        dtype=np.complex128,
    )
    left = _unitary(120)
    right = _unitary(121)
    base = m.project_scaled_unitary(h)
    transformed = m.project_scaled_unitary(left @ h @ right)

    assert np.allclose(
        transformed.h_projected,
        left @ base.h_projected @ right,
        rtol=0.0,
        atol=4e-12,
    )
    assert np.allclose(
        transformed.w,
        right.conj().T @ base.w @ left.conj().T,
        rtol=0.0,
        atol=4e-12,
    )

    alpha = 0.37 - 1.21j
    scaled = m.project_scaled_unitary(alpha * h)
    assert np.allclose(scaled.h_projected, alpha * base.h_projected, atol=4e-12)
    assert np.allclose(scaled.w, base.w / alpha, atol=4e-12)


def test_c3_paired_delta_theory_projection_bias_and_residual():
    m = _module()
    gain = 0.82
    for delta in (0.0, 0.35):
        h = gain * np.diag([1.0 + delta, 1.0 - delta]).astype(np.complex128)
        result = m.project_scaled_unitary(h)
        expected_rho = (1.0 + delta) / (1.0 - delta)
        expected_bias_sq = 2.0 * gain**2 * delta**2
        expected_residual = delta**2

        assert np.isclose(result.g_hat, gain, atol=2e-12)
        assert np.isclose(result.rho, expected_rho, atol=2e-12)
        assert np.isclose(
            np.linalg.norm(result.h_projected - h) ** 2,
            expected_bias_sq,
            atol=2e-12,
        )
        assert np.isclose(
            np.linalg.norm(result.w @ h - np.eye(2)) ** 2 / 2.0,
            expected_residual,
            atol=2e-12,
        )


def test_c4_truth_firewall_is_byte_identical():
    m = _module()
    rng = np.random.default_rng(130)
    pilots = _balanced_pilots(2)
    y_pilots = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    y_payload = rng.normal(size=(2, 11)) + 1j * rng.normal(size=(2, 11))

    assert tuple(inspect.signature(m.candidate_receiver).parameters) == (
        "x_pilots",
        "y_pilots",
        "y_payload",
    )
    first = m.candidate_receiver(pilots, y_pilots, y_payload)
    hidden_truth_a = 0.5 * _unitary(131)
    hidden_truth_b = 1.7 * _unitary(132)
    second = m.candidate_receiver(pilots.copy(), y_pilots.copy(), y_payload.copy())

    assert m.deployable_bytes(first) == m.deployable_bytes(second)
    assert not np.array_equal(
        np.linalg.inv(hidden_truth_a) @ y_payload,
        np.linalg.inv(hidden_truth_b) @ y_payload,
    )


def test_c5_invalid_inputs_fail_closed_without_near_zero_threshold():
    m = _module()
    pilots = _balanced_pilots(2)
    payload = np.ones((2, 3), dtype=np.complex128)

    invalid_cases = [
        (pilots, np.zeros((2, 2), dtype=np.complex128), payload),
        (
            pilots,
            np.diag([1.0, 0.0]).astype(np.complex128) @ pilots,
            payload,
        ),
        (
            np.array([[1, 1], [1, 1]], dtype=np.complex128),
            np.eye(2, dtype=np.complex128),
            payload,
        ),
    ]
    for x_pilots, y_pilots, y_payload in invalid_cases:
        with pytest.raises(m.InvalidEstimate):
            m.candidate_receiver(x_pilots, y_pilots, y_payload)

    for bad in (np.nan, np.inf, -np.inf):
        bad_y = np.eye(2, dtype=np.complex128)
        bad_y[0, 0] = bad
        with pytest.raises(m.InvalidEstimate):
            m.candidate_receiver(pilots, bad_y, payload)

    near_zero = np.diag([1.0, np.finfo(float).tiny]).astype(np.complex128)
    accepted = m.project_scaled_unitary(near_zero)
    assert accepted.g_hat > 0.0
    assert np.isfinite(accepted.rho)
