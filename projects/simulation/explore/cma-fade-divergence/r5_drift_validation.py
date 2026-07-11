"""R5 — CMA 系数漂移模型验证 (预测 vs 实测)。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P5 标方向+状态)

补 Step B (cma_divergence_scan.py) 的缺口: Step B 只存了 max_w_norm, 没存完整
w_norm_traj, 无法验证漂移模型。本脚本重跑关键组合, 保存完整块级 w_norm 轨迹,
从深衰落事件中提取实测漂移, 跟解析模型 D(n) = μ·R²·σ_n·√(n_block) 对比。

漂移模型推导 (TL-20):
  深衰落下 h→0, r≈n (纯噪声驱动), CMA 块末梯度
    grad = mean(e·r*) ≈ mean((R² − |z|²)·n*)   (z≈0 因 r≈n 且 w≈初始)
  → grad ≈ R²·mean(n*) + 高阶项
  系数随机游走: Δw_per_block = μ·grad, |Δw| 的期望 ∝ μ·R²·σ_n·E[|...|]
  累积 n_block 步随机游走 → 漂移量 D ∝ μ·R²·σ_n·√(n_block) (随机游走 √n 律)

参数溯源 (跟 Step B 一致, FR-20):
  - 信道: gg_time_envelope (Step A, block=BLOCK=100, method='gar')
  - 双偏振 SOP: theta = 1e-4 * arange(N) (Step B SOP_RATE=1e-4, cma_divergence_scan.py:112)
  - 噪声: noise_var = 1/(2·γ̄) → σ_n = sqrt(noise_var)
  - CMA: block_size=64 (_cma.py:100), R²=1.0 (QPSK Godard 1980)

验证方法:
  a) 实测: 从 w_norm_traj 提取每个深衰落事件 [start,end] 内的 ‖w‖ 变化量
     drift_measured = ‖w(end)‖ − ‖w(start)‖
  b) 预测: drift_predicted = μ · R² · σ_n · √(n_block_fade)
  c) 散点 + 线性回归 R²

注: ‖w‖ 是范数(非负), 实测漂移用 |Δ‖w‖|。预测量是随机游走期望幅度, 跟实测
    幅度量级可比 (常数 prefactor 由 R² 吸收, 见 Results 讨论)。
"""
import sys
import json
import time
import numpy as np
from pathlib import Path

# 路径设置 (跟 Step B 一致)
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from params import SimulationConfig


# ─── 参数 (FR-20 溯源, 从 params.py 读; Step B 一致) ────────

cfg = SimulationConfig()

# 只跑能验证模型的关键组合 (用户指定):
#   strong + uplink_strong × 4 f_G × {5e-3, 1e-2} × tap=11 × 3 seeds = 48 trials
TURB_LEVELS = {
    'strong':        cfg.turbulence.as_dict()['strong'],          # (1.5, 0.8)
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],   # (1.0, 0.7)
}
F_G_SWEEP = list(cfg.gg_time.GREENWOOD_FREQ_SWEEP)  # 30/100/300/1000 Hz
MU_SWEEP = [5e-3, 1e-2]  # 危险区+临界区 (Step B 证实有发散)
N_TAP = 11               # sat.1553 Fig.13 N=11
N_SEEDS = 3

N_SYMBOLS = 5_000_000
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 → 20 dB
BLOCK = cfg.experiment.BLOCK                  # 100 (信道块)
T_S = cfg.system.T_S                          # 1/2.5e9
R_SYM = cfg.system.R_SYM
R2_QPSK = 1.0                                 # QPSK Godard 1980
CMA_BLOCK = 64                                # _cma.py:100 并行化因子
SOP_RATE = 1e-4                               # Step B SOP_RATE (cma_divergence_scan.py:112)

# 漂移模型常数
NOISE_VAR = 1.0 / (2.0 * GAMMA_BAR)           # = 0.005
SIGMA_N = float(np.sqrt(NOISE_VAR))           # ≈ 0.0707

# 深衰落阈值 (敏感性分析用)
FADE_THRESHOLDS = [0.1, 0.3]


# ─── QPSK 信号生成 (跟 Step B 一致) ─────────────────────────

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1/sqrt(2) → |s|²=0.5... 实际 Step B 用 /sqrt(2) 使 |s|=1."""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)


# ─── 单次试验: 生成信道+信号, 跑 CMA, 返回完整轨迹 ──────────

def run_trial(turb_name, alpha, beta, f_g, mu, seed):
    """跑一次 CMA, 返回 w_norm_traj (块级采样) + h_block (块级 h)。"""
    rng = np.random.default_rng(seed)
    N = N_SYMBOLS
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    # 时间相关 GG 包络 (Step A)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK,
                         t_s=T_S, method='gar', seed=seed)

    # QPSK 双偏振信号 + 噪声 (跟 Step B 一致)
    s = gen_qpsk(N, rng)
    sY = gen_qpsk(N, rng)
    noise_X = np.sqrt(NOISE_VAR) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    noise_Y = np.sqrt(NOISE_VAR) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    # SOP 旋转 (Step B SOP_RATE=1e-4)
    theta = SOP_RATE * np.arange(N)
    rX = np.sqrt(h) * (np.cos(theta) * s + np.sin(theta) * sY) + noise_X
    rY = np.sqrt(h) * (-np.sin(theta) * s + np.cos(theta) * sY) + noise_Y

    # 跑 CMA, 保存完整轨迹
    eq = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
    res = eq.equalize(rX, rY, block_size=CMA_BLOCK)

    return res, h


# ─── 块级 h 重采样 (信道 BLOCK=100 → CMA 块 64 对齐) ────────

def resample_h_to_cma_blocks(h):
    """把逐符号 h 采样到 CMA 块末索引 (跟 _cma.py w_norm_traj 采样对齐)。

    _cma.py 在 idx = blk*block_size + half 处记录 w_norm_traj[idx+block_size-1]。
    即第 blk 块的轨迹点在符号索引 (blk+1)*block_size - 1 + half。
    为对齐, 取该索引处的 h 值 (h 是块内恒定的, 取哪个点都行, 这里取块末)。
    """
    L = N_TAP
    half = L // 2
    n_valid = len(h) - L + 1
    n_blocks = n_valid // CMA_BLOCK
    # 第 blk 块末符号索引 (跟 _cma.py:171 一致)
    sample_idx = []
    for blk in range(n_blocks):
        s = blk * CMA_BLOCK
        idx = s + half + CMA_BLOCK - 1  # _cma.py: w_norm_traj[idx + block_size - 1], idx=s+half
        if idx < len(h):
            sample_idx.append(idx)
    sample_idx = np.array(sample_idx)
    h_at_cma_blocks = h[sample_idx]
    return h_at_cma_blocks, sample_idx


# ─── 深衰落事件识别 ─────────────────────────────────────────

def find_fade_events(h_block, threshold, min_blocks=2):
    """找 h_block < threshold 的连续段 (深衰落事件)。

    返回 [(start, end), ...], end 是 exclusive (事件持续 [start, end) 块)。
    min_blocks: 最短事件长度 (过滤 1-block 抖动, 漂移模型需要足够步数才有 √n 律)。
    """
    below = h_block < threshold
    events = []
    i = 0
    n = len(below)
    while i < n:
        if below[i]:
            j = i
            while j < n and below[j]:
                j += 1
            if (j - i) >= min_blocks:
                events.append((i, j))  # [start, end)
            i = j
        else:
            i += 1
    return events


# ─── 提取漂移数据点 ─────────────────────────────────────────

def extract_drift_points(w_norm_traj, h_block, threshold, max_w_for_diverge=None):
    """从一次试验的轨迹提取 (drift_measured, drift_predicted) 对。

    drift_measured = |‖w(end−1)‖ − ‖w(start)‖|  (事件期间范数变化幅度)
    drift_predicted = μ · R² · σ_n · √(n_block)  (随机游走 √n 律)

    注: end−1 因 end 是 exclusive, 最后一个 below-threshold 块是 end−1。
    """
    events = find_fade_events(h_block, threshold, min_blocks=2)
    points = []
    for (start, end) in events:
        n_block = end - start  # 衰落持续的块数
        # w_norm_traj 已对齐到 h_block (同长度, 块末采样)
        w_start = w_norm_traj[start]
        w_end = w_norm_traj[end - 1]
        drift_measured = abs(w_end - w_start)
        drift_predicted = mu_global * R2_QPSK * SIGMA_N * np.sqrt(n_block)
        points.append({
            'start_block': int(start),
            'end_block': int(end),
            'n_blocks': int(n_block),
            'w_norm_start': float(w_start),
            'w_norm_end': float(w_end),
            'drift_measured': float(drift_measured),
            'drift_predicted': float(drift_predicted),
            'h_min': float(np.min(h_block[start:end])),
            'h_mean': float(np.mean(h_block[start:end])),
        })
    return points


# ─── R² 计算 ────────────────────────────────────────────────

def linear_r2(predicted, measured):
    """线性回归 R²: measured = a·predicted + b 的决定系数。

    用预测作自变量 (x=predicted, y=measured), R² = 1 − SS_res/SS_tot。
    """
    x = np.asarray(predicted, dtype=float)
    y = np.asarray(measured, dtype=float)
    if len(x) < 3:
        return float('nan'), float('nan'), float('nan')
    # 线性拟合 y = a*x + b
    A = np.vstack([x, np.ones_like(x)]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return float(r2), float(a), float(b)


def proportional_r2(predicted, measured):
    """过原点比例拟合 R²: measured = k·predicted。

    漂移模型是无截距比例关系 (drift ∝ √n), 过原点拟合更合理。
    k = Σ(xy)/Σ(x²), R² = 1 − Σ(y−kx)²/Σ(y−ȳ)²。
    """
    x = np.asarray(predicted, dtype=float)
    y = np.asarray(measured, dtype=float)
    if len(x) < 3:
        return float('nan'), float('nan')
    denom = np.sum(x ** 2)
    if denom == 0:
        return float('nan'), float('nan')
    k = np.sum(x * y) / denom
    ss_res = np.sum((y - k * x) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return float(r2), float(k)


# ─── 主循环 ─────────────────────────────────────────────────

# 全局 mu (extract_drift_points 用; 每次 mu 变化时设置)
mu_global = 5e-3


def main():
    global mu_global
    t_start = time.time()

    total = len(TURB_LEVELS) * len(F_G_SWEEP) * len(MU_SWEEP) * N_SEEDS
    print("=" * 70)
    print("R5 — CMA 系数漂移模型验证")
    print("=" * 70)
    print(f"组合: {list(TURB_LEVELS)} × f_G{F_G_SWEEP} × μ{MU_SWEEP} × tap={N_TAP} × {N_SEEDS} seeds")
    print(f"= {total} trials, N={N_SYMBOLS}/trial")
    print(f"σ_n = {SIGMA_N:.4f}, noise_var = {NOISE_VAR}, R² = {R2_QPSK}")
    print(f"CMA block_size = {CMA_BLOCK}, channel BLOCK = {BLOCK}, SOP_RATE = {SOP_RATE}")
    print()

    trials_meta = []
    all_points = {thr: [] for thr in FADE_THRESHOLDS}

    run = 0
    for turb_name, (alpha, beta) in TURB_LEVELS.items():
        for f_g in F_G_SWEEP:
            for mu in MU_SWEEP:
                mu_global = mu
                for seed_idx in range(N_SEEDS):
                    seed = hash((turb_name, f_g, mu, N_TAP, seed_idx)) % (2 ** 32)
                    run += 1
                    t0 = time.time()

                    res, h = run_trial(turb_name, alpha, beta, f_g, mu, seed)

                    # 重采样 h 到 CMA 块级 (跟 w_norm_traj 对齐)
                    h_block, _ = resample_h_to_cma_blocks(h)
                    # w_norm_traj 取前 len(h_block) 个非零对齐点
                    w_traj = res['w_norm_traj']
                    # w_norm_traj 是逐符号数组 (块末非零), 取 h_block 对应索引
                    L = N_TAP
                    half = L // 2
                    n_valid = len(h) - L + 1
                    n_cma_blocks = n_valid // CMA_BLOCK
                    w_block = np.zeros(n_cma_blocks)
                    for blk in range(n_cma_blocks):
                        s = blk * CMA_BLOCK
                        idx = s + half + CMA_BLOCK - 1
                        if idx < len(w_traj):
                            w_block[blk] = w_traj[idx]

                    # 确保长度对齐
                    min_len = min(len(h_block), len(w_block))
                    h_block = h_block[:min_len]
                    w_block = w_block[:min_len]

                    elapsed = time.time() - t0

                    # 对每个阈值提取漂移点
                    n_pts_thr = {}
                    for thr in FADE_THRESHOLDS:
                        pts = extract_drift_points(w_block, h_block, thr)
                        # 标注 trial 元数据
                        for p in pts:
                            p['turb'] = turb_name
                            p['f_g'] = f_g
                            p['mu'] = mu
                            p['seed'] = seed_idx
                            p['threshold'] = thr
                        all_points[thr].extend(pts)
                        n_pts_thr[thr] = len(pts)

                    n_fade_01 = len(find_fade_events(h_block, 0.1))
                    n_fade_03 = len(find_fade_events(h_block, 0.3))
                    diverged = res['diverged']

                    trials_meta.append({
                        'turb': turb_name, 'alpha': alpha, 'beta': beta,
                        'f_g': f_g, 'mu': mu, 'seed': seed_idx,
                        'diverged': diverged,
                        'n_fade_events_h<0.1': n_fade_01,
                        'n_fade_events_h<0.3': n_fade_03,
                        'n_drift_pts_h<0.1': n_pts_thr[0.1],
                        'n_drift_pts_h<0.3': n_pts_thr[0.3],
                        'max_w_norm': float(np.max(w_block)),
                        'elapsed_s': elapsed,
                    })

                    print(f"  [{run}/{total}] {turb_name:14s} f_G={f_g:>5.0f} μ={mu:.0e} "
                          f"seed{seed_idx} | fade(h<.1)={n_fade_01:>3} fade(h<.3)={n_fade_03:>3} "
                          f"| drift_pts: h<.1={n_pts_thr[0.1]:>3} h<.3={n_pts_thr[0.3]:>3} "
                          f"| div={diverged} [{elapsed:.1f}s]")

    total_elapsed = time.time() - t_start
    print(f"\n总耗时: {total_elapsed:.1f}s ({total_elapsed / 60:.1f} min)")

    # ─── R² 分析 ─────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("漂移模型验证: drift_measured vs drift_predicted")
    print("  模型: D = μ·R²·σ_n·√(n_block)")
    print("=" * 70)

    summary = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R5 (CMA 系数漂移模型验证)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'n_trials': total,
            'gamma_bar': GAMMA_BAR,
            'sigma_n': SIGMA_N,
            'noise_var': NOISE_VAR,
            'r2_qpsk': R2_QPSK,
            'cma_block_size': CMA_BLOCK,
            'channel_block': BLOCK,
            't_s': T_S,
            'r_sym': R_SYM,
            'sop_rate': SOP_RATE,
            'n_tap': N_TAP,
            'total_elapsed_s': total_elapsed,
            'drift_model': 'D = mu * R2 * sigma_n * sqrt(n_block)',
        },
        'scan_dims': {
            'turb_levels': list(TURB_LEVELS.keys()),
            'f_g_hz': F_G_SWEEP,
            'mu': MU_SWEEP,
            'n_tap': N_TAP,
            'n_seeds': N_SEEDS,
            'fade_thresholds': FADE_THRESHOLDS,
        },
        'trials': trials_meta,
        'drift_points': {},
        'r2_analysis': {},
    }

    for thr in FADE_THRESHOLDS:
        pts = all_points[thr]
        measured = np.array([p['drift_measured'] for p in pts])
        predicted = np.array([p['drift_predicted'] for p in pts])

        print(f"\n--- 阈值 h < {thr} ---")
        print(f"  fade events (drift points): {len(pts)}")

        if len(pts) >= 3:
            r2_lin, a_lin, b_lin = linear_r2(predicted, measured)
            r2_prop, k_prop = proportional_r2(predicted, measured)

            # 皮尔逊相关 (drift_measured vs drift_predicted)
            if np.std(predicted) > 0 and np.std(measured) > 0:
                r_pearson = float(np.corrcoef(predicted, measured)[0, 1])
            else:
                r_pearson = float('nan')

            print(f"  线性回归 R² (y=a·x+b):  R² = {r2_lin:.4f}, a = {a_lin:.3f}, b = {b_lin:.4f}")
            print(f"  比例拟合 R² (y=k·x):    R² = {r2_prop:.4f}, k = {k_prop:.3f}")
            print(f"  皮尔逊相关 r:            r = {r_pearson:.4f}")
            print(f"  measured: mean={np.mean(measured):.4f}, std={np.std(measured):.4f}, "
                  f"range=[{np.min(measured):.4f}, {np.max(measured):.4f}]")
            print(f"  predicted: mean={np.mean(predicted):.4f}, std={np.std(predicted):.4f}, "
                  f"range=[{np.min(predicted):.4f}, {np.max(predicted):.4f}]")

            # 按 mu 分组 R² (看模型是否在危险区/临界区都成立)
            print(f"  分组 R² (按 μ):")
            for mu_val in MU_SWEEP:
                mask = np.array([p['mu'] == mu_val for p in pts])
                if mask.sum() >= 3:
                    r2_m, _, _ = linear_r2(predicted[mask], measured[mask])
                    print(f"    μ={mu_val:.0e}: n={mask.sum():>3}, R²={r2_m:.4f}")

            summary['r2_analysis'][f'thr_{thr}'] = {
                'n_points': len(pts),
                'r2_linear': r2_lin, 'a_linear': a_lin, 'b_linear': b_lin,
                'r2_proportional': r2_prop, 'k_proportional': k_prop,
                'r_pearson': r_pearson,
                'measured_mean': float(np.mean(measured)),
                'measured_std': float(np.std(measured)),
                'predicted_mean': float(np.mean(predicted)),
                'predicted_std': float(np.std(predicted)),
            }
        else:
            print(f"  ⚠️ 数据点不足 ({len(pts)} < 3), 跳过 R²")
            summary['r2_analysis'][f'thr_{thr}'] = {'n_points': len(pts)}

        # 存原始点 (限量, 避免 JSON 过大)
        summary['drift_points'][f'thr_{thr}'] = pts[:2000]

    # ─── 汇总表 ──────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("试验汇总表")
    print("=" * 70)
    print(f"{'turb':>14} {'f_G':>6} {'μ':>8} {'seed':>4} | {'fade<.1':>7} {'fade<.3':>7} "
          f"| {'pts<.1':>6} {'pts<.3':>6} | {'div':>5} {'max‖w‖':>8}")
    print("-" * 80)
    for t in trials_meta:
        print(f"{t['turb']:>14} {t['f_g']:>6.0f} {t['mu']:>8.0e} {t['seed']:>4} | "
              f"{t['n_fade_events_h<0.1']:>7} {t['n_fade_events_h<0.3']:>7} | "
              f"{t['n_drift_pts_h<0.1']:>6} {t['n_drift_pts_h<0.3']:>6} | "
              f"{str(t['diverged']):>5} {t['max_w_norm']:>8.2f}")

    # 总计
    tot_fade_01 = sum(t['n_fade_events_h<0.1'] for t in trials_meta)
    tot_fade_03 = sum(t['n_fade_events_h<0.3'] for t in trials_meta)
    tot_pts_01 = sum(t['n_drift_pts_h<0.1'] for t in trials_meta)
    tot_pts_03 = sum(t['n_drift_pts_h<0.3'] for t in trials_meta)
    tot_div = sum(1 for t in trials_meta if t['diverged'])
    print("-" * 80)
    print(f"{'TOTAL':>14} {'':>6} {'':>8} {'':>4} | {tot_fade_01:>7} {tot_fade_03:>7} | "
          f"{tot_pts_01:>6} {tot_pts_03:>6} | {tot_div:>5}")
    print(f"\n发散 trials: {tot_div}/{total}")

    summary['totals'] = {
        'n_trials': total,
        'n_diverged': tot_div,
        'total_fade_events_h<0.1': tot_fade_01,
        'total_fade_events_h<0.3': tot_fade_03,
        'total_drift_pts_h<0.1': tot_pts_01,
        'total_drift_pts_h<0.3': tot_pts_03,
    }

    # ─── 保存 ────────────────────────────────────────────────
    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'r5_drift_validation_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")

    return summary


if __name__ == '__main__':
    main()
