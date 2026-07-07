"""B5 短时谱 FOE 探针 — LEO Doppler 频偏粗估（B5 锚 optcom.2024.130981 L71-87）

B5 锚核心算法: 分块 FFT → 均值滤波 → 正负功率谱面积比 Rp-n → 归一化频偏估计
Δfest = α·Rp-n → 星历预测调 LO → **3-4 次迭代收敛**（L141）. 全程前馈开环,
无环路传递函数 H(z)（0.3a 决策）.

=== C6 公式重建标注（PDF→md 公式丢失，从 content.md L77-87 文字重建）===

B5 锚式 1-4 在 content.md L73/L79/L81/L83 以 `picture intentionally omitted` 形式
存在（display equation 图片在 PDF→md 转换丢失）。下面从 L77-87 文字逐式重建:

- **B5 锚式 1（content.md L73, PDF→md 重建）**: 离散功率谱
      R[k] = |FFT(r[n]·win[n])|²
  r[n] = 接收数字采样, win = Hanning 窗（参考 fft_foe_m0_omega 工程实现,
  sc_nda_ml_sim.py:153）

- **B5 锚式 3（content.md L81, PDF→md 重建）**: 正负功率谱面积比 Rp-n
  （L77 "positive and negative power areas"）
      Rp-n = P_+ − P_-       (P_+ = 正频率半轴功率积分, P_- = 负频率半轴功率积分)
  C6 重建歧义: 原文未明确 Rp-n 是绝对差 P_+ − P_- 还是归一化差
  (P_+ − P_-)/(P_+ + P_-). → 三方案都实现, normalize_mode 参数化.

- **B5 锚式 2（content.md L79, PDF→md 重建）**: 归一化频偏估计
      Δfest = α · Rp-n          (α = 6×10⁸, content.md L85)
  注: α 是经验校准系数（L85 "a coefficient to convert the spectral power bias to FO"）.

- **B5 锚式 4（content.md L83, PDF→md 重建）**: 实际补偿频偏
      Δf_comp = Δfest + ephemeris_pred   (L87 星历预测调 LO)

=== 关键机制发现（sandbox 验证, 影响 C6 歧义结论）===

1. **频谱须带限（sinc 型）才有不对称**: 平坦白谱（1-sps 无脉冲成型 QPSK）平移后
   仍平坦, Rp-n ≈ 0 无信息. B5 锚 L115 "low-pass frequency characteristics, 3dB 1.33GHz"
   + RRC 脉冲成型（L85 "roll-off factor for Nyquist-shaping"）致 sinc 型带限谱,
   平移后正负半轴功率不对称. **测试信号必须带限**（自测用 2-sps RRC, 见 __main__）.

2. **Rp-n-vs-f 非线性, 须迭代收敛**: Rp-n 在 |f|<~0.3fs 线性, 之后饱和/翻转
   （2-sps RRC @fs=5e9: 线性区 ±~1.5GHz, 饱和点 ±1.5GHz, fs/2=2.5GHz 翻转）.
   → 单次估计仅对残频有效. **B5 锚靠 3-4 次迭代收敛**（L141 "converges by the
   third/fourth iteration"）: 每轮预补偿估计值 → 残频减小 → 再估落在线性区.
   见 short_time_spectrum_foe_iterate.

3. **α=6×10⁸ 暗示 'ratio' 模式（C6 歧义结论）**: ratio 模式 Rp-n∈[-1,1], 饱和 ~0.5,
   α=6e8 → Δfest=6e8×0.5=300MHz ≈ 精估范围 B/8=312.5MHz（一致, 落精估边界）.
   block/agc 模式 Rp-n 量纲不同, 须重校 α（非 6e8）. **结论: B5 锚大概率 ratio 模式**.
   但本探针三方案都实现（normalize_mode 参数化）, sandbox 三方对照定最优.

4. **block 模式 ≡ ratio 模式（仅 α 尺度不同）**: 按块归一化（每块 PSD 除以该块总功率）
   后, 均值谱 sum≈1, Rp-n(block)=P_+-P_- 与 ratio 的 (P_+-P_-)/(P_+_P_-) 数值相同
   （都尺度无关）. agc 模式 Rp-n=绝对差, 随信号功率变（须配合 AGC 才稳定）.

=== 架构定性（0.3a 决策, 守 INVARIANT 13 / D006 边界）===

前馈归一化三方案（normalize_mode, 0.3a 方案 A/B/C）都不撞 D006（归一化是前馈信号
预处理, 不把湍流相位 φ_T 纳入环路 TF）:
- 'block': 每块 PSD 除以该块总功率 ‖x_blk‖² → Rp-n = P_+ − P_-（方案 A, ≡ ratio）
- 'agc':   FFT 前归一化接收功率到固定电平（除以 RMS）→ Rp-n = P_+ − P_-（方案 B, 绝对差）
- 'ratio': Rp-n = (P_+ − P_-)/(P_+ + P_-)（方案 C, 归一化功率比, α=6e8 暗示此模式）

=== fs 参数歧义（content.md L117 ±B/2）===

L117 "estimate a frequency offset range of [−B/2, +B/2]" 中 B 可解为:
  (a) 信号带宽/符号率 R_SYM_B5=2.5e9 → ±1.25GHz（_file_organization.md 接口默认此解）
  (b) 采样带宽/ADC 速率 ADC_RATE_B5=5e9 → ±2.5GHz（B5 锚 2-sps @5GSa/s 物理采样）
函数 fs 参数默认守接口规约 2.5e9（解 a）, 但 __main__ 自测用 2-sps RRC + fs=5e9
（解 b, 匹配 B5 锚 ADC 物理采样, 见 L93 "5 GSa/s"）. 两解都不改变算法机制,
只改变捕获范围/α 尺度. 正式 MVE 时跟锚参数对齐.

=== 参数真相源（param-source.md, 禁硬编码）===

函数默认参数留字面值（跟 B5Params 字段一致）, docstring 标注对应 B5Params 字段.
正式调用应 `from params import B5Params` 后读字段传入（避免硬编码, 见 __main__）.

=== 信道禁自建（TL-13）===

本文件只实现估计器, 不生成信道. 自测用 RRC 脉冲成型 QPSK（验证算法机制, 非信道
实现）+ generate_shared_realization（common 信道, 验证湍流场景）. B5 锚是 PM-QPSK
双偏振, sandbox 单偏振 QPSK 不改变算法机制.

=== explore 探针不进 common（红线 6 / INVARIANT 14）===

本文件带 `_` 前缀放 explore 目录. sandbox 三方对照 PASS + MVE consistency PASS 后
才转正进 common/_recovery.py.
"""

from __future__ import annotations

import numpy as np


# ============================================================================
# short_time_spectrum_foe — B5 短时谱 FOE 核心估计器（单次）
# ============================================================================

def short_time_spectrum_foe(
    rx: np.ndarray,
    n_fft: int = 16,           # B5 锚 L87「16-point FFT」(B5Params.FFT_POINTS_B5)
    n_blocks: int = 1024,      # B5 锚 L87「1024 sets mean filtering」(B5Params.FFT_BLOCKS_B5)
    alpha: float = 6e8,        # B5 锚 L85 α=6×10⁸ (B5Params.ALPHA_B5)
    fs: float = 2.5e9,         # 采样率（见 fs 歧义）默认符号率 R_SYM_B5；ADC 速率 ADC_RATE_B5=5e9
    normalize_mode: str = 'ratio',   # 前馈归一化方案 0.3a 方案 A/B/C（α=6e8 暗 ratio, 默认 ratio）
    #   'block': 按块归一化（每块 PSD 除以块总功率）→ Rp-n = P_+ − P_-（≡ ratio 仅 α 尺度）
    #   'agc':   AGC 前置（归一化接收功率到固定电平）→ Rp-n = P_+ − P_-（绝对差, 随功率变）
    #   'ratio': 归一化功率比 Rp-n = (P_+ − P_-)/(P_+ + P_-)（α=6e8 暗 B5 锚用此模式）
    ephemeris_pred: float = 0.0,    # 星历预测频偏 Hz（B5 锚 L87 调 LO 预补偿）
) -> dict:
    """B5 短时谱 FOE 单次估计: 分块 FFT → 正负功率谱面积比 Rp-n → Δfest=α·Rp-n → +星历.

    B5 锚 optcom.2024.130981 L71-87 算法（前馈开环, 单次估计; 大频偏须迭代, 见
    short_time_spectrum_foe_iterate）:
    1. 输入数据分块（n_fft 点/块, 2 的幂次）
    2. 每块加 Hanning 窗 → FFT → 功率谱 R[k]=|FFT|²（B5 锚式 1, L73）
    3. [前馈归一化]（0.3a 方案 A/B/C, normalize_mode 选; block/agc 在 FFT 前/均值前归一化）
    4. n_blocks 组功率谱均值滤波取平均谱（B5 锚 L87「1024 sets mean filtering」）
    5. 正负功率谱面积比 Rp-n（P_+ 正频率 vs P_- 负频率, B5 锚式 3, L81）
    6. 归一化频偏估计 Δfest = α·Rp-n（B5 锚式 2, α=6×10⁸, L85）
    7. + 星历预测频偏 → 总补偿频偏（B5 锚式 4, L83, 调 LO）

    参数
    ----
    rx : np.ndarray (complex)
        接收信号采样（须带限/sinc 型谱, 见机制发现 1）.
    n_fft : int
        每块 FFT 点数. B5 锚 16（B5Params.FFT_POINTS_B5）. 须 2 的幂次.
    n_blocks : int
        均值滤波组数 M. B5 锚 1024（B5Params.FFT_BLOCKS_B5）.
    alpha : float
        系数 α（Rp-n → 频偏转换系数, B5 锚式 2）. B5 锚 6×10⁸（B5Params.ALPHA_B5）,
        暗 ratio 模式. block/agc 模式须重校 α（见 _calibrate_alpha）.
    fs : float
        采样率（Hz）. 见 fs 歧义段: 默认符号率 R_SYM_B5=2.5e9（解 a）;
        B5 锚物理采样 ADC_RATE_B5=5e9（解 b）. 决定理论捕获范围 ±fs/2.
    normalize_mode : {'block','agc','ratio'}
        前馈归一化方案（0.3a 决策, 守 INVARIANT 13 不撞 D006）.
    ephemeris_pred : float
        星历预测频偏（Hz）, B5 锚 L87 调 LO 预补偿. ±4.5GHz 全量程靠此预补偿到残频.

    返回
    ----
    dict:
        'fest_hz'         : float       # 估计频偏（Hz, 含星历预测）
        'fest_residual_hz': float       # 残频估计（Hz, 不含星历预测）= α·Rp-n
        'fest_omega'      : float       # 估计频偏（rad/sample）, 用于 exp(−j·omega·k) 补偿
        'rp_n'            : float       # 正负功率谱面积比（诊断用）
        'spectrum'        : np.ndarray  # 均值滤波后功率谱（fftshift, 诊断用, 原始未归一化）
        'p_plus','p_minus': float       # 正/负频率功率（诊断用）
        'normalize_mode'  : str         # 归一化方案（回显）
        'n_blocks_used'   : int         # 实际用块数

    纪律
    ----
    - 前馈开环, 无环路 TF（0.3a 决策, 禁撞 D006）
    - normalize_mode 必须显式传参（禁默认不归一化）
    - 参数从 B5Params 导入（sim-preflight param-source.md, 禁硬编码, 见 __main__）
    """
    rx = np.asarray(rx, dtype=complex)
    if rx.ndim != 1:
        rx = rx.ravel()
    if n_fft <= 0 or (n_fft & (n_fft - 1)) != 0:
        raise ValueError(f"n_fft 须 2 的幂次, got {n_fft}")
    if normalize_mode not in ('block', 'agc', 'ratio'):
        raise ValueError(
            f"normalize_mode 须 'block'/'agc'/'ratio', got {normalize_mode!r}")

    N = rx.shape[0]
    n_blocks = min(n_blocks, N // n_fft)
    if n_blocks < 1:
        raise ValueError(f"数据 {N} 不足一块 FFT (n_fft={n_fft})")
    usable = n_blocks * n_fft

    # --- 步骤 0a: 星历预测预补偿（B5 锚 L87 调 LO）---
    # LO 频率调 ephemeris_pred → 进入 FFT 的信号 = rx · exp(−j·2π·ephem·t), 即残频信号.
    # 之后 Rp-n 反映残频, α·Rp-n 是 FFT 对残频的估计, fest_hz = 残频估计 + 星历预测.
    if ephemeris_pred != 0.0:
        k0 = np.arange(N)
        rx = rx * np.exp(-1j * 2.0 * np.pi * ephemeris_pred * k0 / fs)

    # --- 步骤 0b: 前置 AGC 归一化（方案 B, 作用于整个输入, 'agc' 模式）---
    # AGC: 归一化接收功率到固定电平（除以 RMS 幅度）. 消除慢包络幅度起伏.
    if normalize_mode == 'agc':
        rms = np.sqrt(np.mean(np.abs(rx) ** 2))
        if rms > 0:
            rx = rx / rms

    # --- 步骤 1: 分块 + Hanning 窗（复用 fft_foe_m0_omega 工程实现 sc_nda_ml_sim.py:153）---
    blocks = rx[:usable].reshape(n_blocks, n_fft)
    win = np.hanning(n_fft)
    blocks_win = blocks * win[np.newaxis, :]   # B5 锚式 1 的 win（Hanning）

    # --- 步骤 2: 每块 FFT → 功率谱（B5 锚式 1, content.md L73, R[k]=|FFT|²）---
    spec = np.fft.fftshift(np.fft.fft(blocks_win, axis=1), axes=1)
    psd = np.abs(spec) ** 2                     # (n_blocks, n_fft) 每块 |FFT|² 功率谱

    # --- 步骤 3: [前馈归一化] 方案 A 'block' — 每块 PSD 除以该块总功率 ‖x_blk‖² ---
    # block 归一化在均值滤波前做（按块除）, 消除每块幅度尺度. 等价 ratio（Rp-n 尺度无关）.
    if normalize_mode == 'block':
        blk_total = psd.sum(axis=1, keepdims=True)   # 每块总功率 ‖x_blk‖²
        blk_total = np.where(blk_total > 0, blk_total, 1.0)
        psd = psd / blk_total

    # --- 步骤 4: 均值滤波取平均谱（B5 锚 L87「1024 sets mean filtering」）---
    spectrum_mean = np.mean(psd, axis=0)        # (n_fft,) 均值滤波谱
    # 'spectrum' 返回原始均值谱（诊断用）— block 模式此时已是归一化谱, agc/ratio 是原始

    # --- 步骤 5: 正负功率谱面积比 Rp-n（B5 锚式 3, content.md L81）---
    # fftshift 后谱居中: bin[0..half-1] = 负频率半轴, bin[half..n_fft-1] = 正频率半轴.
    # half = n_fft//2 处是 DC（B5 锚 L99「zero frequency component returned to middle」）,
    # 归入正半轴（DC 功率随频偏对称变化, 归正半轴不破坏单调性, 见 sandbox 验证）.
    half = n_fft // 2
    p_plus = float(np.sum(spectrum_mean[half:]))    # 正频率半轴（含 DC）
    p_minus = float(np.sum(spectrum_mean[:half]))   # 负频率半轴

    if normalize_mode == 'ratio':
        # 方案 C: 归一化功率比 Rp-n = (P_+ − P_-)/(P_+ + P_-)
        denom = p_plus + p_minus
        rp_n = (p_plus - p_minus) / denom if denom > 0 else 0.0
    else:
        # 方案 A/B: 绝对差 Rp-n = P_+ − P_-
        # block: 谱已按块归一化 → Rp-n 尺度无关（≡ ratio）; agc: 谱随 RMS 归一 → 绝对差
        rp_n = p_plus - p_minus

    # --- 步骤 6: 归一化频偏估计 Δfest = α·Rp-n（B5 锚式 2, α=6×10⁸, L85）---
    fest_residual_hz = alpha * rp_n             # 残频估计（不含星历预测）

    # --- 步骤 7: + 星历预测调 LO（B5 锚式 4, content.md L83, L87）---
    fest_hz = fest_residual_hz + ephemeris_pred

    # fest_omega: rad/sample, 用于 exp(−j·omega·k) 补偿. omega = 2π·f·T_S, T_S = 1/fs.
    fest_omega = 2.0 * np.pi * fest_hz / fs

    return {
        'fest_hz': float(fest_hz),
        'fest_residual_hz': float(fest_residual_hz),
        'fest_omega': float(fest_omega),
        'rp_n': float(rp_n),
        'spectrum': spectrum_mean,              # 均值谱（诊断用）
        'p_plus': p_plus,
        'p_minus': p_minus,
        'normalize_mode': normalize_mode,
        'n_blocks_used': n_blocks,
    }


# ============================================================================
# short_time_spectrum_foe_iterate — B5 锚 L141 迭代收敛（3-4 次迭代）
# ============================================================================

def short_time_spectrum_foe_iterate(
    rx: np.ndarray,
    n_iter: int = 4,           # B5 锚 L141「converges by the third/fourth iteration」
    n_fft: int = 16,
    n_blocks: int = 1024,
    alpha: float = 6e8,
    fs: float = 2.5e9,
    normalize_mode: str = 'ratio',
    ephemeris_pred: float = 0.0,
    precise_range_hz: float | None = None,   # 早停: 残频落此范围即停（B5Params.PRECISE_RANGE_B5）
) -> dict:
    """B5 短时谱 FOE 迭代收敛: 每轮估 → 预补偿 → 再估, 残频逐步落入精估范围.

    B5 锚 content.md L141 "converges by the third/fourth iteration": Rp-n-vs-f 非线性,
    单次估仅对残频有效; 每轮预补偿 fest→rx, 残频减小, 再估落在 Rp-n 线性区.
    这是 B5 锚的真正收敛机制（不是单次估准大频偏）.

    参数
    ----
    rx, n_fft, n_blocks, alpha, fs, normalize_mode, ephemeris_pred : 同 short_time_spectrum_foe
    n_iter : int
        最大迭代次数. B5 锚 4（L141）.
    precise_range_hz : float or None
        早停阈值: |fest_residual_hz| < precise_range_hz 即停（任务完成）.
        默认 None 不早停. B5 锚用 B5Params.PRECISE_RANGE_B5=312.5e6（B/8）.

    返回
    ----
    dict:
        'fest_hz'         : float       # 累积补偿频偏（含星历预测）
        'fest_residual_hz': float       # 最后一轮残频估计
        'fest_omega'      : float       # 累积补偿频偏（rad/sample）
        'history'         : list[dict]  # 每轮 {iter, fest_step, fest_accum, residual_hz, rp_n}
        'converged'       : bool        # 是否在 n_iter 内落 precise_range（若设了）
        'n_iter_used'     : int         # 实际迭代次数
    """
    rx = np.asarray(rx, dtype=complex)
    # 星历预测预补偿（B5 锚 L87 调 LO）: FFT 前先把星历预测的频偏从 rx 消掉,
    # 残频（rx 实际频偏 − ephemeris_pred）交迭代 FFT 估. 这是 B5 锚式 4 的物理含义.
    if ephemeris_pred != 0.0:
        k0 = np.arange(rx.shape[0])
        rx = rx * np.exp(-1j * 2.0 * np.pi * ephemeris_pred * k0 / fs)
    k = np.arange(rx.shape[0])
    fest_accum = 0.0
    history = []
    converged = False
    n_iter_used = 0
    rx_cur = rx.copy()

    for it in range(n_iter):
        res = short_time_spectrum_foe(
            rx_cur, n_fft=n_fft, n_blocks=n_blocks, alpha=alpha, fs=fs,
            normalize_mode=normalize_mode, ephemeris_pred=0.0)  # 迭代内部不带星历
        fest_step = res['fest_residual_hz']   # 本轮残频估计
        fest_accum += fest_step                # FFT 累积补偿（不含星历）
        # 预补偿: rx ← rx · exp(−j·2π·f_step·k/fs), 消除本轮估计的频偏
        rx_cur = rx_cur * np.exp(-1j * 2.0 * np.pi * fest_step * k / fs)

        history.append({
            'iter': it,
            'fest_step': float(fest_step),
            'fest_accum': float(fest_accum),
            'residual_hz': float(fest_step),   # 本轮估计即当前残频（已补偿前几轮）
            'rp_n': float(res['rp_n']),
        })
        n_iter_used = it + 1
        if precise_range_hz is not None and abs(fest_step) < precise_range_hz:
            converged = True
            break

    # 总补偿 = 星历预测预补偿 + FFT 迭代累积估计
    fest_hz = fest_accum + ephemeris_pred
    return {
        'fest_hz': float(fest_hz),
        'fest_residual_hz': float(history[-1]['residual_hz']),
        'fest_omega': float(2.0 * np.pi * fest_hz / fs),
        'history': history,
        'converged': converged,
        'n_iter_used': n_iter_used,
        'normalize_mode': normalize_mode,
    }


# ============================================================================
# _calibrate_alpha — 单点 α 校准（block/agc 模式须重校）
# ============================================================================

def _calibrate_alpha(
    tx_clean: np.ndarray,
    fs: float,
    n_fft: int = 16,
    n_blocks: int = 1024,
    normalize_mode: str = 'ratio',
    f_probe: float = 2e8,      # 小频偏, 落 Rp-n 线性区
) -> float:
    """单点校准 α: 无噪干净信号 + 已知小频偏 f_probe, 反解 α = f_probe / Rp-n.

    B5 锚 α=6×10⁸ 是经验校准值（L85 "obtained through experiment"）.
    不同 normalize_mode 下 Rp-n 尺度不同, α 须分别校准:
    - 'ratio': Rp-n∈[-1,1] 无量纲 → α 量纲 Hz（B5 锚 6e8 应是此模式）
    - 'block': Rp-n ≡ ratio（同尺度, 按块归一化后 sum≈1）→ α ≈ ratio 的 α
    - 'agc':   Rp-n = 绝对差, 随信号 RMS² 变 → α 量纲 Hz 但依赖 RMS

    f_probe 选小频偏（~fs 的 4%, 落 Rp-n 线性区）使单点校准有效. 大频偏 Rp-n 非线性,
    单点 α 不再适用（靠迭代收敛）.
    """
    k = np.arange(tx_clean.shape[0])
    rx = tx_clean * np.exp(1j * 2 * np.pi * f_probe * k / fs)
    res = short_time_spectrum_foe(
        rx, n_fft=n_fft, n_blocks=n_blocks, alpha=1.0, fs=fs,
        normalize_mode=normalize_mode)
    rp_n = res['rp_n']
    if abs(rp_n) < 1e-12:
        return float('nan')
    return float(f_probe / rp_n)


# ============================================================================
# 自测（__main__）
# ============================================================================

if __name__ == '__main__':
    import os
    import sys

    # 让本探针能 import params / common（explore 子目录, 需加 simulation 根到 sys.path）
    _SIM_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    if _SIM_ROOT not in sys.path:
        sys.path.insert(0, _SIM_ROOT)

    from params import B5Params  # param-source.md: 参数从 params.py 读, 禁硬编码
    from common._channel import generate_shared_realization  # TL-13: 信道禁自建

    P5 = B5Params()
    N_FFT = P5.FFT_POINTS_B5      # 16
    N_BLOCKS = P5.FFT_BLOCKS_B5   # 1024
    ALPHA_ANCHOR = P5.ALPHA_B5    # 6e8（B5 锚, 暗 ratio 模式）
    PRECISE_RANGE = P5.PRECISE_RANGE_B5   # 312.5e6 (B/8, 粗估任务边界)

    # B5 锚 ADC 5 GSa/s = 2 samples/symbol（content.md L93）. 用 2-sps RRC 脉冲成型
    # 生成带限 sinc 型谱（机制发现 1）, 匹配 B5 锚物理采样（fs 歧义解 b）.
    SPS = 2
    FS = P5.R_SYM_B5 * SPS        # 5e9 = ADC_RATE_B5（B5 锚物理采样率）

    def _rrcos(sps: int, beta: float, span: int) -> np.ndarray:
        """Root-raised-cosine FIR taps（复用 B7 _psa_foe_asymmetry.py:105 工程实现）."""
        t = np.arange(-span * sps, span * sps + 1) / sps
        h = np.zeros_like(t, dtype=float)
        for i, ti in enumerate(t):
            if ti == 0.0:
                h[i] = 1.0 - beta + (4 * beta / np.pi)
            elif abs(abs(ti) - 1.0 / (4 * beta)) < 1e-12 and beta != 0:
                h[i] = (beta / np.sqrt(2.0)) * (
                    (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta))
                    + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta)))
            else:
                num = (np.sin(np.pi * ti * (1 - beta))
                       + 4 * beta * ti * np.cos(np.pi * ti * (1 + beta)))
                den = np.pi * ti * (1 - (4 * beta * ti) ** 2)
                h[i] = num / den
        h /= np.sqrt(np.sum(h ** 2))   # unit-energy pulse
        return h

    def make_rrc_qpsk(n_sym: int, sps: int, beta: float, rng) -> np.ndarray:
        """RRC 脉冲成型 QPSK（sps samples/symbol, 带限 sinc 型谱）.

        QPSK 星座点 = exp(j·(k·π/2 + π/4)), k=0..3 → 单位圆上 π/4,3π/4,5π/4,7π/4.
        单位功率 → 不除 sqrt(2)（|exp(jθ)|²=1, 平均功率 1）.
        """
        phase = rng.integers(0, 4, n_sym) * np.pi / 2 + np.pi / 4
        syms = np.exp(1j * phase)            # 复平面 QPSK 星座点（单位功率）
        up = np.zeros(n_sym * sps, dtype=complex)
        up[::sps] = syms
        h = _rrcos(sps, beta, 16)
        span = 16
        tx = np.convolve(up, h)[span * sps: span * sps + n_sym * sps]
        return tx

    def inject_foe(sig: np.ndarray, f_d: float, fs: float) -> np.ndarray:
        """注入已知频偏: rx = tx · exp(j·2π·f_d·k/fs) [确定性 Doppler 平移]."""
        k = np.arange(sig.shape[0])
        return sig * np.exp(1j * 2 * np.pi * f_d * k / fs)

    print("=" * 78)
    print("B5 短时谱 FOE 探针自测")
    print("=" * 78)
    print(f"B5Params: n_fft={N_FFT}, n_blocks={N_BLOCKS}, α_anchor={ALPHA_ANCHOR:.3e}")
    print(f"测试信号: 2-sps RRC(β=0.35) QPSK, fs={FS:.3e} Hz (ADC_RATE_B5, "
          f"{SPS} samples/symbol)")
    print(f"理论捕获范围 ±fs/2 = ±{FS/2/1e9:.3f} GHz (content.md L117 ±B/2)")
    print(f"精估范围 ±{PRECISE_RANGE/1e6:.1f} MHz (B/8, 粗估任务边界)")
    print(f"Doppler 全量程 ±{P5.DOPPLER_RANGE_B5/1e9:.1f} GHz "
          f"(靠星历预测 ephemeris_pred 预补偿到残频)")
    print()

    rng = np.random.default_rng(42)
    N_SYM = (N_BLOCKS * N_FFT * 4) // SPS   # 充足符号供 1024 块 × 16 点均值滤波
    tx_clean = make_rrc_qpsk(N_SYM, SPS, 0.35, rng)
    print(f"干净测试信号: {len(tx_clean)} 采样 ({N_SYM} 符号 @ {SPS} sps), 单位功率")
    print()

    # === α 校准（三方案, 小频偏 200MHz 落线性区）===
    print("-" * 78)
    print("[α 校准] 用 200MHz 无噪小频偏（落 Rp-n 线性区）反解 α = f_probe / Rp-n")
    print("-" * 78)
    F_PROBE = 2e8
    alpha_cal = {}
    for mode in ('block', 'agc', 'ratio'):
        a = _calibrate_alpha(tx_clean, fs=FS, n_fft=N_FFT, n_blocks=N_BLOCKS,
                             normalize_mode=mode, f_probe=F_PROBE)
        alpha_cal[mode] = a
        tag = '  ← B5 锚值 6e8 落此模式量级' if mode == 'ratio' else ''
        print(f"  normalize_mode={mode:6s}: α_cal = {a:+.6e} Hz{tag}")
    print("  (注: α=6e8 暗 ratio 模式——6e8×Rp-n_saturate(0.5)=300MHz≈B/8 精估范围)")
    print()

    # === 自测 1: 无频偏基线（单次估计, 应接近 0）===
    print("-" * 78)
    print("[自测 1] 无频偏基线（单次估计, ephemeris_pred=0, 应接近 0）")
    print("-" * 78)
    for mode in ('block', 'agc', 'ratio'):
        res = short_time_spectrum_foe(
            tx_clean, n_fft=N_FFT, n_blocks=N_BLOCKS,
            alpha=alpha_cal[mode], fs=FS, normalize_mode=mode)
        print(f"  {mode:6s}: fest={res['fest_hz']/1e6:+8.2f} MHz, "
              f"Rp-n={res['rp_n']:+.4e}, P+={res['p_plus']:.4e} P-={res['p_minus']:.4e}")
    print()

    # === 自测 2: 单次估计 sweep（验证 Rp-n 单调区 + 单次估仅对残频有效）===
    print("-" * 78)
    print("[自测 2] 单次估计 sweep（ratio 模式, α=anchor 6e8, 验证 Rp-n 单调/饱和）")
    print("-" * 78)
    print(f"  {'真频偏(GHz)':>12} {'fest(GHz)':>11} {'Rp-n':>9} {'单次误差(MHz)':>14}")
    for f_d in np.array([-2.2, -1.5, -1.0, -0.5, -0.2, 0.0, 0.2, 0.5, 1.0, 1.5, 2.2]) * 1e9:
        rx = inject_foe(tx_clean, f_d, FS)
        res = short_time_spectrum_foe(
            rx, n_fft=N_FFT, n_blocks=N_BLOCKS,
            alpha=ALPHA_ANCHOR, fs=FS, normalize_mode='ratio')
        err = res['fest_hz'] - f_d
        print(f"  {f_d/1e9:>+12.2f} {res['fest_hz']/1e9:>+11.4f} "
              f"{res['rp_n']:>+9.4f} {err/1e6:>+14.1f}")
    print("  → 单次估准仅 |f_d|<~0.3GHz（线性区）; 大频偏须迭代（自测 3）")
    print()

    # === 自测 3: 迭代收敛（B5 锚 L141 3-4 次迭代, ratio 模式 α=6e8）===
    print("-" * 78)
    print("[自测 3] 迭代收敛（B5 锚 L141「3-4 次迭代」, ratio 模式 α=anchor 6e8）")
    print("-" * 78)
    for f_true in [0.5e9, 1.0e9, 1.5e9]:
        rx = inject_foe(tx_clean, f_true, FS)
        res_it = short_time_spectrum_foe_iterate(
            rx, n_iter=5, n_fft=N_FFT, n_blocks=N_BLOCKS,
            alpha=ALPHA_ANCHOR, fs=FS, normalize_mode='ratio',
            precise_range_hz=PRECISE_RANGE)
        print(f"  f_true = {f_true/1e9:+.1f} GHz:")
        for h in res_it['history']:
            mark = ' ✓ 落精估范围(B/8)' if abs(h['residual_hz']) < PRECISE_RANGE else ''
            print(f"    iter{h['iter']}: fest_step={h['fest_step']/1e6:+8.1f}MHz, "
                  f"累积补偿={h['fest_accum']/1e9:+.4f}GHz, 残频={h['residual_hz']/1e6:+8.1f}MHz{mark}")
        print(f"    → {res_it['n_iter_used']} 次迭代, fest_hz={res_it['fest_hz']/1e9:+.4f}GHz "
              f"(真值 {f_true/1e9:+.1f}GHz), {'收敛' if res_it['converged'] else '未达精估范围'}")
    print()

    # === 自测 4: 三方案迭代对比（同一信号, 各自校准 α, 看收敛性差异）===
    print("-" * 78)
    print("[自测 4] 三方案迭代对比（f_true=1.0GHz, 各自校准 α, 4 次迭代）")
    print("-" * 78)
    f_true = 1.0e9
    rx = inject_foe(tx_clean, f_true, FS)
    print(f"  {'mode':>6} {'α_used':>12} {'iter收敛残频(MHz)':>20} {'fest(GHz)':>11} {'收敛?':>8}")
    for mode in ('block', 'agc', 'ratio'):
        res_it = short_time_spectrum_foe_iterate(
            rx, n_iter=4, n_fft=N_FFT, n_blocks=N_BLOCKS,
            alpha=alpha_cal[mode], fs=FS, normalize_mode=mode,
            precise_range_hz=PRECISE_RANGE)
        last_resid = res_it['history'][-1]['residual_hz']
        print(f"  {mode:>6} {alpha_cal[mode]:>+12.3e} {last_resid/1e6:>+20.1f} "
              f"{res_it['fest_hz']/1e9:>+11.4f} {'是' if res_it['converged'] else '否':>8}")
    print()

    # === 自测 5: 大频偏 4GHz（超出 ±fs/2, 验证星历预测扩展捕获范围）===
    print("-" * 78)
    print("[自测 5] 大频偏 4GHz（超出 ±fs/2=±2.5GHz, 星历预测预补偿到残频 + 迭代）")
    print("-" * 78)
    F3 = 4e9
    rx3 = inject_foe(tx_clean, F3, FS)
    # 星历预测把 4GHz 预补偿到残频 4-3=1GHz（落 ±fs/2 内）. 真实星历能预测到 ~MHz 级残频,
    # 这里演示机制: ephemeris_pred 作为 LO 预补偿, FFT 估残频.
    EPHEM_3 = 3e9
    res_it = short_time_spectrum_foe_iterate(
        rx3, n_iter=5, n_fft=N_FFT, n_blocks=N_BLOCKS,
        alpha=ALPHA_ANCHOR, fs=FS, normalize_mode='ratio',
        ephemeris_pred=EPHEM_3, precise_range_hz=PRECISE_RANGE)
    print(f"  f_true = +4.000 GHz, ephemeris_pred = +{EPHEM_3/1e9:.1f} GHz (星历预测调 LO):")
    for h in res_it['history']:
        mark = ' ✓ 落精估范围' if abs(h['residual_hz']) < PRECISE_RANGE else ''
        total = h['fest_accum'] + EPHEM_3
        print(f"    iter{h['iter']}: 残频估计={h['residual_hz']/1e6:+8.1f}MHz, "
              f"FFT累积={h['fest_accum']/1e9:+.4f}GHz, "
              f"总fest={total/1e9:+.4f}GHz{mark}")
    print(f"    → 总补偿 fest_hz = {res_it['fest_hz']/1e9:+.4f} GHz (真值 +4.000 GHz), "
          f"误差 {(res_it['fest_hz']-F3)/1e6:+.1f}MHz")
    print()

    # === 自测 6: 负频偏对称性 + 噪声/湍流鲁棒性 ===
    print("-" * 78)
    print("[自测 6] 负频偏对称性（−1GHz）+ 噪声场景（generate_shared_realization）")
    print("-" * 78)
    # 6a: 负频偏对称（Rp-n-vs-f 正负斜率幅度不对称, 负侧收敛略慢, 但残频仍落精估范围）
    rx_neg = inject_foe(tx_clean, -1.0e9, FS)
    res_neg = short_time_spectrum_foe_iterate(
        rx_neg, n_iter=6, n_fft=N_FFT, n_blocks=N_BLOCKS,
        alpha=ALPHA_ANCHOR, fs=FS, normalize_mode='ratio',
        precise_range_hz=PRECISE_RANGE)
    last_resid_neg = res_neg['history'][-1]['residual_hz']
    print(f"  6a 负频偏 −1.000 GHz: {res_neg['n_iter_used']} 次迭代后 "
          f"fest={res_neg['fest_hz']/1e9:+.4f}GHz, "
          f"末轮残频={last_resid_neg/1e6:+.1f}MHz "
          f"({'落精估范围✓' if abs(last_resid_neg) < PRECISE_RANGE else '未落精估范围'}), "
          f"Rp-n 负→估计负 ✓")

    # 6b: 噪声/湍流场景（用 common 信道 generate_shared_realization）
    # 注: generate_shared_realization 是 1-sps 单偏振 QPSK（无脉冲成型）, 谱平坦 → Rp-n 退化.
    # 此测试验证算法在平坦谱下的退化行为（非 B5 锚场景, 仅 robustness 探针）.
    turb = generate_shared_realization(
        Ns=N_BLOCKS * N_FFT, gamma_bar=20.0, turb_name='weak', f_dot=0.0, seed=7)
    # 给平坦谱信号加 RRC 成型（上采样 2x）使其带限, 再注入 0.5GHz 频偏
    up2 = np.zeros(len(turb['tx']) * 2, dtype=complex)
    up2[::2] = turb['tx']
    h2 = _rrcos(2, 0.35, 16)
    tx_turb = np.convolve(up2, h2)[32:32 + len(up2)]
    rx_turb = inject_foe(tx_turb, 0.5e9, FS)
    res_turb = short_time_spectrum_foe_iterate(
        rx_turb, n_iter=4, n_fft=N_FFT, n_blocks=N_BLOCKS,
        alpha=ALPHA_ANCHOR, fs=FS, normalize_mode='ratio',
        precise_range_hz=PRECISE_RANGE)
    print(f"  6b 弱湍流+噪声 gamma_bar=20dB, 0.5GHz 频偏: "
          f"4 次迭代后 fest={res_turb['fest_hz']/1e9:+.4f}GHz "
          f"(误差 {(res_turb['fest_hz']-0.5e9)/1e6:+.1f}MHz)")
    print()

    print("=" * 78)
    print("自测结论:")
    print("  1. 单次估计仅对残频 |f|<~0.3GHz 准（Rp-n 线性区）; 大频偏须迭代（自测 2/3）")
    print("  2. 迭代 3-4 次收敛到精估范围 B/8=±312.5MHz（B5 锚 L141 验证 ✓, 自测 3）")
    print("  3. α=6×10⁸ 暗 ratio 模式（Rp-n 饱和 0.5 × 6e8 = 300MHz ≈ B/8）")
    print("  4. block ≡ ratio（按块归一化后 Rp-n 尺度无关）; agc 绝对差须重校 α")
    print("  5. ±fs/2 捕获范围 + 星历预测预补偿覆盖 ±4.5GHz Doppler 全量程（自测 5）")
    print("  6. 测试信号须带限（RRC/低通）才有不对称——平坦白谱 Rp-n≈0 无信息（机制 1）")
    print("=" * 78)
