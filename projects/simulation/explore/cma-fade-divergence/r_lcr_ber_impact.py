"""R_LCR_BER — LCR 对 BER 的独立影响 + ML vs CMA vs oracle 三方对比。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)

## 背景

R4 修正发现固定 μ 后 P_div vs LCR r=+0.88 —— 衰落频率越高, 发散概率越高。
但 P_div 只是"数值发散"（权重溢出）, 对通信质量的实质影响是 BER。

## 关键问题

1. 高 LCR 下 CMA 的 BER 是否恶化? (不只是 P_div 高, BER 也差?)
2. 如果 CMA 在安全 μ (1e-3, 不发散) 下, 高 LCR 的 BER 是否仍然恶化?
   (即 LCR 对 BER 有独立影响, 不通过发散)
3. ML (固定权重) 在高 LCR 下是否有 BER 退化?
   (ML 也退化 → ML 没优势; ML 不退化 → 方法层有真价值)

## 三个实验

Exp1: CMA BER vs f_G (安全 μ=1e-3, 隔离 LCR 对 BER 独立影响) + oracle
Exp2: CMA BER vs f_G (危险 μ=1e-2, 发散+BER 联合) + oracle
Exp3: ML BER vs f_G (每 f_G 训练一个 ML) + CMA(1e-3) + oracle 三方

## 关键约束

- BER 计算需先做 QPSK 相位校正 (CMA/ML 有 π/2 相位模糊): 尝试 4 旋转角度取最低 BER
- BER 算收敛后部分 (跳过前 10% 暂态)
- CMA 发散 trial: BER 单独记 (用 diverge_idx 前的 valid 段)
- SOP_RATE=4e-7 (1 krad/s), 不是 Step B 的 1e-4
- 时间预算 ≤15 分钟: CMA 用 5 seeds, ML 用 3 seeds (复用 CMA 信道)

用法:
  cd projects/simulation && python explore/cma-fade-divergence/r_lcr_ber_impact.py
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
from common import generate_shared_realization_dp
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize

cfg = SimulationConfig()
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 (20 dB)

# ─── 实验参数 ───────────────────────────────────────────────
# f_G 扫描: [10, 30, 100, 300, 1000, 3000] Hz
F_G_SWEEP = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
MOD = 'qpsk'
TURB = 'strong'  # α=1.5, β=0.8
N_TAP = 11
N_SYMBOLS = 2_000_000  # 2M 够算 BER
SOP_RATE = 4e-7  # 1 krad/s (sat.1553 §6.3)
MU_SAFE = 1e-3   # 安全区 (P_div≈0)
MU_DANGER = 1e-2  # 危险区
R2_QPSK = 1.0
SKIP_FRAC = 0.10  # BER 跳过前 10% 暂态
# CMA 用 5 seeds, ML 用 3 seeds (复用 CMA 信道; ML 训练慢)
N_SEEDS_CMA = 5
N_SEEDS_ML = 3
# ML 训练参数 (跟 Step C / sup_stress_test.py 一致)
ML_PARAMS = dict(n_tap=11, lr=0.005, batch_size=1024, n_epochs=20,
                 device='cuda', patience=5)
ML_TRAIN_FRAC = 0.5  # 前 50% 训练, 后 50% 测试

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'


def _load_ckpt(name):
    """加载某实验的 checkpoint dict, 不存在返回 {}."""
    p = RESULTS_DIR / f'r_lcr_ber_{name}_checkpoint.json'
    if p.exists():
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_ckpt(name, data):
    """保存某实验的 checkpoint."""
    try:
        with open(RESULTS_DIR / f'r_lcr_ber_{name}_checkpoint.json', 'w',
                  encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception:
        pass


def qpsk_demap(z):
    z = np.asarray(z).flatten()
    bits = np.zeros(len(z) * 2, dtype=int)
    bits[0::2] = (z.real < 0).astype(int)
    bits[1::2] = (z.imag < 0).astype(int)
    return bits


# ─── BER 计算 (含 π/2 相位校正) ─────────────────────────────

def compute_ber_phase_corrected(z, s, skip_frac=0.0):
    """QPSK BER, 先做 4 旋转角度相位校正取最低 BER (消除 π/2 相位模糊).

    z, s: 均衡后符号 / 发送符号 (复数, shape (N,))
    skip_frac: 跳过前 skip_frac 比例的暂态.
    返回 (ber, best_phase_deg).
    """
    z = np.asarray(z).flatten()
    s = np.asarray(s).flatten()
    n = len(z)
    start = int(n * skip_frac)
    z_eval = z[start:]
    s_eval = s[start:]
    s_bits = qpsk_demap(s_eval)
    best_ber = 1.0
    best_deg = 0
    for deg in [0, 90, 180, 270]:
        rot = np.exp(1j * np.radians(deg))
        ber = float(np.mean(qpsk_demap(z_eval * rot) != s_bits))
        if ber < best_ber:
            best_ber = ber
            best_deg = deg
    return best_ber, best_deg


def compute_ber(z, s, skip_frac=0.0):
    """简写: 只返回 BER (相位校正后)."""
    return compute_ber_phase_corrected(z, s, skip_frac)[0]


# ─── oracle 均衡 (撤销 SOP + MMSE, 参考 sup_stress_test.py) ──

def oracle_equalize(rX, rY, h, theta, gamma_bar):
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 信道生成 (跟 sup_stress_test.py / r4_corrected 一致) ────

def gen_channel(N, alpha, beta, f_g, sop_rate, seed):
    """兼容旧接口：返回 rX, rY, sX, sY, h, theta。"""
    shared = generate_shared_realization_dp(
        N=N,
        alpha=alpha,
        beta=beta,
        f_g=f_g,
        sop_rate=sop_rate,
        seed=seed,
    )
    return tuple(shared[key] for key in ("rX", "rY", "sX", "sY", "h", "theta"))


# ─── 单次 CMA trial ─────────────────────────────────────────

def run_cma_trial(rX, rY, sX, mu):
    """跑一次 CMA, 返回 (ber, diverged, diverge_idx).

    BER 计算策略:
      - 未发散: 用 zX 跳过前 10% 暂态算 BER
      - 发散: 用 diverge_idx 前的 valid 段算 BER (发散后 BER≈0.5 无意义)
    """
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
    res = cma.equalize(rX, rY)
    if res['diverged'] and res['diverge_idx'] is not None:
        valid = max(int(res['diverge_idx']), 1)
        # 发散前 valid 段, 跳过前 10% 暂态 (若 valid 太短则不跳)
        skip = max(1, int(valid * SKIP_FRAC)) if valid > 1000 else 0
        ber = compute_ber(res['zX'][:valid], sX[:valid], skip / valid if valid else 0)
    else:
        ber = compute_ber(res['zX'], sX, SKIP_FRAC)
    return ber, bool(res['diverged']), res['diverge_idx']


def run_oracle_trial(rX, rY, sX, h, theta):
    """oracle MMSE BER (完美 CSI 下界)."""
    zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    return compute_ber(zX_or, sX, SKIP_FRAC)


# ─── Exp1: CMA BER vs f_G (安全 μ=1e-3) ─────────────────────

def run_exp1_safe_mu(cached_channels):
    """CMA 安全 μ=1e-3 vs f_G + oracle. 隔离 LCR 对 BER 独立影响."""
    print("\n" + "=" * 60)
    print("Exp1: CMA BER (安全 μ=1e-3) vs f_G + oracle")
    print("=" * 60)
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    results = defaultdict(lambda: {'cma_ber': [], 'oracle_ber': [],
                                   'cma_diverged': []})
    print(f"{'f_G(Hz)':>8} {'CMA_BER':>10} {'oracle_BER':>11} {'n_div':>6} {'n':>4}")
    ckpt = _load_ckpt('exp1')
    saved = ckpt.get('results', {})
    for f_g in F_G_SWEEP:
        sk = str(f_g)
        if sk in saved and len(saved[sk].get('cma_ber', [])) >= N_SEEDS_CMA:
            v = saved[sk]
            print(f"{f_g:>8.0f} {np.mean(v['cma_ber']):>10.2e} "
                  f"{np.mean(v['oracle_ber']):>11.2e} "
                  f"{int(sum(v['cma_diverged'])):>6d} {N_SEEDS_CMA:>4d} (cached)",
                  flush=True)
            results[f_g] = {
                'cma_ber': list(v['cma_ber']),
                'oracle_ber': list(v['oracle_ber']),
                'cma_diverged': list(v['cma_diverged']),
            }
            continue
        for seed in range(N_SEEDS_CMA):
            seed_int = int(hash(('r_lcr', 'exp1', f_g, seed)) % (2**32))
            rX, rY, sX, sY, h, theta = cached_channels[(f_g, seed_int)]
            ber, div, _ = run_cma_trial(rX, rY, sX, MU_SAFE)
            ber_or = run_oracle_trial(rX, rY, sX, h, theta)
            results[f_g]['cma_ber'].append(ber)
            results[f_g]['oracle_ber'].append(ber_or)
            results[f_g]['cma_diverged'].append(int(div))
        cma_mean = np.mean(results[f_g]['cma_ber'])
        or_mean = np.mean(results[f_g]['oracle_ber'])
        n_div = int(np.sum(results[f_g]['cma_diverged']))
        print(f"{f_g:>8.0f} {cma_mean:>10.2e} {or_mean:>11.2e} "
              f"{n_div:>6d} {N_SEEDS_CMA:>4d}", flush=True)
        _save_ckpt('exp1', {'results': {str(k): val for k, val in results.items()}})
    return {str(k): {'cma_ber_mean': float(np.mean(v['cma_ber'])),
                     'cma_ber_std': float(np.std(v['cma_ber'])),
                     'cma_ber_list': [float(x) for x in v['cma_ber']],
                     'oracle_ber_mean': float(np.mean(v['oracle_ber'])),
                     'oracle_ber_std': float(np.std(v['oracle_ber'])),
                     'oracle_ber_list': [float(x) for x in v['oracle_ber']],
                     'n_diverged': int(np.sum(v['cma_diverged'])),
                     'n_seeds': N_SEEDS_CMA}
            for k, v in results.items()}


# ─── Exp2: CMA BER vs f_G (危险 μ=1e-2) ─────────────────────

def run_exp2_danger_mu(cached_channels):
    """CMA 危险 μ=1e-2 vs f_G + oracle. 发散+BER 联合. 记录发散 trial."""
    print("\n" + "=" * 60)
    print("Exp2: CMA BER (危险 μ=1e-2) vs f_G + oracle (发散 trial 标注)")
    print("=" * 60)
    results = defaultdict(lambda: {'cma_ber': [], 'oracle_ber': [],
                                   'cma_diverged': [], 'cma_ber_nondiv': [],
                                   'cma_ber_div': []})
    print(f"{'f_G(Hz)':>8} {'CMA_BER':>10} {'oracle_BER':>11} {'n_div':>6} "
          f"{'BER_nondiv':>11} {'BER_div':>9}")
    ckpt = _load_ckpt('exp2')
    saved = ckpt.get('results', {})
    for f_g in F_G_SWEEP:
        sk = str(f_g)
        if sk in saved and len(saved[sk].get('cma_ber', [])) >= N_SEEDS_CMA:
            v = saved[sk]
            ber_nd = (float(np.mean(v['cma_ber_nondiv']))
                      if v.get('cma_ber_nondiv') else float('nan'))
            ber_d = (float(np.mean(v['cma_ber_div']))
                     if v.get('cma_ber_div') else float('nan'))
            print(f"{f_g:>8.0f} {np.mean(v['cma_ber']):>10.2e} "
                  f"{np.mean(v['oracle_ber']):>11.2e} "
                  f"{int(sum(v['cma_diverged'])):>6d} {ber_nd:>11.2e} "
                  f"{ber_d:>9.2e} (cached)", flush=True)
            results[f_g] = {
                'cma_ber': list(v['cma_ber']),
                'oracle_ber': list(v['oracle_ber']),
                'cma_diverged': list(v['cma_diverged']),
                'cma_ber_nondiv': list(v.get('cma_ber_nondiv', [])),
                'cma_ber_div': list(v.get('cma_ber_div', [])),
            }
            continue
        for seed in range(N_SEEDS_CMA):
            seed_int = int(hash(('r_lcr', 'exp1', f_g, seed)) % (2**32))
            rX, rY, sX, sY, h, theta = cached_channels[(f_g, seed_int)]
            ber, div, _ = run_cma_trial(rX, rY, sX, MU_DANGER)
            ber_or = run_oracle_trial(rX, rY, sX, h, theta)
            results[f_g]['cma_ber'].append(ber)
            results[f_g]['oracle_ber'].append(ber_or)
            results[f_g]['cma_diverged'].append(int(div))
            if div:
                results[f_g]['cma_ber_div'].append(ber)
            else:
                results[f_g]['cma_ber_nondiv'].append(ber)
        cma_mean = np.mean(results[f_g]['cma_ber'])
        or_mean = np.mean(results[f_g]['oracle_ber'])
        n_div = int(np.sum(results[f_g]['cma_diverged']))
        ber_nd = (float(np.mean(results[f_g]['cma_ber_nondiv']))
                  if results[f_g]['cma_ber_nondiv'] else float('nan'))
        ber_d = (float(np.mean(results[f_g]['cma_ber_div']))
                 if results[f_g]['cma_ber_div'] else float('nan'))
        print(f"{f_g:>8.0f} {cma_mean:>10.2e} {or_mean:>11.2e} {n_div:>6d} "
              f"{ber_nd:>11.2e} {ber_d:>9.2e}", flush=True)
        _save_ckpt('exp2', {'results': {
            str(k): {kk: (list(vv) if isinstance(vv, list) else vv)
                     for kk, vv in val.items()}
            for k, val in results.items()}})
    return {str(k): {'cma_ber_mean': float(np.mean(v['cma_ber'])),
                     'cma_ber_std': float(np.std(v['cma_ber'])),
                     'cma_ber_list': [float(x) for x in v['cma_ber']],
                     'oracle_ber_mean': float(np.mean(v['oracle_ber'])),
                     'oracle_ber_list': [float(x) for x in v['oracle_ber']],
                     'n_diverged': int(np.sum(v['cma_diverged'])),
                     'cma_ber_nondiv_mean': (float(np.mean(v['cma_ber_nondiv']))
                                             if v['cma_ber_nondiv'] else None),
                     'cma_ber_div_mean': (float(np.mean(v['cma_ber_div']))
                                          if v['cma_ber_div'] else None),
                     'n_seeds': N_SEEDS_CMA}
            for k, v in results.items()}


# ─── Exp3: ML BER vs f_G + 三方对比 ─────────────────────────

def _exp3_ckpt_path():
    """Exp3 checkpoint 路径 (每 f_G 存, 支持断点续跑)."""
    return RESULTS_DIR / 'r_lcr_ber_exp3_checkpoint.json'


def run_exp3_ml(cached_channels):
    """ML BER vs f_G + CMA(1e-3) + oracle 三方对比.

    ML 每个 f_G 训练一个模型 (train_frac=0.5), 在测试集上算 BER.
    用 N_SEEDS_ML seeds (ML 训练慢). 每 f_G 写 checkpoint 支持断点续跑.
    """
    print("\n" + "=" * 60)
    print("Exp3: ML BER vs f_G (每 f_G 训练) + CMA(1e-3) + oracle")
    print("=" * 60)
    n_train = int(N_SYMBOLS * ML_TRAIN_FRAC)
    print(f"{'f_G(Hz)':>8} {'ML_BER':>10} {'CMA_BER':>10} {'oracle_BER':>11} {'n':>4}")

    # 断点续跑: 加载已完成 f_G
    ckpt = _exp3_ckpt_path()
    results = defaultdict(lambda: {'ml_ber': [], 'cma_ber': [], 'oracle_ber': []})
    if ckpt.exists():
        try:
            with open(ckpt, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            for k, v in saved.get('results', {}).items():
                if len(v.get('ml_ber', [])) >= N_SEEDS_ML:
                    results[float(k)] = v
            print(f"  [续跑] 已完成 {len(results)} 个 f_G: "
                  f"{sorted(results.keys())}", flush=True)
        except Exception:
            pass

    for f_g in F_G_SWEEP:
        if f_g in results and len(results[f_g]['ml_ber']) >= N_SEEDS_ML:
            ml_mean = np.mean(results[f_g]['ml_ber'])
            cma_mean = np.mean(results[f_g]['cma_ber'])
            or_mean = np.mean(results[f_g]['oracle_ber'])
            print(f"{f_g:>8.0f} {ml_mean:>10.2e} {cma_mean:>10.2e} {or_mean:>11.2e} "
                  f"{N_SEEDS_ML:>4d} (cached)", flush=True)
            continue
        for seed in range(N_SEEDS_ML):
            seed_int = int(hash(('r_lcr', 'exp1', f_g, seed)) % (2**32))
            rX, rY, sX, sY, h, theta = cached_channels[(f_g, seed_int)]

            # ML 训练 (前 50%) + 推理 (全段, BER 只算测试段后 50%)
            ml = MLChannelEqualizer(**ML_PARAMS)
            ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                     val_split=0.2, verbose=False)
            res_ml = ml.equalize(rX, rY)
            zX_ml = res_ml['zX'].flatten()
            # ML 测试段 BER (后 50%, 不跳暂态因 ML 前馈无暂态)
            ml_ber = compute_ber(zX_ml[n_train:], sX[n_train:], 0.0)

            # CMA (1e-3) — 复用 exp1 的逻辑但只测后 50% (公平对比 ML)
            cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
            res_cma = cma.equalize(rX, rY)
            if res_cma['diverged'] and res_cma['diverge_idx'] is not None:
                valid = max(int(res_cma['diverge_idx']), 1)
                # 发散: valid 段可能在训练段内, 取 min(valid, n_train) 前的
                v_end = min(valid, n_train) if valid > n_train else valid
                cma_ber = compute_ber(res_cma['zX'][:v_end], sX[:v_end], 0.0) if v_end > 100 else 0.5
            else:
                cma_ber = compute_ber(res_cma['zX'][n_train:], sX[n_train:], 0.0)

            # oracle (测试段)
            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            or_ber = compute_ber(zX_or[n_train:], sX[n_train:], 0.0)

            results[f_g]['ml_ber'].append(ml_ber)
            results[f_g]['cma_ber'].append(cma_ber)
            results[f_g]['oracle_ber'].append(or_ber)
        ml_mean = np.mean(results[f_g]['ml_ber'])
        cma_mean = np.mean(results[f_g]['cma_ber'])
        or_mean = np.mean(results[f_g]['oracle_ber'])
        print(f"{f_g:>8.0f} {ml_mean:>10.2e} {cma_mean:>10.2e} {or_mean:>11.2e} "
              f"{N_SEEDS_ML:>4d}", flush=True)
        # 每 f_G 写 checkpoint (断点续跑)
        try:
            with open(_exp3_ckpt_path(), 'w', encoding='utf-8') as f:
                json.dump({'results': {str(k): v for k, v in results.items()}},
                          f, indent=1, default=str)
        except Exception:
            pass
    return {str(k): {'ml_ber_mean': float(np.mean(v['ml_ber'])),
                     'ml_ber_std': float(np.std(v['ml_ber'])),
                     'ml_ber_list': [float(x) for x in v['ml_ber']],
                     'cma_ber_mean': float(np.mean(v['cma_ber'])),
                     'cma_ber_list': [float(x) for x in v['cma_ber']],
                     'oracle_ber_mean': float(np.mean(v['oracle_ber'])),
                     'oracle_ber_list': [float(x) for x in v['oracle_ber']],
                     'n_seeds': N_SEEDS_ML}
            for k, v in results.items()}


# ─── 预生成所有信道 (复用, 省 gg_time 生成开销) ─────────────

def pregenerate_channels():
    """预生成所有 (f_G, seed) 信道. CMA 用 exp1 的 5 seeds, ML 复用前 3 个."""
    print(f"预生成信道: {len(F_G_SWEEP)} f_G × {N_SEEDS_CMA} seeds "
          f"= {len(F_G_SWEEP)*N_SEEDS_CMA} channels (N={N_SYMBOLS})")
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    channels = {}
    t0 = time.time()
    for f_g in F_G_SWEEP:
        for seed in range(N_SEEDS_CMA):
            seed_int = int(hash(('r_lcr', 'exp1', f_g, seed)) % (2**32))
            channels[(f_g, seed_int)] = gen_channel(
                N_SYMBOLS, alpha, beta, f_g, SOP_RATE, seed_int)
    print(f"  信道生成完成: {time.time()-t0:.0f}s")
    return channels


# ─── 汇总打印 ───────────────────────────────────────────────

def print_final_summary(exp1, exp2, exp3):
    """打印 BER vs f_G 三方对比汇总表."""
    print("\n" + "=" * 78)
    print("汇总: BER vs f_G (QPSK, strong turb, 20dB, 1krad/s SOP)")
    print("=" * 78)
    print(f"\n{'f_G(Hz)':>8} | {'CMA μ=1e-3':>11} {'CMA μ=1e-2':>11} "
          f"{'ML':>10} | {'oracle':>10} | {'CMA/oracle':>10} {'ML/oracle':>10}")
    print("-" * 78)
    for f_g in F_G_SWEEP:
        k = str(f_g)
        e1 = exp1.get(k, {})
        e2 = exp2.get(k, {})
        e3 = exp3.get(k, {})
        cma_safe = e1.get('cma_ber_mean', float('nan'))
        cma_danger = e2.get('cma_ber_mean', float('nan'))
        ml = e3.get('ml_ber_mean', float('nan'))
        orc = e1.get('oracle_ber_mean', float('nan'))
        ratio_cma = cma_safe / orc if orc > 0 else float('nan')
        ratio_ml = ml / orc if orc > 0 else float('nan')
        print(f"{f_g:>8.0f} | {cma_safe:>11.2e} {cma_danger:>11.2e} "
              f"{ml:>10.2e} | {orc:>10.2e} | {ratio_cma:>10.2f} {ratio_ml:>10.2f}")

    print("\n--- 关键判断 ---")
    # CMA 安全 μ 下 BER 是否随 f_G 恶化?
    cma_safe_bers = [exp1[str(fg)]['cma_ber_mean'] for fg in F_G_SWEEP]
    orc_bers = [exp1[str(fg)]['oracle_ber_mean'] for fg in F_G_SWEEP]
    cma_ratio = [c / o if o > 0 else float('nan')
                 for c, o in zip(cma_safe_bers, orc_bers)]
    ml_bers = [exp3[str(fg)]['ml_ber_mean'] for fg in F_G_SWEEP]
    ml_ratio = [m / o if o > 0 else float('nan')
                for m, o in zip(ml_bers, orc_bers)]
    print(f"  CMA(1e-3) BER 比: {[f'{r:.2f}' for r in cma_ratio]}")
    print(f"  ML BER 比:        {[f'{r:.2f}' for r in ml_ratio]}")
    print(f"  oracle BER 随 fG: {[f'{b:.2e}' for b in orc_bers]}")
    # 趋势: 比较 f_G=10 和 f_G=3000 的 BER
    if all(np.isfinite(cma_ratio)):
        cma_trend = cma_ratio[-1] / cma_ratio[0] if cma_ratio[0] > 0 else float('nan')
        ml_trend = ml_ratio[-1] / ml_ratio[0] if ml_ratio[0] > 0 else float('nan')
        orc_trend = orc_bers[-1] / orc_bers[0] if orc_bers[0] > 0 else float('nan')
        print(f"  BER 比 (3000Hz/10Hz): CMA={cma_trend:.2f}x ML={ml_trend:.2f}x "
              f"oracle={orc_trend:.2f}x")


# ─── 主入口 ─────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("=" * 60)
    print("R_LCR_BER: LCR 对 BER 的独立影响 + ML vs CMA vs oracle")
    print("=" * 60)
    print(f"参数: QPSK, turb={TURB}, N={N_SYMBOLS}, SOP={SOP_RATE} (1krad/s), "
          f"γ̄={GAMMA_BAR} (20dB), tap={N_TAP}")
    print(f"f_G sweep: {F_G_SWEEP}")
    print(f"seeds: CMA={N_SEEDS_CMA}, ML={N_SEEDS_ML}")

    # 预生成信道 (CMA exp1/exp2 共用, ML 复用前 N_SEEDS_ML 个)
    channels = pregenerate_channels()

    # Exp1: CMA 安全 μ
    print(f"\n[1/3] Exp1: CMA BER (安全 μ={MU_SAFE})...")
    t1 = time.time()
    exp1 = run_exp1_safe_mu(channels)
    print(f"  Exp1 耗时: {time.time()-t1:.0f}s")

    # Exp2: CMA 危险 μ
    print(f"\n[2/3] Exp2: CMA BER (危险 μ={MU_DANGER})...")
    t2 = time.time()
    exp2 = run_exp2_danger_mu(channels)
    print(f"  Exp2 耗时: {time.time()-t2:.0f}s")

    # Exp3: ML
    print(f"\n[3/3] Exp3: ML BER vs f_G...")
    t3 = time.time()
    exp3 = run_exp3_ml(channels)
    print(f"  Exp3 耗时: {time.time()-t3:.0f}s")

    # 汇总
    print_final_summary(exp1, exp2, exp3)

    # 保存
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R_LCR_BER (LCR 对 BER 独立影响 + ML vs CMA vs oracle)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': time.time() - t0,
            'params': {
                'mod': MOD, 'turbulence': TURB, 'n_symbols': N_SYMBOLS,
                'sop_rate': SOP_RATE, 'sop_krad_s': SOP_RATE * 2.5e9 / 1e3,
                'gamma_bar': GAMMA_BAR, 'n_tap': N_TAP,
                'f_g_sweep': F_G_SWEEP, 'mu_safe': MU_SAFE, 'mu_danger': MU_DANGER,
                'n_seeds_cma': N_SEEDS_CMA, 'n_seeds_ml': N_SEEDS_ML,
                'ml_train_frac': ML_TRAIN_FRAC,
                'skip_frac': SKIP_FRAC,
            },
        },
        'exp1_cma_safe_mu': exp1,
        'exp2_cma_danger_mu': exp2,
        'exp3_ml_vs_cma_oracle': exp3,
    }
    out_path = RESULTS_DIR / 'r_lcr_ber_impact_results.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")
    print(f"总耗时: {time.time()-t0:.0f}s")
    return out


if __name__ == '__main__':
    main()
