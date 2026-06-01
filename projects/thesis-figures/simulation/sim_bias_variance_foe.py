#!/usr/bin/env python3
"""Bias-Variance FOE Window Simulation

Compares three FOE window strategies:
1. Fixed N=1024 (Zhao 2025 baseline)
2. Old adaptive: N = 80/(gamma_bar*h^2) (noise-only, broken)
3. New adaptive: N = (alpha/h)^{1/5} (bias-variance balanced)

VV and DPLL formulas are unchanged from sim_direction_a.py.
Runs 6 scenarios x 30 trials x 10000 symbols.
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# ═══════════════════════════════════════════════════════════════
# System parameters (from S007 parameter traceability)
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9
T_S = 1 / R_SYM
F_CARRIER = 1.55e14
LASER_LW = 10e3

TURB = {
    'weak':     (4.0, 3.0),
    'moderate': (2.5, 1.8),
    'strong':   (1.5, 0.8),
}
BLOCK = 100

DOPPLER_HIGH = 150e6
DOPPLER_LOW  = 30e6
F_RESIDUAL   = 1e6

FIXED_CFG = {
    'N_fft': 1024,
    'M_vv': 64,
    'omega_n': 8e6,
    'zeta': np.sqrt(2)/2,
}

# ═══════════════════════════════════════════════════════════════
# Basic primitives (same as sim_direction_a.py)
# ═══════════════════════════════════════════════════════════════
def gg_block(N, a, b, bs=BLOCK):
    nb = (N + bs - 1) // bs
    return np.repeat(
        gamma_dist.rvs(a, scale=1/a, size=nb) *
        gamma_dist.rvs(b, scale=1/b, size=nb),
        bs)[:N]

def qpsk_mod(bits):
    return ((2*bits[0::2]-1) + 1j*(2*bits[1::2]-1)) / np.sqrt(2)

def qpsk_demod(s):
    b = np.zeros(2*len(s), dtype=int)
    b[0::2] = (np.real(s) > 0).astype(int)
    b[1::2] = (np.imag(s) > 0).astype(int)
    return b

def awgn(sig, snr_db):
    s2 = 0.5 / 10**(snr_db/10)
    return sig + np.sqrt(s2)*(np.random.randn(len(sig)) + 1j*np.random.randn(len(sig)))

def ber(tx_bits, rx):
    return np.mean(tx_bits != qpsk_demod(rx))

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber(tx_bits, rx * np.exp(-1j*r))
        if b < best: best = b
    return best

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

# ═══════════════════════════════════════════════════════════════
# Doppler time-varying model
# ═══════════════════════════════════════════════════════════════
def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    k = np.arange(N)
    phi_fo = 2 * np.pi * f_res * k * T_S
    phi_dot = np.pi * f_dot * (k * T_S)**2
    phi_laser = np.sqrt(2 * np.pi * lw * T_S) * np.cumsum(np.random.randn(N))
    return phi_fo + phi_dot + phi_laser

# ═══════════════════════════════════════════════════════════════
# FFT-based FOE (4th-power method)
# ═══════════════════════════════════════════════════════════════
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
        alpha = np.abs(R4[idx-1])
        beta = np.abs(R4[idx])
        gamma_val = np.abs(R4[idx+1])
        if beta - alpha > 0 and beta + alpha - 2*gamma_val != 0:
            p = 0.5 * (alpha - gamma_val) / (alpha - 2*beta + gamma_val)
            f_est_norm = (freqs[idx] + p * (freqs[1] - freqs[0]))
        else:
            f_est_norm = freqs[idx]
    else:
        f_est_norm = freqs[idx]
    f_est_norm /= 4
    return 2 * np.pi * f_est_norm

# ═══════════════════════════════════════════════════════════════
# Second-order DPLL
# ═══════════════════════════════════════════════════════════════
def dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2):
    wT = omega_n * T_S
    wT = min(wT, 0.5)
    c1 = 2 * zeta * wT
    c2 = wT**2
    N = len(rx)
    phi_est = np.zeros(N)
    freq_est = np.zeros(N)
    integrator = 0.0
    vco_phase = 0.0
    for k in range(N):
        vco_out = np.exp(-1j * vco_phase)
        mixed = rx[k] * vco_out
        m4 = mixed**4
        pd_out = np.angle(m4) / 4
        integrator += c2 * pd_out
        freq_est[k] = c1 * pd_out + integrator
        vco_phase += freq_est[k]
        phi_est[k] = vco_phase
    return rx * np.exp(-1j * phi_est), phi_est

# ═══════════════════════════════════════════════════════════════
# VV carrier phase recovery
# ═══════════════════════════════════════════════════════════════
def vv_cpr(rx, Nw=64):
    M = 4
    raised = rx**M
    amp = np.abs(raised)
    clip_val = 1e8
    mask = amp > clip_val
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * clip_val
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg)) / M
    return rx * np.exp(-1j * pe), pe

# ═══════════════════════════════════════════════════════════════
# Adaptive parameter calculation — THREE FOE strategies
# ═══════════════════════════════════════════════════════════════

# Pre-compute alpha constant for bias-variance formula
_ALPHA_BV = 27 / (np.pi**4 * (DOPPLER_HIGH * T_S**2)**2 * 100)  # gamma_bar=100

def adaptive_params_old(h_est, gamma_bar_db=20):
    """Old noise-only FOE formula: N = 80/(gamma_bar * h^2).
    VV and DPLL kept at fixed baseline values."""
    gamma_bar = 10**(gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)
    gamma = gamma_bar * h_safe
    N_fft = int(np.clip(80 * gamma_bar / (gamma**2 + 1e-10), 256, 8192))
    N_fft = int(2**np.ceil(np.log2(N_fft)))
    return N_fft

def adaptive_params_bv(h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH):
    """New bias-variance FOE formula: N = (alpha/h)^{1/5}.

    Derivation: minimize MSE = bias^2 + variance where
      bias^2 = (pi*f_dot*Ts^2)^2 * N^2 / 3
      variance = 6 / (pi^2 * N^3 * gamma)
    Optimal: N^5 = 27 / (pi^4 * (f_dot*Ts^2)^2 * gamma_bar * h)

    VV and DPLL kept at fixed baseline values (isolate FOE effect).
    """
    gamma_bar = 10**(gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)

    alpha = 27 / (np.pi**4 * (f_dot * T_S**2)**2 * gamma_bar)
    N_opt = (alpha / h_safe)**(1/5)
    N_fft = int(np.clip(N_opt, 256, 8192))
    N_fft = int(2**np.ceil(np.log2(N_fft)))
    return N_fft

# ═══════════════════════════════════════════════════════════════
# Carrier recovery chains
# ═══════════════════════════════════════════════════════════════
def carrier_recovery_fixed(rx):
    fo_est = fft_foe(rx, N_fft=FIXED_CFG['N_fft'])
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=FIXED_CFG['omega_n'], zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=FIXED_CFG['M_vv'])
    return rx_cpr

def carrier_recovery_old_adapt(rx, h_est, gamma_bar_db=20, h_foe=None):
    """Adaptive FOE only. VV and DPLL use fixed baseline values."""
    if h_foe is None:
        h_foe = h_est
    N_foe = adaptive_params_old(h_foe, gamma_bar_db)
    fo_est = fft_foe(rx, N_fft=N_foe)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=FIXED_CFG['omega_n'], zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=FIXED_CFG['M_vv'])
    return rx_cpr

def carrier_recovery_bv_adapt(rx, h_est, gamma_bar_db=20, f_dot=DOPPLER_HIGH, h_foe=None):
    """Adaptive FOE (bias-variance) only. VV and DPLL use fixed baseline values."""
    if h_foe is None:
        h_foe = h_est
    N_foe = adaptive_params_bv(h_foe, gamma_bar_db, f_dot)
    fo_est = fft_foe(rx, N_fft=N_foe)
    rx_comp = rx * np.exp(-1j * fo_est * np.arange(len(rx)))
    rx_pll, _ = dpll_track(rx_comp, omega_n=FIXED_CFG['omega_n'], zeta=FIXED_CFG['zeta'])
    rx_cpr, _ = vv_cpr(rx_pll, Nw=FIXED_CFG['M_vv'])
    return rx_cpr

# ═══════════════════════════════════════════════════════════════
# MVE experiment
# ═══════════════════════════════════════════════════════════════
def run_mve_trial(Ns, turb_name, f_dot, gamma_bar_db, mode='fixed'):
    """Single MVE trial. mode: 'fixed', 'old_adapt', 'bv_adapt'."""
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns*2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b)
    n_blocks = len(h) // BLOCK
    h_blocks = np.array([np.median(h[i*BLOCK:(i+1)*BLOCK]) for i in range(n_blocks)])
    h_est = np.median(h_blocks)
    h_foe = np.percentile(h_blocks, 10)
    gamma_bar_lin = 10**(gamma_bar_db / 10)
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar_lin)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
    rx = signal + noise
    rx_comp = rx * np.sqrt(h) / (h + 1/gamma_bar_lin)
    rx_comp = amp_limit(rx_comp, 3.0)

    if mode == 'fixed':
        rx_rec = carrier_recovery_fixed(rx_comp)
    elif mode == 'old_adapt':
        rx_rec = carrier_recovery_old_adapt(rx_comp, h_est, gamma_bar_db, h_foe=h_foe)
    elif mode == 'bv_adapt':
        rx_rec = carrier_recovery_bv_adapt(rx_comp, h_est, gamma_bar_db, f_dot, h_foe=h_foe)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return resolve_qpsk(rx_rec, bits)

def run_mve(Ns=10000, n_trials=30, gamma_bar_db=20):
    """Run full MVE: 6 scenarios x 3 modes x n_trials."""
    scenarios = []
    for turb in ['weak', 'moderate', 'strong']:
        for elev, f_dot in [('low', DOPPLER_HIGH), ('high', DOPPLER_LOW)]:
            scenarios.append((turb, elev, f_dot))

    modes = ['fixed', 'old_adapt', 'bv_adapt']
    mode_labels = {
        'fixed': 'Fixed N=1024 (Zhao)',
        'old_adapt': 'Old adapt (noise-only)',
        'bv_adapt': 'New adapt (bias-variance)',
    }
    results = {}

    for turb, elev, f_dot in scenarios:
        label = f"{turb}_{elev}"
        print(f"\n  Scenario: {label} (f_dot={f_dot/1e6:.0f} MHz/s)")

        bers = {m: [] for m in modes}
        for trial in range(n_trials):
            for mode in modes:
                np.random.seed(42 + trial)
                b = run_mve_trial(Ns, turb, f_dot, gamma_bar_db, mode=mode)
                bers[mode].append(b)

        res = {}
        for mode in modes:
            mean_b = np.mean(bers[mode])
            res[mode] = mean_b
            # Gain vs fixed baseline
            fixed_mean = np.mean(bers['fixed'])
            if fixed_mean > 0 and mean_b > 0 and mean_b < fixed_mean:
                gain = 10 * np.log10(fixed_mean / mean_b)
            else:
                gain = 0.0
            res[f'{mode}_gain'] = gain

        results[label] = res
        for mode in modes:
            status = ""
            gain = res[f'{mode}_gain']
            if gain > 0.5: status = "[PASS]"
            elif gain > 0: status = "[WEAK]"
            else: status = "[FAIL/NEG]"
            print(f"    {mode_labels[mode]:30s}: BER={res[mode]:.5f}  Gain={gain:+.2f} dB {status}")

    return results, mode_labels

def plot_mve(results, mode_labels):
    """Plot MVE comparison: BER bars and gain bars."""
    labels = list(results.keys())
    modes = ['fixed', 'old_adapt', 'bv_adapt']
    colors = {'fixed': 'steelblue', 'old_adapt': '#e67e22', 'bv_adapt': '#2ecc71'}

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    # BER comparison
    x = np.arange(len(labels))
    w = 0.25
    for i, mode in enumerate(modes):
        vals = [results[l][mode] for l in labels]
        axes[0].bar(x + (i-1)*w, vals, w, label=mode_labels[mode], color=colors[mode])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
    axes[0].set_ylabel('BER')
    axes[0].set_title('BER Comparison')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_yscale('log')

    # Gain vs fixed
    for mode in ['old_adapt', 'bv_adapt']:
        gains = [results[l][f'{mode}_gain'] for l in labels]
        color = colors[mode]
        axes[1].bar(x if mode == 'old_adapt' else x + 0.3, gains, 0.3,
                    label=mode_labels[mode], color=color)
    axes[1].axhline(0.5, color='green', ls='--', alpha=0.5, label='Pass (0.5 dB)')
    axes[1].axhline(0, color='black', ls='-', alpha=0.3)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=30, ha='right', fontsize=8)
    axes[1].set_ylabel('Gain vs Fixed (dB)')
    axes[1].set_title('Adaptive Gain over Fixed Baseline')
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUT}/mve_bias_variance_foe.pdf')
    plt.close()

def plot_n_opt_comparison():
    """Plot N_opt(h) for all three formulas."""
    h_range = np.linspace(0.05, 3.0, 200)
    gamma_bar = 100  # 20 dB

    N_fixed = np.full_like(h_range, 1024)
    N_old = []
    N_bv = []
    for h in h_range:
        # Old: noise-only
        gamma = gamma_bar * h
        n_old = int(np.clip(80 * gamma_bar / (gamma**2 + 1e-10), 256, 8192))
        n_old = int(2**np.ceil(np.log2(max(n_old, 1))))
        N_old.append(n_old)
        # New: bias-variance
        alpha = 27 / (np.pi**4 * (DOPPLER_HIGH * T_S**2)**2 * gamma_bar)
        n_bv = (alpha / h)**(1/5)
        n_bv = int(np.clip(n_bv, 256, 8192))
        n_bv = int(2**np.ceil(np.log2(max(n_bv, 1))))
        N_bv.append(n_bv)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(h_range, N_fixed, 'b--', lw=2, label='Fixed N=1024 (Zhao)')
    ax.semilogy(h_range, N_old, 'r-', lw=2, label='Old: N=80/(gamma_bar*h^2)')
    ax.semilogy(h_range, N_bv, 'g-', lw=2, label='New: N=(alpha/h)^{1/5} (bias-variance)')
    ax.set_xlabel('Channel gain h')
    ax.set_ylabel('FOE Window N_fft (symbols)')
    ax.set_title('FOE Window Size: Fixed vs Noise-Only vs Bias-Variance Optimal')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(64, 16384)
    plt.tight_layout()
    plt.savefig(f'{OUT}/foe_window_comparison.pdf')
    plt.close()

# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    print("="*60)
    print("Bias-Variance FOE Window Simulation")
    print(f"Output: {OUT}")
    print("="*60)

    # Step 1: N_opt comparison plot
    print("\n[1/3] FOE window comparison plot...")
    plot_n_opt_comparison()
    print("  -> foe_window_comparison.pdf")

    # Step 2: MVE (6 scenarios x 30 trials)
    print("\n[2/3] MVE experiment (6 scenarios x 30 trials x 10000 symbols)...")
    results, mode_labels = run_mve(Ns=10000, n_trials=30, gamma_bar_db=20)
    plot_mve(results, mode_labels)
    print("  -> mve_bias_variance_foe.pdf")

    # Step 3: Summary
    print("\n[3/3] Summary...")
    dt = time.time() - t0
    print(f"\n{'='*60}")
    print(f"Done in {dt:.1f}s\n")

    print("Per-scenario gains (bias-variance vs fixed):")
    bv_pass = 0
    for label, res in results.items():
        gain = res['bv_adapt_gain']
        status = "PASS" if gain > 0.5 else ("WEAK" if gain > 0 else "FAIL/NEG")
        if gain > 0.5:
            bv_pass += 1
        print(f"  {label:20s}: {gain:+.2f} dB [{status}]")
    print(f"\n  BV-FOE scenarios >= 0.5 dB gain: {bv_pass}/6")

    print("\nPer-scenario gains (old noise-only vs fixed):")
    old_pass = 0
    for label, res in results.items():
        gain = res['old_adapt_gain']
        status = "PASS" if gain > 0.5 else ("WEAK" if gain > 0 else "FAIL/NEG")
        if gain > 0.5:
            old_pass += 1
        print(f"  {label:20s}: {gain:+.2f} dB [{status}]")
    print(f"\n  Old-adapt scenarios >= 0.5 dB gain: {old_pass}/6")

    print("\nConclusion:")
    print("  The bias-variance FOE formula gives N ~ h^{-1/5} (weak h-dependence).")
    print("  At LEO FSO parameters, noise dominates over Doppler dynamics,")
    print("  so the optimal N is large (4000-8000), close to Zhao's fixed 1024.")
    if bv_pass >= 4:
        print("  => BV-FOE formula produces POSITIVE gains over fixed baseline.")
    elif bv_pass >= 2:
        print("  => BV-FOE formula produces MIXED results — gains in some scenarios.")
    else:
        print("  => BV-FOE formula shows MINIMAL improvement — noise dominates,")
        print("     confirming that fixed N=1024 is near-optimal for these parameters.")

    # Save results
    save_results = {}
    for label, res in results.items():
        save_results[label] = {k: float(v) if isinstance(v, (np.floating, float)) else v
                               for k, v in res.items()}
    with open(f'{OUT}/mve_bias_variance_results.json', 'w') as f:
        json.dump(save_results, f, indent=2, default=str)
    print(f"\n  Results saved to mve_bias_variance_results.json")
    print("="*60)
