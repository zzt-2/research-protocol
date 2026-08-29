"""Frozen T069 signal generation, receiver ladder, and offline scoring."""

from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path
from typing import NamedTuple

import numpy as np


ROOT = Path(__file__).resolve().parents[4]
SIM_ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from projects.simulation.common import m16apsk_demod, m16apsk_mod  # noqa: E402
from scaled_unitary import InvalidEstimate, plain_ls, project_scaled_unitary  # noqa: E402


class ReceiverAction(NamedTuple):
    z: np.ndarray
    h_hat: np.ndarray
    w: np.ndarray
    rho: float


def balanced_pilots(n_pilots: int) -> np.ndarray:
    """Return the exact manifest pilot matrix."""
    if n_pilots == 2:
        return np.array([[1, 1], [1, -1]], dtype=np.complex128)
    if n_pilots == 4:
        return np.array(
            [[1, 1, 1, 1], [1, 1j, -1, -1j]], dtype=np.complex128
        )
    raise ValueError("T069 only registers Np in {2,4}")


def _random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    return q @ np.diag(diagonal / np.abs(diagonal))


def _hash_arrays(*values: object) -> str:
    digest = hashlib.sha256()
    for value in values:
        array = np.ascontiguousarray(value)
        digest.update(str(array.dtype).encode("ascii"))
        digest.update(struct.pack("<I", array.ndim))
        digest.update(struct.pack(f"<{array.ndim}Q", *array.shape))
        digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def make_realization(
    snr_db: float, n_pilots: int, seed: int, payload_symbols_per_polarization: int
) -> dict[str, object]:
    """Generate one paired static-channel window from a single PCG64 stream."""
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    x_pilots = balanced_pilots(int(n_pilots))
    bits = rng.integers(
        0,
        2,
        size=(2, 4 * int(payload_symbols_per_polarization)),
        dtype=np.int8,
    )
    x_payload = np.vstack([m16apsk_mod(bits[pol]) for pol in range(2)])
    q = _random_unitary(rng)
    irradiance = float(rng.gamma(4.0, 1.0 / 4.0) * rng.gamma(1.9, 1.0 / 1.9))
    gain = float(np.sqrt(irradiance))
    h_true = gain * q
    noise_variance = float(10.0 ** (-float(snr_db) / 10.0))
    noise_scale = np.sqrt(noise_variance / 2.0)
    pilot_noise = noise_scale * (
        rng.normal(size=x_pilots.shape) + 1j * rng.normal(size=x_pilots.shape)
    )
    payload_noise = noise_scale * (
        rng.normal(size=x_payload.shape) + 1j * rng.normal(size=x_payload.shape)
    )
    y_pilots = h_true @ x_pilots + pilot_noise
    y_payload = h_true @ x_payload + payload_noise
    realization_hash = _hash_arrays(
        np.array([snr_db, n_pilots, seed, gain], dtype=np.float64),
        bits,
        x_pilots,
        x_payload,
        q,
        pilot_noise,
        payload_noise,
    )
    observation_hash = _hash_arrays(x_pilots, y_pilots, y_payload)
    return {
        "seed": int(seed),
        "snr_db": float(snr_db),
        "n_pilots": int(n_pilots),
        "bits": bits,
        "x_pilots": x_pilots,
        "y_pilots": y_pilots,
        "y_payload": y_payload,
        "h_true": h_true,
        "gain": gain,
        "realization_hash": realization_hash,
        "observation_hash": observation_hash,
    }


def _invert_exact(h_hat: np.ndarray) -> np.ndarray:
    if np.linalg.det(h_hat) == 0.0:
        raise InvalidEstimate("receiver estimate is exactly rank deficient")
    try:
        w = np.linalg.inv(h_hat)
    except np.linalg.LinAlgError as error:
        raise InvalidEstimate("receiver inverse failed") from error
    if not np.all(np.isfinite(w)):
        raise InvalidEstimate("receiver inverse is nonfinite")
    return w


def receiver_action(
    arm: str,
    x_pilots: np.ndarray,
    y_pilots: np.ndarray,
    y_payload: np.ndarray,
    parameter: float | None,
) -> ReceiverAction:
    """Run B0/B1/B2/C4 from observations only; truth is absent by construction."""
    x = np.asarray(x_pilots, dtype=np.complex128)
    y_p = np.asarray(y_pilots, dtype=np.complex128)
    y = np.asarray(y_payload, dtype=np.complex128)
    h_ls = plain_ls(x, y_p)
    raw_singular_values = np.linalg.svd(h_ls, compute_uv=False)
    rho = float(raw_singular_values[0] / raw_singular_values[1])

    if arm == "B0":
        if parameter is not None:
            raise ValueError("B0 has no parameter")
        h_hat = h_ls
        w = _invert_exact(h_hat)
    elif arm == "B1":
        if parameter is None or float(parameter) < 0.0:
            raise ValueError("B1 requires a nonnegative eta")
        gram = x @ x.conj().T
        regularizer = float(parameter) * float(np.trace(gram).real / 2.0)
        regularized = gram + regularizer * np.eye(2)
        cross = y_p @ x.conj().T
        h_hat = np.linalg.solve(regularized.T, cross.T).T
        w = _invert_exact(h_hat)
    elif arm == "B2":
        if parameter is None or not 0.0 <= float(parameter) <= 1.0:
            raise ValueError("B2 requires tau in [0,1]")
        u, singular_values, vh = np.linalg.svd(h_ls, full_matrices=False)
        floor = float(parameter) * float(singular_values[0])
        floored = np.maximum(singular_values, floor)
        if floored[1] == 0.0:
            raise InvalidEstimate("B2 has an exact zero singular value")
        h_hat = (u * floored) @ vh
        w = (vh.conj().T * (1.0 / floored)) @ u.conj().T
    elif arm == "C4":
        if parameter is not None:
            raise ValueError("C4 has no adaptive parameter")
        projection = project_scaled_unitary(h_ls)
        h_hat = projection.h_projected
        w = projection.w
        rho = projection.rho
    else:
        raise ValueError(f"unregistered deployable arm: {arm}")

    z = w @ y
    if not (
        np.all(np.isfinite(z))
        and np.all(np.isfinite(h_hat))
        and np.all(np.isfinite(w))
        and np.isfinite(rho)
    ):
        raise InvalidEstimate(f"{arm} produced a nonfinite action")
    return ReceiverAction(z=z, h_hat=h_hat, w=w, rho=rho)


def oracle_action(h_true: np.ndarray, y_payload: np.ndarray) -> ReceiverAction:
    """Explicit offline O1 arm; isolated from every deployable receiver API."""
    h = np.asarray(h_true, dtype=np.complex128)
    w = _invert_exact(h)
    return ReceiverAction(z=w @ y_payload, h_hat=h.copy(), w=w, rho=1.0)


def action_bytes(action: ReceiverAction) -> bytes:
    return b"".join(
        np.ascontiguousarray(value, dtype="<c16").tobytes(order="C")
        for value in (action.z, action.h_hat, action.w)
    ) + struct.pack("<d", action.rho)


def score_action(
    action: ReceiverAction, bits: np.ndarray, h_true: np.ndarray
) -> dict[str, float | int]:
    """Offline scorer; payload truth and hidden channel enter only here."""
    truth_bits = np.asarray(bits)
    decided = np.vstack([m16apsk_demod(action.z[pol]) for pol in range(2)])
    bit_errors = int(np.count_nonzero(decided != truth_bits))
    payload_bits = int(truth_bits.size)
    h = np.asarray(h_true, dtype=np.complex128)
    channel_nmse = float(np.linalg.norm(action.h_hat - h) ** 2 / np.linalg.norm(h) ** 2)
    inverse_residual = float(np.linalg.norm(action.w @ h - np.eye(2)) ** 2 / 2.0)
    values = (bit_errors / payload_bits, channel_nmse, inverse_residual, action.rho)
    if not all(np.isfinite(value) for value in values):
        raise InvalidEstimate("offline metric is nonfinite")
    return {
        "bit_errors": bit_errors,
        "payload_bits": payload_bits,
        "ber": float(bit_errors / payload_bits),
        "channel_nmse": channel_nmse,
        "inverse_residual": inverse_residual,
        "rho": float(action.rho),
    }
