"""GMI (generalized mutual information) estimation from soft LLRs.

Two estimators (per the frozen contract):

* ``compute_gmi(llrs, true_bits)`` — PRIMARY: non-parametric HISTOGRAM mutual
  information ``I(bit_k; LLR_k)`` between the raw per-bit LLR and the true bit.
  The raw LLR already encodes both the favoured bit (sign) and the confidence
  (magnitude), so ``I(bit_k; LLR_k)`` captures the full soft information without
  any assumed LLR distribution. ``GMI = sum_k I(bit_k; LLR_k)`` in bits/symbol
  (4 bits for 16QAM), also reported per-bit (bits/bit).
* ``compute_gmi_analytic(llrs, true_bits)`` — SECONDARY cross-check: the
  standard analytic soft-GMI ``4 - sum_k mean log2(1 + exp(-(2b-1)*LLR_k))`` with
  numerically-stable softplus. This assumes the demapper LLRs are BPSK-like
  calibrated per bit (the textbook FEC-agnostic GMI). It is a cross-check on the
  histogram estimator, NOT the primary.

Histogram MI is primary because it makes NO assumption on the LLR distribution
and is robust to the bimodal/inner-ring residual structure the mixture demapper
is designed to model. (The matched-filter ``(2b-1)*LLR`` form is only valid for
the analytic softplus GMI; using it inside the histogram would collapse
perfectly-correlated LLRs to a constant and give MI=0.)

LLR convention (must match soft_demap.py): ``LLR_k >= 0`` => bit ``k = 1`` more
likely. For the histogram estimator the LLR is used RAW; for the analytic
estimator the per-bit matched value ``(2b-1)*LLR`` (positive when the soft
decision is correct) drives the softplus loss.
"""

from __future__ import annotations

import numpy as np

# Perfect 16QAM = 4 bits/symbol.
GMI_CEILING = 4.0


def _histogram_mi(x: np.ndarray, y: np.ndarray, n_bins: int = 16) -> float:
    """Mutual information I(X;Y) in bits via 2-D histogram binning.

    ``x`` is the continuous feature (binned into ``n_bins`` equi-width bins),
    ``y`` is binary {0,1}. MI = sum_{x,y} p(x,y) log2( p(x,y) / (p(x)p(y)) ).
    A constant ``x`` (uninformative feature) yields MI = 0.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    y = np.asarray(y, dtype=np.float64).ravel()
    n = x.size
    if n == 0:
        return 0.0
    # Equi-width bins over the data range (robust default). Constant x => MI=0.
    xmin = float(x.min()); xmax = float(x.max())
    if xmax - xmin < 1e-12:
        return 0.0
    edges = np.linspace(xmin, xmax, n_bins + 1)
    # Bin index per sample (right edge inclusive on the last bin).
    xb = np.digitize(x, edges) - 1
    xb = np.clip(xb, 0, n_bins - 1)
    # Joint counts (bins × 2) and marginals.
    joint = np.zeros((n_bins, 2), dtype=np.float64)
    for cls in (0, 1):
        joint[:, cls] = np.bincount(xb[y == cls], minlength=n_bins)[:n_bins]
    joint /= n
    px = joint.sum(axis=1, keepdims=True)  # (bins,1)
    py = joint.sum(axis=0, keepdims=True)  # (1,2)
    # I(X;Y) over nonzero cells.
    denom = px @ py  # (bins,2) outer product
    mask = (joint > 0) & (denom > 0)
    return float(np.sum(joint[mask] * np.log2(joint[mask] / denom[mask])))


def compute_gmi(
    llrs: np.ndarray, true_bits: np.ndarray, *, n_bins: int = 16,
) -> dict[str, float]:
    """PRIMARY: histogram-mutual-information GMI from per-bit LLRs.

    Computes ``I(bit_k; LLR_k)`` (raw LLR vs bit) for each bit position k and
    sums to bits/symbol. Makes no assumption on the LLR distribution.

    Parameters
    ----------
    llrs : (N, 4) float
        Per-bit LLRs (LLR_k >= 0 => bit k = 1 more likely).
    true_bits : (N, 4) int
        True TX bits.
    n_bins : int
        Number of equi-width bins for the histogram MI estimator.

    Returns
    -------
    dict with ``gmi_per_bit`` (4,) in bits/bit, ``gmi`` aggregate in bits/symbol,
    ``gmi_per_bit_position`` (alias), and ``ceiling`` = 4.0.
    """
    llrs = np.asarray(llrs, dtype=np.float64)
    true_bits = np.asarray(true_bits, dtype=np.float64)
    if llrs.ndim != 2 or llrs.shape[1] != 4:
        raise ValueError(f"llrs must be (N,4), got {llrs.shape}")
    if llrs.shape != true_bits.shape:
        raise ValueError(f"llrs {llrs.shape} != true_bits {true_bits.shape}")

    per_bit = np.empty(4, dtype=np.float64)
    for k in range(4):
        per_bit[k] = _histogram_mi(llrs[:, k], true_bits[:, k], n_bins=n_bins)
    per_bit = np.clip(per_bit, 0.0, 1.0)  # I(bit;LLR) in [0,1] bits
    return {
        "gmi_per_bit": per_bit.tolist(),
        "gmi_per_bit_position": {f"bit{k}": float(per_bit[k]) for k in range(4)},
        "gmi": float(per_bit.sum()),          # bits/symbol (4 bits)
        "gmi_per_bit_mean": float(per_bit.mean()),
        "ceiling": GMI_CEILING,
        "estimator": "histogram",
        "n_bins": int(n_bins),
        "n_samples": int(llrs.shape[0]),
    }


def compute_gmi_analytic(llrs: np.ndarray, true_bits: np.ndarray) -> dict[str, float]:
    """SECONDARY cross-check: analytic soft-GMI = mean log2(1 + exp(-b*LLR)).

    Standard FEC-agnostic GMI assuming BPSK-like per-bit LLR calibration:
        GMI = 4 - sum_k mean_n log2(1 + exp(-(2*b-1)*LLR_k)).
    Numerically stable via softplus (log2(1+e^-x) = log2(e)*softplus(-x) and
    softplus(z) = max(z,0) + log1p(exp(-|z|))). LLRs clipped to the soft_demap
    LLR_CLIP are handled gracefully (softplus saturates).
    """
    llrs = np.asarray(llrs, dtype=np.float64)
    true_bits = np.asarray(true_bits, dtype=np.float64)
    if llrs.ndim != 2 or llrs.shape[1] != 4:
        raise ValueError(f"llrs must be (N,4), got {llrs.shape}")
    if llrs.shape != true_bits.shape:
        raise ValueError(f"llrs {llrs.shape} != true_bits {true_bits.shape}")
    # Per-bit "matched filter" soft value: (2b-1)*LLR. Positive => correct.
    matched = (2.0 * true_bits - 1.0) * llrs  # (N,4)
    # log2(1 + exp(-matched)) = log2(e) * softplus(-matched)
    z = -matched
    softplus = np.maximum(z, 0.0) + np.log1p(np.exp(-np.abs(z)))
    log2e = np.log2(np.e)
    per_bit_loss = log2e * np.mean(softplus, axis=0)  # (4,) bits/symbol per bit
    per_bit = np.clip(1.0 - per_bit_loss, 0.0, 1.0)   # bits/bit
    return {
        "gmi_per_bit": per_bit.tolist(),
        "gmi_per_bit_position": {f"bit{k}": float(per_bit[k]) for k in range(4)},
        "gmi": float(per_bit.sum()),
        "gmi_per_bit_mean": float(per_bit.mean()),
        "ceiling": GMI_CEILING,
        "estimator": "analytic_softplus",
        "n_samples": int(llrs.shape[0]),
    }


__all__ = [
    "GMI_CEILING",
    "compute_gmi",
    "compute_gmi_analytic",
]

