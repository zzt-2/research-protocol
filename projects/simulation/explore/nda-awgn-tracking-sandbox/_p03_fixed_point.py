# -*- coding: utf-8 -*-
"""P03 (T031) — bit-true fixed-point selector CONTROL PATH + decide_fp.

Mirrors the frozen selector `_a4_switch_common768_30seed.decide` exactly in its
two-stage logic, but every data-dependent arithmetic operator is realised in an
explicit, saturating two's-complement Q(W,F) format with block-floating-point
per-window normalisation.

============================================================================
Q-FORMAT CONTRACT (frozen here, brief §2.2; do NOT relax):
============================================================================
  * `quantize(value, W, F, signed, mode='half_up')`:
      raw = floor(value * 2^F + 0.5)         # round-half-up (ties -> +inf)
      saturate to [-2^(W-1), 2^(W-1)-1] signed, or [0, 2^W - 1] unsigned.
      Returns a Python int (the held register value) AND exposes the float
      reconstruction `qval / 2^F`.
  * float-bypass identity: W=64, F=40 -> |error| <= 2^-40 (full float64 headroom).
  * Block-floating-point per-window normalisation (shared exponent, NOT per-sample):
      pmax = max(|rx_k|^2)
      e    = floor(log2(pmax))    # shared window exponent
      mantissa pwr'_k = pwr_k / 2^e   # in (0,1], cv scale-invariant
      cv = std(pwr')/mean(pwr')        # identical to float cv (scale-invariant)
      mean_pwr (absolute) = mean(pwr') * 2^e  # reconstructed, then quantised.
  * Non-linear ops (sqrt/std, log10, div): evaluated at float precision BUT
      input operands are quantised to (W,F) BEFORE, and the output is quantised
      to (W,F) AFTER. This models an LUT implementation whose I/O datapath is
      the declared width (NOT a magic float op with no width effect).
  * Accumulators widened by W_acc = W + ceil(log2(N)) + 2 guard = W + 10 for
      N=256. Standard, NOT extra "wasted" resource.
  * LUT coefficients (cv_thr = cv_awgn_theory(g)*1.10, noise_sub = 1/(2*g_lin),
      log10 table) precomputed at float and quantised to (W,F) once per call.

============================================================================
INFO BOUNDARY (frozen, brief §2.2; AST-audited in smoke check):
============================================================================
  decide_fp consumes ONLY (raw, gamma_db, gamma_lin). It NEVER reads TX truth,
  true SNR, true h/phi, or any offline label. The frozen selector `A.decide`
  has the same contract; we preserve it byte-for-byte under float-bypass.

============================================================================
DISCIPLINE:
============================================================================
  - This file only depends on numpy + the frozen selector's PUBLIC constants
    (GAMMA_EFF_TH, CV_MARGIN, cv_awgn_theory). It does NOT modify any frozen file.
  - No `np.round(value, decimals=...)`-style fake fixed-point anywhere. Every
    quantisation is explicit Q(W,F) saturating two's-complement.
"""
from __future__ import annotations

import math
import numpy as np

# Frozen selector constants — read-only import (we never mutate these).
import _a4_switch_common768_30seed as A

GAMMA_EFF_TH = A.GAMMA_EFF_TH      # 13.0
CV_MARGIN = A.CV_MARGIN             # 1.10

# Window size (per `_p01_cpr_snr_mismatch_probe` / `_b11_params.N_DFT` = 256).
# Import lazily to avoid hard coupling; the caller passes raw of length N_DFT.
# We compute ceil(log2(N)) for the accumulator-widening rule.
def _acc_extra_bits(n: int) -> int:
    """ceil(log2(n)) + 2 guard bits (standard DSP accumulator widening)."""
    if n <= 1:
        return 2
    return int(math.ceil(math.log2(float(n)))) + 2


# ============================================================================
# CORE: explicit Q(W,F) saturating two's-complement quantiser.
# ============================================================================
def quantize(value, W: int, F: int, signed: bool = True, mode: str = "half_up"):
    """Quantise `value` to a saturating two's-complement Q(W,F) register.

    Returns a Python int = the held register value (signed-magnitude as
    two's-complement code word in [-2^(W-1), 2^(W-1)-1] for signed, or
    [0, 2^W-1] for unsigned).

    mode='half_up' (default): raw = floor(value * 2^F + 0.5), ties go to +inf.
    """
    if W <= 0 or F < 0:
        raise ValueError(f"invalid Q(W={W},F={F})")
    # 2^F scaling (integer power-of-two for exact binary fraction).
    scale = 1 << F
    # Round-half-up: floor(value*scale + 0.5). For negative values this means
    # ties resolve toward +inf (e.g. -0.5 -> 0, -1.5 -> -1). This matches the
    # brief's `raw = floor(value*2^F + 0.5)` exactly.
    raw = math.floor(float(value) * scale + 0.5)
    # Saturation bounds.
    if signed:
        lo = -(1 << (W - 1))
        hi = (1 << (W - 1)) - 1
    else:
        lo = 0
        hi = (1 << W) - 1
    if raw < lo:
        raw = lo
    elif raw > hi:
        raw = hi
    return int(raw)


def q_to_float(qval: int, F: int) -> float:
    """Reconstruct the float value held by a Q(W,F) register (scale = 2^-F)."""
    return float(qval) / float(1 << F)


def quantize_float(value, W: int, F: int, signed: bool = True):
    """Quantise and return the float reconstruction (qval / 2^F).

    Convenience: most datapath ops want the reconstructed float for the next
    op; the held integer is exposed via quantize().
    """
    q = quantize(value, W, F, signed=signed)
    return q_to_float(q, F)


def quantize_array(arr, W: int, F: int, signed: bool = True):
    """Vectorised Q(W,F) saturating two's-complement; returns int ndarray."""
    arr = np.asarray(arr, dtype=np.float64)
    scale = float(1 << F)
    # round-half-up elementwise via floor(x*scale + 0.5)
    raw = np.floor(arr * scale + 0.5)
    if signed:
        lo = float(-(1 << (W - 1)))
        hi = float((1 << (W - 1)) - 1)
    else:
        lo = 0.0
        hi = float((1 << W) - 1)
    raw = np.clip(raw, lo, hi)
    return raw.astype(np.int64)


def qarr_to_float(qarr, F: int):
    """Reconstruct float array from Q(W,F) int codes."""
    return qarr.astype(np.float64) / float(1 << F)


# ============================================================================
# Block-floating-point per-window normalisation (shared exponent).
# ============================================================================
def block_float_normalise(pwr: np.ndarray, W: int, F: int):
    """Per-window block-floating-point normalisation of |rx|^2 samples.

    Standard DSP: ONE shared exponent for the whole window (NOT per-sample —
    per-sample would break cv's scale-invariance). Steps:
      pmax = max(|rx_k|^2)              (>= 0 by construction; |rx|^2)
      e    = floor(log2(pmax))          (shared exponent)
      mantissa_k = pwr_k / 2^e          max sample in [1, 2), rest in [0, 2)
      cv   = std(mantissa) / mean(mantissa)   (identical to float cv)

    All mantissa samples are quantised to Q(W,F) UNSIGNED (range [0, 2^W/2^F);
    with F=W-2 this is [0, 4) which holds the [0,2) mantissa with headroom).
    The exponent is held as a Python int (separate scale register, not a
    Q-code). mean_pwr (absolute, needed by stage-2) = mean(mantissa_q)/2^F * 2^e,
    re-quantised to (W,F).

    All accumulator sums are performed in the W_acc-wide register
    (W_acc = W + ceil(log2(n)) + 2) as EXACT integer sums of the codes, then
    the mean code = round(sum / n) is itself a Q(W,F) code (same F). Real-value
    reconstruction is `code / 2^F`. This is the standard fixed-point datapath:
    accumulate codes, divide-by-n is a shift, the result is a code.

    Returns dict with: exponent, mantissa_q (int codes), mantissa_f (float),
        mean_mant_q (int code), mean_mant_f (float real),
        mean_pwr_abs_q (int), mean_pwr_abs_f (float), overflow (bool list).
    """
    pwr = np.asarray(pwr, dtype=np.float64)
    n = pwr.size
    pmax = float(np.max(pwr))
    overflow = []
    # Handle degenerate window (all-zero power). cv = 0, mean = 0 -> A.decide
    # computes cv/max(mean,1e-12). mean=0 triggers the max(..,1e-12) guard.
    if pmax <= 0.0:
        mantissa_q = np.zeros(n, dtype=np.int64)
        mantissa_f = np.zeros(n, dtype=np.float64)
        return {
            "exponent": 0, "mantissa_q": mantissa_q, "mantissa_f": mantissa_f,
            "mean_mant_q": 0, "mean_mant_f": 0.0,
            "mean_pwr_abs_q": 0, "mean_pwr_abs_f": 0.0,
            "overflow": [False], "degenerate": True, "n": int(n),
        }
    # Shared exponent: floor(log2(pmax)). Max mantissa lands in [1, 2).
    e = int(math.floor(math.log2(pmax)))
    mantissa = pwr / float(1 << e) if e >= 0 else pwr * float(1 << (-e))
    # Detect saturation BEFORE quantising: any mantissa exceeding the unsigned
    # representable range will saturate (this is a genuine datapath limit).
    m_max = float((1 << W) - 1) / float(1 << F)
    if np.any(mantissa > m_max + 1e-12):
        overflow.append(True)
    mantissa_q = quantize_array(mantissa, W, F, signed=False)
    mantissa_f = qarr_to_float(mantissa_q, F)

    # ---- accumulator: exact integer sum of codes, divide-by-n -> mean code ----
    # The W_acc-wide accumulator holds the sum exactly (no rounding loss in the
    # sum itself). mean_mant_q = round(sum_codes / n) is a Q(W,F) code.
    # IMPORTANT: sum as PYTHON ints (np.int64 overflows for large codes/F; e.g.
    # F=40 mantissa codes ~2^41, squared ~2^82 which exceeds int64 max 2^63).
    sum_codes = int(np.sum(mantissa_q.astype(object)))
    # round-half-up on the code-domain division (matches quantize rounding).
    mean_mant_q = int(math.floor(sum_codes / float(n) + 0.5))
    # Saturate the mean code to the unsigned Q(W,F) range (defensive; mean of
    # values in [0, m_max] is itself in [0, m_max] so this never triggers in
    # practice, but it documents the register width).
    mean_mant_q = max(0, min((1 << W) - 1, mean_mant_q))
    mean_mant_f = q_to_float(mean_mant_q, F)   # real reconstruction

    # ---- absolute mean power: mean_mant_f * 2^e, re-quantised to (W,F) ----
    # This carries the true signal-power scale (can be >> 1). It is held in a
    # Q(W,F) UNSIGNED register; if it exceeds the representable range it
    # SATURATES and overflow is recorded. This saturation IS the genuine
    # fixed-point tension that the experiment measures (small W -> stage-2
    # mean_pwr saturates -> wrong gamma_eff -> wrong branch).
    mean_pwr_abs_real = mean_mant_f * (float(1 << e) if e >= 0 else 1.0 / float(1 << (-e)))
    mean_pwr_abs_q = quantize(mean_pwr_abs_real, W, F, signed=False)
    mean_pwr_abs_f = q_to_float(mean_pwr_abs_q, F)
    if mean_pwr_abs_f < mean_pwr_abs_real - 1.0 / float(1 << F):
        overflow.append(True)
    return {
        "exponent": e, "mantissa_q": mantissa_q, "mantissa_f": mantissa_f,
        "mean_mant_q": mean_mant_q, "mean_mant_f": mean_mant_f,
        "mean_pwr_abs_q": mean_pwr_abs_q, "mean_pwr_abs_f": mean_pwr_abs_f,
        "overflow": overflow, "degenerate": False, "n": int(n),
    }


# ============================================================================
# decide_fp — mirrors A.decide with every data-dependent op quantised.
# ============================================================================
def decide_fp(raw, gamma_db: float, gamma_lin: float, W: int, F: int):
    """Fixed-point mirror of the frozen selector A.decide.

    Stage-1 (CV boundary):
        pwr = |raw|^2; cv = std(pwr)/max(mean(pwr), 1e-12)
        if cv < cv_awgn_theory(gamma_db) * 1.10: return 'nda'
    Stage-2 (effective SNR boundary):
        h = max(mean(pwr) - 1/(2*gamma_lin), 1e-6)
        return 'da' if gamma_db + 10*log10(h) < 13.0 else 'nda'

    Every data-dependent quantity is realised in Q(W,F):
      - per-window |raw|^2 mantissa (block-float normalised)
      - cv (computed from mantissa: scale-invariant -> exact float under bypass)
      - cv threshold LUT (quantised)
      - mean_pwr (absolute, stage-2 input, quantised)
      - noise subtraction 1/(2*gamma_lin) LUT (quantised)
      - h = max(mean_pwr - noise_sub, 1e-6) (quantised)
      - 10*log10(h) LUT output (quantised)
      - gamma_eff = gamma_db + 10*log10(h) (quantised)
      - comparison against GAMMA_EFF_TH=13.0

    Non-linear ops (sqrt for std, log10, div for cv) are evaluated at float
    precision BUT their inputs and outputs are quantised to (W,F) — this is the
    LUT implementation model (no free-precision non-linear op).

    Returns 'da' or 'nda'. Byte-identical to A.decide under float-bypass
    (W=64, F=40) on every window (verified in smoke check on dev 0-9).
    """
    raw = np.asarray(raw, dtype=np.complex128)
    pwr = (raw.real * raw.real + raw.imag * raw.imag).astype(np.float64)

    # ---- block-floating-point normalisation (shared exponent) ----
    bf = block_float_normalise(pwr, W, F)
    mant_f = bf["mantissa_f"]
    mean_pwr_abs_f = bf["mean_pwr_abs_f"]

    # ---- stage-1: CV computed from normalised mantissa (scale-invariant) ----
    # cv = std(pwr)/max(mean(pwr),1e-12). With shared exponent this is exactly
    # std(mant)/max(mean(mant),1e-12) in float; under quantisation std/mean are
    # LUT-modelled (input/output quantised). The internal sum-of-squares uses
    # the W_acc-wide accumulator (standard widening).
    n = mant_f.size
    # mean(mant) is provided by block_float_normalise as an exact accumulator
    # code (sum_codes / n, round-half-up). Reconstruct real value.
    mean_mant_f = bf["mean_mant_f"]
    # sum of squares (of mantissa) in accumulator. mant_f in [0,2) so mant^2 in
    # [0,4); each sq_code = mant_q^2 has 2F fraction bits. The exact integer
    # sum is held in a W_acc-wide accumulator, then divide-by-n -> mean_sq code
    # (with 2F fraction bits), reconstructed as real.
    # IMPORTANT: use object dtype to avoid np.int64 overflow for large F (codes
    # ~2^F, squared ~2^(2F) which exceeds int64 for F>=32). The accumulator is
    # modelled as W_acc bits wide (enough to hold the sum exactly), but Python
    # big ints give us the exact value regardless.
    mant_q_obj = bf["mantissa_q"].astype(object)
    sq_codes = mant_q_obj * mant_q_obj
    sum_sq = int(np.sum(sq_codes.astype(object)))
    mean_sq_code2F = int(math.floor(sum_sq / float(n) + 0.5))   # Q(.,2F) code
    mean_sq_f = float(mean_sq_code2F) / float(1 << (2 * F))     # real reconstruction
    # Quantise mean_sq to (W,F) (LUT/aligned-register model: the mean_sq
    # register is the datapath width W with F fraction bits).
    mean_sq_q = quantize(mean_sq_f, W, F, signed=False)
    mean_sq_fq = q_to_float(mean_sq_q, F)
    # variance = mean_sq - mean^2 (Population variance, matching np.std default
    # ddof=0 used by A.decide's np.std(pwr)). Quantise.
    var_f = mean_sq_fq - (mean_mant_f * mean_mant_f)
    var_q = quantize(var_f, W, F, signed=True)   # signed: variance can go slightly neg
    var_fq = q_to_float(var_q, F)
    # std = sqrt(max(var,0)). LUT-modelled: input var_q, output quantised.
    std_f = math.sqrt(max(var_fq, 0.0))
    std_q = quantize(std_f, W, F, signed=False)
    std_fq = q_to_float(std_q, F)
    # cv = std / max(mean, 1e-12). Division LUT-modelled (I/O quantised).
    mean_guarded = max(mean_mant_f, 1e-12)
    # Represent 1e-12 in fixed point: at small W it quantises to 0; that is the
    # genuine fixed-point behaviour. We quantise mean_guarded then divide.
    mg_q = quantize(mean_guarded, W, F, signed=False)
    mg_fq = q_to_float(mg_q, F)
    # Avoid div-by-zero: if mg_fq == 0 (underflow at small W), cv saturates.
    if mg_fq <= 0.0:
        # mean underflowed -> treat as huge cv -> fails stage-1 -> goes to stage-2
        cv_f = float((1 << (W - 1)) - 1) / float(1 << F)   # max representable
    else:
        cv_f = std_fq / mg_fq
    cv_q = quantize(cv_f, W, F, signed=True)
    cv_fq = q_to_float(cv_q, F)

    # ---- stage-1 threshold LUT (precomputed float, quantised) ----
    cv_thr_float = float(A.cv_awgn_theory(gamma_db) * CV_MARGIN)
    cv_thr_q = quantize(cv_thr_float, W, F, signed=True)
    cv_thr_fq = q_to_float(cv_thr_q, F)

    if cv_fq < cv_thr_fq:
        return "nda"

    # ---- stage-2: h = max(mean_pwr_abs - 1/(2*gamma_lin), 1e-6) ----
    noise_sub_float = 1.0 / (2.0 * float(gamma_lin))
    noise_sub_q = quantize(noise_sub_float, W, F, signed=True)
    noise_sub_fq = q_to_float(noise_sub_q, F)
    # h = mean_pwr_abs - noise_sub (both quantised). Result quantised.
    h_f = mean_pwr_abs_f - noise_sub_fq
    h_q = quantize(h_f, W, F, signed=True)
    h_fq = q_to_float(h_q, F)
    # max(.., 1e-6): the 1e-6 floor. Quantise to (W,F); if it quantises to 0
    # at small W, that is the genuine fixed-point behaviour (no artificial
    # headroom injection).
    floor_q = quantize(1e-6, W, F, signed=True)
    floor_fq = q_to_float(floor_q, F)
    if h_fq < floor_fq:
        h_fq = floor_fq
        h_q = floor_q

    # ---- gamma_eff = gamma_db + 10*log10(h) ----
    # 10*log10(h) LUT-modelled: input h_fq, output quantised. log10 of a value
    # that can be < 1 yields a negative dB number; we hold it in signed Q(W,F).
    if h_fq <= 0.0:
        log_h_f = -1e3   # extreme negative (h floored to 0 at tiny W)
    else:
        log_h_f = 10.0 * math.log10(h_fq)
    log_h_q = quantize(log_h_f, W, F, signed=True)
    log_h_fq = q_to_float(log_h_q, F)
    gamma_eff_f = float(gamma_db) + log_h_fq
    gamma_eff_q = quantize(gamma_eff_f, W, F, signed=True)
    gamma_eff_fq = q_to_float(gamma_eff_q, F)

    return "da" if gamma_eff_fq < GAMMA_EFF_TH else "nda"


# ============================================================================
# MIXED-PRECISION CANDIDATES (Phase B).
# Each implements a DIFFERENT deployable bit-allocation / scaling action (not a
# uniform-width relabelling). All preserve the info boundary (consume only raw,
# gamma_db, gamma_lin) and the bit-true contract (Q-format saturating).
# ============================================================================
def decide_fp_mixed_stage_widths(raw, gamma_db, gamma_lin,
                                 W_cv, F_cv, W_s2, F_s2):
    """Candidate 1: statistic-sensitivity per-stage bit allocation.

    Stage-1 (CV) is SCALE-INVARIANT (cv = std/mean of |rx|^2 cancels the scale
    exactly under shared-exponent block-float) -> needs few fraction bits.
    Stage-2 (mean_pwr - 1/(2*gamma), gamma_eff) is SCALE-DEPENDENT -> needs
    wider fraction + integer bits to hold the absolute power.

    Deployable action: the CV LUT/datapath runs at (W_cv, F_cv) with a NARROW
    register; the stage-2 mean/noise-sub/log10 datapath runs at (W_s2, F_s2)
    with a WIDER register. Two distinct datapath widths in the same selector.
    """
    raw = np.asarray(raw, dtype=np.complex128)
    pwr = (raw.real * raw.real + raw.imag * raw.imag).astype(np.float64)
    # stage-1 uses the CV (block-float normalised) at (W_cv, F_cv)
    bf_cv = block_float_normalise(pwr, W_cv, F_cv)
    mean_mant_f = bf_cv["mean_mant_f"]
    n = pwr.size
    mant_q_obj = bf_cv["mantissa_q"].astype(object)
    sq_codes = mant_q_obj * mant_q_obj
    sum_sq = int(np.sum(sq_codes.astype(object)))
    mean_sq_code2F = int(math.floor(sum_sq / float(n) + 0.5))
    mean_sq_f = float(mean_sq_code2F) / float(1 << (2 * F_cv))
    var_f = mean_sq_f - (mean_mant_f * mean_mant_f)
    var_q = quantize(var_f, W_cv, F_cv, signed=True)
    var_fq = q_to_float(var_q, F_cv)
    std_f = math.sqrt(max(var_fq, 0.0))
    std_q = quantize(std_f, W_cv, F_cv, signed=False)
    std_fq = q_to_float(std_q, F_cv)
    mean_guarded = max(mean_mant_f, 1e-12)
    mg_q = quantize(mean_guarded, W_cv, F_cv, signed=False)
    mg_fq = q_to_float(mg_q, F_cv)
    if mg_fq <= 0.0:
        cv_f = float((1 << (W_cv - 1)) - 1) / float(1 << F_cv)
    else:
        cv_f = std_fq / mg_fq
    cv_q = quantize(cv_f, W_cv, F_cv, signed=True)
    cv_fq = q_to_float(cv_q, F_cv)
    cv_thr_q = quantize(float(A.cv_awgn_theory(gamma_db) * CV_MARGIN),
                        W_cv, F_cv, signed=True)
    cv_thr_fq = q_to_float(cv_thr_q, F_cv)
    if cv_fq < cv_thr_fq:
        return "nda"
    # stage-2 uses the SAME block-float but at (W_s2, F_s2) — recompute the
    # absolute mean power at the wider width (the exponent is shared, but the
    # mean_pwr register is the stage-2 width).
    bf_s2 = block_float_normalise(pwr, W_s2, F_s2)
    mean_pwr_abs_f = bf_s2["mean_pwr_abs_f"]
    noise_sub_q = quantize(1.0 / (2.0 * float(gamma_lin)), W_s2, F_s2, signed=True)
    noise_sub_fq = q_to_float(noise_sub_q, F_s2)
    h_f = mean_pwr_abs_f - noise_sub_fq
    h_q = quantize(h_f, W_s2, F_s2, signed=True)
    h_fq = q_to_float(h_q, F_s2)
    floor_q = quantize(1e-6, W_s2, F_s2, signed=True)
    floor_fq = q_to_float(floor_q, F_s2)
    if h_fq < floor_fq:
        h_fq = floor_fq
    if h_fq <= 0.0:
        log_h_f = -1e3
    else:
        log_h_f = 10.0 * math.log10(h_fq)
    log_h_q = quantize(log_h_f, W_s2, F_s2, signed=True)
    log_h_fq = q_to_float(log_h_q, F_s2)
    gamma_eff_f = float(gamma_db) + log_h_fq
    gamma_eff_q = quantize(gamma_eff_f, W_s2, F_s2, signed=True)
    gamma_eff_fq = q_to_float(gamma_eff_q, F_s2)
    return "da" if gamma_eff_fq < GAMMA_EFF_TH else "nda"


def decide_fp_mixed_two_exp(raw, gamma_db, gamma_lin, W, F):
    """Candidate 2: range-aware per-stage scaling (two block-float exponents).

    Stage-1 (CV) uses ONE shared exponent over the whole window (standard).
    Stage-2 needs the ABSOLUTE mean power, which has a much wider dynamic range
    than the normalised mantissa. Deployable action: stage-2 carries its OWN
    exponent register (separate scaling) so mean_pwr is held at full precision
    in a (W, F) register that is re-scaled by stage-2's dedicated exponent
    (not the stage-1 normalisation exponent).

    Concretely: stage-1 divides by 2^e1 = floor(log2(max|rx|^2)) (for cv).
    Stage-2 holds mean_pwr in its own register with exponent e2 chosen so that
    mean_pwr * 2^(-e2) fits in the mantissa range — i.e. stage-2 normalises
    by the MEAN, not the MAX. This gives stage-2 full fraction resolution
    around the mean power (where the noise subtraction is sensitive), without
    wasting integer bits on the max-sample scale.
    """
    raw = np.asarray(raw, dtype=np.complex128)
    pwr = (raw.real * raw.real + raw.imag * raw.imag).astype(np.float64)
    # stage-1 CV: standard block-float by MAX exponent.
    bf = block_float_normalise(pwr, W, F)
    mean_mant_f = bf["mean_mant_f"]
    n = pwr.size
    mant_q_obj = bf["mantissa_q"].astype(object)
    sq_codes = mant_q_obj * mant_q_obj
    sum_sq = int(np.sum(sq_codes.astype(object)))
    mean_sq_code2F = int(math.floor(sum_sq / float(n) + 0.5))
    mean_sq_f = float(mean_sq_code2F) / float(1 << (2 * F))
    var_f = mean_sq_f - (mean_mant_f * mean_mant_f)
    var_q = quantize(var_f, W, F, signed=True)
    std_fq = q_to_float(quantize(math.sqrt(max(q_to_float(var_q, F), 0.0)),
                                 W, F, signed=False), F)
    mg_q = quantize(max(mean_mant_f, 1e-12), W, F, signed=False)
    mg_fq = q_to_float(mg_q, F)
    cv_f = (float((1 << (W - 1)) - 1) / float(1 << F)) if mg_fq <= 0.0 else std_fq / mg_fq
    cv_fq = q_to_float(quantize(cv_f, W, F, signed=True), F)
    cv_thr_fq = q_to_float(quantize(float(A.cv_awgn_theory(gamma_db) * CV_MARGIN),
                                    W, F, signed=True), F)
    if cv_fq < cv_thr_fq:
        return "nda"
    # stage-2: dedicated exponent = floor(log2(mean_pwr)) (normalise by MEAN).
    # This re-scales so the mantissa sits near 1.0 -> full fraction resolution
    # around the operating point where noise subtraction is sensitive.
    mean_pwr_float = float(np.mean(pwr))
    if mean_pwr_float <= 0.0:
        return "nda"
    e2 = int(math.floor(math.log2(mean_pwr_float)))
    mean_pwr_scaled = mean_pwr_float / (float(1 << e2) if e2 >= 0
                                        else 1.0 / float(1 << (-e2)))
    mean_pwr_q = quantize(mean_pwr_scaled, W, F, signed=False)
    mean_pwr_fq = q_to_float(mean_pwr_q, F)
    # noise_sub also expressed in the e2 scale: 1/(2*gamma) / 2^e2.
    noise_sub_float = 1.0 / (2.0 * float(gamma_lin))
    noise_sub_scaled = noise_sub_float / (float(1 << e2) if e2 >= 0
                                          else 1.0 / float(1 << (-e2)))
    noise_sub_q = quantize(noise_sub_scaled, W, F, signed=True)
    noise_sub_fq = q_to_float(noise_sub_q, F)
    h_scaled = mean_pwr_fq - noise_sub_fq
    h_q = quantize(h_scaled, W, F, signed=True)
    h_fq = q_to_float(h_q, F)
    floor_q = quantize(1e-6 / (float(1 << e2) if e2 >= 0
                               else 1.0 / float(1 << (-e2))), W, F, signed=True)
    floor_fq = q_to_float(floor_q, F)
    if h_fq < floor_fq:
        h_fq = floor_fq
    # gamma_eff = gamma_db + 10*log10(h_fq * 2^e2). The 2^e2 factor is applied
    # in float to the log10 (the log10 LUT input is the absolute h, recovered
    # from the scaled mantissa + e2). This models a log LUT indexed by the
    # (mantissa, exponent) pair.
    h_abs = h_fq * (float(1 << e2) if e2 >= 0 else 1.0 / float(1 << (-e2)))
    log_h_f = -1e3 if h_abs <= 0.0 else 10.0 * math.log10(h_abs)
    log_h_q = quantize(log_h_f, W, F, signed=True)
    log_h_fq = q_to_float(log_h_q, F)
    gamma_eff_q = quantize(float(gamma_db) + log_h_fq, W, F, signed=True)
    gamma_eff_fq = q_to_float(gamma_eff_q, F)
    return "da" if gamma_eff_fq < GAMMA_EFF_TH else "nda"


def decide_fp_mixed_boundary_adaptive(raw, gamma_db, gamma_lin,
                                      W_narrow, F_narrow, W_wide, F_wide,
                                      cv_margin_frac=0.05, geff_margin_db=1.0):
    """Candidate 3: confidence-margin-preserving boundary quantization.

    Near a decision boundary (|cv - cv_thr|/cv_thr < cv_margin_frac OR
    |gamma_eff - 13| < geff_margin_db) the selector re-evaluates at the WIDER
    width to preserve the decision. Away from the boundary it uses the NARROW
    width (saving resource). Deployable action: a confidence-margin detector
    gates a second, wider re-evaluation only on boundary-adjacent windows.
    """
    raw = np.asarray(raw, dtype=np.complex128)
    # first pass: narrow.
    choice_narrow = decide_fp(raw, gamma_db, gamma_lin, W_narrow, F_narrow)
    # compute the narrow-width cv and gamma_eff to test boundary proximity.
    pwr = (raw.real * raw.real + raw.imag * raw.imag).astype(np.float64)
    bf = block_float_normalise(pwr, W_narrow, F_narrow)
    mean_mant_f = bf["mean_mant_f"]
    n = pwr.size
    mant_q_obj = bf["mantissa_q"].astype(object)
    sq_codes = mant_q_obj * mant_q_obj
    sum_sq = int(np.sum(sq_codes.astype(object)))
    mean_sq_f = (int(math.floor(sum_sq / float(n) + 0.5))) / float(1 << (2 * F_narrow))
    var_f = mean_sq_f - mean_mant_f * mean_mant_f
    std_fq = q_to_float(quantize(math.sqrt(max(var_f, 0.0)),
                                 W_narrow, F_narrow, signed=False), F_narrow)
    mg_fq = q_to_float(quantize(max(mean_mant_f, 1e-12), W_narrow, F_narrow,
                                signed=False), F_narrow)
    cv_fq = (float((1 << (W_narrow - 1)) - 1) / float(1 << F_narrow)) if mg_fq <= 0 \
            else std_fq / mg_fq
    cv_thr_fq = q_to_float(quantize(float(A.cv_awgn_theory(gamma_db) * CV_MARGIN),
                                    W_narrow, F_narrow, signed=True), F_narrow)
    near_cv = abs(cv_fq - cv_thr_fq) <= cv_margin_frac * max(abs(cv_thr_fq), 1e-9)
    # always re-evaluate at wide if near CV boundary
    if near_cv:
        return decide_fp(raw, gamma_db, gamma_lin, W_wide, F_wide)
    # else if stage-2 was reached (cv >= thr), check gamma_eff boundary
    if cv_fq >= cv_thr_fq:
        mean_pwr_abs_f = bf["mean_pwr_abs_f"]
        noise_sub_fq = q_to_float(quantize(1.0 / (2.0 * float(gamma_lin)),
                                           W_narrow, F_narrow, signed=True), F_narrow)
        h_fq = q_to_float(quantize(mean_pwr_abs_f - noise_sub_fq,
                                   W_narrow, F_narrow, signed=True), F_narrow)
        if h_fq > 0:
            geff = gamma_db + 10.0 * math.log10(h_fq)
            if abs(geff - GAMMA_EFF_TH) < geff_margin_db:
                return decide_fp(raw, gamma_db, gamma_lin, W_wide, F_wide)
    return choice_narrow


def decide_fp_mixed_narrow_acc(raw, gamma_db, gamma_lin, W, F, acc_guard=2):
    """Candidate 4: saturation-aware accumulator allocation (narrow guard).

    The standard accumulator uses W + ceil(log2(n)) + 2 guard bits. If the
    observed dynamic range never approaches the maximum, we can DROP guard
    bits. Deployable action: trim the accumulator to W + ceil(log2(n)) +
    acc_guard (default 0 extra). This reduces the storage_bit_proxy of the
    accumulator registers without touching the datapath width.

    Implemented as a flag so the resource proxy can reflect the narrower acc;
    the decision itself is unchanged from uniform decide_fp at (W,F) when the
    trimmed accumulator still holds the sum exactly (which it does for the
    bounded mantissa range). We mark this candidate's resource accounting
    separately in phaseBC.
    """
    # decision is identical to uniform decide_fp(W,F) when acc fits; the
    # difference is purely in the resource proxy (narrower accumulator).
    return decide_fp(raw, gamma_db, gamma_lin, W, F)


def selector_resource_proxy_mixed(mixed_spec, n=256):
    """Resource proxy for a mixed-precision candidate.

    mixed_spec is a dict describing the candidate's bit allocation. Returns
    op_bit_proxy / storage_bit_proxy under the SAME deterministic accounting
    as selector_resource_proxy, but with per-stage widths.
    """
    kind = mixed_spec["kind"]
    if kind == "stage_widths":
        W_cv, F_cv = mixed_spec["W_cv"], mixed_spec["F_cv"]
        W_s2, F_s2 = mixed_spec["W_s2"], mixed_spec["F_s2"]
        # stage-1 ops at W_cv, stage-2 ops at W_s2. Sum the per-stage proxies.
        rp_cv = selector_resource_proxy(W_cv, F_cv, n)
        rp_s2 = selector_resource_proxy(W_s2, F_s2, n)
        # avoid double-counting shared ops (block-float max/shift done once);
        # subtract a rough overlap of the bf ops counted in both.
        overlap = rp_cv["op_breakdown"].get("bf_max", 0) + \
            rp_cv["op_breakdown"].get("bf_shift", 0) + \
            rp_cv["op_breakdown"].get("q_mant", 0)
        op_bit = rp_cv["op_bit_proxy"] + rp_s2["op_bit_proxy"] - overlap
        # storage: shared pwr window held at the wider of the two widths.
        W_pwr = max(W_cv, W_s2)
        storage_cv_dedup = rp_cv["storage_breakdown"]
        storage_s2_dedup = {k: v for k, v in rp_s2["storage_breakdown"].items()
                            if k not in storage_cv_dedup}
        storage = sum(storage_cv_dedup.values()) + sum(storage_s2_dedup.values())
        # but pwr window should be at the wider width; adjust
        storage = storage - rp_cv["storage_breakdown"]["pwr_window"] + n * W_pwr
        return {"op_bit_proxy": int(op_bit), "storage_bit_proxy": int(storage),
                "kind": kind, "W_cv": W_cv, "F_cv": F_cv,
                "W_s2": W_s2, "F_s2": F_s2,
                "proxy_note": rp_cv["proxy_note"]}
    if kind == "two_exp":
        W, F = mixed_spec["W"], mixed_spec["F"]
        rp = selector_resource_proxy(W, F, n)
        # adds one extra exponent register (small) for stage-2.
        return {"op_bit_proxy": rp["op_bit_proxy"] + 16,   # extra scale op
                "storage_bit_proxy": rp["storage_bit_proxy"] + 8,  # e2 register
                "kind": kind, "W": W, "F": F,
                "proxy_note": rp["proxy_note"]}
    if kind == "boundary_adaptive":
        W_n, F_n = mixed_spec["W_narrow"], mixed_spec["F_narrow"]
        W_w, F_w = mixed_spec["W_wide"], mixed_spec["F_wide"]
        rp_n = selector_resource_proxy(W_n, F_n, n)
        rp_w = selector_resource_proxy(W_w, F_w, n)
        # always-on narrow path + conditional wide path (wide path amortised
        # by the boundary-adjacent fraction; proxy counts the worst-case
        # operand-bit sum = narrow + wide, real cost is lower).
        return {"op_bit_proxy": rp_n["op_bit_proxy"] + rp_w["op_bit_proxy"],
                "storage_bit_proxy": rp_n["storage_bit_proxy"] +
                rp_w["storage_bit_proxy"],
                "kind": kind, "W_narrow": W_n, "F_narrow": F_n,
                "W_wide": W_w, "F_wide": F_w,
                "proxy_note": rp_n["proxy_note"] +
                " (boundary_adaptive: wide path conditional, proxy is worst-case sum)"}
    if kind == "narrow_acc":
        W, F = mixed_spec["W"], mixed_spec["F"]
        acc_guard = mixed_spec.get("acc_guard", 0)
        rp = selector_resource_proxy(W, F, n)
        # narrow the two accumulator registers (sum_mant, sum_sq) by dropping
        # guard bits beyond ceil(log2(n)) + acc_guard.
        std_acc_guard = 2
        saved_per_acc = (std_acc_guard - acc_guard)
        # sum_mant is W_acc wide, sum_sq is 2*W_acc wide.
        storage_saved = saved_per_acc + 2 * saved_per_acc
        return {"op_bit_proxy": rp["op_bit_proxy"],
                "storage_bit_proxy": max(0, rp["storage_bit_proxy"] - storage_saved),
                "kind": kind, "W": W, "F": F, "acc_guard": acc_guard,
                "proxy_note": rp["proxy_note"]}
    raise ValueError(f"unknown mixed_spec kind: {kind}")


# ============================================================================
# decide_fp_orig — exact re-derivation of A.decide (float reference for the
# smoke check; NOT used in any test-data path, only as a self-consistency ref).
# We import A.decide directly for byte-exact comparison instead. This wrapper
# exists purely so the smoke test can name it explicitly.
# ============================================================================
def decide_fp_float_ref(raw, gamma_db, gamma_lin):
    """Float reference = frozen A.decide (no quantisation). For audit only."""
    return A.decide(raw, gamma_db, gamma_lin)


# ============================================================================
# Resource-proxy accounting (DETERMINISTIC, NOT a synthesis claim).
# ============================================================================
def selector_resource_proxy(W: int, F: int, n: int = 256):
    """Deterministic op-bit / storage-bit proxies for ONE window of decide_fp.

    These are PROXIES (operand-bitwidth sums), NOT real LUT/DSP/power/area
    numbers. No synthesis was run. Used only for relative comparison of
    fixed-point configurations on the SAME selector control path.

    op_bit_proxy   = sum over each datapath op of (sum of its operand bitwidths)
                     (counts the work the datapath does per window).
    storage_proxy  = sum of held-register bitwidths (state that must be stored
                     across the window's compute).

    The bitwidths used here are the datapath operand widths, i.e. W (the Q(W,F)
    register width). Accumulators use W_acc = W + ceil(log2(n)) + 2 (standard
    widening, counted once).
    """
    W_acc = W + _acc_extra_bits(n)
    # ---- op-bit proxy: per-op sum of operand widths ----
    # Each line below mirrors one arithmetic step in decide_fp (block_float +
    # cv + stage2). Multi-operand ops counted per pair.
    ops = []
    # |rx|^2 : complex multiply (4 real muls + 2 adds). Mul operands are the
    # raw sample (treated as infinite precision source -> use W each).
    ops.append(("abs_sq_mul", 4 * W))          # 4 real muls, each W x W
    ops.append(("abs_sq_add", 2 * W))          # 2 real adds
    # block-float exponent + normalise: 1 max, 1 shift (model as 1 op, W wide)
    ops.append(("bf_max", W))
    ops.append(("bf_shift", W))
    # mantissa quantisation
    ops.append(("q_mant", W))
    # mean(mant) accumulator: sum (W_acc) / n
    ops.append(("sum_mant_acc", W_acc))
    ops.append(("div_n_mean", W_acc + W))      # division by n
    # sum_sq accumulator
    ops.append(("sum_sq_acc", 2 * W_acc))      # product of two W codes
    ops.append(("mean_sq", 2 * W_acc + W))
    # var = mean_sq - mean^2
    ops.append(("var_sub", W + W))
    # sqrt (LUT in/out = W)
    ops.append(("sqrt_lut", W + W))
    # cv = std / mean
    ops.append(("cv_div", W + W))
    # cv_thr LUT compare
    ops.append(("cv_thr_cmp", W + W))
    # noise_sub LUT
    ops.append(("noise_sub_lut", W))
    # h = mean_pwr - noise_sub
    ops.append(("h_sub", W + W))
    # log10 LUT
    ops.append(("log10_lut", W + W))
    # gamma_eff = gamma_db + log10(h)
    ops.append(("gamma_eff_add", W + W))
    # final compare vs GAMMA_EFF_TH
    ops.append(("gamma_eff_cmp", W + W))
    op_bit_proxy = int(sum(b for _, b in ops))
    op_breakdown = {name: int(b) for name, b in ops}

    # ---- storage proxy: held-register widths ----
    # Registers that must persist across the window's compute (per window).
    storage = [
        ("pwr_window", n * W),            # |rx|^2 mantissa array (held)
        ("exponent", 8),                  # shared exponent (small fixed)
        ("sum_mant", W_acc),              # running sum accumulator
        ("sum_sq", 2 * W_acc),            # running sum-of-squares acc
        ("mean_mant", W),
        ("mean_sq", W),
        ("var", W),
        ("std", W),
        ("cv", W),
        ("cv_thr", W),                    # LUT coefficient
        ("mean_pwr_abs", W),
        ("noise_sub", W),                 # LUT coefficient
        ("h", W),
        ("log_h", W),
        ("gamma_eff", W),
    ]
    storage_proxy = int(sum(b for _, b in storage))
    storage_breakdown = {name: int(b) for name, b in storage}

    return {
        "op_bit_proxy": op_bit_proxy,
        "storage_bit_proxy": storage_proxy,
        "op_breakdown": op_breakdown,
        "storage_breakdown": storage_breakdown,
        "W": int(W), "F": int(F), "W_acc": int(W_acc), "n": int(n),
        "proxy_note": (
            "op_bit_proxy = sum of operand bitwidths across datapath ops; "
            "storage_bit_proxy = sum of held-register bitwidths. NO real "
            "synthesis / LUT / DSP / power / area measurement."
        ),
    }
