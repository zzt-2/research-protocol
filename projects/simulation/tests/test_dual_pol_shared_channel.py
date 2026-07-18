"""Regression tests for the shared dual-polarization channel realization."""
from __future__ import annotations

import inspect
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pytest


SIM_DIR = Path(__file__).resolve().parents[1]
EXPLORE_DIR = SIM_DIR / "explore" / "cma-fade-divergence"
sys.path.insert(0, str(EXPLORE_DIR))

from common import generate_shared_realization_dp  # noqa: E402
import common._dual_pol_channel as dual_pol_channel  # noqa: E402
from common._gg_time import gg_time_envelope  # noqa: E402
from params import SimulationConfig  # noqa: E402
import r_lcr_ber_impact  # noqa: E402


def _legacy_gen_channel_reference(N, alpha, beta, f_g, sop_rate, seed):
    """Frozen copy of the pre-extraction production logic."""
    cfg = SimulationConfig()
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(
        N,
        alpha,
        beta,
        tau_c,
        block=cfg.experiment.BLOCK,
        t_s=cfg.system.T_S,
        method="gar",
        seed=seed,
    )

    def gen_qpsk():
        bits = rng.integers(0, 2, N * 2)
        symbols = (
            (1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])
        ) / np.sqrt(2)
        return symbols, bits

    sX, bitsX = gen_qpsk()
    sY, bitsY = gen_qpsk()
    theta = sop_rate * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * cfg.experiment.GAMMA_BAR_DEFAULT)
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
    }


@pytest.mark.parametrize("seed", [0, 17, 1234])
def test_shared_dp_channel_matches_legacy_bit_exact_for_multiple_seeds(seed):
    args = dict(N=511, alpha=1.5, beta=0.8, f_g=100.0,
                sop_rate=4e-7, seed=seed)
    expected = _legacy_gen_channel_reference(**args)
    actual = generate_shared_realization_dp(**args)

    for key in ("rX", "rY", "sX", "sY", "h", "theta", "bitsX", "bitsY"):
        assert np.array_equal(actual[key], expected[key]), key
        assert actual[key].dtype == expected[key].dtype, key


def test_method_default_is_resolved_from_runtime_config(monkeypatch):
    assert inspect.signature(generate_shared_realization_dp).parameters[
        "method"
    ].default is None

    captured = {}
    fake_cfg = SimpleNamespace(
        experiment=SimpleNamespace(GAMMA_BAR_DEFAULT=100.0, BLOCK=7),
        system=SimpleNamespace(T_S=4e-10),
        gg_time=SimpleNamespace(
            AR1_METHOD="lognormal",
            tau_c_from_fg=lambda f_g: 1.0 / f_g,
        ),
    )

    def fake_envelope(N, alpha, beta, tau_c, **kwargs):
        captured.update(kwargs)
        return np.ones(N)

    monkeypatch.setattr(dual_pol_channel, "SimulationConfig", lambda: fake_cfg)
    monkeypatch.setattr(dual_pol_channel, "gg_time_envelope", fake_envelope)
    dual_pol_channel.generate_shared_realization_dp(
        N=11, alpha=1.5, beta=0.8, f_g=100.0, sop_rate=4e-7, seed=3
    )

    assert captured["method"] == "lognormal"


def test_shared_dp_channel_keys_shapes_and_reproducibility():
    args = dict(N=211, alpha=1.5, beta=0.8, f_g=300.0,
                sop_rate=4e-7, seed=91)
    first = generate_shared_realization_dp(**args)
    second = generate_shared_realization_dp(**args)
    different = generate_shared_realization_dp(**{**args, "seed": 92})

    required = {"rX", "rY", "sX", "sY", "h", "theta", "bitsX", "bitsY"}
    assert required <= first.keys()
    for key in ("rX", "rY", "sX", "sY", "h", "theta"):
        assert first[key].shape == (args["N"],)
        assert np.array_equal(first[key], second[key]), key
    for key in ("bitsX", "bitsY"):
        assert first[key].shape == (2 * args["N"],)
        assert np.array_equal(first[key], second[key]), key
    assert not np.array_equal(first["rX"], different["rX"])


def test_legacy_wrapper_calls_shared_generator_once(monkeypatch):
    sentinel = {
        key: np.full(3, index)
        for index, key in enumerate(("rX", "rY", "sX", "sY", "h", "theta"))
    }
    calls = []

    def fake_generate(**kwargs):
        calls.append(kwargs)
        return sentinel

    monkeypatch.setattr(r_lcr_ber_impact, "generate_shared_realization_dp", fake_generate)
    result = r_lcr_ber_impact.gen_channel(3, 1.5, 0.8, 100.0, 4e-7, 5)

    assert len(calls) == 1
    assert calls[0] == {
        "N": 3,
        "alpha": 1.5,
        "beta": 0.8,
        "f_g": 100.0,
        "sop_rate": 4e-7,
        "seed": 5,
    }
    assert all(result[index] is sentinel[key] for index, key in enumerate(
        ("rX", "rY", "sX", "sY", "h", "theta")
    ))
