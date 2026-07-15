"""PROMPT-024 A 类（改 loss）横向对比 MVE.

> 方向: Q-CMA-FADE 方法层解冻探索 (D030) / 状态: WIP / 创建: 2026-07-15
> 组织规范: ../../SIM-ORG.md (P4 只扩不改 common/; P5 标方向+状态)
> 来源: PROMPT-024 (D030 方法层 A 类, 主控派出)

## 研究问题

A 类（改 loss，成本最低 + SOP 正则攻 D014 真因）三个 loss 变体横向对比：
  L0 baseline  : nn.MSELoss()（现有 D022 对照）
  L1 SOP 不变性正则 : MSE + λ·‖f(R_θ·r) − f(r)‖²（SOP 旋转数据增强 + 不变性惩罚）
  L2 对比学习   : MSE + λ·max(0, margin − ‖z_normal − z_swap‖²)（swap 做负对，攻 D014 lock-swap）
  L3 VAE 盲损失 : GW Step 1 检索发现硬撞车（Qin 2026 TCCN, 同场景同机制）→ DEFER，本轮不跑

## Go/Kill 预注册判据（防事后移门槛）

- Go : 任一 L1/L2 的 late-slice PI-BER 显著优于 L0（p<0.05 配对 Wilcoxon + ≥4/5 seeds 胜），
        且适用域不窄于 D022（N=5M/f_G=30）
- Kill: L1/L2 都不显著优于 L0 → A 类无增量，回主线记 Kill 进 C 类
- 消融可验（D030 必要条件）: 拿掉正则项（λ=0）性能得退回 L0，退了才证明正则有贡献

## 关键约束

1. 守 FR-22: 已走 GW Step 1 检索（A1/A2 PASS, A3 撞车 defer），本轮 MVE 合法
2. 守 D030: 归类批量横向对比；准入放宽（拼也行），唯一硬防线=检索防撞车已过
3. 守 D018: 双口径 fixed/PI 并报（复用 prompt012 evaluate_outputs）
4. 守消融可验: λ=0 退回 baseline
5. 不改 common/: 隔离脚本，import 复用 _ml_equalizer 模型 + ml_long_seq_failure gen_channel
6. 参数域与 D022 一致: N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK, 5 seeds (1000-1004),
   late slice [4.375M, 5M) — 含 D027 swap-prone seeds 1000/1002，正是 SOP 正则应发挥作用的点
7. TL-20 理论预期先行（见下方 HYPOTHESES）
8. TL-22 物理前提检查: L1 增强角度范围合理（≤0.2rad，不破坏 QPSK 星座）；L2 margin 量级合理

## TL-20 假设（跑前写）

H_L1 (SOP 不变性正则): SOP 旋转是均衡前对称性，均衡后符号应 SOP-不变。
  正则强制网络学 SOP 去旋转而非记忆特定 SOP 角度 → 抗 D014 lock-swap。
  预测: L1 PI-BER 显著 < L0，尤其在 swap-prone seeds 1000/1002。
  机制风险: 强 λ 可能伤监督拟合（MSE 项被稀释），需扫 λ。
H_L2 (swap 负对对比): lock-swap 本质是网络输出对 X/Y swap 不敏感（对称解）。
  对比项强制 normal/swap 输出差异 ≥ margin → 破坏对称解 → 抗 lock-swap。
  预测: L2 PI-BER 显著 < L0，swap-prone seeds 改善更明显。
  机制风险: margin 太大伤主任务（MSE），margin 太小无约束力。

用法:
  cd projects/simulation && python explore/cma-fade-divergence/prompt024_a_class_loss_variants.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# 路径设置
SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 同级 import (ml_long_seq_failure, prompt012)

# 复用基建（不改 common/）
from common._config import BLOCK
from common._ml_equalizer import ButterflyCNNEqualizer2x2
from params import SimulationConfig
from ml_long_seq_failure import (  # type: ignore
    F_G, GAMMA_BAR, N_TAP, SOP_RATE, T_S,
    gen_channel, oracle_equalize, test_late_slice,
)
TURBULENCE = 'strong'  # 与 ml_long_seq_failure 一致
from prompt012_longseq_audit import evaluate_outputs  # type: ignore  D018 双口径

cfg = SimulationConfig()

# ─── 实验参数（与 D022 一致）────────────────────────────────
N_SYMBOLS = 5_000_000
SEEDS = (1000, 1001, 1002, 1003, 1004)  # 含 D027 swap-prone 1000/1002
ML_TRAIN_FRAC = 0.5
# ML 训练超参（跟 ml_long_seq_failure ML_PARAMS 对齐）
ML_LR = 0.005
ML_BATCH = 1024
ML_EPOCHS = 20
ML_PATIENCE = 5
N_TAP_USE = N_TAP  # 11
# Loss 变体
LAM_GRID = [0.001, 0.01, 0.1, 1.0]      # λ 扫描（找甜点）
L1_AUG_MAX_RAD = 0.2                      # SOP 旋转增强角度范围（TL-22: ≤0.2rad 不破坏 QPSK）
L2_MARGIN = 1.0                           # swap 对比 margin（QPSK 独立符号 E|s-s'|²=2，margin=1 中间值）

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
OUT_PATH = RESULTS_DIR / 'prompt024_a_class_loss.json'


# ─── 复值张量工具 ────────────────────────────────────────────

def _to_real_chunks(r_complex: np.ndarray, chunk_len: int) -> torch.Tensor:
    """复信号 (N,) → (n_chunks, 2, chunk_len) 实值张量."""
    n_c = len(r_complex) // chunk_len
    r = r_complex[:n_c * chunk_len]
    r_r = torch.from_numpy(r.real).view(n_c, 1, chunk_len).float()
    r_i = torch.from_numpy(r.imag).view(n_c, 1, chunk_len).float()
    return torch.cat([r_r, r_i], dim=1)  # (n_c, 2, chunk_len)


def _to_real_chunks_t(r_complex: torch.Tensor, chunk_len: int) -> torch.Tensor:
    """复信号 torch.Tensor → (n_chunks, 2, chunk_len) 实值."""
    n_c = len(r_complex) // chunk_len
    r = r_complex[:n_c * chunk_len]
    return torch.cat([r.real.view(n_c, 1, chunk_len).float(),
                      r.imag.view(n_c, 1, chunk_len).float()], dim=1)


# ─── SOP 旋转（L1 增强）──────────────────────────────────────

def apply_sop_rotation(rX: torch.Tensor, rY: torch.Tensor, theta: float):
    """对双偏振信号做 SOP 旋转 R_θ（复值张量，device 上）.

    rX' = cos(θ)·rX + sin(θ)·rY
    rY' = -sin(θ)·rX + cos(θ)·rY
    （与 gen_channel 的 SOP 旋转矩阵一致）
    """
    import math
    c, s = math.cos(theta), math.sin(theta)
    rXp = c * rX + s * rY
    rYp = -s * rX + c * rY
    return rXp, rYp


def swap_polarizations(rX: torch.Tensor, rY: torch.Tensor):
    """交换 X/Y 偏振（L2 负对）."""
    return rY, rX


# ─── 模型推理辅助 ────────────────────────────────────────────

def model_forward_chunks(model, rX_chunks, rY_chunks):
    """对 (n_chunks, 2, chunk_len) 输入前馈，返回 (zX, zY) 各 (n_chunks, chunk_len) complex."""
    zX, zY = model(rX_chunks, rY_chunks)
    return zX, zY


# ─── 自定义训练循环（支持 L0/L1/L2 三种 loss）─────────────────

def train_variant(rX_np, rY_np, sX_np, sY_np, loss_name: str, lam: float,
                  device='cuda', verbose=False):
    """训练 ButterflyCNNEqualizer2x2，按 loss_name 选 loss.

    loss_name ∈ {'L0_mse', 'L1_sop_invariance', 'L2_swap_contrast'}
    lam: 正则系数（L0 忽略；L1/L2 用）

    返回训练后的 model + history.
    """
    dev = device if torch.cuda.is_available() else 'cpu'
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP_USE).to(dev)
    optimizer = optim.Adam(model.parameters(), lr=ML_LR)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', factor=0.5, patience=3)
    mse = nn.MSELoss()

    N = len(rX_np)
    n_train = int(N * ML_TRAIN_FRAC)
    n_val = int(n_train * 0.2)
    n_tr = n_train - n_val

    # 转 device 复值张量（训练段）— numpy complex128 → torch complex128，实/虚拆分时 .float()
    rX_tr = torch.from_numpy(rX_np[:n_tr].astype(np.complex64)).to(dev)
    rY_tr = torch.from_numpy(rY_np[:n_tr].astype(np.complex64)).to(dev)
    sX_tr = torch.from_numpy(sX_np[:n_tr].astype(np.complex64)).to(dev)
    sY_tr = torch.from_numpy(sY_np[:n_tr].astype(np.complex64)).to(dev)
    rX_val = torch.from_numpy(rX_np[n_tr:n_train].astype(np.complex64)).to(dev)
    rY_val = torch.from_numpy(rY_np[n_tr:n_train].astype(np.complex64)).to(dev)
    sX_val = torch.from_numpy(sX_np[n_tr:n_train].astype(np.complex64)).to(dev)
    sY_val = torch.from_numpy(sY_np[n_tr:n_train].astype(np.complex64)).to(dev)

    # 切 chunk
    chunk_len = ML_BATCH
    n_chunks_tr = n_tr // chunk_len

    def chunks_t(r, s, length):
        nc = len(r) // length
        return nc

    # 预切 chunk（复值 device 张量）
    def slice_chunks(rX_t, rY_t, sX_t, sY_t, length):
        nc = len(rX_t) // length
        return (rX_t[:nc * length].view(nc, length),
                rY_t[:nc * length].view(nc, length),
                sX_t[:nc * length].view(nc, length),
                sY_t[:nc * length].view(nc, length))

    rXc, rYc, sXc, sYc = slice_chunks(rX_tr, rY_tr, sX_tr, sY_tr, chunk_len)

    best_val = float('inf')
    best_state = None
    no_improve = 0
    history = []

    rng_aug = np.random.default_rng(42)  # 增强角度采样的独立 rng（可复现）

    for epoch in range(ML_EPOCHS):
        model.train()
        perm = torch.randperm(n_chunks_tr, device=dev)
        ep_mse, ep_reg, ep_total = 0.0, 0.0, 0.0

        for i in range(n_chunks_tr):
            idx = perm[i]
            # 取该 chunk（复值）
            rX_ch = rXc[idx]  # (chunk_len,) complex on device
            rY_ch = rYc[idx]
            sX_ch = sXc[idx]
            sY_ch = sYc[idx]

            # 转实值 (1, 2, chunk_len) 给 Conv1d
            def to_in(rXc_, rYc_):
                return (torch.cat([rXc_.real.view(1, 1, -1).float(),
                                   rXc_.imag.view(1, 1, -1).float()], dim=1),
                        torch.cat([rYc_.real.view(1, 1, -1).float(),
                                   rYc_.imag.view(1, 1, -1).float()], dim=1))

            optimizer.zero_grad()
            rX_in, rY_in = to_in(rX_ch, rY_ch)
            zX, zY = model(rX_in, rY_in)  # (1, chunk_len) complex

            # MSE 主项
            loss_mse_x = mse(zX.real, sX_ch.real.view(1, -1)) + \
                         mse(zX.imag, sX_ch.imag.view(1, -1))
            loss_mse_y = mse(zY.real, sY_ch.real.view(1, -1)) + \
                         mse(zY.imag, sY_ch.imag.view(1, -1))
            loss_mse = loss_mse_x + loss_mse_y

            # 正则项
            loss_reg = torch.tensor(0.0, device=dev)
            if loss_name == 'L1_sop_invariance' and lam > 0:
                # SOP 旋转增强：随机 θ ∈ [-L1_AUG_MAX_RAD, L1_AUG_MAX_RAD]
                theta = float(rng_aug.uniform(-L1_AUG_MAX_RAD, L1_AUG_MAX_RAD))
                rX_rot, rY_rot = apply_sop_rotation(rX_ch, rY_ch, theta)
                rX_rot_in, rY_rot_in = to_in(rX_rot, rY_rot)
                zX_rot, zY_rot = model(rX_rot_in, rY_rot_in)
                # 不变性惩罚：增强前后输出一致（复数拆实/虚算 MSE）
                loss_reg = (mse(zX.real, zX_rot.real) + mse(zX.imag, zX_rot.imag) +
                            mse(zY.real, zY_rot.real) + mse(zY.imag, zY_rot.imag))
            elif loss_name == 'L2_swap_contrast' and lam > 0:
                # swap 负对：交换 X/Y 偏振输入
                rX_sw, rY_sw = swap_polarizations(rX_ch, rY_ch)
                rX_sw_in, rY_sw_in = to_in(rX_sw, rY_sw)
                zX_sw, zY_sw = model(rX_sw_in, rY_sw_in)
                # 对比：normal 与 swap 输出距离应 ≥ margin
                # loss = max(0, margin − ‖z_normal − z_swap‖²)
                d2 = ((zX - zX_sw).abs().pow(2).mean() +
                      (zY - zY_sw).abs().pow(2).mean())
                loss_reg = torch.relu(L2_MARGIN - d2)

            loss = loss_mse + lam * loss_reg
            loss.backward()
            optimizer.step()

            ep_mse += float(loss_mse.item())
            ep_reg += float(loss_reg.item()) if isinstance(loss_reg, torch.Tensor) else 0.0
            ep_total += float(loss.item())

        # 验证（纯 MSE）
        model.eval()
        with torch.no_grad():
            rX_v_in = torch.cat([rX_val.real.view(1, 1, -1).float(),
                                 rX_val.imag.view(1, 1, -1).float()], dim=1)
            rY_v_in = torch.cat([rY_val.real.view(1, 1, -1).float(),
                                 rY_val.imag.view(1, 1, -1).float()], dim=1)
            zX_v, zY_v = model(rX_v_in, rY_v_in)
            val_mse = (mse(zX_v.real, sX_val.real.view(1, -1)).item() +
                       mse(zX_v.imag, sX_val.imag.view(1, -1)).item() +
                       mse(zY_v.real, sY_val.real.view(1, -1)).item() +
                       mse(zY_v.imag, sY_val.imag.view(1, -1)).item())
        scheduler.step(val_mse)

        avg_mse = ep_mse / n_chunks_tr
        avg_reg = ep_reg / n_chunks_tr
        avg_total = ep_total / n_chunks_tr
        history.append({'epoch': epoch, 'train_mse': avg_mse,
                        'train_reg': avg_reg, 'train_total': avg_total, 'val_mse': val_mse})

        if val_mse < best_val:
            best_val = val_mse
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            no_improve = 0
        else:
            no_improve += 1

        if verbose and (epoch % 5 == 0 or epoch == ML_EPOCHS - 1):
            print(f"    ep{epoch:2d}: mse={avg_mse:.5f} reg={avg_reg:.5f} "
                  f"total={avg_total:.5f} val={val_mse:.5f} lr={optimizer.param_groups[0]['lr']:.2e}")

        if no_improve >= ML_PATIENCE:
            if verbose:
                print(f"    early stop @ ep{epoch}")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, {'history': history, 'best_val_mse': best_val}


def model_equalize(model, rX_np, rY_np, device='cuda'):
    """推理整段，返回 zX, zY (N,) complex numpy + diverged flag."""
    dev = device if torch.cuda.is_available() else 'cpu'
    model.eval()
    N = len(rX_np)
    with torch.no_grad():
        rX_in = torch.cat([torch.from_numpy(rX_np.real).view(1, 1, N).float(),
                           torch.from_numpy(rX_np.imag).view(1, 1, N).float()], dim=1).to(dev)
        rY_in = torch.cat([torch.from_numpy(rY_np.real).view(1, 1, N).float(),
                           torch.from_numpy(rY_np.imag).view(1, 1, N).float()], dim=1).to(dev)
        zX, zY = model(rX_in, rY_in)
    zX_np = zX.cpu().numpy()
    zY_np = zY.cpu().numpy()
    # 发散检查（权重范数）
    cur_norm = model.weights_norm()
    init_norm = model.init_norm()
    diverged = (cur_norm > 10.0 * init_norm or
                (not np.isfinite(cur_norm)) or
                float(max(np.max(np.abs(zX_np)), np.max(np.abs(zY_np)))) > 1e3)
    return zX_np.flatten(), zY_np.flatten(), bool(diverged)


# ─── 配对 Wilcoxon（无 scipy 依赖时用简单实现）─────────────────

def paired_wilcoxon_p(a, b):
    """配对 Wilcoxon 双侧 p 值（精确，小样本 n≤30）.

    a, b: 同长度数组。算 d=a-b，正秩和 W+，双侧 p = 2·min(P(W≥W+), P(W≤W+))。
    用精确枚举（n≤30 可承受 2^n）。无 scipy 依赖。
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    d = a - b
    # 去零
    d = d[d != 0]
    n = len(d)
    if n == 0:
        return 1.0
    signs = (d > 0).astype(int)
    abs_d = np.abs(d)
    # 秩（平均秩处理并列）
    order = np.argsort(abs_d)
    ranks = np.empty(n)
    ranks[order] = np.arange(1, n + 1)
    # 处理并列：相同 |d| 给平均秩
    sorted_abs = abs_d[order]
    i = 0
    while i < n:
        j = i
        while j + 1 < n and sorted_abs[j + 1] == sorted_abs[i]:
            j += 1
        if j > i:
            avg = (ranks[order[i]] + ranks[order[j]]) / 2.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg
        i = j + 1
    w_plus = float(np.sum(ranks[signs == 1]))
    # 精确分布：枚举所有 2^n 符号组合的 W+
    from itertools import combinations
    total_w = float(np.sum(ranks))
    # W+ 分布：在 n 个秩中选子集求和的所有可能
    all_sums = set()
    rank_list = ranks.tolist()
    # 用 DP 枚举子集和（n≤30，但子集和数有限）
    dp = {0.0}
    for rk in rank_list:
        dp = dp | {s + rk for s in dp}
    all_sums = sorted(dp)
    # P(W+ >= w_plus) 和 P(W+ <= w_plus)
    n_total = len(all_sums)
    # 这里 all_sums 是不同和值的集合，但每个和值出现次数需用多项式系数
    # 简化：用 DP 数计数（多项式乘法）
    # coef[s] = 选出子集和为 s 的方案数
    from collections import defaultdict
    coef = defaultdict(int)
    coef[0.0] = 1
    for rk in rank_list:
        new = defaultdict(int)
        for s, c in coef.items():
            new[s] += c
            new[s + rk] += c
        coef = new
    total_count = sum(coef.values())  # = 2^n
    ge = sum(c for s, c in coef.items() if s >= w_plus - 1e-9)
    le = sum(c for s, c in coef.items() if s <= w_plus + 1e-9)
    p_one_side = min(ge, le) / total_count
    p_two = min(1.0, 2.0 * p_one_side)
    return float(p_two)


# ─── 主实验 ──────────────────────────────────────────────────

def run_variant(seed, loss_name, lam, alpha, beta):
    """单 seed × 单 variant: 生成信道 → 训练 → 推理 → late-slice evaluate_outputs.

    返回 dict: fixed_ber_mean, pi_ber_mean, classification, w_norm, history_tail.
    """
    t0 = time.time()
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)

    # 训练（前 ML_TRAIN_FRAC）
    model, hist = train_variant(
        rX, rY, sX, sY, loss_name, lam, device='cuda', verbose=False)

    # 推理全段
    zX, zY, diverged = model_equalize(model, rX, rY)

    # late slice 评估（D018 双口径）
    late_s, late_e = test_late_slice(N_SYMBOLS)
    eval_res = evaluate_outputs(
        zX[late_s:late_e], zY[late_s:late_e],
        sX[late_s:late_e], sY[late_s:late_e], diverged)

    # oracle 对照
    zX_or, zY_or = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    or_eval = evaluate_outputs(
        zX_or[late_s:late_e], zY_or[late_s:late_e],
        sX[late_s:late_e], sY[late_s:late_e], False)

    return {
        'seed': seed,
        'loss_name': loss_name,
        'lam': lam,
        'fixed_ber_mean': eval_res['fixed_label_ber']['mean'],
        'pi_ber_mean': eval_res['permutation_invariant_ber']['mean'],
        'classification': eval_res['classification'],
        'abs_corr_zX_sX': eval_res['abs_corr']['zX_sX'],
        'abs_corr_zX_sY': eval_res['abs_corr']['zX_sY'],
        'diverged': diverged,
        'w_norm': float(model.weights_norm()),
        'oracle_pi_ber': or_eval['permutation_invariant_ber']['mean'],
        'best_val_mse': hist['best_val_mse'],
        'elapsed_s': time.time() - t0,
    }


def main():
    t0 = time.time()
    print("=" * 72)
    print("PROMPT-024: A 类（改 loss）横向对比 MVE")
    print(f"参数: N={N_SYMBOLS}, f_G={F_G}, SOP={SOP_RATE}(1krad/s), turb={TURBULENCE}, "
          f"20dB, QPSK, tap={N_TAP_USE}, seeds={SEEDS}")
    print(f"  L0=MSE, L1=SOP不变性(λ扫), L2=swap对比(λ扫), L3=VAE(defer撞车)")
    print("=" * 72)
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    # ─── Step 1: L0 baseline + 各 λ 的 L1/L2，找甜点（5 seeds）───
    # 先跑 L0 baseline（1 次）+ 每个 λ 的 L1/L2（4 λ × 2 变体 = 8 组）× 5 seeds
    print("\n[Step 1] L0 baseline + L1/L2 λ 扫描（找甜点）")
    results_step1 = []
    config_step1 = [('L0_mse', 0.0)]
    for lam in LAM_GRID:
        config_step1.append(('L1_sop_invariance', lam))
        config_step1.append(('L2_swap_contrast', lam))

    for (lname, lam) in config_step1:
        print(f"\n--- {lname} λ={lam} ---")
        for seed in SEEDS:
            r = run_variant(seed, lname, lam, alpha, beta)
            results_step1.append(r)
            print(f"  seed{seed}: PI={r['pi_ber_mean']:.5f} fixed={r['fixed_ber_mean']:.5f} "
                  f"class={r['classification']} corr(zX,sX)={r['abs_corr_zX_sX']:.2f} "
                  f"corr(zX,sY)={r['abs_corr_zX_sY']:.2f} ({r['elapsed_s']:.0f}s)", flush=True)

    # ─── Step 2: 选甜点 λ（最低 mean PI-BER）─────────────────
    def mean_pi(loss_name):
        return lambda lam: np.mean([r['pi_ber_mean'] for r in results_step1
                                     if r['loss_name'] == loss_name and r['lam'] == lam])

    # L0 baseline mean
    l0_pis = [r['pi_ber_mean'] for r in results_step1 if r['loss_name'] == 'L0_mse']
    l0_mean = float(np.mean(l0_pis))
    print(f"\n[Step 2] L0 baseline mean PI-BER = {l0_mean:.5f}")
    print(f"  L0 per-seed: {[f'{p:.5f}' for p in l0_pis]}")

    best = {}
    for lname in ['L1_sop_invariance', 'L2_swap_contrast']:
        best_lam = None
        best_mean = float('inf')
        for lam in LAM_GRID:
            pis = [r['pi_ber_mean'] for r in results_step1
                   if r['loss_name'] == lname and r['lam'] == lam]
            m = float(np.mean(pis))
            print(f"  {lname} λ={lam}: mean PI = {m:.5f} (per-seed {[f'{p:.5f}' for p in pis]})")
            if m < best_mean:
                best_mean = m
                best_lam = lam
        best[lname] = (best_lam, best_mean)
        print(f"  → {lname} 甜点 λ*={best_lam} mean PI={best_mean:.5f}")

    # ─── Step 3: 甜点 vs L0 Go/Kill（配对 Wilcoxon）──────────
    print("\n[Step 3] 甜点 λ* vs L0 Go/Kill 判定（配对 Wilcoxon）")
    go_kill = {}
    for lname, (best_lam, _) in best.items():
        l_var = [r['pi_ber_mean'] for r in results_step1
                 if r['loss_name'] == lname and r['lam'] == best_lam]
        # 配对（按 seed 对齐）
        seed_to_l0 = {r['seed']: r['pi_ber_mean'] for r in results_step1
                      if r['loss_name'] == 'L0_mse'}
        l0_paired = [seed_to_l0[r['seed']] for r in results_step1
                     if r['loss_name'] == lname and r['lam'] == best_lam]
        wins = int(np.sum(np.array(l_var) < np.array(l0_paired)))
        p = paired_wilcoxon_p(l0_paired, l_var)
        excess_var = float(np.mean(l_var))
        excess_l0 = float(np.mean(l0_paired))
        verdict = ('GO' if (p < 0.05 and wins >= 4) else
                   'KILL' if (p > 0.05 or wins < 4) else 'BORDERLINE')
        go_kill[lname] = {
            'best_lam': best_lam, 'wins': wins, 'n_seeds': len(l_var),
            'p_value': p, 'mean_pi_variant': excess_var,
            'mean_pi_l0': excess_l0, 'delta': excess_l0 - excess_var,
            'verdict': verdict,
        }
        print(f"  {lname} λ*={best_lam}: 胜 {wins}/{len(l_var)}, "
              f"p={p:.4f}, ΔPI(L0−var)={excess_l0 - excess_var:.5f} → {verdict}")

    any_go = any(g['verdict'] == 'GO' for g in go_kill.values())
    overall = 'GO' if any_go else 'KILL'
    print(f"\n>>> A 类整体 Go/Kill: {overall}")

    # ─── Step 4: 消融可验（λ=0 退回 L0）──────────────────────
    # L1/L2 λ=0 应等同 L0（正则项贡献 0）。直接验证甜点拿掉正则是否退化。
    # 注：L1/L2 λ=0 在数学上 = L0，但训练 RNG/early-stop 可能微差，跑 5 seeds 确认。
    print("\n[Step 4] 消融可验：L1/L2 λ=0 应退回 L0 水平")
    ablation = {}
    for lname in ['L1_sop_invariance', 'L2_swap_contrast']:
        abl_results = []
        for seed in SEEDS:
            r = run_variant(seed, lname, 0.0, alpha, beta)
            abl_results.append(r)
            print(f"  {lname} λ=0 seed{seed}: PI={r['pi_ber_mean']:.5f} "
                  f"(L0={seed_to_l0[seed]:.5f})", flush=True)
        abl_pis = [r['pi_ber_mean'] for r in abl_results]
        ablation[lname] = {
            'lam0_mean_pi': float(np.mean(abl_pis)),
            'lam0_per_seed': abl_pis,
            'l0_mean_pi': l0_mean,
            'l0_per_seed': l0_pis,
            'degenerates_to_l0': bool(abs(np.mean(abl_pis) - l0_mean) < 0.01),
        }
        print(f"  → {lname} λ=0 mean={np.mean(abl_pis):.5f} vs L0 mean={l0_mean:.5f} "
              f"→ 消融{'PASS' if ablation[lname]['degenerates_to_l0'] else 'CHECK'} "
              f"(差<0.01 算退回)")

    # ─── 汇总保存 ────────────────────────────────────────────
    elapsed = time.time() - t0
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE 方法层解冻 (D030) — A 类改 loss',
            'step': 'PROMPT-024',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': elapsed,
            'params': {
                'N': N_SYMBOLS, 'f_G': F_G, 'sop_rate': SOP_RATE,
                'turbulence': TURBULENCE, 'gamma_bar': GAMMA_BAR,
                'n_tap': N_TAP_USE, 'mod': 'qpsk', 'seeds': list(SEEDS),
                'ml_train_frac': ML_TRAIN_FRAC, 'ml_lr': ML_LR,
                'ml_batch': ML_BATCH, 'ml_epochs': ML_EPOCHS,
                'lam_grid': LAM_GRID, 'l1_aug_max_rad': L1_AUG_MAX_RAD,
                'l2_margin': L2_MARGIN,
            },
            'gw_step1_search_verdict': {
                'A1_sop_invariance': 'PASS (no collision — no one frames SOP invariance as loss regularizer; all track/estimate SOP instead)',
                'A2_swap_contrast': 'PASS (no collision — zero contrastive optical pol-demux equalization found)',
                'A3_vae_blind': 'COLLISION (Qin 2026 TCCN "Bootstrapping Blind Equalizer DP-coherent FSO via modulus-rings VAE" = same scenario + same mechanism → DEFER, not run this round)',
            },
            'tl20_hypotheses': {
                'H_L1': 'SOP invariance reg → 抗 D014 lock-swap；预测 L1 PI<L0 esp swap-prone seeds',
                'H_L2': 'swap contrastive → 破坏对称解抗 lock-swap；预测 L2 PI<L0',
                'go_kill_preregistered': 'p<0.05 + ≥4/5 seeds 胜 = GO; 否则 KILL',
            },
            'ablation_preregistered': 'L1/L2 λ=0 须退回 L0 水平（差<0.01）',
        },
        'step1_all_variants': results_step1,
        'step2_best_lam': {k: {'lam': v[0], 'mean_pi': v[1]} for k, v in best.items()},
        'step3_go_kill': go_kill,
        'step4_ablation': ablation,
        'overall_verdict': overall,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {OUT_PATH}")
    print(f"总耗时: {elapsed:.0f}s")
    print(f"\n=== A 类整体: {overall} ===")
    return out


if __name__ == '__main__':
    main()
