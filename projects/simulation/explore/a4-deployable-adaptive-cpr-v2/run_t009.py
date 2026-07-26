"""T009 frozen A4-v2 identity smoke and paired mixed-trace experiment."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SIM_ROOT = HERE.parents[1]
ROOT = SIM_ROOT.parents[1]
sys.path[:0] = [str(HERE), str(SIM_ROOT), str(SIM_ROOT / "simulator")]

from a4_v2 import (  # noqa: E402
    Dpll16Apsk,
    FrozenSelectors,
    hard_decision_m16apsk,
    m16apsk_demod,
    m16apsk_mod,
    required_snr_db,
    resolve_ambiguity_from_pilots,
)
from common import da_ml_recovery, generate_shared_realization_apsk, nda_ml_recovery  # noqa: E402
from common._experiment import save_results  # noqa: E402
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402


VAL_SEEDS = list(range(91001, 91011))
TEST_SEEDS = list(range(92001, 92011))
TURBS = ("weak", "moderate", "strong")
SNRS = (16.0, 24.0, 36.0)
CONDITION_ORDER = (
    ("weak", 16.0), ("moderate", 24.0), ("strong", 36.0),
    ("strong", 16.0), ("weak", 36.0), ("moderate", 16.0),
    ("moderate", 36.0), ("strong", 24.0), ("weak", 24.0),
)
DWELL_BLOCKS = 6
PILOT_IDX = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
DATA_SYM = np.ones(P.N_DFT, dtype=bool)
DATA_SYM[PILOT_IDX] = False
DATA_BIT_MASK = np.repeat(DATA_SYM, P.BITS_PER_SYM)
N_DATA_BITS = int(DATA_BIT_MASK.sum())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _agc(rx):
    return rx / max(float(np.sqrt(np.mean(np.abs(rx) ** 2))), 1e-12)


def identity_smoke():
    n = P.N_SYM_PER_POINT
    rng = np.random.default_rng(P.SEED_AWGN + 7)
    bits = rng.integers(0, 2, n * P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, _ = S.awgn_wiener_channel(tx, 18.0, P.SEED_AWGN)

    def evaluate(reset):
        errors = 0
        loop = None
        for block in range(n // P.N_DFT):
            sl = slice(block * P.N_DFT, (block + 1) * P.N_DFT)
            if loop is None or reset:
                loop = Dpll16Apsk(omega_n=50e6, symbol_period=P.T_S)
            corrected = loop.process(_agc(rx[sl]))
            corrected, _ = resolve_ambiguity_from_pilots(
                corrected, PILOT_IDX, tx[sl][PILOT_IDX], m0=P.M0
            )
            decoded = m16apsk_demod(corrected)
            errors += int(np.sum(decoded[DATA_BIT_MASK] != bits[sl.start * 4 : sl.stop * 4][DATA_BIT_MASK]))
        return errors / ((n // P.N_DFT) * N_DATA_BITS)

    continuous = evaluate(False)
    reset = evaluate(True)
    return {
        "continuous_ber": continuous,
        "reset_ber": reset,
        "reset_ratio": reset / continuous,
        "pass": 0.003 <= continuous <= 0.006 and reset >= 1.5 * continuous,
        "historical_anchor": "S011: about 4.1e-3 continuous vs 7.5e-3 reset",
    }


def _block_arms(rx, bits, tx, dpll):
    normalized = _agc(rx)
    pilot_symbols = tx[PILOT_IDX]

    da, _, _ = da_ml_recovery(normalized, PILOT_IDX, pilot_symbols, mod="m16apsk")
    da, _ = resolve_ambiguity_from_pilots(da, PILOT_IDX, pilot_symbols, m0=P.M0)

    nda, _, _, _ = nda_ml_recovery(
        normalized, P.M0, mod="m16apsk", assume_df_zero=True
    )
    nda, _ = resolve_ambiguity_from_pilots(nda, PILOT_IDX, pilot_symbols, m0=P.M0)

    dpll_out = dpll.process(normalized)
    dpll_out, _ = resolve_ambiguity_from_pilots(
        dpll_out, PILOT_IDX, pilot_symbols, m0=P.M0
    )
    decoded = {
        "DA": m16apsk_demod(da),
        "NDA": m16apsk_demod(nda),
        "DPLL": m16apsk_demod(dpll_out),
    }
    target = bits[DATA_BIT_MASK]
    errors = {arm: int(np.sum(value[DATA_BIT_MASK] != target)) for arm, value in decoded.items()}
    power = float(np.mean(np.abs(rx) ** 2))
    decided = hard_decision_m16apsk(normalized)
    innovation = float(np.mean(np.abs(normalized - decided) ** 2))
    return errors, {"power": power, "innovation": innovation}


def generate_pool(seeds, pool):
    rows = []
    for seed in seeds:
        dpll = Dpll16Apsk(omega_n=50e6, symbol_period=P.T_S)
        phase_tail = 0.0
        block_id = 0
        for turb, snr_db in CONDITION_ORDER:
            for dwell in range(DWELL_BLOCKS):
                local_seed = seed * 1000 + block_id
                shared = generate_shared_realization_apsk(
                    P.N_DFT, 10 ** (snr_db / 10), turb, 0.0,
                    mod="m16apsk", seed=local_seed, lw=P.LASER_LW,
                )
                shift = phase_tail - float(shared["phi"][0])
                rx = shared["rx_raw"] * np.exp(1j * shift)
                phase_tail = float(shared["phi"][-1] + shift)
                errors, features = _block_arms(rx, shared["bits"], shared["tx"], dpll)
                rows.append({
                    "pool": pool, "seed": seed, "block": block_id,
                    "condition": f"{turb}@{snr_db:g}", "turbulence": turb,
                    "snr_db_evaluator_only": snr_db, "dwell": dwell,
                    "n_bits": N_DATA_BITS, "errors": errors, "features": features,
                    "realization_key": f"{pool}:{seed}:{block_id}",
                })
                block_id += 1
    return rows


def freeze_selectors(rows):
    arms = ("DA", "NDA", "DPLL")
    totals = {a: sum(r["errors"][a] for r in rows) for a in arms}
    bstar = min(arms, key=totals.get)
    by_condition = {}
    for condition in sorted({r["condition"] for r in rows}):
        subset = [r for r in rows if r["condition"] == condition]
        by_condition[condition] = min(arms, key=lambda a: sum(r["errors"][a] for r in subset))

    powers = np.array([r["features"]["power"] for r in rows])
    innovations = np.array([r["features"]["innovation"] for r in rows])
    best = None
    for power_threshold in np.quantile(powers, [0.25, 0.5, 0.75]):
        for innovation_threshold in np.quantile(innovations, [0.25, 0.5, 0.75]):
            error = sum(
                r["errors"][
                    "NDA" if r["features"]["power"] >= power_threshold
                    and r["features"]["innovation"] <= innovation_threshold else "DA"
                ]
                for r in rows
            )
            candidate = (error, float(power_threshold), float(innovation_threshold))
            best = candidate if best is None or candidate < best else best
    bins = tuple(float(x) for x in np.quantile(powers, [1 / 3, 2 / 3]))
    middle = [r for r in rows if bins[0] <= r["features"]["power"] < bins[1]]
    middle_action = min(("DA", "NDA"), key=lambda a: sum(r["errors"][a] for r in middle))
    selectors = FrozenSelectors(
        power_threshold=best[1], innovation_threshold=best[2], bins=bins,
        bin_actions=("DA", middle_action, "NDA"), confidence_margin=0.05 * (bins[1] - bins[0]),
        global_best=bstar,
    )
    return selectors, {
        "B_star": bstar, "B_condition": by_condition,
        "p1": {"power_threshold": best[1], "innovation_threshold": best[2]},
        "p2": {"bins": bins, "actions": ("DA", middle_action, "NDA")},
        "p3": {"confidence_margin": selectors.confidence_margin, "fallback": bstar},
        "validation_errors": totals,
    }


def aggregate(rows, selectors, frozen):
    output = []
    previous = []
    for row in rows:
        actions = {
            "P1": selectors.p1(previous, row["features"]),
            "P2": selectors.p2(previous, row["features"]),
            "P3": selectors.p3(previous, row["features"]),
            "B*": frozen["B_star"],
            "B-cond": frozen["B_condition"][row["condition"]],
        }
        oracle_action = min(("DA", "NDA", "DPLL"), key=lambda a: row["errors"][a])
        item = dict(row)
        item["actions"] = actions
        item["oracle_action"] = oracle_action
        item["selected_errors"] = {name: row["errors"][arm] for name, arm in actions.items()}
        item["selected_errors"]["oracle"] = row["errors"][oracle_action]
        output.append(item)
        previous.append(row["features"])
    summary = {}
    for condition in sorted({r["condition"] for r in output}):
        subset = [r for r in output if r["condition"] == condition]
        summary[condition] = {}
        for arm in ("DA", "NDA", "DPLL"):
            summary[condition][arm] = sum(r["errors"][arm] for r in subset) / sum(r["n_bits"] for r in subset)
        for arm in ("P1", "P2", "P3", "B*", "B-cond", "oracle"):
            summary[condition][arm] = sum(r["selected_errors"][arm] for r in subset) / sum(r["n_bits"] for r in subset)
    return output, summary


def verdict(summary, rows, frozen):
    methods = ("P1", "P2", "P3")
    bstar = frozen["B_star"]
    gains = defaultdict(dict)
    for turb in TURBS:
        x = list(SNRS)
        base = [summary[f"{turb}@{s:g}"]["B*"] for s in x]
        base_req = required_snr_db(x, base, target=P.HDFEC)
        for method in methods:
            curve = [summary[f"{turb}@{s:g}"][method] for s in x]
            req = required_snr_db(x, curve, target=P.HDFEC)
            gains[method][turb] = (
                base_req - req if isinstance(base_req, float) and isinstance(req, float)
                else "UNRESOLVED_NO_CROSSING"
            )
    best = min(methods, key=lambda m: sum(r["selected_errors"][m] for r in rows))
    base_error = sum(r["selected_errors"]["B*"] for r in rows)
    method_error = sum(r["selected_errors"][best] for r in rows)
    oracle_error = sum(r["selected_errors"]["oracle"] for r in rows)
    headroom = base_error - oracle_error
    closure = (base_error - method_error) / headroom if headroom > 0 else 0.0
    qualifying = [v for v in gains[best].values() if isinstance(v, float) and v >= 0.5]
    disposition = "METHOD_SIGNAL" if len(qualifying) >= 2 and closure >= 0.5 and method_error < base_error else "METHOD_FAIL_WITH_SPACE"
    return {
        "verdict": disposition, "best_method": best, "B_star": bstar,
        "required_snr_gain_db": dict(gains), "oracle_regret_closure": closure,
        "test_errors": {"method": method_error, "B_star": base_error, "oracle": oracle_error},
        "claim_ceiling": disposition,
    }


def main():
    smoke = identity_smoke()
    result_dir = SIM_ROOT / "results" / "a4-deployable-adaptive-cpr-v2"
    if not smoke["pass"]:
        save_results({"identity_smoke": smoke}, str(result_dir / "identity-smoke.json"), "run_t009")
        raise SystemExit("BLOCKED_IDENTITY")
    validation = generate_pool(VAL_SEEDS, "validation")
    selectors, frozen = freeze_selectors(validation)
    validation_summary = {}
    winners = set()
    for condition in sorted({r["condition"] for r in validation}):
        subset = [r for r in validation if r["condition"] == condition]
        bers = {
            arm: sum(r["errors"][arm] for r in subset) / sum(r["n_bits"] for r in subset)
            for arm in ("DA", "NDA")
        }
        winner = min(bers, key=bers.get)
        winners.add(winner)
        validation_summary[condition] = {"ber": bers, "winner": winner}
    mechanism_pass = winners == {"DA", "NDA"}
    if not mechanism_pass:
        adjudication = {
            "verdict": "BLOCKED_IDENTITY",
            "reason": "causal common-mask validation has no reliable DA/NDA ordering crossover",
            "identity_smoke": smoke,
            "mechanism_identity": {
                "pass": False, "observed_winners": sorted(winners),
                "conditions": validation_summary,
                "bounded_repairs_used": 1,
            },
            "selection_manifest_diagnostic_only": frozen,
            "primary_run": False,
        }
        save_results(
            {"identity_smoke": smoke, "validation_rows": validation},
            str(result_dir / "raw.json"), "run_t009",
        )
        save_results(adjudication, str(result_dir / "result.json"), "run_t009")
        print(json.dumps(adjudication, indent=2))
        raise SystemExit("BLOCKED_IDENTITY")
    test = generate_pool(TEST_SEEDS, "test")
    selected, summary = aggregate(test, selectors, frozen)
    decision = verdict(summary, selected, frozen)
    save_results(
        {"identity_smoke": smoke, "validation_rows": validation, "test_rows": selected},
        str(result_dir / "raw.json"), "run_t009",
    )
    save_results(
        {"selection_manifest": frozen, "aggregate": summary, "decision": decision},
        str(result_dir / "result.json"), "run_t009",
    )
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
