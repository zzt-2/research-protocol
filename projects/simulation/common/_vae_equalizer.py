"""Blind 1-sps 2x2 complex-FIR VQ-VAE equalizer.

The objective follows Qin (2026), Eq. (13)/(15): reconstruction MSE plus
``rho`` times the encoder-to-fixed-codebook commitment MSE.  The QPSK
codebook is fixed; no transmitted symbols or labels enter :meth:`fit`.
"""
from __future__ import annotations

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F


class _ComplexButterflyFIR(nn.Module):
    """Four complex FIRs forming a same-length 2x2 butterfly."""

    def __init__(self, n_tap: int) -> None:
        super().__init__()
        if n_tap <= 0 or n_tap % 2 == 0:
            raise ValueError("n_tap must be a positive odd integer")
        self.n_tap = int(n_tap)
        center = n_tap // 2
        for branch in ("wxx", "wxy", "wyx", "wyy"):
            real = torch.zeros(n_tap, dtype=torch.float32)
            imag = torch.zeros(n_tap, dtype=torch.float32)
            if branch in ("wxx", "wyy"):
                real[center] = 1.0
            self.register_parameter(f"{branch}_real", nn.Parameter(real))
            self.register_parameter(f"{branch}_imag", nn.Parameter(imag))

    def _weight(self, name: str) -> torch.Tensor:
        return torch.complex(getattr(self, f"{name}_real"),
                             getattr(self, f"{name}_imag"))

    @property
    def wxx(self) -> torch.Tensor:
        return self._weight("wxx")

    @property
    def wxy(self) -> torch.Tensor:
        return self._weight("wxy")

    @property
    def wyx(self) -> torch.Tensor:
        return self._weight("wyx")

    @property
    def wyy(self) -> torch.Tensor:
        return self._weight("wyy")

    def _fir(self, signal: torch.Tensor, weight: torch.Tensor) -> torch.Tensor:
        half = self.n_tap // 2
        windows = F.pad(signal, (half, half)).unfold(-1, self.n_tap, 1)
        return torch.einsum("...nl,l->...n", windows, weight)

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        return (
            self._fir(x, self.wxx) + self._fir(y, self.wxy),
            self._fir(x, self.wyx) + self._fir(y, self.wyy),
        )


class VQVAEEqualizer2x2(nn.Module):
    """Blind VQ-VAE with linear 2x2 complex FIR encoder and decoder."""

    def __init__(
        self,
        n_tap: int = 29,
        lr: float = 0.01,
        batch_size: int = 128,
        rho: float = 1.0,
        device: str | torch.device = "cpu",
        seed: int = 0,
    ) -> None:
        super().__init__()
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        self.n_tap = int(n_tap)
        self.lr = float(lr)
        self.batch_size = int(batch_size)
        self.rho = float(rho)
        self.device = torch.device(device)
        self.seed = int(seed)
        torch.manual_seed(self.seed)
        if self.device.type == "cuda":
            torch.cuda.manual_seed_all(self.seed)
        self.encoder = _ComplexButterflyFIR(self.n_tap)
        self.decoder = _ComplexButterflyFIR(self.n_tap)
        constellation = torch.tensor(
            [-1 - 1j, -1 + 1j, 1 - 1j, 1 + 1j],
            dtype=torch.complex64,
        ) / np.sqrt(2.0)
        self.register_buffer("constellation", constellation)
        self.to(self.device)

    def _tensor(self, values: np.ndarray | torch.Tensor) -> torch.Tensor:
        return torch.as_tensor(values, dtype=torch.complex64, device=self.device)

    def quantize(self, z: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        distances = torch.abs(z[..., None] - self.constellation) ** 2
        indices = distances.argmin(dim=-1)
        return self.constellation[indices], indices

    @staticmethod
    def straight_through(z: torch.Tensor, hard: torch.Tensor) -> torch.Tensor:
        return z + (hard - z).detach()

    def forward(self, rX: torch.Tensor, rY: torch.Tensor) -> dict[str, torch.Tensor]:
        rX, rY = self._tensor(rX), self._tensor(rY)
        encoded_x, encoded_y = self.encoder(rX, rY)
        hard_x, indices_x = self.quantize(encoded_x)
        hard_y, indices_y = self.quantize(encoded_y)
        quantized_x = self.straight_through(encoded_x, hard_x)
        quantized_y = self.straight_through(encoded_y, hard_y)
        reconstructed_x, reconstructed_y = self.decoder(quantized_x, quantized_y)
        return {
            "encoded_x": encoded_x,
            "encoded_y": encoded_y,
            "hard_x": hard_x,
            "hard_y": hard_y,
            "quantized_x": quantized_x,
            "quantized_y": quantized_y,
            "indices_x": indices_x,
            "indices_y": indices_y,
            "reconstructed_x": reconstructed_x,
            "reconstructed_y": reconstructed_y,
        }

    @staticmethod
    def _complex_mse(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.mean(torch.abs(a - b) ** 2)

    def loss_terms(
        self,
        outputs: dict[str, torch.Tensor],
        rX: torch.Tensor,
        rY: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        rX, rY = self._tensor(rX), self._tensor(rY)
        reconstruction = 0.5 * (
            self._complex_mse(outputs["reconstructed_x"], rX)
            + self._complex_mse(outputs["reconstructed_y"], rY)
        )
        commitment = 0.5 * (
            self._complex_mse(outputs["encoded_x"], outputs["hard_x"].detach())
            + self._complex_mse(outputs["encoded_y"], outputs["hard_y"].detach())
        )
        return {
            "reconstruction": reconstruction,
            "commitment": commitment,
            "total": reconstruction + self.rho * commitment,
        }

    def fit(self, rX, rY, n_iterations, verbose=False):
        """Fit blindly on deterministic consecutive chunks.

        ``n_iterations`` intentionally has no default: the caller must state the
        total update budget rather than this implementation guessing one.
        """
        x, y = self._tensor(rX).flatten(), self._tensor(rY).flatten()
        if x.numel() != y.numel() or x.numel() == 0:
            raise ValueError("rX and rY must be non-empty and equally sized")
        if not isinstance(n_iterations, (int, np.integer)) or n_iterations <= 0:
            raise ValueError("n_iterations must be an explicit positive integer")

        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        total_history: list[float] = []
        reconstruction_history: list[float] = []
        commitment_history: list[float] = []
        n = x.numel()
        cursor = 0
        # The reconstruction path traverses both FIRs, so its receptive-field
        # radius is twice that of one same-padded FIR.
        halo = self.n_tap - 1
        self.train()
        for update in range(int(n_iterations)):
            start = cursor
            end = min(start + self.batch_size, n)
            cursor = 0 if end == n else end
            ext_start = max(0, start - halo)
            ext_end = min(n, end + halo)
            chunk_x = x[ext_start:ext_end][None, :]
            chunk_y = y[ext_start:ext_end][None, :]
            bx, by = x[start:end][None, :], y[start:end][None, :]
            optimizer.zero_grad(set_to_none=True)
            outputs = self(chunk_x, chunk_y)
            center_start = start - ext_start
            center_end = center_start + (end - start)
            center_outputs = {
                key: value[..., center_start:center_end]
                for key, value in outputs.items()
            }
            terms = self.loss_terms(center_outputs, bx, by)
            terms["total"].backward()
            optimizer.step()
            total_history.append(float(terms["total"].detach().cpu()))
            reconstruction_history.append(float(terms["reconstruction"].detach().cpu()))
            commitment_history.append(float(terms["commitment"].detach().cpu()))
            if verbose:
                print(f"update={update + 1} loss={total_history[-1]:.6g}")

        result = self.equalize(x, y, chunk_size=self.batch_size)
        decisions = np.concatenate([result["indicesX"], result["indicesY"]])
        usage = float(np.unique(decisions).size / self.constellation.numel())
        finite = bool(np.isfinite(total_history).all())
        return {
            "loss": total_history,
            "usage": usage,
            "finite": finite,
            "total_loss": total_history,
            "reconstruction_loss": reconstruction_history,
            "commitment_loss": commitment_history,
            "codebook_usage": {"fraction": usage, "count": int(round(4 * usage))},
            "nan_detected": not finite,
            "seed": self.seed,
            "device": str(self.device),
        }

    def equalize(self, rX, rY, chunk_size=4096):
        """Encode in overlapping chunks, avoiding full-sequence activations."""
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        x, y = self._tensor(rX).flatten(), self._tensor(rY).flatten()
        if x.numel() != y.numel():
            raise ValueError("rX and rY must be equally sized")
        half = self.n_tap // 2
        zx_parts, zy_parts, ix_parts, iy_parts = [], [], [], []
        self.eval()
        with torch.no_grad():
            for start in range(0, x.numel(), int(chunk_size)):
                end = min(start + int(chunk_size), x.numel())
                ext_start, ext_end = max(0, start - half), min(x.numel(), end + half)
                zx, zy = self.encoder(x[ext_start:ext_end][None], y[ext_start:ext_end][None])
                left = start - ext_start
                width = end - start
                zx, zy = zx[0, left:left + width], zy[0, left:left + width]
                _, ix = self.quantize(zx)
                _, iy = self.quantize(zy)
                zx_parts.append(zx.cpu())
                zy_parts.append(zy.cpu())
                ix_parts.append(ix.cpu())
                iy_parts.append(iy.cpu())
        zX = torch.cat(zx_parts).numpy() if zx_parts else np.empty(0, np.complex64)
        zY = torch.cat(zy_parts).numpy() if zy_parts else np.empty(0, np.complex64)
        indicesX = torch.cat(ix_parts).numpy() if ix_parts else np.empty(0, np.int64)
        indicesY = torch.cat(iy_parts).numpy() if iy_parts else np.empty(0, np.int64)
        return {"zX": zX, "zY": zY, "indicesX": indicesX, "indicesY": indicesY}
