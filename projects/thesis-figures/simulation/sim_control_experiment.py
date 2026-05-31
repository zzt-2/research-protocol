#!/usr/bin/env python3
"""对照实验 — 分离估计瓶颈 vs 自适应瓶颈

实验设计：
  A) est-only:       LS估计 → 补偿 → 解调（无VV）
  B) est + VV:       LS估计 → 补偿 → 固定窗口VV → 解调
  C) true-h:         真实h → 补偿 → 解调（无VV）
  D) true-h + VV:    真实h → 补偿 → 固定窗口VV → 解调
  E) true-h + adapt: 真实h → 补偿 → 自适应窗口VV → 解调

关键对比：
  A vs C: 估计误差的影响
  B vs D: VV在有无估计噪声下的表现差异
  D vs E: 自适应窗口的增益（隔离估计噪声后）
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.interpolate import interp1d
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

TURB = {'weak': (4.0, 3.0), 'moderate': (2.5, 1.8), 'strong': (1.5, 0.8)}
BLOCK = 100
PILOT_SP = 8

# ─── Primitives (same as sim_prototype) ──────────────────────
def gg_block(N, a, b, bs=BLOCK):
    nb = (N + bs - 1) // bs
    return np.repeat(
        gamma_dist.rvs(a, scale=1/a, size=nb) * gamma_dist.rvs(b, scale=1/b, size=nb),
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

def ber_f(tx, rx): return np.mean(tx != rx)

def nmse(est, true): return np.mean(np.abs(est-true)**2) / np.mean(np.abs(true)**2)

def make_frame(Ns, sp=PILOT_SP):
    N2 = Ns * 2
    bits = np.random.randint(0, 2, N2)
    tx = qpsk_mod(bits)
    pidx = np.arange(0, Ns, sp)
    psym = np.full(len(pidx), (1+1j)/np.sqrt(2), dtype=complex)
    tx[pidx] = psym
    return tx, bits, pidx, psym

def ls_est(rx, psym, pidx, Ns):
    h = rx[pidx] / psym
    return interp1d(pidx, h, kind='linear', fill_value='extrapolate')(np.arange(Ns)), h

def amp_limit(rx, thresh=3.0):
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_f(tx_bits, qpsk_demod(rx * np.exp(-1j*r)))
        if b < best: best = b
    return best

def vv_fixed(rx, Nw=64):
    """VV with fixed window length."""
    M = 4
    raised = rx ** M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe = np.unwrap(np.angle(avg) / M * M) / M
    return rx * np.exp(-1j * pe), pe

def vv_adaptive(rx, h_est, Nw=64):
    """VV with h-weighted sliding average.

    Rationale: E[1/h²] diverges → unweighted average has infinite variance.
    Weight each sample by |g|^{2M} (g=channel coeff=√h_irradiance) so deep fades contribute less.
    Uses full-window convolution with per-sample weights — no block boundary artifacts.
    """
    M = 4
    raised = rx ** M
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8

    # Per-sample weight: proportional to |h|^{2M} for M-th power VV
    w = np.abs(h_est) ** (2 * M)  # |h|^8
    w = w / (np.sum(w) / len(w) + 1e-10)  # normalize so average weight ~ 1

    # Weighted moving average: sum(w_i * raised_i) / sum(w_i) in sliding window
    weighted = raised * w
    ker = np.ones(Nw) / Nw
    num = np.convolve(weighted, ker, mode='same')
    den = np.convolve(w, ker, mode='same')
    avg = num / (den + 1e-10)

    pe = np.unwrap(np.angle(avg)) / M
    return rx * np.exp(-1j * pe), pe, np.array([Nw])

# ─── Control Experiment ──────────────────────────────────────
def run_control():
    print("=" * 70)
    print("对照实验: 分离估计瓶颈 vs 自适应瓶颈")
    print("=" * 70)

    Ns = 2000
    snrs = [5, 10, 15, 20, 25]
    ntrials = 30  # more trials for stable statistics
    fo = 0.002
    pn_scale = 0.003

    conditions = ['A_est_only', 'B_est_vv', 'C_true_only', 'D_true_vv', 'E_true_adapt']
    labels = {
        'A_est_only':    'A: est-only',
        'B_est_vv':      'B: est+VV(fixed)',
        'C_true_only':   'C: true-h only',
        'D_true_vv':     'D: true-h+VV(fixed)',
        'E_true_adapt':  'E: true-h+VV(adapt)',
    }
    colors = {
        'A_est_only': 'green',
        'B_est_vv':   'blue',
        'C_true_only': 'orange',
        'D_true_vv':  'red',
        'E_true_adapt': 'purple',
    }
    markers = {
        'A_est_only': 'D',
        'B_est_vv':   '^',
        'C_true_only': 's',
        'D_true_vv':  'o',
        'E_true_adapt': 'v',
    }

    all_results = {}

    for turb_name, (a, b) in TURB.items():
        print(f"\n--- {turb_name} turbulence (α={a}, β={b}) ---")
        R = {k: [] for k in conditions}
        adapt_nw_stats = {s: [] for s in snrs}

        for snr in snrs:
            bt = {k: [] for k in conditions}
            nw_list = []

            for trial in range(ntrials):
                tx, bits, pidx, psym = make_frame(Ns)
                h = gg_block(Ns, a, b)  # irradiance from GG distribution
                pn = pn_scale * np.cumsum(np.random.randn(Ns))
                carrier = np.exp(1j * (fo * np.arange(Ns) + pn))
                # Coherent detection: signal amplitude ∝ √(irradiance), noise constant
                gamma_bar = 10**(snr/10)
                signal = tx * np.sqrt(h) * carrier
                noise_var = 1.0 / (2 * gamma_bar)  # per-dimension (LO shot noise)
                rx = signal + np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))
                sqrt_h = np.sqrt(h)  # channel coefficient for coherent detection

                # A: |LS est| amplitude-only → compensate → demod (no VV)
                he, _ = ls_est(rx, psym, pidx, Ns)
                he_abs = np.abs(he) + 1e-6  # amplitude only, carrier phase preserved
                rc_a = rx / he_abs
                rc_a = amp_limit(rc_a, 3.0)
                bt['A_est_only'].append(resolve_qpsk(rc_a, bits))

                # B: |LS est| → compensate → fixed VV → demod
                rv_b, _ = vv_fixed(rc_a, Nw=64)
                bt['B_est_vv'].append(resolve_qpsk(rv_b, bits))

                # C: true √h → compensate → demod (no VV)
                rc_c = rx / sqrt_h
                rc_c = amp_limit(rc_c, 3.0)
                bt['C_true_only'].append(resolve_qpsk(rc_c, bits))

                # D: true √h → compensate → fixed VV → demod
                rv_d, _ = vv_fixed(rc_c, Nw=64)
                bt['D_true_vv'].append(resolve_qpsk(rv_d, bits))

                # E: true √h → compensate → adaptive VV → demod
                rv_e, _, nw_blocks = vv_adaptive(rc_c, sqrt_h, Nw=64)
                bt['E_true_adapt'].append(resolve_qpsk(rv_e, bits))
                nw_list.append(np.mean(nw_blocks))

            for k in conditions:
                R[k].append(np.mean(bt[k]))
            adapt_nw_stats[snr] = nw_list

        all_results[turb_name] = R

        # Print table
        print(f"\n  SNR(dB) | {'A:est-only':>11} | {'B:est+VV':>11} | "
              f"{'C:true-h':>11} | {'D:true+VV':>11} | {'E:true+adapt':>12}")
        print("  " + "-" * 78)
        for i, s in enumerate(snrs):
            vals = [R[k][i] for k in conditions]
            line = f"  {s:5d}   "
            for v in vals:
                line += f"| {v:11.5f} "
            print(line)

        # Key comparisons
        print(f"\n  Key comparisons @ 20dB:")
        i20 = snrs.index(20)
        a_v, b_v, c_v, d_v, e_v = [R[k][i20] for k in conditions]
        print(f"    A vs C (est error impact): {a_v:.5f} vs {c_v:.5f} "
              f"(est penalty = {10*np.log10(a_v/(c_v+1e-10)):.1f} dB)")
        print(f"    B vs D (VV with/without est noise): {b_v:.5f} vs {d_v:.5f}")
        if b_v > a_v:
            print(f"    ** B > A: VV hurts with est noise (by {(b_v/a_v-1)*100:.1f}%) **")
        if d_v < c_v:
            print(f"    D < C: VV helps with true h "
                  f"(gain = {10*np.log10(c_v/(d_v+1e-10)):.1f} dB)")
        if e_v < d_v:
            print(f"    E < D: adaptive window helps "
                  f"(gain = {10*np.log10(d_v/(e_v+1e-10)):.1f} dB)")
        elif e_v > d_v:
            print(f"    E > D: adaptive window hurts (by {(e_v/d_v-1)*100:.1f}%)")
        else:
            print(f"    E ≈ D: adaptive window makes no difference")

        # Adaptive window stats
        nw_arr = np.array(adapt_nw_stats[20])
        print(f"    Adaptive Nw @20dB: mean={np.mean(nw_arr):.1f}, "
              f"range=[{np.min(nw_arr):.0f}, {np.max(nw_arr):.0f}]")

    # ─── Plot ─────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    for ai, (turb_name, R) in enumerate(all_results.items()):
        ax = axes[ai]
        for k in conditions:
            bers = R[k]
            # Clip for log scale
            bers_clipped = [max(b, 1e-6) for b in bers]
            ax.semilogy(snrs, bers_clipped, f'{markers[k]}-',
                        color=colors[k], label=labels[k], ms=6, lw=1.5)

        ax.set(xlabel='SNR (dB)', ylabel='BER',
               title=f'{turb_name.capitalize()} turbulence')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=.3)
        ax.set_ylim(1e-5, 1)

    plt.suptitle('Control Experiment: Estimation Bottleneck vs Adaptive Window',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/control_experiment.pdf')
    plt.close()
    print(f"\n  Plot saved: {OUT}/control_experiment.pdf")

    # ─── Summary ──────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("DIAGNOSIS SUMMARY")
    print("=" * 70)
    for turb_name, R in all_results.items():
        i20 = snrs.index(20)
        a_v, b_v, c_v, d_v, e_v = [R[k][i20] for k in conditions]

        print(f"\n{turb_name.upper()}:")
        if d_v < c_v:
            print(f"  ✓ VV effective with true-h: {c_v:.5f} → {d_v:.5f}")
        else:
            print(f"  ✗ VV ineffective even with true-h: {c_v:.5f} → {d_v:.5f}")

        if b_v > a_v:
            print(f"  ✗ VV HURTS with est noise: {a_v:.5f} → {b_v:.5f}")
        else:
            print(f"  ✓ VV helps with est noise: {a_v:.5f} → {b_v:.5f}")

        est_penalty = a_v / (c_v + 1e-10)
        print(f"  Estimation penalty: {est_penalty:.2f}x "
              f"({10*np.log10(est_penalty):.1f} dB)")

        if e_v < d_v:
            adapt_gain = d_v / (e_v + 1e-10)
            print(f"  ✓ Adaptive window gain (over fixed): {adapt_gain:.2f}x "
                  f"({10*np.log10(adapt_gain):.1f} dB)")
        else:
            print(f"  ✗ Adaptive window NO gain: {d_v:.5f} vs {e_v:.5f}")

        print(f"  Bottleneck: ", end="")
        if b_v > a_v and d_v < c_v:
            print("CHANNEL ESTIMATION (VV works with true-h, hurts with est-h)")
        elif d_v >= c_v:
            print("VV ALGORITHM (VV doesn't help even with true-h)")
        else:
            print("BOTH estimation and VV contribute")

    return all_results


if __name__ == '__main__':
    results = run_control()
