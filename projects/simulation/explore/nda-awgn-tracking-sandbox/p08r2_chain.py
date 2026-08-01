"""P08-R2 coded-chain repair module — fixes the three residual root causes
(H7/H8/H9) of D049 that D048/V074 missed.

P08-R (D048) fixed H1-H6 but left three承重 defects:
  H7 : CodedRealizationR.equalize() read self.gamma_bar (true SNR loop variable)
       in three places (blind-h noise floor :344, h_est :354, mmse_equalize :358).
       ⇒ deployable decide indirectly consumed true SNR via eq → prefix σ² → LLR.
  H8 : p08r_verify.py check #5 only scanned method_B0/B1/B2 function-body text
       for "real.gamma_bar", never recursing into real.equalize() → missed H7.
  H9 : MDE = post-hoc power threshold (fixed n then named it MDE); CI_lo=0
       treated as signal-absent; per-trajectory min(B1,B2) = cherry-pick.

This module (P08-R2) preserves the D048 PARTIAL reusable assets verbatim
(CodedContractR, CodecAdapterR, CalibrationPrefix, oracle ladder, get_gg_scenes,
H6 CodedRealizationR physics) and rewrites ONLY the receiver information-boundary
layer:

  H7 fix : estimate_pre_eq_noise_from_prefix() — receiver-visible pre-equalization
           noise variance σ²_pre via least-squares on the KNOWN 32-symbol prefix
           against a 2×2 effective channel (4 complex unknowns, 60 dof residual).
           CodedRealizationR2.equalize() uses σ²_pre (NOT gamma_bar) for the blind-h
           noise floor and passes γ_vis = 1/σ²_pre to mmse_equalize. amp_limit
           (fixed absolute clip, no γ read) is preserved unchanged.
  H8 fix : (verifier side — p08r2_verify.py) AST must recurse into the deployable
           call graph (method → real.equalize → mmse_equalize → estimate_*).
  H9 fix : (Phase A side — p08r2_phaseA.py / p08r2_run.py) MDE is a PRIORI-registered
           (graduation-value FER delta), not a post-hoc power threshold; CI_lo=0 is
           reported honestly as evidence_insufficient; per-trajectory min(B1,B2)
           removed in favour of a single pre-registered conventional comparator.

Physical generation (realize()) still consumes gamma_bar to draw noise — that is
legal (it is the channel, not the receiver). The receiver path (equalize + demap
+ decode) is now gamma_bar-free. The metamorphic information gate
(p08r2_metamorphic_gate.py) verifies this at runtime: flip the hidden gamma_bar,
assert deployable outputs do not change (Δ < tol).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import torch

torch.set_default_device("cpu")

_THIS_DIR = Path(__file__).resolve().parent
_SIM_ROOT = _THIS_DIR.parents[1]  # projects/simulation
if str(_SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(_SIM_ROOT))
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

# --- D048 PARTIAL reusable assets (verbatim re-import, NOT modified) ---------
from p08r_chain import (  # noqa: E402
    get_gg_scenes,                 # H1 fix: (α,β) from params.py single source
    CodedContractR,                # H5 fix: coded identity, option A interleaver
    CodecAdapterR,                 # H5 fix: LDPC5GEncoder(num_bits_per_symbol=4)
    CalibrationPrefix,             # H2 fix: frozen known-symbol prefix
    estimate_sigma2_from_prefix,   # receiver-visible POST-equalization σ² (demapper)
    oracle_sigma2_global,          # H3 fix: O0 global-truth oracle (scoring only)
    oracle_sigma2_block,           # H3 fix: O1 block-truth oracle
    oracle_sigma2_finer,           # H3 fix: O2 finer local-truth oracle
    split_prefix_data,
)
from common._equalizer import amp_limit, mmse_equalize  # noqa: E402 (frozen, not edited)
from common import qam16_mod  # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402


# =============================================================================
# H7 fix — receiver-visible PRE-equalization noise from prefix LS
# =============================================================================

def estimate_pre_eq_noise_from_prefix(
    rx_prefix_X: np.ndarray,
    rx_prefix_Y: np.ndarray,
    tx_prefix_X: np.ndarray,
    tx_prefix_Y: np.ndarray,
    floor: float = 1e-9,
) -> Tuple[float, np.ndarray]:
    """Receiver-visible PRE-equalization noise variance σ²_pre.

    Uses the KNOWN prefix symbols to solve a 2×2 effective-channel least-squares
    problem on the pre-equalization received samples, then takes the residual
    energy as the receiver-visible noise+residual scale. This is the ONLY
    pre-equalization noise source the deployable equalize() may read; it never
    touches gamma_bar / h_truth / theta.

    Model (per prefix symbol, before any equalization):
        [rX]   [h_xx h_xy] [sX]   [nX]
        [rY] = [h_yx h_yy] [sY] + [nY]
    where H_eff absorbs the SOP rotation θ and the GG amplitude √h (both unknown
    to the receiver). With N prefix symbols we have 2N complex equations in 4
    complex unknowns; for N=32 that is 64 equations, 60 dof residual.

    Returns
    -------
    sigma2_pre : float
        mean(|residual|²) over both polarizations — receiver-visible noise scale.
        Equal to 1/γ_vis where γ_vis is the receiver-visible SNR estimate.
    H_eff : (2,2) complex
        the estimated effective channel (returned for diagnostics / verifier).
    """
    # Stack: build (2N, 4) regressor matrix M and (2N,) observation vector r.
    # Row block 0 (X): rX = h_xx·sX + h_xy·sY
    # Row block 1 (Y): rY = h_yx·sX + h_yy·sY
    sX = np.asarray(tx_prefix_X, dtype=np.complex128).ravel()
    sY = np.asarray(tx_prefix_Y, dtype=np.complex128).ravel()
    rX = np.asarray(rx_prefix_X, dtype=np.complex128).ravel()
    rY = np.asarray(rx_prefix_Y, dtype=np.complex128).ravel()
    n = sX.size
    # Regressor: columns correspond to [h_xx, h_xy, h_yx, h_yy]
    M = np.zeros((2 * n, 4), dtype=np.complex128)
    M[:n, 0] = sX        # h_xx contribution to rX
    M[:n, 1] = sY        # h_xy contribution to rX
    M[n:, 2] = sX        # h_yx contribution to rY
    M[n:, 3] = sY        # h_yy contribution to rY
    r = np.concatenate([rX, rY])
    # Least-squares solve (4 unknowns, 2N equations). Uses lstsq for robustness
    # against ill-conditioning in deep-fade trajectories (h→0 ⇒ small r, but the
    # regressor M is built from KNOWN prefix symbols of unit power, so it stays
    # well-conditioned regardless of the channel realization).
    h_hat, residuals, rank, sv = np.linalg.lstsq(M, r, rcond=None)
    H_eff = np.array([[h_hat[0], h_hat[1]],
                      [h_hat[2], h_hat[3]]], dtype=np.complex128)
    r_hat = M @ h_hat
    resid = r - r_hat
    sigma2_pre = float(np.mean(np.abs(resid) ** 2))
    if sigma2_pre < floor:
        sigma2_pre = float(floor)
    return sigma2_pre, H_eff


def gamma_vis_from_prefix(sigma2_pre: float) -> float:
    """Receiver-visible SNR γ_vis = 1/σ²_pre for the mmse_equalize 3rd argument.

    mmse_equalize(rx, h, gamma_bar) treats its 3rd argument as SNR γ (the
    additive noise term in the denominator is 1/γ — see common/_equalizer.py:15).
    The receiver-visible replacement is therefore γ_vis = 1/σ²_pre, derived from
    the prefix LS residual, NOT from the loop variable gamma_bar.
    """
    return 1.0 / max(float(sigma2_pre), 1e-12)


# =============================================================================
# H7 fix — CodedRealizationR2: equalize() reads NO gamma_bar
# =============================================================================

@dataclass
class CodedRealizationR2:
    """One shared paired realization for P08-R2. Physics (h, θ, GG, noise) is
    generated ONCE via realize() using gamma_bar (legal — the channel knows the
    SNR it draws noise at). The RECEIVER path (equalize) is gamma_bar-free:
    pre-equalization noise comes from the prefix LS residual (σ²_pre).

    B0/B1/B2/O0/O1/O2 all consume the SAME realization. Calibration prefix is
    prepended to the TX frame; equalize() uses it to estimate σ²_pre; the scored
    codeword does NOT feed back into calibration (H2 fairness preserved).
    """
    seed: int
    scene: str
    alpha: float
    beta: float
    f_g: float
    sop_rate: float
    gamma_bar: float            # loop variable — used ONLY by realize() (physics)
    n_cw_per_pol: int
    cw_n: int
    codec: CodecAdapterR
    prefix: CalibrationPrefix
    eval_block: int = 100

    # populated by realize()
    rX: np.ndarray = None
    rY: np.ndarray = None
    sX: np.ndarray = None
    sY: np.ndarray = None
    h: np.ndarray = None
    theta: np.ndarray = None
    cw_info_X: np.ndarray = None
    cw_info_Y: np.ndarray = None
    cw_bits_X: np.ndarray = None
    cw_bits_Y: np.ndarray = None
    # populated by equalize() — receiver-visible estimates (NO gamma_bar read)
    sigma2_pre: float = None
    h_eff_estimate: np.ndarray = None

    @property
    def n_prefix(self) -> int:
        return self.prefix.n_prefix_symbols

    @property
    def n_sym_scored_per_pol(self) -> int:
        return self.n_cw_per_pol * (self.cw_n // 4)

    def realize(self, info_rng_seed_offset: int = 0) -> "CodedRealizationR2":
        """Generate TX codewords, prepend frozen prefix, run shared dual-pol SOP
        channel (h/θ/GG/noise from gamma_bar). gamma_bar is consumed HERE ONLY
        (channel physics, legal). Stored arrays are the input to the gamma_bar-free
        equalize()."""
        n_sym_data = self.n_sym_scored_per_pol
        n_sym_total = self.n_prefix + n_sym_data
        rng = np.random.default_rng(self.seed * 1000003 + 17 + info_rng_seed_offset)
        info_X = rng.integers(0, 2, size=(self.n_cw_per_pol, self.codec._k)).astype(np.uint8)
        info_Y = rng.integers(0, 2, size=(self.n_cw_per_pol, self.codec._k)).astype(np.uint8)
        cw_bits_X = self.codec.encode(info_X)
        cw_bits_Y = self.codec.encode(info_Y)
        sX_data = qam16_mod(cw_bits_X.reshape(-1))
        sY_data = qam16_mod(cw_bits_Y.reshape(-1))
        prefix_syms = self.prefix.symbols()
        sX = np.concatenate([prefix_syms, sX_data])
        sY = np.concatenate([prefix_syms.copy(), sY_data])
        base = generate_shared_realization_dp(
            N=n_sym_total, alpha=self.alpha, beta=self.beta, f_g=self.f_g,
            sop_rate=self.sop_rate, seed=self.seed, gamma_bar=self.gamma_bar,
            modulation="qam16",
        )
        h = base["h"]; theta = base["theta"]
        nv = 1.0 / (2.0 * self.gamma_bar)   # LEGAL: physical noise draw (channel side)
        cos_t = np.cos(theta); sin_t = np.sin(theta)
        nrng = np.random.default_rng(self.seed + 1_000_003)
        rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) + np.sqrt(nv) * (
            nrng.standard_normal(n_sym_total) + 1j * nrng.standard_normal(n_sym_total))
        rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) + np.sqrt(nv) * (
            nrng.standard_normal(n_sym_total) + 1j * nrng.standard_normal(n_sym_total))
        self.rX, self.rY = rX, rY
        self.sX, self.sY = sX, sY
        self.h, self.theta = h, theta
        self.cw_info_X, self.cw_info_Y = info_X, info_Y
        self.cw_bits_X, self.cw_bits_Y = cw_bits_X, cw_bits_Y
        return self

    def equalize(self) -> Dict[str, np.ndarray]:
        """Per-block MMSE + amp_limit equalization. H7 FIX: the pre-equalization
        noise floor is the RECEIVER-VISIBLE σ²_pre from the prefix LS residual,
        NOT 1/(2·gamma_bar). The MMSE 3rd argument is γ_vis = 1/σ²_pre. amp_limit
        (fixed absolute clip, no γ) is preserved.

        This function reads NO gamma_bar / h_truth / theta / sX / sY (other than
        the KNOWN prefix symbols, which the receiver legitimately knows). The
        metamorphic information gate verifies this: flipping self.gamma_bar after
        realize() must not change any output here."""
        n_prefix = self.n_prefix
        # --- receiver-visible pre-equalization noise from prefix LS (H7 fix) ---
        rxpX, _ = split_prefix_data(self.rX, n_prefix)
        rxpY, _ = split_prefix_data(self.rY, n_prefix)
        sxp, _ = split_prefix_data(self.sX, n_prefix)   # KNOWN prefix (receiver-known)
        syp, _ = split_prefix_data(self.sY, n_prefix)
        sigma2_pre, H_eff = estimate_pre_eq_noise_from_prefix(
            rxpX, rxpY, sxp, syp)
        gamma_vis = gamma_vis_from_prefix(sigma2_pre)
        # store receiver-visible estimates for verifier / diagnostics
        self.sigma2_pre = sigma2_pre
        self.h_eff_estimate = H_eff
        # --- per-block blind h estimate using σ²_pre (NOT 1/(2·gamma_bar)) ---
        block = self.eval_block
        n = self.rX.size

        def per_block_h(rx, noise_floor):
            h_est = np.empty(n)
            nb = int(np.ceil(n / block))
            for i in range(nb):
                sl = slice(i * block, min((i + 1) * block, n))
                p = float(np.mean(np.abs(rx[sl]) ** 2))
                h_est[sl] = max(p - noise_floor, 1e-6)
            return h_est

        hX = per_block_h(self.rX, sigma2_pre)
        hY = per_block_h(self.rY, sigma2_pre)
        # --- MMSE equalize with γ_vis (NOT gamma_bar); amp_limit absolute clip ---
        eqX = amp_limit(mmse_equalize(self.rX, hX, gamma_vis), 3.0)
        eqY = amp_limit(mmse_equalize(self.rY, hY, gamma_vis), 3.0)
        return {"eqX": eqX, "eqY": eqY, "h_use_X": hX, "h_use_Y": hY,
                "sigma2_pre": sigma2_pre, "gamma_vis": gamma_vis}


__all__ = [
    # re-exported D048 PARTIAL assets (unchanged)
    "get_gg_scenes", "CodedContractR", "CodecAdapterR", "CalibrationPrefix",
    "estimate_sigma2_from_prefix",
    "oracle_sigma2_global", "oracle_sigma2_block", "oracle_sigma2_finer",
    "split_prefix_data",
    # P08-R2 H7 fix
    "estimate_pre_eq_noise_from_prefix", "gamma_vis_from_prefix",
    "CodedRealizationR2",
]
