"""多望远镜信道扩展（⑤，INVARIANT 14）。

从 common/_channel.py 单支路扩展，不进 common（TL-13/INVARIANT 8）。

jphot 信道模型（L101/L243）:
- 各支路独立 Gamma-Gamma 块衰落（不同望远镜收到独立衰落）
- 共享 LO → 共享频偏/Doppler/CPE 相位（jphot-L101 "same LO is shared"）
- 各支路独立 AWGN
- 各支路时延可不同（FS 对齐用）

分集条件（Fried 参数，对话 3 计算）:
- 强湍 Cn2=1e-14, z=10km, λ=1550nm: r0 ≈ 2cm
- 间距 > r0 即独立分集；强湍下极易满足（>2cm）
- 弱湍 r0 ≈ 31cm，需较大间距

守 TL-13: 单支路（n_branches=1）极限退化到 common generate_shared_realization。
"""
import os
import sys

import numpy as np

# 守 TL-13: 从 common 导入信道组件，不自建
_SIM_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common._channel import gg_block, doppler_phase  # noqa: E402
from common._config import BLOCK, TURB, T_S  # noqa: E402
from common._modulation import qpsk_mod  # noqa: E402


def _fried_parameter(lam: float, cn2: float, z: float) -> float:
    """Fried 参数 r0（平面波，垂直传播）。

    r0 = 0.185 * (lam^2 / (cn2 * z))^(3/5)
    用于判独立分集条件（间距 > r0 才独立）。
    """
    return 0.185 * (lam**2 / (cn2 * z)) ** (3 / 5)


def _are_branches_independent(aperture_spacing_m: float, cn2: float,
                              z_km: float, lam: float = 1550e-9) -> bool:
    """判断多望远镜间距是否 > Fried 参数（独立分集条件）。"""
    z = z_km * 1e3
    r0 = _fried_parameter(lam, cn2, z)
    return aperture_spacing_m > r0


def generate_multi_aperture_realization(
    n_branches: int,
    Ns: int,
    gamma_bar: float,
    turb_name: str,
    f_dot: float,
    aperture_spacing_m: float = 0.05,
    seed: int = 42,
    lw: float = 50e3,
    f_res: float = 1e6,
    cn2: float = 1e-14,
    z_km: float = 10.0,
):
    """多望远镜信道实现（INVARIANT 14，从 common 单支路扩展，不进 common）。

    Args:
        n_branches: 支路数（望远镜数）
        Ns: 符号数
        gamma_bar: 平均 SNR（线性）
        turb_name: 'weak'/'moderate'/'strong'（来自 TURB）
        f_dot: Doppler 变化率（Hz/s）
        aperture_spacing_m: 望远镜间距（> 空间相干长度才独立分集）
        seed: 随机种子
        lw: 激光线宽（Hz）
        f_res: 残余频偏（Hz）
        cn2: 折射率结构常数（判分集条件用）
        z_km: 链路距离（km，判分集条件用）

    Returns:
        dict: {branches, h_branches, phi_shared, tx, bits, ...}
    实现:
        - 各支路独立 Gamma-Gamma 块衰落（若间距 > r0）或相关（若 < r0）
        - 共享 LO → 共享频偏/Doppler/CPE 相位（jphot-L101）
        - 各支路独立 AWGN + 支路间固定时延偏移（FS 对齐用）
        - 守 TL-13: 单支路极限退化到 common generate_shared_realization
    """
    rng = np.random.RandomState(seed)
    a, b = TURB[turb_name]

    bits = rng.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    # 共享 LO → 共享相位（频偏/Doppler/线宽，jphot-L101）
    # 用固定 seed 生成共享相位，保证各支路载波一致
    rng_phi = np.random.RandomState(seed + 100000)
    lw_noise = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(rng_phi.randn(Ns))
    k = np.arange(Ns)
    phi_shared = (2 * np.pi * f_res * k * T_S
                  + np.pi * f_dot * (k * T_S) ** 2
                  + lw_noise)
    carrier = np.exp(1j * phi_shared)

    # 分集条件
    independent = _are_branches_independent(aperture_spacing_m, cn2, z_km)

    branches = []
    h_branches = []
    offsets = []  # 各支路时延偏移（FS 对齐用）

    for k_b in range(n_branches):
        # 各支路独立 GG 块衰落（独立时完全独立种子；相关时共享基础+支路扰动）
        rng_b = np.random.RandomState(seed + k_b * 7919 + 1)
        if independent:
            h_k = gg_block(Ns, a, b)
        else:
            # 相关分集：共享大尺度 + 小尺度独立扰动（简化模型）
            h_base = gg_block(Ns, a, b)
            perturb = gamma_rvs_correlated(Ns, a, b, rng_b, corr=0.3)
            h_k = 0.7 * h_base + 0.3 * perturb

        # 支路时延偏移（每支路几符号，FS 需对齐）
        offset_k = k_b  # 简化：第 k 支路偏移 k 符号
        offsets.append(offset_k)

        # 各支路独立 AWGN
        noise_var = 1.0 / (2 * gamma_bar)
        noise = np.sqrt(noise_var) * (
            rng_b.randn(Ns) + 1j * rng_b.randn(Ns)
        )

        signal_k = tx * np.sqrt(h_k) * carrier
        rx_k = signal_k + noise
        branches.append(rx_k)
        h_branches.append(h_k)

    n_blocks = Ns // BLOCK
    h_blocks = np.array([h_branches[0][i * BLOCK] for i in range(n_blocks)]) if n_branches > 0 else np.array([])
    h_med = np.median(h_blocks) if len(h_blocks) > 0 else 0.0

    return {
        'branches': branches,          # list[np.ndarray]，各支路接收信号
        'h_branches': h_branches,      # list[np.ndarray]，各支路信道增益
        'phi_shared': phi_shared,      # 共享载波相位（频偏+Doppler+线宽）
        'tx': tx, 'bits': bits,
        'Ns': Ns, 'gamma_bar': gamma_bar,
        'turb_name': turb_name, 'f_dot': f_dot, 'f_res': f_res,
        'n_branches': n_branches,
        'offsets': offsets,            # 各支路时延偏移
        'aperture_spacing_m': aperture_spacing_m,
        'independent_diversity': independent,
        'r0_cm': _fried_parameter(1550e-9, cn2, z_km * 1e3) * 100,
        'h_blocks': h_blocks, 'h_med': h_med,
        'mod': 'qpsk',
    }


def gamma_rvs_correlated(N, a, b, rng, corr=0.3):
    """简化的相关 Gamma-Gamma 采样（分集退化时用）。"""
    nb = (N + BLOCK - 1) // BLOCK
    g1 = rng.gamma(a, scale=1/a, size=nb) * rng.gamma(b, scale=1/b, size=nb)
    return np.repeat(g1, BLOCK)[:N]
