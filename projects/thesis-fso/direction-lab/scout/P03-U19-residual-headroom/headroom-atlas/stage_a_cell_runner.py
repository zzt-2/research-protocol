"""Headroom Atlas Stage A cell runner — baseline-only, behind the gate.

This runner reuses the P03 frozen source closure (standard-CMA Godard-with-z
+ nearest-QPSK + same-information blind affine + scoring-only oracle affine)
and parameterizes the runnable representative axes: SNR (via gamma_bar),
turbulence timescale (f_g_hz), SOP dynamics (sop_rate) and observation length
(N). It is baseline-only: no ML is trained and the comparators are exactly
the strongest legal non-ML comparators registered for the P03 Scout.

Every cell returns the structured per-cell verdict in the schema declared by
``stage-a-contract.v1.yaml``. The runner is intentionally not callable without
the gate: the :class:`AtlasRunner` in :mod:`atlas_gate` wraps this function
and refuses to call it without an authorization token bound to a fresh PASS
receipt.
"""

from __future__ import annotations

import importlib.util
import math
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

import numpy as np
import yaml


HERE = Path(__file__).resolve()
SCOUT_ROOT = HERE.parent.parent  # .../scout/P03-U19-residual-headroom
REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _sha(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _decode_window(window: Mapping[str, Any]) -> np.ndarray:
    streams = []
    for name in ("zX", "zY"):
        pairs = np.asarray(window["streams"][name], dtype=np.float64)
        streams.append(np.asarray(pairs[:, 0] + 1j * pairs[:,1], dtype=np.complex128))
    return np.column_stack(streams)


def _rule_of_three_upper_bound(n_paired_cells: int, confidence: float = 0.95) -> float:
    """Rule-of-three upper bound on the per-cell error rate when zero errors are
    observed across ``n_paired_cells`` independent paired cells.

    With n independent Bernoulli trials all zero, a 1-sided (1-alpha) upper
    bound on the per-trial success-of-failing probability is 1-(alpha)**(1/n).
    This is the standard "rule of three" used for zero-numerator confidence
    bounds.
    """
    if n_paired_cells <= 0:
        return float("nan")
    alpha = 1.0 - confidence
    return 1.0 - alpha ** (1.0 / float(n_paired_cells))


def _eval_window_for(n_symbols: int, cma_taps: int, *, window_symbols: int = 256, block_size: int = 64) -> tuple[int, int, int, int]:
    """Pick eval_start, calibration_end, eval_end, half_taps.

    Mirrors the P03 v1 contract geometry (calibration 50%, evaluation 50%,
    both inside the CMA-converged tail of the generated sequence), but
    generalizes to arbitrary total length. For long windows, the eval window
    still sits in the late slice so that SOP accumulation is exercised.

    The frozen prompt013 CMA diagnostic aligns trace blocks at
    ``output_start = block * block_size + half``; to keep the adapter's
    ``_validate_trace`` gate passing we therefore require
    ``(eval_start - half) % block_size == 0``. P03 v1 used eval_start=133 with
    half=5 and block_size=64, which satisfies 133 == 2*64+5.
    """
    half_taps = cma_taps // 2
    if half_taps < 1 or block_size < 1:
        raise ValueError("cma_taps and block_size must be positive")
    # leave a CMA convergence prefix proportional to N (P03 v1: 133 prefix on N=512)
    raw_prefix = max(int(round(n_symbols * 0.26)), cma_taps + 1)
    # align prefix to the block + half grid so eval_start = block*block_size + half
    block_index = (raw_prefix - half_taps + block_size - 1) // block_size  # ceil
    eval_start = block_index * block_size + half_taps
    if eval_start <= cma_taps:
        eval_start += block_size
    window_symbols = min(window_symbols, max(n_symbols - eval_start - cma_taps, block_size))
    # also keep the window length a multiple of block_size so the trailing
    # block aligns (the adapter requires the last block's output_end == eval_end)
    window_symbols = (window_symbols // block_size) * block_size
    if window_symbols < block_size:
        raise ValueError(f"eval window too small for N={n_symbols}: window={window_symbols}")
    calibration_end = eval_start + window_symbols // 2
    eval_end = eval_start + window_symbols
    if not (eval_start < calibration_end < eval_end):
        raise ValueError(f"eval window geometry invalid for N={n_symbols}")
    return eval_start, calibration_end, eval_end, half_taps


def _per_cell_decision(
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
) -> dict[str, Any]:
    """Map raw cell metrics to a structured per-cell verdict.

    decision_class follows the Direction Lab claim-scope lattice:
    - LOCAL_NEGATIVE: cell has no visible headroom (oracle_affine == nearest)
    - ADVANCE: cell has visible headroom >= MDE AND the simple same-information
      comparator captures some of it (a learned detector could plausibly do
      better)
    - NON_DECISIVE: visible headroom exists but below the minimum detectable
      effect, or the same-information comparator captured nothing measurable
    """
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


def run_cell(
    cell: Mapping[str, Any],
    contract: Mapping[str, Any],
    *,
    generator: Any,
    runner: Any,
    adapter: Any,
    evaluator: Any,
    run_b001_path: Path,
) -> dict[str, Any]:
    """Run one Stage A cell. Returns the structured per-cell verdict + raw metrics.

    The caller must be the gated :class:`atlas_gate.AtlasRunner`; this function
    does not check the gate itself.
    """
    gamma_bar = float(10.0 ** (float(cell["snr_db"]) / 10.0))
    n_symbols = int(cell["n_symbols"])
    cma_taps = int(contract["frozen_common_axes"]["cma_taps"])
    eval_start, calibration_end, eval_end, half_taps = _eval_window_for(
        n_symbols, cma_taps, window_symbols=256,
        block_size=int(contract["frozen_common_axes"]["cma_block_size"]),
    )
    frozen = contract["frozen_common_axes"]
    paired_seeds = contract["covering_design"]["paired_seeds"]
    per_seed = []
    for seed in paired_seeds:
        realization = generator(
            n_symbols, float(frozen["alpha"]), float(frozen["beta"]), float(cell["f_g_hz"]),
            sop_rate=float(cell["sop_rate"]), seed=int(seed), gamma_bar=gamma_bar,
            block=int(frozen["block"]), t_s=float(frozen["t_s"]), method=str(frozen["method"]),
        )
        cfg = SimpleNamespace(
            mu=float(frozen["cma_mu"]), taps=cma_taps, r2=float(frozen["r2"]),
            block_size=int(frozen["cma_block_size"]), eval_start=eval_start, eval_end=eval_end,
            fade_threshold_h=float(frozen["fade_threshold_h"]), clip_norm=float(frozen["clip_norm"]),
        )
        raw = runner(
            {"rX": realization["rX"], "rY": realization["rY"]}, cfg,
            variant="baseline", return_blind_trace=True,
        )
        if raw.get("provenance", {}).get("gradient") != "Godard-with-z":
            raise RuntimeError(f"standard-CMA identity gate failed for cell {cell['id']} seed {seed}")
        sequence_id = f"atlas-stage-a-{cell['id']}-seed-{seed}"
        window = adapter.adapt_standard_cma_output(
            raw,
            sequence_id=sequence_id,
            symbol_start=eval_start,
            symbol_end=eval_end,
            equalizer_taps=cma_taps,
            csi_access_class="CSI_NONE",
            source_id="run_b001._default_runner",
            source_hash=_sha(run_b001_path),
            receiver_estimated_csi=None,
        )
        z = _decode_window(window)
        split = calibration_end - eval_start
        z_calibration, z_evaluation = z[:split], z[split:]
        truth_calibration = np.column_stack((
            realization["sX"][eval_start:calibration_end],
            realization["sY"][eval_start:calibration_end],
        ))
        truth_evaluation = np.column_stack((
            realization["sX"][calibration_end:eval_end],
            realization["sY"][calibration_end:eval_end],
        ))
        amplitude = float(frozen["constellation_amplitude_per_axis"])
        nearest_predicted = evaluator.hard_qpsk(z_evaluation, amplitude)
        blind = evaluator.blind_affine_compare(z_calibration, z_evaluation, ridge=float(frozen["affine_ridge"]))
        oracle_corrected = evaluator.oracle_affine_bound(
            z_calibration, z_evaluation, truth_calibration, ridge=float(frozen["affine_ridge"])
        )
        nearest_m = evaluator.evaluate_dual_qpsk(nearest_predicted[:, 0], nearest_predicted[:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1])
        blind_m = evaluator.evaluate_dual_qpsk(blind["predicted"][:, 0], blind["predicted"][:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1])
        oracle_m = evaluator.evaluate_dual_qpsk(oracle_corrected[:, 0], oracle_corrected[:, 1], truth_evaluation[:, 0], truth_evaluation[:, 1])
        per_seed.append({
            "seed": int(seed),
            "nearest": nearest_m,
            "blind": blind_m,
            "oracle": oracle_m,
        })
    # aggregate across paired seeds by simple averaging of the per-seed metrics
    def _mean(key): return float(np.mean([row[key]["pi_ser"] for row in per_seed]))
    def _mean_fixed(key): return float(np.mean([row[key]["fixed_label_ser"] for row in per_seed]))
    nearest_pi_ser = _mean("nearest")
    blind_pi_ser = _mean("blind")
    oracle_pi_ser = _mean("oracle")
    # visible headroom is defined per the P03 v1 contract on PI-SER
    visible_headroom = max(nearest_pi_ser - oracle_pi_ser, 0.0)
    simple_gain = max(nearest_pi_ser - min(nearest_pi_ser, blind_pi_ser), 0.0)
    # count error events across seeds for sensitivity reporting
    n_error_events = int(sum(
        int(row["nearest"]["pi_ser"] > 0.0) + int(row["oracle"]["pi_ser"] > 0.0)
        for row in per_seed
    ))
    n_paired_seeds = len(per_seed)
    zero_error_upper_bound = _rule_of_three_upper_bound(n_paired_seeds)
    decision = _per_cell_decision(
        visible_headroom=visible_headroom,
        simple_gain=simple_gain,
        nearest_pi_ser=nearest_pi_ser,
        blind_pi_ser=blind_pi_ser,
        oracle_pi_ser=oracle_pi_ser,
        n_paired_seeds=n_paired_seeds,
        n_error_events=n_error_events,
        zero_error_upper_bound=zero_error_upper_bound,
        minimum_detectable_effect=float(contract["statistical_sensitivity"]["minimum_detectable_effect"]["value"]),
    )
    return {
        "cell_id": str(cell["id"]),
        "axes": {
            "modulation": str(cell["modulation"]),
            "snr_db": float(cell["snr_db"]),
            "f_g_hz": float(cell["f_g_hz"]),
            "sop_rate": float(cell["sop_rate"]),
            "n_symbols": int(cell["n_symbols"]),
            "csi_access_class": "CSI_NONE",
            "task_output": "uncoded_hard_decision",
        },
        "gamma_bar": gamma_bar,
        "eval_window": {"eval_start": eval_start, "calibration_end": calibration_end, "eval_end": eval_end},
        "n_paired_seeds": n_paired_seeds,
        "paired_seeds": [int(seed) for seed in paired_seeds],
        "per_seed_metrics": per_seed,
        "decision": decision,
        "mean_fixed_label_ser": {"nearest": _mean_fixed("nearest"), "blind": _mean_fixed("blind"), "oracle": _mean_fixed("oracle")},
    }


def materialize_closure(contract: Mapping[str, Any]):
    """Build the frozen P03 source closure.

    Returns a context manager that yields a dict of callable pieces
    (generator, runner, adapter, evaluator, run_b001_path, closure_sha). The
    underlying temp source tree is only alive while the context is open, so
    cell runs must happen inside the ``with`` block.
    """
    import contextlib

    equivalence = _load(SCOUT_ROOT / "run_source_equivalence.py", "atlas_stage_a_source_equivalence")
    evaluator = _load(SCOUT_ROOT / "probe_evaluator.py", "atlas_stage_a_probe_evaluator")
    equivalence_contract_path = SCOUT_ROOT / contract["frozen_common_axes"]["source_equivalence_contract"]
    equivalence_contract = yaml.safe_load(equivalence_contract_path.read_text(encoding="utf-8"))

    @contextlib.contextmanager
    def _cm():
        with equivalence.materialized_source(equivalence_contract) as (source_tree, materialization):
            archived_lab = source_tree / "projects/thesis-fso/direction-lab"
            run_b001_path = archived_lab / "tools/run_b001.py"
            run_b001 = _load(run_b001_path, "atlas_stage_a_run_b001")
            adapter = _load(
                archived_lab / "scout/P03-U19-residual-headroom/z_window_adapter.py",
                "atlas_stage_a_z_window_adapter",
            )
            source_root = source_tree / equivalence_contract["base_source_root"]
            generator = run_b001._default_generator(source_root)
            runner, _ = run_b001._default_runner(source_root)
            closure_sha = {
                "run_b001_path": str(run_b001_path),
                "run_b001_sha256": _sha(run_b001_path),
                "z_window_adapter_sha256": _sha(archived_lab / "scout/P03-U19-residual-headroom/z_window_adapter.py"),
                "probe_evaluator_sha256": _sha(SCOUT_ROOT / "probe_evaluator.py"),
                "stage_a_cell_runner_sha256": _sha(HERE),
                "materialization": materialization,
            }
            yield {
                "generator": generator,
                "runner": runner,
                "adapter": adapter,
                "evaluator": evaluator,
                "run_b001_path": run_b001_path,
                "closure_sha": closure_sha,
            }

    return _cm()
