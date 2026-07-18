#!/usr/bin/env python3
"""重验: KF 内部机制 + 导频设计 + 公平性 (TL-24)

从 common.py 导入，覆盖 CONCLUSIONS.md 待重验结论:
  P-05: KF 公平性 (h_med 均衡下 KF pilot vs Fixed)
  P-06: KF h 估计质量 (corr, MSE)
  C4-08: R 矩阵 / Q 灵敏度 / P 初始化
  C4-09: 导频开销 / 导频放置
  P-07: BLOCK 大小

配置: 3 湍流 × 10 seeds × 20dB SNR × 10K 符号
预计运行时间: ~5 分钟
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
import json, time

Ns = 10_000
GAMMA_BAR = 100  # 20dB
N_SEEDS = 10
SEEDS = list(range(N_SEEDS))
TURBS = ['weak', 'moderate', 'strong']
F_DOT = DOPPLER_HIGH

# ═══════════════════════════════════════════════════════════════
# Helper: KF pilot with customizable R/Q/P
# ═══════════════════════════════════════════════════════════════
def kf_pilot_custom(rx, gamma_bar, turb_name, n_pilots, h_med,
                    f_dot=DOPPLER_HIGH, block_size=BLOCK,
                    alpha_ema=0.5, Q_fine_df=(50e3)**2,
                    r_mode='pilot', q_phi_scale=1.0,
                    p00=(np.pi/4)**2, p11=(2*np.pi*100e3)**2):
    """KF pilot recovery with customizable R/Q/P parameters.

    r_mode: 'pilot' | 'frame' | 'awgn' | 'clamp'
    """
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2
    Q_fine[0, 0] *= q_phi_scale

    F_mat = np.array([[1.0, T_S], [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    x = np.array([0.0, 0.0])
    P = np.diag([p00, p11])

    h_est = max(h_med, 0.01)
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    def compute_R(h_val):
        if r_mode == 'pilot':
            return 1.0 / (2 * gamma_bar * max(h_val, 0.01))
        elif r_mode == 'frame':
            return 1.0 / (2 * gamma_bar * max(h_med, 0.01))
        elif r_mode == 'awgn':
            return 1.0 / (2 * gamma_bar)
        elif r_mode == 'clamp':
            return 1.0 / (2 * gamma_bar * max(h_val, 0.1))
        else:
            raise ValueError(f"Unknown r_mode: {r_mode}")

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        pilot_end = start + n_pilots

        # Phase 1: pilots
        for k_idx in range(start, pilot_end):
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            R_val = compute_R(h_est)
            s_p = known_pilots[k_idx - start]
            y = rx_foc[k_idx] * np.conj(s_p)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

        # Phase 2: h estimation from pilots
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        # Phase 3: data (decision-directed)
        for k_idx in range(pilot_end, end):
            R_val = compute_R(h_est)
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = ((np.sign(np.real(rx_rotated))) +
                     1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)
            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    rem_start = n_blocks * block_size
    if rem_start < N:
        for k_idx in range(rem_start, N):
            R_val = compute_R(h_est)
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = ((np.sign(np.real(rx_rotated))) +
                     1j * (np.sign(np.imag(rx_rotated)))) / np.sqrt(2)
            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    return corrected, h_est_per_block


# ═══════════════════════════════════════════════════════════════
# Helper: Pilot insertion with placement mode
# ═══════════════════════════════════════════════════════════════
def insert_pilots_placement(shared, n_pilots_per_block=5, mode='front',
                            block_size=BLOCK):
    """Insert pilots with configurable placement.

    mode: 'front' (default) | 'uniform' | 'center'
    """
    rx_raw = shared['rx_raw']
    tx = shared['tx'].copy()
    bits = shared['bits']
    h = shared['h']
    phi = shared['phi']
    gamma_bar = shared['gamma_bar']
    Ns = shared['Ns']
    n_blocks = Ns // block_size

    known_pilots = get_pilots(n_pilots_per_block)
    pilot_indices = []
    data_indices = []

    for b in range(n_blocks):
        base = b * block_size
        if mode == 'front':
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + p)
        elif mode == 'uniform':
            step = block_size / (n_pilots_per_block + 1)
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + int(step * (p + 1)))
        elif mode == 'center':
            center = block_size // 2
            start_offset = center - n_pilots_per_block // 2
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + start_offset + p)

        pilot_set = set(pilot_indices[len(pilot_indices) - n_pilots_per_block:])
        for d in range(block_size):
            idx = base + d
            if idx not in pilot_set:
                data_indices.append(idx)

    pilot_indices = np.array(pilot_indices, dtype=int)
    data_indices = np.array(data_indices, dtype=int)

    for i, idx in enumerate(pilot_indices):
        tx[idx] = known_pilots[i % len(known_pilots)]

    carrier = np.exp(1j * phi)
    noise = rx_raw - shared['tx'] * np.sqrt(h) * carrier
    signal_pilot = tx * np.sqrt(h) * carrier
    rx_pilot = signal_pilot + noise

    data_bits = np.zeros(len(data_indices) * 2, dtype=int)
    for i, idx in enumerate(data_indices):
        data_bits[2*i] = bits[2*idx]
        data_bits[2*i+1] = bits[2*idx+1]

    return rx_pilot, pilot_indices, data_indices, data_bits


# ═══════════════════════════════════════════════════════════════
# Helper: Channel generation with custom block size
# ═══════════════════════════════════════════════════════════════
def generate_shared_bs(Ns, gamma_bar, turb_name, f_dot, seed, block_size):
    """Generate shared realization with custom block size."""
    np.random.seed(seed)
    a, b = TURB[turb_name]

    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)

    h = gg_block(Ns, a, b, bs=block_size)
    n_blocks = Ns // block_size
    h_blocks = np.array([h[i * block_size] for i in range(n_blocks)])
    h_med = np.median(h_blocks)

    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)

    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_raw = signal + noise

    return {
        'rx_raw': rx_raw, 'bits': bits, 'tx': tx,
        'h': h, 'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
        'Ns': Ns, 'gamma_bar': gamma_bar,
        'turb_name': turb_name, 'f_dot': f_dot,
    }


# ═══════════════════════════════════════════════════════════════
# Section A: P-05 KF Fairness (h_med vs oracle equalization)
# ═══════════════════════════════════════════════════════════════
def run_fairness():
    n_pilots = 5
    schemes = [
        'Fixed_default_oracle', 'Fixed_default_hmed',
        'Fixed_optimal_oracle', 'Fixed_optimal_hmed',
        'KFpilot_oracle', 'KFpilot_hmed',
    ]
    ber_data = {s: {t: [] for t in TURBS} for s in schemes}

    for turb in TURBS:
        print(f"  {turb}...", end='', flush=True)
        for seed in SEEDS:
            shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)

            # Fixed default (Nw=64, omega_n=8e6)
            rx_eq = equalize_oracle(shared)
            rx = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG)
            ber_data['Fixed_default_oracle'][turb].append(
                ber_eval(shared['bits'], rx, mode='oracle'))

            rx_eq = equalize_hmed(shared)
            rx = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG)
            ber_data['Fixed_default_hmed'][turb].append(
                ber_eval(shared['bits'], rx, mode='oracle'))

            # Fixed optimal (Nw=256, omega_n=20e6)
            rx_eq = equalize_oracle(shared)
            rx = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG_OPTIMAL[turb])
            ber_data['Fixed_optimal_oracle'][turb].append(
                ber_eval(shared['bits'], rx, mode='oracle'))

            rx_eq = equalize_hmed(shared)
            rx = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG_OPTIMAL[turb])
            ber_data['Fixed_optimal_hmed'][turb].append(
                ber_eval(shared['bits'], rx, mode='oracle'))

            # KF pilot
            corrected, data_idx, data_bits, _ = run_kf_pilot(
                shared, n_pilots, eq_mode='oracle')
            ber_data['KFpilot_oracle'][turb].append(
                ber_eval(data_bits, corrected[data_idx], mode='oracle'))

            corrected, data_idx, data_bits, _ = run_kf_pilot(
                shared, n_pilots, eq_mode='hmed')
            ber_data['KFpilot_hmed'][turb].append(
                ber_eval(data_bits, corrected[data_idx], mode='oracle'))

        print(" done")

    results = {}
    for s in schemes:
        results[s] = {t: {'mean': float(np.mean(ber_data[s][t])),
                          'per_seed': [float(x) for x in ber_data[s][t]]}
                     for t in TURBS}

    print("\n  Fairness Summary (h_med equalization):")
    for turb in TURBS:
        kf_ber = results['KFpilot_hmed'][turb]['mean']
        fd_ber = results['Fixed_default_hmed'][turb]['mean']
        fo_ber = results['Fixed_optimal_hmed'][turb]['mean']
        gain_d = db_ratio(fd_ber, kf_ber)
        gain_o = db_ratio(fo_ber, kf_ber)
        print(f"    {turb:>8s}: KF={kf_ber:.4e}  "
              f"Fixed_def={fd_ber:.4e} ({gain_d:+.1f}dB)  "
              f"Fixed_opt={fo_ber:.4e} ({gain_o:+.1f}dB)")

    return results


# ═══════════════════════════════════════════════════════════════
# Section B: P-06 h Estimation Quality
# ═══════════════════════════════════════════════════════════════
def run_h_estimation():
    n_pilots = 5
    results = {}

    for turb in TURBS:
        corrs, mses = [], []
        for seed in SEEDS:
            shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
            corrected, data_idx, data_bits, h_est = run_kf_pilot(
                shared, n_pilots, eq_mode='oracle')

            n_blocks = Ns // BLOCK
            h_true = np.array([shared['h'][b * BLOCK] for b in range(n_blocks)])
            h_e = h_est[:n_blocks]

            corrs.append(np.corrcoef(h_true, h_e)[0, 1])
            mses.append(float(np.mean((h_true - h_e)**2)))

        results[turb] = {
            'corr_mean': float(np.mean(corrs)),
            'corr_per_seed': [float(x) for x in corrs],
            'mse_mean': float(np.mean(mses)),
        }
        print(f"  {turb:>8s}: corr={np.mean(corrs):.3f}, MSE={np.mean(mses):.4f}")

    return results


# ═══════════════════════════════════════════════════════════════
# Section C: C4-08 R Matrix Comparison
# ═══════════════════════════════════════════════════════════════
def run_r_matrix():
    r_modes = ['pilot', 'frame', 'awgn', 'clamp']
    n_pilots = 5
    results = {}

    for turb in TURBS:
        results[turb] = {}
        for rm in r_modes:
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots(shared, n_pilots)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots,
                    shared['h_med'], F_DOT, r_mode=rm)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))

            mean_ber = float(np.mean(bers))
            results[turb][rm] = {'mean': mean_ber, 'per_seed': [float(x) for x in bers]}
            print(f"  {turb:>8s} | {rm:>6s} | BER={mean_ber:.4e}")

    # Ratio analysis
    print("\n  R matrix ratio (vs pilot mode):")
    for turb in TURBS:
        pilot_ber = results[turb]['pilot']['mean']
        row = f"    {turb:>8s}:"
        for rm in r_modes:
            ratio = results[turb][rm]['mean'] / pilot_ber if pilot_ber > 0 else 0
            row += f"  {rm}={ratio:.2f}x"
        print(row)

    return results


# ═══════════════════════════════════════════════════════════════
# Section D: C4-08 Q Sensitivity
# ═══════════════════════════════════════════════════════════════
def run_q_sensitivity():
    Q_fine_df_vals = [(10e3)**2, (30e3)**2, (50e3)**2,
                      (100e3)**2, (200e3)**2, (500e3)**2]
    Q_phi_scales = [0.1, 0.5, 1.0, 2.0, 10.0]
    n_pilots = 5
    results = {'qdf_sweep': {}, 'qphi_sweep': {}}

    print("  Q[1,1] sweep:")
    for turb in TURBS:
        results['qdf_sweep'][turb] = {}
        baseline_qdf = (50e3)**2
        for qdf in Q_fine_df_vals:
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots(shared, n_pilots)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots,
                    shared['h_med'], F_DOT, Q_fine_df=qdf)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            results['qdf_sweep'][turb][str(qdf)] = mean_ber
            q_khz = np.sqrt(qdf) / 1e3
            marker = " <--" if qdf == baseline_qdf else ""
            print(f"    {turb:>8s} | {q_khz:>6.0f}kHz | BER={mean_ber:.4e}{marker}")

    print("  Q[0,0] sweep:")
    for turb in TURBS:
        results['qphi_sweep'][turb] = {}
        for scale in Q_phi_scales:
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots(shared, n_pilots)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots,
                    shared['h_med'], F_DOT, q_phi_scale=scale)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            results['qphi_sweep'][turb][str(scale)] = mean_ber
            marker = " <--" if scale == 1.0 else ""
            print(f"    {turb:>8s} | {scale:>5.1f}x | BER={mean_ber:.4e}{marker}")

    return results


# ═══════════════════════════════════════════════════════════════
# Section E: C4-08 P Initialization
# ═══════════════════════════════════════════════════════════════
def run_p_init():
    P00_vals = [0.01, 0.1, (np.pi/4)**2, np.pi**2, 10*np.pi**2]
    P00_labels = ['0.01', '0.1', '(pi/4)^2', 'pi^2', '10pi^2']
    P11_freq_vals = [10e3, 100e3, 1e6]
    P11_labels = ['10kHz', '100kHz', '1MHz']
    n_pilots = 5
    results = {'p00_sweep': {}, 'p11_sweep': {}}

    default_p11 = (2 * np.pi * 100e3 * T_S)**2

    print("  P[0,0] sweep:")
    for turb in TURBS:
        results['p00_sweep'][turb] = {}
        baseline = (np.pi/4)**2
        for p00, label in zip(P00_vals, P00_labels):
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots(shared, n_pilots)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots,
                    shared['h_med'], F_DOT, p00=p00, p11=default_p11)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            results['p00_sweep'][turb][label] = mean_ber
            baseline_ber = results['p00_sweep'][turb].get('(pi/4)^2', mean_ber)
            ratio = mean_ber / baseline_ber if baseline_ber > 0 else 0
            marker = " <--" if label == '(pi/4)^2' else ""
            print(f"    {turb:>8s} | {label:>10s} | BER={mean_ber:.4e} ({ratio:.2f}x){marker}")

    default_p00 = (np.pi/4)**2

    print("  P[1,1] sweep:")
    for turb in TURBS:
        results['p11_sweep'][turb] = {}
        for freq, label in zip(P11_freq_vals, P11_labels):
            p11 = (2 * np.pi * freq * T_S)**2
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots(shared, n_pilots)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots,
                    shared['h_med'], F_DOT, p00=default_p00, p11=p11)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            results['p11_sweep'][turb][label] = mean_ber
            baseline_ber = results['p11_sweep'][turb].get('100kHz', mean_ber)
            ratio = mean_ber / baseline_ber if baseline_ber > 0 else 0
            marker = " <--" if label == '100kHz' else ""
            print(f"    {turb:>8s} | {label:>6s} | BER={mean_ber:.4e} ({ratio:.2f}x){marker}")

    return results


# ═══════════════════════════════════════════════════════════════
# Section F: C4-09 Pilot Overhead Sweep
# ═══════════════════════════════════════════════════════════════
def run_pilot_overhead():
    overhead_pcts = [1, 2, 5, 10, 15, 20, 30]
    results = {}

    for turb in TURBS:
        results[turb] = {}
        for pct in overhead_pcts:
            n_p = pct  # BLOCK=100, so n_pilots=pct gives pct% overhead
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                corrected, data_idx, data_bits, _ = run_kf_pilot(
                    shared, n_p, eq_mode='oracle')
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            net_ber = mean_ber * (1 - pct / 100.0)
            results[turb][str(pct)] = {'ber': mean_ber, 'net_ber': net_ber}
            marker = " <--" if pct == 5 else ""
            print(f"  {turb:>8s} | {pct:>2d}% | BER={mean_ber:.4e} | net={net_ber:.4e}{marker}")

    # Near-optimal check
    print("\n  Near-optimal check (5% vs best net BER):")
    for turb in TURBS:
        net_bers = {p: results[turb][str(p)]['net_ber'] for p in overhead_pcts}
        best_pct = min(net_bers, key=net_bers.get)
        ratio = net_bers[5] / net_bers[best_pct] if net_bers[best_pct] > 0 else float('inf')
        print(f"    {turb:>8s}: best={best_pct}%, 5%/best={ratio:.2f}x")

    return results


# ═══════════════════════════════════════════════════════════════
# Section G: C4-09 Pilot Placement
# ═══════════════════════════════════════════════════════════════
def run_pilot_placement():
    modes = ['front', 'uniform', 'center']
    n_pilots = 5
    results = {}

    for turb in TURBS:
        results[turb] = {}
        for mode in modes:
            bers = []
            for seed in SEEDS:
                shared = generate_shared_realization(Ns, GAMMA_BAR, turb, F_DOT, seed)
                rx_pilot, _, data_idx, data_bits = insert_pilots_placement(
                    shared, n_pilots, mode=mode)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_pilots, shared['h_med'], F_DOT)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            results[turb][mode] = mean_ber
            print(f"  {turb:>8s} | {mode:>8s} | BER={mean_ber:.4e}")

    # Ratio check
    print("\n  Placement ratio (front / best):")
    for turb in TURBS:
        best_mode = min(modes, key=lambda m: results[turb][m])
        ratio = results[turb]['front'] / results[turb][best_mode] if results[turb][best_mode] > 0 else float('inf')
        print(f"    {turb:>8s}: best={best_mode}, front/best={ratio:.2f}x")

    return results


# ═══════════════════════════════════════════════════════════════
# Section H: P-07 Block Size
# ═══════════════════════════════════════════════════════════════
def run_block_size():
    block_sizes = [20, 50, 100, 200]
    pilot_pct = 5  # 5% of block
    results = {}

    for turb in TURBS:
        results[turb] = {}
        for bs in block_sizes:
            n_p = max(1, int(bs * pilot_pct / 100))
            bers = []
            for seed in SEEDS:
                shared = generate_shared_bs(Ns, GAMMA_BAR, turb, F_DOT, seed, bs)
                rx_pilot, _, data_idx, data_bits = insert_pilots_placement(
                    shared, n_p, mode='front', block_size=bs)
                rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], GAMMA_BAR), 3.0)
                corrected, _ = kf_pilot_custom(
                    rx_eq, GAMMA_BAR, turb, n_p, shared['h_med'], F_DOT,
                    block_size=bs)
                bers.append(ber_eval(data_bits, corrected[data_idx], mode='oracle'))
            mean_ber = float(np.mean(bers))
            overhead = n_p / bs
            net_ber = mean_ber * (1 - overhead)
            results[turb][str(bs)] = {
                'ber': mean_ber, 'net_ber': net_ber, 'n_pilots': n_p}
            print(f"  {turb:>8s} | BS={bs:>3d} ({n_p}p) | "
                  f"BER={mean_ber:.4e} | net={net_ber:.4e}")

    # Check BS=20 vs BS=100
    print("\n  BS=20 vs BS=100 ratio (net BER):")
    for turb in TURBS:
        net_20 = results[turb]['20']['net_ber']
        net_100 = results[turb]['100']['net_ber']
        ratio = net_100 / net_20 if net_20 > 0 else float('inf')
        print(f"    {turb:>8s}: BS100/BS20={ratio:.2f}x")

    return results


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
def main():
    t0 = time.time()
    all_results = {
        'config': {
            'Ns': Ns, 'gamma_bar': GAMMA_BAR, 'n_seeds': N_SEEDS,
            'turbs': TURBS, 'f_dot': F_DOT,
            'source': 'common.py (TL-24)',
        }
    }

    sections = [
        ('A', 'P-05: KF Fairness', run_fairness),
        ('B', 'P-06: h Estimation Quality', run_h_estimation),
        ('C', 'C4-08: R Matrix', run_r_matrix),
        ('D', 'C4-08: Q Sensitivity', run_q_sensitivity),
        ('E', 'C4-08: P Initialization', run_p_init),
        ('F', 'C4-09: Pilot Overhead', run_pilot_overhead),
        ('G', 'C4-09: Pilot Placement', run_pilot_placement),
        ('H', 'P-07: Block Size', run_block_size),
    ]

    for code, title, func in sections:
        print(f"\n{'='*60}")
        print(f"Section {code}: {title}")
        print(f"{'='*60}")
        all_results[f'Sec{code}'] = func()

    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"{'='*60}")

    # Save JSON
    results_dir = os.path.join(OUT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(results_dir, 'reverify_kf_internals.json')
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"Results saved to {json_path}")


if __name__ == '__main__':
    main()
