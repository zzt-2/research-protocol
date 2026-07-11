"""补充压力测试 — 压力测试 Q-CMA-FADE Go 判定。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P5 标方向+状态)

三个实验, 诚实检验 Go 判定是否经得起审稿:

Sup-1: 16QAM CMA vs ML vs oracle
  - CMA 在 16QAM 有 modulus mismatch (Qin 2025 L41): 单 R² 不能匹配多环星座
  - 问题: 16QAM 下 CMA 是否更易发散? ML 是否保持优势?
  - 如果 CMA 在 16QAM 连安全区都出问题 → 方向更有价值
  - 如果 CMA 在 16QAM 安全区也 OK → 方向变弱

Sup-2: CMA μ=1e-3 在危险区信道条件下是否够用
  - Step B 说 μ≤1e-3 安全 (P_div≈0), 但没测 BER
  - 问题: μ=1e-3 在快变信道 (f_G=1000Hz) 下能否跟住? BER 够不够?
  - 如果 μ=1e-3 BER≈oracle → "用小步长就行" = 方向根基动摇
  - 如果 μ=1e-3 BER 差 (跟踪太慢) → 真有 tradeoff: 小μ=稳但慢, 大μ=快但发散

Sup-3: ML SOP 漂移退化
  - ML 是固定权重前馈, CMA 是在线自适应 → CMA 天然能跟 SOP, ML 不能
  - 问题: ML 能容忍多少 SOP 漂移? (Nasr 2026 报 ±4° 泛化)
  - 训练 θ=0, 测试 θ=5°/10°/20°/45°/90°
  - 如果 <5° 就退化 → ML 需频繁重训练, pilot 开销大
  - 如果 >20° 还行 → ML 重训练周期可接受
"""
import sys
import json
import time
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from params import SimulationConfig

cfg = SimulationConfig()
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT
BLOCK = cfg.experiment.BLOCK
T_S = cfg.system.T_S


# ─── 16QAM 调制/解调 ────────────────────────────────────────

# 16QAM: levels [-3,-1,1,3], normalized by sqrt(10) → E[|s|²]=1
QAM16_LEVELS = np.array([-3, -1, 1, 3])
QAM16_NORM = np.sqrt(10.0)
# R² for 16QAM (Godard 1980): R² = E[|s|⁴]/E[|s|²]
# |s|² ∈ {2,10,18}/10 = {0.2,1.0,1.8}, probs {4/16,8/16,4/16}
# E[|s|⁴] = (4×0.04 + 8×1.0 + 4×3.24)/16 = 1.32
R2_16QAM = 1.32


def gen_16qam(N, rng):
    """16QAM Gray-coded, E[|s|²]=1. Returns (symbols, bits)."""
    levels = QAM16_LEVELS / QAM16_NORM
    I_idx = rng.integers(0, 4, N)
    Q_idx = rng.integers(0, 4, N)
    s = levels[I_idx] + 1j * levels[Q_idx]
    # Gray: 00->-3, 01->-1, 11->+1, 10->+3
    gray = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    bits = np.zeros(N * 4, dtype=int)
    bits[0::4] = gray[I_idx, 0]
    bits[1::4] = gray[I_idx, 1]
    bits[2::4] = gray[Q_idx, 0]
    bits[3::4] = gray[Q_idx, 1]
    return s, bits


def demap_16qam(z):
    """16QAM nearest-neighbor decision. Returns bits."""
    z = z * QAM16_NORM  # unnormalize
    levels = QAM16_LEVELS
    gray = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    # Nearest level for I/Q
    I_real = np.real(z)
    I_dist = np.abs(I_real[:, None] - levels[None, :])
    I_idx = np.argmin(I_dist, axis=1)
    Q_real = np.imag(z)
    Q_dist = np.abs(Q_real[:, None] - levels[None, :])
    Q_idx = np.argmin(Q_dist, axis=1)
    N = len(z)
    bits = np.zeros(N * 4, dtype=int)
    bits[0::4] = gray[I_idx, 0]
    bits[1::4] = gray[I_idx, 1]
    bits[2::4] = gray[Q_idx, 0]
    bits[3::4] = gray[Q_idx, 1]
    return bits


def gen_qpsk(N, rng):
    bits = rng.integers(0, 2, N * 2)
    s = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    return s, bits


def qpsk_demap(z):
    z = np.asarray(z).flatten()
    bits = np.zeros(len(z) * 2, dtype=int)
    bits[0::2] = (z.real < 0).astype(int)
    bits[1::2] = (z.imag < 0).astype(int)
    return bits


def compute_ber(z, s, mod='qpsk'):
    """BER computation."""
    if mod == 'qpsk':
        return float(np.mean(qpsk_demap(z) != qpsk_demap(s)))
    else:  # 16qam
        z_flat = np.asarray(z).flatten()
        return float(np.mean(demap_16qam(z_flat) != demap_16qam(s)))


def oracle_equalize(rX, rY, h, theta, gamma_bar):
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 信道生成 ───────────────────────────────────────────────

def gen_channel(N, alpha, beta, f_g, sop_rate, seed, mod='qpsk'):
    """生成双偏振 GG 衰落 + SOP 旋转信道."""
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
    if mod == 'qpsk':
        sX, bX = gen_qpsk(N, rng)
        sY, bY = gen_qpsk(N, rng)
    else:
        sX, bX = gen_16qam(N, rng)
        sY, bY = gen_16qam(N, rng)
    theta = sop_rate * np.arange(N)
    rX = np.sqrt(h) * (np.cos(theta) * sX + np.sin(theta) * sY)
    rY = np.sqrt(h) * (-np.sin(theta) * sX + np.cos(theta) * sY)
    nv = 1.0 / (2 * GAMMA_BAR)
    rX += np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY += np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY, sX, sY, bX, bY, h, theta


SOP_REALISTIC = 4e-7  # 1 krad/s (sat.1553 §6.3)


# ─── Sup-1: 16QAM CMA vs ML vs oracle ───────────────────────

def run_sup1_16qam():
    """16QAM: CMA vs ML vs oracle, 危险区 + 安全区."""
    print("=" * 60)
    print("Sup-1: 16QAM CMA vs ML vs oracle")
    print("=" * 60)

    N = 500_000
    scenarios = [
        ('danger_1e-2_1000Hz', 1000.0, 1e-2, 'strong'),
        ('safe_1e-3_30Hz',      30.0, 1e-3, 'strong'),
    ]
    n_trials = 3
    results = []

    for scn_name, f_g, mu, turb_name in scenarios:
        alpha, beta = cfg.turbulence.as_dict()[turb_name]
        print(f"\n--- {scn_name} (16QAM) ---")
        for trial in range(n_trials):
            seed = hash(('sup1', scn_name, trial)) % (2**32)
            rX, rY, sX, sY, bX, bY, h, theta = gen_channel(
                N, alpha, beta, f_g, SOP_REALISTIC, seed, mod='16qam')

            # CMA (R²=1.32 for 16QAM)
            cma = CMAEqualizer2x2(n_tap=11, mu=mu, R2=R2_16QAM)
            res_cma = cma.equalize(rX, rY)
            if res_cma['diverged'] and res_cma['diverge_idx']:
                valid = max(res_cma['diverge_idx'], 1)
                ber_cma = compute_ber(res_cma['zX'][:valid], sX[:valid], '16qam')
            else:
                ber_cma = compute_ber(res_cma['zX'], sX, '16qam')

            # ML
            n_train = N // 2
            ml = MLChannelEqualizer(n_tap=11, lr=0.005, batch_size=1024,
                                    n_epochs=20, device='cuda', patience=5)
            ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                     val_split=0.2, verbose=False)
            res_ml = ml.equalize(rX, rY)
            ber_ml = compute_ber(res_ml['zX'].flatten()[n_train:],
                                 sX[n_train:], '16qam')

            # Oracle
            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            ber_or = compute_ber(zX_or[n_train:], sX[n_train:], '16qam')

            ber_raw = compute_ber(rX[n_train:], sX[n_train:], '16qam')

            print(f"  trial {trial}: CMA div={'Y' if res_cma['diverged'] else 'N'} "
                  f"BER(cma={ber_cma:.4f}/ml={ber_ml:.4f}/oracle={ber_or:.4f}/raw={ber_raw:.4f})")
            results.append({
                'scn': scn_name, 'trial': trial, 'mod': '16qam',
                'cma_diverged': res_cma['diverged'], 'cma_ber': ber_cma,
                'ml_ber': ber_ml, 'oracle_ber': ber_or, 'raw_ber': ber_raw,
            })

    # 同时跑 QPSK 对比
    print("\n--- 对比: 同场景 QPSK ---")
    for scn_name, f_g, mu, turb_name in scenarios:
        alpha, beta = cfg.turbulence.as_dict()[turb_name]
        for trial in range(n_trials):
            seed = hash(('sup1', scn_name, trial)) % (2**32)
            rX, rY, sX, sY, bX, bY, h, theta = gen_channel(
                N, alpha, beta, f_g, SOP_REALISTIC, seed, mod='qpsk')
            cma = CMAEqualizer2x2(n_tap=11, mu=mu, R2=1.0)
            res_cma = cma.equalize(rX, rY)
            if res_cma['diverged'] and res_cma['diverge_idx']:
                valid = max(res_cma['diverge_idx'], 1)
                ber_cma = compute_ber(res_cma['zX'][:valid], sX[:valid], 'qpsk')
            else:
                ber_cma = compute_ber(res_cma['zX'], sX, 'qpsk')
            n_train = N // 2
            ml = MLChannelEqualizer(n_tap=11, lr=0.005, batch_size=1024,
                                    n_epochs=20, device='cuda', patience=5)
            ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                     val_split=0.2, verbose=False)
            res_ml = ml.equalize(rX, rY)
            ber_ml = compute_ber(res_ml['zX'].flatten()[n_train:],
                                 sX[n_train:], 'qpsk')
            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            ber_or = compute_ber(zX_or[n_train:], sX[n_train:], 'qpsk')
            ber_raw = compute_ber(rX[n_train:], sX[n_train:], 'qpsk')
            print(f"  {scn_name} trial {trial}: CMA div={'Y' if res_cma['diverged'] else 'N'} "
                  f"BER(cma={ber_cma:.4f}/ml={ber_ml:.4f}/oracle={ber_or:.4f}/raw={ber_raw:.4f})")
            results.append({
                'scn': scn_name, 'trial': trial, 'mod': 'qpsk',
                'cma_diverged': res_cma['diverged'], 'cma_ber': ber_cma,
                'ml_ber': ber_ml, 'oracle_ber': ber_or, 'raw_ber': ber_raw,
            })

    return results


# ─── Sup-2: CMA μ=1e-3 在危险区信道条件下是否够用 ────────────

def run_sup2_cma_safe_mu():
    """CMA at μ=1e-3 in danger zone channel (strong turb, f_G=1000Hz).

    如果 μ=1e-3 BER≈oracle → "用小步长就行" = 方向根基动摇.
    如果 μ=1e-3 BER 差 → 真有 tradeoff.
    """
    print("\n" + "=" * 60)
    print("Sup-2: CMA μ=1e-3 在危险区信道 (strong, f_G=1000Hz)")
    print("=" * 60)

    N = 500_000
    alpha, beta = cfg.turbulence.as_dict()['strong']
    f_g = 1000.0  # 危险区信道
    n_trials = 3
    results = []

    for mod_name, R2, mod in [('QPSK', 1.0, 'qpsk'), ('16QAM', R2_16QAM, '16qam')]:
        print(f"\n--- {mod_name}, CMA μ=1e-3 vs μ=1e-2, f_G=1000Hz strong ---")
        for trial in range(n_trials):
            seed = hash(('sup2', mod_name, trial)) % (2**32)
            rX, rY, sX, sY, bX, bY, h, theta = gen_channel(
                N, alpha, beta, f_g, SOP_REALISTIC, seed, mod=mod)

            n_train = N // 2
            for mu in [1e-3, 5e-3, 1e-2]:
                cma = CMAEqualizer2x2(n_tap=11, mu=mu, R2=R2)
                res = cma.equalize(rX, rY)
                if res['diverged'] and res['diverge_idx']:
                    valid = max(res['diverge_idx'], 1)
                    ber = compute_ber(res['zX'][:valid], sX[:valid], mod)
                else:
                    ber = compute_ber(res['zX'], sX, mod)
                div = 'Y' if res['diverged'] else 'N'
                print(f"  {mod_name} μ={mu:.0e} trial {trial}: div={div} BER={ber:.4f}")
                results.append({
                    'mod': mod_name, 'mu': mu, 'trial': trial,
                    'cma_diverged': res['diverged'], 'cma_ber': ber,
                })

            # Oracle
            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            ber_or = compute_ber(zX_or[n_train:], sX[n_train:], mod)
            if trial == 0:
                print(f"  {mod_name} oracle BER={ber_or:.4f}")
            results.append({
                'mod': mod_name, 'mu': 'oracle', 'trial': trial,
                'cma_diverged': False, 'cma_ber': ber_or,
            })

    return results


# ─── Sup-3: ML SOP 漂移退化 ─────────────────────────────────

def run_sup3_ml_sop_drift():
    """ML 训练 θ=0, 测试 θ=5°/10°/20°/45°/90°.

    CMA 在线自适应 → 天然跟 SOP.
    ML 固定权重 → 需要重训练才能适应新 SOP.
    测: ML 能容忍多少 SOP 漂移?
    """
    print("\n" + "=" * 60)
    print("Sup-3: ML SOP 漂移退化 (训练 θ=0, 测试 θ=各种角度)")
    print("=" * 60)

    N = 500_000
    alpha, beta = cfg.turbulence.as_dict()['strong']
    f_g = 100.0  # 中等衰落
    seed = 42

    # 训练数据: θ=0 (无 SOP 旋转)
    rng = np.random.default_rng(seed)
    h = gg_time_envelope(N, alpha, beta, cfg.gg_time.tau_c_from_fg(f_g),
                         block=BLOCK, t_s=T_S, method='gar', seed=seed)
    sX, bX = gen_qpsk(N, rng)
    sY, bY = gen_qpsk(N, rng)
    nv = 1.0 / (2 * GAMMA_BAR)
    # θ=0: 无 SOP 旋转
    rX_train = np.sqrt(h) * sX + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY_train = np.sqrt(h) * sY + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    # 训练 ML (θ=0)
    print("Training ML at θ=0 (no SOP rotation)...")
    ml = MLChannelEqualizer(n_tap=11, lr=0.005, batch_size=1024,
                            n_epochs=20, device='cuda', patience=5)
    ml.train(rX_train, rY_train, sX, sY, val_split=0.2, verbose=False)
    print(f"  Training done. best_val_loss={ml.best_loss:.6f}")

    # CMA 在各 θ 下 (CMA 在线自适应, 每次重新跑)
    results = []
    theta_deg_list = [0, 5, 10, 20, 45, 90]

    print(f"\n{'θ(deg)':>8} {'ML_BER':>10} {'CMA_BER':>10} {'CMA_div':>8} {'oracle':>10} {'raw':>10}")

    for theta_deg in theta_deg_list:
        theta_rad = np.radians(theta_deg)
        # 测试数据: 固定 θ 旋转
        rng_test = np.random.default_rng(seed + 1000)
        h_test = gg_time_envelope(N, alpha, beta, cfg.gg_time.tau_c_from_fg(f_g),
                                  block=BLOCK, t_s=T_S, method='gar', seed=seed + 1000)
        sX_test, _ = gen_qpsk(N, rng_test)
        sY_test, _ = gen_qpsk(N, rng_test)
        # 固定 θ (不是 θ(t), 是常数)
        rX_test = np.sqrt(h_test) * (np.cos(theta_rad) * sX_test + np.sin(theta_rad) * sY_test)
        rY_test = np.sqrt(h_test) * (-np.sin(theta_rad) * sX_test + np.cos(theta_rad) * sY_test)
        rX_test += np.sqrt(nv) * (rng_test.standard_normal(N) + 1j * rng_test.standard_normal(N))
        rY_test += np.sqrt(nv) * (rng_test.standard_normal(N) + 1j * rng_test.standard_normal(N))

        # ML (固定权重, θ=0 训练的)
        res_ml = ml.equalize(rX_test, rY_test)
        ber_ml = compute_ber(res_ml['zX'].flatten(), sX_test, 'qpsk')

        # CMA (在线自适应, 从头跑)
        cma = CMAEqualizer2x2(n_tap=11, mu=1e-2, R2=1.0)
        res_cma = cma.equalize(rX_test, rY_test)
        if res_cma['diverged'] and res_cma['diverge_idx']:
            valid = max(res_cma['diverge_idx'], 1)
            ber_cma = compute_ber(res_cma['zX'][:valid], sX_test[:valid], 'qpsk')
        else:
            ber_cma = compute_ber(res_cma['zX'], sX_test, 'qpsk')

        # Oracle
        theta_arr = np.full(N, theta_rad)  # 固定 θ
        zX_or, _ = oracle_equalize(rX_test, rY_test, h_test, theta_arr, GAMMA_BAR)
        ber_or = compute_ber(zX_or, sX_test, 'qpsk')

        ber_raw = compute_ber(rX_test, sX_test, 'qpsk')

        div = 'Y' if res_cma['diverged'] else 'N'
        print(f"{theta_deg:>8} {ber_ml:>10.4f} {ber_cma:>10.4f} {div:>8} {ber_or:>10.4f} {ber_raw:>10.4f}")
        results.append({
            'theta_deg': theta_deg, 'ml_ber': ber_ml, 'cma_ber': ber_cma,
            'cma_diverged': res_cma['diverged'], 'oracle_ber': ber_or,
            'raw_ber': ber_raw,
        })

    return results


# ─── 入口 ───────────────────────────────────────────────────

if __name__ == '__main__':
    t0 = time.time()
    sup1_results = run_sup1_16qam()
    sup2_results = run_sup2_cma_safe_mu()
    sup3_results = run_sup3_ml_sop_drift()

    summary = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'C supplementary stress test',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': time.time() - t0,
        },
        'sup1_16qam': sup1_results,
        'sup2_cma_safe_mu': sup2_results,
        'sup3_ml_sop_drift': sup3_results,
    }

    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'sup_stress_test_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")
    print(f"Total time: {time.time() - t0:.0f}s")
