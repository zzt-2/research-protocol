# -*- coding: utf-8 -*-
"""P07 — analog front-end AGC + I/Q ADC adapter family (family F).

Signal chain (FROZEN in FROZEN_CONTRACT.md §3):
    channel float rx_raw
      -> gain (decided from PAST quantized samples / rail-hit flags /
               receiver-visible stats ONLY)
      -> I/Q rail clip to +/- FS
      -> finite-bitwidth uniform signed I/Q ADC
      -> quantized raw
      -> frozen receiver chain (unchanged)

DISTINCT FROM P03:
    P03 = selector-internal fixed-point Q(W,F) on the CONTROL PATH (digital
    post-processing of the selector's statistics).
    P07 = analog front-end variable gain + ADC full-scale/clipping/quantization
    on rx_raw BEFORE the frozen receiver chain consumes it.

Info-boundary (AST-audited): every decide_gain body consumes ONLY past
quantized samples / rail-hit flags / receiver-visible running stats.
Forbidden substrings: h, alpha, beta, tx, phi, bits, true, oracle, future.

No np.round(decimals=) fake quantization: explicit integer codes, round-half-up,
saturating (never wraps).
"""
import numpy as np


# ============================================================================
# Core ADC: signed I/Q quantizer (saturating two's-complement, round-half-up)
# ============================================================================

def quantize_iq(z, gain, fs, W):
    """Apply analog gain, clip to +/- fs rails, then uniform signed I/Q ADC.

    Parameters
    ----------
    z : complex ndarray
        Float complex I/Q samples (rx_raw).
    gain : float
        Analog gain applied before clipping/ADC (>= 0).
    fs : float
        Full-scale voltage (rails at +/- fs). Must be > 0.
    W : int
        ADC bit width. W=64 with large fs == float-bypass (reconstruction err
        <= 2^-W + rounding). step = 2*fs / 2^W.

    Returns
    -------
    q : complex ndarray
        Reconstructed quantized samples (q = code * step), real & imag each
        clipped to +/- fs.
    code_r, code_i : int ndarray
        Held signed integer codes in [-2^(W-1), 2^(W-1)-1].
    rail_r, rail_i : bool ndarray
        True where the pre-ADC value hit the +/- fs rail (saturation).

    Notes
    -----
    Round-half-up (ties -> +inf): floor(x*2^(W-1)/fs + 0.5). Saturation clips
    (does NOT wrap). The reconstruction uses the SAME step so that
    gain=1, fs=large, W=64 reconstructs the input to <= 2^-W error (float-bypass).
    """
    if fs <= 0:
        raise ValueError(f"fs must be > 0, got {fs}")
    if W < 2:
        raise ValueError(f"W must be >= 2, got {W}")
    step = 2.0 * fs / (2 ** W)
    half = 2 ** (W - 1)               # e.g. W=8 -> 128
    def _adc(v):
        x = gain * v
        rail = (x >= fs) | (x <= -fs)
        x = np.clip(x, -fs, fs)
        # round-half-up: +0.5 then floor
        code = np.floor(x / step + 0.5).astype(np.int64)
        code = np.clip(code, -(half), half - 1)   # saturate, never wrap
        q = code.astype(np.float64) * step
        return q, code, rail
    qr, cr, rr = _adc(np.real(z))
    qi, ci, ri = _adc(np.imag(z))
    return (qr + 1j * qi), cr, ci, rr, ri


def adc_reconstruct_lossless(z_float, gain, fs, W):
    """Float-bypass helper: returns reconstruction max abs error vs z_float."""
    q = quantize_iq(z_float, gain, fs, W)[0]
    return float(np.max(np.abs(q - z_float))) if z_float.size else 0.0


# ============================================================================
# Causal gain decision API
# ----------------------------------------------------------------------------
# Every AGC is a stateful object with:
#   .reset()                         -> reset internal state (window-0 nominal)
#   .update(rxq_past)                -> observe past quantized window (causal)
#   .gain_for_next()                 -> return the gain to apply to NEXT window
#   .state_summary()                 -> dict for provenance / audit
# gain for window b is decided ONLY from windows < b. Window 0 uses the
# nominal gain (no past). gain is clamped to [gain_min, gain_max].
# ============================================================================

NOMINAL_GAIN = 1.0
TARGET_RMS = 0.3          # target per-I/Q RMS in FS units (a priori, ~ unit power/4)
GAIN_MIN = 0.125          # frozen AGC gain bounds (a priori, 8x range)
GAIN_MAX = 8.0
FS = 1.0                  # frozen full-scale (unit-power normalized rails)


class _BaseAGC:
    """Common base: gain clamp + nominal + state log for audit."""
    name = "base"

    def __init__(self, gain_min=GAIN_MIN, gain_max=GAIN_MAX, fs=FS, nominal=NOMINAL_GAIN):
        self.gain_min = float(gain_min)
        self.gain_max = float(gain_max)
        self.fs = float(fs)
        self.nominal = float(nominal)
        self._gain = float(nominal)
        self._n_seen = 0
        self._updates = 0

    def reset(self):
        self._gain = float(self.nominal)
        self._n_seen = 0
        self._updates = 0

    def _clamp(self, g):
        return float(min(self.gain_max, max(self.gain_min, g)))

    def update(self, rxq_past):
        """Observe a PAST quantized window. Override in subclasses."""
        self._n_seen += 1
        # base: no change (keeps nominal)

    def gain_for_next(self):
        return self._gain

    def state_summary(self):
        return {"name": self.name, "gain": self._gain, "n_seen": self._n_seen,
                "updates": self._updates,
                "gain_min": self.gain_min, "gain_max": self.gain_max,
                "fs": self.fs, "nominal": self.nominal}


class FixedGainAGC(_BaseAGC):
    """Fixed (no-op) gain. gain == nominal throughout. Comparator baseline."""
    name = "fixed"

    def __init__(self, gain=NOMINAL_GAIN, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=gain)
        self._gain = float(gain)   # nominal IS the fixed gain

    def update(self, rxq_past):
        self._n_seen += 1   # observe but do not change


class CausalRMSAGC(_BaseAGC):
    """Conventional comparator: causal running-RMS AGC with forgetting factor.

    gain_b = clamp(target_rms / sqrt(EMA(past per-I/Q power)), g_min, g_max)
    Decided from PAST quantized windows only.
    """
    name = "causal_rms"

    def __init__(self, target_rms=TARGET_RMS, lam=0.9, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.lam = float(lam)
        self._pwr_ema = None  # None until first past window seen

    def update(self, rxq_past):
        self._n_seen += 1
        # per-I/Q power of past quantized window
        pwr = (np.mean(np.real(rxq_past) ** 2) + np.mean(np.imag(rxq_past) ** 2)) / 2.0
        if self._pwr_ema is None:
            self._pwr_ema = float(pwr)
        else:
            self._pwr_ema = self.lam * self._pwr_ema + (1.0 - self.lam) * float(pwr)
        rms = np.sqrt(max(self._pwr_ema, 1e-12))
        self._gain = self._clamp(self.target_rms / rms)
        self._updates += 1


class PeakHoldAGC(_BaseAGC):
    """Conventional comparator: peak-hold / attack-release AGC.

    Tracks the max |sample| of past quantized windows with exponential
    decay (release). gain_b = clamp(target_peak / decay_peak, ...). Fast on
    peaks (the peak updates up immediately), slow on fades (release decay).
    """
    name = "peak_hold"

    def __init__(self, target_peak=0.8, release=0.95, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_peak = float(target_peak)
        self.release = float(release)
        self._peak = None

    def update(self, rxq_past):
        self._n_seen += 1
        cur_peak = float(np.max(np.abs(rxq_past))) if rxq_past.size else 0.0
        if self._peak is None:
            self._peak = cur_peak
        else:
            held = self.release * self._peak          # release (decay)
            self._peak = max(held, cur_peak)          # attack (immediate up)
        denom = max(self._peak, 1e-12)
        self._gain = self._clamp(self.target_peak / denom)
        self._updates += 1


class LogDomainAGC(_BaseAGC):
    """Conventional comparator 3: log-domain AGC (gain in dB EMA).

    gain_dB_b = clamp(target_dB - EMA(20log10(rms_past)), dB_min, dB_max).
    Operates in dB so symmetric in attack/release, avoids multiplicative skew.
    """
    name = "log_domain"

    def __init__(self, target_rms=TARGET_RMS, lam=0.9, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.target_dB = 20.0 * np.log10(self.target_rms)
        self.lam = float(lam)
        self.gain_min_dB = 20.0 * np.log10(self.gain_min)
        self.gain_max_dB = 20.0 * np.log10(self.gain_max)
        self._rms_dB_ema = None

    def _clamp_dB(self, g_dB):
        return float(min(self.gain_max_dB, max(self.gain_min_dB, g_dB)))

    def update(self, rxq_past):
        self._n_seen += 1
        pwr = (np.mean(np.real(rxq_past) ** 2) + np.mean(np.imag(rxq_past) ** 2)) / 2.0
        rms = np.sqrt(max(pwr, 1e-12))
        rms_dB = 20.0 * np.log10(rms)
        if self._rms_dB_ema is None:
            self._rms_dB_ema = rms_dB
        else:
            self._rms_dB_ema = self.lam * self._rms_dB_ema + (1.0 - self.lam) * rms_dB
        g_dB = self._clamp_dB(self.target_dB - self._rms_dB_ema)
        self._gain = float(10.0 ** (g_dB / 20.0))
        self._updates += 1


# ============================================================================
# Phase C method-factory candidates (mechanism-distinct deployable actions)
# ============================================================================

class DualTimeConstantAGC(_BaseAGC):
    """M1: dual-time-constant attack/release.

    RMS estimate with TWO forgetting factors: fast lam_attack when the past
    window RMS INCREASED (peak coming), slow lam_release when it decreased
    (fade). Captures asymmetric clipping-vs-resolution urgency.
    """
    name = "dual_tc"

    def __init__(self, target_rms=TARGET_RMS,
                 lam_attack=0.5, lam_release=0.97, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.lam_attack = float(lam_attack)
        self.lam_release = float(lam_release)
        self._pwr_ema = None
        self._prev_rms = None

    def update(self, rxq_past):
        self._n_seen += 1
        pwr = (np.mean(np.real(rxq_past) ** 2) + np.mean(np.imag(rxq_past) ** 2)) / 2.0
        if self._pwr_ema is None:
            self._pwr_ema = float(pwr)
            self._prev_rms = np.sqrt(max(self._pwr_ema, 1e-12))
        else:
            cur_rms = np.sqrt(max(float(pwr), 1e-12))
            lam = self.lam_attack if cur_rms > self._prev_rms else self.lam_release
            self._pwr_ema = lam * self._pwr_ema + (1.0 - lam) * float(pwr)
            self._prev_rms = cur_rms
        rms = np.sqrt(max(self._pwr_ema, 1e-12))
        self._gain = self._clamp(self.target_rms / rms)
        self._updates += 1


class ClippingAwareAGC(_BaseAGC):
    """M2: clipping-aware anti-windup.

    Uses the rail-hit flag of the PAST quantized window: if a burst of
    rail-hits occurred, immediately back the gain off (anti-windup) regardless
    of RMS. Otherwise tracks RMS like causal-RMS. Decided from past rail-hit
    flags only (receiver-visible).
    """
    name = "clipping_aware"

    def __init__(self, target_rms=TARGET_RMS, lam=0.9,
                 rail_frac_thresh=0.05, backoff=0.7, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.lam = float(lam)
        self.rail_frac_thresh = float(rail_frac_thresh)
        self.backoff = float(backoff)
        self._pwr_ema = None

    def update(self, rxq_past, rail_past=None):
        """rail_past: bool ndarray of rail hits in the past window (optional)."""
        self._n_seen += 1
        pwr = (np.mean(np.real(rxq_past) ** 2) + np.mean(np.imag(rxq_past) ** 2)) / 2.0
        if self._pwr_ema is None:
            self._pwr_ema = float(pwr)
        else:
            self._pwr_ema = self.lam * self._pwr_ema + (1.0 - self.lam) * float(pwr)
        rms = np.sqrt(max(self._pwr_ema, 1e-12))
        gain_rms = self.target_rms / rms
        # anti-windup: if rail-hit fraction exceeds threshold, back off
        if rail_past is not None and rail_past.size:
            rail_frac = float(np.mean(rail_past))
            if rail_frac > self.rail_frac_thresh:
                gain_rms = gain_rms * self.backoff
        self._gain = self._clamp(gain_rms)
        self._updates += 1


class RobustPercentileAGC(_BaseAGC):
    """M3: robust Huber/percentile amplitude estimator.

    Instead of RMS (sensitive to the clipped/fade tails), use the 75th
    percentile of |sample| over a causal window as the scale estimate.
    Resists the heavy GG tails that RMS over-weights.
    """
    name = "robust_pct"

    def __init__(self, target_pct=0.3, percentile=75, lam=0.9, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_pct = float(target_pct)
        self.percentile = float(percentile)
        self.lam = float(lam)
        self._pct_ema = None

    def update(self, rxq_past):
        self._n_seen += 1
        mag = np.abs(rxq_past)
        cur_pct = float(np.percentile(mag, self.percentile)) if mag.size else 1e-12
        if self._pct_ema is None:
            self._pct_ema = cur_pct
        else:
            self._pct_ema = self.lam * self._pct_ema + (1.0 - self.lam) * cur_pct
        denom = max(self._pct_ema, 1e-12)
        self._gain = self._clamp(self.target_pct / denom)
        self._updates += 1


class HystereticTwoRangeAGC(_BaseAGC):
    """M4: hysteretic two-range gain.

    Maintains a high/low gain band with hysteresis: when past RMS is high for
    `hyst_lo` consecutive windows, switch to the low-gain band; when low for
    `hyst_hi` consecutive windows, switch to the high-gain band. Different
    mechanism from continuous RMS tracking — a discrete band-switching policy.
    """
    name = "hysteretic"

    def __init__(self, high_gain=2.0, low_gain=0.5,
                 rms_hi=0.4, rms_lo=0.2, hyst_lo=2, hyst_hi=2, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.high_gain = float(high_gain)
        self.low_gain = float(low_gain)
        self.rms_hi = float(rms_hi)
        self.rms_lo = float(rms_lo)
        self.hyst_lo = int(hyst_lo)
        self.hyst_hi = int(hyst_hi)
        self._band = "high"          # start in high-gain band (room for peaks)
        self._cnt_hi = 0             # consecutive high-RMS windows
        self._cnt_lo = 0             # consecutive low-RMS windows

    def update(self, rxq_past):
        self._n_seen += 1
        pwr = (np.mean(np.real(rxq_past) ** 2) + np.mean(np.imag(rxq_past) ** 2)) / 2.0
        rms = float(np.sqrt(max(pwr, 1e-12)))
        if rms >= self.rms_hi:
            self._cnt_hi += 1
            self._cnt_lo = 0
        elif rms <= self.rms_lo:
            self._cnt_lo += 1
            self._cnt_hi = 0
        else:
            self._cnt_hi = 0
            self._cnt_lo = 0
        # band transitions with hysteresis
        if self._band == "high" and self._cnt_hi >= self.hyst_lo:
            self._band = "low"
            self._cnt_hi = 0
        elif self._band == "low" and self._cnt_lo >= self.hyst_hi:
            self._band = "high"
            self._cnt_lo = 0
        self._gain = self.high_gain if self._band == "high" else self.low_gain
        self._gain = self._clamp(self._gain)
        self._updates += 1


# ============================================================================
# Pre-registered candidate factory registry
# ============================================================================

# Fixed-gain ladder (FROZEN a priori in FROZEN_CONTRACT §4; brackets typical
# |rx| swing, NOT cherry-picked to manufacture method benefit).
FIXED_GAIN_LADDER = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0)
BITWIDTHS = (6, 8, 10)
FLOAT_BYPASS_W = 64
FLOAT_BYPASS_FS = 1e6     # large enough that step << signal; float-bypass

CONVENTIONAL_AGCS = {
    "causal_rms": CausalRMSAGC,
    "peak_hold": PeakHoldAGC,
    "log_domain": LogDomainAGC,
}

CANDIDATE_AGCS = {
    "dual_tc": DualTimeConstantAGC,
    "clipping_aware": ClippingAwareAGC,
    "robust_pct": RobustPercentileAGC,
    "hysteretic": HystereticTwoRangeAGC,
}
