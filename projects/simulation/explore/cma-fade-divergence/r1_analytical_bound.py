"""R1 — CMA 发散半解析界推导 + Step B 实测验证。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P5 docstring 标方向+状态)

补 sat.1553 §6.3 L778 自认空白:
  "the probability of the equalizer diverging to a local optimum during
   deep fades has not been analyzed here but could have a major impact"

本脚本 (R1) 推导 CMA 发散概率的半解析界，并用 Step B 的 128 组合 Monte Carlo
实测 P_div 验证。验证有效则该界可作为 Step D 性能门控/预算设计的闭式工具，
无需再跑昂贵 Monte Carlo。

═══ 半解析界推导 (TL-20 + 本脚本形式化) ═══

物理机制 (深衰落 h→0): 接收信号 r = √h·s + n ≈ n (纯噪声)。CMA 块级更新
  W[k+1] = W[k] + μ · mean_k(e·r*),  e = R² − |z|²
深衰落下 z = w·r ≈ w·n, |z|² ∝ |w|²·σ_n² (R²=1 几乎不抵消)。梯度由噪声 r*=n*
驱动，每块更新是均值为 0、方差 ∝ σ_n² 的随机增量 → W 做随机游走。

(a) 单次深衰落内漂移
  一次深衰落持续 AFD 秒。CMA 块级更新周期 = block_size·T_S (块内符号数 × 符号周期)。
  一次衰落内更新次数 N_block = AFD / (block_size·T_S)。
  每块更新 ∥ΔW∥ 的量级 ∝ μ·R²·σ_n (深衰落梯度 ∝ R²·|n|, |z|²项被 R² 主导)。
  N_block 步随机游走累积: ∥ΔW∥_total ∝ μ·R²·σ_n·√N_block  (√N 律)。
  ┌──────────────────────────────────────────────────────────────┐
  │  drift_per_fade = μ · R² · σ_n · √(AFD / (block_size·T_S))  │
  └──────────────────────────────────────────────────────────────┘

(b) 单次衰落发散概率
  发散判据 (_cma.py:133): ∥W∥ > threshold = 10×∥W₀∥ (W₀=中心抽头初始化)。
  对 n_tap tap 蝶形 (2×2): ∥W₀∥=√2 (wxx/wyy 中心=1 各贡献 1), threshold=10√2。
  假设块漂移 ∥ΔW∥ 近高斯 (CLT, N_block 个独立增量), σ_drift=drift_per_fade:
  ┌─────────────────────────────────────────────────────────┐
  │  P_single = 2·Q(threshold / σ_drift)                    │
  └─────────────────────────────────────────────────────────┘
  (因子 2: 单边累积漂移可正可负, 两尾都触发范数超阈; 此处用 √律量级估计)

(c) 整体观测窗口发散概率
  观测窗口 T_obs = N_symbols·T_S 内深衰落事件数 N_events = LCR·T_obs
  (LCR = level crossing rate, 每秒向下跨过 threshold_h 的次数)。
  假设各次衰落独立: ┌───────────────────────────────────────────┐
  │  P_div = 1 − (1 − P_single)^{N_events}     │
  └───────────────────────────────────────────────────┘

n_tap 依赖: 本 √律模型不显式含 n_tap (只含 ∥W₀∥=√2)。实测 tap=22 vs 11
差异来自更多 tap → 更多自由度随机游走 → 实际 σ_drift ∝ √n_tap。本脚本试
σ_drift ∝ √n_tap 修正看是否提升拟合。

用法:
  cd projects/simulation && python explore/cma-fade-divergence/r1_analytical_bound.py
"""
import sys
import os
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime

# 路径设置: 确保从 projects/simulation/ 运行
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope

# 从 gg_time_fading_model.py 复用 fade_statistics (AFD/LCR 估计器)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gg_time_fading_model import fade_statistics


# ─── 参数 (FR-20 溯源, 从 params.py 读, 不硬编码) ──────────────

cfg = SimulationConfig()

T_S = cfg.system.T_S                  # 4e-10 s
BLOCK = cfg.experiment.BLOCK          # 100 (信道块大小)
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 (20 dB)
CMA_BLOCK_SIZE = 64                   # CMA 块级更新大小 (_cma.py:100, 非 BLOCK)

TURB_LEVELS = {
    'weak':          cfg.turbulence.as_dict()['weak'],
    'moderate':      cfg.turbulence.as_dict()['moderate'],
    'strong':        cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}
F_G_SWEEP = list(cfg.gg_time.GREENWOOD_FREQ_SWEEP)  # 30/100/300/1000 Hz
TAU_C_COEFF = cfg.gg_time.TAU_C_COEFF               # 1/(2π)

# Step B 实测参数 (从 results JSON meta 读, 但此处用脚本已知值生成对应包络)
N_SYMBOLS = 5_000_000                # Step B 用 5M 符号
N_TRIALS = 3
MU_SWEEP = [5e-4, 1e-3, 5e-3, 1e-2]
TAP_SWEEP = [11, 22]

# 深衰落强度阈值 h (归一化 GG 包络, 均值=1)。敏感性扫描用。
FADE_THRESHOLDS_H = [0.05, 0.1, 0.2, 0.3, 0.5]
# AFD/LCR 估计序列长度 (要远大于最长 τ_c 以获稳定统计)
N_AFD_SYMBOLS = 50_000_000           # 50M 符号 (覆盖 f_G=30Hz τ_c=5.3ms)

# 噪声 σ_n (复 AWGN): σ_n² = 1/(2·γ̄), σ_n = √(1/(2·γ̄))
SIGMA_N = float(np.sqrt(1.0 / (2.0 * GAMMA_BAR)))
R2_QPSK = 1.0                        # QPSK 恒模 R²=1 (Godard 1980)

# 发散阈值: ∥W∥ > 10×∥W₀∥。2×2 蝶形 ∥W₀∥=√2 (wxx/wyy 中心抽头各 1)
W0_NORM = np.sqrt(2.0)
THRESHOLD = 10.0 * W0_NORM           # = 10√2 ≈ 14.14


# ─── 半解析界核心公式 ───────────────────────────────────────

def drift_per_fade(mu, r2, sigma_n, afd_s, block_size, t_s):
    """(a) 单次深衰落内 CMA 系数随机游走漂移量。

    drift = μ · R² · σ_n · √(AFD / (block_size·T_S))  [√N_block 律]

    参数
    ----
    mu : CMA 步长
    r2 : 恒模半径平方 (QPSK=1)
    sigma_n : 复噪声标准差 = √(1/(2γ̄))
    afd_s : 单次深衰落平均持续 (秒)
    block_size : CMA 块级更新大小 (符号数, _cma.py=64)
    t_s : 符号周期 (秒)
    """
    n_block = afd_s / (block_size * t_s)  # 一次衰落内 CMA 更新次数
    n_block = max(n_block, 1.0)           # 防下溢
    return mu * r2 * sigma_n * np.sqrt(n_block)


def p_single(drift, threshold, kappa=1.0):
    """(b) 单次衰落发散概率 = 2·Q(threshold/drift)。

    drift 近高斯 (CLT, N_block 个独立增量)。两尾 (∥W∥>threshold 任一方向) 都触发。
    κ: 放大系数 (校准用)。纯噪声 √律模型保守 (κ=1 预测 P≈0), 实测发散远高于
    此——深衰落下 |w| 增长反馈使 e=R²−|z|² 随 |w|² 放大 → 自放大不稳定。κ 吸收
    该反馈 + per-block 非平均效应, 使模型数量级匹配实测, 同时保留 √律函数形式。
    """
    drift_eff = kappa * drift
    if drift_eff <= 0:
        return 0.0
    ratio = threshold / drift_eff
    if ratio > 37:  # Q(x>37) 下溢
        return 0.0
    return float(2.0 * _qfunc(ratio))


def p_div_observed(p1, n_events):
    """(c) 观测窗口整体发散概率 = 1 − (1−P_single)^{N_events}。

    各次衰落独立假设。N_events = LCR·T_obs。
    """
    if n_events <= 0:
        return 0.0
    if p1 <= 0:
        return 0.0
    if p1 >= 1:
        return 1.0 - (1e-300) ** n_events
    # 用对数防下溢
    log_survive = n_events * np.log1p(-p1)
    return float(1.0 - np.exp(log_survive))


def _qfunc(x):
    """Q 函数 = 1 − Φ(x) = 0.5·erfc(x/√2)。"""
    from scipy.special import erfc
    return 0.5 * erfc(x / np.sqrt(2.0))


# ─── n_tap 修正 (更多 tap → 更多自由度随机游走) ──────────────

def drift_with_tap(mu, r2, sigma_n, afd_s, block_size, t_s, n_tap,
                   ntap_exp=0.5):
    """带 n_tap 修正的漂移: σ_drift ∝ (n_tap/n_ref)^{ntap_exp}。

    ntap_exp=0: 无修正 (基础 √律)。ntap_exp=0.5: σ_drift ∝ √n_tap。
    n_ref=11 (基准 tap, 使 tap=11 时修正=1)。
    """
    base = drift_per_fade(mu, r2, sigma_n, afd_s, block_size, t_s)
    n_ref = 11.0
    return base * (n_tap / n_ref) ** ntap_exp


# ─── AFD/LCR 估计 (复用 fade_statistics) ────────────────────

def estimate_fade_stats(turb_name, f_g, fade_thresh_h,
                        n_symbols=N_AFD_SYMBOLS, n_seeds=3):
    """对给定 (turb, f_g) 估计 AFD/LCR at fade_thresh_h。

    seed 跟 Step B 一致: seed = hash((turb_name, f_g, mu, n_tap, trial)) % 2**32
    但 fade_statistics 只依赖 turb+f_g+seed → 取一个代表 mu/n_tap/trial 组合的
    seed 集 (此处用 mu=1e-3, tap=11, trial=0..n_seeds-1, 跟 Step B 的 3 个 trial
    seed 对齐, 因 Step B 同 (turb,fg) 下不同 mu/tap 的 trial=0 seed 不同)。

    对 n_seeds 个 seed 生成包络, 平均 AFD/LCR (降低单序列方差)。

    返回 AFD(秒) + LCR(1/秒)。
    """
    alpha, beta = TURB_LEVELS[turb_name]
    tau_c = TAU_C_COEFF / f_g
    block = BLOCK
    t_s = T_S

    n_blocks = n_symbols // block
    afds = []
    lcrs = []
    for trial in range(n_seeds):
        # 用 Step B 的 seed 公式 (固定 mu=1e-3, tap=11 代表, 因 fade_stats
        # 只依赖 turb+fg+seed; 多 seed 平均降方差)
        seed = hash((turb_name, f_g, 1e-3, 11, trial)) % (2 ** 32)
        h = gg_time_envelope(n_symbols, alpha, beta, tau_c,
                             block=block, t_s=t_s, method='gar', seed=seed)
        h_blocks = h[::block][:n_blocks]

        thresholds = np.array([fade_thresh_h])
        fs = fade_statistics(h_blocks, thresholds, block, t_s)
        afd = fs['afd_s'][0]
        lcr = fs['lcr_per_sec'][0]
        if np.isfinite(afd):
            afds.append(afd)
        if np.isfinite(lcr):
            lcrs.append(lcr)

    afd_mean = float(np.mean(afds)) if afds else float('inf')
    lcr_mean = float(np.mean(lcrs)) if lcrs else 0.0
    return afd_mean, lcr_mean


# ─── 预测 P_div (单组合) ─────────────────────────────────────

def predict_p_div(turb_name, f_g, mu, n_tap, fade_thresh_h,
                  afd_s, lcr, ntap_exp=0.0, kappa=1.0):
    """解析界预测 P_div for (turb, f_g, mu, n_tap)。

    afd_s, lcr 由 estimate_fade_stats 预算 (per turb+f_g+threshold)。
    ntap_exp: n_tap 修正指数 (0=无, 0.5=√n_tap)。
    kappa: 放大系数 (校准用, 见 p_single 文档)。
    """
    drift = drift_with_tap(mu, R2_QPSK, SIGMA_N, afd_s, CMA_BLOCK_SIZE,
                           T_S, n_tap, ntap_exp)
    p1 = p_single(drift, THRESHOLD, kappa)
    t_obs = N_SYMBOLS * T_S
    n_events = lcr * t_obs
    return p_div_observed(p1, n_events)


# ─── R² + 趋势一致性 ────────────────────────────────────────

def r_squared(y_true, y_pred):
    """决定系数 R² (y_pred 解释 y_true 方差比例)。

    R² = 1 − SS_res/SS_tot。可负 (模型比均值还差)。
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1.0 - ss_res / ss_tot)


def trend_consistency(y_true, y_pred):
    """趋势一致性: monotonic 相关 (Spearman ρ 的符号化简化版)。

    返回: 对所有 (i,j) 对, (y_true[i]−y_true[j]) 与 (y_pred[i]−y_pred[j])
    同号的比例 (排除相等对)。
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    n = len(y_true)
    concord = 0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            dt = y_true[i] - y_true[j]
            dp = y_pred[i] - y_pred[j]
            if dt == 0 or dp == 0:
                continue
            total += 1
            if np.sign(dt) == np.sign(dp):
                concord += 1
    if total == 0:
        return 0.0
    return concord / total


# ─── 主验证 ─────────────────────────────────────────────────

def load_measured():
    """读 Step B 实测结果。"""
    res_path = SIM_DIR / 'results' / 'cma-fade-divergence' / \
        'cma_divergence_scan_results.json'
    with open(res_path, encoding='utf-8') as f:
        d = json.load(f)
    return d


def main():
    t_start = time.time()
    print("=" * 70)
    print("R1 — CMA 发散半解析界推导 + Step B 实测验证")
    print("=" * 70)
    print(f"σ_n = √(1/(2γ̄)) = √(1/(2·{GAMMA_BAR})) = {SIGMA_N:.5f}")
    print(f"∥W₀∥ = √2 = {W0_NORM:.4f}, threshold = 10·∥W₀∥ = {THRESHOLD:.4f}")
    print(f"CMA block_size = {CMA_BLOCK_SIZE} (非信道 BLOCK={BLOCK})")
    print(f"T_obs = {N_SYMBOLS}·T_S = {N_SYMBOLS*T_S*1e3:.3f} ms")
    print()

    measured = load_measured()
    mres = measured['results']
    print(f"实测: {len(mres)} 组合, "
          f"非零 P_div: {sum(1 for r in mres if r['p_div']>0)}")

    # ─── Step 1: 预算所有 (turb, f_g, threshold) 的 AFD/LCR ───
    # (缓存到磁盘, 避免重复 50M 包络生成的 ~5min 开销)
    cache_path = SIM_DIR / 'results' / 'cma-fade-divergence' / \
        'r1_fade_stats_cache.json'
    fade_stats_cache = {}
    if cache_path.exists():
        with open(cache_path, encoding='utf-8') as f:
            raw = json.load(f)
        for k, v in raw.items():
            t, fg, h = k.split('|')
            fade_stats_cache[(t, float(fg), h)] = tuple(v)
        print(f"  [缓存命中] 加载 {len(fade_stats_cache)} 条 AFD/LCR")

    need_compute = [(t, fg, str(h)) for h in FADE_THRESHOLDS_H
                    for t in TURB_LEVELS for fg in F_G_SWEEP
                    if (t, fg, str(h)) not in fade_stats_cache]
    if need_compute:
        print(f"\n--- 估算 AFD/LCR (N={N_AFD_SYMBOLS} 符号/seed, "
              f"3 seeds 平均, {len(need_compute)} 新条目) ---")
        for (turb_name, f_g, fade_h_str) in need_compute:
            afd, lcr = estimate_fade_stats(turb_name, f_g, float(fade_h_str))
            fade_stats_cache[(turb_name, f_g, fade_h_str)] = (afd, lcr)
        # 持久化缓存
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        raw = {f'{t}|{fg}|{h}': list(v)
               for (t, fg, h), v in fade_stats_cache.items()}
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)
        elapsed = time.time() - t_start
        print(f"  [缓存写入] {cache_path.name} [{elapsed:.0f}s]")
    else:
        print(f"  [缓存完整, 跳过 AFD/LCR 估算]")

    # ─── Step 2: 对每个 threshold + ntap_exp 组合, 拟合 κ 后算预测 + R² ───
    # κ 用网格搜索最小化 SS_res (κ 是唯一自由度, 使模型数量级匹配实测)
    print(f"\n--- 预测 P_div + 拟合优度 (R²/趋势, 含 κ 标定) ---")
    sensitivity = []  # [{threshold, ntap_exp, kappa, r2, trend, n}]

    KAPPA_GRID = np.logspace(1.5, 4.0, 30)  # 30..1e4 对数网格

    for fade_h in FADE_THRESHOLDS_H:
        for ntap_exp in [0.0, 0.5]:
            # 先算每组 base drift (κ=1)
            base_drifts = []
            y_true_list = []
            for r in mres:
                turb = r['turb_name']
                fg = r['f_g_hz']
                mu = r['mu']
                n_tap = r['n_tap']
                afd, lcr = fade_stats_cache[(turb, fg, str(fade_h))]
                bd = drift_with_tap(mu, R2_QPSK, SIGMA_N, afd,
                                    CMA_BLOCK_SIZE, T_S, n_tap, ntap_exp)
                base_drifts.append((bd, lcr))
                y_true_list.append(r['p_div'])
            y_true_arr = np.array(y_true_list)
            t_obs = N_SYMBOLS * T_S

            # 网格搜 κ 最小化 SS_res
            best_kappa = KAPPA_GRID[0]
            best_ss = np.inf
            best_pred = None
            for kap in KAPPA_GRID:
                preds = []
                for (bd, lcr) in base_drifts:
                    p1 = p_single(bd, THRESHOLD, kap)
                    preds.append(p_div_observed(p1, lcr * t_obs))
                preds = np.array(preds)
                ss = np.sum((y_true_arr - preds) ** 2)
                if ss < best_ss:
                    best_ss = ss
                    best_kappa = kap
                    best_pred = preds
            r2 = r_squared(y_true_arr, best_pred)
            tc = trend_consistency(y_true_arr, best_pred)
            sensitivity.append({
                'fade_threshold_h': fade_h, 'ntap_exp': ntap_exp,
                'kappa': float(best_kappa),
                'r_squared': r2, 'trend_consistency': tc,
                'n_combos': len(y_true_arr),
            })
            print(f"  thresh_h={fade_h} ntap_exp={ntap_exp}: "
                  f"κ={best_kappa:.0f}  R²={r2:+.3f}  trend={tc:.3f}")

    # ─── Step 3: 选最佳 (threshold, ntap_exp, κ) 输出逐组对比 ───
    best = max(sensitivity, key=lambda s: s['r_squared'])
    print(f"\n--- 最佳: thresh_h={best['fade_threshold_h']}, "
          f"ntap_exp={best['ntap_exp']}, κ={best['kappa']:.0f}, "
          f"R²={best['r_squared']:+.3f}, trend={best['trend_consistency']:.3f} ---")

    best_h = best['fade_threshold_h']
    best_ne = best['ntap_exp']
    best_kappa = best['kappa']
    per_combo = []
    for r in mres:
        turb = r['turb_name']
        fg = r['f_g_hz']
        mu = r['mu']
        n_tap = r['n_tap']
        afd, lcr = fade_stats_cache[(turb, fg, str(best_h))]
        pp = predict_p_div(turb, fg, mu, n_tap, best_h, afd, lcr,
                           best_ne, best_kappa)
        per_combo.append({
            'turb_name': turb, 'alpha': r['alpha'], 'beta': r['beta'],
            'f_g_hz': fg, 'mu': mu, 'n_tap': n_tap,
            'tau_c_ms': r['tau_c_ms'],
            'afd_s': afd, 'lcr_per_s': lcr,
            'measured_p_div': r['p_div'],
            'predicted_p_div': pp,
            'diverge_count': r['diverge_count'],
            'n_trials': r['n_trials'],
        })

    # ─── Step 4: 汇总表 (按 turb × f_g, 取 mu=5e-3 tap=11 代表) ───
    print(f"\n{'='*70}")
    print(f"汇总表 (mu=5e-3 tap=11, thresh_h={best_h}): P_div 实测 vs 预测")
    print(f"{'='*70}")
    print(f"{'turb':>14s} | {'f_g':>5s} | {'AFD(μs)':>8s} | {'LCR':>7s} | "
          f"{'P_meas':>6s} | {'P_pred':>6s}")
    print("-" * 70)
    for turb in TURB_LEVELS:
        for fg in F_G_SWEEP:
            afd, lcr = fade_stats_cache[(turb, fg, str(best_h))]
            match = [c for c in per_combo
                     if c['turb_name'] == turb and c['f_g_hz'] == fg
                     and abs(c['mu'] - 5e-3) < 1e-12 and c['n_tap'] == 11]
            if match:
                m = match[0]
                print(f"{turb:>14s} | {fg:5.0f} | {afd*1e6:8.2f} | "
                      f"{lcr:7.1f} | {m['measured_p_div']:6.2f} | "
                      f"{m['predicted_p_div']:6.3f}")

    # ─── 单维趋势检验 (按 mu 扫, 固定 turb/fg/tap) ───
    print(f"\n--- 单维趋势: P_div vs mu (strong, f_g=300, tap=11) ---")
    print(f"{'mu':>10s} | {'P_meas':>6s} | {'P_pred':>6s}")
    for mu in MU_SWEEP:
        match = [c for c in per_combo
                 if c['turb_name'] == 'strong' and c['f_g_hz'] == 300.0
                 and abs(c['mu'] - mu) < 1e-12 and c['n_tap'] == 11]
        if match:
            m = match[0]
            print(f"{mu:10.0e} | {m['measured_p_div']:6.2f} | "
                  f"{m['predicted_p_div']:6.3f}")

    print(f"\n--- 单维趋势: P_div vs f_g (uplink_strong, mu=5e-3, tap=22) ---")
    print(f"{'f_g':>5s} | {'P_meas':>6s} | {'P_pred':>6s}")
    for fg in F_G_SWEEP:
        match = [c for c in per_combo
                 if c['turb_name'] == 'uplink_strong'
                 and abs(c['mu'] - 5e-3) < 1e-12 and c['n_tap'] == 22
                 and c['f_g_hz'] == fg]
        if match:
            m = match[0]
            print(f"{fg:5.0f} | {m['measured_p_div']:6.2f} | "
                  f"{m['predicted_p_div']:6.3f}")

    # ─── 有效性判定 ───
    valid = (best['r_squared'] > 0.5) or (best['trend_consistency'] > 0.7)
    print(f"\n{'='*70}")
    print(f"有效性判定: R²>0.5 或 趋势>0.7 → "
          f"{'有效 ✓' if valid else '部分有效/需改进 ✗'}")
    print(f"  最佳 R² = {best['r_squared']:+.3f}")
    print(f"  最佳趋势一致性 = {best['trend_consistency']:.3f}")
    print(f"{'='*70}")

    # ─── 保存结果 ───
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R1 (半解析界推导 + 验证)',
            'status': 'WIP',
            'timestamp': datetime.now().isoformat(),
            'derivation': {
                'drift_per_fade': 'μ·R²·σ_n·√(AFD/(block_size·T_S))',
                'p_single': '2·Q(threshold/σ_drift), σ_drift=drift_per_fade',
                'p_div': '1−(1−P_single)^{N_events}, N_events=LCR·T_obs',
            },
            'params': {
                'sigma_n': SIGMA_N, 'R2': R2_QPSK,
                'w0_norm': W0_NORM, 'threshold': THRESHOLD,
                'cma_block_size': CMA_BLOCK_SIZE, 'block': BLOCK,
                't_s': T_S, 'gamma_bar': GAMMA_BAR,
                'n_symbols': N_SYMBOLS, 't_obs_s': N_SYMBOLS * T_S,
            },
        },
        'sensitivity': sensitivity,
        'best_fit': best,
        'per_combo': per_combo,
        'validity': {
            'valid': valid,
            'criterion': 'R²>0.5 或 趋势一致性>0.7',
            'best_r2': best['r_squared'],
            'best_trend': best['trend_consistency'],
        },
    }
    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'r1_analytical_bound_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")
    print(f"总耗时: {time.time()-t_start:.0f}s")
    return out


if __name__ == '__main__':
    main()
