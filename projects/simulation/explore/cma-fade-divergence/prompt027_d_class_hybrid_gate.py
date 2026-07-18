"""PROMPT-027 D 类 CMA+ML 混合的解析支配门控。

D1/D2 确实作用于 test 段：检测 CMA swap 后切到独立、未污染的固定 ML。因此相较
D028 回滚同一 CMA 状态，它能立即离开 swap 盆地。但注册指标是 late[4.375M,5M)，
D028 已证永久 swap 从 block 36698 起，late 从约 block 68359 起；切换早于 late 时，
hybrid late 输出逐样本等于 L0(固定 ML)，不可能严格优于 L0；切换晚则更差。
故在解析上界门 Kill，不重复运行被支配的 5-seed 性能网格。
"""
from pathlib import Path
import sys

SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
from common._experiment import save_results

OUT = SIM_DIR / "results/cma-fade-divergence/prompt027_d_class_hybrid_gate.json"


def main():
    payload = {
        "experiment": "PROMPT-027 D-class CMA+ML hybrid analytic gate",
        "performance_mve_run": False,
        "search_files": [
            "search-archive/2026-07-16/hybrid-cma-machine-learning-equalization.json",
            "search-archive/2026-07-16/cma-neural-network-switching-optical-equalizer.json",
            "search-archive/2026-07-16/polarization-swap-machine-learning-recovery-coherent-optical.json",
        ],
        "search_assessment": "No direct arXiv hit; OpenAlex was rate-limited, so zero hits are not claimed as absolute novelty",
        "d031": {
            "touches_test_segment": True,
            "passes_temporal_gate": True,
            "why_better_than_rollback": "ML state is independently offline-trained and does not inherit the already-swapped CMA weights; after detection it leaves the bad basin immediately",
            "remaining_d028_shadow": "genie correlation detector still reacts after swap and incurs detection dwell; D028 measured rollback dwell median 11 blocks",
        },
        "four_criteria": {
            "technical_conflict": "CMA tracks SOP online but can permanently lock-swap; independent ML avoids CMA basin contamination",
            "method_output": "D1 CMA-to-ML recovery and D2 selective switch",
            "baseline": "D022 L0 fixed ML plus standard CMA",
            "comparison": "same channel/seeds, fixed/PI BER, detector-off and ML-only ablations",
            "result": "PASS before analytic dominance gate",
        },
        "information_access": "genie/post-hoc: swap detector corr(zX,sY)>corr(zX,sX) uses transmitted symbols; a deployable detector is not supplied",
        "metric_signature": "late[4.375M,5M), fixed-label and permutation-invariant BER",
        "state_lifecycle": "CMA online state until trigger; fixed offline ML has independent state; one-way permanent switch",
        "analytic_dominance": {
            "block_size_symbols": 64,
            "permanent_swap_start_block_d028": 36698,
            "late_start_block_approx": 68359,
            "cases": {
                "switch_before_late": "hybrid late output == L0 ML, so strict improvement is impossible",
                "switch_during_or_after_late": "hybrid contains CMA swapped samples, so no better than switching before late and generally worse than L0",
            },
            "upper_bound": "hybrid late PI-BER >= L0 late PI-BER; equality only under sufficiently early switch",
        },
        "candidates": {
            "D1_CMA_track_ML_recover": "KILL_ANALYTICALLY_DOMINATED_BY_L0",
            "D2_selective_switch": "KILL_ANALYTICALLY_DOMINATED_BY_L0",
        },
        "class_verdict": "KILL_NO_MVE",
        "not_run_reason": "The registered late-slice objective is upper-bounded by the ML-only baseline; a 5-seed run cannot satisfy strict mean PI<L0 and would add genie detection without performance headroom",
        "reopen_condition": "Use a metric including pre-switch operation/complexity, a domain where CMA beats ML before swap, and a deployable blind detector; then re-run GW Step 1 and preregister against both ML-only and CMA-only baselines",
    }
    save_results(payload, str(OUT), "prompt027_d_class_hybrid_gate")


if __name__ == "__main__":
    main()
