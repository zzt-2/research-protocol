"""Temporal channel for the Pilot-Jones component TEMPORAL SEMANTICS adjudication (T005).

This module is the decisive T005 change over T004. It INHERITS the T004
signal/noise/pilot/target/gate engineering fixes (V038 defects #1-#5) but
re-establishes the component channel with the correct TEMPORAL semantics and
DETERMINISTIC provenance required by V039/D065:

  (1) PRIMARY temporal model: the component Jones / PSP basis + DGD is generated
      ONCE per realization and FIXED across the whole frame. A real passive
      optical component does not redraw its principal states every 25.6 ns; the
      canonical R(theta) already carries the time-varying SOP. (T004's
      `build_jones_truth()` redrew U/V every 64 symbols = every 25.6 ns, which
      is an UNSOURCED temporal model.)

  (2) DETERMINISTIC seed: a fixed integer model_id + canonical seed + offset.
      No Python built-in hash() may enter a seed (V039: hash(model_id) is
      process-randomized -> two subprocesses with the same seed disagree).

  (3) FFT-circular PMD forward + reference use the SAME convention (inherited
      from T004), with PMD_GUARD excluded from the metric denominator.

Signal chain (contract.yaml §primary_temporal_model):
    TX full frame (pilots replaced BEFORE the channel)
      -> sqrt(h) R(theta)               atmospheric clean signal   [clean_atm]
      -> ONE FIXED passive component Jones / fixed PSP+DGD           [component op]
      -> post-component AWGN (canonical draw)                        [n_post]
      -> receiver

T003/T004 code is NOT imported (immutable evidence). The verified dual-QPSK
signal/noise separation and FFT-circular PMD logic are re-implemented here so
this package is self-contained and isolated.
"""
from __future__ import annotations
import numpy as np


# ---------------------------------------------------------------------------
# Deterministic seed (V039 fix)
# ---------------------------------------------------------------------------

MODEL_ID_INT = {"M0": 0, "M2": 2, "M3": 3}


def component_rng_seed(canonical_seed: int, model_id: str) -> int:
    """Deterministic, hash-free component-truth RNG seed.

    Same (canonical_seed, model_id) -> same integer in EVERY Python process
    (no built-in hash()). contract.yaml §deterministic_seed.
    """
    mid = MODEL_ID_INT[model_id]
    return int(1_000_000 + 31 * int(canonical_seed) + mid)


# ---------------------------------------------------------------------------
# Atmosphere clean-signal reconstruction + noise separation (T004 defect #1)
# ---------------------------------------------------------------------------

def _atm_clean_signal(realization):
    """Reconstruct clean_atm = sqrt(h)*R(theta)@s, R=[[c,s],[-s,c]]. Returns (2,N)."""
    theta = np.asarray(realization["theta"])
    sX = np.asarray(realization["sX"], dtype=complex)
    sY = np.asarray(realization["sY"], dtype=complex)
    h = np.asarray(realization["h"])
    c = np.cos(theta); s = np.sin(theta)
    cleanX = np.sqrt(h) * (c * sX + s * sY)
    cleanY = np.sqrt(h) * (-s * sX + c * sY)
    return np.stack((cleanX, cleanY), axis=0)


def separate_canonical(realization):
    """Split canonical into the clean atmospheric signal and post-component AWGN.

    clean_original = sqrt(h) * R(theta) @ s_original
    n_post         = r_canonical - clean_original
    """
    clean_original = _atm_clean_signal(realization)
    r = np.stack((np.asarray(realization["rX"], complex),
                  np.asarray(realization["rY"], complex)), axis=0)
    n_post = r - clean_original
    return {"clean_original": clean_original, "n_post": n_post}


# ---------------------------------------------------------------------------
# Passive PDL / fixed PSP component truth — FIXED across the frame (T005 §3.1)
# ---------------------------------------------------------------------------

def pdl_singular_values(pdl_db: float) -> np.ndarray:
    """PASSIVE PDL singular values: sigma_max=1, sigma_min=10^(-PDL/20).

    A passive component cannot amplify -> max transmissivity = 1.
    cond = 10^(PDL/20). (T004 defect #2 fix, inherited.)
    """
    return np.array([1.0, 10.0 ** (-pdl_db / 20.0)])


def _single_random_unitary(rng):
    """One 2x2 complex unitary via QR of complex Gaussian, QR-phase fixed."""
    A = (rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2)))
    q, r = np.linalg.qr(A)
    d = np.diag(r)
    return q * (d / np.abs(d))[None, :]


def build_fixed_jones_truth(rng, model_id, *, pdl_db=0.0):
    """Generate the ONE FIXED component Jones truth for the whole frame.

    M0  identity.
    M2  ONE fixed passive PDL Jones  J = U diag(1, 10^(-PDL/20)) Vh  (sigma_max=1).
    M3  ONE fixed PSP basis (U, Vh) + identity memoryless part; the memory comes
        from the fixed DGD in the PSP basis (see apply_component).
    """
    if model_id == "M0":
        return np.eye(2, dtype=complex)
    if model_id == "M2":
        U = _single_random_unitary(rng)
        V = _single_random_unitary(rng)
        sv = pdl_singular_values(pdl_db)
        return U @ np.diag(sv) @ V.conj().T
    if model_id == "M3":
        # memoryless part is identity; memory comes from the PMD FIR using the
        # FIXED PSP basis (U, Vh) of THIS one Jones. Store identity here so the
        # FFT-circular apply reduces to the PSP-basis differential delay.
        return np.eye(2, dtype=complex)
    raise ValueError(f"unknown model_id={model_id!r}")


def build_fixed_psp_truth(rng, model_id, *, pdl_db=0.0):
    """Generate the ONE FIXED PSP basis (U, Vh) truth for M3.

    For M3 the component channel is J(f) = U @ diag(1, exp(-j2pi f dgd)) @ Vh
    (sigma=[1,1], unitary, noise-preserving in the PSP basis). The basis is
    drawn ONCE and fixed across the frame (V039). Returns (U, Vh) or None for
    M0/M2 (no PSP memory).
    """
    if model_id != "M3":
        return None
    U = _single_random_unitary(rng)
    V = _single_random_unitary(rng)
    return U, V.conj().T


# ---------------------------------------------------------------------------
# Component channel operator: acts on a CLEAN (2, N) frame. FIXED across frame.
# Same operator for pilot and data. FFT-circular PMD convention (inherited).
# ---------------------------------------------------------------------------

PMD_GUARD = 8  # transient samples excluded at each block boundary


def _pmd_freq_operator(U, Vh, dgd_samples, nfft):
    """Per-frequency PMD operator J(f) = U diag(exp(-j2pi f tau)) Vh, tau=[+dgd/2,-dgd/2].

    sigma = [1, 1] (unitary in PSP basis at DGD>0 -> noise-preserving). Used by
    BOTH forward apply and the reference inverse, so they share ONE convention
    and are exact inverses modulo the block-boundary transient (PMD_GUARD).
    dgd=0 -> exp(0)=1 -> identity (limiting-case gate)."""
    f = np.fft.fftfreq(nfft)
    tau = dgd_samples * np.array([0.5, -0.5])
    Hf = np.empty((nfft, 2, 2), dtype=complex)
    phase = np.exp(-1j * 2.0 * np.pi * np.outer(f, tau))      # (nfft, 2)
    for fi in range(nfft):
        Hf[fi] = U @ np.diag(phase[fi]) @ Vh
    return Hf


def apply_component_fixed(clean_frame, jones_fixed, *, block_size, dgd_samples,
                          psp=None):
    """Apply the ONE FIXED component operator to a CLEAN (2, N) frame.

    For M0/M2 the fixed Jones multiplies every block identically.
    For M3 the fixed PSP basis + DGD convolves each block in the FFT-circular
    convention (same as the reference inverse). Noise is NEVER touched.
    """
    r = np.asarray(clean_frame, dtype=complex)
    N = r.shape[1]
    out = np.zeros_like(r)
    use_pmd = psp is not None and dgd_samples > 1e-12
    for b in range((N + block_size - 1) // block_size):
        s = b * block_size
        e = min(s + block_size, N)
        if e <= s:
            continue
        seg = r[:, s:e].copy()
        if use_pmd:
            L = e - s
            U, Vh = psp
            Hf = _pmd_freq_operator(U, Vh, dgd_samples, L)
            segf = np.fft.fft(seg, axis=1)
            out_f = np.einsum("fij,jf->if", Hf, segf)
            seg_out = np.fft.ifft(out_f, axis=1)
        else:
            seg_out = jones_fixed @ seg
        out[:, s:e] = seg_out
    return out


# ---------------------------------------------------------------------------
# Full impaired realization builder (fixed component)
# ---------------------------------------------------------------------------

def build_impaired_realization(realization, *, model_id, block_size, seed,
                               pdl_db=0.0, dgd_ps=0.0, t_s=4e-10):
    """Build the impaired realization with the FIXED component temporal model.

    Steps (T005 §3.1):
      1. separate canonical -> clean_original, n_post
      2. draw the ONE FIXED component Jones / PSP basis with the deterministic
         hash-free RNG seed (V039 fix)
      3. apply the fixed component operator to clean_original -> clean_component
      4. r_out = clean_component + n_post (SAME noise draw; noise untouched)
      5. store the fixed truth for the tagged reference
    """
    sep = separate_canonical(realization)
    clean_original = sep["clean_original"]
    n_post = sep["n_post"]
    N = clean_original.shape[1]

    # DETERMINISTIC seed (V039 fix): no hash()
    rng = np.random.default_rng(component_rng_seed(seed, model_id))
    jones_fixed = build_fixed_jones_truth(rng, model_id, pdl_db=pdl_db)
    psp = build_fixed_psp_truth(rng, model_id, pdl_db=pdl_db)

    pmd_enabled = model_id == "M3"
    dgd_samples = dgd_ps * 1e-12 / t_s if pmd_enabled else 0.0

    clean_component = apply_component_fixed(
        clean_original, jones_fixed, block_size=block_size,
        dgd_samples=dgd_samples, psp=psp)

    r_out = clean_component + n_post

    out = dict(realization)
    out["rX"] = r_out[0]
    out["rY"] = r_out[1]
    out["clean_original"] = clean_original
    out["n_post"] = n_post
    out["clean_component"] = clean_component
    out["jones_truth_fixed"] = jones_fixed
    out["psp_truth_fixed"] = psp
    out["model_id"] = model_id
    out["component_seed"] = component_rng_seed(seed, model_id)
    out["model_params"] = {
        "pdl_db": float(pdl_db), "dgd_ps": float(dgd_ps),
        "t_s": float(t_s), "block_size": int(block_size),
        "dgd_samples": float(dgd_samples), "pmd_enabled": bool(pmd_enabled),
        "cond_target": float(10.0 ** (pdl_db / 20.0)) if pdl_db > 0 else 1.0,
        "sigma_max": 1.0, "sigma_min": float(10.0 ** (-pdl_db / 20.0)),
    }
    return out


def report_insertion_loss(jones_fixed):
    """Passive PDL insertion-loss report (sigma_max=1 -> 0 dB insertion loss)."""
    sv = np.linalg.svd(jones_fixed[np.newaxis] if jones_fixed.ndim == 2 else jones_fixed,
                       compute_uv=False)
    sv = np.atleast_2d(sv)
    smax = float(sv[:, 0].mean())
    smin = float(sv[:, 1].mean())
    return {
        "sigma_max_mean": smax, "sigma_min_mean": smin,
        "insertion_loss_dB": float(-20.0 * np.log10(max(smax, 1e-12))),
        "cond": float(smax / max(smin, 1e-12)),
    }
