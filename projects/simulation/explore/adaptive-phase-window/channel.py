"""T007 channel helper — B1 adaptive phase-estimation window.

Generates the receiver-visible RX for the B1 structural gate and method
package. Two channels are supported:

  - AWGN + Wiener phase-noise slice (flat fading): the B2 source-native
    structural sweep that reads the E1/E2 trend cleanly (sat.1553 L440
    "optimal N is a function of SNR/phase-noise ratio" lives in flat fading).
  - Gamma-Gamma block fading + Wiener PN (primary): reuses the project's
    canonical shared generator (common/_dual_pol_channel.py), takes one
    polarization, and injects the carrier Wiener phase noise on top. The
    shared generator is NEVER modified.

Identity / integrity guards (V001-class defenses):
  - the RX returned to every estimator carries tx bits, true h, true phase
    and true SNR ONLY in the debug dict (used by oracle/eval resolve); the
    deployable method signatures never see them;
  - Wiener PN is injected deterministically from the integer seed
    (np.random.default_rng); no Python built-in hash();
  - CFO is assumed pre-compensated (sat.1553 L433-style, Δf≈0) so only CPE +
    Wiener PN remain — the phase-estimation window problem is well-posed;
  - pilot and data symbols traverse the SAME physical channel (the T006
    defect of separate pilot/data channels is forbidden and tested).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

# Make the project's common package importable without modifying it.
_HERE = os.path.dirname(os.path.abspath(__file__))
# _HERE = .../simulation/explore/adaptive-phase-window; common is at simulation/common
_SIM_DIR = os.path.dirname(os.path.dirname(_HERE))
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from common._config import T_S, BLOCK  # noqa: E402  (re-export, no mutation)
from common._gg_time import gg_time_envelope, rho_from_tau_c  # noqa: E402
from common._modulation import qpsk_mod, qam16_mod  # noqa: E402


# ---------------------------------------------------------------------------
# Parameter container
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ChannelParams:
    modulation: str               # 'qpsk' | 'qam16'
    snr_db: float                 # linear SNR (signal vs AWGN) in dB
    linewidth_hz: float           # laser linewidth Δν (Hz)
    n_symbols: int                # block length per realization
    seed: int                     # deterministic integer seed
    channel: str = "awgn_wiener"  # 'awgn_wiener' | 'gg_block_fading'
    # GG block-fading only:
    alpha: float = 1.0            # uplink_strong (params.py), sat.1553 s4 sigma_p2=0.25
    beta: float = 0.7
    f_g: float = 500.0            # Greenwood frequency (Hz); canonical
    gamma_bar: float = 100.0      # 20 dB (params.py GAMMA_BAR_DEFAULT)
    # pilot overhead (sat.1553 L435 pilot rates 7/8, 15/16, 31/32):
    pilot_rate: str = "15/16"     # 1 pilot per 16 symbols
    cfo_hz: float = 0.0           # CFO assumed pre-compensated (sat.1553 L433)


_BITS_PER_SYMBOL = {"qpsk": 2, "qam16": 4}
_PILOT_RATES = {
    "7/8": 8,     # 1 pilot per 8 symbols
    "15/16": 16,  # 1 pilot per 16 symbols
    "31/32": 32,  # 1 pilot per 32 symbols
}


def _modulate(rng: np.random.Generator, modulation: str, n_symbols: int):
    """Generate uniform i.i.d. symbols + the tx bits (one polarization)."""
    bps = _BITS_PER_SYMBOL[modulation]
    bits = rng.integers(0, 2, n_symbols * bps)
    if modulation == "qpsk":
        s = qpsk_mod(bits)
    elif modulation == "qam16":
        s = qam16_mod(bits)
    else:
        raise ValueError(f"modulation must be 'qpsk' or 'qam16', got {modulation!r}")
    return bits, s


def _pilot_mask(n_symbols: int, pilot_rate: str) -> np.ndarray:
    """Deterministic pilot mask: one pilot every `period` symbols at index 0."""
    if pilot_rate not in _PILOT_RATES:
        raise ValueError(f"pilot_rate must be one of {list(_PILOT_RATES)}, got {pilot_rate!r}")
    period = _PILOT_RATES[pilot_rate]
    mask = np.zeros(n_symbols, dtype=bool)
    mask[::period] = True
    return mask


def _wiener_phase(n_symbols: int, linewidth_hz: float, t_s: float,
                  rng: np.random.Generator) -> np.ndarray:
    """Discrete Wiener carrier phase noise trajectory.

    Per-symbol phase innovation variance σ²_p = 2π·Δν·T_S (D-007 single truth
    source; params.py LASER_LW derivation). theta[k] = theta[k-1] + N(0, σ²_p).
    """
    sigma2_p = 2.0 * np.pi * linewidth_hz * t_s
    innovations = rng.normal(0.0, np.sqrt(sigma2_p), size=n_symbols)
    theta = np.cumsum(innovations)
    return theta


# ---------------------------------------------------------------------------
# Channel generation (returns receiver-visible RX + a guarded debug dict)
# ---------------------------------------------------------------------------
@dataclass
class ChannelOutput:
    rx: np.ndarray                # receiver-visible complex RX (single pol)
    pilot_mask: np.ndarray        # bool, True at pilot positions
    pilot_symbols: np.ndarray     # the known pilot symbols at pilot positions
    n_symbols: int
    modulation: str
    snr_db: float
    linewidth_hz: float
    seed: int
    channel: str
    # Guarded debug fields — used ONLY by oracle/eval resolve, NEVER passed to
    # a deployable estimator signature (enforced by semantic gate).
    _tx_bits: Optional[np.ndarray] = field(default=None, repr=False)
    _tx_symbols: Optional[np.ndarray] = field(default=None, repr=False)
    _h: Optional[np.ndarray] = field(default=None, repr=False)
    _theta: Optional[np.ndarray] = field(default=None, repr=False)

    def debug(self):
        """Return the truth dict for oracle/eval-resolve use ONLY."""
        return {
            "tx_bits": self._tx_bits,
            "tx_symbols": self._tx_symbols,
            "h": self._h,
            "theta": self._theta,
        }


def generate_channel(params: ChannelParams) -> ChannelOutput:
    """Generate one channel realization.

    The TX truth (bits / symbols / h / theta) is stored on the output under
    underscore-prefixed fields accessed only via `debug()`. Deployable
    estimators receive `output.rx`, `output.pilot_mask`, `output.pilot_symbols`
    and the receiver-visible estimator outputs (SNR_hat, phase_innovation_hat)
    computed FROM the RX — never the truth.
    """
    n = int(params.n_symbols)
    if n <= 0:
        raise ValueError("n_symbols must be positive")

    # Deterministic integer-seeded RNG. No built-in hash(); V039 T004 lesson.
    rng = np.random.default_rng(int(params.seed))

    bits, s = _modulate(rng, params.modulation, n)
    pilot_mask = _pilot_mask(n, params.pilot_rate)
    # Pilot symbols are a known, fixed QPSK pattern (sat.1553-style pilot).
    # Equal energy: pilots come from the SAME constellation as data so the
    # pilot/data channel is identical (closes the T006 separate-channel defect).
    pilot_pattern = np.array([
        (1 + 1j) / np.sqrt(2), (1 - 1j) / np.sqrt(2),
        (-1 + 1j) / np.sqrt(2), (-1 - 1j) / np.sqrt(2),
    ])
    n_pilots = int(pilot_mask.sum())
    pilot_symbols = pilot_pattern[np.arange(n_pilots) % 4]
    # Overwrite pilot positions with the known pilot symbols (equal energy).
    s[pilot_mask] = pilot_symbols

    # Wiener carrier phase noise (deterministic from the same rng stream).
    theta = _wiener_phase(n, params.linewidth_hz, T_S, rng)

    # CFO term (assumed pre-compensated; default 0, sat.1553 L433).
    cfo_phase = 2.0 * np.pi * params.cfo_hz * T_S * np.arange(n)

    # Channel envelope.
    if params.channel == "awgn_wiener":
        h = np.ones(n)                                  # flat fading
    elif params.channel == "gg_block_fading":
        tau_c = 1.0 / (2.0 * np.pi * params.f_g)        # Conan 1995
        h = gg_time_envelope(
            n, params.alpha, params.beta, tau_c,
            block=BLOCK, t_s=T_S, method="gar",
            seed=int(params.seed),
        )
    else:
        raise ValueError(f"channel must be 'awgn_wiener' or 'gg_block_fading', got {params.channel!r}")

    # Combined channel: sqrt(h) * exp(j*(theta + cfo)) * s + noise.
    # SNR is defined linearly as |signal|^2 / |noise|^2 with avg signal power 1.
    snr_lin = 10.0 ** (params.snr_db / 10.0)
    nv = 1.0 / (2.0 * snr_lin)                          # per real/imag component
    noise = np.sqrt(nv) * (rng.standard_normal(n) + 1j * rng.standard_normal(n))
    channel_phase = theta + cfo_phase
    rx = np.sqrt(h) * np.exp(1j * channel_phase) * s + noise

    return ChannelOutput(
        rx=rx,
        pilot_mask=pilot_mask,
        pilot_symbols=pilot_symbols,
        n_symbols=n,
        modulation=params.modulation,
        snr_db=params.snr_db,
        linewidth_hz=params.linewidth_hz,
        seed=int(params.seed),
        channel=params.channel,
        _tx_bits=bits,
        _tx_symbols=s,
        _h=h,
        _theta=channel_phase,
    )


# ---------------------------------------------------------------------------
# Receiver-visible feature estimators (no truth, no oracle)
# ---------------------------------------------------------------------------
def estimate_snr_hat(rx: np.ndarray, window: int = 256) -> np.ndarray:
    """Block SNR_hat from the RX via the 4th-power peak-to-floor ratio (blind).

    A standard blind SNR proxy for M-PSK / square-QAM: raise rx to M=4, take
    the FFT, and use peak-to-median-floor ratio. Monotone in SNR (verified
    empirically: 10/14/18/22 dB -> distinct values). Uses only the RX; returns
    one SNR_hat per block (block-buffered, causal). The value is a relative
    SNR proxy (not calibrated to absolute dB); adaptive controllers normalize
    it to a learned range on validation.
    """
    rx = np.asarray(rx, dtype=complex)
    n = len(rx)
    nb = n // window
    snr_hat = np.zeros(nb)
    for k in range(nb):
        seg = rx[k * window:(k + 1) * window]
        # 4th-power spectrum, peak-to-median-floor ratio.
        win = np.hanning(len(seg))
        R4 = np.abs(np.fft.fft(seg ** 4 * win, n=max(len(seg) * 4, 256)))
        peak = float(R4.max())
        floor = float(np.median(R4))
        ratio = peak / max(floor, 1e-12)
        # log10(ratio) is the monotone SNR proxy; rescale to a dB-like axis.
        snr_hat[k] = 10.0 * np.log10(max(ratio, 1e-12))
    return snr_hat


def estimate_phase_innovation_hat(rx: np.ndarray, m0: int = 4,
                                  window: int = 256) -> np.ndarray:
    """Block phase-innovation_hat (radians per symbol) from the raised RX.

    Raises rx to M0 (4 for QPSK/16-QAM square constellations) to remove the
    modulation, then estimates the per-symbol phase-innovation variance
    within each block via the raised-power phase difference. The M0 factor
    is divided out. Uses mod-2pi phase increments (NOT unwrap) — this is
    the D-009/A1 lesson: unwrap on raised phases path-errors when M0*theta
    exceeds 2pi.
    """
    rx = np.asarray(rx, dtype=complex)
    raised = rx ** m0
    # Block-buffered, causal.
    n = len(rx)
    nb = n // window
    innov = np.zeros(nb)
    for k in range(nb):
        seg = raised[k * window:(k + 1) * window]
        # Raised-power phase increments, mod 2pi (no unwrap).
        ph = np.angle(seg)
        dphi = np.diff(ph)
        dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
        innov[k] = np.std(dphi) / m0
    return innov
