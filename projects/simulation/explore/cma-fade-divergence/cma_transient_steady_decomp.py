"""A1 — CMA 跟踪滞后分解: 瞬态 vs 稳态 (R004 batch2 task1).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md

## 目标

分解 CMA BER 差的原因是 (a) 瞬态收敛 (前 K 符号权重未收敛) 还是
(b) 稳态跟踪滞后 (收敛后仍跟不上动态信道)。固定 strong 湍流, SNR=20dB,
跑 CMA μ=1e-3, N=5M 符号, f_G=[30,100,1000]Hz, N_SEEDS=20。每 10000 符号
算窗口 BER, 画 BER vs 符号序号, 自动定收敛点, 报告瞬态/稳态 BER vs f_G。

## 关键设计

- 三方同信道: gen_channel 一次, CMA + oracle 复用同一组 (rX,rY,sX,sY,h,theta)
- 窗口 BER: zX[skip:] 按 10000 符号切片, 每段独立相位校正 (4 旋转)
- 收敛点自动判定两种方法: (1) 窗口 BER 单调停止法 (2) 权重范数稳定法
- 逐 seed 跑省内存, 每 f_G 写 checkpoint 支持断点续跑

用法:
  cd projects/simulation && python explore/cma-fade-divergence/cma_transient_steady_decomp.py
"""
import sys
import json
import time
import numpy as np
from pathlib import Path

# ─── 路径设置 ───────────────────────────────────────────────
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))                                # 让 params import
sys.path.insert(0, str(Path(__file__).resolve().parent))        # 让 r_lcr import

from params import SimulationConfig
from common._cma import CMAEqualizer2x2
from common._equalizer import mmse_equalize
from common._config import BLOCK
from r_lcr_ber_impact import (
    gen_channel, compute_ber, compute_ber_phase_corrected,
    qpsk_demap, gen_qpsk, oracle_equalize,
    GAMMA_BAR, T_S,
)

cfg = SimulationConfig()

# ─── 实验参数 ───────────────────────────────────────────────
MOD = 'qpsk'
TURB = 'strong'                 # α=1.5, β=0.8
SNR_DB = 20.0
GAMMA = 10.0 ** (SNR_DB / 10)   # 100, 与 r_lcr 的 GAMMA_BAR 一致 (覆写以示溯源)
N_SYMBOLS = 5_000_000
SOP_RATE = 4e-7                 # 1 krad/s
F_G_SWEEP = [30.0, 100.0, 1000.0]
N_TAP = 11
MU_CMA = 1e-3
R2_QPSK = 1.0
N_SEEDS = 20
WINDOW_SIZE = 10_000            # 窗口 BER 每段符号数
SKIP_INIT = 1_000               # 瞬态统计跳过最前 1000 符号 (避初始全零)
# 收敛判定 (方法1: 窗口 BER 单调停止法)
CONV_W = 5                      # 连续 W 个窗口不再单调下降 → 收敛
# 收敛判定 (方法2: 权重范数稳定法) — 在窗口 BER 收敛点附近取范数变化率 < 阈值
WNORM_REL_TOL = 0.02            # 相对变化 < 2% 视为稳定

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CKPT_PATH = RESULTS_DIR / 'cma_transient_steady_checkpoint.json'
OUT_PATH = RESULTS_DIR / 'cma_transient_steady_results.json'

TL20_EXPECTED = (
    "瞬态: CMA BER 高→单调下降 (前 ~50k-200k 符号). "
    "收敛点: 跨 f_G 同量级 (主要由 μ/tap 决定, 跟 f_G 弱相关). "
    "稳态 BER vs f_G 单调上升: f_G=30 (dur/τ_c=0.38 静态) 稳态≈oracle; "
    "f_G=1000 (dur/τ_c=12.57 动态) 稳态显著>oracle. "
    "稳态/oracle ratio 随 f_G 上升. "
    "窗口 BER 曲线: 高→下降→plateau, plateau 高度随 f_G 上升."
)
TL22_PHYSICS = (
    "dur/tau_c (N=5M, T_S=4e-10 → dur=2ms): "
    "f_G=30→0.38(静态), 100→1.26, 1000→12.57(充分展开)"
)


# ─── checkpoint ─────────────────────────────────────────────

def _load_ckpt():
    if CKPT_PATH.exists():
        try:
            with open(CKPT_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_ckpt(data):
    try:
        with open(CKPT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception:
        pass


# ─── 窗口 BER ───────────────────────────────────────────────

def compute_window_ber(zX, sX, window_size, valid_end=None):
    """把 zX 按 window_size 切片, 每段独立相位校正算 BER.

    返回 (window_bers, window_centers). centers 是每窗口中心符号序号.
    valid_end: 若发散, 只用到 valid_end 前的符号 (None=全段).
    """
    zX = np.asarray(zX)
    sX = np.asarray(sX)
    N = len(zX)
    if valid_end is None:
        valid_end = N
    n_win = valid_end // window_size
    bers = []
    centers = []
    for w in range(n_win):
        s = w * window_size
        e = s + window_size
        if e > valid_end:
            break
        ber, _ = compute_ber_phase_corrected(zX[s:e], sX[s:e], skip_frac=0.0)
        bers.append(ber)
        centers.append(s + window_size // 2)
    return np.array(bers), np.array(centers)


# ─── 收敛点自动判定 ─────────────────────────────────────────

def detect_convergence_ber(window_bers, window_centers, W=CONV_W):
    """方法1: 窗口 BER 单调停止法.

    找第一个窗口 i, 满足"之后连续 W 个窗口 BER 不再单调下降"。
    即从 i 开始, BER[i+1..i+W] 中至少有一个 >= BER[i] (停止下降)。

    更稳健实现: 找第一个 i 使得 mean(BER[i:i+W]) 与后续 plateau 不可区分——
    这里用"局部最小斜率翻转"判据: 从 i 开始连续 W 步, 每步 BER 差分 <= 容差。

    实际用: 找 BER 序列首次进入"波动区"——前缀单调下降结束的点。
    判据: i 是第一个满足 (存在 j in [i+1, i+W] 使 BER[j] >= BER[i]*0.95) 的点。
    返回收敛点符号序号 (window_centers[i])。若全程单调下降, 返回最后一个窗口中心。
    """
    if len(window_bers) < W + 2:
        return int(window_centers[-1]) if len(window_centers) else 0
    conv_i = len(window_bers) - 1
    for i in range(len(window_bers) - W):
        # 检查 [i, i+W] 窗口内是否还有显著下降
        seg = window_bers[i:i + W + 1]
        # 如果这一段不是严格单调下降 (有任意回升 >= 5%), 认为 i 是收敛点
        diffs = np.diff(seg)
        # 回升: diff > 0 (BER 增加); 容差: 相对回升 > 5% 视为非单调
        rel_increase = diffs[diffs > 0]
        if len(rel_increase) > 0 and rel_increase[0] > 0.05 * abs(seg[0]):
            conv_i = i
            break
        # 或者段内变化幅度已很小 (plateau): max-min < 5% of mean
        if seg.mean() > 0 and (seg.max() - seg.min()) < 0.05 * seg.mean():
            conv_i = i
            break
    return int(window_centers[conv_i])


def detect_convergence_wnorm(w_norm_traj, wnorm_sample_step=64):
    """方法2: 权重范数稳定法.

    w_norm_traj 是块末点 (每 block_size=64 符号一个, 其余为 0)。
    取非零点序列, 找范数相对变化率 < WNORM_REL_TOL 的首个点。

    返回收敛点符号序号。若全程不稳定, 返回最后一个非零点。
    """
    nz = np.nonzero(w_norm_traj)[0]
    if len(nz) < 5:
        return int(nz[-1]) if len(nz) else 0
    norms = w_norm_traj[nz]
    # 相邻范数相对变化
    for i in range(2, len(norms)):
        # 用窗口 [i-2, i] 的相对变化
        local = norms[max(0, i - 4):i + 1]
        if local.mean() > 0:
            rel_var = (local.max() - local.min()) / local.mean()
            if rel_var < WNORM_REL_TOL:
                return int(nz[i])
    return int(nz[-1])


# ─── 单 seed 处理 ───────────────────────────────────────────

def process_seed(seed_int, f_g, alpha, beta):
    """跑一个 seed: gen_channel → CMA → oracle → 窗口 BER + 收敛点.

    返回 dict:
      window_bers, window_centers, conv_idx_ber, conv_idx_wnorm,
      transient_ber (收敛前, 跳过前 SKIP_INIT),
      steady_ber (收敛后), oracle_ber (全段), diverged, diverge_idx
    """
    # 信道 (三方同源)
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, f_g, SOP_RATE, seed_int)

    # CMA
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_CMA, R2=R2_QPSK)
    res = cma.equalize(rX, rY)
    zX = res['zX']
    w_norm_traj = res['w_norm_traj']
    diverged = bool(res['diverged'])
    diverge_idx = res['diverge_idx']

    # valid 段 (发散则截断)
    valid_end = int(diverge_idx) if (diverged and diverge_idx is not None) else N_SYMBOLS

    # 窗口 BER
    window_bers, window_centers = compute_window_ber(
        zX, sX, WINDOW_SIZE, valid_end=valid_end)

    # 收敛点 (两种方法)
    if len(window_bers) > CONV_W + 2:
        conv_idx_ber = detect_convergence_ber(window_bers, window_centers)
    else:
        conv_idx_ber = int(window_centers[-1]) if len(window_centers) else SKIP_INIT
    conv_idx_wnorm = detect_convergence_wnorm(w_norm_traj)

    # 瞬态 BER (收敛点前, 跳过 SKIP_INIT)
    t_end = min(conv_idx_ber, valid_end)
    if t_end > SKIP_INIT:
        transient_ber, _ = compute_ber_phase_corrected(
            zX[SKIP_INIT:t_end], sX[SKIP_INIT:t_end], skip_frac=0.0)
    else:
        transient_ber = float('nan')

    # 稳态 BER (收敛点后到 valid_end)
    s_start = max(conv_idx_ber, SKIP_INIT)
    if valid_end > s_start:
        steady_ber, _ = compute_ber_phase_corrected(
            zX[s_start:valid_end], sX[s_start:valid_end], skip_frac=0.0)
    else:
        steady_ber = float('nan')

    # oracle (全段, 完美 CSI 下界) — 跳过前 SKIP_INIT
    zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    oracle_ber, _ = compute_ber_phase_corrected(
        zX_or[SKIP_INIT:valid_end], sX[SKIP_INIT:valid_end], skip_frac=0.0)

    return {
        'window_bers': window_bers.tolist(),
        'window_centers': window_centers.tolist(),
        'conv_idx_ber': conv_idx_ber,
        'conv_idx_wnorm': conv_idx_wnorm,
        'transient_ber': float(transient_ber),
        'steady_ber': float(steady_ber),
        'oracle_ber': float(oracle_ber),
        'diverged': diverged,
        'diverge_idx': (int(diverge_idx) if diverge_idx is not None else None),
        'final_w_norm': float(res['final_w_norm']),
    }


# ─── 单 f_G 处理 (含断点续跑) ───────────────────────────────

def run_f_g(f_g, alpha, beta, ckpt):
    """跑一个 f_G 的所有 seed, 返回聚合结果 dict."""
    sk = str(f_g)
    if sk in ckpt and len(ckpt[sk].get('per_seed', [])) >= N_SEEDS:
        print(f"  f_G={f_g:.0f}Hz: 已有 {N_SEEDS} seeds (cached)", flush=True)
        return ckpt[sk]

    per_seed = ckpt.get(sk, {}).get('per_seed', [])
    start_seed = len(per_seed)
    print(f"  f_G={f_g:.0f}Hz: 从 seed {start_seed} 跑到 {N_SEEDS}", flush=True)

    t_fg0 = time.time()
    for si in range(start_seed, N_SEEDS):
        # seed 生成: 确定性映射 (不依赖 PYTHONHASHSEED, 跨进程可复现)
        seed_int = make_seed(f_g, si)
        sd = process_seed(seed_int, f_g, alpha, beta)
        per_seed.append(sd)
        elapsed = time.time() - t_fg0
        done = si - start_seed + 1
        print(f"    seed {si+1}/{N_SEEDS} done "
              f"(conv={sd['conv_idx_ber']}, transient_BER={sd['transient_ber']:.3e}, "
              f"steady_BER={sd['steady_ber']:.3e}, oracle_BER={sd['oracle_ber']:.3e}, "
              f"diverged={sd['diverged']}, {elapsed/done:.1f}s/seed)", flush=True)
        # 每 seed 写 checkpoint (断点续跑)
        ckpt[sk] = _aggregate_per_seed(per_seed, f_g)
        _save_ckpt(ckpt)

    return _aggregate_per_seed(per_seed, f_g)


def _aggregate_per_seed(per_seed, f_g):
    """聚合 per_seed 列表 → 结果 dict (含 mean/std/window 曲线)."""
    # 窗口 BER 跨 seed 平均 (需对齐 window_centers; 不同 seed 若发散截断长度不同, 用最短公共长度)
    n_seeds = len(per_seed)
    all_wbers = [np.array(s['window_bers']) for s in per_seed]
    min_len = min(len(w) for w in all_wbers) if all_wbers else 0
    if min_len > 0:
        wber_mat = np.array([w[:min_len] for w in all_wbers])  # (n_seeds, min_len)
        window_ber_mean = wber_mat.mean(axis=0).tolist()
        window_ber_std = wber_mat.std(axis=0).tolist()
        window_centers = per_seed[0]['window_centers'][:min_len]
    else:
        window_ber_mean, window_ber_std, window_centers = [], [], []

    conv_ber = np.array([s['conv_idx_ber'] for s in per_seed])
    conv_wnorm = np.array([s['conv_idx_wnorm'] for s in per_seed])
    transient = np.array([s['transient_ber'] for s in per_seed])
    steady = np.array([s['steady_ber'] for s in per_seed])
    oracle = np.array([s['oracle_ber'] for s in per_seed])

    # 只对非 nan 聚合 (发散 seed 的 transient/steady 可能 nan)
    def _ms(arr):
        arr = arr[np.isfinite(arr)]
        if len(arr) == 0:
            return float('nan'), float('nan')
        return float(arr.mean()), float(arr.std())

    t_mean, t_std = _ms(transient)
    s_mean, s_std = _ms(steady)
    o_mean, o_std = _ms(oracle)
    ratio = s_mean / o_mean if (np.isfinite(s_mean) and o_mean > 0) else float('nan')

    return {
        'window_ber_mean': window_ber_mean,
        'window_ber_std': window_ber_std,
        'window_centers': [int(c) for c in window_centers],
        'convergence_idx_mean': float(conv_ber.mean()),
        'convergence_idx_std': float(conv_ber.std()),
        'convergence_idx_wnorm_mean': float(conv_wnorm.mean()),
        'convergence_idx_wnorm_std': float(conv_wnorm.std()),
        'transient_ber_mean': t_mean,
        'transient_ber_std': t_std,
        'steady_state_ber_mean': s_mean,
        'steady_state_ber_std': s_std,
        'oracle_ber_mean': o_mean,
        'oracle_ber_std': o_std,
        'steady_vs_oracle_ratio': float(ratio),
        'per_seed': per_seed,
        'n_seeds': n_seeds,
        'n_diverged': int(sum(1 for s in per_seed if s['diverged'])),
    }


# ─── smoke test ─────────────────────────────────────────────

def smoke_test():
    """1 seed, N=500K, f_G=1000Hz. 验证窗口 BER 曲线形态 (高→下降→plateau)."""
    print("=" * 60)
    print("SMOKE TEST: 1 seed, N=500K, f_G=1000Hz")
    print("=" * 60)
    global N_SYMBOLS
    N_SYMBOLS_SAVE = N_SYMBOLS
    # monkey-patch N_SYMBOLS 只为 smoke (通过临时改全局)
    import builtins
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    # 直接调 process_seed 但用短 N: 改模块全局
    g = sys.modules[__name__]
    orig_N = g.N_SYMBOLS
    g.N_SYMBOLS = 500_000
    try:
        seed_int = make_seed(1000.0, 0)
        sd = process_seed(seed_int, 1000.0, alpha, beta)
    finally:
        g.N_SYMBOLS = orig_N

    wb = np.array(sd['window_bers'])
    wc = np.array(sd['window_centers'])
    print(f"\n窗口 BER 曲线 (共 {len(wb)} 窗口):")
    # 打印每 5 个窗口一个点
    step = max(1, len(wb) // 20)
    for i in range(0, len(wb), step):
        print(f"  sym={wc[i]:>8d}  BER={wb[i]:.4e}")
    print(f"\n收敛点 (BER 法): {sd['conv_idx_ber']}")
    print(f"收敛点 (wnorm 法): {sd['conv_idx_wnorm']}")
    print(f"瞬态 BER: {sd['transient_ber']:.4e}")
    print(f"稳态 BER: {sd['steady_ber']:.4e}")
    print(f"oracle BER: {sd['oracle_ber']:.4e}")
    print(f"发散: {sd['diverged']}")

    # 形态检查: 前 1/4 vs 后 1/4 BER
    if len(wb) >= 8:
        q1 = wb[:len(wb)//4].mean()
        q4 = wb[-len(wb)//4:].mean()
        print(f"\n形态检查: 前1/4 BER={q1:.4e}, 后1/4 BER={q4:.4e}")
        if q1 > q4:
            print("  ✓ 瞬态高→稳态低 (符合预期)")
        else:
            print("  ✗ 反预期: 后段 BER 不低于前段")
        # plateau 检查: 后 1/4 内波动
        if q4 > 0:
            q4_std = wb[-len(wb)//4:].std()
            print(f"  后1/4 std={q4_std:.4e} (CV={q4_std/q4:.2f})")
    return sd


def make_seed(f_g, seed_idx):
    """确定性 seed 派生 (不依赖 PYTHONHASHSEED).

    hash() 在不同进程间随机化 → 不可复现 + 可能产生偏置 seed。
    用确定性整数映射: f_g 整数 Hz × 大常数 + seed_idx.
    """
    fg_int = int(round(f_g))
    return int((fg_int * 1_000_003 + seed_idx * 99_991) % (2 ** 32))

def main():
    t0 = time.time()
    print("=" * 60)
    print("A1: CMA 瞬态/稳态 BER 分解 (R004 batch2 task1)")
    print("=" * 60)
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    print(f"参数: {MOD}, turb={TURB}(α={alpha},β={beta}), SNR={SNR_DB}dB "
          f"(γ̄={GAMMA}), N={N_SYMBOLS}, SOP={SOP_RATE}")
    print(f"f_G sweep: {F_G_SWEEP}, n_seeds={N_SEEDS}, window={WINDOW_SIZE}")
    print(f"收敛判定: BER单调停止法(W={CONV_W}) + 权重范数稳定法(tol={WNORM_REL_TOL})")
    print(f"\nTL-20 预期:\n  {TL20_EXPECTED}")
    print(f"\nTL-22 物理:\n  {TL22_PHYSICS}")

    # smoke test
    print("\n>>> 先跑 smoke test <<<")
    smoke_test()
    print("\n>>> smoke 完成, 开始全量 <<<\n")

    ckpt = _load_ckpt()
    results = {}
    for fi, f_g in enumerate(F_G_SWEEP):
        print(f"\n[{fi+1}/{len(F_G_SWEEP)}] f_G={f_g:.0f}Hz")
        t_fg = time.time()
        results[str(f_g)] = run_f_g(f_g, alpha, beta, ckpt)
        # 重新加载 ckpt (run_f_g 内部更新了)
        ckpt = _load_ckpt()
        r = results[str(f_g)]
        print(f"  f_G={f_g:.0f}Hz 完成 ({time.time()-t_fg:.0f}s): "
              f"conv={r['convergence_idx_mean']:.0f}±{r['convergence_idx_std']:.0f}, "
              f"transient={r['transient_ber_mean']:.3e}, "
              f"steady={r['steady_state_ber_mean']:.3e}, "
              f"oracle={r['oracle_ber_mean']:.3e}, "
              f"ratio={r['steady_vs_oracle_ratio']:.2f}, "
              f"n_div={r['n_diverged']}", flush=True)

    elapsed = time.time() - t0

    # 汇总表
    print("\n" + "=" * 90)
    print("汇总: 瞬态/稳态/oracle BER vs f_G")
    print("=" * 90)
    print(f"{'f_G':>6} | {'conv_idx':>12} | {'transient':>10} | {'steady':>10} | "
          f"{'oracle':>10} | {'steady/oracle':>13} | {'conv(wnorm)':>12} | n_div")
    print("-" * 90)
    for f_g in F_G_SWEEP:
        r = results[str(f_g)]
        print(f"{f_g:>6.0f} | {r['convergence_idx_mean']:>8.0f}±{r['convergence_idx_std']:>3.0f} | "
              f"{r['transient_ber_mean']:>10.3e} | {r['steady_state_ber_mean']:>10.3e} | "
              f"{r['oracle_ber_mean']:>10.3e} | {r['steady_vs_oracle_ratio']:>13.2f} | "
              f"{r['convergence_idx_wnorm_mean']:>8.0f}±{r['convergence_idx_wnorm_std']:>3.0f} | "
              f"{r['n_diverged']}")

    # 保存最终 JSON (不含 per_seed 的 window_bers 以减小体积? 不, 保留 per_seed 但去掉 window_bers 减体积)
    # 按 PROMPT 要求保留 per_seed (含 convergence_idx/transient/steady/oracle)
    out_results = {}
    for f_g, r in results.items():
        # per_seed 只保留标量字段 (窗口曲线已在顶层 window_ber_mean)
        per_seed_slim = [{
            'seed_idx': i,
            'convergence_idx': s['conv_idx_ber'],
            'convergence_idx_wnorm': s['conv_idx_wnorm'],
            'transient_ber': s['transient_ber'],
            'steady_ber': s['steady_ber'],
            'oracle_ber': s['oracle_ber'],
            'diverged': s['diverged'],
            'diverge_idx': s['diverge_idx'],
            'final_w_norm': s['final_w_norm'],
        } for i, s in enumerate(r['per_seed'])]
        out_results[f_g] = {k: v for k, v in r.items() if k != 'per_seed'}
        out_results[f_g]['per_seed'] = per_seed_slim

    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'A1 CMA transient/steady decomposition (R004 batch2 task1)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': elapsed,
            'params': {
                'mod': MOD, 'turbulence': TURB, 'snr_db': SNR_DB,
                'gamma_bar': GAMMA, 'n_symbols': N_SYMBOLS,
                'sop_rate': SOP_RATE, 'n_tap': N_TAP, 'mu_cma': MU_CMA,
                'f_g_sweep': F_G_SWEEP, 'n_seeds': N_SEEDS,
                'window_size': WINDOW_SIZE, 'skip_init': SKIP_INIT,
                'convergence_method': (
                    'method1=窗口BER单调停止法(W=5: 连续5窗口不再单调下降或plateau<5%); '
                    'method2=权重范数稳定法(块末范数局部相对变化<2%)'),
            },
            'tl20_expected': TL20_EXPECTED,
            'tl22_physics_check': TL22_PHYSICS,
        },
        'results': out_results,
    }
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {OUT_PATH}")
    print(f"总耗时: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    return out


if __name__ == '__main__':
    main()
