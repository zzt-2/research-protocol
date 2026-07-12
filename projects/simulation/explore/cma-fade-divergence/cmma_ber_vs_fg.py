"""G3: CMMA BER vs f_G — QPSK + 16QAM 双调制 (CMMA/CMA/ML/oracle 四方对比).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)
> 来源: R004 批次2 任务2 G3 (R2 只测了 CMMA 发散概率=跟 CMA 逐点相同, 没测 BER)

## TL;DR

补 CMMA 的 BER vs f_G, 跟 CMA/ML/oracle 四方对比.
- QPSK: CMMA(R2_rings=[1.0]) 单环数学上=CMA(R2=1.0), 验证实现正确 (BER 应几乎相同)
- 16QAM: CMMA(R2_rings=[0.2,1.0,1.8]) 多模匹配三环, 看是否降 modulus mismatch BER 惩罚

## 最高纪律
1. QPSK 时 CMMA 必须≈CMA (验证实现正确, 否则代码有 bug)
2. N_SEEDS>=20 报 mean±std
3. 不假设因果链
4. 四方同信道 (CMMA/CMA/ML/oracle 同一组 (rX,rY,sX,sY,h,theta))

## 设计要点

- CMMA (CMMAEqualizer2x2) 在 explore/cma-fade-divergence/r2_cmma_divergence.py
  (不在 common/), 放同目录 import.
- 四方同信道: gen_channel 一次, CMMA/CMA/ML/oracle 复用. 比率免疫 seed-bias.
- ML 训练慢 → CMMA/CMA/oracle 用 20 seeds, ML 用较少 seeds (N_SEEDS_ML).
- BER 暂态: CMA/CMMA 跳前 10% (SKIP_FRAC=0.10); ML 跳前 50% (训练段); oracle 全段.
- 发散 trial: μ=1e-3 安全区应几乎不发散; 若发散, 用 diverge_idx 前的 valid 段算 BER.
- QPSK 相位校正: 4 旋转; 16QAM 相位校正: LS 估计 phi=angle(sum(z·conj(s))).
- 断点续跑: 每完成一个 (mod, f_G) 写 checkpoint.

用法:
  cd projects/simulation && python explore/cma-fade-divergence/cmma_ber_vs_fg.py [--smoke]
"""
import sys
import json
import time
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict

# 路径: 从 projects/simulation/ 运行, 同时把 explore/cma-fade-divergence 加入
# sys.path 以便 import r2_cmma_divergence (CMMAEqualizer2x2 在那)
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from params import SimulationConfig
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from common._config import BLOCK
from common._experiment import save_results

# CMMA 从同目录 import (explore/cma-fade-divergence/r2_cmma_divergence.py)
from r2_cmma_divergence import (
    CMMAEqualizer2x2, R2_RINGS_16QAM, R2_RINGS_QPSK,
    R2_16QAM,  # 1.32 Godard
)

cfg = SimulationConfig()
T_S = cfg.system.T_S

# ─── 实验参数 ───────────────────────────────────────────────
MOD_LIST = ['qpsk', '16qam']
TURB = 'strong'  # α=1.5, β=0.8
SNR_DB = 20.0
GAMMA_BAR = 10.0 ** (SNR_DB / 10.0)  # 100
N_SYMBOLS = 2_000_000  # 跟 r_lcr/ber_16qam 一致
SOP_RATE = 4e-7  # 1 krad/s (sat.1553 §6.3)
F_G_SWEEP = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
N_TAP = 11
MU = 1e-3  # 安全区 (P_div≈0)
R2_QPSK = 1.0  # CMA QPSK
# R2_16QAM = 1.32 (Godard, 从 r2_cmma 导入)
SKIP_FRAC = 0.10  # CMA/CMMA 跳过前 10% 暂态
ML_PARAMS = dict(n_tap=N_TAP, lr=0.005, batch_size=1024, n_epochs=20,
                 device='cuda', patience=5)
ML_TRAIN_FRAC = 0.5
N_SEEDS_CMA = 20
N_SEEDS_ML = 5  # ML 训练慢, 减 seeds; CMMA/CMA/oracle 用 20

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
CKPT_PATH = RESULTS_DIR / 'cmma_ber_vs_fg_checkpoint.json'


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
        CKPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CKPT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception:
        pass


# ─── 调制/解调 ──────────────────────────────────────────────

QAM16_LEVELS = np.array([-3, -1, 1, 3])
QAM16_NORM = np.sqrt(10.0)


def gen_qpsk(N, rng):
    """QPSK, |s|=1. Returns (symbols, bits)."""
    bits = rng.integers(0, 2, N * 2)
    s = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    return s, bits


def qpsk_demap(z):
    z = np.asarray(z).flatten()
    bits = np.zeros(len(z) * 2, dtype=int)
    bits[0::2] = (z.real < 0).astype(int)
    bits[1::2] = (z.imag < 0).astype(int)
    return bits


def gen_16qam(N, rng):
    """16QAM Gray-coded, E[|s|²]=1. Returns (symbols, bits)."""
    levels = QAM16_LEVELS / QAM16_NORM
    I_idx = rng.integers(0, 4, N)
    Q_idx = rng.integers(0, 4, N)
    s = levels[I_idx] + 1j * levels[Q_idx]
    gray = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    bits = np.zeros(N * 4, dtype=int)
    bits[0::4] = gray[I_idx, 0]
    bits[1::4] = gray[I_idx, 1]
    bits[2::4] = gray[Q_idx, 0]
    bits[3::4] = gray[Q_idx, 1]
    return s, bits


def demap_16qam(z):
    """16QAM nearest-neighbor decision. Returns bits."""
    z = np.asarray(z).flatten() * QAM16_NORM  # unnormalize
    levels = QAM16_LEVELS
    gray = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    I_idx = np.argmin(np.abs(np.real(z)[:, None] - levels[None, :]), axis=1)
    Q_idx = np.argmin(np.abs(np.imag(z)[:, None] - levels[None, :]), axis=1)
    N = len(z)
    bits = np.zeros(N * 4, dtype=int)
    bits[0::4] = gray[I_idx, 0]
    bits[1::4] = gray[I_idx, 1]
    bits[2::4] = gray[Q_idx, 0]
    bits[3::4] = gray[Q_idx, 1]
    return bits


# ─── BER 计算 (含相位校正) ──────────────────────────────────

def compute_ber_qpsk(z, s, skip_frac=0.0):
    """QPSK BER, 4 旋转相位校正取最低."""
    z = np.asarray(z).flatten()
    s = np.asarray(s).flatten()
    n = len(z)
    start = int(n * skip_frac)
    z_eval = z[start:]
    s_eval = s[start:]
    s_bits = qpsk_demap(s_eval)
    best_ber = 1.0
    for deg in [0, 90, 180, 270]:
        rot = np.exp(1j * np.radians(deg))
        ber = float(np.mean(qpsk_demap(z_eval * rot) != s_bits))
        if ber < best_ber:
            best_ber = ber
    return best_ber


def compute_ber_16qam(z, s, skip_frac=0.0):
    """16QAM BER, LS 相位估计 phi=angle(sum(z·conj(s)))."""
    z = np.asarray(z).flatten()
    s = np.asarray(s).flatten()
    n = len(z)
    start = int(n * skip_frac)
    z_eval = z[start:]
    s_eval = s[start:]
    phi_hat = np.angle(np.sum(z_eval * np.conj(s_eval)))
    z_corr = z_eval * np.exp(-1j * phi_hat)
    s_bits = demap_16qam(s_eval)
    return float(np.mean(demap_16qam(z_corr) != s_bits))


def compute_ber(mod, z, s, skip_frac=0.0):
    if mod == 'qpsk':
        return compute_ber_qpsk(z, s, skip_frac)
    else:
        return compute_ber_16qam(z, s, skip_frac)


# ─── oracle 均衡 (撤销 SOP + MMSE) ──────────────────────────

def oracle_equalize(rX, rY, h, theta, gamma_bar):
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 信道生成 (双调制参数化) ────────────────────────────────

def gen_channel(mod, N, alpha, beta, f_g, sop_rate, gamma_bar, seed):
    """双偏振 GG 衰落 + SOP 旋转信道. 返回 rX, rY, sX, sY, h, theta."""
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
    if mod == 'qpsk':
        sX, _ = gen_qpsk(N, rng)
        sY, _ = gen_qpsk(N, rng)
    else:  # 16qam
        sX, _ = gen_16qam(N, rng)
        sY, _ = gen_16qam(N, rng)
    theta = sop_rate * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * gamma_bar)
    rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY, sX, sY, h, theta


# ─── 单次 trial: 四方同信道 (CMMA/CMA/ML/oracle) ────────────

def run_trial(mod, rX, rY, sX, sY, h, theta, n_train, run_ml):
    """CMMA/CMA/oracle (+可选 ML) 同信道四方 BER.

    BER 段:
      - CMA/CMMA: 跳前 10% 暂态 (SKIP_FRAC); 发散用 diverge_idx 前 valid 段
      - oracle: 全段 (跳前 10% 暂态一致, 但 oracle 无暂态, 用 0)
      - ML: 测试段后 50% (前 50% 训练)

    返回 dict: cmma_ber/cma_ber/oracle_ber/ml_ber (+diverged 标记).
    """
    R2_cma = R2_QPSK if mod == 'qpsk' else R2_16QAM
    R2_rings_cmma = R2_RINGS_QPSK if mod == 'qpsk' else R2_RINGS_16QAM

    out = {}

    # ── CMA ──
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU, R2=R2_cma)
    res_cma = cma.equalize(rX, rY)
    if res_cma['diverged'] and res_cma['diverge_idx'] is not None:
        valid = max(int(res_cma['diverge_idx']), 1)
        skip = max(1, int(valid * SKIP_FRAC)) if valid > 1000 else 0
        cma_ber = compute_ber(mod, res_cma['zX'][:valid], sX[:valid],
                              skip / valid if valid else 0)
    else:
        cma_ber = compute_ber(mod, res_cma['zX'], sX, SKIP_FRAC)
    out['cma_ber'] = cma_ber
    out['cma_diverged'] = bool(res_cma['diverged'])

    # ── CMMA ──
    cmma = CMMAEqualizer2x2(n_tap=N_TAP, mu=MU, R2_rings=R2_rings_cmma)
    res_cmma = cmma.equalize(rX, rY)
    if res_cmma['diverged'] and res_cmma['diverge_idx'] is not None:
        valid = max(int(res_cmma['diverge_idx']), 1)
        skip = max(1, int(valid * SKIP_FRAC)) if valid > 1000 else 0
        cmma_ber = compute_ber(mod, res_cmma['zX'][:valid], sX[:valid],
                               skip / valid if valid else 0)
    else:
        cmma_ber = compute_ber(mod, res_cmma['zX'], sX, SKIP_FRAC)
    out['cmma_ber'] = cmma_ber
    out['cmma_diverged'] = bool(res_cmma['diverged'])

    # ── oracle ── (全段, 无暂态)
    zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    out['oracle_ber'] = compute_ber(mod, zX_or, sX, 0.0)

    # ── ML ── (可选; 训练前 50%, 测试后 50%)
    if run_ml:
        ml = MLChannelEqualizer(**ML_PARAMS)
        ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                 val_split=0.2, verbose=False)
        res_ml = ml.equalize(rX, rY)
        zX_ml = res_ml['zX'].flatten()
        out['ml_ber'] = compute_ber(mod, zX_ml[n_train:], sX[n_train:], 0.0)
    else:
        out['ml_ber'] = None

    return out


# ─── seed 生成 (确定性, 复现) ───────────────────────────────

def make_seed(mod, f_g, seed_idx):
    return int(hash(('cmma_ber', mod, f_g, seed_idx)) % (2 ** 32))


# ─── 单调制扫描 ─────────────────────────────────────────────

def run_mod_scan(mod, alpha, beta, n_symbols, n_seeds_cma, n_seeds_ml,
                 smoke=False, ml_enabled=True):
    """跑单调制的 CMMA/CMA/oracle (n_seeds_cma) + ML (n_seeds_ml).

    ml_enabled=False 时只跑 CMMA/CMA/oracle (ML 留空, 后续单独补).
    """
    f_g_sweep = F_G_SWEEP if not smoke else [100.0]
    n_train = int(n_symbols * ML_TRAIN_FRAC)

    # results[fg_str] = {cmma_ber:[...], cma_ber:[...], oracle_ber:[...],
    #                    ml_ber:[...], cmma_diverged:[...], cma_diverged:[...]}
    results = defaultdict(lambda: {
        'cmma_ber': [], 'cma_ber': [], 'oracle_ber': [], 'ml_ber': [],
        'cmma_diverged': [], 'cma_diverged': []})

    # 续跑: 从 checkpoint 恢复
    ckpt = _load_ckpt()
    mod_ckpt = ckpt.get(mod, {})
    for k, v in mod_ckpt.items():
        if len(v.get('cmma_ber', [])) >= n_seeds_cma:
            results[k] = v
    done = sum(1 for f_g in f_g_sweep
               if str(f_g) in results
               and len(results[str(f_g)]['cmma_ber']) >= n_seeds_cma)
    print(f"  [{mod}] 续跑: {done}/{len(f_g_sweep)} f_G 完成")

    print(f"  {'f_G(Hz)':>8} | {'CMMA':>10} {'CMA':>10} {'ML':>10} "
          f"{'oracle':>10} | {'CMMA/CMA':>8} {'CMA/or':>8} {'n_div':>6} "
          f"{'t(s)':>6}")

    t_mod0 = time.time()
    for f_g in f_g_sweep:
        key = str(f_g)
        # cached 条件: CMA seeds 满 + (ML 关闭 OR ML seeds 满)
        cma_done = (key in results
                    and len(results[key]['cmma_ber']) >= n_seeds_cma)
        ml_valid = [r for r in results.get(key, {}).get('ml_ber', [])
                    if r is not None]
        ml_done = (not ml_enabled) or (len(ml_valid) >= n_seeds_ml)
        if cma_done and ml_done:
            v = results[key]
            cmma_m = np.mean(v['cmma_ber'])
            cma_m = np.mean(v['cma_ber'])
            or_m = np.mean(v['oracle_ber'])
            ml_m = np.mean(ml_valid) if ml_valid else float('nan')
            ratio = cmma_m / cma_m if cma_m > 0 else float('nan')
            or_ratio = cma_m / or_m if or_m > 0 else float('nan')
            n_div = int(np.sum(v['cmma_diverged'])) + int(np.sum(v['cma_diverged']))
            print(f"  {f_g:>8.0f} | {cmma_m:>10.2e} {cma_m:>10.2e} "
                  f"{ml_m:>10.2e} {or_m:>10.2e} | {ratio:>8.3f} "
                  f"{or_ratio:>8.2f} {n_div:>6d} {'-':>6} (cached)", flush=True)
            continue

        t_fg = time.time()
        n_have = len(results[key]['cmma_ber'])
        # 增量恢复: 若 CMA 数据已满 (n_have>=n_seeds_cma), 不重跑 CMA,
        # 只补缺失的 ML (重新生成对应 seed 的信道, 因信道不持久化).
        cma_already_full = n_have >= n_seeds_cma
        if cma_already_full:
            # 只补 ML (若 ml_enabled 且 ML 不全)
            ml_valid = [r for r in results[key]['ml_ber'] if r is not None]
            if ml_enabled and len(ml_valid) < n_seeds_ml:
                for seed_idx in range(n_seeds_ml):
                    if seed_idx < len(results[key]['ml_ber']) and \
                            results[key]['ml_ber'][seed_idx] is not None:
                        continue
                    seed_int = make_seed(mod, f_g, seed_idx)
                    rX, rY, sX, sY, h, theta = gen_channel(
                        mod, n_symbols, alpha, beta, f_g, SOP_RATE,
                        GAMMA_BAR, seed_int)
                    ml = MLChannelEqualizer(**ML_PARAMS)
                    ml.train(rX[:n_train], rY[:n_train], sX[:n_train],
                             sY[:n_train], val_split=0.2, verbose=False)
                    res_ml = ml.equalize(rX, rY)
                    zX_ml = res_ml['zX'].flatten()
                    ml_ber = compute_ber(mod, zX_ml[n_train:],
                                         sX[n_train:], 0.0)
                    if seed_idx < len(results[key]['ml_ber']):
                        results[key]['ml_ber'][seed_idx] = float(ml_ber)
                    else:
                        results[key]['ml_ber'].append(float(ml_ber))
        else:
            # CMA/CMMA/oracle: 从 n_have 继续跑 n_seeds_cma 个 seed
            for seed_idx in range(n_have, n_seeds_cma):
                seed_int = make_seed(mod, f_g, seed_idx)
                rX, rY, sX, sY, h, theta = gen_channel(
                    mod, n_symbols, alpha, beta, f_g, SOP_RATE,
                    GAMMA_BAR, seed_int)
                # ML 只在前 n_seeds_ml 个 seed 跑 (ml_enabled=False 时跳过)
                run_ml = ml_enabled and seed_idx < n_seeds_ml
                out = run_trial(mod, rX, rY, sX, sY, h, theta, n_train,
                                run_ml)
                results[key]['cmma_ber'].append(float(out['cmma_ber']))
                results[key]['cma_ber'].append(float(out['cma_ber']))
                results[key]['oracle_ber'].append(float(out['oracle_ber']))
                results[key]['cmma_diverged'].append(
                    int(out['cmma_diverged']))
                results[key]['cma_diverged'].append(
                    int(out['cma_diverged']))
                if out['ml_ber'] is not None:
                    results[key]['ml_ber'].append(float(out['ml_ber']))

        v = results[key]
        cmma_m = np.mean(v['cmma_ber'])
        cma_m = np.mean(v['cma_ber'])
        or_m = np.mean(v['oracle_ber'])
        ml_valid = [r for r in v['ml_ber'] if r is not None]
        ml_m = np.mean(ml_valid) if ml_valid else float('nan')
        ratio = cmma_m / cma_m if cma_m > 0 else float('nan')
        or_ratio = cma_m / or_m if or_m > 0 else float('nan')
        n_div = int(np.sum(v['cmma_diverged'])) + int(np.sum(v['cma_diverged']))
        dt = time.time() - t_fg
        print(f"  {f_g:>8.0f} | {cmma_m:>10.2e} {cma_m:>10.2e} "
              f"{ml_m:>10.2e} {or_m:>10.2e} | {ratio:>8.3f} "
              f"{or_ratio:>8.2f} {n_div:>6d} {dt:>6.0f}", flush=True)

        # 写 checkpoint (每 f_G)
        ckpt[mod] = {k: val for k, val in results.items()}
        _save_ckpt(ckpt)

    print(f"  [{mod}] 总耗时: {time.time()-t_mod0:.0f}s")
    return results


# ─── summarize ──────────────────────────────────────────────

def summarize(results, n_seeds_cma, n_seeds_ml):
    out = {}
    for key, v in results.items():
        ml_valid = [r for r in v['ml_ber'] if r is not None]
        out[key] = {
            'cmma_ber_mean': float(np.mean(v['cmma_ber'])),
            'cmma_ber_std': float(np.std(v['cmma_ber'])),
            'cmma_ber_list': [float(x) for x in v['cmma_ber']],
            'cma_ber_mean': float(np.mean(v['cma_ber'])),
            'cma_ber_std': float(np.std(v['cma_ber'])),
            'cma_ber_list': [float(x) for x in v['cma_ber']],
            'ml_ber_mean': (float(np.mean(ml_valid)) if ml_valid else None),
            'ml_ber_list': [float(x) for x in ml_valid],
            'oracle_ber_mean': float(np.mean(v['oracle_ber'])),
            'oracle_ber_list': [float(x) for x in v['oracle_ber']],
            'cmma_diverged_count': int(np.sum(v['cmma_diverged'])),
            'cma_diverged_count': int(np.sum(v['cma_diverged'])),
            'n_seeds_cma': n_seeds_cma,
            'n_seeds_ml': len(ml_valid),
        }
    return out


# ─── smoke test ─────────────────────────────────────────────

def smoke_test():
    """QPSK 1 seed, N=500K, f_G=100Hz, 验证 CMMA≈CMA (实现正确性)."""
    print("=" * 70)
    print("SMOKE TEST: QPSK, 1 seed, N=500K, f_G=100Hz (验证 CMMA≈CMA)")
    print("=" * 70)
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    n_smoke = 500_000
    n_train = int(n_smoke * ML_TRAIN_FRAC)
    f_g = 100.0
    seed_int = make_seed('qpsk', f_g, 0)
    rX, rY, sX, sY, h, theta = gen_channel(
        'qpsk', n_smoke, alpha, beta, f_g, SOP_RATE, GAMMA_BAR, seed_int)
    out = run_trial('qpsk', rX, rY, sX, sY, h, theta, n_train, run_ml=False)
    cmma_ber = out['cmma_ber']
    cma_ber = out['cma_ber']
    oracle_ber = out['oracle_ber']
    print(f"  CMMA(QPSK,R2_rings=[1.0])  BER = {cmma_ber:.4e}")
    print(f"  CMA (QPSK,R2=1.0)         BER = {cma_ber:.4e}")
    print(f"  oracle                    BER = {oracle_ber:.4e}")
    diff = abs(cmma_ber - cma_ber)
    rel = diff / max(cma_ber, 1e-12)
    print(f"  |CMMA-CMA|/CMA = {rel:.3e} (单环数学等价, 应≈0)")
    verdict = 'PASS' if rel < 0.05 else 'FAIL'
    print(f"  Verdict: {verdict}")
    return verdict, cmma_ber, cma_ber


# ─── 主入口 ─────────────────────────────────────────────────

def main(smoke=False, ml_enabled=True):
    t0 = time.time()
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    print("=" * 78)
    print(f"G3: CMMA BER vs f_G (QPSK + 16QAM 双调制, CMMA/CMA/ML/oracle 四方)")
    print("=" * 78)
    print(f"参数: mods={MOD_LIST}, turb={TURB}(α={alpha},β={beta}), N={N_SYMBOLS}")
    print(f"  SNR={SNR_DB}dB(γ̄={GAMMA_BAR}), SOP={SOP_RATE}(1krad/s), tap={N_TAP}, μ={MU}")
    print(f"  f_G={F_G_SWEEP}, seeds: CMA/CMMA/oracle={N_SEEDS_CMA}, ML={N_SEEDS_ML}")
    print(f"  ML enabled: {ml_enabled}")
    print(f"  CMMA 16QAM R2_rings={list(R2_RINGS_16QAM)}, CMA 16QAM R2={R2_16QAM}")

    if smoke:
        smoke_test()
        print(f"\nSmoke 总耗时: {time.time()-t0:.0f}s")
        return None

    all_summaries = {}
    smoke_verdict = None
    smoke_cmma = smoke_cma = None
    # 先跑 smoke 验证实现
    sv, smoke_cmma, smoke_cma = smoke_test()
    smoke_verdict = f"{sv}: QPSK 1seed 500K f_G=100Hz, " \
                    f"CMMA={smoke_cmma:.4e} vs CMA={smoke_cma:.4e}"
    if sv == 'FAIL':
        print("\n!! smoke FAIL: CMMA≠CMA on QPSK, 实现有 bug, 停止 !!")
        return None

    print("\n--- Phase 1: QPSK ---")
    res_qpsk = run_mod_scan('qpsk', alpha, beta, N_SYMBOLS,
                            N_SEEDS_CMA, N_SEEDS_ML, ml_enabled=ml_enabled)
    print("\n--- Phase 2: 16QAM ---")
    res_16qam = run_mod_scan('16qam', alpha, beta, N_SYMBOLS,
                             N_SEEDS_CMA, N_SEEDS_ML, ml_enabled=ml_enabled)

    all_summaries['qpsk'] = summarize(res_qpsk, N_SEEDS_CMA, N_SEEDS_ML)
    all_summaries['16qam'] = summarize(res_16qam, N_SEEDS_CMA, N_SEEDS_ML)

    elapsed = time.time() - t0
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'G3 CMMA BER vs f_G (R004 batch2 task2)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': elapsed,
            'params': {
                'mod_list': MOD_LIST, 'turbulence': TURB,
                'turbulence_alpha_beta': [alpha, beta],
                'snr_db': SNR_DB, 'gamma_bar': GAMMA_BAR,
                'n_symbols': N_SYMBOLS, 'sop_rate': SOP_RATE,
                'sop_krad_s': SOP_RATE * 2.5e9 / 1e3,
                'n_tap': N_TAP, 'mu': MU,
                'f_g_sweep': F_G_SWEEP,
                'cmma_r2_rings_16qam': list(R2_RINGS_16QAM),
                'cmma_r2_rings_qpsk': list(R2_RINGS_QPSK),
                'cma_r2_16qam': float(R2_16QAM), 'cma_r2_qpsk': R2_QPSK,
                'n_seeds_cma': N_SEEDS_CMA, 'n_seeds_ml': N_SEEDS_ML,
                'ml_train_frac': ML_TRAIN_FRAC, 'ml_params': ML_PARAMS,
                'skip_frac': SKIP_FRAC,
                'snr_noise_formula': 'nv = 1/(2*gamma_bar)',
                'qpsk_phase_correction': '4 rotation [0,90,180,270], take min BER',
                'qam16_phase_correction': 'LS: phi_hat=angle(sum(z·conj(s)))',
            },
            'tl20_expected': (
                'QPSK: CMMA(R2_rings=[1.0]) BER ≈ CMA(R2=1.0) BER (数学等价, '
                '验证实现). 排名: ML < oracle < CMMA ≈ CMA. '
                '16QAM: CMMA(R2_rings=[0.2,1.0,1.8]) 应略优于 CMA(R2=1.32) '
                '(多模匹配三环降 modulus mismatch), 但在线更新仍有跟踪滞后 '
                '→ 稳态 BER 仍比 ML/oracle 差. 排名: ML < oracle < CMMA < CMA. '
                '关键对比: CMMA 在 16QAM 是否优于 CMA? '
                '若 CMMA≈CMA → 多模修星座但不降 BER 也是结论.'),
            'smoke_test_qpsk_cmma_eq_cma': smoke_verdict,
        },
        'results': all_summaries,
    }
    out_path = RESULTS_DIR / 'cmma_ber_vs_fg_results.json'
    save_results(out, str(out_path), 'cmma_ber_vs_fg')

    # 清 checkpoint
    try:
        CKPT_PATH.unlink()
        print(f"已清理 checkpoint: {CKPT_PATH}")
    except Exception:
        pass

    print(f"\n总耗时: {elapsed:.0f}s")
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='G3: CMMA BER vs f_G (QPSK + 16QAM 四方)')
    parser.add_argument('--smoke', action='store_true',
                        help='只跑 smoke test (QPSK 1 seed 500K f_G=100)')
    parser.add_argument('--no-ml', action='store_true',
                        help='跳过 ML (只跑 CMMA/CMA/oracle, 后续单独补 ML)')
    args = parser.parse_args()
    main(smoke=args.smoke, ml_enabled=not args.no_ml)
