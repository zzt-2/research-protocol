#!/usr/bin/env python3
"""KF Stress Test C1+C2+C3: Physical scenario robustness

C1: Doppler rate sweep (f_dot)
C2: Laser linewidth sweep (lw)
C3: Residual frequency offset sweep (f_res)
"""

from sim_kf_stress_common import *

# ═══════════════════════════════════════════════════════════════
# Custom signal generation (for C2/C3 with modified lw/f_res)
# ═══════════════════════════════════════════════════════════════
def generate_custom(Ns, gamma_bar, turb_name, f_dot, seed,
                    lw=LASER_LW, f_res=F_RESIDUAL):
    """Generate a single realization with custom lw and f_res."""
    np.random.seed(seed)
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    n_blocks = Ns // BLOCK
    h_blocks = np.array([h[i * BLOCK] for i in range(n_blocks)])
    h_med = np.median(h_blocks)
    # Custom phase with modified lw and f_res
    k = np.arange(Ns)
    phi_fo = 2 * np.pi * f_res * k * T_S
    phi_dot = np.pi * f_dot * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(Ns))
    phi = phi_fo + phi_dot + phi_laser
    carrier = np.exp(1j * phi)
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx_raw = signal + noise
    return {'rx_raw': rx_raw, 'bits': bits, 'tx': tx, 'h': h,
            'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
            'Ns': Ns, 'gamma_bar': gamma_bar,
            'turb_name': turb_name, 'f_dot': f_dot}


# ═══════════════════════════════════════════════════════════════
# KF pilot recovery with custom Q (for C2 linewidth sweep)
# ═══════════════════════════════════════════════════════════════
def kf_pilot_custom_Q(rx, gamma_bar, turb_name, n_pilots, h_med,
                      f_dot=DOPPLER_HIGH, block_size=BLOCK,
                      alpha_ema=0.5, Q_fine_df=(50e3)**2,
                      custom_sigma2_laser=None):
    """KF pilot recovery with custom sigma2_laser in Q[0,0]."""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2
    # Override Q[0,0] with custom laser linewidth
    if custom_sigma2_laser is not None:
        sigma2_turb = Q_TURB_PARAMS[turb_name]['sigma2_turb']
        Q_fine[0, 0] = custom_sigma2_laser + sigma2_turb

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

        # Phase 2: estimate h
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
# Trial runners
# ═══════════════════════════════════════════════════════════════
def trial_c1_fdot(Ns, gamma_bar, turb_name, f_dot, seed, n_pilots=5):
    """C1 trial: fixed f_dot, use generate_shared_realization."""
    shared = generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)
    # Fixed baseline
    rx_fixed = run_fixed(shared)
    ber_fixed = resolve_qpsk(rx_fixed, shared['bits'])
    # KF pilot
    corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots)
    ber_kf = resolve_qpsk(corrected[data_idx], data_bits)
    return ber_fixed, ber_kf


def trial_c2_lw(Ns, gamma_bar, turb_name, f_dot, seed, lw, n_pilots=5):
    """C2 trial: custom linewidth for both signal generation and KF Q."""
    shared = generate_custom(Ns, gamma_bar, turb_name, f_dot, seed, lw=lw)
    # Fixed baseline
    rx_fixed = run_fixed(shared)
    ber_fixed = resolve_qpsk(rx_fixed, shared['bits'])
    # KF pilot with custom Q
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    sigma2_laser_custom = 2 * np.pi * lw * T_S
    corrected, _ = kf_pilot_custom_Q(
        rx_eq, gamma_bar, turb_name, n_pilots, shared['h_med'],
        f_dot, custom_sigma2_laser=sigma2_laser_custom)
    ber_kf = resolve_qpsk(corrected[data_idx], data_bits)
    return ber_fixed, ber_kf


def trial_c3_fres(Ns, gamma_bar, turb_name, f_dot, seed, f_res, n_pilots=5):
    """C3 trial: custom residual frequency offset."""
    shared = generate_custom(Ns, gamma_bar, turb_name, f_dot, seed, f_res=f_res)
    # Fixed baseline
    rx_fixed = run_fixed(shared)
    ber_fixed = resolve_qpsk(rx_fixed, shared['bits'])
    # KF pilot (Q unchanged — f_res doesn't affect Q)
    corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots)
    ber_kf = resolve_qpsk(corrected[data_idx], data_bits)
    return ber_fixed, ber_kf


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

    # C1: Doppler rate sweep
    f_dot_vals = [0, 10e6, 30e6, 50e6, 100e6, 150e6, 300e6]
    f_dot_labels = ['0', '10M', '30M', '50M', '100M', '150M', '300M']

    # C2: Laser linewidth sweep
    lw_vals = [0.1e3, 1e3, 10e3, 100e3, 1000e3]

    # C3: Residual frequency offset sweep
    f_res_vals = [0, 100e3, 500e3, 1e6, 5e6, 10e6]

    results = {
        'params': {
            'Ns': Ns, 'gamma_bar': gamma_bar, 'n_pilots': n_pilots,
            'n_seeds': n_seeds, 'turbs': turbs,
            'f_dot_vals': f_dot_vals,
            'lw_vals': lw_vals,
            'f_res_vals': f_res_vals,
        },
        'C1_fdot': {},     # {turb: {f_dot: {'fixed': ber, 'kf': ber, 'gain_db': db}}}
        'C2_lw': {},       # {turb: {lw: {'fixed': ber, 'kf': ber, 'gain_db': db}}}
        'C3_fres': {},     # {turb: {f_res: {'fixed': ber, 'kf': ber, 'gain_db': db}}}
    }

    t0 = time.time()

    # ── C1: Doppler rate sweep ───────────────────────────────
    print("=" * 70)
    print("C1: Doppler rate sweep (f_dot)")
    print("=" * 70)
    f_dot_default = DOPPLER_HIGH  # 150 MHz
    for turb in turbs:
        results['C1_fdot'][turb] = {}
        for fd in f_dot_vals:
            bers_fixed, bers_kf = [], []
            for seed in seeds:
                bf, bk = trial_c1_fdot(Ns, gamma_bar, turb, fd, seed, n_pilots)
                bers_fixed.append(bf)
                bers_kf.append(bk)
            mean_f = np.mean(bers_fixed)
            mean_k = np.mean(bers_kf)
            gain = db_ratio(mean_f, mean_k)
            results['C1_fdot'][turb][str(fd)] = {
                'fixed': mean_f, 'kf': mean_k, 'gain_db': gain
            }
            print(f"  {turb:>8s} | f_dot={fd/1e6:>6.0f} MHz | "
                  f"Fixed={mean_f:.4e} KF={mean_k:.4e} Gain={gain:>6.1f} dB")
    print()

    # ── C2: Laser linewidth sweep ────────────────────────────
    print("=" * 70)
    print("C2: Laser linewidth sweep")
    print("=" * 70)
    f_dot_c2 = DOPPLER_HIGH
    for turb in turbs:
        results['C2_lw'][turb] = {}
        for lw in lw_vals:
            bers_fixed, bers_kf = [], []
            for seed in seeds:
                bf, bk = trial_c2_lw(Ns, gamma_bar, turb, f_dot_c2, seed, lw, n_pilots)
                bers_fixed.append(bf)
                bers_kf.append(bk)
            mean_f = np.mean(bers_fixed)
            mean_k = np.mean(bers_kf)
            gain = db_ratio(mean_f, mean_k)
            results['C2_lw'][turb][str(lw)] = {
                'fixed': mean_f, 'kf': mean_k, 'gain_db': gain
            }
            print(f"  {turb:>8s} | lw={lw/1e3:>7.1f} kHz | "
                  f"Fixed={mean_f:.4e} KF={mean_k:.4e} Gain={gain:>6.1f} dB")
    print()

    # ── C3: Residual frequency offset sweep ──────────────────
    print("=" * 70)
    print("C3: Residual frequency offset sweep (f_res)")
    print("=" * 70)
    f_dot_c3 = DOPPLER_HIGH
    for turb in turbs:
        results['C3_fres'][turb] = {}
        for fr in f_res_vals:
            bers_fixed, bers_kf = [], []
            for seed in seeds:
                bf, bk = trial_c3_fres(Ns, gamma_bar, turb, f_dot_c3, seed, fr, n_pilots)
                bers_fixed.append(bf)
                bers_kf.append(bk)
            mean_f = np.mean(bers_fixed)
            mean_k = np.mean(bers_kf)
            gain = db_ratio(mean_f, mean_k)
            results['C3_fres'][turb][str(fr)] = {
                'fixed': mean_f, 'kf': mean_k, 'gain_db': gain
            }
            print(f"  {turb:>8s} | f_res={fr/1e6:>5.1f} MHz | "
                  f"Fixed={mean_f:.4e} KF={mean_k:.4e} Gain={gain:>6.1f} dB")
    print()

    elapsed = time.time() - t0
    print(f"Total time: {elapsed:.1f}s")

    # ── Save JSON ─────────────────────────────────────────────
    json_path = os.path.join(OUT, 'results_kf_stress_C1C2C3.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plotting: 1x3 figure
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    turb_colors = {'weak': 'blue', 'moderate': 'green', 'strong': 'red'}
    turb_markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}

    # Panel 0: C1 — BER vs f_dot
    ax = axes[0]
    for turb in turbs:
        fd_arr = np.array(f_dot_vals) / 1e6
        ber_fixed = [results['C1_fdot'][turb][str(fd)]['fixed'] for fd in f_dot_vals]
        ber_kf = [results['C1_fdot'][turb][str(fd)]['kf'] for fd in f_dot_vals]
        ax.semilogy(fd_arr, ber_fixed, '--', marker=turb_markers[turb],
                    color=turb_colors[turb], alpha=0.5, linewidth=1.2,
                    label=f'{turb} Fixed')
        ax.semilogy(fd_arr, ber_kf, '-', marker=turb_markers[turb],
                    color=turb_colors[turb], linewidth=1.5,
                    label=f'{turb} KF')
    ax.set_xlabel('Doppler rate (MHz/s)')
    ax.set_ylabel('BER')
    ax.set_title('C1: BER vs Doppler Rate')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 1: C2 — BER vs linewidth
    ax = axes[1]
    for turb in turbs:
        lw_arr = np.array(lw_vals) / 1e3
        ber_fixed = [results['C2_lw'][turb][str(lw)]['fixed'] for lw in lw_vals]
        ber_kf = [results['C2_lw'][turb][str(lw)]['kf'] for lw in lw_vals]
        ax.semilogy(lw_arr, ber_fixed, '--', marker=turb_markers[turb],
                    color=turb_colors[turb], alpha=0.5, linewidth=1.2,
                    label=f'{turb} Fixed')
        ax.semilogy(lw_arr, ber_kf, '-', marker=turb_markers[turb],
                    color=turb_colors[turb], linewidth=1.5,
                    label=f'{turb} KF')
    ax.set_xscale('log')
    ax.set_xlabel('Laser linewidth (kHz)')
    ax.set_ylabel('BER')
    ax.set_title('C2: BER vs Laser Linewidth')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 2: C3 — BER vs f_res
    ax = axes[2]
    for turb in turbs:
        fr_arr = np.array(f_res_vals) / 1e6
        ber_fixed = [results['C3_fres'][turb][str(fr)]['fixed'] for fr in f_res_vals]
        ber_kf = [results['C3_fres'][turb][str(fr)]['kf'] for fr in f_res_vals]
        ax.semilogy(fr_arr, ber_fixed, '--', marker=turb_markers[turb],
                    color=turb_colors[turb], alpha=0.5, linewidth=1.2,
                    label=f'{turb} Fixed')
        ax.semilogy(fr_arr, ber_kf, '-', marker=turb_markers[turb],
                    color=turb_colors[turb], linewidth=1.5,
                    label=f'{turb} KF')
    ax.set_xlabel('Residual freq offset (MHz)')
    ax.set_ylabel('BER')
    ax.set_title('C3: BER vs Residual Freq Offset')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    fig.suptitle('KF Stress Test C1+C2+C3: Physical Scenario Robustness', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    fig_path = os.path.join(OUT, 'fig_kf_stress_C1C2C3.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to {fig_path}")
    plt.close(fig)

    # ═══════════════════════════════════════════════════════════
    # Summary tables & PASS/FAIL
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("SUMMARY TABLE: C1 Doppler Rate (gain in dB)")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for lb in f_dot_labels:
        header += f" | {lb:>6s}"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        for fd in f_dot_vals:
            gain = results['C1_fdot'][turb][str(fd)]['gain_db']
            row += f" | {gain:>6.1f}"
        print(row)
    print("(positive = KF better, negative = KF worse)")

    print("\n" + "=" * 70)
    print("SUMMARY TABLE: C2 Laser Linewidth (gain in dB)")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for lw in lw_vals:
        header += f" | {lw/1e3:>7.1f}k"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        for lw in lw_vals:
            gain = results['C2_lw'][turb][str(lw)]['gain_db']
            row += f" | {gain:>6.1f}"
        print(row)

    print("\n" + "=" * 70)
    print("SUMMARY TABLE: C3 Residual Freq Offset (gain in dB)")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for fr in f_res_vals:
        header += f" | {fr/1e6:>5.1f}M"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        for fr in f_res_vals:
            gain = results['C3_fres'][turb][str(fr)]['gain_db']
            row += f" | {gain:>6.1f}"
        print(row)

    # ── PASS/FAIL ─────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PASS/FAIL CRITERIA")
    print("=" * 70)

    # C1: f_dot=150e6 gain > 5 dB
    print("\nC1: f_dot=150MHz => gain > 5 dB?")
    c1_pass = True
    for turb in turbs:
        gain = results['C1_fdot'][turb][str(150e6)]['gain_db']
        status = "PASS" if gain > 5 else "FAIL"
        if status == "FAIL":
            c1_pass = False
        print(f"  {turb:>8s}: gain={gain:.1f} dB => {status}")
    print(f"  C1 Overall: {'PASS' if c1_pass else 'FAIL'}")

    # C2: delta_nu <= 100kHz gain > 5 dB
    print("\nC2: linewidth <= 100kHz => gain > 5 dB?")
    c2_pass = True
    for turb in turbs:
        for lw in lw_vals:
            if lw <= 100e3:
                gain = results['C2_lw'][turb][str(lw)]['gain_db']
                status = "PASS" if gain > 5 else "FAIL"
                if status == "FAIL":
                    c2_pass = False
                print(f"  {turb:>8s} lw={lw/1e3:.1f}kHz: gain={gain:.1f} dB => {status}")
    print(f"  C2 Overall: {'PASS' if c2_pass else 'FAIL'}")

    # C3: f_res <= 5MHz gain stable
    print("\nC3: f_res <= 5MHz => gain stable?")
    c3_pass = True
    for turb in turbs:
        gains = [results['C3_fres'][turb][str(fr)]['gain_db']
                 for fr in f_res_vals if fr <= 5e6]
        if gains:
            max_g, min_g = max(gains), min(gains)
            variation = max_g - min_g
            status = "PASS" if variation < 3.0 else "FAIL"
            if status == "FAIL":
                c3_pass = False
            print(f"  {turb:>8s}: range [{min_g:.1f}, {max_g:.1f}] dB, "
                  f"variation={variation:.1f} dB => {status}")
    print(f"  C3 Overall: {'PASS' if c3_pass else 'FAIL'} (variation < 3 dB)")

    print("\n" + "=" * 70)
    print(f"OVERALL: {'ALL PASS' if (c1_pass and c2_pass and c3_pass) else 'FAIL'}")
    print("=" * 70)


if __name__ == '__main__':
    main()
