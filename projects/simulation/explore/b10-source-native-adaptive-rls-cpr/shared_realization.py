"""Isolated single-polarization shared realization for T010."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from common._gg_time import gg_time_envelope
from common._modulation import qam16_mod


PACKAGE_DIR = Path(__file__).resolve().parent
PILOT_COUNT = 128


def _manifest():
    raw = json.loads((PACKAGE_DIR / "pilot-manifest.json").read_text(encoding="utf-8"))
    bits = np.asarray(raw["bits"], dtype=int)
    symbols = np.asarray([complex(real, imag) for real, imag in raw["symbols"]])
    return bits, symbols


def generate_shared_b10_realization(
    *,
    seed: int,
    n_symbols: int,
    symbol_rate: float,
    esn0_db: float,
    linewidth_hz: float,
    cfo_hz: float,
    alpha: float = 11.6,
    beta: float = 10.1,
    greenwood_hz: float = 100.0,
    block: int = 100,
    gg_method: str = "gar",
    pilot_enabled: bool = True,
    use_gg: bool = True,
) -> dict:
    """Generate pilots+data once, then apply one TX-side channel/noise path."""
    if pilot_enabled and n_symbols <= PILOT_COUNT:
        raise ValueError("n_symbols must exceed the 128-symbol pilot")
    t_s = 1.0 / symbol_rate
    data_rng = np.random.default_rng(seed)
    if pilot_enabled:
        pilot_bits, pilot_symbols = _manifest()
        data_bits = data_rng.integers(0, 2, (n_symbols - PILOT_COUNT) * 4)
        data_symbols = qam16_mod(data_bits)
        bits = np.concatenate((pilot_bits, data_bits))
        tx = np.concatenate((pilot_symbols, data_symbols))
        data_mask = np.arange(n_symbols) >= PILOT_COUNT
    else:
        bits = data_rng.integers(0, 2, n_symbols * 4)
        tx = qam16_mod(bits)
        data_bits = bits
        data_mask = np.ones(n_symbols, dtype=bool)

    if use_gg:
        tau_c = 1.0 / (2.0 * np.pi * greenwood_hz)
        h = gg_time_envelope(
            n_symbols,
            alpha,
            beta,
            tau_c,
            block=block,
            t_s=t_s,
            method=gg_method,
            seed=seed,
        )
    else:
        h = np.ones(n_symbols)

    phase_rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
    pn_sigma = np.sqrt(2.0 * np.pi * linewidth_hz * t_s)
    phase_noise = np.cumsum(pn_sigma * phase_rng.standard_normal(n_symbols))
    phase = 2.0 * np.pi * cfo_hz * np.arange(n_symbols) * t_s + phase_noise
    noiseless = np.sqrt(h) * tx * np.exp(1j * phase)
    gamma = 10.0 ** (esn0_db / 10.0)
    noise_rng = np.random.default_rng(np.random.SeedSequence([seed, 2]))
    noise = np.sqrt(1.0 / (2.0 * gamma)) * (
        noise_rng.standard_normal(n_symbols) + 1j * noise_rng.standard_normal(n_symbols)
    )
    rx = noiseless + noise
    return {
        "rx": rx,
        "tx": tx,
        "bits": bits,
        "data_bits": data_bits,
        "data_mask": data_mask,
        "noise": noise,
        "phase": phase,
        "phase_noise": phase_noise,
        "gg_envelope": h,
        "noiseless_rx": noiseless,
        "single_pol": True,
        "pilot_symbols_source": "pilot-manifest.json" if pilot_enabled else None,
        "pilot_enabled": pilot_enabled,
        "bits_per_symbol": 4,
        "symbol_rate": symbol_rate,
        "cfo_hz": cfo_hz,
        "esn0_db": esn0_db,
        "linewidth_hz": linewidth_hz,
        "seed": seed,
    }
