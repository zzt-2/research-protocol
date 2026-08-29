"""Correctness-only Ch4 gated-RDE seam.

Formula authority
-----------------
Ready and Gooch, ICASSP 1990, Section 3 defines radius-directed error from
the equalizer output and nearest constellation radius. Fatadin, Ives, and
Savory, JLT 27(15), 2009, p. 3044, Eq. (10) defines the RDE error criterion
and states that the tap weights use the DD-LMS update in Eq. (9).

For the row-output convention ``z = W @ y``, this seam transcribes the
canonical stochastic-gradient row update as

``W_i <- W_i + mu * g_i * z_i * (R_i**2 - |z_i|**2) * y.conj()``.

The sign, conjugation, and dimensions are frozen by an independent literal
complex-number hand calculation in the target pytest file. This module is a
correctness seam only; it contains no performance-grid or tuning machinery.
"""

from __future__ import annotations

import hashlib
from typing import Callable

import numpy as np


CONSTELLATION_ID = "DP-(8,8)-16APSK"
LABELING_ID = "b0-ring+reflected-gray-8psk"
_GAMMA = 2.57
_R1 = np.sqrt(2.0 / (1.0 + _GAMMA**2))
_R2 = _GAMMA * _R1
_GRAY8 = np.array([0, 1, 3, 2, 6, 7, 5, 4], dtype=np.uint8)
_INNER = np.array(
    [_R1 * np.exp(1j * (np.pi / 8 + k * np.pi / 4)) for k in range(8)],
    dtype=np.complex128,
)
_OUTER = np.array(
    [_R2 * np.exp(1j * k * np.pi / 4) for k in range(8)],
    dtype=np.complex128,
)
_RADII = np.array([_R1, _R2], dtype=float)
_PHYSICAL = np.concatenate((_INNER, _OUTER))
_GRAY16 = np.concatenate((_GRAY8, 8 + _GRAY8))
_BY_LABEL = _PHYSICAL[np.argsort(_GRAY16)]


def m16apsk_constellation_by_label() -> np.ndarray:
    """Return the common-module-compatible label-indexed constellation."""
    return _BY_LABEL.copy()


def nearest_apsk(z: np.ndarray) -> dict[str, np.ndarray]:
    """Nearest point, its ring identity, and two normalized gate scores."""
    values = np.asarray(z, dtype=np.complex128)
    flat = values.reshape(-1)
    distances = np.abs(flat[:, None] - _BY_LABEL[None, :]) ** 2
    labels = np.argmin(distances, axis=1).astype(np.uint8)
    symbols = _BY_LABEL[labels]
    ring_ids = labels >= 8
    radii = np.where(ring_ids, _R2, _R1)
    scale2 = np.maximum(radii**2, np.finfo(float).tiny)
    decision_score = np.abs(flat - symbols) ** 2 / scale2
    ring_score = np.abs(np.abs(flat) ** 2 - radii**2) / scale2
    shape = values.shape
    return {
        "labels": labels.reshape(shape),
        "symbols": symbols.reshape(shape),
        "ring_ids": ring_ids.reshape(shape),
        "radii": radii.reshape(shape),
        "decision_score": decision_score.reshape(shape),
        "ring_score": ring_score.reshape(shape),
    }


def canonical_nearest_radius(z: np.ndarray) -> dict[str, np.ndarray]:
    """Select the receiver-visible canonical RDE radius and native residual."""
    values = np.asarray(z, dtype=np.complex128)
    flat_power = np.abs(values.reshape(-1)) ** 2
    residuals = np.abs(flat_power[:, None] - _RADII[None, :] ** 2)
    ring_ids = np.argmin(residuals, axis=1)
    radii = _RADII[ring_ids]
    scale2 = np.maximum(radii**2, np.finfo(float).tiny)
    ring_score = residuals[np.arange(flat_power.size), ring_ids] / scale2
    shape = values.shape
    return {
        "ring_ids": ring_ids.reshape(shape),
        "radii": radii.reshape(shape),
        "ring_score": ring_score.reshape(shape),
    }


def random_su2(rng: np.random.Generator) -> np.ndarray:
    """Draw a Haar-isotropic SU(2) matrix from a normalized 4-vector."""
    q = rng.normal(size=4)
    q /= np.linalg.norm(q)
    a = q[0] + 1j * q[1]
    b = q[2] + 1j * q[3]
    return np.array([[a, b], [-np.conj(b), np.conj(a)]], dtype=np.complex128)


def orthogonal_pilots(n_pilots: int) -> np.ndarray:
    """Finite two-row Walsh pilot prefix with X X^H = n_pilots I."""
    if n_pilots < 2 or n_pilots % 2:
        raise ValueError("n_pilots must be an even integer >= 2")
    return np.vstack(
        (
            np.ones(n_pilots, dtype=np.complex128),
            (-1.0) ** np.arange(n_pilots),
        )
    )


def pilot_ls_demux(pilot_rx: np.ndarray, pilot_tx: np.ndarray) -> np.ndarray:
    """Receiver-visible LS demux argmin_W ||pilot_tx - W pilot_rx||_F."""
    y = np.asarray(pilot_rx, dtype=np.complex128)
    x = np.asarray(pilot_tx, dtype=np.complex128)
    if x.shape != y.shape or x.ndim != 2 or x.shape[0] != 2:
        raise ValueError("pilot_tx and pilot_rx must both have shape (2, n_pilots)")
    gram = y @ y.conj().T
    return (np.linalg.solve(gram.T, (x @ y.conj().T).T)).T


def canonical_rde_step(
    w: np.ndarray,
    y: np.ndarray,
    radii: np.ndarray,
    *,
    mu: float,
    gates: np.ndarray,
) -> np.ndarray:
    """Apply one canonical two-row RDE update under ``z = W @ y``."""
    w_arr = np.asarray(w, dtype=np.complex128)
    y_arr = np.asarray(y, dtype=np.complex128)
    r_arr = np.asarray(radii, dtype=float)
    g_arr = np.asarray(gates, dtype=float)
    if w_arr.shape != (2, 2) or y_arr.shape != (2,) or r_arr.shape != (2,):
        raise ValueError("expected W=(2,2), y=(2,), radii=(2,)")
    if g_arr.shape != (2,):
        raise ValueError("gates must have shape (2,)")
    z = w_arr @ y_arr
    error = z * (r_arr**2 - np.abs(z) ** 2)
    return w_arr + float(mu) * np.outer(g_arr * error, np.conj(y_arr))


def candidate_gate(
    ring_score: np.ndarray,
    decision_score: np.ndarray,
    *,
    ring_threshold: float,
    decision_threshold: float,
) -> np.ndarray:
    """Inclusive two-evidence hard gate; equality is deterministically open."""
    ring = np.asarray(ring_score, dtype=float)
    decision = np.asarray(decision_score, dtype=float)
    return (ring <= ring_threshold) & (decision <= decision_threshold)


def _run_rde(
    payload_rx: np.ndarray,
    w0: np.ndarray,
    *,
    mu: float,
    gate_fn: Callable[[dict[str, np.ndarray], int], np.ndarray],
) -> dict[str, np.ndarray]:
    y = np.asarray(payload_rx, dtype=np.complex128)
    if y.ndim != 2 or y.shape[0] != 2:
        raise ValueError("payload_rx must have shape (2, n_symbols)")
    w = np.array(w0, dtype=np.complex128, copy=True)
    z_trace = np.empty_like(y)
    gates = np.empty(y.shape, dtype=bool)
    ring_scores = np.empty(y.shape, dtype=float)
    native_ring_scores = np.empty(y.shape, dtype=float)
    decision_scores = np.empty(y.shape, dtype=float)
    for k in range(y.shape[1]):
        z = w @ y[:, k]
        scores = nearest_apsk(z)
        canonical = canonical_nearest_radius(z)
        scores["canonical_radii"] = canonical["radii"]
        scores["canonical_ring_score"] = canonical["ring_score"]
        gate = np.asarray(gate_fn(scores, k), dtype=bool)
        if gate.shape != (2,):
            raise ValueError("gate_fn must return shape (2,)")
        z_trace[:, k] = z
        gates[:, k] = gate
        ring_scores[:, k] = scores["ring_score"]
        native_ring_scores[:, k] = scores["canonical_ring_score"]
        decision_scores[:, k] = scores["decision_score"]
        w = canonical_rde_step(
            w, y[:, k], scores["canonical_radii"], mu=mu, gates=gate
        )
    return {
        "z": z_trace,
        "W": w,
        "gates": gates,
        "ring_score": ring_scores,
        "native_ring_score": native_ring_scores,
        "decision_score": decision_scores,
    }


def run_plain_rde(payload_rx: np.ndarray, w0: np.ndarray, *, mu: float) -> dict:
    """Deployable plain RDE; no truth-bearing inputs."""
    return _run_rde(payload_rx, w0, mu=mu, gate_fn=lambda scores, k: np.ones(2, bool))


def run_cheap_rde(
    payload_rx: np.ndarray,
    w0: np.ndarray,
    *,
    mu: float,
    ring_threshold: float,
) -> dict:
    """Deployable native-ring-residual single-feature hard gate."""
    return _run_rde(
        payload_rx,
        w0,
        mu=mu,
        gate_fn=lambda scores, k: scores["canonical_ring_score"] <= ring_threshold,
    )


def run_candidate_rde(
    payload_rx: np.ndarray,
    w0: np.ndarray,
    *,
    mu: float,
    ring_threshold: float,
    decision_threshold: float,
) -> dict:
    """Deployable two-evidence candidate v1; no TX/J/SNR/BER inputs."""
    return _run_rde(
        payload_rx,
        w0,
        mu=mu,
        gate_fn=lambda scores, k: candidate_gate(
            scores["ring_score"],
            scores["decision_score"],
            ring_threshold=ring_threshold,
            decision_threshold=decision_threshold,
        ),
    )


def run_oracle_rde(
    payload_rx: np.ndarray,
    w0: np.ndarray,
    tx_symbols: np.ndarray,
    *,
    mu: float,
) -> dict:
    """Truth-bearing non-deployable correctness upper-bound arm."""
    truth = nearest_apsk(np.asarray(tx_symbols, dtype=np.complex128))["labels"]
    return _run_rde(
        payload_rx,
        w0,
        mu=mu,
        gate_fn=lambda scores, k: scores["labels"] == truth[:, k],
    )


def _hash_arrays(seed: int, *arrays: np.ndarray) -> str:
    digest = hashlib.sha256(str(int(seed)).encode("ascii"))
    for array in arrays:
        arr = np.ascontiguousarray(array)
        digest.update(str(arr.shape).encode("ascii"))
        digest.update(arr.dtype.str.encode("ascii"))
        digest.update(arr.tobytes())
    return digest.hexdigest()


def generate_shared_correctness_realization(
    *,
    seed: int,
    n_payload: int,
    n_pilots: int,
    snr_db: float,
    identity_jones: bool = False,
    noiseless: bool = False,
) -> dict:
    """One paired DP-APSK/Jones/noise/LS realization for every arm."""
    if n_payload <= 0:
        raise ValueError("n_payload must be positive")
    rng = np.random.default_rng(seed)
    labels = rng.integers(0, 16, size=(2, n_payload), dtype=np.uint8)
    symbols = _BY_LABEL[labels]
    jones = np.eye(2, dtype=np.complex128) if identity_jones else random_su2(rng)
    pilots = orthogonal_pilots(n_pilots)
    noise_var = 0.0 if noiseless else 10.0 ** (-float(snr_db) / 10.0)
    pilot_noise = np.sqrt(noise_var / 2.0) * (
        rng.normal(size=pilots.shape) + 1j * rng.normal(size=pilots.shape)
    )
    noise = np.sqrt(noise_var / 2.0) * (
        rng.normal(size=symbols.shape) + 1j * rng.normal(size=symbols.shape)
    )
    pilot_rx = jones @ pilots + pilot_noise
    payload_rx = jones @ symbols + noise
    w0 = pilot_ls_demux(pilot_rx, pilots)
    realization_hash = _hash_arrays(
        seed, labels, symbols, jones, pilots, pilot_noise, noise, w0, payload_rx
    )
    return {
        "seed": int(seed),
        "snr_db": float(snr_db),
        "noise_var": float(noise_var),
        "symbols": symbols,
        "labels": labels,
        "J": jones,
        "pilots": pilots,
        "pilot_noise": pilot_noise,
        "noise": noise,
        "W0": w0,
        "payload_rx": payload_rx,
        "realization_hash": realization_hash,
    }


def _attach_seam(result: dict, realization: dict) -> dict:
    final_w = result["W"]
    effective_noise = final_w @ realization["noise"]
    sigma_n = effective_noise @ effective_noise.conj().T / effective_noise.shape[1]
    return {
        **result,
        "G_eff": final_w @ realization["J"],
        "Sigma_n": sigma_n,
        "flags": result["gates"],
        "constellation_id": CONSTELLATION_ID,
        "labeling_id": LABELING_ID,
        "realization_hash": realization["realization_hash"],
    }


def run_all_arms(
    realization: dict,
    *,
    mu: float,
    ring_threshold: float,
    decision_threshold: float,
) -> dict[str, dict]:
    """Run all four arms on the exact same pre-generated realization."""
    y = realization["payload_rx"]
    w0 = realization["W0"]
    raw = {
        "plain": run_plain_rde(y, w0, mu=mu),
        "cheap": run_cheap_rde(y, w0, mu=mu, ring_threshold=ring_threshold),
        "candidate": run_candidate_rde(
            y,
            w0,
            mu=mu,
            ring_threshold=ring_threshold,
            decision_threshold=decision_threshold,
        ),
        "oracle": run_oracle_rde(y, w0, realization["symbols"], mu=mu),
    }
    return {name: _attach_seam(result, realization) for name, result in raw.items()}
