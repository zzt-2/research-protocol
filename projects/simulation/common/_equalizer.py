"""均衡器：MMSE + 限幅"""
import numpy as np


def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out


def mmse_equalize(rx, h, gamma_bar):
    """MMSE 均衡，h 可为标量或向量"""
    return rx * np.sqrt(h) / (h + 1/gamma_bar)


def equalize_oracle(shared):
    """oracle h 均衡"""
    return amp_limit(mmse_equalize(shared['rx_raw'], shared['h'], shared['gamma_bar']), 3.0)


def equalize_hmed(shared):
    """h_med 均衡（公平）"""
    return amp_limit(mmse_equalize(shared['rx_raw'], shared['h_med'], shared['gamma_bar']), 3.0)
