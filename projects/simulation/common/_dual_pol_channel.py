"""Shared dual-polarization time-varying Gamma-Gamma channel generation.

Modulation support
------------------
The generator is modulation-aware (CB1 closure, science-scout-2026-07-20).
``modulation='qpsk'`` (default) is byte-identical to the pre-CB1 generator —
the same ``bitsX``/``sX`` layout, the same RNG draw order, the same symbol
formula. This preserves the P03 v1 source-equivalence contract (commit
``65db35bb``) and every protected-history batch (B001-B003) that depends on
QPSK bit-exactness.

``modulation='qam16'`` draws 4 bits/symbol (``N*4`` bits per pol) and emits
Gray-mapped, average-power-normalized 16QAM symbols via
:func:`_modulation.qam16_mod`. The channel physics (GG envelope ``h``, SOP
``theta``, AWGN) is modulation-agnostic.

Provenance: see ``projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/formula-symbol-parameter-provenance.yaml``.
"""

import numpy as np

from params import SimulationConfig

from ._gg_time import gg_time_envelope
from ._modulation import qam16_mod


_SUPPORTED_MODULATIONS = ("qpsk", "qam16")
_BITS_PER_SYMBOL = {"qpsk": 2, "qam16": 4}


def _generate_qpsk_symbols(rng, N):
    """Generate one polarization's QPSK symbols.

    Byte-identical to the pre-CB1 inline formula. Uses ``(1 - 2*bits)`` sign
    convention (NOT the ``(2*bits - 1)`` convention in
    :func:`_modulation.qpsk_mod`), so this function must NOT be replaced by
    ``qpsk_mod`` without a sign-flip migration.
    """
    bits = rng.integers(0, 2, N * 2)
    s = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    return bits, s


def _generate_qam16_symbols(rng, N):
    """Generate one polarization's 16QAM symbols (4 bits/symbol, Gray, /sqrt(10)).

    Provenance: ``qam16_mod`` with gray_map {-3,-1,+3,+1} (a valid reflection
    Gray ordering); average power E[|s|^2] = 1. See formula-symbol-parameter-provenance.yaml F-QAM16.
    """
    bits = rng.integers(0, 2, N * 4)
    s = qam16_mod(bits)
    return bits, s


def generate_shared_realization_dp(
    N,
    alpha,
    beta,
    f_g,
    sop_rate,
    seed,
    gamma_bar=None,
    block=None,
    t_s=None,
    method=None,
    modulation="qpsk",
):
    """Generate one shared dual-polarization channel realization.

    Optional physical parameters are resolved from ``SimulationConfig`` at
    call time so callers can override them explicitly without frozen defaults.

    Parameters
    ----------
    modulation : {'qpsk', 'qam16'}, default 'qpsk'
        Symbol constellation. ``'qpsk'`` (2 bits/symbol) is byte-identical to
        the pre-CB1 generator. ``'qam16'`` (4 bits/symbol) emits Gray-mapped,
        average-power-normalized 16QAM. The channel physics is
        modulation-agnostic; only the symbol generation and the ``bitsX`` /
        ``bitsY`` length differ.

    Notes
    -----
    The RNG draw order is preserved for QPSK (bitsX, sX, bitsY, sY, then
    noise). For 16QAM the draw order is the same shape (bitsX, sX, bitsY,
    sY, then noise), but each bit draw is ``N*4`` instead of ``N*2``.
    """
    if modulation not in _SUPPORTED_MODULATIONS:
        raise ValueError(
            f"modulation={modulation!r} not supported; "
            f"choose from {_SUPPORTED_MODULATIONS}"
        )

    cfg = SimulationConfig()
    gamma_bar = (
        cfg.experiment.GAMMA_BAR_DEFAULT if gamma_bar is None else gamma_bar
    )
    block = cfg.experiment.BLOCK if block is None else block
    t_s = cfg.system.T_S if t_s is None else t_s
    method = cfg.gg_time.AR1_METHOD if method is None else method

    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(
        N,
        alpha,
        beta,
        tau_c,
        block=block,
        t_s=t_s,
        method=method,
        seed=seed,
    )

    if modulation == "qpsk":
        bitsX, sX = _generate_qpsk_symbols(rng, N)
        bitsY, sY = _generate_qpsk_symbols(rng, N)
    else:  # modulation == "qam16"
        bitsX, sX = _generate_qam16_symbols(rng, N)
        bitsY, sY = _generate_qam16_symbols(rng, N)

    theta = sop_rate * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * gamma_bar)
    rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) + np.sqrt(nv) * (
        rng.standard_normal(N) + 1j * rng.standard_normal(N)
    )
    rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) + np.sqrt(nv) * (
        rng.standard_normal(N) + 1j * rng.standard_normal(N)
    )

    return {
        "rX": rX,
        "rY": rY,
        "sX": sX,
        "sY": sY,
        "h": h,
        "theta": theta,
        "bitsX": bitsX,
        "bitsY": bitsY,
        "modulation": modulation,
        "bits_per_symbol": _BITS_PER_SYMBOL[modulation],
        # Compatibility aliases: remove only after every downstream consumer
        # has migrated to the canonical bitsX/bitsY names.
        "bitX": bitsX,
        "bitY": bitsY,
    }
