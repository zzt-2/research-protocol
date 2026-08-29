from __future__ import annotations

import copy
import importlib.util
import inspect
import sys
from pathlib import Path

import numpy as np
import pytest


SEAM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SEAM))


@pytest.fixture(scope="module")
def core():
    path = SEAM / "production_core.py"
    spec = importlib.util.spec_from_file_location("t084_production_core", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _haar(seed: int) -> np.ndarray:
    rng = np.random.Generator(np.random.PCG64(seed))
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    return q @ np.diag(diagonal / np.abs(diagonal))


def test_public_interfaces_and_balanced_pilot_contract(core):
    expected_signatures = {
        "balanced_pilots": ("n_pilots",),
        "make_latent_window": ("scenario", "latent_id", "payload_symbols", "max_pilots"),
        "observe_latent": ("latent", "snr_db", "n_pilots"),
        "receiver_action": ("arm", "x_pilots", "y_pilots", "y_payload", "parameter"),
        "score_action": ("action", "bits", "h_true"),
        "structure_mismatch_matrix": ("left", "right", "delta"),
    }
    for name, parameters in expected_signatures.items():
        assert tuple(inspect.signature(getattr(core, name)).parameters) == parameters

    p2 = np.array([[1, 1], [1, -1]], dtype=np.complex128)
    p4 = np.array([[1, 1, 1, 1], [1, 1j, -1, -1j]], dtype=np.complex128)
    for n_pilots in (2, 4, 8, 16):
        pilots = core.balanced_pilots(n_pilots)
        assert pilots.shape == (2, n_pilots)
        assert pilots.dtype == np.complex128
        assert np.array_equal(pilots @ pilots.conj().T, n_pilots * np.eye(2))
        assert np.array_equal(np.abs(pilots), np.ones_like(pilots.real))
    assert np.array_equal(core.balanced_pilots(2), p2)
    assert np.array_equal(core.balanced_pilots(4), p4)
    assert np.array_equal(core.balanced_pilots(8), np.tile(p4, (1, 2)))
    assert np.array_equal(core.balanced_pilots(16), np.tile(p4, (1, 4)))


@pytest.mark.parametrize("bad", [0, 1, 3, 6, 32, True, 2.0])
def test_balanced_pilots_rejects_unregistered_counts(core, bad):
    with pytest.raises(ValueError):
        core.balanced_pilots(bad)


@pytest.mark.parametrize(
    ("scenario", "scenario_code", "resolved", "scintillation_index"),
    [
        ("weak", 0, (11.6, 10.1), 0.193752),
        ("moderate", 1, (4.0, 1.9), 0.907895),
        ("strong", 2, (4.2, 1.4), 1.122449),
    ],
)
def test_authority_rng_namespace_and_exact_latent_replay(
    core, scenario, scenario_code, resolved, scintillation_index
):
    first = core.make_latent_window(scenario, 17, 12, 16)
    replay = core.make_latent_window(scenario, 17, 12, 16)

    snapshot = first["turbulence"]
    assert (snapshot["alpha"], snapshot["beta"]) == resolved
    assert snapshot["authority"] == (
        "projects/simulation/params.py::SimulationConfig().turbulence"
    )
    alpha, beta = resolved
    assert 1 / alpha + 1 / beta + 1 / (alpha * beta) == pytest.approx(
        scintillation_index, abs=5e-7
    )

    component_codes = {
        "payload_bits": 0,
        "channel_q": 1,
        "gg_gain": 2,
        "pilot_noise": 3,
        "payload_noise": 4,
        "mismatch_left": 5,
        "mismatch_right": 6,
    }
    assert set(first["rng_namespace"]) == set(component_codes)
    for name, component_code in component_codes.items():
        metadata = first["rng_namespace"][name]
        assert metadata == {
            "bit_generator": "PCG64",
            "entropy": 20260830,
            "spawn_key": [84, 1, scenario_code, 17, component_code],
        }

    for key in (
        "bits",
        "x_payload",
        "q",
        "pilot_noise",
        "payload_noise",
        "mismatch_left",
        "mismatch_right",
    ):
        assert np.array_equal(first[key], replay[key])
    assert first["gain"] == replay["gain"]
    assert first["latent_hashes"] == replay["latent_hashes"]

    bits_meta = first["rng_namespace"]["payload_bits"]
    seed_sequence = np.random.SeedSequence(
        bits_meta["entropy"], spawn_key=tuple(bits_meta["spawn_key"])
    )
    oracle_rng = np.random.Generator(np.random.PCG64(seed_sequence))
    oracle_bits = oracle_rng.integers(0, 2, size=(2, 48), dtype=np.int8)
    assert np.array_equal(first["bits"], oracle_bits)


def test_snr_changes_only_analytic_noise_scale(core):
    latent = core.make_latent_window("moderate", 31, 20, 16)
    low = core.observe_latent(latent, 10.0, 4)
    high = core.observe_latent(latent, 20.0, 4)

    assert low["latent_hashes"] == high["latent_hashes"] == latent["latent_hashes"]
    assert low["observation_hashes"] != high["observation_hashes"]
    assert np.array_equal(low["x_pilots"], high["x_pilots"])
    pilot_signal = latent["h_true"] @ low["x_pilots"]
    payload_signal = latent["h_true"] @ latent["x_payload"]
    for observation in (low, high):
        scale = observation["noise_scale"]
        assert np.allclose(
            (observation["y_pilots"] - pilot_signal) / scale,
            latent["pilot_noise"][:, :4],
            atol=2e-14,
        )
        assert np.allclose(
            (observation["y_payload"] - payload_signal) / scale,
            latent["payload_noise"],
            atol=2e-14,
        )
    assert low["noise_scale"] / high["noise_scale"] == pytest.approx(np.sqrt(10.0))


def test_np_changes_only_pilot_prefix_and_balanced_block(core):
    latent = core.make_latent_window("weak", 32, 10, 16)
    observations = {
        n: core.observe_latent(latent, 15.0, n) for n in (2, 4, 8, 16)
    }
    for observation in observations.values():
        assert observation["latent_hashes"] == latent["latent_hashes"]
        assert np.array_equal(observation["y_payload"], observations[2]["y_payload"])
        assert observation["latent_hashes"]["payload_bits"] == latent["latent_hashes"][
            "payload_bits"
        ]
        assert observation["latent_hashes"]["channel_q"] == latent["latent_hashes"][
            "channel_q"
        ]
        assert observation["latent_hashes"]["gg_gain"] == latent["latent_hashes"][
            "gg_gain"
        ]
        assert observation["latent_hashes"]["payload_noise"] == latent["latent_hashes"][
            "payload_noise"
        ]
    assert np.array_equal(
        observations[16]["pilot_noise"], latent["pilot_noise"][:, :16]
    )
    assert np.array_equal(
        observations[8]["pilot_noise"], observations[16]["pilot_noise"][:, :8]
    )
    assert np.array_equal(
        observations[4]["pilot_noise"], observations[8]["pilot_noise"][:, :4]
    )
    assert np.array_equal(
        observations[2]["pilot_noise"], observations[4]["pilot_noise"][:, :2]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "component_key",
        "entropy",
        "bit_generator",
        "spawn_scenario",
        "spawn_latent",
        "spawn_component",
    ],
)
def test_observe_rejects_any_rng_namespace_identity_mutation(core, mutation):
    latent = core.make_latent_window("moderate", 123, 8, 4)
    corrupted = copy.deepcopy(latent)
    if mutation == "component_key":
        corrupted["rng_namespace"]["unknown"] = corrupted["rng_namespace"].pop(
            "payload_bits"
        )
    elif mutation == "entropy":
        corrupted["rng_namespace"]["payload_bits"]["entropy"] += 1
    elif mutation == "bit_generator":
        corrupted["rng_namespace"]["payload_bits"]["bit_generator"] = "MT19937"
    elif mutation == "spawn_scenario":
        corrupted["rng_namespace"]["payload_bits"]["spawn_key"][2] = 0
    elif mutation == "spawn_latent":
        corrupted["rng_namespace"]["payload_bits"]["spawn_key"][3] = 124
    else:
        corrupted["rng_namespace"]["payload_bits"]["spawn_key"][4] = 1
    with pytest.raises(core.InvalidEstimate):
        core.observe_latent(corrupted, 10.0, 2)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("scenario", "weak"),
        ("alpha", 999.0),
        ("beta", 999.0),
        ("scintillation_index", 999.0),
        ("authority", "unregistered-authority"),
    ],
)
def test_observe_rejects_any_turbulence_authority_snapshot_mutation(
    core, field, bad_value
):
    latent = core.make_latent_window("moderate", 123, 8, 4)
    corrupted = copy.deepcopy(latent)
    corrupted["turbulence"][field] = bad_value
    with pytest.raises(core.InvalidEstimate):
        core.observe_latent(corrupted, 10.0, 2)


@pytest.mark.parametrize("bad_latent_id", [-1, True, "123", 1.5, 2**32, 124])
def test_observe_rejects_invalid_or_namespace_inconsistent_latent_id(
    core, bad_latent_id
):
    latent = core.make_latent_window("moderate", 123, 8, 4)
    corrupted = copy.deepcopy(latent)
    corrupted["latent_id"] = bad_latent_id
    with pytest.raises((ValueError, core.InvalidEstimate)):
        core.observe_latent(corrupted, 10.0, 2)


def test_b2_tau_one_and_c4_share_unitary_inverse_with_only_scale_different(core):
    u = _haar(100)
    v = _haar(101)
    singular_values = np.array([2.0, 0.7])
    h = (u * singular_values) @ v.conj().T
    x_pilots = core.balanced_pilots(4)
    y_pilots = h @ x_pilots
    y_payload = np.array([[1, 2j, -1], [0.5j, -0.5, 1j]], dtype=np.complex128)

    b2 = core.receiver_action("B2", x_pilots, y_pilots, y_payload, 1.0)
    c4 = core.receiver_action("C4", x_pilots, y_pilots, y_payload, None)
    u_ls, s_ls, vh_ls = np.linalg.svd(h, full_matrices=False)
    unitary_inverse = vh_ls.conj().T @ u_ls.conj().T

    assert b2["scale"] == pytest.approx(s_ls[0])
    assert c4["scale"] == pytest.approx(np.mean(s_ls))
    assert np.allclose(b2["w"] * b2["scale"], unitary_inverse, atol=2e-14)
    assert np.allclose(c4["w"] * c4["scale"], unitary_inverse, atol=2e-14)
    assert np.allclose(
        b2["w"] / c4["w"], c4["scale"] / b2["scale"], atol=2e-14
    )


def test_arms_without_one_public_singular_scale_use_none_not_nan(core):
    x = core.balanced_pilots(4)
    h = np.array([[1.2, 0.2j], [-0.1j, 0.8]], dtype=np.complex128)
    y_p = h @ x
    y = np.ones((2, 3), dtype=np.complex128)
    assert core.receiver_action("B0", x, y_p, y, None)["scale"] is None
    assert core.receiver_action("B2", x, y_p, y, 0.5)["scale"] is None


def test_b3_psc_matches_closed_form_and_truth_firewall(core):
    latent = core.make_latent_window("moderate", 43, 16, 4)
    observation = core.observe_latent(latent, 14.0, 4)
    args = (
        observation["x_pilots"],
        observation["y_pilots"],
        observation["y_payload"],
    )
    b2 = core.receiver_action("B2", *args, 1.0)
    b3 = core.receiver_action("B3_PSC", *args, 1.0)
    z_pilots = b2["w"] @ observation["y_pilots"]
    numerator = float(np.real(np.vdot(z_pilots, observation["x_pilots"])))
    denominator = float(np.vdot(z_pilots, z_pilots).real)
    expected = max(0.0, numerator / denominator)

    assert b3["psc_scale"] == pytest.approx(expected, abs=2e-15)
    assert np.allclose(b3["z"], expected * b2["z"], atol=2e-14)
    assert np.allclose(b3["w"], expected * b2["w"], atol=2e-14)
    assert np.array_equal(b3["h_hat"], b2["h_hat"])

    assert tuple(inspect.signature(core.receiver_action).parameters) == (
        "arm",
        "x_pilots",
        "y_pilots",
        "y_payload",
        "parameter",
    )
    receiver_source = inspect.getsource(core.receiver_action).lower()
    for forbidden in ("h_true", "bits", "decision", "truth"):
        assert forbidden not in receiver_source


def test_b3_psc_fail_closed_denominator_and_nonfinite_output(core):
    with pytest.raises(core.InvalidEstimate):
        core._pilot_scalar_calibration(
            np.eye(2, dtype=np.complex128),
            np.ones((2, 2), dtype=np.complex128),
            np.zeros((2, 2), dtype=np.complex128),
        )
    with pytest.raises(core.InvalidEstimate):
        core._pilot_scalar_calibration(
            np.eye(2, dtype=np.complex128),
            np.full((2, 2), 1e308, dtype=np.complex128),
            np.full((2, 2), 1e-308, dtype=np.complex128),
        )


def test_structure_mismatch_formula_power_and_ratio(core):
    g = 1.7
    u = _haar(201)
    v = _haar(202)
    ratios = []
    for delta in (0.0, 0.05, 0.10, 0.20, 0.40):
        h = core.structure_mismatch_matrix(g * u, v, delta)
        diagonal = np.diag([1.0 + delta, 1.0 - delta]) / np.sqrt(
            1.0 + delta**2
        )
        expected = g * u @ diagonal @ v.conj().T
        assert np.allclose(h, expected, atol=2e-14)
        assert np.linalg.norm(h, "fro") ** 2 / 2.0 == pytest.approx(g**2, abs=2e-14)
        singular_values = np.linalg.svd(h, compute_uv=False)
        ratios.append(float(singular_values[0] / singular_values[1]))
        assert ratios[-1] == pytest.approx((1 + delta) / (1 - delta), abs=2e-14)
    assert ratios == sorted(ratios)


def test_fail_closed_invalid_paths(core):
    for args in (
        ("unknown", 1, 8, 16),
        ("weak", -1, 8, 16),
        ("weak", 1, 0, 16),
        ("weak", 1, 8, 3),
    ):
        with pytest.raises(ValueError):
            core.make_latent_window(*args)

    latent = core.make_latent_window("weak", 1, 8, 4)
    for snr_db, n_pilots in ((np.nan, 2), (10.0, 8), (10.0, 3)):
        with pytest.raises((ValueError, core.InvalidEstimate)):
            core.observe_latent(latent, snr_db, n_pilots)

    x = core.balanced_pilots(2)
    y_p = np.eye(2, dtype=np.complex128) @ x
    y = np.ones((2, 4), dtype=np.complex128)
    with pytest.raises(ValueError):
        core.receiver_action("unknown", x, y_p, y, None)
    with pytest.raises(core.InvalidEstimate):
        core.receiver_action("C4", x, y_p * np.nan, y, None)
    with pytest.raises(ValueError):
        core.receiver_action("B2", x, y_p, y, 1.1)
    with pytest.raises(ValueError):
        core.receiver_action("B3_PSC", x, y_p, y, None)

    for delta in (-0.1, 1.0, np.nan):
        with pytest.raises((ValueError, core.InvalidEstimate)):
            core.structure_mismatch_matrix(np.eye(2), np.eye(2), delta)
    with pytest.raises(core.InvalidEstimate):
        core.structure_mismatch_matrix(np.ones((2, 2)), np.eye(2), 0.1)
    with pytest.raises(core.InvalidEstimate):
        core.structure_mismatch_matrix(np.eye(2), np.full((2, 2), np.nan), 0.1)


def test_offline_score_is_separate_and_validates_truth(core):
    latent = core.make_latent_window("strong", 51, 8, 4)
    observation = core.observe_latent(latent, 18.0, 4)
    action = core.receiver_action(
        "C4",
        observation["x_pilots"],
        observation["y_pilots"],
        observation["y_payload"],
        None,
    )
    score = core.score_action(action, latent["bits"], latent["h_true"])
    assert set(score) == {
        "bit_errors",
        "payload_bits",
        "ber",
        "channel_nmse",
        "inverse_residual",
        "rho",
    }
    assert 0 <= score["bit_errors"] <= score["payload_bits"]
    assert score["payload_bits"] == latent["bits"].size
    assert 0.0 <= score["ber"] <= 1.0
    with pytest.raises(core.InvalidEstimate):
        core.score_action(action, latent["bits"], np.zeros((2, 2)))
