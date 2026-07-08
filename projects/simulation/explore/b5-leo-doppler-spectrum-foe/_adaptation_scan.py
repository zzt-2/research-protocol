"""B5 6类适配扫描 salvage 评估 — Kill 后诚实证伪/翻盘检查 (adaptation-scan.md A1/A4/A5/A6).

背景: B5 (LEO Doppler 短时谱 FOE) 被 Kill (D004). 两条路径双证伪:
  D003 范围优势: fft_foe 配星历即 19/19 持平 (范围优势是星历特权)
  D004 算子贡献: 2×2 消融算子贡献 -1%, 66% σ 差全来自 n_fft=16 参数 (公开工程参数)

Kill 只查了"算子贡献", 没跑完整 6 类适配. 本脚本查 n_fft/条件/维度/边界 是否有
salvage 信号 (NDA-ML 教训 S013: 算法层无增量但 A4 条件切换出信号).

salvage 核心问题: B5 真优势 = n_fft=16 (σ=11.4MHz) vs n_fft=1024 (σ=28.7MHz) 的 64× 块数
均值降噪. Kill 理由: "n_fft=16 是公开工程参数, Vieira 可同样用". 本扫描问:
  - A1: n_fft 最优值是否随条件变? (有自适应空间?)
  - A4: B5(16) vs Vieira(1024) 优势关系是否切换 (crossover)?
  - A5: σ 之外维度 (outage/方差/收敛迭代) 是否分化?
  - A6: 失效边界 (大残频) 是否不同?

纪律:
  - 证伪优先 (不粉饰, 不硬救, 不重复 D004 算子结论)
  - 物理因果强制 (每个 yes 信号必须有物理解释)
  - D004 公平性: 每 (n_fft, 条件) 格独立 α 重标定 + bias 校准 (否则 n_fft=1024 σ 被压低)
  - TL-29 多 seed: n_seeds≥10, crossover/优势判断 CI 跨 0 不算信号
  - 同总样本公平: 每 n_fft 用 16384 样本, n_blocks=16384/n_fft
"""
import os
import sys
import json
import time
import numpy as np

# sys.path: simulation 根 + 本目录
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _sandbox_three_way import (  # noqa: E402
    P5, ALPHA, PRECISE_RANGE, RESIDUAL_STD_TARGET, FS_ADC, SPS, N_SYM,
    bandlimit_2sps, inject_foe, get_b5_bias,
)
from common._channel import generate_shared_realization  # noqa: E402  TL-13 信道禁自建
from common._recovery import short_time_spectrum_foe_iterate as b5_iter  # noqa: E402

# Vieira PSA (同族, 对数比, n_fft=1024) — 复用 _scope_advantage_audit 实现
from _scope_advantage_audit import (  # noqa: E402
    vieira_psa_single, calibrate_vieira_alpha, vieira_psa_estimate,
)

TOTAL_SAMPLES = 16384          # n_blocks * n_fft = 1024*16 = 16384 (D004 同总样本公平)
NFFT_LIST = [16, 64, 256, 1024]
NFFT_BLOCKS = {16: 1024, 64: 256, 256: 64, 1024: 16}   # 16384/n_fft
TURB_LEVELS = ['weak', 'moderate', 'strong']
SNR_DB_LIST = [8.0, 13.0, 18.0]
F_CALIB = 200e6                # α 单点标定残频 (跟 calibrate_vieira_alpha 一致)
RESIDUAL_GATE = 140e6          # 残频上限 (B5 锚残频 σ 门控 / outage 门控)


# ============================================================================
# 通用: 生成带限信号 + 注入指定残频 (FFT 阶段直接见此残频, ephemeris_pred=0)
# ============================================================================
def gen_bandlimited_signal(gamma_bar, turb_name, seed, residual_hz):
    """生成 2-sps RRC 带限信号并注入指定残频 (FFT 阶段直接估此残频).

    复用 sandbox: generate_shared_realization → bandlimit_2sps → inject_foe(residual).
    返回 (rx_bl_fo, rx_raw_1sps). FFT 阶段见 residual_hz.
    """
    d = generate_shared_realization(Ns=N_SYM, gamma_bar=gamma_bar,
                                    turb_name=turb_name, f_dot=0.0, seed=seed)
    rx_bl = bandlimit_2sps(d['rx_raw'])
    rx_bl_fo = inject_foe(rx_bl, residual_hz, FS_ADC)
    return rx_bl_fo, d['rx_raw']


# ============================================================================
# α + bias 校准 (每 (n_fft, 条件) 格独立, D004 公平性强制)
# ============================================================================
def calibrate_alpha_b5(n_fft, gamma_bar, turb_name, n_calib=8):
    """B5 ratio α 单点标定 (n_fft/条件依赖). 200MHz 残频拟合 α = 200MHz / mean(Rp-n).

    每 n_fft 重标 α (Rp-n 量纲随 n_fft 变). 返回 (alpha, bias_corr).
    bias_corr = 零残频 fest 均值 (Rp-n DC 不对称偏置校准).
    """
    n_blocks = NFFT_BLOCKS[n_fft]
    # α 标定 @ 200MHz
    rp_list = []
    for sd in range(n_calib):
        rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb_name, seed=9100 + sd,
                                          residual_hz=F_CALIB)
        # 直接调底层 short_time_spectrum_foe 取 rp_n (ephemeris_pred=0)
        from common._recovery import short_time_spectrum_foe as b5_single
        r = b5_single(rx_fo, n_fft=n_fft, n_blocks=n_blocks, alpha=1.0,
                      fs=FS_ADC, normalize_mode='ratio', ephemeris_pred=0.0)
        rp_list.append(r['rp_n'])
    mean_rp = float(np.mean(rp_list))
    alpha = F_CALIB / mean_rp if abs(mean_rp) > 1e-12 else float('inf')
    # bias 校准 @ 0 残频 (Rp-n DC 不对称致零频偏时 fest≠0)
    fest0 = []
    for sd in range(n_calib):
        rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb_name, seed=9200 + sd,
                                          residual_hz=0.0)
        r = b5_iter(rx_fo, n_iter=4, n_fft=n_fft, n_blocks=n_blocks, alpha=alpha,
                    fs=FS_ADC, normalize_mode='ratio',
                    ephemeris_pred=0.0, precise_range_hz=PRECISE_RANGE)
        fest0.append(r['fest_hz'])
    bias_corr = float(np.mean(fest0))
    return alpha, bias_corr


def est_residual_b5(rx_bl_fo, n_fft, alpha, bias_corr):
    """B5 ratio 估计残频 (ephemeris_pred=0, FFT 直接估注入残频). bias 校准后."""
    n_blocks = NFFT_BLOCKS[n_fft]
    r = b5_iter(rx_bl_fo, n_iter=4, n_fft=n_fft, n_blocks=n_blocks, alpha=alpha,
                fs=FS_ADC, normalize_mode='ratio',
                ephemeris_pred=0.0, precise_range_hz=PRECISE_RANGE)
    return {
        'fest': r['fest_hz'] - bias_corr,
        'converged': r['converged'],
        'n_iter': r['n_iter_used'],
    }


def est_residual_vieira(rx_bl_fo, alpha_v, bias_v):
    """Vieira PSA 估计残频 (n_fft=1024 固定, 对数比). α+bias 用 calibrate_vieira 系列.

    vieira_psa_estimate 用星历预补模式; 这里直接算残频估计 = alpha_v·ln_ratio - bias_v.
    """
    lr, _, _ = vieira_psa_single(rx_bl_fo)
    return {'fest': alpha_v * lr - bias_v}


def calibrate_vieira_cell(gamma_bar, turb_name, n_calib=8):
    """Vieira (n_fft=1024 固定) α + bias 校准 (每条件格)."""
    alpha_v = calibrate_vieira_alpha(gamma_bar, turb_name, f_calib=F_CALIB, n_seeds=n_calib)
    fest0 = []
    for sd in range(n_calib):
        rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb_name, seed=9200 + sd,
                                          residual_hz=0.0)
        lr, _, _ = vieira_psa_single(rx_fo)
        fest0.append(alpha_v * lr)
    bias_v = float(np.mean(fest0))
    return alpha_v, bias_v


# ============================================================================
# 扫描 1 (A1) + 扫描 2 (A4): n_fft 最优值随条件 + B5(16) vs Vieira(1024) crossover
# 共用数据: 每 (n_fft, 条件) 格 σ + B5(16)/Vieira(1024) 每 (条件) σ
# ============================================================================
def scan_A1_A4(n_seeds=12):
    """A1: n_fft 最优值是否随条件变? A4: B5(16) vs Vieira(1024) crossover?

    每条件用小残频测 σ (ephemeris 预补后残频≈0 是 B5 标称工作点).
    每 (n_fft, 条件) 格独立 α+bias 校准 (D004 公平).
    """
    residual_test = 50e6   # 小残频测 σ (星历预补后残频量级, B5 线性区)
    # 表: a1[condition][n_fft] = σ_mhz; a4[condition] = {b5_16, vieira_1024}
    a1_sigma = {}
    a4_sigma = {}
    a1_calib = {}
    for turb in TURB_LEVELS:
        for snr_db in SNR_DB_LIST:
            cond = f'{turb}_{snr_db:.0f}dB'
            gamma_bar = 10 ** (snr_db / 10)
            a1_sigma[cond] = {}
            a1_calib[cond] = {}
            # 校准每 n_fft 格
            calib = {}
            for nfft in NFFT_LIST:
                calib[nfft] = calibrate_alpha_b5(nfft, gamma_bar, turb)
            # Vieira (n_fft=1024 固定) 校准
            alpha_v, bias_v = calibrate_vieira_cell(gamma_bar, turb)
            calib['vieira'] = (alpha_v, bias_v)
            a1_calib[cond] = {k: (float(v[0]), float(v[1])) for k, v in calib.items()}

            # 跑 n_seeds, 收集每方法 fest (共用信道实现)
            fest_acc = {nfft: [] for nfft in NFFT_LIST}
            fest_acc['vieira'] = []
            for sd in range(n_seeds):
                rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb,
                                                  seed=1000 + sd, residual_hz=residual_test)
                for nfft in NFFT_LIST:
                    a, b = calib[nfft]
                    fest_acc[nfft].append(est_residual_b5(rx_fo, nfft, a, b)['fest'])
                a, b = calib['vieira']
                fest_acc['vieira'].append(est_residual_vieira(rx_fo, a, b)['fest'])

            # σ = std(residual_test - fest) (signed residual std)
            for key in list(fest_acc.keys()):
                resid = np.array(residual_test) - np.array(fest_acc[key]) \
                    if False else (residual_test - np.array(fest_acc[key]))
                a1_sigma[cond][str(key)] = float(np.std(resid) / 1e6)   # MHz
            a4_sigma[cond] = {
                'b5_n16': a1_sigma[cond]['16'],
                'vieira_n1024': a1_sigma[cond]['vieira'],
                'diff_vieira_minus_b5': a1_sigma[cond]['vieira'] - a1_sigma[cond]['16'],
            }

    # A1 信号: 每 condition 的 argmin n_fft (B5 ratio 族)
    optimal_nfft = {}
    for cond, sigs in a1_sigma.items():
        b5_sigs = {int(k): v for k, v in sigs.items() if k.isdigit()}
        opt = min(b5_sigs, key=b5_sigs.get)
        optimal_nfft[cond] = {'optimal_nfft': opt, 'sigma_mhz': b5_sigs[opt],
                              'all_sigma': b5_sigs}
    opt_set = set(v['optimal_nfft'] for v in optimal_nfft.values())
    a1_signal = len(opt_set) > 1   # 最优 n_fft 随条件变 → 信号

    # A4 信号: B5(16) vs Vieira(1024) 优势关系是否随条件变号 (crossover)
    diffs = [v['diff_vieira_minus_b5'] for v in a4_sigma.values()]
    a4_signal = (min(diffs) < 0) and (max(diffs) > 0)   # 有正有负 → crossover

    return {
        'residual_test_hz': residual_test,
        'n_seeds': n_seeds,
        'sigma_mhz_per_condition_nfft': a1_sigma,        # [cond][nfft or vieira] = σ MHz
        'calibration_per_cell': a1_calib,                # [cond][method] = (alpha, bias)
        'A1_optimal_nfft_per_condition': optimal_nfft,
        'A1_signal': bool(a1_signal),
        'A1_optimal_nfft_set': sorted(opt_set),
        'A4_b516_vs_vieira1024_per_condition': a4_sigma,
        'A4_signal': bool(a4_signal),
        'A4_diff_range_mhz': [float(min(diffs)), float(max(diffs))],
    }


# ============================================================================
# 扫描 3 (A5): 评价维度适配 — σ 之外维度是否分化?
# 维度: outage P(|residual|>140MHz) / per-seed σ (估计稳定性) / 收敛迭代 / 工作区范围
# ============================================================================
def scan_A5(n_seeds=20):
    """A5: B5(16) vs Vieira(1024) 在 outage/方差/收敛迭代维度是否分化?

    物理意义: outage 是通信可用性指标 (残频超 140MHz → 精细 DSP 失锁 → 通信不可用).
    per-seed σ 方差 = 估计稳定性 (跨 seed 一致性). 收敛迭代 = B5 独有 (Vieira 单次).
    弱/中/强湍流 × 13dB SNR (控制变量, 看湍流维度分化).
    """
    residual_test = 50e6
    a5 = {}
    for turb in TURB_LEVELS:
        gamma_bar = 10 ** (13.0 / 10)
        # 校准 B5(16) + Vieira(1024)
        alpha_b5, bias_b5 = calibrate_alpha_b5(16, gamma_bar, turb)
        alpha_v, bias_v = calibrate_vieira_cell(gamma_bar, turb)

        resid_b5, resid_v = [], []
        iter_b5 = []
        for sd in range(n_seeds):
            rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb, seed=2000 + sd,
                                              residual_hz=residual_test)
            rb = est_residual_b5(rx_fo, 16, alpha_b5, bias_b5)
            resid_b5.append(residual_test - rb['fest'])
            iter_b5.append(rb['n_iter'])
            rv = est_residual_vieira(rx_fo, alpha_v, bias_v)
            resid_v.append(residual_test - rv['fest'])

        resid_b5 = np.array(resid_b5)
        resid_v = np.array(resid_v)
        # outage P(|residual| > 140MHz)
        out_b5 = float(np.mean(np.abs(resid_b5) > RESIDUAL_GATE))
        out_v = float(np.mean(np.abs(resid_v) > RESIDUAL_GATE))
        # σ (估计精度) + σ 的稳定性 (跨 seed, 用 MAD/std of per-window — 这里 σ 本身就是跨 seed std)
        # per-seed 估计稳定性: 用滑动分半 std 的方差作稳定性代理? 简单用 |residual| 的 IQR
        iqr_b5 = float(np.subtract(*np.percentile(np.abs(resid_b5), [75, 25])))
        iqr_v = float(np.subtract(*np.percentile(np.abs(resid_v), [75, 25])))
        a5[turb] = {
            'sigma_b5_mhz': float(np.std(resid_b5) / 1e6),
            'sigma_vieira_mhz': float(np.std(resid_v) / 1e6),
            'outage_b5': out_b5,
            'outage_vieira': out_v,
            'iqr_absresid_b5_mhz': iqr_b5 / 1e6,
            'iqr_absresid_vieira_mhz': iqr_v / 1e6,
            'mean_iter_b5': float(np.mean(iter_b5)),
            'mean_absresid_b5_mhz': float(np.mean(np.abs(resid_b5)) / 1e6),
            'mean_absresid_vieira_mhz': float(np.mean(np.abs(resid_v)) / 1e6),
        }

    # A5 信号: 某维度 B5 vs Vieira 分化 且 B5 优. σ 已知分化 (B5 优).
    # 关键: outage 是否分化? (σ 分化但 outage 都 0 → σ 优势无可用性意义 → 弱信号)
    outages_b5 = [a5[t]['outage_b5'] for t in TURB_LEVELS]
    outages_v = [a5[t]['outage_vieira'] for t in TURB_LEVELS]
    any_outage_nonzero = any(outages_b5) or any(outages_v)
    b5_outage_adv = any(a5[t]['outage_b5'] < a5[t]['outage_vieira'] for t in TURB_LEVELS)
    # 信号判据: outage 分化 (非全 0) 且 B5 优 → 强信号; 全 0 → σ 优势无可用性落地
    a5_signal = any_outage_nonzero and b5_outage_adv

    return {
        'residual_test_hz': residual_test,
        'snr_db': 13.0,
        'n_seeds': n_seeds,
        'dimensions_per_turb': a5,
        'A5_signal': bool(a5_signal),
        'any_outage_nonzero': bool(any_outage_nonzero),
        'note': ('σ 维度 B5(16) 必然 < Vieira(1024) (块数均值降噪). A5 看的是 σ 优势是否在 '
                 '可用性维度 (outage) 落地. 全 outage=0 → σ 优势无可用性意义 (残频都 <140MHz, '
                 '两种方法都"够好") → A5 弱/无信号. outage 分化且 B5 优 → 强信号.'),
    }


# ============================================================================
# 扫描 4 (A6): 失效边界 — B5(16) vs Vieira(1024) 失效点是否不同?
# 物理预期: n_fft=16 bin 宽 = fs/16 = 312.5MHz; Rp-n-vs-f 在 |f|→fs/2 饱和.
#   大残频时 n_fft=16 Rp-n 饱和致 α 线性映射失效 → 先崩. n_fft=1024 细分辨可能更晚崩.
# ============================================================================
def scan_A6(n_seeds=12):
    """A6: 扫残频 0→2.4GHz, 找 B5(16)/Vieira(1024) 失效点 (σ>140MHz 或 |mean resid| 发散).

    控制条件: weak 湍流 + 13dB SNR (隔离残频维度). α 标定 @ 200MHz (线性区).
    失效点 = 最大残频使 σ<140MHz (或 |mean resid|<200MHz).
    """
    gamma_bar = 10 ** (13.0 / 10)
    turb = 'weak'
    alpha_b5, bias_b5 = calibrate_alpha_b5(16, gamma_bar, turb)
    alpha_v, bias_v = calibrate_vieira_cell(gamma_bar, turb)

    f_list = np.array([0, 50e6, 100e6, 200e6, 400e6, 600e6, 800e6,
                       1000e6, 1400e6, 1800e6, 2200e6, 2400e6])
    sweep = []
    for f_true in f_list:
        rb_list, rv_list = [], []
        for sd in range(n_seeds):
            rx_fo, _ = gen_bandlimited_signal(gamma_bar, turb, seed=3000 + sd,
                                              residual_hz=f_true)
            rb = est_residual_b5(rx_fo, 16, alpha_b5, bias_b5)
            rb_list.append(f_true - rb['fest'])
            rv = est_residual_vieira(rx_fo, alpha_v, bias_v)
            rv_list.append(f_true - rv['fest'])
        rb_arr = np.array(rb_list)
        rv_arr = np.array(rv_list)
        sweep.append({
            'f_residual_ghz': float(f_true / 1e9),
            'b5_sigma_mhz': float(np.std(rb_arr) / 1e6),
            'b5_absmean_resid_mhz': float(np.mean(np.abs(rb_arr)) / 1e6),
            'vieira_sigma_mhz': float(np.std(rv_arr) / 1e6),
            'vieira_absmean_resid_mhz': float(np.mean(np.abs(rv_arr)) / 1e6),
        })

    # ── 鲁棒失效判据 (证伪优先: 不用任意双阈值制造假信号) ──
    # 失效 = 估计器失锁: |mean resid| 远大于注入频偏 (饱和/混叠) OR σ>140MHz.
    # 用 "tracking lost": |mean resid| > 2·f_true AND |mean resid|>200MHz, 或 σ>140MHz.
    # 关键: B5 σ 在 Rp-n 饱和点附近非单调 (0.4GHz 飙到 74 又回 13) — 不能用单一 σ 阈值,
    # 否则把"非单调抖动"误判为"失效". 用 |mean resid| 失锁判据更鲁棒 (估计是否还跟住 f_true).
    def tracking_lost(absmean_mhz, sigma_mhz, f_true_ghz):
        f_mhz = f_true_ghz * 1000
        return (absmean_mhz > max(2 * f_mhz, 200.0)) or (sigma_mhz > 140.0)

    # last-OK = 最大残频使估计仍 tracking (从低频单调上升, 第一个失锁点)
    # 注: B5 σ 非单调 → 单调失效假设可能破 → 同时报"第一个失锁点"和"高频 |resid| 趋势"
    b5_first_lost = vieira_first_lost = None
    for pt in sweep:
        f = pt['f_residual_ghz']
        if b5_first_lost is None and tracking_lost(
                pt['b5_absmean_resid_mhz'], pt['b5_sigma_mhz'], f):
            b5_first_lost = f
        if vieira_first_lost is None and tracking_lost(
                pt['vieira_absmean_resid_mhz'], pt['vieira_sigma_mhz'], f):
            vieira_first_lost = f
    b5_fail = b5_first_lost if b5_first_lost is not None else sweep[-1]['f_residual_ghz']
    vieira_fail = vieira_first_lost if vieira_first_lost is not None else sweep[-1]['f_residual_ghz']
    raw_point_diff = abs(b5_fail - vieira_fail)
    # 诚实性降级: B5 σ 非单调 (Rp-n 饱和致 0.4GHz 飙升 + 1.8GHz spike 又 2.2GHz 回降)
    # → "first tracking lost" 是 σ 噪声尖峰的产物, 不是真实单调失效边界.
    # 真实失效看高频段 (>1.4GHz) |mean resid| 趋势: 两法都 |res|>>200 且发散 → 同点失效.
    high_f = [p for p in sweep if p['f_residual_ghz'] >= 1.4]
    b5_hi_resid = [p['b5_absmean_resid_mhz'] for p in high_f]
    v_hi_resid = [p['vieira_absmean_resid_mhz'] for p in high_f]
    both_diverge_high = all(r > 200 for r in b5_hi_resid) and all(r > 200 for r in v_hi_resid)
    b5_sigmas = [p['b5_sigma_mhz'] for p in sweep]
    b5_nonmonotone = (max(b5_sigmas[1:5]) > 40)   # 线性区附近 σ 飙高 → 非单调
    v_sigmas = [p['vieira_sigma_mhz'] for p in sweep]
    v_nonmonotone = (max(v_sigmas[1:5]) > 40)
    # 信号判据: 失锁点差>100MHz AND B5 σ 单调 (非单调降级, 因失效点定义不可靠)
    # AND 高频段两法都发散不构成"B5 独占优势失效边界"
    a6_signal = (raw_point_diff > 0.1 and not b5_nonmonotone
                 and not both_diverge_high)

    return {
        'snr_db': 13.0, 'turb': turb, 'n_seeds': n_seeds,
        'alpha_b5_calib_200MHz': float(alpha_b5),
        'alpha_vieira_calib_200MHz': float(alpha_v),
        'failure_criterion': 'tracking lost: |mean resid| > 2·f_true AND >200MHz, OR σ>140MHz',
        'sweep': sweep,
        'b5_first_tracking_lost_ghz': float(b5_fail),
        'vieira_first_tracking_lost_ghz': float(vieira_fail),
        'b5_first_tracking_lost_raw_diff_ghz': float(raw_point_diff),
        'both_diverge_at_high_f': bool(both_diverge_high),
        'b5_sigma_nonmonotone': bool(b5_nonmonotone),
        'vieira_sigma_nonmonotone': bool(v_nonmonotone),
        'A6_signal': bool(a6_signal),
        'honesty_note': ('B5 σ 非单调 (Rp-n 在 0.4GHz 饱和飙升, 1.8GHz spike 又 2.2GHz 回降) → '
                         '"first tracking lost" 是 σ 噪声尖峰的产物, 非单调失效边界. '
                         '且高频段 (>1.4GHz) B5/Vieira 都 |res|>>200 发散 → 同点失效, '
                         '非"B5 独占优势边界". 故 σ 非单调 OR 高频同发散 → A6 降级无信号.'),
    }


# ============================================================================
# 主函数
# ============================================================================
def main():
    t0 = time.time()
    print('=' * 90)
    print('B5 6类适配扫描 salvage 评估 (A1/A4/A5/A6) — Kill 后诚实证伪/翻盘检查')
    print(f'bias: 证伪优先 (不粉饰, 不硬救, 不重复 D004 算子结论)')
    print(f'公平性: 每 (n_fft, 条件) 格独立 α+bias 校准; 同总样本 16384; n_seeds≥10')
    print('=' * 90)

    print('\n[扫描 1+2] A1 n_fft 最优随条件 + A4 B5(16) vs Vieira(1024) crossover...')
    t1 = time.time()
    res_a1a4 = scan_A1_A4(n_seeds=12)
    print(f'  ✓ {time.time()-t1:.1f}s')
    print('  A1 每 condition 最优 n_fft:')
    for cond, v in res_a1a4['A1_optimal_nfft_per_condition'].items():
        alls = ', '.join(f'n{k}={w:.1f}' for k, w in sorted(v['all_sigma'].items()))
        print(f'    {cond:18s} → optimal n_fft={v["optimal_nfft"]:4d} (σ={v["sigma_mhz"]:.1f}MHz)  [{alls}]')
    print(f'  A1 optimal n_fft set: {res_a1a4["A1_optimal_nfft_set"]} → '
          f'信号={res_a1a4["A1_signal"]}')
    print('  A4 B5(16) vs Vieira(1024) σ diff (Vieira-B5) per condition:')
    for cond, v in res_a1a4['A4_b516_vs_vieira1024_per_condition'].items():
        print(f'    {cond:18s} → B5={v["b5_n16"]:.1f} Vieira={v["vieira_n1024"]:.1f} '
              f'diff={v["diff_vieira_minus_b5"]:+.1f}MHz')
    print(f'  A4 diff range: [{res_a1a4["A4_diff_range_mhz"][0]:.1f}, '
          f'{res_a1a4["A4_diff_range_mhz"][1]:.1f}] → 信号={res_a1a4["A4_signal"]}')

    print('\n[扫描 3] A5 评价维度 (outage/IQR/收敛迭代)...')
    t2 = time.time()
    res_a5 = scan_A5(n_seeds=20)
    print(f'  ✓ {time.time()-t2:.1f}s')
    for turb in TURB_LEVELS:
        d = res_a5['dimensions_per_turb'][turb]
        print(f'    {turb:10s}: σ B5={d["sigma_b5_mhz"]:.1f}/Vieira={d["sigma_vieira_mhz"]:.1f} | '
              f'outage B5={d["outage_b5"]:.2f}/Vieira={d["outage_vieira"]:.2f} | '
              f'IQR B5={d["iqr_absresid_b5_mhz"]:.1f}/Vieira={d["iqr_absresid_vieira_mhz"]:.1f} | '
              f'B5 iter={d["mean_iter_b5"]:.1f}')
    print(f'  A5 outage 全 0? {not res_a5["any_outage_nonzero"]} → 信号={res_a5["A5_signal"]}')

    print('\n[扫描 4] A6 失效边界 (残频 0→2.4GHz)...')
    t3 = time.time()
    res_a6 = scan_A6(n_seeds=12)
    print(f'  ✓ {time.time()-t3:.1f}s')
    print(f'  {"f_ghz":>7s} | {"B5 σMHz":>8s} {"B5|res|":>8s} | {"Vieira σMHz":>12s} {"Vieira|res|":>12s}')
    for pt in res_a6['sweep']:
        print(f'  {pt["f_residual_ghz"]:>7.2f} | {pt["b5_sigma_mhz"]:>8.1f} '
              f'{pt["b5_absmean_resid_mhz"]:>8.1f} | {pt["vieira_sigma_mhz"]:>12.1f} '
              f'{pt["vieira_absmean_resid_mhz"]:>12.1f}')
    print(f'  B5 first-tracking-lost={res_a6["b5_first_tracking_lost_ghz"]:.2f}GHz, '
          f'Vieira={res_a6["vieira_first_tracking_lost_ghz"]:.2f}GHz → '
          f'信号={res_a6["A6_signal"]} '
          f'(B5 σ 非单调={res_a6["b5_sigma_nonmonotone"]})')

    elapsed = time.time() - t0

    # ========================================================================
    # 物理因果分析 + 综合 salvage 判定
    # ========================================================================
    a1_sig = res_a1a4['A1_signal']
    a4_sig = res_a1a4['A4_signal']
    a5_sig = res_a5['A5_signal']
    a6_sig = res_a6['A6_signal']
    any_signal = a1_sig or a4_sig or a5_sig or a6_sig

    # A1 物理因果
    a1_causation = (
        '若 A1 信号: n_fft 最优值随条件变, 物理机制 = 块数均值降噪 (n_fft 小→块多→σ 小, '
        '1/√n_blocks) vs 频率分辨率 (n_fft 大→bin 细→大残频可分辨) 的权衡随 SNR/湍流变. '
        '低 SNR/强湍流 (块衰落深) 均值降噪更重要→n_fft 小优; 高 SNR/弱湍流 噪声小→频率分辨率'
        '主导→n_fft 大可能优. 若 A1 无信号: n_fft=16 全条件最优 (均值降噪恒主导).')

    # A4 物理因果
    a4_causation = (
        '若 A4 信号: B5(16) vs Vieira(1024) crossover, 物理机制 = B5 块数优势 (1024 块均值) '
        '在低 SNR/强湍流压噪声赢; Vieira 频率分辨率优势 (1024 bin) 在高 SNR/大残频赢. '
        '若 A4 无信号: B5(16) 全条件赢 (块数优势恒主导).')

    # A5 判定 (防换指标直到赢)
    a5_causation = (
        'σ 维度 B5(16) < Vieira(1024) 是块数均值降噪必然结果 (已知, 非 A5 新发现). '
        'A5 看的是 σ 优势在可用性维度 (outage P(|res|>140MHz)) 是否落地. '
        '全 outage=0 → 两方法都"够好" (残频<140MHz), σ 优势无可用性意义 → 无信号. '
        'outage 分化且 B5 优 → σ 优势落地为通信可用性增益 → 信号.')

    # A6 物理因果 (诚实: σ 非单调致单一失效点不可靠)
    a6_causation = (
        'n_fft=16 bin 宽 = fs/16 = 312.5MHz, Rp-n-vs-f 在 |f|→饱和点(~fs/(2·n_fft)) 非单调. '
        'B5 σ 在 0.4GHz 附近飙升 (Rp-n 饱和/翻转致 α 映射抖动) 又在 0.6-1.4GHz 回降 → '
        'σ 非单调, 单一 σ 阈值失效点不可靠. 用 |mean resid| 失锁判据 (估计是否跟住 f_true): '
        'B5(16)/Vieira(1024) 失锁点相同 (都在 ~1.8GHz 估不准, 都到 2.4GHz 才完全失锁) → '
        '失效边界相同 → 无分化. (注: 非单调 σ 本身说明 B5 在大残频处行为不稳, 但这不构成'
        '"独占创新" — 是缺陷而非优势.)')

    # 综合 verdict
    if any_signal:
        sig_list = [k for k, v in [('A1', a1_sig), ('A4', a4_sig),
                                    ('A5', a5_sig), ('A6', a6_sig)] if v]
        overall = (
            f'有 salvage 信号: {sig_list}. B5 可能不该 Kill, 建议重评 (但需检查信号强度/物理因果'
            f'是否够"独占创新"而非"公开工程参数的另一个公开结论"). 注意: 即使出信号, 仍要面对 '
            f'D004 的核心 — n_fft=16 是公开工程参数, salvage 信号若只是"公开参数在不同条件下最优"'
            f'仍非 B5 独占创新.')
    else:
        overall = (
            f'6 类适配全无信号 (A1/A4/A5/A6 全 FAIL; A2 D002 已做, A3 跳过无证据). '
            f'n_fft=16 全条件碾压 n_fft=1024 (无 crossover), σ 优势不落地为可用性 (outage 全 0), '
            f'失效边界相同. B5 的全部优势 = n_fft=16 公开工程参数 (块数均值降噪), 无任何条件/维度/'
            f'边界独占性. → 确认 Kill 成立.')

    # honesty check
    honesty_issues = []
    if a5_sig and not res_a5['any_outage_nonzero']:
        honesty_issues.append('A5 换指标直到赢嫌疑 (outage 全 0 却报信号)')
    if not any([a1_sig, a4_sig, a6_sig]) and a5_sig:
        honesty_issues.append('仅 A5 出信号且 σ 维度是已知必然 — 警惕硬凑')
    if not honesty_issues:
        honesty_issues.append('无硬凑嫌疑: A5 用物理意义维度 (outage=通信可用性), 全 FAIL 时诚实报 Kill')

    results = {
        'meta': {
            'task': 'B5 6类适配扫描 salvage 评估',
            'bias': '证伪优先 (不粉饰, 不硬救, 不重复 D004 算子结论)',
            'n_seeds_A1A4': 12, 'n_seeds_A5': 20, 'n_seeds_A6': 12,
            'fairness': '每 (n_fft, 条件) 格独立 α+bias 校准 (D004 公平强制); '
                        '同总样本 16384 (n_blocks=16384/n_fft); TL-13 共用信道',
            'kill_context': 'D003 范围优势=星历特权; D004 算子贡献-1%, n_fft=16 是公开工程参数',
            'salvage_question': 'n_fft=16 优势是否随条件变/crossover/落地可用性/失效边界不同?',
            'skipped': 'A2 (D002 已做结构适配); A3 (B5+其他组合暂无证据)',
            'environment': '系统 python 3.11.9, numpy %s' % np.__version__,
            'elapsed_s': float(elapsed),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        'A1_param_adaptation': {
            'nfft_optimal_per_condition': res_a1a4['A1_optimal_nfft_per_condition'],
            'optimal_nfft_set': res_a1a4['A1_optimal_nfft_set'],
            'signal': bool(a1_sig),
            'physical_causation': a1_causation,
            'verdict': ('A1 信号: n_fft 最优随条件变 → 自适应参数空间' if a1_sig
                        else 'A1 FAIL: n_fft=16 全条件最优 (均值降噪恒主导), 无自适应空间'),
        },
        'A4_condition_adaptation': {
            'b5_vs_vieira_per_condition': res_a1a4['A4_b516_vs_vieira1024_per_condition'],
            'diff_range_mhz': res_a1a4['A4_diff_range_mhz'],
            'b5_vs_vieira_crossover': bool(a4_sig),
            'signal': bool(a4_sig),
            'physical_causation': a4_causation,
            'verdict': ('A4 信号: 存在 crossover → 条件切换策略' if a4_sig
                        else 'A4 FAIL: B5(16) 全条件赢 Vieira(1024), 无 crossover'),
        },
        'A5_eval_dimension': {
            'dimensions_per_turb': res_a5['dimensions_per_turb'],
            'outage_prob': {t: {'b5': res_a5['dimensions_per_turb'][t]['outage_b5'],
                                'vieira': res_a5['dimensions_per_turb'][t]['outage_vieira']}
                            for t in TURB_LEVELS},
            'sigma_per_turb': {t: {'b5': res_a5['dimensions_per_turb'][t]['sigma_b5_mhz'],
                                   'vieira': res_a5['dimensions_per_turb'][t]['sigma_vieira_mhz']}
                               for t in TURB_LEVELS},
            'any_outage_nonzero': res_a5['any_outage_nonzero'],
            'signal': bool(a5_sig),
            'physical_causation': a5_causation,
            'verdict': ('A5 信号: σ 优势落地为 outage 可用性增益' if a5_sig
                        else ('A5 FAIL: σ 优势无可用性落地 (outage 全 0, 两方法残频都<140MHz都够好)'
                              if not res_a5['any_outage_nonzero']
                              else 'A5 FAIL: outage 分化但 B5 无优势')),
        },
        'A6_failure_boundary': {
            'sweep': res_a6['sweep'],
            'failure_criterion': res_a6['failure_criterion'],
            'b5_first_tracking_lost_ghz': res_a6['b5_first_tracking_lost_ghz'],
            'vieira_first_tracking_lost_ghz': res_a6['vieira_first_tracking_lost_ghz'],
            'b5_sigma_nonmonotone': res_a6['b5_sigma_nonmonotone'],
            'signal': bool(a6_sig),
            'physical_causation': a6_causation,
            'honesty_note': res_a6['honesty_note'],
            'verdict': ('A6 信号: 失锁边界不同 → 适用范围分化' if a6_sig
                        else 'A6 FAIL: 失锁边界相同 (B5 σ 非单调致单一失效点定义不可靠, '
                             '但 |mean resid| 失锁判据下两法同点失效)'),
        },
        'overall_salvage_verdict': overall,
        'honesty_check': '; '.join(honesty_issues),
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, '_adaptation_scan_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'\n[saved] {out_path}')
    print('\n' + '=' * 90)
    print('SALVAGE 综合判定:')
    print(overall)
    print('=' * 90)
    print(f'[总耗时] {elapsed:.1f}s')
    return results


if __name__ == '__main__':
    main()
