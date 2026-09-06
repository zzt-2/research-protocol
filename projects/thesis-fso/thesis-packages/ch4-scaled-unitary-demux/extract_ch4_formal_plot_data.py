"""Materialize deterministic thesis-plot CSVs from frozen Ch4 evidence.

The script is intentionally read-only with respect to the scientific artifacts.
It verifies their frozen byte identities, pools integer error counts, applies the
frozen Jeffreys BER convention, and exports only matched formal-production data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
EVIDENCE_DIR = REPO / "projects/simulation/explore/ch4-scaled-unitary-pilot-ls"
RAW_PATH = EVIDENCE_DIR / "ch4_formal_raw.json"
AGGREGATE_PATH = EVIDENCE_DIR / "ch4_formal_aggregate.json"
RECEIPT_PATH = EVIDENCE_DIR / "ch4_formal_receipt.json"
DATA_DIR = HERE / "data"

FROZEN_SHA256 = {
    RAW_PATH: "642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b",
    AGGREGATE_PATH: "916c4ba5f75703a5a63bc40931e74d161ad3e61ac0b72baa918b77de95c55602",
    RECEIPT_PATH: "0fac1304f9aa8a4a4463c14ed5a43059a04b5c1de031b69c1d7fa9f03376e697",
}

METHOD_ORDER = ("B0", "B2_TUNED", "C4_FWD", "B3_PSC", "O1")
METHOD_NAMES = {
    "B0": "普通 LS",
    "B2_TUNED": "调参奇异值下限",
    "C4_FWD": "前向误差尺度",
    "B3_PSC": "导频重构尺度",
    "O1": "理想 CSI 参考",
}
ENGINEERING_BER = 3.8e-3
FIXED_SNR_DB = 25.0
EXPECTED_LATENTS = 128
EXPECTED_BITS_PER_LATENT = 32768

CSV_FIELDS = {
    "ch4-formal-ber-curves.csv": (
        "scene",
        "n_pilots",
        "snr_db",
        "method_code",
        "method_name",
        "method_parameter",
        "errors",
        "bits",
        "ber_jeffreys",
        "latent_clusters",
        "cell_kind",
    ),
    "ch4-formal-required-snr.csv": (
        "scene",
        "n_pilots",
        "threshold_ber",
        "variant_code",
        "variant_name",
        "baseline_code",
        "baseline_name",
        "comparison_status",
        "baseline_crossing_status",
        "variant_crossing_status",
        "baseline_required_snr_db",
        "variant_required_snr_db",
        "gain_db",
        "ci95_lower_db",
        "ci95_upper_db",
        "bootstrap_valid_replicates",
        "bootstrap_requested_replicates",
    ),
    "ch4-formal-pilot-sensitivity.csv": (
        "scene",
        "n_pilots",
        "method_code",
        "method_name",
        "method_parameter",
        "threshold_ber",
        "crossing_status",
        "required_snr_db",
        "fixed_snr_db",
        "fixed_snr_errors",
        "fixed_snr_bits",
        "fixed_snr_ber_jeffreys",
        "latent_clusters",
    ),
    "ch4-formal-mismatch.csv": (
        "scene",
        "n_pilots",
        "snr_db",
        "delta",
        "source_status",
        "method_code",
        "method_name",
        "method_parameter",
        "errors",
        "bits",
        "ber_jeffreys",
        "latent_clusters",
    ),
    "ch4-formal-mechanism.csv": (
        "scene",
        "n_pilots",
        "snr_db",
        "method_code",
        "method_name",
        "method_parameter",
        "latent_clusters",
        "channel_nmse_mean",
        "channel_nmse_status",
        "inherited_channel_nmse_mean",
        "inverse_residual_mean",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_frozen_artifacts() -> None:
    for path, expected in FROZEN_SHA256.items():
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"frozen artifact identity mismatch: {path.name}")


def load_evidence() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    verify_frozen_artifacts()
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    aggregate = json.loads(AGGREGATE_PATH.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "t087.ch4-formal-raw.v1":
        raise ValueError("unexpected formal raw schema")
    if aggregate.get("schema_version") != "t087.ch4-formal-aggregate.v1":
        raise ValueError("unexpected formal aggregate schema")
    if receipt.get("schema_version") != "t087.ch4-formal-receipt.v1":
        raise ValueError("unexpected formal receipt schema")
    if len(raw.get("latents", [])) != EXPECTED_LATENTS:
        raise ValueError("formal raw must contain exactly 128 latent clusters")
    bindings = receipt.get("artifact_hashes", {})
    if bindings.get("formal_raw_sha256") != FROZEN_SHA256[RAW_PATH]:
        raise ValueError("receipt does not bind the frozen raw")
    if bindings.get("formal_aggregate_sha256") != FROZEN_SHA256[AGGREGATE_PATH]:
        raise ValueError("receipt does not bind the frozen aggregate")
    return raw, aggregate, receipt


def render(value: Any) -> str | int:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("CSV output cannot contain non-finite values")
        return format(value, ".17g")
    return value


def write_csv(path: Path, rows: list[dict[str, Any]], fields: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: render(row.get(key)) for key in writer.fieldnames})


def iter_cells(raw: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for latent in raw["latents"]:
        for scene in latent["scenes"]:
            yield from scene["cells"]


def validate_row(cell: dict[str, Any], row: dict[str, Any]) -> None:
    metrics = row["metrics"]
    errors = int(metrics["bit_errors"])
    bits = int(metrics["payload_bits"])
    if row.get("validity") != "VALID" or errors < 0 or bits != EXPECTED_BITS_PER_LATENT:
        raise ValueError(f"invalid formal row in {cell['cell_id']}")
    if not math.isclose(float(metrics["ber"]), errors / bits, rel_tol=0.0, abs_tol=0.0):
        raise ValueError(f"BER numerator/denominator mismatch in {cell['cell_id']}")


def collect_groups(raw: dict[str, Any]) -> tuple[dict[tuple[Any, ...], list[dict[str, Any]]], dict[tuple[Any, ...], list[dict[str, Any]]]]:
    primary: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    mismatch: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for cell in iter_cells(raw):
        rows = cell.get("rows", [])
        if tuple(row.get("public_role") for row in rows) != METHOD_ORDER:
            raise ValueError(f"method coverage/order mismatch in {cell['cell_id']}")
        for row in rows:
            validate_row(cell, row)
            role = row["public_role"]
            if cell["kind"] == "primary":
                key = (cell["scene"], int(cell["n_pilots"]), float(cell["snr_db"]), role)
                primary[key].append(row)
            elif cell["kind"] == "mismatch":
                key = (
                    cell["scene"],
                    int(cell["n_pilots"]),
                    float(cell["snr_db"]),
                    float(cell["delta"]),
                    role,
                )
                mismatch[key].append(row)
            else:
                raise ValueError(f"unexpected stored cell kind: {cell['kind']}")
    for collection in (primary, mismatch):
        for key, rows in collection.items():
            if len(rows) != EXPECTED_LATENTS:
                raise ValueError(f"incomplete matched cluster group: {key}")
    return primary, mismatch


def common_parameter(rows: list[dict[str, Any]]) -> float | None:
    values = {row.get("parameter") for row in rows}
    if len(values) != 1:
        raise ValueError("method parameter is not constant within a matched cell")
    return values.pop()


def pooled_counts(rows: list[dict[str, Any]]) -> tuple[int, int, float]:
    errors = sum(int(row["metrics"]["bit_errors"]) for row in rows)
    bits = sum(int(row["metrics"]["payload_bits"]) for row in rows)
    return errors, bits, (errors + 0.5) / (bits + 1)


def crossing(curve: list[tuple[float, float]]) -> tuple[str, float | None]:
    curve = sorted(curve)
    if curve[0][1] <= ENGINEERING_BER:
        return "BELOW_RANGE", None
    downward = [
        index
        for index in range(1, len(curve))
        if curve[index - 1][1] > ENGINEERING_BER and curve[index][1] <= ENGINEERING_BER
    ]
    if not downward:
        return "UNREACHED", None
    first = downward[0]
    upward_after = any(
        curve[index - 1][1] <= ENGINEERING_BER and curve[index][1] > ENGINEERING_BER
        for index in range(first + 1, len(curve))
    )
    if len(downward) != 1 or upward_after:
        return "UNSTABLE", None
    x0, y0 = curve[first - 1]
    x1, y1 = curve[first]
    if y1 == ENGINEERING_BER:
        return "STABLE", x1
    log0, log1, target = math.log10(y0), math.log10(y1), math.log10(ENGINEERING_BER)
    snr = x0 + (target - log0) * (x1 - x0) / (log1 - log0)
    return "STABLE", snr


def curve_rows(primary: dict[tuple[Any, ...], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scene_order = {"weak": 0, "moderate": 1, "strong": 2}
    for key in sorted(primary, key=lambda x: (scene_order[x[0]], x[1], x[2], METHOD_ORDER.index(x[3]))):
        scene, n_pilots, snr_db, role = key
        group = primary[key]
        errors, bits, ber = pooled_counts(group)
        rows.append(
            {
                "scene": scene,
                "n_pilots": n_pilots,
                "snr_db": snr_db,
                "method_code": role,
                "method_name": METHOD_NAMES[role],
                "method_parameter": common_parameter(group),
                "errors": errors,
                "bits": bits,
                "ber_jeffreys": ber,
                "latent_clusters": len(group),
                "cell_kind": "primary",
            }
        )
    if len(rows) != 570:
        raise ValueError(f"expected 570 pooled curve rows, got {len(rows)}")
    return rows


def curve_lookup(rows: list[dict[str, Any]]) -> dict[tuple[str, int, str], list[tuple[float, float]]]:
    lookup: dict[tuple[str, int, str], list[tuple[float, float]]] = defaultdict(list)
    for row in rows:
        lookup[(row["scene"], row["n_pilots"], row["method_code"])].append(
            (float(row["snr_db"]), float(row["ber_jeffreys"]))
        )
    return lookup


def required_snr_rows(aggregate: dict[str, Any], curves: dict[tuple[str, int, str], list[tuple[float, float]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in ("C4_FWD", "B3_PSC"):
        for n_pilots in (2, 4):
            item = aggregate["headline_curve_comparisons"][variant][str(n_pilots)]
            b_status, b_snr = crossing(curves[("moderate", n_pilots, "B2_TUNED")])
            v_status, v_snr = crossing(curves[("moderate", n_pilots, variant)])
            if b_status != item["baseline_crossing"]["status"] or v_status != item["variant_crossing"]["status"]:
                raise ValueError("crossing status differs from the frozen aggregate")
            if not math.isclose(b_snr or 0.0, item["baseline_crossing"]["snr_required_db"], rel_tol=0.0, abs_tol=1e-12):
                raise ValueError("baseline crossing differs from the frozen aggregate")
            if not math.isclose(v_snr or 0.0, item["variant_crossing"]["snr_required_db"], rel_tol=0.0, abs_tol=1e-12):
                raise ValueError("variant crossing differs from the frozen aggregate")
            if not math.isclose((b_snr or 0.0) - (v_snr or 0.0), item["point_gain_db"], rel_tol=0.0, abs_tol=1e-12):
                raise ValueError("required-SNR gain differs from the frozen aggregate")
            rows.append(
                {
                    "scene": "moderate",
                    "n_pilots": n_pilots,
                    "threshold_ber": ENGINEERING_BER,
                    "variant_code": variant,
                    "variant_name": METHOD_NAMES[variant],
                    "baseline_code": "B2_TUNED",
                    "baseline_name": METHOD_NAMES["B2_TUNED"],
                    "comparison_status": item["status"],
                    "baseline_crossing_status": b_status,
                    "variant_crossing_status": v_status,
                    "baseline_required_snr_db": item["baseline_crossing"]["snr_required_db"],
                    "variant_required_snr_db": item["variant_crossing"]["snr_required_db"],
                    "gain_db": item["point_gain_db"],
                    "ci95_lower_db": item["ci_lower_db"],
                    "ci95_upper_db": item["ci_upper_db"],
                    "bootstrap_valid_replicates": item["valid_replicates"],
                    "bootstrap_requested_replicates": 5000,
                }
            )
    return rows


def pilot_rows(
    primary: dict[tuple[Any, ...], list[dict[str, Any]]],
    curves: dict[tuple[str, int, str], list[tuple[float, float]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n_pilots in (2, 4, 8, 16):
        for role in METHOD_ORDER:
            group = primary[("moderate", n_pilots, FIXED_SNR_DB, role)]
            errors, bits, ber = pooled_counts(group)
            status, required = crossing(curves[("moderate", n_pilots, role)])
            rows.append(
                {
                    "scene": "moderate",
                    "n_pilots": n_pilots,
                    "method_code": role,
                    "method_name": METHOD_NAMES[role],
                    "method_parameter": common_parameter(group),
                    "threshold_ber": ENGINEERING_BER,
                    "crossing_status": status,
                    "required_snr_db": required,
                    "fixed_snr_db": FIXED_SNR_DB,
                    "fixed_snr_errors": errors,
                    "fixed_snr_bits": bits,
                    "fixed_snr_ber_jeffreys": ber,
                    "latent_clusters": len(group),
                }
            )
    return rows


def mismatch_rows(
    primary: dict[tuple[Any, ...], list[dict[str, Any]]],
    mismatch: dict[tuple[Any, ...], list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for delta in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4):
        for role in METHOD_ORDER:
            if delta == 0.0:
                group = primary[("moderate", 2, FIXED_SNR_DB, role)]
                source_status = "exact_reference"
            else:
                group = mismatch[("moderate", 2, FIXED_SNR_DB, delta, role)]
                source_status = "stored_mismatch_cell"
            errors, bits, ber = pooled_counts(group)
            rows.append(
                {
                    "scene": "moderate",
                    "n_pilots": 2,
                    "snr_db": FIXED_SNR_DB,
                    "delta": delta,
                    "source_status": source_status,
                    "method_code": role,
                    "method_name": METHOD_NAMES[role],
                    "method_parameter": common_parameter(group),
                    "errors": errors,
                    "bits": bits,
                    "ber_jeffreys": ber,
                    "latent_clusters": len(group),
                }
            )
    return rows


def mechanism_rows(primary: dict[tuple[Any, ...], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n_pilots in (2, 4):
        for snr_db in range(5, 42, 2):
            for role in METHOD_ORDER:
                group = primary[("moderate", n_pilots, float(snr_db), role)]
                semantics = {row["metrics"]["channel_nmse_semantics"] for row in group}
                if len(semantics) != 1:
                    raise ValueError("channel-NMSE semantics vary within a matched cell")
                semantic = semantics.pop()
                nmse_mean = sum(float(row["metrics"]["channel_nmse"]) for row in group) / len(group)
                inverse_mean = sum(float(row["metrics"]["inverse_residual"]) for row in group) / len(group)
                inherited = nmse_mean if semantic == "pre_calibration_inherited" else None
                direct = nmse_mean if semantic == "direct_estimate" else None
                rows.append(
                    {
                        "scene": "moderate",
                        "n_pilots": n_pilots,
                        "snr_db": float(snr_db),
                        "method_code": role,
                        "method_name": METHOD_NAMES[role],
                        "method_parameter": common_parameter(group),
                        "latent_clusters": len(group),
                        "channel_nmse_mean": direct,
                        "channel_nmse_status": semantic,
                        "inherited_channel_nmse_mean": inherited,
                        "inverse_residual_mean": inverse_mean,
                    }
                )
    return rows


def build_outputs() -> dict[str, list[dict[str, Any]]]:
    raw, aggregate, _receipt = load_evidence()
    primary, mismatch = collect_groups(raw)
    curves_rows = curve_rows(primary)
    curves = curve_lookup(curves_rows)
    return {
        "ch4-formal-ber-curves.csv": curves_rows,
        "ch4-formal-required-snr.csv": required_snr_rows(aggregate, curves),
        "ch4-formal-pilot-sensitivity.csv": pilot_rows(primary, curves),
        "ch4-formal-mismatch.csv": mismatch_rows(primary, mismatch),
        "ch4-formal-mechanism.csv": mechanism_rows(primary),
    }


def check_existing(outputs: dict[str, list[dict[str, Any]]]) -> None:
    for name, rows in outputs.items():
        path = DATA_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"missing materialized CSV: {path}")
        with path.open("r", encoding="utf-8", newline="") as handle:
            actual = list(csv.DictReader(handle))
        expected = [
            {field: str(render(row.get(field))) for field in CSV_FIELDS[name]}
            for row in rows
        ]
        if actual != expected:
            raise ValueError(f"materialized CSV differs from frozen evidence: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="verify existing CSVs without writing")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check_only:
        check_existing(outputs)
    else:
        for name, rows in outputs.items():
            write_csv(DATA_DIR / name, rows, CSV_FIELDS[name])
    print("PASS: frozen Ch4 evidence materialized into deterministic matched CSVs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
