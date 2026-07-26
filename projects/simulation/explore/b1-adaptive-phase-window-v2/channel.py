"""T008 v2 channel helper — B1 adaptive phase-estimation window (identity-repaired).

Generates the receiver-visible RX for the v2 package. Two channels:

  - AWGN + Wiener phase-noise slice (flat fading): the B2 source-native
    structural sweep (reads the E1/E2 trend cleanly).
  - Gamma-Gamma block fading + Wiener PN (primary): reuses the project's
    canonical shared generator (common/_gg_time.gg_time_envelope), single
    polarization, with carrier Wiener phase noise injected on top.

v2 differences from T007 channel.py (identity-gap closures):
  - block size is the canonical params.py BLOCK (=100), NOT the T007-hardcoded
    256 in run_gg_oracle_headroom. This is the GG block-fading unit and the
    adaptation unit; it is frozen in the contract.
  - one realization per (cell, seed) is generated ONCE and shared by every
    arm/oracle (the runner caches realizations by (cell, seed)).
  - pilot and data traverse the SAME physical channel (T006 defect forbidden).

Identity / integrity guards (V001-class defenses):
  - the RX returned to every estimator carries tx bits / true h / true phase /
    true SNR ONLY in the debug dict (used by oracle/eval resolve); deployable
    method signatures never see them;
  - Wiener PN injected deterministically from the integer seed
    (np.random.default_rng); no Python built-in hash();
  - CFO assumed pre-compensated (sat.1553 L433-style, Δf≈0);
  - pilot and data traverse the SAME physical channel (T006 defect forbidden).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

# Make the project's common package importable without modifying it.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR = os.path.dirname(os.path.dirname(_HERE))
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from common._config import T_S, BLOCK  # noqa: E402  (re-export, no mutation)
from common._gg_time import gg_time_envelope  # noqa: E402
from common._modulation import qpsk_mod, qam16_mod  # noqa: E402


# ---------------------------------------------------------------------------
# Parameter container
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ChannelParams:
    modulation: str               # 'qpsk' | 'qam16'
    snr_db: float                 # linear SNR (signal vs AWGN) in dB
    linewidth_hz: float           # laser linewidth Δν (Hz)
    n_symbols: int                # realization length
    seed: int                     # deterministic integer seed
    channel: str = "awgn_wiener"  # 'awgn_wiener' | 'gg_block_fading'
    # GG block-fading only (canonical params.py values):
    alpha: float = 1.0            # uplink_strong
    beta: float = 0.7
    f_g: float = 500.0            # Greenwood frequency (Hz); canonical
    gamma_bar: float = 100.0      # 20 dB (params.py GAMMA_BAR_DEFAULT)
    pilot_rate: str = "15/16"     # 1 pilot per 16 symbols
    cfo_hz: float = 0.0           # CFO assumed pre-compensated (sat.1553 L433)
    block: int = BLOCK            # canonical BLOCK (frozen in contract)


_BITS_PER_SYMBOL = {"qpsk": 2, "qam16": 4}
_PILOT_RATES = {"7/8": 8, "15/16": 16, "31/32": 32}

# Known QPSK pilot pattern (sat.1553-style). Equal energy: pilots come from
# the SAME constellation as data so pilot/data channel is identical.
_PILOT_PATTERN = np.array([
    (1 + 1j) / np.sqrt(2), (1 - 1j) / np.sqrt(2),
    (-1 + 1j) / np.sqrt(2), (-1 - 1j) / np.sqrt(2),
])


def _modulate(rng: np.random.Generator, modulation: str, n_symbols: int):
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
    if pilot_rate not in _PILOT_RATES:
        raise ValueError(f"pilot_rate must be one of {list(_PILOT_RATES)}, got {pilot_rate!r}")
    period = _PILOT_RATES[pilot_rate]
    mask = np.zeros(n_symbols, dtype=bool)
    mask[::period] = True
    return mask


def _wiener_phase(n_symbols: int, linewidth_hz: float, t_s: float,
                  rng: np.random.Generator) -> np.ndarray:
    """Discrete Wiener carrier phase noise. σ²_p = 2π·Δν·T_S (D-007 truth)."""
    sigma2_p = 2.0 * np.pi * linewidth_hz * t_s
    innovations = rng.normal(0.0, np.sqrt(sigma2_p), size=n_symbols)
    theta = np.cumsum(innovations)
    return theta


# ---------------------------------------------------------------------------
# Channel output (RX is receiver-visible; truth is in the guarded debug dict)
# ---------------------------------------------------------------------------
@dataclass
class ChannelOutput:
    rx: np.ndarray                # receiver-visible complex RX (single pol)
    pilot_mask: np.ndarray
    pilot_symbols: np.ndarray
    n_symbols: int
    modulation: str
    snr_db: float
    linewidth_hz: float
    seed: int
    channel: str
    block: int
    # Guarded debug fields — oracle/eval-resolve ONLY; never passed to a
    # deployable estimator signature (enforced by identity smoke #2).
    _tx_bits: Optional[np.ndarray] = field(default=None, repr=False)
    _tx_symbols: Optional[np.ndarray] = field(default=None, repr=False)
    _h: Optional[np.ndarray] = field(default=None, repr=False)
    _theta: Optional[np.ndarray] = field(default=None, repr=False)

    def debug(self):
        return {
            "tx_bits": self._tx_bits,
            "tx_symbols": self._tx_symbols,
            "h": self._h,
            "theta": self._theta,
        }


def generate_channel(params: ChannelParams) -> ChannelOutput:
    """Generate one channel realization.

    TX truth (bits/symbols/h/theta) is stored under underscore-prefixed fields
    accessed only via debug(). Deployable estimators receive output.rx,
    output.pilot_mask, output.pilot_symbols and the receiver-visible estimators
    (SNR_hat, phase_innovation_hat) computed FROM the RX — never the truth.
    """
    n = int(params.n_symbols)
    if n <= 0:
        raise ValueError("n_symbols must be positive")
    if params.channel == "gg_block_fading" and n % params.block != 0:
        raise ValueError(f"gg_block_fading n_symbols ({n}) must be a multiple of block ({params.block})")

    # Deterministic integer-seeded RNG. No built-in hash(); V039 T004 lesson.
    rng = np.random.default_rng(int(params.seed))

    bits, s = _modulate(rng, params.modulation, n)
    pilot_mask = _pilot_mask(n, params.pilot_rate)
    n_pilots = int(pilot_mask.sum())
    pilot_symbols = _PILOT_PATTERN[np.arange(n_pilots) % 4]
    # Overwrite pilot positions with the known pilot symbols (equal energy).
    s[pilot_mask] = pilot_symbols

    theta = _wiener_phase(n, params.linewidth_hz, T_S, rng)
    cfo_phase = 2.0 * np.pi * params.cfo_hz * T_S * np.arange(n)

    if params.channel == "awgn_wiener":
        h = np.ones(n)
    elif params.channel == "gg_block_fading":
        tau_c = 1.0 / (2.0 * np.pi * params.f_g)
        h = gg_time_envelope(
            n, params.alpha, params.beta, tau_c,
            block=params.block, t_s=T_S, method="gar",
            seed=int(params.seed),
        )
    else:
        raise ValueError(f"channel must be 'awgn_wiener' or 'gg_block_fading', got {params.channel!r}")

    snr_lin = 10.0 ** (params.snr_db / 10.0)
    nv = 1.0 / (2.0 * snr_lin)
    noise = np.sqrt(nv) * (rng.standard_normal(n) + 1j * rng.standard_normal(n))
    channel_phase = theta + cfo_phase
    rx = np.sqrt(h) * np.exp(1j * channel_phase) * s + noise

    return ChannelOutput(
        rx=rx, pilot_mask=pilot_mask, pilot_symbols=pilot_symbols,
        n_symbols=n, modulation=params.modulation, snr_db=params.snr_db,
        linewidth_hz=params.linewidth_hz, seed=int(params.seed),
        channel=params.channel, block=params.block,
        _tx_bits=bits, _tx_symbols=s, _h=h, _theta=channel_phase,
    )


# ---------------------------------------------------------------------------
# Receiver-visible feature estimators (no truth, no oracle)
# ---------------------------------------------------------------------------
def estimate_snr_hat(rx: np.ndarray, window: int) -> np.ndarray:
    """Block SNR_hat from the RX via the 4th-power peak-to-floor ratio (blind).

    Returns one SNR_hat per block (block-buffered, causal). The value is a
    relative SNR proxy (dB-like axis), NOT calibrated to absolute dB; adaptive
    controllers normalize it to a validation-learned range.
    """
    rx = np.asarray(rx, dtype=complex)
    n = len(rx)
    nb = n // window
    snr_hat = np.zeros(nb)
    for k in range(nb):
        seg = rx[k * window:(k + 1) * window]
        win = np.hanning(len(seg))
        R4 = np.abs(np.fft.fft(seg ** 4 * win, n=max(len(seg) * 4, 256)))
        peak = float(R4.max())
        floor = float(np.median(R4))
        ratio = peak / max(floor, 1e-12)
        snr_hat[k] = 10.0 * np.log10(max(ratio, 1e-12))
    return snr_hat


def estimate_phase_innovation_hat(rx: np.ndarray, m0: int = 4, window: int = 256) -> np.ndarray:
    """Block phase-innovation_hat (radians/symbol) from the raised RX.

    Mod-2pi phase increments (NOT unwrap) — the D-009/A1 lesson: unwrap on
    raised phases path-errors when M0*theta exceeds 2pi.
    """
    rx = np.asarray(rx, dtype=complex)
    raised = rx ** m0
    n = len(rx)
    nb = n // window
    innov = np.zeros(nb)
    for k in range(nb):
        seg = raised[k * window:(k + 1) * window]
        ph = np.angle(seg)
        dphi = np.diff(ph)
        dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
        innov[k] = np.std(dphi) / m0
    return innov
