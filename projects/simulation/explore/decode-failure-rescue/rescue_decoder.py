"""Instrumented NOMS LDPC decoder for the decode-failure-rescue module.

ROUTE DECISION (probe 2026-09-20, sionna 2.0.1, torch 2.13.0+cpu)
-----------------------------------------------------------------
Sionna's ``LDPC5GDecoder`` supports exact single-iteration state stepping,
so this module uses Sionna itself as the decoding engine (no mirror):

* ``LDPCBPDecoder.call(llr_ch, num_iter, msg_v2c)`` accepts the decoder
  state (v2c edge messages) and, with ``return_state=True``, returns the
  post-iteration state
  (sionna/phy/fec/ldpc/decoding.py:837-910, LDPC5GDecoder.call:1571-1701).
* With flooding scheduling and no v2c/c2v callbacks (the frozen B0 config),
  every stateful quantity except ``msg_v2c`` is recomputed from scratch in
  each iteration: ``msg_c2v`` is fully overwritten by the flooding CN
  update (decoding.py:754-768) and ``x_hat`` by the VN update
  (decoding.py:777).  Chaining ``num_iter=1`` calls through the returned
  state is therefore *bit-exact* equal to one fresh ``num_iter=N`` call
  (probe-verified: 0/40-codeword mismatches on info and coded bits).
* The 5G wrapper rebuilds ``llr_5g`` deterministically from ``llr_ch`` on
  every call (decoding.py:1641-1667), so stepped continuation on the same
  frame reuses the identical internal channel vector.  State tensors have
  shape [batch, num_edges] and are engine-independent for a shared
  encoder, enabling
  - mid-run config switching (R3: (0.75,0.0) -> (0.875,0.1)), and
  - channel-LLR resets at transmitted positions (R2/O1) while keeping the
    message state hot.

INTERNAL COORDINATES (pruned pcm space; BG2, z=104, prune_pcm default)
----------------------------------------------------------------------
num_vns=1760, num_cns=720, num_edges=5360 (decoder.pcm property,
decoding.py:579; pruning at decoding.py:1487-1513):

* [0,1024)    information bits u (``u_hat = x_hat[:, :k]``); of these
              [0,208) is the 2z=208 punctured systematic prefix carried at
              channel LLR 0 (recovered only via extrinsic messages);
* [1024,1040) k_filler=16 filler bits at channel LLR -llr_max;
* [1040,1760) parity part surviving pcm pruning (``_n_pruned``=1760).

Rate recovery mirrored from decoding.py (encoder-side counterpart in
encoding.py: ``out_int``/``out_int_inv`` buffers, ``n_cb_comp``):

    llr_buf = llr_ch[:, out_int_inv]            (+zero pad; here none)
    llr_5g  = [0(2z) | llr_buf[:, :816] | -llr_max(16) | llr_buf[:, 816:1536]]
    x_no_filler = [x[:, :1024] | x[:, 1040:1760]]
    x_short     = x_no_filler[:, 208:208+1536]
    coded_hat (transmission order) = x_short[:, out_int]

The transmitted stream is [u[208:1024] | parity(720)] in de-interleaved
order; ``to_internal`` / ``from_internal`` below implement both directions
and are probe-verified against Sionna's own outputs (u_hat==u, x_short==c
on clean frames).

SYNDROME WEIGHT DEFINITION (frozen for this module)
---------------------------------------------------
``s_t`` = number of unsatisfied checks of the decoder's own pruned parity
check matrix ``H = engine.pcm`` evaluated on the internal full-codeword
hard decision ``x_hat_t`` (all 1760 VNs, including the punctured prefix
and filler columns):  ``s_t = ||(H x_hat_t) mod 2||_0``.

Rationale: ``H`` is exactly the constraint set the BP iteration enforces;
pruning only removed trailing degree-1 VN/CN pairs whose checks cannot be
violated.  ``s_t == 0`` iff ``x_hat_t`` is a codeword of the pruned code,
which is equivalent to re-encode consistency (probe-verified jointly on
clean frames: u_hat==u, x_short==c, s=0).  Weights are computed in the
internal (not 1536-transmitted) space so that untransmitted-but-constrained
variables (punctured prefix, filler) contribute exactly as the decoder
sees them.

Determinism: no RNG anywhere in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence

import numpy as np
import torch
from sionna.phy.fec.ldpc import LDPC5GEncoder, LDPC5GDecoder, cn_update_offset_minsum
from sionna.phy.fec.ldpc.decoding import LDPCBPDecoder


@dataclass(frozen=True)
class DecoderConfig:
    """Frozen NOMS configuration: alpha * cn_update_offset_minsum(offset)."""

    alpha: float = 0.75
    offset: float = 0.0

    def cn_update(self, msg_v2c, mask, llr_clipping=None):
        return self.alpha * cn_update_offset_minsum(
            msg_v2c, mask, llr_clipping, offset=self.offset
        )


B0_CONFIG = DecoderConfig(alpha=0.75, offset=0.0)
R3_CONFIG = DecoderConfig(alpha=0.875, offset=0.1)


class RescueDecoder:
    """Stateful stepping wrapper around Sionna NOMS BP decoding.

    One instance owns one frozen encoder (and its interleaver / pcm); the
    per-(alpha, offset) BP engines are built lazily and cached.  ``decode``
    may be called repeatedly on the same frame with ``state`` chained from
    the previous return value: that is the hot-continuation semantic
    (equivalent to a fresh longer run, correctness gate 2).
    """

    def __init__(
        self,
        encoder: LDPC5GEncoder,
        *,
        llr_max: float = 20.0,
        backend_input_clip: float = 20.0,
        device: str = "cpu",
        batch_size: int = 1,
    ) -> None:
        self.encoder = encoder
        self.llr_max = float(llr_max)
        self.backend_input_clip = float(backend_input_clip)
        self.device = device
        self.batch_size = int(batch_size)

        self._k = int(encoder.k)
        self._n = int(encoder.n)
        self._z = int(encoder.z)
        self._k_filler = int(encoder.k_filler)
        self._k_ldpc = int(encoder.k_ldpc)

        self._out_int = np.asarray(encoder.out_int.detach().cpu(), dtype=np.int64)
        self._out_int_inv = np.asarray(
            encoder.out_int_inv.detach().cpu(), dtype=np.int64
        )

        # engines: hard_out=True for stepping, hard_out=False twin for LLR view
        self._engines: dict[tuple[float, float], LDPC5GDecoder] = {}
        self._engines_soft: dict[tuple[float, float], LDPC5GDecoder] = {}

        # Probe engine only to fix the pruned geometry (decoding.py:1487-1513).
        probe = self._engine(B0_CONFIG)
        self._n_pruned = int(probe._n_pruned)
        self._nb_pruned = int(probe._nb_pruned_nodes)
        self._num_edges = int(probe.num_edges)
        self._buf_len = int(encoder.n_cb_comp) - self._nb_pruned

        pcm = probe.pcm.toarray().astype(np.uint8)
        if pcm.shape[1] != self._n_pruned:
            raise RuntimeError("pruned pcm width mismatch")
        self._pcm = pcm  # [num_cns, n_pruned] binary

        # internal position -> transmitted (de-interleaved) position or -1
        internal_to_tx = np.full(self._n_pruned, -1, dtype=np.int64)
        tx_pos = np.arange(self._n)
        nofill = np.concatenate(
            (np.arange(self._k), np.arange(self._k_ldpc, self._n_pruned))
        )
        raw_positions = nofill[2 * self._z : 2 * self._z + self._n]  # x_short order
        internal_to_tx[raw_positions] = tx_pos
        self._internal_to_tx = internal_to_tx
        self._tx_to_internal = raw_positions  # transmitted (de-int) -> internal
        self._raw_to_tx = self._out_int  # x_short raw idx -> transmission order

    # ------------------------------------------------------------------ #
    # engine construction
    # ------------------------------------------------------------------ #
    def _engine(self, config: DecoderConfig, *, soft: bool = False) -> LDPC5GDecoder:
        cache = self._engines_soft if soft else self._engines
        key = (config.alpha, config.offset)
        engine = cache.get(key)
        if engine is None:
            engine = LDPC5GDecoder(
                self.encoder,
                num_iter=1,
                cn_update=config.cn_update,
                hard_out=not soft,
                return_infobits=True,  # unused: base-class call is invoked directly
                llr_max=self.llr_max,
                return_state=True,
                device=self.device,
            )
            cache[key] = engine
        return engine

    # ------------------------------------------------------------------ #
    # coordinate mapping (mirrors decoding.py:1641-1667, 1687-1698)
    # ------------------------------------------------------------------ #
    def to_internal(self, llr: np.ndarray) -> torch.Tensor:
        """[B,1536] transmitted LLR -> [B,n_pruned] internal channel vector."""
        value = np.asarray(llr, dtype=np.float32)
        if value.ndim != 2 or value.shape[1] != self._n:
            raise ValueError("llr must have shape [B,1536]")
        value = np.clip(value, -self.backend_input_clip, self.backend_input_clip)
        deint = value[:, self._out_int_inv]
        if self._buf_len > self._n:
            deint = np.concatenate(
                (
                    deint,
                    np.zeros(
                        (deint.shape[0], self._buf_len - self._n), dtype=np.float32
                    ),
                ),
                axis=1,
            )
        llr_5g = np.concatenate(
            (
                np.zeros((deint.shape[0], 2 * self._z), dtype=np.float32),
                deint[:, : self._k - 2 * self._z],
                -self.llr_max
                * np.ones((deint.shape[0], self._k_filler), dtype=np.float32),
                deint[:, self._k - 2 * self._z :],
            ),
            axis=1,
        )
        if llr_5g.shape[1] != self._n_pruned:
            raise RuntimeError("internal channel vector length mismatch")
        return torch.as_tensor(llr_5g, dtype=torch.float32, device=self.device)

    def _hard_views(self, x_int: torch.Tensor) -> tuple[np.ndarray, np.ndarray]:
        """Internal hard bits -> (info_bits [B,k], coded_hat [B,n] tx order)."""
        xi = x_int.detach().cpu().numpy().astype(np.uint8)
        nofill = np.concatenate((xi[:, : self._k], xi[:, self._k_ldpc :]), axis=1)
        x_short = nofill[:, 2 * self._z : 2 * self._z + self._n]
        return xi[:, : self._k], x_short[:, self._raw_to_tx]

    def final_llr_tx(self, x_int_soft: torch.Tensor) -> np.ndarray:
        """Internal soft logits (positive=bit1) -> [B,1536] transmitted order."""
        xl = x_int_soft.detach().cpu().numpy().astype(np.float64)
        nofill = np.concatenate((xl[:, : self._k], xl[:, self._k_ldpc :]), axis=1)
        x_short = nofill[:, 2 * self._z : 2 * self._z + self._n]
        return x_short[:, self._raw_to_tx]

    def syndrome(self, x_int: torch.Tensor) -> np.ndarray:
        """Per-item syndrome weight ||(H x) mod 2||_0 on internal hard bits."""
        xi = x_int.detach().cpu().numpy().astype(np.uint8)
        # uint8 matmul overflow wraps at even moduli, preserving parity.
        parity = (xi @ self._pcm.T) % 2
        return parity.sum(axis=1).astype(np.int64)

    def unsat_variables_internal(self, x_int: torch.Tensor) -> list[np.ndarray]:
        """Internal VN indices touched by unsatisfied checks, per batch item."""
        xi = x_int.detach().cpu().numpy().astype(np.uint8)
        parity = (xi @ self._pcm.T) % 2
        out = []
        for row in parity:
            unsat_rows = np.flatnonzero(row)
            if unsat_rows.size == 0:
                out.append(np.empty(0, dtype=np.int64))
            else:
                touched = np.flatnonzero(self._pcm[unsat_rows].sum(axis=0))
                out.append(touched)
        return out

    def internal_positions_to_tx(self, internal: np.ndarray) -> np.ndarray:
        """Map internal VN positions to transmitted (channel-order) indices.

        internal -> x_short raw index q via ``_internal_to_tx``; the transmitted
        stream is ``x_short[:, out_int]``, so raw position q is carried at
        channel index ``out_int_inv[q]``.  The out_int_inv composition is the
        R030 fix: returning q directly made R2 rank/erase channel positions
        that belong to unrelated variables.
        """
        pos = np.asarray(internal, dtype=np.int64)
        raw = self._internal_to_tx[pos]
        raw = raw[raw >= 0]
        return self._out_int_inv[raw]

    # ------------------------------------------------------------------ #
    # main API
    # ------------------------------------------------------------------ #
    def decode(
        self,
        llr: np.ndarray,
        *,
        num_iter: int,
        alpha: float = 0.75,
        offset: float = 0.0,
        reset_positions: Optional[Sequence[int]] = None,
        trajectory: bool = True,
        state: Optional[torch.Tensor] = None,
        early_stop: bool = False,
        return_final_llr: bool = False,
    ) -> dict[str, Any]:
        """Run up to ``num_iter`` single NOMS iterations.

        Semantics:
        * ``state=None`` starts fresh (v2c init from the channel vector,
          matching a fresh Sionna call); passing the previous ``state``
          continues the same frame's decoding hot (bit-exact equal to a
          longer fresh run for an unmodified ``llr``).
        * ``reset_positions``: transmission-order indices whose *channel*
          LLR is set to 0 before this call (used by R2/O1); message state
          stays hot unless ``state`` is None.
        * ``early_stop``: stop the loop as soon as every batch item has hit
          syndrome 0 once (stage-2 acceptance rule); the accepted iterate
          is the one at the stopping iteration.

        Returns dict with keys:
          info_bits [B,k] uint8, coded_hat [B,n] uint8 (transmission order),
          syndrome_weights list[[int]*B] (per iteration, when trajectory),
          converged_at list[int|None] (first iteration with syndrome 0,
          counted within this call), final_syndrome [B],
          unsat_check_variables (internal VN index arrays, final iterate),
          state (torch.Tensor, None-safe for chaining),
          iterations_run int, final_llr [B,n] float64 or None.
        """
        config = DecoderConfig(alpha=float(alpha), offset=float(offset))
        value = np.array(llr, dtype=np.float32, copy=True)
        if value.ndim != 2 or value.shape[1] != self._n:
            raise ValueError("llr must have shape [B,1536]")
        if reset_positions is not None and len(reset_positions):
            pos = np.asarray(sorted(set(int(p) for p in reset_positions)), dtype=np.int64)
            if pos.size and (pos.min() < 0 or pos.max() >= self._n):
                raise ValueError("reset_positions out of range")
            value[:, pos] = 0.0
        llr_5g = self.to_internal(value)
        engine = self._engine(config)

        batch = value.shape[0]
        weights: list[list[int]] = [[] for _ in range(batch)]
        converged_at: list[Optional[int]] = [None] * batch
        x_int: Optional[torch.Tensor] = None
        prev_state = state
        run_state = state
        iterations_run = 0
        for it in range(1, int(num_iter) + 1):
            prev_state = run_state
            with torch.no_grad():
                x_int, run_state = LDPCBPDecoder.call(
                    engine, llr_5g, num_iter=1, msg_v2c=run_state
                )
            iterations_run = it
            if trajectory or early_stop:
                s = self.syndrome(x_int)
                for b in range(batch):
                    weights[b].append(int(s[b]))
                    if s[b] == 0 and converged_at[b] is None:
                        converged_at[b] = it
                if early_stop and np.all(s == 0):
                    break
        if x_int is None:
            raise ValueError("num_iter must be >= 1")

        info_bits, coded_hat = self._hard_views(x_int)
        final_syndrome = self.syndrome(x_int)
        unsat = (
            self.unsat_variables_internal(x_int)
            if np.any(final_syndrome > 0)
            else [np.empty(0, dtype=np.int64) for _ in range(batch)]
        )

        final_llr = None
        if return_final_llr:
            soft_engine = self._engine(config, soft=True)
            with torch.no_grad():
                x_soft, _ = LDPCBPDecoder.call(
                    soft_engine, llr_5g, num_iter=1, msg_v2c=prev_state
                )
            final_llr = self.final_llr_tx(x_soft)

        return {
            "info_bits": info_bits,
            "coded_hat": coded_hat,
            "syndrome_weights": weights,
            "converged_at": converged_at,
            "final_syndrome": final_syndrome,
            "unsat_check_variables": unsat,
            "state": run_state,
            "prev_state": prev_state,
            "iterations_run": iterations_run,
            "final_llr": final_llr,
        }

    # ------------------------------------------------------------------ #
    # reference single-shot decoders (correctness gates / T077 anchor)
    # ------------------------------------------------------------------ #
    def sionna_reference(
        self, llr: np.ndarray, *, num_iter: int, config: DecoderConfig = B0_CONFIG
    ) -> tuple[np.ndarray, np.ndarray]:
        """Fresh single-call Sionna decode (frozen B0 construction).

        Mirrors coded-decoder-feedback/codec.py:_SionnaBackend decoder
        construction (num_iter, cn_update=alpha*cn_update_offset_minsum,
        hard_out=True, return_infobits, llr_max=20, input clamp +-20).
        Returns (info_bits [B,k], coded_hat [B,n]) both uint8.
        """
        value = np.asarray(llr, dtype=np.float32)
        value = np.clip(value, -self.backend_input_clip, self.backend_input_clip)
        outputs = []
        for return_infobits in (True, False):
            dec = LDPC5GDecoder(
                self.encoder,
                num_iter=int(num_iter),
                cn_update=config.cn_update,
                hard_out=True,
                return_infobits=return_infobits,
                llr_max=self.llr_max,
                return_state=False,
                device=self.device,
            )
            tensor = torch.as_tensor(value, dtype=torch.float32, device=self.device)
            with torch.no_grad():
                out = dec(tensor)
            outputs.append(out.detach().cpu().numpy().astype(np.uint8))
        return outputs[0], outputs[1]


def make_encoder(*, k: int = 1024, n: int = 1536, num_bits_per_symbol: int = 4):
    """Frozen T077 encoder identity (codec.py:_SionnaBackend pins bg2/z=104)."""
    import sionna

    if sionna.__version__ != "2.0.1":
        raise RuntimeError(f"unsupported Sionna version: {sionna.__version__}")
    encoder = LDPC5GEncoder(
        k=k, n=n, num_bits_per_symbol=num_bits_per_symbol, device="cpu"
    )
    if (
        getattr(encoder, "_bg", None) != "bg2"
        or getattr(encoder, "_z", None) != 104
        or getattr(encoder, "_num_bits_per_symbol", None) != 4
    ):
        raise RuntimeError("live Sionna BG/Z/interleaver metadata mismatch")
    return encoder


def classify_failure(syndrome_weights: Sequence[int], info_errors: int) -> str:
    """Contract failure_classification (decode-failure-rescue/contract.yaml).

    converged_wrong: syndrome hit 0 within the 20 iterations but the final
                     information output != truth;
    stagnated:       s_16..s_20 all equal and > 0;
    oscillating:     last 8 iterations repeat a short period (2 or 3) cycle,
                     not all-equal, not strictly descending;
    descending:      last 8 iterations strictly decreasing, final value > 0;
    other:           everything else (incl. final syndrome 0 with wrong info
                     is impossible: syndrome 0 + wrong info is caught by
                     converged_wrong first).
    """
    w = [int(x) for x in syndrome_weights]
    if not w:
        return "other"
    if min(w) == 0 and info_errors > 0:
        return "converged_wrong"
    tail = w[-8:]
    if all(t == tail[0] for t in tail):
        return "stagnated" if tail[0] > 0 else "other"
    if all(tail[i + 1] < tail[i] for i in range(len(tail) - 1)):
        return "descending"
    for period in (2, 3):
        window = tail[-(2 * period):]
        if len(window) == 2 * period and all(
            window[i] == window[i + period] for i in range(period)
        ):
            return "oscillating"
    return "other"
