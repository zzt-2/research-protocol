"""B7 OFC 2026 — 数值重建 Fig.1a: Gardner TED 增益 G(f_D) ↔ Doppler f_D 映射.

目的 (见 task brief):
  poster 文字声称 "Doppler 频偏 f_D 与 Gardner TED 增益之间存在周期性相关", Fig.1a
  (机制证据图) 在 PDF→md 转换中丢失. 本脚本用数值实验重建这张图, 判断周期性是否真实.

poster 关键参数 (content.md):
  - 25-Gbaud DP-QPSK, roll-off 0.1  (行 21, 47)
  - Doppler 扫频 0-23 GHz, 间隔 1 GHz  (行 49)
  - Gardner TED [6]=1986  (行 47, 引 6)
  - 增益定义 = "maximum value of the S-curve"  (行 25/37)
  - (−B, B) 内可逆映射  (行 37)

Gardner TED 公式 (task brief 指定, 标准 1986 复形式):
    e(k) = Re{ y(t-T/2) · [y*(t) − y*(t-T)] }
  y(t-T/2)=中间半采样点, y(t-T)=前一符号, y(t)=当前符号.
  (本地 Matlab 公式源 PSKTimingErrDetector.m L11-12 用去直流变种, 等价; 本脚本主用 brief 复形式)

方法 (确定性数值实验, 非蒙特卡洛):
  1. 单偏振 QPSK 符号 → RRC 成型 (α=0.1, sps_up=16 高速率以便精细扫 τ)
  2. 对每个 f_D: rx(t) = tx(t)·exp(j·2π·f_D·t)  (确定性频偏, 禁 np.random 撒 Doppler)
  3. 对每个 τ ∈ [0,T) (16 点) 算 E[e(τ)] (N_sym=1024 平均) → S-curve(τ; f_D)
  4. G(f_D) = max_τ |S-curve(τ; f_D)|  (兼报 max_τ S-curve, 看哪个呈周期)
  5. 画 G(f_D) vs f_D, FFT/自相关检测周期性

纪律:
  - 只在 explore/b7-gardner-ted-foe/ 写私有脚本, 不改 common/
  - 频偏用确定性 exp(j2πf_D t), 不撒随机
  - 时间预算 ≤15 min: N_sym=1024, sps_up=16, 扫频 ~55 点×2 条件
"""
import os
import sys
import json
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =============================================================================
# B7 参数 (content.md 行 21/47/49)
# =============================================================================
BAUD = 25e9              # 25 Gbaud (DP-QPSK, 单偏振验证机制)
T_SYM = 1.0 / BAUD       # 符号周期 40 ps
ROLLOFF = 0.1            # RRC roll-off (行 47)
SPS_UP = 16              # 高速率每符号样本数 (B7 实采 2 sps, 这里用 16 以便精细扫 τ)
OSNR_DUT = 17.0          # 主测点 OSNR 17 dB (行 49)
B_REF = 12.5e9           # OSNR 参考带宽 0.1 nm (光通信标准)

# 扫频配置 (对齐 poster)
F_SWEEP_COARSE = np.arange(0, 24, 1) * 1e9      # 0-23 GHz, 1 GHz 步进 (行 49)
F_SWEEP_FINE   = np.arange(0, 30, 1) * 0.1e9    # 0-2.9 GHz, 0.1 GHz 步进 (细节)
F_SWEEP_DIAG   = np.arange(0, 76, 1) * 1e9      # 0-75 GHz 诊断扫频 (≈3 个 baud-rate 周期, 供 FFT 测周期)

N_SYM = 1024            # 每频偏点符号数 (task brief 默认 1024)
TAU_N = 16              # τ 遍历一个符号周期的点数
N_NOISE_AVG = 6         # 噪声实现平均次数 (仅 OSNR 条件用; 降低单次实现方差, 使 G 曲线可信)


# =============================================================================
# RRC 成型滤波器 (自写, 不动 common/)
# =============================================================================
def rrc_filter(beta, span, sps):
    """平方根升余弦 (RRC) 脉冲成型滤波器冲激响应.

    标准 RRC 公式 (e.g. Proakis). span=符号数, sps=每符号样本.
    """
    N = span * sps + 1
    t = np.arange(N) - (N - 1) / 2.0
    x = t / sps
    h = np.zeros_like(x, dtype=float)
    eps = 1e-10
    for i, xi in enumerate(x):
        ax = abs(xi)
        if ax < eps:
            h[i] = 1.0 - beta + (4 * beta / np.pi)
        elif abs(ax - 1.0 / (4 * beta)) < eps or abs(ax + 1.0 / (4 * beta)) < eps:
            h[i] = (beta / np.sqrt(2)) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta))
                + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta))
            )
        else:
            num = np.sin(np.pi * (1 - beta) * xi) + 4 * beta * xi * np.cos(np.pi * (1 + beta) * xi)
            den = np.pi * xi * (1 - (4 * beta * xi) ** 2)
            h[i] = num / den
    h = h / np.sqrt(np.sum(h ** 2))   # 单位能量
    return h


# =============================================================================
# 发射信号生成 (确定性, 仅符号用一次随机种子)
# =============================================================================
def make_tx_signal(n_sym, seed=20260707):
    """QPSK 符号 → 上采样 → RRC 成型 → 高速率复信号. 返回 tx_high (功率归一化到 1)."""
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, n_sym * 2)
    syms = ((2 * bits[0::2] - 1) + 1j * (2 * bits[1::2] - 1)) / np.sqrt(2)
    # 上采样 (零插值) 到 SPS_UP
    up = np.zeros(n_sym * SPS_UP, dtype=complex)
    up[::SPS_UP] = syms
    # RRC 成型 (TX 侧)
    h = rrc_filter(ROLLOFF, span=8, sps=SPS_UP)
    tx_high = np.convolve(up, h, mode='same')
    # 功率归一化 (使 mean|tx|^2 = 1, 便于 OSNR 定标)
    P = np.mean(np.abs(tx_high) ** 2)
    tx_high = tx_high / np.sqrt(P)
    return tx_high


def apply_foe(tx_high, f_D):
    """确定性施加 Doppler 频偏: rx(t)=tx(t)·exp(j2πf_D·t). t=n·T_s_high, T_s_high=1/(B·SPS_UP)."""
    n = np.arange(len(tx_high))
    t = n / (BAUD * SPS_UP)
    return tx_high * np.exp(1j * 2 * np.pi * f_D * t)


def add_awgn(rx_high, osnr_db, real_idx=0):
    """按 OSNR(0.1nm) 加复 AWGN. 噪声功率在 B_REF=12.5GHz 内 = signal/10^(OSNR/10).
    复噪声方差 σ² = 10^(-OSNR/10)·(fs/B_REF), fs=B·SPS_UP (信号全带宽).
    real_idx 用于多次实现平均 (减少单次随机性对 G 估计的污染).
    """
    if osnr_db is None:
        return rx_high
    fs = BAUD * SPS_UP
    sigma2 = 10.0 ** (-osnr_db / 10.0) * (fs / B_REF)
    rng = np.random.default_rng(12345 + int(round(osnr_db * 100)) * 1000 + real_idx)
    noise = np.sqrt(sigma2 / 2.0) * (
        rng.standard_normal(len(rx_high)) + 1j * rng.standard_normal(len(rx_high))
    )
    return rx_high + noise


# =============================================================================
# Gardner TED S-curve 计算
# =============================================================================
def gardner_s_curve(rx_high, tau_n=TAU_N):
    """对 τ ∈ [0, T) 遍历, 算 E[e(τ)] (统计平均) → S-curve.

    Gardner e(k) = Re{ y_mid · (y_curr* − y_prev*) }
      y_prev = 符号 k-1 处样本, y_mid = 半符号处, y_curr = 符号 k 处.
    τ 以符号周期为单位 ∈ [0,1), 转样本偏移 = τ·SPS_UP.
    """
    L = len(rx_high)
    # 跳过首尾各 span 符号避免卷积边界
    margin = 2 * SPS_UP
    n_sym_avail = (L - 2 * margin) // SPS_UP - 1
    if n_sym_avail < 8:
        return np.zeros(tau_n)

    scurve = np.zeros(tau_n)
    for it, tau in enumerate(np.arange(tau_n) / tau_n):   # τ ∈ [0,1)
        off = int(round(tau * SPS_UP))
        e_acc = 0.0
        cnt = 0
        # 对每个符号 k: 采样点 (符号数→样本索引)
        #   prev_idx = (k-1)*SPS_UP + off
        #   mid_idx  =  (k-1)*SPS_UP + SPS_UP//2 + off   (= k*SPS_UP - SPS_UP/2 + off)
        #   curr_idx =  k*SPS_UP + off
        for k in range(1, n_sym_avail):
            i_prev = (k - 1) * SPS_UP + off + margin
            i_mid  = (k - 1) * SPS_UP + SPS_UP // 2 + off + margin
            i_curr = k * SPS_UP + off + margin
            y_prev = rx_high[i_prev]
            y_mid  = rx_high[i_mid]
            y_curr = rx_high[i_curr]
            e = np.real(y_mid * (np.conj(y_curr) - np.conj(y_prev)))
            e_acc += e
            cnt += 1
        scurve[it] = e_acc / max(cnt, 1)
    return scurve


def compute_gain(scurve):
    """G = max|S-curve| (主); 兼报 max S-curve (signed). 返回 dict."""
    return {
        'G_abs':  float(np.max(np.abs(scurve))),
        'G_signed': float(np.max(scurve)),
    }


# =============================================================================
# 扫频主循环
# =============================================================================
def sweep(f_list, tx_high, osnr_db, n_sym):
    """对 f_list 每个频偏算 G(f_D) + S-curve. 返回 dict 列表.
    OSNR 条件下做 N_NOISE_AVG 次噪声实现平均 (单次实现的随机性会污染 G 曲线,
    伪化周期性判断; 平均后得到稳定的 E[G])."""
    out = []
    n_avg = 1 if osnr_db is None else N_NOISE_AVG
    for f_D in f_list:
        rx0 = apply_foe(tx_high, f_D)
        scs = []
        for ri in range(n_avg):
            rx = add_awgn(rx0, osnr_db, real_idx=ri)
            scs.append(gardner_s_curve(rx))
        sc = np.mean(np.array(scs), axis=0)
        g = compute_gain(sc)
        g['f_D_Hz'] = float(f_D)
        g['f_D_GHz'] = float(f_D / 1e9)
        g['scurve'] = sc.tolist()
        g['n_noise_avg'] = n_avg
        out.append(g)
    return out


# =============================================================================
# 周期性分析
# =============================================================================
def analyze_periodicity(f_list_GHz, G_list):
    """FFT + 自相关检测周期性.
    返回: peak_freq_GHz (主频), period_GHz (=1/peak_freq), energy_ratio (主频能量占比),
          is_periodic (energy_ratio>0.5?), ac_period_GHz (自相关峰滞后), ac_mono(单调可逆?).
    """
    f = np.asarray(f_list_GHz)
    G = np.asarray(G_list)
    G = G - G.mean()                      # 去直流
    # FFT
    df = f[1] - f[0]
    N = len(G)
    spec = np.abs(np.fft.rfft(G)) ** 2
    freqs = np.fft.rfftfreq(N, d=df)      # cycles per GHz
    if len(spec) > 1:
        spec_no_dc = spec[1:]             # 去 DC
        freqs_no_dc = freqs[1:]
        peak_idx = int(np.argmax(spec_no_dc))
        peak_freq = freqs_no_dc[peak_idx]
        peak_power = spec_no_dc[peak_idx]
        total_power = float(np.sum(spec_no_dc))
        energy_ratio = peak_power / total_power if total_power > 0 else 0.0
        period = 1.0 / peak_freq if peak_freq > 0 else float('inf')
    else:
        peak_freq = 0.0
        period = float('inf')
        energy_ratio = 0.0
    is_periodic = bool(energy_ratio > 0.5)
    # 自相关 (全分辨率, 偏向 unbiased 前半)
    Gc = G - G.mean()
    ac = np.correlate(Gc, Gc, mode='full')[N - 1:]
    ac /= (ac[0] + 1e-30)
    # 找首个非零滞后峰 (周期估计)
    ac_period = None
    if len(ac) > 2:
        # 在滞后 > 1 个 df 中找最大
        peak_lag = 1 + int(np.argmax(ac[1:]))
        if ac[peak_lag] > 0.3:
            ac_period = float(f[peak_lag] - f[0])
    # 单调可逆检查: 在 (0, B) 内 G 是否单调 (用差分符号一致性)
    mono_sign = np.sign(np.diff(G))
    n_pos = int(np.sum(mono_sign > 0))
    n_neg = int(np.sum(mono_sign < 0))
    frac_dom = max(n_pos, n_neg) / max(len(mono_sign), 1)
    return {
        'peak_freq_per_GHz': float(peak_freq),
        'period_GHz': float(period) if np.isfinite(period) else None,
        'period_norm_B': float(period / 25.0) if np.isfinite(period) else None,
        'energy_ratio': float(energy_ratio),
        'is_periodic_FFT': is_periodic,
        'ac_period_GHz': ac_period,
        'ac_mono_dominant_frac': float(frac_dom),
    }


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    print("=" * 78)
    print("B7 OFC 2026 Fig.1a 重建 — Gardner TED 增益 G(f_D) ↔ Doppler f_D")
    print(f"  {BAUD/1e9:.0f}-Gbaud QPSK, roll-off {ROLLOFF}, SPS_UP={SPS_UP}, N_sym={N_SYM}")
    print("=" * 78)

    # OSNR→Es/N0 sanity print (归因标注: 推测性换算)
    fs = BAUD * SPS_UP
    sigma2 = 10.0 ** (-OSNR_DUT / 10.0) * (fs / B_REF)
    # 等效符号率 Es/N0: 信号功率1 over Rs=25GHz, 噪声PSD = sigma2/fs
    esn0_lin = 1.0 / (sigma2 / fs * BAUD)
    esn0_db = 10 * np.log10(esn0_lin)
    print(f"[OSNR 换算] OSNR={OSNR_DUT}dB(0.1nm) → 等效 Es/N0≈{esn0_db:.1f}dB "
          f"(推测换算: 噪声PSD×Rs; 仅供参考)")

    tx_high = make_tx_signal(N_SYM)
    print(f"[TX] 长度={len(tx_high)} 样本, 功率={np.mean(np.abs(tx_high)**2):.3f}")

    results = {
        'meta': {
            'baud_Hz': BAUD, 'roll_off': ROLLOFF, 'sps_up': SPS_UP,
            'n_sym': N_SYM, 'tau_n': TAU_N, 'n_noise_avg': N_NOISE_AVG,
            'osnr_main_dB': OSNR_DUT,
            'gardner_formula': "e(k)=Re{y_mid*(y_curr*-y_prev*)}",  # brief 复形式
            'note': '单偏振 QPSK 验证机制; 频偏确定性 exp(j2πf_D t)',
        },
        'curves': {},
    }

    for cond_name, osnr_db in [('no_noise', None), ('osnr17dB', OSNR_DUT)]:
        print(f"\n--- 条件: {cond_name} (OSNR={osnr_db}) ---")
        c = {}
        c['coarse'] = sweep(F_SWEEP_COARSE, tx_high, osnr_db, N_SYM)
        c['fine']   = sweep(F_SWEEP_FINE, tx_high, osnr_db, N_SYM)
        c['diag']   = sweep(F_SWEEP_DIAG, tx_high, osnr_db, N_SYM)
        results['curves'][cond_name] = c
        # 快速打印 coarse 曲线
        Gs = [d['G_abs'] for d in c['coarse']]
        print("  G_abs(f_D) coarse [0..23GHz]: " +
              ", ".join(f"{g:.3f}" for g in Gs))

    # 周期性分析 (用 diag 0-75GHz 扫频, 1GHz 步进, ~3 个 baud 周期)
    print("\n" + "=" * 78)
    print("周期性分析 (诊断扫频 0-75 GHz, FFT + 自相关)")
    print("=" * 78)
    analysis = {}
    for cond_name in ['no_noise', 'osnr17dB']:
        c = results['curves'][cond_name]
        f_GHz = [d['f_D_GHz'] for d in c['diag']]
        for gtype in ['G_abs', 'G_signed']:
            G = [d[gtype] for d in c['diag']]
            ana = analyze_periodicity(f_GHz, G)
            analysis[f'{cond_name}/{gtype}'] = ana
            print(f"  [{cond_name}/{gtype}] 主频={ana['peak_freq_per_GHz']:.4f}/GHz  "
                  f"周期={ana['period_GHz']} GHz (={ana['period_norm_B']}·B)  "
                  f"主频能量占比={ana['energy_ratio']*100:.1f}%  "
                  f"周期?{'是' if ana['is_periodic_FFT'] else '否'}  "
                  f"自相关周期={ana['ac_period_GHz']} GHz  "
                  f"单调主导占比={ana['ac_mono_dominant_frac']*100:.0f}%")
    results['analysis'] = analysis

    # 单调可逆 (在 0-23GHz poster 主测段, 用 G_abs)
    print("\n--- (−B,B) 可逆性 (poster 行 37): 0-23GHz 主测段 G_abs 单调性 ---")
    for cond_name in ['no_noise', 'osnr17dB']:
        c = results['curves'][cond_name]['coarse']
        G = np.array([d['G_abs'] for d in c])
        d = np.diff(G)
        n_pos = int(np.sum(d > 0)); n_neg = int(np.sum(d < 0))
        frac = max(n_pos, n_neg) / len(d)
        # 局部极值数 (越多越不可逆)
        n_turn = int(np.sum((np.sign(d[:-1]) * np.sign(d[1:])) < 0))
        print(f"  [{cond_name}] G_abs@0-23GHz: 升{n_pos}/降{n_neg} "
              f"主导占比={frac*100:.0f}%  转折点数={n_turn} "
              f"→ {'单调' if frac>0.8 and n_turn<=1 else '非单调'}")

    # 画图
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for col, cond_name in enumerate(['no_noise', 'osnr17dB']):
        c = results['curves'][cond_name]
        ax = axes[0, col]
        fh = [d['f_D_GHz'] for d in c['coarse']]
        ax.plot(fh, [d['G_abs'] for d in c['coarse']], 'o-', label='G=max|S-curve|', ms=4)
        ax.plot(fh, [d['G_signed'] for d in c['coarse']], 's--', label='G=max S-curve(signed)', ms=4)
        ax.set_xlabel('Doppler f_D (GHz)')
        ax.set_ylabel('TED gain')
        ax.set_title(f'{cond_name}: G(f_D) 0-23 GHz')
        ax.axvline(25, color='r', ls=':', alpha=0.5, label='B=25 GHz')
        ax.grid(True, alpha=0.3); ax.legend(fontsize=7)
        # S-curve 样本 (几个 f_D)
        ax2 = axes[1, col]
        for fd in [0, 5, 10, 15, 20]:
            d0 = c['coarse'][fd]
            tau = np.arange(TAU_N) / TAU_N
            ax2.plot(tau, d0['scurve'], '-o', ms=3,
                     label=f"f_D={fd} GHz")
        ax2.set_xlabel('timing offset τ/T')
        ax2.set_ylabel('E[e(τ)]')
        ax2.set_title(f'{cond_name}: S-curve(τ; f_D) 样本')
        ax2.grid(True, alpha=0.3); ax2.legend(fontsize=7)
    fig.suptitle('B7 OFC 2026 Fig.1a 重建: Gardner TED gain ↔ Doppler', fontsize=12)
    fig.tight_layout()
    png_path = os.path.join(os.path.dirname(__file__), '_b7_map_curve.png')
    fig.savefig(png_path, dpi=110)
    print(f"\n[保存图] {png_path}")

    json_path = os.path.join(os.path.dirname(__file__), '_b7_map_results.json')
    with open(json_path, 'w') as fh:
        json.dump(results, fh, indent=2)
    print(f"[保存数据] {json_path}")

    print(f"\n[耗时] {time.time()-t0:.1f} s")


if __name__ == '__main__':
    main()
