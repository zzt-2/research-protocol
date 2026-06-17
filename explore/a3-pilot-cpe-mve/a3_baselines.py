"""A3 §4a 维度 D MVE — Baseline 方法（M2/M3/M4）+ 频偏估计。

M2 AGC+DPLL（FR-14 最强简单先验）
M3 VV 盲 CPE（BC-2 失效参照，TL-18）
M4 PASC 数字近似（FR-15 目标基线，BC-1）
"""
import numpy as np
from a3_channel import T_S, F_RESIDUAL


# ═══════════════════════════════════════════════════════════════
# 频偏估计（前置，所有方法都可能用）
# ═══════════════════════════════════════════════════════════════
def fft_foe(rx, M=4, N_fft=2048, nfft_zp=16384):
    """M-th power FFT 频偏估计（V&V 风格）。返回角频偏 rad/sample。"""
    N_fft = min(N_fft, len(rx))
    seg = rx[:N_fft]
    rM = seg ** M
    win = np.hanning(N_fft)
    R = np.fft.fftshift(np.fft.fft(rM * win, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    idx = np.argmax(np.abs(R))
    if 1 <= idx < len(R) - 1:
        av, bv, gv = np.abs(R[idx-1]), np.abs(R[idx]), np.abs(R[idx+1])
        if bv - av > 0 and bv + av - 2*gv != 0:
            p = 0.5 * (av - gv) / (av - 2*bv + gv)
            f_est = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            f_est = freqs[idx]
    else:
        f_est = freqs[idx]
    return 2 * np.pi * f_est / M


def kay_estimator(rx, M=4):
    """Kay 频偏估计器（数据辅助，4th-power 去调制后差分相位加权平均）。

    Kay 1989：f_hat = (1/M) * sum_k w[k] * angle(z[k+1] * conj(z[k]))
    其中 z[k] = rx[k]^M（去调制），w[k] = |z[k+1]*conj(z[k])|（高 SNR 样本权重高）。
    比 fft_foe 精得多（渐近达到 CRLB），适合大频偏场景。
    返回角频偏 rad/sample。
    """
    z = rx ** M
    # 差分相位
    diff = z[1:] * np.conj(z[:-1])
    # Kay 权重：|diff|（高幅度样本更可信）
    w = np.abs(diff)
    w_sum = np.sum(w)
    if w_sum < 1e-12:
        return 0.0
    # 加权平均差分相位
    f_est = np.sum(w * np.angle(diff)) / w_sum
    return f_est / M   # 除 M 还原真实频偏（4th-power 把频偏也乘 4）


def ml_estimator(rx, M=4, n_fft=65536):
    """M&L (Luise-Reggiannini) 频偏估计：频域细化搜索，精度更高。

    在 fft_foe 给的粗估附近做细化 FFT，达 ML 最优。
    返回角频偏 rad/sample。
    """
    f_coarse = fft_foe(rx, M=M)
    # 在粗估附近 ±0.01 rad/sample 范围细化网格搜
    f_grid = f_coarse + np.linspace(-0.01, 0.01, 401)
    z = rx ** M
    # ML 目标：|sum_k z[k] exp(-j M f k)|²
    N = len(z)
    k = np.arange(N)
    obj = np.array([np.abs(np.sum(z * np.exp(-1j * Mf * k)))**2 for Mf in f_grid])
    return f_grid[np.argmax(obj)] / 1   # f_grid 已经是真实频偏网格（不乘 M）


# ═══════════════════════════════════════════════════════════════
# M2: AGC + DPLL
# ═══════════════════════════════════════════════════════════════
def agc(rx, win=32, floor=0.3):
    """数字 AGC：滑窗估计幅度并归一化。

    **bug 修复**：原版无下限，deep fade (amp_est≈0) 时除以近零值把噪声放大千倍。
    floor: 幅度估计下限（相对平均幅度的比例）。低于此值不放大（模拟真实 AGC 噪声地板）。
    Paillier §III AGC 是真实硬件，有噪声地板，不会无限放大 fade 瞬态。
    """
    amp = np.abs(rx)
    kernel = np.ones(win) / win
    amp_est = np.sqrt(np.convolve(amp**2, kernel, mode='same') + 1e-12)
    mean_amp_est = np.sqrt(np.mean(amp_est**2))
    # 下限：不低于平均幅度的 floor 比例（避免 deep fade 放大噪声）
    amp_est_clamped = np.maximum(amp_est, floor * mean_amp_est)
    return rx / amp_est_clamped * mean_amp_est   # 归一化到平均功率


def dpll_track(rx_after_agc, f0=None, bn_norm=0.05, zeta=np.sqrt(2)/2):
    """二阶 DPLL 跟踪相位。rx_after_agc 已 AGC 归一化。

    参数化：bn_norm = 归一化环路带宽 Bn·T_S（典型 0.01-0.2）。
    f0: 初始频偏估计（rad/sample），None 则用 fft_foe 估。
    返回 phi_est（估计相位，用于补偿）。

    **bug 修复**：原 phi_est[0]=angle(rx[0])，deep fade 首样可能为噪声 → 初始错。
    改为初始化为 f0·0=0（用频偏先验，首样靠环路收敛）。
    """
    N = len(rx_after_agc)
    if f0 is None:
        f0 = fft_foe(rx_after_agc, M=4)
    wT = min(2 * np.pi * bn_norm, 0.5)   # 稳定性上界
    c1 = 2 * zeta * wT
    c2 = wT ** 2

    phi_est = np.zeros(N)
    phi_est[0] = 0.0   # 用频偏先验初始化，不依赖首样（fade 首样可能噪声）
    freq_est = f0
    for k in range(1, N):
        phi_pred = phi_est[k-1] + freq_est
        # QPSK 4th-power 鉴相器：r^4 的角度/4 = 残余相位误差（去 π/2 模糊）
        r = rx_after_agc[k] * np.exp(-1j*phi_pred)
        e = np.angle(r**4) / 4   # 输出 [-π/4, π/4]
        freq_est += c2 * e
        phi_est[k] = phi_pred + c1 * e
    return phi_est


def m2_agc_dpll(rx_raw, bn_norm=0.05, zeta=np.sqrt(2)/2):
    """M2 全流程：AGC → DPLL → 补偿后 symbol。返回 rx_compensated, phi_est。"""
    rx_agc = agc(rx_raw)
    phi_est = dpll_track(rx_agc, bn_norm=bn_norm, zeta=zeta)
    rx_comp = rx_agc * np.exp(-1j * phi_est)
    return rx_comp, phi_est


def m2_grid_search(rx_raw, tx, data_mask=None):
    """M2 baseline 网格搜索（TL-14，TL-25 #4）。

    **bug 修复**：原 score=残余相位方差，奖励追噪声（fade 块方差小≠跟踪好）。
    改用**真实 BER**（需传 tx）作 score，这是唯一正确的 baseline 优化目标。
    返回最优参数 + 最优结果。
    """
    from a3_channel import ber_count
    best = {'bn_norm': 0.05, 'zeta': 0.707, 'ber': 1.0, 'phi_est': None, 'rx_comp': None}
    for bn_norm in [0.005, 0.01, 0.03, 0.05, 0.1]:
        for zeta in [0.5, 0.707, 1.0]:
            rx_comp, phi_est = m2_agc_dpll(rx_raw, bn_norm=bn_norm, zeta=zeta)
            ber = ber_count(tx, rx_comp, data_mask=data_mask, resolve_ambiguity=True)
            if ber < best['ber']:
                best = {'bn_norm': bn_norm, 'zeta': zeta, 'ber': ber,
                        'phi_est': phi_est, 'rx_comp': rx_comp}
    return best


# ═══════════════════════════════════════════════════════════════
# M3: VV 盲 CPE（BC-2 失效参照，TL-18）
# ═══════════════════════════════════════════════════════════════
def vv_cpe(rx_raw, M=4, block_len=32):
    """V&V M-th power 盲 CPE。QPSK M=4。

    block_len: 块平均窗（symbol 数）
    返回 phi_est（每 symbol 相位估计），rx_comp。
    """
    N = len(rx_raw)
    # 先去频偏（fft_foe 返回 rad/sample）
    f0 = fft_foe(rx_raw, M=M)
    rx_fo = rx_raw * np.exp(-1j * f0 * np.arange(N))

    phi_est = np.zeros(N)
    half = block_len // 2
    for k in range(N):
        lo = max(0, k - half)
        hi = min(N, k + half + 1)
        seg = rx_fo[lo:hi]
        # M-th power 去调制 + 平均
        phi_raw = np.angle(np.sum(seg ** M))
        phi_est[k] = phi_raw / M
    rx_comp = rx_fo * np.exp(-1j * phi_est)
    return phi_est, rx_comp


def m3_vv_grid(rx_raw, tx, data_mask=None):
    """M3 VV 窗长网格搜索（用真实 BER 作 score，bug 修复同 m2）。"""
    from a3_channel import ber_count
    best = {'block_len': 32, 'ber': 1.0, 'phi_est': None, 'rx_comp': None}
    for block_len in [16, 32, 64, 128]:
        phi_est, rx_comp = vv_cpe(rx_raw, M=4, block_len=block_len)
        ber = ber_count(tx, rx_comp, data_mask=data_mask, resolve_ambiguity=True)
        if ber < best['ber']:
            best = {'block_len': block_len, 'ber': ber, 'phi_est': phi_est, 'rx_comp': rx_comp}
    return best


# ═══════════════════════════════════════════════════════════════
# M4: PASC 数字近似（FR-15 目标基线，BC-1）
# ═══════════════════════════════════════════════════════════════
# PASC = phase- and amplitude-sensitive coherence（self-coherent 光域共轭补偿）。
# 真实 PASC 是光域 self-coherent（pilot tone 在光域做共轭补偿，无 PLL/unpack）。
# 数字近似：用 pilot tone 提取相位后直接减（不做 unwrap，不做 PAPU）——
#   近似 PASC"光域即时补偿"特性。记录与真 PASC 差距（真实 PASC 无采样损失）。
def m4_pasc_digital(rx_with_tone, tone_idx, pilot_power_frac=0.05):
    """M4 PASC 数字近似：从 pilot tone 直接提相位并减（不 unwrap，不 PAPU）。

    rx_with_tone: 含 pilot tone 的接收信号（tone 在 tone_idx 位置，或频域）
    tone_idx: pilot tone 的 symbol 索引
    pilot_power_frac: tone 占总功率（记录用）
    返回 rx_comp（data symbol 补偿后）。
    """
    # 简化：pilot tone 给每 symbol 一个相位参考（近似连续 tone 的离散采样）
    # tone 相位 = angle(rx[tone_idx])，直接减
    # 但 tone 本身受噪声影响——这就是数字 PASC 与光域 PASC 的差距来源
    N = len(rx_with_tone)
    phi_tone = np.angle(rx_with_tone[tone_idx])   # 单点相位（近似）
    # 若 tone_idx 是序列，用插值（这里 tone_idx 假定是密集采样的连续 tone）
    if hasattr(tone_idx, '__len__') and len(tone_idx) > 1:
        phi_ref = np.interp(np.arange(N), tone_idx, np.angle(rx_with_tone[tone_idx]))
    else:
        # 单 tone：用 Wiener 平滑估连续相位（近似光域低通）
        from scipy.signal import savgol_filter
        raw_phase = np.angle(rx_with_tone)
        # unwrap 后平滑
        raw_phase_u = np.unwrap(raw_phase)
        phi_ref = savgol_filter(raw_phase_u, 31, 2) if N > 31 else raw_phase_u
    rx_comp = rx_with_tone * np.exp(-1j * phi_ref)
    return rx_comp, phi_ref


if __name__ == '__main__':
    # 自检：VV 在 strong 湍流应复现失效（TL-18 管道自检）
    from a3_channel import generate_shared_realization
    print("=== M3 VV 失效复现自检（TL-18）===")
    for turb in ['weak', 'strong']:
        ch = generate_shared_realization(8192, 10.0, turb, seed=42)
        res = m3_vv_grid(ch['rx_raw'])
        # VV 补偿后 BER（用 tx 比较）
        from a3_channel import ber_count
        ber = ber_count(ch['tx'], res['rx_comp'])
        # 无处理 BER 对照
        ber_raw = ber_count(ch['tx'], ch['rx_raw'])
        print(f"  {turb}: VV block_len={res['block_len']}, BER(VV)={ber:.4f}, BER(raw)={ber_raw:.4f}, score={res['score']:.4f}")
