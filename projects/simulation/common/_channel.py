"""信道模型：Gamma-Gamma 衰落 + 多普勒相位"""
import numpy as np
from scipy.stats import gamma as gamma_dist

from ._config import BLOCK, TURB, F_RESIDUAL, DOPPLER_HIGH, LASER_LW, T_S
from ._modulation import qpsk_mod, apsk8_mod, m16apsk_mod


def gg_block(N, a, b, bs=BLOCK):
    nb = (N + bs - 1) // bs
    return np.repeat(
        gamma_dist.rvs(a, scale=1/a, size=nb) *
        gamma_dist.rvs(b, scale=1/b, size=nb),
        bs)[:N]


def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    k = np.arange(N)
    phi_fo = 2 * np.pi * f_res * k * T_S
    phi_dot = np.pi * f_dot * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser


def generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed=42):
    """
    生成单次信道/噪声/相位实现，所有方案共享。

    Returns:
        dict: rx_raw, bits, tx, h, h_blocks, h_med, phi,
              Ns, gamma_bar, turb_name, f_dot
    """
    np.random.seed(seed)
    a, b = TURB[turb_name]

    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    h = gg_block(Ns, a, b)
    n_blocks = Ns // BLOCK
    h_blocks = np.array([h[i * BLOCK] for i in range(n_blocks)])
    h_med = np.median(h_blocks)

    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_raw = signal + noise

    return {
        'rx_raw': rx_raw, 'bits': bits, 'tx': tx,
        'h': h, 'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
        'Ns': Ns, 'gamma_bar': gamma_bar,
        'turb_name': turb_name, 'f_dot': f_dot,
    }


def generate_shared_realization_apsk(
    Ns, gamma_bar, turb_name, f_dot, mod='m16apsk', seed=42,
):
    """M-APSK 调制版信道实现（B11 NDA-ML STO+CPE / B7 Gardner TED FOE MVE 共用）。

    与 ``generate_shared_realization`` 共用同一 Gamma-Gamma 块衰落 + 多普勒/线宽相位
    实现（守 TL-13：B11/B7/B3 必须共用同一信道实现，禁自建），仅调制方式可换。

    参数
    ----
    Ns : int
        符号数。
    gamma_bar : float
        平均 SNR（线性）。
    turb_name : str
        'weak' / 'moderate' / 'strong'（来自 TURB）。
    f_dot : float
        多普勒变化率（Hz/s）。
    mod : str
        'm16apsk' (默认, B11 锚 (8,8)-16APSK) / 'apsk8' (8PSK) / 'qpsk'。
    seed : int
        随机种子（可复现）。

    返回
    ----
    dict: 与 ``generate_shared_realization`` 同构，新增 ``clw`` / ``fec_threshold``
          字段（来自 B11 参数族，默认 CLW=500 kHz / HD-FEC=7%，供 BER/FEC 评估标记）。
          rx_raw 已含 ``signal = tx * sqrt(h) * carrier`` 相干约定（TL-01）。
    """
    np.random.seed(seed)
    a, b = TURB[turb_name]

    # 调制（守 TL-13：与 generate_shared_realization 共用同一信道实现）
    if mod == 'qpsk':
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
    elif mod == 'apsk8':
        bits = np.random.randint(0, 2, Ns * 3)
        tx = apsk8_mod(bits)
    elif mod == 'm16apsk':
        bits = np.random.randint(0, 2, Ns * 4)
        tx = m16apsk_mod(bits)
    else:
        raise ValueError(f"Unknown mod: {mod} (expected 'qpsk'/'apsk8'/'m16apsk')")

    h = gg_block(Ns, a, b)
    n_blocks = Ns // BLOCK
    h_blocks = np.array([h[i * BLOCK] for i in range(n_blocks)])
    h_med = np.median(h_blocks)

    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_raw = signal + noise

    return {
        'rx_raw': rx_raw, 'bits': bits, 'tx': tx,
        'h': h, 'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
        'Ns': Ns, 'gamma_bar': gamma_bar,
        'turb_name': turb_name, 'f_dot': f_dot,
        'mod': mod,
    }
