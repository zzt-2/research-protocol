"""LCR 驱动发散的物理机制验证 — R4 修正后续。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)

验证 "LCR 越高越易发散" (R4 修正: 固定 μ=1e-3 后 P_div vs LCR r=+0.88) 的物理机制。

## 假设
  H1 (重收敛累积): 每次衰落恢复后 CMA 需重新收敛。衰落期间 h→0 权重被噪声
    扰动 (drift); 恢复后 h 突变回正常, CMA 收敛过程叠加新扰动。高 LCR =
    频繁"收敛-打断-重收敛"循环 → 累积漂移超阈值 → 发散。
  H2 (边沿梯度突变): h 从低到高跳变时接收信号幅度突变, CMA 误差 e=R²-|z|²
    突然变大 → 梯度 ∇w 突变 → 权重跳变。高 LCR = 更多跳变点。

## TL-20 可证伪预测
  - H1 成立 → 发散集中在衰落恢复沿 (up-cross) 之后若干 block
  - H2 成立 → 发散在 h 跳变点下一个 block 更新触发
  - 两者都不是 → 发散分布与衰落事件位置无关 (LCR 伪相关)

## 三个任务
  1. 重跑 CMA 记录完整 w_norm_traj + z_amp_traj, 定位 diverge_idx vs 衰落事件
  2. 分析 diverge_idx 位置分布 (衰落内部/恢复沿/边沿/正常区) + 到最近 up-cross 距离
  3. 剂量-效应: 固定 μ=5e-3 扫 f_G=[10,30,100,300,1000,3000]Hz, 看 P_div vs LCR

用法:
  cd projects/simulation && python explore/cma-fade-divergence/r_lcr_mechanism.py
"""
import sys
import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict

# 路径设置: 确保从 projects/simulation/ 运行
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._config import BLOCK

# fade_statistics 在 gg_time_fading_model.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gg_time_fading_model import fade_statistics


# ─── 参数 (从 params.py 读, FR-20 P3) ─────────────────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S
BLOCK_SIZE = BLOCK  # 100
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 (20 dB)
R2_QPSK = 1.0

# R4 修正参数: SOP_RATE=4e-7 rad/sym = 1 krad/s (sat.1553 §6.3 真实值)
SOP_RATE = 4e-7

# 关键组合 (任务 1/2)
TURB_STRONG = cfg.turbulence.as_dict()['strong']  # (1.5, 0.8)
N_SYMBOLS = 5_000_000  # 5M 够看位置模式
N_BLOCKS = N_SYMBOLS // BLOCK_SIZE  # 50000
N_TRIALS = 10
N_TAP = 11

# 衰落阈值
THR_DEEP = 0.1
THR_MODERATE = 0.3

# 剂量-效应 (任务 3)
F_G_DOSE = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
MU_DOSE = 5e-3  # 临界区, 有发散但不全部

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'

# CMA 内部并行化块大小 (sat.1553 §6.3 L756 "parallelization factor of 64")
# 注意: 这是 CMA 权重更新粒度, 与信道块 BLOCK_SIZE(100) 不同。
# w_norm_traj 是逐符号数组, 但仅在 CMA 块末位置 (idx = blk*64 + 64-1 + half) 非零。
CMA_BLOCK = 64

# 发散判据 (跟 _cma.py 一致, 用于重新扫轨迹找发散块)
# 这里不重新判发散, 直接用 res['diverged']/res['diverge_idx']


def w_traj_at_block(w_traj, chan_blk, block_size=BLOCK_SIZE):
    """取 w_norm_traj 在信道块 chan_blk 处的最近非零样本。

    w_traj 仅在 CMA 块末位置非零 (间隔 CMA_BLOCK=64 符号)。信道块 chan_blk
    对应符号区间 [chan_blk*block_size, (chan_blk+1)*block_size)。取该区间内
    最后一个非零 w_traj 样本 (即该信道块末尾的权重范数)。
    """
    sym_lo = chan_blk * block_size
    sym_hi = min((chan_blk + 1) * block_size, len(w_traj))
    if sym_hi <= sym_lo:
        return None
    seg = w_traj[sym_lo:sym_hi]
    nz = seg[seg > 0]
    return float(nz[-1]) if len(nz) > 0 else None


# ─── QPSK + 信道生成 (跟 cma_divergence_scan.py / r4_corrected 一致) ───

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1 (sat.1553 §6)。"""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)


def gen_channel(alpha, beta, f_g, seed, n_symbols=None):
    """生成 h 包络 + 双偏振信号 (1 krad/s SOP)。

    返回 (h, rX, rY)。跟 r4_corrected_sop_rate.run_single_trial 一致。
    """
    rng = np.random.default_rng(seed)
    N = n_symbols if n_symbols is not None else N_SYMBOLS
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK_SIZE,
                         t_s=T_S, method='gar', seed=seed)
    s = gen_qpsk(N, rng)
    sY = gen_qpsk(N, rng)
    noise_var = 1.0 / (2 * GAMMA_BAR)
    noise_X = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    noise_Y = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    theta = SOP_RATE * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    rX = np.sqrt(h) * (cos_t * s + sin_t * sY) + noise_X
    rY = np.sqrt(h) * (-sin_t * s + cos_t * sY) + noise_Y
    return h, rX, rY


# ─── 衰落事件检测 (down-cross / up-cross) ─────────────────────

def detect_fade_events(h_blocks, thr):
    """检测块级 h 序列的下穿/上穿事件。

    down_cross: h[k-1] >= thr 且 h[k] < thr  (衰落开始)
    up_cross:   h[k-1] < thr 且 h[k] >= thr  (衰落恢复)

    返回 (down_cross_blocks, up_cross_blocks) — 块索引数组。
    """
    below = h_blocks < thr
    down_cross = np.where(below[1:] & ~below[:-1])[0] + 1  # 块索引
    up_cross = np.where(~below[1:] & below[:-1])[0] + 1
    return down_cross, up_cross


def classify_diverge_location(diverge_idx, h_blocks, thr,
                              edge_win=1, recovery_win=100):
    """分类 diverge_idx 相对衰落事件的位置。

    判据 (按优先级):
      - 'edge':      diverge 在 down/up-cross **当块或之后** edge_win 个 block 内 → H2
                     (diverge 必须 >= cross_blk; cross 之前的 diverge 仍在衰落内部)
      - 'inside':    diverge 时 h<thr (衰落内部)
      - 'recovery':  diverge 在 up-cross 后 recovery_win 个 block 内 (非 edge) → H1
      - 'normal':    远离任何事件 (h>thr 且不在恢复窗) → 两者都不支持

    物理约定: CMA 在 block k 用 block k 信号算梯度、更新权重。h 跳变
    (up/down-cross) 发生在 block k, 发散在 block k 的权重更新触发 → diverge_blk ≈ k。

    返回 (category, dist_to_nearest_upcross)。
    dist_to_nearest_upcross: diverge 块到最近 up-cross 的绝对 block 数 (None 若无事件)。
    """
    div_blk = diverge_idx // BLOCK_SIZE
    n_blk = len(h_blocks)

    down_cross, up_cross = detect_fade_events(h_blocks, thr)

    # diverge 处的 h 值
    if 0 <= div_blk < n_blk:
        h_at_div = h_blocks[div_blk]
    else:
        return 'out_of_range', None

    # 最近 up-cross 绝对距离 (输出用)
    if len(up_cross) > 0:
        dist_up_abs = int(np.min(np.abs(up_cross - div_blk)))
    else:
        dist_up_abs = None

    # H2 edge: diverge 在 cross 当块或之后 edge_win 内 (signed: div_blk - cross ∈ [0, edge_win])
    def _edge_after(cross_idx):
        if len(cross_idx) == 0:
            return False
        delta = div_blk - cross_idx  # 正 = diverge 在 cross 之后
        return bool(np.any((delta >= 0) & (delta <= edge_win)))

    if _edge_after(down_cross):
        return 'edge_down', dist_up_abs
    if _edge_after(up_cross):
        return 'edge_up', dist_up_abs

    # inside fade
    if h_at_div < thr:
        return 'inside_fade', dist_up_abs

    # H1 recovery: diverge 在 up-cross 之后 (过了 edge) recovery_win 内
    if len(up_cross) > 0:
        delta_up = div_blk - up_cross
        if np.any((delta_up > edge_win) & (delta_up <= recovery_win)):
            return 'recovery', dist_up_abs

    # normal
    return 'normal', dist_up_abs


# ─── 任务 1+2: 重跑 CMA 记录轨迹 + 定位 ──────────────────────

def run_position_analysis():
    """任务 1+2: 关键组合 (2 f_G × 2 μ × 10 seeds), 记录轨迹 + 发散位置。

    返回位置分布统计 + diverge-to-upcross 距离分布 + 漂移对比。
    """
    configs = []
    for f_g in [30.0, 1000.0]:
        for mu in [5e-3, 1e-2]:
            configs.append((f_g, mu))
    total = len(configs) * N_TRIALS
    print(f"\n[任务 1+2] 关键组合位置分析: {len(configs)} combos × {N_TRIALS} seeds = {total} runs")
    print(f"  N_symbols={N_SYMBOLS}, SOP_RATE={SOP_RATE} rad/sym ({SOP_RATE*2.5e9/1e3:.0f} krad/s)")
    print(f"  configs: {[(fg, f'{mu:.0e}') for fg, mu in configs]}")

    alpha, beta = TURB_STRONG
    trials = []
    run_count = 0
    t_start = time.time()

    for f_g, mu in configs:
        for trial in range(N_TRIALS):
            seed = hash(('lcr_mech', f_g, mu, N_TAP, trial)) % (2 ** 32)
            h, rX, rY = gen_channel(alpha, beta, f_g, seed)
            eq = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
            res = eq.equalize(rX, rY)

            diverged = res['diverged']
            diverge_idx = res['diverge_idx']
            w_traj = res['w_norm_traj']
            init_norm = res['init_w_norm']

            # 块级 h + 事件
            h_blocks = h[::BLOCK_SIZE]

            # 对 thr=0.3 和 thr=0.1 都分类
            loc_mod, dist_up_mod = (None, None)
            loc_deep, dist_up_deep = (None, None)
            if diverged and diverge_idx is not None:
                loc_mod, dist_up_mod = classify_diverge_location(
                    diverge_idx, h_blocks, THR_MODERATE)
                loc_deep, dist_up_deep = classify_diverge_location(
                    diverge_idx, h_blocks, THR_DEEP)

            # 恢复后漂移分析 (任务 2c): 提取每次 up-cross (thr=0.3) 后
            # 100 信道块 的 w_norm 相对变化 Δ|w|/|w|。
            # 仅统计 diverge_idx 之前的 up-cross (测量正常恢复漂移, 非发散后爆炸)。
            _, up_cross_mod = detect_fade_events(h_blocks, THR_MODERATE)
            drifts_after_recovery = []
            for uc_blk in up_cross_mod:
                end_blk = uc_blk + 100
                if end_blk >= len(h_blocks):
                    continue
                # 发散 trial 只统计 diverge 之前的恢复 (避免发散后 w→inf 污染)
                if diverged and diverge_idx is not None:
                    div_chan_blk = diverge_idx // BLOCK_SIZE
                    if end_blk >= div_chan_blk:
                        continue
                ws = w_traj_at_block(w_traj, uc_blk, BLOCK_SIZE)
                we = w_traj_at_block(w_traj, end_blk, BLOCK_SIZE)
                if ws is not None and we is not None and ws > 0:
                    drifts_after_recovery.append((we - ws) / ws)
            drifts_after_recovery = np.array(drifts_after_recovery)

            # 衰落统计 (LCR/AFD)
            fs = fade_statistics(h_blocks, np.array([THR_DEEP, THR_MODERATE]),
                                 BLOCK_SIZE, T_S)
            total_time_s = len(h_blocks) * BLOCK_SIZE * T_S
            lcr_mod = fs['lcr_per_sec'][1]
            lcr_deep = fs['lcr_per_sec'][0]

            trials.append({
                'f_g_hz': float(f_g),
                'mu': mu,
                'seed': int(seed),
                'diverged': bool(diverged),
                'diverge_idx': (int(diverge_idx) if diverge_idx is not None else None),
                'diverge_idx_frac': (float(diverge_idx / N_SYMBOLS)
                                     if diverge_idx is not None else None),
                'loc_thr03': loc_mod,
                'dist_upcross_thr03': dist_up_mod,
                'loc_thr01': loc_deep,
                'dist_upcross_thr01': dist_up_deep,
                'lcr_thr03': float(lcr_mod),
                'lcr_thr01': float(lcr_deep),
                'n_events_thr03': float(lcr_mod * total_time_s),
                'drift_after_recovery_mean': (float(np.mean(drifts_after_recovery))
                                              if len(drifts_after_recovery) > 0 else None),
                'drift_after_recovery_median': (float(np.median(drifts_after_recovery))
                                                if len(drifts_after_recovery) > 0 else None),
                'n_recovery_events': int(len(drifts_after_recovery)),
            })
            run_count += 1
            elapsed = time.time() - t_start
            eta = elapsed / run_count * (total - run_count)
            if run_count % 5 == 0 or run_count <= 2 or run_count == total:
                print(f"  [{run_count}/{total}] f_G={f_g}μ={mu:.0e} "
                      f"→ div={'Y' if diverged else 'N'}"
                      f"  [{elapsed:.0f}s, ETA {eta:.0f}s]", flush=True)

    # ─── 汇总位置分布 ───
    div_trials = [t for t in trials if t['diverged'] and t['diverge_idx'] is not None]
    n_div = len(div_trials)

    summary = {
        'n_runs': len(trials),
        'n_diverged': n_div,
        'configs': configs,
    }

    if n_div == 0:
        summary['note'] = 'No diverged trials — cannot analyze position'
        return summary, trials

    # 位置分类分布 (thr=0.3 主指标)
    cats = [t['loc_thr03'] for t in div_trials]
    cat_counts = defaultdict(int)
    for c in cats:
        cat_counts[c] += 1
    summary['category_distribution_thr03'] = {
        c: {'count': cat_counts[c],
            'pct': float(cat_counts[c] / n_div * 100)}
        for c in ['edge_down', 'edge_up', 'inside_fade', 'recovery', 'normal', 'out_of_range']
        if cat_counts[c] > 0}
    # 简化的 H1/H2 汇总
    n_edge = cat_counts.get('edge_down', 0) + cat_counts.get('edge_up', 0)
    n_recovery = cat_counts.get('recovery', 0)
    n_inside = cat_counts.get('inside_fade', 0)
    n_normal = cat_counts.get('normal', 0)
    summary['h_support'] = {
        'H2_edge_pct': float(n_edge / n_div * 100),
        'H1_recovery_pct': float(n_recovery / n_div * 100),
        'inside_fade_pct': float(n_inside / n_div * 100),
        'normal_pct': float(n_normal / n_div * 100),
    }

    # thr=0.1 位置分布 (深衰落)
    cats_deep = [t['loc_thr01'] for t in div_trials]
    cat_counts_deep = defaultdict(int)
    for c in cats_deep:
        cat_counts_deep[c] += 1
    summary['category_distribution_thr01'] = {
        c: {'count': cat_counts_deep[c],
            'pct': float(cat_counts_deep[c] / n_div * 100)}
        for c in ['edge_down', 'edge_up', 'inside_fade', 'recovery', 'normal', 'out_of_range']
        if cat_counts_deep[c] > 0}

    # diverge-to-nearest-upcross 距离分布 (thr=0.3)
    dists = [t['dist_upcross_thr03'] for t in div_trials
             if t['dist_upcross_thr03'] is not None]
    if dists:
        dists = np.array(dists)
        summary['dist_upcross_thr03'] = {
            'n_with_events': len(dists),
            'median_blocks': float(np.median(dists)),
            'mean_blocks': float(np.mean(dists)),
            'p25': float(np.percentile(dists, 25)),
            'p75': float(np.percentile(dists, 75)),
            'median_symbols': float(np.median(dists) * BLOCK_SIZE),
            'pct_lt100blocks': float(np.mean(dists < 100) * 100),
            'pct_le1block': float(np.mean(dists <= 1) * 100),
        }

    # 任务 2c: 发散 vs 非发散 trial 的恢复后漂移对比
    # 按 f_g 分组 (LCR 在同 f_g 内一致), 比较 diverged vs non-diverged
    summary['drift_comparison'] = {}
    for f_g in [30.0, 1000.0]:
        for mu in [5e-3, 1e-2]:
            key = f'fg{int(f_g)}_mu{mu:.0e}'
            div_d = [t['drift_after_recovery_mean'] for t in trials
                     if t['f_g_hz'] == f_g and t['mu'] == mu and t['diverged']
                     and t['drift_after_recovery_mean'] is not None]
            non_d = [t['drift_after_recovery_mean'] for t in trials
                     if t['f_g_hz'] == f_g and t['mu'] == mu and not t['diverged']
                     and t['drift_after_recovery_mean'] is not None]
            summary['drift_comparison'][key] = {
                'n_div': len(div_d),
                'n_nondiv': len(non_d),
                'drift_div_mean': float(np.mean(div_d)) if div_d else None,
                'drift_div_median': float(np.median(div_d)) if div_d else None,
                'drift_nondiv_mean': float(np.mean(non_d)) if non_d else None,
                'drift_nondiv_median': float(np.median(non_d)) if non_d else None,
            }

    return summary, trials


# ─── 任务 3: 剂量-效应 (P_div vs f_G/LCR) ────────────────────

def run_dose_response():
    """任务 3: 固定 μ=5e-3, 扫 f_G=[10,30,100,300,1000,3000]Hz。

    每 f_G 10 seeds, 记 P_div + LCR。返回剂量-效应曲线数据。
    """
    alpha, beta = TURB_STRONG
    mu = MU_DOSE
    total = len(F_G_DOSE) * N_TRIALS
    print(f"\n[任务 3] 剂量-效应: μ={mu}, {len(F_G_DOSE)} f_G × {N_TRIALS} seeds = {total} runs")
    print(f"  f_G = {F_G_DOSE} Hz")

    results = []
    run_count = 0
    t_start = time.time()

    for f_g in F_G_DOSE:
        div_count = 0
        lcrs = []
        for trial in range(N_TRIALS):
            seed = hash(('dose', f_g, mu, N_TAP, trial)) % (2 ** 32)
            h, rX, rY = gen_channel(alpha, beta, f_g, seed)
            eq = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
            res = eq.equalize(rX, rY)
            if res['diverged']:
                div_count += 1
            h_blocks = h[::BLOCK_SIZE]
            fs = fade_statistics(h_blocks, np.array([THR_MODERATE]),
                                 BLOCK_SIZE, T_S)
            lcrs.append(fs['lcr_per_sec'][0])
            run_count += 1
            if run_count % 10 == 0:
                elapsed = time.time() - t_start
                eta = elapsed / run_count * (total - run_count)
                print(f"  [{run_count}/{total}] f_G={f_g}Hz "
                      f"[{elapsed:.0f}s, ETA {eta:.0f}s]", flush=True)
        p_div = div_count / N_TRIALS
        results.append({
            'f_g_hz': float(f_g),
            'tau_c_ms': cfg.gg_time.tau_c_from_fg(f_g) * 1e3,
            'mu': mu,
            'n_trials': N_TRIALS,
            'diverge_count': div_count,
            'p_div': p_div,
            'lcr_thr03_mean': float(np.mean(lcrs)),
            'lcr_thr03_median': float(np.median(lcrs)),
            'lcr_thr03_std': float(np.std(lcrs)),
        })
        print(f"  f_G={f_g:>6.0f}Hz: P_div={p_div:.2f} ({div_count}/{N_TRIALS}), "
              f"LCR(0.3)={np.mean(lcrs):.1f}/s, τ_c={cfg.gg_time.tau_c_from_fg(f_g)*1e3:.3f}ms",
              flush=True)

    # 单调性 + 阈值检测
    p_divs = np.array([r['p_div'] for r in results])
    lcrs_mean = np.array([r['lcr_thr03_mean'] for r in results])
    f_gs = np.array([r['f_g_hz'] for r in results])

    # Spearman/Pearson P_div vs LCR
    from scipy.stats import spearmanr, pearsonr
    def _safe(x, y):
        try:
            rp, pp = pearsonr(x, y)
        except Exception:
            rp, pp = float('nan'), float('nan')
        try:
            rs, ps = spearmanr(x, y)
        except Exception:
            rs, ps = float('nan'), float('nan')
        return {'pearson': float(rp), 'p_pearson': float(pp),
                'spearman': float(rs), 'p_spearman': float(ps)}

    dose_summary = {
        'curve': results,
        'corr_P_div_vs_LCR': _safe(lcrs_mean, p_divs),
        'corr_P_div_vs_fG': _safe(np.log10(f_gs), p_divs),
        'monotonic_increasing': bool(np.all(np.diff(p_divs) >= -0.01)),
        'max_p_div': float(np.max(p_divs)),
        'min_p_div': float(np.min(p_divs)),
        # 阈值检测: 找 P_div 首次 > 0.3 的 f_G
        'threshold_fg_first_gt03': (float(f_gs[np.argmax(p_divs > 0.3)])
                                    if np.any(p_divs > 0.3) else None),
    }
    return dose_summary


# ─── 入口 ────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("LCR 驱动发散的物理机制验证 (Q-CMA-FADE, R4 修正后续)")
    print("=" * 72)
    print(f"参数: N_symbols={N_SYMBOLS}, block={BLOCK_SIZE}, "
          f"t_s={T_S:.2e}s, SOP_RATE={SOP_RATE} rad/sym "
          f"({SOP_RATE*2.5e9/1e3:.0f} krad/s)")
    print(f"强湍 α={TURB_STRONG[0]}, β={TURB_STRONG[1]}, tap={N_TAP}")
    print(f"衰落阈值: h<{THR_DEEP} (深), h<{THR_MODERATE} (中度)")

    t0 = time.time()

    # 任务 1+2: 位置分析
    pos_summary, pos_trials = run_position_analysis()

    # 任务 3: 剂量-效应
    dose_summary = run_dose_response()

    elapsed = time.time() - t0
    print(f"\n总耗时: {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # ─── 保存结果 ───
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R-LCR-mechanism (验证 LCR 驱动发散物理机制)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'block': BLOCK_SIZE,
            'sop_rate_rad_per_sym': SOP_RATE,
            'sop_rate_krad_per_s': SOP_RATE * 2.5e9 / 1e3,
            'n_tap': N_TAP,
            'n_trials_per_combo': N_TRIALS,
            'turb': 'strong',
            'alpha': TURB_STRONG[0],
            'beta': TURB_STRONG[1],
            'fade_threshold_deep': THR_DEEP,
            'fade_threshold_moderate': THR_MODERATE,
            'gamma_bar': GAMMA_BAR,
            'elapsed_s': elapsed,
            'hypotheses': {
                'H1': '重收敛累积: 衰落恢复后 CMA 需重新收敛, 频繁打断累积漂移',
                'H2': '边沿梯度突变: h 跳变点误差/梯度突变触发发散',
            },
        },
        'position_analysis': pos_summary,
        'position_trials': pos_trials,
        'dose_response': dose_summary,
    }
    out_path = RESULTS_DIR / 'r_lcr_mechanism_results.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")

    # ─── 打印汇总 ───
    print("\n" + "=" * 72)
    print("汇总: LCR 驱动发散物理机制")
    print("=" * 72)

    if pos_summary.get('n_diverged', 0) > 0:
        print(f"\n[位置分析] 发散 trial: {pos_summary['n_diverged']}/{pos_summary['n_runs']}")
        print("\n  diverge_idx 位置分类 (thr=0.3):")
        for cat, d in pos_summary.get('category_distribution_thr03', {}).items():
            print(f"    {cat:15s}: {d['count']:3d} ({d['pct']:.0f}%)")
        hs = pos_summary['h_support']
        print(f"\n  H 支持:")
        print(f"    H2 (边沿突变) edge:  {hs['H2_edge_pct']:.0f}%")
        print(f"    H1 (重收敛) recovery: {hs['H1_recovery_pct']:.0f}%")
        print(f"    inside_fade:          {hs['inside_fade_pct']:.0f}%")
        print(f"    normal:               {hs['normal_pct']:.0f}%")

        if 'dist_upcross_thr03' in pos_summary:
            d = pos_summary['dist_upcross_thr03']
            print(f"\n  diverge→最近 up-cross 距离 (thr=0.3):")
            print(f"    中位 {d['median_blocks']:.0f} block "
                  f"({d['median_symbols']:.0f} sym), 均值 {d['mean_blocks']:.0f}")
            print(f"    <100 block (≈6400 sym): {d['pct_lt100blocks']:.0f}% "
                  f"→ {'支持 H1' if d['pct_lt100blocks'] > 50 else '不支持 H1'}")
            print(f"    ≤1 block (边沿): {d['pct_le1block']:.0f}% "
                  f"→ {'支持 H2' if d['pct_le1block'] > 50 else '不支持 H2'}")

        print("\n  发散 vs 非发散恢复后漂移对比 (Δ|w|/|w|, 100 block):")
        for key, d in pos_summary.get('drift_comparison', {}).items():
            if d['drift_div_mean'] is not None and d['drift_nondiv_mean'] is not None:
                ratio = (d['drift_div_mean'] / d['drift_nondiv_mean']
                         if abs(d['drift_nondiv_mean']) > 1e-15 else float('inf'))
                print(f"    {key}: div={d['drift_div_mean']:+.2f} "
                      f"vs nondiv={d['drift_nondiv_mean']:+.2f} "
                      f"(ratio {ratio:.1f}×)")
            else:
                print(f"    {key}: div n={d['n_div']} nondiv n={d['n_nondiv']} "
                      f"(数据不足)")
    else:
        print(f"\n[位置分析] 无发散 trial (n_diverged={pos_summary.get('n_diverged', 0)})")

    print("\n[剂量-效应] P_div vs f_G (固定 μ=5e-3):")
    print(f"  {'f_G(Hz)':>8} {'τ_c(ms)':>9} {'P_div':>6} {'LCR(0.3)':>10}")
    for r in dose_summary['curve']:
        print(f"  {r['f_g_hz']:>8.0f} {r['tau_c_ms']:>9.3f} "
              f"{r['p_div']:>6.2f} {r['lcr_thr03_mean']:>10.1f}")
    c = dose_summary['corr_P_div_vs_LCR']
    print(f"\n  P_div~LCR: r={c['pearson']:+.3f}(p={c['p_pearson']:.3f}), "
          f"ρ={c['spearman']:+.3f}(p={c['p_spearman']:.3f})")
    print(f"  单调递增: {dose_summary['monotonic_increasing']}")
    if dose_summary['threshold_fg_first_gt03'] is not None:
        print(f"  阈值: P_div>0.3 首次出现于 f_G={dose_summary['threshold_fg_first_gt03']:.0f}Hz")


if __name__ == '__main__':
    main()
