from dataclasses import replace
import copy
from pathlib import Path
import importlib
import inspect
import sys
from types import SimpleNamespace

import numpy as np
import pytest


SIMULATION_ROOT = Path(__file__).resolve().parents[1]
D0_ROOT = SIMULATION_ROOT / "explore" / "coded-decoder-feedback"
if str(D0_ROOT) not in sys.path:
    sys.path.insert(0, str(D0_ROOT))

from contract import load_contract


OWNER = (
    SIMULATION_ROOT.parent
    / "thesis-fso"
    / "coded-decoder-feedback-groundwork"
    / "d0-defect-smoke-contract.yaml"
)


@pytest.fixture(scope="module")
def d0_contract():
    return load_contract(OWNER)


def _codec_module():
    """Import inside the test so an absent first production file is a valid RED."""
    importlib.invalidate_caches()
    return importlib.import_module("codec")


def _schemas_module():
    importlib.invalidate_caches()
    return importlib.import_module("schemas")


def _receiver_module():
    """Import inside the test so the new I09 module produces the intended RED."""
    importlib.invalidate_caches()
    return importlib.import_module("receiver")


def _methods_module():
    """Import inside the test so the new I12 module produces the intended RED."""
    importlib.invalidate_caches()
    return importlib.import_module("methods")


def test_rm01_one_complex_gain_uses_rss_over_31():
    receiver = _receiver_module()
    known = np.exp(1j * np.arange(32) * np.pi / 8.0)
    residual = np.linspace(-0.2, 0.2, 32) + 1j * np.linspace(0.3, -0.3, 32)
    residual -= known * (np.vdot(known, residual) / np.vdot(known, known))
    gain = 0.75 - 0.25j
    received = gain * known + residual

    calibration = receiver.estimate_prefix_calibration(received, known)
    rss = float(np.sum(np.abs(received - calibration.gain * known) ** 2))
    assert calibration.gain == pytest.approx(gain, abs=1e-15)
    assert calibration.c_pre_cplx == pytest.approx(rss / 31.0, abs=1e-15)
    assert calibration.c_pre_cplx != pytest.approx(rss / 32.0, abs=1e-12)
    assert calibration.receipt["estimator_id"] == "known_prefix_ls_rss_over_31_v1"


def test_rm02_scalar_equalizer_and_noiseless_branch():
    receiver = _receiver_module()
    samples = np.concatenate(
        (np.full(100, 2.0 + 0.0j), np.full(37, 1.0 + 1.0j))
    )
    equalized, receipt = receiver.scalar_visible_power_equalize(
        samples, c_pre_cplx=0.0
    )
    np.testing.assert_allclose(equalized[:100], 1.0 + 0.0j, atol=1e-15)
    np.testing.assert_allclose(
        equalized[100:], (1.0 + 1.0j) / np.sqrt(2.0), atol=1e-15
    )
    assert receipt["block_symbols"] == 100
    assert receipt["noiseless_branch"] is True

    noisy, _ = receiver.scalar_visible_power_equalize(
        np.full(100, 2.0 + 0.0j), c_pre_cplx=1.0
    )
    expected = 2.0 * np.sqrt(3.0) / 4.0
    np.testing.assert_allclose(noisy, expected, atol=1e-15)
    assert np.max(np.abs(receiver.scalar_visible_power_equalize(
        np.full(100, 100.0 + 0.0j), c_pre_cplx=1.0
    )[0])) <= 3.0


def test_rm03_common_bps_six_cell_exact_and_receipt():
    receiver = _receiver_module()
    from common._recovery import bps_cpr

    base = np.array(
        [-3 - 3j, -3 - 1j, -1 + 3j, 1 - 3j, 3 + 1j, 3 + 3j],
        dtype=np.complex128,
    ) / np.sqrt(10.0)
    samples = np.resize(base, 131) * np.exp(1j * np.linspace(0.0, 0.4, 131))
    for B in (32, 64):
        for Nw in (31, 61, 127):
            expected_samples, expected_phase = bps_cpr(samples, B=B, Nw=Nw, mod="qam16")
            result = receiver.run_common_bps(samples, B=B, Nw=Nw)
            np.testing.assert_array_equal(result.samples, expected_samples)
            np.testing.assert_array_equal(result.phase_trace, expected_phase)
            assert result.receipt == {
                "implementation": "common._recovery.bps_cpr",
                "modulation": "qam16",
                "B": B,
                "Nw": Nw,
                "edge_rule": "numpy_convolve_same_zero_padding_full_Nw_denominator",
            }


def test_rm04_common_bps_rejects_outside_frozen_six_cell_grid():
    receiver = _receiver_module()
    samples = np.ones(127, dtype=np.complex128)
    for B, Nw in ((16, 31), (32, 33), (48, 61), (64, 129)):
        with pytest.raises((TypeError, ValueError)):
            receiver.run_common_bps(samples, B=B, Nw=Nw)
    assert "snr" not in inspect.signature(receiver.run_common_bps).parameters


def test_rm05_global_resolution_uses_four_states_and_even_prefix_only():
    receiver = _receiver_module()
    known = np.resize(
        np.array([-3 - 3j, -1 + 3j, 3 + 1j, 1 - 1j]) / np.sqrt(10.0), 32
    )
    suffix = np.array([0.25 + 0.5j, -0.5 + 0.25j])
    reference = np.concatenate((known, suffix))
    for state in range(4):
        observed = reference * (1j**state)
        observed[1:32:2] += 100.0 - 50.0j
        result = receiver.resolve_global_symmetry(observed, known)
        assert result.state == state
        np.testing.assert_allclose(
            result.samples[0:32:2], known[0:32:2], rtol=0.0, atol=1e-14
        )
        np.testing.assert_allclose(
            result.samples[32:], suffix, rtol=0.0, atol=1e-14
        )
        assert result.receipt["candidate_states"] == (0, 1, 2, 3)
        assert result.receipt["selection_indices"] == tuple(range(0, 32, 2))


def test_rm06_post_bps_residual_is_odd_only_and_never_equalizer_input():
    receiver = _receiver_module()
    known = np.ones(32, dtype=np.complex128)
    resolved = np.ones(40, dtype=np.complex128)
    resolved[1:32:2] += 0.25j
    expected = np.mean(np.abs(resolved[1:32:2] - known[1:32:2]) ** 2)
    assert receiver.estimate_post_bps_residual(resolved, known) == pytest.approx(expected)

    even_mutant = resolved.copy()
    even_mutant[0:32:2] += 1e6
    assert receiver.estimate_post_bps_residual(even_mutant, known) == pytest.approx(expected)
    assert "c_post" not in inspect.signature(
        receiver.scalar_visible_power_equalize
    ).parameters


def test_decoder_hard_output_owner_goldens_and_opaque_authority():
    schemas_module = _schemas_module()
    zero_bits = np.zeros((16, 1024), dtype=np.uint8)
    first_bit = zero_bits.copy()
    first_bit[0, 0] = 1

    zero = schemas_module.build_decoder_hard_output_ref(zero_bits)
    first = schemas_module.build_decoder_hard_output_ref(first_bit)
    assert type(zero) is schemas_module.DecoderHardOutputRef
    assert zero.decoder_hard_output_sha256 == (
        "1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960"
    )
    assert first.decoder_hard_output_sha256 == (
        "9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e"
    )
    assert tuple(zero.payload) == (
        "schema",
        "cw_count",
        "information_bits_per_cw",
        "cw_order",
        "bit_packing",
        "decoded_information_bits_base64",
    )
    assert zero.payload["schema"] == "coded_decoder_feedback.d0.decoder_hard_output.v1"
    encoded = zero.payload["decoded_information_bits_base64"]
    assert len(encoded) == 2732 and encoded.endswith("=") and encoded.count("=") == 1
    assert not any(character.isspace() for character in encoded)

    schemas_module.assert_decoder_hard_output_ref(zero)
    schemas_module.assert_decoder_hard_output_ref(first)
    materialized = first.info_bits
    assert materialized.shape == (16, 1024)
    assert materialized.dtype == np.uint8
    materialized[0, 0] = 0
    assert first.info_bits[0, 0] == 1
    assert first.info_bits is not first.info_bits
    with pytest.raises(TypeError):
        schemas_module.DecoderHardOutputRef()
    with pytest.raises((TypeError, ValueError)):
        schemas_module.assert_decoder_hard_output_ref(copy.copy(first))


def test_decoder_hard_output_factory_and_store_fail_closed():
    schemas_module = _schemas_module()
    valid = np.zeros((16, 1024), dtype=np.uint8)
    invalid_bits = (
        np.zeros((1, 1024), dtype=np.uint8),
        np.zeros((16, 1023), dtype=np.uint8),
        np.zeros((16, 1024, 1), dtype=np.uint8),
        np.full((16, 1024), 2, dtype=np.int8),
        np.full((16, 1024), -1, dtype=np.int8),
        np.full((16, 1024), 0.5, dtype=np.float64),
        np.full((16, 1024), np.nan, dtype=np.float64),
        np.zeros((16, 1024), dtype=object),
        np.zeros((16, 1024), dtype=[("bit", np.int8)]),
    )
    for mutant in invalid_bits:
        with pytest.raises((TypeError, ValueError)):
            schemas_module.build_decoder_hard_output_ref(mutant)

    zero = schemas_module.build_decoder_hard_output_ref(valid)
    one = valid.copy()
    one[0, 0] = 1
    first = schemas_module.build_decoder_hard_output_ref(one)
    records = (zero.store_record, first.store_record)
    roots = frozenset(
        (zero.decoder_hard_output_sha256, first.decoder_hard_output_sha256)
    )
    schemas_module.validate_decoder_hard_output_store(records, referenced_roots=roots)

    wrong_root = dict(zero.store_record)
    wrong_root["decoder_hard_output_sha256"] = "0" * 64
    changed_payload = dict(zero.store_record)
    changed_payload["payload"] = dict(changed_payload["payload"])
    changed_payload["payload"]["decoded_information_bits_base64"] = (
        "B" + changed_payload["payload"]["decoded_information_bits_base64"][1:]
    )
    for mutant_records, mutant_roots in (
        ((zero.store_record, zero.store_record), roots),
        ((zero.store_record,), roots),
        (records, frozenset((zero.decoder_hard_output_sha256,))),
        ((wrong_root, first.store_record), roots),
        ((changed_payload, first.store_record), roots),
    ):
        with pytest.raises((TypeError, ValueError)):
            schemas_module.validate_decoder_hard_output_store(
                mutant_records, referenced_roots=mutant_roots
            )


def test_gray16_roundtrip_rotation():
    codec_module = _codec_module()
    labels = np.arange(16, dtype=np.uint8)
    bit_weights = np.array([8, 4, 2, 1], dtype=np.uint8)
    bits = ((labels[:, None] & bit_weights) != 0).astype(np.uint8)

    symbols = codec_module.gray16_map(bits)
    axis = np.array([-3.0, -1.0, 3.0, 1.0]) / np.sqrt(10.0)
    expected = axis[2 * bits[:, 0] + bits[:, 1]] + 1j * axis[
        2 * bits[:, 2] + bits[:, 3]
    ]
    np.testing.assert_array_equal(symbols, expected)
    np.testing.assert_array_equal(codec_module.gray16_hard_demap(symbols), bits)

    for state in range(4):
        rotated = codec_module.rotate_gray16(symbols, state=state)
        np.testing.assert_allclose(rotated, symbols * (1j**state), rtol=0.0, atol=1e-15)
        assert codec_module.rotation_state(rotated, symbols) == state


def test_ldpc_noiseless_roundtrip_one_cw(d0_contract):
    codec_module = _codec_module()
    codec = codec_module.D0Codec(d0_contract)
    info = np.random.default_rng(20260810).integers(0, 2, size=(16, 1024), dtype=np.uint8)

    coded = codec.encode(info)
    assert coded.shape == (16, 1536)
    llr = np.where(coded == 1, 30.0, -30.0)
    decoded = codec.decode_fresh(
        llr,
        cw_ids=tuple(f"RM08-CW{i}" for i in range(16)),
        candidate_id="RM08",
    )
    assert type(decoded.hard_output) is _schemas_module().DecoderHardOutputRef
    np.testing.assert_array_equal(decoded.info_bits, info)

    metadata = codec.live_metadata
    assert metadata.sionna_version == "2.0.1"
    assert metadata.base_graph == "bg2"
    assert metadata.lifting_size == 104
    assert metadata.interleaver == "3gpp-ts-38.212-5.4.2.2"
    assert decoded.receipt.truth_correction is False


class _CountingBackend:
    def __init__(self):
        self.initial_states = []

    def decode(self, llr, *, message_state=None, warm_state=None):
        self.initial_states.append((message_state, warm_state))
        if message_state is not None or warm_state is not None:
            raise AssertionError("decoder message/warm state reuse tripwire")
        return np.zeros((llr.shape[0], 1024), dtype=np.uint8)


class _CountingBackendFactory:
    def __init__(self):
        self.calls = 0
        self.backend = None

    def __call__(self, **_kwargs):
        self.calls += 1
        self.backend = _CountingBackend()
        return self.backend


def test_every_decode_fresh_state(d0_contract):
    codec_module = _codec_module()
    factory = _CountingBackendFactory()
    codec = codec_module.D0Codec(d0_contract, backend_factory=factory)

    for candidate_id in ("B1", "B2"):
        cw_batch = 16
        decoded = codec.decode_fresh(
            np.zeros((cw_batch, 1536), dtype=np.float64),
            cw_ids=tuple(f"{candidate_id}-{i}" for i in range(cw_batch)),
            candidate_id=candidate_id,
        )
        assert decoded.receipt.cw_batch == cw_batch
        assert decoded.receipt.restart is True
        assert decoded.receipt.bp_iterations == 20 * cw_batch

    assert factory.calls == 1  # backend object caching is permitted
    assert factory.backend.initial_states == [(None, None), (None, None)]

    with pytest.raises(AssertionError, match="state reuse tripwire"):
        factory.backend.decode(
            np.zeros((1, 1536)), message_state=object(), warm_state=None
        )


def test_b1_exact_reencode_nll(d0_contract):
    codec_module = _codec_module()
    codec = codec_module.D0Codec(d0_contract)
    c_hat = np.array([[0, 1, 1, 0]], dtype=np.uint8)
    llr = np.array([[2.0, 2.0, -3.0, -3.0]], dtype=np.float64)
    expected = np.logaddexp(0.0, (1.0 - 2.0 * c_hat) * llr).mean()

    assert codec.reencode_nll(c_hat, llr) == pytest.approx(expected, abs=1e-15)
    assert codec.reencode_nll(np.repeat(c_hat, 3, axis=1), np.repeat(llr, 3, axis=1)) == pytest.approx(
        expected, abs=1e-15
    )
    assert codec.llr_semantics == "positive_means_bit_1"
    assert codec.demapper_preclip == 30.0
    assert codec.decoder_llr_max == 20.0
    assert codec.decoder_iterations == 20
    assert codec.per_real_noise_power(0.5) == pytest.approx(0.25, abs=0.0)


def test_codec_rejects_wrong_contract_identity(d0_contract):
    codec_module = _codec_module()
    control = d0_contract.control
    code = d0_contract.population.code
    mutants = (
        replace(d0_contract, schema_version="coded_decoder_feedback.d0.v4"),
        replace(d0_contract, control=replace(control, epoch=13)),
        replace(d0_contract, control=replace(control, checkpoint="CP013")),
        replace(d0_contract, control=replace(control, decision="D012")),
        replace(d0_contract, control=replace(control, verification="V006")),
        replace(d0_contract, control=replace(control, execution_authorized=True)),
        replace(
            d0_contract,
            control=replace(control, scientific_experiment_authorized=True),
        ),
        replace(
            d0_contract,
            population=replace(
                d0_contract.population,
                code=replace(code, family="lookalike_bg2"),
            ),
        ),
    )

    for mutant in mutants:
        with pytest.raises((TypeError, ValueError, PermissionError)):
            codec_module.D0Codec(mutant)


class _OutputBackend:
    def __init__(self, output):
        self.output = output

    def decode(self, _llr, *, message_state=None, warm_state=None):
        assert message_state is None
        assert warm_state is None
        return self.output


def test_codec_rejects_nonbinary_backend_output(d0_contract):
    codec_module = _codec_module()
    llr = np.zeros((16, 1536), dtype=np.float64)
    bad_outputs = (
        np.full((16, 1024), 2, dtype=np.int64),
        np.full((16, 1024), 0.5, dtype=np.float64),
        np.full((16, 1024), np.nan, dtype=np.float64),
        np.zeros((16, 1024), dtype=object),
        np.zeros((16, 1024), dtype=[("bit", np.int8)]),
        np.zeros((1, 1024), dtype=np.uint8),
    )

    for bad_output in bad_outputs:
        codec = codec_module.D0Codec(
            d0_contract,
            backend_factory=lambda output=bad_output, **_kwargs: _OutputBackend(output),
        )
        with pytest.raises((TypeError, ValueError, RuntimeError)):
            codec.decode_fresh(
                llr,
                cw_ids=tuple(f"CW{i}" for i in range(16)),
                candidate_id="NEGATIVE",
            )

    expected = np.tile(np.arange(1024) % 2, (16, 1))
    for dtype in (np.bool_, np.int64, np.float64):
        output = expected.astype(dtype)
        codec = codec_module.D0Codec(
            d0_contract,
            backend_factory=lambda output=output, **_kwargs: _OutputBackend(output),
        )
        decoded = codec.decode_fresh(
            llr,
            cw_ids=tuple(f"CW{i}" for i in range(16)),
            candidate_id="LEGAL",
        )
        assert decoded.info_bits.dtype == np.uint8
        np.testing.assert_array_equal(decoded.info_bits, expected.astype(np.uint8))


def test_codec_rejects_boolean_noise_power(d0_contract):
    codec_module = _codec_module()
    codec = codec_module.D0Codec(d0_contract)

    for value in (True, False, np.bool_(True), np.bool_(False)):
        with pytest.raises((TypeError, ValueError)):
            codec.per_real_noise_power(value)

    for value, expected in ((0, 0.0), (0.0, 0.0), (1, 0.5), (0.5, 0.25)):
        assert codec.per_real_noise_power(value) == pytest.approx(expected, abs=0.0)


class _MethodSpyCodec:
    """Small deterministic codec double; production orchestration remains real."""

    def __init__(self):
        self.decode_calls = []
        self.demap_inputs = []

    def demap(self, samples, *, complex_noise_power):
        value = np.asarray(samples, dtype=np.complex128)
        assert value.shape == (6144,)
        assert complex_noise_power == 0.25
        state = int(
            np.argmin(
                [abs(value[0] - np.exp(-0.5j * np.pi * k)) for k in range(4)]
            )
        )
        # k=2 and k=3 deliberately tie so the owner tie-break is exercised.
        scores = (4.0, 2.0, 1.0, 1.0)
        llr = np.full((16, 1536), scores[state], dtype=np.float64)
        self.demap_inputs.append(value.copy())
        return llr.reshape(-1)

    def decode_fresh(self, llr, *, cw_ids, candidate_id):
        value = np.asarray(llr, dtype=np.float64)
        self.decode_calls.append((candidate_id, tuple(cw_ids), value.copy()))
        info_bits = np.zeros((16, 1024), dtype=np.uint8)
        return SimpleNamespace(info_bits=info_bits, candidate_id=candidate_id)

    def encode(self, info_bits):
        assert np.asarray(info_bits).shape == (16, 1024)
        return np.zeros((16, 1536), dtype=np.uint8)

    @staticmethod
    def reencode_nll(_coded, llr):
        return float(np.asarray(llr, dtype=np.float64)[0, 0])


def test_rm11_b0_one_decode_and_b1_four_fresh_candidates_with_tie_break():
    methods = _methods_module()
    samples = np.ones(6144, dtype=np.complex128)
    cw_ids = tuple(f"RM11-CW{i}" for i in range(16))

    b0_codec = _MethodSpyCodec()
    b0 = methods.run_b0(
        b0_codec,
        samples,
        complex_noise_power=0.25,
        cw_ids=cw_ids,
    )
    assert b0.method_id == "COMMON_BPS_PLUS_ONE_LDPC"
    assert b0.selected_rotation_k == 0
    assert len(b0_codec.decode_calls) == 1

    b1_codec = _MethodSpyCodec()
    b1 = methods.run_b1(
        b1_codec,
        samples,
        complex_noise_power=0.25,
        cw_ids=cw_ids,
    )
    assert b1.method_id == "GLOBAL_FOUR_ROTATION_DECODER_SELECTION"
    assert b1.selected_rotation_k == 2
    assert b1.candidate_scores == (4.0, 2.0, 1.0, 1.0)
    assert [call[0] for call in b1_codec.decode_calls] == [
        "B1_K0",
        "B1_K1",
        "B1_K2",
        "B1_K3",
    ]
    assert len({id(call[2]) for call in b1_codec.decode_calls}) == 4
    for k, demap_input in enumerate(b1_codec.demap_inputs):
        np.testing.assert_allclose(
            demap_input,
            samples * np.exp(-0.5j * np.pi * k),
            rtol=0.0,
            atol=1e-15,
        )


def _issue_rm_deployment_seal(d0_contract):
    verify = importlib.import_module("verify")
    contract = importlib.import_module("contract")
    receiver_view = contract.ReceiverView(
        received_samples=np.ones((2, 6240), dtype=np.complex128),
        equalized_samples=np.ones((2, 6240), dtype=np.complex128),
        common_cpr_phase_trace=np.zeros((2, 6240), dtype=np.float64),
        known_prefix=np.ones((2, 32), dtype=np.complex128),
        periodic_pilots=np.ones((2, 64), dtype=np.complex128),
        code_layout=d0_contract.population.code,
        waveform_layout=contract.WaveformLayout(32, 100, 6144, 6240),
        b2_parameters={}, receipts={},
    )
    resolved = contract.ResolvedDevFreeze(
        "5" * 64,
        {
            "common_bps": (
                {"tuple_id": "M2_N100", "winner": {"B": 32, "Nw": 31}},
            ),
            "final_b2_tuple": {"tuple_id": "M2_N100"},
        },
        {"dev_freeze_sha256": "5" * 64},
    )
    receipts = tuple(
        {"phase": phase, "dev_freeze_sha256": resolved.freeze_id}
        for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4")
    )
    return verify.DeploymentBoundary(verify.deployment_callable_registry()).seal(
        d0_contract, receiver_view, resolved,
        phase="D0_UNIT_TEST", phase_receipts=receipts,
    )


def test_rm12_nine_copy_on_write_fixtures_and_outputs_frozen_o1_only(d0_contract):
    methods = _methods_module()
    clean = np.vstack(
        (
            np.linspace(1.0, 2.0, 6144) + 1j * np.linspace(-0.5, 0.5, 6144),
            np.linspace(-2.0, -1.0, 6144) + 1j * np.linspace(0.5, -0.5, 6144),
        )
    ).astype(np.complex128)
    clean_before = clean.copy()
    seal_codec = _MethodSpyCodec()
    cw_ids = tuple(f"RM12-SEAL-CW{i}" for i in range(16))
    b0 = methods.run_b0(
        seal_codec, clean[0], complex_noise_power=0.25, cw_ids=cw_ids
    )
    b1 = methods.run_b1(
        seal_codec, clean[0], complex_noise_power=0.25, cw_ids=cw_ids
    )
    deployment_seal = _issue_rm_deployment_seal(d0_contract)
    authority_fixture = methods.inject_controlled_fixture(
        clean, target_polarization=0, boundary_after_data=1536, rotation_k=1
    )
    frozen = methods.freeze_deployable_outputs(
        b0=b0, b1=b1, deployment_seal=deployment_seal,
        fixture=authority_fixture,
    )
    assert frozen.is_frozen is True
    with pytest.raises((TypeError, ValueError)):
        methods.freeze_deployable_outputs(
            b0=SimpleNamespace(method_id="COMMON_BPS_PLUS_ONE_LDPC"),
            b1=SimpleNamespace(method_id="GLOBAL_FOUR_ROTATION_DECODER_SELECTION"),
            deployment_seal=deployment_seal,
            fixture=authority_fixture,
        )

    fixture_ids = []
    for boundary_after_data in (1536, 3072, 4608):
        for rotation_k in (1, 2, 3):
            fixture = methods.inject_controlled_fixture(
                clean,
                target_polarization=0,
                boundary_after_data=boundary_after_data,
                rotation_k=rotation_k,
            )
            fixture_ids.append(fixture.fixture_id)
            frozen = methods.freeze_deployable_outputs(
                b0=b0, b1=b1, deployment_seal=deployment_seal, fixture=fixture
            )
            np.testing.assert_array_equal(clean, clean_before)
            assert not fixture.samples.flags.writeable
            np.testing.assert_array_equal(
                fixture.samples[1], clean_before[1]
            )
            np.testing.assert_array_equal(
                fixture.samples[0, :boundary_after_data],
                clean_before[0, :boundary_after_data],
            )

            codec = _MethodSpyCodec()
            result = methods.evaluate_o1_inverse(
                codec,
                fixture,
                frozen_outputs=frozen,
                complex_noise_power=0.25,
                cw_ids=tuple(f"RM12-CW{i}" for i in range(16)),
            )
            np.testing.assert_allclose(
                result.corrected_samples,
                clean_before,
                rtol=0.0,
                atol=1e-14,
            )
            assert result.method_id == "TRUTH_BOUNDARY_ROTATION_CORRECTION"
            assert result.evaluator_only is True
            assert len(codec.decode_calls) == 1

    assert fixture_ids == [
        "B04_K1", "B04_K2", "B04_K3",
        "B08_K1", "B08_K2", "B08_K3",
        "B12_K1", "B12_K2", "B12_K3",
    ]
    with pytest.raises((TypeError, ValueError, PermissionError)):
        methods.evaluate_o1_inverse(
            _MethodSpyCodec(),
            methods.inject_controlled_fixture(
                clean, target_polarization=0, boundary_after_data=1536, rotation_k=1
            ),
            frozen_outputs=object(),
            complex_noise_power=0.25,
            cw_ids=tuple(f"NEG-CW{i}" for i in range(16)),
        )
    assert "evaluate_o1_inverse" not in inspect.getsource(_receiver_module())
    assert "TruthView" not in inspect.getsource(methods.run_b0)
    assert "TruthView" not in inspect.getsource(methods.run_b1)


def test_i19a_o1_requires_issued_fixture_outputs_and_authenticated_deployment_seal(
    d0_contract,
):
    methods = _methods_module()
    verify = importlib.import_module("verify")
    contract = importlib.import_module("contract")
    total = 6240
    receiver_view = contract.ReceiverView(
        received_samples=np.ones((2, total), dtype=np.complex128),
        equalized_samples=np.ones((2, total), dtype=np.complex128),
        common_cpr_phase_trace=np.zeros((2, total), dtype=np.float64),
        known_prefix=np.ones((2, 32), dtype=np.complex128),
        periodic_pilots=np.ones((2, 64), dtype=np.complex128),
        code_layout=d0_contract.population.code,
        waveform_layout=contract.WaveformLayout(32, 100, 6144, total),
        b2_parameters={},
        receipts={},
    )
    resolved = contract.ResolvedDevFreeze(
        "5" * 64,
        {
            "common_bps": (
                {"tuple_id": "M2_N100", "winner": {"B": 32, "Nw": 31}},
            ),
            "final_b2_tuple": {"tuple_id": "M2_N100"},
        },
        {"dev_freeze_sha256": "5" * 64},
    )
    phase_receipts = tuple(
        {"phase": phase, "dev_freeze_sha256": resolved.freeze_id}
        for phase in ("S1", "S2", "S3_DEV", "S3_TEST", "S4")
    )
    deployment_seal = verify.DeploymentBoundary(
        verify.deployment_callable_registry()
    ).seal(
        d0_contract,
        receiver_view,
        resolved,
        phase="D0_UNIT_TEST",
        phase_receipts=phase_receipts,
    )
    clean = np.ones((2, 6144), dtype=np.complex128)
    fixture = methods.inject_controlled_fixture(
        clean, target_polarization=0, boundary_after_data=1536, rotation_k=1
    )
    codec = _MethodSpyCodec()
    cw_ids = tuple(f"I19A-CW{i}" for i in range(16))
    b0 = methods.run_b0(codec, clean[0], complex_noise_power=0.25, cw_ids=cw_ids)
    b1 = methods.run_b1(codec, clean[0], complex_noise_power=0.25, cw_ids=cw_ids)
    frozen = methods.freeze_deployable_outputs(
        b0=b0,
        b1=b1,
        deployment_seal=deployment_seal,
        fixture=fixture,
    )
    assert methods.evaluate_o1_inverse(
        _MethodSpyCodec(), fixture, frozen_outputs=frozen,
        complex_noise_power=0.25, cw_ids=cw_ids,
    ).evaluator_only

    with pytest.raises(PermissionError, match="controlled"):
        methods.FrozenDeployableOutputs(b0=b0, b1=b1)
    with pytest.raises(PermissionError, match="controlled"):
        methods.ControlledFixture(
            samples=fixture.samples,
            target_polarization=0,
            boundary_after_data=1536,
            boundary_time=1536,
            rotation_k=1,
            fixture_id="B04_K1",
        )
    with pytest.raises(PermissionError):
        methods.freeze_deployable_outputs(
            b0=b0, b1=b1, deployment_seal=object(), fixture=fixture
        )
    with pytest.raises(PermissionError):
        methods.evaluate_o1_inverse(
            _MethodSpyCodec(), fixture,
            frozen_outputs=copy.copy(frozen),
            complex_noise_power=0.25, cw_ids=cw_ids,
        )
    forged = object.__new__(methods.FrozenDeployableOutputs)
    with pytest.raises(PermissionError):
        methods.evaluate_o1_inverse(
            _MethodSpyCodec(), fixture, frozen_outputs=forged,
            complex_noise_power=0.25, cw_ids=cw_ids,
        )
    object.__setattr__(frozen, "fixture_id", "FORGED")
    with pytest.raises(PermissionError, match="tampered"):
        methods.evaluate_o1_inverse(
            _MethodSpyCodec(), fixture, frozen_outputs=frozen,
            complex_noise_power=0.25, cw_ids=cw_ids,
        )
