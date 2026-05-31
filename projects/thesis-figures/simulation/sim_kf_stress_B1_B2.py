#!/usr/bin/env python3
"""KF Stress Test B1+B2: Q matrix sensitivity & R matrix alternatives

B1: Q[1,1] sweep, Q[0,0] sweep, Q heatmap
B2: R matrix mode comparison (pilot h / frame h / AWGN / clamped)
"""

from sim_kf_stress_common import *
import itertools

# ═══════════════════════════════════════════════════════════════
# B1 variant: kf_pilot_recovery with Q_phi_scale
# ═══════════════════════════════════════════════════════════════
def kf_pilot_b1(rx, gamma_bar, turb_name, n_pilots, h_med,
                f_dot=DOPPLER_HIGH, block_size=BLOCK,
                alpha_ema=0.5, Q_fine_df=(50e3)**2, Q_phi_scale=1.0):
    """kf_pilot_recovery with adjustable Q[0,0] scale."""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2
    Q_fine[0, 0] *= Q_phi_scale

    F_mat = np.array([[1.0, T_S], [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    x = np.array([0.0, 0.0])
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    h_est = max(h_med, 0.01)
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        pilot_end = start + n_pilots

        for k_idx in range(start, pilot_end):
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
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

        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        for k_idx in range(pilot_end, end):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
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
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
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
# B2 variant: kf_pilot_recovery with r_mode
# ═══════════════════════════════════════════════════════════════
def kf_pilot_b2(rx, gamma_bar, turb_name, n_pilots, h_med,
                f_dot=DOPPLER_HIGH, block_size=BLOCK,
                alpha_ema=0.5, Q_fine_df=(50e3)**2, r_mode='pilot'):
    """kf_pilot_recovery with alternative R computation.

    r_mode:
        'pilot'  -> 1/(2*gamma_bar*h_est_pilot)  [original]
        'frame'  -> 1/(2*gamma_bar*h_med)         [frame-level h]
        'awgn'   -> 1/(2*gamma_bar)               [ignore h]
        'clamp'  -> 1/(2*gamma_bar*max(h_est,0.1)) [deep fade clamp]
    """
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    F_mat = np.array([[1.0, T_S], [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    x = np.array([0.0, 0.0])
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

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

        # Always estimate h from pilots (needed for pilot & clamp modes,
        # and for fair comparison -- estimation effort is identical).
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

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
# Trial runners
# ═══════════════════════════════════════════════════════════════
def trial_b1_qdf(shared, n_pilots, q_df_val, q_phi_scale=1.0):
    """Single trial for B1: sweep Q[1,1] or Q[0,0]."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    corrected, _ = kf_pilot_b1(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'],
        Q_fine_df=q_df_val, Q_phi_scale=q_phi_scale)
    return resolve_qpsk(corrected[data_idx], data_bits)


def trial_b2_rmode(shared, n_pilots, r_mode):
    """Single trial for B2: R matrix mode comparison."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    corrected, _ = kf_pilot_b2(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'], r_mode=r_mode)
    return resolve_qpsk(corrected[data_idx], data_bits)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
def main():
    Ns = 10000
    gamma_bar = GAMMA_BAR_DEFAULT
    n_pilots = 5
    n_seeds = 30
    seeds = list(range(n_seeds))
    turbs = ['weak', 'moderate', 'strong']
    f_dot = DOPPLER_HIGH

    # B1 parameters
    Q_fine_df_vals = [(10e3)**2, (30e3)**2, (50e3)**2,
                      (100e3)**2, (200e3)**2, (500e3)**2]
    Q_phi_scales = [0.1, 0.5, 1.0, 2.0, 10.0]

    # B2 parameters
    r_modes = ['pilot', 'frame', 'awgn', 'clamp']
    r_labels = {
        'pilot':  'R1: pilot h',
        'frame':  'R2: frame h',
        'awgn':   'R3: AWGN',
        'clamp':  'R4: clamp 0.1',
    }

    results = {
        'params': {
            'Ns': Ns, 'gamma_bar': gamma_bar, 'n_pilots': n_pilots,
            'n_seeds': n_seeds, 'turbs': turbs,
            'Q_fine_df_vals': Q_fine_df_vals,
            'Q_phi_scales': Q_phi_scales,
            'r_modes': r_modes,
        },
        'B1_qdf_sweep': {},      # {turb: {qdf_val: mean_BER}}
        'B1_qphi_sweep': {},     # {turb: {scale: mean_BER}}
        'B1_heatmap': {},        # {(qdf_idx, scale_idx): mean_BER}
        'B2_rmode': {},          # {turb: {r_mode: mean_BER}}
    }

    t0 = time.time()

    # ── B1a: Q[1,1] sweep ──────────────────────────────────
    print("=" * 60)
    print("B1a: Q[1,1] (Q_fine_df) sweep")
    print("=" * 60)
    for turb in turbs:
        results['B1_qdf_sweep'][turb] = {}
        for qdf in Q_fine_df_vals:
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b1_qdf(shared, n_pilots, qdf)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B1_qdf_sweep'][turb][str(qdf)] = mean_ber
            q_khz = np.sqrt(qdf) / 1e3
            print(f"  {turb:>8s} | Q_df={q_khz:>6.0f} kHz | BER={mean_ber:.4e}")
    print()

    # ── B1b: Q[0,0] sweep ──────────────────────────────────
    print("=" * 60)
    print("B1b: Q[0,0] (Q_phi_scale) sweep")
    print("=" * 60)
    for turb in turbs:
        results['B1_qphi_sweep'][turb] = {}
        for scale in Q_phi_scales:
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b1_qdf(shared, n_pilots, (50e3)**2, q_phi_scale=scale)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B1_qphi_sweep'][turb][str(scale)] = mean_ber
            print(f"  {turb:>8s} | scale={scale:>5.1f}x | BER={mean_ber:.4e}")
    print()

    # ── B1c: Q heatmap (moderate turbulence) ───────────────
    print("=" * 60)
    print("B1c: Q heatmap (moderate turbulence)")
    print("=" * 60)
    turb_hm = 'moderate'
    heatmap = np.zeros((len(Q_fine_df_vals), len(Q_phi_scales)))
    for i, qdf in enumerate(Q_fine_df_vals):
        for j, scale in enumerate(Q_phi_scales):
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb_hm, f_dot, seed)
                ber = trial_b1_qdf(shared, n_pilots, qdf, q_phi_scale=scale)
                bers.append(ber)
            heatmap[i, j] = np.mean(bers)
            results['B1_heatmap'][f"{i},{j}"] = {
                'qdf': qdf, 'scale': scale, 'ber': heatmap[i, j]
            }
            q_khz = np.sqrt(qdf) / 1e3
            print(f"  Q_df={q_khz:>6.0f}kHz scale={scale:>5.1f}x | BER={heatmap[i,j]:.4e}")
    print()

    # ── B2: R matrix comparison ────────────────────────────
    print("=" * 60)
    print("B2: R matrix mode comparison")
    print("=" * 60)
    for turb in turbs:
        results['B2_rmode'][turb] = {}
        for rm in r_modes:
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b2_rmode(shared, n_pilots, rm)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B2_rmode'][turb][rm] = mean_ber
            print(f"  {turb:>8s} | {r_labels[rm]:>16s} | BER={mean_ber:.4e}")
    print()

    elapsed = time.time() - t0
    print(f"Total time: {elapsed:.1f}s")

    # ── Save JSON ──────────────────────────────────────────
    json_path = os.path.join(OUT, 'results_kf_stress_B1B2.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plotting: 2x2 figure
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    turb_colors = {'weak': 'blue', 'moderate': 'green', 'strong': 'red'}
    turb_markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}

    # Panel (0,0): Q[1,1] sweep
    ax = axes[0, 0]
    for turb in turbs:
        q_khz_vals = [np.sqrt(float(q)) / 1e3 for q in Q_fine_df_vals]
        ber_vals = [results['B1_qdf_sweep'][turb][str(q)] for q in Q_fine_df_vals]
        ax.semilogy(q_khz_vals, ber_vals, marker=turb_markers[turb],
                    color=turb_colors[turb], label=turb, linewidth=1.5)
    ax.axvline(x=50, color='gray', linestyle='--', alpha=0.7, label='design (50kHz)')
    ax.set_xlabel('Q[1,1] root (kHz)')
    ax.set_ylabel('BER')
    ax.set_title('B1a: BER vs Q[1,1] (Q_fine_df)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel (0,1): Q[0,0] sweep
    ax = axes[0, 1]
    for turb in turbs:
        ber_vals = [results['B1_qphi_sweep'][turb][str(s)] for s in Q_phi_scales]
        ax.semilogy(Q_phi_scales, ber_vals, marker=turb_markers[turb],
                    color=turb_colors[turb], label=turb, linewidth=1.5)
    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.7, label='design (1.0x)')
    ax.set_xscale('log')
    ax.set_xlabel('Q[0,0] scale factor')
    ax.set_ylabel('BER')
    ax.set_title('B1b: BER vs Q[0,0] scale')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel (1,0): Q heatmap (moderate)
    ax = axes[1, 0]
    q_khz_labels = [f'{np.sqrt(q)/1e3:.0f}' for q in Q_fine_df_vals]
    scale_labels = [f'{s:.1f}' for s in Q_phi_scales]
    log_heat = np.log10(heatmap + 1e-10)
    im = ax.imshow(log_heat, aspect='auto', origin='lower',
                   extent=[-0.5, len(scale_labels)-0.5,
                           -0.5, len(q_khz_labels)-0.5])
    ax.set_xticks(range(len(scale_labels)))
    ax.set_xticklabels(scale_labels)
    ax.set_yticks(range(len(q_khz_labels)))
    ax.set_yticklabels(q_khz_labels)
    # Mark design point (50kHz=index 2, 1.0x=index 2)
    design_i, design_j = 2, 2
    ax.plot(design_j, design_i, 'w*', markersize=15, markeredgecolor='black',
            markeredgewidth=1.5)
    ax.set_xlabel('Q[0,0] scale')
    ax.set_ylabel('Q[1,1] (kHz)')
    ax.set_title('B1c: log10(BER) heatmap (moderate turb)')
    plt.colorbar(im, ax=ax, label='log10(BER)')
    # Annotate BER values
    for i in range(len(q_khz_labels)):
        for j in range(len(scale_labels)):
            ax.text(j, i, f'{heatmap[i,j]:.2e}', ha='center', va='center',
                    fontsize=6, color='white' if log_heat[i,j] < np.median(log_heat) else 'black')

    # Panel (1,1): R mode comparison
    ax = axes[1, 1]
    x_pos = np.arange(len(r_modes))
    bar_width = 0.25
    for idx, turb in enumerate(turbs):
        ber_vals = [results['B2_rmode'][turb][rm] for rm in r_modes]
        ax.bar(x_pos + idx * bar_width, ber_vals, bar_width,
               color=turb_colors[turb], label=turb, alpha=0.8)
    ax.set_xticks(x_pos + bar_width)
    ax.set_xticklabels([r_labels[rm] for rm in r_modes], fontsize=9)
    ax.set_ylabel('BER')
    ax.set_title('B2: R matrix mode comparison')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')

    fig.suptitle('KF Stress Test B1+B2: Q Sensitivity & R Alternatives', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig_path = os.path.join(OUT, 'fig_kf_stress_B1B2.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to {fig_path}")
    plt.close(fig)

    # ═══════════════════════════════════════════════════════════
    # Summary tables & PASS/FAIL
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("SUMMARY: B1a Q[1,1] Sensitivity")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for qdf in Q_fine_df_vals:
        header += f" | {np.sqrt(qdf)/1e3:>6.0f}kHz"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        baseline_ber = results['B1_qdf_sweep'][turb][str((50e3)**2)]
        for qdf in Q_fine_df_vals:
            ber = results['B1_qdf_sweep'][turb][str(qdf)]
            ratio = ber / baseline_ber if baseline_ber > 0 else 0
            row += f" | {ratio:>6.2f}x"
        print(row)
    print("(ratio relative to design point 50kHz)")

    print("\n" + "=" * 70)
    print("SUMMARY: B1b Q[0,0] Sensitivity")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for s in Q_phi_scales:
        header += f" | {s:>5.1f}x"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        baseline_ber = results['B1_qphi_sweep'][turb][str(1.0)]
        for s in Q_phi_scales:
            ber = results['B1_qphi_sweep'][turb][str(s)]
            ratio = ber / baseline_ber if baseline_ber > 0 else 0
            row += f" | {ratio:>5.2f}x"
        print(row)
    print("(ratio relative to design point 1.0x)")

    print("\n" + "=" * 70)
    print("SUMMARY: B1c Heatmap — Design Point Location Check")
    print("=" * 70)
    design_ber = heatmap[2, 2]  # (50kHz, 1.0x)
    min_ber = heatmap.min()
    min_idx = np.unravel_index(heatmap.argmin(), heatmap.shape)
    max_ber_nearby = max(heatmap[max(0,2-1):2+2, max(0,2-1):2+2].flat)
    variation_1hop = max_ber_nearby / design_ber if design_ber > 0 else float('inf')
    print(f"  Design point BER: {design_ber:.4e}")
    print(f"  Best BER: {min_ber:.4e} at Q_df={np.sqrt(Q_fine_df_vals[min_idx[0]])/1e3:.0f}kHz, scale={Q_phi_scales[min_idx[1]]:.1f}x")
    print(f"  1-hop max variation ratio: {variation_1hop:.2f}x")
    if variation_1hop < 1.5:
        print("  => Design point in PLATEAU region (robust)")
    elif variation_1hop < 3.0:
        print("  => Design point near EDGE of plateau (moderate sensitivity)")
    else:
        print("  => Design point on CLIFF (fragile)")

    print("\n" + "=" * 70)
    print("SUMMARY: B2 R Matrix — PASS/FAIL")
    print("=" * 70)
    all_pass = True
    for turb in turbs:
        ber_pilot = results['B2_rmode'][turb]['pilot']
        ber_awgn = results['B2_rmode'][turb]['awgn']
        improvement = ber_awgn / ber_pilot if ber_pilot > 0 else 0
        status = "PASS" if improvement > 1.5 else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {turb:>8s}: pilot={ber_pilot:.4e}, awgn={ber_awgn:.4e}, "
              f"ratio={improvement:.2f}x => {status}")
    print(f"\n  Overall B2: {'ALL PASS' if all_pass else 'FAIL'} "
          f"(R1(pilot) significantly better than R3(AWGN))")

    # B1 overall verdict
    print("\n" + "=" * 70)
    print("OVERALL VERDICT")
    print("=" * 70)
    b1a_pass = True
    for turb in turbs:
        baseline = results['B1_qdf_sweep'][turb][str((50e3)**2)]
        for qdf in Q_fine_df_vals:
            ratio = results['B1_qdf_sweep'][turb][str(qdf)] / baseline if baseline > 0 else 0
            if ratio > 3.0:
                b1a_pass = False
                break
    print(f"  B1 Q[1,1] sweep: {'PASS' if b1a_pass else 'FAIL'} (no 3x+ jump from design)")
    print(f"  B1 Q[0,0] sweep: {'PASS' if variation_1hop < 3.0 else 'FAIL'} (heatmap plateau check)")
    print(f"  B2 R comparison: {'PASS' if all_pass else 'FAIL'} (pilot > awgn)")


if __name__ == '__main__':
    main()
