"""GG 深衰落前兆可辨识性分析 (PROMPT-017 前置可行性).

> 方向: Q-CMA-FADE (预测性 fade 检测可行性) | 状态: WIP | 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P4 只扩不改; 新分析=1新文件+0改动现有)

## 研究问题 (核心前置门控)

预测性 fade 检测→触发 DSP 恢复 这个方向是否物理可行? 关键判据:

  **GG 深衰落 (h<0.3) 发生前, 信道增益 h(t) 的下降趋势是否可辨识 (可预测)?**

  - 渐变型: h 在数百~数千 block 内平滑下降 → 预测窗口存在 → 方向可行
  - 突变型: h 在 1-2 block 内骤降 → 预测窗口不存在 → 方向死

只分析信道模型时间序列 (gg_time_envelope), **不训练 ML, 不跑均衡器**.

## 模型结构 (已读源码 common/_gg_time.py 核对)

gg_time_envelope 返回符号级 h(t):
  - 块内恒定 (每 block=100 符号一个 h 值) — np.repeat(h_blocks, block)
  - 块间 AR(1) 相关, ρ = exp(-Δt/τ_c), Δt = block·t_s = 100/2.5e9 = 40 ns
  - GG = big(α) × small(β), 各自独立 gar AR(1) (精确 Gamma 边缘)
  - "前兆"看的是块间 h 序列的趋势 (块内恒定, 无块内信息)

时间尺度 (block=100, t_s=1/2.5e9 → 1 block = 40 ns):
  - f_G=30 Hz:   τ_c=5.31 ms = 132629 block  (ρ=0.9999925)
  - f_G=100 Hz:  τ_c=1.59 ms = 39789 block   (ρ=0.9999748)
  - f_G=1000 Hz: τ_c=0.159 ms = 3979 block   (ρ=0.9997484)

## 序列长度 (重要修正)

任务默认 N=5M 符号 = 50000 block = 2.0 ms. 但 AR(1) 混合需序列长 ≫ τ_c 才能看
多个独立衰落谷; 慢 f_G 下 2 ms < τ_c 会卡初始瞬态 (整段 h 偏低). 因此本脚本对
每个 f_G 用 **自适应序列长度 = 15·τ_c**, 块级生成.

## 核心物理发现 (驱动指标设计)

块级 h 是 AR(1) 但 GG 边缘 (α=1.5/β=0.8, β<1 右偏重尾) 使单 block h 抖动远大于
AR(1) 平均斜率. 实测 f_G=100 典型衰落 (peak h≈0.65 → trough h≈0.24, 跨 ~450 block):

  |平滑窗|   下降斜率     块级噪声σ    趋势 SNR
     20       -0.00085/blk   0.00466/blk   0.18
    200       -0.00068/blk   0.00164/blk   0.42   ← 最佳
   1000       -0.00027/blk   0.00132/blk   0.20

  → **下降趋势斜率在所有平滑窗下都 < 块级噪声 (SNR<1)**. 块间 h 下降占比仅 ~50%
    (即与"掷硬币"无别, 非单调下降). 衰落是"在噪声中从上抖到底", 而非平滑 S 曲线.

因此前兆指标:
  1. **下降段长度** (peak→trough): 物理前兆上限 (h 从局部峰到触底的距离)
  2. **趋势 SNR**: 平滑下降斜率 / 块级斜率噪声 — 衡量下降能否从噪声分辨
  3. **可检测预警时间**: 因果 level-drop 检测器 (h_MA 比 SW block 前低 k·σ) 在触
     底前多少 block 首次报警 — 这是实际可用的预测窗口.

判据:
  - "可预测": 可检测预警 ≥50 block (2 μs) → 够做轻量响应
  - "突变型": 下降段 <5 block (0.2 μs)

用法:
  cd projects/simulation && python explore/cma-fade-divergence/fade_precursor_analysis.py
"""
import sys
import time
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope_blockwise, rho_from_tau_c
from common._config import BLOCK

# ─── 参数 ───────────────────────────────────────────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S
ALPHA, BETA = cfg.turbulence.as_dict()['strong']  # α=1.5, β=0.8

BLOCK_SIZE = BLOCK
BLOCK_DT = BLOCK_SIZE * T_S                        # 40 ns

F_G_VALUES = [30.0, 100.0, 1000.0]
SEEDS = list(range(1000, 1010))
METHOD = 'gar'
TAU_C_MULT = 15.0

DEEP_FADE_THR = 0.3
RECOVER_THR = 0.5
ENTER_MARGIN = 0.4                                 # 找下降起点回溯阈值

# 检测器参数
DET_SW = 200                                       # level-drop 检测平滑窗
DET_K = 3.0                                        # k-σ 阈值

PRED_THRESHOLDS = [50, 1000]
SUDDEN_THRESH = 5


def block_to_us(blk):
    return blk * BLOCK_DT * 1e6


def moving_avg(x, win):
    if win <= 1:
        return x.copy()
    kernel = np.ones(win) / win
    pad = win // 2
    xp = np.pad(x, pad, mode='reflect')
    return np.convolve(xp, kernel, mode='valid')[:len(x)]


# ─── 事件识别 ───────────────────────────────────────────────

def identify_fade_events(h_blocks, thr=DEEP_FADE_THR, recover=RECOVER_THR,
                         gap_merge=50):
    """识别深衰落谷底事件 (合并小 gap 的二次探底). 每事件取触底 h 最小点."""
    below = h_blocks < thr
    n = len(h_blocks)
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
    # 合并: 间隔 < gap_merge 视为同事件
    merged = []
    for reg in raw:
        if merged and reg[0] - merged[-1][1] < gap_merge:
            merged[-1] = [merged[-1][0], reg[1]]
            continue
        merged.append(reg)
    out = []
    for (s, e) in merged:
        seg = h_blocks[s:e]
        off = int(np.argmin(seg))
        out.append({
            'trough_idx': s + off, 'trough_h': float(h_blocks[s + off]),
            'start': s, 'end': e, 'width': e - s,
        })
    return out


def find_descent_peak(h_blocks, ev, margin=ENTER_MARGIN, lookback_max=20000):
    """触底前下降段的局部峰. 回溯找最后 h>margin 点; 找不到取范围内最大."""
    b = ev['trough_idx']
    lo = max(0, b - lookback_max)
    seg = h_blocks[lo:b + 1]
    high = np.where(seg > margin)[0]
    off = high[-1] if len(high) else int(np.argmax(seg))
    return lo + off, float(h_blocks[lo + off])


# ─── 单事件前兆分析 ─────────────────────────────────────────

def analyze_precursor(h_blocks, ev, ma, slope_sigma, noise_sigma_raw,
                      sw=DET_SW, k=DET_K):
    b = ev['trough_idx']
    peak_idx, peak_h = find_descent_peak(h_blocks, ev)
    descent_len = b - peak_idx

    # 下降段平滑趋势斜率 + SNR (用原始块级噪声, 平滑窗=sw)
    if descent_len > sw:
        trend_slope = (ma[b] - ma[peak_idx]) / descent_len
    elif descent_len > 1:
        trend_slope = (ma[b] - ma[peak_idx]) / descent_len
    else:
        trend_slope = float('nan')
    noise_ma = noise_sigma_raw / np.sqrt(sw)
    snr = abs(trend_slope) / noise_ma if noise_ma > 0 else float('inf')

    # 因果 level-drop 检测: 从触底向前找 ma[i]-ma[i-sw] < -k*noise_ma 的最早点
    sig_ma = noise_sigma_raw / np.sqrt(sw)
    thresh = k * sig_ma
    det_lead = 0
    i = b
    while i - sw >= 0:
        drop = ma[i] - ma[i - sw]
        if drop < -thresh:
            det_lead = b - i
            break
        i -= 1

    h_at = {}
    for d in [1, 5, 10, 50, 100]:
        idx = b - d
        h_at[d] = float(h_blocks[idx]) if idx >= 0 else float('nan')

    return {
        'peak_idx': peak_idx, 'peak_h': peak_h,
        'descent_len': descent_len,
        'descent_drop': float(peak_h - ev['trough_h']),
        'trend_slope': float(trend_slope),
        'snr': float(snr),
        'det_lead': int(det_lead),
        'h_at': h_at,
        'trough_idx': b, 'trough_h': ev['trough_h'],
        'width': ev['width'],
    }


def estimate_noise(h_blocks):
    """块级 h 差分噪声 σ (平稳高 h 段)."""
    high = h_blocks > 0.7
    if high.sum() < 100:
        high = h_blocks > 0.5
    d = np.diff(h_blocks[high])
    return float(np.std(d)) if len(d) > 10 else 1e-12


# ─── 单 seed 分析 ───────────────────────────────────────────

def run_one(f_g, seed, n_blocks, sw=DET_SW):
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    hb = gg_time_envelope_blockwise(
        n_blocks, ALPHA, BETA, tau_c, block=BLOCK_SIZE, t_s=T_S,
        method=METHOD, seed=seed)
    events = identify_fade_events(hb)
    if not events:
        return hb, []
    noise = estimate_noise(hb)
    ma = moving_avg(hb, sw)
    # 块级短窗斜率噪声 (供参考)
    short_slope_sigma = np.std(np.diff(moving_avg(hb, 20))[hb[:-1] > 0.7]) \
        if (hb > 0.7).sum() > 50 else 1e-12
    infos = [analyze_precursor(hb, ev, ma, short_slope_sigma, noise, sw)
             for ev in events]
    return hb, infos


def aggregate(seed_results):
    all_infos = [info for infos in seed_results for info in infos]
    n_events = len(all_infos)
    if n_events == 0:
        return {'n_events': 0}
    desc = np.array([info['descent_len'] for info in all_infos])
    det = np.array([info['det_lead'] for info in all_infos])
    snr = np.array([info['snr'] for info in all_infos])
    widths = np.array([info['width'] for info in all_infos])
    trough_h = np.array([info['trough_h'] for info in all_infos])
    return {
        'n_events': n_events,
        'descent_med': float(np.median(desc)),
        'descent_p25': float(np.percentile(desc, 25)),
        'descent_p75': float(np.percentile(desc, 75)),
        'pred50_descent': float(np.mean(desc >= 50)),
        'pred1000_descent': float(np.mean(desc >= 1000)),
        'det_med': float(np.median(det)),
        'pred50_detect': float(np.mean(det >= 50)),
        'pred1000_detect': float(np.mean(det >= 1000)),
        'snr_med': float(np.median(snr)),
        'snr_mean': float(np.mean(snr)),
        'snr_gt1_frac': float(np.mean(snr > 1.0)),
        'sudden_frac': float(np.mean(desc < SUDDEN_THRESH)),
        'width_med': float(np.median(widths)),
        'trough_h_med': float(np.median(trough_h)),
    }


def main():
    t0 = time.time()
    print("=" * 84)
    print("PROMPT-017 前置: GG 深衰落前兆可辨识性分析")
    print("=" * 84)
    print(f"参数: α={ALPHA}, β={BETA} (strong), method={METHOD}")
    print(f"block={BLOCK_SIZE}, t_s={T_S*1e9:.2f} ns → 1 block = "
          f"{BLOCK_DT*1e9:.0f} ns = {BLOCK_DT*1e6:.3f} μs")
    print(f"f_G ∈ {F_G_VALUES} Hz, {len(SEEDS)} seeds ({SEEDS[0]}-{SEEDS[-1]})")
    print(f"序列长度 = {TAU_C_MULT}·τ_c; 深衰落 h<{DEEP_FADE_THR}, 分离 recover>{RECOVER_THR}")
    print(f"检测器: level-drop, SW={DET_SW} block, k={DET_K}σ")

    fg_nblocks = {}
    for f_g in F_G_VALUES:
        tau_c = cfg.gg_time.tau_c_from_fg(f_g)
        nb = int(TAU_C_MULT * tau_c / BLOCK_DT)
        fg_nblocks[f_g] = nb
        rho = rho_from_tau_c(tau_c, BLOCK_SIZE, T_S)
        print(f"\n  f_G={f_g:>5.0f} Hz: τ_c={tau_c*1e3:7.3f} ms = "
              f"{tau_c/BLOCK_DT:8.0f} block, ρ={rho:.7f}, "
              f"n_blocks={nb} ({nb*BLOCK_DT*1e3:.1f} ms)")

    summary = {}
    typical = {}
    for f_g in F_G_VALUES:
        nb = fg_nblocks[f_g]
        print("\n" + "-" * 84)
        print(f"f_G = {f_g} Hz  (n_blocks={nb}, {nb*BLOCK_DT*1e3:.1f} ms)")
        print("-" * 84)
        per_seed = []
        example = None
        for seed in SEEDS:
            ts = time.time()
            hb, infos = run_one(f_g, seed, nb)
            per_seed.append(infos)
            print(f"  seed {seed}: {len(infos):3d} 事件, "
                  f"h 中位={np.median(hb):.3f}, "
                  f"P(<0.3)={np.mean(hb<DEEP_FADE_THR):.3f} "
                  f"({time.time()-ts:.1f}s)")
            if infos and example is None:
                cand = sorted(infos, key=lambda x: x['descent_len'])
                example = (seed, cand[len(cand)//2])

        agg = aggregate(per_seed)
        summary[f_g] = agg
        typical[f_g] = example
        if agg['n_events'] == 0:
            print("  → 无深衰落事件")
            continue
        print(f"\n  汇总 ({agg['n_events']} 事件 / {len(SEEDS)} seeds):")
        print(f"    下降段长度 中位: {agg['descent_med']:.0f} block = "
              f"{block_to_us(agg['descent_med']):.1f} μs  "
              f"[P25 {agg['descent_p25']:.0f}, P75 {agg['descent_p75']:.0f}]")
        print(f"    下降段 ≥50 block (2μs) 占比:    {agg['pred50_descent']:.1%}")
        print(f"    下降段 ≥1000 block (40μs) 占比:  {agg['pred1000_descent']:.1%}")
        print(f"    可检测预警(level-drop) 中位: {agg['det_med']:.0f} block = "
              f"{block_to_us(agg['det_med']):.1f} μs")
        print(f"    可检测预警 ≥50block 占比:       {agg['pred50_detect']:.1%}")
        print(f"    可检测预警 ≥1000block 占比:     {agg['pred1000_detect']:.1%}")
        print(f"    趋势 SNR 中位/均值: {agg['snr_med']:.2f}/{agg['snr_mean']:.2f}  "
              f"(SNR>1 占比 {agg['snr_gt1_frac']:.1%})")
        print(f"    突变型 (<{SUDDEN_THRESH} block) 占比: {agg['sudden_frac']:.1%}")
        print(f"    谷底宽度中位: {agg['width_med']:.0f} block = "
              f"{block_to_us(agg['width_med']):.1f} μs")

    # ─── 汇总表 ───
    print("\n" + "=" * 84)
    print("【汇总表】 (每 f_G 一行;  block=40ns, 50blk=2μs)")
    print("=" * 84)
    hdr = (f"{'f_G(Hz)':>8} {'事件数':>6} {'下降段中位':>10} {'(μs)':>7} "
           f"{'下降≥50b':>8} {'可检测≥50b':>10} {'SNR中位':>7} {'突变占比':>8}")
    print(hdr)
    print("-" * len(hdr))
    for f_g in F_G_VALUES:
        a = summary[f_g]
        if a['n_events'] == 0:
            print(f"{f_g:>8.0f} {'0':>6} {'—':>10} {'—':>7} {'—':>8} "
                  f"{'—':>10} {'—':>7} {'—':>8}")
            continue
        print(f"{f_g:>8.0f} {a['n_events']:>6d} {a['descent_med']:>10.0f} "
              f"{block_to_us(a['descent_med']):>6.1f} "
              f"{a['pred50_descent']:>7.1%} {a['pred50_detect']:>9.1%} "
              f"{a['snr_med']:>7.2f} {a['sudden_frac']:>7.1%}")
    print("\n  注: '下降段中位/≥50b' = 物理前兆上限 (peak→trough); "
          "'可检测≥50b' = 因果 level-drop 检测器(3σ)提前≥50block 报警比例")

    # ─── 典型事件前兆轨迹 ───
    print("\n" + "=" * 84)
    print("【典型 fade 事件前兆轨迹】 (peak → trough, 稀疏采样)")
    print("=" * 84)
    for f_g in F_G_VALUES:
        ex = typical.get(f_g)
        if ex is None:
            print(f"\nf_G={f_g} Hz: 无事件")
            continue
        seed, info = ex
        tau_c = cfg.gg_time.tau_c_from_fg(f_g)
        nb = fg_nblocks[f_g]
        hb = gg_time_envelope_blockwise(
            nb, ALPHA, BETA, tau_c, block=BLOCK_SIZE, t_s=T_S,
            method=METHOD, seed=seed)
        p, b = info['peak_idx'], info['trough_idx']
        desc = info['descent_len']
        seg = hb[p:b + 1]
        mono_neg = float(np.mean(np.diff(seg) < 0)) if len(seg) > 5 else float('nan')
        print(f"\nf_G={f_g} Hz (seed {seed}): peak@{p} (h={info['peak_h']:.3f}) "
              f"→ trough@{b} (h={info['trough_h']:.3f})")
        print(f"  下降段 {desc} block = {block_to_us(desc):.1f} μs, "
              f"趋势斜率 {info['trend_slope']:+.5f}/block, SNR={info['snr']:.2f}, "
              f"可检测预警 {info['det_lead']} block")
        print(f"  块间 h↓ 占比: {mono_neg:.0%} "
              f"({'近单调下降' if mono_neg>0.6 else '抖动为主(≈掷硬币)'})")
        fracs = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
        print("  位置(peak起)   block(rel peak)   h")
        for fr in fracs:
            idx = int(p + (b - p) * (1 - fr))
            print(f"  {fr:>4.1f}          {idx-p:>+6d}            {hb[idx]:.3f}")

    print(f"\n总耗时: {time.time()-t0:.1f}s")
    return summary


if __name__ == '__main__':
    main()
