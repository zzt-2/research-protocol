"""Shared corrector adapter for the C04/C09 batch.

Both function classes (MLPCorrector, GRUCorrector) share:
  - Input contract: calibrate(z_calib) where z_calib is a [N, 2] complex dual-pol
    calibration slice (receiver-visible only; NO TX truth).
  - Output contract: get_correction() returns (A, b) where A is a 2x2 complex
    affine matrix and b is a 2-component complex offset.
  - Application: apply_correction(z_eval, A, b) -> z_corrected = z_eval @ A.T + b.

The candidate NEVER reads TX truth. The training loss (in run_corrector_batch.py)
is MSE(z_corrected, hard_16qam(z_corrected)) — receiver-visible pseudo-labels.

The difference between the function classes:
  - MLPCorrector: maps SUMMARY STATISTICS of z_calib (per-pol mean, variance,
    lag-1 autocorrelation, cross-correlation) to (A, b). Context = statistics.
  - GRUCorrector: encodes the full z_calib TIME SERIES through a GRU, maps the
    final hidden state to (A, b). Context = sequence.

Both are trained the SAME way (Adam, MSE on pseudo-labels, early stopping on
validation seeds). The adapter exposes a uniform interface so the runner can
treat them identically.

NOTE on the affine form: z_corrected_eval = A @ z_eval + b is the SAME
functional form as blind_affine_compare_16qam's closed-form ridge fit. The
difference is that the candidate's (A, b) is CONTEXT-DEPENDENT (varies with
z_calib), whereas blind affine's (A, b) is a single closed-form fit per slice.
A candidate that cannot model context-dependence will collapse to blind affine
(or worse).
"""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
import torch.nn as nn


def apply_correction(z_eval: np.ndarray, A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Apply the affine correction: z_corrected = z_eval @ A.T + b.

    z_eval: [N, 2] complex dual-pol evaluation slice.
    A: [2, 2] complex matrix.
    b: [2] complex offset.
    Returns: [N, 2] complex corrected slice.
    """
    z_eval = np.asarray(z_eval, dtype=np.complex128)
    A = np.asarray(A, dtype=np.complex128)
    b = np.asarray(b, dtype=np.complex128)
    if z_eval.ndim != 2 or z_eval.shape[1] != 2:
        raise ValueError(f"z_eval must be [N, 2], got {z_eval.shape}")
    if A.shape != (2, 2):
        raise ValueError(f"A must be (2, 2), got {A.shape}")
    if b.shape != (2,):
        raise ValueError(f"b must be (2,), got {b.shape}")
    return (z_eval @ A.T) + b[None, :]


def _z_to_real_features(z: np.ndarray) -> np.ndarray:
    """Convert a [N, 2] complex array to a real feature representation.

    For per-symbol features we stack [re(x), im(x), re(y), im(y)] → [N, 4].
    """
    z = np.asarray(z, dtype=np.complex128)
    return np.stack([z[:, 0].real, z[:, 0].imag, z[:, 1].real, z[:, 1].imag], axis=-1)


def _summary_statistics(z_calib: np.ndarray) -> np.ndarray:
    """Compute a compact receiver-visible context vector from z_calib.

    Returns a real feature vector capturing:
      - per-pol mean (4 reals: re/im of x-pol mean, re/im of y-pol mean)
      - per-pol variance (2 reals)
      - lag-1 autocorrelation magnitude per pol (2 reals)
      - cross-correlation x↔y (2 reals: real, imag)
    Total = 10 real features.
    """
    z = np.asarray(z_calib, dtype=np.complex128)
    x = z[:, 0]
    y = z[:, 1]
    feats = []
    # Means (4)
    feats.extend([x.mean().real, x.mean().imag, y.mean().real, y.mean().imag])
    # Variances (2)
    feats.extend([float(np.var(x)), float(np.var(y))])
    # Lag-1 autocorrelation magnitude per pol (2)
    if len(x) > 1:
        feats.append(float(np.abs(np.corrcoef(x[:-1].real, x[1:].real)[0, 1])))
        feats.append(float(np.abs(np.corrcoef(y[:-1].real, y[1:].real)[0, 1])))
    else:
        feats.extend([0.0, 0.0])
    # Cross-correlation x ↔ y (2: real and imag of E[x * conj(y)] / sqrt(var))
    denom = float(np.sqrt(np.var(x) * np.var(y)))
    if denom > 0:
        xc = np.mean(x * np.conj(y))  # complex scalar
        feats.extend([float(xc.real) / denom, float(xc.imag) / denom])
    else:
        feats.extend([0.0, 0.0])
    arr = np.asarray(feats, dtype=np.float32)
    # Replace NaNs / Infs with 0 (defensive; shouldn't occur for real z).
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return arr


# =============================================================================
# Output head: maps a real context embedding to (A, b) complex.
# =============================================================================

class _AffineHead(nn.Module):
    """Maps a real context embedding (hidden_dim,) to (A, b):
       A: 2x2 complex = 8 reals, b: 2 complex = 4 reals. Total 12 real outputs.
    """

    def __init__(self, hidden_dim: int):
        super().__init__()
        self.fc = nn.Linear(hidden_dim, 12)

    def forward(self, h: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        out = self.fc(h)
        # Split into A (8 reals → 2x2 complex) and b (4 reals → 2 complex).
        a_real = out[:, :8]
        b_real = out[:, 8:12]
        # Interpret as complex: pairs of (re, im).
        A = torch.complex(a_real[:, 0::2], a_real[:, 1::2]).view(-1, 2, 2)
        b = torch.complex(b_real[:, 0::2], b_real[:, 1::2]).view(-1, 2)
        return A, b


# =============================================================================
# C04: MLP corrector (context = summary statistics)
# =============================================================================

class MLPCorrector(nn.Module):
    """C04: maps z_calib summary statistics to a context-specific (A, b).

    Receiver-visible only. The training signal is the MSE between the affine-
    corrected z_calib and its hard_16qam pseudo-labels (computed in the runner).
    """

    def __init__(self, hidden_dim: int = 32, n_input_features: int = 10):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_input_features = n_input_features
        self.net = nn.Sequential(
            nn.Linear(n_input_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.head = _AffineHead(hidden_dim)
        # The calibration context (cached after calibrate()).
        self._context: torch.Tensor | None = None

    def calibrate(self, z_calib: np.ndarray) -> None:
        """Set the internal context from the calibration slice (receiver-visible)."""
        feats = _summary_statistics(z_calib)
        # Normalize features to unit norm (stabilizes training).
        norm = np.linalg.norm(feats)
        if norm > 0:
            feats = feats / norm
        device = next(self.parameters()).device
        self._context = torch.from_numpy(feats).float().unsqueeze(0).to(device)

    def forward(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Output (A, b) for the current calibration context.

        NOTE: this is a single forward() per calibration context (the context
        is what makes the affine context-dependent). The training loop calls
        this once per (training realization) and applies the SAME (A, b) to
        the whole calibration + eval slice.
        """
        if self._context is None:
            raise RuntimeError("calibrate() must be called before forward()")
        h = self.net(self._context)
        return self.head(h)

    def get_correction(self) -> tuple[np.ndarray, np.ndarray]:
        """Return (A, b) as numpy complex arrays. A: (2,2), b: (2,)."""
        A, b = self.forward()
        return A.detach().cpu().numpy().squeeze().astype(np.complex128), \
               b.detach().cpu().numpy().squeeze().astype(np.complex128)

    def set_context_from_features(self, feats: np.ndarray) -> None:
        """Set context directly from a feature vector (used in training)."""
        feats = np.asarray(feats, dtype=np.float32)
        norm = np.linalg.norm(feats)
        if norm > 0:
            feats = feats / norm
        # Place on the same device as the model parameters.
        device = next(self.parameters()).device
        self._context = torch.from_numpy(feats).float().unsqueeze(0).to(device)


# =============================================================================
# C09: GRU corrector (context = full calibration time series)
# =============================================================================

class GRUCorrector(nn.Module):
    """C09: encodes the z_calib time series with a GRU, maps the final hidden
    state to a context-specific (A, b). Receiver-visible only.
    """

    def __init__(self, hidden_dim: int = 32, gru_layers: int = 1):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.gru_layers = gru_layers
        # Input dim = 4 (re/im of x-pol, re/im of y-pol).
        self.gru = nn.GRU(input_size=4, hidden_size=hidden_dim,
                          num_layers=gru_layers, batch_first=True)
        self.head = _AffineHead(hidden_dim)
        self._sequence: torch.Tensor | None = None

    def calibrate(self, z_calib: np.ndarray) -> None:
        """Set the internal sequence from the calibration slice (receiver-visible)."""
        feats = _z_to_real_features(z_calib)  # [N, 4]
        # Normalize per-feature (mean/std over the sequence).
        mean = feats.mean(axis=0, keepdims=True)
        std = feats.std(axis=0, keepdims=True) + 1e-6
        feats = (feats - mean) / std
        device = next(self.parameters()).device
        self._sequence = torch.from_numpy(feats).float().unsqueeze(0).to(device)

    def forward(self) -> tuple[torch.Tensor, torch.Tensor]:
        if self._sequence is None:
            raise RuntimeError("calibrate() must be called before forward()")
        _, h = self.gru(self._sequence)  # h: [layers, 1, hidden]
        h_last = h[-1]  # [1, hidden]
        return self.head(h_last)

    def get_correction(self) -> tuple[np.ndarray, np.ndarray]:
        A, b = self.forward()
        return A.detach().cpu().numpy().squeeze().astype(np.complex128), \
               b.detach().cpu().numpy().squeeze().astype(np.complex128)

    def set_sequence_from_array(self, seq: np.ndarray) -> None:
        """Set sequence directly from a [N, 4] real array (used in training)."""
        seq = np.asarray(seq, dtype=np.float32)
        mean = seq.mean(axis=0, keepdims=True)
        std = seq.std(axis=0, keepdims=True) + 1e-6
        seq = (seq - mean) / std
        device = next(self.parameters()).device
        self._sequence = torch.from_numpy(seq).float().unsqueeze(0).to(device)


__all__ = [
    "apply_correction",
    "MLPCorrector",
    "GRUCorrector",
    "_summary_statistics",
    "_z_to_real_features",
]
