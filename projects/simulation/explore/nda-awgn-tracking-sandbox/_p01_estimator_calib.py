# -*- coding: utf-8 -*-
"""P01 — calibration of receiver-visible pilot SNR estimators under turbulence.

Compares three conventional estimators against TRUE gamma to pick the Phase B
adapter. None of them see true gamma; this is just to measure their bias so the
adapter choice is informed.
  1. coherent pilot:   h=|mean(e)|^2, sigma2=mean|e-mean(e)|^2  (biased by fading)
  2. noncoherent h:    h=mean|e|^2 (incl noise) — needs separate noise est
  3. M2M4 moments:     sigma2=(M4-M2^2)/(2 M2), S=M2-sigma2
All use e(p)=r(p)/s(p) at pilot positions (receiver-visible).
"""
import os
import sys
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _b11_params as P  # noqa: E402
from common import generate_shared_realization_apsk  # noqa: E402
from params import SimulationConfig  # noqa: E402

cfg = SimulationConfig()
PIDX = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)


def est_coherent(raw, tx):
    e = raw[PIDX] / tx[PIDX]
    mu = np.mean(e)
    h = float(np.abs(mu) ** 2)
    s2 = float(np.mean(np.abs(e - mu) ** 2))
    s2 = max(s2, 1e-12)
    return 10 * np.log10(max(h / s2, 1e-12))


def est_m2m4(raw, tx):
    e = raw[PIDX] / tx[PIDX]
    m2 = float(np.mean(np.abs(e) ** 2))
    m4 = float(np.mean(np.abs(e) ** 4))
    if m2 <= 0:
        return 30.0
    s2 = (m4 - m2 * m2) / (2 * m2)
    s2 = max(s2, 1e-12)
    S = max(m2 - s2, 1e-12)
    return 10 * np.log10(S / s2)


def est_noncoherent_block(raw, tx):
    """Block-wise non-coherent: per channel block, h_blk=mean|e|^2, noise from
    the within-block deviation.  Uses known pilot spacing; channel block=CH_BLOCK."""
    e = raw[PIDX] / tx[PIDX]
    mag2 = np.abs(e) ** 2
    n_pilots_per_block = max(1, P.CH_BLOCK // P.DA_PILOT_SPACING)
    S_acc = s2_acc = 0.0
    n_blk = 0
    for i in range(0, len(mag2), n_pilots_per_block):
        seg = mag2[i:i + n_pilots_per_block]
        if len(seg) < 2:
            continue
        h_blk = float(np.mean(seg))
        # within-block variance of |e|^2 driven by noise; for complex AWGN
        # Var(|sqrt(h)+n|^2)=sigma2^2+2 h sigma2.  Solve for sigma2:
        v = float(np.var(seg))
        # sigma2^2 + 2 h sigma2 - v = 0 -> sigma2 = -h + sqrt(h^2+v)
        s2 = -h_blk + np.sqrt(h_blk * h_blk + v)
        s2 = max(s2, 1e-12)
        S_acc += h_blk - s2   # signal power estimate (subtract noise)
        s2_acc += s2
        n_blk += 1
    if n_blk == 0:
        return 30.0
    S = max(S_acc / n_blk, 1e-12)
    s2 = max(s2_acc / n_blk, 1e-12)
    return 10 * np.log10(S / s2)


print("Pilot SNR estimator calibration (50 windows/cell, true gamma NEVER passed to estimator):")
print(f"{'cell':<18}{'true':>6}{'coherent':>10}{'M2M4':>9}{'noncoh_blk':>11}")
for scene in ['weak', 'moderate', 'strong']:
    for snr_true in [5.0, 9.0, 13.0, 17.0]:
        gl = 10 ** (snr_true / 10)
        ec = em = en = []
        ec, em, en = [], [], []
        for b in range(50):
            ws = P.SEED_TURB0 + 0 * 400 + b
            r = generate_shared_realization_apsk(P.N_DFT, gl, scene,
                                                 cfg.doppler.DOPPLER_HIGH,
                                                 mod='m16apsk', seed=ws)
            ec.append(est_coherent(r['rx_raw'], r['tx']))
            em.append(est_m2m4(r['rx_raw'], r['tx']))
            en.append(est_noncoherent_block(r['rx_raw'], r['tx']))
        cell = f"{scene}@{snr_true:.0f}dB"
        print(f"{cell:<18}{snr_true:>6.0f}"
              f"{np.mean(ec):>+8.2f}({np.mean(ec)-snr_true:+.1f})"
              f"{np.mean(em):>+7.2f}({np.mean(em)-snr_true:+.1f})"
              f"{np.mean(en):>+9.2f}({np.mean(en)-snr_true:+.1f})")
