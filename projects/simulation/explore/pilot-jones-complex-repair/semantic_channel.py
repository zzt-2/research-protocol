"""Semantic channel for the Pilot-Jones complex-model REPAIR (T004).

This module fixes the five semantic defects located by V038/D064:

  #1 NOISE PLACEMENT — T003 applied the component Jones to the canonical RX that
     already contained AWGN, so J^{-1} undid the noise transform too. The PDL
     headroom was therefore bit-identical to M0 (a construction identity).
     FIX: separate the clean atmospheric signal from the canonical realization,
          then apply the component operator to the CLEAN signal only and ADD the
          SAME post-component noise draw back. The component NEVER touches n_post.

  #2 PDL PASSIVITY — T003 used g=[cond,1], so the max singular value = cond > 1,
     i.e. the "PDL component" amplified. A real passive component cannot amplify.
     FIX: singular values = [1, 10^(-PDL_dB/20)]; sigma_max=1, cond=10^(PDL/20).

  #3 PRE-CHANNEL PILOT — T003 reconstructed pilot RX with a memoryless J@atm and
     never passed pilots through the PMD FIR; residual carried old-data ISI.
     FIX: pilots are injected into the TX frame BEFORE the channel; pilot and
          data then traverse the SAME component operator + SAME noise.

Information boundary
--------------------
The component truth (Jones / PSP delays) is GENERATED once per realization and
stored as truth. Deployable baselines/methods read ONLY the receiver-visible RX
+ pilots + own state. The oracle reads the truth to build the ideal inverse
(tagged upper bound / Kill only).

Signal chain (see repair-contract.yaml §primary_signal_chain):
    TX full frame (pilots replaced BEFORE the channel)
      -> sqrt(h) R(theta)               atmospheric clean signal   [clean_atm]
      -> passive component Jones/PMD/PDL component op              [H_op]
      -> post-component AWGN (canonical draw)                      [n_post]
      -> receiver
"""
from __future__ import annotations
import numpy as np


# ---------------------------------------------------------------------------
# Atmosphere clean-signal reconstruction + noise separation from canonical
# ---------------------------------------------------------------------------

def _atm_clean_signal(realization):
    """Reconstruct the atmosphere clean signal clean_atm = sqrt(h)*R(theta)@s
    from the canonical realization, where R(theta)=[[c,s],[-s,c]].

    Returns clean (2, N). This is what the component operator must act on.
    """
    theta = np.asarray(realization["theta"])
    sX = np.asarray(realization["sX"], dtype=complex)
    sY = np.asarray(realization["sY"], dtype=complex)
    h = np.asarray(realization["h"])
    c = np.cos(theta); s = np.sin(theta)
    cleanX = np.sqrt(h) * (c * sX + s * sY)
    cleanY = np.sqrt(h) * (-s * sX + c * sY)
    return np.stack((cleanX, cleanY), axis=0)  # (2, N)


def separate_canonical(realization):
    """Split the canonical realization into the clean atmospheric signal and the
    post-component AWGN noise:

        clean_original = sqrt(h) * R(theta) @ s_original
        n_post         = r_canonical - clean_original

    The component channel operator is then applied to ``clean_original`` (with
    pilots injected) and the SAME ``n_post`` is added back. This is the fix for
    V038 defect #1.
    """
    clean_original = _atm_clean_signal(realization)            # (2, N)
    r = np.stack((np.asarray(realization["rX"], complex),
                  np.asarray(realization["rY"], complex)), axis=0)  # (2, N)
    n_post = r - clean_original
    return {"clean_original": clean_original, "n_post": n_post}


# ---------------------------------------------------------------------------
# Passive PDL / complex-unitary Jones matrices
# ---------------------------------------------------------------------------

def _random_unitary(rng, n: int) -> np.ndarray:
    """n independent 2x2 complex unitary matrices via QR of complex Gaussian."""
    A = (rng.standard_normal((n, 2, 2)) + 1j * rng.standard_normal((n, 2, 2)))
    U = np.empty_like(A)
    for k in range(n):
        q, r = np.linalg.qr(A[k])
        d = np.diag(r)
        q = q * (d / np.abs(d))[None, :]   # fix QR phase ambiguity
        U[k] = q
    return U


def pdl_singular_values(pdl_db: float) -> np.ndarray:
    """PASSIVE PDL singular values: sigma_max = 1, sigma_min = 10^(-PDL/20).

    A passive component cannot amplify -> max transmissivity = 1.
    cond = sigma_max/sigma_min = 10^(PDL_dB/20).  (V038 defect #2 fix.)
    """
    return np.array([1.0, 10.0 ** (-pdl_db / 20.0)])


def _pdl_to_cond(pdl_db: float) -> float:
    return float(10.0 ** (pdl_db / 20.0))


def build_jones_truth(rng, model_id, *, n_blocks, pdl_db=0.0):
    """Generate the per-block component Jones TRUTH (memoryless part).

    M0  identity.            M1  arbitrary complex unitary (cond==1).
    M2  passive PDL J=U diag(1,10^(-PDL/20)) Vh  (sigma_max==1, passive).
    M3  identity Jones + PMD FIR memory (delay in the PSP basis).
    M4  PDL Jones + PMD FIR memory (composable).
    """
    jones = np.zeros((n_blocks, 2, 2), dtype=complex)
    if model_id == "M0":
        jones[:] = np.eye(2, dtype=complex)
        return jones
    if model_id == "M1":
        jones[:] = _random_unitary(rng, n_blocks)
        return jones
    if model_id in ("M2", "M4"):
        U = _random_unitary(rng, n_blocks)
        V = _random_unitary(rng, n_blocks)
        sv = pdl_singular_values(pdl_db)
        for b in range(n_blocks):
            jones[b] = U[b] @ np.diag(sv) @ V[b].conj().T
        return jones
    if model_id in ("M3",):
        # memoryless part is identity; the memory comes from the PMD FIR.
        jones[:] = np.eye(2, dtype=complex)
        return jones
    raise ValueError(f"unknown model_id={model_id!r}")


# ---------------------------------------------------------------------------
# Component channel operator: acts on a CLEAN (2, N) frame, returns (2, N).
# It is the SAME operator for pilot and data (defect #3 fix). dgd=0 -> memoryless.
# ---------------------------------------------------------------------------

PMD_GUARD = 8  # transient samples excluded at each block boundary


def pmd_circular_freq(jones_b, dgd_samples, nfft):
    """Per-frequency PMD Jones operator for one block (FFT-circular convention):

        J(f) = U @ diag(sv_i * exp(-j 2 pi f tau_i)) @ Vh , tau = dgd*[+1/2,-1/2]

    Used by BOTH the forward component application and the oracle inverse, so the
    forward model and its oracle use the SAME convolution convention and are exact
    inverses modulo the block-boundary transient (excluded from the metric).
    At dgd=0 -> exp(0)=1 -> reduces to the memoryless J_b (limiting-case gate).
    """
    U, sv, Vh = np.linalg.svd(jones_b)
    f = np.fft.fftfreq(nfft)
    tau = dgd_samples * np.array([0.5, -0.5])
    Hf = np.zeros((nfft, 2, 2), dtype=complex)
    phase = np.exp(-1j * 2 * np.pi * np.outer(f, tau))       # (nfft, 2)
    for fi in range(nfft):
        Hf[fi] = U @ np.diag(sv * phase[fi]) @ Vh
    return Hf, U, sv, Vh


def apply_component(clean_frame, jones, *, block_size, dgd_samples,
                    pmd_enabled):
    """Apply the component channel operator to a CLEAN (2, N) frame.

    Parameters
    ----------
    clean_frame : (2, N) complex clean atmospheric signal (pilots already injected).
    jones       : (n_blocks, 2, 2) per-block component Jones truth.
    dgd_samples : differential group delay in symbol units (0 -> memoryless).
    pmd_enabled : if True and dgd_samples>0, apply the PSP-basis PMD memory.

    Returns the component-transformed (2, N) clean signal. Noise is NOT touched.
    The memoryless part (M0/M1/M2) multiplies J_b per block. The PMD part (M3/M4)
    convolves each PSP by +/- dgd/2 samples in the FFT-circular convention (same as
    the oracle inverse), so forward and oracle are exact inverses except at the
    block-boundary transient (PMD_GUARD samples, excluded from the metric). dgd=0
    reduces exactly to the memoryless Jones (limiting-case gate).
    """
    r = np.asarray(clean_frame, dtype=complex)
    N = r.shape[1]
    n_blocks = jones.shape[0]
    out = np.zeros_like(r)
    use_pmd = bool(pmd_enabled and dgd_samples > 1e-12)
    for b in range(n_blocks):
        s = b * block_size
        e = min(s + block_size, N)
        if e <= s:
            continue
        J = jones[b]
        seg = r[:, s:e].copy()
        if use_pmd:
            L = e - s
            nfft = L  # FFT-circular on the segment itself (guard excludes transient)
            Hf, U, sv, Vh = pmd_circular_freq(J, dgd_samples, nfft)
            segf = np.fft.fft(seg, axis=1)              # (2, nfft)
            out_f = np.empty((2, nfft), dtype=complex)
            for fi in range(nfft):
                out_f[:, fi] = Hf[fi] @ segf[:, fi]
            seg_out = np.fft.ifft(out_f, axis=1)
        else:
            seg_out = J @ seg
        out[:, s:e] = seg_out
    return out


# ---------------------------------------------------------------------------
# Full impaired realization builder
# ---------------------------------------------------------------------------

def build_impaired_realization(realization, *, model_id, block_size, rng,
                               pdl_db=0.0, dgd_ps=0.0, t_s=4e-10):
    """Build the repaired impaired realization from the canonical realization.

    Steps (T004 §3.1):
      1. separate canonical -> clean_original, n_post
      2. build per-block component Jones truth
      3. apply component operator to clean_original -> clean_component
      4. r_out = clean_component + n_post   (SAME noise draw; noise untouched)
      5. store truth for the tagged oracle

    The component operator is applied to clean_original which has NO pilots
    injected yet (pilots are injected into the TX frame at the pilot layer, then
    the WHOLE frame re-runs the atmosphere + component chain — see
    pilot_and_baselines.inject_pre_channel_pilots).
    """
    sep = separate_canonical(realization)
    clean_original = sep["clean_original"]
    n_post = sep["n_post"]
    N = clean_original.shape[1]
    n_blocks = (N + block_size - 1) // block_size

    jones = build_jones_truth(rng, model_id, n_blocks=n_blocks, pdl_db=pdl_db)
    pmd_enabled = model_id in ("M3", "M4")
    dgd_samples = dgd_ps * 1e-12 / t_s if pmd_enabled else 0.0

    clean_component = apply_component(clean_original, jones,
                                      block_size=block_size,
                                      dgd_samples=dgd_samples,
                                      pmd_enabled=pmd_enabled)
    r_out = clean_component + n_post

    out = dict(realization)  # keep sX/sY/h/theta/bits (evaluation only)
    out["rX"] = r_out[0]
    out["rY"] = r_out[1]
    out["clean_original"] = clean_original      # (2,N) clean atmospheric signal
    out["n_post"] = n_post                       # (2,N) post-component AWGN
    out["clean_component"] = clean_component     # (2,N) clean after component
    out["jones_truth"] = jones                   # (n_blocks,2,2) oracle truth
    out["model_id"] = model_id
    out["model_params"] = {
        "pdl_db": float(pdl_db), "dgd_ps": float(dgd_ps),
        "t_s": float(t_s), "block_size": int(block_size),
        "dgd_samples": float(dgd_samples), "pmd_enabled": bool(pmd_enabled),
        "cond_target": float(_pdl_to_cond(pdl_db)) if pdl_db > 0 else 1.0,
        "sigma_max": 1.0, "sigma_min": float(10.0 ** (-pdl_db / 20.0)),
    }
    return out


def report_insertion_loss(jones):
    """Report per-block insertion loss + two-path gain of the passive PDL.

    insertion_loss_dB = -20*log10(sigma_max)  (0 dB for a passive PDL, sigma_max=1)
    two-path gains = singular values.
    """
    sv = np.linalg.svd(jones, compute_uv=False)            # (n_blocks, 2)
    smax = float(sv[:, 0].mean())
    smin = float(sv[:, 1].mean())
    return {
        "sigma_max_mean": smax, "sigma_min_mean": smin,
        "insertion_loss_dB": float(-20.0 * np.log10(max(smax, 1e-12))),
        "cond_mean": float((sv[:, 0] / sv[:, 1]).mean()),
    }
