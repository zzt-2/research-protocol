from pathlib import Path
import importlib
import sys
import warnings

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))


def _b2_module():
    """Import inside the test so an absent I14 production file is a valid RED."""
    importlib.invalidate_caches()
    return importlib.import_module("b2")


def _gray16_points_and_bits():
    codec = importlib.import_module("codec")
    labels = np.arange(16, dtype=np.uint8)
    weights = np.array([8, 4, 2, 1], dtype=np.uint8)
    bits = ((labels[:, None] & weights) != 0).astype(np.uint8)
    return codec.gray16_map(bits), bits


def test_b201_transition_distance_matches_matrix_power_and_slip_probability():
    b2 = _b2_module()
    p_s = 0.23
    one_step = b2.transition_matrix(p_s, distance=1)
    distance_seven = b2.transition_matrix(p_s, distance=7)

    np.testing.assert_allclose(
        distance_seven,
        np.linalg.matrix_power(one_step, 7),
        rtol=0.0,
        atol=2e-15,
    )
    np.testing.assert_allclose(one_step.sum(axis=1), 1.0, rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(
        1.0 - np.diag(one_step), p_s, rtol=0.0, atol=1e-15
    )


def test_b202_zero_slip_is_exact_log_identity_without_probability_floor():
    b2 = _b2_module()
    log_transition = b2.log_transition_matrix(0.0, distance=37)

    np.testing.assert_array_equal(np.diag(log_transition), np.zeros(4))
    off_diagonal = log_transition[~np.eye(4, dtype=bool)]
    assert np.all(np.isneginf(off_diagonal))
    np.testing.assert_array_equal(np.exp(log_transition), np.eye(4))


def test_b203_moment_split_removes_phase_once_and_preserves_symbol_energy():
    b2 = _b2_module()
    c_post_cplx = 0.91
    sigma_e2 = 0.37
    e_cal = 1.25
    symbols = np.array([1.0 + 0.0j, 3.0 + 1.0j]) / np.sqrt(10.0)

    result = b2.moment_variance(
        c_post_cplx=c_post_cplx,
        sigma_e2=sigma_e2,
        e_cal=e_cal,
        x=symbols,
    )
    mu = np.exp(-sigma_e2 / 2.0)
    expected_n0 = max(0.0, c_post_cplx - 2.0 * (1.0 - mu) * e_cal)
    expected_v = expected_n0 + np.abs(symbols) ** 2 * (1.0 - mu**2)

    assert result.mu == pytest.approx(mu, abs=1e-15)
    assert result.n0_hat_cplx == pytest.approx(expected_n0, abs=1e-15)
    assert result.noise_var_real == pytest.approx(expected_n0 / 2.0, abs=1e-15)
    np.testing.assert_allclose(result.v_x, expected_v, rtol=0.0, atol=1e-15)
    assert not np.allclose(
        result.v_x,
        c_post_cplx + np.abs(symbols) ** 2 * (1.0 - mu**2),
        rtol=0.0,
        atol=1e-15,
    )

    clamped = b2.moment_variance(
        c_post_cplx=0.01,
        sigma_e2=1.0,
        e_cal=2.0,
        x=symbols,
    )
    assert clamped.n0_hat_cplx == 0.0
    assert np.all(np.isfinite(clamped.v_x))


def test_b204_emission_matches_p08_n0_over_two_and_rejects_factor_two_scale():
    b2 = _b2_module()
    constellation, bits = _gray16_points_and_bits()
    y = 0.17 - 0.29j
    state = 3
    n0_hat_cplx = 0.74

    emission = b2.emission_log_weight(
        y,
        state=state,
        x=constellation,
        mu=1.0,
        n0_hat_cplx=n0_hat_cplx,
    )
    b2_llr = np.array(
        [
            np.max(emission[bits[:, bit_index] == 1])
            - np.max(emission[bits[:, bit_index] == 0])
            for bit_index in range(4)
        ]
    )

    rotated = y * np.exp(-0.5j * np.pi * state)
    distance2 = np.abs(rotated - constellation) ** 2
    p08_sigma2 = n0_hat_cplx / 2.0
    p08_llr = np.array(
        [
            (
                np.min(distance2[bits[:, bit_index] == 0])
                - np.min(distance2[bits[:, bit_index] == 1])
            )
            / (2.0 * p08_sigma2)
            for bit_index in range(4)
        ]
    )
    wrong_factor_two = p08_llr / 2.0

    np.testing.assert_allclose(b2_llr, p08_llr, rtol=0.0, atol=2e-15)
    assert np.all(np.abs(p08_llr) > 1e-12)
    np.testing.assert_allclose(wrong_factor_two, 0.5 * b2_llr, rtol=0.0, atol=1e-15)
    assert not np.allclose(b2_llr, wrong_factor_two, rtol=0.0, atol=1e-12)


def test_b205_zero_variance_uses_exact_dirac_weights_without_nan():
    b2 = _b2_module()
    x = np.array([1.0 + 3.0j, -1.0 - 3.0j]) / np.sqrt(10.0)
    state = 2
    mean = (1j**state) * x
    y = np.array([mean[0], mean[1] + 1e-15j])

    result = b2.emission_log_weight(
        y,
        state=state,
        x=x,
        mu=1.0,
        n0_hat_cplx=0.0,
    )
    assert result[0] == 0.0
    assert np.isneginf(result[1])
    assert not np.any(np.isnan(result))

    variance = b2.moment_variance(
        c_post_cplx=0.0,
        sigma_e2=0.0,
        e_cal=1.0,
        x=x,
    )
    np.testing.assert_array_equal(variance.v_x, np.zeros(2))


def test_b206_state_permutation_reorders_posterior_without_changing_llr():
    b2 = _b2_module()
    constellation, bits = _gray16_points_and_bits()
    rotations = np.array([1.0, 1.0j, -1.0, -1.0j])
    posterior = np.array([0.07, 0.19, 0.31, 0.43])
    permutation = np.array([2, 0, 3, 1])

    reference = b2.data_llr(
        0.37 - 0.22j, posterior, mu=0.91, n0_hat_cplx=0.38,
        constellation=constellation, bit_labels=bits, state_rotations=rotations,
        output_clip=None,
    )
    permuted = b2.data_llr(
        0.37 - 0.22j, posterior[permutation], mu=0.91,
        n0_hat_cplx=0.38, constellation=constellation, bit_labels=bits,
        state_rotations=rotations[permutation], output_clip=None,
    )
    np.testing.assert_allclose(permuted, reference, rtol=0.0, atol=2e-15)


def test_b206_rejects_nonfinite_state_rotations_instead_of_returning_nan():
    b2 = _b2_module()
    rotations = np.array([1.0, 1.0j, np.nan + 0.0j, -1.0j])
    with pytest.raises(b2.B2MathError, match="state_rotations"):
        b2.data_llr(
            0.1 + 0.2j, np.full(4, 0.25), mu=0.9, n0_hat_cplx=0.3,
            state_rotations=rotations,
        )


def test_b207_received_rotation_inverse_shift_and_coordinate_rotation_covariance():
    b2 = _b2_module()
    constellation, bits = _gray16_points_and_bits()
    posterior = np.array([0.52, 0.11, 0.09, 0.28])
    y = 0.63 - 0.17j
    kwargs = dict(mu=0.87, n0_hat_cplx=0.29, bit_labels=bits, output_clip=None)
    reference = b2.data_llr(y, posterior, constellation=constellation, **kwargs)

    # Rotating received coordinates alone moves old state s to new state s+1;
    # np.roll performs the corresponding inverse lookup of the old labels.
    received_rotated = b2.data_llr(
        1j * y, np.roll(posterior, 1), constellation=constellation, **kwargs
    )
    coordinate_rotated = b2.data_llr(
        1j * y, posterior, constellation=1j * constellation, **kwargs
    )
    np.testing.assert_allclose(received_rotated, reference, rtol=0.0, atol=3e-15)
    np.testing.assert_allclose(coordinate_rotated, reference, rtol=0.0, atol=3e-15)


def test_b208_uniform_state_erases_direction_bits_only():
    b2 = _b2_module()
    constellation, bits = _gray16_points_and_bits()
    llr = b2.data_llr(
        0.84 + 0.16j, np.full(4, 0.25), mu=0.94, n0_hat_cplx=0.21,
        constellation=constellation, bit_labels=bits, output_clip=None,
    )
    np.testing.assert_allclose(llr[[0, 2]], np.zeros(2), rtol=0.0, atol=3e-15)
    assert abs(llr[1]) > 1e-6
    assert llr[1] == pytest.approx(llr[3], abs=3e-15)


def test_b209_nearest_pilots_break_equal_distance_ties_toward_earlier_time():
    b2 = _b2_module()
    pilot_times = np.array([2, 8, 12, 18, 30])
    selected = b2.select_nearest_pilot_indices(10, pilot_times, M=3)
    np.testing.assert_array_equal(selected, np.array([1, 2, 0]))


def test_b210_llr_uses_state_logsumexp_but_symbol_maxlog():
    b2 = _b2_module()
    constellation, bits = _gray16_points_and_bits()
    y = -0.23 + 0.71j
    posterior = np.array([0.13, 0.21, 0.29, 0.37])
    state_terms = np.empty((4, 4))
    for state in range(4):
        emission = b2.emission_log_weight(
            y, state=state, x=constellation, mu=0.83, n0_hat_cplx=0.44
        )
        for bit_index in range(4):
            one = np.max(emission[bits[:, bit_index] == 1])
            zero = np.max(emission[bits[:, bit_index] == 0])
            state_terms[state, bit_index] = one - zero

    def lse(values):
        top = np.max(values)
        return top + np.log(np.sum(np.exp(values - top)))

    expected = []
    log_p = np.log(posterior)
    for bit_index in range(4):
        one = []
        zero = []
        for state in range(4):
            emission = b2.emission_log_weight(
                y, state=state, x=constellation, mu=0.83, n0_hat_cplx=0.44
            )
            one.append(log_p[state] + np.max(emission[bits[:, bit_index] == 1]))
            zero.append(log_p[state] + np.max(emission[bits[:, bit_index] == 0]))
        expected.append(lse(np.array(one)) - lse(np.array(zero)))
    actual = b2.data_llr(
        y, posterior, mu=0.83, n0_hat_cplx=0.44,
        constellation=constellation, bit_labels=bits, output_clip=None,
    )
    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=3e-15)
    assert not np.allclose(actual, np.sum(posterior[:, None] * state_terms, axis=0))


def test_b211_pilot_posterior_is_normalized_truth_free_and_honors_earlier_tie():
    b2 = _b2_module()
    pilot_times = np.array([2, 8, 12, 18])
    known = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2)
    observed = 1j * known
    posterior = b2.pilot_state_posterior(
        10, pilot_times, observed, known, M=2, p_s=0.0,
        mu=1.0, n0_hat_cplx=0.0,
    )
    np.testing.assert_array_equal(posterior, np.array([0.0, 1.0, 0.0, 0.0]))
    assert not hasattr(b2.pilot_state_posterior, "truth")


def test_b212_run_b2_decodes_each_polarization_once_with_fresh_state_only():
    b2 = _b2_module()

    class DecoderSpy:
        def __init__(self):
            self.calls = []

        def decode_fresh(self, llr_cw, *, cw_ids, candidate_id):
            self.calls.append((np.array(llr_cw, copy=True), tuple(cw_ids), candidate_id))
            return {"candidate_id": candidate_id, "shape": np.shape(llr_cw)}

    rng = np.random.default_rng(206212)
    data = rng.normal(size=(2, 6144)) + 1j * rng.normal(size=(2, 6144))
    posterior = rng.random((2, 6144, 4))
    posterior /= posterior.sum(axis=-1, keepdims=True)
    cw_ids = tuple(tuple(f"{pol}-{cw}" for cw in range(16)) for pol in range(2))
    decoder = DecoderSpy()

    result = b2.run_b2(
        data, posterior, codec=decoder, cw_ids_by_polarization=cw_ids,
        mu=0.92, n0_hat_cplx=0.35, candidate_id="B2",
    )
    assert len(decoder.calls) == 2
    assert [call[2] for call in decoder.calls] == ["B2:X", "B2:Y"]
    assert all(call[0].shape == (16, 1536) for call in decoder.calls)
    assert len(result.decode_batches) == 2
    assert result.llr_by_polarization.shape == (2, 6144, 4)
    assert np.max(np.abs(result.llr_by_polarization)) <= 30.0


def test_b212_rejects_nonexact_per_polarization_cw_ids_before_decode():
    b2 = _b2_module()

    class RejectCallSpy:
        def decode_fresh(self, *args, **kwargs):
            raise AssertionError("invalid cw_ids reached decoder")

    data = np.zeros((2, 6144), dtype=np.complex128)
    posterior = np.full((2, 6144, 4), 0.25)
    valid = tuple(f"cw-{index}" for index in range(16))
    invalid_groups = (
        (("only-one",), valid),
        (("duplicate",) * 16, valid),
        (tuple(range(16)), valid),
    )
    for cw_ids in invalid_groups:
        with pytest.raises(b2.B2MathError, match="cw_ids_by_polarization"):
            b2.run_b2(
                data, posterior, codec=RejectCallSpy(),
                cw_ids_by_polarization=cw_ids, mu=1.0,
                n0_hat_cplx=0.2, candidate_id="B2",
            )


def test_b213_zero_variance_all_impossible_pilots_fail_closed_without_warning():
    b2 = _b2_module()
    pilot_times = np.array([2, 8])
    known = np.array([1.0 + 0.0j, 1.0 + 0.0j])
    observed = np.array([0.123 + 0.456j, 0.321 + 0.654j])
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        with pytest.raises(b2.B2MathError, match="all hypotheses are impossible"):
            b2.pilot_state_posterior(
                5, pilot_times, observed, known, M=2, p_s=0.0,
                mu=1.0, n0_hat_cplx=0.0,
            )
    assert not captured


def test_b214_zero_variance_all_impossible_data_llr_fails_closed_without_warning():
    b2 = _b2_module()
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        with pytest.raises(b2.B2MathError, match="all hypotheses are impossible"):
            b2.data_llr(
                0.123 + 0.456j, np.full(4, 0.25),
                mu=1.0, n0_hat_cplx=0.0, output_clip=None,
            )
    assert not captured
