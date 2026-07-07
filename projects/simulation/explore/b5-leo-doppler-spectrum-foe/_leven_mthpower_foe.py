"""[60] Leven Mth-power 频偏估计器 (祖师爷对照, baseline 之一).

[60] Leven 2007 IEEE PTL "Frequency Estimation in Intradyne Reception"
(doi:10.1109/LPT.2007.891893) L55-65 算法 (前馈开环 feed-forward).

定位 (0.4.1): 祖师爷对照 — 经典频偏估计方法 (2007 Bell Labs), 任务环节为
*精细 FE* (前置于相位估计), 非主 baseline. 主 baseline 是传统 FFT FOE
(common.fft_foe). 本文件供 sandbox 三方对照 (C7) 用, MVE 通过才转正进 common.

C6 标注: PDF→md 公式 (content.md L39-51/L69-81) picture omitted, 从 L55-65
文字描述重建. Mth-power 频偏估计是经典无线算法 (Leven 引 [7] Meyr 1998 教材).

算法 ([60] Leven L55-65 重建):
  1. 符号差分: z[k] = r[k] · conj(r[k-1])  → 相位增量
  2. 去调制 (Mth-power): z[k]^M  (QPSK M=4, 数据差分相位×4 落到 2π 整数倍)
  3. 求和平均: s = Σ z[k]^M  (N_sum=500 样本, L57 "sample size of 500")
  4. 相位提取: Δφ = angle(s) / M  (除以 M 修正 M 次方)
  5. 频偏估计: Δf = Δφ / (2π·T_S)
  6. 补偿: φ_acc[k] = k·Δφ, r_comp[k] = r[k]·exp(−j·φ_acc[k])

捕获范围 ([60] Leven §VI L127): Mth-power 把相位平面切成 M 等分, 差分相位
窗口需落在 [−π/M, π/M] 内无歧义 → Δf ∈ [−fs/(2M), fs/(2M)].
QPSK M=4 @ 2.5GBaud → ±312.5 MHz (跟 B5 锚 PRECISE_RANGE_B5 同族).

纪律红线:
  - 前馈开环 (INVARIANT 13): [60] Leven 本身 feed-forward (L17), 不撞 D006
  - 公平对照: normalize_mode 跟 short_time_spectrum_foe 同方案 (block/agc/ratio),
    三方法都归一化保证公平 (0.4.1 §公平性保证)
  - 参数溯源: M/N_sum 从 [60] Leven 原文 L57, fs 从 B5Params.R_SYM_B5 (sandbox
    跟 B5 同场景 2.5GBaud 对比才公平, [60] Leven 原场景 10GBaud 不通用)
  - 信道禁自建 (TL-13): 自测用 common._channel.generate_shared_realization
  - explore 探针不进 common (红线 6): 文件放 explore 目录, _ 前缀
"""

import numpy as np


def _normalize(rx, mode):
    """前馈归一化预处理 (0.4.1 公平性保证, 三方法同方案).

    在符号差分 *之前* 对 rx 幅度归一化, 消除湍流致慢包络幅度起伏
    (_architecture_decision.md L106 "归一化是信号预处理, 不把湍流相位纳入环路 TF").

    三方案语义跟 short_time_spectrum_foe 对齐 (_file_organization.md L78-81):
      'block': 块内归一化 — 除以整段 RMS 功率 (消除块间整体幅度, 保留逐符号起伏)
      'agc':   AGC 前置 — 每符号幅度归一化到 1 (瞬时 AGC, 消除强湍流 fade)
      'ratio': 差分域归一化 — 差分后 |z| 归一 (只保留相位信息, 等价差分域瞬时 AGC)
               注: short_time_spectrum_foe 的 'ratio' 是功率谱面积比 Rp-n;
               Leven 无功率谱, 这里对齐为"差分后归一"保持三方案可比.
    """
    if mode == 'none':
        return rx
    if mode == 'block':
        p = np.sqrt(np.mean(np.abs(rx) ** 2))  # RMS 功率
        if p < 1e-12:
            return rx
        return rx / p
    if mode == 'agc':
        a = np.abs(rx)
        a[a < 1e-12] = 1e-12
        return rx / a  # 瞬时幅度 → 1
    if mode == 'ratio':
        # ratio 在差分域处理 (见 leven_mthpower_foe 内 z = z/|z|), 此处透传
        return rx
    raise ValueError(f"normalize_mode must be 'block'/'agc'/'ratio'/'none', got {mode!r}")


def leven_mthpower_foe(
    rx: np.ndarray,
    M: int = 4,
    N_sum: int = 500,
    fs: float = 2.5e9,
    normalize_mode: str = 'block',
):
    """[60] Leven Mth-power FOE: 符号差分 → M次方去调制 → N求和 → 相位/M → 频偏估计.

    [60] Leven 2007 IEEE PTL L55-65 算法 (前馈开环, C6 PDF→md 重建).

    参数
    ----
    rx : np.ndarray (complex, 1D)
        接收符号序列 (1 sample/symbol, 已时钟恢复).
    M : int, default 4
        PSK 阶数 (QPSK M=4). [60] Leven L55 "number of constellation points".
    N_sum : int, default 500
        求和样本数. [60] Leven L57 "sample size of 500".
    fs : float, default 2.5e9
        符号率 (B5Params.R_SYM_B5, sandbox 跟 B5 同场景).
    normalize_mode : str, default 'block'
        前馈归一化方案 ('block'/'agc'/'ratio'/'none'). 0.4.1 公平对照, 跟
        short_time_spectrum_foe 同方案.

    返回
    ----
    dict:
        'fest_hz'        : float  估计频偏 (Hz)
        'fest_omega'     : float  估计频偏 (rad/sample), = Δφ = 2π·fest_hz·T_S
        'delta_phi'      : float  连续样本间相位增量估计 (rad), = fest_omega
        'phi_acc'        : np.ndarray 累积相位偏移 φ_acc[k]=k·Δφ (rad), len=len(rx)
        'normalize_mode' : str    使用的归一化方案 (回显)
        'sum_complex'    : complex M次方求和结果 (诊断用)
        'M'              : int    去调制阶数 (回显)
        'N_sum'          : int    求和样本数 (回显)
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if N < 2:
        raise ValueError(f"len(rx)={N} 太短, 差分至少需 2 个样本")
    if M < 2:
        raise ValueError(f"M={M} 必须 >= 2 (PSK 阶数)")

    T_S = 1.0 / fs

    # ── 步骤 0: 前馈归一化 (0.4.1 公平性保证) ──────────────────
    rx_n = _normalize(rx, normalize_mode)

    # ── 步骤 1: 符号差分 ([60] Leven L55) ──────────────────────
    # z[k] = r[k] · conj(r[k-1]), 相位 = 载波相位增量 + 数据差分相位
    z = rx_n[1:] * np.conj(rx_n[:-1])  # len = N-1

    if normalize_mode == 'ratio':
        # 差分域归一化: z = z / |z|, 只保留相位信息 (对齐 short_time_spectrum ratio)
        za = np.abs(z)
        za[za < 1e-12] = 1e-12
        z = z / za

    # ── 步骤 2: Mth-power 去调制 ([60] Leven L55-57) ──────────
    # z^M 相位 = M × (载波相位增量 + 数据差分相位); QPSK M=4, 数据差分相位×4
    # 落到 2π 整数倍 → 相位消失, 只剩 M×载波相位增量
    z_M = z ** M

    # ── 步骤 3: 求和平均 ([60] Leven L57 "summed up over... 500 samples") ──
    n = min(N_sum, len(z_M))
    s = np.sum(z_M[:n])  # 复数相干求和 (噪声+残数据随机相位被平均掉)

    # ── 步骤 4: 相位提取, 除以 M ([60] Leven L65) ─────────────
    delta_phi = np.angle(s) / M  # 连续样本间相位增量估计 (rad)

    # ── 步骤 5: 频偏估计 ──────────────────────────────────────
    # Δf = Δφ / (2π·T_S)  ([60] Leven L37 "phase shift between two consecutive
    # samples ... caused by a frequency offset", sampling time T_S)
    fest_hz = delta_phi / (2.0 * np.pi * T_S)
    fest_omega = 2.0 * np.pi * fest_hz * T_S  # = delta_phi (rad/sample)

    # ── 步骤 6: 累积相位补偿 ([60] Leven L67-83) ──────────────
    # φ_acc[k] = k · Δφ, r_comp[k] = r[k]·exp(−j·φ_acc[k])
    k = np.arange(N, dtype=float)
    phi_acc = k * delta_phi

    return {
        'fest_hz': fest_hz,
        'fest_omega': fest_omega,
        'delta_phi': delta_phi,
        'phi_acc': phi_acc,
        'normalize_mode': normalize_mode,
        'sum_complex': s,
        'M': M,
        'N_sum': N_sum,
    }


def capture_range_hz(fs, M=4):
    """[60] Leven Mth-power 无歧义捕获范围 (±fs/(2M)).

    [60] Leven §VI L127: Mth-power 把相位平面切 M 等分, 差分相位窗口需落
    [−π/M, π/M] 无歧义 → Δf ∈ [−fs/(2M), fs/(2M)].
    QPSK M=4 @ 2.5GBaud → ±312.5 MHz.
    """
    return fs / (2.0 * M)


# ════════════════════════════════════════════════════════════════
# 自测 ([60] Leven 捕获范围小, 只测 ±300MHz 内, 不测 4GHz 超范围)
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    import os
    import sys

    # 信道 import (TL-13: 禁自建, 用 common._channel)
    _sim_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if _sim_root not in sys.path:
        sys.path.insert(0, _sim_root)
    from common._channel import generate_shared_realization

    np.random.seed(0)

    # ── 测试参数 (sandbox 跟 B5 同场景 2.5GBaud/QPSK) ──────────
    FS = 2.5e9              # B5Params.R_SYM_B5
    T_S = 1.0 / FS
    M = 4                   # QPSK
    N_SUM = 500             # [60] Leven L57
    NS = 8000               # 符号数 (> N_sum, 给求和留余量)
    GAMMA = 100.0           # 20 dB SNR (B5Params.GAMMA_BAR_DEFAULT)
    MODES = ['block', 'agc', 'ratio']

    cap_range = capture_range_hz(FS, M)
    print("=" * 72)
    print("[60] Leven Mth-power FOE 自测")
    print(f"  场景: QPSK / {FS/1e9:.1f} GBaud / Ns={NS} / N_sum={N_SUM} / γ̄={GAMMA}")
    print(f"  捕获范围 (理论 ±fs/(2M)): ±{cap_range/1e6:.2f} MHz")
    print("=" * 72)

    def _make_test_signal(df_hz, turb='weak', f_dot=0.0, seed=42):
        """用 common 信道生成 QPSK, 叠加纯净频率偏移 df_hz.

        channel.phi 已含 f_res(1MHz)+f_dot+线宽, 这里再叠一层已知 Δf 做测试.
        f_dot=0 关掉多普勒变化率 (测纯恒定频偏, 避免二次相位污染差分).
        """
        d = generate_shared_realization(
            Ns=NS, gamma_bar=GAMMA, turb_name=turb, f_dot=f_dot, seed=seed)
        rx = d['rx_raw']
        # 加已知频偏: rx * exp(j·2π·Δf·k·T_S)
        k = np.arange(NS)
        if df_hz != 0.0:
            rx = rx * np.exp(1j * 2 * np.pi * df_hz * k * T_S)
        return rx, d

    # ── 测试 1: 无频偏基线 (期望 fest ≈ 0) ─────────────────────
    print("\n[测试 1] 无频偏基线 (df=0, 弱湍流, f_dot=0)")
    print(f"  {'mode':<8} {'fest_hz (MHz)':>16} {'|fest| (MHz)':>14} {'err (MHz)':>12}")
    for mode in MODES:
        rx, _ = _make_test_signal(0.0)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode=mode)
        err = r['fest_hz'] - 0.0
        print(f"  {mode:<8} {r['fest_hz']/1e6:>16.4f} {abs(r['fest_hz'])/1e6:>14.4f} {err/1e6:>12.4f}")

    # ── 测试 2: 已知频偏 100 MHz (期望 fest ≈ 100MHz, 在范围内) ─
    print("\n[测试 2] 已知频偏 100 MHz (范围内, 弱湍流, f_dot=0)")
    DF = 100e6
    print(f"  {'mode':<8} {'fest_hz (MHz)':>16} {'err (MHz)':>12} {'rel_err (%)':>12}")
    for mode in MODES:
        rx, _ = _make_test_signal(DF)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode=mode)
        err = r['fest_hz'] - DF
        rel = abs(err) / DF * 100
        print(f"  {mode:<8} {r['fest_hz']/1e6:>16.4f} {err/1e6:>+12.4f} {rel:>12.3f}")

    # ── 测试 3: 边界频偏 300 MHz (接近 ±312.5MHz 边界) ─────────
    print("\n[测试 3] 边界频偏 300 MHz (接近 ±312.5MHz 边界, 弱湍流, f_dot=0)")
    DF = 300e6
    print(f"  {'mode':<8} {'fest_hz (MHz)':>16} {'err (MHz)':>12} {'rel_err (%)':>12}")
    for mode in MODES:
        rx, _ = _make_test_signal(DF)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode=mode)
        err = r['fest_hz'] - DF
        rel = abs(err) / DF * 100
        print(f"  {mode:<8} {r['fest_hz']/1e6:>16.4f} {err/1e6:>+12.4f} {rel:>12.3f}")

    # ── 测试 4: 湍流强度对比 (100MHz, weak/moderate/strong) ─────
    print("\n[测试 4] 湍流强度对比 (100MHz 频偏, f_dot=0, normalize=block)")
    print(f"  {'turb':<10} {'fest_hz (MHz)':>16} {'err (MHz)':>12}")
    for turb in ['weak', 'moderate', 'strong']:
        rx, _ = _make_test_signal(100e6, turb=turb)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode='block')
        err = r['fest_hz'] - 100e6
        print(f"  {turb:<10} {r['fest_hz']/1e6:>16.4f} {err/1e6:>+12.4f}")

    # ── 测试 5: 多 seed 统计 (100MHz, block, 弱湍流, 10 seed) ───
    print("\n[测试 5] 多 seed 统计 (100MHz, block, 弱湍流, f_dot=0, 20 seed)")
    ests = []
    for sd in range(20):
        rx, _ = _make_test_signal(100e6, seed=sd + 100)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode='block')
        ests.append(r['fest_hz'])
    ests = np.array(ests)
    print(f"  mean = {ests.mean()/1e6:.4f} MHz")
    print(f"  std  = {ests.std()/1e6:.4f} MHz")
    print(f"  bias = {(ests.mean() - 100e6)/1e6:+.4f} MHz")
    print(f"  max|err| = {np.max(np.abs(ests - 100e6))/1e6:.4f} MHz")

    # ── 测试 6: 捕获范围实测扫描 (找实际无歧义边界) ─────────────
    print("\n[测试 6] 捕获范围实测扫描 (block, 弱湍流, 找实际无歧义边界)")
    print(f"  理论 ±fs/(2M) = ±{cap_range/1e6:.2f} MHz")
    print(f"  {'df (MHz)':>10} {'fest (MHz)':>12} {'status':<16}")
    for df_mhz in [50, 100, 150, 200, 250, 300, 312.5, 350, 400]:
        df = df_mhz * 1e6
        rx, _ = _make_test_signal(df)
        r = leven_mthpower_foe(rx, M=M, N_sum=N_SUM, fs=FS, normalize_mode='block')
        fest = r['fest_hz']
        if df_mhz <= 312.5:
            ok = abs(fest - df) < 0.1 * df + 5e6  # 10% 或 5MHz 容差
            status = "OK" if ok else "DRIFT"
        else:
            # 超范围: 期望折叠 (angle 模 2π/M) → fest 会跳到另一值
            status = "超范围(折叠)"
        print(f"  {df_mhz:>10.1f} {fest/1e6:>12.3f} {status:<16}")

    print("\n" + "=" * 72)
    print("自测完成. 捕获范围实测见测试 6.")
    print("=" * 72)
