"""PROMPT-026 B 类架构候选的 D031 前馈时序门控记录。

本脚本不运行性能 MVE：B1/B2/B3 均是离线训练后固定前馈，检索未提供其对未见
SOP 极端旋转保持等变/不变的证据，因此在 H013 的 D031 硬门处 defer。
运行脚本只把预注册筛选、检索证据、四判据和“不运行理由”注入元数据后落盘。
"""
from pathlib import Path
import sys

SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
from common._experiment import save_results

OUT = SIM_DIR / "results/cma-fade-divergence/prompt026_b_class_architecture_gate.json"

SEARCH = {
    "B1": [
        "search-archive/2026-07-16/2026-07-16-complex-valued-neural-network-rf-mimo-equalization-1.json",
        "search-archive/2026-07-16/complex-valued-neural-network-coherent-optical-equalizer.json",
    ],
    "B2": [
        "search-archive/2026-07-16/rotation-equivariant-cnn-optical-communication-equalization.json",
        "search-archive/2026-07-16/sop-rotation-equivariant-neural-network-polarization-optical.json",
    ],
    "B3": [
        "search-archive/2026-07-16/dual-branch-polarization-demultiplexing-neural-network.json",
        "search-archive/2026-07-16/2026-07-16-dual-polarization-optical-neural-equalizer-branch-demultiple-1.json",
    ],
}


def main():
    common = {
        "problem": "D014 SOP-driven polarization mixing degrades the fixed ML equalizer in test-late",
        "baseline": "D022 L0 ButterflyCNNEqualizer2x2",
        "comparison": "same channel/seeds, fixed+PI BER, parameter-count matched ablation",
    }
    payload = {
        "experiment": "PROMPT-026 B-class D031 architecture admission gate",
        "performance_mve_run": False,
        "preregistered_gate": "Only an architecture with literature/analysis support for unseen-SOP equivariance may enter MVE",
        "search_files": SEARCH,
        "candidates": {
            "B1_complex_valued": {
                "four_criteria": {**common, "method_output": "complex-valued butterfly network"},
                "collision": "Strong adjacent hit: Optics Letters 2024 10.1364/OL.512416, MIMO-CVNN preserving phase and X/Y polarization relations in PDM link",
                "touches_test_state": False,
                "breaks_temporal_orthogonality": False,
                "reason": "Complex arithmetic improves representation but supplies neither online state nor group-equivariance to unseen SOP rotation",
                "verdict": "DEFER",
            },
            "B2_sop_angle_attention": {
                "four_criteria": {**common, "method_output": "SOP-sensitive attention/equivariant architecture"},
                "collision": "No direct hit in two registered searches; zero results is not evidence of feasibility",
                "touches_test_state": False,
                "breaks_temporal_orthogonality": False,
                "reason": "Attention fixed after training has no observed SOP angle/test-time state; searches supplied no rotation-equivariance support in optical equalization",
                "verdict": "DEFER",
            },
            "B3_dual_branch": {
                "four_criteria": {**common, "method_output": "separate X/Y polarization branches with fusion"},
                "collision": "No direct hit in two registered searches",
                "touches_test_state": False,
                "breaks_temporal_orthogonality": False,
                "reason": "Fixed X/Y branches are basis-dependent; SOP rotation mixes the branches and no adaptive/equivariant mechanism follows the test basis",
                "verdict": "DEFER",
            },
        },
        "class_verdict": "DEFER_NO_MVE",
        "not_run_reason": "All variants fail the H013/D031 test-segment admission gate; running the 5-seed grid would repeat A/C temporal-orthogonality failure without a falsifiable mechanism",
        "planned_mve_if_reopened": {
            "domain": "N=5M,f_G=30,SOP=4e-7,strong,20dB,QPSK,seeds1000-1004,late[4.375M,5M)",
            "metrics": ["fixed-label BER", "PI-BER"],
            "controls": ["L0", "parameter-matched real network", "module-off ablation"],
        },
    }
    save_results(payload, str(OUT), "prompt026_b_class_architecture_gate")


if __name__ == "__main__":
    main()
