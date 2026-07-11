"""R4 修正验证 — 真实 SOP 速率 (1 krad/s) + 更长序列 (10M 符号) 重跑 R4 相关性分析。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)

排查"250 krad/s SOP 掩盖深衰落作用"的伪影假设。

## 背景

R4（上一轮）发现：发散主要由高 μ 数值不稳定驱动，深衰落不是必要触发条件
（57% 发散前零深衰落事件，30% 前 10% 就发散）。

但 R4 用的是 Step B 的参数：
  - SOP_RATE = 1e-4 rad/sym → 250 krad/s（cma_divergence_scan.py L112）
    真实 OSL SOP 速率 ~1 krad/s（sat.1553 §6.3），原 R4 是 250× 过快。
    高 SOP 旋转可能本身就不稳定，掩盖了深衰落的作用。
  - N_SYMBOLS = 5M = 2ms 观测窗口 → AFD 无法计算（序列太短）。

## 修正参数

  - SOP_RATE = 4e-7 rad/sym（1 krad/s, sat.1553 §6.3 真实值, Step C 已修正的值）
    4e-7 rad/sym × 2.5e9 sym/s = 1.0e3 rad/s = 1 krad/s ✓
  - N_SYMBOLS = 10_000_000（10M 符号 = 4ms 观测窗口）
    拉长窗口让 AFD 可以计算，让 LCR 有更多事件。

## 分析内容（跟 R4 一致，对照 cma_divergence_scan.py）

1. 遍历 strong + uplink_strong × 4 f_G(30/100/300/1000) × 4 μ
   (5e-4/1e-3/5e-3/1e-2) × tap=11 × 3 seeds = 96 trials
2. 对每个 trial，用 seed 重新生成 h（10M 符号, 1 krad/s SOP）
3. 用 fade_statistics 算 AFD/LCR（threshold h<0.1）
4. 跑 CMA（CMAEqualizer2x2），记录 diverged + diverge_idx
5. 算相关系数：
   - P_div vs AFD / LCR / μ / f_G；固定 μ 后 P_div vs LCR
6. 检查 diverge_idx 位置分布（是否仍前 10% 早发散？）
7. 检查 diverged trial 前窗口的深衰落事件数（是否仍 57% 零事件？）

## 关键对比

跟原 R4（250 krad/s, 5M 符号）对比：
  - 若修正后深衰落触发出现（diverge_idx 不再集中在前面，前窗口有深衰落事件）
    → R4 原结论是 250 krad/s 伪影
  - 若修正后仍无深衰落触发 → 发散确实由高 μ 驱动，R4 原结论成立

用法:
  cd projects/simulation && python explore/cma-fade-divergence/r4_corrected_sop_rate.py
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
from common._gg_time import gg_time_envelope, gg_time_envelope_blockwise
from common._cma import CMAEqualizer2x2
from common._config import BLOCK

# fade_statistics 是 gg_time_fading_model.py 的函数, 直接 import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gg_time_fading_model import fade_statistics

from scipy.stats import pearsonr, spearmanr


# ─── 参数（从 params.py 读, FR-20 P3 单一真相源）────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
ORIG_R4_PATH = RESULTS_DIR / 'r4_fade_correlation_results.json'

# ─── 修正参数（区别于原 R4 / Step B）────────────────────────
# SOP_RATE: 4e-7 rad/sym → 1 krad/s（sat.1553 §6.3 真实 OSL SOP 速率）
#   原 R4 / Step B 用 1e-4 rad/sym → 250 krad/s（250× 过快）
SOP_RATE = 4e-7  # rad/sym; × 2.5e9 sym/s = 1.0e3 rad/s = 1 krad/s
# N_SYMBOLS: 10M = 4ms 观测窗口（原 R4 用 5M = 2ms，AFD 无法计算）
N_SYMBOLS = 10_000_000
BLOCK_SIZE = BLOCK  # 100
N_BLOCKS = N_SYMBOLS // BLOCK_SIZE  # 100000

# 扫描维度（跟原 R4 一致，但只取有发散的 strong + uplink_strong）
TURB_LEVELS = {
    'strong': cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}
F_G_SWEEP = list(cfg.gg_time.GREENWOOD_FREQ_SWEEP)  # 30/100/300/1000 Hz
MU_SWEEP = [5e-4, 1e-3, 5e-3, 1e-2]
N_TAP = 11
N_TRIALS = 3

GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 20 dB (linear 100)
R2_QPSK = 1.0

# 衰落阈值：多档（跟 R4 一致），主指标用 0.3
FADE_THRESHOLDS = np.array([0.1, 0.3, 0.5])
DEEP_FADE_THR = 0.1
MAIN_THR = 0.3
# 发散触发窗口: diverge_idx 前 N_sym 符号（跟 R4 一致, ~10× block）
DIVERGE_LOOKBACK_SYM = 1000


# ─── QPSK 信号生成（跟 cma_divergence_scan.py 一致）──────────

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1 (sat.1553 §6 标准 QPSK)。"""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2*bits[0::2]) + 1j * (1 - 2*bits[1::2])) / np.sqrt(2)


# ─── 单次 trial（修正 SOP_RATE + 10M 符号）───────────────────

def run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed):
    """跑一次 CMA 发散测试（1 krad/s SOP, 10M 符号），返回是否发散 + 统计。

    信道模型跟 cma_divergence_scan.py 一致，唯一区别：
      theta = SOP_RATE * np.arange(N)  （4e-7 = 1 krad/s, 非 1e-4 = 250 krad/s）
    """
    rng = np.random.default_rng(seed)
    N = N_SYMBOLS
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    # 生成时间相关 GG 包络（Step A, 块内恒定块间 AR(1)）
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK_SIZE,
                         t_s=T_S, method='gar', seed=seed)

    # QPSK 信号
    s = gen_qpsk(N, rng)
    sY = gen_qpsk(N, rng)  # 独立符号（Y 偏振）

    # 噪声
    noise_var = 1.0 / (2 * GAMMA_BAR)
    noise_X = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    noise_Y = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    # SOP 旋转: sat.1553 Eq.(51) Jones J=rot(theta(t))
    # 修正: theta = 4e-7 * np.arange(N) → 1 krad/s（sat.1553 §6.3 真实 OSL SOP 速率）
    theta = SOP_RATE * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    rX = np.sqrt(h) * (cos_t * s + sin_t * sY) + noise_X
    rY = np.sqrt(h) * (-sin_t * s + cos_t * sY) + noise_Y

    eq = CMAEqualizer2x2(n_tap=n_tap, mu=mu, R2=R2_QPSK)
    res = eq.equalize(rX, rY)

    return {
        'h': h,
        'diverged': res['diverged'],
        'diverge_idx': res['diverge_idx'],
        'final_w_norm': res['final_w_norm'],
        'init_w_norm': res['init_w_norm'],
        'max_w_norm': float(np.max(res['w_norm_traj'])) if len(res['w_norm_traj']) > 0 else 0,
        'max_z_amp': float(np.max(res['z_amp_traj'])) if len(res['z_amp_traj']) > 0 else 0,
    }


# ─── 相关性工具（复用 R4 的 safe_corr）──────────────────────

def safe_corr(x, y):
    """算 Pearson + Spearman, 处理常量数组/小样本。"""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        return {'n': n, 'pearson': float('nan'), 'spearman': float('nan'),
                'p_pearson': float('nan'), 'p_spearman': float('nan')}
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
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


# ─── 主扫描 ─────────────────────────────────────────────────

def _ckpt_path():
    """检查点路径（部分结果，防中断丢失）。"""
    return RESULTS_DIR / 'r4_corrected_checkpoint.json'


def run_scan():
    """跑 96 trials (2 turb × 4 f_G × 4 μ × 1 tap × 3 seeds)，建 trial 表。"""
    total_combos = (len(TURB_LEVELS) * len(F_G_SWEEP) *
                    len(MU_SWEEP) * 1)  # tap 固定 11
    total_runs = total_combos * N_TRIALS
    print(f"扫描: {total_combos} combos × {N_TRIALS} trials = {total_runs} runs")
    print(f"  N_symbols={N_SYMBOLS} (4ms 窗口), SOP_RATE={SOP_RATE} rad/sym "
          f"({SOP_RATE*2.5e9/1e3:.0f} krad/s)")
    print(f"  turb={list(TURB_LEVELS.keys())}, f_G={F_G_SWEEP}")
    print(f"  mu={MU_SWEEP}, tap={N_TAP}", flush=True)

    trials_table = []
    # 断点续跑: 若 checkpoint 存在则加载已完成 trials
    ckpt = _ckpt_path()
    if ckpt.exists():
        try:
            with open(ckpt, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            trials_table = saved.get('trials_table', [])
            print(f"  [续跑] 从 checkpoint 恢复 {len(trials_table)} trials", flush=True)
        except Exception:
            trials_table = []
    run_count = len(trials_table)
    t_start = time.time()

    for turb_name, (alpha, beta) in TURB_LEVELS.items():
        for f_g in F_G_SWEEP:
            for mu in MU_SWEEP:
                for trial in range(N_TRIALS):
                    # seed 生成跟 Step B 一致（cma_divergence_scan.py L168）
                    seed = hash((turb_name, f_g, mu, N_TAP, trial)) % (2**32)
                    # 支持断点续跑: 若 checkpoint 已有该 trial 则跳过
                    key_match = any(
                        tt['turb_name'] == turb_name and tt['f_g_hz'] == float(f_g)
                        and tt['mu'] == mu and tt['seed'] == int(seed)
                        for tt in trials_table
                    )
                    if key_match:
                        run_count += 1
                        continue
                    res = run_single_trial(
                        turb_name, alpha, beta, f_g, mu, N_TAP, seed)
                    h = res['h']
                    diverged = res['diverged']
                    diverge_idx = res['diverge_idx']

                    # 块级 h（fade_statistics 输入）
                    h_blocks = h[::BLOCK_SIZE]
                    fs = fade_statistics(h_blocks, FADE_THRESHOLDS,
                                         BLOCK_SIZE, T_S)
                    total_time_s = len(h_blocks) * BLOCK_SIZE * T_S

                    idx_main = list(FADE_THRESHOLDS).index(MAIN_THR)
                    lcr_main = fs['lcr_per_sec'][idx_main]
                    afd_main = fs['afd_s'][idx_main]
                    p_below_main = fs['p_below'][idx_main]
                    n_events_main = lcr_main * total_time_s

                    # 深衰落 (thr=0.1) 统计
                    idx_deep = list(FADE_THRESHOLDS).index(DEEP_FADE_THR)
                    lcr_deep = fs['lcr_per_sec'][idx_deep]
                    afd_deep = fs['afd_s'][idx_deep]
                    n_events_deep = lcr_deep * total_time_s

                    # diverge_idx 处的 h 值 + 前窗口统计
                    diverge_h_val = None
                    diverge_pre_window_min_h = None
                    if diverge_idx is not None:
                        sym_idx = int(diverge_idx)
                        blk_idx = sym_idx // BLOCK_SIZE
                        if 0 <= blk_idx < len(h_blocks):
                            diverge_h_val = float(h_blocks[blk_idx])
                        blk_lo = max(0, (sym_idx - DIVERGE_LOOKBACK_SYM) // BLOCK_SIZE)
                        blk_hi = min(len(h_blocks), sym_idx // BLOCK_SIZE + 1)
                        if blk_hi > blk_lo:
                            window = h_blocks[blk_lo:blk_hi]
                            diverge_pre_window_min_h = float(np.min(window))

                    min_h = float(np.min(h_blocks))

                    trials_table.append({
                        'turb_name': turb_name,
                        'alpha': alpha, 'beta': beta,
                        'f_g_hz': float(f_g),
                        'tau_c_ms': cfg.gg_time.tau_c_from_fg(f_g) * 1e3,
                        'mu': mu,
                        'n_tap': N_TAP,
                        'seed': int(seed),
                        'diverged': bool(diverged),
                        'diverge_idx': (int(diverge_idx)
                                        if diverge_idx is not None else None),
                        # 主指标 (thr=0.3)
                        'afd_s': float(afd_main),
                        'lcr_per_sec': float(lcr_main),
                        'n_events': float(n_events_main),
                        'p_below': float(p_below_main),
                        # 深衰落 (thr=0.1)
                        'afd_deep_s': float(afd_deep),
                        'lcr_deep_per_sec': float(lcr_deep),
                        'n_events_deep': float(n_events_deep),
                        # 位置分析
                        'min_h': min_h,
                        'diverge_h_val': diverge_h_val,
                        'diverge_pre_window_min_h': diverge_pre_window_min_h,
                    })
                    # 增量 checkpoint（每 trial 后写盘，防中断丢失）
                    try:
                        with open(ckpt, 'w', encoding='utf-8') as f:
                            json.dump({'trials_table': trials_table,
                                       'n_done': len(trials_table)}, f,
                                      indent=1, default=str)
                    except Exception:
                        pass

                    run_count += 1
                    elapsed = time.time() - t_start
                    eta = elapsed / run_count * (total_runs - run_count)
                    if run_count % 8 == 0 or run_count <= 4:
                        print(f"  [{run_count}/{total_runs}] {turb_name} f_G={f_g}"
                              f" μ={mu} → div={'Y' if diverged else 'N'}"
                              f"  [{elapsed:.0f}s, ETA {eta:.0f}s]", flush=True)

    return trials_table


# ─── 相关性分析（复用 R4 逻辑）──────────────────────────────

def compute_correlations(trials_table):
    """算相关系数。聚合到 P_div（按 turb×f_g×mu×tap, 3 trials 均值）。"""
    results = {}

    groups = defaultdict(list)
    for t in trials_table:
        key = (t['turb_name'], t['f_g_hz'], t['mu'], t['n_tap'])
        groups[key].append(t)

    agg = []
    for key, ts in groups.items():
        turb, f_g, mu, tap = key
        p_div = np.mean([t['diverged'] for t in ts])
        afd_mean = np.mean([t['afd_s'] for t in ts])
        afd_deep_mean = np.mean([t['afd_deep_s'] for t in ts])
        lcr_mean = np.mean([t['lcr_per_sec'] for t in ts])
        n_events_mean = np.mean([t['n_events'] for t in ts])
        n_events_deep_mean = np.mean([t['n_events_deep'] for t in ts])
        agg.append({
            'turb': turb, 'f_g': f_g, 'mu': mu, 'tap': tap,
            'p_div': p_div, 'afd_mean': afd_mean, 'afd_deep_mean': afd_deep_mean,
            'lcr_mean': lcr_mean, 'n_events_mean': n_events_mean,
            'n_events_deep_mean': n_events_deep_mean,
            'n_trials': len(ts),
        })

    p_divs = np.array([a['p_div'] for a in agg])
    afds = np.array([a['afd_mean'] for a in agg])
    lcrs = np.array([a['lcr_mean'] for a in agg])
    n_events = np.array([a['n_events_mean'] for a in agg])
    f_gs = np.array([a['f_g'] for a in agg])
    mus = np.array([a['mu'] for a in agg])

    results['overall'] = {
        'P_div_vs_AFD': safe_corr(afds, p_divs),
        'P_div_vs_LCR': safe_corr(lcrs, p_divs),
        'P_div_vs_n_events': safe_corr(n_events, p_divs),
        'P_div_vs_fG': safe_corr(f_gs, p_divs),
        'P_div_vs_mu': safe_corr(np.log10(mus), p_divs),
        'n_combos': len(agg),
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

    # 固定 f_G 下 P_div vs LCR/AFD
    results['within_fG'] = {}
    for f_g_val in sorted(set(f_gs.tolist())):
        mask = f_gs == f_g_val
        results['within_fG'][str(int(f_g_val))] = {
            'P_div_vs_AFD': safe_corr(afds[mask], p_divs[mask]),
            'P_div_vs_LCR': safe_corr(lcrs[mask], p_divs[mask]),
        }

    # 固定 turb
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

    # Trial 级别
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


# ─── diverge_idx 位置分析（复用 R4 逻辑）────────────────────

def analyze_diverge_location(trials_table):
    """分析 diverge_idx 位置 vs h 值：发散是否由深衰落触发。

    跟 R4 一致：重新算 [0, diverge_idx] 前窗口的 min_h + 深衰落事件数，
    跟同配置非发散 trial 全序列 min_h 对比。
    """
    from scipy.stats import mannwhitneyu

    diverged_trials = [t for t in trials_table if t['diverged']
                       and t['diverge_h_val'] is not None]
    nondiv_trials = [t for t in trials_table if not t['diverged']]

    if not diverged_trials:
        return {'n_diverged_with_h': 0, 'note': 'No diverged trials with h value'}

    nondiv_min_by_cfg = defaultdict(list)
    for t in nondiv_trials:
        key = (t['turb_name'], t['f_g_hz'], t['mu'], t['n_tap'])
        nondiv_min_by_cfg[key].append(t['min_h'])

    div_h_vals = np.array([t['diverge_h_val'] for t in diverged_trials])
    min_h_vals = np.array([t['min_h'] for t in diverged_trials])
    div_idx = np.array([t['diverge_idx'] for t in diverged_trials])

    # 重新算前窗口统计（用已存的 h；trial_table 没存 h, 重新生成块级 h）
    pre_div_min_h = []
    pre_div_events_thr03 = []
    matched_nondiv_min = []
    loc_thr = 0.3
    for t in diverged_trials:
        seed = t['seed']
        tau_c = cfg.gg_time.tau_c_from_fg(t['f_g_hz'])
        h_blocks = gg_time_envelope_blockwise(
            N_BLOCKS, t['alpha'], t['beta'], tau_c,
            block=BLOCK_SIZE, t_s=T_S, method='gar', seed=seed)
        div_blk = t['diverge_idx'] // BLOCK_SIZE
        pre_h = h_blocks[:div_blk] if div_blk > 0 else h_blocks[:1]
        pre_div_min_h.append(float(np.min(pre_h)))
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
        'diverge_h_mean': float(np.mean(div_h_vals)),
        'diverge_h_median': float(np.median(div_h_vals)),
        # 发散位置（占序列比例）
        'diverge_idx_frac_mean': float(np.mean(div_idx / N_SYMBOLS)),
        'diverge_idx_frac_median': float(np.median(div_idx / N_SYMBOLS)),
        'pct_diverge_early_lt10pct': float(np.mean(div_idx < 0.1 * N_SYMBOLS)),
        'pct_diverge_before_25pct': float(np.mean(div_idx < 0.25 * N_SYMBOLS)),
        # 前窗口 [0, diverge_idx] 统计
        'pre_div_min_h_mean': float(np.mean(pre_div_min_h)),
        'pre_div_min_h_median': float(np.median(pre_div_min_h)),
        'matched_nondiv_min_h_mean': float(np.mean(matched_nondiv_min_h)),
        'matched_nondiv_min_h_median': float(np.median(matched_nondiv_min_h)),
        # 前窗口深衰落事件数
        'pre_div_events_thr03_mean': float(np.mean(pre_div_events)),
        'pre_div_events_thr03_median': float(np.median(pre_div_events)),
        'pct_pre_div_zero_events': float(np.mean(pre_div_events == 0)),
        'pct_pre_div_le2_events': float(np.mean(pre_div_events <= 2)),
        # 全序列 min_h
        'min_h_mean_diverged_full': float(np.mean(min_h_vals)),
        'min_h_mean_nondiverged_full': float(
            np.mean([t['min_h'] for t in nondiv_trials])) if nondiv_trials else None,
    }

    if len(matched_nondiv_min_h) > 3:
        try:
            u, p = mannwhitneyu(pre_div_min_h, matched_nondiv_min_h, alternative='less')
            result['mw_pre_div_min_lt_nondiv_p'] = float(p)
        except Exception:
            pass
    nondiv_all_min = np.array([t['min_h'] for t in nondiv_trials]) if nondiv_trials else np.array([])
    if len(nondiv_all_min) > 3 and len(min_h_vals) > 3:
        try:
            u, p = mannwhitneyu(min_h_vals, nondiv_all_min, alternative='less')
            result['mw_fullseq_min_div_lt_nondiv_p'] = float(p)
        except Exception:
            pass

    return result


# ─── AFD 可计算性分析（R4 修正新增）─────────────────────────

def analyze_afd_computability(trials_table):
    """检查 AFD 是否可计算（10M 符号 = 4ms 是否够长）。

    R4 原（5M=2ms）AFD 多为 inf（无下穿事件）。这里统计：
      - 各阈值下 AFD 有限（非 inf）的比例
      - AFD 中位数（剔除 inf）
    """
    results = {}
    for thr_label, thr in [('thr_0.1', DEEP_FADE_THR), ('thr_0.3', MAIN_THR)]:
        # 用深衰落/主阈值的 afd（trial 级）
        if thr == DEEP_FADE_THR:
            afds = np.array([t['afd_deep_s'] for t in trials_table])
            n_events = np.array([t['n_events_deep'] for t in trials_table])
        else:
            afds = np.array([t['afd_s'] for t in trials_table])
            n_events = np.array([t['n_events'] for t in trials_table])
        finite_mask = np.isfinite(afds)
        finite_afds = afds[finite_mask]
        results[thr_label] = {
            'n_trials': len(afds),
            'n_finite': int(finite_mask.sum()),
            'pct_finite': float(finite_mask.mean()),
            'afd_finite_median_ms': (float(np.median(finite_afds) * 1e3)
                                     if len(finite_afds) > 0 else None),
            'afd_finite_mean_ms': (float(np.mean(finite_afds) * 1e3)
                                   if len(finite_afds) > 0 else None),
            'n_events_mean': float(np.mean(n_events)),
            'n_events_median': float(np.median(n_events)),
            'pct_zero_events': float(np.mean(n_events == 0)),
        }
    return results


# ─── 汇总打印 + 对比 ────────────────────────────────────────

def print_summary(corr_results, loc_results, afd_results, agg, orig_r4):
    """打印汇总表 + 跟原 R4 对比。"""
    print("\n" + "=" * 72)
    print("R4 修正验证: 1 krad/s SOP + 10M 符号 (Q-CMA-FADE)")
    print("=" * 72)

    print(f"\n聚合组合数: {corr_results['overall']['n_combos']} "
          f"(2 turb × 4 f_G × 4 μ × 1 tap)")
    tl = corr_results['trial_level']
    print(f"Trial 总数: {tl['n_trials']}, 发散: {tl['n_diverged']} "
          f"({tl['n_diverged']/tl['n_trials']*100:.0f}%)")

    print("\n--- 整体相关（组合级, P_div vs X）| 修正 vs 原始 R4 ---")
    o = corr_results['overall']
    orig_o = orig_r4.get('correlations', {}).get('overall', {})
    print(f"  {'指标':22s} {'修正(1krad/s,10M)':>22s}   {'原始(250krad/s,5M)':>22s}")
    for name in ['P_div_vs_mu', 'P_div_vs_fG', 'P_div_vs_LCR',
                 'P_div_vs_n_events', 'P_div_vs_AFD']:
        c = o[name]
        oc = orig_o.get(name, {})
        def _fmt(d):
            if d is None or (isinstance(d, dict) and d.get('pearson', 'nan') != d.get('pearson', 'nan') and np.isnan(d.get('pearson', float('nan')))):
                return 'nan'
            if isinstance(d, dict):
                if np.isnan(d.get('pearson', float('nan'))):
                    return f"r=nan (ρ={d['spearman']:+.2f})"
                return f"r={d['pearson']:+.3f} (ρ={d['spearman']:+.2f})"
            return str(d)
        print(f"  {name:22s} {_fmt(c):>22s}   {_fmt(oc):>22s}")

    print("\n--- 固定 μ 下 P_div vs LCR/AFD/fG（关键检验: 控制 μ）---")
    for mu_val, c in sorted(corr_results['within_mu'].items()):
        lcr_c = c['P_div_vs_LCR']
        afd_c = c['P_div_vs_AFD']
        fg_c = c['P_div_vs_fG']
        print(f"  μ={float(mu_val):.0e}: "
              f"~LCR r={lcr_c['pearson']:+.3f}(p={lcr_c['p_pearson']:.2f}) | "
              f"~AFD r={afd_c['pearson']:+.3f} | "
              f"~fG r={fg_c['pearson']:+.3f}(p={fg_c['p_pearson']:.3f}) [n={lcr_c['n']}]")

    print("\n--- 固定 f_G 下 P_div vs LCR/AFD ---")
    for f_g_val, c in sorted(corr_results['within_fG'].items()):
        lcr_c = c['P_div_vs_LCR']
        afd_c = c['P_div_vs_AFD']
        print(f"  f_G={f_g_val:>4s}Hz: "
              f"~LCR r={lcr_c['pearson']:+.3f}(p={lcr_c['p_pearson']:.2f}) | "
              f"~AFD r={afd_c['pearson']:+.3f} [n={lcr_c['n']}]")

    print("\n--- Trial 级别: diverged(0/1) vs LCR/n_events/AFD ---")
    print(f"  diverged~LCR: r={tl['diverged_vs_LCR']['pearson']:+.3f} "
          f"(p={tl['diverged_vs_LCR']['p_pearson']:.1e}) | "
          f"~n_evt: r={tl['diverged_vs_n_events']['pearson']:+.3f} | "
          f"~AFD: r={tl['diverged_vs_AFD']['pearson']:+.3f}")

    # === diverge_idx 位置对比 ===
    print("\n--- diverge_idx 位置 | 修正 vs 原始 R4 ---")
    orig_loc = orig_r4.get('diverge_location', {})
    if loc_results['n_diverged_with_h'] > 0:
        print(f"  发散 trial 数: 修正={loc_results['n_diverged_with_h']} | "
              f"原始={orig_loc.get('n_diverged_with_h', '?')}")
        print(f"  median 发散位置: 修正={loc_results['diverge_idx_frac_median']*100:.0f}% | "
              f"原始={orig_loc.get('diverge_idx_frac_median', 0)*100:.0f}%")
        print(f"  早发散(<10%): 修正={loc_results['pct_diverge_early_lt10pct']*100:.0f}% | "
              f"原始={orig_loc.get('pct_diverge_early_lt10pct', 0)*100:.0f}%")
        print(f"  发散前(<25%): 修正={loc_results['pct_diverge_before_25pct']*100:.0f}% | "
              f"原始={orig_loc.get('pct_diverge_before_25pct', 0)*100:.0f}%")

    # === 前窗口深衰落事件对比 ===
    print("\n--- diverged trial 前窗口深衰落事件 | 修正 vs 原始 R4 ---")
    print(f"  前窗口 0 事件占比: 修正={loc_results['pct_pre_div_zero_events']*100:.0f}% | "
          f"原始={orig_loc.get('pct_pre_div_zero_events', 0)*100:.0f}%")
    print(f"  前窗口 ≤2 事件占比: 修正={loc_results['pct_pre_div_le2_events']*100:.0f}% | "
          f"原始={orig_loc.get('pct_pre_div_le2_events', 0)*100:.0f}%")
    print(f"  前窗口事件 median: 修正={loc_results['pre_div_events_thr03_median']:.0f} | "
          f"原始={orig_loc.get('pre_div_events_thr03_median', 0):.0f}")
    print(f"  前窗口 min_h median: 修正={loc_results['pre_div_min_h_median']:.4f} | "
          f"原始={orig_loc.get('pre_div_min_h_median', 0):.4f}")
    print(f"  发散.min vs 非发散.min (median): 修正={loc_results['pre_div_min_h_median']:.4f} vs "
          f"{loc_results['matched_nondiv_min_h_median']:.4f} | "
          f"原始={orig_loc.get('pre_div_min_h_median', 0):.4f} vs "
          f"{orig_loc.get('matched_nondiv_min_h_median', 0):.4f}")

    # === AFD 可计算性 ===
    print("\n--- AFD 可计算性（10M=4ms 是否够长）---")
    for thr_label in ['thr_0.1', 'thr_0.3']:
        a = afd_results[thr_label]
        print(f"  {thr_label}: AFD 有限 {a['pct_finite']*100:.0f}% "
              f"(finite median={a['afd_finite_median_ms']}ms), "
              f"n_events median={a['n_events_median']:.0f}, "
              f"0事件占 {a['pct_zero_events']*100:.0f}%")

    # === P_div 汇总表 ===
    print("\n--- P_div 汇总（turb × f_G, 跨 μ 平均）---")
    tf_pdiv = defaultdict(list)
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
            row += f"  {np.mean(vals):>7.2f}" if vals else f"  {'N/A':>7}"
        print(row)


def main():
    print("=== R4 修正验证: 真实 SOP 速率 (1 krad/s) + 10M 符号 ===")
    print(f"参数: N_symbols={N_SYMBOLS} (4ms 窗口), block={BLOCK_SIZE}, "
          f"n_blocks={N_BLOCKS}, t_s={T_S:.2e}s")
    print(f"SOP_RATE={SOP_RATE} rad/sym = {SOP_RATE*2.5e9/1e3:.0f} krad/s "
          f"(原 R4 用 1e-4 = 250 krad/s, 250× 过快)")
    print(f"衰落阈值: h<{DEEP_FADE_THR} (深衰落), 主指标 h<{MAIN_THR}")

    print(f"\n读取原始 R4 结果用于对比: {ORIG_R4_PATH}")
    orig_r4 = {}
    if ORIG_R4_PATH.exists():
        with open(ORIG_R4_PATH, 'r', encoding='utf-8') as f:
            orig_r4 = json.load(f)
        print(f"  原始 R4: n_symbols={orig_r4['meta']['n_symbols']}, "
              f"n_diverged={orig_r4['diverge_location'].get('n_diverged_with_h', '?')}")
    else:
        print(f"  [警告] 原始 R4 结果不存在, 仅打印修正结果")

    print("\n[1/4] 跑 96 trials (1 krad/s SOP, 10M 符号)...")
    t0 = time.time()
    trials_table = run_scan()
    print(f"  完成: {len(trials_table)} trials, 耗时 {time.time()-t0:.0f}s")

    print("\n[2/4] 算相关系数...")
    corr_results, agg = compute_correlations(trials_table)

    print("\n[3/4] 分析 diverge_idx 位置 vs h 值...")
    loc_results = analyze_diverge_location(trials_table)

    print("\n[4/4] 分析 AFD 可计算性...")
    afd_results = analyze_afd_computability(trials_table)

    # 打印汇总 + 对比
    print_summary(corr_results, loc_results, afd_results, agg, orig_r4)

    # 保存结果
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R4-corrected (修正 SOP 速率 1 krad/s + 10M 符号)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'block': BLOCK_SIZE,
            'n_blocks': N_BLOCKS,
            'sop_rate_rad_per_sym': SOP_RATE,
            'sop_rate_krad_per_s': SOP_RATE * 2.5e9 / 1e3,
            'fade_threshold_deep': DEEP_FADE_THR,
            'fade_threshold_main': MAIN_THR,
            'n_tap': N_TAP,
            'n_trials_per_combo': N_TRIALS,
            'correction_note': ('原 R4 用 SOP_RATE=1e-4 (250 krad/s) + 5M 符号 (2ms); '
                                '本修正用 4e-7 (1 krad/s, sat.1553 §6.3 真实值) + '
                                '10M 符号 (4ms)'),
            'orig_r4_source': str(ORIG_R4_PATH.relative_to(SIM_DIR)),
        },
        'correlations': corr_results,
        'diverge_location': loc_results,
        'afd_computability': afd_results,
        'trial_table': trials_table,
        'agg_table': agg,
    }
    out_path = RESULTS_DIR / 'r4_corrected_results.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")

    return out


if __name__ == '__main__':
    main()
