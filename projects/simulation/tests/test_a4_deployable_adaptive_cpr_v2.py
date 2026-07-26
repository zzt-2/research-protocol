"""Identity tests for the isolated T009 A4-v2 package."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = (
    Path(__file__).parents[1]
    / "explore"
    / "a4-deployable-adaptive-cpr-v2"
    / "a4_v2.py"
)


def _load():
    spec = importlib.util.spec_from_file_location("a4_v2", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_nearest_16apsk_hard_decision_is_identity_on_constellation():
    a4 = _load()
    constellation = a4.m16apsk_constellation()
    np.testing.assert_allclose(a4.hard_decision_m16apsk(constellation), constellation)


def test_causal_ambiguity_resolve_uses_only_known_pilots():
    a4 = _load()
    rng = np.random.default_rng(17)
    bits = rng.integers(0, 2, 256 * 4)
    tx = a4.m16apsk_mod(bits)
    rotation = 3 * np.pi / 4
    rx = tx * np.exp(1j * rotation)
    pilot_idx = np.arange(0, 256, 4)
    resolved, branch = a4.resolve_ambiguity_from_pilots(
        rx, pilot_idx, tx[pilot_idx], m0=8
    )
    assert branch == 3
    np.testing.assert_allclose(resolved, tx, atol=1e-12)


def test_dpll_vco_state_continues_across_block_boundaries():
    a4 = _load()
    rng = np.random.default_rng(23)
    bits = rng.integers(0, 2, 512 * 4)
    tx = a4.m16apsk_mod(bits)
    phase = np.linspace(0.0, 0.42, 512)
    rx = tx * np.exp(1j * phase)
    loop = a4.Dpll16Apsk(omega_n=50e6, symbol_period=4e-10)
    y0 = loop.process(rx[:256])
    state_after_first = loop.vco_phase
    y1 = loop.process(rx[256:])
    assert state_after_first != 0.0
    assert loop.vco_phase != state_after_first
    assert len(np.concatenate([y0, y1])) == 512


def test_selector_is_causal_and_future_block_cannot_change_current_action():
    a4 = _load()
    frozen = a4.FrozenSelectors(
        power_threshold=0.8,
        innovation_threshold=0.25,
        bins=(0.6, 0.9),
        bin_actions=("DA", "DA", "NDA"),
        confidence_margin=0.08,
        global_best="DA",
    )
    history = [{"power": 0.72, "innovation": 0.31}]
    current = {"power": 1.02, "innovation": 0.08}
    action0 = frozen.p3(history, current)
    action1 = frozen.p3(
        history, current, future_debug={"power": 0.01, "innovation": 9.0}
    )
    assert action0 == action1 == "NDA"


def test_required_snr_reports_unresolved_without_real_crossing():
    a4 = _load()
    assert (
        a4.required_snr_db([10, 12, 14], [0.2, 0.1, 0.05], target=3.8e-3)
        == "UNRESOLVED_NO_CROSSING"
    )
    crossing = a4.required_snr_db(
        [10, 12, 14], [1e-2, 3e-3, 1e-3], target=3.8e-3
    )
    assert 11.0 < crossing < 12.0
