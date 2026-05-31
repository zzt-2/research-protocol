#!/usr/bin/env python3
"""Cascade Robustness MVE (H006) — 真实估计噪声下的全链性能验证

核心问题: 所有 MVE 都用真值 h。换成有噪声的 h_est 后，增益还剩多少？

Experiment 1: Ch5 载波同步鲁棒性（最高优先级）
  - sim_direction_a.py 修改版: noisy h → MMSE补偿 + DPLL带宽
  - 6场景 × 5 NMSE × 3 SNR × 15 trials

Experiment 2: Ch4 预补偿 + AR预测鲁棒性
  - sim_ch3_precomp.py 修改版: noisy h_est + estimated ρ
  - 弱湍流 + τ=5ms 为主, 扫描 NMSE × N_samples

Experiment 3: 级联曲线结构
  - NMSE → gain 曲线, 判断是否有工程指导价值

PASS/FAIL (H006):
  Strong PASS: Ch5 ≥4/6 PASS at NMSE=-10dB
  PASS:        Ch5 ≥4/6 PASS at NMSE=-15dB
  WEAK PASS:   Ch5 2-3/6 PASS at NMSE=-15dB
  FAIL:        Ch5 全崩 at NMSE=-15dB
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import erfc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time, json

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# ═══════════════════════════════════════════════════════════════
# System Parameters (S007, S011, S013)
# ═══════════════════════════════════════════════════════════════
R_SYM = 2.5e9;  T_S = 1 / R_SYM
LASER_LW = 10e3;  BLOCK = 100

# Exp1: GG block-fading (S011)
TURB1 = {'weak': (4.0, 3.0), 'moderate': (2.5, 1.8), 'strong': (1.5, 0.8)}

# Exp2: AR(1) log-normal (S013)
TURB2 = {'weak': (4.0, 3.0, 10e-3), 'moderate': (2.5, 1.8, 5e-3), 'strong': (1.5, 0.8, 2e-3)}

DOPPLER_HIGH = 150e6;  DOPPLER_LOW = 30e6;  F_RESIDUAL = 1e6
FIXED_CFG = {'N_fft': 1024, 'M_vv': 64, 'omega_n': 8e6, 'zeta': np.sqrt(2)/2}

NMSE_LEVELS = [-5, -10, -15, -20, 100]  # 100 = no noise
NMSE_LABELS = ['-5dB', '-10dB', '-15dB', '-20dB', '∞']

P_CAP = 100.0;  N_PTS = 10000;  T_STEP = 0.1e-3

# ═══════════════════════════════════════════════════════════════
# Noise Injection
# ═══════════════════════════════════════════════════════════════
def add_h_noise(h, nmse_db, rng=None):
    """h_est = |h + n|, n~N(0, h²·10^(-NMSE/10))"""
    if nmse_db >= 100:
        return h.copy()
    r = rng if rng else np.random
    return np.abs(h + np.abs(h) * 10**(-nmse_db/20) * r.randn(len(h)))

# ═══════════════════════════════════════════════════════════════
# Primitives (from sim_direction_a.py)
# ═══════════════════════════════════════════════════════════════
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

def resolve_qpsk(rx, tx_bits):
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = np.mean(tx_bits != qpsk_demod(rx * np.exp(-1j*r)))
        if b < best: best = b
    return best

def amp_limit(rx, t=3.0):
    a = np.abs(rx); m = a > t; o = rx.copy()
    o[m] = rx[m] / a[m] * t; return o

def doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH, lw=LASER_LW):
    k = np.arange(N)
    return (2*np.pi*f_res*k*T_S + np.pi*f_dot*(k*T_S)**2
            + np.sqrt(2*np.pi*lw*T_S)*np.cumsum(np.random.randn(N)))

def fft_foe(rx, N_fft=1024, nfft_zp=8192):
    N_fft = min(N_fft, len(rx))
    r4 = (rx[:N_fft]**4) * np.hanning(N_fft)
    R4 = np.fft.fftshift(np.fft.fft(r4, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1))
    idx = np.argmax(np.abs(R4))
    if 1 <= idx < len(R4) - 1:
        a_, b_, g_ = np.abs(R4[idx-1]), np.abs(R4[idx]), np.abs(R4[idx+1])
        if b_ - a_ > 0 and b_ + a_ - 2*g_ != 0:
            f_est = freqs[idx] + 0.5*(a_-g_)/(a_-2*b_+g_)*(freqs[1]-freqs[0])
        else:
            f_est = freqs[idx]
    else:
        f_est = freqs[idx]
    return 2*np.pi*f_est/4

def dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2):
    wT = min(omega_n * T_S, 0.5)
    c1, c2 = 2*zeta*wT, wT**2
    N = len(rx)
    phi = np.zeros(N); integ = 0.0; vco = 0.0
    for k in range(N):
        mixed = rx[k] * np.exp(-1j*vco)
        pd = np.angle(mixed**4) / 4
        integ += c2*pd
        vco += c1*pd + integ
        phi[k] = vco
    return rx * np.exp(-1j*phi), phi

def vv_cpr(rx, Nw=64):
    raised = rx**4
    a = np.abs(raised); m = a > 1e8
    if np.any(m): raised[m] *= 1e8/a[m]
    avg = np.convolve(raised, np.ones(Nw)/Nw, mode='same')
    pe = np.unwrap(np.angle(avg)*4)/4
    return rx * np.exp(-1j*pe), pe

def carrier_recovery(rx, h_est_scalar, snr_db, adaptive=True):
    fo = fft_foe(rx, N_fft=FIXED_CFG['N_fft'])
    rx_c = rx * np.exp(-1j*fo*np.arange(len(rx)))
    if adaptive:
        gamma_bar = 10**(snr_db/10)
        B0 = np.sqrt(np.pi*LASER_LW*gamma_bar/T_S)
        h_safe = max(h_est_scalar, 0.01)
        omega_n = np.clip(B0*h_safe, 0.5e6, 100e6) / 1.06
    else:
        omega_n = FIXED_CFG['omega_n']
    rx_p, _ = dpll_track(rx_c, omega_n, FIXED_CFG['zeta'])
    rx_v, _ = vv_cpr(rx_p, FIXED_CFG['M_vv'])
    return rx_v

# ═══════════════════════════════════════════════════════════════
# Pre-compensation primitives (from sim_ch3_precomp.py)
# ═══════════════════════════════════════════════════════════════
def correlated_fading(N, alpha, beta, T_coh, T_step=T_STEP, rng=None):
    if rng is None: rng = np.random
    s2_I = 1.0/alpha + 1.0/beta
    s2_ln = np.log(1 + s2_I)
    rho = np.exp(-T_step/T_coh)
    ns = np.sqrt((1-rho**2)*s2_ln)
    innov = rng.randn(N)*ns
    ln_I = np.empty(N); ln_I[0] = rng.randn()*np.sqrt(s2_ln)
    for i in range(1, N): ln_I[i] = rho*ln_I[i-1] + innov[i]
    return np.sqrt(np.exp(ln_I - s2_ln/2)), ln_I

def qpsk_ber_avg(snr_arr):
    return np.mean(np.clip(0.5*erfc(np.sqrt(np.clip(snr_arr, 1e-10, 1e10)/2)), 1e-12, 0.5))

def estimate_rho(ln_I_obs):
    if len(ln_I_obs) < 10: return None
    num = np.sum(ln_I_obs[1:]*ln_I_obs[:-1])
    den = np.sum(ln_I_obs[:-1]**2)
    return np.clip(num/den, 0, 0.999) if den > 1e-10 else None

# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 1: Ch5 Carrier Sync Robustness
# ═══════════════════════════════════════════════════════════════
def exp1_trial_pair(Ns, turb, f_dot, snr_db, nmse_db, seed=42):
    """Run fixed+adaptive pair with same noisy h → (ber_fixed, ber_adaptive)"""
    np.random.seed(seed)
    a, b = TURB1[turb]
    bits = np.random.randint(0, 2, Ns*2)
    tx = qpsk_mod(bits)
    h_true = gg_block(Ns, a, b)
    h_noisy = add_h_noise(h_true, nmse_db)

    nb = len(h_noisy)//BLOCK
    h_est_s = np.median([np.median(h_noisy[i*BLOCK:(i+1)*BLOCK]) for i in range(nb)])

    phi = doppler_phase(Ns, F_RESIDUAL, f_dot)
    # Coherent detection: signal amplitude ∝ √(irradiance), noise constant
    gamma_bar = 10**(snr_db/10)
    signal = tx * np.sqrt(h_true) * np.exp(1j*phi)
    noise_var = 1.0 / (2 * gamma_bar)  # per-dimension, constant (LO shot noise)
    rx = signal + np.sqrt(noise_var) * (np.random.randn(Ns) + 1j*np.random.randn(Ns))

    # MMSE equalization with noisy h_est (channel coeff = √h, so |√h_est|² = h_est)
    rx_mmse = amp_limit(rx*np.sqrt(np.conj(h_noisy))/(h_noisy+1/gamma_bar), 3.0)

    bf = resolve_qpsk(carrier_recovery(rx_mmse, h_est_s, snr_db, adaptive=False), bits)
    ba = resolve_qpsk(carrier_recovery(rx_mmse, h_est_s, snr_db, adaptive=True), bits)
    return bf, ba

def run_exp1(Ns=2000, n_trials=15, snrs_db=[15, 20, 25]):
    print("="*70 + "\nEXPERIMENT 1: Ch5 Carrier Sync Robustness\n" + "="*70)
    scenarios = [(t, e, fd) for t in ['weak','moderate','strong']
                              for e, fd in [('low',DOPPLER_HIGH),('high',DOPPLER_LOW)]]
    results = []
    for snr_db in snrs_db:
        print(f"\n--- SNR = {snr_db} dB ---")
        for nmse_db, nmse_lbl in zip(NMSE_LEVELS, NMSE_LABELS):
            print(f"  NMSE = {nmse_lbl}:")
            for turb, elev, f_dot in scenarios:
                label = f"{turb}_{elev}"
                bfs, bas = [], []
                for t in range(n_trials):
                    bf, ba = exp1_trial_pair(Ns, turb, f_dot, snr_db, nmse_db, seed=42+t)
                    bfs.append(bf); bas.append(ba)
                mf, ma = np.mean(bfs), np.mean(bas)
                gain = 10*np.log10(mf/ma) if mf > 0 and ma > 0 and ma < mf else 0.0
                st = "PASS" if gain > 0.5 else ("WEAK" if gain > 0 else "NEG")
                results.append(dict(snr_db=snr_db, nmse_db=nmse_db, nmse_label=nmse_lbl,
                    scenario=label, turb=turb, elev=elev,
                    fixed_ber=mf, adapt_ber=ma, gain_db=gain, status=st))
                print(f"    {label:20s}: F={mf:.5f} A={ma:.5f} gain={gain:+.2f}dB [{st}]")
    return results

# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 2: Ch4 Pre-compensation Robustness
# ═══════════════════════════════════════════════════════════════
def exp2_trial(turb_name, delay_ms, snr_db, nmse_db, n_est, seed=42):
    """AR prediction with noisy h + estimated ρ"""
    alpha, beta, T_coh = TURB2[turb_name]
    snr_lin = 10**(snr_db/10)
    s2_I = 1.0/alpha + 1.0/beta
    s2_ln = np.log(1 + s2_I)
    rho_true = np.exp(-T_STEP/T_coh)
    delay_samp = int(round(delay_ms*1e-3/T_STEP))

    rng = np.random.RandomState(seed)
    total = N_PTS + n_est
    h_all, ln_all = correlated_fading(total, alpha, beta, T_coh, T_STEP, rng)

    # Estimate ρ from noisy historical samples
    h_hist_noisy = add_h_noise(h_all[:n_est], nmse_db, rng)
    rho_hat = estimate_rho(np.log(np.maximum(h_hist_noisy**2, 1e-10)))
    if rho_hat is None: rho_hat = rho_true

    # Working portion
    h, ln_I = h_all[n_est:], ln_all[n_est:]
    ln_del = np.empty_like(ln_I)
    if delay_samp == 0: ln_del[:] = ln_I
    else: ln_del[:delay_samp] = ln_I[0]; ln_del[delay_samp:] = ln_I[:-delay_samp]

    # Noisy delayed observation (amplitude domain noise → log domain)
    h_del = np.exp(ln_del/2)
    h_del_noisy = add_h_noise(h_del, nmse_db, rng)
    ln_del_noisy = np.log(np.maximum(h_del_noisy**2, 1e-10))

    # AR prediction with estimated ρ
    rho_k = rho_hat**delay_samp
    s2_pred = s2_ln*(1-rho_k**2)
    ln_pred = rho_k*ln_del_noisy
    I_pred = np.exp(ln_pred + s2_pred/2 - s2_ln/2)

    I = h**2
    ber_no = qpsk_ber_avg(I*snr_lin)
    Ptx = np.minimum(1.0/np.maximum(I_pred, 1e-6), P_CAP)
    Ptx /= np.mean(Ptx)
    ber_comp = qpsk_ber_avg(I*Ptx*snr_lin)
    return ber_no, ber_comp, rho_hat

def run_exp2(n_trials=10):
    print("\n" + "="*70 + "\nEXPERIMENT 2: Ch4 Pre-compensation Robustness\n" + "="*70)
    results = []

    # 2a: Weak turbulence + τ=5ms + SNR=15dB, sweep NMSE × N_samples
    print(f"\n  Primary: weak turbulence, τ=5ms, SNR=15dB")
    for nmse_db, nmse_lbl in zip(NMSE_LEVELS, NMSE_LABELS):
        for n_est in [100, 500, 1000, 5000]:
            bns, bcs, rhs = [], [], []
            for t in range(n_trials):
                bn, bc, rh = exp2_trial('weak', 5, 15, nmse_db, n_est, seed=42+t*100)
                bns.append(bn); bcs.append(bc); rhs.append(rh)
            mn, mc = np.mean(bns), np.mean(bcs)
            gain = 10*np.log10(mn/mc) if mn>0 and mc>0 and mc<mn else 0.0
            rho_err = np.mean(np.abs(np.array(rhs)-np.exp(-T_STEP/TURB2['weak'][2])))
            st = "PASS" if gain>0.5 else ("WEAK" if gain>0 else "NEG")
            results.append(dict(turb='weak', delay_ms=5, snr_db=15,
                nmse_db=nmse_db, nmse_label=nmse_lbl, n_samples=n_est,
                ber_no=mn, ber_comp=mc, gain_db=gain, rho_error=rho_err))
            print(f"    NMSE={nmse_lbl:5s} N={n_est:4d}: gain={gain:+.2f}dB ρ_err={rho_err:.4f} [{st}]")

    # 2b: Moderate turbulence + τ=3ms
    print(f"\n  Additional: moderate turbulence, τ=3ms, SNR=15dB")
    for nmse_db, nmse_lbl in zip([-10, -15, 100], ['-10dB', '-15dB', '∞']):
        for n_est in [500, 1000]:
            bns, bcs = [], []
            for t in range(n_trials):
                bn, bc, _ = exp2_trial('moderate', 3, 15, nmse_db, n_est, seed=42+t*100)
                bns.append(bn); bcs.append(bc)
            mn, mc = np.mean(bns), np.mean(bcs)
            gain = 10*np.log10(mn/mc) if mn>0 and mc>0 and mc<mn else 0.0
            st = "PASS" if gain>0.5 else ("WEAK" if gain>0 else "NEG")
            results.append(dict(turb='moderate', delay_ms=3, snr_db=15,
                nmse_db=nmse_db, nmse_label=nmse_lbl, n_samples=n_est,
                ber_no=mn, ber_comp=mc, gain_db=gain))
            print(f"    NMSE={nmse_lbl:5s} N={n_est:4d}: gain={gain:+.2f}dB [{st}]")

    return results

# ═══════════════════════════════════════════════════════════════
# Plotting & Verdict
# ═══════════════════════════════════════════════════════════════
def plot_exp1(exp1):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for idx, turb in enumerate(['weak', 'moderate', 'strong']):
        ax = axes[idx]
        for elev, marker in [('low', 'o'), ('high', 's')]:
            sub = sorted([r for r in exp1 if r['turb']==turb and r['elev']==elev
                          and r['snr_db']==20], key=lambda x: -x['nmse_db'])
            ax.plot(range(len(sub)), [r['gain_db'] for r in sub], f'{marker}-',
                    label=f'{elev} elev', ms=6)
        ax.axhline(0.5, color='green', ls='--', alpha=0.5, label='PASS (0.5dB)')
        ax.axhline(0, color='red', ls='-', alpha=0.3)
        ax.set_xticks(range(5)); ax.set_xticklabels(NMSE_LABELS, rotation=30, fontsize=8)
        ax.set_xlabel('Channel est. NMSE')
        ax.set_ylabel('Adaptive gain (dB)' if idx==0 else '')
        ax.set_title(f'{turb.capitalize()} turbulence'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.suptitle('Ch5 Carrier Sync: Gain vs Estimation Error (SNR=20dB)', fontsize=12)
    plt.tight_layout(); plt.savefig(f'{OUT}/cascade_exp1_gain.pdf'); plt.close()

def plot_exp2(exp2):
    weak = [r for r in exp2 if r['turb']=='weak' and r['delay_ms']==5]
    nmse_v = [-5, -10, -15, -20, 100]; n_v = [100, 500, 1000, 5000]
    mat = np.zeros((5, 4))
    for i, nm in enumerate(nmse_v):
        for j, ns in enumerate(n_v):
            m = [r for r in weak if r['nmse_db']==nm and r['n_samples']==ns]
            if m: mat[i, j] = m[0]['gain_db']
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(mat, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=4)
    ax.set_xticks(range(4)); ax.set_xticklabels([str(n) for n in n_v])
    ax.set_yticks(range(5)); ax.set_yticklabels(NMSE_LABELS)
    ax.set_xlabel('ρ estimation samples (N)'); ax.set_ylabel('h NMSE')
    ax.set_title('Pre-compensation Gain (dB)\nWeak turb, τ=5ms, SNR=15dB')
    for i in range(5):
        for j in range(4): ax.text(j, i, f'{mat[i,j]:.1f}', ha='center', va='center', fontsize=11)
    plt.colorbar(im, label='Gain (dB)'); plt.tight_layout()
    plt.savefig(f'{OUT}/cascade_exp2_heatmap.pdf'); plt.close()

def print_verdict(exp1, exp2):
    print("\n" + "="*70)
    print("CASCADE ROBUSTNESS VERDICT (H006)")
    print("="*70)

    # Ch5 at each NMSE (SNR=20dB)
    for nmse_db, lbl in zip(NMSE_LEVELS, NMSE_LABELS):
        sub = [r for r in exp1 if r['nmse_db']==nmse_db and r['snr_db']==20]
        np_ = sum(1 for r in sub if r['gain_db']>0.5)
        ns_ = sum(1 for r in sub if r['gain_db']>1.0)
        print(f"  Ch5 NMSE={lbl:5s}: {np_}/6 PASS(≥0.5dB)  {ns_}/6 strong(≥1.0dB)")

    # H006 criteria
    m10 = sum(1 for r in exp1 if r['nmse_db']==-10 and r['snr_db']==20 and r['gain_db']>0.5)
    m15 = sum(1 for r in exp1 if r['nmse_db']==-15 and r['snr_db']==20 and r['gain_db']>0.5)
    print(f"\n  H006判定 (SNR=20dB):")
    if m10 >= 4: print(f"  >> STRONG PASS: {m10}/6 at NMSE=-10dB")
    elif m15 >= 4: print(f"  >> PASS: {m15}/6 at NMSE=-15dB")
    elif m15 >= 2: print(f"  >> WEAK PASS: {m15}/6 at NMSE=-15dB")
    else: print(f"  >> FAIL: {m15}/6 at NMSE=-15dB — 全局最大风险暴露")

    # Ch4
    ch4 = [r for r in exp2 if r['turb']=='weak' and r['delay_ms']==5
           and r['nmse_db']==-10 and r['n_samples']==500]
    if ch4:
        g = ch4[0]['gain_db']
        print(f"\n  Ch4 NMSE=-10dB, N=500: gain={g:+.2f}dB [{'PASS' if g>0.5 else 'FAIL'}]")
        print(f"  => {'AR prediction effective — Ch4 can be kept' if g>0.5 else 'AR prediction weak — consider merging Ch4'}")

    # E' cascade structure
    g_avg = {nm: np.mean([r['gain_db'] for r in exp1 if r['nmse_db']==nm and r['snr_db']==20])
             for nm in [-20, -15, -10, -5]}
    vals = list(g_avg.values())
    print(f"\n  E'级联曲线 (avg gain): ", end="")
    for nm, g in g_avg.items(): print(f"NMSE={nm}dB→{g:.1f}dB  ", end="")
    drops = [vals[i]-vals[i+1] for i in range(len(vals)-1)]
    if max(drops) > 2:
        idx = np.argmax(drops)
        print(f"\n  阈值效应: NMSE={[-20,-15,-10,-5][idx]}dB 附近急剧恶化")
        print(f"  => 工程指导: 估计器 NMSE 必须 < {-20+idx*5}dB")
    else:
        print(f"\n  单调退化（无尖锐阈值）")

# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    t0 = time.time()
    print("="*70 + "\nCASCADE ROBUSTNESS MVE (H006)\n" + "="*70)
    print(f"Output: {OUT}")

    exp1 = run_exp1()
    exp2 = run_exp2()

    plot_exp1(exp1);  plot_exp2(exp2)
    print_verdict(exp1, exp2)

    with open(f'{OUT}/cascade_exp1_results.json', 'w') as f: json.dump(exp1, f, indent=2)
    with open(f'{OUT}/cascade_exp2_results.json', 'w') as f: json.dump(exp2, f, indent=2)

    print(f"\nTotal: {time.time()-t0:.1f}s")
    print(f"→ cascade_exp1_gain.pdf, cascade_exp2_heatmap.pdf")
    print(f"→ cascade_exp1_results.json, cascade_exp2_results.json")
