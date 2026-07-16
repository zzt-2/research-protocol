"""PROMPT-033 E2 排列对称破缺网络 — 攻 ML swap 的架构根源 MVE.

> 方向: Q-CMA-FADE 方法层解冻 (D030, 机制 E ML 范式) / 状态: WIP / 创建: 2026-07-16
> 组织规范: ../../SIM-ORG.md (P4 只扩不改 common/; P5 标方向+状态)
> 来源: PROMPT-033 (S033 Tier 1, 主控派出, 方向 1)

## 研究问题

S033 坐实 swap 是 SOP 累积旋转现象。但 prompt032 (D3 MMA) 揭示关键事实分化：
  - standard-CMA (有 z 因子, 盲, 在线更新): 新域 4.2/1.4 下 5/5 **不 swap** (fixed≈2e-4)
  - ML ButterflyCNN (监督, 固定权重): 新域 4.2/1.4 下 5/5 **clean-swap** (fixed≈0.495)
  - current-CMA (无 z 因子, common/_cma.py): 5/5 swap (实现 bug, D020 已知)

→ swap 主要是 **ML 固定权重的泛化失败** (D015 原结论回归), 不是"CMA 也 swap".
→ prompt030/S033 不变量9 "CMA 和 ML 都 swap" 部分是 current-CMA 无 z 因子 bug 的假象
   (standard-CMA 有 z 因子不 swap). 本 MVE 记此债, 但聚焦 E2 本职: 攻 ML swap.

**E2 核心洞察 (本脚本 smoke 验证)**: 标准 ButterflyCNN 蝶形结构
  zX = wxx∗rX + wxy∗rY; zY = wyx∗rX + wyy∗rY
在初始化 (wxx=wyy 中心=1, wxy=wyx=0) 下是**精确排列等变**: 输入 rX/rY 交换 →
输出 zX/zY 精确交换 (smoke 实测 |zX(orig)-zY(swap)|=0.000000).
→ 架构本身对 X/Y swap 不敏感, 这是 swap 盆地等势的架构根源.

## TL-20 假设 (跑前写, 含信息论边界先验)

H_E2 (机制, 主): 打破 ButterflyCNN 的排列对称 (wxx/wyy 独立 + 非对称锚点) →
  网络能区分 X/Y → swap 盆地不等势 → ML swap 率下降, fixed_ber 显著降低.
  预测: E2 fixed_ber < 0.2 (多数 seed 不 swap), L0 fixed_ber ≈ 0.5 (全 swap).
H_info_bound (S032 §B, 强先验): 监督学习有训练标签 (X/Y 不对称参考), 但 test 段
  SOP 旋转超出训练范围时, 固定权重仍可能泛化失败. 排列对称破缺只是必要非充分条件.
  预测: E2 可能降低 swap 率但无法完全消除 (D015 SOP 泛化边界仍在).

预注册 Go/Kill (防事后移门槛, 守铁律 #2 fixed-label BER 作 Go 判据):
  - GO  : E2 mean fixed-label BER 显著低于 L0 (≥4/5 seeds 胜 + 配对 Wilcoxon p<0.05),
          且 E2 mean fixed_ber < 0.2 (实质降 swap)
  - KILL: E2 与 L0 无显著差异 (swap 率相同) → 排列对称破缺不解决 ML swap,
          swap 是 SOP 泛化问题非排列对称问题

## 关键约束 (守纪律)

1. 守 FR-22: GW Step 1 检索完成 (子 agent 报告: 偏振解复用/盲分离攻 swap 场景
   无硬撞车, GO). 邻近 = 音频 BSS 排列等变 (Audioslots arXiv 2305.05591) 非光学;
   Pan 2026 OE (10.1364/oe.582599) 盲 CMA-DNN 仍困 swap 证实空白.
2. 守 D030: 归融可验 (拿掉非对称锚点 λ_asym=0 → 退回 L0 标准 ButterflyCNN).
3. 守 D018: 双口径 fixed/PI 并报 (复用 prompt012 evaluate_outputs).
4. 守铁律 #3: swap 分类用 correlation 口径 (prompt012 evaluate_outputs).
5. 不改 common/: 隔离脚本, E2 非对称网络在本文件内实现, 复用 gen_channel/oracle/
   evaluate_outputs/ml_long_seq_failure 训练超参.
6. 参数域与 prompt024 L0 一致: N=5M/f_G=30/SOP=4e-7/strong(4.2/1.4)/20dB/QPSK,
   seeds 1000-1004 (prompt024 L0 证实 5/5 clean-swap), late [4.375M, 5M).
7. 与提示词1 (E1/CMA+H1, prompt031) 不碰: 本脚本 prompt033, 不碰 prompt031 文件.

## E2 架构: 非对称 ButterflyCNN

标准 ButterflyCNN (_ml_equalizer.py): wxx/wxy/wyx/wyy 各自独立 ComplexFIRConv1d,
但初始化对称 (wxx=wyy 中心1, wxy=wyx=0) + 蝶形结构内在排列等变.

E2 打破对称的两层:
  (a) 结构层: 加一个**非对称锚点头** — zX 和 zY 经过不同的可学习标量门
      gX, gY (初始化 gX=1+ε, gY=1-ε, ε 小正数), 让两路输出有确定性差异.
      这让网络在训练时能"选择"哪路对应 X 哪路对应 Y (监督标签提供方向).
  (b) 损失层: 加 **排列敏感正则** — 强制 ‖f(rX,rY) - swap(f(rY,rX))‖² > margin,
      即正常输入和交换输入的输出要有差异 (打破排列等变性).
      loss = MSE + λ_asym · relu(margin - ‖z_normal - z_swapped‖²)

消融: λ_asym=0 且 gX=gY=1 → 退回 L0 标准 ButterflyCNN (验证退回).

用法:
  cd projects/simulation && python explore/cma-fade-divergence/prompt033_e2_perm_symmetry_break_mve.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from collections import defaultdict

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# 路径设置
SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from params import SimulationConfig
from common._config import BLOCK
from common._ml_equalizer import ComplexFIRConv1d
from ml_long_seq_failure import (  # type: ignore
    F_G, GAMMA_BAR, N_TAP, SOP_RATE, T_S,
    gen_channel, oracle_equalize, test_late_slice,
)
from prompt012_longseq_audit import evaluate_outputs  # type: ignore

cfg = SimulationConfig()

# ─── 实验参数 (与 prompt024 L0 一致) ──────────────────────────
N_SYMBOLS = 5_000_000
TURBULENCE = "strong"   # α=4.2, β=1.4
SEEDS = (1000, 1001, 1002, 1003, 1004)  # prompt024 L0 证实 5/5 clean-swap
LATE_S, LATE_E = test_late_slice(N_SYMBOLS)
ML_TRAIN_FRAC = 0.5
ML_LR = 0.005
ML_BATCH = 1024
ML_EPOCHS = 20
ML_PATIENCE = 5
N_TAP_USE = N_TAP  # 11

# E2 超参
LAM_ASYM_GRID = [0.01, 0.1, 1.0]   # 排列敏感正则系数 (找甜点)
ASYM_MARGIN = 1.0                   # 排列差异 margin (QPSK 独立符号 E|s-s'|²=2, margin=1 中间)
ASYM_EPS = 0.1                      # 非对称锚点初始偏置 (gX=1+ε, gY=1-ε)

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
OUT_PATH = RESULTS_DIR / 'prompt033_e2_perm_symmetry_break.json'


# ─── E2 非对称 ButterflyCNN ──────────────────────────────────

class AsymButterflyCNN2x2(nn.Module):
    """非对称 ButterflyCNN: 标准 4 复 FIR 蝶形 + 非对称输出门.

    打破排列等变: (a) gX/gY 非对称可学习标量门 (初始化 1±ε);
                  (b) 结构与标准 ButterflyCNN 相同 (wxx/wxy/wyx/wyy 独立 ComplexFIRConv1d).
    排列等变破缺靠 gX≠gY + 排列敏感正则 (训练时施加).

    消融: asym=False 时 gX=gY=1 (退回标准 ButterflyCNN), 复用同一架构.
    """

    def __init__(self, n_tap=11, asym=True, eps=0.1):
        super().__init__()
        self.n_tap = n_tap
        self.asym = asym
        self.wxx = ComplexFIRConv1d(n_tap)
        self.wxy = ComplexFIRConv1d(n_tap)
        self.wyx = ComplexFIRConv1d(n_tap)
        self.wyy = ComplexFIRConv1d(n_tap)
        # 非对称输出门 (可学习标量). asym=False → gX=gY=1 (锁定, 退回标准).
        if asym:
            self.gX_real = nn.Parameter(torch.tensor(1.0 + eps))
            self.gX_imag = nn.Parameter(torch.tensor(0.0))
            self.gY_real = nn.Parameter(torch.tensor(1.0 - eps))
            self.gY_imag = nn.Parameter(torch.tensor(0.0))
        else:
            self.register_buffer('gX_real', torch.tensor(1.0))
            self.register_buffer('gX_imag', torch.tensor(0.0))
            self.register_buffer('gY_real', torch.tensor(1.0))
            self.register_buffer('gY_imag', torch.tensor(0.0))

    def _gate(self, z_r, z_i, gr, gi):
        """复数门: (gr+j·gi)·(z_r+j·z_i) = (gr·z_r - gi·z_i) + j·(gr·z_i + gi·z_r)."""
        return gr * z_r - gi * z_i, gr * z_i + gi * z_r

    def _butterfly(self, rX_r, rX_i, rY_r, rY_i):
        """蝶形: zX = wxx∗rX + wxy∗rY; zY = wyx∗rX + wyy∗rY (复 FIR)."""
        zX_r_xx, zX_i_xx = self.wxx(rX_r, rX_i)
        zX_r_xy, zX_i_xy = self.wxy(rY_r, rY_i)
        zX_r = zX_r_xx + zX_r_xy
        zX_i = zX_i_xx + zX_i_xy
        zY_r_yx, zY_i_yx = self.wyx(rX_r, rX_i)
        zY_r_yy, zY_i_yy = self.wyy(rY_r, rY_i)
        zY_r = zY_r_yx + zY_r_yy
        zY_i = zY_i_yx + zY_i_yy
        return zX_r, zX_i, zY_r, zY_i

    def forward(self, rX, rY):
        """rX/rY: (B, 2, N) 实值 [real; imag] → (zX, zY) (B, N) complex."""
        rX_r = rX[:, 0:1].float()
        rX_i = rX[:, 1:2].float()
        rY_r = rY[:, 0:1].float()
        rY_i = rY[:, 1:2].float()
        zX_r, zX_i, zY_r, zY_i = self._butterfly(rX_r, rX_i, rY_r, rY_i)
        # 非对称门
        zX_r, zX_i = self._gate(zX_r, zX_i, self.gX_real, self.gX_imag)
        zY_r, zY_i = self._gate(zY_r, zY_i, self.gY_real, self.gY_imag)
        zX = torch.complex(zX_r.squeeze(1), zX_i.squeeze(1))
        zY = torch.complex(zY_r.squeeze(1), zY_i.squeeze(1))
        return zX, zY

    def weights_norm(self):
        with torch.no_grad():
            total = 0.0
            for fir in [self.wxx, self.wxy, self.wyx, self.wyy]:
                for conv in [fir.conv_RR, fir.conv_RI]:
                    total += float(torch.sum(conv.weight ** 2))
            return float(np.sqrt(total))

    def init_norm(self):
        return float(np.sqrt(2.0))


# ─── 训练 (支持 L0/E2 两种 loss) ──────────────────────────────

def train_variant(rX_np, rY_np, sX_np, sY_np, loss_name, lam,
                  device='cuda', verbose=False):
    """训练 AsymButterflyCNN2x2, 按 loss_name 选 loss.

    loss_name ∈ {'L0_mse', 'E2_asym'}.
      L0: asym=False (标准 ButterflyCNN) + 纯 MSE.
      E2: asym=True + MSE + λ·排列敏感正则 (输入交换前后输出差异 ≥ margin).
    """
    dev = device if torch.cuda.is_available() else 'cpu'
    asym = (loss_name == 'E2_asym')
    model = AsymButterflyCNN2x2(n_tap=N_TAP_USE, asym=asym, eps=ASYM_EPS).to(dev)
    optimizer = optim.Adam(model.parameters(), lr=ML_LR)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', factor=0.5, patience=3)
    mse = nn.MSELoss()

    N = len(rX_np)
    n_train = int(N * ML_TRAIN_FRAC)
    n_val = int(n_train * 0.2)
    n_tr = n_train - n_val

    rX_tr = torch.from_numpy(rX_np[:n_tr].astype(np.complex64)).to(dev)
    rY_tr = torch.from_numpy(rY_np[:n_tr].astype(np.complex64)).to(dev)
    sX_tr = torch.from_numpy(sX_np[:n_tr].astype(np.complex64)).to(dev)
    sY_tr = torch.from_numpy(sY_np[:n_tr].astype(np.complex64)).to(dev)
    rX_val = torch.from_numpy(rX_np[n_tr:n_train].astype(np.complex64)).to(dev)
    rY_val = torch.from_numpy(rY_np[n_tr:n_train].astype(np.complex64)).to(dev)
    sX_val = torch.from_numpy(sX_np[n_tr:n_train].astype(np.complex64)).to(dev)
    sY_val = torch.from_numpy(sY_np[n_tr:n_train].astype(np.complex64)).to(dev)

    chunk_len = ML_BATCH
    n_chunks_tr = n_tr // chunk_len

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

    for epoch in range(ML_EPOCHS):
        model.train()
        perm = torch.randperm(n_chunks_tr, device=dev)
        ep_mse, ep_reg, ep_total = 0.0, 0.0, 0.0

        for i in range(n_chunks_tr):
            idx = perm[i]
            rX_ch = rXc[idx]; rY_ch = rYc[idx]
            sX_ch = sXc[idx]; sY_ch = sYc[idx]

            def to_in(rXc_, rYc_):
                return (torch.cat([rXc_.real.view(1, 1, -1).float(),
                                   rXc_.imag.view(1, 1, -1).float()], dim=1),
                        torch.cat([rYc_.real.view(1, 1, -1).float(),
                                   rYc_.imag.view(1, 1, -1).float()], dim=1))

            optimizer.zero_grad()
            rX_in, rY_in = to_in(rX_ch, rY_ch)
            zX, zY = model(rX_in, rY_in)

            loss_mse_x = mse(zX.real, sX_ch.real.view(1, -1)) + \
                         mse(zX.imag, sX_ch.imag.view(1, -1))
            loss_mse_y = mse(zY.real, sY_ch.real.view(1, -1)) + \
                         mse(zY.imag, sY_ch.imag.view(1, -1))
            loss_mse = loss_mse_x + loss_mse_y

            # 默认无正则 (CPU scalar, 避免 GPU tensor 累积致 illegal memory access, D019 同类问题)
            loss_reg_val = 0.0
            if loss_name == 'E2_asym' and lam > 0:
                # 排列敏感正则: 输入交换, 输出应有差异
                rX_sw_in, rY_sw_in = to_in(rY_ch, rX_ch)  # 交换输入
                zX_sw, zY_sw = model(rX_sw_in, rY_sw_in)
                # ‖z_normal - z_swapped‖² 应 > margin (打破排列等变)
                d2 = ((zX - zX_sw).abs().pow(2).mean() +
                      (zY - zY_sw).abs().pow(2).mean())
                loss_reg = torch.relu(ASYM_MARGIN - d2)
                loss_reg_val = float(loss_reg.item()) if loss_reg.requires_grad else loss_reg

            loss = loss_mse + lam * (loss_reg if loss_name == 'E2_asym' and lam > 0 else 0.0)
            loss.backward()
            optimizer.step()

            ep_mse += float(loss_mse.item())
            ep_reg += loss_reg_val
            ep_total += float(loss.item())

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
                  f"total={avg_total:.5f} val={val_mse:.5f}")

        if no_improve >= ML_PATIENCE:
            if verbose:
                print(f"    early stop @ ep{epoch}")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, {'history': history, 'best_val_mse': best_val}


def model_equalize(model, rX_np, rY_np, device='cuda'):
    """推理整段, 返回 zX, zY (N,) complex numpy + diverged flag."""
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
    cur_norm = model.weights_norm()
    init_norm = model.init_norm()
    diverged = (cur_norm > 10.0 * init_norm or
                (not np.isfinite(cur_norm)) or
                float(max(np.max(np.abs(zX_np)), np.max(np.abs(zY_np)))) > 1e3)
    return zX_np.flatten(), zY_np.flatten(), bool(diverged)


# ─── 配对 Wilcoxon (复用 prompt024/prompt032 实现) ─────────────

def paired_wilcoxon_p(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    d = a - b
    d = d[d != 0]
    n = len(d)
    if n == 0:
        return 1.0
    signs = (d > 0).astype(int)
    abs_d = np.abs(d)
    order = np.argsort(abs_d)
    ranks = np.empty(n)
    ranks[order] = np.arange(1, n + 1)
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
    rank_list = ranks.tolist()
    coef = defaultdict(int)
    coef[0.0] = 1
    for rk in rank_list:
        new = defaultdict(int)
        for s, c in coef.items():
            new[s] += c
            new[s + rk] += c
        coef = new
    total_count = sum(coef.values())
    ge = sum(c for s, c in coef.items() if s >= w_plus - 1e-9)
    le = sum(c for s, c in coef.items() if s <= w_plus + 1e-9)
    p_one_side = min(ge, le) / total_count
    return float(min(1.0, 2.0 * p_one_side))


# ─── 单 seed × 单 variant ────────────────────────────────────

def run_variant(seed, loss_name, lam, alpha, beta):
    t0 = time.time()
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)
    model, hist = train_variant(rX, rY, sX, sY, loss_name, lam, device='cuda', verbose=False)
    zX, zY, diverged = model_equalize(model, rX, rY)
    w_norm = float(model.weights_norm())
    eval_res = evaluate_outputs(
        zX[LATE_S:LATE_E], zY[LATE_S:LATE_E],
        sX[LATE_S:LATE_E], sY[LATE_S:LATE_E], diverged)
    zX_or, zY_or = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    or_eval = evaluate_outputs(
        zX_or[LATE_S:LATE_E], zY_or[LATE_S:LATE_E],
        sX[LATE_S:LATE_E], sY[LATE_S:LATE_E], False)
    # 显式释放显存 (防 D019 同类 illegal memory access: 连续训练多模型累积)
    del model, zX, zY, zX_or, zY_or
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return {
        'seed': seed, 'loss_name': loss_name, 'lam': lam,
        'fixed_ber_mean': eval_res['fixed_label_ber']['mean'],
        'pi_ber_mean': eval_res['permutation_invariant_ber']['mean'],
        'classification': eval_res['classification'],
        'abs_corr_zX_sX': eval_res['abs_corr']['zX_sX'],
        'abs_corr_zX_sY': eval_res['abs_corr']['zX_sY'],
        'diverged': diverged,
        'w_norm': w_norm,
        'oracle_pi_ber': or_eval['permutation_invariant_ber']['mean'],
        'oracle_fixed_ber': or_eval['fixed_label_ber']['mean'],
        'best_val_mse': hist['best_val_mse'],
        'elapsed_s': time.time() - t0,
    }


def _save(payload, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)


CKPT_PATH = RESULTS_DIR / 'prompt033_ckpt.json'


def main():
    t0 = time.time()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    print("=" * 78)
    print("PROMPT-033: E2 排列对称破缺网络 — 攻 ML swap 架构根源 MVE")
    print(f"参数: N={N_SYMBOLS}, f_G={F_G}, SOP={SOP_RATE}(1krad/s), turb={TURBULENCE} "
          f"(α={alpha},β={beta}), 20dB, QPSK, tap={N_TAP_USE}")
    print(f"  L0=标准ButterflyCNN(排列等变, prompt024证实5/5 swap), E2=非对称锚点+排列敏感正则")
    print(f"  seeds={SEEDS}, λ_grid={LAM_ASYM_GRID}, late=[{LATE_S},{LATE_E})")
    print("=" * 78)

    # 加载 checkpoint (断点续跑)
    config_list = [('L0_mse', 0.0)]
    for lam in LAM_ASYM_GRID:
        config_list.append(('E2_asym', lam))

    if CKPT_PATH.exists():
        with open(CKPT_PATH, 'r', encoding='utf-8') as f:
            ckpt = json.load(f)
        results = ckpt.get('results', [])
        done = {(r['loss_name'], r['lam'], r['seed']) for r in results}
        print(f"[checkpoint] 已完成 {len(results)} runs, 续跑剩余")
    else:
        results = []
        done = set()

    # ── Step 1: L0 baseline + E2 λ 扫描 (支持断点续跑) ──
    print("\n[Step 1] L0 baseline + E2 λ 扫描")
    for (lname, lam) in config_list:
        print(f"\n--- {lname} λ={lam} ---")
        for seed in SEEDS:
            key = (lname, lam, seed)
            if key in done:
                r = next(x for x in results if (x['loss_name'], x['lam'], x['seed']) == key)
                print(f"  seed{seed}: (cached) fixed={r['fixed_ber_mean']:.4f}", flush=True)
                continue
            r = run_variant(seed, lname, lam, alpha, beta)
            results.append(r)
            done.add(key)
            # 每 run 存 checkpoint
            _save({'results': results}, CKPT_PATH)
            print(f"  seed{seed}: fixed={r['fixed_ber_mean']:.4f} pi={r['pi_ber_mean']:.5f} "
                  f"class={r['classification']} corr(zX,sX)={r['abs_corr_zX_sX']:.2f} "
                  f"corr(zX,sY)={r['abs_corr_zX_sY']:.2f} ({r['elapsed_s']:.0f}s)", flush=True)

    # ── Step 2: 选甜点 λ ──
    l0_pis = [r['pi_ber_mean'] for r in results if r['loss_name'] == 'L0_mse']
    l0_fixed = [r['fixed_ber_mean'] for r in results if r['loss_name'] == 'L0_mse']
    l0_mean_pi = float(np.mean(l0_pis))
    l0_mean_fixed = float(np.mean(l0_fixed))
    print(f"\n[Step 2] L0 baseline: mean fixed={l0_mean_fixed:.4f} mean PI={l0_mean_pi:.5f}")
    print(f"  L0 per-seed fixed: {[f'{x:.4f}' for x in l0_fixed]}")

    best = {}
    for lname in ['E2_asym']:
        best_lam = None
        best_mean = float('inf')
        for lam in LAM_ASYM_GRID:
            fixed = [r['fixed_ber_mean'] for r in results
                     if r['loss_name'] == lname and r['lam'] == lam]
            m = float(np.mean(fixed))  # 按 fixed-label BER 选甜点 (铁律#2)
            print(f"  {lname} λ={lam}: mean fixed={m:.4f} (per-seed {[f'{x:.4f}' for x in fixed]})")
            if m < best_mean:
                best_mean = m
                best_lam = lam
        best[lname] = (best_lam, best_mean)
        print(f"  → {lname} 甜点 λ*={best_lam} mean fixed={best_mean:.4f}")

    # ── Step 3: 甜点 vs L0 Go/Kill (fixed-label BER) ──
    print("\n[Step 3] 甜点 λ* vs L0 Go/Kill 判定 (fixed-label BER)")
    go_kill = {}
    for lname, (best_lam, _) in best.items():
        e2_fixed = [r['fixed_ber_mean'] for r in results
                    if r['loss_name'] == lname and r['lam'] == best_lam]
        seed_to_l0 = {r['seed']: r['fixed_ber_mean'] for r in results
                      if r['loss_name'] == 'L0_mse'}
        l0_paired = [seed_to_l0[r['seed']] for r in results
                     if r['loss_name'] == lname and r['lam'] == best_lam]
        wins = int(np.sum(np.array(e2_fixed) < np.array(l0_paired)))
        p = paired_wilcoxon_p(l0_paired, e2_fixed)
        e2_mean = float(np.mean(e2_fixed))
        verdict = ('GO' if (p < 0.05 and wins >= 4 and e2_mean < 0.2)
                   else 'KILL')
        e2_swap = sum(1 for r in results if r['loss_name'] == lname and r['lam'] == best_lam
                      and 'swap' in r['classification'])
        l0_swap = sum(1 for r in results if r['loss_name'] == 'L0_mse'
                      and 'swap' in r['classification'])
        go_kill[lname] = {
            'best_lam': best_lam, 'wins': wins, 'n_seeds': len(e2_fixed),
            'p_value': p, 'mean_fixed_variant': e2_mean,
            'mean_fixed_l0': l0_mean_fixed,
            'delta_fixed': l0_mean_fixed - e2_mean,
            'e2_swap_count': e2_swap, 'l0_swap_count': l0_swap,
            'verdict': verdict,
        }
        print(f"  {lname} λ*={best_lam}: 胜 {wins}/{len(e2_fixed)} (fixed), p={p:.4f}, "
              f"E2 mean fixed={e2_mean:.4f} (swap {e2_swap}/{len(e2_fixed)}) vs "
              f"L0 mean fixed={l0_mean_fixed:.4f} (swap {l0_swap}/{len(e2_fixed)}) → {verdict}")

    overall = 'GO' if any(g['verdict'] == 'GO' for g in go_kill.values()) else 'KILL'

    # ── Step 4: 消融可验 (E2 λ=0 + asym=False 应退回 L0) ──
    print("\n[Step 4] 消融: E2 λ=0 应退回 L0 水平")
    ablation = {}
    abl_results = [r for r in results if r['loss_name'] == 'E2_asym' and r['lam'] == 0.0]
    for seed in SEEDS:
        if any(r['seed'] == seed for r in abl_results):
            r = next(x for x in abl_results if x['seed'] == seed)
            print(f"  E2 λ=0 seed{seed}: (cached) fixed={r['fixed_ber_mean']:.4f} "
                  f"(L0={seed_to_l0[seed]:.4f})", flush=True)
            continue
        r = run_variant(seed, 'E2_asym', 0.0, alpha, beta)
        abl_results.append(r)
        results.append(r)
        _save({'results': results}, CKPT_PATH)
        print(f"  E2 λ=0 seed{seed}: fixed={r['fixed_ber_mean']:.4f} "
              f"(L0={seed_to_l0[seed]:.4f})", flush=True)
    abl_fixed = [r['fixed_ber_mean'] for r in abl_results]
    # E2 λ=0 仍有 asym 锚点 (gX≠gY), 但无排列正则. 检查是否接近 L0.
    ablation['lam0_mean_fixed'] = float(np.mean(abl_fixed))
    ablation['lam0_per_seed'] = abl_fixed
    ablation['l0_mean_fixed'] = l0_mean_fixed
    ablation['l0_per_seed'] = l0_fixed
    ablation['degenerates_to_l0'] = bool(abs(np.mean(abl_fixed) - l0_mean_fixed) < 0.1)
    print(f"  → E2 λ=0 mean={np.mean(abl_fixed):.4f} vs L0 mean={l0_mean_fixed:.4f} "
          f"→ 消融{'PASS' if ablation['degenerates_to_l0'] else 'CHECK (锚点单独有效果)'}")

    elapsed = time.time() - t0
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE 方法层解冻 (D030) — E2 排列对称破缺 (机制 E ML)',
            'step': 'PROMPT-033',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': elapsed,
            'params': {
                'N': N_SYMBOLS, 'f_G': F_G, 'sop_rate': SOP_RATE,
                'turbulence': TURBULENCE, 'alpha': alpha, 'beta': beta,
                'gamma_bar': GAMMA_BAR, 'n_tap': N_TAP_USE, 'mod': 'qpsk',
                'seeds': list(SEEDS), 'ml_train_frac': ML_TRAIN_FRAC,
                'ml_lr': ML_LR, 'ml_batch': ML_BATCH, 'ml_epochs': ML_EPOCHS,
                'lam_asym_grid': LAM_ASYM_GRID, 'asym_margin': ASYM_MARGIN,
                'asym_eps': ASYM_EPS, 'late_slice': [LATE_S, LATE_E],
            },
            'gw_step1_search_verdict': (
                'GO (子 agent 报告: 偏振解复用/盲分离攻 swap 场景无硬撞车). 邻近=音频BSS '
                '排列等变 (Audioslots arXiv 2305.05591) 非光学; Pan 2026 OE '
                '(10.1364/oe.582599) 盲 CMA-DNN 仍困 swap 证实空白.'),
            'tl20_hypotheses': {
                'H_E2': '打破ButterflyCNN排列对称(非对称锚点+排列敏感正则) → swap盆地不等势 → fixed_ber<0.2',
                'H_info_bound': '监督标签是X/Y不对称参考, 但test段SOP超出训练范围时固定权重仍可能泛化失败 (强先验)',
                'go_kill_preregistered': 'GO: E2 mean fixed<L0, ≥4/5胜 p<0.05, 且mean<0.2; 否则KILL',
                'key_finding_from_prompt032': 'standard-CMA(有z)新域0/5 swap vs ML 5/5 swap → swap主要是ML固定权重泛化失败非CMA也swap',
            },
            'ablation_preregistered': 'E2 λ=0 应退回接近 L0 (差<0.1); 若锚点单独有效果则记CHECK',
        },
        'step1_all_variants': results,
        'step2_best_lam': {k: {'lam': v[0], 'mean_fixed': v[1]} for k, v in best.items()},
        'step3_go_kill': go_kill,
        'step4_ablation': ablation,
        'overall_verdict': overall,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {OUT_PATH}")
    print(f"总耗时: {elapsed:.0f}s")
    print(f"\n=== E2 排列对称破缺整体: {overall} ===")
    return out


if __name__ == '__main__':
    main()
