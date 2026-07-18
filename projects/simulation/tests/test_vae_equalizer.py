from __future__ import annotations

import inspect

import numpy as np
import torch

from common._vae_equalizer import VQVAEEqualizer2x2


def _qpsk(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    signs = 1 - 2 * rng.integers(0, 2, size=(2, n))
    return (signs[0] + 1j * signs[1]) / np.sqrt(2)


def test_identity_initialization_and_shapes():
    eq = VQVAEEqualizer2x2(n_tap=29, device="cpu", seed=1)
    for fir in (eq.encoder, eq.decoder):
        assert fir.wxx[14] == 1 + 0j
        assert fir.wyy[14] == 1 + 0j
        assert torch.count_nonzero(fir.wxy) == 0
        assert torch.count_nonzero(fir.wyx) == 0
    x = torch.tensor(_qpsk(61, 2), dtype=torch.complex64)[None]
    out = eq(x, x)
    assert out["encoded_x"].shape == x.shape
    assert out["reconstructed_y"].shape == x.shape


def test_qpsk_hard_decision_and_ste_gradient():
    eq = VQVAEEqualizer2x2(n_tap=1, device="cpu", seed=2)
    z = torch.tensor([[2 + 0.1j, -0.1 - 3j]], dtype=torch.complex64,
                     requires_grad=True)
    hard, _ = eq.quantize(z)
    expected = torch.tensor([[1 + 1j, -1 - 1j]], dtype=torch.complex64) / np.sqrt(2)
    assert torch.allclose(hard, expected)
    q = eq.straight_through(z, hard)
    q.real.sum().backward()
    assert torch.equal(z.grad.real, torch.ones_like(z.grad.real))


def test_loss_formula_and_fit_is_blind():
    assert list(inspect.signature(VQVAEEqualizer2x2.fit).parameters) == [
        "self", "rX", "rY", "n_iterations", "verbose"
    ]
    eq = VQVAEEqualizer2x2(n_tap=1, rho=2.0, device="cpu", seed=3)
    x = torch.tensor(_qpsk(32, 3), dtype=torch.complex64)[None]
    out = eq(x, x)
    terms = eq.loss_terms(out, x, x)
    expected = terms["reconstruction"] + 2 * terms["commitment"]
    assert torch.allclose(terms["total"], expected)


def test_same_seed_reproduces_training_and_chunked_equalization():
    x, y = 1.2 * _qpsk(384, 4), 0.8 * _qpsk(384, 5)
    a = VQVAEEqualizer2x2(n_tap=3, batch_size=128, seed=9, device="cpu")
    b = VQVAEEqualizer2x2(n_tap=3, batch_size=128, seed=9, device="cpu")
    da = a.fit(x, y, n_iterations=8, verbose=False)
    db = b.fit(x, y, n_iterations=8, verbose=False)
    assert da["loss"] == db["loss"]
    assert np.array_equal(a.equalize(x, y, chunk_size=73)["zX"],
                          b.equalize(x, y, chunk_size=73)["zX"])


def test_fit_batches_never_join_sequence_end_to_start():
    x = np.arange(260, dtype=np.float32).astype(np.complex64)
    eq = VQVAEEqualizer2x2(n_tap=5, batch_size=128, seed=10, device="cpu")
    observed = []

    def capture_input(_module, args):
        observed.append(args[0].detach().cpu().numpy().real.ravel())

    handle = eq.encoder.register_forward_pre_hook(capture_input)
    eq.fit(x, x, n_iterations=3, verbose=False)
    handle.remove()

    training_batches = observed[:3]
    # Encoder + decoder each contribute a two-sample receptive-field radius.
    assert [len(batch) for batch in training_batches] == [132, 136, 8]
    for batch in training_batches:
        assert np.all(np.diff(batch) == 1), "a training chunk wrapped end-to-start"


def test_chunked_equalize_matches_full_encoder_with_random_weights():
    x, y = _qpsk(503, 20), _qpsk(503, 21)
    eq = VQVAEEqualizer2x2(n_tap=9, seed=22, device="cpu")
    generator = torch.Generator().manual_seed(23)
    with torch.no_grad():
        for parameter in eq.encoder.parameters():
            parameter.copy_(torch.randn(parameter.shape, generator=generator))
    with torch.no_grad():
        full_x, full_y = eq.encoder(
            torch.tensor(x, dtype=torch.complex64)[None],
            torch.tensor(y, dtype=torch.complex64)[None],
        )
    chunked = eq.equalize(x, y, chunk_size=67)
    assert np.allclose(chunked["zX"], full_x[0].numpy(), atol=1e-6)
    assert np.allclose(chunked["zY"], full_y[0].numpy(), atol=1e-6)


def test_small_identifiable_qpsk_mixture_improves_without_collapse():
    sx, sy = _qpsk(1024, 10), _qpsk(1024, 11)
    rx = 1.25 * sx + 0.25 * sy
    ry = -0.2 * sx + 0.8 * sy
    eq = VQVAEEqualizer2x2(
        n_tap=1, lr=0.01, batch_size=128, seed=12, device="cpu"
    )
    diagnostics = eq.fit(rx, ry, n_iterations=30, verbose=False)
    assert diagnostics["loss"][-1] < diagnostics["loss"][0]
    assert diagnostics["usage"] > 0.5
    assert diagnostics["finite"]
    z = eq.equalize(rx, ry, chunk_size=127)
    assert np.std(z["zX"]) > 0.2
    assert np.std(z["zY"]) > 0.2
