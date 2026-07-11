"""MVE: ML vs CMA 均衡深衰落对比 — Step C 方法层。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P5 标方向+状态)

补 Qin/Nasr 实验缺口:
  - Qin 2025: VAEMR vs CMA 在单一中强湍流 r₀=0.4mm 固定下测 BER/收敛速度
  - Nasr 2026: ANN vs MI 在 θ/ϕ 抽象均匀采样下测 Q-factor
  - 两人都未在 Step B 确认的"发散条件边界"下对比 ML vs CMA 的稳定性
  - 我们补: 在 (μ, f_G) 发散条件判据下, 测 ML vs CMA 的发散概率 + BER + 恢复时间

TL-20 理论预期:
  ML 在发散条件下*应该*比 CMA 稳定:
  - CMA 逐块梯度更新: 深衰落 h→0 时 r≈n, 梯度 ∇w=μ·R²·n* 噪声驱动 → 系数随机游走 → 漂移超阈值 → 不可恢复
  - ML batch 梯度下降: 梯度对整个 batch 平均 → 单个深衰落样本噪声被 batch 稀释
    → 漂移 ∝ μ_ml·σ_n/√B (B=batch size) 远小于 CMA 的 ∝ μ_cma·σ_n
  - 预测: 危险区 (μ≥1e-2, f_G≥100Hz) ML P_div ≪ CMA P_div

测试场景 (Step B 确认的发散条件):
  - 危险区 (CMA 必发散): μ=1e-2, f_G=1000Hz, strong/uplink_strong
  - 临界区 (CMA 可能发散): μ=5e-3, f_G=100/300Hz
  - 安全区 (CMA 稳定, 对照): μ=1e-3, f_G=30Hz

三方对照 (C7 强制):
  1. CMA (传统 baseline, FR-14 先验): common._cma.CMAEqualizer2x2
  2. ML 均衡器 (我们的方法): common._ml_equalizer.MLChannelEqualizer
  3. oracle MMSE (下界参照): undo SOP + MMSE with perfect CSI (h, theta)

公平对照 (守 Freire 2022 6 陷阱):
  - 同一信道实现 (同 seed)
  - ML 训练集 vs 测试集分离 (前 50% 训练, 后 50% 测试)
  - BER 非 EVM (陷阱 1)
  - MTRS 非 PRBS (陷阱 3): numpy randint
  - batch≥1024 (陷阱 4)
  - MSE 回归非 CEL (陷阱 5)
  - 复杂度报告 RMpS (陷阱 6)

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
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer, compute_rmps
from common._equalizer import mmse_equalize
from params import SimulationConfig


# ─── 参数 (FR-20 溯源, 从 params.py 读) ─────────────────────

cfg = SimulationConfig()

TURB_LEVELS = {
    'strong':        cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}

# 测试场景 (Step B 发散条件判据)
SCENARIOS = [
    # (name, f_G, mu_cma, turb_name, description)
    ('danger_1e-2_1000Hz', 1000.0, 1e-2, 'strong',        '危险区: μ=1e-2, f_G=1000Hz, strong'),
    ('danger_1e-2_1000Hz_up', 1000.0, 1e-2, 'uplink_strong', '危险区: μ=1e-2, f_G=1000Hz, uplink_strong'),
    ('critical_5e-3_100Hz',  100.0,  5e-3, 'strong',        '临界区: μ=5e-3, f_G=100Hz, strong'),
    ('critical_5e-3_300Hz',  300.0,  5e-3, 'strong',        '临界区: μ=5e-3, f_G=300Hz, strong'),
    ('safe_1e-3_30Hz',        30.0,  1e-3, 'strong',        '安全区: μ=1e-3, f_G=30Hz, strong (对照)'),
]

N_SYMBOLS = 500_000      # 500K 符号 (够 ML 训练 + 覆盖多个深衰落事件)
N_TRIALS = 5             # 5 seeds (比 Step B 的 3 多, P_div 分辨率 0.2)
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 = 20 dB
BLOCK = cfg.experiment.BLOCK  # 100
T_S = cfg.system.T_S  # 1/2.5e9

# ML 参数 (FR-20: Qin 2025 L275/283/397)
ML_N_TAP = 11          # 跟 CMA 对齐 (sat.1553 Fig.13 N=11)
ML_LR = 0.005          # Qin 2025 L397
ML_BATCH = 1024        # Freire 2022 L349
ML_EPOCHS = 20         # 适中
ML_TRAIN_FRAC = 0.5    # 前 50% 训练, 后 50% 测试

R2_QPSK = 1.0
CMA_TAP = 11           # 跟 ML 对齐
# SOP 旋转速率: sat.1553 §6.3 L778 "OSL SOP ~krad/s"
# Step B 用 1e-4 rad/sym (250 krad/s) 过快;
# 真实 OSL SOP ~1 krad/s = 4e-7 rad/sym (sat.1553 L778 + L745 "SOP 旋转较慢")
# 验证: 真实 SOP 下 CMA 发散仍由 μ 驱动 (与 Step B 结论一致, SOP 速率不改变发散机制)
SOP_RATE = 4e-7        # 1 krad/s (sat.1553 §6.3 真实 OSL SOP 速率)


# ─── QPSK 信号生成 (MTRS, Freire 陷阱 3) ────────────────────

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1. 用 numpy randint (MTRS, 非 LFSR PRBS)."""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2*bits[0::2]) + 1j * (1 - 2*bits[1::2])) / np.sqrt(2)


def qpsk_demap(z):
    """QPSK 判决解映射."""
    z = np.asarray(z).flatten()
    bits = np.zeros(len(z) * 2, dtype=int)
    bits[0::2] = (z.real < 0).astype(int)
    bits[1::2] = (z.imag < 0).astype(int)
    return bits


def compute_ber(z, s):
    """计算 BER (QPSK)."""
    return float(np.mean(qpsk_demap(z) != qpsk_demap(s)))


# ─── oracle MMSE (完美 CSI: h + SOP θ) ──────────────────────

def oracle_equalize(rX, rY, h, theta, gamma_bar):
    """oracle 均衡: 完美 CSI (h + SOP θ) → undo SOP + MMSE on h.

    这是理论下界: 假设均衡器完全知道信道状态 (衰落 h + SOP 旋转 θ).
    """
    # undo SOP rotation (完美已知 θ)
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_undone = cos_t * rX + sin_t * rY
    rY_undone = -sin_t * rX + cos_t * rY
    # MMSE on h (完美已知 h)
    zX = mmse_equalize(rX_undone, h, gamma_bar)
    zY = mmse_equalize(rY_undone, h, gamma_bar)
    return zX, zY


# ─── 单次试验 ───────────────────────────────────────────────

def run_single_trial(scenario_name, f_g, mu_cma, turb_name, alpha, beta, seed):
    """跑一次 ML vs CMA vs oracle 三方对比.

    返回 dict: 各方法的 diverged / BER / 收敛信息.
    """
    rng = np.random.default_rng(seed)
    N = N_SYMBOLS
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    # 生成时间相关 GG 包络 (Step A)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK,
                         t_s=T_S, method='gar', seed=seed)

    # QPSK 信号 (双偏振独立符号)
    sX = gen_qpsk(N, rng)
    sY = gen_qpsk(N, rng)

    # SOP 旋转 (sat.1553 Eq.51 Jones J=rot(theta(t)))
    theta = SOP_RATE * np.arange(N)

    # 双偏振信道: 共享 h, SOP 旋转
    rX = np.sqrt(h) * (np.cos(theta) * sX + np.sin(theta) * sY)
    rY = np.sqrt(h) * (-np.sin(theta) * sX + np.cos(theta) * sY)

    # AWGN
    nv = 1.0 / (2 * GAMMA_BAR)
    rX += np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY += np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    # ─── 1. CMA (传统 baseline) ───
    cma = CMAEqualizer2x2(n_tap=CMA_TAP, mu=mu_cma, R2=R2_QPSK)
    res_cma = cma.equalize(rX, rY)

    # CMA BER (发散前部分; 发散后不可恢复)
    if res_cma['diverged'] and res_cma['diverge_idx'] is not None:
        valid = max(res_cma['diverge_idx'], 1)
        ber_cma = compute_ber(res_cma['zX'][:valid], sX[:valid])
        # 发散后部分 BER ≈ 0.5
        if valid < N:
            ber_post = compute_ber(res_cma['zX'][valid:], sX[valid:])
        else:
            ber_post = 0.5
    else:
        ber_cma = compute_ber(res_cma['zX'], sX)
        ber_post = None

    # ─── 2. ML 均衡器 (我们的方法) ───
    n_train = int(N * ML_TRAIN_FRAC)

    # 训练 (前 50%, pilot 已知)
    ml = MLChannelEqualizer(n_tap=ML_N_TAP, lr=ML_LR, batch_size=ML_BATCH,
                            n_epochs=ML_EPOCHS, device='cuda', patience=5)
    train_hist = ml.train(rX[:n_train], rY[:n_train],
                          sX[:n_train], sY[:n_train],
                          val_split=0.2, verbose=False)

    # 推理 (全段, 但 BER 只报测试集 = 后 50%)
    res_ml = ml.equalize(rX, rY)
    zX_ml = res_ml['zX'].flatten()

    # ML BER (测试集 = 后 50%, 不含训练集 → 无泄漏, Freire 陷阱 2)
    test_start = n_train
    ber_ml = compute_ber(zX_ml[test_start:], sX[test_start:])

    # ─── 3. oracle MMSE (下界参照) ───
    zX_oracle, zY_oracle = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    ber_oracle = compute_ber(zX_oracle[test_start:], sX[test_start:])

    # raw BER (无均衡, 对照)
    ber_raw = compute_ber(rX[test_start:], sX[test_start:])

    return {
        'scenario': scenario_name,
        'seed': seed,
        'f_g_hz': f_g,
        'mu_cma': mu_cma,
        'turb_name': turb_name,
        # CMA
        'cma_diverged': res_cma['diverged'],
        'cma_diverge_idx': res_cma['diverge_idx'],
        'cma_ber_test': ber_cma,
        'cma_ber_post_divergence': ber_post,
        'cma_final_w_norm': res_cma['final_w_norm'],
        # ML
        'ml_diverged': res_ml['diverged'],
        'ml_ber_test': ber_ml,
        'ml_train_converged': train_hist['converged'],
        'ml_best_val_loss': train_hist['best_val_loss'],
        'ml_final_w_norm': train_hist['final_w_norm'],
        'ml_epochs_run': train_hist['epochs_run'],
        # oracle
        'oracle_ber_test': ber_oracle,
        # raw
        'raw_ber_test': ber_raw,
    }


# ─── 扫描主循环 ─────────────────────────────────────────────

def run_mve(scenarios=None, n_trials=None, label='mve'):
    """跑 ML vs CMA vs oracle 三方对比 MVE."""
    scenarios = scenarios or SCENARIOS
    n_trials = n_trials or N_TRIALS

    total_runs = len(scenarios) * n_trials
    print(f"[{label}] {len(scenarios)} scenarios × {n_trials} trials = {total_runs} runs")
    print(f"  N_symbols={N_SYMBOLS}, ML train_frac={ML_TRAIN_FRAC}")
    print(f"  ML: tap={ML_N_TAP}, lr={ML_LR}, batch={ML_BATCH}, epochs={ML_EPOCHS}")
    print(f"  CMA: tap={CMA_TAP}, mu per scenario")
    print(f"  RMpS: ML={compute_rmps(ML_N_TAP)}, CMA={CMA_TAP*8}")
    print()

    results = []
    run_count = 0
    t_start = time.time()

    for scenario_name, f_g, mu_cma, turb_name, desc in scenarios:
        alpha, beta = TURB_LEVELS[turb_name]
        print(f"--- {scenario_name}: {desc} ---")

        for trial in range(n_trials):
            seed = hash((scenario_name, trial)) % (2**32)
            res = run_single_trial(scenario_name, f_g, mu_cma, turb_name,
                                   alpha, beta, seed)
            results.append(res)
            run_count += 1

            elapsed = time.time() - t_start
            eta = elapsed / run_count * (total_runs - run_count)
            print(f"  [{run_count}/{total_runs}] seed={seed} "
                  f"CMA div={'Y' if res['cma_diverged'] else 'N'} "
                  f"BER(cma={res['cma_ber_test']:.4f}/ml={res['ml_ber_test']:.4f}"
                  f"/oracle={res['oracle_ber_test']:.4f}/raw={res['raw_ber_test']:.4f}) "
                  f"  [{elapsed:.0f}s, ETA {eta:.0f}s]")

    # 汇总
    summary = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'C (ML vs CMA MVE, 方法层)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'n_trials': n_trials,
            'gamma_bar': GAMMA_BAR,
            'block': BLOCK,
            't_s': T_S,
            'ml_params': {
                'n_tap': ML_N_TAP, 'lr': ML_LR, 'batch_size': ML_BATCH,
                'n_epochs': ML_EPOCHS, 'train_frac': ML_TRAIN_FRAC,
                'source': 'Qin 2025 L275/283/397 + Freire 2022 L349',
            },
            'cma_params': {
                'n_tap': CMA_TAP,
                'source': 'sat.1553 §6 + Godard 1980',
            },
            'rmps': {'ml': compute_rmps(ML_N_TAP), 'cma': CMA_TAP * 8},
        },
        'scenarios': [
            {'name': s[0], 'f_g': s[1], 'mu_cma': s[2], 'turb': s[3], 'desc': s[4]}
            for s in scenarios
        ],
        'results': results,
        'summary_by_scenario': summarize_by_scenario(results),
    }
    return summary


def summarize_by_scenario(results):
    """按场景汇总: P_div, mean BER."""
    from collections import defaultdict
    by_scn = defaultdict(list)
    for r in results:
        by_scn[r['scenario']].append(r)

    summary = {}
    for scn, trials in by_scn.items():
        n = len(trials)
        summary[scn] = {
            'n_trials': n,
            'cma_p_div': sum(1 for t in trials if t['cma_diverged']) / n,
            'ml_p_div': sum(1 for t in trials if t['ml_diverged']) / n,
            'cma_mean_ber': float(np.mean([t['cma_ber_test'] for t in trials])),
            'ml_mean_ber': float(np.mean([t['ml_ber_test'] for t in trials])),
            'oracle_mean_ber': float(np.mean([t['oracle_ber_test'] for t in trials])),
            'raw_mean_ber': float(np.mean([t['raw_ber_test'] for t in trials])),
            'ml_mean_val_loss': float(np.mean([t['ml_best_val_loss'] for t in trials])),
            'ml_mean_epochs': float(np.mean([t['ml_epochs_run'] for t in trials])),
        }
    return summary


# ─── 结果保存 ───────────────────────────────────────────────

def save_results(summary, filename):
    """保存结果到 results/cma-fade-divergence/ (SIM-ORG P1)."""
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
    parser = argparse.ArgumentParser(description='ML vs CMA MVE (Step C)')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 场景 × 2 seeds)')
    parser.add_argument('--n-symbols', type=int, default=N_SYMBOLS)
    parser.add_argument('--n-trials', type=int, default=N_TRIALS)
    args = parser.parse_args()

    N_SYMBOLS = args.n_symbols
    N_TRIALS = args.n_trials

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (小规模验证)")
        print("=" * 60)
        summary = run_mve(
            scenarios=[SCENARIOS[0]],  # 危险区 only
            n_trials=2,
            label='smoke',
        )
        save_results(summary, 'mve_cma_vs_ml_smoke.json')
    else:
        print("=" * 60)
        print("FULL MVE (ML vs CMA vs oracle, 全场景)")
        print("=" * 60)
        summary = run_mve(label='full')
        save_results(summary, 'mve_cma_vs_ml_results.json')

    # 打印汇总表
    print("\n" + "=" * 60)
    print("汇总表 (按场景)")
    print("=" * 60)
    print(f"{'scenario':>28} {'CMA_Pdiv':>9} {'ML_Pdiv':>8} "
          f"{'CMA_BER':>8} {'ML_BER':>8} {'oracle':>8} {'raw':>8}")
    for scn, s in summary['summary_by_scenario'].items():
        print(f"{scn:>28} {s['cma_p_div']:>9.2f} {s['ml_p_div']:>8.2f} "
              f"{s['cma_mean_ber']:>8.4f} {s['ml_mean_ber']:>8.4f} "
              f"{s['oracle_mean_ber']:>8.4f} {s['raw_mean_ber']:>8.4f}")
