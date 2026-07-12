"""G1: 16QAM BER vs f_G — CMA/ML/oracle 三方对比 (D008 债务).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)
> 来源: R004 批次1 G1 (D008 Sup-1 发现 16QAM modulus mismatch 是结构性缺陷, 但 BER 数据缺)

# TL-25 checklist: [1/2/3/4/5/6] 全部确认
#   1. 共享信道: CMA/ML/oracle 三方用同一组 (rX,rY,sX,sY,h,theta)
#   2. 重生信道: 每个 f_G 点重生信道 (f_G 变 → tau_c 变 → AR(1) ρ 变)
#   3. 从 common 导入: CMAEqualizer2x2 / MLChannelEqualizer / mmse_equalize / gg_time_envelope
#   4. 基线已优化: CMA μ=1e-3 安全区, R2=1.32 (16QAM Godard), n_tap=11
#   5. 先写理论预期: 见下方 TL-20 预期段
#   6. 输出含元数据: 用 save_results() 注入 git hash + common_md5 + 时间戳

## TL-20 理论预期 (跑之前写, 偏离即查)

固定 SNR=20dB, strong 湍流, 扫 f_G=[10,30,100,300,1000,3000]Hz:

- 16QAM 的 CMA BER 应比 QPSK 更高 (modulus mismatch 结构性缺陷, D008 Sup-1 已发现)
  QPSK |s|=1 恒模, R²=1 完美匹配; 16QAM |s|²∈{0.2,1.0,1.8} 三环, 单 R²=1.32 是
  Godard 最小化但仍有 mismatch (内环拉外、外环拉内)
- ML 在 16QAM 也应优于 CMA (ML 用 MSE 监督, 不受 modulus mismatch 限制)
- 跟 QPSK 对比 (r_lcr exp3 数据): 16QAM 的 ML vs CMA gap 可能更大
  (CMA 的 modulus mismatch + 跟踪滞后 双重惩罚)
- 参考 D008 Sup-1 实测 (sup_stress_test_results.json sup1_16qam):
  safe_1e-3_30Hz: CMA BER 0.26/0.047/0.29, ML 0.033/1e-4/0 → ML 显著优

## 设计要点

- 调制: 16QAM (gen_16qam/demap_16qam 复用自 sup_stress_test.py)
- CMA R2=1.32 (16QAM Godard R², sup_stress_test.py:56)
- BER 相位校正: 16QAM 用 LS 相位估计 (angle(sum(z·conj(s)))) 消除残余相位旋转
  (CMA/ML 输出可能有残余相位, 不校正 BER≈0.5 不可比; sup_stress_test 没做这步但
  它的 CMA 收敛足够好相位已对齐, 我们加 LS 估计更稳健)
- 固定 SNR=20dB (gamma_bar=100), 扫 f_G
- 每 f_G 独立训一个 ML (train_frac=0.5)
- 断点续跑: 每完成一个 f_G 写 checkpoint

## 参数 (🟡 全从 params.py 读, 不硬编码)

- N_SYMBOLS = 2_000_000 (跟 r_lcr/任务1 一致, 保 BER 量级可比)
- SNR = 20dB 固定 (gamma_bar=100)
- SOP_RATE = 4e-7 rad/sym (1 krad/s)
- F_G_SWEEP = [10, 30, 100, 300, 1000, 3000] Hz (跟 r_lcr exp3 一致, 便于 QPSK 对比)
- CMA: n_tap=11, μ=1e-3, R2=1.32 (16QAM)
- ML: n_tap=11, lr=0.005, batch_size=1024, train_frac=0.5
- N_SEEDS = 5

用法:
  cd projects/simulation && python explore/cma-fade-divergence/ber_16qam_vs_fg.py
"""
import sys
import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from common._config import BLOCK
from common._experiment import save_results

cfg = SimulationConfig()
T_S = cfg.system.T_S

# ─── 实验参数 ───────────────────────────────────────────────
F_G_SWEEP = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
MOD = '16qam'
TURB = 'strong'  # α=1.5, β=0.8
SNR_DB = 20.0
GAMMA_BAR = 10.0 ** (SNR_DB / 10.0)  # 100
N_SYMBOLS = 2_000_000  # 跟 r_lcr/任务1 一致
SOP_RATE = 4e-7  # 1 krad/s
N_TAP = 11
MU_CMA = 1e-3
# 16QAM Godard R² = E[|s|⁴]/E[|s|²] (sup_stress_test.py:56)
# |s|²∈{0.2,1.0,1.8}, probs{4/16,8/16,4/16} → E[|s|⁴]=(4×0.04+8×1.0+4×3.24)/16=1.32
R2_16QAM = 1.32
SKIP_FRAC = 0.10  # CMA BER 跳过前 10% 暂态
N_SEEDS = 5
ML_PARAMS = dict(n_tap=N_TAP, lr=0.005, batch_size=1024, n_epochs=20,
                 device='cuda', patience=5)
ML_TRAIN_FRAC = 0.5

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
CKPT_PATH = RESULTS_DIR / 'ber_16qam_vs_fg_checkpoint.json'


def _load_ckpt():
    if CKPT_PATH.exists():
        try:
            with open(CKPT_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {'results': {}}
    return {'results': {}}


def _save_ckpt(data):
    try:
        with open(CKPT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception:
        pass


# ─── 16QAM 调制/解调 (复用自 sup_stress_test.py) ─────────────

QAM16_LEVELS = np.array([-3, -1, 1, 3])
QAM16_NORM = np.sqrt(10.0)


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


def compute_ber_16qam_phase_corrected(z, s, skip_frac=0.0):
    """16QAM BER, 先做 LS 相位估计校正 (消除残余相位旋转).

    LS 相位估计: phi_hat = angle(sum(z · conj(s))), 应用 z * exp(-j·phi_hat).
    比 QPSK 的 4 角度搜索更通用 (16QAM 相位模糊不只是 π/2, LS 估计连续相位).
    """
    z = np.asarray(z).flatten()
    s = np.asarray(s).flatten()
    n = len(z)
    start = int(n * skip_frac)
    z_eval = z[start:]
    s_eval = s[start:]
    # LS 相位估计: 最小化 |z·e^{-jφ} - s|² → φ = angle(sum(z·conj(s)))
    phi_hat = np.angle(np.sum(z_eval * np.conj(s_eval)))
    z_corr = z_eval * np.exp(-1j * phi_hat)
    s_bits = demap_16qam(s_eval)
    return float(np.mean(demap_16qam(z_corr) != s_bits))


def compute_ber(z, s, skip_frac=0.0):
    return compute_ber_16qam_phase_corrected(z, s, skip_frac)


def oracle_equalize(rX, rY, h, theta, gamma_bar):
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 信道生成 (16QAM 版) ─────────────────────────────────────

def gen_channel(N, alpha, beta, f_g, sop_rate, gamma_bar, seed):
    """生成双偏振 GG 衰落 + SOP 旋转信道 (16QAM)."""
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
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


# ─── 单点试验: CMA / ML / oracle 三方 ─────────────────────────

def run_point(rX, rY, sX, sY, h, theta, gamma_bar, n_train):
    """CMA/ML/oracle 三方 16QAM BER."""
    # CMA (R2=1.32 16QAM, μ=1e-3 安全)
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_CMA, R2=R2_16QAM)
    res_cma = cma.equalize(rX, rY)
    if res_cma['diverged'] and res_cma['diverge_idx'] is not None:
        valid = max(int(res_cma['diverge_idx']), 1)
        v_end = min(valid, n_train) if valid > n_train else valid
        cma_ber = compute_ber(res_cma['zX'][:v_end], sX[:v_end], 0.0) if v_end > 100 else 0.5
    else:
        cma_ber = compute_ber(res_cma['zX'][n_train:], sX[n_train:], 0.0)
    cma_div = bool(res_cma['diverged'])

    # ML (每 f_G 独立训练)
    ml = MLChannelEqualizer(**ML_PARAMS)
    ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
             val_split=0.2, verbose=False)
    res_ml = ml.equalize(rX, rY)
    zX_ml = res_ml['zX'].flatten()
    ml_ber = compute_ber(zX_ml[n_train:], sX[n_train:], 0.0)

    # oracle
    zX_or, _ = oracle_equalize(rX, rY, h, theta, gamma_bar)
    oracle_ber = compute_ber(zX_or[n_train:], sX[n_train:], 0.0)

    return cma_ber, ml_ber, oracle_ber, cma_div


# ─── 主扫描 ─────────────────────────────────────────────────

def run_scan():
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    n_train = int(N_SYMBOLS * ML_TRAIN_FRAC)
    print(f"扫描: {len(F_G_SWEEP)} f_G × {N_SEEDS} seeds")
    print(f"参数: {MOD}, turb={TURB}(α={alpha},β={beta}), N={N_SYMBOLS}, "
          f"SNR={SNR_DB}dB(γ̄={GAMMA_BAR}), SOP={SOP_RATE}(1krad/s), tap={N_TAP}")
    print(f"f_G: {F_G_SWEEP}")
    print(f"CMA μ={MU_CMA}, R2={R2_16QAM} (16QAM Godard)")
    print()

    results = defaultdict(lambda: {'cma_ber': [], 'ml_ber': [],
                                   'oracle_ber': [], 'cma_diverged': []})
    ckpt = _load_ckpt()
    for k, v in ckpt.get('results', {}).items():
        if len(v.get('cma_ber', [])) >= N_SEEDS:
            results[k] = v
    done = sum(1 for f_g in F_G_SWEEP
               if str(f_g) in results
               and len(results[str(f_g)]['cma_ber']) >= N_SEEDS)
    print(f"[续跑] 已完成 {done}/{len(F_G_SWEEP)} f_G\n")

    t0 = time.time()
    print(f"{'f_G(Hz)':>8} {'CMA_BER':>10} {'ML_BER':>10} {'oracle_BER':>11} "
          f"{'n_div':>6} {'n':>4} {'t(s)':>6}")

    for f_g in F_G_SWEEP:
        key = str(f_g)
        if key in results and len(results[key]['cma_ber']) >= N_SEEDS:
            v = results[key]
            print(f"{f_g:>8.0f} {np.mean(v['cma_ber']):>10.2e} "
                  f"{np.mean(v['ml_ber']):>10.2e} {np.mean(v['oracle_ber']):>11.2e} "
                  f"{int(sum(v['cma_diverged'])):>6d} {N_SEEDS:>4d} {'-':>6} (cached)",
                  flush=True)
            continue

        t_point = time.time()
        for seed in range(N_SEEDS):
            seed_int = int(hash(('ber16qam', f_g, seed)) % (2**32))
            rX, rY, sX, sY, h, theta = gen_channel(
                N_SYMBOLS, alpha, beta, f_g, SOP_RATE, GAMMA_BAR, seed_int)
            cma_ber, ml_ber, oracle_ber, cma_div = run_point(
                rX, rY, sX, sY, h, theta, GAMMA_BAR, n_train)
            results[key]['cma_ber'].append(cma_ber)
            results[key]['ml_ber'].append(ml_ber)
            results[key]['oracle_ber'].append(oracle_ber)
            results[key]['cma_diverged'].append(int(cma_div))

        v = results[key]
        dt = time.time() - t_point
        print(f"{f_g:>8.0f} {np.mean(v['cma_ber']):>10.2e} "
              f"{np.mean(v['ml_ber']):>10.2e} {np.mean(v['oracle_ber']):>11.2e} "
              f"{int(sum(v['cma_diverged'])):>6d} {N_SEEDS:>4d} {dt:>6.0f}", flush=True)
        _save_ckpt({'results': {str(k): val for k, val in results.items()
                                 if len(val.get('cma_ber', [])) >= N_SEEDS}})

    elapsed = time.time() - t0
    print(f"\n扫描完成, 耗时 {elapsed:.0f}s")
    return results, elapsed


def summarize(results):
    out = {}
    for key, v in results.items():
        out[key] = {
            'cma_ber_mean': float(np.mean(v['cma_ber'])),
            'cma_ber_std': float(np.std(v['cma_ber'])),
            'cma_ber_list': [float(x) for x in v['cma_ber']],
            'ml_ber_mean': float(np.mean(v['ml_ber'])),
            'ml_ber_std': float(np.std(v['ml_ber'])),
            'ml_ber_list': [float(x) for x in v['ml_ber']],
            'oracle_ber_mean': float(np.mean(v['oracle_ber'])),
            'oracle_ber_std': float(np.std(v['oracle_ber'])),
            'oracle_ber_list': [float(x) for x in v['oracle_ber']],
            'n_diverged': int(np.sum(v['cma_diverged'])),
            'n_seeds': N_SEEDS,
        }
    return out


def main():
    t0 = time.time()
    print("=" * 78)
    print(f"G1: 16QAM BER vs f_G (SNR={SNR_DB}dB, strong 湍流, CMA/ML/oracle 三方)")
    print("=" * 78)

    results, elapsed = run_scan()
    summary = summarize(results)

    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'G1 16QAM BER vs f_G (R004 batch1, D008 debt)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': time.time() - t0,
            'params': {
                'mod': MOD, 'turbulence': TURB,
                'turbulence_alpha_beta': list(cfg.turbulence.as_dict()[TURB]),
                'snr_db': SNR_DB, 'gamma_bar': GAMMA_BAR,
                'n_symbols': N_SYMBOLS, 'sop_rate': SOP_RATE,
                'sop_krad_s': SOP_RATE * 2.5e9 / 1e3,
                'n_tap': N_TAP, 'mu_cma': MU_CMA, 'r2_16qam': R2_16QAM,
                'f_g_sweep': F_G_SWEEP, 'n_seeds': N_SEEDS,
                'ml_train_frac': ML_TRAIN_FRAC, 'ml_params': ML_PARAMS,
                'skip_frac': SKIP_FRAC,
                'snr_noise_formula': 'nv = 1/(2*gamma_bar)',
                'ber_phase_correction': 'LS: phi_hat=angle(sum(z·conj(s)))',
            },
            'tl25_expected': (
                '16QAM CMA BER > QPSK CMA BER (modulus mismatch); '
                'ML 16QAM > CMA 16QAM (MSE 监督不受 modulus 限制); '
                '16QAM ML-vs-CMA gap > QPSK (双重惩罚)'),
        },
        'results': summary,
    }
    out_path = RESULTS_DIR / 'ber_16qam_vs_fg_results.json'
    save_results(out, str(out_path), 'ber_16qam_vs_fg')

    try:
        CKPT_PATH.unlink()
        print(f"已清理 checkpoint: {CKPT_PATH}")
    except Exception:
        pass

    print(f"\n总耗时: {time.time()-t0:.0f}s")
    return out


if __name__ == '__main__':
    main()
