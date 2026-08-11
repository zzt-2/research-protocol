import hashlib
import importlib
from dataclasses import fields, replace
from pathlib import Path
import sys

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))


def _waveform_module():
    return importlib.import_module("waveform")


def _channel_module():
    return importlib.import_module("channel")


def _contract_module():
    return importlib.import_module("contract")


def _sha256_array(value):
    array = np.ascontiguousarray(value)
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


def _payload_and_data(contract_module, *, flip_coded_bit=False):
    information = np.zeros((2, 16, 1024), dtype=np.uint8)
    coded = np.zeros((2, 16, 1536), dtype=np.uint8)
    if flip_coded_bit:
        coded[1, 15, 1535] = 1
    groups = coded.reshape(2, 6144, 4)
    labels = (
        groups[..., 0] * 8 + groups[..., 1] * 4
        + groups[..., 2] * 2 + groups[..., 3]
    )
    axis = np.array([-3.0, -1.0, 3.0, 1.0], dtype=np.float64)
    data = (axis[labels >> 2] + 1j * axis[labels & 3]) / np.sqrt(10.0)
    return contract_module.PayloadTruth(information, coded), data.astype(np.complex128)


def test_registered_prefix_bytes_hashes():
    waveform = _waveform_module()
    prefix = waveform.registered_prefix()

    assert prefix.bits.shape == (32, 4)
    assert prefix.bits.dtype == np.uint8
    assert prefix.labels.shape == (32,)
    assert prefix.labels.dtype == np.uint8
    assert prefix.symbols.shape == (32,)
    assert prefix.symbols.dtype == np.complex128
    assert _sha256_array(prefix.bits) == (
        "1168a4cce1eef1403b4c609f0d2d15541ffd1cdfd175ca809da6701ad81c6d85"
    )
    assert _sha256_array(prefix.labels) == (
        "31c73fa861c3c9f27bbcb0d8cfcba7fcfccfc59f5e12429946d3720e196616b0"
    )
    assert _sha256_array(prefix.symbols) == (
        "69989be842342bf388cf2603be0a260f637da876dc912ed74deaed22ff9123c0"
    )
    assert _sha256_array(prefix.even_symbols) == (
        "81350b996fcc3f6ef91b05b83957c85b182f4df6bf1e31be48a0f31cca89a4bc"
    )
    assert _sha256_array(prefix.odd_symbols) == (
        "436cdb61597776f8dc045b0d8465265a3978ca089cdf41f1b50893a86a7e062a"
    )
    assert prefix.sample_mean_energy.hex() == float(1.0250000000000001).hex()


def test_registered_pilot_hashes_counts():
    waveform = _waveform_module()
    expected = {
        10: (684, 6860, "2c58efb90b9b4a82b676db4e219f21094cc0a546f54c126b1010764fc68375bd"),
        20: (325, 6501, "1d14610847c0023475cb03ff7a932fddc1202f02c2a7ca4c25d0fb544504af82"),
        100: (64, 6240, "17bdb8755470902084e9f1331fb6e36633332f9e2392a7d247e061ec1b0a810c"),
        200: (32, 6208, "0d515c32e1447d3d8b1a55d367b53feacafbee792989697fd4114161ca2357d4"),
    }

    for pilot_period, (pilot_count, total_symbols, expanded_sha) in expected.items():
        pilots = waveform.registered_pilots(pilot_period)
        assert pilots.cycle.shape == (4,)
        assert pilots.cycle.dtype == np.complex128
        assert _sha256_array(pilots.cycle) == (
            "db860e05d78202f159e28f16fbe26c8e060fc8c65c4b872c8bb3f7fc5915071e"
        )
        assert pilots.expanded.shape == (pilot_count,)
        assert _sha256_array(pilots.expanded) == expanded_sha
        assert pilots.pilot_count == pilot_count
        assert pilots.total_symbols == total_symbols


def test_data_time_map_bijective():
    waveform = _waveform_module()
    data = (
        np.arange(2 * 6144, dtype=np.float64).reshape(2, 6144)
        + 1j * np.arange(2 * 6144, dtype=np.float64).reshape(2, 6144)[::-1]
    ).astype(np.complex128)

    for pilot_period in (10, 20, 100, 200):
        built = waveform.build_waveform(data, N=pilot_period)
        ranks = built.time_to_data[built.data_to_time]
        assert np.array_equal(ranks, np.arange(6144, dtype=np.int64))
        assert np.unique(built.data_to_time).size == 6144
        assert np.count_nonzero(built.time_to_data >= 0) == 6144
        assert np.all(built.time_to_data[built.known_mask] == -1)
        assert built.time_to_data[-1] == -1
        assert built.known_mask[-1]
        for boundary in (1536, 3072, 4608):
            absolute_boundary = int(built.data_to_time[boundary])
            assert built.time_to_data[absolute_boundary] == boundary
            assert np.any(built.known_mask[absolute_boundary + 1 :])


def test_controlled_jump_copy_on_write():
    waveform = _waveform_module()
    data = np.vstack(
        (
            np.linspace(1.0, 2.0, 6144) + 1j * np.linspace(-2.0, -1.0, 6144),
            np.linspace(3.0, 4.0, 6144) + 1j * np.linspace(-4.0, -3.0, 6144),
        )
    ).astype(np.complex128)
    base = waveform.build_waveform(data, N=20)
    base_bytes = base.waveform.tobytes(order="C")
    boundary_after_data = 1536
    boundary_time = int(base.data_to_time[boundary_after_data])

    rotated = waveform.apply_persistent_rotation(
        base,
        target_pol=0,
        boundary_after_data=boundary_after_data,
        k=1,
    )

    assert base.waveform.tobytes(order="C") == base_bytes
    assert rotated.waveform[0, :boundary_time].tobytes(order="C") == (
        base.waveform[0, :boundary_time].tobytes(order="C")
    )
    assert rotated.waveform[1].tobytes(order="C") == base.waveform[1].tobytes(order="C")
    assert np.array_equal(
        rotated.waveform[0, boundary_time:],
        base.waveform[0, boundary_time:] * np.complex128(1j),
    )
    later_pilots = np.flatnonzero(base.known_mask & (np.arange(base.known_mask.size) >= boundary_time))
    assert later_pilots.size > 1
    assert np.array_equal(
        rotated.waveform[0, later_pilots],
        base.waveform[0, later_pilots] * np.complex128(1j),
    )
    assert rotated.known_symbols.tobytes(order="C") == base.known_symbols.tobytes(order="C")
    assert rotated.data_to_time.tobytes(order="C") == base.data_to_time.tobytes(order="C")
    assert rotated.time_to_data.tobytes(order="C") == base.time_to_data.tobytes(order="C")


def test_waveform_build_relational_validation_fail_closed():
    import pytest

    waveform = _waveform_module()
    data = np.zeros((2, 6144), dtype=np.complex128)
    base = waveform.build_waveform(data, N=20)

    def construct(**overrides):
        values = {
            "waveform": base.waveform,
            "known_symbols": base.known_symbols,
            "known_mask": base.known_mask,
            "data_to_time": base.data_to_time,
            "time_to_data": base.time_to_data,
            "N": base.N,
        }
        values.update(overrides)
        return waveform.WaveformBuild(**values)

    total = base.time_to_data.size
    mutations = []
    mutations.append({"N": 999})
    mutations.append({"waveform": base.waveform[:, :-1]})
    mutations.append({"known_symbols": base.known_symbols[:, :-1]})
    mutations.append({"known_mask": base.known_mask[:-1]})
    mutations.append({"data_to_time": base.data_to_time[:-1]})
    mutations.append({"time_to_data": base.time_to_data[:-1]})

    duplicate = base.data_to_time.copy()
    duplicate[1] = duplicate[0]
    mutations.append({"data_to_time": duplicate})

    out_of_range = base.data_to_time.copy()
    out_of_range[0] = total
    mutations.append({"data_to_time": out_of_range})

    broken_inverse = base.time_to_data.copy()
    broken_inverse[base.data_to_time[0]] = 1
    mutations.append({"time_to_data": broken_inverse})

    reordered_data_to_time = base.data_to_time.copy()
    reordered_data_to_time[:2] = reordered_data_to_time[1::-1]
    reordered_time_to_data = base.time_to_data.copy()
    reordered_time_to_data[reordered_data_to_time[0]] = 0
    reordered_time_to_data[reordered_data_to_time[1]] = 1
    mutations.append(
        {
            "data_to_time": reordered_data_to_time,
            "time_to_data": reordered_time_to_data,
        }
    )

    for position in (0, 32, total - 1):
        mask = base.known_mask.copy()
        mask[position] = False
        mutations.append({"known_mask": mask})
    data_marked_known = base.known_mask.copy()
    data_marked_known[base.data_to_time[0]] = True
    mutations.append({"known_mask": data_marked_known})

    for position in (0, 32, total - 1):
        known = base.known_symbols.copy()
        known[:, position] += 1.0 + 0.0j
        mutations.append({"known_symbols": known})
    data_reference = base.known_symbols.copy()
    data_reference[:, base.data_to_time[0]] = 1.0 + 0.0j
    mutations.append({"known_symbols": data_reference})

    nonfinite_waveform = base.waveform.copy()
    nonfinite_waveform[0, 0] = np.nan + 0.0j
    mutations.append({"waveform": nonfinite_waveform})
    nonfinite_known = base.known_symbols.copy()
    nonfinite_known[0, 0] = np.inf + 0.0j
    mutations.append({"known_symbols": nonfinite_known})

    for mutation in mutations:
        with pytest.raises((TypeError, ValueError)):
            construct(**mutation)

    assert base.N == 20
    for target_pol in (0, 1):
        for boundary_after_data in (1536, 3072, 4608):
            for state in (0, 1, 2, 3):
                rotated = waveform.apply_persistent_rotation(
                    base,
                    target_pol=target_pol,
                    boundary_after_data=boundary_after_data,
                    k=state,
                )
                for value in (
                    rotated.waveform,
                    rotated.known_symbols,
                    rotated.known_mask,
                    rotated.data_to_time,
                    rotated.time_to_data,
                ):
                    assert value.flags.writeable is False


def test_named_seedsequence_spawn_receipt():
    import pytest

    channel = _channel_module()
    names = ("payload_x", "payload_y", "gamma_gamma", "wiener", "awgn_x", "awgn_y")
    expected_states = (
        (3266050706, 1887055844, 1461557160, 2996136905),
        (3343219654, 1032298547, 699191632, 1868348364),
        (157891243, 1038186739, 3357904763, 3218992381),
        (2798376449, 1110574254, 2655777939, 437581613),
        (323304033, 3521305635, 2405495353, 528075890),
        (2365027968, 4151886221, 2472561045, 2584979073),
    )
    global_before = np.random.get_state()
    streams = channel.spawn_named_streams(999901)
    global_after = np.random.get_state()

    assert streams.names == names
    assert tuple(receipt.name for receipt in streams.receipts) == names
    assert tuple(receipt.child_generate_state_4_uint32 for receipt in streams.receipts) == (
        expected_states
    )
    for index, receipt in enumerate(streams.receipts):
        assert receipt.root_entropy == 999901
        assert receipt.numpy_version == np.__version__
        assert receipt.child_spawn_key == (index,)
        assert receipt.pool_size == 4
        assert getattr(streams, receipt.name).bit_generator.__class__ is np.random.PCG64
    assert global_before[0] == global_after[0]
    assert np.array_equal(global_before[1], global_after[1])
    assert global_before[2:] == global_after[2:]
    assert len(set(expected_states)) == 6

    for invalid in (True, -1, 1.5, "999901"):
        with pytest.raises((TypeError, ValueError)):
            channel.spawn_named_streams(invalid)


def test_stream_consumption_isolation():
    channel = _channel_module()
    isolated_names = ("gamma_gamma", "wiener", "awgn_x", "awgn_y")
    control = channel.spawn_named_streams(999901)
    perturbed = channel.spawn_named_streams(999901)
    perturbed.payload_x.integers(0, 2, size=10003, dtype=np.uint8)
    for name in isolated_names:
        expected = getattr(control, name).standard_normal(32)
        observed = getattr(perturbed, name).standard_normal(32)
        assert observed.tobytes(order="C") == expected.tobytes(order="C")

    forward = channel.spawn_named_streams(999901)
    reverse = channel.spawn_named_streams(999901)
    forward_bytes = {
        name: getattr(forward, name).standard_normal(8).tobytes(order="C")
        for name in forward.names
    }
    reverse_bytes = {
        name: getattr(reverse, name).standard_normal(8).tobytes(order="C")
        for name in reversed(reverse.names)
    }
    assert reverse_bytes == forward_bytes


def test_shared_gg_wiener_independent_awgn():
    from collections.abc import Mapping
    from dataclasses import fields, is_dataclass, replace
    import re

    import pytest

    channel = _channel_module()
    contract_module = _contract_module()
    waveform = _waveform_module()
    supplied = np.vstack(
        (
            np.linspace(0.25, 1.75, 16) + 1j * np.linspace(-0.5, 0.5, 16),
            np.linspace(-1.0, 0.5, 16) + 1j * np.linspace(1.5, -0.25, 16),
        )
    ).astype(np.complex128)
    one = channel.realize_supplied_waveform(
        supplied,
        streams=channel.spawn_named_streams(999901),
        snr_db=14,
        linewidth_hz=20000,
    )
    two = channel.realize_supplied_waveform(
        supplied,
        streams=channel.spawn_named_streams(999901),
        snr_db=14,
        linewidth_hz=20000,
    )

    assert one.intensity[0].tobytes(order="C") == one.intensity[1].tobytes(order="C")
    assert one.field_fade[0].tobytes(order="C") == one.field_fade[1].tobytes(order="C")
    assert one.phase[0].tobytes(order="C") == one.phase[1].tobytes(order="C")
    assert one.noise[0].tobytes(order="C") != one.noise[1].tobytes(order="C")
    for name in ("received", "intensity", "field_fade", "phase", "noise"):
        first = getattr(one, name)
        second = getattr(two, name)
        assert first.tobytes(order="C") == second.tobytes(order="C")
        assert first.flags.writeable is False
    expected = one.field_fade * supplied * np.exp(1j * one.phase) + one.noise
    assert np.array_equal(one.received, expected)

    owner = contract_module.load_contract(
        SIMULATION_ROOT.parent / "thesis-fso" / "coded-decoder-feedback-groundwork"
        / "d0-defect-smoke-contract.yaml"
    )
    payload_truth, data = _payload_and_data(contract_module)
    built = waveform.build_waveform(data, N=20)
    cell = next(
        cell
        for cell in owner.population_manifest
        if cell.snr_db == 14 and cell.linewidth_hz == 20000
    )
    receiver, truth = channel.build_views(
        owner, built, root_seed=999901, physical_cell=cell,
        payload_truth=payload_truth,
    )
    assert isinstance(receiver, contract_module.ReceiverView)
    assert isinstance(truth, contract_module.TruthView)
    assert receiver.received_samples.shape == built.waveform.shape
    assert truth.transmitted_symbols.shape == built.waveform.shape
    assert not np.shares_memory(receiver.received_samples, truth.transmitted_symbols)
    for dataclass_value in (receiver, truth):
        for field in fields(dataclass_value):
            value = getattr(dataclass_value, field.name)
            if isinstance(value, np.ndarray):
                assert value.flags.writeable is False
    truth_aliases = frozenset(
        (
        "information_bits",
        "coded_bits",
        "transmitted_symbols",
        "true_phase",
        "channel_h",
        "physical_snr_db",
        "fade",
        "noise_receipt",
        "event_label",
        "final_codeword_correctness",
        )
    )
    receiver_direct_fields = frozenset(field.name for field in fields(receiver))
    assert receiver_direct_fields.isdisjoint(truth_aliases)
    assert receiver.code_layout.information_bits_per_cw == 1024
    assert receiver.waveform_layout.data_symbols_per_polarization == 6144

    def normalized_name(value):
        return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")

    def assert_receipt_graph_truth_free(value, *, path="receipts", seen=None):
        if seen is None:
            seen = set()
        if isinstance(value, (str, bytes, int, float, complex, bool, type(None), np.generic)):
            return
        marker = id(value)
        if marker in seen:
            return
        seen.add(marker)
        if isinstance(value, np.ndarray):
            return
        if isinstance(value, Mapping):
            for key, item in value.items():
                if isinstance(key, str):
                    assert normalized_name(key) not in truth_aliases, f"{path}.{key}"
                assert_receipt_graph_truth_free(item, path=f"{path}.{key}", seen=seen)
            return
        if is_dataclass(value) and not isinstance(value, type):
            for field in fields(value):
                assert normalized_name(field.name) not in truth_aliases, f"{path}.{field.name}"
                assert_receipt_graph_truth_free(
                    getattr(value, field.name), path=f"{path}.{field.name}", seen=seen
                )
            return
        slots = getattr(type(value), "__slots__", ())
        if isinstance(slots, str):
            slots = (slots,)
        if slots:
            for name in slots:
                if not isinstance(name, str) or not hasattr(value, name):
                    continue
                assert normalized_name(name) not in truth_aliases, f"{path}.{name}"
                assert_receipt_graph_truth_free(
                    getattr(value, name), path=f"{path}.{name}", seen=seen
                )
            return
        if isinstance(value, (tuple, list, set, frozenset)):
            for index, item in enumerate(value):
                assert_receipt_graph_truth_free(
                    item, path=f"{path}[{index}]", seen=seen
                )

    assert_receipt_graph_truth_free(receiver.receipts)

    with pytest.raises((TypeError, ValueError)):
        channel.realize_supplied_waveform(
            supplied[:1], streams=channel.spawn_named_streams(1), snr_db=14,
            linewidth_hz=20000,
        )
    nonfinite = supplied.copy()
    nonfinite[0, 0] = np.nan
    with pytest.raises((TypeError, ValueError)):
        channel.realize_supplied_waveform(
            nonfinite, streams=channel.spawn_named_streams(1), snr_db=14,
            linewidth_hz=20000,
        )
    bad_cell = contract_module.PhysicalCell("bad", 11, 20000)
    with pytest.raises((TypeError, ValueError)):
        channel.build_views(
            owner, built, root_seed=999901, physical_cell=bad_cell,
            payload_truth=payload_truth,
        )
    with pytest.raises((TypeError, ValueError, PermissionError)):
        channel.build_views(
            replace(owner, schema_version="bad"),
            built,
            root_seed=999901,
            physical_cell=cell,
            payload_truth=payload_truth,
        )


def test_gamma_gamma_wiener_formulas():
    channel = _channel_module()
    symbol_period = 1.0 / 2.5e9
    tau = channel.gamma_gamma_tau_c(100.0)
    rho = channel.gamma_gamma_rho(100, symbol_period, tau)
    assert tau.hex() == (1.0 / (2.0 * np.pi * 100.0)).hex()
    assert rho.hex() == np.exp(-100.0 * symbol_period / tau).hex()
    assert rho.hex() == float(0.999974867574596).hex()

    for linewidth in (10000, 20000, 80000):
        observed = channel.wiener_innovation_variance(linewidth, symbol_period)
        expected = 2.0 * np.pi * linewidth * symbol_period
        assert observed.hex() == expected.hex()
        streams = channel.spawn_named_streams(999901)
        expected_streams = channel.spawn_named_streams(999901)
        expected_innovations = (
            expected_streams.wiener.standard_normal(8) * np.sqrt(expected)
        )
        phase = channel.generate_wiener_phase(
            8,
            rng=streams.wiener,
            linewidth_hz=linewidth,
            symbol_period_s=symbol_period,
        )
        assert phase[0].hex() == expected_innovations[0].hex()
        assert np.array_equal(phase, np.cumsum(expected_innovations, dtype=np.float64))
        assert phase.flags.writeable is False

    per_real, complex_power = channel.awgn_variances(10.0)
    gamma = 10.0 ** (10.0 / 10.0)
    assert per_real.hex() == (1.0 / (2.0 * gamma)).hex()
    assert complex_power.hex() == (1.0 / gamma).hex()


def _view_fixture():
    channel = _channel_module()
    contract_module = _contract_module()
    waveform = _waveform_module()
    owner = contract_module.load_contract(
        SIMULATION_ROOT.parent / "thesis-fso" / "coded-decoder-feedback-groundwork"
        / "d0-defect-smoke-contract.yaml"
    )
    payload, data = _payload_and_data(contract_module)
    built = waveform.build_waveform(data, N=20)
    cell = next(
        item for item in owner.population_manifest
        if item.snr_db == 14 and item.linewidth_hz == 20000
    )
    receiver, truth = channel.build_views(
        owner, built, root_seed=999901, physical_cell=cell,
        payload_truth=payload,
    )
    return channel, contract_module, waveform, owner, payload, built, cell, receiver, truth


def test_i19a_build_views_materializes_scalar_receiver_front_end():
    _, _, _, _, _, _, _, receiver_view, _ = _view_fixture()
    receiver = importlib.import_module("receiver")

    expected_samples = []
    expected_phases = []
    expected_c_post = []
    for pol in range(2):
        calibration = receiver.estimate_prefix_calibration(
            receiver_view.received_samples[pol, :32],
            receiver_view.known_prefix[pol],
        )
        equalized, _ = receiver.scalar_visible_power_equalize(
            receiver_view.received_samples[pol],
            c_pre_cplx=calibration.c_pre_cplx,
        )
        bps = receiver.run_common_bps(equalized, B=32, Nw=31)
        resolved = receiver.resolve_global_symmetry(
            bps.samples, receiver_view.known_prefix[pol]
        )
        expected_samples.append(resolved.samples)
        expected_phases.append(bps.phase_trace)
        expected_c_post.append(
            receiver.estimate_post_bps_residual(
                resolved.samples, receiver_view.known_prefix[pol]
            )
        )

    np.testing.assert_array_equal(
        receiver_view.equalized_samples, np.stack(expected_samples)
    )
    np.testing.assert_array_equal(
        receiver_view.common_cpr_phase_trace, np.stack(expected_phases)
    )
    assert not np.array_equal(
        receiver_view.equalized_samples, receiver_view.received_samples
    )
    assert not np.all(receiver_view.common_cpr_phase_trace == 0.0)
    assert receiver_view.receipts["receiver_front_end_id"] == (
        "scalar_per_pol_receiver_only_v1"
    )
    assert dict(receiver_view.receipts["common_bps"]) == {"B": 32, "Nw": 31}
    np.testing.assert_allclose(
        receiver_view.receipts["c_post_cplx_per_pol"], expected_c_post
    )


def test_i06_receiver_noise_is_observation_only():
    channel, _, _, _, _, _, _, receiver, _ = _view_fixture()
    observed = _independent_c_pre(receiver)
    assert receiver.receiver_noise_estimate.shape == (2,)
    assert receiver.receiver_noise_estimate.dtype == np.float64
    assert np.array_equal(receiver.receiver_noise_estimate, observed)
    assert receiver.receipts["receiver_noise_estimator_id"] == "known_prefix_ls_rss_over_31_v1"
    assert np.array_equal(receiver.receipts["receiver_noise_estimate_per_pol"], observed)
    forbidden = {"physical_snr", "physical_snr_db", "complex_noise_power", "snr_db"}
    assert forbidden.isdisjoint(receiver.receipts)
    assert not np.all(receiver.receiver_noise_estimate == channel.awgn_variances(14)[1])


def _independent_c_pre(receiver):
    observed = np.empty(2, dtype=np.float64)
    for pol in range(2):
        known = receiver.known_prefix[pol]
        received = receiver.received_samples[pol, :32]
        gain = np.sum(np.conj(known) * received) / np.sum(np.abs(known) ** 2)
        residual = received - gain * known
        observed[pol] = float(np.sum(np.abs(residual) ** 2) / 31.0)
    return observed


def test_i06_receiver_noise_estimate_is_init_free_derived():
    channel, contract_module, _, _, _, _, _, receiver, _ = _view_fixture()
    noise_field = next(
        item for item in fields(contract_module.ReceiverView)
        if item.name == "receiver_noise_estimate"
    )
    assert noise_field.init is False
    assert np.allclose(receiver.receiver_noise_estimate, _independent_c_pre(receiver))

    init_kwargs = {
        item.name: getattr(receiver, item.name)
        for item in fields(contract_module.ReceiverView)
        if item.init
    }
    for injected in (
        receiver.receiver_noise_estimate[::-1],
        np.full(2, channel.awgn_variances(14)[1], dtype=np.float64),
        np.array([0.0, 0.0], dtype=np.float64),
        np.array([0.1], dtype=np.float64),
    ):
        with pytest.raises(TypeError, match="receiver_noise_estimate"):
            contract_module.ReceiverView(
                **init_kwargs,
                receiver_noise_estimate=injected,
            )
        with pytest.raises(ValueError, match="init=False"):
            replace(receiver, receiver_noise_estimate=injected)

    changed_received = receiver.received_samples.copy()
    changed_received[0, :32] += np.linspace(0.0, 0.25, 32)
    replaced_received = replace(receiver, received_samples=changed_received)
    assert np.allclose(
        replaced_received.receiver_noise_estimate,
        _independent_c_pre(replaced_received),
    )
    assert not np.array_equal(
        replaced_received.receiver_noise_estimate,
        receiver.receiver_noise_estimate,
    )

    changed_known = receiver.known_prefix.copy()
    changed_known[1] *= np.exp(1j * np.linspace(0.0, 0.4, 32))
    replaced_known = replace(receiver, known_prefix=changed_known)
    assert np.allclose(
        replaced_known.receiver_noise_estimate,
        _independent_c_pre(replaced_known),
    )
    assert not np.array_equal(
        replaced_known.receiver_noise_estimate,
        receiver.receiver_noise_estimate,
    )

    forged_receipts = dict(receiver.receipts)
    forged_receipts["receiver_noise_estimate_per_pol"] = np.array([9.0, 8.0])
    forged_receipts["receiver_noise_estimator_id"] = "caller-forged"
    rebuilt = contract_module.ReceiverView(**{**init_kwargs, "receipts": forged_receipts})
    assert np.array_equal(
        rebuilt.receipts["receiver_noise_estimate_per_pol"],
        rebuilt.receiver_noise_estimate,
    )
    assert rebuilt.receipts["receiver_noise_estimator_id"] == (
        "known_prefix_ls_rss_over_31_v1"
    )
    with pytest.raises(contract_module.ContractError, match="truth alias"):
        contract_module.ReceiverView(
            **{
                **init_kwargs,
                "receipts": {"complex_noise_power": channel.awgn_variances(14)[1]},
            }
        )


def test_i06_payload_truth_lifecycle_complete():
    channel, contract_module, waveform, owner, payload, built, cell, receiver, truth = _view_fixture()
    assert truth.information_bits.shape == (2, 16, 1024)
    assert truth.coded_bits.shape == (2, 16, 1536)
    assert truth.final_codeword_correctness is None
    assert np.array_equal(truth.information_bits, payload.information_bits)
    assert np.array_equal(truth.coded_bits, payload.coded_bits)

    decoded = truth.information_bits.copy()
    decoded[1, 15, 0] ^= np.uint8(1)
    finalized = channel.finalize_truth_view(truth, decoded_information_bits=decoded)
    expected = np.ones((2, 16), dtype=np.bool_)
    expected[1, 15] = False
    assert np.array_equal(finalized.final_codeword_correctness, expected)
    assert finalized.final_codeword_correctness.flags.writeable is False
    assert truth.final_codeword_correctness is None
    with pytest.raises((TypeError, ValueError)):
        channel.finalize_truth_view(finalized, decoded_information_bits=decoded)
    with pytest.raises((TypeError, ValueError)):
        replace(truth, final_codeword_correctness=np.ones((2, 16), dtype=np.bool_))

    bad_payloads = (
        (np.zeros((1, 16, 1024), np.uint8), payload.coded_bits),
        (np.zeros((2, 15, 1024), np.uint8), payload.coded_bits),
        (np.zeros((2, 16, 1023), np.uint8), payload.coded_bits),
        (np.zeros((2, 16, 1024), np.bool_), payload.coded_bits),
        (np.full((2, 16, 1024), 2, np.uint8), payload.coded_bits),
        (np.full((2, 16, 1024), np.nan), payload.coded_bits),
        (payload.information_bits, np.zeros((1, 16, 1536), np.uint8)),
        (payload.information_bits, np.zeros((2, 15, 1536), np.uint8)),
        (payload.information_bits, np.zeros((2, 16, 1535), np.uint8)),
        (payload.information_bits, np.zeros((2, 16, 1536), np.bool_)),
        (payload.information_bits, np.full((2, 16, 1536), 2, np.uint8)),
        (payload.information_bits, np.full((2, 16, 1536), np.nan)),
    )
    for information, coded in bad_payloads:
        with pytest.raises((TypeError, ValueError)):
            contract_module.PayloadTruth(information, coded)

    for bad_decoded in (
        np.zeros((2, 16, 1023), np.uint8),
        np.zeros((2, 16, 1024), np.bool_),
        np.full((2, 16, 1024), 2, np.uint8),
        np.full((2, 16, 1024), np.nan),
    ):
        with pytest.raises((TypeError, ValueError)):
            channel.finalize_truth_view(truth, decoded_information_bits=bad_decoded)

    bad_coded_payload, bad_coded_data = _payload_and_data(
        contract_module, flip_coded_bit=True
    )
    with pytest.raises((TypeError, ValueError)):
        channel.build_views(
            owner, waveform.build_waveform(bad_coded_data, N=20),
            root_seed=999901, physical_cell=cell,
            payload_truth=bad_coded_payload,
        )
    changed_information = payload.information_bits.copy()
    changed_information[0, 0, 0] = 1
    with pytest.raises((TypeError, ValueError)):
        channel.build_views(
            owner, built, root_seed=999901, physical_cell=cell,
            payload_truth=contract_module.PayloadTruth(
                changed_information, payload.coded_bits
            ),
        )
    with pytest.raises((TypeError, ValueError)):
        channel.build_views(
            owner, waveform.build_waveform(np.zeros((2, 6144), np.complex128), N=20),
            root_seed=999901, physical_cell=cell, payload_truth=payload,
        )


def test_i06_truth_finalization_is_constructor_sealed():
    channel, contract_module, _, _, _, _, _, _, truth = _view_fixture()
    assert not hasattr(contract_module, "_TRUTH_FINALIZER_TOKEN")
    correctness_field = next(
        item for item in fields(contract_module.TruthView)
        if item.name == "final_codeword_correctness"
    )
    assert correctness_field.init is False
    assert truth.final_codeword_correctness is None

    pending_bytes = truth.information_bits.tobytes(order="C")
    init_kwargs = {
        item.name: getattr(truth, item.name)
        for item in fields(contract_module.TruthView)
        if item.init
    }
    forged_correctness = np.zeros((2, 16), dtype=np.bool_)
    with pytest.raises(TypeError, match="final_codeword_correctness"):
        contract_module.TruthView(
            **init_kwargs,
            final_codeword_correctness=forged_correctness,
        )
    with pytest.raises(ValueError, match="init=False"):
        replace(truth, final_codeword_correctness=forged_correctness)

    tampered_pending = replace(truth)
    object.__setattr__(
        tampered_pending,
        "final_codeword_correctness",
        forged_correctness,
    )
    with pytest.raises(contract_module.ContractError, match="pending|correctness"):
        channel.finalize_truth_view(
            tampered_pending,
            decoded_information_bits=truth.information_bits,
        )

    decoded = truth.information_bits.copy()
    decoded[0, 3, 11] ^= np.uint8(1)
    evaluated = channel.finalize_truth_view(
        truth,
        decoded_information_bits=decoded,
    )
    assert type(evaluated).__name__ == "EvaluatedTruthView"
    assert type(evaluated) is not type(truth)
    assert "final_codeword_correctness" not in {
        item.name for item in fields(type(evaluated))
    }
    expected = np.ones((2, 16), dtype=np.bool_)
    expected[0, 3] = False
    assert np.array_equal(evaluated.final_codeword_correctness, expected)
    assert evaluated.final_codeword_correctness.flags.writeable is False
    assert truth.final_codeword_correctness is None
    assert truth.information_bits.tobytes(order="C") == pending_bytes

    with pytest.raises(TypeError, match="final_codeword_correctness"):
        contract_module.EvaluatedTruthView(
            truth=truth,
            decoded_information_bits=decoded,
            final_codeword_correctness=forged_correctness,
        )
    with pytest.raises((TypeError, ValueError)):
        replace(evaluated, final_codeword_correctness=forged_correctness)
    with pytest.raises((TypeError, ValueError)):
        channel.finalize_truth_view(
            evaluated,
            decoded_information_bits=decoded,
        )

    for invalid in (
        np.zeros((2, 16, 1023), dtype=np.uint8),
        np.zeros((2, 16, 1024), dtype=np.bool_),
        np.full((2, 16, 1024), 2, dtype=np.uint8),
        np.full((2, 16, 1024), np.nan),
    ):
        with pytest.raises((TypeError, ValueError)):
            channel.finalize_truth_view(
                truth,
                decoded_information_bits=invalid,
            )


def test_i06_evaluated_correctness_is_derived_not_stored():
    channel, contract_module, _, _, _, _, _, _, truth = _view_fixture()
    decoded = truth.information_bits.copy()
    decoded[1, 7, 19] ^= np.uint8(1)
    evaluated = channel.finalize_truth_view(
        truth,
        decoded_information_bits=decoded,
    )
    assert "final_codeword_correctness" not in {
        item.name for item in fields(type(evaluated))
    }
    assert "final_codeword_correctness" not in type(evaluated).__slots__
    expected = np.ones((2, 16), dtype=np.bool_)
    expected[1, 7] = False
    first = evaluated.final_codeword_correctness
    assert np.array_equal(first, expected)
    assert first.flags.writeable is False

    forged = np.zeros((2, 16), dtype=np.bool_)
    with pytest.raises((AttributeError, TypeError)):
        object.__setattr__(evaluated, "final_codeword_correctness", forged)
    with pytest.raises((AttributeError, TypeError)):
        setattr(evaluated, "final_codeword_correctness", forged)
    with pytest.raises((TypeError, ValueError)):
        replace(evaluated, final_codeword_correctness=forged)
    with pytest.raises(TypeError, match="final_codeword_correctness"):
        contract_module.EvaluatedTruthView(
            truth=truth,
            decoded_information_bits=decoded,
            final_codeword_correctness=forged,
        )

    first.setflags(write=True)
    first[:] = False
    second = evaluated.final_codeword_correctness
    assert np.array_equal(second, expected)
    assert second.flags.writeable is False
    assert second is not first


def test_i06_receiver_noise_alias_family_fails_closed():
    channel, contract_module, _, _, _, _, _, receiver, _ = _view_fixture()
    init_kwargs = {
        item.name: getattr(receiver, item.name)
        for item in fields(contract_module.ReceiverView)
        if item.init
    }
    aliases = (
        "noise_samples",
        "NoiseSamples",
        "noise-samples",
        "NOISE_SAMPLES",
        "awgn_samples",
        "AWGNSamples",
        "physical-awgn-samples",
        "physicalAWGNSamples",
        "n0",
        "N_0",
        "n0Samples",
        "snrValue",
        "noiseVariance2",
    )
    physical = np.ones((2, 32), dtype=np.complex128)
    for alias in aliases:
        with pytest.raises(contract_module.ContractError, match="truth alias"):
            contract_module.ReceiverView(
                **{**init_kwargs, "receipts": {alias: physical}},
            )
        with pytest.raises(contract_module.ContractError, match="truth alias"):
            contract_module.ReceiverView(
                **{**init_kwargs, "b2_parameters": {alias: physical}},
            )

    safe = contract_module.ReceiverView(
        **{
            **init_kwargs,
            "receipts": {
                "receiver_noise_estimator_id": "forged",
                "receiver_noise_estimate_per_pol": np.array([9.0, 8.0]),
                "source_sha256": "a" * 64,
            },
        }
    )
    assert safe.receipts["receiver_noise_estimator_id"] == (
        "known_prefix_ls_rss_over_31_v1"
    )
    assert np.array_equal(
        safe.receipts["receiver_noise_estimate_per_pol"],
        safe.receiver_noise_estimate,
    )
    assert safe.receipts["source_sha256"] == "a" * 64


def test_i06_root_seed_requires_exact_builtin_int():
    channel, _, _, owner, payload, built, cell, _, _ = _view_fixture()
    invalid_roots = (
        np.int64(999901),
        np.int32(999901),
        np.uint64(999901),
        np.bool_(True),
        True,
        999901.0,
        "999901",
        -1,
        2**63,
    )
    for root in invalid_roots:
        with pytest.raises((TypeError, ValueError)):
            channel.spawn_named_streams(root)
        with pytest.raises((TypeError, ValueError)):
            channel.build_views(
                owner,
                built,
                root_seed=root,
                physical_cell=cell,
                payload_truth=payload,
            )
    assert channel.spawn_named_streams(999901).root_seed == 999901


def test_i06_seed_cell_scalar_bounds():
    channel, contract_module, _, owner, payload, built, cell, _, _ = _view_fixture()
    for root in (True, -1, 1.5, "1", 2**63):
        with pytest.raises((TypeError, ValueError)):
            channel.spawn_named_streams(root)
    for args in (
        (cell.cell_id, float(cell.snr_db), cell.linewidth_hz),
        (cell.cell_id, cell.snr_db, float(cell.linewidth_hz)),
        (cell.cell_id, True, cell.linewidth_hz),
        (cell.cell_id, cell.snr_db, True),
    ):
        with pytest.raises((TypeError, ValueError)):
            contract_module.PhysicalCell(*args)
    forged = replace(owner, population=replace(owner.population, symbol_rate_baud=2.4e9))
    with pytest.raises((TypeError, ValueError, PermissionError)):
        channel.build_views(
            forged, built, root_seed=999901, physical_cell=cell,
            payload_truth=payload,
        )
