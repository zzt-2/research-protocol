"""B7 OFC 2026 Gardner-TED-reused FOE — three-way comparison MVE.

Three-way comparison (sim-preflight v1.3.0 C7 + V2):
  1. B7 proposed FOE (candidate method)
     - Feed-forward frequency scanning (CV multiplier 1, content.md L37):
       for each f_cand in scan grid, compensate rx by exp(-j*2*pi*f_cand*t),
       compute Gardner TED S-curve peak G(f_residual); f_D_est = f_cand at max G.
     - Two-candidate ambiguity from cos(pi*f_D/B) symmetry (content.md L37
       "generating two Doppler-shift candidates"); resolved by TED2 std
       (smaller std = correct candidate).
     - LPF2 noise suppression (content.md L65, the 0.6dB gain source).
  2. Gardner 1986 TR (grandfather side, V3 red-line alert)
     - Feedback timing recovery loop: Gardner TED -> PI loop filter
       (C1=1/2^5, C2=C1^2/2) -> NCO -> cubic interpolation.
     - Task = STR (timing recovery, estimate tau), NOT FOE (estimate f_D).
     - Python re-implementation of user's Tx2Rx.m L176-214 + PSKTimingErrDetector.m.
     - V3 alert: B7 vs 1986 BER gap should be >0.1dB (orthogonal tasks).
       If parity -> check B7 impl bug (feed-forward misimplemented as feedback).
  3. PSA FOE (baseline, FR-15 target opponent)
     - Spectral-asymmetry CFE (Vieira 2023 VI): dF_est = alpha*ln(P+/P-)/2.
     - Imported from ./_psa_foe_asymmetry.py (S005 rewrite, NOT common/_recovery.py
       which is pilot-aided concept-wrong, D004).
     - D006 coarse-only weak: linear range ~1GHz at 25GBaud/beta=0.1, BER gain
       reported as upper bound.

Source formula audit (V1, sim-preflight v1.3.0 C6):
  - Gardner TED: e(k) = Re{y_mid * (y_curr* - y_prev*)}
      from PSKTimingErrDetector.m L11-12 (zero-DC variant, equivalent) +
      0.2a _b7_map_reconstruction.py (complex form) + Gardner 1986 TM.
  - B7 FOE mechanism: content.md L37 (CV multiplier 1 scan + two candidates +
      TED2 std decision) + L25 (TED gain = max S-curve value).
  - G(f_D) = K_max*|cos(pi*f_D/B)| analytic (S005, _ted_gain_analytic_results.json).
  - PSA FOE: Vieira 2023 VI, dF=alpha*ln(P+/P-)/2 (./_psa_foe_asymmetry.py C6 audit).

Three-way fairness (TL-13):
  - All three methods share the SAME QPSK 25GBaud signal + SAME seed + SAME
    deterministic f_D sweep (rx = tx * exp(j*2*pi*f_D*t)).
  - All three outputs feed the SAME BER evaluation (QPSK hard decision).

This is GW Step 4a dimension D MVE (FR-22). D005 pragmatic route: Go = beat
traditional unoptimized baseline (PSA FOE) by ~dB; FR-21 CRB not Kill gate
(S005 verified CRB std=59.42kHz << 1GHz scan interval).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal as scisig

# Import B7 scenario params from params.py (D005, do not hardcode)
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from params import B7Params  # noqa: E402  (25GBaud/1.8kHz, D005)

# Import PSA FOE baseline (S005 spectral-asymmetry rewrite)
sys.path.insert(0, _HERE)
import _psa_foe_asymmetry as psa  # noqa: E402

# =============================================================================
# Scenario params (from B7Params, D005 溯源; only MVE-specific knobs here)
# =============================================================================
_B7 = B7Params()
BAUD = _B7.R_SYM_B7                  # 25 GHz
ROLL_OFF = _B7.ROLL_OFF              # 0.1
OSNR_MAIN = _B7.OSNR_WORKING_POINT_MAIN   # 17 dB
OSNR_LOW = _B7.OSNR_WORKING_POINT_LOW     # 10 dB
DOPPLER_RANGE = _B7.DOPPLER_RANGE    # 23 GHz
DOPPLER_INTERVAL = _B7.DOPPLER_INTERVAL  # 1 GHz scan step

# Generation / processing rates
SPS_GEN = 16                         # high-rate generation
SPS_RX = 2                           # rate into FOE (content.md L47 "downsampled to 2 sps")
B_REF = 12.5e9                       # 0.1 nm OSNR reference bandwidth

# MVE-scale knobs (smoke test shrinks these)
N_SYM_DEFAULT = 4096
N_SEED_DEFAULT = 3
F_D_GRID_DEFAULT = np.arange(0, 24, 1) * 1e9   # 0..23 GHz step 1 GHz (content.md L49)


# =============================================================================
# Shared signal generation (TL-13: three methods share SAME signal+seed)
# =============================================================================
def make_tx(n_sym, sps_gen, roll_off, rng):
    """Single-pol QPSK -> upsample -> RRC shaping.

    Returns (tx_high unit power, syms original QPSK at 1 sample/sym).
    syms is the BER reference (kept around so BER eval does not need to
    reconstruct from rx via matched filter — which is offset-sensitive).
    """
    bits = rng.integers(0, 2, n_sym * 2)
    syms = ((2 * bits[0::2] - 1) + 1j * (2 * bits[1::2] - 1)) / np.sqrt(2.0)
    up = np.zeros(n_sym * sps_gen, dtype=complex)
    up[::sps_gen] = syms
    h = _rrcos(sps_gen, roll_off, span=8)
    tx = np.convolve(up, h, mode="same")
    P = np.mean(np.abs(tx) ** 2)
    return tx / np.sqrt(P), syms


def _rrcos(sps, beta, span):
    """Root-raised-cosine FIR (unit energy). Matches _b7_map_reconstruction.py."""
    n = span * sps + 1
    t = np.arange(n) - (n - 1) / 2.0
    x = t / sps
    h = np.zeros_like(x, dtype=float)
    eps = 1e-10
    for i, xi in enumerate(x):
        ax = abs(xi)
        if ax < eps:
            h[i] = 1.0 - beta + (4 * beta / np.pi)
        elif abs(ax - 1.0 / (4 * beta)) < eps or abs(ax + 1.0 / (4 * beta)) < eps:
            h[i] = (beta / np.sqrt(2)) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta))
                + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta))
            )
        else:
            num = np.sin(np.pi * (1 - beta) * xi) + 4 * beta * xi * np.cos(np.pi * (1 + beta) * xi)
            den = np.pi * xi * (1 - (4 * beta * xi) ** 2)
            h[i] = num / den
    return h / np.sqrt(np.sum(h ** 2))


def decimate_to_rx(tx_high):
    """High-rate (sps_gen) -> RX rate (sps_rx) via FIR decimation. Returns (tx_rx, fs_rx)."""
    dec = SPS_GEN // SPS_RX
    tx_rx = scisig.decimate(tx_high, dec, ftype="fir", zero_phase=True)
    fs_rx = SPS_RX * BAUD
    return tx_rx, fs_rx


def inject_foe(tx, f_d, fs):
    """Deterministic Doppler shift: rx = tx * exp(j*2*pi*f_D*t)."""
    t = np.arange(tx.size) / fs
    return tx * np.exp(1j * 2 * np.pi * f_d * t)


def add_awgn(sig, osnr_db, baud, rng):
    """Add complex AWGN for OSNR(dB) measured over B_REF=0.1nm bandwidth."""
    if osnr_db is None:
        return sig
    sig_pow = np.mean(np.abs(sig) ** 2)
    fs = SPS_RX * baud
    # noise power spectral density scaled so OSNR over B_REF matches
    noise_var_per_hz = sig_pow / (10.0 ** (osnr_db / 10.0) * B_REF)
    noise_pow = noise_var_per_hz * fs
    n = (rng.standard_normal(sig.size) + 1j * rng.standard_normal(sig.size)) * np.sqrt(noise_pow / 2.0)
    return sig + n


# =============================================================================
# Gardner TED (shared primitive; V1 formula source: PSKTimingErrDetector.m L11-12)
# =============================================================================
def gardner_ted_error(prev_s, mid_s, curr_s):
    """Gardner TED error sample (complex form, equivalent to user's zero-DC variant).

    e(k) = Re{ y_mid * (y_curr* - y_prev*) }
    Source: _b7_map_reconstruction.py + PSKTimingErrDetector.m L11-12 (D001).
    """
    return float(np.real(mid_s * (np.conj(curr_s) - np.conj(prev_s))))


def gardner_s_curve_peak(rx_rx, fs_rx, tau_n=16):
    """Compute Gardner TED S-curve peak G = max_tau |E[e(tau)]| at 2 sps.

    Samples at 2 sps: prev = sym(k-1), mid = sym(k)-0.5, curr = sym(k).
    tau swept over [0,1) symbol in tau_n steps via fractional sample shift
    (here approximated by choosing even/odd sample phase since sps=2).

    Returns G (the S-curve peak = TED gain at the residual Doppler in rx).
    Used by B7 FOE scan to find the f_cand that maximizes G.
    """
    sps = SPS_RX
    n = rx_rx.size
    margin = 2 * sps
    if n < 2 * margin + sps + 1:
        return 0.0
    n_avail = (n - 2 * margin) // sps - 1
    if n_avail < 8:
        return 0.0
    # S-curve over tau in [0,1) symbol; at 2 sps tau has 2 integer phases + we
    # add fractional interpolation by linear shift for tau_n points.
    scurve = np.zeros(tau_n)
    for it in range(tau_n):
        tau = it / tau_n  # [0,1)
        off_f = tau * sps
        off_i = int(np.floor(off_f))
        off_w = off_f - off_i  # linear interp weight for fractional part
        e_acc = 0.0
        cnt = 0
        for k in range(1, n_avail):
            i_prev = (k - 1) * sps + off_i + margin
            i_mid = (k - 1) * sps + sps // 2 + off_i + margin
            i_curr = k * sps + off_i + margin
            if i_curr >= n:
                break
            # fractional-shifted samples via linear interp (sps=2 so fractional
            # part shifts within half-sample; sufficient for peak detection)
            y_prev = rx_rx[i_prev] * (1 - off_w) + rx_rx[i_prev + 1] * off_w if off_w > 0 else rx_rx[i_prev]
            y_mid = rx_rx[i_mid] * (1 - off_w) + rx_rx[i_mid + 1] * off_w if off_w > 0 else rx_rx[i_mid]
            y_curr = rx_rx[i_curr] * (1 - off_w) + (rx_rx[i_curr + 1] * off_w if i_curr + 1 < n else 0) if off_w > 0 else rx_rx[i_curr]
            e_acc += gardner_ted_error(y_prev, y_mid, y_curr)
            cnt += 1
        scurve[it] = e_acc / max(cnt, 1)
    return float(np.max(np.abs(scurve)))


# =============================================================================
# Method 1: B7 proposed FOE (feed-forward frequency scan)
# =============================================================================
def b7_proposed_foe(rx_rx, fs_rx, scan_grid_hz, lpf2_en=True):
    """B7 OFC 2026 proposed FOE (content.md L37).

    1. CV multiplier 1: scan f_cand over (-B, B); for each, compensate
       rx_comp = rx * exp(-j*2*pi*f_cand*t); compute G(rx_comp) = TED gain.
    2. Find f_cand maximizing G -> two candidates (cos symmetry gives +/-).
    3. (LPF2) low-pass filter the compensated signal before TED2 std decision.
    4. TED2 std decision: pick candidate with smaller residual timing-error std.

    Returns (f_D_est, two_candidates, G_curve).
    """
    t = np.arange(rx_rx.size) / fs_rx
    G_curve = np.zeros(len(scan_grid_hz))
    for i, fc in enumerate(scan_grid_hz):
        rx_comp = rx_rx * np.exp(-1j * 2 * np.pi * fc * t)
        if lpf2_en:
            rx_comp = _lpf2(rx_comp, fs_rx)
        G_curve[i] = gardner_s_curve_peak(rx_comp, fs_rx)
    # two candidates: local maxima in G_curve above threshold (content.md L37
    # "generating two Doppler-shift candidates"). Include endpoints as
    # candidates too (the G=K_max|cos(pi*f_D/B)| peak can sit at f=0 or at
    # the scan boundary when f_D_true is near the edge).
    thr = 0.5 * np.max(G_curve)
    peaks_idx = [i for i in range(1, len(G_curve) - 1)
                 if G_curve[i] > thr and G_curve[i] >= G_curve[i - 1] and G_curve[i] >= G_curve[i + 1]]
    # check endpoints (left/right boundary can be a local max)
    if G_curve[0] >= G_curve[1] and G_curve[0] > thr:
        peaks_idx.insert(0, 0)
    if G_curve[-1] >= G_curve[-2] and G_curve[-1] > thr:
        peaks_idx.append(len(G_curve) - 1)
    if not peaks_idx:
        peaks_idx = [int(np.argmax(G_curve))]
    # keep the two strongest distinct peaks
    peaks_idx = sorted(set(peaks_idx), key=lambda i: -G_curve[i])[:2]
    cands = [scan_grid_hz[i] for i in peaks_idx]
    # Single-peak clear case: if only one peak is prominent, no disambiguation
    # is needed — TED2 std decision (content.md L37) is only meaningful when
    # cos(pi*f_D/B) twin peaks are actually comparable. Forcing two candidates
    # when G has one clear max causes TED2 std to pick a residual ~= B alias
    # (TR loop converges but BER blows up). Single-sided scan over one baud
    # period typically yields a single clear peak per true f_D.
    if len(cands) == 1:
        f_D_est = cands[0]
        return f_D_est, cands, G_curve.tolist()
    # Two peaks: only run TED2 std decision if they are comparable in height.
    # If the second peak is much weaker (< 0.7x the primary), trust argmax.
    g_sorted = sorted([G_curve[i] for i in peaks_idx], reverse=True)
    if g_sorted[1] < 0.7 * g_sorted[0]:
        f_D_est = scan_grid_hz[peaks_idx[0]]
        return f_D_est, cands, G_curve.tolist()
    # TED2 std decision: trial-compensate each candidate, run Gardner TR loop,
    # pick smaller residual timing-error std.
    stds = []
    for fc in cands:
        rx_comp = rx_rx * np.exp(-1j * 2 * np.pi * fc * t)
        if lpf2_en:
            rx_comp = _lpf2(rx_comp, fs_rx)
        _, te_std = gardner_1986_tr(rx_comp, fs_rx, return_timing_error=True)
        stds.append(te_std)
    best = int(np.argmin(stds))
    f_D_est = cands[best]
    return f_D_est, cands, G_curve.tolist()


def residual_foe_mth_power(rx, fs_rx, M=4):
    """Residual frequency-offset cleanup via M-th power (QPSK M=4).

    Aligns with poster DSP chain (content.md L47 "MP FOC [7]"), which cleans
    residual FOE after the main FOE stage. Needed for fair three-way BER:
    PSA FOE has bias at f_D=0 (log-asymmetry noise floor) that would otherwise
    leave a small residual FOE ~0.3GHz and wreck the downstream TR loop over
    a 4096-symbol block (2*pi*0.3e9*164ns ~ 6 cycles of phase rotation).
    """
    rx_m = rx ** M
    # coarse residual FOE via FFT peak of M-th power signal
    n = rx_m.size
    spec = np.abs(np.fft.fft(rx_m))
    freqs = np.fft.fftfreq(n, d=1.0 / fs_rx)
    peak_idx = np.argmax(spec)
    df_res = freqs[peak_idx] / M
    t = np.arange(n) / fs_rx
    return rx * np.exp(-1j * 2 * np.pi * df_res * t), df_res


def _lpf2(rx, fs_rx):
    """LPF2 noise suppression (content.md L65, the 0.6dB gain source).

    A low-pass filter applied to the compensated signal before the TR loop,
    which suppresses out-of-band noise and improves the TED2 std decision.
    Cutoff at (1+roll_off)*BAUD/2 = 13.75 GHz (signal bandwidth).
    """
    cutoff = (1 + ROLL_OFF) * BAUD / 2.0
    nyq = fs_rx / 2.0
    wn = min(cutoff / nyq, 0.95)
    b, a = scisig.butter(4, wn, btype="low")
    return scisig.filtfilt(b, a, rx)


# =============================================================================
# Method 2: Gardner 1986 TR (grandfather side, V3 red-line alert)
# Python re-implementation of user's Tx2Rx.m L176-214 (D001).
# =============================================================================
def gardner_1986_tr(rx_rx, fs_rx, return_timing_error=False):
    """Feedback timing recovery loop (Gardner 1986, user's Tx2Rx.m L176-214).

    Gardner TED -> PI loop filter (C1=1/2^5, C2=C1^2/2) -> NCO -> cubic interp.
    Task = STR (estimate tau, timing offset), NOT FOE.

    Returns recovered symbols at optimal sampling instants.
    If return_timing_error, also returns residual timing-error std (for TED2
    decision in B7 FOE and for diagnostics).
    """
    sps = SPS_RX
    C1 = 1.0 / 2 ** 5
    C2 = C1 ** 2 / 2.0
    n = rx_rx.size
    # Normalize amplitude (matches Tx2Rx.m L179 "Amp = max(abs(MatchSig))")
    amp = np.max(np.abs(rx_rx)) + 1e-12
    x = rx_rx / amp
    eta = np.zeros(n)          # NCO output (fractional position)
    omega = np.zeros(n)        # NCO control word (= 1/sps nominal)
    omega[:2] = 1.0 / sps
    eck = np.zeros(n)          # timing error samples
    muk = np.zeros(n)          # fractional mu (0:1)
    inter_one = np.zeros(n, dtype=complex)
    inter_half = np.zeros(n, dtype=complex)
    mk = 0
    te_errors = []
    # Main loop mirrors Tx2Rx.m L192-214
    nstop = n - 4 * 2
    k = 1
    while k < nstop:
        eta[k + 1] = eta[k] - omega[k]
        if eta[k + 1] < 0:
            mk += 1
            eta[k + 1] += 1.0
            muk[k + 1] = eta[k] * sps
            mu = muk[k + 1]
            # cubic interpolation at fractional position mu within (k-1..k+2)
            if k - 1 >= 0 and k + 6 < n:
                inter_one[mk] = _cubic_interp(mu, x[k - 1:k + 3])
                inter_half[mk] = _cubic_interp(mu, x[k + 1:k + 5])
                if mk + 1 < inter_one.size:
                    inter_one[mk + 1] = _cubic_interp(mu, x[k + 3:k + 7])
                # Gardner TED (PSKTimingErrDetector.m L11-12)
                if inter_one[mk + 1] != 0:
                    e = _psk_ted(inter_one[mk], inter_half[mk], inter_one[mk + 1])
                    eck[mk] = e
                    te_errors.append(e)
                    # PI loop filter
                    if mk > 1:
                        omega[k + 1] = (C1 + C2) * eck[mk] - C1 * eck[mk - 1] + omega[k]
                    else:
                        omega[k + 1] = (C1 + C2) * eck[mk] + omega[k]
        else:
            omega[k + 1] = omega[k]
            muk[k + 1] = muk[k]
        k += 1
    out = inter_one[1:mk + 1]
    if return_timing_error:
        te_std = float(np.std(te_errors)) if te_errors else 0.0
        return out, te_std
    return out


def _cubic_interp(mu, y4):
    """Cubic (Farrow) interpolation. mu in [0,1), y4 = 4 samples [y(-1),y(0),y(1),y(2)].

    Matches InterpCubic.m (user's cubic interpolator). Uses standard cubic.
    """
    # Farrow / piecewise-cubic with mu in [0,1] relative to y4[1]
    y = np.asarray(y4)
    mu2 = mu * mu
    mu3 = mu2 * mu
    # standard cubic Hermite coefficients
    h0 = 2 * mu3 - 3 * mu2 + 1
    h1 = mu3 - 2 * mu2 + mu
    h2 = -mu3 + mu2
    h3 = -2 * mu3 + 3 * mu2
    # shift so that interpolation is at y4[1] + mu*(y4[2]-y4[1]) direction
    return h0 * y[1] + h1 * (y[2] - y[0]) / 2.0 + h2 * (y[3] - y[1]) / 2.0 + h3 * y[2]


def _psk_ted(s_prev, s_mid, s_curr):
    """PSKTimingErrDetector.m L11-12 zero-DC variant Gardner TED.

    e = (Re(y_mid) - (Re(y_curr)+Re(y_prev))/2) * (Re(y_curr) - Re(y_prev))
      + (Im(y_mid) - (Im(y_curr)+Im(y_prev))/2) * (Im(y_curr) - Im(y_prev))
    """
    yr = [np.real(s_prev), np.real(s_mid), np.real(s_curr)]
    yi = [np.imag(s_prev), np.imag(s_mid), np.imag(s_curr)]
    er = (yr[1] - (yr[2] + yr[0]) / 2.0) * (yr[2] - yr[0])
    ei = (yi[1] - (yi[2] + yi[0]) / 2.0) * (yi[2] - yi[0])
    return er + ei


# =============================================================================
# Method 3: PSA FOE (baseline) — imported from _psa_foe_asymmetry.py (S005)
# =============================================================================
def psa_foe_baseline(rx_rx, fs_rx, alpha):
    """PSA spectral-asymmetry FOE (Vieira 2023 VI). Returns (rx_comp, df_est)."""
    return psa.psa_foe_asymmetry(rx_rx, fs_rx, alpha, psa.FFT_N)


def calibrate_psa_alpha(tx_rx, fs_rx):
    """Calibrate alpha by 1-point slope fit (Vieira sequential-search proxy)."""
    return psa.calibrate_alpha(tx_rx, fs_rx)


def calibrate_psa_alpha_sequential(tx_rx, fs_rx, cal_grid_GHz=None):
    """Stronger PSA alpha calibration via multi-point linear regression.

    Vieira 2023 uses sequential search to find alpha minimizing estimation
    error. Our 1-point fit (calibrate_psa_alpha) is a crude proxy and
    produces a weak baseline (D006 + S006 finding B: PSA estimation bias
    keeps BER floor high). This stronger calibration fits alpha over a range
    of known f_D points in the linear region, giving a more accurate slope
    df_est / (ln(P+/P-)/2).

    Returns alpha (Hz) that minimizes total |df_est - f_D_true| over cal grid.
    """
    if cal_grid_GHz is None:
        cal_grid_GHz = np.arange(0.5, 3.1, 0.5)
    t = np.arange(tx_rx.size) / fs_rx
    half_logs = []
    f_trues = []
    for f_g in cal_grid_GHz:
        f_D = f_g * 1e9
        rx_shifted = tx_rx * np.exp(1j * 2 * np.pi * f_D * t)
        hl = psa.log_asymmetry(rx_shifted, fs_rx)
        if abs(hl) > 1e-9:
            half_logs.append(hl)
            f_trues.append(f_D)
    half_logs = np.array(half_logs)
    f_trues = np.array(f_trues)
    alpha = float(np.sum(f_trues * half_logs) / np.sum(half_logs ** 2))
    f_est = alpha * half_logs
    rmse_GHz = float(np.sqrt(np.mean((f_est - f_trues) ** 2)) / 1e9)
    return alpha, rmse_GHz, cal_grid_GHz.tolist()


def psa_foe_baseline_strong(rx_rx, fs_rx, alpha):
    """Stronger PSA FOE with finer CFE stage (coarse + fine two-stage).

    Poster content.md L37 describes a finer CFE stage ("scan range can be
    narrowed to directly obtain the Doppler-shift estimate") for B7; the
    same two-stage principle applies to PSA. The coarse stage (alpha*ln-ratio)
    gives a rough estimate; the fine stage searches a narrow window around it
    to minimize the residual log-asymmetry, achieving <<100MHz accuracy
    instead of the coarse stage's ~100MHz floor (which was causing the
    -0.35rad residual phase that wrecked BER, TL-22 finding).

    Returns (rx_compensated, df_est, df_est_fine).
    """
    # Stage 1: coarse CFE (spectral asymmetry, same as psa_foe_baseline)
    rx_comp, df_coarse = psa.psa_foe_asymmetry(rx_rx, fs_rx, alpha, psa.FFT_N)
    # Stage 2: finer CFE — search a narrow window around df_coarse to find
    # the offset that minimizes the residual |log_asymmetry| of the compensated
    # signal. The compensated signal should have ln(P+/P-)/2 ~ 0 when the
    # estimate is exact, so we hunt for the residual offset that zeros it.
    fine_step = 10e6   # 10 MHz finesse (vs coarse ~100MHz floor)
    fine_window = 0.3e9  # +/- 0.3 GHz around coarse (covers coarse err)
    cands = np.arange(df_coarse - fine_window, df_coarse + fine_window, fine_step)
    t = np.arange(rx_rx.size) / fs_rx
    best_df = df_coarse
    best_residual = abs(psa.log_asymmetry(rx_comp, fs_rx))
    for dc in cands:
        rx_try = rx_rx * np.exp(-1j * 2 * np.pi * dc * t)
        res = abs(psa.log_asymmetry(rx_try, fs_rx))
        if res < best_residual:
            best_residual = res
            best_df = dc
    rx_comp_fine = rx_rx * np.exp(-1j * 2 * np.pi * best_df * t)
    return rx_comp_fine, best_df, df_coarse


def psa_foe_two_stage(rx_rx, fs_rx, alpha, coarse_fft=1024, fine_fft=512, M=4):
    """Vieira 2023 two-stage PSA FOE (content.md L343-387).

    Stage 1 coarse CFE: spectral asymmetry alpha*ln(P+/P-)/2 (FFT 1024 sample).
    Stage 2 fine CFE: per-block M-th power FFT (512 sample, M=4 for QPSK),
    each block independently estimates residual FOE and compensates.

    Returns (rx_compensated, df_coarse).
    """
    t = np.arange(rx_rx.size) / fs_rx
    # Stage 1: coarse CFE
    hl = psa.log_asymmetry(rx_rx, fs_rx, coarse_fft)
    df_coarse = alpha * hl
    rx_c = rx_rx * np.exp(-1j * 2 * np.pi * df_coarse * t)
    # Stage 2: fine CFE 分块 M-th power
    n = rx_c.size
    n_blocks = n // fine_fft
    rx_fine = rx_c.copy()
    for blk in range(n_blocks):
        s = slice(blk * fine_fft, (blk + 1) * fine_fft)
        chunk = rx_c[s]
        chunk_m = chunk ** M
        spec = np.abs(np.fft.fft(chunk_m))
        freqs = np.fft.fftfreq(fine_fft, d=1.0 / fs_rx)
        peak = int(np.argmax(spec))
        df_res = freqs[peak] / M
        t_blk = np.arange(fine_fft) / fs_rx + blk * fine_fft / fs_rx
        rx_fine[s] = chunk * np.exp(-1j * 2 * np.pi * df_res * t_blk)
    return rx_fine, df_coarse


# =============================================================================
# Method 4 & 5: classic FOE baselines (4th-power F4.4 + Kay 1989 ML)
# Added as credible BER-gain references: PSA spectral-asymmetry is intrinsically
# weak and inflates B7's BER gain. Classic NDA FOEs give a fairer ceiling.
# =============================================================================
def fourth_power_foe(rx_rx, fs_rx, N_fft=2048, nfft_zp=8192):
    """4th-power FOE (formulas-master.md F4.4, QPSK M=4).

    r4[k] = r[k]^4, R4(f) = FFT{r4 * w_Hann}, f_est = (1/4) * argmax|R4|.
    Range limit: +/- Rs/(2M) = +/- 3.125 GHz at 25GBaud. High precision
    within range. Classic NDA FOE, well-established (Liu 2023, user's
    undergrad code sim_direction_a.py L114-142).

    Returns (rx_compensated, f_est_Hz).
    """
    seg = rx_rx[:N_fft]
    r4 = seg ** 4
    win = np.hanning(N_fft)
    R4 = np.fft.fftshift(np.fft.fft(r4 * win, n=nfft_zp))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft_zp, d=1.0 / fs_rx))
    idx = int(np.argmax(np.abs(R4)))
    # parabolic interpolation for sub-bin accuracy
    if 1 <= idx < len(R4) - 1:
        av, bv, gv = np.abs(R4[idx-1]), np.abs(R4[idx]), np.abs(R4[idx+1])
        if bv - av > 0 and bv + av - 2*gv != 0:
            p = 0.5 * (av - gv) / (av - 2*bv + gv)
        else:
            p = 0.0
    else:
        p = 0.0
    f_est = (freqs[idx] + p * (freqs[1] - freqs[0])) / 4.0
    t = np.arange(rx_rx.size) / fs_rx
    rx_comp = rx_rx * np.exp(-1j * 2 * np.pi * f_est * t)
    return rx_comp, f_est


def kay_foe(rx_rx, fs_rx):
    """Kay 1989 ML frequency estimator (weighted phase-diff average).

    f_est = (1/(2*pi*T)) * sum_k w[k] * angle(y[k]*conj(y[k-1]))
    w[k] = 6*(N-k)*(N-k+1) / (N*(N^2-1))   (ML optimal weights, Kay 1989)

    Theoretically optimal NDA FOE for AWGN. Sensitive to phase wrapping
    at large offsets (range limit ~ +/- Rs/(2*pi) per sample step).
    Reference: Kay, "A Fast and Accurate Single Frequency Estimator,"
    IEEE T-ASSP, 1989.

    Returns (rx_compensated, f_est_Hz).
    """
    n = rx_rx.size
    # phase differences of consecutive samples
    phases = np.angle(rx_rx[1:] * np.conj(rx_rx[:-1]))
    # ML weights w[k] for k=1..N-1 (Kay 1989 Eq. 12)
    k = np.arange(1, n)  # k=1..N-1
    w = 6.0 * (n - k) * (n - k + 1) / (n * (n**2 - 1))
    # weighted average phase -> frequency
    mean_phase = np.sum(w * phases) / np.sum(w)
    T_s = 1.0 / fs_rx
    f_est = mean_phase / (2 * np.pi * T_s)
    t = np.arange(n) / fs_rx
    rx_comp = rx_rx * np.exp(-1j * 2 * np.pi * f_est * t)
    return rx_comp, f_est


# =============================================================================
# BER evaluation (QPSK hard decision, MVE simplified)
# =============================================================================
def qpsk_hard_decision_ber(syms, ref_syms):
    """BER via QPSK hard decision. syms = recovered (post-compensation),
    ref_syms = transmitted QPSK reference.

    Handles two ambiguities automatically:
      1. Symbol-index alignment: TR loop output may be offset from reference
         by a few symbols (loop initialization). Resolved by |.| cross-correlation.
      2. QPSK pi/2 phase rotation: resolved by trying 4 rotations.

    Skips initial transient (first 10% of symbols, TR loop convergence).
    """
    n = min(len(syms), len(ref_syms))
    if n < 40:
        return 0.5
    # find best integer lag via |.| cross-correlation (search small window)
    a = np.abs(syms)
    b = np.abs(ref_syms)
    best_ber = 0.5
    for lag in range(-4, 5):
        if lag >= 0:
            o = syms[lag:lag + min(len(syms) - lag, len(ref_syms))]
            r = ref_syms[:len(o)]
        else:
            r = ref_syms[-lag:-lag + min(len(ref_syms) + lag, len(syms))]
            o = syms[:len(r)]
        if len(o) < 30:
            continue
        skip = max(1, len(o) // 10)
        o, r = o[skip:], r[skip:]
        ref_re = np.real(r) > 0
        ref_im = np.imag(r) > 0
        for rot_idx in range(4):
            rot = np.exp(1j * rot_idx * np.pi / 2)
            s = o * rot
            err = np.sum((np.real(s) > 0) != ref_re) + np.sum((np.imag(s) > 0) != ref_im)
            ber = err / (2 * len(o))
            if ber < best_ber:
                best_ber = ber
    return float(best_ber)


# =============================================================================
# Three-way comparison sweep
# =============================================================================
def run_three_way(n_sym, n_seed, f_d_grid, osnr_list, out_dir):
    """Run B7 / Gardner1986 / PSA three-way comparison over f_D grid x OSNR."""
    t0 = time.time()
    rng_master = np.random.default_rng(0)
    # generate one clean TX, decimate to RX rate, calibrate PSA alpha once
    tx_high, ref_syms_master = make_tx(n_sym, SPS_GEN, ROLL_OFF, rng_master)
    tx_rx_clean, fs_rx = decimate_to_rx(tx_high)
    alpha_psa = calibrate_psa_alpha(tx_rx_clean, fs_rx)
    print(f"[calib] PSA alpha = {alpha_psa/1e9:.3f} GHz "
          f"(Vieira sequential-search proxy, 1GHz 1-point fit)")

    # scan grid for B7 (single-sided 0..DOPPLER_RANGE per content.md L49
    # "scan range is set to 0 GHz-23 GHz"). Bilateral scan across >1 baud
    # period introduces inter-period ambiguity (G(f_D)=K_max|cos(pi*f_D/B)|
    # repeats every 2B), so we keep poster's single-sided grid. The two
    # candidates inside one period come from |cos|'s twin peaks near f=0
    # and f=B (content.md L37 "two Doppler-shift candidates"), resolved by
    # TED2 std.
    scan_grid = np.arange(0, DOPPLER_RANGE + DOPPLER_INTERVAL, DOPPLER_INTERVAL)

    results = {
        "meta": {
            "baud_Hz": BAUD, "roll_off": ROLL_OFF, "sps_gen": SPS_GEN, "sps_rx": SPS_RX,
            "n_sym": n_sym, "n_seed": n_seed, "osnr_list_dB": list(osnr_list),
            "f_d_grid_GHz": [round(f / 1e9, 2) for f in f_d_grid],
            "alpha_psa_GHz": alpha_psa / 1e9,
            "scan_grid_GHz": [round(f / 1e9, 2) for f in scan_grid],
            "source_B7": "content.md L37 (CV multiplier 1 scan + 2 cand + TED2 std)",
            "source_gardner1986": "user Tx2Rx.m L176-214 + PSKTimingErrDetector.m L11-12",
            "source_psa": "Vieira 2023 VI, ./_psa_foe_asymmetry.py (S005 rewrite)",
            "tl20_expectation": "see _fair_comparison_framework.md §5",
        },
        "curves": {},
    }

    for osnr_db in osnr_list:
        cond = "no_noise" if osnr_db is None else f"osnr{osnr_db:.0f}dB"
        print(f"\n=== Condition: {cond} ===")
        cond_rows = []
        for f_d in f_d_grid:
            row = {"f_D_true_GHz": round(f_d / 1e9, 3)}
            ber_b7, ber_g1986, ber_psa = [], [], []
            est_b7, est_psa = [], []
            for seed_i in range(n_seed):
                rng = np.random.default_rng(1000 + seed_i * 17 + int(round(f_d / 1e6)))
                # identical signal + identical Doppler injection across methods.
                # TX symbols are FIXED across seeds (seed 20260707) so BER
                # variations come only from noise realization, not symbol
                # pattern — keeps three-way comparison apples-to-apples.
                tx_high_s, ref_syms = make_tx(n_sym, SPS_GEN, ROLL_OFF,
                                              np.random.default_rng(20260707))
                tx_rx, _ = decimate_to_rx(tx_high_s)
                rx = inject_foe(tx_rx, f_d, fs_rx)
                if osnr_db is not None:
                    rx = add_awgn(rx, osnr_db, BAUD, rng)

                # Method 1: B7 proposed FOE
                f_b7, cands_b7, _ = b7_proposed_foe(rx, fs_rx, scan_grid, lpf2_en=True)
                t_v = np.arange(rx.size) / fs_rx
                rx_comp_b7 = rx * np.exp(-1j * 2 * np.pi * f_b7 * t_v)
                rx_comp_b7 = _lpf2(rx_comp_b7, fs_rx)
                rx_comp_b7, _ = residual_foe_mth_power(rx_comp_b7, fs_rx, M=4)
                out_b7, _ = gardner_1986_tr(rx_comp_b7, fs_rx, return_timing_error=True)
                ber_b7.append(qpsk_hard_decision_ber(out_b7, ref_syms))
                est_b7.append(f_b7)

                # Method 2: Gardner 1986 TR only (no FOE, V3 grandfather)
                # No FOE compensation, no residual cleanup — this is STR only.
                out_g = gardner_1986_tr(rx, fs_rx)
                ber_g1986.append(qpsk_hard_decision_ber(out_g, ref_syms))

                # Method 3: PSA FOE baseline (Vieira 2023 two-stage)
                rx_comp_psa, f_psa = psa_foe_two_stage(rx, fs_rx, alpha_psa)
                rx_comp_psa, _ = residual_foe_mth_power(rx_comp_psa, fs_rx, M=4)
                out_psa, _ = gardner_1986_tr(rx_comp_psa, fs_rx, return_timing_error=True)
                ber_psa.append(qpsk_hard_decision_ber(out_psa, ref_syms))
                est_psa.append(f_psa)

            row["ber_B7_mean"] = float(np.mean(ber_b7))
            row["ber_B7_std"] = float(np.std(ber_b7))
            row["ber_Gardner1986_mean"] = float(np.mean(ber_g1986))
            row["ber_PSA_mean"] = float(np.mean(ber_psa))
            row["f_D_est_B7_GHz"] = round(float(np.mean(est_b7)) / 1e9, 3)
            row["f_D_est_PSA_GHz"] = round(float(np.mean(est_psa)) / 1e9, 3)
            row["foe_err_B7_GHz"] = round(abs(float(np.mean(est_b7)) - f_d) / 1e9, 3)
            row["foe_err_PSA_GHz"] = round(abs(float(np.mean(est_psa)) - f_d) / 1e9, 3)
            # V3 alert metric: B7 vs Gardner1986 BER gap
            row["V3_gap_B7_vs_1986_BER"] = float(row["ber_Gardner1986_mean"] - row["ber_B7_mean"])
            cond_rows.append(row)
            print(f"  f_D={f_d/1e9:>5.1f}GHz | B7 BER={row['ber_B7_mean']:.3e} "
                  f"1986 BER={row['ber_Gardner1986_mean']:.3e} "
                  f"PSA BER={row['ber_PSA_mean']:.3e} | "
                  f"B7 est={row['f_D_est_B7_GHz']:>5.1f} err={row['foe_err_B7_GHz']:.2f} "
                  f"PSA est={row['f_D_est_PSA_GHz']:>5.1f} err={row['foe_err_PSA_GHz']:.2f}")
        results["curves"][cond] = cond_rows

    results["meta"]["elapsed_s"] = round(time.time() - t0, 1)
    out_json = os.path.join(out_dir, "_mve_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[wrote] {out_json}  (elapsed {results['meta']['elapsed_s']}s)")
    _plot_results(results, out_dir)
    return results


# =============================================================================
# Plotting
# =============================================================================
def _plot_results(results, out_dir):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (cond, rows) in zip(axes[0], results["curves"].items()):
        fd = [r["f_D_true_GHz"] for r in rows]
        ax.semilogy(fd, [r["ber_B7_mean"] for r in rows], "o-", ms=4, label="B7 proposed")
        ax.semilogy(fd, [r["ber_Gardner1986_mean"] for r in rows], "s-", ms=4, label="Gardner 1986 TR")
        ax.semilogy(fd, [r["ber_PSA_mean"] for r in rows], "^-", ms=4, label="PSA FOE")
        ax.set_xlabel("true f_D (GHz)")
        ax.set_ylabel("BER")
        ax.set_title(f"{cond} — BER vs Doppler")
        ax.legend(fontsize=8)
        ax.grid(True, which="both", alpha=0.3)
    # FOE estimate accuracy
    for ax, (cond, rows) in zip(axes[1], results["curves"].items()):
        fd = [r["f_D_true_GHz"] for r in rows]
        ax.plot(fd, fd, "k--", lw=1, label="ideal")
        ax.plot(fd, [r["f_D_est_B7_GHz"] for r in rows], "o-", ms=4, label="B7 est")
        ax.plot(fd, [r["f_D_est_PSA_GHz"] for r in rows], "^-", ms=4, label="PSA est")
        ax.set_xlabel("true f_D (GHz)")
        ax.set_ylabel("estimated f_D (GHz)")
        ax.set_title(f"{cond} — FOE estimate")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    fig.suptitle("B7 Gardner-TED FOE three-way MVE "
                 f"({results['meta']['n_sym']} sym x {results['meta']['n_seed']} seed)",
                 fontsize=11)
    fig.tight_layout()
    out_png = os.path.join(out_dir, "_mve_curves.png")
    fig.savefig(out_png, dpi=130)
    print(f"[wrote] {out_png}")


# =============================================================================
# OSNR sweep mode (for BER gain @ BER 2e-2 / HD-FEC quantification)
# =============================================================================
def run_osnr_sweep(n_sym, n_seed, f_d_representative_GHz, osnr_grid_dB, out_dir):
    """Fixed f_D, sweep OSNR -> BER vs OSNR curves -> read off BER gain.

    For each representative f_D, produces BER-vs-OSNR for B7 / Gardner1986 / PSA.
    BER gain @ target_BER = OSNR_PSA(target_BER) - OSNR_B7(target_BER) in dB.
    Targets: BER 2e-2 (poster anchor) + HD-FEC 3.8e-3 (cross-candidate main).

    This complements run_three_way (which fixes OSNR and sweeps f_D): the
    Doppler-sweep MVE proved B7 wins on range + robustness; this OSNR-sweep
    quantifies the BER gain in dB so we can compare against poster's 0.6dB.
    """
    t0 = time.time()
    rng_master = np.random.default_rng(0)
    tx_high, ref_syms_master = make_tx(n_sym, SPS_GEN, ROLL_OFF, rng_master)
    tx_rx_clean, fs_rx = decimate_to_rx(tx_high)
    # Stronger PSA calibration: multi-point sequential-search fit (D006 + S006
    # finding B fix — 1-point fit was producing a weak baseline; this multi-
    # point regression aligns with Vieira 2023's sequential-search procedure).
    # NOTE: a finer-CEF-stage variant was also tried (psa_foe_baseline_strong)
    # but made estimation worse (minimizing residual log-asymmetry is not the
    # same as maximizing accuracy), so the OSNR sweep keeps the multi-point
    # alpha fit + coarse CFE. PSA's residual-phase problem (~1.3rad at 5GHz)
    # is deeper than alpha/stage can fix — it's in the spectral-asymmetry
    # method's FFT-block-averaging phase handling (see S007 finding).
    alpha_psa, alpha_rmse, alpha_calpts = calibrate_psa_alpha_sequential(tx_rx_clean, fs_rx)
    scan_grid = np.arange(0, DOPPLER_RANGE + DOPPLER_INTERVAL, DOPPLER_INTERVAL)
    print(f"[calib] PSA alpha = {alpha_psa/1e9:.3f} GHz "
          f"(sequential-search multi-point fit, {len(alpha_calpts)} pts, "
          f"RMSE={alpha_rmse*1e3:.0f} MHz)")

    results = {
        "meta": {
            "mode": "osnr_sweep",
            "baud_Hz": BAUD, "n_sym": n_sym, "n_seed": n_seed,
            "f_d_GHz": [float(x) for x in f_d_representative_GHz],
            "osnr_grid_dB": [float(x) for x in osnr_grid_dB],
            "alpha_psa_GHz": alpha_psa / 1e9,
            "alpha_psa_method": "sequential-search multi-point fit",
            "alpha_psa_cal_points_GHz": alpha_calpts,
            "alpha_psa_rmse_MHz": alpha_rmse * 1e3,
            "psa_method": "Vieira 2023 two-stage (coarse CFE FFT 1024 + fine CFE M=4 FFT 512)",
            "baselines": ["B7", "Gardner1986", "PSA_two_stage", "4th_power_F4.4", "Kay1989"],
            "targets": {"BER_2e2": 2e-2, "HD_FEC": 3.8e-3},
        },
        "curves": {},
    }

    for f_d_g in f_d_representative_GHz:
        f_d = f_d_g * 1e9
        cond = f"f_D{f_d_g:.0f}GHz"
        print(f"\n=== OSNR sweep at {cond} ===")
        rows = []
        for osnr_db in osnr_grid_dB:
            ber_b7, ber_g1986, ber_psa, ber_4p, ber_kay = [], [], [], [], []
            for seed_i in range(n_seed):
                rng = np.random.default_rng(20000 + seed_i * 31 + int(round(f_d_g * 7)) + int(round(osnr_db * 13)))
                tx_high_s, ref_syms = make_tx(n_sym, SPS_GEN, ROLL_OFF,
                                              np.random.default_rng(20260707))
                tx_rx, _ = decimate_to_rx(tx_high_s)
                rx = inject_foe(tx_rx, f_d, fs_rx)
                rx = add_awgn(rx, osnr_db, BAUD, rng)

                # Method 1: B7 proposed FOE
                f_b7, _, _ = b7_proposed_foe(rx, fs_rx, scan_grid, lpf2_en=True)
                t_v = np.arange(rx.size) / fs_rx
                rx_comp_b7 = rx * np.exp(-1j * 2 * np.pi * f_b7 * t_v)
                rx_comp_b7 = _lpf2(rx_comp_b7, fs_rx)
                rx_comp_b7, _ = residual_foe_mth_power(rx_comp_b7, fs_rx, M=4)
                out_b7, _ = gardner_1986_tr(rx_comp_b7, fs_rx, return_timing_error=True)
                ber_b7.append(qpsk_hard_decision_ber(out_b7, ref_syms))

                # Method 2: Gardner 1986 TR only
                out_g = gardner_1986_tr(rx, fs_rx)
                ber_g1986.append(qpsk_hard_decision_ber(out_g, ref_syms))

                # Method 3: PSA FOE (Vieira 2023 two-stage: coarse CFE + 分块 fine CFE M=4)
                rx_comp_psa, f_psa = psa_foe_two_stage(rx, fs_rx, alpha_psa)
                # whole-block residual cleanup: 分块 fine CFE 量化(24.4MHz/bin)残留
                # ~2MHz 恒定 FOE, 在 4096 sym 块上累积 ~8rad 相位旋转, 必须清掉.
                # 与 B7 路径对称 (B7 也 = b7_proposed_foe + residual_foe_mth_power).
                rx_comp_psa, _ = residual_foe_mth_power(rx_comp_psa, fs_rx, M=4)
                out_psa, _ = gardner_1986_tr(rx_comp_psa, fs_rx, return_timing_error=True)
                ber_psa.append(qpsk_hard_decision_ber(out_psa, ref_syms))

                # Method 4: 4th-power FOE (F4.4, classic NDA)
                rx_comp_4p, f_4p = fourth_power_foe(rx, fs_rx)
                rx_comp_4p, _ = residual_foe_mth_power(rx_comp_4p, fs_rx, M=4)
                out_4p, _ = gardner_1986_tr(rx_comp_4p, fs_rx, return_timing_error=True)
                ber_4p.append(qpsk_hard_decision_ber(out_4p, ref_syms))

                # Method 5: Kay 1989 ML FOE
                rx_comp_kay, f_kay = kay_foe(rx, fs_rx)
                rx_comp_kay, _ = residual_foe_mth_power(rx_comp_kay, fs_rx, M=4)
                out_kay, _ = gardner_1986_tr(rx_comp_kay, fs_rx, return_timing_error=True)
                ber_kay.append(qpsk_hard_decision_ber(out_kay, ref_syms))

            row = {
                "OSNR_dB": float(osnr_db),
                "ber_B7_mean": float(np.mean(ber_b7)),
                "ber_B7_std": float(np.std(ber_b7)),
                "ber_Gardner1986_mean": float(np.mean(ber_g1986)),
                "ber_PSA_mean": float(np.mean(ber_psa)),
                "ber_4thpower_mean": float(np.mean(ber_4p)),
                "ber_Kay_mean": float(np.mean(ber_kay)),
            }
            rows.append(row)
            print(f"  OSNR={osnr_db:>4.0f}dB | B7={row['ber_B7_mean']:.3e} "
                  f"1986={row['ber_Gardner1986_mean']:.3e} "
                  f"PSA={row['ber_PSA_mean']:.3e} "
                  f"4thP={row['ber_4thpower_mean']:.3e} "
                  f"Kay={row['ber_Kay_mean']:.3e}")
        results["curves"][cond] = rows

    # BER gain computation via log-interpolation of BER vs OSNR
    def osnr_at_ber(osnr_arr, ber_arr, target):
        """OSNR at which BER crosses target, via linear interp on log(BER)."""
        lber = np.log10(np.clip(ber_arr, 1e-6, 0.5))
        # monotonic decreasing expected; find first crossing from high BER
        if np.all(ber_arr > target) or np.all(ber_arr < target):
            return None
        for i in range(len(lber) - 1):
            if (lber[i] - np.log10(target)) * (lber[i + 1] - np.log10(target)) <= 0:
                # linear interp on log(BER)
                frac = (np.log10(target) - lber[i]) / (lber[i + 1] - lber[i] + 1e-30)
                return float(osnr_arr[i] + frac * (osnr_arr[i + 1] - osnr_arr[i]))
        return None

    gains = {}
    for cond, rows in results["curves"].items():
        osnr = np.array([r["OSNR_dB"] for r in rows])
        b7 = np.array([r["ber_B7_mean"] for r in rows])
        curves_to_compare = {
            "PSA": np.array([r["ber_PSA_mean"] for r in rows]),
            "4thpower": np.array([r["ber_4thpower_mean"] for r in rows]),
            "Kay": np.array([r["ber_Kay_mean"] for r in rows]),
        }
        cond_gain = {}
        for tgt_name, tgt in [("BER_2e2", 2e-2), ("HD_FEC", 3.8e-3)]:
            osnr_b7 = osnr_at_ber(osnr, b7, tgt)
            tgt_gain = {"OSNR_B7_dB": osnr_b7}
            for bl_name, bl_curve in curves_to_compare.items():
                osnr_bl = osnr_at_ber(osnr, bl_curve, tgt)
                gain_db = (osnr_bl - osnr_b7) if (osnr_b7 is not None and osnr_bl is not None) else None
                tgt_gain[f"OSNR_{bl_name}_dB"] = osnr_bl
                tgt_gain[f"gain_vs_{bl_name}_dB"] = gain_db
            cond_gain[tgt_name] = tgt_gain
        gains[cond] = cond_gain
        # 打印三个 gain
        for tgt_name in ["BER_2e2", "HD_FEC"]:
            g = cond_gain[tgt_name]
            print(f"[gain @ {cond} {tgt_name}] B7@{g['OSNR_B7_dB']}dB | "
                  f"vs PSA={g.get('gain_vs_PSA_dB')} | "
                  f"vs 4th={g.get('gain_vs_4thpower_dB')} | "
                  f"vs Kay={g.get('gain_vs_Kay_dB')}")
    results["gains"] = gains

    results["meta"]["elapsed_s"] = round(time.time() - t0, 1)
    out_json = os.path.join(out_dir, "_mve_osnr_sweep_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[wrote] {out_json}  (elapsed {results['meta']['elapsed_s']}s)")
    _plot_osnr_sweep(results, out_dir)
    return results


def _plot_osnr_sweep(results, out_dir):
    fig, ax = plt.subplots(1, len(results["curves"]), figsize=(5 * len(results["curves"]), 4.5))
    if len(results["curves"]) == 1:
        ax = [ax]
    for a, (cond, rows) in zip(ax, results["curves"].items()):
        osnr = [r["OSNR_dB"] for r in rows]
        a.semilogy(osnr, [r["ber_B7_mean"] for r in rows], "o-", ms=4, label="B7 proposed")
        a.semilogy(osnr, [r["ber_Gardner1986_mean"] for r in rows], "s-", ms=4, label="Gardner 1986 TR")
        a.semilogy(osnr, [r["ber_PSA_mean"] for r in rows], "^-", ms=4, label="PSA FOE")
        a.semilogy(osnr, [r["ber_4thpower_mean"] for r in rows], "D-", ms=4, label="4th-power F4.4")
        a.semilogy(osnr, [r["ber_Kay_mean"] for r in rows], "v-", ms=4, label="Kay 1989")
        a.axhline(2e-2, color="k", ls=":", alpha=0.5, label="BER 2e-2 (anchor)")
        a.axhline(3.8e-3, color="r", ls=":", alpha=0.5, label="HD-FEC 3.8e-3")
        a.set_xlabel("OSNR (dB)")
        a.set_ylabel("BER")
        a.set_title(f"{cond}")
        a.legend(fontsize=7)
        a.grid(True, which="both", alpha=0.3)
    fig.suptitle("B7 OSNR sweep — BER gain quantification", fontsize=11)
    fig.tight_layout()
    out_png = os.path.join(out_dir, "_mve_osnr_sweep_curves.png")
    fig.savefig(out_png, dpi=130)
    print(f"[wrote] {out_png}")


# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="B7 Gardner-TED FOE three-way MVE")
    parser.add_argument("--smoke", action="store_true",
                        help="smoke test: small scale, verify pipeline runs")
    parser.add_argument("--osnr-sweep", action="store_true",
                        help="OSNR sweep mode: fixed representative f_D, sweep OSNR "
                             "to quantify BER gain @ BER 2e-2 and HD-FEC")
    parser.add_argument("--n-sym", type=int, default=N_SYM_DEFAULT)
    parser.add_argument("--n-seed", type=int, default=N_SEED_DEFAULT)
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))

    if args.osnr_sweep:
        print("=" * 70)
        print("OSNR SWEEP MODE (fixed f_D, sweep OSNR, quantify BER gain)")
        print("=" * 70)
        # representative f_D: 5GHz (PSA fair zone) + 12GHz (PSA edge) + 23GHz (B7 edge)
        f_d_repr = [5.0, 12.0, 23.0]
        # OSNR sweep covering BER from ~0.3 (low) down past HD-FEC 3.8e-3 (high).
        # Extended to 35dB because PSA's estimation bias keeps its BER floor high
        # even at 25dB, so we need the high-OSNR tail to reach BER 2e-2 / HD-FEC.
        osnr_grid = np.arange(5, 38, 3)   # 5..35 dB step 3dB, ~11 points
        run_osnr_sweep(args.n_sym, args.n_seed, f_d_repr, osnr_grid, here)
        return

    if args.smoke:
        print("=" * 70)
        print("SMOKE TEST MODE (small scale, verify pipeline)")
        print("=" * 70)
        n_sym, n_seed = 4096, 1
        f_d_grid = np.array([0, 5, 12, 15, 23]) * 1e9
        osnr_list = [OSNR_MAIN]
    else:
        n_sym, n_seed = args.n_sym, args.n_seed
        f_d_grid = F_D_GRID_DEFAULT
        osnr_list = [None, OSNR_MAIN, OSNR_LOW]

    run_three_way(n_sym, n_seed, f_d_grid, osnr_list, here)


if __name__ == "__main__":
    main()
