"""PROMPT-031 (方向 1): E1 群等变神经网络 — 攻 SOP 累积旋转泛化失败

> 方向: S032 机制 E (ML 范式创新) / E1 群等变 CNN | 状态: WIP
> 来源: S033 §F 方法层下一步方向 1（prompt030 坐实 ML N=8M/SOP=1e-6 崩塌=泛化失败）
> 组织规范: ../../SIM-ORG.md

===========================================================================
 TL;DR / 物理假设 (TL-20 理论先行)
===========================================================================
S033 不变量 9：swap 是 SOP 累积旋转的物理现象，ML fixed-weight 在 test late 段
SOP 累积旋转超训练域时泛化失败（D015 Q2 周期性失效带：N=5M late SOP≈57° 崩塌，
N=8M degraded_swap，SOP=1e-6 崩塌更惨）。

【E1 核心机制】：
SOP 旋转群 SO(2) 作用于双偏振信号 (rX, rY)：
  rX' = cos(θ)·rX + sin(θ)·rY
  rY' = -sin(θ)·rX + cos(θ)·rY
等变性要求：f(rX', rY') = R(θ)·f(rX, rY)（输出也旋转 θ）

若网络对 SOP 旋转严格等变，则：
  - 训练时见的小角度旋转不变性 → 架构保证泛化到任意大角度
  - test late SOP 57° 不再崩塌（无需"见过"57°，等变性把训练域外推）
  - 解决 D031 的"训练段 SOP 角度泛化不到 test late 段"痛点

【实现策略 — 约束等变 (regularized equivariance)】：
  - 基础架构：ButterflyCNNEqualizer2x2（D022 L0 baseline, Qin 2025）
  - 训练时每个 batch 做两次前向：
    (1) 原输入 (rX, rY) → 监督 MSE loss（学均衡）
    (2) 随机旋转 θ∈[0, 2π) 的输入 (rX', rY') → 等变一致性 loss
        L_equiv = ‖f(rX', rY') - R(θ)·f(rX, rY)‖²
  - 总 loss = MSE + λ·L_equiv
  - 消融：λ=0 退回 L0（验证等变约束是性能来源, 守 D030 准入 5）

【与 A1（SOP 不变性正则）的区别 — 关键】：
  - A1 (D031 KILL)：训练段加 SOP 不变性正则，但 loss 在训练段施加，训练段 SOP
    漂移远小于 test late 57°，学到的"不变性"泛化不到（D031 时序正交）
  - E1：等变性是**架构级约束**（输入转 θ→输出转 θ），不是训练段 loss 的局部
    正则。等变性一旦在训练域（小 θ）成立，架构保证它在全角度成立（群结构）
  - 但实现上是约束等变（soft），非严格等变（hard, 需群卷积）。soft 是否足够
    须 MVE 实证

PASS 标准 (预注册, 用 fixed-label BER 作 Go 判据 — 不变量 10):
  - E1 late fixed-label BER 显著优于 L0 baseline（ButterflyCNNEqualizer2x2）
    （L0 fixed≈0.5 clean_swap → E1 显著降, 如 < 0.1）
  - 消融可验：λ=0 退回 L0（去掉等变约束性能退）
  - ML SOP 泛化带（D015 Q2）不再周期性失效

FAIL 标准:
  - E1 fixed BER ≈ L0（约束等变不足以打破训练/test 时序正交）
  - 或消融 λ=0 仍同性能（等变约束不是性能来源, 装饰）

===========================================================================
 约束 (硬约束)
===========================================================================
1. strong GG = 4.2/1.4（D022 域）。不硬编码旧 1.5/0.8。
2. swap 分类用 correlation 口径（prompt030 classify_swap，threshold=0.5）。
3. Go 判据用 fixed-label BER。fixed/PI 双口径并报（守 D018）。
4. 隔离原则：不改 common/_ml_equalizer.py，自定义训练循环（复用 prompt024 模式）。
5. λ 扫描 + 消融（守 D030 准入 5 消融可验）。

===========================================================================
 实验设计
===========================================================================
参数域: N=5M, strong (4.2/1.4 动态读), F_G=30, SOP=4e-7, 20dB, QPSK
late [4.375M,5M), seeds 1000-1004（D022 域）

方法网格：
  - L0: ButterflyCNNEqualizer2x2, MSE loss only（D022 baseline）
  - E1 (λ=0.001/0.01/0.1/1.0): L0 + 等变一致性 loss
  - 消融: E1 λ=0（应退回 L0）

度量: late fixed BER, PI BER, swap 分类
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

from common._config import BLOCK
from common._experiment import save_results
from common._ml_equalizer import ButterflyCNNEqualizer2x2
from ml_long_seq_failure import (
    F_G, GAMMA_BAR, N_TAP, SOP_RATE,
    compute_ber_phase_corrected, gen_qpsk, oracle_equalize,
    test_late_slice,
)
from params import SimulationConfig
from prompt030_domain_swap_audit import classify_swap, gen_channel


N_SYMBOLS = 5_000_000
LATE_START, LATE_END = test_late_slice(N_SYMBOLS)
ML_TRAIN_FRAC = 0.5
LR = 0.005
BATCH_SIZE = 1024
N_EPOCHS = 20
PATIENCE = 5
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]
LAMBDAS = [0.0, 0.01, 1.0]  # λ=0 消融 + 中档 + 高档（每档 ~250s, 控制总时长）

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt031_e1_equivariant.json"
)

cfg = SimulationConfig()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def rotate_inputs(rX, rY, theta):
    """SOP 旋转群 SO(2) 作用于双偏振信号 (复值 batch tensor, 保留供参考)."""
    cos_t = torch.cos(theta).unsqueeze(1)
    sin_t = torch.sin(theta).unsqueeze(1)
    rXp = cos_t * rX + sin_t * rY
    rYp = -sin_t * rX + cos_t * rY
    return rXp, rYp


def _to_chunks(r_np, length, dev):
    """复信号 (N,) ndarray → (n_chunks, 2, length) 实值 tensor (跟 MLChannelEqualizer 一致)."""
    n_c = len(r_np) // length
    r = r_np[:n_c * length]
    r_t = torch.from_numpy(r).to(dev)
    r_r = r_t.real.view(n_c, 1, length).float()
    r_i = r_t.imag.view(n_c, 1, length).float()
    return torch.cat([r_r, r_i], dim=1)  # (n_c, 2, length)


def _complex_chunks(r_np, length, dev):
    """复信号 (N,) → (n_chunks, length) 复值 tensor (等变 loss 用)."""
    n_c = len(r_np) // length
    r_t = torch.from_numpy(r_np[:n_c * length]).to(dev)
    return r_t.view(n_c, length)


def rotate_real_chunks(rx_chunk, ry_chunk, theta):
    """SOP 旋转作用于 (B, 2, L) 实值 chunk.

    复旋转 rX' = cos·rX + sin·rY 分别作用于实部和虚部.
    rx_chunk: (B, 2, L) [real, imag]
    theta: (B,) angles
    """
    cos_t = torch.cos(theta).view(-1, 1, 1)  # (B,1,1)
    sin_t = torch.sin(theta).view(-1, 1, 1)
    rxp = cos_t * rx_chunk + sin_t * ry_chunk
    ryp = -sin_t * rx_chunk + cos_t * ry_chunk
    return rxp, ryp


def train_e1(model, rX_train, rY_train, sX_train, sY_train,
             lr=LR, batch_size=BATCH_SIZE, n_epochs=N_EPOCHS,
             lam=0.0, patience=PATIENCE, verbose=False):
    """训练 E1 等变约束 ML 均衡器.

    Loss = MSE(f(rX,rY), s) + λ·‖f(R(θ)·r) - R(θ)·f(r)‖²

    复用 MLChannelEqualizer.train 的 chunk 模式: (1, 2, chunk_len) 实值.
    """
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    n = len(rX_train)
    chunk_len = batch_size
    n_chunks = n // chunk_len

    rX_chunks = _to_chunks(rX_train, chunk_len, device)   # (n_chunks, 2, L) real
    rY_chunks = _to_chunks(rY_train, chunk_len, device)
    sX_chunks = _to_chunks(sX_train, chunk_len, device)
    sY_chunks = _to_chunks(sY_train, chunk_len, device)
    # 复值 chunks 用于等变 loss（方便复数旋转）
    rX_c_chunks = _complex_chunks(rX_train, chunk_len, device)  # (n_chunks, L) complex
    rY_c_chunks = _complex_chunks(rY_train, chunk_len, device)

    criterion = nn.MSELoss()
    best_loss = float('inf')
    best_state = None
    bad = 0
    for ep in range(n_epochs):
        model.train()
        perm = torch.randperm(n_chunks, device=device)
        ep_loss = 0.0
        for i in range(n_chunks):
            idx = perm[i]
            rX_c = rX_chunks[idx:idx+1]  # (1, 2, L)
            rY_c = rY_chunks[idx:idx+1]
            sX_c = sX_chunks[idx:idx+1]
            sY_c = sY_chunks[idx:idx+1]

            opt.zero_grad()
            zX, zY = model(rX_c, rY_c)  # (1, L) complex
            # MSE loss (跟 MLChannelEqualizer 一致: 实/虚分别 MSE)
            loss_x = criterion(zX.real, sX_c[:, 0]) + criterion(zX.imag, sX_c[:, 1])
            loss_y = criterion(zY.real, sY_c[:, 0]) + criterion(zY.imag, sY_c[:, 1])
            mse = loss_x + loss_y

            # 等变一致性 loss（随机 θ）
            if lam > 0:
                theta = torch.rand(1, device=device) * (2 * np.pi)
                rXp, rYp = rotate_real_chunks(rX_c, rY_c, theta)
                zXp_in, zYp_in = model(rXp, rYp)  # f(R(θ)·r)
                # 目标：R(θ)·f(r) — 对当前输出 zX/zY 做复旋转
                cos_t = torch.cos(theta).view(-1, 1)
                sin_t = torch.sin(theta).view(-1, 1)
                zXp_tgt = cos_t * zX.detach() + sin_t * zY.detach()
                zYp_tgt = -sin_t * zX.detach() + cos_t * zY.detach()
                equiv = criterion(zXp_in.real, zXp_tgt.real) + \
                        criterion(zXp_in.imag, zXp_tgt.imag) + \
                        criterion(zYp_in.real, zYp_tgt.real) + \
                        criterion(zYp_in.imag, zYp_tgt.imag)
                loss = mse + lam * equiv
            else:
                loss = mse

            loss.backward()
            opt.step()
            ep_loss += float(loss.item())

        avg = ep_loss / max(n_chunks, 1)
        if verbose:
            print(f"    epoch {ep+1}/{n_epochs} loss={avg:.6f}", flush=True)
        if avg < best_loss - 1e-6:
            best_loss = avg
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            bad = 0
        else:
            bad += 1
            if bad >= patience:
                break
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def run_ml_e1_trial(rX, rY, sX, sY, lam):
    """训练 E1 (给定 λ) + 推理全段 + 返回 zX/zY 全段 (numpy 复值)."""
    n_total = len(rX)
    n_train = int(n_total * ML_TRAIN_FRAC)
    torch.manual_seed(42)  # 训练确定性（D031 同 seed 债务口径）
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model = train_e1(model, rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                     lr=LR, batch_size=BATCH_SIZE, n_epochs=N_EPOCHS,
                     lam=lam, patience=PATIENCE, verbose=False)
    model.eval()
    with torch.no_grad():
        N = n_total
        rX_t = torch.from_numpy(rX).to(device)
        rY_t = torch.from_numpy(rY).to(device)
        # 整段前馈 (1, 2, N) 实值
        rX_chunk = torch.cat([rX_t.real.view(1, 1, N).float(),
                              rX_t.imag.view(1, 1, N).float()], dim=1)
        rY_chunk = torch.cat([rY_t.real.view(1, 1, N).float(),
                              rY_t.imag.view(1, 1, N).float()], dim=1)
        zX, zY = model(rX_chunk, rY_chunk)
        zX_np = zX.cpu().numpy().flatten()
        zY_np = zY.cpu().numpy().flatten()
    return zX_np, zY_np, n_train


def run_trial(seed):
    """单 seed: 跑 L0 + E1 各 λ. 返回 dict."""
    turb = cfg.turbulence.as_dict()
    alpha, beta = turb["strong"]
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)

    sXl = sX[LATE_START:LATE_END]
    sYl = sY[LATE_START:LATE_END]
    h_l = h[LATE_START:LATE_END]
    th_l = theta[LATE_START:LATE_END]

    out = {'seed': seed, 'alpha': alpha, 'beta': beta, 'lambdas': {}}

    # oracle
    zX_or, zY_or = oracle_equalize(
        rX[LATE_START:LATE_END], rY[LATE_START:LATE_END], h_l, th_l, GAMMA_BAR)
    out['oracle'] = {
        'fixed_ber': float(0.5 * (
            compute_ber_phase_corrected(zX_or, sXl)
            + compute_ber_phase_corrected(zY_or, sYl)
        )),
    }

    # L0 + E1 各 λ
    for lam in LAMBDAS:
        tag = 'L0' if lam == 0.0 else f'E1_lam{lam}'
        t1 = time.time()
        zX_ml, zY_ml, _ = run_ml_e1_trial(rX, rY, sX, sY, lam)
        zXl = zX_ml[LATE_START:LATE_END]
        zYl = zY_ml[LATE_START:LATE_END]
        cls = classify_swap(zXl, zYl, sXl, sYl, threshold=0.5)
        fixed = float(0.5 * (
            compute_ber_phase_corrected(zXl, sXl)
            + compute_ber_phase_corrected(zYl, sYl)
        ))
        pi = float(min(
            compute_ber_phase_corrected(zXl, sXl),
            compute_ber_phase_corrected(zXl, sYl),
        ))
        out['lambdas'][tag] = {
            'lam': lam,
            'fixed_ber': fixed,
            'pi_ber': pi,
            'swap_class': cls,
            'runtime_s': round(time.time() - t1, 1),
        }
        print(f"    {tag}: fixed={fixed:.4e} pi={pi:.4e} swap={cls} "
              f"({out['lambdas'][tag]['runtime_s']}s)", flush=True)

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--seeds', default='5')
    args = ap.parse_args()

    seeds = SEEDS_5 if args.seeds == '5' else list(range(1000, 1000 + int(args.seeds)))
    if args.smoke:
        seeds = [1000]

    t0 = time.time()
    trials = []
    for sd in seeds:
        print(f"  seed={sd} ...", flush=True)
        tr = run_trial(sd)
        trials.append(tr)

    # 汇总
    tags = ['L0'] + [f'E1_lam{lam}' for lam in LAMBDAS if lam > 0]
    summary = {}
    for tag in tags:
        fixed_arr = np.array([t['lambdas'][tag]['fixed_ber'] for t in trials])
        pi_arr = np.array([t['lambdas'][tag]['pi_ber'] for t in trials])
        swap_dist = {c: sum(1 for t in trials if t['lambdas'][tag]['swap_class'] == c)
                     for c in ['clean', 'normal', 'clean_swap', 'degraded_swap', 'degraded', 'mixed']}
        summary[tag] = {
            'mean_fixed_ber': float(np.mean(fixed_arr)),
            'mean_pi_ber': float(np.mean(pi_arr)),
            'swap_dist': swap_dist,
            'per_seed_fixed': [float(x) for x in fixed_arr],
        }

    summary['oracle'] = {
        'mean_fixed_ber': float(np.mean([t['oracle']['fixed_ber'] for t in trials])),
    }

    # Go/Kill
    l0_fixed = summary['L0']['mean_fixed_ber']
    best_e1_tag = min([tg for tg in tags if tg != 'L0'],
                      key=lambda t: summary[t]['mean_fixed_ber'])
    best_e1_fixed = summary[best_e1_tag]['mean_fixed_ber']
    improvement = l0_fixed / max(best_e1_fixed, 1e-12)
    summary['go_kill'] = {
        'l0_fixed': float(l0_fixed),
        'best_e1_tag': best_e1_tag,
        'best_e1_fixed': float(best_e1_fixed),
        'improvement': float(improvement),
        'verdict': 'PASS' if best_e1_fixed < 0.1 and improvement > 10 else 'FAIL',
        'criterion': 'E1 best fixed<0.1 且 改善>10× vs L0',
    }

    result = {
        'experiment': 'PROMPT-031 方向1 E1 群等变 NN (攻 SOP 泛化)',
        'hypothesis': 'SOP 旋转等变约束让 ML 泛化到 test late 大角度旋转 (D031 痛点)',
        'invariants': [
            'swap 是 SOP 物理现象 CMA/ML 都 swap (S033 不变量 9)',
            'PI-BER 失明 fixed-label 是真记分牌 (不变量 10)',
            'swap 分类用 correlation 口径 (不用 divergence trigger)',
        ],
        'params': {
            'N': N_SYMBOLS, 'alpha': 'dynamic params.py strong (4.2/1.4)',
            'f_G': F_G, 'sop_rate': SOP_RATE, 'gamma_bar': GAMMA_BAR,
            'late_slice': [LATE_START, LATE_END], 'seeds': seeds,
            'lambdas': LAMBDAS, 'lr': LR, 'batch_size': BATCH_SIZE,
            'n_epochs': N_EPOCHS, 'patience': PATIENCE,
            'equiv_loss': '||f(R(θ)r) - R(θ)f(r)||^2, θ~U[0,2pi)',
        },
        'pass_criterion': 'E1 best fixed<0.1 且 改善>10× vs L0',
        'fail_criterion': 'E1 ≈ L0 (约束等变不足以打破时序正交)',
        'summary': summary,
        'trials': trials,
        'total_runtime_s': round(time.time() - t0, 1),
    }
    save_results(result, RESULT_PATH, script_name="prompt031_e1_equivariant")

    print("\n" + "=" * 80)
    print("E1 群等变 NN — late [4.375M,5M) 各 λ 对比")
    print("=" * 80)
    print(f"{'方法':<14} | {'fixed BER':>12} | {'PI BER':>12} | swap 分布")
    print("-" * 80)
    for tag in tags:
        s = summary[tag]
        sd = s['swap_dist']
        swap_str = f"cs={sd.get('clean_swap',0)} ds={sd.get('degraded_swap',0)} n={sd.get('normal',0)}"
        print(f"{tag:<14} | {s['mean_fixed_ber']:>12.4e} | {s['mean_pi_ber']:>12.4e} | {swap_str}")
    print(f"{'oracle':<14} | {summary['oracle']['mean_fixed_ber']:>12.4e} | {'--':>12} | CSI 下界")
    print("-" * 80)
    g = summary['go_kill']
    print(f"判定: {g['verdict']} (best={g['best_e1_tag']} fixed={g['best_e1_fixed']:.4e}, "
          f"L0={g['l0_fixed']:.4e}, 改善 {g['improvement']:.1f}×)")
    print("=" * 80)
    print(f"结果: {RESULT_PATH} | 总耗时: {result['total_runtime_s']}s")


if __name__ == "__main__":
    main()
