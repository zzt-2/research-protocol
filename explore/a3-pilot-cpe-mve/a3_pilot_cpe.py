"""A3 §4a 维度 D MVE — Pilot 前馈 CPE 主方法（M1a/M1b）。

Cheng 2013 公式实现（papers/_read_notes/cheng2013-papu-original.md verified）：
  Eq.(1) 信号模型 s(k) = c(k)·exp(jθ(k)) + n(k)
  Eq.(2) Pilot header 相位估计 φ_hat(m) = arg(sum_{i=0}^{P-1} d*(i)·s(mP+i))
  Eq.(3)(4) Unwrap 算子（等价 numpy.unwrap，rng=π/2 for QPSK）
  Eq.(5) CS 修正核心：φ_u = φ0u - round[(φ0u - φ')/2π]·2π

M1a：时域 frame-header pilot（Cheng 2013 原版，P 个 pilot header/frame）
M1b：频域连续 tone（Cheng 2013 Eq.5 迁移，N_data→0 极限，每 symbol 都有 pilot 参考）

TL-22 教训记录：调试中发现 pilot 位置必须是已知 pilot_sym（with_pilot_header=True），
否则提取的是随机数据相位，pilot CPE 完全失效。
"""
import numpy as np
from a3_baselines import fft_foe


# ═══════════════════════════════════════════════════════════════
# Cheng 2013 公式实现
# ═══════════════════════════════════════════════════════════════
def cheng_eq2_pilot_phase(rx_seg, pilot_seq):
    """Eq.(2)：P 个 pilot symbol 相干积累估相位。

    φ_hat = arg(sum_{i=0}^{P-1} d*(i)·s(i))
    rx_seg: P 个接收 pilot symbol
    pilot_seq: P 个已知 pilot symbol（d(i)）
    返回 φ_hat（弧度）。
    """
    corr = np.sum(np.conj(pilot_seq) * rx_seg)
    return np.angle(corr)


def cheng_eq5_cs_correction(phi0u, phi_ref):
    """Eq.(5)：CS（cycle slip）修正核心公式。

    φ_u = φ0u - round[(φ0u - φ')/2π]·2π
    phi0u: 普通 unwrap 后相位（可能带整数倍 2π CS）
    phi_ref: pilot 参考（从 pilot 估的连续相位）
    返回 CS 修正后相位。

    机制：差 > π/2（round 出 ±1）则 ±2π 修正；差 < π/2（round 出 0）不动。
    """
    n_slip = np.round((phi0u - phi_ref) / (2 * np.pi))
    return phi0u - n_slip * 2 * np.pi


def unwrap_qpsk(phi_raw, rng=np.pi/2):
    """Eq.(3)(4)：QPSK unwrap 算子（等价 numpy.unwrap with period=2π，但可配 rng）。

    对 QPSK，rng=π/2（partitioning 间隔）。等价 numpy.unwrap 默认 period=2π。
    """
    return np.unwrap(phi_raw, discont=np.pi)  # 标准 unwrap，discont=π


def count_cycle_slips(phi_est, phi_true, thresh=np.pi/2):
    """统计 cycle slip 率（Cheng 2013 仿真阈值）。

    估计相位 vs 真值绝对差 > thresh 计为 CS。
    返回 CS 率（CS 样本数 / 总样本数）。
    """
    err = phi_est - phi_true
    err_wrapped = (err + np.pi) % (2*np.pi) - np.pi
    return np.mean(np.abs(err_wrapped) > thresh)


# ═══════════════════════════════════════════════════════════════
# M1a：时域 frame-header pilot + Cheng 2013 Eq.1-5
# ═══════════════════════════════════════════════════════════════
def m1a_frame_header_pilot(ch, P=4, frame_len=32, with_cs_correction=True):
    """M1a：时域 frame-header pilot。

    结构：每 frame_len symbol，前 P 个是 pilot header（已知 BPSK 训练序列），后 (frame_len-P) 是 data。
    overhead = P / frame_len
    流程：
      1. fft_foe 估多普勒粗频偏
      2. Eq.(2) 每 frame 用 P 个 pilot 相干积累估 frame 起始相位
      3. unwrap 得连续参考 φ'
      4. Eq.(5) CS 修正（可选）
      5. 插值补偿 data symbol

    Args:
        ch: generate_shared_realization 输出（必须 with_pilot_header=True, frame_len 一致）
        P: pilot header 长度
        frame_len: frame 长度
        with_cs_correction: 是否用 Cheng Eq.5 CS 修正
    返回 rx_comp, phi_est, cs_rate, params。
    """
    N = len(ch['rx_raw'])
    rx = ch['rx_raw']
    # 1. 多普勒粗估
    f0 = fft_foe(rx, M=4)
    rx_defo = rx * np.exp(-1j * f0 * np.arange(N))

    # 2. 生成 pilot 训练序列（已知 BPSK ±1，固定种子保证可复现）
    rng = np.random.RandomState(123)
    pilot_seq = (2*rng.randint(0, 2, P) - 1).astype(complex)  # ±1 BPSK

    # 3. 每 frame 用 Eq.(2) 估相位
    n_frames = N // frame_len
    pilot_time = []
    pilot_phase_est = []
    for m in range(n_frames):
        fstart = m * frame_len
        pidx = np.arange(fstart, fstart + P)
        if pidx[-1] >= N:
            break
        phi_m = cheng_eq2_pilot_phase(rx_defo[pidx], pilot_seq)
        pilot_phase_est.append(phi_m)
        pilot_time.append(fstart + P // 2)

    pilot_phase_est = np.array(pilot_phase_est)
    pilot_time = np.array(pilot_time)

    # 4. unwrap（Eq.3,4）
    pilot_phase_u = unwrap_qpsk(pilot_phase_est)

    # 5. Eq.(5) CS 修正（用 unwrap 后自身作 φ' 参考，抑制 false fluctuation）
    if with_cs_correction:
        # φ' 用平滑后的 pilot 相位（移动平均）
        from scipy.ndimage import uniform_filter1d
        phi_smooth = uniform_filter1d(pilot_phase_u, size=3, mode='nearest')
        pilot_phase_u = cheng_eq5_cs_correction(pilot_phase_u, phi_smooth)

    # 6. 插值得每 symbol 相位参考
    phi_ref = np.interp(np.arange(N), pilot_time, pilot_phase_u)

    # 7. 补偿
    rx_comp = rx_defo * np.exp(-1j * phi_ref)

    # data mask（pilot header 位置不算 BER）
    data_mask = np.ones(N, dtype=bool)
    for m in range(n_frames):
        fstart = m * frame_len
        data_mask[fstart:fstart + P] = False

    # CS 率统计
    phi_true_resid = ch['phi_ao'] + ch['phi_doppler'] - f0 * np.arange(N)
    cs_rate = count_cycle_slips(phi_ref, phi_true_resid)

    params = {'P': P, 'frame_len': frame_len, 'overhead': P/frame_len,
              'with_cs_correction': with_cs_correction, 'f0_est': f0}
    return rx_comp, phi_ref, cs_rate, params, data_mask


# ═══════════════════════════════════════════════════════════════
# M1b：频域连续 tone + Cheng 2013 Eq.5 迁移
# ═══════════════════════════════════════════════════════════════
def m1b_frequency_tone(ch, tone_spacing=2, with_cs_correction=True):
    """M1b：频域连续 tone（密集 pilot，N_data→0 极限）。

    结构：每 tone_spacing symbol 一个 pilot（密集），近似连续 tone。
    overhead = 1 / tone_spacing
    与 M1a 区别：pilot 更密，每 symbol 都有近的 pilot 参考，不需长插值。
    Eq.(5) 直接用（symbol-by-symbol，不依赖 pilot 插值形态）。

    Args:
        ch: generate_shared_realization 输出（必须 with_pilot_header=True, frame_len=tone_spacing）
        tone_spacing: pilot 间隔（symbol 数）
    """
    N = len(ch['rx_raw'])
    rx = ch['rx_raw']
    f0 = fft_foe(rx, M=4)
    rx_defo = rx * np.exp(-1j * f0 * np.arange(N))

    pilot_sym = (1 + 1j) / np.sqrt(2)  # 单一已知 pilot symbol
    pilot_idx = ch['pilot_idx']

    # 每 pilot 估相位（单 symbol，N_data→0 极限）
    pilot_phase_est = np.angle(rx_defo[pilot_idx] / pilot_sym)
    pilot_phase_u = unwrap_qpsk(pilot_phase_est)

    # Eq.(5) CS 修正
    if with_cs_correction:
        from scipy.ndimage import uniform_filter1d
        phi_smooth = uniform_filter1d(pilot_phase_u, size=5, mode='nearest')
        pilot_phase_u = cheng_eq5_cs_correction(pilot_phase_u, phi_smooth)

    # 插值（密集 pilot，插值损失小）
    phi_ref = np.interp(np.arange(N), pilot_idx, pilot_phase_u)
    rx_comp = rx_defo * np.exp(-1j * phi_ref)

    data_mask = ch['data_bits_mask'].copy()
    phi_true_resid = ch['phi_ao'] + ch['phi_doppler'] - f0 * np.arange(N)
    cs_rate = count_cycle_slips(phi_ref, phi_true_resid)

    params = {'tone_spacing': tone_spacing, 'overhead': 1.0/tone_spacing,
              'with_cs_correction': with_cs_correction, 'f0_est': f0}
    return rx_comp, phi_ref, cs_rate, params, data_mask


if __name__ == '__main__':
    # M1a/M1b 自检（strong γ=20dB，gap_fill 应 >50%）
    from a3_channel import generate_shared_realization, ber_count

    print("=== M1a frame-header pilot 自检 ===")
    for turb in ['weak', 'strong']:
        for gdb in [10, 20]:
            for P, fl in [(4, 32), (8, 64)]:
                ch = generate_shared_realization(8192, gdb, turb, seed=42,
                                                  with_pilot_header=True, frame_len=fl)
                rx_comp, phi_ref, cs_rate, params, dm = m1a_frame_header_pilot(ch, P=P, frame_len=fl)
                ber = ber_count(ch['tx'], rx_comp, data_mask=dm, resolve_ambiguity=True)
                rx_oracle = ch['rx_raw'] * np.exp(-1j * ch['phi_total'])
                ber_oracle = ber_count(ch['tx'], rx_oracle, resolve_ambiguity=True)
                f0 = fft_foe(ch['rx_raw'], M=4)
                rx_raw = ch['rx_raw'] * np.exp(-1j * f0 * np.arange(len(ch['rx_raw'])))
                ber_raw = ber_count(ch['tx'], rx_raw, resolve_ambiguity=True)
                gf = (ber_raw - ber) / max(ber_raw - ber_oracle, 1e-9)
                print(f"  {turb} γ={gdb}dB P={P} fl={fl}: pilot BER={ber:.6f}, "
                      f"gap_fill={gf:.1%}, cs_rate={cs_rate:.4f}")

    print("\n=== M1b 频域 tone 自检 ===")
    for turb in ['weak', 'strong']:
        for gdb in [10, 20]:
            for sp in [2, 4, 8]:
                ch = generate_shared_realization(8192, gdb, turb, seed=42,
                                                  with_pilot_header=True, frame_len=sp)
                rx_comp, phi_ref, cs_rate, params, dm = m1b_frequency_tone(ch, tone_spacing=sp)
                ber = ber_count(ch['tx'], rx_comp, data_mask=dm, resolve_ambiguity=True)
                rx_oracle = ch['rx_raw'] * np.exp(-1j * ch['phi_total'])
                ber_oracle = ber_count(ch['tx'], rx_oracle, resolve_ambiguity=True)
                f0 = fft_foe(ch['rx_raw'], M=4)
                rx_raw = ch['rx_raw'] * np.exp(-1j * f0 * np.arange(len(ch['rx_raw'])))
                ber_raw = ber_count(ch['tx'], rx_raw, resolve_ambiguity=True)
                gf = (ber_raw - ber) / max(ber_raw - ber_oracle, 1e-9)
                print(f"  {turb} γ={gdb}dB sp={sp}: pilot BER={ber:.6f}, "
                      f"gap_fill={gf:.1%}, cs_rate={cs_rate:.4f}")
