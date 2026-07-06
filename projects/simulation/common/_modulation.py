"""调制/解调/BER 评估"""
import numpy as np


def qpsk_mod(bits):
    return ((2*bits[0::2]-1) + 1j*(2*bits[1::2]-1)) / np.sqrt(2)

def qpsk_demod(s):
    b = np.zeros(2*len(s), dtype=int)
    b[0::2] = (np.real(s) > 0).astype(int)
    b[1::2] = (np.imag(s) > 0).astype(int)
    return b

def ber_count(tx_bits, rx):
    return np.mean(tx_bits != qpsk_demod(rx))

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def qam16_mod(bits):
    """16-QAM modulation: 4 bits/symbol, avg power normalized to 1.
    Gray mapping: 00→-3, 01→-1, 11→+1, 10→+3 per axis.
    """
    ns = len(bits) // 4
    bits = bits[:ns*4]
    bi = 2*bits[0::4] + bits[1::4]  # 2-bit I index
    bq = 2*bits[2::4] + bits[3::4]  # 2-bit Q index
    # Gray decode: 00→-3, 01→-1, 11→+1, 10→+3
    gray_map = np.array([-3, -1, +3, +1])
    si = gray_map[bi]
    sq = gray_map[bq]
    # Normalize: E[|s|²] = (9+1+1+9)/4 * 2 = 10, so divide by sqrt(10)
    return (si + 1j * sq) / np.sqrt(10)

def qam16_demod(s):
    """16-QAM demodulation with Gray mapping."""
    s = s * np.sqrt(10)  # undo normalization
    si = np.real(s)
    sq = np.imag(s)
    # Slice to {-3, -1, +1, +3}
    di = np.clip(np.round((si + 3) / 2) * 2 - 3, -3, 3).astype(int)
    dq = np.clip(np.round((sq + 3) / 2) * 2 - 3, -3, 3).astype(int)
    # Gray encode: -3→00, -1→01, +1→11, +3→10
    gray_enc = {-3: (0,0), -1: (0,1), 1: (1,1), 3: (1,0)}
    ns = len(s)
    bits = np.zeros(4*ns, dtype=int)
    for k in range(ns):
        b0, b1 = gray_enc.get(int(di[k]), (0,0))
        b2, b3 = gray_enc.get(int(dq[k]), (0,0))
        bits[4*k]   = b0
        bits[4*k+1] = b1
        bits[4*k+2] = b2
        bits[4*k+3] = b3
    return bits

def ber_count_qam16(tx_bits, rx):
    return np.mean(tx_bits != qam16_demod(rx))

def resolve_qam16(rx, tx_bits):
    """QAM16 resolve: try 8 pi/4 rotations, pick lowest BER."""
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count_qam16(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def ber_eval(tx_bits, rx, mode='direct'):
    """统一 BER 评估。

    mode='direct' (默认): 直接解调 ber_count — 公平，无 oracle
    mode='oracle': resolve_qpsk — 用 TX bits 选最优旋转（oracle 方法）
    """
    if mode == 'direct':
        return ber_count(tx_bits, rx)
    elif mode == 'oracle':
        return resolve_qpsk(rx, tx_bits)
    else:
        raise ValueError(f"Unknown mode: {mode}")

def hard_decision(z, mod='qpsk'):
    """Hard decision for QPSK or 16-QAM. Works with scalars and arrays."""
    if mod == 'qpsk':
        return (np.sign(np.real(z)) + 1j * np.sign(np.imag(z))) / np.sqrt(2)
    s = z * np.sqrt(10)
    di = np.clip(np.round((np.real(s) + 3) / 2) * 2 - 3, -3, 3)
    dq = np.clip(np.round((np.imag(s) + 3) / 2) * 2 - 3, -3, 3)
    return (di + 1j * dq) / np.sqrt(10)


# =============================================================================
# M-APSK 调制（B11 锚调制族：8PSK / (8,8)-16APSK / (4,12,16)-32APSK）
# 接口对齐 QPSK/16-QAM：*_mod(bits) / *_demod(s) / ber_count_*(tx_bits, rx) / resolve_*(rx, tx_bits)
# 来源: B11 (10.1109_LPT.2024.3523478) 行 12/155 使用 (8,8)-16APSK/(4,4)-8APSK；
#        星座结构按 DVB-S2 (ETSI EN 302 307-1) 标准。
# =============================================================================

# --- 8PSK: 单环 8 点, 3 bit/symbol, Gray 映射, 平均功率归一化到 1 ---
# 半径=1（均匀环 8 点相位 π/8 + k·π/4），平均功率 = 1² = 1 已归一化。
# 物理 k=0..7 位置的 Gray 标签（相邻相位差 1 bit, 标准反射 Gray 序）：
_APSK8_GRAY = np.array([0b000, 0b001, 0b011, 0b010,
                        0b110, 0b111, 0b101, 0b100])
_APSK8_SYM = np.array([np.exp(1j * (np.pi/8 + k*np.pi/4)) for k in range(8)])
# 按标签值 0..7 排好序的星座点（sym_by_label[label] = 该 label 的星座点）:
_APSK8_SYM_BY_LABEL = np.empty(8, dtype=complex)
_APSK8_SYM_BY_LABEL[_APSK8_GRAY] = _APSK8_SYM


def apsk8_mod(bits):
    """8PSK modulation (B11 (4,4)-8APSK 等价单环形式): 3 bit/symbol, Gray, avg power=1.

    来源: B11 行 12/155 (4,4)-8APSK；星座相位 π/8 + k·π/4, 半径 1（均匀环）。
    """
    ns = len(bits) // 3
    bits = bits[:ns*3]
    idx = (4*bits[0::3] + 2*bits[1::3] + bits[2::3]).astype(int)
    return _APSK8_SYM_BY_LABEL[idx]


def apsk8_demod(s):
    """8PSK demodulation: 最近星座点（欧氏距离最小）, 向量化。

    对每符号独立算到 8 个星座点的距离, 返回 Gray label bits。
    """
    s = np.atleast_1d(s)
    # 距离矩阵 (N, 8); _APSK8_SYM_BY_LABEL 索引即 label 值
    dist = np.abs(s[:, np.newaxis] - _APSK8_SYM_BY_LABEL[np.newaxis, :]) ** 2
    labels = np.argmin(dist, axis=1)   # argmin 直接给出 label 值 0..7
    bits = np.zeros(3 * len(s), dtype=int)
    bits[0::3] = (labels >> 2) & 1
    bits[1::3] = (labels >> 1) & 1
    bits[2::3] = labels & 1
    return bits


def ber_count_apsk8(tx_bits, rx):
    return np.mean(tx_bits != apsk8_demod(rx))


def resolve_apsk8(rx, tx_bits):
    """8PSK resolve: 8PSK 有 M₀=8 相位模糊, 试 8 个 2π/8 旋转取最低 BER.

    仿 resolve_qpsk/resolve_qam16（M₀ 来自 B11 行 75 升幂阶数）。
    """
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count_apsk8(tx_bits, rx * np.exp(-1j*r))
        if b < best:
            best = b
    return best


def resolve_apsk8_blockwise(rx, tx_bits, block_size=256, mod='apsk8'):
    """逐块 resolve M₀-fold 相位模糊（解 Wiener PN 累积致块间落入不同模糊 m）.

    修复 Bug 2: NDA 升 M₀=8 次幂有 8 重相位模糊 (φ̂+2πm/8). Wiener PN 累积致块间真 φ(k)
    落入不同模糊 m（块间 φ 差超 2π/8）→ 全局单旋转（试 8 个 π/4 取最低 BER）无法同时
    解所有块的模糊 → BER 灾难. 正确做法: 逐块各自 resolve（每块用其 tx_bits 选最优旋转）.

    对每 block 试 8 个 2π/8 旋转, 用该 block 的 tx_bits 选最低 BER 旋转, 返回 per-block
    旋转补偿后的 rx. block_size 默认 256（对齐 B11 DFT_SIZE）.

    来源: 诊断脚本 _awgn_repro_diagnostic.py resolve_m16apsk_blockwise.
    注: resolve 用已知 tx_bits（MVE 风格 / DA ML 评估场景）, 与 B11 行 129 genie-aided
        解卷绕精神一致; 纯盲 NDA 可改用每块硬判决众数投票（本轮先用 tx_bits 版本）。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    L = n_blk * block_size
    bits_per_sym = 3  # 8PSK: 3 bit/symbol
    out = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        tb = tx_bits[b * block_size * bits_per_sym:(b + 1) * block_size * bits_per_sym]
        best_ber = 1.0
        best_seg = seg
        for r in np.arange(0, 2 * np.pi, np.pi / 4):
            ber = np.mean(tb != apsk8_demod(seg * np.exp(-1j * r)))
            if ber < best_ber:
                best_ber = ber
                best_seg = seg * np.exp(-1j * r)
        out[s] = best_seg
    return out


# --- (8,8)-16APSK: 两环各 8 点, 4 bit/symbol, Gray 映射, 平均功率归一化到 1 ---
# DVB-S2 标准 (ETSI EN 302 307-1 §5.4.3): 内环 r1 外环 r2, 半径比 γ=r2/r1≈2.57。
# 平均功率归一化: (8·r1² + 8·r2²)/16 = 1 → r1² + r2² = 2, γ=2.57 →
#   r1 = sqrt(2/(1+γ²)) ≈ 0.5129, r2 = γ·r1 ≈ 1.3180。
_APSK16_GAMMA = 2.57  # DVB-S2 标准半径比 (ETSI EN 302 307-1)
_R1_16 = np.sqrt(2.0 / (1.0 + _APSK16_GAMMA**2))         # 内环半径 ≈ 0.5129
_R2_16 = _APSK16_GAMMA * _R1_16                          # 外环半径 ≈ 1.3180
# 内环 8 点相位 π/8 + k·π/4（半径 r1）, 外环 8 点相位 k·π/4（半径 r2）。
_INNER16 = np.array([_R1_16 * np.exp(1j * (np.pi/8 + k*np.pi/4)) for k in range(8)])
_OUTER16 = np.array([_R2_16 * np.exp(1j * (k*np.pi/4)) for k in range(8)])
_M16APSK_SYM = np.concatenate([_INNER16, _OUTER16])  # (16,) index 0-7 内, 8-15 外
# Gray 映射（4 bit/symbol, 相邻星座差 1 bit; b0 选环 b0=0→内 1→外, b1b2b3 环内 Gray）
_M16APSK_GRAY = np.array([
    0b0000, 0b0001, 0b0011, 0b0010, 0b0110, 0b0111, 0b0101, 0b0100,   # 内环 b0=0
    0b1000, 0b1001, 0b1011, 0b1010, 0b1110, 0b1111, 0b1101, 0b1100,   # 外环 b0=1
])
_M16APSK_SYM_BY_LABEL = _M16APSK_SYM[_M16APSK_GRAY.argsort()]  # 按 label 0..15 排序的星座点


def m16apsk_mod(bits):
    """(8,8)-16APSK modulation (B11 锚调制): 4 bit/symbol, Gray, avg power=1.

    来源: B11 行 12/155 (8,8)-16APSK；DVB-S2 标准 (ETSI EN 302 307-1 §5.4.3)。
    半径比 γ=r2/r1=2.57, r1≈0.5129, r2≈1.3180, 平均功率 (8r1²+8r2²)/16=1。
    """
    ns = len(bits) // 4
    bits = bits[:ns*4]
    idx = (8*bits[0::4] + 4*bits[1::4] + 2*bits[2::4] + bits[3::4]).astype(int)
    return _M16APSK_SYM_BY_LABEL[idx]


def m16apsk_demod(s):
    """(8,8)-16APSK demodulation: 最近星座点（欧氏距离最小）, 向量化。

    先用半径判环（|s| 阈值 (r1+r2)/2）选 b0, 再环内 8 点相位最近选 b1b2b3。
    """
    s = np.atleast_1d(s)
    thr = 0.5 * (_R1_16 + _R2_16)
    is_outer = np.abs(s) > thr
    # 每符号到内/外环 8 点的距离
    d_inner = np.abs(s[:, np.newaxis] - _INNER16[np.newaxis, :]) ** 2
    d_outer = np.abs(s[:, np.newaxis] - _OUTER16[np.newaxis, :]) ** 2
    k_inner = np.argmin(d_inner, axis=1)
    k_outer = np.argmin(d_outer, axis=1)
    # 用整体最小距离决定环（避免半径模糊区误判）
    d_inner_min = d_inner[np.arange(len(s)), k_inner]
    d_outer_min = d_outer[np.arange(len(s)), k_outer]
    pick_outer = (d_outer_min < d_inner_min) | is_outer
    # 环内 Gray 标签 b1b2b3（与 8PSK 相同的 Gray 序）
    gray3 = _APSK8_GRAY
    b1 = np.zeros(len(s), dtype=int)
    b2 = np.zeros(len(s), dtype=int)
    b3 = np.zeros(len(s), dtype=int)
    ki = gray3[k_inner]
    ko = gray3[k_outer]
    b1[~pick_outer] = (ki[~pick_outer] >> 2) & 1
    b2[~pick_outer] = (ki[~pick_outer] >> 1) & 1
    b3[~pick_outer] = ki[~pick_outer] & 1
    b1[pick_outer] = (ko[pick_outer] >> 2) & 1
    b2[pick_outer] = (ko[pick_outer] >> 1) & 1
    b3[pick_outer] = ko[pick_outer] & 1
    b0 = pick_outer.astype(int)
    bits = np.zeros(4 * len(s), dtype=int)
    bits[0::4] = b0
    bits[1::4] = b1
    bits[2::4] = b2
    bits[3::4] = b3
    return bits


def ber_count_m16apsk(tx_bits, rx):
    return np.mean(tx_bits != m16apsk_demod(rx))


def resolve_m16apsk(rx, tx_bits):
    """(8,8)-16APSK resolve: M₀=8 相位模糊（两环各 8 点）, 试 8 个 2π/8 旋转取最低 BER.

    来源: B11 行 75 升 M₀=8 次幂隐含 8 重相位模糊。
    """
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_count_m16apsk(tx_bits, rx * np.exp(-1j*r))
        if b < best:
            best = b
    return best


def resolve_m16apsk_blockwise(rx, tx_bits, block_size=256, mod='m16apsk'):
    """逐块 resolve M₀-fold 相位模糊（解 Wiener PN 累积致块间落入不同模糊 m）.

    修复 Bug 2: NDA 升 M₀=8 次幂有 8 重相位模糊 (φ̂+2πm/8). Wiener PN 累积致块间真 φ(k)
    落入不同模糊 m（块间 φ 差超 2π/8）→ 全局单旋转（试 8 个 π/4 取最低 BER）无法同时
    解所有块的模糊 → BER 灾难. 正确做法: 逐块各自 resolve（每块用其 tx_bits 选最优旋转）.

    对每 block 试 8 个 2π/8 旋转, 用该 block 的 tx_bits 选最低 BER 旋转, 返回 per-block
    旋转补偿后的 rx. block_size 默认 256（对齐 B11 DFT_SIZE, B11 行 155 N=256）.

    来源: 诊断脚本 _awgn_repro_diagnostic.py resolve_m16apsk_blockwise.
    注: resolve 用已知 tx_bits（MVE 风格 / DA ML 评估场景）, 与 B11 行 129 genie-aided
        解卷绕精神一致; 纯盲 NDA 可改用每块硬判决众数投票（本轮先用 tx_bits 版本）。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    L = n_blk * block_size
    bits_per_sym = 4  # (8,8)-16APSK: 4 bit/symbol
    out = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        tb = tx_bits[b * block_size * bits_per_sym:(b + 1) * block_size * bits_per_sym]
        best_ber = 1.0
        best_seg = seg
        for r in np.arange(0, 2 * np.pi, np.pi / 4):
            ber = np.mean(tb != m16apsk_demod(seg * np.exp(-1j * r)))
            if ber < best_ber:
                best_ber = ber
                best_seg = seg * np.exp(-1j * r)
        out[s] = best_seg
    return out


# TODO B3: (4,12,16)-32APSK 三环（DVB-S2 标准）apsk32_mod/demod/ber_count_apsk32/resolve_apsk32
# B3 扩展备用, 本轮（B11/B7/B3 Step 4a 共用基建）暂不实现。
