"""A3 §4a 维度 D MVE — 信道生成模块。

信号模型（Paillier 2020 §III，TL-01 锁定）：
    s_RX(k) = sqrt(rho(k)) * exp(j*(doppler(k) + phi_AO(k) + mod_phase(k))) + n(k)

A3 攻击点（TL-22 红线）：deep fade 瞬态（rho(k) 骤降）→ 瞬态 SNR 跌破 PLL critical SNR →
相位估计方差暴增。不是 AO 残留活塞相位（那是 B1 死因）。

保真度声明（FR-04）：Gamma-Gamma 块衰落近似 Paillier TURANDOT 波动光学（35 层相位屏）。
保留核心结构：deep fade 瞬态 / 块间相位跳变 / 多普勒残余频偏。省略 AO 闭环动态（用静态 GG）。
"""
import numpy as np
from scipy.stats import gamma as gamma_dist

# ═══════════════════════════════════════════════════════════════
# 信道参数
# ═══════════════════════════════════════════════════════════════
# Gamma-Gamma 湍流参数（alpha, beta）—— 归一化均值 1，σ²_I = 1/(ab)+1/a+1/b 对标 Paillier §IV-C
# _find_gg_params.py 解析校准：weak σ²_I≈0.1 / moderate≈0.3 / strong≈0.684（Paillier 目标）
# 注：lasercomms 文献常写 α=1.5,β=0.8 是另一套参数化（不同归一化），这里用 σ²_I 直接对标
TURB = {
    'weak':     (12.0, 12.0),   # σ²_I ≈ 0.097
    'moderate': (7.0, 7.0),     # σ²_I ≈ 0.306
    'strong':   (3.4, 3.3),     # σ²_I ≈ 0.686 ≈ Paillier 0.684
}

BLOCK = 64          # 块衰落尺寸（symbol 数）—— Paillier 相干时间量级
F_RESIDUAL = 100e6  # 多普勒残余频偏 100 MHz（Paillier §IV-C）
T_S = 1e-9          # symbol 时间 1 ns（~1 Gbaud，Paillier 10 Gbaud 的简化）
LASER_LW = 1e3      # 激光线宽 1 kHz（相干检测典型，远小于多普勒）
# AO 残余活塞相位等效线宽（Paillier §IV-A/B 主导损伤）。
# AO 校正后残余 piston 抖动等效一个相位 Wiener 过程。
# **文献依据（Paillier 2020 §II verified）**：相干时间 τ_c ~ 1 ms（"of the order of 1 ms"）。
# Wiener 过程 τ_c = 1/(2π·Δν) → Δν ≈ 159 Hz（strong）。
# 三档对应湍流强度（强湍流 AO 校正残余更大 → τ_c 更短）：
#   weak: τ_c=10ms → Δν=16Hz；moderate: τ_c=3ms → 53Hz；strong: τ_c=1ms → 159Hz。
# 历史教训：初版误用 30k/100k/300k Hz（大 188-1885x），致 MVE 虚高，已修正。
AO_RESIDUAL_LW = {
    'weak':     16,      # τ_c ≈ 10 ms（AO 校正好，残余小且慢）
    'moderate': 53,      # τ_c ≈ 3 ms
    'strong':   159,     # τ_c ≈ 1 ms（对标 Paillier Fig.4 实测）
}


def gg_block(N, a, b, bs=BLOCK):
    """Gamma-Gamma 块衰落幅度 h = sqrt(I)，I ~ Gamma(a)*Gamma(b) 归一化到均值 1。

    返回 h（幅度，非强度），块内常数。
    """
    nb = (N + bs - 1) // bs
    I = gamma_dist.rvs(a, scale=1.0/a, size=nb) * gamma_dist.rvs(b, scale=1.0/b, size=nb)
    h = np.sqrt(np.repeat(I, bs)[:N])   # 幅度 sqrt(I)
    return h


def ao_residual_phase(N, lw_ao, ts=T_S):
    """AO 校正后残余活塞相位（Wiener 过程，Paillier §IV-A/B 主导损伤）。

    phi_ao = sqrt(2π lw_ao T) * cumsum(randn)
    lw_ao: AO 残余等效线宽（Hz），远大于激光线宽 1kHz。
    这是 A3 攻击的相位损伤源——deep fade 瞬态下此相位估计方差暴增。
    """
    return np.sqrt(2 * np.pi * lw_ao * ts) * np.cumsum(np.random.randn(N))


def doppler_phase(N, f_res=F_RESIDUAL, f_dot=0.0, lw=LASER_LW, ts=T_S):
    """多普勒残余频偏 + 线宽 Wiener 相位。

    phi_fo = 2π f_res k T  （线性频偏 → 相位累积）
    phi_laser = sqrt(2π lw T) * cumsum(randn)  （Wiener 相位噪声）
    返回相位序列（弧度）。
    """
    k = np.arange(N)
    phi_fo = 2 * np.pi * f_res * k * ts
    phi_laser = np.sqrt(2 * np.pi * lw * ts) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_laser


def qpsk_mod(bits):
    """QPSK 调制（标准 4 点 π/4 偏置星座），归一化到单位平均符号功率 Es=1。

    4 个点 (±1±1j)/√2，角度 ±π/4, ±3π/4。|s|²=1。
    bits[0::2]=I 路比特，bits[1::2]=Q 路比特。
    """
    return ((2*bits[0::2]-1) + 1j*(2*bits[1::2]-1)) / np.sqrt(2)


def qpsk_demod(s):
    """QPSK 解调，与 mod 的 (±1±1j)/√2 星座匹配（Re>0/Im>0 判象限）。"""
    b = np.zeros(2*len(s), dtype=int)
    b[0::2] = (np.real(s) > 0).astype(int)
    b[1::2] = (np.imag(s) > 0).astype(int)
    return b


def generate_shared_realization(Ns, gamma_bar_db, turb_name, seed=42, with_pilot_header=False, frame_len=64):
    """生成单次信道/噪声/相位/比特实现，所有方法共享（TL-25 #1 强制）。

    Args:
        Ns: symbol 数
        gamma_bar_db: 平均 SNR (dB)，γ=Es/N0
        turb_name: 'weak'/'moderate'/'strong'
        seed: 随机种子
        with_pilot_header: 是否在 bit 流中预留 frame-header pilot（M1a 用）
        frame_len: frame length（M1a 用，pilot 1 header/frame）

    Returns:
        dict: tx, tx_pilot, pilot_idx, bits, data_bits, h, phi_doppler,
              noise, rx_raw, gamma_bar, turb_name, seed, Ns, frame_len
    """
    np.random.seed(seed)
    a, b = TURB[turb_name]
    gamma_bar = 10 ** (gamma_bar_db / 10)

    # 比特流：QPSK 每 symbol 2 bit
    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    # M1a frame-header pilot：每 frame_len 个 symbol，第 1 个是 pilot（已知 BPSK 训练）
    # pilot 用全 1+1j 序列（已知），data 是剩余 symbol
    pilot_idx = None
    tx_pilot = None
    data_bits_mask = np.ones(Ns, dtype=bool)
    if with_pilot_header:
        pilot_idx = np.arange(0, Ns, frame_len)   # 每 frame 第 1 symbol 是 pilot
        data_bits_mask[pilot_idx] = False
        # pilot symbol = (1+1j)/sqrt2，已知
        tx_pilot = np.ones(len(pilot_idx), dtype=complex) * (1+1j)/np.sqrt(2)
        # 把 pilot 写入 tx 对应位置
        tx[pilot_idx] = (1+1j)/np.sqrt(2)

    # 信道
    h = gg_block(Ns, a, b)                          # 幅度块衰落
    phi_doppler = doppler_phase(Ns)                 # 多普勒 + 激光线宽相位（可忽略）
    phi_ao = ao_residual_phase(Ns, AO_RESIDUAL_LW[turb_name])  # AO 残余活塞相位（主导损伤）

    # 接收信号：sqrt(h) * tx * exp(j*phi) + noise
    # 总相位 phi = phi_doppler（多普勒+激光线宽）+ phi_ao（AO 残余，主导）
    phi_total = phi_doppler + phi_ao
    # SNR 定义 γ = Es/N0 = (平均信号功率)/(噪声单边功率谱密度)
    # 噪声方差 σ² = 1/γ（自洽惯例，N1 MVE bug1 教训：不用 1/(2γ)）
    carrier = np.exp(1j * phi_total)
    signal = h * tx * carrier                        # sqrt(I) * tx * exp(j phi)
    noise_var = 1.0 / gamma_bar
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns)) / np.sqrt(2)
    # 除以 sqrt(2) 使每复数噪声方差 = noise_var（复噪声 = N(0,σ²) 实+虚各 σ²/2 → |n|² 期望 σ²）
    rx_raw = signal + noise

    return {
        'tx': tx, 'tx_pilot': tx_pilot, 'pilot_idx': pilot_idx,
        'data_bits_mask': data_bits_mask,
        'bits': bits, 'h': h,
        'phi_doppler': phi_doppler, 'phi_ao': phi_ao, 'phi_total': phi_total,
        'noise': noise, 'rx_raw': rx_raw,
        'gamma_bar': gamma_bar, 'gamma_bar_db': gamma_bar_db,
        'turb_name': turb_name, 'seed': seed, 'Ns': Ns, 'frame_len': frame_len,
        'ao_lw': AO_RESIDUAL_LW[turb_name],
    }


def ber_count(tx_symbols, rx_symbols, data_mask=None, resolve_ambiguity=True):
    """计算 BER（QPSK）。data_mask 指定哪些 symbol 是 data（排除 pilot）。

    resolve_ambiguity: True 则试 4 个 π/2 旋转取最小 BER（解 CPE 残留的 QPSK 整体相位模糊）。
        M2/M3/M4 等 CPE 方法输出可能整体转 π/2 整数倍，不解模糊会判错。
        M1 pilot CPE 有绝对参考，理论上不需——但保险起见也开。
    """
    if data_mask is not None:
        tx_d = tx_symbols[data_mask]
        rx_d = rx_symbols[data_mask]
    else:
        tx_d, rx_d = tx_symbols, rx_symbols
    # 反推 tx bits
    tx_bits = np.zeros(2*len(tx_d), dtype=int)
    tx_bits[0::2] = (np.real(tx_d) > 0).astype(int)
    tx_bits[1::2] = (np.imag(tx_d) > 0).astype(int)
    if resolve_ambiguity:
        best = 1.0
        for r in [0, np.pi/2, np.pi, 3*np.pi/2]:
            rx_bits = qpsk_demod(rx_d * np.exp(-1j*r))
            b = np.mean(tx_bits != rx_bits)
            if b < best:
                best = b
        return best
    else:
        rx_bits = qpsk_demod(rx_d)
        return np.mean(tx_bits != rx_bits)


if __name__ == '__main__':
    # 自检：σ²_I 量级
    np.random.seed(0)
    N = 100000
    for name, (a, b) in TURB.items():
        I = gamma_dist.rvs(a, scale=1.0/a, size=N//BLOCK) * gamma_dist.rvs(b, scale=1.0/b, size=N//BLOCK)
        sigma2_I = np.var(I) / (np.mean(I)**2)
        print(f"{name}: σ²_I = {sigma2_I:.3f}")
