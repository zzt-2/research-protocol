"""R4 — 发散事件与 AFD/LCR 的相关性分析。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)

验证 Step B 核心假设: 发散由 LCR（事件计数/衰落频率）驱动, 而非 AFD
（单次持续时间）。Step B 发现 f_G 是发散的第二驱动（仅次于 μ），物理上
f_G↑ → τ_c↓ → 衰落事件越频繁（LCR 大）→ 发散概率高。

分析步骤:
  1. 遍历 Step B 的 128 组合 × 3 trials = 384 trials
  2. 对每个 trial, 用其 seed（JSON 中已存）重新生成 h 包络（块级,
     gg_time_envelope_blockwise, 参数与 Step B 一致）
  3. 用 fade_statistics 算 AFD/LCR（threshold h<0.1 代表深衰落）
  4. 建 (AFD, LCR, f_G, μ, tap, turb, diverged) 表
  5. 算相关系数（Pearson + Spearman）:
     - P_div vs AFD（跨同 f_G 组合）
     - P_div vs LCR（跨同 f_G 组合）
     - 固定 μ 下 P_div vs LCR（控制 μ 后看 LCR 解释力——关键检验）
  6. diverge_idx 位置 vs h 值: 发散是否集中在深衰落附近

注:
  - Channel（h 包络）只依赖 turb_name + f_g + seed（不依赖 μ/tap）, 但
    不同 μ/tap 组合用不同 seed（cma_divergence_scan.py:168）, 所以 channel
    不同。对每个 trial 用其 seed 重新生成 h 即可。
  - diverge_idx 是符号索引, h[sym_idx] = h_blocks[sym_idx // BLOCK]。
  - seed 直接从 Step B JSON 读（避免 Python hash() 跨进程随机性）。

用法:
  cd projects/simulation && python explore/cma-fade-divergence/r4_fade_correlation.py
"""
import sys
import os
import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict

# 路径设置: 确保从 projects/simulation/ 运行
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope_blockwise
from common._config import BLOCK

# fade_statistics 是 gg_time_fading_model.py 的函数, 直接 import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gg_time_fading_model import fade_statistics

from scipy.stats import pearsonr, spearmanr


# ─── 参数（从 params.py 读, FR-20 P3 单一真相源）────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S

# Step B 结果路径
RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
STEP_B_PATH = RESULTS_DIR / 'cma_divergence_scan_results.json'

# 序列参数（必须与 Step B 一致）
N_SYMBOLS = 5_000_000
BLOCK_SIZE = BLOCK  # 100
N_BLOCKS = N_SYMBOLS // BLOCK_SIZE  # 50000

# 衰落阈值: 多档, 因为 5M 符号序列仅 2ms 总时长, 块级分辨率 40ns
# 无法分辨 AFD（大多≈0 或 ∞）。LCR（事件计数）才是稳健指标。
# 用多档阈值避免单一阈值退化为 0 事件。
FADE_THRESHOLDS = np.array([0.1, 0.3, 0.5])
DEEP_FADE_THR = 0.1
# 发散触发窗口: diverge_idx 前 N_sym 符号内的最小 h（探测滞后检测前的触发衰落）
# CMA block_size=64, 取 ~10 倍 block = 640 符号 ≈ 1.6 个 fG=1000Hz 周期
DIVERGE_LOOKBACK_SYM = 1000


# ─── 主逻辑 ───────────────────────────────────────────────

def safe_corr(x, y):
    """算 Pearson + Spearman, 处理常量数组/小样本。

    返回 dict, nan 表示无法计算。
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        return {'n': n, 'pearson': float('nan'), 'spearman': float('nan'),
                'p_pearson': float('nan'), 'p_spearman': float('nan')}
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
        # 常量数组 → 相关系数无定义
        return {'n': n, 'pearson': float('nan'), 'spearman': float('nan'),
                'p_pearson': float('nan'), 'p_spearman': float('nan')}
    try:
        r_p, p_p = pearsonr(x, y)
    except Exception:
        r_p, p_p = float('nan'), float('nan')
    try:
        r_s, p_s = spearmanr(x, y)
    except Exception:
        r_s, p_s = float('nan'), float('nan')
    return {'n': n, 'pearson': float(r_p), 'spearman': float(r_s),
            'p_pearson': float(p_p), 'p_spearman': float(p_s)}


def build_trial_table(step_b_data):
    """遍历 Step B 的 384 trials, 对每个 trial 重新生成 h 算 AFD/LCR。

    返回 list[dict], 每项:
      turb_name, alpha, beta, f_g_hz, tau_c_ms, mu, n_tap, seed,
      diverged, diverge_idx, afd_s, lcr_per_sec, p_below,
      diverge_h_val (发散处 h 值, 未发散为 null)
    """
    trials_table = []
    t_start = time.time()
    n_done = 0

    for combo in step_b_data['results']:
        turb_name = combo['turb_name']
        alpha = combo['alpha']
        beta = combo['beta']
        f_g = combo['f_g_hz']
        tau_c = cfg.gg_time.tau_c_from_fg(f_g)
        mu = combo['mu']
        n_tap = combo['n_tap']

        for trial in combo['trials']:
            seed = trial['seed']
            diverged = trial['diverged']
            diverge_idx = trial['diverge_idx']

            # 重新生成块级 h（seed 与 Step B 的符号级 h 一致,
            # gg_time_envelope_blockwise 是 gg_time_envelope 的块级版,
            # 已验证相同 seed 生成相同 h_blocks）
            h_blocks = gg_time_envelope_blockwise(
                N_BLOCKS, alpha, beta, tau_c,
                block=BLOCK_SIZE, t_s=T_S, method='gar', seed=seed,
            )

            # 算 AFD/LCR（多档阈值）
            fs = fade_statistics(h_blocks, FADE_THRESHOLDS, BLOCK_SIZE, T_S)
            lcr_by_thr = {f'thr_{t}': fs['lcr_per_sec'][i]
                          for i, t in enumerate(FADE_THRESHOLDS)}
            afd_by_thr = {f'thr_{t}': fs['afd_s'][i]
                          for i, t in enumerate(FADE_THRESHOLDS)}
            p_below_by_thr = {f'thr_{t}': fs['p_below'][i]
                              for i, t in enumerate(FADE_THRESHOLDS)}
            # 事件总数（与 f_G 无关的原始计数, 跨 f_G 更可比）
            # n_events = LCR * total_time = LCR * N_blocks * block * t_s
            total_time_s = N_BLOCKS * BLOCK_SIZE * T_S
            n_events_by_thr = {f'thr_{t}': fs['lcr_per_sec'][i] * total_time_s
                               for i, t in enumerate(FADE_THRESHOLDS)}

            # 选主要阈值（thr=0.3, 多数配置有非零事件）做主指标
            main_thr = 0.3
            idx_main = list(FADE_THRESHOLDS).index(main_thr)
            lcr_main = fs['lcr_per_sec'][idx_main]
            afd_main = fs['afd_s'][idx_main]
            p_below_main = fs['p_below'][idx_main]
            n_events_main = lcr_main * total_time_s

            # diverge_idx 处的 h 值（符号索引 → 块索引）
            diverge_h_val = None
            # 发散检测是滞后的（norm>10× 才触发）→ 看 diverge_idx 前
            # DIVERGE_LOOKBACK_SYM 符号窗口内的最小 h（触发发散的深衰落）
            diverge_pre_window_min_h = None
            diverge_pre_window_mean_h = None
            if diverge_idx is not None:
                sym_idx = int(diverge_idx)
                blk_idx = sym_idx // BLOCK_SIZE
                if 0 <= blk_idx < len(h_blocks):
                    diverge_h_val = float(h_blocks[blk_idx])
                # 前窗口
                blk_lo = max(0, (sym_idx - DIVERGE_LOOKBACK_SYM) // BLOCK_SIZE)
                blk_hi = min(len(h_blocks), sym_idx // BLOCK_SIZE + 1)
                if blk_hi > blk_lo:
                    window = h_blocks[blk_lo:blk_hi]
                    diverge_pre_window_min_h = float(np.min(window))
                    diverge_pre_window_mean_h = float(np.mean(window))

            # 该 trial 序列全局统计（辅助: 最小 h, 深衰落事件数）
            min_h = float(np.min(h_blocks))

            trials_table.append({
                'turb_name': turb_name,
                'alpha': alpha, 'beta': beta,
                'f_g_hz': float(f_g),
                'tau_c_ms': tau_c * 1e3,
                'mu': mu,
                'n_tap': n_tap,
                'seed': int(seed),
                'diverged': bool(diverged),
                'diverge_idx': int(diverge_idx) if diverge_idx is not None else None,
                # 主指标 (thr=0.3)
                'afd_s': float(afd_main),
                'lcr_per_sec': float(lcr_main),
                'n_events': float(n_events_main),
                'p_below': float(p_below_main),
                # 多档阈值（完整保存）
                'lcr_by_thr': {k: float(v) for k, v in lcr_by_thr.items()},
                'afd_by_thr': afd_by_thr,
                'n_events_by_thr': {k: float(v) for k, v in n_events_by_thr.items()},
                'p_below_by_thr': {k: float(v) for k, v in p_below_by_thr.items()},
                # 位置分析
                'min_h': min_h,
                'diverge_h_val': diverge_h_val,
                'diverge_pre_window_min_h': diverge_pre_window_min_h,
                'diverge_pre_window_mean_h': diverge_pre_window_mean_h,
            })
            n_done += 1

        if n_done % 48 == 0:
            elapsed = time.time() - t_start
            eta = elapsed / n_done * (384 - n_done)
            print(f"  [{n_done}/384] {elapsed:.0f}s, ETA {eta:.0f}s")

    return trials_table


def compute_correlations(trials_table):
    """算相关系数。

    因为同一 channel 的 AFD/LCR 由 (turb, f_g) 大体决定, 但不同 μ/tap
    的 trial 用不同 seed → 不同 channel 实现 → AFD/LCR 有 trial 间变异。
    我们把数据按 (turb, f_g, mu, tap) 聚合成 P_div, 然后看 P_div 与
    该组的平均 AFD/LCR 的相关性。

    但更细的检验: 在 trial 级别看 diverged(0/1) vs AFD/LCR。
    """
    results = {}

    # === A. 聚合到 P_div（按 turb×f_g×mu×tap 组合, 3 trials 的均值）===
    groups = defaultdict(list)
    for t in trials_table:
        key = (t['turb_name'], t['f_g_hz'], t['mu'], t['n_tap'])
        groups[key].append(t)

    agg = []
    for key, ts in groups.items():
        turb, f_g, mu, tap = key
        p_div = np.mean([t['diverged'] for t in ts])
        afd_mean = np.mean([t['afd_s'] for t in ts])
        lcr_mean = np.mean([t['lcr_per_sec'] for t in ts])
        n_events_mean = np.mean([t['n_events'] for t in ts])
        p_below_mean = np.mean([t['p_below'] for t in ts])
        agg.append({
            'turb': turb, 'f_g': f_g, 'mu': mu, 'tap': tap,
            'p_div': p_div, 'afd_mean': afd_mean, 'lcr_mean': lcr_mean,
            'n_events_mean': n_events_mean,
            'p_below_mean': p_below_mean, 'n_trials': len(ts),
        })

    p_divs = np.array([a['p_div'] for a in agg])
    afds = np.array([a['afd_mean'] for a in agg])
    lcrs = np.array([a['lcr_mean'] for a in agg])
    n_events = np.array([a['n_events_mean'] for a in agg])
    f_gs = np.array([a['f_g'] for a in agg])
    mus = np.array([a['mu'] for a in agg])

    # 整体相关（128 组合级）
    results['overall'] = {
        'P_div_vs_AFD': safe_corr(afds, p_divs),
        'P_div_vs_LCR': safe_corr(lcrs, p_divs),
        'P_div_vs_n_events': safe_corr(n_events, p_divs),
        'P_div_vs_fG': safe_corr(f_gs, p_divs),
        'P_div_vs_mu': safe_corr(np.log10(mus), p_divs),
        'n_combos': len(agg),
    }

    # 跨同 f_G 组合（控制 f_G 后看 AFD/LCR 的解释力）
    # → 按 f_G 分组, 组内 P_div vs AFD/LCR
    results['within_fG'] = {}
    for f_g_val in sorted(set(f_gs.tolist())):
        mask = f_gs == f_g_val
        results['within_fG'][str(int(f_g_val))] = {
            'P_div_vs_AFD': safe_corr(afds[mask], p_divs[mask]),
            'P_div_vs_LCR': safe_corr(lcrs[mask], p_divs[mask]),
        }

    # 固定 μ 下 P_div vs LCR（关键检验: 控制 μ 后 LCR 的解释力）
    results['within_mu'] = {}
    for mu_val in sorted(set(mus.tolist())):
        mask = mus == mu_val
        results['within_mu'][str(mu_val)] = {
            'P_div_vs_AFD': safe_corr(afds[mask], p_divs[mask]),
            'P_div_vs_LCR': safe_corr(lcrs[mask], p_divs[mask]),
            'P_div_vs_n_events': safe_corr(n_events[mask], p_divs[mask]),
            'P_div_vs_fG': safe_corr(f_gs[mask], p_divs[mask]),
        }

    # 固定 turb（控制湍流强度后, 看 f_G/LCR 的影响）
    turbs = np.array([a['turb'] for a in agg])
    results['within_turb'] = {}
    for turb_val in sorted(set(turbs.tolist())):
        mask = turbs == turb_val
        results['within_turb'][turb_val] = {
            'P_div_vs_AFD': safe_corr(afds[mask], p_divs[mask]),
            'P_div_vs_LCR': safe_corr(lcrs[mask], p_divs[mask]),
            'P_div_vs_n_events': safe_corr(n_events[mask], p_divs[mask]),
            'P_div_vs_fG': safe_corr(f_gs[mask], p_divs[mask]),
        }

    # === B. Trial 级别: diverged(0/1) vs LCR/AFD ===
    div_flags = np.array([1.0 if t['diverged'] else 0.0 for t in trials_table])
    trial_lcrs = np.array([t['lcr_per_sec'] for t in trials_table])
    trial_afds = np.array([t['afd_s'] for t in trials_table])
    trial_n_events = np.array([t['n_events'] for t in trials_table])
    results['trial_level'] = {
        'diverged_vs_LCR': safe_corr(trial_lcrs, div_flags),
        'diverged_vs_AFD': safe_corr(trial_afds, div_flags),
        'diverged_vs_n_events': safe_corr(trial_n_events, div_flags),
        'n_trials': len(trials_table),
        'n_diverged': int(np.sum(div_flags)),
    }

    return results, agg


def analyze_diverge_location(trials_table):
    """分析 diverge_idx 位置 vs h 值: 发散是否由深衰落触发。

    关键洞察: CMA 发散检测是滞后的（norm>10×init 才触发）, 所以发散检测
    点的 h 偏高（系数已被噪声放大）。要检验"深衰落触发发散"假设, 必须:
      (a) 重新生成每个发散 trial 的 h, 取 [0, diverge_idx] 前窗口的统计
      (b) 与同配置（turb,fG,mu,tap）的非发散 trial 的全序列统计对比
      (c) 数前窗口的深衰落事件数（thr<0.3）

    若假设成立: 发散 trial 前窗口的 min_h 应 << 非发散 trial 的 min_h,
    且前窗口应有 ≥1 深衰落事件。若不成立（实际观测）: 发散由高 μ 的
    CMA 数值不稳定主导, 与触发性的深衰落无关。
    """
    from scipy.stats import mannwhitneyu

    diverged_trials = [t for t in trials_table if t['diverged']
                       and t['diverge_h_val'] is not None]
    nondiv_trials = [t for t in trials_table if not t['diverged']]

    if not diverged_trials:
        return {'n_diverged_with_h': 0, 'note': 'No diverged trials with h value'}

    # 非发散 trial 的 min_h, 按 (turb,fG,mu,tap) 分组（对照）
    nondiv_min_by_cfg = defaultdict(list)
    for t in nondiv_trials:
        key = (t['turb_name'], t['f_g_hz'], t['mu'], t['n_tap'])
        nondiv_min_by_cfg[key].append(t['min_h'])

    div_h_vals = np.array([t['diverge_h_val'] for t in diverged_trials])
    min_h_vals = np.array([t['min_h'] for t in diverged_trials])
    div_idx = np.array([t['diverge_idx'] for t in diverged_trials])

    # 重新生成 h, 算 [0, diverge_idx] 前窗口统计（稳健检验）
    pre_div_min_h = []
    pre_div_events_thr03 = []  # 前窗口深衰落事件数 (thr<0.3)
    matched_nondiv_min = []
    loc_thr = 0.3
    for t in diverged_trials:
        seed = t['seed']
        tau_c = cfg.gg_time.tau_c_from_fg(t['f_g_hz'])
        h = gg_time_envelope_blockwise(
            N_BLOCKS, t['alpha'], t['beta'], tau_c,
            block=BLOCK_SIZE, t_s=T_S, method='gar', seed=seed)
        div_blk = t['diverge_idx'] // BLOCK_SIZE
        pre_h = h[:div_blk] if div_blk > 0 else h[:1]
        pre_div_min_h.append(float(np.min(pre_h)))
        # 数前窗口深衰落事件 (向下跨 thr)
        below = pre_h < loc_thr
        n_ev = int((below[1:] & ~below[:-1]).sum())
        pre_div_events_thr03.append(n_ev)
        key = (t['turb_name'], t['f_g_hz'], t['mu'], t['n_tap'])
        matched_nondiv_min.extend(nondiv_min_by_cfg.get(key, []))

    pre_div_min_h = np.array(pre_div_min_h)
    pre_div_events = np.array(pre_div_events_thr03)
    matched_nondiv_min_h = np.array(matched_nondiv_min)

    result = {
        'n_diverged_with_h': len(diverged_trials),
        # 发散检测点 h（滞后, 预期偏高——CMA 已发散放大）
        'diverge_h_mean': float(np.mean(div_h_vals)),
        'diverge_h_median': float(np.median(div_h_vals)),
        'diverge_h_min': float(np.min(div_h_vals)),
        'diverge_h_max': float(np.max(div_h_vals)),
        # 发散位置（占序列比例）
        'diverge_idx_frac_mean': float(np.mean(div_idx / N_SYMBOLS)),
        'diverge_idx_frac_median': float(np.median(div_idx / N_SYMBOLS)),
        'pct_diverge_early_lt10pct': float(np.mean(div_idx < 0.1 * N_SYMBOLS)),
        'pct_diverge_before_25pct': float(np.mean(div_idx < 0.25 * N_SYMBOLS)),
        # 前窗口 [0, diverge_idx] 统计（关键）
        'pre_div_min_h_mean': float(np.mean(pre_div_min_h)),
        'pre_div_min_h_median': float(np.median(pre_div_min_h)),
        'matched_nondiv_min_h_mean': float(np.mean(matched_nondiv_min_h)),
        'matched_nondiv_min_h_median': float(np.median(matched_nondiv_min_h)),
        # 前窗口深衰落事件数
        'pre_div_events_thr03_mean': float(np.mean(pre_div_events)),
        'pre_div_events_thr03_median': float(np.median(pre_div_events)),
        'pct_pre_div_zero_events': float(np.mean(pre_div_events == 0)),
        'pct_pre_div_le2_events': float(np.mean(pre_div_events <= 2)),
        # 全序列 min_h（发散 vs 非发散, 不分窗口）
        'min_h_mean_diverged_full': float(np.mean(min_h_vals)),
        'min_h_mean_nondiverged_full': float(
            np.mean([t['min_h'] for t in nondiv_trials])) if nondiv_trials else None,
    }

    # 统计检验
    # (1) 发散前窗口 min_h vs 同配置非发散全序列 min_h（假设: 发散应有更深前窗口）
    if len(matched_nondiv_min_h) > 3:
        try:
            u, p = mannwhitneyu(pre_div_min_h, matched_nondiv_min_h, alternative='less')
            result['mw_pre_div_min_lt_nondiv_p'] = float(p)
        except Exception:
            pass
    # (2) 全序列 min_h: 发散 vs 非发散
    nondiv_all_min = np.array([t['min_h'] for t in nondiv_trials]) if nondiv_trials else np.array([])
    if len(nondiv_all_min) > 3 and len(min_h_vals) > 3:
        try:
            u, p = mannwhitneyu(min_h_vals, nondiv_all_min, alternative='less')
            result['mw_fullseq_min_div_lt_nondiv_p'] = float(p)
        except Exception:
            pass

    return result


def print_summary(corr_results, loc_results, agg):
    """打印汇总表。"""
    print("\n" + "=" * 70)
    print("R4: 发散事件 vs AFD/LCR 相关性分析 (Q-CMA-FADE)")
    print("=" * 70)

    print(f"\n聚合组合数: {corr_results['overall']['n_combos']} (128 turb×fG×mu×tap)")
    print(f"Trial 总数: {corr_results['trial_level']['n_trials']}, "
          f"发散: {corr_results['trial_level']['n_diverged']}")

    print("\n--- 整体相关（128 组合级, P_div vs X）---")
    o = corr_results['overall']
    for name in ['P_div_vs_mu', 'P_div_vs_fG', 'P_div_vs_LCR', 'P_div_vs_n_events', 'P_div_vs_AFD']:
        c = o[name]
        print(f"  {name:22s}: Pearson r={c['pearson']:+.3f} (p={c['p_pearson']:.1e}), "
              f"Spearman ρ={c['spearman']:+.3f} (p={c['p_spearman']:.1e}) [n={c['n']}]")

    print("\n--- 固定 μ 下 P_div vs LCR/n_events/AFD/fG（关键检验: 控制 μ）---")
    for mu_val, c in sorted(corr_results['within_mu'].items()):
        lcr_c = c['P_div_vs_LCR']
        ne_c = c['P_div_vs_n_events']
        afd_c = c['P_div_vs_AFD']
        fg_c = c['P_div_vs_fG']
        print(f"  μ={float(mu_val):.0e}: "
              f"~LCR r={lcr_c['pearson']:+.3f}(p={lcr_c['p_pearson']:.2f}) | "
              f"~n_evt r={ne_c['pearson']:+.3f}(p={ne_c['p_pearson']:.2f}) | "
              f"~AFD r={afd_c['pearson']:+.3f} | "
              f"~fG r={fg_c['pearson']:+.3f}(p={fg_c['p_pearson']:.3f}) [n={lcr_c['n']}]")

    print("\n--- 固定 f_G 下 P_div vs LCR/n_events/AFD ---")
    for f_g_val, c in sorted(corr_results['within_fG'].items()):
        lcr_c = c['P_div_vs_LCR']
        afd_c = c['P_div_vs_AFD']
        print(f"  f_G={f_g_val:>4s}Hz: "
              f"~LCR r={lcr_c['pearson']:+.3f}(p={lcr_c['p_pearson']:.2f}) | "
              f"~AFD r={afd_c['pearson']:+.3f} [n={lcr_c['n']}]")

    print("\n--- 固定 turb 下 P_div vs LCR/n_events/fG ---")
    for turb_val, c in sorted(corr_results['within_turb'].items()):
        lcr_c = c['P_div_vs_LCR']
        ne_c = c['P_div_vs_n_events']
        afd_c = c['P_div_vs_AFD']
        fg_c = c['P_div_vs_fG']
        print(f"  {turb_val:14s}: "
              f"~LCR r={lcr_c['pearson']:+.3f}(p={lcr_c['p_pearson']:.2f}) | "
              f"~n_evt r={ne_c['pearson']:+.3f}(p={ne_c['p_pearson']:.2f}) | "
              f"~fG r={fg_c['pearson']:+.3f}(p={fg_c['p_pearson']:.3f}) [n={lcr_c['n']}]")

    print("\n--- Trial 级别: diverged(0/1) vs LCR/n_events/AFD ---")
    tl = corr_results['trial_level']
    print(f"  diverged~LCR: r={tl['diverged_vs_LCR']['pearson']:+.3f} "
          f"(p={tl['diverged_vs_LCR']['p_pearson']:.1e}) | "
          f"~n_evt: r={tl['diverged_vs_n_events']['pearson']:+.3f} "
          f"(p={tl['diverged_vs_n_events']['p_pearson']:.1e}) | "
          f"~AFD: r={tl['diverged_vs_AFD']['pearson']:+.3f}")

    print("\n--- diverge_idx 位置 vs h 值（发散是否由深衰落触发）---")
    if loc_results['n_diverged_with_h'] > 0:
        print(f"  发散 trial 数（有 h 值）: {loc_results['n_diverged_with_h']}")
        print(f"  发散位置: median@{loc_results['diverge_idx_frac_median']*100:.0f}% 序列, "
              f"早发散(<10%): {loc_results['pct_diverge_early_lt10pct']*100:.0f}%")
        print(f"  发散检测点 h（滞后, 预期偏高）: mean={loc_results['diverge_h_mean']:.3f}, "
              f"median={loc_results['diverge_h_median']:.3f}")
        print(f"  ── 前窗口 [0, diverge_idx] 统计（关键检验）──")
        print(f"  发散前窗口 min_h: mean={loc_results['pre_div_min_h_mean']:.4f}, "
              f"median={loc_results['pre_div_min_h_median']:.4f}")
        print(f"  同配置非发散 min_h: mean={loc_results['matched_nondiv_min_h_mean']:.4f}, "
              f"median={loc_results['matched_nondiv_min_h_median']:.4f}")
        if 'mw_pre_div_min_lt_nondiv_p' in loc_results:
            print(f"  Mann-Whitney 发散.前窗口min < 非发散.min: "
                  f"p={loc_results['mw_pre_div_min_lt_nondiv_p']:.3f} "
                  f"{'(<0.05 支持深衰落触发)' if loc_results['mw_pre_div_min_lt_nondiv_p'] < 0.05 else '(≥0.05 不支持深衰落触发)'}")
        print(f"  前窗口深衰落事件数(thr<0.3): median={loc_results['pre_div_events_thr03_median']:.0f}, "
              f"0事件占{loc_results['pct_pre_div_zero_events']*100:.0f}%, "
              f"≤2事件占{loc_results['pct_pre_div_le2_events']*100:.0f}%")
        print(f"  全序列 min_h: 发散={loc_results['min_h_mean_diverged_full']:.4f} vs "
              f"非发散={loc_results['min_h_mean_nondiverged_full']:.4f}")
        if 'mw_fullseq_min_div_lt_nondiv_p' in loc_results:
            print(f"  Mann-Whitney 全序列: 发散.min < 非发散.min: "
                  f"p={loc_results['mw_fullseq_min_div_lt_nondiv_p']:.3f}")
    else:
        print(f"  {loc_results.get('note', '无发散 trial 有 h 值')}")

    # P_div 汇总表（turb × f_G, 平均跨 μ/tap）
    print("\n--- P_div 汇总（turb × f_G, 跨 μ/tap 平均）---")
    from collections import defaultdict as dd
    tf_pdiv = dd(list)
    for a in agg:
        tf_pdiv[(a['turb'], a['f_g'])].append(a['p_div'])
    turbs_sorted = sorted(set(a['turb'] for a in agg))
    fgs_sorted = sorted(set(a['f_g'] for a in agg))
    header = f"{'turb':>16}" + "".join(f"  f_G={int(fg):>5d}" for fg in fgs_sorted)
    print(header)
    for turb in turbs_sorted:
        row = f"{turb:>16}"
        for fg in fgs_sorted:
            vals = tf_pdiv.get((turb, fg), [])
            if vals:
                row += f"  {np.mean(vals):>7.2f}"
            else:
                row += f"  {'N/A':>7}"
        print(row)


def main():
    print("=== R4: 发散事件 vs AFD/LCR 相关性分析 ===")
    print(f"参数: N_symbols={N_SYMBOLS}, block={BLOCK_SIZE}, "
          f"n_blocks={N_BLOCKS}, t_s={T_S:.2e}s")
    print(f"衰落阈值: h<{DEEP_FADE_THR} (深衰落)")
    print(f"Step B 结果: {STEP_B_PATH}")

    if not STEP_B_PATH.exists():
        raise FileNotFoundError(f"Step B results not found: {STEP_B_PATH}")

    with open(STEP_B_PATH, 'r', encoding='utf-8') as f:
        step_b_data = json.load(f)

    print(f"Step B: {len(step_b_data['results'])} 组合 × "
          f"{step_b_data['meta']['n_trials']} trials")

    print("\n[1/3] 遍历 384 trials, 重新生成 h 算 AFD/LCR...")
    trials_table = build_trial_table(step_b_data)
    print(f"  完成: {len(trials_table)} trials")

    print("\n[2/3] 算相关系数...")
    corr_results, agg = compute_correlations(trials_table)

    print("\n[3/3] 分析 diverge_idx 位置 vs h 值...")
    loc_results = analyze_diverge_location(trials_table)

    # 打印汇总
    print_summary(corr_results, loc_results, agg)

    # 保存结果
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R4 (发散 vs AFD/LCR 相关性)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'block': BLOCK_SIZE,
            'n_blocks': N_BLOCKS,
            'fade_threshold': DEEP_FADE_THR,
            'step_b_source': str(STEP_B_PATH.relative_to(SIM_DIR)),
        },
        'correlations': corr_results,
        'diverge_location': loc_results,
        'trial_table': trials_table,
        'agg_table': agg,
    }
    out_path = RESULTS_DIR / 'r4_fade_correlation_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")

    return out


if __name__ == '__main__':
    main()
