"""CMA 发散概率扫描 — Step B 分析层。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P5 标方向+状态)

补 sat.1553 §6.3 L778 自认空白:
  "the probability of the equalizer diverging to a local optimum during
   deep fades has not been analyzed here but could have a major impact"

扫描维度 (守 C1 关键参数扫描非单点):
  1. scintillation index: weak(4,3) / moderate(2.5,1.8) / strong(1.5,0.8)
     + uplink_strong(1.0,0.7) 更极端档
  2. f_G / τ_c: 30/100/300/1000 Hz (Step A 已建, tau_c=1/(2*pi*f_G))
  3. CMA 步长 μ: 1e-4 / 5e-4 / 1e-3 / 5e-3 / 1e-2
  4. 均衡器 tap 数: 7 / 11 / 22 (sat.1553 L572, Qin 22 tap)

发散判据 (TL-20 预定义, 见 _cma.py):
  - 系数范数 |w| > 10× 初始范数
  - 或输出幅度 |z| > 1e3
  - 或 NaN (数值溢出)

TL-20 理论预期:
  深衰落下 h→0, r≈n (纯噪声), CMA 梯度 ∇w = -e·r* 由噪声驱动
  → 系数随机游走, 漂移量 ∝ μ·σ_n·√(AFD) (步长×噪声×衰落持续时间)
  预期 P_div 随 (a) 衰落深度↑ (b) μ↑ (c) AFD↑ (d) tap↑ 而增大
  弱湍 P_div≈0, 强湍/uplink 显著上升

执行方式: 子 agent 跑, 主对话接收结果 (gw-feasibility §D step 8)
"""
import sys
import os
import json
import time
import numpy as np
from pathlib import Path

# 路径设置
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer1x1, CMAEqualizer2x2
from params import SimulationConfig


# ─── 参数 (FR-20 溯源, 从 params.py 读) ─────────────────────

cfg = SimulationConfig()

TURB_LEVELS = {
    'weak':          cfg.turbulence.as_dict()['weak'],
    'moderate':      cfg.turbulence.as_dict()['moderate'],
    'strong':        cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}

F_G_SWEEP = list(cfg.gg_time.GREENWOOD_FREQ_SWEEP)  # 30/100/300/1000 Hz
MU_SWEEP = [5e-4, 1e-3, 5e-3, 1e-2]  # 跳 1e-4 (太小肯定不发散)
TAP_SWEEP = [11, 22]  # sat.1553 L572 N=11 / Qin 2025 L263 22 tap (跳 7 太小)

N_SYMBOLS = 5_000_000   # 5M 符号 (覆盖多个 τ_c: f_G=100Hz→1.59ms→5M/2.5G=2ms≈1.3周期; f_G=1000Hz→16周期)
N_TRIALS = 3            # 每个组合的种子数 (统计发散概率)
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 20 dB
BLOCK = cfg.experiment.BLOCK  # 100
T_S = cfg.system.T_S  # 1/2.5e9

R_SYM = cfg.system.R_SYM
R2_QPSK = 1.0  # QPSK 恒模 R²=1 (Godard 1980)


# ─── QPSK 信号生成 ─────────────────────────────────────────

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1 (sat.1553 §6 标准 QPSK)。"""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2*bits[0::2]) + 1j * (1 - 2*bits[1::2])) / np.sqrt(2)


# ─── 单次发散测试 ───────────────────────────────────────────

def run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed,
                     use_dual_pol=True):
    """跑一次 CMA 发散测试, 返回是否发散 + 统计。

    信道模型:
      - 强度衰落: gg_time_envelope (Step A, 块内恒定块间 AR(1))
      - 双偏振: 两偏振共享 h(t) (同大气路径), SOP 用 Jones 旋转
      - 单偏振退化: 无 SOP, 纯强度衰落
    """
    rng = np.random.default_rng(seed)
    N = N_SYMBOLS
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    # 生成时间相关 GG 包络 (Step A)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK,
                         t_s=T_S, method='gar', seed=seed)

    # QPSK 信号
    s = gen_qpsk(N, rng)

    # 噪声
    noise_var = 1.0 / (2 * GAMMA_BAR)
    noise_X = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    if use_dual_pol:
        # 双偏振: X/Y 共享 h, Y 有不同符号 + SOP 旋转
        sY = gen_qpsk(N, rng)  # 独立符号
        noise_Y = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

        # SOP 旋转: sat.1553 Eq.(51) Jones J=rot(theta(t))
        # 用慢旋转 (sat.1553 §6.3: OSL SOP ~krad/s, 远低于 300 krad/s 跟踪能力)
        theta = 1e-4 * np.arange(N)  # ~slow SOP rotation
        rX_raw = np.sqrt(h) * (np.cos(theta) * s + np.sin(theta) * sY) + noise_X
        rY_raw = np.sqrt(h) * (-np.sin(theta) * s + np.cos(theta) * sY) + noise_Y

        eq = CMAEqualizer2x2(n_tap=n_tap, mu=mu, R2=R2_QPSK)
        res = eq.equalize(rX_raw, rY_raw)
    else:
        # 单偏振退化
        r = np.sqrt(h) * s + noise_X
        eq = CMAEqualizer1x1(n_tap=n_tap, mu=mu, R2=R2_QPSK)
        res = eq.equalize(r)

    return {
        'diverged': res['diverged'],
        'diverge_idx': res['diverge_idx'],
        'final_w_norm': res['final_w_norm'],
        'init_w_norm': res['init_w_norm'],
        'max_w_norm': float(np.max(res['w_norm_traj'])) if len(res['w_norm_traj']) > 0 else 0,
        'max_z_amp': float(np.max(res['z_amp_traj'])) if len(res['z_amp_traj']) > 0 else 0,
    }


# ─── 扫描主循环 ─────────────────────────────────────────────

def run_scan(turb_levels=None, f_g_list=None, mu_list=None, tap_list=None,
             n_trials=None, use_dual_pol=True, label='scan'):
    """跑发散概率扫描。

    总组合数 = len(turb) × len(f_g) × len(mu) × len(tap) × n_trials
    每个组合跑 n_trials 个种子, 统计 P_div = 发散次数 / n_trials。
    """
    turb_levels = turb_levels or TURB_LEVELS
    f_g_list = f_g_list or F_G_SWEEP
    mu_list = mu_list or MU_SWEEP
    tap_list = tap_list or TAP_SWEEP
    n_trials = n_trials or N_TRIALS

    total_combos = (len(turb_levels) * len(f_g_list) *
                    len(mu_list) * len(tap_list))
    total_runs = total_combos * n_trials
    print(f"[{label}] {total_combos} combos × {n_trials} trials = {total_runs} runs")
    print(f"  N_symbols={N_SYMBOLS}, dual_pol={use_dual_pol}")
    print(f"  turb={list(turb_levels.keys())}, f_G={f_g_list}")
    print(f"  mu={mu_list}, taps={tap_list}")

    results = []
    run_count = 0
    t_start = time.time()

    for turb_name, (alpha, beta) in turb_levels.items():
        for f_g in f_g_list:
            for mu in mu_list:
                for n_tap in tap_list:
                    diverge_count = 0
                    trial_details = []
                    for trial in range(n_trials):
                        seed = hash((turb_name, f_g, mu, n_tap, trial)) % (2**32)
                        res = run_single_trial(
                            turb_name, alpha, beta, f_g, mu, n_tap, seed,
                            use_dual_pol=use_dual_pol)
                        if res['diverged']:
                            diverge_count += 1
                        trial_details.append({
                            'seed': seed,
                            'diverged': res['diverged'],
                            'diverge_idx': res['diverge_idx'],
                            'max_w_norm': res['max_w_norm'],
                            'max_z_amp': res['max_z_amp'],
                        })
                        run_count += 1

                    p_div = diverge_count / n_trials
                    combo = {
                        'turb_name': turb_name,
                        'alpha': alpha, 'beta': beta,
                        'f_g_hz': f_g,
                        'tau_c_ms': cfg.gg_time.tau_c_from_fg(f_g) * 1e3,
                        'mu': mu,
                        'n_tap': n_tap,
                        'n_trials': n_trials,
                        'diverge_count': diverge_count,
                        'p_div': p_div,
                        'trials': trial_details,
                    }
                    results.append(combo)

                    elapsed = time.time() - t_start
                    eta = elapsed / run_count * (total_runs - run_count)
                    print(f"  [{run_count}/{total_runs}] {turb_name} f_G={f_g}μ={mu}tap={n_tap}"
                          f" → P_div={p_div:.2f} ({diverge_count}/{n_trials})"
                          f"  [{elapsed:.0f}s, ETA {eta:.0f}s]")

    # 汇总
    summary = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'B (CMA 发散概率扫描)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'n_trials': n_trials,
            'gamma_bar': GAMMA_BAR,
            'block': BLOCK,
            't_s': T_S,
            'r_sym': R_SYM,
            'dual_pol': use_dual_pol,
            'method': 'gar',
        },
        'scan_dims': {
            'turb_levels': list(turb_levels.keys()),
            'f_g_hz': f_g_list,
            'mu': mu_list,
            'n_tap': tap_list,
        },
        'results': results,
    }
    return summary


# ─── 结果保存 ───────────────────────────────────────────────

def save_results(summary, filename):
    """保存结果到 results/cma-fade-divergence/ (SIM-ORG P1)。"""
    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")
    return out_path


# ─── 入口 ───────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='CMA 发散概率扫描 (Step B)')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (小规模验证正确性)')
    parser.add_argument('--no-dual-pol', action='store_true',
                        help='用单偏振退化模式 (无 SOP 旋转)')
    parser.add_argument('--n-symbols', type=int, default=N_SYMBOLS)
    parser.add_argument('--n-trials', type=int, default=N_TRIALS)
    args = parser.parse_args()

    N_SYMBOLS = args.n_symbols
    N_TRIALS = args.n_trials

    if args.smoke:
        # Smoke test: 1 湍流档 × 1 f_G × 3 mu × 1 tap × 3 trials
        print("=" * 60)
        print("SMOKE TEST (小规模验证)")
        print("=" * 60)
        summary = run_scan(
            turb_levels={'strong': TURB_LEVELS['strong'],
                         'uplink_strong': TURB_LEVELS['uplink_strong']},
            f_g_list=[100.0, 1000.0],
            mu_list=[1e-3, 5e-3, 1e-2],
            tap_list=[11],
            n_trials=3,
            use_dual_pol=not args.no_dual_pol,
            label='smoke',
        )
        save_results(summary, 'cma_divergence_smoke.json')
    else:
        # 全量扫描
        print("=" * 60)
        print("FULL SCAN (全量发散概率扫描)")
        print("=" * 60)
        summary = run_scan(
            use_dual_pol=not args.no_dual_pol,
            label='full',
        )
        save_results(summary, 'cma_divergence_scan_results.json')

    # 打印汇总表
    print("\n" + "=" * 60)
    print("P_div 汇总表 (按湍流档 × f_G)")
    print("=" * 60)
    for turb_name in summary['scan_dims']['turb_levels']:
        print(f"\n[{turb_name}]")
        header = f"{'mu/tap':>12}" + "".join(f"  f_G={fg:>5.0f}" for fg in summary['scan_dims']['f_g_hz'])
        print(header)
        for mu in summary['scan_dims']['mu']:
            for n_tap in summary['scan_dims']['n_tap']:
                row = f"  mu={mu:.0e} tap={n_tap:>2}"
                for f_g in summary['scan_dims']['f_g_hz']:
                    match = [r for r in summary['results']
                             if r['turb_name'] == turb_name and r['f_g_hz'] == f_g
                             and r['mu'] == mu and r['n_tap'] == n_tap]
                    if match:
                        p = match[0]['p_div']
                        row += f"  {p:>7.2f}"
                    else:
                        row += f"  {'N/A':>7}"
                print(row)
