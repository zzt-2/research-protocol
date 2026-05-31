#!/usr/bin/env python3
"""Ch3 MVE: Power Pre-compensation under Feedback Delay

Question: Does transmitter-side power pre-compensation still work with feedback delay τ?

Method:
1. Generate correlated GG-like fading (AR(1) log-normal approximation)
2. Pre-comp: P_tx(t) = P_nom / |ĥ(t-τ)|², capped at P_max, avg-power normalized
3. Compare BER with/without pre-comp across τ × turbulence × SNR

PASS/FAIL (H004):
- Strong PASS: τ≤20ms gain >3dB
- PASS: τ≤10ms gain >1dB
- Weak PASS: τ≤5ms gain >1dB
- FAIL: τ≥5ms no gain
"""

import numpy as np
from scipy.special import erfc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# ═══════════════════════════════════════════════════════════════
# Parameters (H004 + S007)
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9  # 2.5 Gsps (Zhao 2025)

# Turbulence: (α, β, T_coh)
TURB = {
    'weak':     (4.0, 3.0, 10e-3),
    'moderate': (2.5, 1.8,  5e-3),
    'strong':   (1.5, 0.8,  2e-3),
}

DELAYS_MS = [0, 1, 5, 10, 20, 50, 100]
SNRS_DB = [10, 15, 20]
P_CAP = 100.0       # 20 dB peak power cap (100× nominal)

N_POINTS = 10000     # fading samples per trial
T_STEP = 0.1e-3      # 0.1 ms per sample → 1 s total per trial
N_TRIALS = 10

# ═══════════════════════════════════════════════════════════════
# Channel Model: AR(1) correlated log-normal (GG approximation)
# ═══════════════════════════════════════════════════════════════
def correlated_fading(N, alpha, beta, T_coh, T_step=T_STEP, rng=None):
    """Generate correlated log-normal fading (GG approximation).

    AR(1) on ln(I): ln(I)[n] = ρ·ln(I)[n-1] + √(1-ρ²)·σ_X·w[n]
    Returns amplitude h = √I with E[I] = E[|h|²] = 1.
    """
    if rng is None:
        rng = np.random
    sigma2_I = 1.0 / alpha + 1.0 / beta
    sigma2_ln = np.log(1 + sigma2_I)
    rho = np.exp(-T_step / T_coh)
    noise_std = np.sqrt((1 - rho**2) * sigma2_ln)

    innov = rng.randn(N) * noise_std
    ln_I = np.empty(N)
    ln_I[0] = rng.randn() * np.sqrt(sigma2_ln)
    for i in range(1, N):
        ln_I[i] = rho * ln_I[i - 1] + innov[i]

    # Normalize so E[I] = 1: E[exp(ln_I)] = exp(σ²/2), so subtract σ²/2
    I = np.exp(ln_I - sigma2_ln / 2)
    return np.sqrt(I), ln_I


def qpsk_ber_avg(snr_array):
    """Average QPSK BER over instantaneous SNR array (analytical)."""
    snr = np.clip(snr_array, 1e-10, 1e10)
    return np.mean(np.clip(0.5 * erfc(np.sqrt(snr / 2)), 1e-12, 0.5))

# ═══════════════════════════════════════════════════════════════
# Single Trial (naive: stale estimate, no prediction)
# ═══════════════════════════════════════════════════════════════
def run_trial(turb_name, delay_ms, snr_db, seed=42):
    alpha, beta, T_coh = TURB[turb_name]
    snr_lin = 10 ** (snr_db / 10)
    delay_samples = int(round(delay_ms * 1e-3 / T_STEP))

    rng = np.random.RandomState(seed)
    h, _ = correlated_fading(N_POINTS, alpha, beta, T_coh, T_STEP, rng)

    h_est = np.empty_like(h)
    if delay_samples == 0:
        h_est[:] = h
    else:
        h_est[:delay_samples] = h[0]
        h_est[delay_samples:] = h[:-delay_samples]

    I = h ** 2
    ber_no = qpsk_ber_avg(I * snr_lin)

    P_tx = np.minimum(1.0 / np.maximum(h_est ** 2, 1e-6), P_CAP)
    P_tx = P_tx / np.mean(P_tx)
    ber_comp = qpsk_ber_avg(I * P_tx * snr_lin)

    return ber_no, ber_comp

# ═══════════════════════════════════════════════════════════════
# Single Trial with AR(1) prediction
# ═══════════════════════════════════════════════════════════════
def run_trial_ar(turb_name, delay_ms, snr_db, seed=42):
    """AR(1)-optimal prediction: ĥ_pred(t) from delayed observation.

    AR(1) on ln(I): E[ln(I)(t) | ln(I)(t-k)] = ρ^k · ln(I)(t-k)
    Prediction: I_pred = exp(ρ^k · ln(I)(t-k) + σ²_pred/2)
    where σ²_pred = σ²_ln · (1 - ρ^(2k)) — prediction error variance.

    Key: ρ^k < 1 shrinks estimate toward mean → conservative power
    allocation for large delays.
    """
    alpha, beta, T_coh = TURB[turb_name]
    snr_lin = 10 ** (snr_db / 10)
    sigma2_I = 1.0 / alpha + 1.0 / beta
    sigma2_ln = np.log(1 + sigma2_I)
    rho = np.exp(-T_STEP / T_coh)
    delay_samples = int(round(delay_ms * 1e-3 / T_STEP))

    rng = np.random.RandomState(seed)
    h, ln_I = correlated_fading(N_POINTS, alpha, beta, T_coh, T_STEP, rng)

    # Delayed ln(I) observation
    ln_I_delayed = np.empty_like(ln_I)
    if delay_samples == 0:
        ln_I_delayed[:] = ln_I
    else:
        ln_I_delayed[:delay_samples] = ln_I[0]
        ln_I_delayed[delay_samples:] = ln_I[:-delay_samples]

    # AR(1) optimal prediction of ln(I)(t)
    rho_k = rho ** delay_samples  # total correlation over delay window
    sigma2_pred = sigma2_ln * (1 - rho_k ** 2)
    ln_I_pred = rho_k * ln_I_delayed  # MMSE predictor (zero-mean process)

    # Predicted irradiance: E[I | obs] = exp(pred + σ²_pred/2)
    # But for power allocation we want the point prediction:
    I_pred = np.exp(ln_I_pred + sigma2_pred / 2 - sigma2_ln / 2)
    h_pred = np.sqrt(I_pred)

    I = h ** 2  # true irradiance
    ber_no = qpsk_ber_avg(I * snr_lin)

    P_tx = np.minimum(1.0 / np.maximum(h_pred ** 2, 1e-6), P_CAP)
    P_tx = P_tx / np.mean(P_tx)
    ber_comp = qpsk_ber_avg(I * P_tx * snr_lin)

    return ber_no, ber_comp

# ═══════════════════════════════════════════════════════════════
# Full MVE
# ═══════════════════════════════════════════════════════════════
def run_mve():
    results = []
    for turb_name in ['weak', 'moderate', 'strong']:
        for snr_db in SNRS_DB:
            print(f"\n--- {turb_name}, SNR={snr_db}dB ---")
            for delay_ms in DELAYS_MS:
                bers_no, bers_comp = [], []
                for t in range(N_TRIALS):
                    seed = 42 + t * 100 + hash((turb_name, snr_db)) % 1000
                    bn, bc = run_trial(turb_name, delay_ms, snr_db, seed)
                    bers_no.append(bn)
                    bers_comp.append(bc)

                mn, mc = np.mean(bers_no), np.mean(bers_comp)
                gain = 10 * np.log10(mn / mc) if mn > 0 and mc > 0 and mc < mn else 0.0
                r = dict(turb=turb_name, snr_db=snr_db, delay_ms=delay_ms,
                         ber_no=mn, ber_comp=mc, gain_db=gain)
                results.append(r)
                tag = "PASS" if gain > 1.0 else ("WEAK" if gain > 0.3 else ("ZERO" if gain >= -0.1 else "NEG"))
                print(f"  τ={delay_ms:3d}ms: BER {mn:.6f}→{mc:.6f} ({gain:+.2f}dB) [{tag}]")
    return results

# ═══════════════════════════════════════════════════════════════
# Plotting
# ═══════════════════════════════════════════════════════════════
def plot_gain_vs_delay(results):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for idx, turb_name in enumerate(['weak', 'moderate', 'strong']):
        ax = axes[idx]
        for snr_db in SNRS_DB:
            sub = [r for r in results if r['turb'] == turb_name and r['snr_db'] == snr_db]
            ax.plot([r['delay_ms'] for r in sub], [r['gain_db'] for r in sub],
                    'o-', label=f'SNR={snr_db}dB', ms=5)
        ax.axhline(1.0, color='green', ls='--', alpha=0.5, label='PASS (1dB)')
        ax.axhline(0, color='red', ls='-', alpha=0.3)
        ax.set_xlabel('Feedback delay τ (ms)')
        ax.set_ylabel('Gain (dB)' if idx == 0 else '')
        ax.set_title(f'{turb_name.capitalize()} turbulence')
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
        ax.set_xscale('symlog', linthresh=1)
    plt.suptitle('Ch3 MVE: Power Pre-compensation Gain vs Feedback Delay', fontsize=12)
    plt.tight_layout(); plt.savefig(f'{OUT}/mve_ch3_gain.pdf'); plt.close()


def plot_ber_vs_delay(results):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for idx, turb_name in enumerate(['weak', 'moderate', 'strong']):
        ax = axes[idx]
        for snr_db in SNRS_DB:
            sub = [r for r in results if r['turb'] == turb_name and r['snr_db'] == snr_db]
            ax.semilogy([r['delay_ms'] for r in sub], [r['ber_no'] for r in sub],
                        's--', label=f'No comp ({snr_db}dB)', ms=4, alpha=0.7)
            ax.semilogy([r['delay_ms'] for r in sub], [r['ber_comp'] for r in sub],
                        'o-', label=f'Pre-comp ({snr_db}dB)', ms=4)
        ax.set_xlabel('Feedback delay τ (ms)')
        ax.set_ylabel('BER' if idx == 0 else '')
        ax.set_title(f'{turb_name.capitalize()} turbulence')
        ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
        ax.set_xscale('symlog', linthresh=1)
    plt.suptitle('Ch3 MVE: BER vs Feedback Delay', fontsize=12)
    plt.tight_layout(); plt.savefig(f'{OUT}/mve_ch3_ber.pdf'); plt.close()

# ═══════════════════════════════════════════════════════════════
# Verdict (H004 criteria)
# ═══════════════════════════════════════════════════════════════
def verdict(results):
    print("\n" + "=" * 60)
    print("MVE VERDICT (H004 criteria — excluding τ=0 perfect feedback)")
    print("=" * 60)

    ref = [r for r in results if r['snr_db'] == 15 and r['delay_ms'] > 0]

    strong = any(r['gain_db'] > 3.0 and r['delay_ms'] <= 20 for r in ref)
    regular = any(r['gain_db'] > 1.0 and r['delay_ms'] <= 10 for r in ref)
    weak = any(r['gain_db'] > 1.0 and r['delay_ms'] <= 5 for r in ref)
    fail = all(r['gain_db'] < 0.3 for r in ref if r['delay_ms'] >= 5)

    if strong:
        print("=> STRONG PASS: τ≤20ms gain >3dB — Ch3 充足底气")
    elif regular:
        print("=> PASS: τ≤10ms gain >1dB — Ch3 可写，需限制适用场景")
    elif weak:
        print("=> WEAK PASS: τ≤5ms gain >1dB — 偏薄，考虑加入简单预测")
    elif fail:
        print("=> FAIL: τ≥5ms 无改善 — Ch3 需要换定位或合并到Ch4")
    else:
        print("=> MIXED: 部分场景有增益，需具体分析")

    print("\nPer-turbulence max usable delay (SNR=15dB, >0.5dB gain, τ>0):")
    for turb in ['weak', 'moderate', 'strong']:
        usable = [r['delay_ms'] for r in ref
                  if r['turb'] == turb and r['gain_db'] > 0.5]
        if usable:
            print(f"  {turb}: max τ = {max(usable)}ms "
                  f"(gains: {', '.join(f'{d}ms:{[r for r in ref if r['turb']==turb and r['delay_ms']==d][0]['gain_db']:.1f}dB' for d in sorted(usable))})")
        else:
            print(f"  {turb}: no usable delay >0ms")

# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    n_total = len(DELAYS_MS) * len(TURB) * len(SNRS_DB) * N_TRIALS
    print("=" * 60)
    print("Ch3 MVE: Power Pre-compensation under Feedback Delay")
    print(f"Output: {OUT}")
    print(f"Config: {n_total} trials ({len(DELAYS_MS)}×{len(TURB)}×{len(SNRS_DB)}×{N_TRIALS})")
    print("=" * 60)

    results = run_mve()

    # Fine-grained sweep: 0.5-5ms to find transition point
    print("\n" + "=" * 60)
    print("Fine-grained sweep (0.5-5ms, SNR=15dB)")
    print("=" * 60)
    fine_delays = [0.5, 1, 1.5, 2, 3, 4, 5]
    fine_results = []
    for turb_name in ['weak', 'moderate', 'strong']:
        print(f"\n  {turb_name}:")
        for d_ms in fine_delays:
            bers_no, bers_comp = [], []
            for t in range(N_TRIALS):
                seed = 42 + t * 100 + hash((turb_name, 15, 'fine')) % 1000
                bn, bc = run_trial(turb_name, d_ms, 15, seed)
                bers_no.append(bn)
                bers_comp.append(bc)
            mn, mc = np.mean(bers_no), np.mean(bers_comp)
            gain = 10 * np.log10(mn / mc) if mn > 0 and mc > 0 and mc < mn else 0.0
            fine_results.append(dict(turb=turb_name, snr_db=15, delay_ms=d_ms,
                                     ber_no=mn, ber_comp=mc, gain_db=gain))
            tag = "✓" if gain > 0.5 else "✗"
            print(f"    τ={d_ms:.1f}ms: {mn:.6f}→{mc:.6f} ({gain:+.2f}dB) {tag}")
    results.extend(fine_results)

    # AR(1) prediction sweep: same delays as main MVE
    print("\n" + "=" * 60)
    print("AR(1) Prediction sweep (SNR=15dB)")
    print("=" * 60)
    ar_delays = [0, 1, 2, 3, 5, 10, 15, 20, 50, 100]
    ar_results = []
    for turb_name in ['weak', 'moderate', 'strong']:
        print(f"\n  {turb_name} (AR prediction):")
        for d_ms in ar_delays:
            bers_no, bers_comp = [], []
            for t in range(N_TRIALS):
                seed = 42 + t * 100 + hash((turb_name, 15, 'ar')) % 1000
                bn, bc = run_trial_ar(turb_name, d_ms, 15, seed)
                bers_no.append(bn)
                bers_comp.append(bc)
            mn, mc = np.mean(bers_no), np.mean(bers_comp)
            gain = 10 * np.log10(mn / mc) if mn > 0 and mc > 0 and mc < mn else 0.0
            ar_results.append(dict(turb=turb_name, snr_db=15, delay_ms=d_ms,
                                   ber_no=mn, ber_comp=mc, gain_db=gain, method='AR'))
            tag = "PASS" if gain > 1.0 else ("WEAK" if gain > 0.3 else "NEG")
            print(f"    τ={d_ms:3d}ms: {mn:.6f}→{mc:.6f} ({gain:+.2f}dB) [{tag}]")

    # Naive vs AR comparison table at key delays
    print("\n" + "=" * 60)
    print("Naive vs AR prediction comparison (SNR=15dB)")
    print("=" * 60)
    for turb_name in ['weak', 'moderate', 'strong']:
        print(f"\n  {turb_name}:")
        for d_ms in [1, 3, 5, 10, 20]:
            naive_r = [r for r in results if r['turb'] == turb_name and r['delay_ms'] == d_ms and r['snr_db'] == 15]
            ar_r = [r for r in ar_results if r['turb'] == turb_name and r['delay_ms'] == d_ms]
            naive_g = naive_r[0]['gain_db'] if naive_r else 0.0
            ar_g = ar_r[0]['gain_db'] if ar_r else 0.0
            print(f"    τ={d_ms:2d}ms: naive={naive_g:+6.2f}dB  AR={ar_g:+6.2f}dB  Δ={ar_g-naive_g:+.2f}dB")

    plot_gain_vs_delay(results)
    plot_ber_vs_delay(results)
    verdict(results)

    with open(f'{OUT}/mve_ch3_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nDone in {time.time() - t0:.1f}s")
    print(f"-> mve_ch3_gain.pdf, mve_ch3_ber.pdf, mve_ch3_results.json")
