"""PROMPT-025 C1 在线微调 MVE（隔离脚本，不修改 common/）。

当前在 GW Step 4a 维度 D。GW Step 1 检索见：
  search-archive/2026-07-16/online-fine-tuning-optical-equalizer.json
  search-archive/2026-07-16/online-adaptation-neural-network-optical-communication.json

检索发现 AdaNN (JLT 2020, 10.1109/JLT.2020.2991028) 与 joint PMD
tracking (JLT 2023, 10.1109/JLT.2023.3276373) 已证明光纤场景在线/决策反馈
适配可行，但没有命中“星地相干 FSO + GG 湍流 + SOP lock swap”同场景同机制。

预注册：K=[1000,5000,10000] blocks，lr=[1e-5,1e-4]；任一配置 late PI-BER
低于 L0、至少 4/5 seeds 胜且单侧精确 Wilcoxon p<0.05 为 GO，否则 KILL。
lr=0、K=1000 为消融，必须逐 seed 退回 L0。fixed/PI 双口径并报（D018）。

信息访问边界：本 MVE 的在线一步使用最近 1024 个已知符号作为监督目标，等价于周期
pilot/training burst，属于 genie/pilot-assisted 可行性上界，不可表述为 blind online adaptation。
"""
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

SIM_DIR = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(HERE))

from common._config import BLOCK
from common._experiment import save_results
from ml_long_seq_failure import (F_G, GAMMA_BAR, N_TAP, SOP_RATE, gen_channel,
                                 oracle_equalize, test_late_slice)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs
from prompt024_a_class_loss_variants import model_equalize, train_variant

N_SYMBOLS = 5_000_000
SEEDS = (1000, 1001, 1002, 1003, 1004)
K_GRID = (1000, 5000, 10000)
LR_GRID = (1e-5, 1e-4)
UPDATE_SYMBOLS = 1024
OUT_PATH = SIM_DIR / "results/cma-fade-divergence/prompt025_c1_online_finetune.json"
CFG = SimulationConfig()


def _model_input(x: np.ndarray, device: str) -> torch.Tensor:
    n = len(x)
    return torch.cat((torch.from_numpy(x.real).view(1, 1, n).float(),
                      torch.from_numpy(x.imag).view(1, 1, n).float()), dim=1).to(device)


def _one_supervised_step(model, optimizer, rx, ry, sx, sy, device):
    """最近一个 pilot burst 上做恰好一步；lr=0 是结构相同的消融。"""
    model.train()
    optimizer.zero_grad()
    zx, zy = model(_model_input(rx, device), _model_input(ry, device))
    sx_t = torch.from_numpy(sx.astype(np.complex64)).view(1, -1).to(device)
    sy_t = torch.from_numpy(sy.astype(np.complex64)).view(1, -1).to(device)
    mse = nn.MSELoss()
    loss = (mse(zx.real, sx_t.real) + mse(zx.imag, sx_t.imag) +
            mse(zy.real, sy_t.real) + mse(zy.imag, sy_t.imag))
    loss.backward()
    optimizer.step()
    return float(loss.item())


def online_equalize_late(base_state, rx, ry, sx, sy, k_blocks, lr):
    """顺序处理 test 段；每 K 个物理 block 后用最近 pilot burst 更新一步。"""
    from common._ml_equalizer import ButterflyCNNEqualizer2x2

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model.load_state_dict(copy.deepcopy(base_state))
    optimizer = optim.Adam(model.parameters(), lr=lr)
    test_start = N_SYMBOLS // 2
    late_start, late_end = test_late_slice(N_SYMBOLS)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(late_end - late_start, dtype=np.complex64)
    out_y = np.empty_like(out_x)
    losses, updates = [], 0

    for start in range(test_start, N_SYMBOLS, interval):
        end = min(start + interval, N_SYMBOLS)
        zx, zy, _ = model_equalize(model, rx[start:end], ry[start:end], device=device)
        lo, hi = max(start, late_start), min(end, late_end)
        if lo < hi:
            out_x[lo - late_start:hi - late_start] = zx[lo - start:hi - start]
            out_y[lo - late_start:hi - late_start] = zy[lo - start:hi - start]
        if end < N_SYMBOLS:
            u0 = max(start, end - UPDATE_SYMBOLS)
            losses.append(_one_supervised_step(model, optimizer, rx[u0:end], ry[u0:end],
                                                sx[u0:end], sy[u0:end], device))
            updates += 1
        del zx, zy
    norm = float(model.weights_norm())
    diverged = (not np.isfinite(norm)) or norm > 10.0 * float(model.init_norm())
    return out_x, out_y, diverged, updates, losses


def _metrics(zx, zy, sx, sy, diverged=False):
    e = evaluate_outputs(zx, zy, sx, sy, diverged)
    return {"fixed_ber_mean": float(e["fixed_label_ber"]["mean"]),
            "pi_ber_mean": float(e["permutation_invariant_ber"]["mean"]),
            "classification": e["classification"]}


def _one_sided_wilcoxon(l0, candidate):
    from scipy.stats import wilcoxon
    d = np.asarray(l0) - np.asarray(candidate)
    if np.allclose(d, 0):
        return 1.0
    return float(wilcoxon(d, alternative="greater", method="exact").pvalue)


def _summarize(trials):
    names = sorted(trials[0]["methods"])
    out = {}
    l0 = np.array([t["methods"]["L0"]["pi_ber_mean"] for t in trials])
    for name in names:
        vals = np.array([t["methods"][name]["pi_ber_mean"] for t in trials])
        fixed = np.array([t["methods"][name]["fixed_ber_mean"] for t in trials])
        row = {"mean_pi": float(vals.mean()), "mean_fixed": float(fixed.mean()),
               "per_seed_pi": vals.tolist()}
        if name != "L0":
            row.update({"wins": int(np.sum(vals < l0)),
                        "p_one_sided_exact": _one_sided_wilcoxon(l0, vals),
                        "mean_delta_l0_minus_candidate": float((l0 - vals).mean())})
            row["verdict"] = "GO" if row["wins"] >= 4 and row["p_one_sided_exact"] < 0.05 and row["mean_pi"] < float(l0.mean()) else "KILL"
        out[name] = row
    out["class_verdict"] = "GO" if any(v.get("verdict") == "GO" for v in out.values() if isinstance(v, dict)) else "KILL"
    return out


def _save(payload):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".prompt025_", suffix=".json", dir=OUT_PATH.parent)
    os.close(fd)
    try:
        save_results(payload, tmp, "prompt025_c1_online_finetune")
        os.replace(tmp, OUT_PATH)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    payload = {"experiment": "PROMPT-025 C1 periodic online fine-tuning",
               "preregistered": {"K_blocks": list(K_GRID), "lr": list(LR_GRID),
                                  "seeds": list(SEEDS), "go": "mean PI<L0 and wins>=4/5 and one-sided exact Wilcoxon p<0.05",
                                  "ablation": "K=1000, lr=0 returns to L0"},
               "information_access": "genie/pilot-assisted: latest 1024 known symbols per update",
               "metric_signature": "late[4.375M,5M), fixed-label and permutation-invariant BER",
               "state_lifecycle": "one offline model per seed; cloned per config; online state continuous across test[2.5M,5M)",
               "trials": []}
    alpha, beta = CFG.turbulence.as_dict()["strong"]
    completed = {int(t["seed"]) for t in payload["trials"]}
    for seed in SEEDS:
        if seed in completed:
            continue
        t0 = time.time()
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        rx, ry, sx, sy, h, theta = gen_channel(N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)
        model, hist = train_variant(rx, ry, sx, sy, "L0_mse", 0.0, device="cuda", verbose=False)
        state = copy.deepcopy(model.state_dict())
        late_s, late_e = test_late_slice(N_SYMBOLS)
        zx0, zy0, div0 = model_equalize(model, rx[late_s:late_e], ry[late_s:late_e])
        methods = {"L0": _metrics(zx0, zy0, sx[late_s:late_e], sy[late_s:late_e], div0)}
        for k in K_GRID:
            for lr in LR_GRID:
                name = f"C1_K{k}_lr{lr:.0e}"
                zx, zy, div, updates, losses = online_equalize_late(state, rx, ry, sx, sy, k, lr)
                methods[name] = _metrics(zx, zy, sx[late_s:late_e], sy[late_s:late_e], div)
                methods[name].update({"updates": updates, "update_loss_mean": float(np.mean(losses))})
        zx, zy, div, updates, losses = online_equalize_late(state, rx, ry, sx, sy, 1000, 0.0)
        methods["ablation_K1000_lr0"] = _metrics(zx, zy, sx[late_s:late_e], sy[late_s:late_e], div)
        methods["ablation_K1000_lr0"].update({"updates": updates, "update_loss_mean": float(np.mean(losses))})
        zxo, zyo = oracle_equalize(rx[late_s:late_e], ry[late_s:late_e], h[late_s:late_e], theta[late_s:late_e], GAMMA_BAR)
        methods["oracle"] = _metrics(zxo, zyo, sx[late_s:late_e], sy[late_s:late_e])
        payload["trials"].append({"seed": seed, "methods": methods,
                                  "offline_best_val_mse": float(hist["best_val_mse"]),
                                  "elapsed_s": time.time() - t0})
        payload["checkpoint"] = {"completed_seeds": [t["seed"] for t in payload["trials"]],
                                 "pending_seeds": [s for s in SEEDS if s not in {t["seed"] for t in payload["trials"]}]}
        _save(payload)
        print(seed, {k: round(v["pi_ber_mean"], 6) for k, v in methods.items()}, flush=True)
    payload["summary"] = _summarize(payload["trials"])
    payload["ablation_pass"] = all(abs(t["methods"]["L0"]["pi_ber_mean"] - t["methods"]["ablation_K1000_lr0"]["pi_ber_mean"]) < 1e-12 for t in payload["trials"])
    payload["checkpoint"]["complete"] = len(payload["trials"]) == len(SEEDS)
    _save(payload)
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
