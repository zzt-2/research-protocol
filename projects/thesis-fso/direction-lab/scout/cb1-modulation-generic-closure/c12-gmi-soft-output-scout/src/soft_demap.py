"""Soft demappers for 16QAM — standard max-log, collapse-aware mixture, and oracle.

This is the C12 GMI soft-output evaluator (p04 HALF_DAY unblock). Three
demappers share the SAME frozen fixed-μ CMA z-stream and differ ONLY in their
noise/residual model:

* ``maxlog_soft_demap_16qam(z_eval, sigma2)`` — STANDARD max-log soft demapper.
  Assumes a single per-symbol Gaussian residual with variance ``sigma2``.
  Same-information (uses only z + the public 16QAM alphabet).
* ``mixture_soft_demap_16qam(z_calib, z_eval)`` — THE C12 CANDIDATE. Models the
  per-real-axis residual as a 2-component Gaussian mixture (healthy component +
  collapsed/inner-ring component), estimates the mixture parameters BLIND from
  ``z_calib``, then computes max-log LLRs from the mixture likelihood. Same
  information contract as the standard demapper.
* ``oracle_soft_demap_16qam(z_eval, truth_symbols)`` — SCORING-ONLY Kill bound.
  Uses TX-truth-conditioned noise variance. Never a runtime comparator.

LLR convention (frozen, consistent across all three demappers)
--------------------------------------------------------------
``LLR_k >= 0`` means bit ``k = 1`` is more likely than bit ``k = 0``. The max-log
form is

    LLR_k = min_{s: bit_k=0} [D(s)] - min_{s: bit_k=1} [D(s)]

where ``D(s) = |z - s|² / (2 sigma²)`` is the scaled squared Euclidean distance
from the received sample ``z`` to constellation point ``s``. (With this sign,
``LLR_k > 0`` favours ``bit_k = 1``, matching the convention that the standard
``qam16_demod`` / ``_modulation`` bit order is the bit order used here.)

The 16QAM Gray constellation
----------------------------
``{±1, ±3}/sqrt(10)`` per real axis, average power = 1, identical to
``_modulation.qam16_mod``. The constellation and per-bit label table are built
once at import and verified against ``_modulation`` in the identity tests.

Dependencies: numpy + scipy only (sklearn absent per p04 env probe). The 2-comp
Gaussian mixture is fit by a self-contained EM (no sklearn).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.special import logsumexp


# ─── 16QAM Gray constellation (matches _modulation.qam16_mod exactly) ────────
# Gray map per axis: index 0->-3, 1->-1, 2->+3, 3->+1 (so adjacent levels differ
# by 1 bit). Symbol = (I_level + j Q_level)/sqrt(10); avg power = 1.
# Bit order per symbol: [b0,b1,b2,b3] where
#   b0,b1 = MSB,LSB of the 2-bit I index ; b2,b3 = MSB,LSB of the 2-bit Q index.
def _build_qam16_table() -> tuple[np.ndarray, np.ndarray]:
    gray_map = np.array([-3.0, -1.0, +3.0, +1.0])  # axis level for index 0..3
    inv_sqrt10 = 1.0 / np.sqrt(10.0)
    syms = np.zeros(16, dtype=np.complex128)
    labels = np.zeros((16, 4), dtype=np.int8)
    idx = 0
    for b0 in (0, 1):
        for b1 in (0, 1):
            for b2 in (0, 1):
                for b3 in (0, 1):
                    bi = 2 * b0 + b1  # I index
                    bq = 2 * b2 + b3  # Q index
                    syms[idx] = (gray_map[bi] + 1j * gray_map[bq]) * inv_sqrt10
                    labels[idx] = (b0, b1, b2, b3)
                    idx += 1
    return syms, labels


QAM16_SYM, QAM16_BITS = _build_qam16_table()
# Precompute, per bit position k, the constellation indices where bit k = 0 / 1.
_BIT0_IDX = [np.where(QAM16_BITS[:, k] == 0)[0] for k in range(4)]
_BIT1_IDX = [np.where(QAM16_BITS[:, k] == 1)[0] for k in range(4)]

# LLR clip for numerical stability (prevents inf/0 in downstream GMI/MI).
LLR_CLIP = 30.0


# ─── Helper: clipped scaled-distance min per bit value ───────────────────────
def _llrs_from_distances(d2: np.ndarray, inv_2sigma2: float, clip: float) -> np.ndarray:
    """Max-log LLRs from per-sample squared distances.

    Parameters
    ----------
    d2 : (N, 16) float
        Squared Euclidean distance |z_n - s_i|^2 for each sample n, symbol i.
    inv_2sigma2 : float
        1 / (2 sigma^2) scale. The 1/(2 sigma^2) cancels in the per-bit LLR
        when sigma^2 is the SAME for all symbols (standard demapper), but we
        keep it explicit for code symmetry with the mixture/oracle cases.
    clip : float
        Magnitude clip applied to each LLR.

    Returns
    -------
    (N, 4) float LLRs, LLR_k >= 0 => bit k = 1 more likely.
    """
    scaled = d2 * inv_2sigma2  # (N,16)
    out = np.empty((scaled.shape[0], 4), dtype=np.float64)
    for k in range(4):
        min_bit0 = np.min(scaled[:, _BIT0_IDX[k]], axis=1)  # min over bit_k=0
        min_bit1 = np.min(scaled[:, _BIT1_IDX[k]], axis=1)  # min over bit_k=1
        llr = min_bit0 - min_bit1  # >0 => bit_k=1 closer/more likely
        out[:, k] = np.clip(llr, -clip, clip)
    return out


def _sq_dist(z: np.ndarray) -> np.ndarray:
    """Squared Euclidean distance |z_n - s_i|^2, shape (N, 16)."""
    z = np.asarray(z, dtype=np.complex128).ravel()
    diff = z[:, None] - QAM16_SYM[None, :]
    return np.abs(diff) ** 2


# ─── (1) Standard max-log soft demapper ──────────────────────────────────────
def maxlog_soft_demap_16qam(z_samples: np.ndarray, sigma2: float) -> np.ndarray:
    """Standard max-log soft demapper for 16QAM (single-Gaussian residual).

    For each sample computes 4-bit LLRs using the max-log approximation:
    LLR_k = min_{s: bit_k=0} |z-s|^2/(2 sigma^2)
          - min_{s: bit_k=1} |z-s|^2/(2 sigma^2).

    Parameters
    ----------
    z_samples : (N,) complex
        Equalized (carrier-aligned) symbols.
    sigma2 : float
        Per-symbol residual noise variance. MUST be > 0.

    Returns
    -------
    (N, 4) float LLRs. LLR_k >= 0 => bit k = 1 more likely.
    """
    sigma2 = float(sigma2)
    if sigma2 <= 0.0:
        raise ValueError(f"sigma2 must be > 0, got {sigma2}")
    d2 = _sq_dist(z_samples)
    return _llrs_from_distances(d2, 1.0 / (2.0 * sigma2), LLR_CLIP)


# ─── (2) Collapse-aware mixture soft demapper (THE C12 CANDIDATE) ────────────
def _fit_gmm_1d_em(
    x: np.ndarray, *, n_iter: int = 100, tol: float = 1e-6, seed: int = 0,
) -> dict[str, np.ndarray]:
    """Fit a 2-component 1-D Gaussian mixture by EM (no sklearn).

    Returns a dict with keys: w (2,) mixture weights, mu (2,) means,
    var (2,) variances. Component 0 = healthy (narrower), component 1 =
    collapsed/wide. The collapse fraction is ``w[1]``.

    Initialisation: component 0 = the points below the median |x| (small
    residual = healthy); component 1 = the points above (large residual =
    collapsed/inner-ring). This directly seeds the healthy/collapsed split the
    mixture is meant to represent, so EM converges to the intended mode and not
    a degenerate all-in-one-component solution.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    n = x.size
    if n < 4:
        # Too few points to fit a 2-comp mixture meaningfully -> degenerate to
        # one component (all healthy). Caller still gets a valid (Gaussian) LLR.
        var = float(np.var(x)) if n > 0 else 1.0
        var = max(var, 1e-9)
        return {"w": np.array([1.0, 0.0]), "mu": np.array([np.mean(x) if n else 0.0, 0.0]),
                "var": np.array([var, var])}

    med = np.median(np.abs(x))
    mask_big = np.abs(x) > med
    if (not mask_big.any()) or mask_big.all():
        # Degenerate split — fall back to a healthy-only fit.
        var = max(float(np.var(x)), 1e-9)
        return {"w": np.array([1.0, 0.0]), "mu": np.array([float(np.mean(x)), 0.0]),
                "var": np.array([var, var])}

    # Component 0 = healthy (small |x|), component 1 = collapsed (large |x|)
    mu0 = float(np.mean(x[~mask_big])); var0 = max(float(np.var(x[~mask_big])), 1e-9)
    mu1 = float(np.mean(x[mask_big]));  var1 = max(float(np.var(x[mask_big])), 1e-9)
    w = np.array([float((~mask_big).mean()), float(mask_big.mean())])
    mu = np.array([mu0, mu1]); var = np.array([var0, var1])

    prev_ll = -np.inf
    for _ in range(n_iter):
        # E-step: responsibilities r[n,c] (un-normalised log density)
        logp = np.empty((n, 2))
        for c in range(2):
            logp[:, c] = (np.log(w[c] + 1e-300)
                          - 0.5 * (np.log(2 * np.pi * var[c] + 1e-300)
                                   + (x - mu[c]) ** 2 / var[c]))
        ll = float(logsumexp(logp, axis=1).sum())
        r = np.exp(logp - logsumexp(logp, axis=1, keepdims=True))  # (n,2)
        # M-step
        nk = r.sum(axis=0) + 1e-300
        w = nk / n
        mu = (r * x[:, None]).sum(axis=0) / nk
        var = (r * (x[:, None] - mu[None, :]) ** 2).sum(axis=0) / nk
        var = np.maximum(var, 1e-9)
        if abs(ll - prev_ll) < tol:
            break
        prev_ll = ll

    # Canonicalise: component 0 = healthy (smaller var), component 1 = collapsed.
    order = np.argsort(var)
    return {"w": w[order], "mu": mu[order], "var": var[order]}


def _mixture_loglikelihood_1d(x: np.ndarray, gmm: dict) -> np.ndarray:
    """Per-point log p(x) under a 1-D 2-component Gaussian mixture."""
    n = x.size
    logp = np.empty((n, 2))
    for c in range(2):
        logp[:, c] = (np.log(gmm["w"][c] + 1e-300)
                      - 0.5 * (np.log(2 * np.pi * gmm["var"][c] + 1e-300)
                               + (x - gmm["mu"][c]) ** 2 / gmm["var"][c]))
    return logsumexp(logp, axis=1)


def _fit_mixture_from_calib(z_calib: np.ndarray, min_weight: float = 0.05) -> dict[str, Any]:
    """Fit the per-real-axis 2-comp Gaussian mixture to calib residuals.

    The residual is ``z_calib - hard_16qam(z_calib)`` (blind: only the public
    alphabet is used). The 16QAM collapse concentrates residual mass at a larger
    radius than AWGN (the inner-ring / collapsed component); the mixture
    separates this from the healthy (narrow) component.

    Returns a dict with the Re/Im GMMs and a robust summary sigma^2 used to
    seed the per-symbol effective variance map in the mixture demapper.
    """
    from cb1_evaluator import hard_16qam  # lazy (public-alphabet hard decision)

    z_calib = np.asarray(z_calib, dtype=np.complex128).ravel()
    resid = z_calib - hard_16qam(z_calib)
    gmm_re = _fit_gmm_1d_em(np.real(resid))
    gmm_im = _fit_gmm_1d_em(np.imag(resid))

    # Guard against a degenerate "all collapsed" or "all healthy" fit by flooring
    # each component weight at min_weight (renormalised). Keeps both components
    # alive so the demapper degrades gracefully to the standard demapper when no
    # collapse is present.
    def _floor(gmm):
        w = np.clip(gmm["w"], min_weight, 1.0)
        w = w / w.sum()
        return {"w": w, "mu": gmm["mu"], "var": gmm["var"]}
    gmm_re = _floor(gmm_re)
    gmm_im = _floor(gmm_im)
    return {"re": gmm_re, "im": gmm_im}


def mixture_soft_demap_16qam(
    z_calib: np.ndarray, z_eval: np.ndarray, *, min_weight: float = 0.05,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Collapse-aware 2-component-mixture soft demapper for 16QAM (C12 candidate).

    Fits a per-real-axis healthy/collapsed Gaussian mixture to the BLIND
    calibration residual (``z_calib - hard_16qam(z_calib)``), then computes
    per-bit max-log LLRs from the mixture likelihood.

    The per-symbol residual is treated as independent on the Re and Im axes
    (standard for square QAM soft demapping). For symbol ``s`` and received
    ``z`` the mixture negative log-likelihood (up to an additive constant) is

        NLL(z, s) = -log p(Re(z-s); gmm_re) - log p(Im(z-s); gmm_im)

    The max-log LLR for bit k is then

        LLR_k = min_{s: bit_k=0} NLL(z,s) - min_{s: bit_k=1} NLL(z,s)

    computed on the full likelihood (NOT its min-component approximation) so the
    bimodal residual mass is honoured.

    Parameters
    ----------
    z_calib : (M,) complex
        Calibration slice of the equalized stream (BLIND, alphabet-only).
    z_eval : (N,) complex
        Evaluation slice (same carrier alignment as z_calib).
    min_weight : float
        Floor on each mixture component weight (guards against degeneracy).

    Returns
    -------
    llrs : (N, 4) float
    info : dict with the fitted mixture parameters (for diagnostics/inspection).
    """
    gmm = _fit_mixture_from_calib(z_calib, min_weight=min_weight)
    gmm_re, gmm_im = gmm["re"], gmm["im"]

    z_eval = np.asarray(z_eval, dtype=np.complex128).ravel()
    d_re = (np.real(z_eval)[:, None] - np.real(QAM16_SYM)[None, :])  # (N,16)
    d_im = (np.imag(z_eval)[:, None] - np.imag(QAM16_SYM)[None, :])

    # Per-axis mixture NLL: -log p(delta) for each (sample, symbol), shape (N,16)
    def _nll_1d(delta, gmm):
        n, m = delta.shape
        logp = np.empty((n, m, 2))
        for c in range(2):
            logp[:, :, c] = (np.log(gmm["w"][c] + 1e-300)
                             - 0.5 * (np.log(2 * np.pi * gmm["var"][c] + 1e-300)
                                      + (delta - gmm["mu"][c]) ** 2 / gmm["var"][c]))
        # -logsumexp over the 2 components = negative mixture log-likelihood
        return -logsumexp(logp, axis=2)
    nll = _nll_1d(d_re, gmm_re) + _nll_1d(d_im, gmm_im)  # (N,16)

    out = np.empty((z_eval.size, 4), dtype=np.float64)
    for k in range(4):
        min_bit0 = np.min(nll[:, _BIT0_IDX[k]], axis=1)
        min_bit1 = np.min(nll[:, _BIT1_IDX[k]], axis=1)
        llr = min_bit0 - min_bit1  # >0 => bit_k=1 closer/more likely (NLL lower)
        out[:, k] = np.clip(llr, -LLR_CLIP, LLR_CLIP)

    return out, gmm


# ─── (3) Oracle soft demapper (Kill bound, TX-truth-conditioned variance) ───
def oracle_soft_demap_16qam(
    z_eval: np.ndarray, truth_symbols: np.ndarray,
) -> np.ndarray:
    """Oracle soft demapper: TX-truth-conditioned noise variance (Kill bound).

    Uses the TRUE TX symbol to condition the noise model. This is SCORING ONLY:
    never a runtime comparator (FR-21). It defines the soft-output headroom
    ceiling a perfect noise model could reach on the same z-stream.

    The oracle noise variance is estimated from the residual around the TRUE
    symbols (not hard decisions), so it is the minimum-variance (Cramer-Rao-ish)
    noise estimate. LLRs are then standard max-log with that variance.

    Parameters
    ----------
    z_eval : (N,) complex
    truth_symbols : (N,) complex
        On-grid TX truth symbols (16QAM-normalized).

    Returns
    -------
    (N, 4) float LLRs.
    """
    z_eval = np.asarray(z_eval, dtype=np.complex128).ravel()
    truth_symbols = np.asarray(truth_symbols, dtype=np.complex128).ravel()
    if z_eval.shape != truth_symbols.shape:
        raise ValueError("z_eval and truth_symbols must have the same shape")
    resid = z_eval - truth_symbols
    # Per-symbol total noise variance (complex), truth-conditioned.
    sigma2 = float(np.mean(np.abs(resid) ** 2))
    sigma2 = max(sigma2, 1e-9)
    return maxlog_soft_demap_16qam(z_eval, sigma2)


__all__ = [
    "QAM16_SYM",
    "QAM16_BITS",
    "LLR_CLIP",
    "maxlog_soft_demap_16qam",
    "mixture_soft_demap_16qam",
    "oracle_soft_demap_16qam",
]
