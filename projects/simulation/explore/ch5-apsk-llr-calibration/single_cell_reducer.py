"""Statistics-only reducer for the frozen T077 physical-frame clusters."""

from __future__ import annotations

import warnings

import numpy as np
from scipy.stats import ConstantInputWarning, spearmanr


def gate1_metrics(
    pilot_n0: np.ndarray,
    payload_n0: np.ndarray,
    *,
    seed: int,
    resamples: int,
) -> dict:
    pilot = np.asarray(pilot_n0, dtype=np.float64)
    payload = np.asarray(payload_n0, dtype=np.float64)
    if pilot.ndim != 1 or payload.shape != pilot.shape or pilot.size < 2:
        raise ValueError("Gate 1 needs aligned physical-frame vectors")
    if np.any(~np.isfinite(pilot)) or np.any(~np.isfinite(payload)):
        raise ValueError("Gate 1 variance vectors must be finite")
    if np.any(pilot <= 0.0) or np.any(payload <= 0.0):
        raise ValueError("Gate 1 variance vectors must be positive")
    x = -np.log(pilot)
    y = -np.log(payload)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConstantInputWarning)
        point = float(spearmanr(x, y).statistic)
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    boot = np.empty(int(resamples), dtype=np.float64)
    for index in range(int(resamples)):
        selected = rng.integers(0, pilot.size, size=pilot.size)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConstantInputWarning)
            boot[index] = float(spearmanr(x[selected], y[selected]).statistic)
    finite = boot[np.isfinite(boot)]
    lower = float(np.quantile(finite, 0.05)) if finite.size else float("nan")
    ratio = np.log(pilot / payload)
    q25, median, q75 = np.quantile(ratio, [0.25, 0.5, 0.75])
    passed = bool(np.isfinite(point) and np.isfinite(lower) and point > 0.0 and lower > 0.0)
    return {
        "frames": int(pilot.size),
        "rho": point,
        "ci_one_sided_lower": lower,
        "bootstrap_finite": int(finite.size),
        "bootstrap_resamples": int(resamples),
        "bootstrap_seed": int(seed),
        "log_ratio_median": float(median),
        "log_ratio_iqr": [float(q25), float(q75)],
        "log_ratio_mae": float(np.mean(np.abs(ratio))),
        "pass": passed,
    }


def paired_rate_difference_ci(
    first_errors: np.ndarray,
    second_errors: np.ndarray,
    *,
    denominator_per_frame: int,
    seed: int,
    resamples: int,
) -> dict:
    first = np.asarray(first_errors, dtype=np.int64)
    second = np.asarray(second_errors, dtype=np.int64)
    if first.ndim != 1 or second.shape != first.shape or first.size < 1:
        raise ValueError("paired errors must be aligned physical-frame vectors")
    if np.any(first < 0) or np.any(second < 0) or denominator_per_frame <= 0:
        raise ValueError("paired error counts and denominator must be valid")
    per_frame = (first - second).astype(np.float64) / float(denominator_per_frame)
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    boot = np.empty(int(resamples), dtype=np.float64)
    for start in range(0, int(resamples), 1000):
        stop = min(start + 1000, int(resamples))
        selected = rng.integers(0, first.size, size=(stop - start, first.size))
        boot[start:stop] = np.mean(per_frame[selected], axis=1)
    lower, upper = np.quantile(boot, [0.025, 0.975])
    return {
        "point": float(np.mean(per_frame)),
        "ci_lower": float(lower),
        "ci_upper": float(upper),
        "cluster": "physical_frame",
        "frames": int(first.size),
        "bootstrap_resamples": int(resamples),
        "bootstrap_seed": int(seed),
        "discordant_frames": int(np.count_nonzero(first != second)),
        "first_better_frames": int(np.count_nonzero(first < second)),
        "second_better_frames": int(np.count_nonzero(second < first)),
    }


def gate2_decision(
    b0_bit_errors: np.ndarray,
    b0_fer: np.ndarray,
    o1_bit_errors: np.ndarray,
    o1_fer: np.ndarray,
    *,
    seed: int,
    resamples: int,
) -> dict:
    b0_bits = np.asarray(b0_bit_errors, dtype=np.int64)
    o1_bits = np.asarray(o1_bit_errors, dtype=np.int64)
    b0_frames = np.asarray(b0_fer, dtype=np.int64)
    o1_frames = np.asarray(o1_fer, dtype=np.int64)
    if not (b0_bits.shape == o1_bits.shape == b0_frames.shape == o1_frames.shape):
        raise ValueError("Gate 2 arm vectors must be paired by physical frame")
    ber_difference = paired_rate_difference_ci(
        b0_bits,
        o1_bits,
        denominator_per_frame=1024,
        seed=seed,
        resamples=resamples,
    )
    fer_difference = paired_rate_difference_ci(
        b0_frames,
        o1_frames,
        denominator_per_frame=1,
        seed=seed,
        resamples=resamples,
    )
    frames = int(b0_bits.size)
    arms = {
        "B0": {
            "bit_errors": int(np.sum(b0_bits)),
            "ber": float(np.sum(b0_bits) / (frames * 1024)),
            "frame_errors": int(np.sum(b0_frames)),
            "fer": float(np.mean(b0_frames)),
        },
        "O1": {
            "bit_errors": int(np.sum(o1_bits)),
            "ber": float(np.sum(o1_bits) / (frames * 1024)),
            "frame_errors": int(np.sum(o1_frames)),
            "fer": float(np.mean(o1_frames)),
        },
    }
    insufficient = bool(np.sum(b0_frames) == 0 and np.sum(o1_frames) == 0)
    passed = bool(
        not insufficient
        and ber_difference["ci_lower"] > 0.0
        and arms["O1"]["fer"] <= arms["B0"]["fer"]
    )
    if insufficient:
        terminal = "SINGLE_CELL_INSUFFICIENT_SENSITIVITY"
    elif passed:
        terminal = None
    else:
        terminal = "SINGLE_CELL_NO_HEADROOM"
    return {
        "frames": frames,
        "arms": arms,
        "ber_difference_B0_minus_O1": ber_difference,
        "fer_difference_B0_minus_O1": fer_difference,
        "stronger_fer_headroom": bool(
            fer_difference["ci_lower"] > 0.0
            and fer_difference["discordant_frames"] >= 30
        ),
        "gate2": "PASS" if passed else "FAIL",
        "terminal": terminal,
    }
