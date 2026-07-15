"""载波恢复基线：FFT-FOE, DPLL, VV-CPR, BPS"""
import numpy as np

from ._config import T_S, DEF_B_BPS, DEF_NW_BPS, FIXED_CFG
from ._modulation import hard_decision


def dpll_track_dd(rx, omega_n=8e6, zeta=np.sqrt(2)/2, mod='qpsk'):
    """DD (decision-directed) DPLL for QPSK and 16-QAM.
    Uses hard decision to remove modulation instead of 4th-power."""
    wT = min(omega_n * T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        rotated = rx[k] * np.exp(-1j * vco_phase)
        # DD: hard decision
        if mod == 'qpsk':
            dec = (np.sign(np.real(rotated)) + 1j * np.sign(np.imag(rotated))) / np.sqrt(2)
        else:  # qam16
            s = rotated * np.sqrt(10)
            di = np.clip(np.round((np.real(s)+3)/2)*2-3, -3, 3)
            dq = np.clip(np.round((np.imag(s)+3)/2)*2-3, -3, 3)
            dec = (di + 1j * dq) / np.sqrt(10)
        # Phase error from decision
        pd_out = np.angle(rx[k] * np.exp(-1j * vco_phase) * np.conj(dec))
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est


def fft_foe(rx, N_fft=1024, nfft_zp=8192):
    N_fft = min(N_fft, len(rx))
    seg = rx[:N_fft]
    r4 = seg**4
    win = np.hanning(N_fft)
    r4w = r4 * win
    R4 = np.fft.fftshift(np.fft.fft(r4w, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    idx = np.argmax(np.abs(R4))
    if 1 <= idx < len(R4) - 1:
        a_v, b_v, g_v = np.abs(R4[idx-1]), np.abs(R4[idx]), np.abs(R4[idx+1])
        if b_v - a_v > 0 and b_v + a_v - 2*g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2*b_v + g_v)
            f_est_norm = (freqs[idx] + p * (freqs[1] - freqs[0]))
        else:
            f_est_norm = freqs[idx]
    else:
        f_est_norm = freqs[idx]
    f_est_norm /= 4
    return 2 * np.pi * f_est_norm


def dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2):
    wT = min(omega_n * T_S, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        mixed = rx[k] * np.exp(-1j * vco_phase)
        m4 = mixed**4
        pd_out = np.angle(m4) / 4
        integrator += c2 * pd_out
        freq_out = c1 * pd_out + integrator
        vco_phase += freq_out
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est


def vv_cpr(rx, Nw=64):
    M = 4
    raised = rx**M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg)) / M
    return rx * np.exp(-1j * pe), pe


def bps_cpr(rx, B=DEF_B_BPS, Nw=DEF_NW_BPS, mod='qpsk'):
    """Blind Phase Search (Pfau 2009, JLT)

    B 个测试相位，Nw 符号滑动窗口平均距离度量。
    使用 M=4 相位模糊展开解决 QPSK 模糊。
    mod: 'qpsk' or 'qam16' decision function.
    """
    N = len(rx)
    phases = 2 * np.pi * np.arange(B) / B

    # 向量化计算所有测试相位的距离度量
    rotated = rx[np.newaxis, :] * np.exp(-1j * phases[:, np.newaxis])
    dec = hard_decision(rotated, mod=mod)
    dist = np.abs(rotated - dec)**2
    metrics = dist / (np.abs(dec)**2 + 1e-10) if mod != 'qpsk' else dist

    # 滑动窗口平均
    ker = np.ones(Nw) / Nw
    for b in range(B):
        metrics[b] = np.convolve(metrics[b], ker, mode='same')

    best_b = np.argmin(metrics, axis=0)
    pe_raw = phases[best_b]

    # M=4 相位模糊展开：乘 4 → unwrap 2π 跳变 → 除 4
    pe = np.unwrap(4 * pe_raw) / 4

    return rx * np.exp(-1j * pe), pe


def carrier_recovery_fixed(rx, cfg=None):
    if cfg is None:
        cfg = FIXED_CFG
    fo_est = fft_foe(rx, N_fft=cfg['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=cfg['omega_n'], zeta=cfg['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=cfg['M_vv'])
    return rx_cpr


# =============================================================================
# Step 4a 维度 D MVE 估计器（B11/B7 锚方法 + baseline）
# 接口对齐 fft_foe/vv_cpr/bps_cpr：接收 rx 复数数组, 返回补偿后 rx + 估计量。
# =============================================================================

def da_ml_recovery(rx, pilot_idx, pilot_sym, mod='m16apsk'):
    """DA ML 估计器 (Decision-Aided / Pilot-Aided ML) — B11 baseline.

    来源: Cao 2012 PTL [B11 ref 10] decision-aided pilot-aided ML, 单 pilot 符号。
    数学: 给定 pilot 在位置 n_p, 接收 r(n_p) = pilot_sym · exp(j(φ + 2π·Δf·n_p·T_s))。
    多 pilot 时用最小二乘（线性回归相位 vs 时间）闭式估 (φ, Δf):
        θ_p = angle(r(n_p) / pilot_sym)  →  θ_p ≈ φ + 2π·Δf·n_p·T_s
        Δf̂ = Cov(n, θ)/Var(n)/(2π·T_s),  φ̂ = mean(θ) − 2π·Δf̂·mean(n)·T_s
    返回 (rx_compensated, phi_est, df_est)。单 pilot 时退化为仅估 CPE（Δf=0）。

    参数溯源: pilot 间距/位置由调用方（MVE 脚本）按 B11 帧结构给, 此处 generic。
    """
    rx = np.asarray(rx, dtype=complex)
    pilot_idx = np.atleast_1d(np.asarray(pilot_idx))
    pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))
    n_p = pilot_idx.astype(float)
    # 观测相位（去调制后）
    theta = np.unwrap(np.angle(rx[pilot_idx] / pilot_sym))
    if len(n_p) >= 2:
        # 线性回归 θ = φ + 2π·Δf·n·T_s （用原始 t, 非中心化, 才能正确取 φ 截距 @ n=0）
        t = n_p * T_S
        cov = np.mean(t * theta) - t.mean() * theta.mean()
        var = np.mean(t**2) - t.mean()**2
        slope = cov / var if var > 0 else 0.0          # dθ/dt = 2π·Δf
        df_est = slope / (2 * np.pi)
        phi_est = theta.mean() - slope * t.mean()      # 截距 @ n=0 = φ
    else:
        # 单 pilot: 仅估 CPE, Δf 不可分离 → 置 0
        df_est = 0.0
        phi_est = float(theta[0])
    n_all = np.arange(len(rx))
    rx_comp = rx * np.exp(-1j * (phi_est + 2*np.pi*df_est*T_S * n_all))
    return rx_comp, phi_est, df_est


def nda_ml_recovery(rx, M0, mod='m16apsk', N_fft=None, assume_df_zero=False,
                    intra_block_tracking='none'):
    """NDA-ML 估计器（盲, 升 M₀ 次幂去调制 + 单正弦 ML）— B11 锚方法.

    来源: B11 (10.1109_LPT.2024.3523478) 行 75-121 + Wang 2022 T-SP [B11 ref 13] 单正弦 ML。
    数学（3 步）:
      (1) rx 升 M₀ 次幂去调制相位: rx^M₀ = |rx|^M₀ · exp(j·M₀·(2πτk/N + φ + 2πΔf·k·T_s))·noise
          （M₀ξ(k) 为 2π 整数倍 → 零相位, B11 行 75-77）。
      (2) 升幂后信号相位是 k 的线性函数 → 单复正弦的频率+相位估计:
          用 FFT 找频率（仿 fft_foe 的 Quinn-Rife 插值）, 再线性回归估相位。
      (3) 解卷绕: 除以 M₀ 后 unwrap。
    注: B11 用 genie-aided 解卷绕（行 129-131）; MVE 不能用 oracle, 此处用 np.unwrap +
        M₀ 相位模糊（2π/M₀ 整数倍歧义, 注释标明, resolve_* 另行消除 BER 模糊）。

    参数溯源: M₀=8 对 8PSK/(8,8)-16APSK（B11 行 75-77, params.py M0_POWER=8）。
    返回 (rx_compensated, tau_est, phi_est, df_est)。

    Parameters
    ----------
    assume_df_zero : bool
        If True, skip FFT-df estimation (assume CFO pre-compensated). Use mean-angle
        of rx^M0 to estimate CPE only. 来源: B11 行 33 假设 (湍流/Doppler/CFO 已补偿,
        信道仅 AWGN + 线宽 PN, 真 Δf=0). 在 df=0 时 FFT-df 会锁到噪声伪峰（实测
        df_est≈188 kHz, 本应 0）, 该伪 df 经线性回归 φ 步骤拟合留下块内残余相位斜坡
        → BER 损失; 故 df=0 场景应跳过 FFT-df, 直接估常相位 CPE（B11 场景单常相位足够）。
        If False (default, 未来星地 Doppler 残余场景), keep FFT-df logic（Wang 2022 单正弦 ML）。
    intra_block_tracking : str
        块内相位跟踪模式 (仅 assume_df_zero=True 分支生效; per-scenario 自适应).
        - 'none' (默认): 整块 mean-angle → 块常数 CPE. 湍流场景用此 (sandbox 显示
          segK8 在 strong 湍流有害). 向后兼容.
        - 'segmented': segK8 块内分段跟踪 (sandbox 验证 NDA-segK8). 切 K=8 段 (256/8=32
          符号/段) 每段独立升幂 mean-angle, 段间 unwrap + 线性插值得逐符号相位轨迹.
          AWGN 场景用此 (sandbox: AWGN @18dB 反超 BPS ~1dB). 数学 bit-exact 复制自
          explore/nda-awgn-tracking-sandbox/experiment.py:nda_ml_segmented.
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    k = np.arange(N)
    if assume_df_zero:
        # Variant B (修复 Bug 1): 跳 FFT-df, 纯升幂 mean-angle 估常相位 CPE.
        # 来源: 诊断脚本 _awgn_repro_diagnostic.py nda_ml_fixed_ber (Variant B).
        # B11 行 33 假设 CFO 已补偿 → 真 df=0 → FFT 找频率会锁噪声伪峰 → 残余相位斜坡.
        raised = rx ** M0
        if intra_block_tracking == 'segmented':
            # segK8 块内跟踪 (sandbox 验证): 切 K 段每段独立 mean-angle, 段间 unwrap+线性插值.
            # 数学 bit-exact 复制自 explore/nda-awgn-tracking-sandbox/experiment.py:nda_ml_segmented.
            # 追块内 Wiener PN 漂移 (σ²_φ=2π·CLW·T_S·N_block≈0.032 rad/块 → high-SNR BER floor).
            K = 8  # 溯源: sandbox 实验最优, 256/8=32 符号/段
            seg_len = N // K
            seg_phi = np.empty(K)
            seg_center = np.empty(K)
            for k in range(K):
                lo, hi = k * seg_len, (k + 1) * seg_len
                seg_phi[k] = np.angle(raised[lo:hi].mean())    # 段内常相位近似
                seg_center[k] = (lo + hi) / 2.0
            seg_phi_unw = np.unwrap(seg_phi)                    # 段间可能跨 2π
            t = np.arange(N)
            phi_raised = np.interp(t, seg_center, seg_phi_unw)  # 逐符号相位轨迹
            phi_est = phi_raised / M0
        else:
            # 原版: 整块 mean-angle → 块常数 CPE (intra_block_tracking='none' 默认, 向后兼容).
            phi_raised = np.angle(raised.mean())
            phi_est = phi_raised / M0
        df_est = 0.0           # B11 行 33: 真 df=0, 不估频率
        tau_est = 0.0
        rx_comp = rx * np.exp(-1j * phi_est)
        return rx_comp, tau_est, phi_est, df_est
    # --- 现有 FFT-df 逻辑（assume_df_zero=False, 默认, 未来 Doppler 残余场景）---
    if N_fft is None:
        N_fft = min(N, 4096)
    N_fft = min(N_fft, N)
    # (1) 升 M₀ 次幂去调制
    raised = rx ** M0
    seg = raised[:N_fft]
    win = np.hanning(N_fft)
    # (2a) FFT 找频率（单复正弦的 freq 估计）
    R = np.fft.fftshift(np.fft.fft(seg * win, n=N_fft * 8))
    freqs = np.fft.fftshift(np.fft.fftfreq(N_fft * 8, d=T_S))
    idx = np.argmax(np.abs(R))
    if 1 <= idx < len(R) - 1:
        a_v, b_v, g_v = np.abs(R[idx-1]), np.abs(R[idx]), np.abs(R[idx+1])
        if b_v + a_v - 2*g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2*b_v + g_v)
            df_raised = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            df_raised = freqs[idx]
    else:
        df_raised = freqs[idx]
    # 升幂后频率 = M₀·Δf → 还原
    df_est = df_raised / M0
    # (2b) 去频率后线性回归估相位（解 M₀ 次幂后的常相位）
    raised_def = raised * np.exp(-1j * 2*np.pi*df_raised * k * T_S)
    theta = np.unwrap(np.angle(raised_def))
    t = k * T_S
    cov = np.mean(t * theta) - t.mean() * theta.mean()
    var = np.mean(t**2) - t.mean()**2
    slope = cov / var if var > 0 else 0.0
    phi_raised = theta.mean() - slope * t.mean()
    # (3) 解卷绕: 除以 M₀（M₀ 相位模糊: φ̂ + 2π·m/M₀, m∈Z, 由 resolve_* 消除）
    phi_est = phi_raised / M0
    tau_est = 0.0  # STO 在 B11 OFDM 频域线性相位模型; 单载波时序此处不分离, 标 0
    rx_comp = rx * np.exp(-1j * (phi_est + 2*np.pi*df_est*T_S * k))
    return rx_comp, tau_est, phi_est, df_est


def lmmse_recovery(rx, snr_db, M0=8, L=5, sigma2_p=None, mod='m16apsk',
                   assume_df_zero=True):
    """LMMSE 载波相位估计 (average-energy 简化版) — #15 JPhoto baseline.

    ⚠️ DEPRECATED (2026-07-08): 复现验证发现高 SNR BER floor (LMMSE @20dB BER 0.018
    vs NDA-ML 7.5e-4, 差 24 倍). 根因: #15 论文 PDF→md 转换把 eq(5)(6)(7) 的 R/p 闭式
    公式丢了 (picture intentionally omitted), 此处 R/p 矩阵靠文字描述+物理推导重建,
    缺关键细节 (AOPN 方差升幂后精确表达 / p 向量噪声修正项). 调 4 种变体均不对.
    用户决策 (2026-07-08): 放弃 LMMSE 实测, 切方案 C 用 VV/BPS 经典 baseline. 本函数
    保留作教训, 不准调用. 如要恢复, 先查 [13] Wang 2022 T-SP 原始 LMMSE 公式拿 R/p 闭式.
    详见 verify/lmmse_repro_check.py + decisions.md D-008 (待建).
    """
    # ⚠️ DEPRECATED: 见 docstring 警告
    """LMMSE 载波相位估计 (average-energy 简化版) — #15 JPhoto baseline.

    来源: Wang et al. 2024 IEEE Photonics J "V&V Carrier Phase Estimation for
          Multi-Ring M-APSK with Wiener Phase Noise and Its Performance"
          DOI: 10.1109/JPHOT.2024.3415635, eq (3)-(4)+(10)-(12) avg-energy 版.
    核心方法: 升 M₀ 次幂去调制 + 窗 2L+1 内 LMMSE 权重 w=R⁻¹p (针对 Wiener PN
              + AWGN 双统计优化). 与 nda_ml_recovery 同属 NDA M₀ 次幂框架,
              差异: nda_ml 用 mean-angle (块常数), LMMSE 用 R⁻¹p 加权窗
              (针对 Wiener PN 的近最优权重). avg-energy 简化: AOPN 方差
              σ²_ε = N₀/(2E_s) 全程常数 → R/p 预算一次 O(W³), 滑窗 O(W·N).

    数学:
      升幂归一化: yM(k) = (r(k)/|r(k)|)^M₀ = exp(jM₀θ(k)) + 升幂噪声
      窗 2L+1 观测: yM_win = [yM(k-L), ..., yM(k+L)]^T
      LMMSE 估计: V̂M(k) = w^H · yM_win,  θ̂(k) = angle(V̂M(k))/M₀
      权重: w = R⁻¹·p
        R 自相关 (W×W), (x,y) 元素:
          d = |x-y|
          R[x,y] = exp(-M₀²·σ²_p·d/2) · (1 + σ²_ε·M₀²·δ_{d,0})
          (Wiener 相位差 d 步衰减 + 升幂后 AWGN 在同点 M₀² 倍方差)
        p 互相关 (W×1), l 元素 (中心=L):
          p[l] = exp(-M₀²·σ²_p·|l-L|/2)  (中心=1 向两侧衰减)
        σ²_p = 2π·Δν·T_s (Wiener PN 每符号方差, params SIGMA2_P)
        σ²_ε = 1/(2·10^(snr_db/10))  (avg-energy AOPN, 论文 eq 12)

    边界处理: k<L 或 k>N-1-L 用 edge-padding (复制边缘样本).

    参数溯源:
      M₀=8: (8,8)-16APSK LCM(8,8)=8 (同 nda_ml, 论文 line 79)
      L=5: 论文推荐 memory length (Fig.3-8 主用, line 223 "L=5 更适于多环")
      σ²_p: 默认 None → 从 _b11_params.SIGMA2_P 取 (params LASER_LW 派生)

    与 nda_ml_recovery 接口对齐: 返回 (rx_comp, tau_est, phi_est, df_est).
    assume_df_zero=True (默认): 跳 FFT-df, 纯 CPE 估计 (对齐主实验调用约定).

    References
    ----------
    [15] Q. Wang et al., "V&V CPE for Multi-Ring M-APSK with Wiener PN,"
         IEEE Photonics J., vol. 16, no. 4, art. 7201408, Aug. 2024.
    [13] (LMMSE M-PSK 原始推导, [15] 引用) Wang 2022 IEEE T-SP.
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)

    # --- 参数解析 ---
    if sigma2_p is None:
        # 从 _b11_params 取 (守 D-007 单一真相源), 延迟 import 避免循环
        try:
            from ..simulator._b11_params import SIGMA2_P as _S2P
            sigma2_p = float(_S2P)
        except Exception:
            sigma2_p = 2.51e-5  # fallback: 10kHz@2.5GBaud 派生值 (params.py)

    snr_lin = 10.0 ** (snr_db / 10.0)
    sigma2_eps = 1.0 / (2.0 * snr_lin)            # avg-energy AOPN, 论文 eq(12)
    W = 2 * L + 1                                  # 窗长

    # --- 预算 R/p (avg-energy 全程常数, 算一次) ---
    idx = np.arange(W)
    d = np.abs(idx[:, None] - idx[None, :])        # (W,W) 距离矩阵
    # R[x,y]: Wiener 衰减 × (1 + 升幂 AWGN 在 d=0 加项)
    R = np.exp(-M0**2 * sigma2_p * d / 2.0)
    R[np.diag_indices(W)] *= (1.0 + sigma2_eps * M0**2)
    # p[l]: 中心(L)到两侧的 Wiener 衰减
    p = np.exp(-M0**2 * sigma2_p * np.abs(idx - L) / 2.0)
    # 权重 w = R⁻¹ p (复数权, R 实对称正定)
    w = np.linalg.solve(R, p)
    # 注: 论文 w 为 F(|r|²) 实权重 (optimal nonlinearity), 此处实数实现.

    # --- 升幂归一化 + 滑窗加权 ---
    # yM(k) = (r(k)/|r(k)|)^M₀, 边界 edge-pad (保持窗长)
    rx_n = rx / np.abs(rx)                          # 单位相位项
    yM = rx_n ** M0                                 # 升幂去调制 (含升幂噪声)
    # edge-padding: 左右各补 L 个边缘值
    yM_pad = np.concatenate([np.full(L, yM[0]), yM, np.full(L, yM[-1])])
    # 滑窗提取 (k 从 0..N-1, 窗 [k, k+W) in padded coords)
    # V̂M(k) = sum_l w[l]·yM_pad[k+l]
    # 用卷积实现: V̂M = (yM_pad * w_rev)[L:L+N], 但 w 实数且对称窗 → 直接矩阵乘
    VhatM = np.empty(N, dtype=complex)
    for k in range(N):
        VhatM[k] = np.dot(w, yM_pad[k:k + W])      # w^H · yM_win (w 实数)

    phi_est = np.angle(VhatM) / M0                  # 逐符号相位轨迹 (解 M₀ 缩放)

    # --- 相位补偿 ---
    df_est = 0.0                                    # assume_df_zero: 纯 CPE, 不估频率
    tau_est = 0.0
    rx_comp = rx * np.exp(-1j * phi_est)
    # 注: 逐符号 phi_est, 不像 nda_ml 块常数. M₀-fold 模糊由 resolve_m16apsk_blockwise 消除
    #     (跟 nda_ml 同, 调用方负责, 此处仅返回相位补偿后信号).
    return rx_comp, tau_est, phi_est, df_est


def gardner_ted_recovery(rx, sps=2, mod='qpsk', gain=0.01, damping=np.sqrt(2)/2):
    """Gardner TED 定时恢复 — B7 锚方法.

    来源: Gardner 1986 IEEE T-COM "A BPSK/QPSK Timing-Error Detector for Sampled Receivers"。
    数学: Gardner TED 误差 e(n) = Re{ y(nT + T/2) · (y*(nT+T) − y*((n−1)T)) }
          （中间采样点 × 前后符号差）。经典结构: interpolation + TED + loop filter (PI)。
    实现: 2× 上采样 → Gardner TED → PI 环滤波器（damping/gain 控制环路带宽）→ 符号率采样输出。
    参数溯源: sps=2 (Gardner 1986 经典每符号 2 样本); damping=√2/2 临界阻尼; gain=0.01 环路增益。
    复杂度: 纯 Python loop, 建议后续 numba/cython 加速; MVE 量级 N≤1e5 OK。
    返回 (rx_resampled, timing_offset_est)。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if N < 3:
        return rx, 0.0
    # PI loop filter (与 dpll_track 同风格 c1/c2)
    wn = gain * 2 * np.pi   # 归一化自然频率
    c1 = 2 * damping * wn / sps
    c2 = (wn / sps) ** 2
    integrator = 0.0
    mu = 0.0            # 分数延迟（插值位置）
    out = []
    timing_err_accum = 0.0
    n = 1
    while n*sps + 1 < N:
        i0 = int((n-1)*sps + mu)
        i1 = int(n*sps + mu)
        i2 = int((n+1)*sps + mu)
        if i2 >= N:
            break
        y_prev = rx[i0]
        y_mid = rx[(i0 + i1)//2]
        y_curr = rx[i1]
        # Gardner TED
        e = np.real(y_mid * (np.conj(y_curr) - np.conj(y_prev)))
        # PI loop filter
        integrator += c2 * e
        freq_out = c1 * e + integrator
        mu += freq_out
        # wrap mu into [0, sps)
        if mu >= sps:
            mu -= sps
            n += 1
        elif mu < 0:
            mu += sps
        timing_err_accum += e
        out.append(y_curr)
        n += 1
    rx_resampled = np.array(out, dtype=complex)
    timing_offset_est = timing_err_accum / max(len(out), 1)
    return rx_resampled, timing_offset_est


def psa_foe_recovery(rx, pilot_idx, pilot_sym):
    """PSA FOE (Pilot-Aided Frequency Offset Estimation) — B7 baseline.

    注: 现有 fft_foe 是 blind 4 次幂法（QPSK 专用, 对 8PSK/(8,8)-16APSK M₀≠4 不适用）。
    B7 baseline 需 pilot-aided FOE → fft_foe 不够（仅 blind + 仅 QPSK）, 故加此函数。
    来源: 经典 pilot-aided FOE（Yi 2007 PTL [B11 ref 8] 频域 pilot CPE 思路的时域推广）。
    数学: pilot 相位差分 Δθ_p = angle(r(n_{p+1})·r*(n_p)/(s_{p+1}·s*_p)) = 2π·Δf·Δt_pilot
          → 最小二乘回归 Δθ vs Δt 斜率 = 2π·Δf。
    返回 (rx_compensated, df_est)。
    """
    rx = np.asarray(rx, dtype=complex)
    pilot_idx = np.atleast_1d(np.asarray(pilot_idx))
    pilot_sym = np.atleast_1d(np.asarray(pilot_sym, dtype=complex))
    if len(pilot_idx) < 2:
        # 单 pilot 无法分离 FOE → 退化为 0（与 da_ml 单 pilot 一致）
        df_est = 0.0
    else:
        # 相邻 pilot 差分相位
        r_p = rx[pilot_idx] / pilot_sym
        dtheta = np.diff(np.unwrap(np.angle(r_p)))
        dt = np.diff(pilot_idx.astype(float)) * T_S
        # 最小二乘: dθ = 2π·Δf·dt
        valid = dt > 0
        if np.any(valid):
            df_est = np.sum(dtheta[valid] * dt[valid]) / (2*np.pi * np.sum(dt[valid]**2))
        else:
            df_est = 0.0
    n_all = np.arange(len(rx))
    rx_comp = rx * np.exp(-1j * 2*np.pi*df_est*T_S * n_all)
    return rx_comp, df_est


# ════════════════════════════════════════════════════════════════════════════
# B5 LEO Doppler 短时谱 FOE (转正自 explore/b5-leo-doppler-spectrum-foe/)
# 来源: optcom.2024.130981 L71-87 (MVE S004+S005 PASS, consistency bit-exact)
# ════════════════════════════════════════════════════════════════════════════
def short_time_spectrum_foe(
    rx, n_fft=16, n_blocks=1024, alpha=6e8, fs=2.5e9,
    normalize_mode='ratio', ephemeris_pred=0.0,
):
    """B5 短时谱 FOE 单次估计 (前馈开环, 不撞 D006).

    分块 FFT → Hanning → 均值滤波 → 正负功率谱面积比 Rp-n → Δfest=α·Rp-n → +星历.
    B5 锚 optcom.2024.130981 L71-87. C6 公式重建 (PDF→md 丢失, 从 L77-87 文字):
      式 1 (L73): R[k] = |FFT(r·win)|²        离散功率谱
      式 3 (L81): Rp-n = P₊ − P₋              正负功率谱面积比
      式 2 (L79): Δfest = α · Rp-n            (α=6×10⁸, 暗 ratio 模式)
      式 4 (L83): Δf_comp = Δfest + ephemeris_pred   星历预测调 LO

    normalize_mode: 'block' 按块归一化(≡ratio 仅 α 尺度) / 'agc' AGC 前置(绝对差) /
      'ratio' 归一化功率比 (P₊−P₋)/(P₊+P₋) (α=6×10⁸ 暗 B5 锚用此模式).
    """
    rx = np.asarray(rx, dtype=complex).ravel()
    if n_fft <= 0 or (n_fft & (n_fft - 1)) != 0:
        raise ValueError(f"n_fft 须 2 的幂次, got {n_fft}")
    if normalize_mode not in ('block', 'agc', 'ratio'):
        raise ValueError(f"normalize_mode 须 'block'/'agc'/'ratio', got {normalize_mode!r}")

    N = rx.shape[0]
    n_blocks = min(n_blocks, N // n_fft)
    if n_blocks < 1:
        raise ValueError(f"数据 {N} 不足一块 FFT (n_fft={n_fft})")
    usable = n_blocks * n_fft

    # 星历预测预补偿 (B5 锚 L87 调 LO)
    if ephemeris_pred != 0.0:
        k0 = np.arange(N)
        rx = rx * np.exp(-1j * 2.0 * np.pi * ephemeris_pred * k0 / fs)
    # AGC 前置 (方案 B)
    if normalize_mode == 'agc':
        rms = np.sqrt(np.mean(np.abs(rx) ** 2))
        if rms > 0:
            rx = rx / rms

    # 分块 + Hanning + FFT → 功率谱
    blocks = rx[:usable].reshape(n_blocks, n_fft)
    blocks_win = blocks * np.hanning(n_fft)[np.newaxis, :]
    spec = np.fft.fftshift(np.fft.fft(blocks_win, axis=1), axes=1)
    psd = np.abs(spec) ** 2
    # block 归一化 (方案 A, ≡ ratio)
    if normalize_mode == 'block':
        blk_total = psd.sum(axis=1, keepdims=True)
        blk_total = np.where(blk_total > 0, blk_total, 1.0)
        psd = psd / blk_total
    # 均值滤波 (B5 锚 L87 "1024 sets mean filtering")
    spectrum_mean = np.mean(psd, axis=0)
    # 正负功率谱面积比 Rp-n (fftshift 后 half 处是 DC, 归正半轴)
    half = n_fft // 2
    p_plus = float(np.sum(spectrum_mean[half:]))
    p_minus = float(np.sum(spectrum_mean[:half]))
    if normalize_mode == 'ratio':
        denom = p_plus + p_minus
        rp_n = (p_plus - p_minus) / denom if denom > 0 else 0.0
    else:
        rp_n = p_plus - p_minus
    fest_residual_hz = alpha * rp_n
    fest_hz = fest_residual_hz + ephemeris_pred
    return {
        'fest_hz': float(fest_hz),
        'fest_residual_hz': float(fest_residual_hz),
        'fest_omega': float(2.0 * np.pi * fest_hz / fs),
        'rp_n': float(rp_n),
        'spectrum': spectrum_mean,
        'p_plus': p_plus,
        'p_minus': p_minus,
        'normalize_mode': normalize_mode,
        'n_blocks_used': n_blocks,
    }


def short_time_spectrum_foe_iterate(
    rx, n_iter=4, n_fft=16, n_blocks=1024, alpha=6e8, fs=2.5e9,
    normalize_mode='ratio', ephemeris_pred=0.0, precise_range_hz=None,
):
    """B5 短时谱 FOE 迭代收敛 (B5 锚 L141 "converges by 3rd/4th iteration").

    Rp-n-vs-f 非线性, 单次估仅对残频有效; 每轮预补偿 fest→rx, 残频减小再估.
    大频偏靠星历预测预补偿到残频 (ephemeris_pred), FFT 迭代估残频.
    precise_range_hz: 早停阈值 |fest_residual| < 此值即停 (B5Params.PRECISE_RANGE_B5).
    """
    rx = np.asarray(rx, dtype=complex)
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
            normalize_mode=normalize_mode, ephemeris_pred=0.0)
        fest_step = res['fest_residual_hz']
        fest_accum += fest_step
        rx_cur = rx_cur * np.exp(-1j * 2.0 * np.pi * fest_step * k / fs)
        history.append({'iter': it, 'fest_step': float(fest_step),
                        'fest_accum': float(fest_accum),
                        'residual_hz': float(fest_step), 'rp_n': float(res['rp_n'])})
        n_iter_used = it + 1
        if precise_range_hz is not None and abs(fest_step) < precise_range_hz:
            converged = True
            break
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


def leven_mthpower_foe(rx, M=4, N_sum=500, fs=2.5e9, normalize_mode='block'):
    """[60] Leven Mth-power FOE (祖师爷对照, 前馈开环 feed-forward).

    [60] Leven 2007 IEEE PTL L55-65: 符号差分 → M 次方去调制 → N 求和 → 相位/M → 频偏.
    捕获范围 ±fs/(2M) (QPSK M=4 @ 2.5GBaud → ±312.5MHz). 时域差分相位增量估计,
    跟 B5 频域功率谱面积比机制正交 (V3 祖师爷警报: 非同族).
    normalize_mode: 'block'/'agc'/'ratio' (跟 short_time_spectrum_foe 同方案, 公平对照).
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if N < 2:
        raise ValueError(f"len(rx)={N} 太短, 差分至少需 2 个样本")
    if M < 2:
        raise ValueError(f"M={M} 必须 >= 2 (PSK 阶数)")
    Ts = 1.0 / fs
    # 前馈归一化
    if normalize_mode == 'block':
        p = np.sqrt(np.mean(np.abs(rx) ** 2))
        rx_n = rx / p if p > 1e-12 else rx
    elif normalize_mode == 'agc':
        a = np.abs(rx)
        a[a < 1e-12] = 1e-12
        rx_n = rx / a
    elif normalize_mode in ('ratio', 'none'):
        rx_n = rx
    else:
        raise ValueError(f"normalize_mode must be 'block'/'agc'/'ratio'/'none', got {normalize_mode!r}")
    # 符号差分 z[k] = r[k]·conj(r[k-1])
    z = rx_n[1:] * np.conj(rx_n[:-1])
    if normalize_mode == 'ratio':
        za = np.abs(z)
        za[za < 1e-12] = 1e-12
        z = z / za
    # Mth-power 去调制 + 求和
    z_M = z ** M
    n = min(N_sum, len(z_M))
    s = np.sum(z_M[:n])
    delta_phi = np.angle(s) / M
    fest_hz = delta_phi / (2.0 * np.pi * Ts)
    phi_acc = np.arange(N, dtype=float) * delta_phi
    return {
        'fest_hz': fest_hz,
        'fest_omega': 2.0 * np.pi * fest_hz * Ts,
        'delta_phi': delta_phi,
        'phi_acc': phi_acc,
        'normalize_mode': normalize_mode,
        'sum_complex': s,
        'M': M,
        'N_sum': N_sum,
    }


def leven_capture_range_hz(fs, M=4):
    """[60] Leven Mth-power 无歧义捕获范围 (±fs/(2M))."""
    return fs / (2.0 * M)
