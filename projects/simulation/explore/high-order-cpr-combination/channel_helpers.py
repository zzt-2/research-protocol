"""Channel helpers for T006 — canonical star-ground GG + uniform 16-QAM.

Wraps the SHARED, immutable common/_dual_pol_channel.generate_shared_realization_dp
to produce a single-pol uniform 16-QAM signal with a pilot pattern that ALL
arms share (contract.fairness). Does NOT modify the shared generator.

Block-pilot pattern: pilot at indices {0, L_pilot_block, 2*L_pilot_block, ...}.
Pilot symbols are known 16-QAM symbols. Pilot positions are removed from the
data mask (BER is computed on data positions only).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIM = HERE.parents[1]   # projects/simulation
if str(SIM) not in sys.path:
    sys.path.insert(0, str(SIM))

from common._dual_pol_channel import generate_shared_realization_dp   # noqa: E402
from common._modulation import qam16_mod, qam16_demod   # noqa: E402
from common._config import T_S as CANONICAL_T_S   # noqa: E402

# Flat module import for components (used for truth_assisted_reference below).
import components as components_mod   # noqa: E402


def build_single_pol_qam16_with_pilots(
    *,
    N,
    alpha,
    beta,
    gamma_bar,
    f_g,
    sop_rate,
    seed,
    l_pilot_block=64,
    f_residual_hz=1.0e5,
    f_dot_hz_per_s=0.0,
    laser_lw_hz=10.0e3,
    t_s=CANONICAL_T_S,
):
    """Generate one shared single-pol 16-QAM realization with block pilots.

    Uses the canonical dual-pol generator (modulation='qam16') and extracts
    rX, sX, bitsX. SOP rate is set so the SOP rotation over the frame is small
    (single-pol isolation; the canonical generator models SOP via theta but
    for CPR isolation we keep theta small or zero — controlled by sop_rate).

    Pilot pattern: pilot at symbol index 0 of every l_pilot_block. Pilot
    symbol is a FIXED known 16-QAM symbol (1+1j)/sqrt(2) (replaces the data
    symbol at that position). The data bit stream is generated FIRST (so all
    arms see the same channel+data), then pilot positions are overwritten
    with the known pilot symbol.

    Returns a dict with keys:
        rx : complex ndarray (N,)         single-pol received
        tx_data : complex ndarray (N,)    original data symbols (pre-pilot-overwrite)
        tx_with_pilots : complex ndarray (N,)  tx with pilots at pilot positions
        bits_data : int ndarray (4*N,)    original data bits (pre-pilot-overwrite)
        pilot_idx : int ndarray           pilot symbol indices
        pilot_sym : complex ndarray       known pilot symbols at those indices
        data_mask : bool ndarray (N,)     True where symbol is data (not pilot)
        phi_true : float ndarray (N,)     true per-symbol phase (for O arm only)
        h : float ndarray (N,)            true GG envelope
        theta_sop : float ndarray (N,)    true SOP rotation
        mod : str                         'qam16'
        N, alpha, beta, gamma_bar, f_g, sop_rate, seed
    """
    # Use the canonical dual-pol generator. We force sop_rate and read rX.
    # The canonical generator's noise is per-pol AWGN; rX is single-pol.
    real = generate_shared_realization_dp(
        N, alpha, beta, f_g, sop_rate, seed,
        gamma_bar=gamma_bar, modulation="qam16",
    )
    rX = real["rX"]
    sX = real["sX"]
    bitsX = real["bitsX"]
    h = real["h"]
    theta = real["theta"]

    # The canonical generator's rX already contains sqrt(h) * (cos*sX + sin*sY)
    # + AWGN. The phase of rX relative to sX includes the SOP-induced phase
    # (atan2(sin, cos) of theta). For single-pol CPR we want to track the
    # SOP-induced phase AS the "carrier phase" we recover. But the canonical
    # generator does NOT add an explicit CFO / Wiener laser phase — those are
    # the B10/B12 paper's impairment model. We add them here ON TOP of the
    # canonical channel, using the dimensional-audit CFO/linewidth values.

    # CFO + Wiener laser phase (B10/B12 paper model; added on top of canonical)
    rng = np.random.default_rng(seed + 10**6)   # offset to decorate from canonical draw
    k = np.arange(N)
    phi_fo = 2.0 * np.pi * f_residual_hz * k * t_s
    # Wiener: cumulative sum of Gaussian increments with variance 2*pi*lw*ts
    sigma_pi = np.sqrt(2.0 * np.pi * laser_lw_hz * t_s)
    phi_wiener = sigma_pi * np.cumsum(rng.standard_normal(N))
    phi_sop = theta    # canonical SOP (treated as part of "carrier phase" to recover)
    phi_total = phi_fo + phi_wiener + phi_sop

    # Apply the extra phase (CFO + Wiener) on top of canonical rX.
    # Note: canonical rX already has the SOP rotation; we add CFO+Wiener only.
    # The "true phase" to recover is phi_fo + phi_wiener + phi_sop, all of
    # which are present in rX (SOP from canonical, CFO+Wiener added here).
    rx = rX * np.exp(1j * (phi_fo + phi_wiener))

    # Build pilot pattern: overwrite data with known pilot at pilot positions.
    pilot_idx = np.arange(0, N, l_pilot_block, dtype=int)
    # fixed known pilot symbol (16-QAM-compatible magnitude; use (1+1j)/sqrt(2))
    pilot_sym_value = (1.0 + 1.0j) / np.sqrt(2.0)
    pilot_sym = np.full(pilot_idx.shape, pilot_sym_value, dtype=complex)

    tx_data = sX.copy()
    bits_data = bitsX.copy()
    tx_with_pilots = sX.copy()
    tx_with_pilots[pilot_idx] = pilot_sym
    data_mask = np.ones(N, dtype=bool)
    data_mask[pilot_idx] = False

    # The received signal with pilots: replace rx at pilot positions with the
    # pilot symbol * exp(j*phi_true) + noise. But we cannot "re-noise" — the
    # canonical rx already has the channel+noise baked in at every symbol.
    # The pilot overwrite must therefore happen at the TX side BEFORE the
    # channel; since we cannot re-run the canonical generator, we instead
    # SWAP rx[k] at pilot positions to be (pilot_sym * sqrt(h[k]) * exp(j*phi)
    # + noise[k]). We reconstruct this from the known pilot, the known h and
    # the known phi_total — but that would leak truth into the pilot positions.
    #
    # CORRECT APPROACH: regenerate the canonical channel with pilot-bearing TX.
    # The canonical generator accepts a pre-set symbol stream only via its
    # internal RNG draw; to inject pilots we must overwrite TX BEFORE the
    # channel. Since the canonical draw already happened, we instead rebuild
    # the pilot positions' rx by re-using the SAME noise draw at pilot
    # positions and replacing sX->pilot there. The noise at pilot positions
    # is recoverable from rX (rX - sqrt(h)*exp(j*phi)*sX), so:
    #   rx_pilot[k] = sqrt(h[k]) * exp(j*phi_total[k]) * pilot_sym + noise[k]
    # where noise[k] = rX[k] - sqrt(h[k]) * exp(j*theta[k]) *
    #                 (cos(theta[k])*sX[k] + sin(theta[k])*sY[k])
    # This is noise-preserving and does NOT use TX-truth beyond pilot_sym.
    # For single-pol isolation we approximate: noise[k] ~ rX[k] - sqrt(h[k]) *
    # exp(j*theta[k]) * sX[k] (ignoring the sY cross-term, which is small when
    # theta is small — true for the small sop_rate we use).
    sY = real["sY"]
    # canonical forward: rX = sqrt(h)*(cos*sX + sin*sY) + nX
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    clean_rX = np.sqrt(h) * (cos_t * sX + sin_t * sY)
    nX = rX - clean_rX
    # rebuild rx at pilot positions using pilot_sym
    rx_pilot = rx.copy()
    rx_pilot[pilot_idx] = (
        np.sqrt(h[pilot_idx]) * np.exp(1j * phi_total[pilot_idx]) * pilot_sym
        + nX[pilot_idx]
    )

    return {
        "rx": rx_pilot,
        "tx_data": tx_data,
        "tx_with_pilots": tx_with_pilots,
        "bits_data": bits_data,
        "pilot_idx": pilot_idx,
        "pilot_sym": pilot_sym,
        "data_mask": data_mask,
        "phi_true": phi_total,
        "h": h,
        "theta_sop": theta,
        "mod": "qam16",
        "N": int(N), "alpha": float(alpha), "beta": float(beta),
        "gamma_bar": float(gamma_bar), "f_g": float(f_g),
        "sop_rate": float(sop_rate), "seed": int(seed),
        "l_pilot_block": int(l_pilot_block),
        "f_residual_hz": float(f_residual_hz),
        "f_dot_hz_per_s": float(f_dot_hz_per_s),
        "laser_lw_hz": float(laser_lw_hz),
        "t_s": float(t_s),
    }


def ber_on_data(rx_out, bits_data, data_mask):
    """BER on data positions only (consistent denominator across arms).

    Uses qam16_demod on data positions and compares to bits_data at data
    positions. The denominator is the number of data BITS in the eval window
    (4 * data_mask.sum()), identical across arms.
    """
    rx_out = np.asarray(rx_out, dtype=complex)
    bits_data = np.asarray(bits_data, dtype=int)
    data_mask = np.asarray(data_mask, dtype=bool)
    # demodulate all, then select data positions
    bits_hat = qam16_demod(rx_out)   # 4*N bits
    bits_hat = bits_hat.reshape(-1, 4 * len(rx_out))
    bits_data = bits_data.reshape(-1, 4 * len(rx_out))
    # use data positions only
    n_sym = len(rx_out)
    data_sym_mask = data_mask
    bits_per_sym = 4
    data_bit_mask = np.repeat(data_sym_mask, bits_per_sym)
    n_data_bits = int(data_bit_mask.sum())
    if n_data_bits == 0:
        raise ValueError("no data bits in eval window")
    n_err = int(np.sum(bits_hat[0, data_bit_mask] != bits_data[0, data_bit_mask]))
    return n_err / n_data_bits
