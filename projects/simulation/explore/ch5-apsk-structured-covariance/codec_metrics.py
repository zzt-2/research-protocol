"""APSK soft metrics for the T054 correctness-only seam.

The likelihood follows Layton et al. (2018), Eq. (10), p. 4: a
symbol-dependent bivariate Gaussian with Mahalanobis and log-determinant
terms.  Project LLR convention is positive-means-bit-1.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import numpy as np

from common._modulation import m16apsk_mod


@dataclass(frozen=True)
class Apsk16Identity:
    source: str
    table_sha256: str
    constellation_id: str
    labeling_id: str


def apsk16_table() -> tuple[np.ndarray, np.ndarray]:
    """Return the canonical project (8,8)-16APSK table in label order."""
    labels = np.arange(16, dtype=np.uint8)
    weights = np.array([8, 4, 2, 1], dtype=np.uint8)
    bits = ((labels[:, None] & weights) != 0).astype(np.uint8)
    symbols = np.asarray(m16apsk_mod(bits.reshape(-1)), dtype=np.complex128)
    return symbols, bits


def apsk16_identity() -> Apsk16Identity:
    """Fingerprint constellation and labels from the public project mapper."""
    symbols, bits = apsk16_table()
    digest = sha256()
    digest.update(symbols.view(np.float64).tobytes())
    digest.update(bits.tobytes())
    table_hash = digest.hexdigest()
    source = "common._modulation.m16apsk_mod"
    short = table_hash[:16]
    return Apsk16Identity(
        source=source,
        table_sha256=table_hash,
        constellation_id=f"{source}:symbols:{short}",
        labeling_id=f"{source}:bits:{short}",
    )


def mahalanobis_logdet_llr(
    z: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
    *,
    clip: float,
) -> np.ndarray:
    """Exact-sum 4-bit APSK LLR using matched Gaussian covariances.

    No transmitted payload bits or residual truth are accepted by this API.
    """
    samples = np.asarray(z, dtype=np.complex128).reshape(-1)
    means = np.asarray(means, dtype=np.complex128)
    covariances = np.asarray(covariances, dtype=np.float64)
    if means.shape != (16,) or covariances.shape != (16, 2, 2):
        raise ValueError("means/covariances must have shapes (16,) and (16,2,2)")
    if not np.isfinite(clip) or clip <= 0.0:
        raise ValueError("clip must be finite and positive")

    _, bits = apsk16_table()
    observations = np.column_stack((samples.real, samples.imag))
    centers = np.column_stack((means.real, means.imag))
    logp = np.empty((samples.size, 16), dtype=np.float64)
    for index in range(16):
        covariance = covariances[index]
        sign, logdet = np.linalg.slogdet(covariance)
        if sign <= 0 or not np.isfinite(logdet):
            raise ValueError(f"covariance {index} is not finite positive-definite")
        delta = observations - centers[index]
        solved = np.linalg.solve(covariance, delta.T).T
        quadratic = np.einsum("ni,ni->n", delta, solved)
        logp[:, index] = -0.5 * (quadratic + logdet)

    llr = np.empty((samples.size, 4), dtype=np.float64)
    for bit_index in range(4):
        log_one = np.logaddexp.reduce(logp[:, bits[:, bit_index] == 1], axis=1)
        log_zero = np.logaddexp.reduce(logp[:, bits[:, bit_index] == 0], axis=1)
        llr[:, bit_index] = np.clip(log_one - log_zero, -clip, clip)
    return llr


def gmi_analytic(llrs: np.ndarray, true_bits: np.ndarray) -> float:
    """FEC-agnostic identity metric; used only for sign/zero-LLR smoke."""
    llrs = np.asarray(llrs, dtype=np.float64)
    bits = np.asarray(true_bits, dtype=np.float64)
    if llrs.ndim != 2 or llrs.shape[1] != 4 or bits.shape != llrs.shape:
        raise ValueError("llrs and true_bits must share shape (N,4)")
    if not np.all((bits == 0.0) | (bits == 1.0)):
        raise ValueError("true_bits must be binary")
    matched = (2.0 * bits - 1.0) * llrs
    z = -matched
    softplus = np.maximum(z, 0.0) + np.log1p(np.exp(-np.abs(z)))
    value = 4.0 - float(np.log2(np.e) * np.mean(softplus, axis=0).sum())
    return float(np.clip(value, 0.0, 4.0))


__all__ = [
    "Apsk16Identity",
    "apsk16_identity",
    "apsk16_table",
    "gmi_analytic",
    "mahalanobis_logdet_llr",
]
