from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "explore" / "ch4-apsk-ring-gated-rde"


def _load_core():
    spec = importlib.util.spec_from_file_location("ch4_gated_rde_core", PKG / "core.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = _load_core()


def test_m16apsk_mapping_ring_identity_and_nearest_point_match_common():
    common_path = ROOT / "common" / "_modulation.py"
    spec = importlib.util.spec_from_file_location("simulation_modulation", common_path)
    assert spec is not None and spec.loader is not None
    modulation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulation)

    labels = np.arange(16, dtype=np.uint8)
    bits = ((labels[:, None] >> np.arange(3, -1, -1)) & 1).reshape(-1)
    expected = modulation.m16apsk_mod(bits)
    actual = core.m16apsk_constellation_by_label()
    np.testing.assert_allclose(actual, expected, atol=0.0, rtol=0.0)

    nearest = core.nearest_apsk(actual)
    np.testing.assert_array_equal(nearest["labels"], labels)
    np.testing.assert_array_equal(nearest["ring_ids"], labels >= 8)
    np.testing.assert_allclose(nearest["symbols"], actual, atol=0.0, rtol=0.0)
    np.testing.assert_allclose(nearest["decision_score"], 0.0, atol=1e-30)
    np.testing.assert_allclose(nearest["ring_score"], 0.0, atol=1e-15)


def test_random_su2_and_noiseless_pilot_ls_recover_identity_and_random_jones():
    rng = np.random.default_rng(53001)
    for jones in (np.eye(2, dtype=np.complex128), core.random_su2(rng)):
        np.testing.assert_allclose(jones.conj().T @ jones, np.eye(2), atol=2e-15)
        assert np.linalg.det(jones) == pytest.approx(1.0 + 0.0j, abs=2e-15)
        pilots = core.orthogonal_pilots(16)
        pilot_rx = jones @ pilots
        w0 = core.pilot_ls_demux(pilot_rx, pilots)
        np.testing.assert_allclose(w0 @ jones, np.eye(2), atol=2e-14)


def test_canonical_rde_one_step_matches_hand_calculated_complex_update():
    w0 = np.eye(2, dtype=np.complex128)
    y = np.array([0.5 + 0.25j, -0.75 + 0.5j])
    radii = np.array([1.0, 1.5])
    actual = core.canonical_rde_step(w0, y, radii, mu=0.1, gates=np.ones(2))
    expected = np.array(
        [
            [1.021484375 + 0.0j, -0.0171875 - 0.030078125j],
            [-0.0359375 + 0.062890625j, 1.116796875 + 0.0j],
        ],
        dtype=np.complex128,
    )
    np.testing.assert_allclose(actual, expected, atol=1e-15, rtol=0.0)


def test_all_arms_use_canonical_nearest_radius_while_gates_keep_their_residuals():
    constellation = core.m16apsk_constellation_by_label()
    inner_radius = float(np.min(np.abs(constellation)))
    outer_radius = float(np.max(np.abs(constellation)))
    y = np.array([0.9 + 0.0j, 0.0 + 0.0j], dtype=np.complex128)
    w0 = np.eye(2, dtype=np.complex128)
    point_scores = core.nearest_apsk(y)

    assert point_scores["radii"][0] == pytest.approx(outer_radius)
    squared_radius_residuals = np.abs(
        np.abs(y[0]) ** 2 - np.array([inner_radius, outer_radius]) ** 2
    )
    assert int(np.argmin(squared_radius_residuals)) == 0
    canonical_error = y[0] * (inner_radius**2 - np.abs(y[0]) ** 2)
    point_ring_error = y[0] * (outer_radius**2 - np.abs(y[0]) ** 2)
    assert canonical_error.real < 0.0 < point_ring_error.real

    canonical_radii = np.array([inner_radius, inner_radius])
    expected = core.canonical_rde_step(
        w0, y, canonical_radii, mu=0.1, gates=np.ones(2)
    )
    tx_symbols = point_scores["symbols"][:, None]
    payload = y[:, None]
    arms = {
        "plain": core.run_plain_rde(payload, w0, mu=0.1),
        "cheap": core.run_cheap_rde(
            payload, w0, mu=0.1, ring_threshold=np.inf
        ),
        "candidate": core.run_candidate_rde(
            payload,
            w0,
            mu=0.1,
            ring_threshold=np.inf,
            decision_threshold=np.inf,
        ),
        "oracle": core.run_oracle_rde(payload, w0, tx_symbols, mu=0.1),
    }
    for name, result in arms.items():
        np.testing.assert_allclose(
            result["W"], expected, atol=1e-15, rtol=0.0, err_msg=name
        )

    canonical_ring_score = squared_radius_residuals[0] / inner_radius**2
    point_ring_score = float(point_scores["ring_score"][0])
    assert point_ring_score < 1.0 < canonical_ring_score
    cheap = core.run_cheap_rde(payload, w0, mu=0.1, ring_threshold=1.0)
    candidate = core.run_candidate_rde(
        payload,
        w0,
        mu=0.1,
        ring_threshold=1.0,
        decision_threshold=np.inf,
    )
    assert not cheap["gates"][0, 0]
    assert candidate["gates"][0, 0]


def test_plain_candidate_and_cheap_gate_exact_degeneracies():
    y = np.array(
        [[0.62 + 0.11j, -0.83 + 0.74j], [0.21 - 0.57j, 1.09 + 0.18j]],
        dtype=np.complex128,
    )
    w0 = np.eye(2, dtype=np.complex128)
    plain = core.run_plain_rde(y, w0, mu=1e-3)
    all_one = core.run_candidate_rde(
        y, w0, mu=1e-3, ring_threshold=np.inf, decision_threshold=np.inf
    )
    np.testing.assert_array_equal(all_one["gates"], np.ones_like(all_one["gates"]))
    np.testing.assert_allclose(all_one["z"], plain["z"], atol=0.0, rtol=0.0)
    np.testing.assert_allclose(all_one["W"], plain["W"], atol=0.0, rtol=0.0)

    zero_gate = core.run_candidate_rde(
        y, w0, mu=1e-3, ring_threshold=-1.0, decision_threshold=-1.0
    )
    np.testing.assert_array_equal(zero_gate["gates"], np.zeros_like(zero_gate["gates"]))
    np.testing.assert_allclose(zero_gate["W"], w0, atol=0.0, rtol=0.0)

    cheap = core.run_cheap_rde(y, w0, mu=1e-3, ring_threshold=0.25)
    candidate_single_feature = core.run_candidate_rde(
        y, w0, mu=1e-3, ring_threshold=0.25, decision_threshold=np.inf
    )
    np.testing.assert_array_equal(cheap["gates"], candidate_single_feature["gates"])
    np.testing.assert_allclose(cheap["W"], candidate_single_feature["W"], atol=0.0, rtol=0.0)


def test_hard_gate_boundary_scores_and_truth_firewall():
    z = core.m16apsk_constellation_by_label()[[0, 8]]
    scores = core.nearest_apsk(z)
    boundary = core.candidate_gate(
        scores["ring_score"],
        scores["decision_score"],
        ring_threshold=0.0,
        decision_threshold=0.0,
    )
    np.testing.assert_array_equal(boundary, np.ones(2, dtype=bool))
    assert np.all(np.isfinite(scores["ring_score"])) and np.all(scores["ring_score"] >= 0)
    assert np.all(np.isfinite(scores["decision_score"])) and np.all(scores["decision_score"] >= 0)

    forbidden = {"tx", "truth", "jones", "snr", "ber"}
    for fn in (core.run_plain_rde, core.run_cheap_rde, core.run_candidate_rde):
        names = {name.lower() for name in inspect.signature(fn).parameters}
        assert not any(any(token in name for token in forbidden) for name in names)
    oracle_names = {name.lower() for name in inspect.signature(core.run_oracle_rde).parameters}
    assert any("tx" in name or "truth" in name for name in oracle_names)


def test_paired_realization_hash_and_seam_contract():
    realization = core.generate_shared_correctness_realization(
        seed=53002, n_payload=64, n_pilots=16, snr_db=30.0
    )
    repeated = core.generate_shared_correctness_realization(
        seed=53002, n_payload=64, n_pilots=16, snr_db=30.0
    )
    assert realization["realization_hash"] == repeated["realization_hash"]
    for key in ("symbols", "J", "noise", "W0", "payload_rx"):
        np.testing.assert_array_equal(realization[key], repeated[key])

    arms = core.run_all_arms(realization, mu=1e-4, ring_threshold=0.2, decision_threshold=0.2)
    assert set(arms) == {"plain", "cheap", "candidate", "oracle"}
    for result in arms.values():
        assert result["realization_hash"] == realization["realization_hash"]
        assert result["z"].shape == (2, 64)
        assert result["G_eff"].shape == (2, 2)
        assert result["Sigma_n"].shape == (2, 2)
        assert result["flags"].shape == (2, 64)
        assert np.issubdtype(result["z"].dtype, np.complexfloating)
        assert np.all(np.isfinite(result["z"]))
        assert np.all(np.isfinite(result["G_eff"]))
        assert np.all(np.isfinite(result["Sigma_n"]))
        assert result["constellation_id"] == "DP-(8,8)-16APSK"
        assert result["labeling_id"] == "b0-ring+reflected-gray-8psk"
