# -*- coding: utf-8 -*-
"""P07-R — CORRECTED analog front-end AGC + gain-aware I/Q ADC (family F repair).

Fixes the three root causes reproduced in `p07r_prefail_evidence.json`
(D046 / V072 PART 1):

  H1 SCALE  : the receiver consumes q/g_t (NOT q). The analog gain g_t is a
              receiver-known control (decided from past), not an oracle. After
              ADC, q = Q(g_t * z); the receiver input is q / g_t so that the
              original signal & noise scale is restored. Quantization step and
              clip threshold fold back to the input as step/g_t and FS/g_t.
              `quantize_iq_gainaware` returns (rx_in=q/g, codes, rails, g) and
              guarantees the gain->de-gain identity: with no clip & no quant,
              rx_in == z to float precision for ANY g.

  H2 CONTROL: the causal AGCs use the correct INCREMENTAL form
              g_next = clip(g_current * target_scale / measured_output_scale, ...)
              (not g_next = target/measured_output_scale, which drops g_current).

  H3 LIFECYCLE is handled by the runner/trajectory generator (p07r_runner.py),
              not here. This module only provides scale/correctness primitives.

FOUR-WAY PHYSICAL DECOMPOSITION primitives (task section VI):
  - scale_only : apply g then divide by g, NO clip, NO quant  (must == ideal float)
  - clip_only  : apply g, rail-clip, divide by g, NO quant rounding
  - quant_only : apply g, NO clip (wide rails), quant rounding, divide by g
  - full_adc   : apply g, rail-clip, quant rounding, divide by g  (production)

Info-boundary (AST-audited downstream): every decide_gain body consumes ONLY
past quantized samples / rail-hit flags / receiver-visible running stats.
Forbidden substrings in AGC bodies: h, alpha, beta, tx, phi, bits, true, oracle,
future. (quantize_* primitives DO reference gain/fs/W only, never channel truth.)

DISTINCT FROM P03: P03 = selector-internal fixed-point Q(W,F) on the control
path; P07-R = analog front-end variable gain + ADC full-scale/clipping/
quantization on rx_raw BEFORE the frozen receiver chain.
"""
import numpy as np


# ============================================================================
# Core gain-aware ADC primitives (H1 SCALE fix)
# ============================================================================

def _adc_core(value, gain, fs, W):
    """Signed saturating round-half-up ADC on a REAL array.

    code = clip(floor(gain*value/step + 0.5), -2^(W-1), 2^(W-1)-1)
    step = 2*fs / 2^W. Saturation clips (never wraps).
    Returns (code_int64, rail_bool).
    """
    step = 2.0 * fs / (2 ** W)
    half = 2 ** (W - 1)
    x = gain * value
    rail = (x >= fs) | (x <= -fs)
    x = np.clip(x, -fs, fs)
    code = np.floor(x / step + 0.5).astype(np.int64)
    code = np.clip(code, -half, half - 1)   # saturate, never wrap
    return code, rail, step


def quantize_iq_gainaware(z, gain, fs, W):
    """Gain-aware ADC: returns the RECEIVER-INPUT = q/g (scale restored).

    Pipeline: y = gain*z -> rail clip +-fs -> quantize -> q=code*step -> rx_in=q/gain.

    This is the H1 SCALE fix: the downstream receiver sees rx_in whose signal
    & noise scale equals z (up to quantization error /step and clip saturation
    folded back as FS/gain). gain is a receiver-known control, NOT an oracle.

    Returns
    -------
    rx_in : complex ndarray   (q/gain) -- feed THIS to the frozen receiver
    code_r, code_i : int ndarray   held signed codes (audit)
    rail_r, rail_i : bool ndarray  saturation flags (receiver-visible state)
    step : float               quantization step (= 2*fs/2^W)
    """
    if fs <= 0:
        raise ValueError(f"fs must be > 0, got {fs}")
    if W < 2:
        raise ValueError(f"W must be >= 2, got {W}")
    if gain == 0:
        raise ValueError("gain must be != 0 (receiver must know its own gain)")
    cr, rr, step = _adc_core(np.real(z), gain, fs, W)
    ci, ri, _ = _adc_core(np.imag(z), gain, fs, W)
    q = cr.astype(np.float64) * step + 1j * (ci.astype(np.float64) * step)
    rx_in = q / gain
    return rx_in, cr, ci, rr, ri, float(step)


# ---- four-way physical decomposition primitives ----------------------------

def decomp_scale_only(z, gain):
    """Apply gain then divide by gain, no clip, no quant.

    MUST be the identity (== z) up to float round-off for ANY gain. This is the
    control arm that isolates the clipping+quantization impairment from the
    scale bookkeeping. Returns rx_in (= z) and empty rails.
    """
    rx_in = (gain * z) / gain
    n = z.size
    return rx_in, np.zeros(n, bool), np.zeros(n, bool), 0.0


def decomp_clip_only(z, gain, fs):
    """Apply gain, rail-clip +-fs, divide by gain, NO quant rounding.

    Isolates clipping. rx_in = clip(gain*z, +-fs)/gain. Returns rails.
    """
    xr = np.clip(gain * np.real(z), -fs, fs) / gain
    xi = np.clip(gain * np.imag(z), -fs, fs) / gain
    rr = (gain * np.real(z) >= fs) | (gain * np.real(z) <= -fs)
    ri = (gain * np.imag(z) >= fs) | (gain * np.imag(z) <= -fs)
    return xr + 1j * xi, rr, ri, 0.0


def decomp_quant_only(z, gain, fs, W):
    """Apply gain, quantize (wide rails to exclude clipping), divide by gain.

    Uses a LARGE fs so the rail clip never fires (clipping excluded); isolates
    quantization rounding. step = 2*fs/2^W still controls resolution. Rail flags
    returned for completeness but should be all-False with wide fs.
    """
    rx_in, cr, ci, rr, ri, step = quantize_iq_gainaware(z, gain, fs, W)
    return rx_in, rr, ri, step


def decomp_full_adc(z, gain, fs, W):
    """Full ADC: apply gain, rail-clip, quantize, divide by gain (production)."""
    return quantize_iq_gainaware(z, gain, fs, W)


DECOMPOSITIONS = {
    "scale_only": decomp_scale_only,
    "clip_only": decomp_clip_only,
    "quant_only": decomp_quant_only,
    "full_adc": decomp_full_adc,
}


# ============================================================================
# Causal gain decision API (H2 CONTROL fix: incremental form)
# ----------------------------------------------------------------------------
# Every AGC is stateful:
#   .reset()                 window-0 nominal
#   .update(rxq_past_in)     observe past RECEIVER-INPUT window (q/g, causal)
#   .gain_for_next()         gain to apply to NEXT window
#   .state_summary()
# gain for window b decided ONLY from windows < b. gain clamped to [g_min,g_max].
#
# CORRECT INCREMENTAL FORM (H2 fix):
#   rms(q_past) = g_current * rms(z)   (q_past is the past RECEIVER INPUT q/g,
#                                       whose scale == z scale already!)
# Actually since update() receives rxq_past_in = q/g (scale already restored),
# rms(rxq_past_in) ~ rms(z) directly. The correct gain update is therefore:
#   g_next = clip(target_rms / rms(rxq_past_in), g_min, g_max)
# which is scale-consistent: it targets the INPUT rms (z scale), and the
# measured quantity is already in the input scale because we feed q/g not q.
#
# NOTE on the old bug: the OLD chain fed q (not q/g) and used
# g_next = target/rms(q), which equals target/(g_current*rms(z)) -- a quantity
# that depends on g_current but drops its multiplicative role. With q/g fed,
# target/rms(q/g) == target/rms(z) is the correct, g_current-independent target.
# We keep an explicit incremental option (mult update_factor) for the
# attack-release controller where the update is a fractional step toward target.
# ============================================================================

NOMINAL_GAIN = 1.0
TARGET_RMS = 0.3          # target per-I/Q RMS in FS units (a priori)
GAIN_MIN = 0.125          # frozen AGC gain bounds (8x range)
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

    def update(self, rxq_past_in):
        """Observe a PAST receiver-input window (q/g, scale restored). Causal."""
        self._n_seen += 1

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
        self._gain = float(gain)

    def update(self, rxq_past_in):
        self._n_seen += 1


class CausalRMSAGC(_BaseAGC):
    """CORRECTED conventional comparator: causal running-RMS AGC.

    H2 fix: update() receives rxq_past_in = q/g (receiver input, scale restored
    to z), so rms(rxq_past_in) ~ rms(z) directly. The gain targets the INPUT
    scale: g_next = clip(target_rms / rms(rxq_past_in), g_min, g_max).
    This is scale-consistent (g_current-independent) because the measurement is
    already in input scale.

    Optional incremental smoothing: g_next = clip((1-blend)*g_current +
    blend*target/rms, ...) for attack/release behaviour. blend=1 reproduces the
    pure target/rms form.
    """
    name = "causal_rms"

    def __init__(self, target_rms=TARGET_RMS, lam=0.9, blend=1.0, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.lam = float(lam)
        self.blend = float(blend)
        self._pwr_ema = None

    def update(self, rxq_past_in):
        self._n_seen += 1
        # per-I/Q power of past RECEIVER-INPUT window (scale == z)
        pwr = (np.mean(np.real(rxq_past_in) ** 2) + np.mean(np.imag(rxq_past_in) ** 2)) / 2.0
        if self._pwr_ema is None:
            self._pwr_ema = float(pwr)
        else:
            self._pwr_ema = self.lam * self._pwr_ema + (1.0 - self.lam) * float(pwr)
        rms = np.sqrt(max(self._pwr_ema, 1e-12))
        target_gain = self.target_rms / rms            # input-scale target
        # incremental blend toward target (blend=1 == pure target/rms)
        self._gain = self._clamp((1.0 - self.blend) * self._gain + self.blend * target_gain)
        self._updates += 1


class AttackReleaseAGC(_BaseAGC):
    """CORRECTED peak-hold / attack-release AGC.

    Tracks peak |sample| of past receiver-input windows with asymmetric
    forgetting (fast attack on increasing peak, slow release on fade).
    g_next = clip(target_peak / peak, ...). peak measured in INPUT scale (q/g).
    """
    name = "attack_release"

    def __init__(self, target_peak=0.8, attack=0.5, release=0.95, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_peak = float(target_peak)
        self.attack = float(attack)
        self.release = float(release)
        self._peak = None

    def update(self, rxq_past_in):
        self._n_seen += 1
        cur_peak = float(np.max(np.abs(rxq_past_in))) if rxq_past_in.size else 0.0
        if self._peak is None:
            self._peak = cur_peak
        else:
            lam = self.attack if cur_peak > self._peak else self.release
            self._peak = lam * self._peak + (1.0 - lam) * cur_peak
            self._peak = max(self._peak, cur_peak)   # attack holds the peak up
        denom = max(self._peak, 1e-12)
        self._gain = self._clamp(self.target_peak / denom)
        self._updates += 1


class LogDomainAGC(_BaseAGC):
    """CORRECTED log-domain AGC (gain in dB EMA), input-scale measurement."""
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

    def update(self, rxq_past_in):
        self._n_seen += 1
        pwr = (np.mean(np.real(rxq_past_in) ** 2) + np.mean(np.imag(rxq_past_in) ** 2)) / 2.0
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
# Phase C method-factory candidates (mechanism-distinct; gain-aware)
# ============================================================================

class CensoredMomentAGC(_BaseAGC):
    """C1: censored-moment AGC.

    Estimates input scale from UNCLIPPED (censored) samples only, using the
    rail-hit flags to exclude saturated samples, plus the rail fraction to
    infer the tail. When many samples clip, the unclipped-moment underestimates
    the true scale; this controller corrects via the observed rail fraction.
    """
    name = "censored_moment"

    def __init__(self, target_rms=TARGET_RMS, lam=0.9, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_rms = float(target_rms)
        self.lam = float(lam)
        self._pwr_ema = None
        self._rail_frac_ema = None

    def update(self, rxq_past_in, rail_past=None):
        self._n_seen += 1
        rr = rail_past[0] if isinstance(rail_past, tuple) else (
            rail_past if rail_past is not None else np.zeros(rxq_past_in.size, bool))
        ri = rail_past[1] if isinstance(rail_past, tuple) else (
            rail_past if rail_past is not None else np.zeros(rxq_past_in.size, bool))
        rail_any = rr | ri
        rail_frac = float(np.mean(rail_any)) if rail_any.size else 0.0
        # censored: use only unclipped samples for the moment
        keep = ~rail_any
        if np.any(keep):
            s = rxq_past_in[keep]
            pwr = (np.mean(np.real(s) ** 2) + np.mean(np.imag(s) ** 2)) / 2.0
        else:
            pwr = (np.mean(np.real(rxq_past_in) ** 2) + np.mean(np.imag(rxq_past_in) ** 2)) / 2.0
        if self._pwr_ema is None:
            self._pwr_ema = float(pwr)
            self._rail_frac_ema = rail_frac
        else:
            self._pwr_ema = self.lam * self._pwr_ema + (1.0 - self.lam) * float(pwr)
            self._rail_frac_ema = self.lam * self._rail_frac_ema + (1.0 - self.lam) * rail_frac
        rms = np.sqrt(max(self._pwr_ema, 1e-12))
        # inflate target when rail fraction high (censored moment underestimates)
        inflation = 1.0 + 2.0 * max(self._rail_frac_ema, 0.0)
        self._gain = self._clamp(self.target_rms * inflation / rms)
        self._updates += 1


class UpperQuantileAGC(_BaseAGC):
    """C2: streaming upper-quantile / target-clipping-probability controller.

    Controls the tail probability (fraction of samples near the rail) instead
    of RMS. Drives gain so a target quantile of |sample| sits at a set fraction
    of FS -- a clipping-probability objective, mechanism-distinct from RMS.
    """
    name = "upper_quantile"

    def __init__(self, target_quantile=0.99, target_frac_fs=0.8, lam=0.9, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.target_quantile = float(target_quantile)
        self.target_frac_fs = float(target_frac_fs)
        self.lam = float(lam)
        self._q_ema = None

    def update(self, rxq_past_in):
        self._n_seen += 1
        mag = np.abs(rxq_past_in)
        cur_q = float(np.percentile(mag, self.target_quantile * 100.0)) if mag.size else 1e-12
        if self._q_ema is None:
            self._q_ema = cur_q
        else:
            self._q_ema = self.lam * self._q_ema + (1.0 - self.lam) * cur_q
        denom = max(self._q_ema, 1e-12)
        self._gain = self._clamp(self.target_frac_fs * self.fs / denom)
        self._updates += 1


class TwoRangePGA(_BaseAGC):
    """C3: two-range PGA / ADC range switching with hysteresis.

    Discrete gain bands (high/low) with hysteresis: switch to low band when
    past upper-quantile is high for `hyst_lo` windows; switch to high band when
    low for `hyst_hi` windows. A discrete range-switching policy, distinct from
    continuous RMS tracking.
    """
    name = "two_range_pga"

    def __init__(self, high_gain=2.0, low_gain=0.5,
                 q_hi=0.5, q_lo=0.2, quantile=0.9, hyst_lo=2, hyst_hi=2, fs=FS,
                 gain_min=GAIN_MIN, gain_max=GAIN_MAX, nominal=NOMINAL_GAIN):
        super().__init__(gain_min=gain_min, gain_max=gain_max, fs=fs, nominal=nominal)
        self.high_gain = float(high_gain)
        self.low_gain = float(low_gain)
        self.q_hi = float(q_hi)
        self.q_lo = float(q_lo)
        self.quantile = float(quantile)
        self.hyst_lo = int(hyst_lo)
        self.hyst_hi = int(hyst_hi)
        self._band = "high"
        self._cnt_hi = 0
        self._cnt_lo = 0

    def update(self, rxq_past_in):
        self._n_seen += 1
        mag = np.abs(rxq_past_in)
        cur_q = float(np.percentile(mag, self.quantile * 100.0)) if mag.size else 0.0
        if cur_q >= self.q_hi:
            self._cnt_hi += 1; self._cnt_lo = 0
        elif cur_q <= self.q_lo:
            self._cnt_lo += 1; self._cnt_hi = 0
        else:
            self._cnt_hi = 0; self._cnt_lo = 0
        if self._band == "high" and self._cnt_hi >= self.hyst_lo:
            self._band = "low"; self._cnt_hi = 0
        elif self._band == "low" and self._cnt_lo >= self.hyst_hi:
            self._band = "high"; self._cnt_lo = 0
        self._gain = self._clamp(self.high_gain if self._band == "high" else self.low_gain)
        self._updates += 1


# ============================================================================
# Registries
# ============================================================================

FIXED_GAIN_LADDER = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0)
BITWIDTHS = (6, 8, 10)
FLOAT_BYPASS_W = 64
FLOAT_BYPASS_FS = 1e6

CONVENTIONAL_AGCS = {
    "causal_rms": CausalRMSAGC,
    "attack_release": AttackReleaseAGC,
    "log_domain": LogDomainAGC,
}
CANDIDATE_AGCS = {
    "censored_moment": CensoredMomentAGC,
    "upper_quantile": UpperQuantileAGC,
    "two_range_pga": TwoRangePGA,
}
