"""P08-R coded-chain repair module — fixes the six root causes (H1-H6) of D048.

This module is the SCIENCE_INTEGRITY_REPAIR chain for P08 (per user P08-R execution
instruction + D048). It does NOT modify the old p08_*.py files (those remain as
INVALIDATED audit artifacts). It imports only the *correct* parts of the old chain
(constellation/demap, CodecAdapter skeleton, source_receipt) and rewrites the
defective parts:

  H1 GG provenance      : (α,β) imported from SimulationConfig.get_turb_dict()
                          (params.py single source of truth), never hardcoded.
  H2 runtime information: deployable σ² comes from a frozen calibration prefix of
                          KNOWN symbols (receiver-visible), NOT from the loop
                          variable γ_bar. true γ/h/θ/TX-residual never enter decide.
  H3 oracle action space: O0 (global-truth) / O1 (codeword-block-truth) / O2
                          (finer local-truth) ladder; action space ⊇ candidate.
  H4 metric contract    : dev workspace first to find an achievable SNR/FER region,
                          then freeze test; Primary A (req-SNR@FER) only if all
                          methods cross in the sweep, else pre-frozen Primary B
                          (fixed-SNR paired FER); MDE mapped explicitly, never
                          silent fallback.
  H5 coded identity     : LDPC5GEncoder(..., num_bits_per_symbol=4) enables the
                          real 3GPP §5.4.2.2 sub-block + triangle bit interleaver.
                          Identity frozen (option A) before test.
  H6 state lifecycle    : statistical unit = trajectory/seed cluster (not codeword);
                          raw stores per-trajectory + per-codeword h/fade/pre-BER/
                          FER/iterations; evaluation-only truth fields flagged.

All deployable baselines share: same code/rate, same calibration overhead, same
interleaver (option A), same decoder, same iteration budget, same net information
rate, same paired realization. TX truth is used ONLY for BER/FER/NLL scoring and
for the PRIVILEGED oracle ladder (O0/O1/O2, scoring/headroom only, never Go).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch

torch.set_default_device("cpu")

# --- import correct parts of the old chain (constellation/demap) -------------
_THIS_DIR = Path(__file__).resolve().parent
_SIM_ROOT = _THIS_DIR.parents[1]  # projects/simulation
if str(_SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(_SIM_ROOT))
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from p08_coded_chain import (  # noqa: E402  (reuse correct constellation/demap)
    _build_qam16_constellation,
    maxlog_soft_demap_16qam,
    _qam16_demod_to_bits,
)
from common import qam16_mod  # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
from common._equalizer import amp_limit, mmse_equalize  # noqa: E402

from sionna.phy.fec.ldpc import (  # noqa: E402
    LDPC5GEncoder,
    LDPC5GDecoder,
    cn_update_offset_minsum,
)

from params import SimulationConfig  # noqa: E402  (H1 single source of truth)


# =============================================================================
# H1 fix — GG (α,β) from params.py single source of truth
# =============================================================================

def get_gg_scenes() -> Dict[str, Tuple[float, float]]:
    """Return weak/moderate/strong (α,β) from params.py (H1 fix).

    This is the ONLY place P08-R reads (α,β). Scripts must not hardcode these.
    """
    return SimulationConfig().get_turb_dict()


# =============================================================================
# H5 fix — coded identity with real 3GPP bit interleaver (option A, frozen)
# =============================================================================

@dataclass
class CodedContractR:
    """Frozen coded contract for P08-R (identity = option A, interleaver ON)."""
    standard: str = "3GPP TS 38.212 5G NR LDPC"
    bg: str = "bg2"
    k: int = 1024           # info bits per codeword
    n: int = 1536           # on-air coded bits per codeword (rate 2/3)
    rate: float = field(init=False)
    encoder_type: str = "LDPC5GEncoder systematic"
    decoder_algo: str = "normalized-min-sum"
    alpha: float = 0.75     # decoder normalization
    num_iter: int = 20
    llr_max: float = 20.0
    offset: float = 0.0
    llr_clip: float = 30.0
    sign_convention: str = "logit=log(p(b=1)/p(b=0)); BPSK x=1-2b => logit=-2y/sigma2"
    modulation: str = "16QAM Gray BICM"
    bits_per_symbol: int = 4
    # H5 fix: interleaver identity is now the REAL 3GPP §5.4.2.2 sub-block + triangle
    interleaver: str = ("3GPP TS 38.212 §5.4.2.2 sub-block + triangle bit interleaver "
                        "(num_bits_per_symbol=4, enabled via LDPC5GEncoder)")
    interleaver_enabled: bool = True  # option A frozen (see p08r_identity_freeze.md)
    net_rate: float = field(init=False)
    note: str = (
        "5G NR BG2 rate-matched LDPC component + Gray-16QAM BICM with the real "
        "3GPP §5.4.2.2 bit interleaver. Generic FSO BICM standard baseline; all "
        "methods share this code; code choice is a baseline limitation, not an "
        "innovation. NOT satellite-specific DVB-S2."
    )

    def __post_init__(self) -> None:
        self.rate = self.k / self.n
        self.net_rate = self.rate  # no outer code


class CodecAdapterR:
    """Codec adapter with H5 fix: num_bits_per_symbol=4 enables 3GPP interleaver."""

    def __init__(self, contract: CodedContractR) -> None:
        self.contract = contract
        # H5 fix key change: pass num_bits_per_symbol=bits_per_symbol
        self.enc = LDPC5GEncoder(
            k=contract.k,
            n=contract.n,
            num_bits_per_symbol=contract.bits_per_symbol,  # <-- H5 fix
        )
        # normalized-min-sum with optional offset (matches the proven old-P08 pattern)
        alpha = contract.alpha

        def cn_update(msg_v2c, mask, llr_clipping=None):
            return alpha * cn_update_offset_minsum(
                msg_v2c, mask, llr_clipping, offset=contract.offset
            )

        self.dec = LDPC5GDecoder(
            self.enc, num_iter=contract.num_iter, cn_update=cn_update,
            hard_out=True, llr_max=contract.llr_max,
        )
        self._k = contract.k
        self._n = contract.n
        # expose interleaver permutation for verifier
        self.out_int = np.asarray(self.enc.out_int.cpu()) if self.enc._num_bits_per_symbol is not None else None
        self.out_int_inv = np.asarray(self.enc.out_int_inv.cpu()) if self.enc._num_bits_per_symbol is not None else None

    def encode(self, info_bits: np.ndarray) -> np.ndarray:
        """info_bits (B,k) uint8 -> codeword (B,n) uint8 (on-air, interleaved)."""
        u = torch.tensor(np.asarray(info_bits).astype(np.uint8))
        c = self.enc(u).cpu().numpy().astype(np.uint8)
        return c

    def decode(self, llr: np.ndarray):
        """llr (B,n) float -> (info_hat (B,k) uint8, diag dict). llr is in the
        on-air (post-interleave) cw bit order; the decoder applies out_int_inv
        internally. diag carries per-cw iteration/convergence if available."""
        llr_t = torch.tensor(np.asarray(llr, dtype=np.float32))
        llr_t = torch.clamp(llr_t, -self.contract.llr_max, self.contract.llr_max)
        out = self.dec(llr_t)
        if isinstance(out, tuple):
            uhat, state = out
        else:
            uhat, state = out, None
        uhat = uhat.cpu().numpy().astype(np.uint8)
        diag = {"num_iter_configured": self.contract.num_iter}
        if state is not None:
            try:
                # sionna may return iteration count per cw
                iters = state.cpu().numpy() if hasattr(state, "cpu") else np.asarray(state)
                diag["iterations_per_cw"] = iters.tolist() if hasattr(iters, "tolist") else iters
            except Exception:
                pass
        return uhat, diag


# =============================================================================
# H2 fix — receiver-visible σ² from a frozen calibration prefix
# =============================================================================

@dataclass
class CalibrationPrefix:
    """A frozen, modulation-format known-symbol prefix prepended to every TX frame.
    All methods share the SAME prefix length and symbols, so the calibration
    overhead is identical across methods (fairness). The prefix is generated from
    a deterministic PN sequence (not from TX info bits) and is KNOWN to the
    receiver. It is used ONLY to estimate a receiver-visible noise scale; it must
    NOT be used to carry information, and the scored codeword MUST NOT feed back
    into its own calibration.
    """
    n_prefix_symbols: int = 32  # frozen; same for all methods
    seed: int = 987654321       # deterministic PN; same across all realizations

    def symbols(self) -> np.ndarray:
        """Return the frozen prefix symbols (complex, 16QAM Gray, avg power 1)."""
        rng = np.random.default_rng(self.seed)
        bits = rng.integers(0, 2, size=self.n_prefix_symbols * 4).astype(np.uint8)
        return qam16_mod(bits)


def estimate_sigma2_from_prefix(
    rx_prefix: np.ndarray, tx_prefix: np.ndarray
) -> float:
    """Receiver-visible global noise scale from the known calibration prefix.

    resid = rx_prefix - tx_prefix (after equalization). The complex variance
    mean(|resid|^2) is the receiver-visible estimate of the post-equalization
    noise+residual scale. This is the ONLY σ² source for deployable baselines
    (B0/B1/B2): they never read the loop variable γ_bar.
    """
    resid = rx_prefix - tx_prefix
    return float(np.mean(np.abs(resid) ** 2))


# =============================================================================
# H3 fix — privileged oracle ladder (O0/O1/O2), scoring/headroom only
# =============================================================================

def oracle_sigma2_global(eq: np.ndarray, s_true: np.ndarray) -> float:
    """O0 global-truth oracle: one scalar = mean(|eq - s_true|^2) over the whole
    scored window. Same granularity as the deployable global σ² but uses TX truth.
    PRIVILEGED — scoring/headroom only, never deployable."""
    return float(np.mean(np.abs(eq - s_true) ** 2))


def oracle_sigma2_block(eq: np.ndarray, s_true: np.ndarray, block: int) -> np.ndarray:
    """O1 codeword/block-truth oracle: per-block residual scale, where the block
    size equals the smallest calibration partition the deployable candidates are
    allowed to use. Returns an array (one scalar per block) broadcastable to sym.
    PRIVILEGED — scoring/headroom only."""
    n = eq.size
    nb = int(np.ceil(n / block))
    sig = np.empty(n, dtype=np.float64)
    for i in range(nb):
        sl = slice(i * block, min((i + 1) * block, n))
        resid = eq[sl] - s_true[sl]
        sig[sl] = float(np.mean(np.abs(resid) ** 2))
    return sig


def oracle_sigma2_finer(eq: np.ndarray, s_true: np.ndarray, block: int) -> np.ndarray:
    """O2 finer/local-truth bound: a pre-frozen finer partition than O1, used as
    the heteroscedastic calibration upper bound. PRIVILEGED — scoring/headroom
    only, never deployable. (block here is smaller than O1's block.)"""
    return oracle_sigma2_block(eq, s_true, block)


# =============================================================================
# H6 fix — shared realization with per-trajectory + per-cw evidence, calibration
#           prefix injected once and shared across all methods (no seed change)
# =============================================================================

@dataclass
class CodedRealizationR:
    """One shared paired realization for P08-R. Physics (h, θ, GG, noise) is
    generated ONCE; B0/B1/B2/O0/O1/O2 all consume the SAME realization. Different
    methods do NOT change seed. Calibration prefix is prepended to the TX frame,
    equalized, and used for receiver-visible σ²; the scored codeword does NOT
    feed back into calibration (H2 fix).
    """
    seed: int
    scene: str                  # weak/moderate/strong (label; α,β from params)
    alpha: float
    beta: float
    f_g: float
    sop_rate: float
    gamma_bar: float            # loop variable, used ONLY to generate noise (physics)
    n_cw_per_pol: int           # codewords per polarization (shared fade)
    cw_n: int                   # coded bits per codeword (= contract.n)
    codec: CodecAdapterR
    prefix: CalibrationPrefix
    eval_block: int = 100       # block size for equalize + O1 oracle partition

    # populated by realize()
    rX: np.ndarray = None       # full received X incl prefix
    rY: np.ndarray = None
    sX: np.ndarray = None       # TX symbols X incl prefix (truth, scoring only)
    sY: np.ndarray = None
    h: np.ndarray = None
    theta: np.ndarray = None
    cw_info_X: np.ndarray = None   # (n_cw, k) TX info bits X (scoring only)
    cw_info_Y: np.ndarray = None
    cw_bits_X: np.ndarray = None   # (n_cw, n) TX coded bits X (scoring only)
    cw_bits_Y: np.ndarray = None

    @property
    def n_prefix(self) -> int:
        return self.prefix.n_prefix_symbols

    @property
    def n_sym_scored_per_pol(self) -> int:
        return self.n_cw_per_pol * (self.cw_n // 4)

    def realize(self, info_rng_seed_offset: int = 0) -> "CodedRealizationR":
        """Generate TX codewords (deterministic info bits from seed), prepend the
        frozen calibration prefix, run through the SHARED dual-pol SOP channel
        (h/θ/GG/noise from gamma_bar), store per-trajectory + per-cw evidence."""
        n_sym_data = self.n_sym_scored_per_pol
        n_sym_total = self.n_prefix + n_sym_data
        # 1) TX codewords (deterministic info bits; same for X and Y but drawn
        #    from independent streams so the two polarizations carry different data)
        rng = np.random.default_rng(self.seed * 1000003 + 17 + info_rng_seed_offset)
        info_X = rng.integers(0, 2, size=(self.n_cw_per_pol, self.codec._k)).astype(np.uint8)
        info_Y = rng.integers(0, 2, size=(self.n_cw_per_pol, self.codec._k)).astype(np.uint8)
        cw_bits_X = self.codec.encode(info_X)  # (n_cw, n) on-air bits (interleaved)
        cw_bits_Y = self.codec.encode(info_Y)
        # 2) data symbols per pol (flatten cw -> symbols)
        sX_data = qam16_mod(cw_bits_X.reshape(-1))  # (n_sym_data,)
        sY_data = qam16_mod(cw_bits_Y.reshape(-1))
        # 3) prepend the SAME frozen prefix to both pol (known to receiver)
        prefix_syms = self.prefix.symbols()
        sX = np.concatenate([prefix_syms, sX_data])
        sY = np.concatenate([prefix_syms.copy(), sY_data])
        # 4) shared dual-pol SOP channel physics (h, θ, GG, noise) — ONE draw
        base = generate_shared_realization_dp(
            N=n_sym_total, alpha=self.alpha, beta=self.beta, f_g=self.f_g,
            sop_rate=self.sop_rate, seed=self.seed, gamma_bar=self.gamma_bar,
            modulation="qam16",
        )
        h = base["h"]; theta = base["theta"]
        nv = 1.0 / (2.0 * self.gamma_bar)
        cos_t = np.cos(theta); sin_t = np.sin(theta)
        # noise drawn from an independent stream (offset) so coded != base bit-identical,
        # but ALL methods in this realization share the SAME noise (paired).
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
        """Per-block MMSE + amp_limit equalization, receiver-visible per-block h.
        Returns eqX/eqY over the FULL window (prefix+data)."""
        nv = 1.0 / (2.0 * self.gamma_bar)  # physics noise floor, used only for blind h est
        block = self.eval_block
        n = self.rX.size

        def per_block_h(rx):
            h_est = np.empty(n)
            nb = int(np.ceil(n / block))
            for i in range(nb):
                sl = slice(i * block, min((i + 1) * block, n))
                p = float(np.mean(np.abs(rx[sl]) ** 2))
                h_est[sl] = max(p - nv, 1e-6)
            return h_est

        hX = per_block_h(self.rX); hY = per_block_h(self.rY)
        eqX = amp_limit(mmse_equalize(self.rX, hX, self.gamma_bar), 3.0)
        eqY = amp_limit(mmse_equalize(self.rY, hY, self.gamma_bar), 3.0)
        return {"eqX": eqX, "eqY": eqY, "h_use_X": hX, "h_use_Y": hY}


def split_prefix_data(arr: np.ndarray, n_prefix: int):
    """Split a full-window array into (prefix_part, data_part)."""
    return arr[:n_prefix], arr[n_prefix:]


__all__ = [
    "get_gg_scenes", "CodedContractR", "CodecAdapterR",
    "CalibrationPrefix", "estimate_sigma2_from_prefix",
    "oracle_sigma2_global", "oracle_sigma2_block", "oracle_sigma2_finer",
    "CodedRealizationR", "split_prefix_data",
]
