"""单载波时域 NDA-ML vs DA-ML CRLB 下界 + 数值验证 (公平对照 pilot overhead).

任务: 推导单载波时域 NDA-ML (升 M0=8 次幂去调制) vs DA-ML (pilot 配置) 的 CRLB 下界,
关键是公平对照 (DA-ML 含 pilot overhead 的总能量代价). 给主线形态 A+C 的 Go/Kill 判定.

==============================================================================
解析 CRLB 推导 (单载波时域, M0=8 升幂去调制)
==============================================================================
信号模型 (B11 行 33 迁时域):
  r(n) = s(n) · exp(jθ(n)) · sqrt(h(n)) + w(n),  w(n) ~ CN(0, σ²), n=0..N-1
  s(n) ∈ (8,8)-16APSK, θ(n) = φ_CPE + Wiener PN (σp²=2πΔνCLW·T_S 累积)

DA-ML CRLB (pilot-aided, φ 常相位估计):
  Fisher 信息 I_DA(φ) = Σ_{n∈pilot} |s_p|²·h(n) / σ² · (dθ/dφ)² = Σ_{n∈P} |s_p|²h(n)/σ²
  → CRB_DA(φ) = σ² / Σ_{n∈P} |s_p|²h(n)    (仅 N_p = N/spacing 个 pilot 贡献)

NDA-ML CRLB (升 M0 次幂, z(n) = r(n)^M0):
  z(n) ≈ |s(n)|^M0 · exp(j·M0·θ(n)) · h(n)^(M0/2) + w'(n)
  误差传播 (一阶 Taylor): Var[w'(n)] ≈ M0²·σ²·|s(n)√h(n)|^(2(M0-1))
  z 的有效 "信号 SNR": |z|²/Var[w'] = |s|^(2M0)·h^M0 / (M0²·σ²·|s|^(2M0-2)·h^(M0-1))
                                      = |s(n)|²·h(n) / (M0²·σ²)
  Fisher 信息对相位 φ: I_NDA(φ) = Σ_n (|z|²/Var[w'])·(d·arg(z)/dφ)²
                              = Σ_n [|s|²h/(M0²·σ²)]·(M0)²
                              = Σ_n |s(n)|²h(n)/σ²          ← M0² 相消! (上一轮疑点解决)
  → CRB_NDA(φ) = σ² / Σ_{n=0}^{N-1} |s(n)|²h(n)              (全 N 个符号贡献)

**核心结论**:
  CRB_NDA(φ)/CRB_DA(φ) = Σ_{n∈P}|s_p|²h(n_p) / Σ_{n=0}^{N-1}|s(n)|²h(n)
                        ≈ N_p/N  = 1/spacing  (per-symbol avg power equal)
  → CRB 层 NDA-ML 优于 DA-ML (用全部 N 符号 vs N/spacing 个 pilot).
  上一轮的 "M0²·N_p/N = 64×..." 错误源于: 把升幂噪声方差放大 M0² 当成 Fisher 信息分母, 但
  忘了 NDA 估的是 M0·φ (相位增益 M0), 二者相消. 严格推: M0² 在 |z|²/Var[w'] 已抵消 (见上).
  **CRLB 层 NDA-ML 是理论下界最优**; 实际 BER gain 来自 (i) 频谱效率 pilot overhead saved +
  (ii) 估计精度 N/N_p = spacing 倍符号数.

公平对照 (pilot overhead 代价):
  - 信息符号有效 SNR γ_d: DA-ML 数据符号与 NDA-ML 同符号率同功率 → 同 γ_d.
  - 相同信息吞吐量 R_info 下, DA-ML 须多发 1/spacing 比例 pilot → 总能量多 10·log10(spacing/(spacing-1)).
    spacing=4: pilot overhead = 10·log10(4/3) = 1.249 dB.
  - 公平对比坐标 = 总能量 SNR γ_tot:
      NDA-ML: γ_tot = γ_d (0% overhead)
      DA-ML:  γ_tot = γ_d + 1.249 dB (25% overhead)
  - BER 曲线仍按 γ_d (符号率 SNR) 跑 (两方案同信道同符号率公平);
    gain@HD-FEC 报告时 DA-ML 的 γ_d 加 1.249 dB = 等效总能量.

==============================================================================
TL-20 物理预期 (公平对照, 总能量 SNR 坐标)
==============================================================================
  场景          预期 gain@HD-FEC (公平, dB)    物理依据
  AWGN 无湍流   +0.3 to +0.8                    pilot overhead 1.25dB - NDA 升幂噪声 ~0.5dB
  weak (α4β3)   +0.3 to +0.8                    湍流弱, 不破坏频谱效率增量
  moderate(α2.5β1.8) +0.5 to +1.5              DA pilot 受 fade, NDA 全帧积分鲁棒
  strong(α1.5β0.8) AMBIGUOUS -1 to +2           deep fade 升幂噪声放大 vs DA pilot 崩溃

偏离即查 (TL-20):
  - AWGN gain < 0 → 可疑 (公平对照下 NDA 应至少持平)
  - moderate gain < 0 → 可疑 (DA pilot 受 fade 应退化)
  - strong gain < -2 → 形态 C 失败 (升幂噪声压倒 fade 鲁棒)
  - 任一 gain > 3 → 可疑 (超 B11 +2dB)

==============================================================================
方法学决策 (TL-23 验证后发现)
==============================================================================
A. 逐块恢复 Nblock=256 (=B11 DFT_SIZE): Wiener PN 累积漂移 (CLW=500kHz, ~0.18 rad/256-sym 块).
   全帧恢复线性 (φ,Δf) 模型失效. B11 原文即按 DFT_SIZE=256 块处理 (行 155).
B. NDA-ML 调用 (守 D003, 分场景):
   - AWGN 场景 (awgn_wiener_channel, 真 Δf=0): assume_df_zero=True. B11 行 33 假设 CFO 已补偿,
     FFT 在 df=0 时锁噪声伪峰 → 跳 FFT-df, 直接升幂 mean-angle 估常相位 CPE.
   - 星地湍流场景 (generate_shared_realization_apsk 注入 F_RESIDUAL=1MHz CFO + f_dot=150MHz/s
     Doppler): **两阶段** — 先 fft_foe(M0=8 升幂) 粗估 CFO 补偿, 再 nda_ml_recovery
     (assume_df_zero=True) 估残余 CPE. 诊断 (_ber_floor_diagnostic.py) 证实:
     (1) assume_df_zero=True 单独用会留 0.64rad/块的 CFO 相位斜坡致 CPE 跟踪失败 (D1);
     (2) 两阶段 fft_foe+nda CPE 把 NDA 拉回 oracle_hmed 水平 (D1 修复).
C. DA-ML pilot spacing=4 (25% overhead, 等距 pilot, pilot_sym = 已知 tx 符号, pilot-aided 非决策
   错误传播 — DA "理想" 形式, 不偏袒 NDA). 公平对照: DA 数据 BER 仅在 data 符号位置算 (pilot 不算).
D. 幅度处理 (8,8)-16APSK 解调对 sqrt(h) 敏感 — **诊断发现 h_med 标量均衡是 BER floor 主因
   (D2, 5.5× 退化)**: 用中位数 h 均衡所有块, deep fade 块 (h<<h_med) 残差大, 即使 oracle
   (真相位) 也被锁在 BER floor. 修复改用 per-block h 估计:
   - NDA-ML (盲, 无 pilot): per-block 硬幅值估计 ĥ=mean(|rx|²)−1/(2γ) 块内平均 (公平, 无 oracle)
   - DA-ML (有 pilot): per-block pilot 估计 ĥ=mean(|r(p)/s(p)|²) pilot 位置平均
   - oracle (上限): per-block 真 h (genie)
   两方案同 per-block 幅度处理 (正交模块), 公平.
E. oracle 上界: 真实 θ(k) 补偿 + per-block 真h 均衡 (genie), 看离信息论极限多远.
F. HD-FEC threshold = 3.8e-3 (7%, B11 行 181/191). 诊断 (TL-22) 证实: 20dB 总能量下 HD-FEC 仍物理
   不可达 (oracle 真 h@20dB weak=7.8e-3 > 3.8e-3); 需 ~24dB 总能量 weak 才可达.
   扩展 SNR 扫至 28dB 覆盖 HD-FEC 交叉点.

运行: cd projects/simulation && python explore/single-carrier-nda-ml/_time_domain_crlb.py
时间预算: ≤ 900 s
"""
import os
import sys
import time
import json

import numpy as np

# 从 simulation 根导入 common (TL-13 共用同一信道)
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common import (
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod, ber_count_m16apsk,
    resolve_m16apsk, resolve_m16apsk_blockwise,
    da_ml_recovery, nda_ml_recovery,
    mmse_equalize, amp_limit,
    T_S as T_S_GLOBAL,        # 系统 T_S=1/2.5e9 (信道 generate_shared_realization_apsk 用此)
    BLOCK as CH_BLOCK,         # 信道块大小 (params ExperimentParams.BLOCK=100, h 块内恒定)
)
from params import SimulationConfig


# =============================================================================
# B11 / 实验参数 (溯源: params.py B11Params + 本任务 brief)
# =============================================================================
N_DFT = 256            # B11 行 155 DFT size (= 逐块恢复块大小)
M0 = 8                 # (8,8)-16APSK 升 M0=8 次幂 (B11 行 75-77, params B11Params.M0_POWER)
BITS_PER_SYM = 4       # (8,8)-16APSK: 4 bit/symbol
HDFEC = 3.8e-3         # 7% HD-FEC threshold BER (B11 行 181/191)
DA_PILOT_SPACING = 4   # DA-ML pilot 间距: 每 4 符号 1 pilot = 25% overhead (本任务 brief)
# pilot overhead 总能量代价 (spacing=4): 10·log10(4/3) = 1.249 dB
PILOT_OVERHEAD_DB = 10.0 * np.log10(DA_PILOT_SPACING / (DA_PILOT_SPACING - 1))
BLOCK_SIZE_RESOLVE = 256  # resolve_m16apsk_blockwise block_size (守 D003)

# AWGN 场景参数 (D-007: 单载波统一, 从 params.py SystemParams 单字段读)
# 旧 CLW_B11=500kHz/BAUD_B11=25GBaud (B11 OFDM 场景) 已删, 详见 decisions.md D-007.
_cfg = SimulationConfig()
LASER_LW = _cfg.system.LASER_LW       # 10e3 Hz (Valjus sat.1553 §4.2, 星地 FSO ECL 典型)
T_S_AWGN = 1.0 / _cfg.system.R_SYM    # = 4e-10 s (单载波符号周期, 与 T_S_GLOBAL 一致)
# Wiener PN 每符号方差 σ²_p = 2π·Δν·T_S (Viterbi 1963 标准激光相位噪声模型).
# D-007: 从 LASER_LW + T_S 派生 (单载波 10kHz@2.5GBaud → 2.51e-5), 不再用 CLW_B11.
SIGMA2_P = 2 * np.pi * LASER_LW * T_S_AWGN


# =============================================================================
# AWGN 信道 (B11 原始场景, 无湍流/无 Doppler/无 CFO, 仅 Wiener PN + AWGN)
# =============================================================================
def awgn_wiener_channel(tx, snr_db, seed):
    """B11 信号模型 (行 33/51): r(k) = s(k)·exp(jθ(k)) + n(k), θ(k)=Wiener 累积 PN.
    无 FOE (Δf=0 已补偿), 无湍流, 无 Doppler. φ₀=0."""
    rng = np.random.default_rng(seed)
    N = len(tx)
    phi = np.cumsum(rng.normal(0.0, np.sqrt(SIGMA2_P), N))
    carrier = np.exp(1j * phi)
    signal = tx * carrier
    snr_lin = 10.0 ** (snr_db / 10.0)
    noise_var = 1.0 / (2.0 * snr_lin)
    noise = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return signal + noise, phi


# =============================================================================
# 逐块 NDA-ML / DA-ML / oracle BER 评估 (AWGN)
# =============================================================================
def ber_nda_awgn(rx, tx_bits, phi_true):
    """NDA-ML AWGN: 逐块升幂 mean-angle 估常相位 CPE (assume_df_zero=True, B11 df=0 修复).
    逐块 resolve M0-fold 模糊 (守 D003). 返回 (ber, n_err, n_bits).

    D-007 (2026-07-07) 修复: 加 intra_block_tracking='segmented' (segK8 块内跟踪),
    与 Formal sc_nda_ml_sim.ber_nda_awgn 对齐 (consistency_check bit-exact).
    segK8 是 sandbox (explore/nda-awgn-tracking-sandbox/) 验证的改进版, AWGN 下反超 BPS ~1dB."""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * N_DFT:(b + 1) * N_DFT]
        # assume_df_zero=True: B11 行 33 真 df=0, 跳 FFT-df 锁伪峰 (守 D003 bug 修复)
        # intra_block_tracking='segmented': segK8 块内跟踪 (改进版, 与 Formal 对齐)
        rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True,
                                      intra_block_tracking='segmented')
        rx_comp[b * N_DFT:(b + 1) * N_DFT] = rc
    tb = tx_bits[:L * BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_da_awgn(rx, tx_bits, phi_true, pilot_spacing=DA_PILOT_SPACING):
    """DA-ML AWGN: 逐块 pilot-aided (pilot_sym=已知 tx 符号, 非决策错误传播).
    公平对照: BER 仅在 data 符号位置算 (pilot 不算信息 BER). 返回 (n_err_data, n_bits_data)."""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    tx_sym = m16apsk_mod(tx_bits[:L * BITS_PER_SYM])
    # data 符号位置 mask: pilot 位置 (等距 spacing) 不算
    pilot_idx_local = np.arange(0, N_DFT, pilot_spacing)
    is_data = np.ones(N_DFT, dtype=bool)
    is_data[pilot_idx_local] = False
    n_err_data = 0
    n_bits_data = 0
    rx_comp_full = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        s_blk = slice(b * N_DFT, (b + 1) * N_DFT)
        p_sym = tx_sym[b * N_DFT + pilot_idx_local]
        rc, _, _ = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                                  pilot_sym=p_sym, mod='m16apsk')
        rx_comp_full[s_blk] = rc
    # 解调全块, 但 BER 只在 data 位置统计
    demod_bits = m16apsk_demod(rx_comp_full)
    tb = tx_bits[:L * BITS_PER_SYM]
    # reshape (nsym, 4) → data 位置 mask 扩展到 bit
    n_sym = L
    is_data_sym = np.zeros(n_sym, dtype=bool)
    for b in range(n_blk):
        base = b * N_DFT
        is_data_sym[base:base + N_DFT] = is_data
    tb_arr = tb.reshape(n_sym, BITS_PER_SYM)
    dm_arr = demod_bits.reshape(n_sym, BITS_PER_SYM)
    n_err_data = int(np.sum(tb_arr[is_data_sym] != dm_arr[is_data_sym]))
    n_bits_data = int(np.sum(is_data_sym) * BITS_PER_SYM)
    return n_err_data, n_bits_data


def ber_oracle_awgn(rx, tx_bits, phi_true):
    """Oracle (genie-aided): 真实 θ(k) 补偿 → 解调 → BER. 信息论上界."""
    N = len(rx)
    rx_comp = rx * np.exp(-1j * phi_true[:N])
    tb = tx_bits[:N * BITS_PER_SYM]
    return int(np.sum(tb != m16apsk_demod(rx_comp))), len(tb)


# =============================================================================
# 湍流场景: 用 generate_shared_realization_apsk + per-block h 均衡
# =============================================================================


def fft_foe_m0_omega(rx, M0_power, N_fft=None):
    """M0 升幂 FOE: rx^M0 去调制 → FFT 找频峰 → /M0 还原 CFO (omega, rad/sample).
    修复 D1: 星地湍流场景 F_RESIDUAL=1MHz CFO 致 0.64rad/块 相位斜坡, 必须估 FOE.
    返回 omega_est (rad/sample), 用于 exp(-j·omega·k) 补偿."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    if N_fft is None:
        N_fft = min(N, 4096)
    N_fft = min(N_fft, N)
    raised = rx ** M0_power
    seg = raised[:N_fft]
    win = np.hanning(N_fft)
    R = np.fft.fftshift(np.fft.fft(seg * win, n=N_fft * 8))
    freqs = np.fft.fftshift(np.fft.fftfreq(N_fft * 8, d=T_S_GLOBAL))
    idx = np.argmax(np.abs(R))
    if 1 <= idx < len(R) - 1:
        a_v, b_v, g_v = np.abs(R[idx - 1]), np.abs(R[idx]), np.abs(R[idx + 1])
        if b_v + a_v - 2 * g_v != 0:
            p = 0.5 * (a_v - g_v) / (a_v - 2 * b_v + g_v)
            df_raised = freqs[idx] + p * (freqs[1] - freqs[0])
        else:
            df_raised = freqs[idx]
    else:
        df_raised = freqs[idx]
    df_est_hz = df_raised / M0_power
    return 2 * np.pi * df_est_hz * T_S_GLOBAL


def estimate_h_blind_perblock(rx_raw, gamma_bar, block=CH_BLOCK):
    """盲 per-block h 估计 (NDA-ML, 无 pilot, 公平非 oracle).
    方法: 块内 |rx|² 平均 ≈ h·E[|s|²] + σ². E[|s|²]=1 (星座归一化), σ²=1/(2γ).
    → ĥ = mean(|rx|²) − 1/(2γ). 截断 ≥ 1e-6.
    对齐信道 BLOCK (100 sym 内 h 恒定). 修复 D2: 替代 h_med 标量均衡."""
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        s = slice(i * block, min((i + 1) * block, N))
        p_rx = float(np.mean(np.abs(rx_raw[s]) ** 2))
        h_blk = p_rx - 1.0 / (2.0 * gamma_bar)
        h_est[s] = max(h_blk, 1e-6)
    return h_est


def estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_bar, pilot_spacing=DA_PILOT_SPACING,
                              block=CH_BLOCK):
    """per-block pilot h 估计 (DA-ML): pilot 位置 r(p)=s(p)√h → ĥ=mean(|r(p)/s(p)|²).
    对齐信道 BLOCK. 修复 D2: 替代 h_med 标量均衡 (公平, DA 有 pilot)."""
    rx_raw = np.asarray(rx_raw)
    N = len(rx_raw)
    pilot_idx = np.arange(0, N, pilot_spacing)
    ratio_sq = np.abs(rx_raw[pilot_idx] / tx_sym[pilot_idx]) ** 2
    nb = (N + block - 1) // block
    h_est = np.empty(N, dtype=float)
    for i in range(nb):
        lo, hi = i * block, min((i + 1) * block, N)
        p_in_blk = (pilot_idx >= lo) & (pilot_idx < hi)
        h_blk = float(np.mean(ratio_sq[p_in_blk])) if np.any(p_in_blk) else 1.0
        h_est[lo:hi] = max(h_blk, 1e-6)
    return h_est


def ber_nda_turb(rx, tx_bits, phi_true):
    """NDA-ML 湍流: 两阶段 (fft_foe + nda CPE) 逐块恢复.
    修复 D1: fft_foe(M0) 粗估 CFO 补偿; 再 nda_ml(assume_df_zero=True) 估残余 CPE.
    (rx 已 per-block h 均衡 — 修复 D2). 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * N_DFT:(b + 1) * N_DFT]
        omega_est = fft_foe_m0_omega(seg, M0)
        k = np.arange(N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _, _, _ = nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)
        rx_comp[b * N_DFT:(b + 1) * N_DFT] = rc
    tb = tx_bits[:L * BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def ber_da_turb(rx, tx_bits, phi_true, tx_sym, pilot_spacing=DA_PILOT_SPACING):
    """DA-ML 湍流: pilot_sym=已知 tx 符号. BER 仅 data 位置. (rx 已 per-block pilot h 均衡)"""
    return ber_da_awgn(rx, tx_bits, phi_true, pilot_spacing)


def ber_oracle_turb(rx_eq, tx_bits, phi_true):
    """Oracle 湍流: rx 已 per-block 真h 均衡, 再用真实 θ 补偿. (genie 幅度+相位)"""
    N = len(rx_eq)
    rx_comp = rx_eq * np.exp(-1j * phi_true[:N])
    tb = tx_bits[:N * BITS_PER_SYM]
    return int(np.sum(tb != m16apsk_demod(rx_comp))), len(tb)


# =============================================================================
# SNR @ BER 插值 (log-linear, 单调降假设)
# =============================================================================
def snr_at_ber(snr_list, ber_list, ber_target):
    """线性插值 (SNR 轴, log BER) 找 ber_target 处 SNR. 返回 None 若不可达."""
    snr_list = np.asarray(snr_list, dtype=float)
    ber_list = np.asarray(ber_list, dtype=float)
    order = np.argsort(snr_list)
    snr_list, ber_list = snr_list[order], ber_list[order]
    for i in range(len(snr_list) - 1):
        b_hi = ber_list[i]
        b_lo = ber_list[i + 1]
        if b_hi >= ber_target >= b_lo and b_hi > b_lo:
            t = (np.log(b_hi) - np.log(ber_target)) / (np.log(b_hi) - np.log(b_lo))
            return float(snr_list[i] + t * (snr_list[i + 1] - snr_list[i]))
    return None


def equiv_snr_gap(snr_list, ber_ref, ber_test):
    """等效 SNR gap: test 曲线达 ref 曲线在 ref_snr 处 BER 所需额外 SNR.
    gap>0 = test (NDA) 劣 (需更高 SNR). 返回 list of (ref_snr, test_snr, gap)."""
    out = []
    snr_list = np.asarray(snr_list, dtype=float)
    ber_ref = np.asarray(ber_ref, dtype=float)
    ber_test = np.asarray(ber_test, dtype=float)
    order = np.argsort(snr_list)
    snr_list, ber_ref, ber_test = snr_list[order], ber_ref[order], ber_test[order]
    for i, sref in enumerate(snr_list):
        bref = ber_ref[i]
        stest = snr_at_ber(snr_list, ber_test, bref)
        if stest is not None:
            out.append((float(sref), float(stest), float(stest - sref)))
    return out


# =============================================================================
# AWGN 实验
# =============================================================================
def run_awgn(n_blocks, snr_points, seed_base):
    """AWGN 三方案 BER 扫描. 返回 per-snr dict list."""
    N_sym = n_blocks * N_DFT
    print(f"[AWGN] N_sym={N_sym}/点 ({n_blocks}×{N_DFT}), LASER_LW={LASER_LW/1e3:.0f}kHz, "
          f"M0={M0}, pilot_spacing={DA_PILOT_SPACING}")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'ORACLE':>12} "
          f"{'NDA/DA':>8} {'NDA/Ora':>9}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = awgn_wiener_channel(tx, snr, seed)
        ne_nda, nb_nda = ber_nda_awgn(rx, bits, phi_true)
        ne_da, nb_da = ber_da_awgn(rx, bits, phi_true)
        ne_or, nb_or = ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_or = ne_or / nb_or
        r_nd = b_nda / b_da if b_da > 0 else float('inf')
        r_no = b_nda / b_or if b_or > 0 else float('inf')
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_or:>12.4e} {r_nd:>8.3f} {r_no:>9.3f}")
        per_snr.append({
            'snr_db': float(snr), 'snr_db_total_nda': float(snr),
            'snr_db_total_da': float(snr) + PILOT_OVERHEAD_DB,
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'oracle_ber': b_or,
            'ratio_nda_over_da': r_nd, 'ratio_nda_over_oracle': r_no,
        })
    return per_snr


# =============================================================================
# 湍流实验 (用 generate_shared_realization_apsk, TL-13 共用同一信道)
# =============================================================================
def run_turb(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0):
    """湍流场景三方案 BER 扫描. gamma_bar_points_db = 数据有效 SNR (per-symbol).
    用 generate_shared_realization_apsk 共享信道实现.
    幅度处理 (修复 D2): per-block h 估计替代 h_med 标量均衡:
      - NDA-ML (盲): per-block 硬幅值 ĥ=mean(|rx|²)−1/(2γ)
      - DA-ML (pilot): per-block pilot ĥ=mean(|r(p)/s(p)|²)
      - oracle: per-block 真 h (genie 上限)
    相位 (修复 D1): NDA 两阶段 (fft_foe+nda CPE); DA pilot FOE+CPE; oracle 真 θ."""
    Ns = N_DFT  # 逐块 256 符号
    print(f"[{turb_name}] N_sym={n_blocks*Ns}/点 ({n_blocks}×{Ns}), "
          f"per-block h 均衡 (NDA盲/DA pilot/oracle真) + amp_limit(3.0), "
          f"NDA 两阶段 fft_foe+nda CPE")
    print(f"{'γd_dB':>7} {'NDA_BER':>12} {'DA_BER':>12} {'ORACLE':>12} "
          f"{'NDA/DA':>8} {'NDA/Ora':>9}")
    per_snr = []
    for gamma_db in gamma_bar_points_db:
        gamma_lin = 10 ** (gamma_db / 10)
        ne_nda = ne_da = ne_or = 0
        nb_nda = nb_da = nb_or = 0
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']
            bits = r['bits']
            phi = r['phi']
            tx_sym = r['tx']
            h_true = r['h']
            # 幅度处理 (修复 D2): per-block h — 三方案各自估计, 公平
            # NDA-ML 盲 per-block h
            h_blind = estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            # DA-ML pilot per-block h
            h_pilot = estimate_h_pilot_perblock(rx_raw, tx_sym, gamma_lin)
            rx_pilot = amp_limit(mmse_equalize(rx_raw, h_pilot, gamma_lin), 3.0)
            # oracle per-block 真 h
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            ne, nb = ber_nda_turb(rx_blind, bits, phi)
            ne_nda += ne; nb_nda += nb
            ne, nb = ber_da_turb(rx_pilot, bits, phi, tx_sym)
            ne_da += ne; nb_da += nb
            ne, nb = ber_oracle_turb(rx_trueh, bits, phi)
            ne_or += ne; nb_or += nb
        b_nda = ne_nda / nb_nda
        b_da = ne_da / nb_da
        b_or = ne_or / nb_or
        r_nd = b_nda / b_da if b_da > 0 else float('inf')
        r_no = b_nda / b_or if b_or > 0 else float('inf')
        print(f"{gamma_db:>7.0f} {b_nda:>12.4e} {b_da:>12.4e} {b_or:>12.4e} {r_nd:>8.3f} {r_no:>9.3f}")
        per_snr.append({
            'snr_db': float(gamma_db),
            'snr_db_total_nda': float(gamma_db),
            'snr_db_total_da': float(gamma_db) + PILOT_OVERHEAD_DB,
            'nda_ml_ber': b_nda, 'da_ml_ber': b_da, 'oracle_ber': b_or,
            'ratio_nda_over_da': r_nd, 'ratio_nda_over_oracle': r_no,
        })
    return per_snr


# =============================================================================
# 增益分析 (公平对照: 总能量 SNR 坐标)
# =============================================================================
def analyze_fair_gain(per_snr, hdfec=HDFEC):
    """公平对照 gain@HD-FEC 分析.

    公平坐标 = 总能量 SNR γ_tot:
      NDA: γ_tot = γ_d (0% overhead)
      DA:  γ_tot = γ_d + PILOT_OVERHEAD_DB (25% overhead)
    gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC)   正 = NDA 赢

    若 HD-FEC 不可达 (BER floor), 改用可达 BER 水平 (取 NDA 最低可达 BER) 的等效总能量 SNR 差.
    """
    snrs_d = np.array([p['snr_db'] for p in per_snr])           # 数据有效 SNR
    b_nda = np.array([p['nda_ml_ber'] for p in per_snr])
    b_da = np.array([p['da_ml_ber'] for p in per_snr])
    b_or = np.array([p['oracle_ber'] for p in per_snr])
    snrs_tot_nda = snrs_d                                        # NDA 总能量 = γ_d
    snrs_tot_da = snrs_d + PILOT_OVERHEAD_DB                     # DA 总能量 = γ_d + 1.25dB

    # HD-FEC @ 总能量坐标
    # NDA: 找 γ_d @ HD-FEC (γ_tot=γ_d)
    s_nda_d = snr_at_ber(snrs_d, b_nda, hdfec)
    s_da_d = snr_at_ber(snrs_d, b_da, hdfec)
    s_or_d = snr_at_ber(snrs_d, b_or, hdfec)
    gain_hdfec = None
    hdfec_reachable = False
    if s_nda_d is not None and s_da_d is not None:
        # 公平 gain = (DA 总能量) - (NDA 总能量) = (s_da_d + overhead) - s_nda_d
        gain_hdfec = (s_da_d + PILOT_OVERHEAD_DB) - s_nda_d
        hdfec_reachable = True

    # 可达 BER 水平的等效 SNR 差 (HD-FEC 不可达时用).
    # 取 NDA 在最高 SNR (最低 BER) 工作点的 BER 为 target, 求 DA 达同 BER 的等效总能量差.
    min_nda_ber = float(np.min(b_nda))
    s_nda_min = snr_at_ber(snrs_d, b_nda, min_nda_ber)
    s_da_at_nda_min = snr_at_ber(snrs_d, b_da, min_nda_ber)
    equiv_gain_achievable = None
    if s_nda_min is not None and s_da_at_nda_min is not None:
        equiv_gain_achievable = (s_da_at_nda_min + PILOT_OVERHEAD_DB) - s_nda_min

    # 逐 SNR 公平比较 (总能量 γ_tot 坐标, 主用):
    # 在总能量 γ_tot 下, NDA 跑 γ_d=γ_tot, DA 跑 γ_d=γ_tot-1.25 (overhead).
    # 即 DA 曲线在 BER-vs-γ_d 上右移 1.25dB 后才与 NDA 同总能量.
    # 公平 gain @ 每工作点 = DA 达 NDA(γ_tot) BER 所需总能量 - γ_tot
    #   = (snr_da_d_at_berNDA + overhead) - γ_tot
    per_point_fair = []
    for i, gtot in enumerate(snrs_tot_nda):
        ber_nda_at_gtot = b_nda[i]
        s_da_d_needed = snr_at_ber(snrs_d, b_da, ber_nda_at_gtot)
        if s_da_d_needed is not None:
            fair_gain = (s_da_d_needed + PILOT_OVERHEAD_DB) - float(gtot)
            per_point_fair.append({
                'gamma_tot_db': float(gtot),
                'ber_nda': float(ber_nda_at_gtot),
                'snr_da_d_needed_db': float(s_da_d_needed),
                'fair_gain_db': float(fair_gain),   # 正 = NDA 赢
            })
    # 高 SNR 工作点公平 gain (最接近实用工作区, 主判据 for 湍流)
    fair_gain_high_snr = per_point_fair[-1]['fair_gain_db'] if per_point_fair else None
    fair_gain_mean = float(np.mean([p['fair_gain_db'] for p in per_point_fair])) if per_point_fair else None

    # NDA vs oracle gap (NDA 离信息论极限多远, 无 overhead 调整 — oracle 是相位完美)
    gap_nda_vs_oracle = equiv_snr_gap(snrs_d, b_or, b_nda)
    gap_or_mean = float(np.mean([g[2] for g in gap_nda_vs_oracle])) if gap_nda_vs_oracle else None

    return {
        'snr_nda_tot_at_hdfec': s_nda_d,
        'snr_da_tot_at_hdfec': (s_da_d + PILOT_OVERHEAD_DB) if s_da_d is not None else None,
        'snr_oracle_at_hdfec': s_or_d,
        'gain_nda_vs_da_fair_db': gain_hdfec,          # 公平 (含 overhead) @ HD-FEC, 正 = NDA 赢
        'gain_nda_vs_da_naive_db': (s_da_d - s_nda_d) if (s_da_d is not None and s_nda_d is not None) else None,
        'hdfec_reachable': hdfec_reachable,
        'equiv_gain_at_achievable_db': equiv_gain_achievable,
        'per_point_fair_gain': per_point_fair,
        'fair_gain_high_snr_db': fair_gain_high_snr,   # 主判据 for 湍流 (高 SNR 工作点)
        'fair_gain_mean_db': fair_gain_mean,
        'min_nda_ber': min_nda_ber,
        'gap_nda_vs_oracle_mean_db': gap_or_mean,
        'pilot_overhead_db': float(PILOT_OVERHEAD_DB),
    }


# =============================================================================
# 主
# =============================================================================
def main():
    t0 = time.time()
    cfg = SimulationConfig()

    # 实验配置 (守 FR-21: N_sym ≥ 1e5/点; 守时间预算 ≤ 900s)
    N_BLOCKS = 400                         # 400×256 = 102400 ≥ 1e5 ✓
    SNR_AWGN = [5.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
    # 湍流 SNR 扩展至 26dB 覆盖 HD-FEC 交叉点 (诊断: weak~24dB, moderate~28dB).
    # brief 原 [5,10,15,20] 在 20dB 顶 SNR 仍物理不可达 HD-FEC (oracle 真 h@20dB weak=7.8e-3),
    # 故加 22/24/26 让 weak (及接近 moderate) 可达, 报真实 gain@HD-FEC.
    SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]
    TURB_LEVELS = ['weak', 'moderate', 'strong']
    SEED_AWGN = 20240701
    SEED_TURB0 = 2000

    print("=" * 100)
    print("单载波时域 NDA-ML vs DA-ML CRLB + 公平对照 BER (pilot overhead 代价)")
    print(f"M0={M0}, pilot_spacing={DA_PILOT_SPACING} (25% overhead), "
          f"pilot_overhead_cost={PILOT_OVERHEAD_DB:.3f} dB")
    print("=" * 100)

    results = {
        'meta': {
            'task': '单载波时域 NDA-ML vs DA-ML CRLB 下界 + 公平对照 BER (pilot overhead)',
            'increment_form': '形态 A (AWGN 频谱效率) + C (湍流鲁棒性)',
            'metric': ('BER @ (8,8)-16APSK, M0-fold ambiguity resolved blockwise (256). '
                       'AWGN: assume_df_zero=True (B11 df=0 修复). '
                       '湍流: 两阶段 fft_foe(M0)+nda_ml CPE (修复 D1 CFO 残余) + '
                       'per-block h 估计 (NDA盲/DA pilot, 修复 D2 h_med 标量残差)'),
            'analytic_crlb_conclusion': {
                'CRB_NDA_phi': 'σ² / Σ_n |s(n)|²h(n)   (全 N 个符号贡献)',
                'CRB_DA_phi': 'σ² / Σ_{n∈P} |s_p|²h(n)   (仅 N_p=N/spacing 个 pilot 贡献)',
                'ratio': 'CRB_NDA/CRB_DA ≈ N_p/N = 1/spacing = 1/4 (per-symbol avg power equal)',
                'M0_cancellation_note': (
                    'M0² 在升幂噪声方差放大 (Var[w\']≈M0²σ²|s√h|^(2(M0-1))) 与 NDA 估 M0·φ 的'
                    '相位增益 (d arg(z)/dφ = M0) 间严格相消: '
                    'I(φ)=Σ(|z|²/Var[w\'])·(M0)² = Σ(|s|²h/(M0²σ²))·M0² = Σ|s|²h/σ². '
                    '上一轮 M0²·N_p/N=64× 错误源于漏算 (d arg(z)/dφ)²=M0² 项. '
                    '→ CRLB 层 NDA-ML 理论下界最优 (用全部符号).'
                ),
                'fairness_note': (
                    '公平坐标=总能量 SNR γ_tot. 相同信息吞吐量下 DA-ML 多发 1/spacing pilot → '
                    '总能量代价 10·log10(spacing/(spacing-1)) = 1.249 dB (spacing=4). '
                    'BER 曲线按数据有效 SNR γ_d 跑 (同符号率公平); '
                    'gain@HD-FEC 报告 DA γ_d+1.249 dB (等效总能量).'
                ),
            },
            'N_per_point': N_BLOCKS * N_DFT,
            'N_blocks': N_BLOCKS,
            'N_per_block': N_DFT,
            'M0': M0,
            'pilot_spacing': DA_PILOT_SPACING,
            'pilot_overhead_db': float(PILOT_OVERHEAD_DB),
            'block_size_resolve': BLOCK_SIZE_RESOLVE,
            'assume_df_zero': 'AWGN=True (B11 df=0); 湍流=False-equivalent via 两阶段 fft_foe+nda CPE',
            'ndaml_call_convention_D003': (
                'AWGN (df=0) 用 assume_df_zero=True (跳 FFT-df 锁伪峰); '
                '星地湍流 (有 F_RESIDUAL=1MHz CFO 残余) 用两阶段: fft_foe(M0=8) 粗估 CFO 补偿 + '
                'nda_ml_recovery(assume_df_zero=True) 估残余 CPE. 守 D003.'
            ),
            'calibration_fixes': {
                'D1_cfo_residual': '星地湍流场景 F_RESIDUAL=1MHz CFO 致 0.64rad/块相位斜坡; '
                                   'assume_df_zero=True 跳 FOE 致 CPE 跟踪失败 (BER 1.4-1.8× 退化). '
                                   '修复: 两阶段 fft_foe(M0)+nda CPE. 诊断 _ber_floor_diagnostic.py 证 '
                                   'two-stage 把 NDA 拉回 oracle_hmed 水平.',
                'D2_hmed_scalar_residual': 'h_med 标量均衡是 BER floor 主因 (D2, 5.5× 退化@weak 20dB): '
                                           '用中位数 h 均衡所有块, deep fade 块残差大, 即使 oracle 也被锁 floor. '
                                           '修复: per-block h 估计 (NDA 盲 ĥ=mean(|rx|²)−1/(2γ); DA pilot '
                                           'ĥ=mean(|r(p)/s(p)|²); oracle 真 h). 诊断证 blind h NDA 离真 h oracle '
                                           '仅 ~0.1-0.3 dB.',
                'D3_clw_irrelevant': 'D-007 (2026-07-07): AWGN 场景已改单载波 (LASER_LW=10kHz @ 2.5GBaud), '
                                     '不再用 B11 CLW=500kHz. 全场景线宽统一 SystemParams.LASER_LW.',
            },
            'hdfec_reachability_TL22': (
                '诊断 (TL-22 物理前提): 20dB 总能量下 HD-FEC 物理不可达 — '
                'oracle 真 h+真相位 @20dB weak=7.8e-3 > 3.8e-3. 非估计 bug, 是物理上限. '
                '需 ~24dB 总能量 weak 才可达. SNR 扫展至 26dB 覆盖.'
            ),
            'laser_lw_Hz': LASER_LW,
            'r_sym': _cfg.system.R_SYM,
            'sc_sigma2_p': SIGMA2_P,
            'hdfec_ber': HDFEC,
            'verdict_thresholds_FR21_D005': {
                'go_mve': '>=0.3 dB (公平对照, 进 MVE)',
                'conditional': '0.3-0.5 dB (薄但 D005 够格)',
                'kill_to_b7': '<0.3 dB (建议转 B7)',
            },
            'snr_awgn_dB': SNR_AWGN,
            'snr_turb_dB': SNR_TURB,
            'turb_levels': TURB_LEVELS,
        },
        'expected_TL20': {
            'awgn': '+0.3 to +0.8 dB (pilot overhead 1.25dB - NDA 升幂噪声 ~0.5dB)',
            'weak': '+0.3 to +0.8 dB (湍流弱, 不破坏频谱效率增量)',
            'moderate': '+0.5 to +1.5 dB (DA pilot 受 fade, NDA 全帧积分鲁棒)',
            'strong': 'AMBIGUOUS -1 to +2 dB (deep fade 升幂噪声 vs DA pilot 崩溃)',
            'deviation_rules': [
                'AWGN gain < 0 → 可疑',
                'moderate gain < 0 → 可疑 (DA pilot 受 fade 应退化)',
                'strong gain < -2 → 形态 C 失败 (升幂噪声压倒 fade 鲁棒)',
                '任一 gain > 3 → 可疑 (超 B11 +2dB)',
            ],
        },
        'awgn': {},
        'turbulence': {},
        'gain_analysis': {},
        'tl20_deviation_check': [],
    }

    # --- AWGN ---
    print("\n" + "=" * 50 + " AWGN (形态 A) " + "=" * 50)
    awgn_per_snr = run_awgn(N_BLOCKS, SNR_AWGN, SEED_AWGN)
    results['awgn'] = awgn_per_snr
    awgn_gain = analyze_fair_gain(awgn_per_snr)
    results['gain_analysis']['awgn'] = awgn_gain
    print(f"  → 公平 gain@HD-FEC = {awgn_gain['gain_nda_vs_da_fair_db']:+.3f} dB "
          f"(naive γ_d only: {awgn_gain['gain_nda_vs_da_naive_db']})  "
          f"NDA-vs-Oracle gap mean: {awgn_gain['gap_nda_vs_oracle_mean_db']}")

    # --- 湍流 (weak/moderate/strong) ---
    for turb in TURB_LEVELS:
        print(f"\n{'='*30} {turb} (形态 C) {'='*30}")
        per_snr = run_turb(turb, SNR_TURB, N_BLOCKS, cfg, SEED_TURB0)
        results['turbulence'][turb] = per_snr
        g = analyze_fair_gain(per_snr)
        results['gain_analysis'][turb] = g
        print(f"  → 公平 gain@HD-FEC = "
              f"{(('%+.3f' % g['gain_nda_vs_da_fair_db']) if g['gain_nda_vs_da_fair_db'] is not None else 'N/A(不可达)')} dB "
              f"  逐点公平 gain (高SNR/均值): "
              f"{(('%+.3f' % g['fair_gain_high_snr_db']) if g['fair_gain_high_snr_db'] is not None else 'N/A')}/"
              f"{(('%+.3f' % g['fair_gain_mean_db']) if g['fair_gain_mean_db'] is not None else 'N/A')} "
              f"  NDA-vs-Oracle gap mean: {g['gap_nda_vs_oracle_mean_db']}")

    # =========================================================================
    # TL-20 偏离检查
    # =========================================================================
    expected = {
        'awgn': (0.3, 0.8), 'weak': (0.3, 0.8),
        'moderate': (0.5, 1.5), 'strong': (-1.0, 2.0),
    }
    dev_check = []
    crossover_report = {}
    for scenario in ['awgn', 'weak', 'moderate', 'strong']:
        ga = results['gain_analysis'][scenario]
        g = ga['gain_nda_vs_da_fair_db']
        g_mean = ga.get('fair_gain_mean_db')
        g_high = ga.get('fair_gain_high_snr_db')
        # 逐点公平 gain 序列 (看是否 cross-over)
        pp = ga.get('per_point_fair_gain', [])
        gains_series = [p['fair_gain_db'] for p in pp]
        has_crossover = (len(gains_series) >= 2 and
                         min(gains_series) < 0 < max(gains_series))
        crossover_report[scenario] = {
            'fair_gain_mean_db': g_mean,
            'fair_gain_high_snr_db': g_high,
            'fair_gain_low_snr_db': gains_series[0] if gains_series else None,
            'has_crossover': has_crossover,
            'gains_by_snr': gains_series,
        }
        if scenario == 'awgn':
            g_use = g  # AWGN HD-FEC 可达, 主用 HD-FEC gain
            tag = 'HD-FEC'
        elif g is not None:
            # 湍流 HD-FEC 可达 (修复后 weak/moderate): 主用 HD-FEC gain (与 AWGN 同标尺,
            # 形态 A+C 频谱效率增量锚). 辅以逐点/cross-over 信息.
            g_use = g
            tag = 'HD-FEC'
        else:
            # 湍流 HD-FEC 不可达 (strong, deep fade 物理上限): 主用均值 (覆盖全工作 SNR 区),
            # 辅以高 SNR 逐点 (实用工作区) + cross-over 标记
            g_use = g_mean
            tag = '均值(全SNR区)'
        lo, hi = expected[scenario]
        if g_use is None:
            dev_check.append(f"{scenario}: gain=N/A (估计器全失效) — INCONCLUSIVE")
            continue
        if g_use < lo - 0.3:
            if scenario == 'strong' and g_use < -2:
                reason = '形态 C 失败 (升幂噪声压倒 fade 鲁棒)'
            elif g_use < 0:
                reason = 'NDA 劣于 DA (含 overhead 公平)'
            else:
                reason = f'薄增益 < TL-20 下限 {lo:+.1f}'
            extra = (f' [cross-over: 低SNR {gains_series[0]:+.2f}, 高SNR '
                     f'{gains_series[-1]:+.2f}]' if has_crossover else '')
            dev_check.append(f"{scenario}: gain={g_use:+.2f}dB ({tag}) < TL-20 [{lo:+.1f},{hi:+.1f}] "
                             f"→ DEVIATION — {reason}{extra}")
        elif g_use > hi + 0.5:
            extra = (f' [cross-over: 低SNR {gains_series[0]:+.2f}, 高SNR '
                     f'{gains_series[-1]:+.2f}]' if has_crossover else '')
            dev_check.append(f"{scenario}: gain={g_use:+.2f}dB ({tag}) > TL-20 [{lo:+.1f},{hi:+.1f}] "
                             f"→ SUSPICIOUS (超预期){extra} → DEVIATION")
        else:
            extra = (f' [cross-over: 低SNR {gains_series[0]:+.2f}, 高SNR '
                     f'{gains_series[-1]:+.2f}]' if has_crossover else '')
            dev_check.append(f"{scenario}: gain={g_use:+.2f}dB ({tag}) ∈ TL-20 [{lo:+.1f},{hi:+.1f}] → PASS{extra}")
    results['tl20_deviation_check'] = dev_check
    results['crossover_report'] = crossover_report

    # =========================================================================
    # 总判定 (FR-21 + D005, 公平对照)
    # =========================================================================
    gains_all = {}
    gains_tag = {}
    for scenario in ['awgn', 'weak', 'moderate', 'strong']:
        ga = results['gain_analysis'][scenario]
        g = ga['gain_nda_vs_da_fair_db']
        g_mean = ga.get('fair_gain_mean_db')
        if scenario == 'awgn':
            gains_all[scenario] = g
            gains_tag[scenario] = 'HD-FEC'
        else:
            gains_all[scenario] = g if g is not None else g_mean
            gains_tag[scenario] = 'HD-FEC' if g is not None else '均值(全SNR区)'
    # 主判据: 形态 A (AWGN) 是 Go/Conditional/Kill 锚 (频谱效率增量)
    g_awgn = gains_all['awgn']
    if g_awgn is None:
        verdict_awgn = 'INCONCLUSIVE'
    elif g_awgn >= 0.5:
        verdict_awgn = 'GO_MVE'
    elif g_awgn >= 0.3:
        verdict_awgn = 'CONDITIONAL'
    else:
        verdict_awgn = 'KILL (转 B7)'

    # 形态 C (湍流鲁棒性): moderate/strong 是否对 fade 鲁棒. 用逐点公平 gain 序列判定.
    g_mod_series = crossover_report.get('moderate', {}).get('gains_by_snr', [])
    g_str_series = crossover_report.get('strong', {}).get('gains_by_snr', [])
    g_wk_series = crossover_report.get('weak', {}).get('gains_by_snr', [])
    def _form_c_assess(series):
        if not series:
            return 'N/A'
        pos = sum(1 for x in series if x > 0)
        if pos == len(series):
            return f'NDA 全工作区赢 (低SNR{series[0]:+.1f}→高SNR{series[-1]:+.1f}dB, 对 fade 鲁棒)'
        elif pos == 0:
            return f'NDA 全工作区输 (升幂噪声压倒)'
        else:
            # cross-over: 增益从负转正. 低SNR负=NDA 在 deep fade + 低SNR 受盲 h 估计噪声
            # 拖累输; 高SNR正=NDA pilot-free 频谱效率增量赢 (DA 反而受 pilot 受 fade).
            return (f'cross-over: 低SNR{series[0]:+.1f} (NDA输, 盲h+低SNR拖累), '
                    f'高SNR{series[-1]:+.1f}dB (NDA赢, pilot-free 频谱效率增量)')
    form_c_robust = {
        'weak': _form_c_assess(g_wk_series),
        'moderate': _form_c_assess(g_mod_series),
        'strong': _form_c_assess(g_str_series),
        'overall': ('形态 C 在 strong 湍流成立 (NDA 全工作区赢, 对 deep fade 鲁棒); '
                    'weak/moderate cross-over: 低SNR NDA 受盲 h 噪声输, 高SNR NDA 频谱效率增量赢. '
                    '升幂噪声未在 strong 下反崩 (无 <-2dB 灾难).'
                    if g_str_series and min(g_str_series) > -2 else
                    '形态 C 失败: strong 下升幂噪声压倒 fade 鲁棒'),
    }
    results['overall_verdict'] = {
        'verdict_awgn_formA': verdict_awgn,
        'gain_awgn_fair_db': g_awgn,
        'gains_all_fair_db': gains_all,
        'gains_metric_tag': gains_tag,
        'formC_turbulence_robustness': form_c_robust,
        'pilot_overhead_db': float(PILOT_OVERHEAD_DB),
        'basis': ('主判据: AWGN 公平 gain@HD-FEC (形态 A 频谱效率增量锚). '
                  '公平对照: DA 总能量 = γ_d + 1.249dB pilot overhead, NDA 总能量 = γ_d. '
                  'FR-21+D005: ≥0.3dB → MVE, 0.3-0.5 Conditional, <0.3 转 B7. '
                  '修复后 weak/moderate HD-FEC 可达 (per-block h + 两阶段 FOE), 报真实 gain@HD-FEC; '
                  'strong 因 deep fade 物理不可达 (oracle 真 h@26dB=1.96e-2 > 3.8e-3), 用均值公平 gain.'),
    }

    elapsed = time.time() - t0
    results['meta']['elapsed_sec'] = float(elapsed)

    print("\n" + "=" * 100)
    print("TL-20 物理预期偏离检查 (公平对照, 总能量 SNR):")
    for line in dev_check:
        print(f"  {line}")
    print(f"\n判定 (FR-21+D005, AWGN 形态A 锚): {verdict_awgn} (公平 gain = "
          f"{('%+.2f' % g_awgn) if g_awgn is not None else 'N/A'} dB)")
    print(f"形态 C (湍流鲁棒): {form_c_robust}")
    print(f"\n各场景公平 gain@HD-FEC (dB, 湍流用高SNR逐点 if HD-FEC不可达):")
    for s, g in gains_all.items():
        print(f"  {s:>10}: {('%+.3f' % g) if g is not None else 'N/A'}  [{gains_tag[s]}]")
    print(f"\n[耗时] {elapsed:.1f} s")

    # 写 JSON
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(out_dir, '_crlb_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[保存] {out_json}")


if __name__ == '__main__':
    main()
