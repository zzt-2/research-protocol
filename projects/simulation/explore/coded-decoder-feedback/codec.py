"""Truth-free Gray-16QAM and fresh 5G-NR LDPC adapter for D0.

The Sionna backend is constructed lazily.  This module deliberately does not
runtime-import any P08 module: its numerical conventions are source-bound here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

import numpy as np

from contract import D0Contract, assert_action_authorized
from schemas import DecoderHardOutputRef, build_decoder_hard_output_ref


_AXIS = np.array([-3.0, -1.0, 3.0, 1.0], dtype=np.float64) / np.sqrt(10.0)


def _as_bit_groups(bits: np.ndarray) -> np.ndarray:
    value = np.asarray(bits)
    if value.ndim < 1 or value.shape[-1] != 4:
        raise ValueError("Gray-16QAM bits must have final dimension 4")
    if not np.all((value == 0) | (value == 1)):
        raise ValueError("Gray-16QAM bits must be binary")
    return value.astype(np.uint8, copy=False)


def gray16_map(bits: np.ndarray) -> np.ndarray:
    """Map bit groups ``[b0,b1,b2,b3]`` to unit-power square 16QAM."""
    value = _as_bit_groups(bits)
    i_index = 2 * value[..., 0] + value[..., 1]
    q_index = 2 * value[..., 2] + value[..., 3]
    return _AXIS[i_index] + 1j * _AXIS[q_index]


def gray16_hard_demap(symbols: np.ndarray) -> np.ndarray:
    """Nearest-neighbour hard demap preserving the input symbol shape."""
    value = np.asarray(symbols)
    i_index = np.argmin(np.abs(value.real[..., None] - _AXIS), axis=-1).astype(np.uint8)
    q_index = np.argmin(np.abs(value.imag[..., None] - _AXIS), axis=-1).astype(np.uint8)
    return np.stack(
        (i_index // 2, i_index % 2, q_index // 2, q_index % 2), axis=-1
    ).astype(np.uint8, copy=False)


def _validate_rotation_state(state: int) -> int:
    if isinstance(state, (bool, np.bool_)) or not isinstance(state, (int, np.integer)):
        raise TypeError("rotation state must be an integer")
    state = int(state)
    if state not in (0, 1, 2, 3):
        raise ValueError("rotation state must be one of 0,1,2,3")
    return state


def rotate_gray16(symbols: np.ndarray, *, state: int) -> np.ndarray:
    """Apply the exact coordinate rotation represented by an integer state."""
    state = _validate_rotation_state(state)
    return np.asarray(symbols) * (1j**state)


def rotation_state(rotated: np.ndarray, reference: np.ndarray) -> int:
    """Recover the unique legal coordinate rotation, failing on ambiguity."""
    rotated_value = np.asarray(rotated)
    reference_value = np.asarray(reference)
    if rotated_value.shape != reference_value.shape:
        raise ValueError("rotated and reference arrays must have identical shapes")
    matches = [
        state
        for state in range(4)
        if np.allclose(
            rotated_value,
            reference_value * (1j**state),
            rtol=0.0,
            atol=1e-15,
        )
    ]
    if len(matches) != 1:
        raise ValueError("rotation does not identify exactly one legal state")
    return matches[0]


@dataclass(frozen=True)
class LiveCodecMetadata:
    sionna_version: str
    base_graph: str
    lifting_size: int
    interleaver: str


@dataclass(frozen=True)
class DecodeReceipt:
    cw_batch: int
    restart: bool
    bp_iterations: int
    truth_correction: bool = False


@dataclass(frozen=True)
class DecodeBatch:
    hard_output: DecoderHardOutputRef
    receipt: DecodeReceipt
    cw_ids: tuple[str, ...]
    candidate_id: str

    @property
    def info_bits(self) -> np.ndarray:
        """Compatibility view; every read is a fresh authority materialization."""
        return self.hard_output.info_bits


class _SionnaBackend:
    """Small CPU-only wrapper whose decoder never retains message state."""

    def __init__(self) -> None:
        import sionna
        import torch
        from sionna.phy.fec.ldpc import (
            LDPC5GDecoder,
            LDPC5GEncoder,
            cn_update_offset_minsum,
        )

        if sionna.__version__ != "2.0.1":
            raise RuntimeError(f"unsupported Sionna version: {sionna.__version__}")
        self._torch = torch
        self.encoder = LDPC5GEncoder(
            k=1024,
            n=1536,
            num_bits_per_symbol=4,
            device="cpu",
        )
        if (
            getattr(self.encoder, "_bg", None) != "bg2"
            or getattr(self.encoder, "_z", None) != 104
            or getattr(self.encoder, "_num_bits_per_symbol", None) != 4
        ):
            raise RuntimeError("live Sionna BG/Z/interleaver metadata mismatch")
        out_int = np.asarray(self.encoder.out_int.detach().cpu())
        out_int_inv = np.asarray(self.encoder.out_int_inv.detach().cpu())
        expected = np.arange(1536)
        if (
            out_int.shape != (1536,)
            or out_int_inv.shape != (1536,)
            or not np.array_equal(out_int[out_int_inv], expected)
        ):
            raise RuntimeError("live Sionna interleaver permutation is invalid")

        def normalized_min_sum(msg_v2c, mask, llr_clipping=None):
            return 0.75 * cn_update_offset_minsum(
                msg_v2c, mask, llr_clipping, offset=0.0
            )

        self.decoder = LDPC5GDecoder(
            self.encoder,
            num_iter=20,
            cn_update=normalized_min_sum,
            hard_out=True,
            return_infobits=True,
            llr_max=20.0,
            return_state=False,
            device="cpu",
        )
        self.metadata = LiveCodecMetadata(
            sionna_version=sionna.__version__,
            base_graph="bg2",
            lifting_size=104,
            interleaver="3gpp-ts-38.212-5.4.2.2",
        )

    def encode(self, info_bits: np.ndarray) -> np.ndarray:
        tensor = self._torch.as_tensor(info_bits, dtype=self._torch.float32, device="cpu")
        with self._torch.no_grad():
            coded = self.encoder(tensor)
        return coded.detach().cpu().numpy().astype(np.uint8, copy=False)

    def decode(
        self,
        llr: np.ndarray,
        *,
        message_state: Any = None,
        warm_state: Any = None,
    ) -> np.ndarray:
        if message_state is not None or warm_state is not None:
            raise AssertionError("decoder message/warm state reuse tripwire")
        tensor = self._torch.as_tensor(llr, dtype=self._torch.float32, device="cpu")
        tensor = self._torch.clamp(tensor, -20.0, 20.0)
        with self._torch.no_grad():
            decoded = self.decoder(tensor)
        if isinstance(decoded, tuple):
            decoded = decoded[0]
        return decoded.detach().cpu().numpy().astype(np.uint8, copy=False)


class D0Codec:
    """Lazy source-bound codec with a fresh-state decode contract."""

    llr_semantics = "positive_means_bit_1"
    demapper_preclip = 30.0
    decoder_llr_max = 20.0
    decoder_iterations = 20

    def __init__(self, contract: Any, backend_factory: Callable[..., Any] | None = None):
        if not isinstance(contract, D0Contract):
            raise TypeError("contract must be the frozen D0Contract type")
        assert_action_authorized("D0_TESTBED_IMPLEMENTATION", contract)
        code = contract.population.code
        if (
            code.family != "5g_ldpc_bg2"
            or code.information_bits_per_cw != 1024
            or code.transmitted_bits_per_cw != 1536
            or code.decoder_iterations != 20
        ):
            raise ValueError("D0 contract codec identity mismatch")
        self.contract = contract
        self._backend_factory = backend_factory
        self._backend: Any | None = None

    def _ensure_backend(self) -> Any:
        if self._backend is None:
            if self._backend_factory is None:
                self._backend = _SionnaBackend()
            else:
                self._backend = self._backend_factory(contract=self.contract)
        return self._backend

    @property
    def live_metadata(self) -> LiveCodecMetadata:
        backend = self._ensure_backend()
        metadata = getattr(backend, "metadata", None)
        if not isinstance(metadata, LiveCodecMetadata):
            raise RuntimeError("backend has no validated live codec metadata")
        return metadata

    @staticmethod
    def per_real_noise_power(complex_noise_power: float) -> float:
        if isinstance(complex_noise_power, (bool, np.bool_)):
            raise TypeError("complex noise power must not be boolean")
        value = float(complex_noise_power)
        if not np.isfinite(value) or value < 0.0:
            raise ValueError("complex noise power must be finite and non-negative")
        return value / 2.0

    def encode(self, info_bits: np.ndarray) -> np.ndarray:
        value = np.asarray(info_bits)
        if value.ndim != 2 or value.shape[1] != 1024:
            raise ValueError("info_bits must have shape [B,1024]")
        if not np.all((value == 0) | (value == 1)):
            raise ValueError("info_bits must be binary")
        coded = np.asarray(self._ensure_backend().encode(value.astype(np.uint8, copy=False)))
        if coded.shape != (value.shape[0], 1536) or not np.all((coded == 0) | (coded == 1)):
            raise RuntimeError("encoder returned an invalid coded-bit array")
        return coded.astype(np.uint8, copy=False)

    def demap(self, z: np.ndarray, *, complex_noise_power: float) -> np.ndarray:
        variance = self.per_real_noise_power(complex_noise_power)
        if variance <= 0.0:
            raise ValueError("complex noise power must be positive for soft demapping")
        symbols = np.asarray(z).reshape(-1)
        labels = np.arange(16, dtype=np.uint8)
        weights = np.array([8, 4, 2, 1], dtype=np.uint8)
        bits = ((labels[:, None] & weights) != 0).astype(np.uint8)
        constellation = gray16_map(bits)
        distance2 = np.abs(symbols[:, None] - constellation[None, :]) ** 2
        result = np.empty((symbols.size, 4), dtype=np.float64)
        scale = 1.0 / (2.0 * variance)
        for bit_index in range(4):
            zero = bits[:, bit_index] == 0
            min_zero = np.min(distance2[:, zero], axis=1)
            min_one = np.min(distance2[:, ~zero], axis=1)
            result[:, bit_index] = np.clip(
                (min_zero - min_one) * scale,
                -self.demapper_preclip,
                self.demapper_preclip,
            )
        return result.astype(np.float32).reshape(-1)

    def decode_fresh(
        self,
        llr_cw: np.ndarray,
        *,
        cw_ids: Sequence[str],
        candidate_id: str,
    ) -> DecodeBatch:
        llr = np.asarray(llr_cw, dtype=np.float64)
        if llr.shape != (16, 1536) or not np.all(np.isfinite(llr)):
            raise ValueError("llr_cw must be a finite exact (16,1536) array")
        ids = tuple(str(value) for value in cw_ids)
        if len(ids) != llr.shape[0] or len(set(ids)) != len(ids):
            raise ValueError("cw_ids must be unique and match the codeword batch")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValueError("candidate_id must be a non-empty string")
        preclipped = np.clip(llr, -self.demapper_preclip, self.demapper_preclip)
        info_bits = np.asarray(
            self._ensure_backend().decode(
                preclipped,
                message_state=None,
                warm_state=None,
            )
        )
        if info_bits.shape != (16, 1024):
            raise RuntimeError("decoder returned an invalid information-bit shape")
        dtype = info_bits.dtype
        if (
            dtype.hasobject
            or dtype.fields is not None
            or not (
                np.issubdtype(dtype, np.bool_)
                or np.issubdtype(dtype, np.integer)
                or np.issubdtype(dtype, np.floating)
            )
        ):
            raise TypeError("decoder hard output must use a plain real numeric or bool dtype")
        if not np.all(np.isfinite(info_bits)):
            raise RuntimeError("decoder hard output must be finite")
        if not np.all((info_bits == 0) | (info_bits == 1)):
            raise RuntimeError("decoder hard output must contain only binary values")
        hard_output = build_decoder_hard_output_ref(info_bits)
        return DecodeBatch(
            hard_output=hard_output,
            receipt=DecodeReceipt(
                cw_batch=llr.shape[0],
                restart=True,
                bp_iterations=self.decoder_iterations * llr.shape[0],
                truth_correction=False,
            ),
            cw_ids=ids,
            candidate_id=candidate_id,
        )

    @staticmethod
    def reencode_nll(c_hat: np.ndarray, llr: np.ndarray) -> float:
        coded = np.asarray(c_hat)
        channel_llr = np.asarray(llr, dtype=np.float64)
        if coded.shape != channel_llr.shape or coded.size == 0:
            raise ValueError("c_hat and llr must have the same non-empty shape")
        if not np.all((coded == 0) | (coded == 1)) or not np.all(np.isfinite(channel_llr)):
            raise ValueError("c_hat must be binary and llr must be finite")
        losses = np.logaddexp(0.0, (1.0 - 2.0 * coded) * channel_llr)
        return float(losses.mean())
