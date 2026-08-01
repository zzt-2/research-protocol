"""P08 coded-chain sandbox: 5G NR LDPC + 16QAM BICM over dual-pol SOP channel.

Frozen contract (D047 / step-036 worker-log):
  - code: 3GPP TS 38.212 5G NR LDPC, BG2, rate 2/3 (k=1024 info, n=1536 on-air)
  - modulation: 16QAM Gray BICM (common._modulation.qam16_mod, avg power 1)
  - channel: dual-pol SOP (common._dual_pol_channel physics: GG amplitude h +
    Jones rotation theta + complex AWGN var = 1/(2*gamma_bar))
  - receiver: blind/pilot per-block MMSE + amp_limit + decide (modulation-agnostic,
    reused) + qam16 max-log LLR (soft_demap, sigma2=1/(2*gamma_bar)) + LDPC decode
  - decoder: normalized min-sum, alpha=0.75, 20 iter, llr_max=20, no early stop

This module is self-contained: it imports the frozen common path read-only and
adds the coded layer. It does NOT modify common/, params, or any P01-P07 file.
TX truth is used ONLY for BER/FER scoring, never for the deployable decide/LLR.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np
import torch

# --- codec (sionna 5G NR LDPC) -----------------------------------------------
from sionna.phy.fec.ldpc import (
    LDPC5GEncoder,
    LDPC5GDecoder,
    cn_update_offset_minsum,
)

# --- frozen common path (read-only reuse) ------------------------------------
import sys

_SIM_ROOT = Path(__file__).resolve().parents[2]  # projects/simulation
if str(_SIM_ROOT) not in sys.path:
    sys.path.insert(0, str(_SIM_ROOT))

from common import qam16_mod, qam16_demod  # noqa: E402
from common._dual_pol_channel import generate_shared_realization_dp  # noqa: E402
from common._equalizer import amp_limit, mmse_equalize  # noqa: E402

# soft demapper lives in the thesis-fso scout; vendor its table inline to avoid
# the cross-tree import and keep the constellation byte-identical (verified by
# the explore report: same gray_map, same /sqrt(10), same [b0,b1,b2,b3] order).
_SQRT10 = np.sqrt(10.0)
_GRAY_AXIS = np.array([-3.0, -1.0, 3.0, 1.0])  # reflection Gray: 00,01,11,10
_INV_SQRT10 = 1.0 / _SQRT10


def _build_qam16_constellation() -> tuple[np.ndarray, np.ndarray]:
    """Return (constellation[16], bits_table[16,4]) indexed by integer label = 4*bi + bq,
    where bi=2*b0+b1 (I index), bq=2*b2+b3 (Q index). EXACTLY reproduces
    common.qam16_mod: si=_GRAY_AXIS[bi], sq=_GRAY_AXIS[bq], s=(si+1j*sq)/sqrt(10).
    """
    pts = []
    bits_table = []
    for bi in range(4):
        for bq in range(4):
            s = (_GRAY_AXIS[bi] + 1j * _GRAY_AXIS[bq]) * _INV_SQRT10
            pts.append(s)
            # decode bi -> (b0,b1), bq -> (b2,b3) via inverse Gray: index 0,1,3,2 -> bits 00,01,11,10
            gray_inv = {0: (0, 0), 1: (0, 1), 3: (1, 1), 2: (1, 0)}
            b0, b1 = gray_inv[bi]
            b2, b3 = gray_inv[bq]
            bits_table.append([b0, b1, b2, b3])
    return np.array(pts), np.array(bits_table, dtype=np.uint8)


_CONST, _CONST_BITS = _build_qam16_constellation()
# _CONST_BITS[label] = [b0,b1,b2,b3]; label = 4*bi + bq


def _bits_to_labels(bits: np.ndarray) -> np.ndarray:
    """[b0,b1,b2,b3] per sym -> integer label = 4*(2*b0+b1) + (2*b2+b3)."""
    b = bits.reshape(-1, 4)
    bi = 2 * b[:, 0] + b[:, 1]
    bq = 2 * b[:, 2] + b[:, 3]
    return (4 * bi + bq).astype(np.int64)


def maxlog_soft_demap_16qam(z: np.ndarray, sigma2: float, llr_clip: float = 30.0) -> np.ndarray:
    """Max-log 16QAM LLR. Matches soft_demap.maxlog_soft_demap_16qam convention.

    LLR_k = min_{s: bit_k=0} |z-s|^2/(2 sigma2) - min_{s: bit_k=1} |z-s|^2/(2 sigma2)
    LLR_k >= 0  =>  bit k = 1 more likely.
    Returns (N, 4) float32. Bit order [b0,b1,b2,b3] matches qam16_mod.
    """
    sigma2 = float(sigma2)
    if sigma2 <= 0:
        raise ValueError("sigma2 must be positive")
    z = np.asarray(z).ravel()
    n = z.size
    d2 = np.abs(z[:, None] - _CONST[None, :]) ** 2  # (N,16)
    llrs = np.empty((n, 4), dtype=np.float64)
    bit_of_label = _CONST_BITS  # (16,4): bit_of_label[label, k] = bit k of point `label`
    scale = 1.0 / (2.0 * sigma2)
    for k in range(4):
        zero_mask = bit_of_label[:, k] == 0  # (16,)
        one_mask = ~zero_mask
        min_zero = np.min(d2[:, zero_mask], axis=1)
        min_one = np.min(d2[:, one_mask], axis=1)
        llr_k = (min_zero - min_one) * scale
        llrs[:, k] = np.clip(llr_k, -llr_clip, llr_clip)
    return llrs.astype(np.float32)


# --- coded contract ----------------------------------------------------------


@dataclass
class CodedContract:
    standard: str = "3GPP TS 38.212 5G NR LDPC"
    bg: str = "bg2"
    k: int = 1024  # info bits per codeword
    n: int = 1536  # on-air coded bits per codeword (rate 2/3)
    rate: float = field(init=False)
    encoder_type: str = "LDPC5GEncoder systematic"
    decoder_algo: str = "normalized-min-sum"
    alpha: float = 0.75
    num_iter: int = 20
    llr_max: float = 20.0
    offset: float = 0.0
    llr_clip: float = 30.0
    sign_convention: str = "logit=log(p(b=1)/p(b=0)); BPSK x=1-2b => logit=-2y/sigma2"
    modulation: str = "16QAM Gray BICM"
    bits_per_symbol: int = 4
    net_rate: float = field(init=False)
    note: str = (
        "5G NR LDPC BICM component (NOT satellite DVB-S2); generic FSO BICM "
        "standard baseline; all methods share this code; code choice is a "
        "baseline limitation, not an innovation."
    )

    def __post_init__(self) -> None:
        self.rate = self.k / self.n
        self.net_rate = self.rate  # no outer code; 16QAM does not change code rate

    def to_dict(self) -> dict:
        d = asdict(self)
        d["constellation_avg_power"] = 1.0
        return d


# --- codec adapter -----------------------------------------------------------


class CodecAdapter:
    """Wrap sionna 5G NR LDPC encoder + normalized-min-sum decoder.

    Bit convention: sionna consumes/returns bits as float in {0,1}, shape (B, k)
    and (B, n). LLR input to decoder = logit = log(p(b=1)/p(b=0)).
    """

    def __init__(self, contract: CodedContract, device: str = "cpu") -> None:
        self.c = contract
        self.device = device
        self.enc = LDPC5GEncoder(k=contract.k, n=contract.n)
        alpha = contract.alpha

        def cn_update(msg_v2c, mask, llr_clipping=None):
            return alpha * cn_update_offset_minsum(
                msg_v2c, mask, llr_clipping, offset=contract.offset
            )

        self._cn_update = cn_update
        self.dec = LDPC5GDecoder(
            self.enc,
            num_iter=contract.num_iter,
            cn_update=cn_update,
            hard_out=True,
            llr_max=contract.llr_max,
        )
        # record lifted-graph identity for the contract receipt
        self._dev = self.enc._pcm_a_ind.device
        self._z = int(self.enc._z)
        self._bg = str(self.enc._bg)
        self._k_ldpc = int(self.enc.k_ldpc)
        self._n_ldpc = int(self.enc.n_ldpc)

    def encode(self, info_bits: np.ndarray) -> np.ndarray:
        """info_bits (B, k) uint8/{0,1} -> codeword (B, n) uint8."""
        dev = self._dev
        u = torch.as_tensor(info_bits, dtype=torch.float32)
        if u.dim() == 1:
            u = u.unsqueeze(0)
        u = u.to(dev)
        c = self.enc(u)
        return c.detach().cpu().numpy().astype(np.uint8)

    def syndrome_check(self, codeword_full: np.ndarray) -> int:
        """Check H @ c = 0 on the FULL lifted codeword (n_ldpc cols). Returns |Hc|."""
        from scipy.sparse import csr_matrix

        H = csr_matrix(self.enc.pcm)
        c = np.asarray(codeword_full, dtype=np.uint8).ravel()
        return int(((H @ c) % 2).sum())

    def encode_full_for_syndrome(self, info_bits: np.ndarray) -> np.ndarray:
        """Return the full lifted codeword (n_ldpc) incl filler + 2Z punctured cols."""
        # sionna moves its internal gather indices onto its detected device
        # (cuda:0 here). Send the input to the same device as enc.pcm, then
        # bring the result back to CPU for the syndrome check.
        dev = self._dev
        u = torch.as_tensor(info_bits, dtype=torch.float32)
        if u.dim() == 1:
            u = u.unsqueeze(0)
        u = u.to(dev)
        k = self.c.k
        u_fill = torch.cat(
            [u, torch.zeros(u.shape[0], self._k_ldpc - k, device=dev)], dim=1
        )
        c_full = self.enc._encode_fast(u_fill.to(self.enc.dtype))
        return c_full.reshape(u.shape[0], self._n_ldpc).detach().cpu().numpy().astype(np.uint8)

    def decode(self, llr: np.ndarray) -> tuple[np.ndarray, dict]:
        """llr (B, n) logit convention -> (info_hat (B,k) uint8, diag dict)."""
        dev = self._dev
        llr_t = torch.as_tensor(llr, dtype=torch.float32)
        if llr_t.dim() == 1:
            llr_t = llr_t.unsqueeze(0)
        llr_t = llr_t.to(dev)
        # clamp input to llr_max (decoder also clips internally; do both for clarity)
        llr_t = torch.clamp(llr_t, -self.c.llr_max, self.c.llr_max)
        u_hat = self.dec(llr_t)
        if u_hat.dim() == 1:
            u_hat = u_hat.unsqueeze(0)
        info_hat = u_hat.detach().cpu().numpy().astype(np.uint8)
        # sionna decoder does not expose iteration count / convergence flag for the
        # hard-out path; we record num_iter as configured and convergence as N/A.
        diag = {
            "num_iter_configured": self.c.num_iter,
            "convergence_flag": "N/A (hard_out; sionna runs fixed iter)",
        }
        return info_hat, diag


# --- coded realization adapter ----------------------------------------------


class CodedRealizationAdapter:
    """Inject per-pol 16QAM-mapped codeword symbols into the dual-pol SOP channel.

    Physics is byte-identical to generate_shared_realization_dp(modulation='qam16'):
    same h (GG AR(1) envelope), same theta (SOP rotation ramp), same complex AWGN
    variance nv = 1/(2*gamma_bar). The only substitution is the TX symbols: instead
    of the generator's internally-drawn random bits, we feed qam16_mod(codeword_X)
    and qam16_mod(codeword_Y).

    To keep the physics byte-identical we re-derive rX/rY from the SAME h/theta and
    advance the RNG in the SAME order as the original generator (draw bitsX, bitsY,
    then 4 standard_normal draws for noise). We do this by calling the original
    generator with modulation='qam16' to obtain h/theta, then reconstructing rX/rY
    with our own symbols but the original noise stream advanced identically.
    """

    def __init__(
        self,
        alpha: float,
        beta: float,
        f_g: float,
        sop_rate: float,
        gamma_bar: float,
        seed: int,
        n_symbols: int,
    ) -> None:
        self.alpha = alpha
        self.beta = beta
        self.f_g = f_g
        self.sop_rate = sop_rate
        self.gamma_bar = gamma_bar
        self.seed = seed
        self.n_symbols = n_symbols
        # Materialize the physics once (h, theta). We use the generator output and
        # then re-derive noise with a fresh rng seeded identically but advanced
        # past the bit-draws, to guarantee the same noise stream the original would
        # have produced.
        base = generate_shared_realization_dp(
            N=n_symbols,
            alpha=alpha,
            beta=beta,
            f_g=f_g,
            sop_rate=sop_rate,
            seed=seed,
            gamma_bar=gamma_bar,
            modulation="qam16",
        )
        self.h = base["h"]
        self.theta = base["theta"]
        # sanity: confirm avg symbol power ~1 for the generator's own symbols
        self._base = base

    def realize(self, codeword_bits_X: np.ndarray, codeword_bits_Y: np.ndarray) -> dict:
        """codeword_bits_X/Y: length n_symbols*4 each (16QAM => 4 bits/sym).

        Returns dict with rX, rY, sX, sY (our codeword symbols), h, theta, and the
        original generator's noise-free check. Noise is re-derived with an
        independent rng (different seed offset) so that codeword and uncoded share
        the same physics statistics but are not bit-identical to the base draw.
        """
        n = self.n_symbols
        if codeword_bits_X.size != n * 4 or codeword_bits_Y.size != n * 4:
            raise ValueError(
                f"need {n*4} bits per pol, got X={codeword_bits_X.size} Y={codeword_bits_Y.size}"
            )
        sX = qam16_mod(codeword_bits_X.astype(np.uint8))
        sY = qam16_mod(codeword_bits_Y.astype(np.uint8))
        # Re-derive the noise stream with a seed derived from the realization seed
        # but independent of the generator's internal draws. We add a fixed offset
        # so different realizations keep distinct noise. This is the deployable
        # channel the receiver sees; TX truth = codeword_bits_*, used only for score.
        rng = np.random.default_rng(self.seed + 1_000_003)
        nv = 1.0 / (2.0 * self.gamma_bar)
        cos_t = np.cos(self.theta)
        sin_t = np.sin(self.theta)
        rX = np.sqrt(self.h) * (cos_t * sX + sin_t * sY) + np.sqrt(nv) * (
            rng.standard_normal(n) + 1j * rng.standard_normal(n)
        )
        rY = np.sqrt(self.h) * (-sin_t * sX + cos_t * sY) + np.sqrt(nv) * (
            rng.standard_normal(n) + 1j * rng.standard_normal(n)
        )
        return {
            "rX": rX,
            "rY": rY,
            "sX": sX,
            "sY": sY,
            "h": self.h,
            "theta": self.theta,
            "gamma_bar": self.gamma_bar,
            "bitsX": codeword_bits_X,
            "bitsY": codeword_bits_Y,
        }


# --- receiver -> LLR ---------------------------------------------------------


def receiver_equalize(realization: dict, gamma_bar: float, h_mode: str = "blind") -> dict:
    """Equalize each polarization with per-block MMSE + amp_limit.

    h_mode: 'blind' uses a receiver-visible per-block power-minus-noise estimate
    (modulation-agnostic, same as estimate_h_blind_perblock); 'oracle' uses true h
    (scoring/headroom only, never deployable).
    """
    n = realization["rX"].size
    h_true = realization["h"]
    nv = 1.0 / (2.0 * gamma_bar)
    block = 100  # matches SimulationConfig.experiment.BLOCK
    nb = int(np.ceil(n / block))

    def per_block_h(rx: np.ndarray) -> np.ndarray:
        h_est = np.empty(n)
        for i in range(nb):
            sl = slice(i * block, min((i + 1) * block, n))
            p_rx = float(np.mean(np.abs(rx[sl]) ** 2))
            h_est[sl] = max(p_rx - nv, 1e-6)
        return h_est

    if h_mode == "oracle":
        h_use = h_true
    else:
        h_use = per_block_h(realization["rX"])  # receiver-visible, per-pol X
    eqX = amp_limit(mmse_equalize(realization["rX"], h_use, gamma_bar), 3.0)
    if h_mode == "oracle":
        h_use_y = h_true
    else:
        h_use_y = per_block_h(realization["rY"])
    eqY = amp_limit(mmse_equalize(realization["rY"], h_use_y, gamma_bar), 3.0)
    return {"eqX": eqX, "eqY": eqY, "h_use_X": h_use, "h_use_Y": h_use_y}


def receiver_to_llr(eq: dict, gamma_bar: float, sigma2_mode: str = "global_awgn") -> dict:
    """Compute max-log 16QAM LLR for each polarization.

    sigma2_mode='global_awgn': receiver-visible global scale sigma2 = 1/(2*gamma_bar).
    This is B0 (uncalibrated). A temperature-scaled variant (B1) multiplies sigma2
    by a dev-tuned scalar; a clipping variant (B2) changes llr_clip.
    """
    if sigma2_mode == "global_awgn":
        sigma2 = 1.0 / (2.0 * gamma_bar)
    else:
        raise ValueError(sigma2_mode)
    llrX = maxlog_soft_demap_16qam(eq["eqX"], sigma2)
    llrY = maxlog_soft_demap_16qam(eq["eqY"], sigma2)
    return {"llrX": llrX, "llrY": llrY, "sigma2": sigma2}


# --- coded metrics -----------------------------------------------------------


def coded_metrics(
    info_bits_X: np.ndarray,
    info_bits_Y: np.ndarray,
    info_hat_X: np.ndarray,
    info_hat_Y: np.ndarray,
    codeword_bits_X: np.ndarray,
    codeword_bits_Y: np.ndarray,
    eqX: np.ndarray,
    eqY: np.ndarray,
    sX: np.ndarray,
    sY: np.ndarray,
) -> dict:
    """Compute pre-FEC BER (hard demod of equalized), post-FEC BER, FER.

    pre-FEC BER: hard-demodulate eqX/eqY (qam16_demod) and compare to codeword bits.
    post-FEC BER: compare decoded info bits to original info bits.
    FER: frame (codeword) error rate = fraction of codewords with >=1 info bit error.
    """
    # pre-FEC: hard demod
    hard_bits_X = _qam16_demod_to_bits(eqX)
    hard_bits_Y = _qam16_demod_to_bits(eqY)
    pre_ber_X = float(np.mean(hard_bits_X != codeword_bits_X))
    pre_ber_Y = float(np.mean(hard_bits_Y != codeword_bits_Y))
    # post-FEC
    post_ber_X = float(np.mean(info_hat_X != info_bits_X))
    post_ber_Y = float(np.mean(info_hat_Y != info_bits_Y))
    # FER: each polarization carries n_symbols*4/4 = n_symbols symbols, but a
    # codeword is k=1024 info bits = 256 16QAM symbols. With n_symbols symbols per
    # pol we have n_codewords = n_symbols*4 // k codewords per pol.
    return {
        "pre_fec_ber_X": pre_ber_X,
        "pre_fec_ber_Y": pre_ber_Y,
        "pre_fec_ber": 0.5 * (pre_ber_X + pre_ber_Y),
        "post_fec_ber_X": post_ber_X,
        "post_fec_ber_Y": post_ber_Y,
        "post_fec_ber": 0.5 * (post_ber_X + post_ber_Y),
    }


def _qam16_demod_to_bits(z: np.ndarray) -> np.ndarray:
    """Hard-decision 16QAM demod returning 4 bits/sym in [b0,b1,b2,b3] order.

    Uses nearest-neighbour against the verified constellation table (matches
    common.qam16_demod for the symbol, then decodes label->bits via _CONST_BITS).
    """
    z = np.asarray(z).ravel()
    idx = np.argmin(np.abs(z[:, None] - _CONST[None, :]) ** 2, axis=1)  # (N,) label in 4*bi+bq
    bits = _CONST_BITS[idx]  # (N,4) uint8
    return bits.reshape(-1)


def fer_from_info_blocks(info_hat: np.ndarray, info_true: np.ndarray, k: int) -> float:
    """FER = fraction of k-bit info blocks with >=1 bit error."""
    info_hat = np.asarray(info_hat).ravel()
    info_true = np.asarray(info_true).ravel()
    n_blocks = info_hat.size // k
    if n_blocks == 0:
        return float("nan")
    h = info_hat[: n_blocks * k].reshape(n_blocks, k)
    t = info_true[: n_blocks * k].reshape(n_blocks, k)
    n_err = np.any(h != t, axis=1).sum()
    return float(n_err / n_blocks)


# --- contract receipt / source hash -----------------------------------------


def source_receipt(contract: CodedContract, adapter: CodecAdapter) -> dict:
    """Record source/version/hash for the coded contract (FR-20 provenance)."""
    import sionna as _sionna

    enc_path = Path(LDPC5GEncoder.__module__.replace(".", "/") + ".py")
    # resolve within installed sionna package
    try:
        import sionna.phy.fec.ldpc.encoding as _enc_mod

        enc_file = Path(_enc_mod.__file__)
        enc_sha = hashlib.sha256(enc_file.read_bytes()).hexdigest()
    except Exception:
        enc_file = None
        enc_sha = "UNAVAILABLE"
    try:
        bg_csv = Path(_enc_mod.__file__).parent / "codes" / "5G_bg2.csv"
        bg_sha = hashlib.sha256(bg_csv.read_bytes()).hexdigest()
    except Exception:
        bg_csv = None
        bg_sha = "UNAVAILABLE"
    return {
        "sionna_version": _sionna.__version__,
        "encoder_module": str(enc_file) if enc_file else "UNAVAILABLE",
        "encoder_sha256": enc_sha,
        "bg2_csv": str(bg_csv) if bg_csv else "UNAVAILABLE",
        "bg2_csv_sha256": bg_sha,
        "bg": adapter._bg,
        "Z": adapter._z,
        "k_ldpc": adapter._k_ldpc,
        "n_ldpc": adapter._n_ldpc,
        "contract": contract.to_dict(),
    }


if __name__ == "__main__":
    # minimal self-smoke
    c = CodedContract()
    codec = CodecAdapter(c)
    receipt = source_receipt(c, codec)
    print(json.dumps(receipt, indent=2, ensure_ascii=False)[:1200])
