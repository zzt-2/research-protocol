"""PROMPT-016: parameter-sweep robustness for Q-CMA-FADE (5 seeds).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-14
> 来源: PROMPT-016 (主控派发, A 边低优先机械活)
> 性质: 鲁棒性展示 (非预注册 Go/No-Go 判决), 5 seeds 非最终版

## 任务

PROMPT-015 只在 f_G=30 一个点验证 ML 优于 standard-CMA。本脚本扩参数域看 ML
优势在 f_G / SNR / 调制阶数变化下稳不稳, 给论文 results 画鲁棒性趋势图。

## 参数网格 (35 cells, 每 cell 5 seeds = seeds 1000-1004)

固定: N=2M, strong turbulence (α=1.5 β=0.8), SOP=4e-7 (1krad/s), tap=11, block=100

三组扫描:
  - f_G 扫: f_G ∈ {30, 100, 1000} × {QPSK, 20dB} × 5 seeds = 15 cells (只变 f_G)
  - SNR 扫: SNR ∈ {20, 15, 10} dB × {QPSK, f_G=30} × 5 seeds = 15 cells (只变 SNR)
  - 16QAM : 1 点 {16QAM, f_G=30, 20dB} × 5 seeds = 5 cells (只变调制)

## 每个方法

四方法/cell: current-CMA, standard-CMA, ML-original, oracle (ML-aligned 省略,
PROMPT-015 已证初始化不敏感)。

## 双口径 (D018 规定)

fixed-label BER + permutation-invariant (PI) BER 必须并报. PI 需 pilot/帧头消歧.

## 边界标注 (陷阱3)

N=2M 在 f_G=30/100/1000 已被 PROMPT-012 审计覆盖 (D018 第4条). 新参数点
(不同 SNR / 16QAM) 用 2M 须标注"未独立审计 2M 在这些点的适用性".

## 已知陷阱

1. seed 数: 5 seeds (用户明确非最终版够). 接近的胜场 (3/5) 标"需加 seed"
2. PI-BER 双口径: fixed + PI 并报 (D018)
3. N=2M vs 5M: 2M 加速但新参数点未独立审计
4. 16QAM: D008 发现 CMA modulus mismatch, ML/CMA gap 可能反预期小于 QPSK,
   诚实记录不挑数据
5. evaluate_outputs 内部用 QPSK 4 旋转 BER → 16QAM cell 须自写 PI-BER

用法:
  cd projects/simulation
  python explore/cma-fade-divergence/prompt016_param_sweep.py --smoke   # 1 seed 验证
  python explore/cma-fade-divergence/prompt016_param_sweep.py            # 全量
"""
from __future__ import annotations

import argparse
import json
import math
import time
from itertools import permutations
from pathlib import Path
import sys

import numpy as np

SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

os_path = Path(__file__).resolve()
# CUBLAS deterministic before torch import
import os as _os
_os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

from common._config import BLOCK
from common._experiment import save_results
from common._ml_equalizer import MLChannelEqualizer
from params import SimulationConfig

# PROMPT-015/P013 helpers (QPSK dual-metric eval + CMA diagnostic)
from prompt012_longseq_audit import evaluate_outputs, ml_diverged, seed_ml
from prompt013_swap_mechanism_q2 import run_cma_diagnostic

# SNR-sweep parameterized channel (QPSK, gamma_bar arg)
from ber_vs_snr_scan import (
    gen_channel as gen_channel_qpsk,
    oracle_equalize as oracle_equalize_qpsk,
    snr_db_to_gamma,
)

# 16QAM gen/demap + parameterized channel (gamma_bar arg)
from ber_16qam_vs_fg import (
    gen_channel as gen_channel_16qam,
    oracle_equalize as oracle_equalize_16qam,
    compute_ber_16qam_phase_corrected,
    R2_16QAM,
)

# Common ML + CMA constants
from ml_long_seq_failure import ML_PARAMS, ML_TRAIN_FRAC, MU_SAFE, N_TAP


# ─── 实验参数 ───────────────────────────────────────────────────

N_SYMBOLS = 2_000_000
TURBULENCE = "strong"          # α=1.5, β=0.8
SOP_RATE = 4e-7                # 1 krad/s (sat.1553 §6.3)
SEEDS = tuple(range(1000, 1005))   # 5 seeds (PROMPT-016 §0: 中间验证 5 seeds 够)

# 扫描点
F_G_SWEEP = (30.0, 100.0, 1000.0)
SNR_SWEEP_DB = (20.0, 15.0, 10.0)   # 20dB 已知, 降 SNR
DEFAULT_FG = 30.0
DEFAULT_GAMMA = snr_db_to_gamma(20.0)   # = 100

# late slice: test 段 (后 50%) 的后 1/4 → [1.75M, 2M) for N=2M
N_TRAIN = int(N_SYMBOLS * ML_TRAIN_FRAC)   # 1.0M
N_TEST = N_SYMBOLS - N_TRAIN               # 1.0M
LATE_START = N_TRAIN + int(N_TEST * 0.75)  # 1.75M
LATE_END = N_SYMBOLS                       # 2.0M

R2_QPSK = 1.0
METHOD_ORDER = ("current-CMA", "standard-CMA", "ML-original", "oracle")

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt016_param_sweep.json"
)


# ─── cell 定义 ──────────────────────────────────────────────────

def build_grid():
    """构建 6 唯一 cells (f_G=30/snr20 是 f_G 扫与 SNR 扫共享基准点, 去重).

    PROMPT-016 §2 列的 35 cells 把基准点算了两次; 实际 6 唯一 cell × 5 seeds = 30.
    每个 cell = (cell_id, mod, f_g, snr_db, group)."""
    cells = []
    seen = set()
    def add(cell):
        if cell["cell_id"] not in seen:
            seen.add(cell["cell_id"])
            cells.append(cell)
    # f_G 扫 (QPSK, 20dB, 只变 f_G)
    for f_g in F_G_SWEEP:
        add({
            "cell_id": f"fg{int(f_g)}_qpsk_snr20",
            "mod": "QPSK", "f_g": float(f_g), "snr_db": 20.0,
            "group": "f_G_sweep",
        })
    # SNR 扫 (QPSK, f_G=30, 只变 SNR)
    for snr_db in SNR_SWEEP_DB:
        add({
            "cell_id": f"fg30_qpsk_snr{int(snr_db)}",
            "mod": "QPSK", "f_g": DEFAULT_FG, "snr_db": float(snr_db),
            "group": "snr_sweep",
        })
    # 16QAM (f_G=30, 20dB, 只变调制)
    add({
        "cell_id": "fg30_16qam_snr20",
        "mod": "16QAM", "f_g": DEFAULT_FG, "snr_db": 20.0,
        "group": "modulation",
    })
    return cells


# ─── 16QAM PI-BER 评估 (evaluate_outputs 是 QPSK 专用, 16QAM 须自写) ──

def evaluate_outputs_16qam(z_x, z_y, s_x, s_y, diverged: bool):
    """16QAM 双口径: fixed-label + PI (排列不变), LS 相位校正.

    跟 evaluate_outputs 结构同构, 但 BER 用 compute_ber_16qam_phase_corrected
    (LS 连续相位估计, 非 QPSK 4 旋转).
    """
    outputs = (np.asarray(z_x), np.asarray(z_y))
    sources = (np.asarray(s_x), np.asarray(s_y))
    fixed_per_output = [
        compute_ber_16qam_phase_corrected(outputs[0], sources[0]),
        compute_ber_16qam_phase_corrected(outputs[1], sources[1]),
    ]
    candidates = []
    for assignment in permutations((0, 1)):
        bers = [
            compute_ber_16qam_phase_corrected(outputs[i], sources[assignment[i]])
            for i in range(2)
        ]
        candidates.append((float(np.mean(bers)), assignment, bers))
    pi_mean, assignment, pi_per_output = min(candidates, key=lambda item: item[0])
    return {
        "fixed_label_ber": {
            "zX_sX": float(fixed_per_output[0]),
            "zY_sY": float(fixed_per_output[1]),
            "mean": float(np.mean(fixed_per_output)),
        },
        "permutation_invariant_ber": {
            "mean": pi_mean,
            "per_output": [float(x) for x in pi_per_output],
            "assignment": ["sX" if i == 0 else "sY" for i in assignment],
        },
        "diverged": bool(diverged),
    }


def _evaluate(z_x, z_y, s_x, s_y, diverged: bool, mod: str):
    if mod == "QPSK":
        return evaluate_outputs(z_x, z_y, s_x, s_y, diverged)
    return evaluate_outputs_16qam(z_x, z_y, s_x, s_y, diverged)


# ─── 单 seed 单 cell ────────────────────────────────────────────

def run_cell_seed(cell: dict, seed: int) -> dict:
    """跑一个 (cell, seed) 的四方法对比. 返回 trial dict."""
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    mod = cell["mod"]
    f_g = cell["f_g"]
    gamma_bar = snr_db_to_gamma(cell["snr_db"])
    r2 = R2_QPSK if mod == "QPSK" else R2_16QAM

    # 信道 (7 参, gamma_bar 参数化)
    if mod == "QPSK":
        r_x, r_y, s_x, s_y, h, theta = gen_channel_qpsk(
            N_SYMBOLS, alpha, beta, f_g, SOP_RATE, gamma_bar, int(seed)
        )
    else:
        r_x, r_y, s_x, s_y, h, theta = gen_channel_16qam(
            N_SYMBOLS, alpha, beta, f_g, SOP_RATE, gamma_bar, int(seed)
        )

    late = slice(LATE_START, LATE_END)
    source_x = s_x[late]
    source_y = s_y[late]

    # --- CMA current / standard (late_slice 适配 N=2M) ---
    current = run_cma_diagnostic(
        r_x, r_y, mode="current", mu=MU_SAFE, n_tap=N_TAP, r2=r2,
        late_slice=(LATE_START, LATE_END), fork_at=LATE_START,
    )
    standard = run_cma_diagnostic(
        r_x, r_y, mode="standard", mu=MU_SAFE, n_tap=N_TAP, r2=r2,
        late_slice=(LATE_START, LATE_END), fork_at=LATE_START,
    )

    # --- ML-original (训练前 50%, 推理全段) ---
    seed_ml(seed)
    ml = MLChannelEqualizer(**ML_PARAMS)
    ml.train(r_x[:N_TRAIN], r_y[:N_TRAIN], s_x[:N_TRAIN], s_y[:N_TRAIN],
             val_split=0.2, verbose=False)
    ml_res = ml.equalize(r_x, r_y)
    z_x_ml = np.asarray(ml_res["zX"]).flatten()
    z_y_ml = np.asarray(ml_res["zY"]).flatten()
    ml_div = ml_diverged(ml_res, z_x_ml, z_y_ml)

    # --- oracle (撤销 SOP + MMSE) ---
    if mod == "QPSK":
        oracle_x, oracle_y = oracle_equalize_qpsk(r_x, r_y, h, theta, gamma_bar)
    else:
        oracle_x, oracle_y = oracle_equalize_16qam(r_x, r_y, h, theta, gamma_bar)

    trial = {
        "seed": int(seed),
        "cell_id": cell["cell_id"],
        "mod": mod,
        "f_g": float(f_g),
        "snr_db": float(cell["snr_db"]),
        "gamma_bar": float(gamma_bar),
        "r2": float(r2),
        "late_slice": [LATE_START, LATE_END],
        "elapsed_s": time.time() - started,
        "methods": {
            "current-CMA": _evaluate(
                current["online"]["zX"], current["online"]["zY"],
                source_x, source_y, False, mod,
            ),
            "standard-CMA": _evaluate(
                standard["online"]["zX"], standard["online"]["zY"],
                source_x, source_y, False, mod,
            ),
            "ML-original": _evaluate(
                z_x_ml[late], z_y_ml[late], source_x, source_y, ml_div, mod,
            ),
            "oracle": _evaluate(
                oracle_x[late], oracle_y[late], source_x, source_y, False, mod,
            ),
        },
    }

    # 超额 PI-BER vs oracle
    oracle_pi = float(trial["methods"]["oracle"]["permutation_invariant_ber"]["mean"])
    for name in METHOD_ORDER:
        if name == "oracle":
            continue
        pi = float(trial["methods"][name]["permutation_invariant_ber"]["mean"])
        trial["methods"][name]["excess_pi_ber_vs_oracle"] = pi - oracle_pi

    return trial


# ─── 配对胜场 (ML vs standard-CMA, 描述用) ─────────────────────

def paired_wins(trials: list[dict]) -> dict:
    """cell 内 5 seeds, ML-original vs standard-CMA 配对胜场 (超额 PI-BER)."""
    seeds = sorted(int(t["seed"]) for t in trials)
    by_seed = {int(t["seed"]): t for t in trials}
    diffs = []
    for seed in seeds:
        t = by_seed[seed]
        ml_excess = float(t["methods"]["ML-original"]["excess_pi_ber_vs_oracle"])
        std_excess = float(t["methods"]["standard-CMA"]["excess_pi_ber_vs_oracle"])
        diffs.append(ml_excess - std_excess)   # <0 → ML 赢
    diffs = np.asarray(diffs)
    ml_wins = int(np.sum(diffs < 0))
    std_wins = int(np.sum(diffs > 0))
    ties = int(np.sum(diffs == 0))
    return {
        "n_seeds": len(seeds),
        "ml_wins": ml_wins,
        "standard_cma_wins": std_wins,
        "ties": ties,
        "ml_win_fraction": float(ml_wins / len(seeds)) if seeds else 0.0,
        "mean_excess_diff_ml_minus_std": float(np.mean(diffs)),
    }


def summarize_cell(cell: dict, trials: list[dict]) -> dict:
    """聚合一个 cell 的 5 seeds → 均值/SD + 胜场."""
    summary = {
        "cell_id": cell["cell_id"],
        "mod": cell["mod"],
        "f_g": cell["f_g"],
        "snr_db": cell["snr_db"],
        "group": cell["group"],
        "n_seeds": len(trials),
    }
    for name in METHOD_ORDER:
        pi_vals = [float(t["methods"][name]["permutation_invariant_ber"]["mean"]) for t in trials]
        fixed_vals = [float(t["methods"][name]["fixed_label_ber"]["mean"]) for t in trials]
        entry = {
            "pi_ber_mean": float(np.mean(pi_vals)),
            "pi_ber_std": float(np.std(pi_vals)),
            "fixed_ber_mean": float(np.mean(fixed_vals)),
            "fixed_ber_std": float(np.std(fixed_vals)),
        }
        if name != "oracle":
            excess = [float(t["methods"][name]["excess_pi_ber_vs_oracle"]) for t in trials]
            entry["excess_pi_ber_mean"] = float(np.mean(excess))
            entry["excess_pi_ber_std"] = float(np.std(excess))
        summary[name] = entry
    summary["paired_ml_vs_standard_cma"] = paired_wins(trials)
    return summary


# ─── checkpoint ─────────────────────────────────────────────────

def _load_ckpt() -> dict:
    if RESULT_PATH.exists():
        try:
            return json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_ckpt(payload: dict):
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_results(payload, str(RESULT_PATH), "prompt016_param_sweep")


def _completed_keys(payload: dict) -> set:
    """已完成的 (cell_id, seed) 对."""
    done = set()
    for t in payload.get("trials", []):
        done.add((t["cell_id"], int(t["seed"])))
    return done


# ─── main ───────────────────────────────────────────────────────

def _parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--smoke", action="store_true",
                   help="只跑 1 seed 1 cell 验证管线")
    p.add_argument("--cells", nargs="*", default=None,
                   help="只跑指定 cell_id (默认全 35)")
    p.add_argument("--seeds", nargs="*", type=int, default=None,
                   help="只跑指定 seeds (默认 1000-1004)")
    p.add_argument("--max-runs", type=int, default=None,
                   help="本次最多新增 (cell,seed) 数 (防超时; 已完成的不计)")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    cells = build_grid()
    if args.cells:
        wanted = set(args.cells)
        cells = [c for c in cells if c["cell_id"] in wanted]
    seeds = list(args.seeds) if args.seeds else list(SEEDS)
    if args.smoke:
        cells = cells[:1]
        seeds = seeds[:1]

    t0 = time.time()
    print("=" * 72)
    print(f"PROMPT-016: 参数域鲁棒性扫描 ({len(cells)} cells × {len(seeds)} seeds)")
    print(f"N={N_SYMBOLS}, turb={TURBULENCE}, SOP={SOP_RATE} (1krad/s), "
          f"late_slice=[{LATE_START},{LATE_END})")
    print(f"ML_CONFIG={ML_PARAMS}")
    print(f"工作目录: {SIM_DIR}")
    if args.smoke:
        print("** SMOKE TEST: 1 cell × 1 seed **")
    print("=" * 72)

    payload = _load_ckpt()
    payload.setdefault("experiment", "PROMPT-016 param sweep")
    payload.setdefault("trials", [])
    payload["config"] = {
        "n_symbols": N_SYMBOLS,
        "turbulence": TURBULENCE,
        "sop_rate": SOP_RATE,
        "seeds": seeds,
        "late_slice": [LATE_START, LATE_END],
        "ml_config": ML_PARAMS,
        "ml_train_fraction": ML_TRAIN_FRAC,
        "mu_safe": MU_SAFE,
        "n_tap": N_TAP,
        "r2_qpsk": R2_QPSK,
        "r2_16qam": float(R2_16QAM),
        "f_g_sweep": list(F_G_SWEEP),
        "snr_sweep_db": list(SNR_SWEEP_DB),
        "smoke": bool(args.smoke),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    done = _completed_keys(payload)

    n_run = 0
    n_skip = 0
    max_runs = args.max_runs
    stop_early = False
    for cell in cells:
        if stop_early:
            break
        cell_id = cell["cell_id"]
        cell_trials = []
        for seed in seeds:
            key = (cell_id, int(seed))
            if key in done and not args.smoke:
                # 从已有 payload 取
                for t in payload["trials"]:
                    if t["cell_id"] == cell_id and int(t["seed"]) == int(seed):
                        cell_trials.append(t)
                        break
                n_skip += 1
                continue
            if max_runs is not None and n_run >= max_runs:
                stop_early = True
                break
            t1 = time.time()
            trial = run_cell_seed(cell, int(seed))
            cell_trials.append(trial)
            # 追加到 payload 并存盘 (checkpoint per seed)
            payload["trials"].append(trial)
            payload["trials"].sort(key=lambda r: (r["cell_id"], int(r["seed"])))
            done.add(key)
            if not args.smoke:
                _save_ckpt(payload)
            n_run += 1
            pi_ml = trial["methods"]["ML-original"]["permutation_invariant_ber"]["mean"]
            pi_std = trial["methods"]["standard-CMA"]["permutation_invariant_ber"]["mean"]
            print(f"  {cell_id} seed{seed}: "
                  f"ML PI={pi_ml:.5f} stdCMA PI={pi_std:.5f} "
                  f"({time.time()-t1:.0f}s)", flush=True)

    # 汇总 (smoke 模式不汇总, 只验证管线)
    if not args.smoke:
        summaries = []
        for cell in cells:
            cell_id = cell["cell_id"]
            cell_trials = [t for t in payload["trials"] if t["cell_id"] == cell_id]
            if cell_trials:
                summaries.append(summarize_cell(cell, cell_trials))
        payload["summaries"] = summaries

    payload["config"]["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    payload["config"]["elapsed_s"] = time.time() - t0
    payload["config"]["n_run"] = n_run
    payload["config"]["n_skipped"] = n_skip
    _save_ckpt(payload)

    print(f"\n完成: 跑 {n_run} 个 (cell,seed), 跳过 {n_skip} 个 (cached)")
    print(f"总耗时: {time.time()-t0:.0f}s")
    print(f"结果: {RESULT_PATH}")
    return payload


if __name__ == "__main__":
    main()
