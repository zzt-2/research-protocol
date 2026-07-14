"""PROMPT-021: Q-DP4 形态1（检测+回滚）维度 D MVE 第二轮

> 方向: Q-DP4 (SOP 驱动 polarization lock swap 防跳变) | 状态: WIP | 创建: 2026-07-15
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)
> 隔离原则: 不改 common/, 复用 prompt019 StandardCMA2x2 + prompt012 evaluate_outputs/_abs_corr

## 背景 (S022 形态2 Kill 后)

D027 Kill 了 Q-DP4 形态2（预防性约束）——V3 FAIL: J_XCA 对 clean swap 无效 (输出互相关≈0),
diag 约束最好仅 1.24× 且大α反引发更多 swap。根因: swap 是恒模代价多解地形在 SOP 旋转下让权重跳盆地,
约束权重分量不改变地形结构。

但 V1 证实 Q-DP4 问题陈述 (D3=收敛后防 swap) 真实: 6× PI-BER 差距 (CMA 0.03174 vs ML 0.00523)
来自 swap 相关权重漂移 (B0/B2=8.3×), CMA 跟踪能力够 (B1/oracle=2.2×)。

形态1（检测+回滚）从未做过。关键区别: R7 冻结/D026 压μ响应的是 fade (h<阈值),
形态1 响应的是 swap (极化锁定跳变)——不同检测对象。

## 形态1 的真正 hinge (V3 物理洞察推出)

回滚后 CMA 继续在线更新, 代价地形多解不变, CMA 是否立即再次跳到次优盆地?
  - 回滚后中位 dwell time < ~1000 块 → 形态1 无效 (跟 R7 阴影重合), Q-DP4 Kill
  - 回滚后中位 dwell time > ~10000 块 → 形态1 有窗口, 可能有效

## 两个验证 (按门控顺序)

验证0 (Kill 门控前置): swap 时间频率
  问题: swap 事件在 late 段多频繁? swap 之间间隔多少块?
  设计: 复用 prompt020 StandardCMA2x2, 新增 block 级 swap 检测
    每 block (block_size=64) 算 corr(zX,sY), 超阈值=swap 事件, 记录 block index
  Kill 门控: late 段 (625000 块) swap 间隔中位 < 1000 块 → 形态1 无窗口直接 Kill
  PASS 门控: 间隔中位 > 1000 块 → 继续验证1

验证1 (Go/Kill hinge): swap 检测 + 权重回滚 dwell time
  问题: 检测到 swap 后回滚权重到 swap 前快照, CMA 多久后再次 swap?
  设计:
    - 基于验证0 的 swap 事件序列, 对每个 swap 事件做"回滚实验"
    - swap 检测: corr(zX,sY) 突增超阈值 (检测延迟 = 回滚触发前的 block 数)
    - 回滚动作: 权重恢复到 swap 前 N_snapshot 块的快照 (N_snapshot 扫 {100, 500, 1000})
    - 回滚后跟踪: CMA 从回滚点继续在线更新, 记录回滚后到下次 swap 的 dwell time
  对照: standard-CMA (无回滚) vs 形态1 (检测+回滚) vs oracle
  指标: late 段 PI-BER (双口径 D018) + swap 总持续时间占比 + 回滚后中位 dwell time

## 理论预期 (TL-20, 实验前写)

验证0 预期: swap 间隔分布宽尾——swap 是 SOP 累积旋转驱动的离散事件, SOP 旋转速率 1 krad/s
  (sop_rate=4e-7 rad/sym × 2.5 GBaud), 每 block (64 sym = 25.6 ns) 旋转 4e-7×64=2.56e-5 rad,
  累积到 π/2 (首次 swap 带 3.6°→14.3° from D015) 需 ~250-1000 块。但 swap 不是周期性的——
  SOP 持续旋转穿过 π/2 整数倍时触发, 间隔取决于 SOP 穿越速率, 预期间隔中位在
  数百到数千块量级 (不确定, 须实证)。

验证1 预期 (基于 V3 物理洞察): 回滚后 dwell time 不长 (倾向 FAIL) ——代价地形多解不变,
  回滚把权重拉回正确盆地但 CMA 在线更新会在 SOP 持续旋转下再次漂入 swap 盆地。
  D015 Q2 显示 N=8M CMA late 跟踪 SOP 到 90° 附近时 BER=0.037 (CMA 能跟踪), 但
  S022 V1 B1 (identity 重初始化 late 跟踪) PI=0.0180 仍 swap (clean-swap seeds),
  说明即使从正确盆地开始 CMA 在 late 625K 块内仍漂入 swap。
  关键不确定: 回滚后 CMA 是否立即再跳 (dwell < 1000) 还是有实质窗口 (dwell > 5000)?
  预期 dwell 中位 < 5000 块 (倾向 Kill), 但须实证确认。

## 预注册 Go/Kill 判据 (FR-25 分离)

Go 标准 (全部满足):
  1. 形态1 PI-BER 显著低于 standard-CMA (5 seeds Wilcoxon p<0.05 + ≥4/5 胜)
  2. 形态1 PI-BER 比 standard-CMA 降 ≥2×
  3. 回滚后中位 dwell time > 5000 块 (回滚有实质窗口)

Kill 标准 (任一触发):
  1. 验证0: late 段 swap 间隔中位 < 1000 块 (无窗口)
  2. 验证1: 回滚后中位 dwell time < 1000 块 (R7 阴影重合, CMA 立即再跳)
  3. 验证1: PI-BER 无显著改善

不用 oracle 当 Go 判据 (FR-25)。

## 参数溯源 (FR-20)
  sop_rate=4e-7: sat.1553 §6.3 L778 仿真值 (1 krad/s 真实 OSL 速率)
  f_G=30: D022 注册域 (与 S022 V1 一致, 便于对照 swap seeds 1000/1002)
  N=5M: D022 注册域; late [4.375M, 5M): D022/D018 一致
  μ=1e-3: D006 安全区低风险 (D018 收紧)
  swap 检测阈值 corr>0.5: 经验阈值, 报告敏感性 (0.3/0.5/0.7 三档)
"""
from __future__ import annotations

import argparse
import json
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
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    gen_channel,
    oracle_equalize,
)
from params import SimulationConfig
from prompt019_mu_compress_mve import StandardCMA2x2, compute_h_block_series
from prompt012_longseq_audit import evaluate_outputs, _abs_corr, classify_failure


# ─── 实验参数 (FR-20 溯源) ──────────────────────────────────

N_SYMBOLS = 5_000_000          # 5M (D022 注册域, 与 S022 V1 一致)
TURBULENCE = "strong"          # α=1.5, β=0.8 (GG 强湍流)
F_G_PRIMARY = 30.0             # D022 注册域 (与 S022 V1 一致, 便于对照 swap seeds)
LATE_START = 4_375_000
LATE_END = 5_000_000
CMA_BLOCK_SIZE = 64            # sat.1553 §6.3 L756 并行化因子
SEEDS_5 = [1000, 1001, 1002, 1003, 1004]

# swap 检测阈值 (经验值, 报告敏感性)
SWAP_THRESHOLDS = [0.3, 0.5, 0.7]
SWAP_THRESHOLD_DEFAULT = 0.5

# 验证1: 回滚快照窗口
SNAPSHOT_WINDOWS = [100, 500, 1000]

RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence" / "prompt021_qdp4_form1_mve.json"
)


# ═══════════════════════════════════════════════════════════
#  Block 级 swap 检测工具
# ═══════════════════════════════════════════════════════════

def compute_block_corr_series(zX, zY, sX, sY, block_size=CMA_BLOCK_SIZE):
    """计算 block 级相关性序列.

    每 block 算 4 个相关: corr(zX,sX), corr(zX,sY), corr(zY,sX), corr(zY,sY).
    返回 (n_blocks,) 的 4 个数组 + block 起始 index 数组.

    用途: 检测 swap 事件 (corr(zX,sY) 突增 = X 输出串入 Y 数据)。
    """
    N = len(zX)
    n_valid = N - N_TAP + 1
    half = N_TAP // 2
    n_blocks = n_valid // block_size

    corr_zX_sX = np.zeros(n_blocks)
    corr_zX_sY = np.zeros(n_blocks)
    corr_zY_sX = np.zeros(n_blocks)
    corr_zY_sY = np.zeros(n_blocks)
    block_starts = np.zeros(n_blocks, dtype=int)

    for blk in range(n_blocks):
        s = blk * block_size + half   # 对齐 CMA 输出 (中心 index)
        e = s + block_size
        if e > N:
            break
        zx_blk = zX[s:e]
        zy_blk = zY[s:e]
        sx_blk = sX[s:e]
        sy_blk = sY[s:e]
        corr_zX_sX[blk] = _abs_corr(zx_blk, sx_blk)
        corr_zX_sY[blk] = _abs_corr(zx_blk, sy_blk)
        corr_zY_sX[blk] = _abs_corr(zy_blk, sx_blk)
        corr_zY_sY[blk] = _abs_corr(zy_blk, sy_blk)
        block_starts[blk] = s

    return {
        'corr_zX_sX': corr_zX_sX[:blk+1] if blk + 1 <= n_blocks else corr_zX_sX,
        'corr_zX_sY': corr_zX_sY[:blk+1] if blk + 1 <= n_blocks else corr_zX_sY,
        'corr_zY_sX': corr_zY_sX[:blk+1] if blk + 1 <= n_blocks else corr_zY_sX,
        'corr_zY_sY': corr_zY_sY[:blk+1] if blk + 1 <= n_blocks else corr_zY_sY,
        'block_starts': block_starts[:blk+1] if blk + 1 <= n_blocks else block_starts,
        'n_blocks': n_blocks,
    }


def detect_swap_events(corr_zX_sY, corr_zX_sX, threshold=SWAP_THRESHOLD_DEFAULT,
                       min_consecutive=1):
    """检测 swap 事件序列.

    swap 判据: corr(zX,sY) > threshold 且 corr(zX,sY) > corr(zX,sX)
    (X 输出与 Y 数据相关性超过阈值且超过与 X 数据的相关性 = 极化锁定跳变)

    返回 swap 事件列表: 每个 = (start_block, end_block, peak_corr)
    连续 swap block 合并为一个事件 (min_consecutive 控制最小持续 block 数, 默认 1)。
    """
    n = len(corr_zX_sY)
    is_swap = (corr_zX_sY > threshold) & (corr_zX_sY > corr_zX_sX)

    events = []
    i = 0
    while i < n:
        if is_swap[i]:
            j = i
            while j < n and is_swap[j]:
                j += 1
            run_len = j - i
            if run_len >= min_consecutive:
                peak = float(np.max(corr_zX_sY[i:j]))
                events.append({
                    'start_block': int(i),
                    'end_block': int(j - 1),
                    'length_blocks': int(run_len),
                    'peak_corr_zX_sY': peak,
                })
            i = j
        else:
            i += 1
    return events


def compute_swap_intervals(events, late_start_block, late_end_block):
    """计算 late 段内的 swap 事件间隔 + swap 占比.

    间隔 = 事件 i+1 的 start - 事件 i 的 end (同一 swap 状态外的间隔)。
    只算 late 段内的事件。swap 持续时间 = 事件与 late 段交集的 block 数 (裁剪到 late 范围)。
    """
    late_events = [e for e in events
                   if e['end_block'] >= late_start_block and e['start_block'] < late_end_block]

    intervals = []
    for k in range(1, len(late_events)):
        interval = late_events[k]['start_block'] - late_events[k-1]['end_block']
        if interval > 0:
            intervals.append(int(interval))

    # swap 持续时间: 事件与 late 段交集 (裁剪), 非事件全长
    swap_duration = 0
    for e in late_events:
        seg_start = max(e['start_block'], late_start_block)
        seg_end = min(e['end_block'], late_end_block - 1)
        if seg_end >= seg_start:
            swap_duration += seg_end - seg_start + 1
    late_duration = late_end_block - late_start_block
    swap_fraction = swap_duration / max(late_duration, 1)

    return {
        'n_events_late': len(late_events),
        'intervals': intervals,
        'interval_median': float(np.median(intervals)) if intervals else None,
        'interval_mean': float(np.mean(intervals)) if intervals else None,
        'interval_min': int(np.min(intervals)) if intervals else None,
        'interval_max': int(np.max(intervals)) if intervals else None,
        'swap_duration_blocks': int(swap_duration),
        'late_duration_blocks': int(late_duration),
        'swap_fraction': float(swap_fraction),
        'events': late_events,
    }


# ═══════════════════════════════════════════════════════════
#  验证0: swap 时间频率 (Kill 门控前置)
# ═══════════════════════════════════════════════════════════

def run_v0_swap_frequency(seed, f_g=F_G_PRIMARY, n_symbols=N_SYMBOLS,
                          threshold=SWAP_THRESHOLD_DEFAULT):
    """验证0: 单 seed 的 swap 事件检测 + 间隔统计."""
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        n_symbols, alpha, beta, f_g, SOP_RATE, int(seed))

    # standard-CMA (复用 prompt019)
    eq = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res = eq.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)

    # block 级相关性序列
    corr_series = compute_block_corr_series(res['zX'], res['zY'], sX, sY, CMA_BLOCK_SIZE)

    # swap 事件检测
    events = detect_swap_events(
        corr_series['corr_zX_sY'], corr_series['corr_zX_sX'], threshold=threshold)

    # late 段 block 范围
    half = N_TAP // 2
    late_start_block = (LATE_START - half) // CMA_BLOCK_SIZE
    late_end_block = (LATE_END - half) // CMA_BLOCK_SIZE

    swap_stats = compute_swap_intervals(events, late_start_block, late_end_block)

    return {
        "seed": int(seed),
        "threshold": float(threshold),
        "elapsed_s": time.time() - started,
        "diverged": res['diverged'],
        "final_w_norm": float(res['final_w_norm']),
        "n_blocks_total": corr_series['n_blocks'],
        "late_start_block": int(late_start_block),
        "late_end_block": int(late_end_block),
        "swap_stats": swap_stats,
    }


def run_v0_all_seeds(seeds, threshold=SWAP_THRESHOLD_DEFAULT, label=''):
    """验证0: 全 seeds swap 频率统计."""
    trials = []
    for i, seed in enumerate(seeds):
        t = run_v0_swap_frequency(seed, threshold=threshold)
        trials.append(t)
        ss = t['swap_stats']
        med = ss['interval_median']
        print(f"  [v0 {label} {i+1}/{len(seeds)}] seed={seed} thr={threshold}: "
              f"n_events={ss['n_events_late']} interval_med={med} "
              f"swap_frac={ss['swap_fraction']:.4f} div={t['diverged']}", flush=True)
    return trials


def summarize_v0(trials, kill_threshold_blocks=1000):
    """验证0 判定: swap 间隔是否给形态1 窗口."""
    all_intervals = []
    total_events = 0
    swap_fractions = []
    for t in trials:
        ss = t['swap_stats']
        all_intervals.extend(ss['intervals'])
        total_events += ss['n_events_late']
        swap_fractions.append(ss['swap_fraction'])

    median_interval = float(np.median(all_intervals)) if all_intervals else None
    mean_interval = float(np.mean(all_intervals)) if all_intervals else None
    mean_swap_fraction = float(np.mean(swap_fractions)) if swap_fractions else 0.0

    # Kill 门控: 间隔中位 < kill_threshold → 无窗口
    if median_interval is None:
        verdict = "PASS_NO_SWAP"
        interpretation = "无 swap 事件 → 形态1 无对象, 但也无 swap 问题 (clean seeds)"
    elif median_interval < kill_threshold_blocks:
        verdict = "KILL"
        interpretation = (
            f"KILL: swap 间隔中位 {median_interval:.0f} < {kill_threshold_blocks} 块 "
            f"(swap 极频繁, 形态1 无窗口)"
        )
    else:
        verdict = "PASS"
        interpretation = (
            f"PASS: swap 间隔中位 {median_interval:.0f} ≥ {kill_threshold_blocks} 块 "
            f"(形态1 有窗口, 继续验证1)"
        )

    return {
        "total_events_late": int(total_events),
        "all_intervals_count": len(all_intervals),
        "interval_median": median_interval,
        "interval_mean": mean_interval,
        "interval_min": int(np.min(all_intervals)) if all_intervals else None,
        "interval_max": int(np.max(all_intervals)) if all_intervals else None,
        "mean_swap_fraction_late": mean_swap_fraction,
        "kill_threshold_blocks": int(kill_threshold_blocks),
        "verdict": verdict,
        "interpretation": interpretation,
    }


# ═══════════════════════════════════════════════════════════
#  验证1: swap 检测 + 权重回滚 dwell time (Go/Kill hinge)
# ═══════════════════════════════════════════════════════════

class Form1CMA(StandardCMA2x2):
    """形态1 CMA: 检测 swap → 回滚权重到 pre-swap 快照 → 继续在线更新.

    机制:
      1. 每 block 算 corr(zX,sY), 若 > threshold 且 > corr(zX,sX) → swap 检测
      2. 检测到 swap 后, 权重回滚到 N_snapshot 块前的快照 (pre-swap 正确盆地)
      3. 回滚后 CMA 继续在线更新 (不冻结不压μ, 纯回滚)
      4. 记录每次回滚后的 dwell time (到下次 swap 检测的 block 数)

    与 R7 冻结/D026 压μ的区别:
      R7/D026: 检测 fade (h<阈值) → 响应 (冻结/压μ)
      形态1: 检测 swap (corr 跳变) → 响应 (回滚权重)
      不同检测对象 (swap vs fade), 不同响应 (回滚 vs 冻结/压μ)
    """

    def __init__(self, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK,
                 swap_threshold=SWAP_THRESHOLD_DEFAULT, snapshot_window=100,
                 detect_cooldown=10):
        super().__init__(n_tap=n_tap, mu=mu, R2=R2)
        self.swap_threshold = swap_threshold
        self.snapshot_window = snapshot_window
        self.detect_cooldown = detect_cooldown  # 回滚后冷却 block 数 (防立即重触发)

    def _snapshot(self):
        return (self.wxx.copy(), self.wxy.copy(),
                self.wyx.copy(), self.wyy.copy())

    def _restore(self, snap):
        self.wxx, self.wxy, self.wyx, self.wyy = (
            snap[0].copy(), snap[1].copy(), snap[2].copy(), snap[3].copy())

    def equalize_with_rollback(self, rX, rY, sX, sY, h_block_series=None,
                               block_size=CMA_BLOCK_SIZE):
        """块级 CMA + swap 检测 + 权重回滚."""
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

        # 快照缓冲 (滑动窗口): 存最近 snapshot_window 个 block 的权重快照
        from collections import deque
        snapshot_buffer = deque(maxlen=self.snapshot_window)

        rollback_events = []   # 每次 swap 检测+回滚的记录
        dwell_times = []       # 回滚后到下次 swap 的 dwell time
        last_rollback_block = None
        blocks_since_rollback = 0

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

            # CMA 梯度更新 (standard Godard, 含 z 因子)
            eX = self.R2 - np.abs(zx_blk) ** 2
            eY = self.R2 - np.abs(zy_blk) ** 2
            self.wxx += self.mu * np.mean((eX * zx_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * np.mean((eX * zx_blk)[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += self.mu * np.mean((eY * zy_blk)[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += self.mu * np.mean((eY * zy_blk)[:, None] * np.conj(rY_blk), axis=0)

            # 记录快照 (更新后)
            snapshot_buffer.append(self._snapshot())

            # swap 检测 (用本 block 输出算 corr)
            c_xsY = _abs_corr(zx_blk, sY[idx:idx + block_size])
            c_xsX = _abs_corr(zx_blk, sX[idx:idx + block_size])
            blocks_since_rollback += 1

            if (c_xsY > self.swap_threshold and c_xsY > c_xsX
                    and blocks_since_rollback > self.detect_cooldown
                    and len(snapshot_buffer) >= 1):
                # 记录回滚前 dwell time (上次回滚到这次 swap 检测)
                if last_rollback_block is not None:
                    dwell = blk - last_rollback_block
                    dwell_times.append({
                        'from_block': last_rollback_block,
                        'to_block': blk,
                        'dwell_blocks': int(dwell),
                    })

                # 回滚到 snapshot_window 块前的快照 (正确盆地)
                snap_idx = min(self.snapshot_window - 1, len(snapshot_buffer) - 1)
                rollback_snap = snapshot_buffer[0]  # 最早可用的快照 (window 块前)
                rollback_from_norm = self._norm()
                self._restore(rollback_snap)
                rollback_to_norm = self._norm()

                rollback_events.append({
                    'detect_block': int(blk),
                    'corr_zX_sY': float(c_xsY),
                    'corr_zX_sX': float(c_xsX),
                    'snapshot_age_blocks': snap_idx + 1,
                    'norm_before': float(rollback_from_norm),
                    'norm_after': float(rollback_to_norm),
                })
                last_rollback_block = blk
                blocks_since_rollback = 0
                # 清空快照缓冲 (回滚后重新积累)
                snapshot_buffer.clear()
                snapshot_buffer.append(self._snapshot())

            # 发散检测
            cur_norm = self._norm()
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
            'n_rollbacks': len(rollback_events),
            'rollback_events': rollback_events,
            'dwell_times': dwell_times,
        }


def run_v1_trial(seed, f_g=F_G_PRIMARY, n_symbols=N_SYMBOLS,
                 snapshot_window=100, threshold=SWAP_THRESHOLD_DEFAULT):
    """验证1: 单 seed × snapshot_window × threshold trial.

    三对照:
      A = standard-CMA (无回滚, baseline)
      B = 形态1 (检测+回滚)
      C = oracle
    """
    started = time.time()
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]

    rX, rY, sX, sY, h, theta = gen_channel(
        n_symbols, alpha, beta, f_g, SOP_RATE, int(seed))

    late = slice(LATE_START, LATE_END)
    source_x = sX[late]
    source_y = sY[late]

    # ── A: standard-CMA (baseline, 无回滚) ──
    eq_a = StandardCMA2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
    res_a = eq_a.equalize(rX, rY, block_size=CMA_BLOCK_SIZE)
    eval_a = evaluate_outputs(res_a['zX'][late], res_a['zY'][late],
                              source_x, source_y, res_a['diverged'])

    # ── B: 形态1 (检测+回滚) ──
    eq_b = Form1CMA(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK,
                    swap_threshold=threshold, snapshot_window=snapshot_window)
    res_b = eq_b.equalize_with_rollback(rX, rY, sX, sY, block_size=CMA_BLOCK_SIZE)
    eval_b = evaluate_outputs(res_b['zX'][late], res_b['zY'][late],
                              source_x, source_y, res_b['diverged'])

    # ── C: oracle ──
    oracle_x, oracle_y = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    eval_c = evaluate_outputs(oracle_x[late], oracle_y[late],
                              source_x, source_y, False)

    # dwell time 统计 (late 段内)
    late_start_block = (LATE_START - N_TAP // 2) // CMA_BLOCK_SIZE
    late_end_block = (LATE_END - N_TAP // 2) // CMA_BLOCK_SIZE
    late_dwells = [d['dwell_blocks'] for d in res_b['dwell_times']
                   if late_start_block <= d['from_block'] < late_end_block]
    late_rollbacks = [r for r in res_b['rollback_events']
                      if late_start_block <= r['detect_block'] < late_end_block]

    return {
        "seed": int(seed),
        "snapshot_window": int(snapshot_window),
        "threshold": float(threshold),
        "elapsed_s": time.time() - started,
        "A_standard_cma": {
            "pi_ber": float(eval_a["permutation_invariant_ber"]["mean"]),
            "fixed_ber": float(eval_a["fixed_label_ber"]["mean"]),
            "classification": eval_a.get("classification", "unknown"),
            "diverged": bool(res_a['diverged']),
        },
        "B_form1_rollback": {
            "pi_ber": float(eval_b["permutation_invariant_ber"]["mean"]),
            "fixed_ber": float(eval_b["fixed_label_ber"]["mean"]),
            "classification": eval_b.get("classification", "unknown"),
            "diverged": bool(res_b['diverged']),
            "n_rollbacks_total": int(res_b['n_rollbacks']),
            "n_rollbacks_late": int(len(late_rollbacks)),
            "dwell_median_late": float(np.median(late_dwells)) if late_dwells else None,
            "dwell_mean_late": float(np.mean(late_dwells)) if late_dwells else None,
            "dwell_min_late": int(np.min(late_dwells)) if late_dwells else None,
            "dwell_max_late": int(np.max(late_dwells)) if late_dwells else None,
            "dwell_values_late": late_dwells,
        },
        "C_oracle": {
            "pi_ber": float(eval_c["permutation_invariant_ber"]["mean"]),
            "fixed_ber": float(eval_c["fixed_label_ber"]["mean"]),
        },
    }


def run_v1_all_seeds(seeds, snapshot_window=100,
                     threshold=SWAP_THRESHOLD_DEFAULT, label=''):
    """验证1: 全 seeds × 单 snapshot_window."""
    trials = []
    for i, seed in enumerate(seeds):
        t = run_v1_trial(seed, snapshot_window=snapshot_window, threshold=threshold)
        trials.append(t)
        b = t['B_form1_rollback']
        a = t['A_standard_cma']
        dm = b['dwell_median_late']
        print(f"  [v1 {label} {i+1}/{len(seeds)}] seed={seed} snap={snapshot_window}: "
              f"A_pi={a['pi_ber']:.4f} B_pi={b['pi_ber']:.4f} "
              f"n_rollbacks={b['n_rollbacks_late']} dwell_med={dm} "
              f"B_class={b['classification']}", flush=True)
    return trials


def summarize_v1(trials, snapshot_window, kill_dwell_blocks=1000):
    """验证1 判定."""
    a_pis = [t["A_standard_cma"]["pi_ber"] for t in trials]
    b_pis = [t["B_form1_rollback"]["pi_ber"] for t in trials]
    c_pis = [t["C_oracle"]["pi_ber"] for t in trials]

    a_mean = float(np.mean(a_pis))
    b_mean = float(np.mean(b_pis))
    c_mean = float(np.mean(c_pis))

    # 配对比较
    wins = sum(1 for a, b in zip(a_pis, b_pis) if b < a)
    diffs = [a - b for a, b in zip(a_pis, b_pis)]
    nonzero_diffs = [d for d in diffs if abs(d) > 1e-9]
    p_value = None
    if len(nonzero_diffs) >= 3:
        try:
            stat, p_value = wilcoxon(diffs, alternative="greater")
            p_value = float(p_value)
        except Exception:
            p_value = None

    # dwell time 统计
    all_dwells = []
    for t in trials:
        all_dwells.extend(t["B_form1_rollback"]["dwell_values_late"])
    dwell_median = float(np.median(all_dwells)) if all_dwells else None

    # 改善比
    improvement_ratio = a_mean / max(b_mean, 1e-9) if b_mean > 0 else float('inf')

    # Go/Kill 判定 (FR-25 分离)
    sig = (p_value is not None and p_value < 0.05 and wins >= 4)
    big_gain = improvement_ratio >= 2.0
    has_window = (dwell_median is not None and dwell_median > 5000)

    kill_no_window = (dwell_median is not None and dwell_median < kill_dwell_blocks)
    no_improvement = not sig or not big_gain

    if sig and big_gain and has_window:
        verdict = "GO"
        interpretation = (
            f"GO: 形态1 PI-BER {b_mean:.4f} vs standard-CMA {a_mean:.4f} "
            f"({improvement_ratio:.1f}× 降), p={p_value:.4f}, {wins}/5 胜, "
            f"dwell 中位 {dwell_median:.0f} > 5000"
        )
    elif kill_no_window:
        verdict = "KILL"
        interpretation = (
            f"KILL: 回滚后 dwell 中位 {dwell_median:.0f} < {kill_dwell_blocks} 块 "
            f"(R7 阴影重合, CMA 立即再跳)"
        )
    elif no_improvement:
        verdict = "KILL"
        interpretation = (
            f"KILL: PI-BER 无显著改善 (form1 {b_mean:.4f} vs stdCMA {a_mean:.4f}, "
            f"{improvement_ratio:.1f}×, p={p_value}, {wins}/5 胜)"
        )
    else:
        verdict = "AMBIGUOUS"
        interpretation = (
            f"AMBIGUOUS: 部分满足 (sig={sig}, gain={big_gain}, window={has_window}), "
            f"dwell_med={dwell_median}, 须主控判断"
        )

    return {
        "snapshot_window": int(snapshot_window),
        "A_standard_cma_pi_mean": a_mean,
        "A_standard_cma_pi_values": a_pis,
        "B_form1_pi_mean": b_mean,
        "B_form1_pi_values": b_pis,
        "C_oracle_pi_mean": c_mean,
        "B_wins_vs_A": wins,
        "wilcoxon_p": p_value,
        "improvement_ratio_A_over_B": float(improvement_ratio),
        "dwell_median_all": dwell_median,
        "dwell_count": len(all_dwells),
        "n_rollbacks_late_total": sum(t["B_form1_rollback"]["n_rollbacks_late"] for t in trials),
        "verdict": verdict,
        "interpretation": interpretation,
    }


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def main(argv=None):
    parser = argparse.ArgumentParser(description='PROMPT-021: Q-DP4 形态1 (检测+回滚) MVE')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 seed, 500K symbols)')
    parser.add_argument('--v0-only', action='store_true',
                        help='只跑验证0 (swap 频率, Kill 门控前置)')
    parser.add_argument('--v1-only', action='store_true',
                        help='只跑验证1 (回滚 dwell time, 跳过验证0 门控)')
    parser.add_argument('--threshold', type=float, default=SWAP_THRESHOLD_DEFAULT,
                        help=f'swap 检测阈值 (默认 {SWAP_THRESHOLD_DEFAULT})')
    parser.add_argument('--snapshot', type=int, default=None,
                        help='单 snapshot window (默认扫 {100,500,1000})')
    parser.add_argument('--seeds', nargs='*', type=int, default=None)
    args = parser.parse_args(argv)

    t_global = time.time()

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (验证实现正确性, 1 seed 500K)")
        print("=" * 60)
        global LATE_START, LATE_END, N_SYMBOLS
        n_sym = 500_000
        LATE_START = int(n_sym * 0.875)
        LATE_END = n_sym
        N_SYMBOLS = n_sym
        print("\n--- V0 smoke ---")
        t0 = run_v0_swap_frequency(1000, n_symbols=n_sym, threshold=args.threshold)
        ss = t0['swap_stats']
        print(f"V0: n_events_late={ss['n_events_late']} "
              f"interval_med={ss['interval_median']} swap_frac={ss['swap_fraction']:.4f}")
        print("\n--- V1 smoke ---")
        t1 = run_v1_trial(1000, n_symbols=n_sym, snapshot_window=100, threshold=args.threshold)
        b = t1['B_form1_rollback']
        print(f"V1: A_pi={t1['A_standard_cma']['pi_ber']:.4f} "
              f"B_pi={b['pi_ber']:.4f} n_rollbacks={b['n_rollbacks_late']} "
              f"dwell_med={b['dwell_median_late']}")
        return

    seeds = args.seeds or SEEDS_5
    threshold = args.threshold

    payload = {
        "experiment": "PROMPT-021 Q-DP4 form-1 (detect+rollback) MVE",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "params": {
            "f_g_primary": F_G_PRIMARY, "turbulence": TURBULENCE,
            "n_symbols": N_SYMBOLS, "gamma_bar": GAMMA_BAR,
            "sop_rate": SOP_RATE, "mu_safe": MU_SAFE, "n_tap": N_TAP,
            "late_slice": [LATE_START, LATE_END],
            "cma_block_size": CMA_BLOCK_SIZE,
            "seeds": seeds,
            "swap_threshold_default": threshold,
            "snapshot_windows": SNAPSHOT_WINDOWS,
            "swap_thresholds_sweep": SWAP_THRESHOLDS,
        },
        "tl20_expectations": {
            "v0": "swap 间隔宽尾分布, 中位数百~数千块 (SOP 旋转驱动离散事件, 须实证)",
            "v1": "回滚后 dwell time 倾向不长 (代价地形多解不变 CMA 倾向再跳), 倾向 Kill 但须实证",
        },
        "preregistered_criteria": {
            "go": "form1 PI-BER < standard-CMA (p<0.05 + ≥4/5 胜) + 降 ≥2× + dwell 中位 > 5000 块",
            "kill": "v0 间隔中位 < 1000 块 OR v1 dwell 中位 < 1000 块 OR PI-BER 无改善",
            "no_oracle_go": "FR-25: 不用 oracle 当 Go 判据",
        },
    }

    run_v0 = not args.v1_only
    run_v1 = not args.v0_only

    # ── 验证0: swap 时间频率 (Kill 门控前置) ──
    v0_pass = True
    if run_v0:
        print("=" * 60)
        print(f"PROMPT-021 验证0: swap 时间频率 (Kill 门控前置, {len(seeds)} seeds)")
        print(f"参数: f_G={F_G_PRIMARY}, SOP={SOP_RATE}, N={N_SYMBOLS}, thr={threshold}")
        print("=" * 60)
        t0 = time.time()
        v0_trials = run_v0_all_seeds(seeds, threshold=threshold, label=f'thr{threshold}')
        v0_summary = summarize_v0(v0_trials)
        payload["v0_swap_frequency"] = {"trials": v0_trials, "summary": v0_summary,
                                        "elapsed_s": time.time() - t0}
        print(f"\nV0 判定: {v0_summary['verdict']}")
        print(f"  {v0_summary['interpretation']}")
        print(f"  total_events_late={v0_summary['total_events_late']} "
              f"interval_med={v0_summary['interval_median']} "
              f"swap_frac_mean={v0_summary['mean_swap_fraction_late']:.4f}")

        # Kill 门控
        if v0_summary['verdict'] == "KILL":
            v0_pass = False
            print("\n" + "=" * 60)
            print("验证0 KILL 门控触发: 形态1 无窗口, 跳过验证1")
            print("=" * 60)
            run_v1 = False

    # ── 验证1: swap 检测 + 权重回滚 dwell time ──
    if run_v1 and v0_pass:
        # 如果验证0 不是默认阈值跑的, 仍用默认阈值跑 v1
        print("\n" + "=" * 60)
        print(f"PROMPT-021 验证1: swap 检测 + 权重回滚 dwell time ({len(seeds)} seeds)")
        print(f"snapshot windows: {SNAPSHOT_WINDOWS}, threshold={threshold}")
        print("=" * 60)
        t1 = time.time()
        v1_by_snapshot = {}
        for snap in SNAPSHOT_WINDOWS:
            print(f"\n--- snapshot_window={snap} ---")
            v1_trials = run_v1_all_seeds(seeds, snapshot_window=snap,
                                         threshold=threshold, label=f'snap{snap}')
            v1_summary = summarize_v1(v1_trials, snap)
            v1_by_snapshot[f"snap_{snap}"] = {"trials": v1_trials, "summary": v1_summary}
            print(f"\nV1 (snap={snap}) 判定: {v1_summary['verdict']}")
            print(f"  {v1_summary['interpretation']}")
        payload["v1_rollback"] = {"by_snapshot": v1_by_snapshot,
                                  "elapsed_s": time.time() - t1}

        # 选最佳 snapshot
        best_snap = None
        best_pi = float('inf')
        for key, v in v1_by_snapshot.items():
            if v["summary"]["B_form1_pi_mean"] < best_pi:
                best_pi = v["summary"]["B_form1_pi_mean"]
                best_snap = key
        payload["v1_rollback"]["best_snapshot"] = best_snap
        payload["v1_rollback"]["best_summary"] = v1_by_snapshot[best_snap]["summary"]

    # ── swap 检测阈值敏感性 (验证0 用三档阈值重跑轻量版) ──
    if run_v0:
        print("\n" + "=" * 60)
        print(f"swap 检测阈值敏感性 ({SWAP_THRESHOLDS})")
        print("=" * 60)
        t_sens = time.time()
        sensitivity = {}
        for thr in SWAP_THRESHOLDS:
            sens_trials = run_v0_all_seeds(seeds, threshold=thr, label=f'thr{thr}')
            sens_summary = summarize_v0(sens_trials)
            sensitivity[f"thr_{thr}"] = {"summary": sens_summary}
            print(f"  thr={thr}: interval_med={sens_summary['interval_median']} "
                  f"verdict={sens_summary['verdict']}")
        payload["threshold_sensitivity"] = {"results": sensitivity,
                                            "elapsed_s": time.time() - t_sens}

    payload["elapsed_s"] = time.time() - t_global

    # ── 综合 Go/Kill 判定 ──
    consolidated = {"v0": None, "v1": None, "overall": None}
    if "v0_swap_frequency" in payload:
        consolidated["v0"] = payload["v0_swap_frequency"]["summary"]["verdict"]
    if "v1_rollback" in payload:
        best = payload["v1_rollback"].get("best_summary")
        if best:
            consolidated["v1"] = best["verdict"]

    if consolidated["v0"] == "KILL":
        consolidated["overall"] = "KILL (v0 无窗口)"
    elif consolidated["v1"] == "KILL":
        consolidated["overall"] = "KILL (v1 dwell 无窗口或无改善)"
    elif consolidated["v1"] == "GO":
        consolidated["overall"] = "GO (form1 有效)"
    elif consolidated["v0"] == "PASS" and consolidated["v1"] is None:
        consolidated["overall"] = "v0 PASS, v1 未跑"
    else:
        consolidated["overall"] = "见详细判定"
    payload["consolidated_verdict"] = consolidated

    # ── 保存 ──
    out_path = RESULT_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果保存: {out_path}")
    print(f"总耗时: {payload['elapsed_s']:.0f}s")

    # ── 汇总打印 ──
    print("\n" + "=" * 60)
    print("PROMPT-021 Q-DP4 形态1 (检测+回滚) MVE 汇总")
    print("=" * 60)
    print(f"验证0 (swap 频率): {consolidated['v0']}")
    print(f"验证1 (回滚 dwell): {consolidated['v1']}")
    print(f"综合判定: {consolidated['overall']}")

    return payload


if __name__ == '__main__':
    main()
