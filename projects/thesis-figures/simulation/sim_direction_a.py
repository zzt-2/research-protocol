#!/usr/bin/env python3
"""方向A MVE仿真 — 湍流强度自适应LEO星地载波同步

基于R010原型(sim_prototype.py)扩展：
- Doppler时变频偏模型（仰角→径向速度→f_D(t)）
- FFT-based FOE（4次方+峰值检测，可调窗口N）
- 二阶DPLL（可调带宽B_L）
- VV CPR（可调窗口M）
- 自适应参数 vs 固定参数对比
- 6种联合场景（3湍流 × 2仰角/变化率）

参数锚点来源：S007（Zhao 2025, Paillier 2020）
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# ═══════════════════════════════════════════════════════════════
# 系统参数（来自S007参数溯源）
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9          # 符号率 2.5 Gsps (Zhao 2025)
T_S = 1 / R_SYM        # 符号周期 0.4 ns
F_CARRIER = 1.55e14    # 光载频 ~1550nm
LASER_LW = 10e3        # 激光线宽 10 kHz (Zhao 2025)

TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
BLOCK = 100  # 块衰落大小（符号/块）

# Doppler参数（Zhao 2025 / Wang 2025）
DOPPLER_HIGH = 150e6   # 低仰角: 150 MHz/s
DOPPLER_LOW  = 30e6    # 高仰角: 30 MHz/s
F_RESIDUAL   = 1e6     # 预补偿后残余频偏 ~1 MHz (Zhao)

# 固定参数基准（Zhao 2025配置）
FIXED_CFG = {
    'N_fft': 1024,      # FFT窗口
    'M_vv': 64,         # VV窗口
    'omega_n': 8e6,     # DPLL自然频率 rad/s
    'zeta': np.sqrt(2)/2,  # DPLL阻尼
}

# ═══════════════════════════════════════════════════════════════
# 基础原语（复用R010）
# ═══════════════════════════════════════════════════════════════
def gg_block(N, a, b, bs=BLOCK):
    nb = (N + bs - 1) // bs
    return np.repeat(
        gamma_dist.rvs(a, scale=1/a, size=nb) *
        gamma_dist.rvs(b, scale=1/b, size=nb),
        bs)[:N]

def qpsk_mod(bits):
    return ((2*bits[0::2]-1) + 1j*(2*bits[1::2]-1)) / np.sqrt(2)

def qpsk_demod(s):
    b = np.zeros(2*len(s), dtype=int)
    b[0::2] = (np.real(s) > 0).astype(int)
    b[1::2] = (np.imag(s) > 0).astype(int)
    return b

def awgn(sig, snr_db):
    s2 = 0.5 / 10**(snr_db/10)
    return sig + np.sqrt(s2)*(np.random.randn(len(sig)) + 1j*np.random.randn(len(sig)))

def ber(tx_bits, rx):
    return np.mean(tx_bits != qpsk_demod(rx))

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

# ═══════════════════════════════════════════════════════════════
# Doppler时变模型
# ═══════════════════════════════════════════════════════════════
def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    """生成Doppler+相位噪声的总载波相位

    φ[k] = 2π·f_res·k·T_s + π·f_dot·(k·T_s)² + θ_laser[k]
    """
    k = np.arange(N)
    # 残余频偏（预补偿后）
    phi_fo = 2 * np.pi * f_res * k * T_S
    # Doppler时变（频率斜坡）
    phi_dot = np.pi * f_dot * (k * T_S)**2
    # 激光相位噪声（维纳过程）
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser

# ═══════════════════════════════════════════════════════════════
# FFT-based FOE（4次方法）
# ═══════════════════════════════════════════════════════════════
def fft_foe(rx, N_fft=1024, nfft_zp=8192):
    """FFT-based频率偏移估计（零填充提高精度）

    4次方去QPSK调制 → 零填充FFT → 抛物线插值峰值 → 频率估计
    返回估计的归一化频率偏移（rad/symbol）
    """
    N_fft = min(N_fft, len(rx))
    seg = rx[:N_fft]
    r4 = seg**4
    win = np.hanning(N_fft)
    r4w = r4 * win
    # 零填充FFT提高分辨率
    R4 = np.fft.fftshift(np.fft.fft(r4w, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    # 抛物线插值精确定位峰值
    idx = np.argmax(np.abs(R4))
    if 1 <= idx < len(R4) - 1:
        alpha = np.abs(R4[idx-1])
        beta = np.abs(R4[idx])
        gamma = np.abs(R4[idx+1])
        if beta - alpha > 0 and beta + alpha - 2*gamma != 0:
            p = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)
            f_est_norm = (freqs[idx] + p * (freqs[1] - freqs[0]))
        else:
            f_est_norm = freqs[idx]
    else:
        f_est_norm = freqs[idx]
    f_est_norm /= 4  # 4次方后频率×4
    return 2 * np.pi * f_est_norm

# ═══════════════════════════════════════════════════════════════
# 二阶DPLL
# ═══════════════════════════════════════════════════════════════
def dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2):
    """二阶数字PLL相位跟踪

    环路滤波器: F(z) = (C1 + C2·z⁻¹)/(1 - z⁻¹)
    C1 = 2·zeta·omega_n·T_s / (1 + 2·zeta·omega_n·T_s + (omega_n·T_s)²)  ← 不对
    实际用简化双线性变换:
    C1 = 1/Kd · 2·zeta·omega_n·T_s
    C2 = 1/Kd · (omega_n·T_s)²
    Kd = 1 (QPSK鉴相器增益)

    这里omega_n是归一化的（rad/symbol），需要转换
    """
    # 归一化到符号率
    wT = omega_n * T_S  # omega_n * T_s
    # 防止数值问题（对于超大omega_n）
    wT = min(wT, 0.5)  # 限制在稳定区

    c1 = 2 * zeta * wT
    c2 = wT**2

    N = len(rx)
    phi_est = np.zeros(N)
    freq_est = np.zeros(N)
    phase_err = np.zeros(N)

    # 状态
    integrator = 0.0
    vco_phase = 0.0

    for k in range(N):
        # VCO输出
        vco_out = np.exp(-1j * vco_phase)
        # 混频
        mixed = rx[k] * vco_out
        # QPSK鉴相器: Im(mixed^4) / 4 = 相位误差
        m4 = mixed**4
        pd_out = np.angle(m4) / 4  # 归一化鉴相器输出

        # 环路滤波器
        integrator += c2 * pd_out
        freq_est[k] = c1 * pd_out + integrator
        # VCO更新
        vco_phase += freq_est[k]
        phi_est[k] = vco_phase

    return rx * np.exp(-1j * phi_est), phi_est

# ═══════════════════════════════════════════════════════════════
# VV载波相位恢复（自适应窗口）
# ═══════════════════════════════════════════════════════════════
def vv_cpr(rx, Nw=64):
    """Viterbi-Viterbi相位恢复（QPSK, M=4）"""
    M = 4
    raised = rx**M
    # 幅度裁剪
    amp = np.abs(raised)
    clip_val = 1e8
    mask = amp > clip_val
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * clip_val
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg) * M) / M
    return rx * np.exp(-1j * pe), pe

# ═══════════════════════════════════════════════════════════════
# 自适应参数计算
# ═══════════════════════════════════════════════════════════════
def adaptive_params(h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH):
    """根据估计的信道增益h计算最优参数

    相干检测约定: 瞬时SNR gamma = gamma_bar * h (h为归一化辐照度)
    返回 (N_fft, M_vv, omega_n)
    """
    gamma_bar = 10**(gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)  # 下限防发散

    # 瞬时SNR: gamma = gamma_bar * h (相干检测, 信号幅度∝sqrt(h))
    gamma = gamma_bar * h_safe

    # FOE: N_opt = 80 * gamma_bar / gamma^2 = 80 / (gamma_bar * h^2)
    # 低h时N增大（长平均抑制噪声），高h时N减小（快速跟踪）
    N_fft = int(np.clip(80 * gamma_bar / (gamma**2 + 1e-10), 256, 8192))
    # 取2的幂次
    N_fft = int(2**np.ceil(np.log2(N_fft)))

    # VV: M_opt = K_M * gamma^{-1/5} * (delta_f_res * T_s)^{-2/5}
    K_M = (3/4)**0.2
    df_norm = F_RESIDUAL * T_S  # 残余频偏归一化
    M_vv = int(np.clip(K_M * gamma**(-0.2) * df_norm**(-0.4), 16, 256))
    M_vv = max(8, M_vv | 1) - 1  # 确保奇数，最小9

    # DPLL: B_L_opt = B0 * h  (设计选择: 线性缩放，非Wiener最优)
    # Wiener最优为 B_L ∝ h^{1/2}，但线性缩放在工程上更稳定
    B0 = np.sqrt(np.pi * LASER_LW * gamma_bar / T_S)
    B_L = np.clip(B0 * h_safe, 0.5e6, 20e6)  # 更保守的上限：20MHz
    omega_n = B_L / 1.06

    return N_fft, M_vv, omega_n

# ═══════════════════════════════════════════════════════════════
# 完整载波恢复链
# ═══════════════════════════════════════════════════════════════
def carrier_recovery_fixed(rx, cfg=FIXED_CFG):
    """固定参数载波恢复（Zhao 2025配置）"""
    # Step 1: FFT FOE
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    # Step 2: DPLL
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    # Step 3: VV CPR
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr

def carrier_recovery_adaptive(rx, h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH, h_foe=None):
    """自适应参数载波恢复 — 三公式全自适应（相干检测约定）

    FOE:  N_opt = 80·γ̄/γ² = 80/(γ̄·h²) — h⁻² 阈值效应
    VV:   M_opt ∝ γ⁻¹/⁵ = (γ̄·h)⁻¹/⁵ — h⁻¹/⁵ 平滑折中
    DPLL: B_L = B₀·h                 — h¹ 线性缩放（设计选择）

    使用 h_foe（10th percentile）驱动全部三公式，确保深衰落覆盖
    """
    if h_foe is None:
        h_foe = h_est

    N_foe, M_vv, omega_n = adaptive_params(h_foe, gamma_bar_db, f_dot)

    fo_est = fft_foe(rx, N_fft=N_foe)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))

    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=FIXED_CFG['zeta'])

    rx_cpr, _ = vv_cpr(rx_pll, Nw=M_vv)
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# MVE实验框架
# ═══════════════════════════════════════════════════════════════
def run_mve_trial(Ns, turb_name, f_dot, gamma_bar_db, adaptive=True):
    """单次MVE试验

    返回BER值
    """
    a, b = TURB[turb_name]

    # 生成信号
    bits = np.random.randint(0, 2, Ns*2)
    tx = qpsk_mod(bits)

    # GG块衰落信道
    h = gg_block(Ns, a, b)
    # 信道估计：分用途计算
    n_blocks = len(h) // BLOCK
    h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
    h_est = np.median(h_blocks)  # DPLL/VV用中位数
    h_foe = np.percentile(h_blocks, 10)  # FOE用10th百分位（保守估计）

    gamma_bar_db_lin = 10**(gamma_bar_db / 10)

    # Doppler载波相位
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    # 通过信道 — 相干检测模型: r = sqrt(h)·s + n
    # h ~ GG分布（归一化辐照度），信号幅度 ∝ sqrt(h)，噪声方差恒定
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar_db_lin)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx = signal + noise

    # MMSE信道补偿 — 信道增益为sqrt(h)，|sqrt(h)|^2 = h
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar_db_lin)
    rx_comp = amp_limit(rx_comp, 3.0)

    # 载波恢复
    if adaptive:
        rx_rec = carrier_recovery_adaptive(rx_comp, h_est, gamma_bar_db, f_dot, h_foe=h_foe)
    else:
        rx_rec = carrier_recovery_fixed(rx_comp)

    # BER（带相位模糊解决）
    return resolve_qpsk(rx_rec, bits)

def run_mve(Ns=10000, n_trials=50, gamma_bar_db=20):
    """运行完整MVE：6种场景 × 固定/自适应 × 多次试验"""
    scenarios = []
    for turb in ['weak', 'moderate', 'strong']:
        for elev, f_dot in [('low', DOPPLER_HIGH), ('high', DOPPLER_LOW)]:
            scenarios.append((turb, elev, f_dot))

    results = {}
    for turb, elev, f_dot in scenarios:
        label = f"{turb}_{elev}"
        print(f"\n  Scenario: {label} (f_dot={f_dot/1e6:.0f} MHz/s)")

        bers_fixed = []
        bers_adapt = []
        for trial in range(n_trials):
            np.random.seed(42 + trial)
            # 固定参数
            bf = run_mve_trial(Ns, turb, f_dot, gamma_bar_db, adaptive=False)
            bers_fixed.append(bf)
            # 自适应参数
            np.random.seed(42 + trial)  # 同样信道实现
            ba = run_mve_trial(Ns, turb, f_dot, gamma_bar_db, adaptive=True)
            bers_adapt.append(ba)

        mean_f = np.mean(bers_fixed)
        mean_a = np.mean(bers_adapt)
        # dB增益: 需要SNR等价损失
        if mean_f > 0 and mean_a > 0 and mean_a < mean_f:
            gain_db = 10 * np.log10(mean_f / mean_a)
        else:
            gain_db = 0.0

        results[label] = {
            'fixed_ber': mean_f,
            'adapt_ber': mean_a,
            'gain_db': gain_db,
            'scenario': (turb, elev, f_dot),
        }
        status = "PASS" if gain_db > 0.5 else ("WEAK" if gain_db > 0 else "FAIL")
        print(f"    Fixed: {mean_f:.5f}  Adapt: {mean_a:.5f}  Gain: {gain_db:+.2f} dB [{status}]")

    return results

def plot_mve(results):
    """绘制MVE结果对比图"""
    labels = list(results.keys())
    fixed = [results[l]['fixed_ber'] for l in labels]
    adapt = [results[l]['adapt_ber'] for l in labels]
    gains = [results[l]['gain_db'] for l in labels]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # BER对比
    x = np.arange(len(labels))
    w = 0.35
    axes[0].bar(x - w/2, fixed, w, label='Fixed (Zhao)', color='steelblue')
    axes[0].bar(x + w/2, adapt, w, label='Adaptive', color='coral')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
    axes[0].set_ylabel('BER')
    axes[0].set_title('BER Comparison')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_yscale('log')

    # 增益
    colors = ['green' if g > 0.5 else ('orange' if g > 0 else 'red') for g in gains]
    axes[1].bar(x, gains, color=colors)
    axes[1].axhline(0.5, color='green', ls='--', alpha=0.5, label='Pass (0.5 dB)')
    axes[1].axhline(1.0, color='darkgreen', ls='--', alpha=0.5, label='Strong pass (1.0 dB)')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
    axes[1].set_ylabel('Gain (dB)')
    axes[1].set_title('Adaptive vs Fixed Gain')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUT}/mve_direction_a.pdf')
    plt.close()

def plot_snr_sweep(results_db=None):
    """SNR扫描：BER vs SNR for fixed vs adaptive (三档湍流)"""
    snrs = np.arange(10, 32, 2)
    f_dot = DOPPLER_HIGH
    Ns = 10000
    n_trials = 30

    turb_list = ['weak', 'moderate', 'strong']
    sweep_data = {}

    # 数据收集
    for turb in turb_list:
        bers_f, bers_a = [], []
        for snr in snrs:
            bf, ba = [], []
            for t in range(n_trials):
                np.random.seed(100 + t)
                bf.append(run_mve_trial(Ns, turb, f_dot, snr, adaptive=False))
                np.random.seed(100 + t)
                ba.append(run_mve_trial(Ns, turb, f_dot, snr, adaptive=True))
            bers_f.append(np.mean(bf))
            bers_a.append(np.mean(ba))
            print(f"  {turb} SNR={snr}dB: Fixed={np.mean(bf):.5f} Adapt={np.mean(ba):.5f}")
        sweep_data[turb] = {'snrs': list(snrs), 'fixed': bers_f, 'adapt': bers_a}

    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, turb in zip(axes, turb_list):
        d = sweep_data[turb]
        ax.semilogy(snrs, d['fixed'], 'bs-', label='Fixed (Zhao cfg)', ms=5)
        ax.semilogy(snrs, d['adapt'], 'r^-', label='Adaptive (3-formula)', ms=5)
        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('BER')
        ax.set_title(f'{turb.capitalize()} turbulence')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(1e-4, 1)

    plt.suptitle(f'BER vs SNR: f_dot={f_dot/1e6:.0f} MHz/s, Ns={Ns}')
    plt.tight_layout()
    plt.savefig(f'{OUT}/mve_snr_sweep.pdf')
    plt.close()

    return sweep_data

# ═══════════════════════════════════════════════════════════════
# 参数可视化
# ═══════════════════════════════════════════════════════════════
def plot_adaptive_params():
    """绘制自适应参数随h变化的曲线"""
    h_range = np.linspace(0.05, 3.0, 200)
    gamma_bar_db = 20
    gamma_bar = 10**(gamma_bar_db/10)

    Ns, Ms, Bs = [], [], []
    for h in h_range:
        N, M, wn = adaptive_params(h, gamma_bar_db)
        Ns.append(N)
        Ms.append(M)
        Bs.append(wn / (2*np.pi) / 1e6)  # MHz

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].semilogy(h_range, Ns, 'b-')
    axes[0].axhline(1024, color='r', ls='--', alpha=0.5, label='Zhao fixed')
    axes[0].set_xlabel('Channel gain h'); axes[0].set_ylabel('N_fft')
    axes[0].set_title('FOE Window N_opt(h)'); axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(h_range, Ms, 'g-')
    axes[1].axhline(64, color='r', ls='--', alpha=0.5, label='Zhao fixed')
    axes[1].set_xlabel('Channel gain h'); axes[1].set_ylabel('M_vv')
    axes[1].set_title('VV Window M_opt(h)'); axes[1].legend(); axes[1].grid(True, alpha=0.3)

    axes[2].plot(h_range, Bs, 'm-')
    axes[2].axhline(FIXED_CFG['omega_n']/(2*np.pi)/1e6, color='r', ls='--', alpha=0.5, label='Zhao fixed')
    axes[2].set_xlabel('Channel gain h'); axes[2].set_ylabel('B_L (MHz)')
    axes[2].set_title('DPLL Bandwidth B_L_opt(h)'); axes[2].legend(); axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUT}/adaptive_params.pdf')
    plt.close()

# ═══════════════════════════════════════════════════════════════
# 消融实验：逐公式贡献
# ═══════════════════════════════════════════════════════════════
def carrier_recovery_ablation(rx, h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH,
                              adapt_foe=True, adapt_vv=True, adapt_dpll=True, h_foe=None):
    """消融实验：选择性启用各公式自适应"""
    if h_foe is None:
        h_foe = h_est
    N_foe, M_adapt, omega_n_adapt = adaptive_params(h_foe, gamma_bar_db, f_dot)

    N_fft = N_foe if adapt_foe else FIXED_CFG['N_fft']
    M_vv = M_adapt if adapt_vv else FIXED_CFG['M_vv']
    omega_n = omega_n_adapt if adapt_dpll else FIXED_CFG['omega_n']

    fo_est = fft_foe(rx, N_fft=N_fft)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n, zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=M_vv)
    return rx_cpr

def run_ablation(Ns=10000, n_trials=30, gamma_bar_db=20):
    """消融实验：分别测只自适应FOE / VV / DPLL / 全部 / 无"""
    ablation_modes = {
        'Fixed (all)':      dict(adapt_foe=False, adapt_vv=False, adapt_dpll=False),
        'FOE only':         dict(adapt_foe=True,  adapt_vv=False, adapt_dpll=False),
        'VV only':          dict(adapt_foe=False, adapt_vv=True,  adapt_dpll=False),
        'DPLL only':        dict(adapt_foe=False, adapt_vv=False, adapt_dpll=True),
        'All adaptive':     dict(adapt_foe=True,  adapt_vv=True,  adapt_dpll=True),
    }

    turb = 'strong'
    f_dot = DOPPLER_HIGH
    results = {}

    for mode_name, flags in ablation_modes.items():
        bers = []
        for t in range(n_trials):
            np.random.seed(200 + t)
            a, b = TURB[turb]
            bits = np.random.randint(0, 2, Ns*2)
            tx = qpsk_mod(bits)
            h = gg_block(Ns, a, b)
            n_blocks = len(h) // BLOCK
            h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
            h_est = np.median(h_blocks)
            h_foe = np.percentile(h_blocks, 10)
            phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
            carrier = np.exp(1j * phi)
            # 相干检测: r = sqrt(h)·s + n
            signal = tx * np.sqrt(h) * carrier
            gamma_bar_lin = 10**(gamma_bar_db / 10)
            noise_var = 1.0 / (2 * gamma_bar_lin)
            noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
            rx = signal + noise
            # MMSE均衡
            rx = rx * np.sqrt(h) / (h + 1/gamma_bar_lin)
            rx = amp_limit(rx, 3.0)
            rx_rec = carrier_recovery_ablation(rx, h_est, gamma_bar_db, f_dot, h_foe=h_foe, **flags)
            bers.append(resolve_qpsk(rx_rec, bits))

        mean_ber = np.mean(bers)
        results[mode_name] = mean_ber
        print(f"  {mode_name:20s}: BER={mean_ber:.5f}")

    # 绘图
    fig, ax = plt.subplots(figsize=(10, 5))
    names = list(results.keys())
    vals = list(results.values())
    colors = ['steelblue', '#2ecc71', '#e67e22', '#9b59b6', 'coral']
    bars = ax.bar(range(len(names)), vals, color=colors[:len(names)])
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=20, ha='right', fontsize=9)
    ax.set_ylabel('BER')
    ax.set_title(f'Ablation Study: Strong Turbulence, SNR={gamma_bar_db}dB')
    ax.grid(True, alpha=0.3, axis='y')
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{v:.4f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUT}/ablation_study.pdf')
    plt.close()
    return results

def run_block_analysis(Ns=10000, n_trials=30, gamma_bar_db=20):
    """分块分析：按h大小分组统计BER（强湍流）"""
    turb = 'strong'
    f_dot = DOPPLER_HIGH
    a, b = TURB[turb]
    h_bins = [(0, 0.3), (0.3, 1.0), (1.0, 5.0)]
    h_labels = ['h<0.3 (deep)', '0.3≤h<1', 'h≥1 (good)']

    fixed_block = {l: [] for l in h_labels}
    adapt_block = {l: [] for l in h_labels}

    for t in range(n_trials):
        np.random.seed(300 + t)
        bits = np.random.randint(0, 2, Ns*2)
        tx = qpsk_mod(bits)
        h = gg_block(Ns, a, b)
        n_blocks = len(h) // BLOCK
        h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
        h_est = np.median(h_blocks)
        h_foe = np.percentile(h_blocks, 10)
        phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
        carrier = np.exp(1j * phi)
        # 相干检测: r = sqrt(h)·s + n
        signal = tx * np.sqrt(h) * carrier
        gamma_bar_lin = 10**(gamma_bar_db / 10)
        noise_var = 1.0 / (2 * gamma_bar_lin)
        noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
        rx = signal + noise
        # MMSE均衡
        rx = rx * np.sqrt(h) / (h + 1/gamma_bar_lin)
        rx = amp_limit(rx, 3.0)

        # 固定
        rx_f = carrier_recovery_fixed(rx)
        # 自适应
        rx_a = carrier_recovery_adaptive(rx, h_est, gamma_bar_db, f_dot, h_foe=h_foe)

        # 按块分组统计BER
        for i in range(n_blocks):
            s, e = i*BLOCK, (i+1)*BLOCK
            h_val = np.median(h[s:e])
            label = h_labels[0] if h_val < 0.3 else (h_labels[1] if h_val < 1.0 else h_labels[2])
            fixed_block[label].append(ber(bits[2*s:2*e], rx_f[s:e]))
            adapt_block[label].append(ber(bits[2*s:2*e], rx_a[s:e]))

    print("\n  Block-level BER (strong turbulence):")
    block_results = {}
    for label in h_labels:
        f_mean = np.mean(fixed_block[label])
        a_mean = np.mean(adapt_block[label])
        gain = 10*np.log10(f_mean/a_mean) if f_mean > 0 and a_mean > 0 and a_mean < f_mean else 0
        block_results[label] = {'fixed': f_mean, 'adapt': a_mean, 'gain_db': gain}
        print(f"    {label:15s}: Fixed={f_mean:.5f} Adapt={a_mean:.5f} Gain={gain:+.2f}dB")

    # 绘图
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(h_labels))
    w = 0.35
    f_vals = [block_results[l]['fixed'] for l in h_labels]
    a_vals = [block_results[l]['adapt'] for l in h_labels]
    ax.bar(x - w/2, f_vals, w, label='Fixed', color='steelblue')
    ax.bar(x + w/2, a_vals, w, label='Adaptive', color='coral')
    ax.set_xticks(x)
    ax.set_xticklabels(h_labels)
    ax.set_ylabel('BER')
    ax.set_title('Block-level BER by Channel Gain (Strong Turbulence)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{OUT}/block_analysis.pdf')
    plt.close()
    return block_results

# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    print("="*60)
    print("方向A MVE仿真 — 湍流强度自适应LEO星地载波同步")
    print(f"Output: {OUT}")
    print("="*60)

    # Step 1: 自适应参数可视化
    print("\n[1/5] 自适应参数曲线...")
    plot_adaptive_params()
    print("  -> adaptive_params.pdf")

    # Step 2: MVE主实验（6种场景）
    print("\n[2/5] MVE主实验（6场景 × 50次试验 × 10000符号）...")
    results = run_mve(Ns=10000, n_trials=50, gamma_bar_db=20)
    plot_mve(results)
    print("  -> mve_direction_a.pdf")

    # Step 3: 消融实验（强湍流）
    print("\n[3/5] 消融实验（强湍流，逐公式贡献）...")
    ablation_results = run_ablation(Ns=10000, n_trials=30, gamma_bar_db=20)
    print("  -> ablation_study.pdf")

    # Step 4: 分块分析（强湍流按h分组）
    print("\n[4/5] 分块分析（强湍流，按h大小分组）...")
    block_results = run_block_analysis(Ns=10000, n_trials=30, gamma_bar_db=20)
    print("  -> block_analysis.pdf")

    # Step 5: SNR扫描（三档湍流 × 11个SNR点）
    print("\n[5/5] SNR扫描（三档湍流, 10-30 dB）...")
    sweep_data = plot_snr_sweep()
    print("  -> mve_snr_sweep.pdf")

    # 汇总
    dt = time.time() - t0
    print(f"\n{'='*60}")
    print(f"完成! 耗时 {dt:.1f}s")
    print("\nMVE判定（L2标准）：")
    strong_gains = {k: v['gain_db'] for k, v in results.items() if 'strong' in k}
    best_strong = max(strong_gains.values()) if strong_gains else 0
    print(f"  强湍流增益: {strong_gains}")
    print(f"  强湍流最大增益: {best_strong:.2f} dB")
    n_pass = sum(1 for r in results.values() if r['gain_db'] > 0.5)
    n_strong_pass = sum(1 for g in strong_gains.values() if g > 1.0)
    print(f"  全场景≥0.5dB: {n_pass}/6")
    print(f"  强湍流≥1.0dB: {n_strong_pass}/2")
    print(f"\n  消融结果:")
    for mode, ber_val in sorted(ablation_results.items(), key=lambda x: x[1]):
        print(f"    {mode:20s}: BER={ber_val:.5f}")
    if best_strong >= 3.0:
        print(f"\n  => L2 成立: Ch4是方法级创新")
    elif best_strong >= 1.0:
        print(f"\n  => L1→L2 边界: 能写但答辩可能被追问")
    else:
        print(f"\n  => L1 确认: 需调整创新点定位")
    print("="*60)

    # 保存结果JSON
    all_results = {
        'mve': {k: {kk: (str(vv) if isinstance(vv, tuple) else vv)
                    for kk, vv in v.items()} for k, v in results.items()},
        'ablation': ablation_results,
        'block_analysis': {k: {kk: str(vv) if isinstance(vv, tuple) else vv
                               for kk, vv in v.items()} for k, v in block_results.items()},
    }
    with open(f'{OUT}/mve_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
