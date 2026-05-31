#!/usr/bin/env python3
"""KF Stress Test B3+B4+B5: P init sensitivity, pilot density, pilot placement

B3: P[0,0] and P[1,1] initialization sensitivity
B4: Pilot overhead sweep (1%~30%) with net BER analysis
B5: Pilot placement strategy (front / uniform / center)
"""

from sim_kf_stress_common import *
import itertools

# ═══════════════════════════════════════════════════════════════
# B3: kf_pilot with custom P_init
# ═══════════════════════════════════════════════════════════════
def kf_pilot_b3(rx, gamma_bar, turb_name, n_pilots, h_med,
                f_dot=DOPPLER_HIGH, block_size=BLOCK,
                alpha_ema=0.5, Q_fine_df=(50e3)**2,
                p_init_p00=(np.pi/4)**2, p_init_p11=(2*np.pi*100e3)**2):
    """kf_pilot_recovery with custom P initialization."""
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
    P = np.diag([p_init_p00, p_init_p11])

    h_est = max(h_med, 0.01)
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        pilot_end = start + n_pilots

        # Phase 1: pilots
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

        # Phase 2: h estimation
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        # Phase 3: data (decision-directed)
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
# B4/B5: insert_pilots with placement mode
# ═══════════════════════════════════════════════════════════════
def insert_pilots_placement(shared, n_pilots_per_block=5, mode='front'):
    """Insert pilots with configurable placement mode.

    mode:
        'front'   -> first n_pilots positions per block (original)
        'uniform' -> evenly spaced within each block
        'center'  -> center n_pilots positions per block
    """
    rx_raw = shared['rx_raw']
    tx = shared['tx'].copy()
    bits = shared['bits']
    h = shared['h']
    phi = shared['phi']
    gamma_bar = shared['gamma_bar']
    Ns = shared['Ns']
    n_blocks = Ns // BLOCK

    known_pilots = get_pilots(n_pilots_per_block)
    pilot_indices = []
    data_indices = []

    for b in range(n_blocks):
        base = b * BLOCK
        if mode == 'front':
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + p)
        elif mode == 'uniform':
            step = BLOCK / (n_pilots_per_block + 1)
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + int(step * (p + 1)))
        elif mode == 'center':
            center = BLOCK // 2
            start_offset = center - n_pilots_per_block // 2
            for p in range(n_pilots_per_block):
                pilot_indices.append(base + start_offset + p)

        pilot_set = set(pilot_indices[len(pilot_indices) - n_pilots_per_block:])
        for d in range(BLOCK):
            idx = base + d
            if idx not in pilot_set:
                data_indices.append(idx)

    pilot_indices = np.array(pilot_indices, dtype=int)
    data_indices = np.array(data_indices, dtype=int)

    for i, idx in enumerate(pilot_indices):
        tx[idx] = known_pilots[i % len(known_pilots)]

    # Rebuild rx with pilot symbols
    carrier = np.exp(1j * phi)
    noise = rx_raw - shared['tx'] * np.sqrt(h) * carrier
    signal_pilot = tx * np.sqrt(h) * carrier
    rx_pilot = signal_pilot + noise

    # Data bits
    data_bits = np.zeros(len(data_indices) * 2, dtype=int)
    for i, idx in enumerate(data_indices):
        data_bits[2*i] = bits[2*idx]
        data_bits[2*i+1] = bits[2*idx+1]

    return rx_pilot, pilot_indices, data_indices, data_bits


# ═══════════════════════════════════════════════════════════════
# B5: kf_pilot with placement-aware pilot recovery
# ═══════════════════════════════════════════════════════════════
def kf_pilot_b5(rx, gamma_bar, turb_name, n_pilots, h_med,
                pilot_indices, data_indices, n_blocks,
                f_dot=DOPPLER_HIGH, block_size=BLOCK,
                alpha_ema=0.5, Q_fine_df=(50e3)**2):
    """kf_pilot_recovery with arbitrary pilot positions."""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

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

    # Build per-block pilot list
    pilot_per_block = []
    for b in range(n_blocks):
        s, e = b * block_size, (b+1) * block_size
        block_pilots = [idx for idx in pilot_indices if s <= idx < e]
        block_pilots.sort()
        pilot_per_block.append(block_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        bp = pilot_per_block[b]

        # Collect pilot residuals for h estimation
        pilot_corrected = []

        # Run KF across the whole block
        for k_idx in range(start, end):
            is_pilot = k_idx in bp

            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine

            if is_pilot:
                p_local = bp.index(k_idx)
                s_p = known_pilots[p_local % len(known_pilots)]
                R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
                y = rx_foc[k_idx] * np.conj(s_p)
                z_obs = np.angle(y)
            else:
                R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
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

            if is_pilot:
                pilot_corrected.append(corrected[k_idx])

        # h estimation from pilots
        if len(pilot_corrected) > 0:
            pilot_res = np.array(pilot_corrected)
            s_pilots = known_pilots[:len(pilot_corrected)]
            h_est_raw = abs(np.mean(pilot_res * np.conj(s_pilots)))**2
            h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
            h_est = max(h_est, 0.01)
            h_est_prev = h_est
            h_est_per_block[b] = h_est

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
# Trial runners
# ═══════════════════════════════════════════════════════════════
def trial_b3_pinit(shared, n_pilots, p00, p11):
    """B3: single trial with custom P_init."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    corrected, _ = kf_pilot_b3(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'],
        p_init_p00=p00, p_init_p11=p11)
    return resolve_qpsk(corrected[data_idx], data_bits)


def trial_b4_density(shared, n_pilots):
    """B4: single trial with given pilot density."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    corrected, _ = kf_pilot_recovery(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'])
    return resolve_qpsk(corrected[data_idx], data_bits)


def trial_b5_placement(shared, n_pilots, mode):
    """B5: single trial with pilot placement mode."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots_placement(
        shared, n_pilots, mode=mode)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    n_blocks = shared['Ns'] // BLOCK
    corrected, _ = kf_pilot_b5(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], pilot_idx, data_idx, n_blocks,
        shared['f_dot'])
    return resolve_qpsk(corrected[data_idx], data_bits)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
def main():
    Ns = 10000
    gamma_bar = GAMMA_BAR_DEFAULT
    n_seeds = 30
    seeds = list(range(n_seeds))
    turbs = ['weak', 'moderate', 'strong']
    f_dot = DOPPLER_HIGH

    # B3 parameters
    P00_vals = [0.01, 0.1, (np.pi/4)**2, np.pi**2, 10*np.pi**2]
    P00_labels = ['0.01', '0.1', '(pi/4)^2', 'pi^2', '10pi^2']
    P11_freq_vals = [10e3, 100e3, 1e6]  # Hz
    P11_vals = [(f * T_S)**2 for f in P11_freq_vals]
    P11_labels = ['(10kHz)^2', '(100kHz)^2', '(1MHz)^2']

    # B4 parameters
    overhead_pcts = [1, 2, 5, 10, 15, 20, 30]
    n_pilots_vals = overhead_pcts  # 1p=1%, 2p=2%, ... (block=100, so n_pilots=pct)

    # B5 parameters
    placement_modes = ['front', 'uniform', 'center']
    n_pilots_b5 = 5

    results = {
        'params': {
            'Ns': Ns, 'gamma_bar': gamma_bar, 'n_seeds': n_seeds,
            'turbs': turbs,
            'P00_vals': P00_vals, 'P00_labels': P00_labels,
            'P11_vals': P11_vals, 'P11_labels': P11_labels,
            'overhead_pcts': overhead_pcts,
            'placement_modes': placement_modes,
        },
        'B3_p00_sweep': {},    # {turb: {label: mean_BER}}
        'B3_p11_sweep': {},    # {turb: {label: mean_BER}}
        'B4_density': {},      # {turb: {overhead: {ber, net_ber}}}
        'B5_placement': {},    # {turb: {mode: mean_BER}}
    }

    t0 = time.time()

    # ── B3a: P[0,0] sweep ────────────────────────────────────
    print("=" * 60)
    print("B3a: P[0,0] initialization sensitivity")
    print("=" * 60)
    default_p11 = (2 * np.pi * 100e3)**2
    for turb in turbs:
        results['B3_p00_sweep'][turb] = {}
        for p00, label in zip(P00_vals, P00_labels):
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b3_pinit(shared, 5, p00, default_p11)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B3_p00_sweep'][turb][label] = mean_ber
            print(f"  {turb:>8s} | P00={label:>10s} | BER={mean_ber:.4e}")
    print()

    # ── B3b: P[1,1] sweep ────────────────────────────────────
    print("=" * 60)
    print("B3b: P[1,1] initialization sensitivity")
    print("=" * 60)
    default_p00 = (np.pi/4)**2
    for turb in turbs:
        results['B3_p11_sweep'][turb] = {}
        for p11, label in zip(P11_vals, P11_labels):
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b3_pinit(shared, 5, default_p00, p11)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B3_p11_sweep'][turb][label] = mean_ber
            print(f"  {turb:>8s} | P11={label:>12s} | BER={mean_ber:.4e}")
    print()

    # ── B4: Pilot density sweep ──────────────────────────────
    print("=" * 60)
    print("B4: Pilot density sweep")
    print("=" * 60)
    for turb in turbs:
        results['B4_density'][turb] = {}
        for pct in overhead_pcts:
            n_p = pct  # block_size=100, so n_pilots=pct gives pct% overhead
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b4_density(shared, n_p)
                bers.append(ber)
            mean_ber = np.mean(bers)
            overhead = pct / 100.0
            net_ber = mean_ber * (1 - overhead)
            results['B4_density'][turb][str(pct)] = {
                'ber': mean_ber, 'net_ber': net_ber, 'overhead': overhead
            }
            print(f"  {turb:>8s} | {pct:>2d}% ({n_p:>2d}p) | "
                  f"BER={mean_ber:.4e} | net_BER={net_ber:.4e}")
    print()

    # ── B5: Pilot placement ──────────────────────────────────
    print("=" * 60)
    print("B5: Pilot placement strategy")
    print("=" * 60)
    for turb in turbs:
        results['B5_placement'][turb] = {}
        for mode in placement_modes:
            bers = []
            for seed in seeds:
                shared = generate_shared_realization(Ns, gamma_bar, turb, f_dot, seed)
                ber = trial_b5_placement(shared, n_pilots_b5, mode)
                bers.append(ber)
            mean_ber = np.mean(bers)
            results['B5_placement'][turb][mode] = mean_ber
            print(f"  {turb:>8s} | {mode:>8s} | BER={mean_ber:.4e}")
    print()

    elapsed = time.time() - t0
    print(f"Total time: {elapsed:.1f}s")

    # ── Save JSON ─────────────────────────────────────────────
    json_path = os.path.join(OUT, 'results_kf_stress_B3B4B5.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plotting: 1x3 figure
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    turb_colors = {'weak': 'blue', 'moderate': 'green', 'strong': 'red'}
    turb_markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}

    # Panel 0: B3 P[0,0] sweep
    ax = axes[0]
    x_pos_p00 = np.arange(len(P00_labels))
    bar_width = 0.25
    for idx, turb in enumerate(turbs):
        ber_vals = [results['B3_p00_sweep'][turb][lbl] for lbl in P00_labels]
        ax.bar(x_pos_p00 + idx * bar_width, ber_vals, bar_width,
               color=turb_colors[turb], label=turb, alpha=0.8)
    ax.set_xticks(x_pos_p00 + bar_width)
    ax.set_xticklabels(P00_labels, fontsize=8)
    ax.set_yscale('log')
    ax.set_ylabel('BER')
    ax.set_title('B3a: BER vs P[0,0] init')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')
    # Mark design point
    design_idx = P00_labels.index('(pi/4)^2')
    ax.axvline(x=design_idx + bar_width, color='gray', linestyle='--', alpha=0.5)

    # Panel 1: B4 pilot density
    ax = axes[1]
    for turb in turbs:
        ber_vals = [results['B4_density'][turb][str(p)]['ber'] for p in overhead_pcts]
        net_vals = [results['B4_density'][turb][str(p)]['net_ber'] for p in overhead_pcts]
        ax.plot(overhead_pcts, ber_vals, marker=turb_markers[turb],
                color=turb_colors[turb], label=f'{turb} BER', linewidth=1.5)
        ax.plot(overhead_pcts, net_vals, marker=turb_markers[turb],
                color=turb_colors[turb], linestyle='--',
                label=f'{turb} net BER', linewidth=1.2, alpha=0.7)
    ax.axvline(x=5, color='gray', linestyle=':', alpha=0.7, label='5% design')
    ax.set_xlabel('Pilot overhead (%)')
    ax.set_ylabel('BER / net BER')
    ax.set_yscale('log')
    ax.set_title('B4: BER vs pilot overhead')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 2: B5 placement
    ax = axes[2]
    x_pos_pl = np.arange(len(placement_modes))
    bar_width_pl = 0.25
    for idx, turb in enumerate(turbs):
        ber_vals = [results['B5_placement'][turb][m] for m in placement_modes]
        ax.bar(x_pos_pl + idx * bar_width_pl, ber_vals, bar_width_pl,
               color=turb_colors[turb], label=turb, alpha=0.8)
    ax.set_xticks(x_pos_pl + bar_width_pl)
    ax.set_xticklabels(placement_modes, fontsize=9)
    ax.set_yscale('log')
    ax.set_ylabel('BER')
    ax.set_title('B5: Pilot placement (5% overhead)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('KF Stress Test B3+B4+B5: Init, Density, Placement', fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig_path = os.path.join(OUT, 'fig_kf_stress_B3B4B5.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to {fig_path}")
    plt.close(fig)

    # ═══════════════════════════════════════════════════════════
    # Summary tables & PASS/FAIL
    # ═══════════════════════════════════════════════════════════

    # B3 summary
    print("\n" + "=" * 70)
    print("SUMMARY: B3a P[0,0] Initialization Sensitivity")
    print("=" * 70)
    design_label_p00 = '(pi/4)^2'
    for turb in turbs:
        baseline = results['B3_p00_sweep'][turb][design_label_p00]
        row = f"  {turb:>8s}:"
        for lbl in P00_labels:
            ber = results['B3_p00_sweep'][turb][lbl]
            ratio = ber / baseline if baseline > 0 else 0
            row += f"  {lbl}={ratio:.2f}x"
        print(row)
    print(f"  (ratio relative to design point {design_label_p00})")

    print("\n" + "=" * 70)
    print("SUMMARY: B3b P[1,1] Initialization Sensitivity")
    print("=" * 70)
    design_label_p11 = '(100kHz)^2'
    for turb in turbs:
        baseline = results['B3_p11_sweep'][turb][design_label_p11]
        row = f"  {turb:>8s}:"
        for lbl in P11_labels:
            ber = results['B3_p11_sweep'][turb][lbl]
            ratio = ber / baseline if baseline > 0 else 0
            row += f"  {lbl}={ratio:.2f}x"
        print(row)
    print(f"  (ratio relative to design point {design_label_p11})")

    # B3 PASS/FAIL
    b3_pass = True
    print("\n" + "=" * 70)
    print("B3 PASS/FAIL: P_init sensitivity")
    print("=" * 70)
    for turb in turbs:
        # P[0,0] check: max ratio < 3x
        baseline_p00 = results['B3_p00_sweep'][turb][design_label_p00]
        max_ratio_p00 = max(
            results['B3_p00_sweep'][turb][lbl] / baseline_p00
            for lbl in P00_labels if baseline_p00 > 0
        )
        # P[1,1] check
        baseline_p11 = results['B3_p11_sweep'][turb][design_label_p11]
        max_ratio_p11 = max(
            results['B3_p11_sweep'][turb][lbl] / baseline_p11
            for lbl in P11_labels if baseline_p11 > 0
        )
        p00_ok = max_ratio_p00 < 3.0
        p11_ok = max_ratio_p11 < 3.0
        if not (p00_ok and p11_ok):
            b3_pass = False
        print(f"  {turb:>8s}: P00 ratio={max_ratio_p00:.2f}x {'PASS' if p00_ok else 'FAIL'}, "
              f"P11 ratio={max_ratio_p11:.2f}x {'PASS' if p11_ok else 'FAIL'}")
    print(f"  B3 overall: {'PASS' if b3_pass else 'FAIL'} (steady-state BER insensitive to P_init)")

    # B4 summary
    print("\n" + "=" * 70)
    print("SUMMARY: B4 Pilot Density (net BER)")
    print("=" * 70)
    b4_pass = True
    for turb in turbs:
        net_bers = {p: results['B4_density'][turb][str(p)]['net_ber']
                    for p in overhead_pcts}
        best_pct = min(net_bers, key=net_bers.get)
        net_5 = net_bers[5]
        net_best = net_bers[best_pct]
        ratio = net_5 / net_best if net_best > 0 else float('inf')
        is_pass = ratio < 1.5  # 5% within 1.5x of optimal
        if not is_pass:
            b4_pass = False
        row = f"  {turb:>8s}:"
        for p in overhead_pcts:
            marker = " <--" if p == best_pct else ""
            row += f"  {p}%={net_bers[p]:.4e}{marker}"
        print(row)
        print(f"           Best={best_pct}%, 5% ratio={ratio:.2f}x => {'PASS' if is_pass else 'FAIL'}")
    print(f"  B4 overall: {'PASS' if b4_pass else 'FAIL'} (5% near-optimal in net BER)")

    # B5 summary
    print("\n" + "=" * 70)
    print("SUMMARY: B5 Pilot Placement")
    print("=" * 70)
    b5_pass = True
    for turb in turbs:
        bers_pl = {m: results['B5_placement'][turb][m] for m in placement_modes}
        best_mode = min(bers_pl, key=bers_pl.get)
        front_ber = bers_pl['front']
        best_ber = bers_pl[best_mode]
        ratio = front_ber / best_ber if best_ber > 0 else float('inf')
        is_ok = ratio < 2.0  # front within 2x of best
        if not is_ok:
            b5_pass = False
        row = f"  {turb:>8s}:"
        for m in placement_modes:
            marker = " <--best" if m == best_mode else ""
            row += f"  {m}={bers_pl[m]:.4e}{marker}"
        print(row)
        print(f"           front/best={ratio:.2f}x => {'PASS' if is_ok else 'FAIL'}")
    print(f"  B5 overall: {'PASS' if b5_pass else 'FAIL'} (front placement competitive)")

    # Overall verdict
    print("\n" + "=" * 70)
    print("OVERALL VERDICT")
    print("=" * 70)
    print(f"  B3 P_init sensitivity: {'PASS' if b3_pass else 'FAIL'}")
    print(f"  B4 Pilot density:      {'PASS' if b4_pass else 'FAIL'}")
    print(f"  B5 Pilot placement:    {'PASS' if b5_pass else 'FAIL'}")


if __name__ == '__main__':
    main()
