"""PROMPT-014 blind VQ-VAE core and shared dual-pol channel tests."""
from __future__ import annotations

import inspect
from pathlib import Path
import sys

import numpy as np
import pytest
import torch

from common import generate_shared_realization_dp
from common._gg_time import gg_time_envelope
from common._vae_equalizer import VQVAEEqualizer2x2
from params import SimulationConfig


EXPLORE_DIR = Path(__file__).resolve().parents[1] / "explore" / "cma-fade-divergence"
sys.path.insert(0, str(EXPLORE_DIR))
from r_lcr_ber_impact import gen_channel  # noqa: E402


def _qpsk(n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, 2 * n)
    return ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)


def _legacy_gen_channel_reference(N, alpha, beta, f_g, sop_rate, seed):
    """Frozen pre-extraction implementation used only for regression."""
    cfg = SimulationConfig()
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(
        N,
        alpha,
        beta,
        tau_c,
        block=100,
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

    sX, bitX = gen_qpsk()
    sY, bitY = gen_qpsk()
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
    return rX, rY, sX, sY, h, theta, bitX, bitY


def test_qin_faithful_initialization_and_shapes():
    equalizer = VQVAEEqualizer2x2(n_tap=29, device="cpu", seed=7)
    center = 14

    for fir in (equalizer.encoder, equalizer.decoder):
        assert fir.wxx_real[center].item() == 1.0
        assert fir.wyy_real[center].item() == 1.0
        assert torch.count_nonzero(fir.wxx_real).item() == 1
        assert torch.count_nonzero(fir.wyy_real).item() == 1
        for name in ("wxx_imag", "wxy_real", "wxy_imag", "wyx_real",
                     "wyx_imag", "wyy_imag"):
            assert torch.count_nonzero(getattr(fir, name)).item() == 0

    rX = torch.as_tensor(_qpsk(257, 1), dtype=torch.complex64).unsqueeze(0)
    rY = torch.as_tensor(_qpsk(257, 2), dtype=torch.complex64).unsqueeze(0)
    outputs = equalizer(rX, rY)
    assert outputs["encoded_x"].shape == (1, 257)
    assert outputs["quantized_y"].shape == (1, 257)
    assert outputs["reconstructed_x"].shape == (1, 257)


def test_fixed_qpsk_nearest_neighbor_quantization():
    equalizer = VQVAEEqualizer2x2(device="cpu", seed=3)
    points = torch.tensor(
        [[0.9 + 0.8j, -2.0 + 0.1j, -0.2 - 3.0j, 4.0 - 2.0j]],
        dtype=torch.complex64,
    )
    quantized, indices = equalizer.quantize(points)
    expected = torch.tensor(
        [[1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]], dtype=torch.complex64
    ) / np.sqrt(2)
    assert torch.allclose(quantized, expected)
    assert indices.tolist() == [[3, 1, 0, 2]]
    assert not any("codebook" in name for name, _ in equalizer.named_parameters())


def test_ste_propagates_gradients_to_encoder_and_decoder():
    equalizer = VQVAEEqualizer2x2(n_tap=5, device="cpu", seed=4)
    rX = torch.randn(2, 64, dtype=torch.complex64)
    rY = torch.randn(2, 64, dtype=torch.complex64)
    outputs = equalizer(rX, rY)
    losses = equalizer.loss_terms(outputs, rX, rY)
    losses["reconstruction"].backward()

    encoder_grad = sum(
        float(parameter.grad.abs().sum())
        for parameter in equalizer.encoder.parameters()
        if parameter.grad is not None
    )
    decoder_grad = sum(
        float(parameter.grad.abs().sum())
        for parameter in equalizer.decoder.parameters()
        if parameter.grad is not None
    )
    assert encoder_grad > 0.0
    assert decoder_grad > 0.0

    # With identity encoder/decoder and rho=1, the reconstruction and
    # commitment gradients cancel exactly at this symmetric initial point.
    equalizer.zero_grad(set_to_none=True)
    outputs = equalizer(rX, rY)
    equalizer.loss_terms(outputs, rX, rY)["total"].backward()
    total_encoder_grad = sum(
        float(parameter.grad.abs().sum())
        for parameter in equalizer.encoder.parameters()
        if parameter.grad is not None
    )
    assert total_encoder_grad == pytest.approx(0.0, abs=1e-7)


def test_fit_is_blind_and_seed_reproducible():
    assert list(inspect.signature(VQVAEEqualizer2x2.fit).parameters) == [
        "self", "rX", "rY", "n_iterations", "verbose"
    ]
    rX = 1.35 * _qpsk(512, 10)
    rY = 0.75 * _qpsk(512, 11)

    first = VQVAEEqualizer2x2(n_tap=5, batch_size=128, device="cpu", seed=22)
    second = VQVAEEqualizer2x2(n_tap=5, batch_size=128, device="cpu", seed=22)
    diag_first = first.fit(rX, rY, n_iterations=12, verbose=False)
    diag_second = second.fit(rX, rY, n_iterations=12, verbose=False)

    assert diag_first["total_loss"] == diag_second["total_loss"]
    out_first = first.equalize(rX, rY, chunk_size=173)
    out_second = second.equalize(rX, rY, chunk_size=173)
    assert np.array_equal(out_first["zX"], out_second["zX"])
    assert np.array_equal(out_first["zY"], out_second["zY"])


def test_fit_reduces_loss_and_keeps_codebook_healthy():
    rX = 1.4 * _qpsk(1024, 30)
    rY = 0.7 * _qpsk(1024, 31)
    equalizer = VQVAEEqualizer2x2(
        n_tap=1, lr=0.01, batch_size=128, device="cpu", seed=32
    )
    diagnostics = equalizer.fit(rX, rY, n_iterations=30, verbose=False)

    assert diagnostics["total_loss"][-1] < diagnostics["total_loss"][0]
    assert diagnostics["reconstruction_loss"]
    assert diagnostics["commitment_loss"]
    assert diagnostics["codebook_usage"]["fraction"] > 0.5
    assert not diagnostics["nan_detected"]
    assert diagnostics["seed"] == 32
    assert diagnostics["device"] == "cpu"


def test_different_inputs_do_not_collapse_to_same_output():
    equalizer = VQVAEEqualizer2x2(n_tap=1, device="cpu", seed=40)
    first = equalizer.equalize(_qpsk(256, 41), _qpsk(256, 42), chunk_size=64)
    second = equalizer.equalize(_qpsk(256, 43), _qpsk(256, 44), chunk_size=64)
    assert not np.array_equal(first["zX"], second["zX"])
    assert not np.array_equal(first["zY"], second["zY"])


def test_shared_dp_channel_is_bit_exact_with_legacy_generator():
    args = (511, 1.5, 0.8, 100.0, 4e-7, 1234)
    expected = _legacy_gen_channel_reference(*args)
    shared = generate_shared_realization_dp(
        args[0], alpha=args[1], beta=args[2], f_g=args[3],
        sop_rate=args[4], seed=args[5]
    )
    actual = tuple(shared[key] for key in (
        "rX", "rY", "sX", "sY", "h", "theta", "bitX", "bitY"
    ))
    assert all(np.array_equal(left, right) for left, right in zip(expected, actual))

    legacy_tuple = gen_channel(*args)
    assert all(
        np.array_equal(left, right)
        for left, right in zip(expected[:6], legacy_tuple)
    )


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
def test_cuda_smoke():
    equalizer = VQVAEEqualizer2x2(n_tap=5, device="cuda", seed=50)
    result = equalizer.equalize(_qpsk(64, 51), _qpsk(64, 52), chunk_size=64)
    assert result["zX"].shape == (64,)
