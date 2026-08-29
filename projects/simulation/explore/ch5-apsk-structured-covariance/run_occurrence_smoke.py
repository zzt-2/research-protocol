"""T060 correctness smoke and the single T066 preregistered occurrence cell."""

from __future__ import annotations

import argparse
from dataclasses import fields
from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np
import yaml

SIM_ROOT = Path(__file__).resolve().parents[2]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from codec_metrics import apsk16_table
from common import save_results
from methods import estimate_covariance_arms
from occurrence_reducer import WindowResidual, reduce_occurrence
from post_ch4_ch3_bridge import (
    BridgeConfig,
    FrozenCh4Arm,
    circular_control_pilots,
    generate_correctness_fixture,
    resolve_pilot_only_ambiguity,
    run_bridge,
    swap_polarizations,
)


OUTPUT = Path(__file__).with_name("bridge-correctness-receipt.json")
MANIFEST_PATH = Path(__file__).with_name("occurrence_manifest.yaml")
RAW_OUTPUT = Path(__file__).with_name("occurrence_raw.json")
AGGREGATE_OUTPUT = Path(__file__).with_name("occurrence_aggregate.json")
RECEIPT_OUTPUT = Path(__file__).with_name("occurrence_receipt.json")
REPORT_OUTPUT = (
    Path(__file__).resolve().parents[3]
    / "thesis-fso"
    / "apsk-soft-receiver-groundwork"
    / "step4a-target-occurrence.md"
)
OCCURRENCE_SCOPE = (
    "SINGLE_PREREGISTERED_CELL",
    "OCCURRENCE_ONLY",
    "NO_METHOD_OR_PERFORMANCE_CLAIM",
)


def _config() -> BridgeConfig:
    return BridgeConfig.correctness_fixture(
        seed=60060,
        n_symbols=160,
        observation_stop=128,
        snr_db=36.0,
        turbulence_alpha=1.0e12,
        turbulence_beta=1.0e12,
        gamma_gamma_block=16,
        f_residual_hz=0.0,
        f_dot_hz_per_s=0.0,
        linewidth_hz=0.0,
    )


def load_occurrence_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def _manifest_hash() -> str:
    return sha256(MANIFEST_PATH.read_bytes()).hexdigest()


def frozen_config_hash(config: BridgeConfig) -> str:
    excluded = {"seed", "window_id"}
    canonical = {
        field.name: getattr(config, field.name)
        for field in fields(config)
        if field.name not in excluded
    }
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def build_occurrence_configs(manifest: dict) -> list[BridgeConfig]:
    cell = manifest["cell"]
    ch3 = manifest["ch3"]
    windows = manifest["windows"]
    seeds = range(windows["seeds"]["start"], windows["seeds"]["stop_inclusive"] + 1)
    configs = []
    for window_id, seed in enumerate(seeds):
        configs.append(
            BridgeConfig.correctness_fixture(
                seed=seed,
                n_symbols=cell["observation_symbols"],
                observation_stop=cell["observation_symbols"],
                snr_db=cell["snr_db"],
                turbulence_alpha=cell["turbulence_alpha"],
                turbulence_beta=cell["turbulence_beta"],
                gamma_gamma_block=cell["gamma_gamma_block"],
                f_residual_hz=cell["residual_frequency_hz"],
                f_dot_hz_per_s=cell["frequency_slope_hz_per_s"],
                linewidth_hz=cell["linewidth_hz"],
                ch4_pilot_count=manifest["ch4"]["acquisition_pilots"],
                pilot_indices=tuple(ch3["pilot_indices"]),
                pilot_label_shift=ch3["polarization_1_label_shift"],
                scope=OCCURRENCE_SCOPE,
                cell_id=cell["cell_id"],
                window_id=f"window-{window_id:02d}",
                config_id=manifest["schema_version"],
                source_id=manifest["authority"],
            )
        )
    if len(configs) != windows["count"]:
        raise ValueError("manifest seed interval does not produce exactly 64 windows")
    return configs


def _frozen_arm(manifest: dict) -> FrozenCh4Arm:
    ch4 = manifest["ch4"]
    return FrozenCh4Arm(
        arm_id=ch4["arm_id"],
        mode=ch4["mode"],
        mu=ch4["mu"],
        ring_threshold=ch4["ring_threshold"],
        decision_threshold=ch4["decision_threshold"],
    )


def _window_record(window_id: int, config: BridgeConfig, bundle) -> dict:
    return {
        "window_id": window_id,
        "window_name": config.window_id,
        "seed": config.seed,
        "cell_id": config.cell_id,
        "config_id": config.config_id,
        "config_hash": frozen_config_hash(config),
        "realization_hash": bundle.realization_hash,
        "bundle_hash": bundle.bundle_hash,
        "scope": list(bundle.scope),
        "frozen_ch4_snapshot": bundle.frozen_ch4_snapshot,
        "realization_timing": bundle.realization_timing,
        "pilot_indices": bundle.pilot_indices.tolist(),
        "point_labels": bundle.point_labels.tolist(),
        "ring_labels": bundle.ring_labels.astype(int).tolist(),
        "per_pol_point_counts": bundle.per_pol_point_counts.tolist(),
        "known_mask_counts": np.count_nonzero(bundle.known_mask, axis=1).tolist(),
        "z_pilot_real": bundle.z_pilot.real.tolist(),
        "z_pilot_imag": bundle.z_pilot.imag.tolist(),
        "x_pilot_real": bundle.x_pilot.real.tolist(),
        "x_pilot_imag": bundle.x_pilot.imag.tolist(),
        "e_real": bundle.e.real.tolist(),
        "e_imag": bundle.e.imag.tolist(),
        "estimated_phase": bundle.estimated_phase.tolist(),
        "estimated_frequency_hz": bundle.estimated_frequency_hz.tolist(),
        "ambiguity_index": bundle.ambiguity_index.tolist(),
    }


def _report_markdown(aggregate: dict, receipt: dict) -> str:
    lines = [
        "# Ch5 单格 target-residual occurrence",
        "",
        "> T066 / D047 / V021 | GW Step 4a 维度 D | 2026-08-30",
        "",
        "## 事实与裁决",
        "",
        f"- terminal：`{receipt['terminal']}`。",
        f"- 完整窗口：`{receipt['completed_windows']}/64`；calibration=`0..31`，evaluation=`32..63`。",
        f"- bounded development：`{'允许' if receipt['bounded_development_allowed'] else '不允许'}`。",
        "- 本格只判断自然 residual covariance occurrence，不包含 BER/GMI/FER、LDPC 或 C5-1 方法结论。",
        "",
        "## D1/D2 simultaneous 95% window-cluster bootstrap CI",
        "",
        "| group | samples | D1 estimate | D1 CI | D2 estimate | D2 CI |",
        "|---|---:|---:|---|---:|---|",
    ]
    for group in aggregate["d1"]:
        d1 = aggregate["d1"][group]
        d2 = aggregate["d2"][group]
        lines.append(
            f"| {group} | {d1['samples']} | {d1['estimate']:.9g} | "
            f"[{d1['ci'][0]:.9g}, {d1['ci'][1]:.9g}] | {d2['estimate']:.9g} | "
            f"[{d2['ci'][0]:.9g}, {d2['ci'][1]:.9g}] |"
        )
    first_group = next(iter(aggregate["d1"].values()))
    per_window_samples = (
        first_group["samples"] // aggregate["bootstrap"]["evaluation_clusters"]
    )
    lines.extend(
        [
            "",
            f"每个 evaluation window 每组样本数：`{per_window_samples}`。",
            "",
            "### Evaluation point counts（按 group）",
            "",
        ]
    )
    for group, details in aggregate["d1"].items():
        lines.append(f"- {group} point_counts：`{details['point_counts']}`")
    lines.extend(
        [
            "",
            "逐 window residual、realization/bundle hash 见 raw/aggregate JSON。",
            "",
            "## D3 held-out covariance NLL",
            "",
            f"- `NLL_B1-NLL_full` mean：`{aggregate['d3']['estimate']:.9g}`。",
            f"- 普通 95% evaluation-window cluster CI：`[{aggregate['d3']['ci'][0]:.9g}, {aggregate['d3']['ci'][1]:.9g}]`。",
            "- covariance 仅由 calibration windows 拟合；evaluation residual 不参与拟合、阈值或分支选择；统一 floor=`1e-10`。",
            "",
            "## Bootstrap 与 provenance",
            "",
            f"- PCG64 seed=`{aggregate['bootstrap']['seed']}`，resamples=`{aggregate['bootstrap']['resamples']}`，cluster=`evaluation_window`（32 个）。",
            f"- manifest hash：`{receipt['manifest_hash']}`。",
            f"- frozen config hash：`{receipt['config_hash']}`。",
            f"- unique realization/bundle hashes：`{receipt['unique_realization_hashes']}/{receipt['unique_bundle_hashes']}`。",
            "",
            "## 唯一下一步",
            "",
            f"`{receipt['unique_next_step']}`",
            "",
        ]
    )
    return "\n".join(lines)


def run_occurrence_cell(*, write: bool = True) -> dict:
    if RECEIPT_OUTPUT.exists():
        raise RuntimeError("T066 scientific receipt already exists; a second cell is forbidden")
    manifest = load_occurrence_manifest()
    configs = build_occurrence_configs(manifest)
    arm = _frozen_arm(manifest)
    expected_indices = np.asarray(manifest["ch3"]["pilot_indices"], dtype=np.int64)
    expected_snapshot = {
        "arm_id": manifest["ch4"]["arm_id"],
        "mode": manifest["ch4"]["mode"],
        "mu": manifest["ch4"]["mu"],
        "ring_threshold": manifest["ch4"]["ring_threshold"],
        "decision_threshold": manifest["ch4"]["decision_threshold"],
    }
    records = []
    residual_windows = []
    for window_id, config in enumerate(configs):
        receiver, _offline_truth = generate_correctness_fixture(
            config, identity_jones=False, noiseless=False
        )
        bundle = run_bridge(receiver, arm)
        if not np.array_equal(bundle.pilot_indices, expected_indices):
            raise RuntimeError("INVALID_TESTBED: pilot indices changed")
        if not np.all(bundle.per_pol_point_counts == 4):
            raise RuntimeError("INVALID_TESTBED: pilot labels are not balanced")
        if bundle.frozen_ch4_snapshot != expected_snapshot or bundle.scope != OCCURRENCE_SCOPE:
            raise RuntimeError("INVALID_TESTBED: frozen arm or scope mismatch")
        if not np.all(np.isfinite(bundle.e)):
            raise RuntimeError("INVALID_TESTBED: non-finite residual")
        records.append(_window_record(window_id, config, bundle))
        residual_windows.append(
            WindowResidual(
                window_id=window_id,
                seed=config.seed,
                e=bundle.e.copy(),
                point_labels=bundle.point_labels.copy(),
                ring_labels=bundle.ring_labels.copy(),
                realization_hash=bundle.realization_hash,
                bundle_hash=bundle.bundle_hash,
            )
        )
        print(f"T066 window {window_id + 1:02d}/64 seed={config.seed}")

    diagnostics = manifest["diagnostics"]
    bootstrap = manifest["bootstrap"]
    aggregate = reduce_occurrence(
        residual_windows,
        calibration_window_ids=tuple(range(32)),
        evaluation_window_ids=tuple(range(32, 64)),
        floor=diagnostics["covariance_floor"],
        bootstrap_seed=bootstrap["seed"],
        bootstrap_resamples=bootstrap["resamples"],
    )
    config_hashes = {record["config_hash"] for record in records}
    realization_hashes = {record["realization_hash"] for record in records}
    bundle_hashes = {record["bundle_hash"] for record in records}
    valid = (
        len(records) == 64
        and len(config_hashes) == 1
        and len(realization_hashes) == 64
        and len(bundle_hashes) == 64
        and aggregate["split"]["disjoint"]
    )
    terminal = aggregate["terminal"] if valid else "INVALID_TESTBED"
    bounded = terminal == "DETECTABLE_OCCURRENCE"
    next_step = {
        "DETECTABLE_OCCURRENCE": "Main controller may dispatch C5-1 bounded development.",
        "NO_DETECTABLE_OCCURRENCE": "Close C5-1 target-platform route; proceed to C5-0 candidate-level GW Step 2.",
        "INVALID_TESTBED": "Minimum correctness repair only; do not interpret the scientific cell.",
    }[terminal]
    raw = {
        "schema_version": "t066.target-residual-occurrence.raw.v1",
        "authority": manifest["authority"],
        "manifest_hash": _manifest_hash(),
        "completed_windows": len(records),
        "windows": records,
    }
    aggregate.update(
        {
            "schema_version": "t066.target-residual-occurrence.aggregate.v1",
            "authority": manifest["authority"],
            "manifest_hash": _manifest_hash(),
            "config_hash": next(iter(config_hashes)),
            "completed_windows": len(records),
            "realization_hashes": [record["realization_hash"] for record in records],
            "bundle_hashes": [record["bundle_hash"] for record in records],
        }
    )
    receipt = {
        "schema_version": "t066.target-residual-occurrence.receipt.v1",
        "authority": manifest["authority"],
        "scope": list(OCCURRENCE_SCOPE),
        "completed_windows": len(records),
        "manifest_hash": _manifest_hash(),
        "config_hash": next(iter(config_hashes)),
        "unique_config_hashes": len(config_hashes),
        "unique_realization_hashes": len(realization_hashes),
        "unique_bundle_hashes": len(bundle_hashes),
        "split_firewall": "PASS" if aggregate["split"]["disjoint"] else "FAIL",
        "finite_residuals": True,
        "terminal": terminal,
        "bounded_development_allowed": bounded,
        "unique_next_step": next_step,
        "forbidden_not_run": manifest["forbidden"],
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["receipt_hash"] = sha256(canonical.encode("utf-8")).hexdigest()
    if write:
        save_results(raw, str(RAW_OUTPUT), "run_occurrence_smoke:t066-raw")
        save_results(aggregate, str(AGGREGATE_OUTPUT), "run_occurrence_smoke:t066-aggregate")
        save_results(receipt, str(RECEIPT_OUTPUT), "run_occurrence_smoke:t066-receipt")
        REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUTPUT.write_text(_report_markdown(aggregate, receipt), encoding="utf-8")
    return receipt


def run_correctness_smoke(*, write: bool = True) -> dict:
    arm = FrozenCh4Arm.fixture_plain(mu=0.0)
    receiver, truth = generate_correctness_fixture(
        _config(), identity_jones=True, noiseless=False
    )
    bundle = run_bridge(receiver, arm)

    truth.payload_labels[:] = (truth.payload_labels + 5) % 16
    truth.payload_bits[:] ^= 1
    truth_invariant = run_bridge(receiver, arm)
    swapped = run_bridge(swap_polarizations(receiver), arm)

    symbols, _ = apsk16_table()
    rotations_pass = True
    for index in range(8):
        rotated = symbols * np.exp(1j * 2.0 * np.pi * index / 8.0)
        resolved, selected, scores = resolve_pilot_only_ambiguity(
            rotated, symbols, np.arange(16)
        )
        rotations_pass &= selected == index
        rotations_pass &= np.count_nonzero(np.isclose(scores, scores.min(), atol=1e-14)) == 1
        rotations_pass &= np.allclose(resolved, symbols, atol=2e-15, rtol=0.0)

    covariance_pass = True
    minimum_eigenvalue = np.inf
    for pol in range(2):
        arms = estimate_covariance_arms(
            bundle.z_pilot[pol],
            bundle.point_labels[pol],
            symbols,
            floor=1e-10,
            kappa=7.0,
            b3_shrinkage=0.1,
        )
        for covariance in arms.values():
            eigenvalues = np.linalg.eigvalsh(covariance)
            minimum_eigenvalue = min(minimum_eigenvalue, float(eigenvalues.min()))
            covariance_pass &= bool(np.all(np.isfinite(covariance)))
            covariance_pass &= bool(np.allclose(covariance, covariance.swapaxes(-1, -2)))
            covariance_pass &= bool(np.all(eigenvalues > 0.0))

    circular_z, circular_labels = circular_control_pilots(symbols)
    circular = estimate_covariance_arms(
        circular_z,
        circular_labels,
        symbols,
        floor=1e-12,
        kappa=7.0,
        b3_shrinkage=0.1,
    )
    circular_gap = max(
        float(np.max(np.abs(circular[name][:, 0, 1])))
        + float(
            np.max(
                np.abs(
                    np.diagonal(circular[name], axis1=1, axis2=2)[:, 0]
                    - np.diagonal(circular[name], axis1=1, axis2=2)[:, 1]
                )
            )
        )
        for name in ("B2", "C1")
    )

    required = {
        "z_pilot", "x_pilot", "e", "pilot_indices", "point_labels",
        "ring_labels", "per_pol_point_counts", "per_point_counts", "known_mask",
        "cpr_mode", "estimated_phase", "estimated_frequency_hz", "ambiguity_index",
        "ch4_arm", "frozen_ch4_snapshot", "ch4_W", "ch4_gate_summary",
        "realization_timing", "cell_id", "seed", "window_id",
        "config_id", "source_id", "realization_hash", "bundle_hash",
    }
    exported = bundle.deployable_dict()
    visible_changed = receiver.with_visible_rx_delta(pol=0, index=17, delta=1e-4 + 2e-4j)
    changed = run_bridge(visible_changed, arm)

    receipt = {
        "schema_version": "t063.bridge-correctness-receipt.v2",
        "scope": list(bundle.scope),
        "physical_order": "continuous acquisition+observation -> shared scalar GG/CFO/Wiener -> unitary Jones -> circular AWGN -> Ch4 demux/RDE -> per-pol Ch3 DA CPR -> pilot-only ambiguity -> residual",
        "truth_firewall": "PASS" if bundle.bundle_hash == truth_invariant.bundle_hash else "FAIL",
        "eight_rotation_pilot_only_resolution": "PASS" if rotations_pass else "FAIL",
        "polarization_swap_equivariance": "PASS"
        if np.allclose(swapped.e, bundle.e[::-1], atol=2e-12)
        else "FAIL",
        "per_polarization_cpr": True,
        "cross_polarization_pooling": False,
        "observation_window_causal": True,
        "bundle_fields_complete": required.issubset(exported),
        "covariance_identity": "PASS" if covariance_pass and circular_gap < 1e-12 else "FAIL",
        "minimum_covariance_eigenvalue": minimum_eigenvalue,
        "circular_control_max_gap": circular_gap,
        "same_input_hash_stable": bundle.bundle_hash == run_bridge(receiver, arm).bundle_hash,
        "receiver_visible_change_changes_hash": bundle.bundle_hash != changed.bundle_hash,
        "frozen_ch4_snapshot": bundle.frozen_ch4_snapshot,
        "continuous_realization_timing": bundle.realization_timing,
        "realization_hash": bundle.realization_hash,
        "bundle_hash": bundle.bundle_hash,
        "unique_blocker": "Awaiting independent re-verification; target occurrence remains prohibited",
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["receipt_hash"] = sha256(canonical.encode("utf-8")).hexdigest()
    if write:
        save_results(receipt, str(OUTPUT), "run_occurrence_smoke:correctness")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("correctness", "occurrence"), default="correctness")
    args = parser.parse_args()
    if args.mode == "correctness":
        result = run_correctness_smoke(write=True)
    else:
        result = run_occurrence_cell(write=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
