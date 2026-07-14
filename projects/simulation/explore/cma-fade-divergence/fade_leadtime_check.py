"""因果 fade 检测器预警提前量 (warning lead time) 量化.

> 方向: Q-CMA-FADE (Step B, PROMPT-017 续) | 状态: WIP | 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P4 只扩不改; 新分析=1新文件+0改动现有)

## 研究问题 (上一轮结论的延伸)

上一轮 (fade_precursor_analysis.py) 确认: fade 触底前约 55% 事件有统计显著的
下降趋势 (p<0.05). 但"有趋势" ≠ "能提前报警". 本脚本量化 **预警提前量**
(warning lead time): 一个因果检测器在 trough 前多少 block 首次触发.

## 检测器设计 (因果)

- 对平滑序列 sm (uniform_filter1d, size=200), 在每个 block t 处用
  sm[t-200 : t+1] (201 个点) 做线性回归.
- 触发条件: slope<0 且 p<0.01 (显著下降).
- 因果性: t 处的检测只看 t 及之前的数据 (无未来泄漏).
- lead time = trough_idx - t_first_trigger (t_first_trigger 是最后一个满足条件的点
  离 trough 多远 — 用"trough 前 (slope<0 且 p<0.01) 的连续触发段最远端").

  具体实现: 因为我们关心"trough 前检测器持续多久报警", 取 trough 前最近的触发点 t*,
  然后回溯找到最早的连续触发点 t0 (t0..t* 都触发, t0-1 不触发), lead = trough - t0.
  这样度量的是"信号持续显著下降"的最早可检测时刻, 而非最后一个抖动点.

## 性能优化 (关键)

不逐 block 逐 trough 回归. 而是:
  1. 预处理: 向量化算"每个 block 的 201-窗回归 slope + p 值" (用卷积/累积和).
     - slope[t] 用 O(1) 增量 (cumsum 预计算 Σx,Σy,Σxy,Σx²).
     - p 值由 t 统计量 = |slope| / SE_slope, SE_slope = sqrt(MSE / S_xx), 查正态近似.
  2. 每 trough 查询: 在触发数组上找连续段 → O(段长), 但段长平均小, 总开销 << 全扫描.
  整体 O(n_blocks) 预处理 + 近似 O(1) 每 trough. 3 seed × ~600k block < 数秒.

## 参数 (单点, 不扩)
  f_G=100 Hz, α=1.5/β=0.8 (strong), t_s=1/2.5e9, BLOCK=100
  τ_c=1/(2π·100)≈1.59ms, 序列=15·τ_c 的 block 数, seeds=1000,1001,1002

## 时间换算 (BLOCK=100, t_s=0.4ns → 1 block = 40ns)
  50 blocks = 2µs, 200 blocks = 8µs, 1000 blocks = 40µs

用法:
  cd projects/simulation && python explore/cma-fade-divergence/fade_leadtime_check.py
"""
import sys
import time
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from scipy.stats import norm
from scipy.ndimage import uniform_filter1d
from common._gg_time import gg_time_envelope_blockwise
from common._config import BLOCK
from params import SimulationConfig

# ─── 参数 ───────────────────────────────────────────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S
ALPHA, BETA = cfg.turbulence.as_dict()['strong']  # (1.5, 0.8)

BLOCK_DT = BLOCK * T_S  # 40 ns

F_G = 100.0
TAU_C = 1.0 / (2.0 * np.pi * F_G)           # 1.59 ms
N_BLOCKS = int(15.0 * TAU_C / BLOCK_DT)      # ~596831
SEEDS = [1000, 1001, 1002]
METHOD = 'gar'

# 事件识别
DEEP_FADE_THR = 0.3
GAP_MERGE = 50

# 检测器
SMOOTH_WIN = 200                              # 平滑窗
REG_WIN = 201                                 # 回归窗 (含 t, 看 t-200..t)
P_THR = 0.01                                  # 显著性阈值
Z_THR = norm.ppf(1.0 - P_THR / 2.0)           # 双侧 z (slope<0 用单侧, 这里用双侧近似保守)

# 提前量阈值 (blocks → µs)
LEAD_THRESH = [50, 200, 1000]


def block_to_us(blk):
    return blk * BLOCK_DT * 1e6


# ─── 向量化回归: 每个 block 的 REG_WIN-窗 slope + p ─────────

def vectorized_regression_signals(y, win=REG_WIN):
    """对平滑序列 y, 算每个 t (win-1 <= t < n) 的 win-窗线性回归 slope + z.

    回归窗 = [t-win+1, t] (含 t, 共 win 个点), 因果 (不看 t 之后).
    x_local = arange(win) 是 **窗内局部** 索引 (0..win-1), 不是全局索引.

    slope = (win·Σxy − Σx·Σy) / (win·Σx² − (Σx)²)
    残差 → MSE → SE_slope = sqrt(MSE / S_xx)
    z = slope / SE_slope (slope<0 显著 ⇔ z < -z_thr)

    向量化:
      Sy, Syy 用前缀和 (窗 [a,b), a=t-win+1, b=t+1).
      Sxy_local = Σ_{k=0}^{win-1} k·y[a+k] 用核卷积 (kk=[0,1,...,win-1] 翻转),
        Sxy_local[a] = sum_k k·y[a+k], 卷积 mode='valid' 长度 n-win+1.
    """
    n = len(y)
    x = np.arange(win, dtype=float)
    Sx = x.sum()
    Sxx = (x * x).sum()
    denom = win * Sxx - Sx * Sx              # = win²·(win²-1)/12

    # 前缀和: Sy, Syy
    cy = np.concatenate(([0.0], np.cumsum(y)))
    cyy = np.concatenate(([0.0], np.cumsum(y * y)))
    # Sxy_local: 核卷积 (局部索引 0..win-1)
    kk = np.arange(win, dtype=float)
    Sxy_local = np.convolve(y, kk[::-1], mode='valid')   # 长 n-win+1, 对应 a=0..n-win

    valid = np.arange(win - 1, n)            # t 的合法范围 (win-1..n-1)
    t = valid
    a = t - win + 1                          # 窗起 (含), 与 Sxy_local 索引一致
    b = t + 1                                # 窗止 (不含)
    Sy = cy[b] - cy[a]
    Syy = cyy[b] - cyy[a]
    Sxy = Sxy_local[a]                       # a 是窗起点索引

    slope = (win * Sxy - Sx * Sy) / denom
    # 拟合值残差 SSE = Syy - slope·Sxy - intercept·Sy
    intercept = (Sy - slope * Sx) / win
    sse = Syy - slope * Sxy - intercept * Sy
    sse = np.maximum(sse, 1e-30)             # 防 0
    dof = win - 2
    mse = sse / dof
    # SE_slope = sqrt(MSE / S_xx), S_xx = Σ(x-x̄)² = Sxx - Sx²/win = denom/win
    Sxx_cent = denom / win
    se_slope = np.sqrt(mse / Sxx_cent)
    z = slope / se_slope                     # 正负号反映 slope 方向

    # 输出全长数组, 前 win-1 个置 nan
    slope_full = np.full(n, np.nan)
    z_full = np.full(n, np.nan)
    slope_full[t] = slope
    z_full[t] = z
    return slope_full, z_full


# ─── 事件识别 (复用 fade_precursor_analysis 思路) ───────────

def identify_troughs(h, thr=DEEP_FADE_THR, gap_merge=GAP_MERGE):
    """找所有深衰落 trough (h<thr 连续区间内 argmin), 合并近邻 gap."""
    below = h < thr
    n = len(h)
    raw = []
    i = 0
    while i < n:
        if below[i]:
            j = i
            while j < n and below[j]:
                j += 1
            raw.append([i, j])
            i = j
        else:
            i += 1
    merged = []
    for reg in raw:
        if merged and reg[0] - merged[-1][1] < gap_merge:
            merged[-1] = [merged[-1][0], reg[1]]
            continue
        merged.append(reg)
    troughs = []
    for (s, e) in merged:
        off = int(np.argmin(h[s:e]))
        troughs.append(s + off)
    return troughs


# ─── lead time 查询 ─────────────────────────────────────────

def lead_time_for_trough(triggered, trough_idx, reg_win=REG_WIN):
    """trough 前最近触发点 t*, 回溯找最早连续触发 t0.

    triggered: bool 数组 (slope<0 且显著).
    返回 lead = trough_idx - t0 (blocks). 若 trough 前无触发, 返回 0.
    排除 trough 自身及 trough 后的点 (因果: 不能用 trough 时刻).
    """
    t_end = trough_idx - 1                   # 不含 trough (检测器在 trough 时已太晚)
    if t_end < reg_win - 1:
        return 0
    # 从 t_end 向前找最近触发点
    t_star = t_end
    while t_star >= reg_win - 1 and not triggered[t_star]:
        t_star -= 1
    if t_star < reg_win - 1:
        return 0
    # 从 t_star 向前找连续触发段起点
    t0 = t_star
    while t0 - 1 >= reg_win - 1 and triggered[t0 - 1]:
        t0 -= 1
    return trough_idx - t0


# ─── 主流程 ─────────────────────────────────────────────────

def run():
    t0 = time.time()
    print(f"f_G={F_G} Hz, α={ALPHA}/β={BETA} (strong), τ_c={TAU_C*1e3:.3f} ms")
    print(f"N_BLOCKS={N_BLOCKS} ({N_BLOCKS*BLOCK_DT*1e3:.2f} ms), "
          f"SMOOTH_WIN={SMOOTH_WIN}, REG_WIN={REG_WIN}, p<{P_THR}")
    print(f"z_thr(双侧 p<{P_THR})={Z_THR:.3f}")
    print("-" * 70)

    all_leads = []
    n_events_per_seed = []
    for seed in SEEDS:
        h = gg_time_envelope_blockwise(N_BLOCKS, ALPHA, BETA, TAU_C,
                                       block=BLOCK, t_s=T_S, method=METHOD,
                                       seed=seed)
        sm = uniform_filter1d(h, size=SMOOTH_WIN)

        slope, z = vectorized_regression_signals(sm, REG_WIN)
        triggered = (slope < 0) & (z < -Z_THR) & ~np.isnan(z)

        troughs = identify_troughs(h)
        leads = [lead_time_for_trough(triggered, tb, REG_WIN) for tb in troughs]
        leads = np.array(leads, dtype=float)

        all_leads.append(leads)
        n_events_per_seed.append(len(troughs))
        print(f"seed {seed}: {len(troughs)} fade events, "
              f"lead median={np.median(leads):.0f}, "
              f"mean={np.mean(leads):.0f}, "
              f"P(≥50)={np.mean(leads>=50)*100:.0f}%, "
              f"P(≥200)={np.mean(leads>=200)*100:.0f}%")

    all_leads_cat = np.concatenate(all_leads)
    total_events = int(all_leads_cat.size)
    print("-" * 70)
    print(f"总 fade 事件数 (3 seed 合计): {total_events}")
    print(f"  per seed: {n_events_per_seed}")
    print()
    print("Lead time 分布 (blocks):")
    med = np.median(all_leads_cat)
    mean = np.mean(all_leads_cat)
    print(f"  median = {med:.0f} blocks ({block_to_us(med):.1f} µs)")
    print(f"  mean   = {mean:.0f} blocks ({block_to_us(mean):.1f} µs)")
    for L in LEAD_THRESH:
        p = np.mean(all_leads_cat >= L)
        print(f"  P(lead ≥ {L} blocks = {block_to_us(L):.0f}µs) = {p*100:.1f}%")
    p0 = np.mean(all_leads_cat == 0)
    print(f"  P(lead = 0, 未提前报警) = {p0*100:.1f}%")
    print()
    print(f"时间换算: 1 block = {BLOCK_DT*1e9:.0f} ns; "
          f"50 blk=2µs, 200 blk=8µs, 1000 blk=40µs")
    print(f"耗时: {time.time()-t0:.1f}s")


if __name__ == '__main__':
    run()
