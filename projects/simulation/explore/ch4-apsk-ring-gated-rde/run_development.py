"""T059 preregistered bounded development driver for Ch4 gated RDE.

This file is intentionally independent of the correctness receipt. It imports
the verified seam, freezes tuning on 54101--54103, evaluates only 54201--54206,
and never generates a seed at or above the confirmation firewall (54301).
"""

from __future__ import annotations

import hashlib
import math
import sys
import time
from pathlib import Path

import numpy as np
import yaml


HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]
REPO = SIM.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(SIM) not in sys.path:
    sys.path.insert(0, str(SIM))

import core
from common._experiment import save_results


MANIFEST = HERE / "development_manifest.yaml"
RAW_PATH = HERE / "development_raw.json"
AGG_PATH = HERE / "development_aggregate.json"
RECEIPT_PATH = HERE / "development_receipt.json"
REPORT_PATH = HERE / "development_report.md"


def load_manifest(path: Path = MANIFEST) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_manifest(m: dict) -> None:
    expected_r1 = [("D1", 14, 2), ("D2", 18, 2), ("D3", 14, 8)]
    expected_r2 = [("D4", 14, 4), ("D5", 18, 4), ("D6", 18, 8)]
    got = lambda key: [(c["id"], c["snr_db"], c["pilots"]) for c in m[key]]
    if got("round1_cells") != expected_r1 or got("round2_cells") != expected_r2:
        raise ValueError("development cell grid differs from T059")
    if m["payload_symbols"] != 8192 or m["block_symbols"] != 256:
        raise ValueError("payload/block size differs from T059")
    if m["tune_seeds"] != [54101, 54102, 54103]:
        raise ValueError("tune seeds differ from T059")
    if m["eval_seeds"] != [54201, 54202, 54203, 54204, 54205, 54206]:
        raise ValueError("development-eval seeds differ from T059")
    if max(m["eval_seeds"] + m["tune_seeds"]) >= min(m["confirmation_seeds_reserved"]):
        raise ValueError("confirmation seed firewall violated")


def jeffreys_ber(errors: int, total: int) -> float:
    return (float(errors) + 0.5) / (float(total) + 1.0)


def binary_auc(scores: np.ndarray, labels: np.ndarray) -> float | None:
    s = np.asarray(scores, float).reshape(-1)
    y = np.asarray(labels, bool).reshape(-1)
    n_pos, n_neg = int(y.sum()), int((~y).sum())
    if n_pos == 0 or n_neg == 0:
        return None
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), float)
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[order[j]] == s[order[i]]:
            j += 1
        ranks[order[i:j]] = 0.5 * (i + 1 + j)
        i = j
    return float((ranks[y].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def count_matched_masks(source: np.ndarray, *, seed: int, block_size: int = 256) -> np.ndarray:
    source = np.asarray(source, bool)
    rng = np.random.default_rng(int(seed))
    out = np.zeros_like(source)
    for pol in range(source.shape[0]):
        for start in range(0, source.shape[1], block_size):
            stop = min(start + block_size, source.shape[1])
            count = int(source[pol, start:stop].sum())
            if count:
                chosen = rng.choice(stop - start, size=count, replace=False)
                out[pol, start + chosen] = True
    return out


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _labels_to_bits(labels: np.ndarray) -> np.ndarray:
    labels = np.asarray(labels, np.uint8)
    return ((labels[..., None] >> np.arange(3, -1, -1)) & 1).astype(np.uint8)


def _measure(result: dict, truth_labels: np.ndarray, *, thresholds: tuple[float, float] | None = None) -> dict:
    pred = core.nearest_apsk(result["z"])["labels"]
    pred_bits = _labels_to_bits(pred)
    truth_bits = _labels_to_bits(truth_labels)
    mismatch = pred_bits != truth_bits
    mid = mismatch.shape[1] // 2
    errors = int(mismatch.sum())
    first = int(mismatch[:, :mid].sum())
    second = int(mismatch[:, mid:].sum())
    total = int(mismatch.size)
    wrong_symbol = pred != truth_labels
    wrong_ring = (pred >= 8) != (truth_labels >= 8)
    accepted = np.asarray(result["gates"], bool)
    accepted_count = int(accepted.sum())
    contamination = int(np.count_nonzero(accepted & wrong_symbol))
    wrong_ring_accepted = int(np.count_nonzero(accepted & wrong_ring))
    ring_auc = binary_auc(result["native_ring_score"], wrong_ring)
    decision_auc = binary_auc(result["decision_score"], wrong_symbol)
    if thresholds is None:
        combined_score = np.maximum(result["native_ring_score"], result["decision_score"])
    else:
        tr, td = thresholds
        combined_score = np.maximum(result["ring_score"] / tr, result["decision_score"] / td)
    return {
        "errors": errors,
        "total_bits": total,
        "ber": errors / total,
        "jeffreys_ber": jeffreys_ber(errors, total),
        "first_half_errors": first,
        "first_half_ber": first / (total // 2),
        "second_half_errors": second,
        "second_half_ber": second / (total // 2),
        "accepted_count": accepted_count,
        "accepted_fraction": accepted_count / accepted.size,
        "wrong_symbol_count": int(wrong_symbol.sum()),
        "wrong_ring_count": int(wrong_ring.sum()),
        "wrong_symbol_update_count": contamination,
        "wrong_symbol_update_contamination": contamination / max(accepted_count, 1),
        "wrong_ring_update_count": wrong_ring_accepted,
        "wrong_ring_update_contamination": wrong_ring_accepted / max(accepted_count, 1),
        "ring_auc": ring_auc,
        "decision_auc": decision_auc,
        "combined_auc": binary_auc(combined_score, wrong_symbol),
        "w_norm": float(np.linalg.norm(result["W"])),
        "finite": bool(np.all(np.isfinite(result["z"])) and np.all(np.isfinite(result["W"]))),
    }


def _ls_result(real: dict) -> dict:
    z = real["W0"] @ real["payload_rx"]
    n = z.shape[1]
    return {
        "z": z, "W": real["W0"], "gates": np.zeros((2, n), bool),
        "ring_score": np.zeros((2, n)), "native_ring_score": np.zeros((2, n)),
        "decision_score": np.zeros((2, n)),
    }


def _configs(m: dict, arm: str) -> list[dict]:
    if arm in ("plain", "oracle"):
        return [{"mu": float(mu)} for mu in m["tuning"]["plain_oracle_mu"]]
    mus = m["tuning"]["gated_mu"]
    ts = m["tuning"]["thresholds"]
    if arm == "cheap":
        return [{"mu": float(mu), "tau_r": float(t)} for mu in mus for t in ts]
    return [{"mu": float(mu), "tau_r": float(t), "tau_d": float(t)} for mu in mus for t in ts]


def _run_arm(arm: str, real: dict, cfg: dict) -> dict:
    y, w0 = real["payload_rx"], real["W0"]
    if arm == "plain":
        return core.run_plain_rde(y, w0, mu=cfg["mu"])
    if arm == "cheap":
        return core.run_cheap_rde(y, w0, mu=cfg["mu"], ring_threshold=cfg["tau_r"])
    if arm == "candidate":
        return core.run_candidate_rde(y, w0, mu=cfg["mu"], ring_threshold=cfg["tau_r"], decision_threshold=cfg["tau_d"])
    if arm == "oracle":
        return core.run_oracle_rde(y, w0, real["symbols"], mu=cfg["mu"])
    raise KeyError(arm)


def _real(cell: dict, seed: int, payload: int) -> dict:
    if seed >= 54301:
        raise ValueError("confirmation seed firewall violated")
    return core.generate_shared_correctness_realization(
        seed=seed, n_payload=payload, n_pilots=cell["pilots"], snr_db=cell["snr_db"]
    )


def tune(m: dict) -> tuple[dict, dict]:
    cache = {(c["id"], s): _real(c, s, m["payload_symbols"]) for c in m["round1_cells"] for s in m["tune_seeds"]}
    selected, ledger = {}, {}
    for arm in ("plain", "cheap", "candidate", "oracle"):
        scored = []
        for cfg in _configs(m, arm):
            logs, accepts = [], []
            for cell in m["round1_cells"]:
                for seed in m["tune_seeds"]:
                    real = cache[(cell["id"], seed)]
                    result = _run_arm(arm, real, cfg)
                    thresholds = (cfg.get("tau_r", 1.0), cfg.get("tau_d", 1.0)) if arm == "candidate" else None
                    met = _measure(result, real["labels"], thresholds=thresholds)
                    logs.append(math.log10(met["jeffreys_ber"]))
                    accepts.append(met["accepted_fraction"])
            obj = float(np.mean(logs))
            scored.append({"config": cfg, "objective_mean_log10_jeffreys_ber": obj,
                           "geometric_jeffreys_ber": 10.0**obj, "accepted_fraction": float(np.mean(accepts))})
        best_geo = min(x["geometric_jeffreys_ber"] for x in scored)
        tied = [x for x in scored if x["geometric_jeffreys_ber"] <= 1.01 * best_geo]
        best = sorted(tied, key=lambda x: (-x["accepted_fraction"], x["config"]["mu"]))[0]
        selected[arm] = best["config"]
        ledger[arm] = {"selected": best, "all_configs": scored}
    return selected, ledger


def _count_matched(real: dict, source_result: dict, *, mu: float, seed: int) -> dict:
    masks = count_matched_masks(source_result["gates"], seed=seed)
    return core._run_rde(real["payload_rx"], real["W0"], mu=mu,
                         gate_fn=lambda scores, k: masks[:, k])


def evaluate_cells(m: dict, cells: list[dict], selected: dict, *, round_no: int) -> list[dict]:
    rows = []
    for cell in cells:
        for seed in m["eval_seeds"]:
            real = _real(cell, seed, m["payload_symbols"])
            base = {"round": round_no, "cell": cell["id"], "snr_db": cell["snr_db"], "pilots": cell["pilots"],
                    "seed": seed, "realization_hash": real["realization_hash"]}
            ls = _ls_result(real)
            results = {"ls_only": ls}
            for arm in ("plain", "cheap", "candidate", "oracle"):
                results[arm] = _run_arm(arm, real, selected[arm])
            for arm in ("cheap", "candidate"):
                results[f"count_matched_{arm}"] = _count_matched(
                    real, results[arm], mu=selected[arm]["mu"], seed=seed + (100000 if arm == "cheap" else 200000)
                )
            for arm, result in results.items():
                cfg = selected.get(arm, {})
                thresholds = (cfg.get("tau_r", 1.0), cfg.get("tau_d", 1.0)) if arm == "candidate" else None
                rows.append({**base, "arm": arm, "config": cfg, **_measure(result, real["labels"], thresholds=thresholds),
                             "source_gate_count": int(results[arm.replace("count_matched_", "")]["gates"].sum()) if arm.startswith("count_matched_") else None})
    return rows


def _bootstrap(values: list[float], seed: int, n: int) -> dict:
    arr = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boots = np.mean(arr[rng.integers(0, len(arr), size=(n, len(arr)))], axis=1)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"mean": float(arr.mean()), "lo": float(lo), "hi": float(hi), "n": len(arr)}


def aggregate(m: dict, rows: list[dict]) -> dict:
    cells = {}
    for cell_id in sorted({r["cell"] for r in rows}):
        cr = [r for r in rows if r["cell"] == cell_id]
        by_arm = {a: [r for r in cr if r["arm"] == a] for a in sorted({r["arm"] for r in cr})}
        sums = {a: {"errors": sum(x["errors"] for x in xs), "bits": sum(x["total_bits"] for x in xs)} for a, xs in by_arm.items()}
        bers = {a: v["errors"] / v["bits"] for a, v in sums.items()}
        bstar_arm = "ls_only" if bers["ls_only"] <= bers["plain"] else "plain"
        bstar = bers[bstar_arm]
        oracle_headroom = (bstar - bers["oracle"]) / max(bstar, 1e-300)
        entry = {"bstar_arm": bstar_arm, "bstar_ber": bstar, "oracle_headroom": oracle_headroom,
                 "underpowered": sums[bstar_arm]["errors"] < m["underpowered_error_count"], "arms": {}}
        for arm, xs in by_arm.items():
            gain = (bstar - bers[arm]) / max(bstar, 1e-300)
            per_seed = []
            bmap = {x["seed"]: x for x in by_arm[bstar_arm]}
            for x in xs:
                bb = bmap[x["seed"]]["ber"]
                per_seed.append((bb - x["ber"]) / max(bb, 0.5 / x["total_bits"]))
            ci = _bootstrap(per_seed, m["bootstrap_seed"] + sum(ord(c) for c in cell_id + arm), m["bootstrap_replicates"])
            entry["arms"][arm] = {
                "ber": bers[arm], "errors": sums[arm]["errors"], "gain_vs_bstar": gain,
                "wins": int(sum(v > 0 for v in per_seed)), "paired_gain_bootstrap95": ci,
                "accepted_fraction": float(np.mean([x["accepted_fraction"] for x in xs])),
                "contamination": float(np.mean([x["wrong_symbol_update_contamination"] for x in xs])),
                "ring_auc": float(np.mean([x["ring_auc"] for x in xs if x["ring_auc"] is not None])) if any(x["ring_auc"] is not None for x in xs) else None,
                "decision_auc": float(np.mean([x["decision_auc"] for x in xs if x["decision_auc"] is not None])) if any(x["decision_auc"] is not None for x in xs) else None,
                "combined_auc": float(np.mean([x["combined_auc"] for x in xs if x["combined_auc"] is not None])) if any(x["combined_auc"] is not None for x in xs) else None,
                "gap_recovery": (bstar - bers[arm]) / max(bstar - bers["oracle"], 1e-300) if bstar > bers["oracle"] else 0.0,
            }
        entry["combined_auc"] = entry["arms"]["candidate"]["combined_auc"] or 0.0
        cells[cell_id] = entry
    return {"cells": cells}


def round1_decision(agg: dict) -> dict:
    cells = agg["cells"]
    eligible = {"candidate": False, "cheap": False}
    for arm in eligible:
        auc_key = "combined_auc" if arm == "candidate" else "ring_auc"
        eligible[arm] = any(
            (c["arms"][arm]["gain_vs_bstar"] >= 0.10 and c["arms"][arm]["wins"] >= 5)
            or (c["arms"][arm]["gap_recovery"] >= 0.20
                and (c["arms"][arm].get(auc_key) or 0.0) >= 0.60)
            for c in cells.values()
        )
    winner = "candidate" if eligible["candidate"] else ("cheap" if eligible["cheap"] else "none")
    if eligible["cheap"] and eligible["candidate"]:
        increments = []
        for c in cells.values():
            cheap = c["arms"]["cheap"]["ber"]
            cand = c["arms"]["candidate"]["ber"]
            increments.append((cheap - cand) / max(cheap, 1e-300))
        if max(increments) < 0.05:
            winner = "cheap"
    stop_reasons = []
    if cells and all(c.get("oracle_headroom", 0.0) < 0.10 for c in cells.values()): stop_reasons.append("NO_ORACLE_HEADROOM")
    if cells and all(c.get("combined_auc", 0.0) <= 0.55 for c in cells.values()): stop_reasons.append("NO_SCORE_DISCRIMINATION")
    has_gap_or_selection = False
    apparent = []
    for c in cells.values():
        for arm in ("cheap", "candidate"):
            method = c["arms"][arm]
            cm = c["arms"].get(f"count_matched_{arm}")
            better_than_cm = cm is None or method.get("ber", math.inf) < cm.get("ber", math.inf)
            has_gap_or_selection |= method["gap_recovery"] >= 0.20 or better_than_cm
            if method["gain_vs_bstar"] > 0 and cm is not None:
                apparent.append(better_than_cm)
    if not has_gap_or_selection:
        stop_reasons.append("NO_GAP_RECOVERY_OR_SELECTION_QUALITY")
    if apparent and not any(apparent):
        stop_reasons.append("ALL_GAIN_COUNT_MATCHED_ABSORBED")
    if winner == "none": stop_reasons.append("NO_PREREGISTERED_GATE_SIGNAL")
    hard_stop = any(reason in stop_reasons for reason in (
        "NO_ORACLE_HEADROOM", "NO_SCORE_DISCRIMINATION",
        "NO_GAP_RECOVERY_OR_SELECTION_QUALITY", "ALL_GAIN_COUNT_MATCHED_ABSORBED",
    ))
    if hard_stop:
        winner = "none"
    return {"enter_round2": winner != "none", "winner": winner, "eligible": eligible, "stop_reasons": stop_reasons}


def provisional_grade(m: dict, agg: dict, winner: str) -> str:
    if winner == "none":
        return "D/STOP_NO_METHOD_SIGNAL"
    cells = agg["cells"]
    powered = [c for c in cells.values() if not c["underpowered"]]
    improve20 = [c for c in powered if c["arms"][winner]["gain_vs_bstar"] >= 0.20]
    improve10 = [c for c in powered if c["arms"][winner]["gain_vs_bstar"] >= 0.10]
    ci_pos = [c for c in powered if c["arms"][winner]["paired_gain_bootstrap95"]["lo"] > 0]
    harmed = [c for c in powered if c["arms"][winner]["gain_vs_bstar"] < -0.10]
    count_wins = [c for c in powered if c["arms"][winner]["ber"] <= 0.95 * c["arms"][f"count_matched_{winner}"]["ber"]]
    if len(improve20) >= 3 and len(count_wins) >= 2 and not harmed and len(ci_pos) >= 1:
        auc_metric = "ring_auc" if winner == "cheap" else "combined_auc"
        auc_ok = sum((c["arms"][winner][auc_metric] or 0) >= 0.65 for c in powered) >= 1
        contam_ok = any(c["arms"][winner]["contamination"] <= 0.8 * c["arms"]["plain"]["contamination"] for c in powered)
        if auc_ok and contam_ok:
            return "A"
    if len(improve10) >= 2 and ci_pos and not harmed:
        return "B"
    if any(c["arms"][winner]["gain_vs_bstar"] >= 0.05 for c in powered):
        return "C"
    return "D/STOP_NO_METHOD_SIGNAL"


def _report(m: dict, agg: dict, decision: dict, grade: str, elapsed: float) -> str:
    lines = ["# Ch4 gated-RDE bounded development", "", f"- Round 2: {'RUN' if decision['enter_round2'] else 'SKIPPED'}",
             f"- winner: `{decision['winner']}`", f"- provisional grade: `{grade}`", f"- runtime: `{elapsed:.2f} s`", "",
             f"- Round-1 stop reasons: `{', '.join(decision['stop_reasons']) or 'none'}`", "",
             "| cell | B0* | candidate gain | cheap gain | oracle headroom | ring/decision/combined AUROC | candidate vs count-match | cheap vs count-match | underpowered |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for cid, c in agg["cells"].items():
        cand, cheap = c["arms"]["candidate"], c["arms"]["cheap"]
        cm_c, cm_h = c["arms"]["count_matched_candidate"], c["arms"]["count_matched_cheap"]
        cand_vs_cm = (cm_c["ber"] - cand["ber"]) / max(cm_c["ber"], 1e-300)
        cheap_vs_cm = (cm_h["ber"] - cheap["ber"]) / max(cm_h["ber"], 1e-300)
        aucs = "/".join("N/A" if v is None else f"{v:.3f}" for v in (cand["ring_auc"], cand["decision_auc"], cand["combined_auc"]))
        lines.append(f"| {cid} ({c['bstar_arm']}) | {c['bstar_ber']:.6g} | {cand['gain_vs_bstar']:.3%} | {cheap['gain_vs_bstar']:.3%} | {c['oracle_headroom']:.3%} | {aucs} | {cand_vs_cm:.3%} | {cheap_vs_cm:.3%} | {c['underpowered']} |")
    apparent = [(c, a) for c, entry in agg["cells"].items() for a in ("candidate", "cheap") if entry["arms"][a]["gain_vs_bstar"] > 0]
    absorption = "No apparent gain over B0* existed, so count-matched absorption is not the stopping mechanism." if not apparent else "See per-cell count-match columns; positive values mean selection beat matched random updates."
    lines += ["", f"- Count-matched finding: {absorption}",
              "- Unique next action: stop C4-2 gated-RDE development and return to the master for the preregistered C4-1/C4-0 rotation; do not tune a third gate variant.", "",
              "Development-only evidence. No confirmation seeds were generated and no final method signal is claimed."]
    return "\n".join(lines) + "\n"


def main() -> int:
    started = time.perf_counter()
    m = load_manifest(); validate_manifest(m)
    selected, tuning = tune(m)
    rows = evaluate_cells(m, m["round1_cells"], selected, round_no=1)
    agg = aggregate(m, rows)
    decision = round1_decision(agg)
    if decision["enter_round2"]:
        rows += evaluate_cells(m, m["round2_cells"], selected, round_no=2)
        agg = aggregate(m, rows)
    grade = provisional_grade(m, agg, decision["winner"])
    elapsed = time.perf_counter() - started
    raw = {"schema_version": "ch4.gated-rde.raw.v1", "manifest_sha256": _sha(MANIFEST), "selected": selected,
           "tuning": tuning, "rows": rows}
    save_results(raw, str(RAW_PATH), "t059_ch4_gated_rde_development")
    aggregate_out = {"schema_version": "ch4.gated-rde.aggregate.v1", **agg, "round1_decision": decision,
                     "winner": decision["winner"], "provisional_grade": grade, "elapsed_s": elapsed}
    save_results(aggregate_out, str(AGG_PATH), "t059_ch4_gated_rde_development")
    receipt = {"schema_version": "ch4.gated-rde.development-receipt.v1", "verdict_ceiling": "PROVISIONAL",
               "manifest_sha256": _sha(MANIFEST), "core_sha256": _sha(HERE / "core.py"), "driver_sha256": _sha(Path(__file__)),
               "test_sha256": _sha(SIM / "tests" / "test_ch4_apsk_ring_gated_rde_development.py"),
               "round2_run": decision["enter_round2"], "winner": decision["winner"], "provisional_grade": grade,
               "confirmation_seed_floor": 54301, "max_generated_seed": max(m["eval_seeds"]), "elapsed_s": elapsed,
               "raw_path": str(RAW_PATH.relative_to(REPO)), "aggregate_path": str(AGG_PATH.relative_to(REPO))}
    save_results(receipt, str(RECEIPT_PATH), "t059_ch4_gated_rde_development")
    REPORT_PATH.write_text(_report(m, agg, decision, grade, elapsed), encoding="utf-8")
    print(f"ROUND2={'RUN' if decision['enter_round2'] else 'SKIPPED'} winner={decision['winner']} grade={grade} elapsed_s={elapsed:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
