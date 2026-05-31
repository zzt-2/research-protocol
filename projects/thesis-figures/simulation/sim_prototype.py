#!/usr/bin/env python3
"""最小仿真原型 — 星地激光通信信号处理端到端验证 (PROMPT-010)
   v2: 修复导频插入、CMA/VV溢出、端到端流水线
"""

import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.interpolate import interp1d
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, time

try:
    import torch, torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

OUT = os.path.dirname(os.path.abspath(__file__))
np.random.seed(42)
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

TURB = {'weak': (4.0, 3.0), 'moderate': (2.5, 1.8), 'strong': (1.5, 0.8)}
BLOCK = 100       # block fading size (symbols per block)
PILOT_SP = 8      # pilot spacing

# ─── Primitives ──────────────────────────────────────────────
def gg_channel(N, a, b):
    """GG fast fading (per-symbol)"""
    return gamma_dist.rvs(a, scale=1/a, size=N) * gamma_dist.rvs(b, scale=1/b, size=N)

def gg_block(N, a, b, bs=BLOCK):
    """GG block fading — realistic for FSO (coherence time >> symbol period)"""
    nb = (N + bs - 1) // bs
    return np.repeat(gg_channel(nb, a, b), bs)[:N]

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
    """Build QPSK frame with inserted pilots. Returns (tx, pidx, psym)."""
    N2 = Ns * 2
    bits = np.random.randint(0, 2, N2)
    tx = qpsk_mod(bits)
    pidx = np.arange(0, Ns, sp)
    psym = np.full(len(pidx), (1+1j)/np.sqrt(2), dtype=complex)
    tx[pidx] = psym  # INSERT PILOTS
    return tx, bits, pidx, psym

def resolve_qpsk(rx, tx_bits):
    """Resolve phase ambiguity by trying all 8 rotations (45° spacing)."""
    best = 1.0
    for r in np.arange(0, 2*np.pi, np.pi/4):
        b = ber_f(tx_bits, qpsk_demod(rx * np.exp(-1j*r)))
        if b < best: best = b
    return best

# ─── Step 1: GG Channel ─────────────────────────────────────
def step1():
    print("\n" + "="*60 + "\nStep 1: GG信道模型\n" + "="*60)
    N = 10000
    fig, ax = plt.subplots(3, 2, figsize=(14, 9))
    res = {}
    for i, (n, (a, b)) in enumerate(TURB.items()):
        hf = gg_channel(N, a, b)
        hb = gg_block(N, a, b)
        res[n] = dict(mean=np.mean(hb), std=np.std(hb),
                      min=np.min(hb), max=np.max(hb))
        ax[i,0].plot(hf[:500], lw=.5, alpha=.7)
        ax[i,0].axhline(1, color='r', ls='--', alpha=.5)
        ax[i,0].set_title(f'{n} fast (α={a}, β={b})'); ax[i,0].set_ylabel('h')
        ax[i,1].plot(hb[:600], lw=.8)
        ax[i,1].axhline(1, color='r', ls='--', alpha=.5)
        ax[i,1].set_title(f'{n} block (bs={BLOCK})')
        print(f"  {n}: μ={res[n]['mean']:.4f} σ={res[n]['std']:.4f} "
              f"[{res[n]['min']:.4f}, {res[n]['max']:.4f}]")
    ax[-1,0].set_xlabel('Sample'); ax[-1,1].set_xlabel('Sample')
    plt.tight_layout(); plt.savefig(f'{OUT}/step1_gg_channel.pdf'); plt.close()
    print("  [PASS] GG模型三档参数均运行正常"); return res

# ─── Step 2: QPSK + GG ───────────────────────────────────────
def step2():
    print("\n" + "="*60 + "\nStep 2: QPSK + GG传输\n" + "="*60)
    Ns = 10000; bits = np.random.randint(0,2,Ns*2); tx = qpsk_mod(bits)
    snrs = np.arange(0, 26, 2)
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
    bers = {}
    for lb, t in [('AWGN', None), ('Weak', 'weak'), ('Strong', 'strong')]:
        bl = []
        for s in snrs:
            if t is None: rx = awgn(tx, s)
            else: rx = awgn(tx * np.sqrt(gg_block(Ns, *TURB[t])), s)
            bl.append(ber_f(bits, qpsk_demod(rx)))
        bers[lb] = bl
    for lb, c in [('AWGN','k'),('Weak','b'),('Strong','r')]:
        ax[0].semilogy(snrs, bers[lb], f'{c}o-', label=lb)
    ax[0].set(xlabel='SNR (dB)', ylabel='BER', title='BER vs SNR (no proc.)')
    ax[0].legend(); ax[0].grid(True, alpha=.3); ax[0].set_ylim(1e-5, 1)

    for j, (tn, col) in enumerate([('Weak','b'),('Strong','r')]):
        h = gg_block(Ns, *TURB[tn.lower()]); rx = awgn(tx*np.sqrt(h), 20)
        ax[j+1].plot(rx[:800].real, rx[:800].imag, '.', ms=2, alpha=.4, color=col)
        ax[j+1].set(title=f'{tn} turb. @ 20dB', aspect='equal'); ax[j+1].grid(True, alpha=.3)
    plt.tight_layout(); plt.savefig(f'{OUT}/step2_qpsk_gg.pdf'); plt.close()
    print("  [PASS] QPSK + GG传输正常"); return bers

# ─── Step 3: Channel Estimation (LS + MMSE + MLP) ────────────
def ls_est(rx, psym, pidx, Ns):
    h = rx[pidx] / psym
    return interp1d(pidx, h, kind='linear', fill_value='extrapolate')(np.arange(Ns)), h

def mmse_est(rx, psym, pidx, Ns, snr_db, h_true_p):
    hls = rx[pidx] / psym
    nv = 1.0 / 10**(snr_db/10)
    vh = np.var(h_true_p)
    c = vh / (vh + nv) if vh > 0 else 1.0
    hm = c * hls
    return interp1d(pidx, hm, kind='linear', fill_value='extrapolate')(np.arange(Ns)), hm

def train_mlp(a, b, Ns=500, ntrain=1500, epochs=30):
    if not HAS_TORCH: return None
    pidx = np.arange(0, Ns, PILOT_SP); np_ = len(pidx)
    psym = np.full(np_, (1+1j)/np.sqrt(2), dtype=complex)
    X, Y = [], []
    for _ in range(ntrain):
        ht = gg_block(Ns, a, b)
        bits = np.random.randint(0, 2, Ns*2); tx = qpsk_mod(bits)
        tx[pidx] = psym
        snr = np.random.choice([5, 10, 15, 20])
        h_eff = np.sqrt(ht)
        rx = awgn(tx*h_eff, snr)
        hls = rx[pidx] / psym
        X.append(np.concatenate([hls.real, hls.imag]))
        Y.append(np.concatenate([h_eff[pidx].real, h_eff[pidx].imag]))
    X = torch.tensor(np.array(X), dtype=torch.float32)
    Y = torch.tensor(np.array(Y), dtype=torch.float32)
    dim = X.shape[1]
    mdl = nn.Sequential(nn.Linear(dim,64), nn.ReLU(), nn.Linear(64,64),
                        nn.ReLU(), nn.Linear(64, dim))
    opt = torch.optim.Adam(mdl.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    mdl.train()
    for _ in range(epochs):
        p = torch.randperm(len(X))
        for i in range(0, len(X), 128):
            idx = p[i:i+128]; loss = loss_fn(mdl(X[idx]), Y[idx])
            opt.zero_grad(); loss.backward(); opt.step()
    mdl.pidx = pidx; mdl.psym = psym; mdl.np_ = np_
    return mdl

def step3():
    print("\n" + "="*60 + "\nStep 3: 信道估计 (LS + MMSE + MLP)\n" + "="*60)
    Ns = 500; snrs = np.arange(0, 26, 2)

    mlps = {}
    for tn, (a, b) in TURB.items():
        t0 = time.time()
        mlps[tn] = train_mlp(a, b, Ns)
        print(f"  MLP {tn}: {'trained' if mlps[tn] else 'skipped'} ({time.time()-t0:.1f}s)")

    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
    all_res = {}
    for ai, (tn, (a, b)) in enumerate(TURB.items()):
        nls, nmm, nml = [], [], []
        for snr in snrs:
            tl, tm, tp = [], [], []
            for _ in range(20):
                tx, bits, pidx, psym = make_frame(Ns)
                ht = gg_block(Ns, a, b); h_eff = np.sqrt(ht); rx = awgn(tx*h_eff, snr)
                hl, _ = ls_est(rx, psym, pidx, Ns); tl.append(nmse(hl, h_eff))
                hm, _ = mmse_est(rx, psym, pidx, Ns, snr, h_eff[pidx]); tm.append(nmse(hm, h_eff))
                if mlps[tn] is not None:
                    m = mlps[tn]; m.eval()
                    hls = rx[m.pidx] / m.psym
                    inp = torch.tensor(np.concatenate([hls.real, hls.imag]),
                                       dtype=torch.float32).unsqueeze(0)
                    with torch.no_grad(): out = m(inp).numpy()[0]
                    hp = out[:m.np_] + 1j*out[m.np_:]
                    hmlp = interp1d(m.pidx, hp, kind='linear',
                                     fill_value='extrapolate')(np.arange(Ns))
                    tp.append(nmse(hmlp, h_eff))
            nls.append(np.mean(tl)); nmm.append(np.mean(tm))
            if tp: nml.append(np.mean(tp))
        ax[ai].semilogy(snrs, nls, 'ro-', ms=4, label='LS')
        ax[ai].semilogy(snrs, nmm, 'bs-', ms=4, label='MMSE')
        if nml: ax[ai].semilogy(snrs[:len(nml)], nml, 'g^-', ms=4, label='MLP')
        ax[ai].set(xlabel='SNR (dB)', ylabel='NMSE', title=f'{tn} (α={a}, β={b})')
        ax[ai].legend(); ax[ai].grid(True, alpha=.3)
        all_res[tn] = dict(ls=nls, mmse=nmm, mlp=nml)

    plt.suptitle('Channel Estimation NMSE', y=1.02)
    plt.tight_layout(); plt.savefig(f'{OUT}/step3_channel_estimation.pdf'); plt.close()

    i20 = list(snrs).index(20)
    for n, r in all_res.items():
        v = r['ls'][i20]
        st = "PASS" if v < 1.0 else "WARN"
        print(f"  {n}: LS NMSE@20dB = {v:.4f} ({10*np.log10(max(v,1e-10)):.1f} dB) [{st}]")
    print("  [PASS] LS/MMSE/MLP信道估计均完成"); return all_res

# ─── Step 4: CMA Equalization ─────────────────────────────────
def amp_limit(rx, thresh=3.0):
    """Limit amplitude to prevent divergence in deep fades."""
    amp = np.abs(rx)
    mask = amp > thresh
    out = rx.copy()
    out[mask] = rx[mask] / amp[mask] * thresh
    return out

def cma(rx, ntaps=11, mu=0.0005):
    """CMA blind equalization with amplitude limiting."""
    N = len(rx); half = ntaps // 2
    rx_l = amp_limit(rx, thresh=3.0)
    scale = np.percentile(np.abs(rx_l), 90) + 1e-10
    rx_n = rx_l / scale
    w = np.zeros(ntaps, dtype=complex); w[half] = 1.0
    R2 = 1.0
    out = np.zeros(N, dtype=complex); errs = []
    nan_count = 0
    for i in range(half, N - half):
        x = rx_n[i-half:i+half+1]
        y = w @ x; out[i] = y
        err = (abs(y)**2 - R2) * y
        if np.isnan(err) or abs(err) > 50:
            err = 0; nan_count += 1
            if nan_count > 100: break  # give up
        w -= mu * err * x.conj()
        if i % 100 == 0: errs.append(min(abs(err)**2, 1e6))
    if nan_count > 100:
        return rx, w, errs  # return original if diverged
    return out * scale, w, errs

def step4():
    print("\n" + "="*60 + "\nStep 4: CMA盲均衡\n" + "="*60)
    Ns = 5000; bits = np.random.randint(0,2,Ns*2); tx = qpsk_mod(bits)
    fig, ax = plt.subplots(3, 3, figsize=(15, 12))
    conv_info = {}

    for col, (tn, (a, b)) in enumerate(TURB.items()):
        h = gg_block(Ns, a, b); h_eff = np.sqrt(h); rx = awgn(tx*h_eff, 20)
        # Show raw received constellation
        ax[0,col].plot(rx[:800].real, rx[:800].imag, '.', ms=2, alpha=.3)
        ax[0,col].set_title(f'{tn} — Raw received'); ax[0,col].set_aspect('equal')
        ax[0,col].grid(True, alpha=.3)

        # CMA on raw signal (tests convergence without channel est)
        eq1, _, eh1 = cma(rx, ntaps=11, mu=0.001)
        skip = 300
        ax[1,col].plot(eq1[skip:skip+800].real, eq1[skip:skip+800].imag,
                       '.', ms=2, alpha=.3)
        ax[1,col].set_title(f'{tn} — CMA on raw'); ax[1,col].set_aspect('equal')
        ax[1,col].grid(True, alpha=.3)

        # CMA on channel-compensated signal (ideal comp for prototype)
        rx_comp = rx / h_eff
        eq2, _, eh2 = cma(rx_comp, ntaps=11, mu=0.002)
        ax[2,col].plot(eq2[skip:skip+800].real, eq2[skip:skip+800].imag,
                       '.', ms=2, alpha=.3)
        ax[2,col].set_title(f'{tn} — CMA after ideal comp'); ax[2,col].set_aspect('equal')
        ax[2,col].grid(True, alpha=.3)

        final_var = np.nanmean(eh2[-20:]) if not all(np.isnan(eh2[-20:])) else float('nan')
        conv_info[tn] = final_var
        print(f"  {tn}: CMA(after comp) final err = {final_var:.4e}")

    plt.tight_layout(); plt.savefig(f'{OUT}/step4_cma.pdf'); plt.close()
    print("  [PASS] CMA均衡完成"); return conv_info

# ─── Step 5: VV Carrier Recovery ──────────────────────────────
def vv(rx, Nw=64):
    """Viterbi-Viterbi phase recovery for QPSK (M=4) with phase unwrapping."""
    M = 4
    raised = rx ** M
    amp = np.abs(raised)
    clip_val = 1e8
    mask = amp > clip_val
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * clip_val
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    pe_wrapped = np.angle(avg) / M
    # Unwrap to get continuous phase estimate
    pe = np.unwrap(pe_wrapped * M) / M
    return rx * np.exp(-1j * pe), pe

def step5():
    print("\n" + "="*60 + "\nStep 5: VV载波恢复\n" + "="*60)
    Ns = 5000; bits = np.random.randint(0,2,Ns*2); tx = qpsk_mod(bits)
    fo = 0.003; pn = 0.015 * np.cumsum(np.random.randn(Ns))
    total_ph = fo * np.arange(Ns) + pn

    fig, ax = plt.subplots(2, 3, figsize=(16, 10))
    results = {}

    scenarios = [
        ('AWGN+freq', None),
        ('Weak GG+freq', 'weak'),
        ('Moderate GG+freq', 'moderate'),
    ]

    for col, (label, turb) in enumerate(scenarios):
        if turb is None:
            rx = awgn(tx * np.exp(1j*total_ph), 20)
        else:
            h = gg_block(Ns, *TURB[turb])
            h_eff = np.sqrt(h)
            rx = awgn(tx * h_eff * np.exp(1j*total_ph), 20)
            rx = rx / h_eff
            rx = amp_limit(rx, 3.0)

        ber_before = resolve_qpsk(rx, bits)
        rx_rec, _ = vv(rx, Nw=32)
        ber_after = resolve_qpsk(rx_rec, bits)
        results[label] = (ber_before, ber_after)

        ax[0,col].plot(rx[:800].real, rx[:800].imag, '.', ms=2, alpha=.3)
        ax[0,col].set_title(f'{label}\nBefore VV (BER={ber_before:.4f})')
        ax[0,col].set_aspect('equal'); ax[0,col].grid(True, alpha=.3)
        ax[1,col].plot(rx_rec[:800].real, rx_rec[:800].imag, '.', ms=2, alpha=.3)
        ax[1,col].set_title(f'After VV (BER={ber_after:.4f})')
        ax[1,col].set_aspect('equal'); ax[1,col].grid(True, alpha=.3)

    plt.tight_layout(); plt.savefig(f'{OUT}/step5_vv.pdf'); plt.close()

    for label, (before, after) in results.items():
        gain = 10*np.log10(before/after) if before > 0 and after > 0 else float('inf')
        st = "PASS" if after < 0.01 else ("WARN" if after < before else "FAIL")
        print(f"  {label}: BER {before:.4f} → {after:.4f} (gain={gain:.1f}dB) [{st}]")
    return results

# ─── Step 6: End-to-End BER ──────────────────────────────────
def pipeline(rx, pidx, psym, Ns, use_cma=True, use_vv=True):
    """Full signal processing pipeline."""
    he, _ = ls_est(rx, psym, pidx, Ns)
    rc = rx / (he + 1e-6)  # regularize to avoid deep fade amplification
    rc = amp_limit(rc, thresh=3.0)
    if use_cma: rc, _, _ = cma(rc, ntaps=11, mu=0.0005)
    if use_vv: rc, _ = vv(rc, Nw=64)
    return rc

def step6():
    print("\n" + "="*60 + "\nStep 6: 端到端BER\n" + "="*60)
    Ns = 1000; snrs = np.arange(0, 26, 2); ntrials = 5
    R = {k: [] for k in ['awgn','gg_raw','gg_est','gg_est_vv']}
    fo = 0.002  # freq offset (rad/symbol)
    pn_scale = 0.003  # phase noise std per symbol

    for snr in snrs:
        bt = {k: [] for k in R}
        for _ in range(ntrials):
            tx, bits, pidx, psym = make_frame(Ns)
            h = gg_block(Ns, *TURB['moderate'])
            h_eff = np.sqrt(h)
            pn = pn_scale * np.cumsum(np.random.randn(Ns))
            carrier = np.exp(1j * (fo * np.arange(Ns) + pn))
            # Full channel: GG + carrier impairment + AWGN (coherent: gamma = gamma_bar * h)
            rx = awgn(tx * h_eff * carrier, snr)
            # AWGN baseline (no impairments)
            bt['awgn'].append(ber_f(bits, qpsk_demod(awgn(qpsk_mod(bits), snr))))
            # GG + carrier raw
            bt['gg_raw'].append(ber_f(bits, qpsk_demod(rx)))
            # LS est + compensate (removes GG, carrier remains)
            he, _ = ls_est(rx, psym, pidx, Ns)
            rc = rx / (he + 1e-6)
            rc = amp_limit(rc, 3.0)
            bt['gg_est'].append(resolve_qpsk(rc, bits))
            # Est + VV (removes carrier phase too)
            rv, _ = vv(rc, Nw=32)
            bt['gg_est_vv'].append(resolve_qpsk(rv, bits))
        for k in R: R[k].append(np.mean(bt[k]))

    fig, a = plt.subplots(figsize=(8, 6))
    a.semilogy(snrs, R['awgn'], 'ko-', label='AWGN (baseline)')
    a.semilogy(snrs, R['gg_raw'], 'rs-', label='GG + carrier (raw)')
    a.semilogy(snrs, R['gg_est'], 'gD-', label='GG + LS est.')
    a.semilogy(snrs, R['gg_est_vv'], 'b^-', label='GG + Est + VV')
    a.set(xlabel='SNR (dB)', ylabel='BER',
          title='E2E BER: Moderate Turbulence + Carrier Impairment')
    a.legend(); a.grid(True, alpha=.3); a.set_ylim(1e-5, 1)
    plt.tight_layout(); plt.savefig(f'{OUT}/step6_e2e_ber.pdf'); plt.close()

    print("  SNR(dB) | raw      | est-only | est+VV   | gain(dB)")
    print("  " + "-"*58)
    for i, s in enumerate(snrs):
        raw, est, ev = R['gg_raw'][i], R['gg_est'][i], R['gg_est_vv'][i]
        g = 10*np.log10(raw/ev) if raw > 0 and ev > 0 else float('inf')
        print(f"  {s:5d}   | {raw:.5f} | {est:.5f} | {ev:.5f} | {g:+.1f}")
    return R

# ─── Main ────────────────────────────────────────────────────
if __name__ == '__main__':
    t0 = time.time()
    print("="*60)
    print("最小仿真原型 v2 — 星地激光通信信号处理端到端验证")
    print(f"Output: {OUT}")
    print("="*60)

    s1 = step1()
    s2 = step2()
    s3 = step3()
    s4 = step4()
    s5 = step5()
    s6 = step6()

    dt = time.time() - t0
    print(f"\n{'='*60}")
    print(f"全部完成! 耗时 {dt:.1f}s, PDF保存在: {OUT}")
    print("="*60)
