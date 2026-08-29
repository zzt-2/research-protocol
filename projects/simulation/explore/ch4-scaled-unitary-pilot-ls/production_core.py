"""Correctness-frozen production kernel for the Ch4 scaled-unitary receiver."""

from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[4]
SIM_ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from projects.simulation.common import m16apsk_demod, m16apsk_mod  # noqa: E402
from projects.simulation.params import SimulationConfig  # noqa: E402
from scaled_unitary import InvalidEstimate, plain_ls, project_scaled_unitary  # noqa: E402


_ENTROPY = 20260830
_NAMESPACE_PREFIX = (84, 1)
_SCENARIO_CODES = {"weak": 0, "moderate": 1, "strong": 2}
_COMPONENT_CODES = {
    "payload_bits": 0,
    "channel_q": 1,
    "gg_gain": 2,
    "pilot_noise": 3,
    "payload_noise": 4,
    "mismatch_left": 5,
    "mismatch_right": 6,
}
_SUPPORTED_PILOTS = (2, 4, 8, 16)
_TURBULENCE_AUTHORITY = (
    "projects/simulation/params.py::SimulationConfig().turbulence"
)


def _registered_int(value: object, name: str, *, positive: bool = False) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be an integer")
    integer = int(value)
    if positive and integer <= 0:
        raise ValueError(f"{name} must be positive")
    return integer


def _finite_matrix(
    value: object,
    name: str,
    *,
    rows: int = 2,
    columns: int | None = None,
) -> np.ndarray:
    array = np.asarray(value, dtype=np.complex128)
    if array.ndim != 2 or array.shape[0] != rows:
        raise InvalidEstimate(f"{name} must have shape ({rows}, N)")
    if columns is not None and array.shape[1] != columns:
        raise InvalidEstimate(f"{name} column count mismatch")
    if not np.all(np.isfinite(array)):
        raise InvalidEstimate(f"{name} contains NaN or Inf")
    return array


def _hash_arrays(*values: object) -> str:
    digest = hashlib.sha256()
    for value in values:
        array = np.ascontiguousarray(value)
        digest.update(str(array.dtype).encode("ascii"))
        digest.update(struct.pack("<I", array.ndim))
        digest.update(struct.pack(f"<{array.ndim}Q", *array.shape))
        digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def _random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    try:
        q, r = np.linalg.qr(raw)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("unitary QR failed") from error
    diagonal = np.diag(r)
    if np.any(np.abs(diagonal) == 0.0):
        raise InvalidEstimate("unitary QR produced a zero diagonal")
    unitary = q @ np.diag(diagonal / np.abs(diagonal))
    if not np.all(np.isfinite(unitary)):
        raise InvalidEstimate("unitary draw is nonfinite")
    return unitary


def _component_rngs(
    scenario: str, latent_id: int
) -> tuple[dict[str, np.random.Generator], dict[str, dict[str, object]]]:
    scenario_code = _SCENARIO_CODES[scenario]
    rngs: dict[str, np.random.Generator] = {}
    metadata: dict[str, dict[str, object]] = {}
    for name, component_code in _COMPONENT_CODES.items():
        spawn_key = (*_NAMESPACE_PREFIX, scenario_code, latent_id, component_code)
        sequence = np.random.SeedSequence(_ENTROPY, spawn_key=spawn_key)
        rngs[name] = np.random.Generator(np.random.PCG64(sequence))
        metadata[name] = {
            "bit_generator": "PCG64",
            "entropy": _ENTROPY,
            "spawn_key": list(spawn_key),
        }
    return rngs, metadata


def _resolved_turbulence(scenario: str) -> dict[str, object]:
    if scenario not in _SCENARIO_CODES:
        raise ValueError(f"unsupported turbulence scenario: {scenario!r}")
    resolved = SimulationConfig().turbulence.as_dict()
    alpha, beta = resolved[scenario]
    if not (np.isfinite(alpha) and np.isfinite(beta) and alpha > 0 and beta > 0):
        raise InvalidEstimate(f"invalid turbulence authority for {scenario}")
    return {
        "scenario": scenario,
        "alpha": float(alpha),
        "beta": float(beta),
        "scintillation_index": float(1.0 / alpha + 1.0 / beta + 1.0 / (alpha * beta)),
        "authority": _TURBULENCE_AUTHORITY,
    }


def balanced_pilots(n_pilots) -> np.ndarray:
    """Return the frozen balanced pilot matrix for a registered pilot count."""
    count = _registered_int(n_pilots, "n_pilots", positive=True)
    if count == 2:
        return np.array([[1, 1], [1, -1]], dtype=np.complex128)
    if count not in (4, 8, 16):
        raise ValueError(f"unsupported n_pilots: {count}")
    block = np.array(
        [[1, 1, 1, 1], [1, 1j, -1, -1j]], dtype=np.complex128
    )
    return np.tile(block, (1, count // 4))


def make_latent_window(scenario, latent_id, payload_symbols, max_pilots) -> dict:
    """Draw one SNR/Np-independent latent window from named SeedSequence streams."""
    if not isinstance(scenario, str):
        raise ValueError("scenario must be a registered string")
    snapshot = _resolved_turbulence(scenario)
    identifier = _registered_int(latent_id, "latent_id")
    if not 0 <= identifier <= np.iinfo(np.uint32).max:
        raise ValueError("latent_id must fit one SeedSequence spawn-key word")
    payload_count = _registered_int(payload_symbols, "payload_symbols", positive=True)
    maximum = _registered_int(max_pilots, "max_pilots", positive=True)
    if maximum not in _SUPPORTED_PILOTS:
        raise ValueError(f"unsupported max_pilots: {maximum}")

    rngs, namespace = _component_rngs(scenario, identifier)
    bits = rngs["payload_bits"].integers(
        0, 2, size=(2, 4 * payload_count), dtype=np.int8
    )
    x_payload = np.vstack([m16apsk_mod(bits[polarization]) for polarization in range(2)])
    q = _random_unitary(rngs["channel_q"])
    alpha = float(snapshot["alpha"])
    beta = float(snapshot["beta"])
    irradiance = float(
        rngs["gg_gain"].gamma(alpha, 1.0 / alpha)
        * rngs["gg_gain"].gamma(beta, 1.0 / beta)
    )
    gain = float(np.sqrt(irradiance))
    if not np.isfinite(gain) or gain <= 0.0:
        raise InvalidEstimate("Gamma-Gamma gain is invalid")
    pilot_noise = (
        rngs["pilot_noise"].normal(size=(2, maximum))
        + 1j * rngs["pilot_noise"].normal(size=(2, maximum))
    ).astype(np.complex128)
    payload_noise = (
        rngs["payload_noise"].normal(size=x_payload.shape)
        + 1j * rngs["payload_noise"].normal(size=x_payload.shape)
    ).astype(np.complex128)
    mismatch_left = _random_unitary(rngs["mismatch_left"])
    mismatch_right = _random_unitary(rngs["mismatch_right"])
    h_true = gain * q
    latent_hashes = {
        "payload_bits": _hash_arrays(bits),
        "channel_q": _hash_arrays(q),
        "gg_gain": _hash_arrays(np.array([gain], dtype=np.float64)),
        "pilot_noise": _hash_arrays(pilot_noise),
        "payload_noise": _hash_arrays(payload_noise),
        "mismatch_left": _hash_arrays(mismatch_left),
        "mismatch_right": _hash_arrays(mismatch_right),
    }
    return {
        "scenario": scenario,
        "latent_id": identifier,
        "payload_symbols": payload_count,
        "max_pilots": maximum,
        "turbulence": snapshot,
        "rng_namespace": namespace,
        "bits": bits,
        "x_payload": x_payload,
        "q": q,
        "gain": gain,
        "h_true": h_true,
        "pilot_noise": pilot_noise,
        "payload_noise": payload_noise,
        "mismatch_left": mismatch_left,
        "mismatch_right": mismatch_right,
        "latent_hashes": latent_hashes,
    }


def _validated_latent(latent: object) -> dict[str, Any]:
    if not isinstance(latent, dict):
        raise InvalidEstimate("latent must be a dictionary")
    required = {
        "scenario",
        "latent_id",
        "payload_symbols",
        "max_pilots",
        "turbulence",
        "rng_namespace",
        "bits",
        "x_payload",
        "q",
        "gain",
        "h_true",
        "pilot_noise",
        "payload_noise",
        "mismatch_left",
        "mismatch_right",
        "latent_hashes",
    }
    if not required.issubset(latent):
        raise InvalidEstimate("latent schema is incomplete")
    scenario = latent["scenario"]
    if not isinstance(scenario, str) or scenario not in _SCENARIO_CODES:
        raise InvalidEstimate("latent scenario is invalid")
    try:
        identifier = _registered_int(latent["latent_id"], "latent_id")
    except ValueError as error:
        raise InvalidEstimate("latent_id is invalid") from error
    if not 0 <= identifier <= np.iinfo(np.uint32).max:
        raise InvalidEstimate("latent_id must fit one SeedSequence spawn-key word")
    _, expected_namespace = _component_rngs(scenario, identifier)
    actual_namespace = latent["rng_namespace"]
    if not isinstance(actual_namespace, dict) or set(actual_namespace) != set(
        expected_namespace
    ):
        raise InvalidEstimate("latent RNG namespace component set is invalid")
    for name, expected_metadata in expected_namespace.items():
        actual_metadata = actual_namespace[name]
        if (
            not isinstance(actual_metadata, dict)
            or set(actual_metadata) != set(expected_metadata)
            or actual_metadata["bit_generator"] != expected_metadata["bit_generator"]
            or actual_metadata["entropy"] != expected_metadata["entropy"]
            or not isinstance(actual_metadata["spawn_key"], list)
            or actual_metadata["spawn_key"] != expected_metadata["spawn_key"]
        ):
            raise InvalidEstimate(f"latent RNG namespace is invalid for {name}")
    expected_turbulence = _resolved_turbulence(scenario)
    actual_turbulence = latent["turbulence"]
    if (
        not isinstance(actual_turbulence, dict)
        or set(actual_turbulence) != set(expected_turbulence)
        or any(
            actual_turbulence[field] != expected_value
            for field, expected_value in expected_turbulence.items()
        )
    ):
        raise InvalidEstimate("latent turbulence authority snapshot is invalid")
    maximum = _registered_int(latent["max_pilots"], "max_pilots", positive=True)
    payload_count = _registered_int(
        latent["payload_symbols"], "payload_symbols", positive=True
    )
    if maximum not in _SUPPORTED_PILOTS:
        raise InvalidEstimate("latent max_pilots is unsupported")
    bits = np.asarray(latent["bits"])
    if bits.shape != (2, 4 * payload_count) or not np.all((bits == 0) | (bits == 1)):
        raise InvalidEstimate("latent payload bits are invalid")
    x_payload = _finite_matrix(
        latent["x_payload"], "x_payload", columns=payload_count
    )
    q = _finite_matrix(latent["q"], "q", columns=2)
    h_true = _finite_matrix(latent["h_true"], "h_true", columns=2)
    pilot_noise = _finite_matrix(
        latent["pilot_noise"], "pilot_noise", columns=maximum
    )
    payload_noise = _finite_matrix(
        latent["payload_noise"], "payload_noise", columns=payload_count
    )
    mismatch_left = _finite_matrix(latent["mismatch_left"], "mismatch_left", columns=2)
    mismatch_right = _finite_matrix(
        latent["mismatch_right"], "mismatch_right", columns=2
    )
    gain = float(latent["gain"])
    if not np.isfinite(gain) or gain <= 0.0:
        raise InvalidEstimate("latent gain is invalid")
    if not np.allclose(q.conj().T @ q, np.eye(2), atol=2e-12):
        raise InvalidEstimate("latent channel_q is not unitary")
    if not np.allclose(h_true, gain * q, atol=2e-12):
        raise InvalidEstimate("latent channel identity is inconsistent")
    for name, matrix in (
        ("mismatch_left", mismatch_left),
        ("mismatch_right", mismatch_right),
    ):
        if not np.allclose(matrix.conj().T @ matrix, np.eye(2), atol=2e-12):
            raise InvalidEstimate(f"latent {name} is not unitary")
    expected_hashes = {
        "payload_bits": _hash_arrays(bits),
        "channel_q": _hash_arrays(q),
        "gg_gain": _hash_arrays(np.array([gain], dtype=np.float64)),
        "pilot_noise": _hash_arrays(pilot_noise),
        "payload_noise": _hash_arrays(payload_noise),
        "mismatch_left": _hash_arrays(mismatch_left),
        "mismatch_right": _hash_arrays(mismatch_right),
    }
    if latent["latent_hashes"] != expected_hashes:
        raise InvalidEstimate("latent hashes do not match latent values")
    return latent


def observe_latent(latent, snr_db, n_pilots) -> dict:
    """Apply one analytic SNR scale and one frozen pilot prefix to a latent window."""
    window = _validated_latent(latent)
    count = _registered_int(n_pilots, "n_pilots", positive=True)
    if count not in _SUPPORTED_PILOTS or count > int(window["max_pilots"]):
        raise ValueError(f"unsupported n_pilots for latent: {count}")
    try:
        snr = float(snr_db)
    except (TypeError, ValueError) as error:
        raise ValueError("snr_db must be finite") from error
    if not np.isfinite(snr):
        raise ValueError("snr_db must be finite")
    noise_scale = float(np.sqrt(10.0 ** (-snr / 10.0) / 2.0))
    if not np.isfinite(noise_scale) or noise_scale <= 0.0:
        raise InvalidEstimate("analytic noise scale is invalid")
    x_pilots = balanced_pilots(count)
    pilot_noise = np.asarray(window["pilot_noise"])[:, :count].copy()
    payload_noise = np.asarray(window["payload_noise"]).copy()
    y_pilots = window["h_true"] @ x_pilots + noise_scale * pilot_noise
    y_payload = window["h_true"] @ window["x_payload"] + noise_scale * payload_noise
    if not (np.all(np.isfinite(y_pilots)) and np.all(np.isfinite(y_payload))):
        raise InvalidEstimate("observation is nonfinite")
    return {
        "scenario": window["scenario"],
        "latent_id": int(window["latent_id"]),
        "snr_db": snr,
        "n_pilots": count,
        "noise_scale": noise_scale,
        "x_pilots": x_pilots,
        "y_pilots": y_pilots,
        "y_payload": y_payload,
        "pilot_noise": pilot_noise,
        "latent_hashes": dict(window["latent_hashes"]),
        "observation_hashes": {
            "x_pilots": _hash_arrays(x_pilots),
            "y_pilots": _hash_arrays(y_pilots),
            "y_payload": _hash_arrays(y_payload),
        },
    }


def _invert_exact(h_hat: np.ndarray) -> np.ndarray:
    if np.linalg.det(h_hat) == 0.0:
        raise InvalidEstimate("receiver estimate is exactly rank deficient")
    try:
        inverse = np.linalg.inv(h_hat)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("receiver inverse failed") from error
    if not np.all(np.isfinite(inverse)):
        raise InvalidEstimate("receiver inverse is nonfinite")
    return inverse


def _tau(parameter: object, arm: str) -> float:
    if isinstance(parameter, (bool, np.bool_)) or parameter is None:
        raise ValueError(f"{arm} requires tau in [0,1]")
    try:
        tau = float(parameter)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{arm} requires tau in [0,1]") from error
    if not np.isfinite(tau) or not 0.0 <= tau <= 1.0:
        raise ValueError(f"{arm} requires tau in [0,1]")
    return tau


def _pilot_scalar_calibration(
    w: np.ndarray, x_pilots: np.ndarray, y_pilots: np.ndarray
) -> float:
    receiver = _finite_matrix(w, "w", columns=2)
    x = _finite_matrix(x_pilots, "x_pilots")
    y = _finite_matrix(y_pilots, "y_pilots", columns=x.shape[1])
    with np.errstate(over="ignore", invalid="ignore", under="ignore"):
        z_pilots = receiver @ y
        denominator = float(np.vdot(z_pilots, z_pilots).real)
        numerator = float(np.real(np.vdot(z_pilots, x)))
    if not np.isfinite(denominator) or denominator <= 0.0:
        raise InvalidEstimate("B3_PSC denominator is nonpositive or nonfinite")
    if not np.isfinite(numerator):
        raise InvalidEstimate("B3_PSC numerator is nonfinite")
    scalar = max(0.0, numerator / denominator)
    if not np.isfinite(scalar):
        raise InvalidEstimate("B3_PSC scalar is nonfinite")
    return float(scalar)


def receiver_action(arm, x_pilots, y_pilots, y_payload, parameter) -> dict:
    """Run one registered observation-only receiver arm."""
    if not isinstance(arm, str) or arm not in {"B0", "B2", "B3_PSC", "C4"}:
        raise ValueError(f"unsupported receiver arm: {arm!r}")
    x = _finite_matrix(x_pilots, "x_pilots")
    y_p = _finite_matrix(y_pilots, "y_pilots", columns=x.shape[1])
    y = _finite_matrix(y_payload, "y_payload")
    h_ls = plain_ls(x, y_p)
    try:
        u, singular_values, vh = np.linalg.svd(h_ls, full_matrices=False)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("receiver SVD failed") from error
    if singular_values[1] <= 0.0 or not np.all(np.isfinite(singular_values)):
        raise InvalidEstimate("receiver estimate is rank deficient or nonfinite")
    rho = float(singular_values[0] / singular_values[1])
    psc_scale = 1.0

    if arm == "B0":
        if parameter is not None:
            raise ValueError("B0 has no parameter")
        h_hat = h_ls
        w = _invert_exact(h_hat)
        scale = None
    elif arm in {"B2", "B3_PSC"}:
        tau = _tau(parameter, arm)
        floor = tau * float(singular_values[0])
        floored = np.maximum(singular_values, floor)
        if floored[1] <= 0.0:
            raise InvalidEstimate(f"{arm} has an exact zero singular value")
        h_hat = (u * floored) @ vh
        w = (vh.conj().T * (1.0 / floored)) @ u.conj().T
        scale = float(floored[0]) if tau == 1.0 else None
        if arm == "B3_PSC":
            psc_scale = _pilot_scalar_calibration(w, x, y_p)
            w = psc_scale * w
    else:
        if parameter is not None:
            raise ValueError("C4 has no parameter")
        projection = project_scaled_unitary(h_ls)
        h_hat = projection.h_projected
        w = projection.w
        rho = projection.rho
        scale = projection.g_hat

    z = w @ y
    finite_scalars = (rho, psc_scale)
    if scale is not None:
        finite_scalars = (*finite_scalars, scale)
    if not (
        np.all(np.isfinite(z))
        and np.all(np.isfinite(h_hat))
        and np.all(np.isfinite(w))
        and all(np.isfinite(value) for value in finite_scalars)
    ):
        raise InvalidEstimate(f"{arm} produced a nonfinite action")
    return {
        "arm": arm,
        "z": z,
        "h_hat": h_hat,
        "w": w,
        "rho": float(rho),
        "singular_values": singular_values.copy(),
        "scale": None if scale is None else float(scale),
        "psc_scale": float(psc_scale),
    }


def score_action(action, bits, h_true) -> dict:
    """Score a frozen action offline; hidden quantities enter only here."""
    if not isinstance(action, dict) or not {"z", "h_hat", "w", "rho"}.issubset(action):
        raise InvalidEstimate("action schema is incomplete")
    z = _finite_matrix(action["z"], "action.z")
    h_hat = _finite_matrix(action["h_hat"], "action.h_hat", columns=2)
    w = _finite_matrix(action["w"], "action.w", columns=2)
    channel = _finite_matrix(h_true, "h_true", columns=2)
    channel_power = float(np.linalg.norm(channel) ** 2)
    if not np.isfinite(channel_power) or channel_power <= 0.0:
        raise InvalidEstimate("h_true has nonpositive or nonfinite power")
    payload_bits = np.asarray(bits)
    if (
        payload_bits.shape != (2, 4 * z.shape[1])
        or not np.all((payload_bits == 0) | (payload_bits == 1))
    ):
        raise InvalidEstimate("payload bits do not match action symbols")
    decided = np.vstack([m16apsk_demod(z[polarization]) for polarization in range(2)])
    bit_errors = int(np.count_nonzero(decided != payload_bits))
    bit_count = int(payload_bits.size)
    channel_nmse = float(np.linalg.norm(h_hat - channel) ** 2 / channel_power)
    inverse_residual = float(np.linalg.norm(w @ channel - np.eye(2)) ** 2 / 2.0)
    rho = float(action["rho"])
    metrics = (bit_errors / bit_count, channel_nmse, inverse_residual, rho)
    if not all(np.isfinite(value) for value in metrics):
        raise InvalidEstimate("offline metric is nonfinite")
    return {
        "bit_errors": bit_errors,
        "payload_bits": bit_count,
        "ber": float(bit_errors / bit_count),
        "channel_nmse": channel_nmse,
        "inverse_residual": inverse_residual,
        "rho": rho,
    }


def structure_mismatch_matrix(left, right, delta) -> np.ndarray:
    """Return ``g U D_delta V^H`` with ``g U`` supplied as ``left``."""
    l_factor = _finite_matrix(left, "left", columns=2)
    r_factor = _finite_matrix(right, "right", columns=2)
    try:
        mismatch = float(delta)
    except (TypeError, ValueError) as error:
        raise ValueError("delta must be finite and in [0,1)") from error
    if not np.isfinite(mismatch) or not 0.0 <= mismatch < 1.0:
        raise ValueError("delta must be finite and in [0,1)")
    left_gram = l_factor.conj().T @ l_factor
    gain_squared = float(np.trace(left_gram).real / 2.0)
    if not np.isfinite(gain_squared) or gain_squared <= 0.0:
        raise InvalidEstimate("left factor has invalid gain")
    if not np.allclose(
        left_gram, gain_squared * np.eye(2), rtol=2e-12, atol=2e-12
    ):
        raise InvalidEstimate("left must be a positive scale times a unitary matrix")
    if not np.allclose(
        r_factor.conj().T @ r_factor, np.eye(2), rtol=2e-12, atol=2e-12
    ):
        raise InvalidEstimate("right must be unitary")
    diagonal = np.diag([1.0 + mismatch, 1.0 - mismatch]) / np.sqrt(
        1.0 + mismatch**2
    )
    result = l_factor @ diagonal @ r_factor.conj().T
    if not np.all(np.isfinite(result)):
        raise InvalidEstimate("mismatch matrix is nonfinite")
    return result
