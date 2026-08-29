"""Synthetic post-Ch4 fixture strictly limited to T054 correctness checks."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import numpy as np

from codec_metrics import apsk16_identity, apsk16_table


CORRECTNESS_FLAGS = frozenset(
    {
        "CORRECTNESS_ONLY",
        "SYNTHETIC_CORRECTNESS_ONLY",
        "SYNTHETIC_RESIDUAL",
        "NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL",
    }
)


@dataclass(frozen=True)
class PostCh4Bundle:
    z: np.ndarray
    G_eff: complex
    Sigma_n: np.ndarray
    sample_phase: np.ndarray
    flags: frozenset[str]
    constellation_id: str
    labeling_id: str
    pilot_mask: np.ndarray
    pilot_labels: np.ndarray
    realization_hash: str


@dataclass(frozen=True)
class SyntheticPair:
    train: PostCh4Bundle
    eval: PostCh4Bundle
    realization_hash: str


def _residuals(
    rng: np.random.Generator, labels: np.ndarray, symbols: np.ndarray
) -> np.ndarray:
    theta = np.angle(symbols[labels])
    radial_std = 0.018 + 0.0015 * (labels % 4)
    tangential_std = 0.010 + 0.0010 * ((labels // 2) % 3)
    radial = rng.standard_normal(labels.size) * radial_std
    tangential = rng.standard_normal(labels.size) * tangential_std
    return (radial + 1j * tangential) * np.exp(1j * theta)


def make_synthetic_correctness_pair(
    *, seed: int, pilots_per_point: int = 12, eval_count: int = 256
) -> SyntheticPair:
    """Create paired train/eval residuals without asserting natural occurrence."""
    if pilots_per_point < 2 or eval_count < 1:
        raise ValueError("pilots_per_point >=2 and eval_count >=1 are required")
    symbols, _ = apsk16_table()
    modulation_identity = apsk16_identity()
    seed_sequence = np.random.SeedSequence(seed)
    train_rng, eval_rng = [np.random.default_rng(child) for child in seed_sequence.spawn(2)]

    train_labels = np.repeat(np.arange(16, dtype=np.int64), pilots_per_point)
    train_z = symbols[train_labels] + _residuals(train_rng, train_labels, symbols)
    eval_symbol_indices = eval_rng.integers(0, 16, size=eval_count, dtype=np.int64)
    eval_z = symbols[eval_symbol_indices] + _residuals(eval_rng, eval_symbol_indices, symbols)

    digest = sha256()
    digest.update(np.asarray(seed, dtype=np.int64).tobytes())
    digest.update(train_z.view(np.float64).tobytes())
    digest.update(train_labels.tobytes())
    digest.update(eval_z.view(np.float64).tobytes())
    realization_hash = digest.hexdigest()

    common = {
        "G_eff": 1.0 + 0.0j,
        "Sigma_n": np.eye(2, dtype=np.float64) * 1e-4,
        "flags": CORRECTNESS_FLAGS,
        "constellation_id": modulation_identity.constellation_id,
        "labeling_id": modulation_identity.labeling_id,
        "realization_hash": realization_hash,
    }
    train = PostCh4Bundle(
        z=train_z,
        sample_phase=np.angle(train_z),
        pilot_mask=np.ones(train_z.size, dtype=bool),
        pilot_labels=train_labels,
        **common,
    )
    evaluation = PostCh4Bundle(
        z=eval_z,
        sample_phase=np.angle(eval_z),
        pilot_mask=np.zeros(eval_z.size, dtype=bool),
        pilot_labels=np.full(eval_z.size, -1, dtype=np.int64),
        **common,
    )
    return SyntheticPair(train=train, eval=evaluation, realization_hash=realization_hash)


__all__ = ["PostCh4Bundle", "SyntheticPair", "make_synthetic_correctness_pair"]
