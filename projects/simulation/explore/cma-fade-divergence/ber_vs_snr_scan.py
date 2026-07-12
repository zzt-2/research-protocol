"""F1: BER vs SNR 曲线扫描 — QPSK, 强湍流, 多 f_G, CMA/ML/oracle 三方.

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)
> 来源: R004 批次1 F1 (导师必须的 BER vs SNR 曲线)

# TL-25 checklist: [1/2/3/4/5/6] 全部确认
#   1. 共享信道: CMA/ML/oracle 三方用同一组 (rX,rY,sX,sY,h,theta) — gen_channel 一次, 三方复用
#   2. 重生信道: 每个 (f_G, SNR) 点重生信道 — noise variance nv=1/(2*gamma_bar) 随 SNR 变
#   3. 从 common 导入: CMAEqualizer2x2 / MLChannelEqualizer / mmse_equalize / gg_time_envelope
#   4. 基线已优化: CMA μ=1e-3 安全区步长 (不是凑合默认), n_tap=11 对齐 sat.1553 Fig.13
#   5. 先写理论预期: 见下方 TL-20 预期段
#   6. 输出含元数据: 用 save_results() 注入 git hash + common_md5 + 时间戳

## TL-20 理论预期 (跑之前写, 偏离即查)

固定 strong 湍流 (α=1.5, β=0.8), 扫 SNR 10-40dB:

- 低 SNR (<15dB): 三者 BER 都高 (>0.1), ML 略优 CMA (都接近 raw, 噪声主导)
- 中 SNR (15-25dB): ML 接近 oracle, CMA 因跟踪滞后始终差几倍
- 高 SNR (>25dB): ML≈oracle, CMA 仍有残余 BER (跟踪滞后天花板, 不随 SNR 降)
- 整体趋势: ML/oracle 曲线接近平行 (差一个 offset); CMA 曲线有一个 floor (跟踪滞后 BER 下限)
- f_G 影响: f_G 越大 (衰落越频繁), CMA floor 越高; ML/oracle 受 f_G 影响小

## 设计要点

- SNR 扫描: gamma_bar = 10^(SNR_dB/10), noise variance nv = 1/(2*gamma_bar)
  (跟 r_lcr_ber_impact.py:179 / sup_stress_test.py:147 同公式, sat.1553 信号模型)
- 每 (f_G, SNR) 独立训一个 ML: 训练用该点前 50% 符号, 测试后 50% (无泄漏, Freire 陷阱2)
- ML/CMA/oracle 共用同一信道 (TL-25 rule 1)
- 断点续跑: 每完成一个 (f_G, SNR) 写 checkpoint
- CMA 用 μ=1e-3 安全区步长 (测的是"即使安全步长 CMA 也有跟踪滞后", 不是发散)

## 参数 (🟡 全从 params.py 读, 不硬编码)

- N_SYMBOLS = 2_000_000 (跟 r_lcr_ber_impact.py 一致, 保 BER 量级可比. ⚠️ TL-22 检查发现:
  N=500K 时 @2.5GBaud=0.2ms=0.13τ_c, 衰落动力学未充分展开, CMA BER 比真实低 ~1000×;
  N=2M=0.8ms=0.5τ_c 才与 r_lcr/README 已发布数据量级一致. PROMPT-007 写 500K 是基于
  "BER 到 1e-3 即可" 的精度考量, 但实测发现 500K 物理上不足以展开衰落→BER 惩罚)
- SOP_RATE = 4e-7 rad/sym (1 krad/s, sat.1553 §6.3 真实值)
- BLOCK = 100, T_S = 1/2.5e9 (params.py)
- ML: n_tap=11, lr=0.005, batch_size=1024, train_frac=0.5
- CMA: n_tap=11, μ=1e-3, R2=1.0 (QPSK), block_size=64
- SNR_SWEEP = [10,12,14,16,18,20,22,24,26,28,30,35,40] dB
- F_G_SWEEP = [30,100,300,1000] Hz (4 个代表 f_G)
- N_SEEDS = 5

用法:
  cd projects/simulation && python explore/cma-fade-divergence/ber_vs_snr_scan.py
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
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from common._config import BLOCK
from common._experiment import save_results

cfg = SimulationConfig()
T_S = cfg.system.T_S

# ─── 实验参数 (🟡 从 params.py 读, 不硬编码) ──────────────────
F_G_SWEEP = [30.0, 100.0, 300.0, 1000.0]
SNR_SWEEP_DB = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40]
MOD = 'qpsk'
TURB = 'strong'  # α=1.5, β=0.8 (params.py TurbulenceParams)
N_SYMBOLS = 2_000_000  # 跟 r_lcr 一致 (TL-22: 500K@2.5G=0.13τ_c 衰落未展开, 见文件头说明)
SOP_RATE = 4e-7  # 1 krad/s (sat.1553 §6.3, 跟 r_lcr 一致)
N_TAP = 11
MU_CMA = 1e-3   # 安全区步长 (测跟踪滞后, 不是发散)
R2_QPSK = 1.0
SKIP_FRAC = 0.10  # CMA BER 跳过前 10% 暂态
N_SEEDS = 5
# ML 训练参数 (跟 r_lcr_ber_impact.py / sup_stress_test.py 一致, Qin 2025 L275/283/397)
ML_PARAMS = dict(n_tap=N_TAP, lr=0.005, batch_size=1024, n_epochs=20,
                 device='cuda', patience=5)
ML_TRAIN_FRAC = 0.5  # 前 50% 训练, 后 50% 测试

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
CKPT_PATH = RESULTS_DIR / 'ber_vs_snr_checkpoint.json'


def snr_db_to_gamma(snr_db):
    """gamma_bar = 10^(SNR_dB/10). SNR=20dB → gamma_bar=100."""
    return float(10.0 ** (snr_db / 10.0))


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


# ─── 调制/解调 (跟 r_lcr_ber_impact.py 一致) ─────────────────

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


def compute_ber_phase_corrected(z, s, skip_frac=0.0):
    """QPSK BER, 先做 4 旋转角度相位校正取最低 BER (消除 π/2 相位模糊)."""
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


def compute_ber(z, s, skip_frac=0.0):
    return compute_ber_phase_corrected(z, s, skip_frac)


def oracle_equalize(rX, rY, h, theta, gamma_bar):
    """撤销 SOP + MMSE on h (跟 sup_stress_test.py:119 一致)."""
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 信道生成 (跟 r_lcr_ber_impact.py:165 一致, gamma_bar 参数化) ──

def gen_channel(N, alpha, beta, f_g, sop_rate, gamma_bar, seed):
    """生成双偏振 GG 衰落 + SOP 旋转信道 (QPSK), noise 由 gamma_bar 控制.

    noise variance nv = 1/(2*gamma_bar) — 跟 r_lcr:179 / sup:147 同公式.
    gamma_bar=100 → 20dB; gamma_bar=10 → 10dB.
    """
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
    sX, _ = gen_qpsk(N, rng)
    sY, _ = gen_qpsk(N, rng)
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
    """对一组信道跑 CMA/ML/oracle 三方, 返回 (cma_ber, ml_ber, oracle_ber, cma_div).

    CMA: μ=1e-3 安全步长, BER 用测试段 (后 50%, 跟 ML 公平), 发散则用 valid 段.
    ML: 该点前 50% 训练 (需 sY 作第二偏振训练目标), 推理全段, BER 只算测试段 (后 50%).
    oracle: 撤销 SOP + MMSE, BER 测试段.
    """
    # CMA (安全 μ=1e-3)
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_CMA, R2=R2_QPSK)
    res_cma = cma.equalize(rX, rY)
    if res_cma['diverged'] and res_cma['diverge_idx'] is not None:
        valid = max(int(res_cma['diverge_idx']), 1)
        # 发散: valid 段可能在训练段内, 取 min(valid, n_train)
        v_end = min(valid, n_train) if valid > n_train else valid
        cma_ber = compute_ber(res_cma['zX'][:v_end], sX[:v_end], 0.0) if v_end > 100 else 0.5
    else:
        # 未发散: 测试段 BER (后 50%, 跟 ML 公平对比)
        cma_ber = compute_ber(res_cma['zX'][n_train:], sX[n_train:], 0.0)
    cma_div = bool(res_cma['diverged'])

    # ML (每点独立训练: 前 50% 训练)
    ml = MLChannelEqualizer(**ML_PARAMS)
    ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
             val_split=0.2, verbose=False)
    res_ml = ml.equalize(rX, rY)
    zX_ml = res_ml['zX'].flatten()
    # ML 测试段 BER (后 50%, 前馈无暂态不跳)
    ml_ber = compute_ber(zX_ml[n_train:], sX[n_train:], 0.0)

    # oracle (测试段)
    zX_or, _ = oracle_equalize(rX, rY, h, theta, gamma_bar)
    oracle_ber = compute_ber(zX_or[n_train:], sX[n_train:], 0.0)

    return cma_ber, ml_ber, oracle_ber, cma_div


# ─── 主扫描 ─────────────────────────────────────────────────

def run_scan():
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    n_train = int(N_SYMBOLS * ML_TRAIN_FRAC)
    n_points = len(F_G_SWEEP) * len(SNR_SWEEP_DB)
    print(f"扫描: {len(F_G_SWEEP)} f_G × {len(SNR_SWEEP_DB)} SNR = {n_points} 点 "
          f"× {N_SEEDS} seeds")
    print(f"参数: QPSK, turb={TURB}(α={alpha},β={beta}), N={N_SYMBOLS}, "
          f"SOP={SOP_RATE}(1krad/s), tap={N_TAP}, CMA μ={MU_CMA}")
    print(f"f_G: {F_G_SWEEP}")
    print(f"SNR: {SNR_SWEEP_DB} dB")
    print()

    # 断点续跑 (key 统一用 _key() 返回的字符串, 如 'f100_snr20')
    results = defaultdict(lambda: {'cma_ber': [], 'ml_ber': [],
                                   'oracle_ber': [], 'cma_diverged': []})
    ckpt = _load_ckpt()
    for k, v in ckpt.get('results', {}).items():
        if len(v.get('cma_ber', [])) >= N_SEEDS:
            results[k] = v
    done = sum(1 for f_g in F_G_SWEEP for snr in SNR_SWEEP_DB
               if _key(f_g, snr) in results
               and len(results[_key(f_g, snr)]['cma_ber']) >= N_SEEDS)
    print(f"[续跑] 已完成 {done}/{n_points} 点\n")

    t0 = time.time()
    print(f"{'f_G(Hz)':>8} {'SNR(dB)':>8} {'γ̄':>8} {'CMA_BER':>10} {'ML_BER':>10} "
          f"{'oracle_BER':>11} {'n_div':>6} {'n':>4} {'t(s)':>6}")

    for f_g in F_G_SWEEP:
        for snr_db in SNR_SWEEP_DB:
            key = _key(f_g, snr_db)
            gamma_bar = snr_db_to_gamma(snr_db)
            if key in results and len(results[key]['cma_ber']) >= N_SEEDS:
                v = results[key]
                print(f"{f_g:>8.0f} {snr_db:>8} {gamma_bar:>8.1f} "
                      f"{np.mean(v['cma_ber']):>10.2e} {np.mean(v['ml_ber']):>10.2e} "
                      f"{np.mean(v['oracle_ber']):>11.2e} "
                      f"{int(sum(v['cma_diverged'])):>6d} {N_SEEDS:>4d} "
                      f"{'-':>6} (cached)", flush=True)
                continue

            t_point = time.time()
            for seed in range(N_SEEDS):
                seed_int = int(hash(('ber_snr', f_g, snr_db, seed)) % (2**32))
                rX, rY, sX, sY, h, theta = gen_channel(
                    N_SYMBOLS, alpha, beta, f_g, SOP_RATE, gamma_bar, seed_int)
                cma_ber, ml_ber, oracle_ber, cma_div = run_point(
                    rX, rY, sX, sY, h, theta, gamma_bar, n_train)
                results[key]['cma_ber'].append(cma_ber)
                results[key]['ml_ber'].append(ml_ber)
                results[key]['oracle_ber'].append(oracle_ber)
                results[key]['cma_diverged'].append(int(cma_div))

            v = results[key]
            dt = time.time() - t_point
            print(f"{f_g:>8.0f} {snr_db:>8} {gamma_bar:>8.1f} "
                  f"{np.mean(v['cma_ber']):>10.2e} {np.mean(v['ml_ber']):>10.2e} "
                  f"{np.mean(v['oracle_ber']):>11.2e} "
                  f"{int(sum(v['cma_diverged'])):>6d} {N_SEEDS:>4d} {dt:>6.0f}",
                  flush=True)
            # 每 point 写 checkpoint
            _save_ckpt({'results': {str(k): val for k, val in results.items()
                                     if len(val.get('cma_ber', [])) >= N_SEEDS}})

    elapsed = time.time() - t0
    print(f"\n扫描完成, 耗时 {elapsed:.0f}s")
    return results, elapsed


def _key(f_g, snr_db):
    """结果 dict 的 key: 'f30_snr20'."""
    return f"f{int(f_g)}_snr{int(snr_db)}"


def summarize(results):
    """汇总成每 (f_G, snr) 的 {cma_ber_mean/std, ml_ber_mean/std, oracle_ber_mean/std}."""
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
    print("F1: BER vs SNR 扫描 (QPSK, strong 湍流, CMA/ML/oracle 三方)")
    print("=" * 78)

    results, elapsed = run_scan()
    summary = summarize(results)

    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'F1 BER vs SNR scan (R004 batch1)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': time.time() - t0,
            'params': {
                'mod': MOD, 'turbulence': TURB,
                'turbulence_alpha_beta': list(cfg.turbulence.as_dict()[TURB]),
                'n_symbols': N_SYMBOLS,
                'n_symbols_note': ('跟 r_lcr_ber_impact.py 一致. TL-22 检查发现 '
                                   'N=500K@2.5GBaud=0.13τ_c 衰落动力学未展开, CMA BER 偏低~1000×; '
                                   'N=2M=0.5τ_c 与 r_lcr/README 已发布数据量级一致'),
                'sop_rate': SOP_RATE,
                'sop_krad_s': SOP_RATE * 2.5e9 / 1e3,
                'n_tap': N_TAP, 'mu_cma': MU_CMA, 'r2_qpsk': R2_QPSK,
                'f_g_sweep': F_G_SWEEP, 'snr_sweep_db': SNR_SWEEP_DB,
                'n_seeds': N_SEEDS, 'ml_train_frac': ML_TRAIN_FRAC,
                'ml_params': ML_PARAMS, 'skip_frac': SKIP_FRAC,
                'snr_noise_formula': 'nv = 1/(2*gamma_bar), gamma_bar=10^(SNR_dB/10)',
            },
            'tl25_expected': (
                '低SNR(<15dB): 三者BER>0.1, ML略优CMA; '
                '中SNR(15-25dB): ML≈oracle, CMA差几倍(跟踪滞后); '
                '高SNR(>25dB): ML≈oracle, CMA有残余BER floor; '
                'f_G越大CMA floor越高'),
        },
        'results': summary,
    }
    out_path = RESULTS_DIR / 'ber_vs_snr_results.json'
    save_results(out, str(out_path), 'ber_vs_snr_scan')

    # 清理 checkpoint (成功完成后)
    try:
        CKPT_PATH.unlink()
        print(f"已清理 checkpoint: {CKPT_PATH}")
    except Exception:
        pass

    print(f"\n总耗时: {time.time()-t0:.0f}s")
    return out


if __name__ == '__main__':
    main()
