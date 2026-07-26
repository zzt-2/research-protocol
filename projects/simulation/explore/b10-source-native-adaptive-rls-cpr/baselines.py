"""Conventional C1 comparator arms with a shared fourth-power coarse FOE."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from common._modulation import hard_decision
from common._recovery import bps_cpr, fft_foe


PACKAGE_DIR = Path(__file__).resolve().parent
FROZEN_SYMBOL_RATE = 2.5e9
DPLL_ZETA = np.sqrt(2.0) / 2.0


def _require_symbol_rate(symbol_rate: float) -> None:
    if not np.isfinite(symbol_rate) or not np.isclose(
        symbol_rate, FROZEN_SYMBOL_RATE, rtol=0.0, atol=1e-6
    ):
        raise ValueError(
            "symbol_rate must equal the C1 contract/B5 source-transfer value "
            f"({FROZEN_SYMBOL_RATE} sym/s)"
        )


def _coarse_4opm(rx: np.ndarray, symbol_rate: float) -> tuple[np.ndarray, float]:
    _require_symbol_rate(symbol_rate)
    rx = np.asarray(rx, dtype=complex)
    omega = float(fft_foe(rx))
    corrected = rx * np.exp(-1j * omega * np.arange(len(rx)))
    return corrected, omega * symbol_rate / (2.0 * np.pi)


def _resolve_manifest_ambiguity(
    corrected: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Resolve only the global pi/2 ambiguity using receiver-known pilots."""
    raw = json.loads((PACKAGE_DIR / "pilot-manifest.json").read_text(encoding="utf-8"))
    pilots = np.asarray([complex(real, imag) for real, imag in raw["symbols"]])
    candidates = np.arange(4) * (np.pi / 2.0)
    metric = [
        np.mean(np.abs(corrected[: len(pilots)] * np.exp(-1j * phase) - pilots) ** 2)
        for phase in candidates
    ]
    offset = float(candidates[int(np.argmin(metric))])
    return corrected * np.exp(-1j * offset), offset


def _continuous_dd_dpll(
    rx: np.ndarray,
    *,
    symbol_rate: float,
    omega_n: float,
    zeta: float = DPLL_ZETA,
) -> tuple[np.ndarray, np.ndarray]:
    """Isolated continuous DD-DPLL with an explicit per-call symbol period.

    The PI-loop semantics match the existing receiver algorithm: decision-
    directed phase detector, proportional-plus-integral filter and continuous
    VCO state. omega_n remains a future validation-frozen project parameter;
    zeta=sqrt(2)/2 is the classical Butterworth/critical-damping convention.
    """
    _require_symbol_rate(symbol_rate)
    if not np.isfinite(omega_n) or omega_n <= 0:
        raise ValueError("omega_n must be finite and positive")
    if not np.isfinite(zeta) or zeta <= 0:
        raise ValueError("zeta must be finite and positive")
    rx = np.asarray(rx, dtype=complex)
    t_s = 1.0 / symbol_rate
    w_t = min(omega_n * t_s, 0.5)
    c1 = 2.0 * zeta * w_t
    c2 = w_t**2
    phase = np.zeros(len(rx))
    integrator = 0.0
    vco_phase = 0.0
    for index, sample in enumerate(rx):
        rotated = sample * np.exp(-1j * vco_phase)
        decision = hard_decision(rotated, mod="qam16")
        phase_error = float(np.angle(rotated * np.conj(decision)))
        integrator += c2 * phase_error
        vco_phase += c1 * phase_error + integrator
        phase[index] = vco_phase
    return rx * np.exp(-1j * phase), phase


def run_4opm_bps(
    rx: np.ndarray, *, symbol_rate: float, test_phases: int, window: int
) -> dict:
    if test_phases != 32:
        raise ValueError("T010 conventional BPS identity requires exactly 32 test phases")
    if not isinstance(window, int) or window <= 0 or window % 2 == 0:
        raise ValueError("BPS window must be a positive odd integer")
    coarse, frequency = _coarse_4opm(rx, symbol_rate)
    corrected, phase = bps_cpr(coarse, B=test_phases, Nw=window, mod="qam16")
    corrected, global_offset = _resolve_manifest_ambiguity(corrected)
    phase = phase + global_offset
    return {
        "corrected": corrected,
        "phase_estimate": phase,
        "coarse_frequency_hz": frequency,
        "coarse_stage": "4OPM",
        "global_pilot_offset": global_offset,
    }


def run_4opm_dd_dpll(
    rx: np.ndarray, *, symbol_rate: float, omega_n: float
) -> dict:
    coarse, frequency = _coarse_4opm(rx, symbol_rate)
    corrected, phase = _continuous_dd_dpll(
        coarse,
        symbol_rate=symbol_rate,
        omega_n=omega_n,
        zeta=DPLL_ZETA,
    )
    corrected, global_offset = _resolve_manifest_ambiguity(corrected)
    phase = phase + global_offset
    return {
        "corrected": corrected,
        "phase_estimate": phase,
        "coarse_frequency_hz": frequency,
        "coarse_stage": "4OPM",
        "global_pilot_offset": global_offset,
        "dpll_parameters": {
            "symbol_rate": symbol_rate,
            "symbol_period": 1.0 / symbol_rate,
            "omega_n": omega_n,
            "omega_n_provenance": "validation_tuned_unfrozen_C1",
            "zeta": DPLL_ZETA,
            "zeta_provenance": "sqrt(2)/2 Butterworth damping convention",
        },
    }
