"""T067 preregistered bounded BER/GMI development runner.

# TL-25 checklist: [1/2/3/4/5/6] all confirmed by T067/D048/V022.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

import numpy as np
import yaml

SIM_ROOT = Path(__file__).resolve().parents[2]
if str(SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(SIM_ROOT))

from codec_metrics import apsk16_table, gmi_analytic, mahalanobis_logdet_llr
from common._experiment import save_results
from development_reducer import reduce_round1
from methods import GaussianArm, estimate_gaussian_arms, estimate_covariance_arms
from post_ch4_ch3_bridge import (
    BridgeConfig,
    FrozenCh4Arm,
    generate_correctness_fixture,
    run_bridge_with_observation,
)


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "development_manifest.yaml"
RAW_PATH = ROOT / "development_raw.json"
AGGREGATE_PATH = ROOT / "development_aggregate.json"
RECEIPT_PATH = ROOT / "development_receipt.json"
REPORT_PATH = (
    ROOT.parents[2]
    / "thesis-fso"
    / "apsk-soft-receiver-groundwork"
    / "step4a-bounded-development.md"
)
DEVELOPMENT_SCOPE = (
    "BOUNDED_DEVELOPMENT",
    "PROVISIONAL_ONLY",
    "NO_FINAL_CLAIM",
)


def load_development_manifest(path: Path = MANIFEST_PATH) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def payload_indices(n_symbols: int, pilot_indices: np.ndarray) -> np.ndarray:
    mask = np.ones(int(n_symbols), dtype=bool)
    indices = np.asarray(pilot_indices, dtype=np.int64)
    if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= n_symbols):
        raise ValueError("pilot indices must be one-dimensional and in range")
    mask[indices] = False
    return np.flatnonzero(mask)


def _base_config(manifest: dict, *, seed: int, window_id: str, snr_db: float) -> BridgeConfig:
    chain = manifest["shared_chain"]
    turbulence = chain["turbulence"]
    pilot_spacing = int(chain["pilot_spacing"])
    n_symbols = int(chain["observation_symbols"])
    return BridgeConfig.correctness_fixture(
        seed=int(seed),
        n_symbols=n_symbols,
        observation_stop=n_symbols,
        snr_db=float(snr_db),
        turbulence_alpha=float(turbulence["alpha"]),
        turbulence_beta=float(turbulence["beta"]),
        gamma_gamma_block=int(turbulence["block"]),
        f_residual_hz=float(chain["residual_frequency_hz"]),
        f_dot_hz_per_s=float(chain["frequency_slope_hz_per_s"]),
        linewidth_hz=float(chain["linewidth_hz"]),
        ch4_pilot_count=int(chain["ch4"]["acquisition_pilots"]),
        pilot_indices=tuple(range(0, n_symbols, pilot_spacing)),
        pilot_label_shift=3,
        scope=DEVELOPMENT_SCOPE,
        cell_id=manifest["round1"]["cell_id"],
        window_id=window_id,
        config_id=manifest["schema_version"],
        source_id=manifest["authority"],
    )


def build_round1_configs(manifest: dict) -> list[BridgeConfig]:
    round1 = manifest["round1"]
    seeds = range(int(round1["seeds"]["start"]), int(round1["seeds"]["stop_inclusive"]) + 1)
    return [
        _base_config(
            manifest,
            seed=seed,
            window_id=f"round1-window-{index:02d}",
            snr_db=float(round1["snr_db"]),
        )
        for index, seed in enumerate(seeds)
    ]


def frozen_ch4_arm(manifest: dict) -> FrozenCh4Arm:
    value = manifest["shared_chain"]["ch4"]
    return FrozenCh4Arm(
        arm_id=value["arm_id"],
        mode=value["mode"],
        mu=float(value["mu"]),
        ring_threshold=value["ring_threshold"],
        decision_threshold=value["decision_threshold"],
    )


def _config_hash(config: BridgeConfig) -> str:
    payload = asdict(config)
    payload.pop("seed")
    payload.pop("window_id")
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _score_model(
    observations: np.ndarray,
    true_labels: np.ndarray,
    true_bits: np.ndarray,
    models: list[GaussianArm],
    *,
    clip: float,
    floor: float,
) -> dict:
    llrs = []
    bits = []
    nll_values = []
    eigenvalues = []
    started = time.perf_counter()
    for pol in range(2):
        model = models[pol]
        llr = mahalanobis_logdet_llr(
            observations[pol], model.means, model.covariances, clip=clip
        )
        llrs.append(llr)
        bits.append(true_bits[pol])
        eigenvalues.append(np.linalg.eigvalsh(model.covariances))
        xy = np.column_stack((observations[pol].real, observations[pol].imag))
        means_xy = np.column_stack((model.means.real, model.means.imag))
        for sample_index, label in enumerate(true_labels[pol]):
            covariance = model.covariances[int(label)]
            delta = xy[sample_index] - means_xy[int(label)]
            sign, logdet = np.linalg.slogdet(covariance)
            if sign <= 0:
                raise ValueError("non-positive covariance reached payload scoring")
            quadratic = float(delta @ np.linalg.solve(covariance, delta))
            nll_values.append(0.5 * (quadratic + logdet + 2.0 * np.log(2.0 * np.pi)))
    llr_array = np.concatenate(llrs, axis=0)
    bit_array = np.concatenate(bits, axis=0).astype(np.uint8, copy=False)
    hard = (llr_array >= 0.0).astype(np.uint8)
    errors = int(np.count_nonzero(hard != bit_array))
    total = int(bit_array.size)
    eigen = np.concatenate(eigenvalues, axis=0)
    condition = eigen[:, 1] / eigen[:, 0]
    return {
        "gmi": gmi_analytic(llr_array, bit_array),
        "ber": float(errors / total),
        "bit_errors": errors,
        "payload_bits": total,
        "nll": float(np.mean(nll_values)),
        "condition_max": float(np.max(condition)),
        "floor_rate": float(np.mean(eigen <= floor * (1.0 + 1.0e-9))),
        "runtime_s": float(time.perf_counter() - started),
    }


def evaluate_window(
    config: BridgeConfig,
    manifest: dict,
    *,
    round_name: str,
    split: str,
    snr_db: float,
) -> dict:
    """Generate one shared physical realization and score every frozen arm."""
    receiver, truth = generate_correctness_fixture(
        config, identity_jones=False, noiseless=False
    )
    bundle, observation = run_bridge_with_observation(
        receiver, frozen_ch4_arm(manifest)
    )
    payload = payload_indices(config.observation_stop, bundle.pilot_indices)
    payload_observation = observation[:, payload]
    payload_labels = truth.payload_labels[:, payload]
    payload_bits = truth.payload_bits[:, payload]
    symbols, _ = apsk16_table()
    floor = float(manifest["fairness"]["covariance_floor"])
    clip = float(manifest["fairness"]["llr_clip"])
    c1_values = [float(value) for value in manifest["round1"]["tuning"]["C1_kappa"]]
    b3_values = [float(value) for value in manifest["round1"]["tuning"]["B3_shrinkage"]]

    model_sets: dict[tuple[str, float | None], list[GaussianArm]] = {}
    for pol in range(2):
        base = estimate_gaussian_arms(
            bundle.z_pilot[pol],
            bundle.point_labels[pol],
            symbols,
            floor=floor,
            kappa=c1_values[0],
            b3_shrinkage=b3_values[0],
        )
        for key in (("B1", None), ("B2", None)):
            model_sets.setdefault(key, []).append(base[key[0]])
        for value in b3_values:
            covariance = estimate_covariance_arms(
                bundle.z_pilot[pol], bundle.point_labels[pol], symbols,
                floor=floor, kappa=c1_values[0], b3_shrinkage=value,
            )["B3"]
            model_sets.setdefault(("B3", value), []).append(
                GaussianArm(means=base["B1"].means, covariances=covariance)
            )
        for value in c1_values:
            covariance = estimate_covariance_arms(
                bundle.z_pilot[pol], bundle.point_labels[pol], symbols,
                floor=floor, kappa=value, b3_shrinkage=b3_values[0],
            )["C1"]
            model_sets.setdefault(("C1", value), []).append(
                GaussianArm(means=base["B1"].means, covariances=covariance)
            )

    rows = []
    for (arm, parameter), models in model_sets.items():
        metrics = _score_model(
            payload_observation,
            payload_labels,
            payload_bits,
            models,
            clip=clip,
            floor=floor,
        )
        rows.append({"arm": arm, "parameter": parameter, **metrics})
    rows.sort(key=lambda row: (row["arm"], -1.0 if row["parameter"] is None else float(row["parameter"])))
    window_id = int(config.seed - (3000 if round_name == "round1" else config.seed))
    if round_name == "round1":
        window_id = config.seed - 3000
    return {
        "round": round_name,
        "window_id": int(window_id),
        "window_name": config.window_id,
        "seed": int(config.seed),
        "split": split,
        "snr_db": float(snr_db),
        "config_hash": _config_hash(config),
        "realization_hash": bundle.realization_hash,
        "bundle_hash": bundle.bundle_hash,
        "pilot_symbols_per_polarization": int(bundle.pilot_indices.size),
        "payload_symbols_per_polarization": int(payload.size),
        "per_pol_point_counts": bundle.per_pol_point_counts.tolist(),
        "rows": rows,
    }


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _canonical_hash(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _round1_report(aggregate: dict, receipt: dict) -> str:
    lines = [
        "# Ch5 structured-covariance 有界 BER/GMI 开发",
        "",
        "> T067 / D048 / V022 | `PROVISIONAL` ceiling | Groundwork Step 4a dimension D",
        "",
        "## 事实与数字",
        "",
        f"- Round 1：`{aggregate['round1_windows']}/64` windows；tune `0..31`，evaluation `32..63`。",
        f"- 调参冻结：C1 `kappa={aggregate['tuning']['C1_kappa']}`；B3 `shrinkage={aggregate['tuning']['B3_shrinkage']}`。",
        f"- terminal：`{aggregate['terminal']}`；strongest structured comparator：`{aggregate['strongest_comparator']}`。",
        f"- Round 2 authorized：`{str(aggregate['round2_authorized']).lower()}`；provisional grade：`{receipt['provisional_grade']}`。",
        "",
        "### Evaluation arms（32 window clusters）",
        "",
        "| arm | mean GMI | mean BER | errors / bits | held-out NLL | max condition | floor rate | runtime (s) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in ("B1", "B2", "B3", "C1"):
        value = aggregate["arms"][arm]
        lines.append(
            f"| {arm} | {value['mean_gmi']:.10f} | {value['mean_ber']:.10e} | "
            f"{value['bit_errors']} / {value['payload_bits']} | {value['held_out_nll']:.10f} | "
            f"{value['condition_max']:.6g} | {value['floor_rate']:.6g} | {value['runtime_s']:.6f} |"
        )
    lines.extend(["", "### Paired differences（candidate − baseline）", ""])
    for name in ("B2_vs_B1", "B3_vs_B1", "C1_vs_B1", "C1_vs_B2", "C1_vs_B3"):
        value = aggregate["comparisons"][name]
        lines.append(
            f"- `{name}`：GMI Δ={value['gmi']['mean_diff']:.10f}, 95% CI "
            f"[{value['gmi']['ci'][0]:.10f}, {value['gmi']['ci'][1]:.10f}], wins={value['gmi']['wins']}/32；"
            f"BER Δ={value['ber']['mean_diff']:.10e}, 95% CI "
            f"[{value['ber']['ci'][0]:.10e}, {value['ber']['ci'][1]:.10e}], wins={value['ber']['wins']}/32。"
        )
    lines.extend(
        [
            "",
            "## 实现真相三联卡",
            "",
            "- `information_access`：bridge/estimator 只读本 window known pilots、接收 observation、冻结 constellation/arm/config；payload labels/bits 仅在离线 BER/GMI/NLL scorer 中消费。",
            "- `metric_signature`：每 evaluation window 含 2 polarizations × 192 payload symbols × 4 bits；BER 分子为 hard-LLR bit errors、分母为 1536；GMI 使用同一 payload bits/LLR；聚合单位与 bootstrap cluster 均为 window。",
            "- `state_lifecycle`：每 seed 独立 window；同 window 的 Ch4 preamble + observation 共用连续 scalar→Jones→AWGN realization；Ch4/Ch3 state 每 window 重置，不跨 window 或 polarization pooling。",
            "",
            "## 裁决",
            "",
            f"`{aggregate['terminal']}`。本结果等级上限为 `{receipt['provisional_grade']}`，不是 FINAL，也不是 confirmation。",
            "",
            f"唯一下一步：{receipt['unique_next_step']}",
            "",
            "## 禁止边界",
            "",
            "未运行 LDPC/FER grid、第二湍流级、新损伤、第三轮、扩展参数/SNR/seeds、fresh confirmation；未修改 common/、params.py、Skill/controller 或论文正文。",
            "",
        ]
    )
    return "\n".join(lines)


def run_round1(manifest: dict) -> tuple[dict, dict, dict]:
    configs = build_round1_configs(manifest)
    windows = []
    for window_id, config in enumerate(configs):
        split = "tune" if window_id < 32 else "evaluation"
        windows.append(
            evaluate_window(
                config,
                manifest,
                round_name="round1",
                split=split,
                snr_db=float(manifest["round1"]["snr_db"]),
            )
        )
        print(f"Round 1 {window_id + 1:02d}/64 seed={config.seed}")
    raw = {
        "schema_version": "t067.structured-covariance-development.raw.v1",
        "authority": manifest["authority"],
        "manifest_hash": _sha256(MANIFEST_PATH),
        "round1": windows,
        "round2": [],
    }
    aggregate = reduce_round1(windows, manifest)
    aggregate["manifest_hash"] = raw["manifest_hash"]
    aggregate["provisional_grade"] = (
        "PENDING_ROUND2"
        if aggregate["round2_authorized"]
        else "PROVISIONAL_C"
        if aggregate["terminal"] == "GMI_ONLY_SIGNAL"
        else "D"
    )
    next_steps = {
        "C1_SIGNAL": "Run only the preregistered frozen-winner Round 2 three-point BER/GMI curve.",
        "SIMPLE_MIGRATION_SIGNAL": "Run only the preregistered frozen-winner Round 2 three-point BER/GMI curve.",
        "GMI_ONLY_SIGNAL": "Stop SNR-curve development; consider one separately authorized coded gate or retain as supporting material.",
        "NO_METHOD_SIGNAL": "Close C5-1 and return to C5-0 Groundwork Step 2.",
    }
    receipt = {
        "schema_version": "t067.structured-covariance-development.receipt.v1",
        "authority": manifest["authority"],
        "manifest_hash": raw["manifest_hash"],
        "completed_round1_windows": len(windows),
        "completed_round2_windows": 0,
        "terminal": aggregate["terminal"],
        "winner": aggregate["winner"],
        "provisional_grade": aggregate["provisional_grade"],
        "round2_authorized": aggregate["round2_authorized"],
        "split_firewall": "PASS",
        "finite_metrics": True,
        **aggregate["hashes"],
        "unique_next_step": next_steps[aggregate["terminal"]],
        "forbidden_not_run": list(manifest["forbidden"]),
    }
    receipt["receipt_hash"] = _canonical_hash(receipt)
    return raw, aggregate, receipt


def write_round1_artifacts(raw: dict, aggregate: dict, receipt: dict) -> None:
    save_results(raw, str(RAW_PATH), "run_development:t067-round1-raw")
    save_results(aggregate, str(AGGREGATE_PATH), "run_development:t067-round1-aggregate")
    save_results(receipt, str(RECEIPT_PATH), "run_development:t067-round1-receipt")
    REPORT_PATH.write_text(_round1_report(aggregate, receipt), encoding="utf-8")


def raw_only_probe(manifest: dict) -> dict:
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    rebuilt = reduce_round1(raw["round1"], manifest)
    saved = json.loads(AGGREGATE_PATH.read_text(encoding="utf-8"))
    for key in ("terminal", "winner", "tuning", "arms", "comparisons", "hashes"):
        if rebuilt[key] != saved[key]:
            raise ValueError(f"raw-only reducer mismatch at {key}")
    print(
        f"RAW_ONLY_PASS terminal={rebuilt['terminal']} "
        f"windows={rebuilt['round1_windows']} sha256={_sha256(RAW_PATH)}"
    )
    return rebuilt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", choices=("round1",), default="round1")
    parser.add_argument("--reduce-only", action="store_true")
    args = parser.parse_args()
    manifest = load_development_manifest()
    if args.reduce_only:
        raw_only_probe(manifest)
        return
    raw, aggregate, receipt = run_round1(manifest)
    write_round1_artifacts(raw, aggregate, receipt)
    print(
        f"ROUND1_TERMINAL={aggregate['terminal']} winner={aggregate['winner']} "
        f"round2_authorized={aggregate['round2_authorized']}"
    )


__all__ = [
    "build_round1_configs",
    "frozen_ch4_arm",
    "load_development_manifest",
    "payload_indices",
    "evaluate_window",
    "raw_only_probe",
    "run_round1",
]


if __name__ == "__main__":
    main()
