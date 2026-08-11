"""Four-state B2 transition, variance, and emission primitives for D0."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Sequence

import numpy as np


class B2MathError(ValueError):
    """Raised when a frozen B2 mathematical input is invalid."""


def _finite_nonnegative(value: Any, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be a finite non-negative number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a finite non-negative number") from exc
    if not math.isfinite(result) or result < 0.0:
        raise B2MathError(f"{name} must be a finite non-negative number")
    return result


def _distance(value: Any) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, np.integer)
    ):
        raise TypeError("distance must be a non-negative integer")
    result = int(value)
    if result < 0:
        raise B2MathError("distance must be a non-negative integer")
    return result


def _state(value: Any) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (int, np.integer)
    ):
        raise TypeError("state must be an integer")
    result = int(value)
    if result not in (0, 1, 2, 3):
        raise B2MathError("state must be one of 0,1,2,3")
    return result


def transition_matrix(p_s: float, *, distance: int = 1) -> np.ndarray:
    """Return the frozen four-state transition raised to symbol distance."""
    probability = _finite_nonnegative(p_s, "p_s")
    if probability > 1.0:
        raise B2MathError("p_s must not exceed one")
    steps = _distance(distance)
    q = 1.0 - math.sqrt(1.0 - probability)
    q_distance = (1.0 - (1.0 - 2.0 * q) ** steps) / 2.0
    stay = (1.0 - q_distance) ** 2
    adjacent = q_distance * (1.0 - q_distance)
    opposite = q_distance**2
    result = np.array(
        [
            [stay, adjacent, opposite, adjacent],
            [adjacent, stay, adjacent, opposite],
            [opposite, adjacent, stay, adjacent],
            [adjacent, opposite, adjacent, stay],
        ],
        dtype=np.float64,
    )
    result.setflags(write=False)
    return result


def log_transition_matrix(p_s: float, *, distance: int = 1) -> np.ndarray:
    """Return exact log probabilities, retaining impossible paths as ``-inf``."""
    probability = transition_matrix(p_s, distance=distance)
    result = np.full((4, 4), -np.inf, dtype=np.float64)
    positive = probability > 0.0
    result[positive] = np.log(probability[positive])
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class B2Variance:
    mu: float
    n0_hat_cplx: float
    noise_var_real: float
    v_x: np.ndarray


def moment_variance(
    *,
    c_post_cplx: float,
    sigma_e2: float,
    e_cal: float,
    x: Any,
) -> B2Variance:
    """Split prefix residual power once, then form the symbol-dependent variance."""
    residual_power = _finite_nonnegative(c_post_cplx, "c_post_cplx")
    phase_variance = _finite_nonnegative(sigma_e2, "sigma_e2")
    calibration_energy = _finite_nonnegative(e_cal, "e_cal")
    symbols = np.asarray(x, dtype=np.complex128)
    if not np.all(np.isfinite(symbols)):
        raise B2MathError("x must contain finite symbols")

    mu = math.exp(-phase_variance / 2.0)
    n0_hat_cplx = max(
        0.0,
        residual_power - 2.0 * (1.0 - mu) * calibration_energy,
    )
    v_x = np.asarray(
        n0_hat_cplx + np.abs(symbols) ** 2 * (1.0 - mu**2),
        dtype=np.float64,
    )
    if not np.all(np.isfinite(v_x)) or np.any(v_x < 0.0):
        raise B2MathError("derived symbol variance must be finite and non-negative")
    v_x.setflags(write=False)
    return B2Variance(
        mu=mu,
        n0_hat_cplx=n0_hat_cplx,
        noise_var_real=n0_hat_cplx / 2.0,
        v_x=v_x,
    )


def emission_log_weight(
    y: Any,
    *,
    state: int,
    x: Any,
    mu: float,
    n0_hat_cplx: float,
) -> float | np.ndarray:
    """Evaluate the Gaussian emission or its exact zero-variance Dirac branch."""
    state_value = _state(state)
    mean_scale = _finite_nonnegative(mu, "mu")
    if mean_scale > 1.0:
        raise B2MathError("mu must not exceed one")
    noise_power = _finite_nonnegative(n0_hat_cplx, "n0_hat_cplx")
    observations = np.asarray(y, dtype=np.complex128)
    symbols = np.asarray(x, dtype=np.complex128)
    if not np.all(np.isfinite(observations)):
        raise B2MathError("y must contain finite observations")
    if not np.all(np.isfinite(symbols)):
        raise B2MathError("x must contain finite symbols")

    means = mean_scale * (1j**state_value) * symbols
    variances = noise_power + np.abs(symbols) ** 2 * (1.0 - mean_scale**2)
    observations, means, variances = np.broadcast_arrays(
        observations, means, variances
    )
    result = np.full(observations.shape, -np.inf, dtype=np.float64)
    positive = variances > 0.0
    result[positive] = (
        -np.abs(observations[positive] - means[positive]) ** 2
        / variances[positive]
        - np.log(np.pi * variances[positive])
    )
    zero = ~positive
    result[zero & (observations == means)] = 0.0
    if np.any(np.isnan(result)):
        raise RuntimeError("B2 emission produced NaN")
    if result.ndim == 0:
        return float(result)
    result.setflags(write=False)
    return result


def _logsumexp(values: np.ndarray, *, axis: int) -> np.ndarray:
    """Stable log-sum-exp that preserves an exact all-impossible branch."""
    array = np.asarray(values, dtype=np.float64)
    top = np.max(array, axis=axis, keepdims=True)
    finite = np.isfinite(top)
    shifted = np.full(array.shape, -np.inf, dtype=np.float64)
    np.subtract(array, top, out=shifted, where=np.broadcast_to(finite, array.shape))
    total = np.sum(np.exp(shifted), axis=axis, keepdims=True)
    log_total = np.full(total.shape, -np.inf, dtype=np.float64)
    np.log(total, out=log_total, where=total > 0.0)
    result = np.full(top.shape, -np.inf, dtype=np.float64)
    np.add(top, log_total, out=result, where=finite)
    return np.squeeze(result, axis=axis)


def _require_possible(log_mass: np.ndarray, *, context: str) -> np.ndarray:
    if np.any(~np.isfinite(log_mass)):
        raise B2MathError(f"{context}: all hypotheses are impossible")
    return log_mass


def select_nearest_pilot_indices(
    query_time: int, pilot_times: Any, *, M: int
) -> np.ndarray:
    """Select nearest pilots, resolving equal distance toward earlier time."""
    query = _distance(query_time)
    times = np.asarray(pilot_times)
    if times.ndim != 1 or times.size == 0 or not np.issubdtype(times.dtype, np.integer):
        raise B2MathError("pilot_times must be a non-empty integer vector")
    times = times.astype(np.int64, copy=False)
    if np.any(times < 0) or len(np.unique(times)) != times.size:
        raise B2MathError("pilot_times must be unique and non-negative")
    if isinstance(M, (bool, np.bool_)) or not isinstance(M, (int, np.integer)):
        raise TypeError("M must be an integer")
    count = int(M)
    if count <= 0 or count > times.size:
        raise B2MathError("M must select between one and all pilots")
    order = np.lexsort((times, np.abs(times - query)))[:count]
    result = np.asarray(order, dtype=np.int64)
    result.setflags(write=False)
    return result


def pilot_state_posterior(
    query_time: int,
    pilot_times: Any,
    received_pilots: Any,
    known_pilots: Any,
    *,
    M: int,
    p_s: float,
    mu: float,
    n0_hat_cplx: float,
) -> np.ndarray:
    """Infer the four-state query posterior from receiver-visible pilots only."""
    query = _distance(query_time)
    times = np.asarray(pilot_times)
    observed = np.asarray(received_pilots, dtype=np.complex128)
    known = np.asarray(known_pilots, dtype=np.complex128)
    if (
        times.ndim != 1
        or observed.shape != times.shape
        or known.shape != times.shape
        or not np.all(np.isfinite(observed))
        or not np.all(np.isfinite(known))
    ):
        raise B2MathError("pilot inputs must be aligned finite vectors")
    selected = select_nearest_pilot_indices(query, times, M=M)
    nodes = [(int(times[index]), int(index)) for index in selected]
    if any(time == query for time, _ in nodes):
        raise B2MathError("query_time must identify a data position, not a pilot")
    nodes.append((query, -1))
    nodes.sort(key=lambda item: item[0])
    query_index = next(i for i, (_, index) in enumerate(nodes) if index == -1)

    emissions = np.zeros((len(nodes), 4), dtype=np.float64)
    for node_index, (_, pilot_index) in enumerate(nodes):
        if pilot_index >= 0:
            for state in range(4):
                emissions[node_index, state] = emission_log_weight(
                    observed[pilot_index], state=state, x=known[pilot_index],
                    mu=mu, n0_hat_cplx=n0_hat_cplx,
                )

    alpha = np.full_like(emissions, -np.inf)
    alpha[0] = math.log(0.25) + emissions[0]
    alpha[0] -= _require_possible(
        _logsumexp(alpha[0], axis=0), context="pilot posterior")
    for index in range(1, len(nodes)):
        distance = nodes[index][0] - nodes[index - 1][0]
        transition = log_transition_matrix(p_s, distance=distance)
        alpha[index] = emissions[index] + _logsumexp(
            alpha[index - 1][:, None] + transition, axis=0
        )
        alpha[index] -= _require_possible(
            _logsumexp(alpha[index], axis=0), context="pilot posterior")

    beta = np.zeros_like(emissions)
    for index in range(len(nodes) - 2, -1, -1):
        distance = nodes[index + 1][0] - nodes[index][0]
        transition = log_transition_matrix(p_s, distance=distance)
        beta[index] = _logsumexp(
            transition + emissions[index + 1][None, :] + beta[index + 1][None, :],
            axis=1,
        )
        beta[index] -= _require_possible(
            _logsumexp(beta[index], axis=0), context="pilot posterior")

    log_posterior = alpha[query_index] + beta[query_index]
    log_posterior -= _require_possible(
        _logsumexp(log_posterior, axis=0), context="pilot posterior")
    posterior = np.exp(log_posterior)
    posterior[posterior == 0.0] = 0.0
    posterior.setflags(write=False)
    return posterior


def _gray16_constellation() -> tuple[np.ndarray, np.ndarray]:
    labels = np.arange(16, dtype=np.uint8)
    weights = np.array([8, 4, 2, 1], dtype=np.uint8)
    bits = ((labels[:, None] & weights) != 0).astype(np.uint8)
    axis = np.array([-3.0, -1.0, 3.0, 1.0], dtype=np.float64) / math.sqrt(10.0)
    constellation = axis[2 * bits[:, 0] + bits[:, 1]] + 1j * axis[
        2 * bits[:, 2] + bits[:, 3]
    ]
    return constellation, bits


def data_llr(
    y: Any,
    state_posterior: Any,
    *,
    mu: float,
    n0_hat_cplx: float,
    constellation: Any | None = None,
    bit_labels: Any | None = None,
    state_rotations: Any | None = None,
    output_clip: float | None = 30.0,
) -> np.ndarray:
    """Return P08-inner-max-log LLRs exactly marginalized across B2 states."""
    observations = np.asarray(y, dtype=np.complex128)
    scalar = observations.ndim == 0
    if observations.ndim > 1 or not np.all(np.isfinite(observations)):
        raise B2MathError("y must be a finite scalar or vector")
    observations = observations.reshape(-1)
    posterior = np.asarray(state_posterior, dtype=np.float64)
    if posterior.shape == (4,):
        posterior = np.broadcast_to(posterior, (observations.size, 4))
    if posterior.shape != (observations.size, 4):
        raise B2MathError("state_posterior must have shape (4,) or (len(y),4)")
    if not np.all(np.isfinite(posterior)) or np.any(posterior < 0.0):
        raise B2MathError("state_posterior must be finite and non-negative")
    totals = posterior.sum(axis=1, keepdims=True)
    if np.any(totals <= 0.0):
        raise B2MathError("state_posterior rows must have positive mass")
    posterior = posterior / totals

    default_constellation, default_bits = _gray16_constellation()
    symbols = np.asarray(
        default_constellation if constellation is None else constellation,
        dtype=np.complex128,
    )
    bits = np.asarray(default_bits if bit_labels is None else bit_labels)
    rotations = np.asarray(
        np.array([1.0, 1.0j, -1.0, -1.0j])
        if state_rotations is None else state_rotations,
        dtype=np.complex128,
    )
    if symbols.shape != (16,) or bits.shape != (16, 4) or rotations.shape != (4,):
        raise B2MathError("constellation/bit_labels/state_rotations have invalid shape")
    if not np.all(np.isfinite(rotations)):
        raise B2MathError("state_rotations must contain finite complex values")
    if not np.all((bits == 0) | (bits == 1)) or not np.all(np.isfinite(symbols)):
        raise B2MathError("constellation labels must be finite and binary")

    mean_scale = _finite_nonnegative(mu, "mu")
    noise_power = _finite_nonnegative(n0_hat_cplx, "n0_hat_cplx")
    if mean_scale > 1.0:
        raise B2MathError("mu must not exceed one")
    means = mean_scale * rotations[None, :, None] * symbols[None, None, :]
    variances = noise_power + np.abs(symbols) ** 2 * (1.0 - mean_scale**2)
    residual = observations[:, None, None] - means
    emission = np.full(residual.shape, -np.inf, dtype=np.float64)
    positive = variances > 0.0
    emission[..., positive] = (
        -np.abs(residual[..., positive]) ** 2 / variances[positive]
        - np.log(np.pi * variances[positive])
    )
    if np.any(~positive):
        emission[..., ~positive] = np.where(residual[..., ~positive] == 0.0, 0.0, -np.inf)
    log_p = np.full(posterior.shape, -np.inf, dtype=np.float64)
    active = posterior > 0.0
    log_p[active] = np.log(posterior[active])
    result = np.empty((observations.size, 4), dtype=np.float64)
    for bit_index in range(4):
        one_metric = np.max(emission[..., bits[:, bit_index] == 1], axis=-1)
        zero_metric = np.max(emission[..., bits[:, bit_index] == 0], axis=-1)
        one_log_mass = _require_possible(
            _logsumexp(log_p + one_metric, axis=1), context="data LLR bit partition")
        zero_log_mass = _require_possible(
            _logsumexp(log_p + zero_metric, axis=1), context="data LLR bit partition")
        result[:, bit_index] = one_log_mass - zero_log_mass
    if output_clip is not None:
        clip = _finite_nonnegative(output_clip, "output_clip")
        result = np.clip(result, -clip, clip)
    result.setflags(write=False)
    return result[0] if scalar else result


@dataclass(frozen=True, slots=True)
class B2RunResult:
    llr_by_polarization: np.ndarray
    decode_batches: tuple[Any, Any]


def run_b2(
    data_samples_by_polarization: Any,
    state_posterior_by_polarization: Any,
    *,
    codec: Any,
    cw_ids_by_polarization: Sequence[Sequence[str]],
    mu: float,
    n0_hat_cplx: float,
    candidate_id: str = "B2",
) -> B2RunResult:
    """Form B2 LLRs and make exactly one fresh LDPC call per polarization."""
    samples = np.asarray(data_samples_by_polarization, dtype=np.complex128)
    posterior = np.asarray(state_posterior_by_polarization, dtype=np.float64)
    if samples.shape != (2, 6144) or posterior.shape != (2, 6144, 4):
        raise B2MathError("B2 requires two polarizations of exactly 6144 data symbols")
    if len(cw_ids_by_polarization) != 2:
        raise B2MathError("cw_ids_by_polarization must contain X and Y batches")
    cw_ids = tuple(tuple(group) for group in cw_ids_by_polarization)
    for group in cw_ids:
        if (
            len(group) != 16
            or any(type(value) is not str or not value for value in group)
            or len(set(group)) != 16
        ):
            raise B2MathError(
                "cw_ids_by_polarization must contain two exact batches of "
                "16 unique non-empty string IDs"
            )
    if not isinstance(candidate_id, str) or not candidate_id:
        raise B2MathError("candidate_id must be a non-empty string")

    llr_by_pol = np.empty((2, 6144, 4), dtype=np.float64)
    decoded: list[Any] = []
    for pol_index, pol_name in enumerate(("X", "Y")):
        llr = data_llr(
            samples[pol_index], posterior[pol_index], mu=mu,
            n0_hat_cplx=n0_hat_cplx, output_clip=30.0,
        )
        llr_by_pol[pol_index] = llr
        decoded.append(
            codec.decode_fresh(
                llr.reshape(16, 1536),
                cw_ids=cw_ids[pol_index],
                candidate_id=f"{candidate_id}:{pol_name}",
            )
        )
    llr_by_pol.setflags(write=False)
    return B2RunResult(llr_by_pol, (decoded[0], decoded[1]))


__all__ = [
    "B2MathError", "B2RunResult", "B2Variance", "data_llr",
    "emission_log_weight", "log_transition_matrix", "moment_variance",
    "pilot_state_posterior", "run_b2", "select_nearest_pilot_indices",
    "transition_matrix",
]
