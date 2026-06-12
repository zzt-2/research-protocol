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
