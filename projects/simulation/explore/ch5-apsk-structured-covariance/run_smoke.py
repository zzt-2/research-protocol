"""Run the deterministic T054 correctness/GMI-identity smoke."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


SIM_ROOT = Path(__file__).resolve().parents[2]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from codec_metrics import apsk16_table, gmi_analytic, mahalanobis_logdet_llr
from methods import (
    estimate_covariance_arms,
    estimate_gaussian_arms,
    point_local_rt_covariances,
)
from post_ch4_fixture import make_synthetic_correctness_pair


def _scalar_gap(covariances: np.ndarray) -> float:
    scalar = np.trace(covariances, axis1=1, axis2=2) / 2.0
    target = scalar[:, None, None] * np.eye(2)[None, :, :]
    return float(np.max(np.abs(covariances - target)))


def run_smoke(*, seed: int) -> dict[str, object]:
    """Return machine-readable correctness evidence without performance claims."""
    floor = 1e-8
    kappa = 7.0
    b3_shrinkage = 0.1
    symbols, bits = apsk16_table()
    pair = make_synthetic_correctness_pair(seed=seed)
    gaussian_arms = estimate_gaussian_arms(
        pair.train.z,
        pair.train.pilot_labels,
        symbols,
        floor=floor,
        kappa=kappa,
        b3_shrinkage=b3_shrinkage,
    )
    arms = {name: model.covariances for name, model in gaussian_arms.items()}
    shared_mean_object = len({id(model.means) for model in gaussian_arms.values()}) == 1
    angle = 0.371
    phasor = np.exp(1j * angle)
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    rotated_arms = estimate_covariance_arms(
        pair.train.z * phasor,
        pair.train.pilot_labels,
        symbols * phasor,
        floor=floor,
        kappa=kappa,
        b3_shrinkage=b3_shrinkage,
    )
    rotation_error = max(
        float(
            np.max(
                np.abs(
                    rotated_arms[name]
                    - np.einsum("ab,kbc,dc->kad", rotation, value, rotation)
                )
            )
        )
        for name, value in arms.items()
    )

    llr = mahalanobis_logdet_llr(
        symbols,
        symbols,
        np.repeat((np.eye(2) * 1e-4)[None, :, :], 16, axis=0),
        clip=30.0,
    )
    label_errors = int(np.count_nonzero((llr >= 0).astype(np.uint8) != bits))

    offsets = np.array([0.02, -0.02, 0.02j, -0.02j], dtype=np.complex128)
    circular_labels = np.repeat(np.arange(16), 4)
    circular_z = np.repeat(symbols, 4) + np.tile(offsets, 16)
    circular = estimate_covariance_arms(
        circular_z,
        circular_labels,
        symbols,
        floor=1e-10,
        kappa=kappa,
        b3_shrinkage=b3_shrinkage,
    )

    local = point_local_rt_covariances(
        pair.train.z, pair.train.pilot_labels, symbols, floor=floor
    )
    zero_kappa = estimate_covariance_arms(
        pair.train.z,
        pair.train.pilot_labels,
        symbols,
        floor=floor,
        kappa=0.0,
        b3_shrinkage=b3_shrinkage,
    )["C1"]
    large = estimate_covariance_arms(
        pair.train.z,
        pair.train.pilot_labels,
        symbols,
        floor=floor,
        kappa=1e15,
        b3_shrinkage=b3_shrinkage,
    )

    identity_bits = np.tile(bits, (32, 1))
    correct_llr = (2.0 * identity_bits - 1.0) * 20.0
    receipt = {
        "schema_version": "t054.correctness-receipt.v1",
        "scope": [
            "CORRECTNESS_ONLY",
            "SYNTHETIC_RESIDUAL",
            "NO_TARGET_OCCURRENCE_OR_METHOD_SIGNAL",
        ],
        "seed": int(seed),
        "realization_hash": pair.realization_hash,
        "constellation_id": pair.train.constellation_id,
        "labeling_id": pair.train.labeling_id,
        "arms": ["B1", "B2", "B3", "C1"],
        "shared_pilot_mean_object": shared_mean_object,
        "label_roundtrip_bit_errors": label_errors,
        "minimum_covariance_eigenvalue": float(
            min(np.min(np.linalg.eigvalsh(value)) for value in arms.values())
        ),
        "circular_b2_scalar_gap": _scalar_gap(circular["B2"]),
        "circular_c1_scalar_gap": _scalar_gap(circular["C1"]),
        "rotation_equivariance_max_abs_error": rotation_error,
        "kappa_zero_local_max_abs_error": float(np.max(np.abs(zero_kappa - local))),
        "kappa_large_b2_max_abs_error": float(
            np.max(np.abs(large["C1"] - large["B2"]))
        ),
        "gmi_correct": gmi_analytic(correct_llr, identity_bits),
        "gmi_zero": gmi_analytic(np.zeros_like(correct_llr), identity_bits),
        "gmi_flipped": gmi_analytic(-correct_llr, identity_bits),
        "scientific_verdict": "NOT_AUTHORIZED",
        "target_occurrence": "NOT_TESTED",
        "method_signal": "NOT_TESTED",
    }
    return receipt


def main() -> None:
    from common._experiment import save_results

    output = Path(__file__).with_name("correctness-receipt.json")
    receipt = run_smoke(seed=54)
    save_results(receipt, str(output), "t054_ch5_structured_covariance_correctness")
    print(receipt)


if __name__ == "__main__":
    main()
