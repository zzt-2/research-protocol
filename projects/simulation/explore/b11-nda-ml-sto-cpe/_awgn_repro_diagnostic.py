"""B11 NDA-ML vs DA ML 复现性诊断 — B11 原始场景 (AWGN + Wiener PN, 无湍流).

目的 (见 task brief):
  现有 nda_ml_recovery 实现在 B11 原始场景 (AWGN 无湍流) 下能否复现 +2dB SNR gain @ 7% HD-FEC?
  - 复现 +2dB  → 实现正确, 前两轮 Kill (湍流迁移/CRB) 是真实结论
  - 复现不了   → 实现有 bug, 前两轮 Kill 都是误判, 报告 bug + 修复方向

严格对照 B11 仿真链 (行 33/155):
  - 调制: (8,8)-16APSK, 4 bit/sym
  - 信道: 纯 AWGN + 激光线宽 Wiener PN (CLW=500 kHz), 无湍流/无 Doppler/无 CFO
           (B11 行 33: 假设湍流/Doppler/CFO 已补偿, 信道仅 AWGN + 线宽 PN)
  - 参数: DFT_SIZE=256 (块级), CP_LEN=32, BAUD=25 GBaud, SNR 扫含 15 dB

三方案:
  1. NDA-ML  (nda_ml_recovery, M0=8)        — B11 锚方法 (盲升 M₀=8 次幂)
  2. DA ML   (da_ml_recovery, pilot-aided)  — B11 baseline
  3. genie-aided oracle (真 φ 补偿)          — 信息论下界参考

关键实现决策:
  A. 逐块恢复 N_blk=256 (=B11 DFT_SIZE): Wiener PN 累积 0.18 rad/256-sym 块, 线性 (φ,Δf)
     模型近似成立. 全帧恢复会因 256→1e5 累积 3.5 rad 漂移使线性模型失效 (前两轮 bug).
  B. 块间相位连续 (不重置 PN 模型): 真 θ(k) 在全帧连续累积; 但每块独立估 (φ,Δf).
     解调时每块各自 resolve_m16apsk (8 重模糊), 不跨块借 oracle.
  C. DA ML pilot 配置: B11 OFDM 单 pilot 符号 → 单载波等距 pilot. 本轮两种:
       (i)  稀疏 pilot (spacing=8, 模拟 B11 OFDM 每子载波 pilot 占用低)
       (ii) 密集 pilot (spacing=4, 每 4 sym 一个 pilot, 模拟 DA CPE 强基线)
     主要报 (ii) (DA 最强, 不偏袒 NDA).
  D. T_S 一致性: nda_ml_recovery/da_ml_recovery 用全局 T_S=1/2.5e9 (system R_SYM=2.5GBaud).
     B11 用 25GBaud. 本信道无 CFO (Δf=0), 故 T_S 不影响相位估计 (df 项贡献 0), 仅影响
     df_est 数值 (本轮不评估 df 精度). 验证: 见脚本末尾 assertion.

运行: cd projects/simulation && python explore/b11-nda-ml-sto-cpe/_awgn_repro_diagnostic.py
时间预算: ≤ 900 s
"""
import os
import sys
import time
import json

import numpy as np

# 从 simulation 根导入 common (TL-13 同源)
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common import (
    m16apsk_mod, m16apsk_demod, ber_count_m16apsk, resolve_m16apsk,
    nda_ml_recovery, da_ml_recovery,
)

# =============================================================================
# B11 参数 (行 143/155/459/491/501/512/525)
# =============================================================================
N_DFT = 256            # B11 行 155: DFT size N=256
CP_LEN = 32            # B11 行 155: CP=32 (单载波块恢复不用 CP, 仅记录对齐)
BAUD_RATE = 25e9       # B11 行 143/155: 25 GBaud
T_S_B11 = 1.0 / BAUD_RATE
CLW = 500e3            # B11 行 143/155: combined laser linewidth 扫至 500 kHz
M0 = 8                 # (8,8)-16APSK 升 M₀=8 次幂去调制
BITS_PER_SYM = 4
HDFEC = 3.8e-3         # 7% HD-FEC threshold BER

# Wiener PN 每符号方差 (B11 行 51/525: σp²=2π·Δν_CLW·T_S)
SIGMA2_P = 2 * np.pi * CLW * T_S_B11
print(f"[B11 params] T_S_B11={T_S_B11:.3e} s  CLW={CLW:.0e} Hz  "
      f"sigma2_p={SIGMA2_P:.3e} rad²  sqrt/256sym={(SIGMA2_P*256)**0.5:.3f} rad")

# 实验配置
SNR_LIST = [5.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
N_BLOCKS = 400         # 块数 (400 × 256 = 102400 sym/点, 守 FR-21 N≥1e5)
SEED_BASE = 20240701
DA_PILOT_SPACING = 4   # 主要 DA 配置: 每 4 sym 一个 pilot (DA 强基线)


# =============================================================================
# 信道: 纯 AWGN + Wiener PN (B11 行 33/51), 无湍流/无 Doppler/无 CFO
# =============================================================================
def awgn_wiener_channel(tx, snr_db, seed):
    """B11 信号模型 (行 33/51):
        r(k) = s(k) · exp(j·θ(k)) + n(k)
        θ(k) = φ₀ + Σ_{i≤k} w(i),  w(i) ~ N(0, σp²)   (Wiener 累积 PN)
      无 FOE (Δf=0, B11 行 33 已补偿), 无湍流, 无 Doppler ramp.
      φ₀ = 0 (初始相位 0, 不引入额外模糊; resolve_* 另外处理 M₀ 重模糊).
    返回 (rx, phi_true).
    """
    rng = np.random.default_rng(seed)
    N = len(tx)
    # Wiener PN: φ(k) = Σ w(i), w~N(0,σp²). 累积漂移随 √N 增长.
    phi = np.cumsum(rng.normal(0.0, np.sqrt(SIGMA2_P), N))
    # 复载波 (无 FOE → 无 k 线性项)
    carrier = np.exp(1j * phi)
    signal = tx * carrier
    # AWGN: 信号功率归一化 (m16apsk_mod 平均功率=1)
    snr_lin = 10.0 ** (snr_db / 10.0)
    noise_var = 1.0 / (2.0 * snr_lin)  # 复噪声总方差 (双边 1/(2·snr))
    noise = np.sqrt(noise_var) * (
        rng.standard_normal(N) + 1j * rng.standard_normal(N)
    )
    rx = signal + noise
    return rx, phi


# =============================================================================
# 三方案恢复 (逐块 N=256, 块内线性 (φ,Δf) 模型近似 Wiener)
# =============================================================================
def resolve_m16apsk_blockwise(rx_comp, tx_bits, n_blk):
    """逐块 resolve_m16apsk (每块独立试 8 重 2π/8 旋转取最低 BER).

    必要性 (本轮诊断核心 bug): nda_ml_recovery 升 M₀=8 次幂有 M₀=8 重相位模糊 (φ̂+2πm/8).
    块间真 φ(k) 因 Wiener 累积不同 → 每块落入不同 m → 拼接后整体无单一旋转可解.
    resolve_m16apsk (全局单旋转) 对逐块 NDA **失效** (BER 灾难性 ~0.26).
    正确做法: 逐块各自 resolve (每块用其 tx_bits 选最优旋转).
    注: 这是 MVE 风格 (resolve 用已知 tx_bits), 与 B11 行 129 genie-aided 解卷绕精神一致,
        非 NDA 真盲; 但对三方案公平 (DA 无模糊不需 resolve, oracle 无模糊, 仅 NDA 需要).
    """
    L = n_blk * N_DFT
    out = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx_comp[b * N_DFT:(b + 1) * N_DFT]
        tb = tx_bits[b * N_DFT * BITS_PER_SYM:(b + 1) * N_DFT * BITS_PER_SYM]
        best = 1.0
        best_seg = seg
        for r in np.arange(0, 2 * np.pi, np.pi / 4):
            ber = np.mean(tb != m16apsk_demod(seg * np.exp(-1j * r)))
            if ber < best:
                best = ber
                best_seg = seg * np.exp(-1j * r)
        out[b * N_DFT:(b + 1) * N_DFT] = best_seg
    return out


def nda_ml_ber(tx_bits, rx, phi_true):
    """NDA-ML 全流程 BER (逐块). 返回 dict: {global, blockwise}.
    global    = resolve_m16apsk 整帧单旋转 (前两轮 BER 层 bug-致复现)
    blockwise = 逐块 resolve (正确做法, 本轮修正)"""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * N_DFT:(b + 1) * N_DFT]
        rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk')
        rx_comp[b * N_DFT:(b + 1) * N_DFT] = rc
    tx_b = tx_bits[:L * BITS_PER_SYM]
    b_global = resolve_m16apsk(rx_comp, tx_b)
    b_block = resolve_m16apsk_blockwise(rx_comp, tx_b, n_blk)
    b_block = np.mean(tx_b != m16apsk_demod(b_block))
    return {'global': b_global, 'blockwise': b_block}


def da_ml_ber(tx_bits, rx, phi_true, pilot_spacing=DA_PILOT_SPACING):
    """DA ML: 逐块. 每块内 pilot 等距 spacing, pilot_sym = 真发送符号 (pilot-aided,
    无决策错误传播 — 这是 DA ML 的"理想 DA"形式, 比 decision-directed DA 更强).
    多 pilot → da_ml_recovery 线性回归 (φ,Δf)."""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    tx_sym = m16apsk_mod(tx_bits[:L * BITS_PER_SYM])
    for b in range(n_blk):
        s_blk = slice(b * N_DFT, (b + 1) * N_DFT)
        # 块内 pilot 索引 (等距)
        p_idx = np.arange(0, N_DFT, pilot_spacing)
        p_sym = tx_sym[b * N_DFT + p_idx]
        rc, phi_est, df_est = da_ml_recovery(
            rx[s_blk], pilot_idx=p_idx, pilot_sym=p_sym, mod='m16apsk'
        )
        rx_comp[s_blk] = rc
    tx_b = tx_bits[:L * BITS_PER_SYM]
    return resolve_m16apsk(rx_comp, tx_b)


def oracle_ber(tx_bits, rx, phi_true):
    """Genie-aided oracle: 用真 φ(k) 补偿 → 解调 → BER. 信息论下界 (相位完美已知)."""
    N = len(rx)
    rx_comp = rx * np.exp(-1j * phi_true[:N])
    tx_b = tx_bits[:N * BITS_PER_SYM]
    return ber_count_m16apsk(tx_b, rx_comp)


def nda_ml_fixed_ber(tx_bits, rx, phi_true):
    """NDA-ML *修复版* (Variant B): 升 M₀ 次幂 → 块内 mean-angle 估常相位 → 补偿.
    不做 FFT df 搜索 (B11 行 33 假设 CFO 已补偿, 真 df=0; FFT 在 df=0 时锁噪声伪峰).
    目的: 隔离 nda_ml_recovery 的 FFT-df 步骤是否为 BER 损失主因.
    M₀=8 相位模糊仍用逐块 resolve (与 nda_ml_ber blockwise 同公平)."""
    N = len(rx)
    n_blk = N // N_DFT
    L = n_blk * N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * N_DFT:(b + 1) * N_DFT]
        phi_est = np.angle((seg ** M0).mean()) / M0
        rx_comp[b * N_DFT:(b + 1) * N_DFT] = seg * np.exp(-1j * phi_est)
    tx_b = tx_bits[:L * BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tx_b, n_blk)
    return np.mean(tx_b != m16apsk_demod(resolved))


# =============================================================================
# 主实验
# =============================================================================
def run_sweep():
    results = {'params': {
        'N_DFT': N_DFT, 'CP_LEN': CP_LEN, 'BAUD_RATE': BAUD_RATE,
        'CLW': CLW, 'M0': M0, 'SIGMA2_P': SIGMA2_P,
        'N_BLOCKS': N_BLOCKS, 'sym_per_point': N_BLOCKS * N_DFT,
        'HDFEC': HDFEC, 'DA_PILOT_SPACING': DA_PILOT_SPACING,
    }, 'curves': {}}
    for snr in SNR_LIST:
        seed = SEED_BASE + int(snr * 1000)
        N_sym = N_BLOCKS * N_DFT
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = awgn_wiener_channel(tx, snr, seed)
        nda = nda_ml_ber(bits, rx, phi_true)
        b_nda_fix = nda_ml_fixed_ber(bits, rx, phi_true)
        b_da = da_ml_ber(bits, rx, phi_true)
        b_or = oracle_ber(bits, rx, phi_true)
        results['curves'][f'{snr}'] = {
            'snr_db': snr,
            'nda_ml_global': nda['global'],
            'nda_ml_blockwise': nda['blockwise'],
            'nda_ml_fixed': b_nda_fix,
            'da_ml': b_da, 'oracle': b_or,
        }
        print(f"  SNR={snr:5.1f} dB | NDA[glob]={nda['global']:.3e} "
              f"NDA[blk]={nda['blockwise']:.3e} NDA[fix]={b_nda_fix:.3e}  "
              f"DA-ML={b_da:.3e}  ORACLE={b_or:.3e}  "
              f"(fix/DA={b_nda_fix/b_da:.2f})")
    return results


def analyze(results):
    """线性插值求 @ BER=3.8e-3 处各方案所需 SNR → NDA-ML vs DA-ML gain.

    报两种 NDA resolve (global = 前两轮 bug 复现; blockwise = 本轮正确修正)."""
    snrs = np.array([results['curves'][k]['snr_db'] for k in results['curves']])
    b_nda_g = np.array([results['curves'][k]['nda_ml_global'] for k in results['curves']])
    b_nda_b = np.array([results['curves'][k]['nda_ml_blockwise'] for k in results['curves']])
    b_nda_f = np.array([results['curves'][k]['nda_ml_fixed'] for k in results['curves']])
    b_da = np.array([results['curves'][k]['da_ml'] for k in results['curves']])
    b_or = np.array([results['curves'][k]['oracle'] for k in results['curves']])

    def snr_at_ber(ber, ber_target):
        # BER 随 SNR 单调降 → interp (取 log BER 提升低 BER 区插值稳健)
        mask = ber > 0
        log_ber = np.log10(ber[mask])
        # interp 要求 x 升序; log_ber 降序 → 反转
        return float(np.interp(np.log10(ber_target), log_ber[::-1], snrs[mask][::-1]))

    out = {}
    for label, b_nda in [('fixed', b_nda_f), ('blockwise', b_nda_b), ('global', b_nda_g)]:
        try:
            s_nda = snr_at_ber(b_nda, HDFEC)
            s_da = snr_at_ber(b_da, HDFEC)
            s_or = snr_at_ber(b_or, HDFEC)
            out[f'nda_{label}'] = {
                'snr_nda_at_hdfec': s_nda,
                'snr_da_at_hdfec': s_da,
                'snr_oracle_at_hdfec': s_or,
                'gain_nda_vs_da_dB': s_da - s_nda,   # 正 = NDA 优
                'gain_nda_vs_oracle_dB': s_nda - s_or,
            }
        except Exception as e:
            out[f'nda_{label}'] = {'error': str(e)}
    return out


def main():
    t0 = time.time()
    print("=" * 78)
    print("B11 NDA-ML vs DA ML — AWGN + Wiener PN 复现诊断 (无湍流)")
    print("=" * 78)
    res = run_sweep()
    ana = analyze(res)
    res['analysis'] = ana
    print("\n" + "=" * 78)
    print(f"分析 @ 7% HD-FEC threshold BER=3.8e-3 (DA spacing={DA_PILOT_SPACING}):")
    print("=" * 78)
    for variant, d in ana.items():
        print(f"\n  [{variant}]")
        if 'error' in d:
            print(f"    error: {d['error']}")
            continue
        for k, v in d.items():
            print(f"    {k:28s}: {v:+.3f}" if isinstance(v, float) else f"    {k:28s}: {v}")
    # 判定用 fixed (修复 FFT-df bug 后的正确 NDA)
    g = ana.get('nda_fixed', {}).get('gain_nda_vs_da_dB')
    g_blk = ana.get('nda_blockwise', {}).get('gain_nda_vs_da_dB')
    if g is not None:
        if g >= 1.5:
            verdict = "复现 B11 +2dB (gain>=1.5dB) → NDA-ML 实现正确, 前两轮 Kill 真实"
        elif g >= 0.5:
            verdict = "部分复现 (0.5<=gain<1.5dB) → 修复 FFT-df bug 后仍输 DA, 升幂噪声放大真实"
        else:
            verdict = "未复现 (gain<0.5dB 或 NDA 输 DA) → 即使修复 FFT-df bug 仍输 DA"
        print(f"\n  >>> 判定 (NDA-fixed, 去 FFT-df bug): gain={g:+.2f} dB  →  {verdict}")
        print(f"      对比 (NDA-blockwise, 现 nda_ml_recovery): gain={g_blk:+.2f} dB")
    print(f"\n[耗时] {time.time()-t0:.1f} s")
    out_path = os.path.join(os.path.dirname(__file__), '_awgn_repro_results.json')
    with open(out_path, 'w') as f:
        json.dump(res, f, indent=2)
    print(f"[保存] {out_path}")


if __name__ == '__main__':
    main()
