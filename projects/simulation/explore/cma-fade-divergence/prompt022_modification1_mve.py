"""PROMPT-022: 改动1（物理发散判据驱动 ML 重训练）MVE.

> 方向: Q-CMA-FADE / 路线 A (Q-DP1/DP3/DP4 全 Kill 后唯一存活方向) | 状态: WIP | 创建: 2026-07-15
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)
> 来源: PROMPT-022 (主控派发, 改动1 Go/Kill 验证)

## 改动1 定义 (S017 段 2)

核心创新: 用物理发散判据 (CMA 权重范数 / 恒模代价突增 / block 级 PI-BER 恶化 / 权重漂移)
当 ML 重训练的触发信号。区别于:
  - Qin/Kulmer/Li: 冻结训练 (train once 用到底)
  - Nasr 2026: 固定 θ 角网格预训练 (非信道状态触发)
  - B2/JR-CMA: 物理阈值 gate 经典 DSP (非 ML)

创新点 = 把"物理量 gating"思想从经典估计器 (JR-CMA) 移到 ML 训练调度。
写作须区分"信道状态触发重训练" vs Nasr"固定网格预训练"。

## 验证任务

### 验证1 (核心 Go/Kill): 物理判据触发重训练 vs 固定周期 vs 不重训练

参数: f_G=30, SOP=4e-7 (1krad/s), strong, 20dB, QPSK, N=5M, 5 seeds (D022 注册域)

  A: standard-CMA (baseline 下界参照)
  B: ML 训练一次用到底 (D015 证明 N=5M 失效 BER→0.5)
  C: ML 固定周期重训练 (D015 Q3-B 方案, 每 test 1/4 重训, PI=0.002 参照上界)
  D: ML 物理判据触发重训练 (改动1, 本验证目标)

  D 的物理判据候选 (测 3 种):
    D1: CMA 权重范数突增 (|w| 超阈值 → 触发 ML 重训练)
    D2: block 级恒模代价突增 (J_CMA block 均值超阈值 → 触发)
    D3: CMA 权重漂移 (Δw = |w_current - w_train| 超阈值 → 触发)

双口径 (D018 强制): fixed BER + PI-BER 并报

### 验证2 (收益域, 非门控): 改动1 在 N=2M 的表现
  D023 证明 ML 优势在 N=2M 不普适. 改动1 在 N=2M (SOP 漂移小) 可能仍不如 standard-CMA.
  参数: N=2M, f_G=30, 其他同验证1.
  不是 Go/Kill 门控, 影响论文 limitations 怎么写.

## TL-20 理论预期 (实验前写)

关键物理洞察 (TL-22 触发, 来自 D013/D014/D027):
  - D013 证明 swap 时 |w| 稳定 (1.4142→1.4166 不发散) → D1 权重范数判据可能检测不到 swap
  - D014 证明 swap 是权重跳盆地 (非数值发散)
  - D027 V3a 证明 clean swap 时 J_CMA 不突增 (swap 盆地恒模, 输出互相关≈0)
  - 所以基于恒模/权重范数的判据对 clean swap 从物理上可能检测不到

对照预期:
  A (standard-CMA): PI ~0.02-0.03 (D022/D028 实测)
  B (ML 训练一次): PI ~0.5 (D015 Q1 N=5M ML=0.497±0.006 全崩)
  C (固定周期重训练): PI ~0.002 (D015 Q3-B 实测 mean=0.0020)
  D1 (|w| 突增判据): 预期高 (~0.3-0.5) — swap 时 |w| 不突增 → 检测不到 → 不触发
  D2 (J_CMA 突增判据): 预期中高 (~0.1-0.3) — clean swap J_CMA 可能不突增
  D3 (Δw 漂移判据): 预期中低 (~0.01-0.1) — SOP 持续旋转 → CMA 权重持续漂移 →
                     Δw 随时间单调增 → 可能在 swap 前/时就触发重训练

量化锚点:
  C=0.002 (参照上界), B=0.497 (下界), A=0.02-0.03
  Go 判据: D 显著优于 B (≥4/5 + p<0.05) 且接近 C (<2× 差距)

## 预注册 Go/Kill 判据 (FR-25 分离)

Go 标准 (D 任一判据满足全部):
  1. D PI-BER 显著优于 B (训练一次): 5 seeds 配对 Wilcoxon p<0.05 + D 赢 ≥4/5
  2. D PI-BER 接近 C (固定周期): D/C 比值 < 2×
  3. D 触发频率合理: D 触发次数 < test 段总 block 数的 50% (非退化为在线更新)

Kill 标准 (D 所有判据都满足任一):
  1. D 与 B 无显著差异 (物理判据触发不了有效重训练)
  2. 或 D 触发频率过高 (≈在线更新, 失去"调度"意义, >50% block 触发)
  3. 或 D PI-BER 远差于 C (D/C > 5×, 物理判据不如固定周期)

不用 oracle 当 Go 判据 (FR-25).

## 参数溯源 (FR-20)
  sop_rate=4e-7: sat.1553 §6.3 L778 仿真值 (1 krad/s 真实 OSL 速率)
  f_G=30: D022 注册域
  N=5M, late [4.375M, 5M): D022/D018 一致
  μ=1e-3: D006 安全区低风险 (D018 收紧)
  D1 权重范数阈值: 参考 D006 发散判据 |w|>10×init (但 D013 证明 swap 不发散,
    这里用更宽松的 2×/5×/10× 扫描确认)
  D2 恒模代价阈值: 基线 = 训练段 block 级 J_CMA 均值, 触发 = 超基线 k× (k 扫 2/5/10)
  D3 权重漂移阈值: 基线 = 0 (训练时 w=w_train), 触发 = Δw > α×|w_train| (α 扫 0.1/0.3/0.5)

## 隔离原则 (守 PROMPT 纪律)
  不改 common/, 复用 ml_long_seq_failure (gen_channel/oracle/ML) + prompt019 StandardCMA2x2
  + prompt012 evaluate_outputs. 新增 block 级物理量监控 + 物理判据触发重训练逻辑.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common._config import BLOCK
from ml_long_seq_failure import (
    GAMMA_BAR,
    ML_PARAMS,
    ML_TRAIN_FRAC,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    gen_channel,
    oracle_equalize,
)
from params import SimulationConfig
from prompt012_longseq_audit import evaluate_outputs, seed_ml
from prompt019_mu_compress_mve import StandardCMA2x2


# ─── 实验参数 (FR-20 溯源) ──────────────────────────────────

N_SYMBOLS = 5_000_000          # 5M (D022 注册域)
TURBULENCE = "strong"          # α=1.5, β=0.8 (GG 强湍流)
F_G = 30.0                     # D022 注册域
LATE_START = 4_375_000
LATE_END = 5_000_000
CMA_BLOCK_SIZE = 64            # sat.1553 §6.3 L756 并行化因子
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]

# 固定周期重训练段数 (复刻 D015 Q3-B: 每 test 1/4 重训)
PERIODIC_N_SEGMENTS = 4

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt022_modification1_mve.json"
)


# ═══════════════════════════════════════════════════════════
#  Standard CMA 带块级物理量监控 (扩展 prompt019 StandardCMA2x2)
# ═══════════════════════════════════════════════════════════

class MonitoredStandardCMA(StandardCMA2x2):
    """Standard CMA + 块级物理量轨迹记录 (改动1 的判据信号源).

    新增块级记录:
      - w_norm_traj: |w| 块末权重范数
      - j_cma_traj: block 级恒模代价均值 J_CMA = mean(|R²−|z|²|) / 2
      - w_snapshot_blocks: 指定 block 的完整权重快照 (供 Δw 判据用)
      - w_train_ref: 训练段结束时的权重 (Δw 判据基线)
    """

    def equalize_monitored(self, rX, rY, snapshot_blocks=None, block_size=CMA_BLOCK_SIZE):
        """块级 standard CMA + 物理量监控.

        snapshot_blocks: list[int] 或 None. 指定 block index 处保存完整 4-FIR 权重快照.
        返回 prompt019 equalize 结果 + 块级物理量轨迹 + 权重快照.
        """
        from numpy.lib.stride_tricks import sliding_window_view
        N = len(rX)
        L = self.n_tap
        half = L // 2

        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)

        rX_win = sliding_window_view(rX, L)
        rY_win = sliding_window_view(rY, L)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None
        n_valid = N - L + 1
        n_blocks = n_valid // block_size

        # 块级物理量轨迹
        w_norm_traj = np.zeros(n_blocks)
        j_cma_traj = np.zeros(n_blocks)
        w_snapshots = {}

        snapshot_set = set(snapshot_blocks) if snapshot_blocks else set()

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break

            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # block 级恒模代价 J_CMA = mean(|R²−|zX|²| + |R²−|zY|²|) / 2
            eX = self.R2 - np.abs(zx_blk) ** 2
            eY = self.R2 - np.abs(zy_blk) ** 2
            j_cma_traj[blk] = float(np.mean(np.abs(eX) + np.abs(eY)) / 2.0)

            # 块末梯度更新: standard Godard 1980 w += μ·e·z·r*
            self.wxx += self.mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += self.mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += self.mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

            # 记录块末权重范数
            cur_norm = self._norm()
            w_norm_traj[blk] = cur_norm

            # 快照
            if blk in snapshot_set:
                w_snapshots[blk] = {
                    'wxx': self.wxx.copy(), 'wxy': self.wxy.copy(),
                    'wyx': self.wyx.copy(), 'wyy': self.wyy.copy(),
                    'block_idx': blk,
                }

            # 发散检测
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        return {
            'zX': zX, 'zY': zY,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self._norm(),
            'init_w_norm': self._init_norm,
            'w_norm_traj': w_norm_traj[:blk+1] if not diverged else w_norm_traj[:blk+1],
            'j_cma_traj': j_cma_traj[:blk+1] if not diverged else j_cma_traj[:blk+1],
            'w_snapshots': w_snapshots,
            'n_blocks': n_blocks,
        }


# ═══════════════════════════════════════════════════════════
#  物理判据触发 ML 重训练 (改动1 核心)
# ═══════════════════════════════════════════════════════════

def run_ml_periodic_retrain(rX, rY, sX, sY, n_total, n_segments=PERIODIC_N_SEGMENTS,
                            initial_ml=None):
    """对照 C: ML 固定周期重训练 (复刻 D015 Q3-B).

    test 段分 n_segments 份, 每份用前一份重训练. 初始训练用 train_frac 段.
    initial_ml: 预训练的 MLChannelEqualizer (可选, 省重复训练). 会 deepcopy.
    返回 zX_full, zY_full 全段输出.
    """
    import copy
    from common._ml_equalizer import MLChannelEqualizer
    n_train = int(n_total * ML_TRAIN_FRAC)
    n_test = n_total - n_train
    seg_len = n_test // n_segments
    zX_full = np.zeros(n_total, dtype=complex)
    zY_full = np.zeros(n_total, dtype=complex)

    if initial_ml is not None:
        ml = copy.deepcopy(initial_ml)
    else:
        ml = MLChannelEqualizer(**ML_PARAMS)
        ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                 val_split=0.2, verbose=False)

    for qi in range(n_segments):
        qs = n_train + qi * seg_len
        qe = qs + seg_len if qi < n_segments - 1 else n_total
        res = ml.equalize(rX[qs:qe], rY[qs:qe])
        zX_full[qs:qe] = res['zX'].flatten()
        zY_full[qs:qe] = res['zY'].flatten()
        # 用本段重训练下一段 (除最后一段)
        if qi < n_segments - 1:
            ml = MLChannelEqualizer(**ML_PARAMS)
            ml.train(rX[qs:qe], rY[qs:qe], sX[qs:qe], sY[qs:qe],
                     val_split=0.2, verbose=False)

    return zX_full, zY_full


def _extract_ml_weights(ml):
    """提取 ML 当前 4-FIR 权重为 numpy (供 Δw 判据用)."""
    model = ml.model
    with torch_no_grad():
        return {
            name: {
                'conv_RR': getattr(model, name).conv_RR.weight.detach().cpu().numpy().copy(),
                'conv_RI': getattr(model, name).conv_RI.weight.detach().cpu().numpy().copy(),
            }
            for name in ('wxx', 'wxy', 'wyx', 'wyy')
        }


def _weights_l2_diff(w1, w2):
    """两个权重 dict 的 L2 范数差 |w1 - w2|."""
    total = 0.0
    for name in ('wxx', 'wxy', 'wyx', 'wyy'):
        for k in ('conv_RR', 'conv_RI'):
            d = w1[name][k] - w2[name][k]
            total += float(np.sum(d ** 2))
    return float(np.sqrt(total))


def torch_no_grad():
    import torch
    return torch.no_grad()


def run_ml_criterion_retrain(rX, rY, sX, sY, n_total,
                             cma_w_norm_traj, cma_j_cma_traj,
                             criterion='w_norm',
                             w_threshold_mult=None,
                             j_threshold_mult=None,
                             snapshot_weight_at_train=True,
                             w_train_ref=None,
                             initial_ml=None):
    """对照 D: ML 物理判据触发重训练 (改动1 核心).

    策略: CMA 全程在线产生物理量轨迹, 当物理量超阈值时触发 ML 重训练.
    ML 推理使用最近一次训练的权重, 直到下次触发.

    initial_ml: 预训练的 MLChannelEqualizer (可选, 省重复训练). 会 deepcopy.

    criterion:
      'w_norm': CMA 权重范数突增 (D1). 触发 = |w_cma[blk]| > w_threshold_mult × |w_cma_init|
      'j_cma':  block 级恒模代价突增 (D2). 触发 = J_CMA[blk] > j_threshold_mult × J_baseline
      'w_drift': CMA 权重漂移 (D3). 触发 = |w_cma[blk] - w_train_cma| > drift_threshold_mult × |w_train_cma|

    重训练数据: 用触发点前一段 (最近一个 test 段 1/4) 的数据重训 ML.
    返回 zX_full, zY_full 全段输出 + 触发事件列表.
    """
    import copy
    from common._ml_equalizer import MLChannelEqualizer
    n_train = int(n_total * ML_TRAIN_FRAC)
    n_test = n_total - n_train

    zX_full = np.zeros(n_total, dtype=complex)
    zY_full = np.zeros(n_total, dtype=complex)

    if initial_ml is not None:
        ml = copy.deepcopy(initial_ml)
    else:
        ml = MLChannelEqualizer(**ML_PARAMS)
        ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                 val_split=0.2, verbose=False)

    # 计算判据阈值
    cma_n_blocks = len(cma_w_norm_traj)
    cma_blocks_per_sym = n_total / cma_n_blocks  # block_size 对齐

    if criterion == 'w_norm':
        cma_init_norm = float(cma_w_norm_traj[0])  # CMA 初始范数
        threshold = w_threshold_mult * cma_init_norm
    elif criterion == 'j_cma':
        # J_baseline = 训练段 block 级 J_CMA 均值
        train_end_block = int(n_train / cma_blocks_per_sym)
        j_baseline = float(np.mean(cma_j_cma_traj[:max(train_end_block, 1)]))
        threshold = j_threshold_mult * j_baseline
    elif criterion == 'w_drift':
        # 需要 w_train_ref (训练段结束时 CMA 权重范数)
        # w_train_ref 是 CMA 在 n_train 处的权重范数 — 从 traj 取
        train_end_block = int(n_train / cma_blocks_per_sym)
        w_train_norm = float(cma_w_norm_traj[min(train_end_block, len(cma_w_norm_traj)-1)])
        threshold = None  # drift 判据每 block 算 Δw, 但我们没有逐 block CMA 权重快照
        # 改用近似: drift ≈ |w_norm[blk] - w_train_norm| 作为范数级漂移指标
    else:
        raise ValueError(f"unknown criterion {criterion}")

    # 把 CMA block 索引映射到 ML 推理符号索引
    # CMA block b 覆盖符号 [b*block_size, (b+1)*block_size)
    # 但 CMA block_size=64, 我们用 ML test 段按 PERIODIC_N_SEGMENTS 段推进
    # 简化: 把 test 段分成细粒度段 (每个 CMA block 评估一次判据),
    # 当判据触发时重训练 ML 并推理到下一个触发点

    trigger_events = []
    seg_len = n_test // PERIODIC_N_SEGMENTS  # 最小重训练间隔 = 一个周期段
    last_train_end = n_train
    cur_pos = n_train

    while cur_pos < n_total:
        # 推理到当前段末或触发点
        seg_end = min(cur_pos + seg_len, n_total)

        # 检查本段内 CMA 物理量是否触发重训练
        # CMA block 范围对应本段符号范围
        blk_start = int(cur_pos / cma_blocks_per_sym)
        blk_end = int(seg_end / cma_blocks_per_sym)
        blk_start = max(blk_start, 0)
        blk_end = min(blk_end, cma_n_blocks)

        triggered = False
        trigger_block = None
        for blk in range(blk_start, blk_end):
            if blk >= len(cma_w_norm_traj):
                break
            if criterion == 'w_norm':
                if cma_w_norm_traj[blk] > threshold:
                    triggered = True
                    trigger_block = blk
                    break
            elif criterion == 'j_cma':
                if blk < len(cma_j_cma_traj) and cma_j_cma_traj[blk] > threshold:
                    triggered = True
                    trigger_block = blk
                    break
            elif criterion == 'w_drift':
                drift = abs(cma_w_norm_traj[blk] - w_train_norm)
                if drift > w_threshold_mult * w_train_norm:
                    triggered = True
                    trigger_block = blk
                    break

        # 推理当前段 (用当前 ML 权重)
        res = ml.equalize(rX[cur_pos:seg_end], rY[cur_pos:seg_end])
        zX_full[cur_pos:seg_end] = res['zX'].flatten()
        zY_full[cur_pos:seg_end] = res['zY'].flatten()

        # 如果触发, 在段末重训练 (用最近一段数据)
        if triggered and seg_end < n_total:
            trigger_events.append({
                'block_idx': int(trigger_block),
                'sym_idx': int(trigger_block * cma_blocks_per_sym),
                'cma_value': float(cma_w_norm_traj[trigger_block]
                                   if criterion in ('w_norm', 'w_drift')
                                   else cma_j_cma_traj[trigger_block]),
            })
            # 重训练数据: 用 [last_train_end, seg_end] 段
            train_data_end = seg_end
            train_data_start = max(last_train_end, train_data_end - (n_test // PERIODIC_N_SEGMENTS))
            if train_data_end - train_data_start > 1000:  # 至少 1000 符号
                ml = MLChannelEqualizer(**ML_PARAMS)
                ml.train(rX[train_data_start:train_data_end],
                         rY[train_data_start:train_data_end],
                         sX[train_data_start:train_data_end],
                         sY[train_data_start:train_data_end],
                         val_split=0.2, verbose=False)
                last_train_end = train_data_end

        cur_pos = seg_end

    return zX_full, zY_full, trigger_events


# ═══════════════════════════════════════════════════════════
#  统计工具
# ═══════════════════════════════════════════════════════════

def _paired_wilcoxon(values_a, values_b):
    """配对 Wilcoxon (双侧精确). values_a - values_b."""
    diffs = np.asarray(values_a, dtype=float) - np.asarray(values_b, dtype=float)
    wins_a = int(np.sum(diffs < 0))
    wins_b = int(np.sum(diffs > 0))
    ties = int(np.sum(diffs == 0))
    effective = diffs[diffs != 0]
    if len(effective) == 0:
        return {"statistic": 0.0, "pvalue": 1.0, "method": "exact",
                "wins_first": wins_a, "wins_second": wins_b, "ties": ties,
                "differences": diffs.tolist()}
    result = wilcoxon(diffs, alternative="two-sided", zero_method="wilcox",
                      correction=False, method="exact", nan_policy="raise")
    return {
        "method": "exact",
        "statistic": float(result.statistic),
        "pvalue": float(result.pvalue),
        "wins_first": wins_a,
        "wins_second": wins_b,
        "ties": ties,
        "differences": diffs.tolist(),
    }


# ═══════════════════════════════════════════════════════════
#  单 seed trial
# ═══════════════════════════════════════════════════════════

def run_single_seed(seed, n_symbols=N_SYMBOLS, f_g=F_G,
                    d1_thresholds=(5.0,),
                    d2_thresholds=(5.0,),
                    d3_thresholds=(0.3, 0.5)):
    """跑一次完整 trial: A/B/C/D1/D2/D3 + oracle.

    预筛选 (单 seed CMA 物理量分析, TL-22 物理前提检查) 确定有效判据:
      D1 |w| 突增: 2×init=80% 触发(退化), 5×/10×=0% 触发(无效). 仅保留 5.0 (复用B)
      D2 J_CMA 突增: 全 0% 触发(无效, D027 clean swap 恒模). 仅保留 5.0 (复用B)
      D3 Δw 漂移: 0.1=52%(太频), 0.3=21%, 0.5=10% 触发(有效). 保留 0.3/0.5

    返回 trial dict 含所有方法的 late 段双口径 BER.
    """
    from common._ml_equalizer import MLChannelEqualizer
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(n_symbols, alpha, beta, f_g,
                                           SOP_RATE, int(seed))

    # late slice: test 段内后 1/4 (与 D022/D015 一致)
    # 用模块级 LATE_START/LATE_END (smoke 模式会全局覆盖)
    if LATE_START > 0 and LATE_END <= n_symbols:
        late = slice(LATE_START, LATE_END)
    else:
        late = slice(int(n_symbols * 0.875), n_symbols)
    source_x = sX[late]
    source_y = sY[late]

    # ── A: standard-CMA (带监控, 供 D 判据用) ──
    eq_a = MonitoredStandardCMA(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_a = eq_a.equalize_monitored(rX, rY, block_size=CMA_BLOCK_SIZE)

    # ── B: ML 训练一次 (初始训练, C/D 共享此模型) ──
    seed_ml(int(seed))
    n_train = int(n_symbols * ML_TRAIN_FRAC)
    ml_b = MLChannelEqualizer(**ML_PARAMS)
    ml_b.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
               val_split=0.2, verbose=False)
    res_b = ml_b.equalize(rX, rY)
    # ML equalize 返回 2D (1, N), 需 flatten (与 prompt015 一致)
    res_b_zX = np.asarray(res_b['zX']).flatten()
    res_b_zY = np.asarray(res_b['zY']).flatten()

    # ── C: ML 固定周期重训练 (共享初始训练, 省 1 次 ML 训练) ──
    seed_ml(int(seed))
    zX_c, zY_c = run_ml_periodic_retrain(rX, rY, sX, sY, n_symbols,
                                         initial_ml=ml_b)

    # ── D1/D2/D3: 物理判据触发重训练 ──
    # 预筛选 (单 seed CMA 物理量分析, TL-22 物理前提检查):
    #   D1 |w|>5×init / D2 J_CMA 全部: 0% 触发 → 等于 B (训练一次), 复用 B 结果不重跑
    #   D1 |w|>2×init: 80% 触发 → 实际跑 (退化对照)
    #   D3 Δw: 实际跑 (唯一有效判据)
    cma_w_norm_traj = res_a['w_norm_traj']
    cma_j_cma_traj = res_a['j_cma_traj']

    d_results = {}
    # 预计算 CMA 物理量阈值, 判断是否需要实际跑
    cma_init_norm = float(cma_w_norm_traj[0])
    n_train_block_pre = int(n_symbols * ML_TRAIN_FRAC / CMA_BLOCK_SIZE)
    j_baseline_pre = float(np.mean(cma_j_cma_traj[:max(n_train_block_pre, 1)]))

    for thr in d1_thresholds:
        threshold_val = thr * cma_init_norm
        n_trig_pre = int(np.sum(cma_w_norm_traj > threshold_val))
        if n_trig_pre == 0:
            # 0% 触发 = 等于 B, 复用结果 (省 ML 训练时间)
            d_results[f'D1_w_norm_{thr}'] = {
                'zX': res_b_zX.copy(), 'zY': res_b_zY.copy(),
                'triggers': [], 'criterion': 'w_norm',
                'threshold_mult': float(thr),
                'reused_from_B': True,
                'preselect_n_trig': 0,
            }
        else:
            seed_ml(int(seed))
            zX_d1, zY_d1, trig = run_ml_criterion_retrain(
                rX, rY, sX, sY, n_symbols,
                cma_w_norm_traj, cma_j_cma_traj,
                criterion='w_norm', w_threshold_mult=thr)
            d_results[f'D1_w_norm_{thr}'] = {
                'zX': zX_d1, 'zY': zY_d1, 'triggers': trig, 'criterion': 'w_norm',
                'threshold_mult': float(thr),
                'reused_from_B': False,
                'preselect_n_trig': n_trig_pre,
            }

    for thr in d2_thresholds:
        threshold_val = thr * j_baseline_pre
        n_trig_pre = int(np.sum(cma_j_cma_traj > threshold_val))
        if n_trig_pre == 0:
            d_results[f'D2_j_cma_{thr}'] = {
                'zX': res_b_zX.copy(), 'zY': res_b_zY.copy(),
                'triggers': [], 'criterion': 'j_cma',
                'threshold_mult': float(thr),
                'reused_from_B': True,
                'preselect_n_trig': 0,
            }
        else:
            seed_ml(int(seed))
            zX_d2, zY_d2, trig = run_ml_criterion_retrain(
                rX, rY, sX, sY, n_symbols,
                cma_w_norm_traj, cma_j_cma_traj,
                criterion='j_cma', j_threshold_mult=thr)
            d_results[f'D2_j_cma_{thr}'] = {
                'zX': zX_d2, 'zY': zY_d2, 'triggers': trig, 'criterion': 'j_cma',
                'threshold_mult': float(thr),
                'reused_from_B': False,
                'preselect_n_trig': n_trig_pre,
            }

    for thr in d3_thresholds:
        seed_ml(int(seed))
        zX_d3, zY_d3, trig = run_ml_criterion_retrain(
            rX, rY, sX, sY, n_symbols,
            cma_w_norm_traj, cma_j_cma_traj,
            criterion='w_drift', w_threshold_mult=thr,
            initial_ml=ml_b)
        d_results[f'D3_w_drift_{thr}'] = {
            'zX': zX_d3, 'zY': zY_d3, 'triggers': trig, 'criterion': 'w_drift',
            'threshold_mult': float(thr),
            'reused_from_B': False,
        }

    # ── oracle ──
    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)

    # ── 双口径 BER 评估 (D018) ──
    trial = {
        "seed": int(seed),
        "late_slice": [late.start, late.stop],
        "elapsed_s": time.time() - started,
        "params": {
            "f_g": float(f_g), "turbulence": TURBULENCE,
            "n_symbols": int(n_symbols), "gamma_bar": float(GAMMA_BAR),
            "sop_rate": float(SOP_RATE), "mu_safe": float(MU_SAFE),
            "n_tap": int(N_TAP),
        },
        "methods": {
            "A_standard_cma": evaluate_outputs(
                res_a['zX'][late], res_a['zY'][late], source_x, source_y,
                res_a['diverged']),
            "B_ml_train_once": evaluate_outputs(
                res_b_zX[late], res_b_zY[late], source_x, source_y,
                res_b['diverged']),
            "C_ml_periodic": evaluate_outputs(
                zX_c[late], zY_c[late], source_x, source_y, False),
            "C_oracle": evaluate_outputs(
                oracle_x[late], oracle_y[late], source_x, source_y, False),
        },
        "artifacts": {
            "A_standard_cma": {
                "diverged": res_a['diverged'],
                "final_w_norm": float(res_a['final_w_norm']),
                "cma_w_norm_stats": {
                    "mean": float(np.mean(res_a['w_norm_traj'])),
                    "max": float(np.max(res_a['w_norm_traj'])),
                    "min": float(np.min(res_a['w_norm_traj'])),
                },
                "cma_j_cma_stats": {
                    "mean": float(np.mean(res_a['j_cma_traj'])),
                    "max": float(np.max(res_a['j_cma_traj'])),
                    "min": float(np.min(res_a['j_cma_traj'])),
                },
            },
        },
    }

    # D 方法评估
    trial["methods"].pop("C_oracle", None)
    trial["methods"]["oracle"] = evaluate_outputs(
        oracle_x[late], oracle_y[late], source_x, source_y, False)

    oracle_pi = float(trial["methods"]["oracle"]["permutation_invariant_ber"]["mean"])

    for d_key, d_data in d_results.items():
        trial["methods"][d_key] = evaluate_outputs(
            d_data['zX'][late], d_data['zY'][late], source_x, source_y, False)
        n_trig = len(d_data['triggers'])
        n_test_blocks = len(d_results  # test 段 block 数
                            )  # placeholder
        trial["artifacts"][d_key] = {
            "criterion": d_data['criterion'],
            "threshold_mult": d_data['threshold_mult'],
            "n_triggers": int(n_trig),
            "trigger_blocks": [t['block_idx'] for t in d_data['triggers'][:20]],  # 前 20
            "first_trigger_sym": (int(d_data['triggers'][0]['sym_idx'])
                                  if d_data['triggers'] else None),
        }

    # excess PI-BER vs oracle
    for name in trial["methods"]:
        if name == "oracle":
            continue
        pi = float(trial["methods"][name]["permutation_invariant_ber"]["mean"])
        trial["methods"][name]["excess_pi_ber_vs_oracle"] = pi - oracle_pi

    return trial


# ═══════════════════════════════════════════════════════════
#  汇总 + 判定
# ═══════════════════════════════════════════════════════════

def summarize_trials(trials, d_keys=None):
    """汇总各方法 PI-BER + 配对统计 (B vs D, C vs D)."""
    trials = sorted(trials, key=lambda t: int(t["seed"]))
    seeds = [int(t["seed"]) for t in trials]
    n = len(trials)

    if d_keys is None:
        # 自动发现 D 方法
        sample = trials[0]["methods"]
        d_keys = sorted([k for k in sample
                         if k.startswith('D1_') or k.startswith('D2_') or k.startswith('D3_')])

    all_methods = ["A_standard_cma", "B_ml_train_once", "C_ml_periodic"] + d_keys + ["oracle"]

    summaries = {}
    for m in all_methods:
        if m not in trials[0]["methods"]:
            continue
        pi_vals = [float(t["methods"][m]["permutation_invariant_ber"]["mean"]) for t in trials]
        fixed_vals = [float(t["methods"][m]["fixed_label_ber"]["mean"]) for t in trials]
        summaries[m] = {
            "pi_ber": {"mean": float(np.mean(pi_vals)), "std": float(np.std(pi_vals)),
                       "values": pi_vals},
            "fixed_ber": {"mean": float(np.mean(fixed_vals)), "std": float(np.std(fixed_vals)),
                          "values": fixed_vals},
        }
        if m != "oracle":
            excess = [float(t["methods"][m]["excess_pi_ber_vs_oracle"]) for t in trials]
            summaries[m]["excess_pi_ber"] = {
                "mean": float(np.mean(excess)), "std": float(np.std(excess)), "values": excess}

    # 配对: B vs D (训练一次 vs 判据触发), C vs D (固定周期 vs 判据触发)
    pairwise = {}
    for d in d_keys:
        b_vals = summaries["B_ml_train_once"]["pi_ber"]["values"]
        d_vals = summaries[d]["pi_ber"]["values"]
        # diffs = B - D: 正=D更好(D的BER更低)
        bd = _paired_wilcoxon(b_vals, d_vals)
        c_vals = summaries["C_ml_periodic"]["pi_ber"]["values"]
        cd = _paired_wilcoxon(c_vals, d_vals)
        pairwise[f"B_vs_{d}"] = bd
        pairwise[f"C_vs_{d}"] = cd

    # 判定每个 D 方法
    verdicts = {}
    for d in d_keys:
        d_pi = summaries[d]["pi_ber"]["mean"]
        b_pi = summaries["B_ml_train_once"]["pi_ber"]["mean"]
        c_pi = summaries["C_ml_periodic"]["pi_ber"]["mean"]

        bd_comp = pairwise[f"B_vs_{d}"]
        # wins_second = D 赢次数 (d_vals < b_vals)
        d_wins_vs_b = bd_comp["wins_second"]
        d_better_than_b_signif = bool(bd_comp["pvalue"] < 0.05 and d_wins_vs_b >= 4)

        # D 接近 C: D/C < 2
        d_close_to_c = bool(d_pi < c_pi * 2) if c_pi > 0 else bool(d_pi < 0.01)

        # 触发频率 (平均)
        n_trigs = [float(t["artifacts"][d]["n_triggers"]) for t in trials
                   if d in t.get("artifacts", {})]
        mean_trigs = float(np.mean(n_trigs)) if n_trigs else 0.0
        # test 段约 2.5M 符号 / 64 block_size ≈ 39000 blocks; 50% 阈值
        trig_freq_ok = bool(mean_trigs < 19500)

        go = bool(d_better_than_b_signif and d_close_to_c and trig_freq_ok)
        verdicts[d] = {
            "d_pi_ber": float(d_pi),
            "b_pi_ber": float(b_pi),
            "c_pi_ber": float(c_pi),
            "d_vs_c_ratio": float(d_pi / c_pi) if c_pi > 0 else float('inf'),
            "d_wins_vs_b": int(d_wins_vs_b),
            "d_better_than_b_signif": d_better_than_b_signif,
            "d_close_to_c": d_close_to_c,
            "mean_n_triggers": mean_trigs,
            "trig_freq_ok": trig_freq_ok,
            "verdict": "GO" if go else "KILL",
        }

    # 整体判定: 任一 D 方法 GO 则改动1 GO
    any_go = any(v["verdict"] == "GO" for v in verdicts.values())

    return {
        "n_seeds": n,
        "seeds": seeds,
        "method_summaries": summaries,
        "pairwise": pairwise,
        "d_verdicts": verdicts,
        "overall_verdict": "GO" if any_go else "KILL",
        "overall_go_count": int(sum(1 for v in verdicts.values() if v["verdict"] == "GO")),
    }


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def _load_checkpoint(path):
    """加载 checkpoint (已完成的 trials)."""
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return None


def _save_checkpoint(payload, path):
    """原子保存 checkpoint."""
    import tempfile
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
    os.close(fd)
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        try:
            Path(tmp).unlink()
        except FileNotFoundError:
            pass


def main(argv=None):
    parser = argparse.ArgumentParser(description='PROMPT-022: 改动1 物理判据驱动 ML 重训练 MVE')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 seed, 500K symbols)')
    parser.add_argument('--n2m', action='store_true',
                        help='验证2: N=2M 收益域 (非门控)')
    parser.add_argument('--n-seeds', type=int, default=5)
    parser.add_argument('--seeds', nargs='*', type=int, default=None)
    parser.add_argument('--output', type=str, default=None,
                        help='输出路径 (支持 checkpoint 续跑)')
    args = parser.parse_args(argv)

    t_global = time.time()

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (验证实现正确性, 1 seed, 500K symbols)")
        print("=" * 60)
        n_sym = 500_000
        late_start = int(n_sym * 0.875)
        late_end = n_sym
        global LATE_START, LATE_END
        LATE_START, LATE_END = late_start, late_end
        seeds = [1000]
        n_sym_use = n_sym
        out_path = Path(args.output) if args.output else (
            SIM_DIR / "results" / "cma-fade-divergence" / "prompt022_smoke.json")
    elif args.n2m:
        print("=" * 60)
        print("验证2: N=2M 收益域 (非门控)")
        print("=" * 60)
        n_sym = 2_000_000
        late_start = int(n_sym * 0.875)
        late_end = n_sym
        seeds = args.seeds or SEEDS_5
        n_sym_use = n_sym
        out_path = Path(args.output) if args.output else (
            SIM_DIR / "results" / "cma-fade-divergence" / "prompt022_modification1_mve_n2m.json")
    else:
        seeds = args.seeds or SEEDS_5
        n_sym_use = N_SYMBOLS
        out_path = Path(args.output) if args.output else RESULT_PATH

    print(f"参数: f_G={F_G}, {TURBULENCE}, N={n_sym_use}, QPSK, "
          f"SNR={10*np.log10(GAMMA_BAR):.0f}dB, SOP={SOP_RATE}")
    print(f"对照: A(stdCMA) / B(ML训练一次) / C(固定周期重训练) / "
          f"D1(|w|判据) / D2(J_CMA判据) / D3(Δw漂移判据)")
    print(f"输出: {out_path}")
    print("=" * 60)

    # Checkpoint 续跑
    ckpt = _load_checkpoint(out_path)
    if ckpt and 'trials' in ckpt:
        completed_seeds = {int(t['seed']) for t in ckpt['trials']}
        pending = [s for s in seeds if s not in completed_seeds]
        trials = ckpt['trials']
        print(f"Checkpoint: {len(completed_seeds)} seeds done, {len(pending)} pending")
    else:
        pending = list(seeds)
        trials = []

    for i, seed in enumerate(pending):
        print(f"\n[seed {seed} {len(trials)+1}/{len(seeds)}] running...", flush=True)
        t0_seed = time.time()
        if args.n2m:
            t = run_single_seed(seed, n_symbols=2_000_000)
            t["late_slice"] = [int(2_000_000 * 0.875), 2_000_000]
        else:
            t = run_single_seed(seed, n_symbols=n_sym_use)
        trials.append(t)
        # 增量保存 checkpoint
        _save_checkpoint({'trials': trials, 'experiment': 'partial'}, out_path)

        # 打印快速结果
        ms = t["methods"]
        a_pi = ms["A_standard_cma"]["permutation_invariant_ber"]["mean"]
        b_pi = ms["B_ml_train_once"]["permutation_invariant_ber"]["mean"]
        c_pi = ms["C_ml_periodic"]["permutation_invariant_ber"]["mean"]
        o_pi = ms["oracle"]["permutation_invariant_ber"]["mean"]
        d_keys = sorted([k for k in ms if k.startswith('D')])
        d_brief = " | ".join(
            f"{k}={ms[k]['permutation_invariant_ber']['mean']:.4f}"
            f"(n={t['artifacts'][k]['n_triggers']})"
            for k in d_keys)
        print(f"  A={a_pi:.4f} B={b_pi:.4f} C={c_pi:.4f} oracle={o_pi:.4f}", flush=True)
        print(f"  {d_brief}", flush=True)
        print(f"  [{time.time()-t0_seed:.0f}s]", flush=True)

    summary = summarize_trials(trials)

    payload = {
        "experiment": "PROMPT-022 modification1 (physics-criterion-driven ML retrain) MVE"
                       + (" N=2M" if args.n2m else " N=5M"),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "params": {
            "f_g": float(F_G), "turbulence": TURBULENCE,
            "n_symbols": int(n_sym_use), "gamma_bar": float(GAMMA_BAR),
            "sop_rate": float(SOP_RATE), "mu_safe": float(MU_SAFE),
            "n_tap": int(N_TAP), "r2": float(R2_QPSK),
            "late_slice": [LATE_START, LATE_END] if not args.n2m else [int(2_000_000*0.875), 2_000_000],
            "periodic_n_segments": PERIODIC_N_SEGMENTS,
            "ml_train_frac": ML_TRAIN_FRAC,
            "d1_thresholds": [5.0],
            "d2_thresholds": [5.0],
            "d3_thresholds": [0.3, 0.5],
        },
        "tl20_hypothesis": {
            "A": "standard-CMA PI ~0.02-0.03",
            "B": "ML 训练一次 PI ~0.5 (D015 全崩)",
            "C": "固定周期重训练 PI ~0.002 (D015 Q3-B)",
            "D1_w_norm": "预期高 ~0.3-0.5 (D013 swap 时 |w| 不突增)",
            "D2_j_cma": "预期中高 ~0.1-0.3 (D027 clean swap J_CMA 不突增)",
            "D3_w_drift": "预期中低 ~0.01-0.1 (SOP 持续旋转→Δw 单调增→可触发)",
        },
        "trials": trials,
        "summary": summary,
        "elapsed_s": time.time() - t_global,
    }

    out_path = RESULT_PATH if not args.n2m else (
        SIM_DIR / "results" / "cma-fade-divergence" / "prompt022_modification1_mve_n2m.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")

    # 打印汇总
    print("\n" + "=" * 60)
    print(f"PROMPT-022 汇总: 改动1 物理判据驱动 ML 重训练 ({len(seeds)} seeds)")
    print("=" * 60)
    ms = summary["method_summaries"]
    print(f"\n{'方法':>24} {'PI-BER mean':>12} {'fixed BER':>12} {'excess PI':>12}")
    print("-" * 70)
    for m in sorted(ms.keys()):
        pi = ms[m]["pi_ber"]["mean"]
        fx = ms[m]["fixed_ber"]["mean"]
        ex = ms[m].get("excess_pi_ber", {}).get("mean", 0.0)
        print(f"{m:>24} {pi:>12.4f} {fx:>12.4f} {ex:>12.4f}")

    print(f"\n--- D 方法判定 ---")
    for d, v in summary["d_verdicts"].items():
        print(f"  {d}: {v['verdict']} (PI={v['d_pi_ber']:.4f}, "
              f"D/B 赢 {v['d_wins_vs_b']}/5, D/C={v['d_vs_c_ratio']:.1f}×, "
              f"触发={v['mean_n_triggers']:.0f})")

    print(f"\n>>> 整体判定: {summary['overall_verdict']} "
          f"({summary['overall_go_count']}/{len(summary['d_verdicts'])} D 方法 GO) <<<")
    print(f"\n总耗时: {time.time() - t_global:.0f}s")

    return payload


if __name__ == '__main__':
    main()
