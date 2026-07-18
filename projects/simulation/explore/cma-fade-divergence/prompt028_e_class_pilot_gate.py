"""PROMPT-028 E 类 pilot 前置准入门；不运行性能 MVE。"""
from pathlib import Path
import sys

SIM_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = SIM_DIR.parents[1]
sys.path.insert(0, str(SIM_DIR))
from common._experiment import save_results

OUT = SIM_DIR / "results/cma-fade-divergence/prompt028_e_class_pilot_gate.json"
SEARCH_FILES = [
    "search-archive/2026-07-16/e-pilot-sop-estimation.json",
    "search-archive/2026-07-16/e-pilot-polarization-tracking.json",
    "search-archive/2026-07-16/e-training-jones-estimation.json",
    "search-archive/2026-07-16/e-pilot-demux-broad.json",
    "search-archive/2026-07-16/e-data-aided-jones-broad.json",
]


def main():
    assert all((REPO_DIR / p).exists() for p in SEARCH_FILES)
    payload = {
        "experiment": "PROMPT-028 E-class pilot-aided SOP/Jones admission gate",
        "performance_mve_run": False,
        "search_files": SEARCH_FILES,
        "d031": {
            "verdict": "PASS",
            "reason": "Test-segment pilots estimate SOP/Jones state and feed forward compensation, so the mechanism directly reaches late swap.",
        },
        "four_criteria": {
            "problem_real": "PASS",
            "method_increment": "UNRESOLVED",
            "falsifiable_mve": "PASS",
            "novelty_hard_collision": "UNRESOLVED",
        },
        "class_verdict": "DEFER_NO_MVE",
        "search_result_accounting": "The first mixed-source query returned 10 records; the other four arXiv-only queries returned zero. It is false to describe all five searches as zero-result.",
        "strong_collision_evidence": [
            "2018 JLT 10.1109/JLT.2017.2785341: pilot-aided equalization with fast 1-tap SOP estimation (metadata; abstract unavailable).",
            "2023 JLT 10.1109/JLT.2023.3243828: training-sequence/data-aided DSP for fast coherent-PON convergence.",
            "2023 JLT 10.1109/JLT.2023.3253383: inserted pilots estimate channel response and feed-forward compensation tracks fast SOP transients.",
            "2024 JLT 10.1109/JLT.2023.3320905: inserted pilots continuously track SOP and equalizer coefficients.",
            "2026 JLT 10.1109/JLT.2025.3640695: shared preamble supports SOP tracking and adaptive polarization equalization.",
        ],
        "defer_reason": "Pilot/data-aided SOP/Jones estimation plus feed-forward compensation is strongly occupied in coherent fiber/PON. FSO Gamma-Gamma/SOP lock-swap is a scenario migration, but current evidence supports at most application validation, not a method increment; direct FSO coverage and full-text boundaries remain unresolved.",
        "information_access": {
            "pilot_method": "Known inserted pilot symbols only; pilot overhead must be charged.",
            "oracle_upper_bound": "True simulated SOP/Jones state; upper bound only, never described as blind or deployable.",
            "blind_claim_allowed": False,
        },
        "metric_contract": {
            "domain": "D022 historical: alpha=1.5,beta=0.8,N=5M,f_G=30,SOP=4e-7,strong,20dB,QPSK,seeds1000-1004,late[4.375M,5M)",
            "report": ["fixed-label BER", "PI-BER", "pilot overhead"],
            "paired_seed_test": "exact one-sided Wilcoxon against L0",
            "go": "mean PI < L0, >=4/5 paired wins, p<0.05, with pilot overhead disclosed",
            "kill": "fails any Go condition or zero-comp/module-off does not remove the gain",
        },
        "state_contract": {
            "causality": "pilot observations at or before block b may control compensation from b onward; no future symbols",
            "estimator_state": "reset once per seed; sequential through test-late",
            "equalizer_state": "same initialization and lifecycle across paired methods",
        },
        "planned_methods_if_reopened": {
            "L0": "registered ML-only baseline",
            "pilot_estimate_comp_equalizer": "minimum pilot-density Jones/SOP estimate, causal compensation, then equalizer",
            "oracle_sop_upper_bound": "true-state compensation, explicitly non-deployable upper bound",
            "no_pilot_zero_comp_ablation": "identical pipeline with zero compensation/module off",
        },
        "revival_conditions": [
            "Obtain full text for the direct pilot/data-aided SOP/Jones precedents and finish direct FSO coverage screening.",
            "Show a mechanism increment beyond applying the occupied pilot/feed-forward chain to FSO; scenario-only validation is insufficient.",
            "Freeze pilot density, estimator, overhead accounting, and causal timing before any performance run.",
        ],
        "performance_numbers": None,
    }
    save_results(payload, str(OUT), "prompt028_e_class_pilot_gate")


if __name__ == "__main__":
    main()
