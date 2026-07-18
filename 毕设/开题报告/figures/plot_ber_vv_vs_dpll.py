#!/usr/bin/env python3
"""BER comparison: 4 methods over GG fading, 3 turbulence levels (separate plots).

Methods:
  1. Ideal coherent (analytical, perfect phase knowledge)
  2. VV feedforward (M=64, differential decoding — no oracle)
  3. DPLL 2nd-order feedback (decision-directed)
  4. KF 2-state (phase + freq, decision-directed)

Three separate figures for weak / moderate / strong turbulence.

Short-burst simulation: each burst has N_burst symbols, independent channel
realization. DPLL/KF start with perfect initial phase (simulates ideal acquisition).

Style: SimHei, white bg, light grid, no title, 300 dpi PNG.
Usage: ~/.venvs/torch/bin/python plot_ber_vv_vs_dpll.py
"""

import numpy as np
import os
import json
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from scipy.special import erfc

# ── Style ──
_FONT_PATH = "/mnt/c/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT_PATH):
    fontManager.addfont(_FONT_PATH)
plt.rcParams["font.sans-serif"] = ["SimHei"] + plt.rcParams["font.sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')

# ── Turbulence configs ──
TURB = [
    ('weak',     4.0, 3.0, '弱湍流（α=4.0, β=3.0）',    'ber-vv-vs-dpll-weak.png'),
    ('moderate', 2.5, 1.8, '中等湍流（α=2.5, β=1.8）',  'ber-vv-vs-dpll-moderate.png'),
    ('strong',   1.5, 0.8, '强湍流（α=1.5, β=0.8）',    'ber-vv-vs-dpll-strong.png'),
]

# ── Simulation parameters ──
N_burst = 1000
B_s = 100
N_bursts = 1000
M = 64
delta_f = 5e-4
sigma_pn = 0.008

snr_db = np.arange(0, 26, 2)
snr_lin = 10.0 ** (snr_db / 10.0)

# KF process noise per turbulence
Q_KF = {
    'weak':     1e-4,
    'moderate': 1e-3,
    'strong':   5e-3,
}


def sim_one_burst(N, B_s, alpha, beta, delta_f, sigma_pn, snr_lin,
                  turb_key, rng_ch, rng_sig, rng_noise):
    """Simulate one burst, return (ber_ideal, ber_vv, ber_pll, ber_kf)."""
    # Channel
    h = np.empty(N)
    for i in range(N // B_s):
        X = rng_ch.gamma(alpha, 1.0 / alpha)
        Y = rng_ch.gamma(beta, 1.0 / beta)
        h[i * B_s:(i + 1) * B_s] = X * Y

    # Signal
    theta = delta_f * np.arange(N) + np.cumsum(rng_sig.normal(0, sigma_pn, N))
    k_tx = rng_sig.integers(0, 4, N)
    s = np.exp(1j * (np.pi / 4 + np.pi / 2 * k_tx))

    # Noise
    n = (rng_noise.standard_normal(N) + 1j * rng_noise.standard_normal(N)) \
        / np.sqrt(2 * snr_lin)
    r = h * s * np.exp(1j * theta) + n

    # ── Ideal coherent BER ──
    ber_ideal = np.mean(0.5 * erfc(np.sqrt(snr_lin * h ** 2)))

    # ── VV + differential decoding (no oracle) ──
    r4 = r ** 4
    window = np.ones(M) / M
    avg = np.convolve(r4, window, mode='same')
    theta_vv = np.unwrap(np.angle(avg)) / 4.0
    comp_vv = r * np.exp(-1j * theta_vv)
    # Differential decode: π/4 cancels in diff, so d_phase ≈ k_diff*π/2
    d_vv = comp_vv[1:] * np.conj(comp_vv[:-1])
    d_phase = np.angle(d_vv)
    k_hat_vv = np.mod(np.round(d_phase / (np.pi / 2)).astype(int), 4)
    k_diff = np.mod(k_tx[1:] - k_tx[:-1], 4)
    ber_vv = np.mean(k_diff != k_hat_vv) / 2.0

    # ── DPLL (2nd order, decision-directed) ──
    zeta = 1.0 / np.sqrt(2)
    wn = 0.02
    K1 = 2 * zeta * wn
    K2 = wn ** 2
    theta_pll = np.zeros(N)
    theta_pll[0] = theta[0]
    acc = 0.0
    for k in range(1, N):
        x = r[k] * np.exp(-1j * theta_pll[k - 1])
        s_hat_angle = np.pi / 4 * np.round(np.angle(x) / (np.pi / 4))
        s_hat = np.exp(1j * s_hat_angle)
        e = np.angle(x * np.conj(s_hat))
        acc += K2 * e
        theta_pll[k] = theta_pll[k - 1] + K1 * e + acc

    comp_pll = r * np.exp(-1j * theta_pll)
    k_hat_pll = np.mod(np.round((np.angle(comp_pll) - np.pi / 4)
                                / (np.pi / 2)).astype(int), 4)
    ber_pll = np.mean(k_tx != k_hat_pll) / 2.0

    # ── KF (2-state: phase + freq, 4th-power PD like common.py dpll_track) ──
    q_noise = Q_KF[turb_key]
    Q = np.diag([q_noise, q_noise * 1e-4])
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    x_state = np.array([theta[0], delta_f])  # perfect init
    P_cov = np.diag([0.01, 1e-8])
    theta_kf = np.zeros(N)
    theta_kf[0] = theta[0]

    for k in range(1, N):
        x_pred = F @ x_state
        P_pred = F @ P_cov @ F.T + Q

        # 4th-power phase detector (like common.py dpll_track)
        rx_rot = r[k] * np.exp(-1j * x_pred[0])
        pd_out = np.angle(rx_rot ** 4) / 4.0

        innov = pd_out - x_pred[0]
        innov = (innov + np.pi) % (2 * np.pi) - np.pi

        R = 0.5 / (snr_lin + 1.0)  # simpler, more stable R
        S = H @ P_pred @ H.T + R
        K_gain = P_pred @ H.T / S

        x_state = x_pred + K_gain.flatten() * innov
        x_state[0] = (x_state[0] + np.pi) % (2 * np.pi) - np.pi
        P_cov = (np.eye(2) - K_gain @ H) @ P_pred
        theta_kf[k] = x_state[0]

    comp_kf = r * np.exp(-1j * theta_kf)
    k_hat_kf = np.mod(np.round((np.angle(comp_kf) - np.pi / 4)
                                / (np.pi / 2)).astype(int), 4)
    ber_kf = np.mean(k_tx != k_hat_kf) / 2.0

    return ber_ideal, ber_vv, ber_pll, ber_kf


def run_sweep(alpha, beta, turb_key, label):
    """Run full BER sweep for one turbulence level (with JSON cache)."""
    cache = os.path.join(OUT_DIR, f'ber-cache-{turb_key}.json')
    if os.path.exists(cache):
        with open(cache) as f:
            d = json.load(f)
        print(f"  {label}: loaded from cache")
        return np.array(d['ideal']), np.array(d['vv']), \
               np.array(d['pll']), np.array(d['kf'])

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  {N_bursts} bursts × {N_burst} symbols, VV M={M}, B_s={B_s}")
    print(f"{'='*60}")

    ber_ideal = np.zeros(len(snr_lin))
    ber_vv = np.zeros(len(snr_lin))
    ber_pll = np.zeros(len(snr_lin))
    ber_kf = np.zeros(len(snr_lin))

    t0 = time.time()
    for j, snr in enumerate(snr_lin):
        n_err = [0, 0, 0, 0]
        n_sym_total = 0

        for b in range(N_bursts):
            rng_ch = np.random.default_rng(42 + b * 100 + j)
            rng_sig = np.random.default_rng(100 + b * 100 + j)
            rng_noise = np.random.default_rng(1000 + b * 100 + j)

            bi, bv, bp, bk = sim_one_burst(
                N_burst, B_s, alpha, beta, delta_f, sigma_pn, snr,
                turb_key, rng_ch, rng_sig, rng_noise)
            n_sym = N_burst
            n_err[0] += int(bi * n_sym)
            n_err[1] += int(bv * (n_sym - 1))  # diff decode loses 1 sym
            n_err[2] += int(bp * n_sym)
            n_err[3] += int(bk * n_sym)
            n_sym_total += n_sym

        ber_ideal[j] = max(n_err[0] / n_sym_total, 1.0 / n_sym_total)
        ber_vv[j] = max(n_err[1] / n_sym_total, 1.0 / n_sym_total)
        ber_pll[j] = max(n_err[2] / n_sym_total, 1.0 / n_sym_total)
        ber_kf[j] = max(n_err[3] / n_sym_total, 1.0 / n_sym_total)

        elapsed = time.time() - t0
        print(f"  SNR={snr_db[j]:2d} dB | ideal={ber_ideal[j]:.2e}  "
              f"VV={ber_vv[j]:.2e}  DPLL={ber_pll[j]:.2e}  "
              f"KF={ber_kf[j]:.2e} | {elapsed:.0f}s")

    with open(cache, 'w') as f:
        json.dump({'ideal': ber_ideal.tolist(), 'vv': ber_vv.tolist(),
                   'pll': ber_pll.tolist(), 'kf': ber_kf.tolist()}, f)
    return ber_ideal, ber_vv, ber_pll, ber_kf


def plot_one(ber_ideal, ber_vv, ber_pll, ber_kf, label, filename):
    """Generate one BER figure with smoothed curves and zoomed y-axis."""
    from scipy.interpolate import interp1d
    from scipy.ndimage import uniform_filter1d

    # Interpolate to finer grid
    snr_fine = np.linspace(snr_db[0], snr_db[-1], 100)
    curves = {}
    for name, ber in [('ideal', ber_ideal), ('vv', ber_vv),
                       ('pll', ber_pll), ('kf', ber_kf)]:
        log_ber = np.log10(np.clip(ber, 1e-8, 1))
        f = interp1d(snr_db, log_ber, kind='cubic')
        smoothed = uniform_filter1d(f(snr_fine), size=7)
        curves[name] = np.clip(10 ** smoothed, 1e-8, 1)

    fig, ax = plt.subplots(figsize=(5.5, 4))

    ax.semilogy(snr_fine, curves['ideal'],
                'k--', label='理想相干', linewidth=1.2, alpha=0.7)
    ax.semilogy(snr_fine, curves['vv'],
                '#FF2C00', label='VV 前馈（差分）', linewidth=1.5,
                marker='o', markersize=3, markevery=12)
    ax.semilogy(snr_fine, curves['pll'],
                '#0C5DA5', label='DPLL 反馈', linewidth=1.5,
                marker='s', markersize=3, markevery=12)
    ax.semilogy(snr_fine, curves['kf'],
                '#00B945', label='卡尔曼滤波', linewidth=1.5,
                marker='^', markersize=3, markevery=12)

    ax.set_xlabel('$E_b/N_0$ (dB)')
    ax.set_ylabel('误码率')
    ax.set_ylim(1e-4, 0.5)
    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
    ax.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$',
                        r'$10^{-2}$', r'$10^{-1}$'])
    ax.set_xlim(0, 25)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3, which='both')
    fig.tight_layout()

    out = os.path.join(OUT_DIR, filename)
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"  Saved: {out}")
    plt.close(fig)


# ── Main ──
if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)

    for turb_key, alpha, beta, label, filename in TURB:
        ber_ideal, ber_vv, ber_pll, ber_kf = run_sweep(
            alpha, beta, turb_key, label)
        plot_one(ber_ideal, ber_vv, ber_pll, ber_kf, label, filename)

    print("\nDone.")
