"""CB1 baseline Atlas cell runner — standard-CMA (Godard-with-z), modulation-aware.

This runner is the CB1 modulation-generic-closure analogue of P03's
``stage_a_cell_runner.py``. It exercises the same standard-CMA baseline
(Godard-with-z), the same comparator lattice (nearest-decision + same-
information blind affine + scoring-only oracle affine), and the same per-cell
decision schema. It differs from P03 only in that the modulation axis is
parameterized: it accepts ``modulation='qpsk'`` or ``'qam16'`` cells.

Implementation note — identity gate (CRITICAL)
----------------------------------------------
The canonical baseline is standard-CMA = Godard-with-z: the weight update
includes an extra ``z`` factor compared to the scalar-error CMA,

    Δw_standard ∝ (R² - |z|²) · z · r*     # Godard-with-z (P03 canonical)
    Δw_scalar  ∝ (R² - |z|²) · r*         # scalar-error (NOT canonical)

The protected-history runner (``tools/run_b001._default_runner``) obtains
standard-CMA by calling ``prompt013.run_cma_diagnostic(mode='standard')``
and stamps ``provenance.gradient = 'Godard-with-z'``. ``CMAEqualizer2x2`` in
``common/_cma.py`` implements the SCALAR-error gradient, so it would NOT pass
the identity gate truthfully. This runner therefore re-implements the
Godard-with-z blockwise update directly (replicating prompt013:301-306), and
stamps the same provenance string the protected-history runner does. The QPSK
anchor cell reproduces P03 v1 (PI-SER ≈ 0) which is the wiring regression.

Option A (per the task brief) is "use CMAEqualizer2x2 directly"; we deviate
to a direct Godard-with-z implementation only because Option A's identity gate
would be false. This is the documented Option B fallback ("only if Option A
fails the identity gate").
"""

from __future__ import annotations

from itertools import permutations
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


HERE = Path(__file__).resolve()


# ─── Standard-CMA (Godard-with-z) blockwise equalizer ────────────────────────

def standard_cma_godard_with_z(
    rX: np.ndarray,
    rY: np.ndarray,
    *,
    n_tap: int = 11,
    mu: float = 1e-3,
    R2: float = 1.0,
    block_size: int = 64,
) -> dict[str, Any]:
    """Run standard-CMA (Godard-with-z) blockwise on a dual-pol input.

    Replicates prompt013 ``run_cma_diagnostic(mode='standard')`` online branch:
    blockwise filter with fixed intra-block weights, block-end gradient update
    using the Godard-with-z gradient Δw ∝ (R²-|z|²)·z·r*.

    Returns the full zX/zY traces (length N), divergence flags, the block trace
    (for downstream ML features if ever needed; here it is informational), and
    the provenance stamp that satisfies the standard-CMA identity gate.
    """
    rX = np.asarray(rX, dtype=complex)
    rY = np.asarray(rY, dtype=complex)
    N = len(rX)
    L = int(n_tap)
    half = L // 2
    center = half
    block_size = int(block_size)

    # Center-tap initialization (prompt013:335-337, _cma.py:80-86, Qin 2025 L283)
    wxx = np.zeros(L, dtype=complex); wxx[center] = 1.0
    wyy = np.zeros(L, dtype=complex); wyy[center] = 1.0
    wxy = np.zeros(L, dtype=complex)
    wyx = np.zeros(L, dtype=complex)

    def _wnorm():
        return float(np.sqrt(
            np.sum(np.abs(wxx) ** 2) + np.sum(np.abs(wxy) ** 2)
            + np.sum(np.abs(wyx) ** 2) + np.sum(np.abs(wyy) ** 2)
        ))

    init_norm = _wnorm()

    zX = np.zeros(N, dtype=complex)
    zY = np.zeros(N, dtype=complex)
    trace: list[dict[str, Any]] = []

    # Divergence criteria (TL-20, _cma.py:132-134)
    norm_thresh = 10.0 * init_norm
    z_amp_thresh = 1e3

    diverged = False
    diverge_idx = None

    rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
    rY_win = sliding_window_view(rY, L)
    n_valid = N - L + 1
    n_blocks = n_valid // block_size

    for blk in range(n_blocks):
        s = blk * block_size
        e = s + block_size
        if e > n_valid:
            break
        rX_blk = rX_win[s:e]
        rY_blk = rY_win[s:e]

        # Intra-block filter with fixed weights (prompt013:377-378, Eq.28)
        zx_blk = rX_blk @ wxx + rY_blk @ wxy
        zy_blk = rX_blk @ wyx + rY_blk @ wyy

        # Write to output aligned at s+half (prompt013:369, _cma.py:155)
        idx = s + half
        zX[idx:idx + block_size] = zx_blk
        zY[idx:idx + block_size] = zy_blk

        # Godard-with-z block-end gradient (prompt013:301-306)
        eX = R2 - np.abs(zx_blk) ** 2
        eY = R2 - np.abs(zy_blk) ** 2
        wxx += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
        wxy += mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
        wyx += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
        wyy += mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

        cur_norm = _wnorm()
        cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
        trace.append({
            "output_start": int(idx),
            "output_end": int(idx + block_size),
            "cm_error": float(np.mean((R2 - np.abs(zx_blk) ** 2) ** 2
                                      + (R2 - np.abs(zy_blk) ** 2) ** 2)),
            "output_power": float(np.mean(np.abs(zx_blk) ** 2 + np.abs(zy_blk) ** 2)),
            "update_norm": float(np.sqrt(
                np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)) ** 2)
                + np.sum(np.abs(mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)) ** 2)
            )),
            "w_norm": cur_norm,
            "z_amp_max": cur_zamp,
        })

        if not diverged:
            if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                    or not np.isfinite(cur_norm)):
                diverged = True
                diverge_idx = idx + block_size - 1
                break

    return {
        "zX": zX,
        "zY": zY,
        "diverged": diverged,
        "divergence_symbol": diverge_idx,
        "final_w_norm": _wnorm(),
        "init_w_norm": init_norm,
        "trace": trace,
        # Identity-gate stamp: matches run_b001._default_runner provenance
        # (tools/run_b001.py:149-151). The gradient string is what the cell
        # runner verifies per cell.
        "provenance": {
            "implementation": "cb1_cell_runner.standard_cma_godard_with_z",
            "entry": "blockwise standard-CMA (mode='standard', prompt013:301-306)",
            "gradient": "Godard-with-z",
        },
    }


# ─── Eval window geometry (mirrors P03 _eval_window_for) ─────────────────────

def eval_window_for(
    n_symbols: int, cma_taps: int, *, window_symbols: int = 256, block_size: int = 64
) -> tuple[int, int, int, int]:
    """eval_start, calibration_end, eval_end, half_taps (P03 _eval_window_for)."""
    half_taps = cma_taps // 2
    if half_taps < 1 or block_size < 1:
        raise ValueError("cma_taps and block_size must be positive")
    raw_prefix = max(int(round(n_symbols * 0.26)), cma_taps + 1)
    block_index = (raw_prefix - half_taps + block_size - 1) // block_size  # ceil
    eval_start = block_index * block_size + half_taps
    if eval_start <= cma_taps:
        eval_start += block_size
    window_symbols = min(window_symbols, max(n_symbols - eval_start - cma_taps, block_size))
    window_symbols = (window_symbols // block_size) * block_size
    if window_symbols < block_size:
        raise ValueError(f"eval window too small for N={n_symbols}: window={window_symbols}")
    calibration_end = eval_start + window_symbols // 2
    eval_end = eval_start + window_symbols
    if not (eval_start < calibration_end < eval_end):
        raise ValueError(f"eval window geometry invalid for N={n_symbols}")
    return eval_start, calibration_end, eval_end, half_taps


def rule_of_three_upper_bound(n_paired_cells: int, confidence: float = 0.95) -> float:
    if n_paired_cells <= 0:
        return float("nan")
    alpha = 1.0 - confidence
    return 1.0 - alpha ** (1.0 / float(n_paired_cells))


# ─── Per-cell decision (mirrors P03 _per_cell_decision) ──────────────────────

def per_cell_decision(
    *,
    visible_headroom: float,
    simple_gain: float,
    nearest_pi_ser: float,
    blind_pi_ser: float,
    oracle_pi_ser: float,
    n_paired_seeds: int,
    n_error_events: int,
    zero_error_upper_bound: float,
    minimum_detectable_effect: float,
    diverged: bool = False,
) -> dict[str, Any]:
    """Map raw cell metrics to a structured per-cell verdict (P03 schema).

    Adds a DIVERGENT decision_class for cells where standard-CMA diverged on
    at least one seed (per task brief discipline #6: divergence counts as a
    baseline-failure observation, reported as such, not as a headroom number).
    """
    if diverged:
        return {
            "status": "DIVERGENT",
            "decision_class": "DIVERGENT",
            "visible_headroom": float(visible_headroom),
            "simple_analytic_gain": float(simple_gain),
            "nearest_pi_ser": float(nearest_pi_ser),
            "blind_pi_ser": float(blind_pi_ser),
            "oracle_pi_ser": float(oracle_pi_ser),
            "n_paired_seeds": int(n_paired_seeds),
            "n_error_events": int(n_error_events),
            "zero_error_upper_bound": float(zero_error_upper_bound),
            "meets_minimum_detectable_effect": False,
        }
    has_visible_headroom = visible_headroom > 0.0
    simple_captures = simple_gain > 0.0
    if not has_visible_headroom:
        status = "NO_VISIBLE_HEADROOM"
        decision_class = "LOCAL_NEGATIVE"
    elif visible_headroom >= minimum_detectable_effect and simple_captures:
        status = "LOCAL_HEADROOM"
        decision_class = "ADVANCE"
    elif n_error_events == 0 and zero_error_upper_bound > minimum_detectable_effect:
        status = "INSUFFICIENT_SENSITIVITY"
        decision_class = "NON_DECISIVE"
    else:
        status = "SUB_MDE_HEADROOM"
        decision_class = "NON_DECISIVE"
    return {
        "status": status,
        "decision_class": decision_class,
        "visible_headroom": float(visible_headroom),
        "simple_analytic_gain": float(simple_gain),
        "nearest_pi_ser": float(nearest_pi_ser),
        "blind_pi_ser": float(blind_pi_ser),
        "oracle_pi_ser": float(oracle_pi_ser),
        "n_paired_seeds": int(n_paired_seeds),
        "n_error_events": int(n_error_events),
        "zero_error_upper_bound": float(zero_error_upper_bound),
        "meets_minimum_detectable_effect": bool(visible_headroom >= minimum_detectable_effect),
    }


# ─── One cell ────────────────────────────────────────────────────────────────

def run_cell(
    cell: Mapping[str, Any],
    contract: Mapping[str, Any],
    *,
    generator: Any,
    evaluator: Any,
) -> dict[str, Any]:
    """Run one CB1 baseline Atlas cell.

    Parameters
    ----------
    cell : mapping
        ``{id, modulation, snr_db, f_g_hz, sop_rate, n_symbols}``.
    contract : mapping
        Frozen common axes + statistical sensitivity. Same schema as P03
        ``stage-a-contract.v1.yaml`` ``frozen_common_axes`` and
        ``statistical_sensitivity``.
    generator, evaluator : callables
        ``generate_shared_realization_dp`` and the CB1 evaluator module.
    """
    import sys as _sys
    # The evaluator imports ``common._modulation`` lazily; make sure
    # projects/simulation is importable. _HERE parents[6] is the worktree root.
    # _HERE = .../scout/cb1-modulation-generic-closure/baseline-atlas/cb1_cell_runner.py
    sim_dir = Path(__file__).resolve().parents[6] / "projects" / "simulation"
    sim_dir_str = str(sim_dir)
    if not any(Path(p).resolve() == sim_dir.resolve() for p in _sys.path):
        _sys.path.insert(0, sim_dir_str)

    modulation = str(cell["modulation"])
    if modulation not in ("qpsk", "qam16"):
        raise ValueError(f"cell {cell['id']}: unsupported modulation {modulation!r}")
    R2 = 1.0 if modulation == "qpsk" else 1.32

    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    n_symbols = int(cell["n_symbols"])
    frozen = contract["frozen_common_axes"]
    cma_taps = int(frozen["cma_taps"])
    block_size = int(frozen["cma_block_size"])
    eval_start, calibration_end, eval_end, half_taps = eval_window_for(
        n_symbols, cma_taps, window_symbols=256, block_size=block_size,
    )
    paired_seeds = contract["covering_design"]["paired_seeds"]
    affine_ridge = float(frozen["affine_ridge"])

    per_seed: list[dict[str, Any]] = []
    cell_diverged = False
    identity_gate_ok = True
    for seed in paired_seeds:
        realization = generator(
            n_symbols, float(frozen["alpha"]), float(frozen["beta"]), float(cell["f_g_hz"]),
            sop_rate=float(cell["sop_rate"]), seed=int(seed), gamma_bar=gamma_bar,
            block=int(frozen["block"]), t_s=float(frozen["t_s"]), method=str(frozen["method"]),
            modulation=modulation,
        )
        raw = standard_cma_godard_with_z(
            realization["rX"], realization["rY"],
            n_tap=cma_taps, mu=float(frozen["cma_mu"]), R2=R2, block_size=block_size,
        )
        if raw["provenance"].get("gradient") != "Godard-with-z":
            identity_gate_ok = False
            per_seed.append({"seed": int(seed), "identity_gate": "FAILED", "diverged": bool(raw["diverged"])})
            continue
        if raw["diverged"]:
            cell_diverged = True
            per_seed.append({
                "seed": int(seed),
                "identity_gate": "PASS",
                "diverged": True,
                "divergence_symbol": int(raw["divergence_symbol"]) if raw["divergence_symbol"] is not None else None,
                "final_w_norm": float(raw["final_w_norm"]),
            })
            continue

        # Slice the eval window out of the converged tail.
        zX = np.asarray(raw["zX"])
        zY = np.asarray(raw["zY"])
        z_calib = np.column_stack((zX[eval_start:calibration_end], zY[eval_start:calibration_end]))
        z_eval = np.column_stack((zX[calibration_end:eval_end], zY[calibration_end:eval_end]))
        truth_calib = np.column_stack((
            realization["sX"][eval_start:calibration_end],
            realization["sY"][eval_start:calibration_end],
        ))
        truth_eval = np.column_stack((
            realization["sX"][calibration_end:eval_end],
            realization["sY"][calibration_end:eval_end],
        ))
        bits_x_calib = realization["bitsX"][eval_start * 4:calibration_end * 4] if modulation == "qam16" \
            else realization["bitsX"][eval_start * 2:calibration_end * 2]
        bits_y_calib = realization["bitsY"][eval_start * 4:calibration_end * 4] if modulation == "qam16" \
            else realization["bitsY"][eval_start * 2:calibration_end * 2]
        bits_x_eval = realization["bitsX"][calibration_end * 4:eval_end * 4] if modulation == "qam16" \
            else realization["bitsX"][calibration_end * 2:eval_end * 2]
        bits_y_eval = realization["bitsY"][calibration_end * 4:eval_end * 4] if modulation == "qam16" \
            else realization["bitsY"][calibration_end * 2:eval_end * 2]

        # Decide which evaluator to use based on modulation
        if modulation == "qam16":
            nearest_predicted = evaluator.hard_16qam(z_eval)
            blind = evaluator.blind_affine_compare_16qam(z_calib, z_eval, ridge=affine_ridge)
            oracle_corrected = evaluator.oracle_affine_bound_16qam(
                z_calib, z_eval, truth_calib, ridge=affine_ridge,
            )
            nearest_m = evaluator.evaluate_dual_16qam(
                nearest_predicted[:, 0], nearest_predicted[:, 1],
                truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
            )
            blind_m = evaluator.evaluate_dual_16qam(
                blind["predicted"][:, 0], blind["predicted"][:, 1],
                truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
            )
            oracle_m = evaluator.evaluate_dual_16qam(
                oracle_corrected[:, 0], oracle_corrected[:, 1],
                truth_eval[:, 0], truth_eval[:, 1], bits_x_eval, bits_y_eval,
            )
        else:  # qpsk — use P03 evaluator for byte-identical regression
            p03 = evaluator._P03
            amplitude = float(frozen["constellation_amplitude_per_axis"])
            nearest_predicted = p03.hard_qpsk(z_eval, amplitude)
            blind = p03.blind_affine_compare(z_calib, z_eval, ridge=affine_ridge)
            oracle_corrected = p03.oracle_affine_bound(
                z_calib, z_eval, truth_calib, ridge=affine_ridge,
            )
            nearest_m = p03.evaluate_dual_qpsk(
                nearest_predicted[:, 0], nearest_predicted[:, 1],
                truth_eval[:, 0], truth_eval[:, 1],
            )
            blind_m = p03.evaluate_dual_qpsk(
                blind["predicted"][:, 0], blind["predicted"][:, 1],
                truth_eval[:, 0], truth_eval[:, 1],
            )
            oracle_m = p03.evaluate_dual_qpsk(
                oracle_corrected[:, 0], oracle_corrected[:, 1],
                truth_eval[:, 0], truth_eval[:, 1],
            )

        per_seed.append({
            "seed": int(seed),
            "identity_gate": "PASS",
            "diverged": False,
            "nearest": nearest_m,
            "blind": blind_m,
            "oracle": oracle_m,
        })

    # Aggregate across paired seeds by simple averaging of per-seed metrics
    valid_seeds = [row for row in per_seed if row.get("identity_gate") == "PASS" and not row.get("diverged", False)]

    def _mean(key, metric="pi_ser"):
        vals = [float(row[key][metric]) for row in valid_seeds if key in row]
        return float(np.mean(vals)) if vals else float("nan")

    def _mean_fixed(key):
        vals = [float(row[key]["fixed_label_ser"]) for row in valid_seeds if key in row]
        return float(np.mean(vals)) if vals else float("nan")

    nearest_pi_ser = _mean("nearest")
    blind_pi_ser = _mean("blind")
    oracle_pi_ser = _mean("oracle")
    visible_headroom = (
        float("nan") if np.isnan(nearest_pi_ser) or np.isnan(oracle_pi_ser)
        else max(nearest_pi_ser - oracle_pi_ser, 0.0)
    )
    simple_gain = (
        float("nan") if np.isnan(nearest_pi_ser) or np.isnan(blind_pi_ser)
        else max(nearest_pi_ser - min(nearest_pi_ser, blind_pi_ser), 0.0)
    )
    n_error_events = int(sum(
        int(row["nearest"]["pi_ser"] > 0.0) + int(row["oracle"]["pi_ser"] > 0.0)
        for row in valid_seeds
    ))
    n_paired_seeds = len(valid_seeds)
    zero_error_upper_bound = rule_of_three_upper_bound(n_paired_seeds)
    decision = per_cell_decision(
        visible_headroom=visible_headroom if not np.isnan(visible_headroom) else 0.0,
        simple_gain=simple_gain if not np.isnan(simple_gain) else 0.0,
        nearest_pi_ser=nearest_pi_ser,
        blind_pi_ser=blind_pi_ser,
        oracle_pi_ser=oracle_pi_ser,
        n_paired_seeds=n_paired_seeds,
        n_error_events=n_error_events,
        zero_error_upper_bound=zero_error_upper_bound,
        minimum_detectable_effect=float(contract["statistical_sensitivity"]["minimum_detectable_effect"]["value"]),
        diverged=cell_diverged,
    )
    return {
        "cell_id": str(cell["id"]),
        "axes": {
            "modulation": modulation,
            "snr_db": float(cell["snr_db"]),
            "f_g_hz": float(cell["f_g_hz"]),
            "sop_rate": float(cell["sop_rate"]),
            "n_symbols": int(cell["n_symbols"]),
            "csi_access_class": "CSI_NONE",
            "task_output": "uncoded_hard_decision",
        },
        "R2": R2,
        "gamma_bar": gamma_bar,
        "eval_window": {"eval_start": eval_start, "calibration_end": calibration_end, "eval_end": eval_end},
        "n_paired_seeds": n_paired_seeds,
        "n_paired_seeds_requested": len(paired_seeds),
        "n_diverged_seeds": int(sum(1 for row in per_seed if row.get("diverged", False))),
        "identity_gate_ok": bool(identity_gate_ok),
        "paired_seeds": [int(seed) for seed in paired_seeds],
        "per_seed_metrics": per_seed,
        "decision": decision,
        "mean_fixed_label_ser": {"nearest": _mean_fixed("nearest"), "blind": _mean_fixed("blind"), "oracle": _mean_fixed("oracle")},
    }


__all__ = [
    "standard_cma_godard_with_z",
    "eval_window_for",
    "rule_of_three_upper_bound",
    "per_cell_decision",
    "run_cell",
]
