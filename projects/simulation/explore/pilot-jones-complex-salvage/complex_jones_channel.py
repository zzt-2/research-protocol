"""Complex-Jones / PMD / PDL channel ladder for the Pilot-Jones model-sufficiency
salvage (T003).

Design
------
Each model is a RECEIVER-SIDE post-processor applied on top of the canonical
realization produced by ``generate_shared_realization_dp`` (the shared truth
source, T002 source-closure.yaml). The canonical model already contains the
atmospheric part (GG fade ``h`` + real SOP rotation ``theta``). The T003 models
add the component/transceiver impairment that the canonical model omits:

    M0  control           : real unitary rotation only (== canonical, cond==1)
    M1  complex-unitary   : arbitrary complex unitary Jones U (still cond==1)
    M2  non-unitary PDL   : J = U @ diag(g1,g2) @ Vh, g1/g2 from PDL dB (cond>1)
    M3  first-order PMD   : frequency-dependent 2x2 Jones / short 2x2 FIR memory
                            (DGD in seconds; frequency-selective within the band)
    M4  combined          : M2 + M3 (only if budget allows and M2/M3 pass gate)

All impairments are BLOCK-CONSTANT (block << tau_c, consistent with the GG
block-constant assumption) so the pilot-LS seam of T002 still applies block-by-
block. The impairment is applied to BOTH pilot and data symbols identically
(no selective bias), so all arms (B0/B1/B2/B3/P/O) see the same channel.

Information boundary
--------------------
The impairment parameters are GENERATED once per realization and stored as
``extra`` truth in the realization dict. The deployable methods (baselines +
proposed) read ONLY the receiver-visible RX (rX,rY) + pilots + own state. The
oracle reads the true Jones to build the ideal inverse (tagged upper bound).

No function here reads TX data except the oracle constructor (tagged). The
canonical realization (sX/sY) is passed through unchanged for evaluation only.
"""
from __future__ import annotations
import numpy as np


# ---------------------------------------------------------------------------
# Helpers for building unitary / PDL Jones matrices
# ---------------------------------------------------------------------------

def _random_unitary(rng, n: int) -> np.ndarray:
    """Draw n independent 2x2 complex unitary matrices via QR of a complex Gaussian.

    Returns shape (n, 2, 2). Each U satisfies U @ U.conj().T == I.
    """
    A = (rng.standard_normal((n, 2, 2)) + 1j * rng.standard_normal((n, 2, 2)))
    U = np.empty_like(A)
    for k in range(n):
        q, r = np.linalg.qr(A[k])
        # fix the phase ambiguity so QR gives a unique unitary
        d = np.diag(r)
        q = q * (d / np.abs(d))[None, :]
        U[k] = q
    return U


def _pdl_to_cond(pdl_db: float) -> float:
    """PDL(dB) -> singular-value ratio (condition number of the Jones matrix).

    PDL(dB) = 10*log10(Pmax/Pmin); with field singular values sigma and
    P = sigma^2, PDL = 20*log10(sigma_max/sigma_min) = 20*log10(cond).
    VERIFIED relation (see model-evidence.yaml Q3).
    """
    return float(10 ** (pdl_db / 20.0))


def _real_rotation_stack(theta: np.ndarray) -> np.ndarray:
    """Stack of 2x2 real rotation matrices [[c,-s],[s,c]] (note the sign
    convention matches the canonical generator row order)."""
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.zeros((len(theta), 2, 2))
    R[:, 0, 0] = c
    R[:, 0, 1] = s      # matches canonical rX = c*sX + s*sY
    R[:, 1, 0] = -s     # matches canonical rY = -s*sX + c*sY
    R[:, 1, 1] = c
    return R


# ---------------------------------------------------------------------------
# Model ladder. Each function returns a dict with keys:
#   rX, rY       : impaired received signals (complex, length N)
#   sX, sY       : TX symbols (passed through unchanged, evaluation only)
#   h, theta     : canonical fade / SOP (passed through)
#   bitsX, bitsY : TX bits (passed through)
#   modulation / bits_per_symbol / bitX / bitY : compatibility aliases
#   jones_truth  : (N,2,2) true Jones applied (oracle only; tagged)
#   model_id     : 'M0'..'M4'
#   model_params : dict of impairment parameters used
# ---------------------------------------------------------------------------

def apply_complex_jones(realization, *, model_id, block_size, rng,
                        pdl_db=0.0, dgd_ps=0.0, t_s=4e-10,
                        unitary_complex=False, n_fft=None):
    """Apply a complex-Jones / PMD / PDL impairment on top of the canonical
    realization.

    The canonical realization already encodes r_canonical = sqrt(h)*R(theta)@s +
    noise. We insert an ADDITIONAL block-constant Jones impairment J (component/
    transceiver) AFTER the atmospheric part but reusing the canonical RX to keep
    the same noise draw:

        r_out = J_b @ r_canonical   (no new noise; J_b block-constant)

    This preserves the canonical shared-noise contract while adding the missing
    component structure. Because J is block-constant and applied to the already-
    faded RX, the noise covariance is scaled by J_b J_b^H block-by-block (a
    real, identifiable consequence of PDL — not a fake noise draw).

    Parameters
    ----------
    model_id : {'M0','M1','M2','M3','M4'}
    pdl_db   : PDL in dB (M2/M4). cond = 10**(pdl_db/20).
    dgd_ps   : DGD in ps (M3/M4). Frequency-selective if dgd_ps > 0.
    t_s      : symbol period (s), for converting DGD to a fraction of T_S.
    unitary_complex : if True (M1), draw an arbitrary complex unitary J.
    n_fft    : FFT size for the frequency-selective PMD model (M3). Default
               uses the next power of two >= N.
    """
    rX = np.asarray(realization["rX"], dtype=complex).copy()
    rY = np.asarray(realization["rY"], dtype=complex).copy()
    N = len(rX)
    r = np.stack((rX, rY), axis=0)  # (2, N)

    # one block-constant Jones per block
    n_blocks = (N + block_size - 1) // block_size
    jones = np.zeros((n_blocks, 2, 2), dtype=complex)

    cond_target = _pdl_to_cond(pdl_db) if pdl_db > 0 else 1.0

    for b in range(n_blocks):
        # base Jones: identity (M0) or complex unitary (M1) or PDL (M2/M4)
        if model_id in ("M0",):
            J = np.eye(2, dtype=complex)
        elif model_id == "M1" or unitary_complex:
            U = _random_unitary(rng, 1)[0]
            J = U
        elif model_id in ("M2", "M4"):
            U = _random_unitary(rng, 1)[0]
            V = _random_unitary(rng, 1)[0]
            g = np.array([cond_target, 1.0])
            J = U @ np.diag(g) @ V.conj().T
        else:
            J = np.eye(2, dtype=complex)
        jones[b] = J

    # ---- frequency-selective PMD (M3/M4): convolve each block with a 2x2 FIR
    #      that has a differential group delay dgd_ps ------------------------
    if model_id in ("M3", "M4") and dgd_ps > 0:
        # fractional delay in samples; >0 -> genuine memory (ISI).
        delay_samples = dgd_ps * 1e-12 / t_s
        # build a 2x2 complex FIR per block: PSP along J's two singular vectors.
        # J(f) = U @ diag(exp(-j 2 pi f tau1), exp(-j 2 pi f tau2)) @ Vh,
        # with tau1-tau2 = dgd. Equivalent short FIR: fractional-delay filters.
        r = _apply_pmd_fir(r, jones, block_size, delay_samples, rng)
    else:
        # memoryless application, block by block
        r = _apply_memoryless_jones(r, jones, block_size)

    out = dict(realization)  # copy canonical (keeps sX/sY/h/theta/bits)
    out["rX"] = r[0]
    out["rY"] = r[1]
    out["jones_truth"] = jones  # (n_blocks,2,2) true Jones per block (oracle)
    out["model_id"] = model_id
    out["model_params"] = {
        "pdl_db": float(pdl_db),
        "dgd_ps": float(dgd_ps),
        "cond_target": float(cond_target),
        "unitary_complex": bool(unitary_complex),
        "block_size": int(block_size),
        "t_s": float(t_s),
    }
    return out


def _apply_memoryless_jones(r, jones, block_size):
    """Apply block-constant Jones J_b to a (2,N) signal."""
    N = r.shape[1]
    out = r.copy()
    n_blocks = jones.shape[0]
    for b in range(n_blocks):
        s = b * block_size
        e = min(s + block_size, N)
        if e <= s:
            continue
        out[:, s:e] = jones[b] @ r[:, s:e]
    return out


def _apply_pmd_fir(r, jones, block_size, delay_samples, rng):
    """Frequency-selective first-order PMD: per block, apply a 2x2 FIR that
    realizes a differential group delay ``delay_samples`` (in symbol units)
    along the two principal states of ``jones[b]``.

    Implementation: in the principal-state basis (columns of V from J=U D Vh),
    one state is delayed by +d/2 and the other by -d/2 samples via a fractional-
    delay sinc filter (band-limited, ~17 taps). This produces genuine inter-
    symbol memory proportional to d; at d=0 it reduces to the memoryless J.
    """
    N = r.shape[1]
    out = np.zeros_like(r)
    n_blocks = jones.shape[0]
    ntaps = 17
    half = ntaps // 2
    # precompute fractional-delay kernels for +/- d/2
    d = float(delay_samples)

    def _frac_delay_kernel(delta):
        # band-limited sinc fractional-delay filter (Lagrange/sinc), centered.
        n = np.arange(ntaps) - half
        if abs(delta) < 1e-9:
            k = np.zeros(ntaps); k[half] = 1.0
            return k
        # ideal sinc fractional delay, windowed
        h = np.sinc(n - delta)
        h = h * np.hanning(ntaps)
        h = h / h.sum() if h.sum() != 0 else h
        return h

    for b in range(n_blocks):
        s = b * block_size
        e = min(s + block_size, N)
        if e <= s:
            continue
        J = jones[b]
        # principal states: right singular vectors V (columns)
        U, sv, Vh = np.linalg.svd(J)
        V = Vh.conj().T
        seg = r[:, s:e].copy()
        L = e - s
        # rotate into PSP basis
        psp = Vh @ seg  # (2, L)
        # delay each PSP by +/- d/2. Use edge-padded 'same' convolution so the
        # output length always equals the segment length L (handles short last
        # block and keeps block boundaries consistent).
        k_pos = _frac_delay_kernel(+d / 2.0)
        k_neg = _frac_delay_kernel(-d / 2.0)
        delayed = np.empty_like(psp)
        delayed[0] = _conv_same(psp[0], k_pos)
        delayed[1] = _conv_same(psp[1], k_neg)
        # rotate back and apply U (amplitude) — reconstruct J(f) approx
        seg_out = V @ delayed
        # the amplitude part (singular values) is applied as memoryless gain
        seg_out = U @ np.diag(sv) @ seg_out
        out[:, s:e] = seg_out
    return out


def _conv_same(sig, kernel):
    """Edge-padded convolution returning the SAME length as ``sig``."""
    L = len(sig)
    nt = len(kernel)
    half = nt // 2
    padded = np.concatenate([np.full(half, sig[0]), sig, np.full(nt - 1 - half, sig[-1])])
    conv = np.convolve(padded, kernel, mode="valid")
    # conv has length L; safety trim/pad to exactly L
    if len(conv) > L:
        conv = conv[:L]
    elif len(conv) < L:
        conv = np.concatenate([conv, np.zeros(L - len(conv))])
    return conv


# ---------------------------------------------------------------------------
# Oracle: build the ideal inverse from the true Jones (tagged upper bound).
# For memoryless models the inverse is J_b^-1. For PMD (M3) the memoryless
# inverse is a LOWER bound on oracle (it cannot undo ISI); we also expose a
# full frequency-domain MMSE oracle for the headroom ceiling.
# ---------------------------------------------------------------------------

def jones_inverse_truth(realization_imp, *, block_size):
    """Return the per-block true inverse J_b^-1 (memoryless oracle inverse).

    Only used by the tagged oracle arm. For M3 (PMD) this is a memoryless
    inverse that cannot remove ISI, so it is a LOWER bound on the achievable
    oracle; a full frequency-domain oracle is computed separately for the
    headroom ceiling (see salvage_methods.oracle_fde).
    """
    J = np.asarray(realization_imp["jones_truth"])  # (n_blocks,2,2)
    inv = np.linalg.inv(J)
    return inv  # (n_blocks,2,2)
